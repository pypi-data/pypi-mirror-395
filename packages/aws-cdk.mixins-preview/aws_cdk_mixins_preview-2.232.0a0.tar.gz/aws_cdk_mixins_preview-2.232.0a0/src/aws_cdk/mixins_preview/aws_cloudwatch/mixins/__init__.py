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
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAlarmMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions_enabled": "actionsEnabled",
        "alarm_actions": "alarmActions",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "comparison_operator": "comparisonOperator",
        "datapoints_to_alarm": "datapointsToAlarm",
        "dimensions": "dimensions",
        "evaluate_low_sample_count_percentile": "evaluateLowSampleCountPercentile",
        "evaluation_periods": "evaluationPeriods",
        "extended_statistic": "extendedStatistic",
        "insufficient_data_actions": "insufficientDataActions",
        "metric_name": "metricName",
        "metrics": "metrics",
        "namespace": "namespace",
        "ok_actions": "okActions",
        "period": "period",
        "statistic": "statistic",
        "tags": "tags",
        "threshold": "threshold",
        "threshold_metric_id": "thresholdMetricId",
        "treat_missing_data": "treatMissingData",
        "unit": "unit",
    },
)
class CfnAlarmMixinProps:
    def __init__(
        self,
        *,
        actions_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmPropsMixin.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        extended_statistic: typing.Optional[builtins.str] = None,
        insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric_name: typing.Optional[builtins.str] = None,
        metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmPropsMixin.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        namespace: typing.Optional[builtins.str] = None,
        ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        period: typing.Optional[jsii.Number] = None,
        statistic: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        threshold: typing.Optional[jsii.Number] = None,
        threshold_metric_id: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional[builtins.str] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAlarmPropsMixin.

        :param actions_enabled: Indicates whether actions should be executed during any changes to the alarm state. The default is TRUE. Default: - true
        :param alarm_actions: The list of actions to execute when this alarm transitions into an ALARM state from any other state. Specify each action as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutMetricAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param alarm_description: The description of the alarm.
        :param alarm_name: The name of the alarm. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the alarm name. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param comparison_operator: The arithmetic operation to use when comparing the specified statistic and threshold. The specified statistic value is used as the first operand.
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M, and the value that you set for ``EvaluationPeriods`` is the N value. For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* . If you omit this parameter, CloudWatch uses the same value here that you set for ``EvaluationPeriods`` , and the alarm goes to alarm state if that many consecutive periods are breaching.
        :param dimensions: The dimensions for the metric associated with the alarm. For an alarm based on a math expression, you can't specify ``Dimensions`` . Instead, you use ``Metrics`` .
        :param evaluate_low_sample_count_percentile: Used only for alarms based on percentiles. If ``ignore`` , the alarm state does not change during periods with too few data points to be statistically significant. If ``evaluate`` or this parameter is not used, the alarm is always evaluated and possibly changes state no matter how many data points are available.
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. If you are setting an alarm that requires that a number of consecutive data points be breaching to trigger the alarm, this value specifies that number. If you are setting an "M out of N" alarm, this value is the N, and ``DatapointsToAlarm`` is the M. For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* .
        :param extended_statistic: The percentile statistic for the metric associated with the alarm. Specify a value between p0.0 and p100. For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both. For an alarm based on a math expression, you can't specify ``ExtendedStatistic`` . Instead, you use ``Metrics`` .
        :param insufficient_data_actions: The actions to execute when this alarm transitions to the ``INSUFFICIENT_DATA`` state from any other state. Each action is specified as an Amazon Resource Name (ARN).
        :param metric_name: The name of the metric associated with the alarm. This is required for an alarm based on a metric. For an alarm based on a math expression, you use ``Metrics`` instead and you can't specify ``MetricName`` .
        :param metrics: An array that enables you to create an alarm based on the result of a metric math expression. Each item in the array either retrieves a metric or performs a math expression. If you specify the ``Metrics`` parameter, you cannot specify ``MetricName`` , ``Dimensions`` , ``Period`` , ``Namespace`` , ``Statistic`` , ``ExtendedStatistic`` , or ``Unit`` .
        :param namespace: The namespace of the metric associated with the alarm. This is required for an alarm based on a metric. For an alarm based on a math expression, you can't specify ``Namespace`` and you use ``Metrics`` instead. For a list of namespaces for metrics from AWS services, see `AWS Services That Publish CloudWatch Metrics. <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_
        :param ok_actions: The actions to execute when this alarm transitions to the ``OK`` state from any other state. Each action is specified as an Amazon Resource Name (ARN).
        :param period: The period, in seconds, over which the statistic is applied. This is required for an alarm based on a metric. Valid values are 10, 20, 30, 60, and any multiple of 60. For an alarm based on a math expression, you can't specify ``Period`` , and instead you use the ``Metrics`` parameter. *Minimum:* 10
        :param statistic: The statistic for the metric associated with the alarm, other than percentile. For percentile statistics, use ``ExtendedStatistic`` . For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both. For an alarm based on a math expression, you can't specify ``Statistic`` . Instead, you use ``Metrics`` .
        :param tags: A list of key-value pairs to associate with the alarm. You can associate as many as 50 tags with an alarm. To be able to associate tags with the alarm when you create the alarm, you must have the ``cloudwatch:TagResource`` permission. Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.
        :param threshold: The value to compare with the specified statistic.
        :param threshold_metric_id: In an alarm based on an anomaly detection model, this is the ID of the ``ANOMALY_DETECTION_BAND`` function used as the threshold for the alarm.
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Valid values are ``breaching`` , ``notBreaching`` , ``ignore`` , and ``missing`` . For more information, see `Configuring How CloudWatch Alarms Treat Missing Data <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarms-and-missing-data>`_ in the *Amazon CloudWatch User Guide* . If you omit this parameter, the default behavior of ``missing`` is used.
        :param unit: The unit of the metric associated with the alarm. Specify this only if you are creating an alarm based on a single metric. Do not specify this if you are specifying a ``Metrics`` array. You can specify the following values: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits, Terabits, Percent, Count, Bytes/Second, Kilobytes/Second, Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second, Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second, Count/Second, or None.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
            
            cfn_alarm_mixin_props = cloudwatch_mixins.CfnAlarmMixinProps(
                actions_enabled=False,
                alarm_actions=["alarmActions"],
                alarm_description="alarmDescription",
                alarm_name="alarmName",
                comparison_operator="comparisonOperator",
                datapoints_to_alarm=123,
                dimensions=[cloudwatch_mixins.CfnAlarmPropsMixin.DimensionProperty(
                    name="name",
                    value="value"
                )],
                evaluate_low_sample_count_percentile="evaluateLowSampleCountPercentile",
                evaluation_periods=123,
                extended_statistic="extendedStatistic",
                insufficient_data_actions=["insufficientDataActions"],
                metric_name="metricName",
                metrics=[cloudwatch_mixins.CfnAlarmPropsMixin.MetricDataQueryProperty(
                    account_id="accountId",
                    expression="expression",
                    id="id",
                    label="label",
                    metric_stat=cloudwatch_mixins.CfnAlarmPropsMixin.MetricStatProperty(
                        metric=cloudwatch_mixins.CfnAlarmPropsMixin.MetricProperty(
                            dimensions=[cloudwatch_mixins.CfnAlarmPropsMixin.DimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        period=123,
                        stat="stat",
                        unit="unit"
                    ),
                    period=123,
                    return_data=False
                )],
                namespace="namespace",
                ok_actions=["okActions"],
                period=123,
                statistic="statistic",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                threshold=123,
                threshold_metric_id="thresholdMetricId",
                treat_missing_data="treatMissingData",
                unit="unit"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b488250c806abadbacc97410fe1dd8e7394fff83b8a94c03b191b5dc3cad79b)
            check_type(argname="argument actions_enabled", value=actions_enabled, expected_type=type_hints["actions_enabled"])
            check_type(argname="argument alarm_actions", value=alarm_actions, expected_type=type_hints["alarm_actions"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument evaluate_low_sample_count_percentile", value=evaluate_low_sample_count_percentile, expected_type=type_hints["evaluate_low_sample_count_percentile"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument extended_statistic", value=extended_statistic, expected_type=type_hints["extended_statistic"])
            check_type(argname="argument insufficient_data_actions", value=insufficient_data_actions, expected_type=type_hints["insufficient_data_actions"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument ok_actions", value=ok_actions, expected_type=type_hints["ok_actions"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument threshold_metric_id", value=threshold_metric_id, expected_type=type_hints["threshold_metric_id"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if alarm_actions is not None:
            self._values["alarm_actions"] = alarm_actions
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if comparison_operator is not None:
            self._values["comparison_operator"] = comparison_operator
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if evaluate_low_sample_count_percentile is not None:
            self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if extended_statistic is not None:
            self._values["extended_statistic"] = extended_statistic
        if insufficient_data_actions is not None:
            self._values["insufficient_data_actions"] = insufficient_data_actions
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if metrics is not None:
            self._values["metrics"] = metrics
        if namespace is not None:
            self._values["namespace"] = namespace
        if ok_actions is not None:
            self._values["ok_actions"] = ok_actions
        if period is not None:
            self._values["period"] = period
        if statistic is not None:
            self._values["statistic"] = statistic
        if tags is not None:
            self._values["tags"] = tags
        if threshold is not None:
            self._values["threshold"] = threshold
        if threshold_metric_id is not None:
            self._values["threshold_metric_id"] = threshold_metric_id
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def actions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether actions should be executed during any changes to the alarm state.

        The default is TRUE.

        :default: - true

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-actionsenabled
        '''
        result = self._values.get("actions_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of actions to execute when this alarm transitions into an ALARM state from any other state.

        Specify each action as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutMetricAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-alarmactions
        '''
        result = self._values.get("alarm_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-alarmdescription
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The name of the alarm.

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the alarm name.
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-alarmname
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comparison_operator(self) -> typing.Optional[builtins.str]:
        '''The arithmetic operation to use when comparing the specified statistic and threshold.

        The specified statistic value is used as the first operand.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-comparisonoperator
        '''
        result = self._values.get("comparison_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of datapoints that must be breaching to trigger the alarm.

        This is used only if you are setting an "M out of N" alarm. In that case, this value is the M, and the value that you set for ``EvaluationPeriods`` is the N value. For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* .

        If you omit this parameter, CloudWatch uses the same value here that you set for ``EvaluationPeriods`` , and the alarm goes to alarm state if that many consecutive periods are breaching.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-datapointstoalarm
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmPropsMixin.DimensionProperty"]]]]:
        '''The dimensions for the metric associated with the alarm.

        For an alarm based on a math expression, you can't specify ``Dimensions`` . Instead, you use ``Metrics`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-dimensions
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmPropsMixin.DimensionProperty"]]]], result)

    @builtins.property
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[builtins.str]:
        '''Used only for alarms based on percentiles.

        If ``ignore`` , the alarm state does not change during periods with too few data points to be statistically significant. If ``evaluate`` or this parameter is not used, the alarm is always evaluated and possibly changes state no matter how many data points are available.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-evaluatelowsamplecountpercentile
        '''
        result = self._values.get("evaluate_low_sample_count_percentile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        If you are setting an alarm that requires that a number of consecutive data points be breaching to trigger the alarm, this value specifies that number. If you are setting an "M out of N" alarm, this value is the N, and ``DatapointsToAlarm`` is the M.

        For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-evaluationperiods
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def extended_statistic(self) -> typing.Optional[builtins.str]:
        '''The percentile statistic for the metric associated with the alarm. Specify a value between p0.0 and p100.

        For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both.

        For an alarm based on a math expression, you can't specify ``ExtendedStatistic`` . Instead, you use ``Metrics`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-extendedstatistic
        '''
        result = self._values.get("extended_statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insufficient_data_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the ``INSUFFICIENT_DATA`` state from any other state.

        Each action is specified as an Amazon Resource Name (ARN).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-insufficientdataactions
        '''
        result = self._values.get("insufficient_data_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric associated with the alarm.

        This is required for an alarm based on a metric. For an alarm based on a math expression, you use ``Metrics`` instead and you can't specify ``MetricName`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-metricname
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metrics(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmPropsMixin.MetricDataQueryProperty"]]]]:
        '''An array that enables you to create an alarm based on the result of a metric math expression.

        Each item in the array either retrieves a metric or performs a math expression.

        If you specify the ``Metrics`` parameter, you cannot specify ``MetricName`` , ``Dimensions`` , ``Period`` , ``Namespace`` , ``Statistic`` , ``ExtendedStatistic`` , or ``Unit`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-metrics
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmPropsMixin.MetricDataQueryProperty"]]]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the metric associated with the alarm.

        This is required for an alarm based on a metric. For an alarm based on a math expression, you can't specify ``Namespace`` and you use ``Metrics`` instead.

        For a list of namespaces for metrics from AWS services, see `AWS Services That Publish CloudWatch Metrics. <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the ``OK`` state from any other state.

        Each action is specified as an Amazon Resource Name (ARN).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-okactions
        '''
        result = self._values.get("ok_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def period(self) -> typing.Optional[jsii.Number]:
        '''The period, in seconds, over which the statistic is applied.

        This is required for an alarm based on a metric. Valid values are 10, 20, 30, 60, and any multiple of 60.

        For an alarm based on a math expression, you can't specify ``Period`` , and instead you use the ``Metrics`` parameter.

        *Minimum:* 10

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-period
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''The statistic for the metric associated with the alarm, other than percentile. For percentile statistics, use ``ExtendedStatistic`` .

        For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both.

        For an alarm based on a math expression, you can't specify ``Statistic`` . Instead, you use ``Metrics`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-statistic
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs to associate with the alarm.

        You can associate as many as 50 tags with an alarm. To be able to associate tags with the alarm when you create the alarm, you must have the ``cloudwatch:TagResource`` permission.

        Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value to compare with the specified statistic.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-threshold
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold_metric_id(self) -> typing.Optional[builtins.str]:
        '''In an alarm based on an anomaly detection model, this is the ID of the ``ANOMALY_DETECTION_BAND`` function used as the threshold for the alarm.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-thresholdmetricid
        '''
        result = self._values.get("threshold_metric_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def treat_missing_data(self) -> typing.Optional[builtins.str]:
        '''Sets how this alarm is to handle missing data points.

        Valid values are ``breaching`` , ``notBreaching`` , ``ignore`` , and ``missing`` . For more information, see `Configuring How CloudWatch Alarms Treat Missing Data <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarms-and-missing-data>`_ in the *Amazon CloudWatch User Guide* .

        If you omit this parameter, the default behavior of ``missing`` is used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-treatmissingdata
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''The unit of the metric associated with the alarm.

        Specify this only if you are creating an alarm based on a single metric. Do not specify this if you are specifying a ``Metrics`` array.

        You can specify the following values: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits, Terabits, Percent, Count, Bytes/Second, Kilobytes/Second, Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second, Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second, Count/Second, or None.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-unit
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlarmMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAlarmPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAlarmPropsMixin",
):
    '''The ``AWS::CloudWatch::Alarm`` type specifies an alarm and associates it with the specified metric or metric math expression.

    When this operation creates an alarm, the alarm state is immediately set to ``INSUFFICIENT_DATA`` . The alarm is then evaluated and its state is set appropriately. Any actions associated with the new state are then executed.

    When you update an existing alarm, its state is left unchanged, but the update completely overwrites the previous configuration of the alarm.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html
    :cloudformationResource: AWS::CloudWatch::Alarm
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
        
        cfn_alarm_props_mixin = cloudwatch_mixins.CfnAlarmPropsMixin(cloudwatch_mixins.CfnAlarmMixinProps(
            actions_enabled=False,
            alarm_actions=["alarmActions"],
            alarm_description="alarmDescription",
            alarm_name="alarmName",
            comparison_operator="comparisonOperator",
            datapoints_to_alarm=123,
            dimensions=[cloudwatch_mixins.CfnAlarmPropsMixin.DimensionProperty(
                name="name",
                value="value"
            )],
            evaluate_low_sample_count_percentile="evaluateLowSampleCountPercentile",
            evaluation_periods=123,
            extended_statistic="extendedStatistic",
            insufficient_data_actions=["insufficientDataActions"],
            metric_name="metricName",
            metrics=[cloudwatch_mixins.CfnAlarmPropsMixin.MetricDataQueryProperty(
                account_id="accountId",
                expression="expression",
                id="id",
                label="label",
                metric_stat=cloudwatch_mixins.CfnAlarmPropsMixin.MetricStatProperty(
                    metric=cloudwatch_mixins.CfnAlarmPropsMixin.MetricProperty(
                        dimensions=[cloudwatch_mixins.CfnAlarmPropsMixin.DimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        namespace="namespace"
                    ),
                    period=123,
                    stat="stat",
                    unit="unit"
                ),
                period=123,
                return_data=False
            )],
            namespace="namespace",
            ok_actions=["okActions"],
            period=123,
            statistic="statistic",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            threshold=123,
            threshold_metric_id="thresholdMetricId",
            treat_missing_data="treatMissingData",
            unit="unit"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAlarmMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudWatch::Alarm``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__343d3a7244cfdd02b43743a4fde04969313158d8b843b7e4697dd63ac45a8483)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84b5d80090a3a2c800531e93edb14f17def89eeabf51433c280e98acee19dde4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3adc0535a2f1874b04f5c63909e1303e3fefcc2fd42074796e675410d7bae97b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAlarmMixinProps:
        return typing.cast(CfnAlarmMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAlarmPropsMixin.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class DimensionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Dimension is an embedded property of the ``AWS::CloudWatch::Alarm`` type.

            Dimensions are name/value pairs that can be associated with a CloudWatch metric. You can specify a maximum of 30 dimensions for a given metric.

            :param name: The name of the dimension, from 1–255 characters in length. This dimension name must have been included when the metric was published.
            :param value: The value for the dimension, from 1–255 characters in length.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                dimension_property = cloudwatch_mixins.CfnAlarmPropsMixin.DimensionProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e566726e76eac48e5e384233e24b0ffc4417e864c4d41a41f42df2a0cf624b33)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the dimension, from 1–255 characters in length.

            This dimension name must have been included when the metric was published.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-dimension.html#cfn-cloudwatch-alarm-dimension-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the dimension, from 1–255 characters in length.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-dimension.html#cfn-cloudwatch-alarm-dimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAlarmPropsMixin.MetricDataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "expression": "expression",
            "id": "id",
            "label": "label",
            "metric_stat": "metricStat",
            "period": "period",
            "return_data": "returnData",
        },
    )
    class MetricDataQueryProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            expression: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            label: typing.Optional[builtins.str] = None,
            metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmPropsMixin.MetricStatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            period: typing.Optional[jsii.Number] = None,
            return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The ``MetricDataQuery`` property type specifies the metric data to return, and whether this call is just retrieving a batch set of data for one metric, or is performing a math expression on metric data.

            Any expression used must return a single time series. For more information, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* .

            :param account_id: The ID of the account where the metrics are located, if this is a cross-account alarm.
            :param expression: The math expression to be performed on the returned data, if this object is performing a math expression. This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. For more information about metric math expressions, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* . Within each MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.
            :param id: A short name used to tie this object to the results in the response. This name must be unique within a single call to ``GetMetricData`` . If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscore. The first character must be a lowercase letter.
            :param label: A human-readable label for this metric or expression. This is especially useful if this is an expression, so that you know what the value represents. If the metric or expression is shown in a CloudWatch dashboard widget, the label is shown. If ``Label`` is omitted, CloudWatch generates a default.
            :param metric_stat: The metric to be returned, along with statistics, period, and units. Use this parameter only if this object is retrieving a metric and not performing a math expression on returned data. Within one MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.
            :param period: The granularity, in seconds, of the returned data points. For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 20, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` operation that includes a ``StorageResolution of 1 second`` .
            :param return_data: This option indicates whether to return the timestamps and raw data values of this metric. When you create an alarm based on a metric math expression, specify ``True`` for this value for only the one math expression that the alarm is based on. You must specify ``False`` for ``ReturnData`` for all the other metrics and expressions used in the alarm. This field is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_data_query_property = cloudwatch_mixins.CfnAlarmPropsMixin.MetricDataQueryProperty(
                    account_id="accountId",
                    expression="expression",
                    id="id",
                    label="label",
                    metric_stat=cloudwatch_mixins.CfnAlarmPropsMixin.MetricStatProperty(
                        metric=cloudwatch_mixins.CfnAlarmPropsMixin.MetricProperty(
                            dimensions=[cloudwatch_mixins.CfnAlarmPropsMixin.DimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        period=123,
                        stat="stat",
                        unit="unit"
                    ),
                    period=123,
                    return_data=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8cf7b0e5ce11ffdc8705522d5cb6b4d26f3e7d2ad1324e12d953167e44701e1)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if expression is not None:
                self._values["expression"] = expression
            if id is not None:
                self._values["id"] = id
            if label is not None:
                self._values["label"] = label
            if metric_stat is not None:
                self._values["metric_stat"] = metric_stat
            if period is not None:
                self._values["period"] = period
            if return_data is not None:
                self._values["return_data"] = return_data

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the account where the metrics are located, if this is a cross-account alarm.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The math expression to be performed on the returned data, if this object is performing a math expression.

            This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. For more information about metric math expressions, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* .

            Within each MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A short name used to tie this object to the results in the response.

            This name must be unique within a single call to ``GetMetricData`` . If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscore. The first character must be a lowercase letter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''A human-readable label for this metric or expression.

            This is especially useful if this is an expression, so that you know what the value represents. If the metric or expression is shown in a CloudWatch dashboard widget, the label is shown. If ``Label`` is omitted, CloudWatch generates a default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_stat(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmPropsMixin.MetricStatProperty"]]:
            '''The metric to be returned, along with statistics, period, and units.

            Use this parameter only if this object is retrieving a metric and not performing a math expression on returned data.

            Within one MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-metricstat
            '''
            result = self._values.get("metric_stat")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmPropsMixin.MetricStatProperty"]], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The granularity, in seconds, of the returned data points.

            For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 20, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` operation that includes a ``StorageResolution of 1 second`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def return_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This option indicates whether to return the timestamps and raw data values of this metric.

            When you create an alarm based on a metric math expression, specify ``True`` for this value for only the one math expression that the alarm is based on. You must specify ``False`` for ``ReturnData`` for all the other metrics and expressions used in the alarm.

            This field is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-returndata
            '''
            result = self._values.get("return_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAlarmPropsMixin.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "namespace": "namespace",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmPropsMixin.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Metric`` property type represents a specific metric.

            ``Metric`` is a property of the `MetricStat <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html>`_ property type.

            :param dimensions: The metric dimensions that you want to be used for the metric that the alarm will watch.
            :param metric_name: The name of the metric that you want the alarm to watch. This is a required field.
            :param namespace: The namespace of the metric that the alarm will watch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_property = cloudwatch_mixins.CfnAlarmPropsMixin.MetricProperty(
                    dimensions=[cloudwatch_mixins.CfnAlarmPropsMixin.DimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e83b20a6531e2706341516bd09f926d8b4a4199c847e6aa7668ab1b3bfa7771)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmPropsMixin.DimensionProperty"]]]]:
            '''The metric dimensions that you want to be used for the metric that the alarm will watch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmPropsMixin.DimensionProperty"]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric that you want the alarm to watch.

            This is a required field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric that the alarm will watch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAlarmPropsMixin.MetricStatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric": "metric",
            "period": "period",
            "stat": "stat",
            "unit": "unit",
        },
    )
    class MetricStatProperty:
        def __init__(
            self,
            *,
            metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmPropsMixin.MetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            period: typing.Optional[jsii.Number] = None,
            stat: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines the metric to be returned, along with the statistics, period, and units.

            ``MetricStat`` is a property of the `MetricDataQuery <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html>`_ property type.

            :param metric: The metric to return, including the metric name, namespace, and dimensions.
            :param period: The granularity, in seconds, of the returned data points. For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 20, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` call that includes a ``StorageResolution`` of 1 second. If the ``StartTime`` parameter specifies a time stamp that is greater than 3 hours ago, you must specify the period as follows or no data points in that time range is returned: - Start time between 3 hours and 15 days ago - Use a multiple of 60 seconds (1 minute). - Start time between 15 and 63 days ago - Use a multiple of 300 seconds (5 minutes). - Start time greater than 63 days ago - Use a multiple of 3600 seconds (1 hour).
            :param stat: The statistic to return. It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* .
            :param unit: The unit to use for the returned data points. Valid values are: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits, Terabits, Percent, Count, Bytes/Second, Kilobytes/Second, Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second, Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second, Count/Second, or None.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_stat_property = cloudwatch_mixins.CfnAlarmPropsMixin.MetricStatProperty(
                    metric=cloudwatch_mixins.CfnAlarmPropsMixin.MetricProperty(
                        dimensions=[cloudwatch_mixins.CfnAlarmPropsMixin.DimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        namespace="namespace"
                    ),
                    period=123,
                    stat="stat",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ddd062229b7b3bc664dfcd5ed204b7c2920c2eacc08b996aa32b378536586c38)
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric is not None:
                self._values["metric"] = metric
            if period is not None:
                self._values["period"] = period
            if stat is not None:
                self._values["stat"] = stat
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmPropsMixin.MetricProperty"]]:
            '''The metric to return, including the metric name, namespace, and dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-metric
            '''
            result = self._values.get("metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmPropsMixin.MetricProperty"]], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The granularity, in seconds, of the returned data points.

            For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 20, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` call that includes a ``StorageResolution`` of 1 second.

            If the ``StartTime`` parameter specifies a time stamp that is greater than 3 hours ago, you must specify the period as follows or no data points in that time range is returned:

            - Start time between 3 hours and 15 days ago - Use a multiple of 60 seconds (1 minute).
            - Start time between 15 and 63 days ago - Use a multiple of 300 seconds (5 minutes).
            - Start time greater than 63 days ago - Use a multiple of 3600 seconds (1 hour).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stat(self) -> typing.Optional[builtins.str]:
            '''The statistic to return.

            It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-stat
            '''
            result = self._values.get("stat")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit to use for the returned data points.

            Valid values are: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits, Terabits, Percent, Count, Bytes/Second, Kilobytes/Second, Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second, Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second, Count/Second, or None.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "dimensions": "dimensions",
        "metric_characteristics": "metricCharacteristics",
        "metric_math_anomaly_detector": "metricMathAnomalyDetector",
        "metric_name": "metricName",
        "namespace": "namespace",
        "single_metric_anomaly_detector": "singleMetricAnomalyDetector",
        "stat": "stat",
    },
)
class CfnAnomalyDetectorMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        metric_characteristics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.MetricCharacteristicsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metric_math_anomaly_detector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.MetricMathAnomalyDetectorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metric_name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        single_metric_anomaly_detector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.SingleMetricAnomalyDetectorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stat: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAnomalyDetectorPropsMixin.

        :param configuration: Specifies details about how the anomaly detection model is to be trained, including time ranges to exclude when training and updating the model. The configuration can also include the time zone to use for the metric.
        :param dimensions: The dimensions of the metric associated with the anomaly detection band.
        :param metric_characteristics: Use this object to include parameters to provide information about your metric to CloudWatch to help it build more accurate anomaly detection models. Currently, it includes the ``PeriodicSpikes`` parameter.
        :param metric_math_anomaly_detector: The CloudWatch metric math expression for this anomaly detector.
        :param metric_name: The name of the metric associated with the anomaly detection band.
        :param namespace: The namespace of the metric associated with the anomaly detection band.
        :param single_metric_anomaly_detector: The CloudWatch metric and statistic for this anomaly detector.
        :param stat: The statistic of the metric associated with the anomaly detection band.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
            
            cfn_anomaly_detector_mixin_props = cloudwatch_mixins.CfnAnomalyDetectorMixinProps(
                configuration=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.ConfigurationProperty(
                    excluded_time_ranges=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.RangeProperty(
                        end_time="endTime",
                        start_time="startTime"
                    )],
                    metric_time_zone="metricTimeZone"
                ),
                dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                    name="name",
                    value="value"
                )],
                metric_characteristics=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricCharacteristicsProperty(
                    periodic_spikes=False
                ),
                metric_math_anomaly_detector=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricMathAnomalyDetectorProperty(
                    metric_data_queries=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricDataQueryProperty(
                        account_id="accountId",
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricStatProperty(
                            metric=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricProperty(
                                dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            period=123,
                            stat="stat",
                            unit="unit"
                        ),
                        period=123,
                        return_data=False
                    )]
                ),
                metric_name="metricName",
                namespace="namespace",
                single_metric_anomaly_detector=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.SingleMetricAnomalyDetectorProperty(
                    account_id="accountId",
                    dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace",
                    stat="stat"
                ),
                stat="stat"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ecba4636969c85aeee29cc6948ace6e56a281231555a9705d6decf5206caadc)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument metric_characteristics", value=metric_characteristics, expected_type=type_hints["metric_characteristics"])
            check_type(argname="argument metric_math_anomaly_detector", value=metric_math_anomaly_detector, expected_type=type_hints["metric_math_anomaly_detector"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument single_metric_anomaly_detector", value=single_metric_anomaly_detector, expected_type=type_hints["single_metric_anomaly_detector"])
            check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if metric_characteristics is not None:
            self._values["metric_characteristics"] = metric_characteristics
        if metric_math_anomaly_detector is not None:
            self._values["metric_math_anomaly_detector"] = metric_math_anomaly_detector
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if namespace is not None:
            self._values["namespace"] = namespace
        if single_metric_anomaly_detector is not None:
            self._values["single_metric_anomaly_detector"] = single_metric_anomaly_detector
        if stat is not None:
            self._values["stat"] = stat

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.ConfigurationProperty"]]:
        '''Specifies details about how the anomaly detection model is to be trained, including time ranges to exclude when training and updating the model.

        The configuration can also include the time zone to use for the metric.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.ConfigurationProperty"]], result)

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.DimensionProperty"]]]]:
        '''The dimensions of the metric associated with the anomaly detection band.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-dimensions
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.DimensionProperty"]]]], result)

    @builtins.property
    def metric_characteristics(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricCharacteristicsProperty"]]:
        '''Use this object to include parameters to provide information about your metric to CloudWatch to help it build more accurate anomaly detection models.

        Currently, it includes the ``PeriodicSpikes`` parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metriccharacteristics
        '''
        result = self._values.get("metric_characteristics")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricCharacteristicsProperty"]], result)

    @builtins.property
    def metric_math_anomaly_detector(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricMathAnomalyDetectorProperty"]]:
        '''The CloudWatch metric math expression for this anomaly detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metricmathanomalydetector
        '''
        result = self._values.get("metric_math_anomaly_detector")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricMathAnomalyDetectorProperty"]], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric associated with the anomaly detection band.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metricname
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the metric associated with the anomaly detection band.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_metric_anomaly_detector(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.SingleMetricAnomalyDetectorProperty"]]:
        '''The CloudWatch metric and statistic for this anomaly detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector
        '''
        result = self._values.get("single_metric_anomaly_detector")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.SingleMetricAnomalyDetectorProperty"]], result)

    @builtins.property
    def stat(self) -> typing.Optional[builtins.str]:
        '''The statistic of the metric associated with the anomaly detection band.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-stat
        '''
        result = self._values.get("stat")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnomalyDetectorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAnomalyDetectorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorPropsMixin",
):
    '''The ``AWS::CloudWatch::AnomalyDetector`` type specifies an anomaly detection band for a certain metric and statistic.

    The band represents the expected "normal" range for the metric values. Anomaly detection bands can be used for visualization of a metric's expected values, and for alarms.

    For more information see `Using CloudWatch anomaly detection. <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html
    :cloudformationResource: AWS::CloudWatch::AnomalyDetector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
        
        cfn_anomaly_detector_props_mixin = cloudwatch_mixins.CfnAnomalyDetectorPropsMixin(cloudwatch_mixins.CfnAnomalyDetectorMixinProps(
            configuration=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.ConfigurationProperty(
                excluded_time_ranges=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.RangeProperty(
                    end_time="endTime",
                    start_time="startTime"
                )],
                metric_time_zone="metricTimeZone"
            ),
            dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                name="name",
                value="value"
            )],
            metric_characteristics=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricCharacteristicsProperty(
                periodic_spikes=False
            ),
            metric_math_anomaly_detector=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricMathAnomalyDetectorProperty(
                metric_data_queries=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricDataQueryProperty(
                    account_id="accountId",
                    expression="expression",
                    id="id",
                    label="label",
                    metric_stat=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricStatProperty(
                        metric=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricProperty(
                            dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        period=123,
                        stat="stat",
                        unit="unit"
                    ),
                    period=123,
                    return_data=False
                )]
            ),
            metric_name="metricName",
            namespace="namespace",
            single_metric_anomaly_detector=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.SingleMetricAnomalyDetectorProperty(
                account_id="accountId",
                dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                    name="name",
                    value="value"
                )],
                metric_name="metricName",
                namespace="namespace",
                stat="stat"
            ),
            stat="stat"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAnomalyDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudWatch::AnomalyDetector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0383645e7aa5da97e96df45f86f3716887fc5c6779b891c48368e99f5a60a1b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aac4fce888ec7125836002a82c931a552c12f7924b5c50c661e1bc77e682282a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d274c369e27c704dd46beec3f9dfdd88a472b13ab9b134761842e222f969db)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAnomalyDetectorMixinProps:
        return typing.cast(CfnAnomalyDetectorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorPropsMixin.ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "excluded_time_ranges": "excludedTimeRanges",
            "metric_time_zone": "metricTimeZone",
        },
    )
    class ConfigurationProperty:
        def __init__(
            self,
            *,
            excluded_time_ranges: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.RangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies details about how the anomaly detection model is to be trained, including time ranges to exclude when training and updating the model.

            The configuration can also include the time zone to use for the metric.

            :param excluded_time_ranges: Specifies an array of time ranges to exclude from use when the anomaly detection model is trained and updated. Use this to make sure that events that could cause unusual values for the metric, such as deployments, aren't used when CloudWatch creates or updates the model.
            :param metric_time_zone: The time zone to use for the metric. This is useful to enable the model to automatically account for daylight savings time changes if the metric is sensitive to such time changes. To specify a time zone, use the name of the time zone as specified in the standard tz database. For more information, see `tz database <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Tz_database>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                configuration_property = cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.ConfigurationProperty(
                    excluded_time_ranges=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.RangeProperty(
                        end_time="endTime",
                        start_time="startTime"
                    )],
                    metric_time_zone="metricTimeZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea215bb0479410afd8fece46dc08fbd12361c855f9e93f57b9d4f1b03363d1bb)
                check_type(argname="argument excluded_time_ranges", value=excluded_time_ranges, expected_type=type_hints["excluded_time_ranges"])
                check_type(argname="argument metric_time_zone", value=metric_time_zone, expected_type=type_hints["metric_time_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excluded_time_ranges is not None:
                self._values["excluded_time_ranges"] = excluded_time_ranges
            if metric_time_zone is not None:
                self._values["metric_time_zone"] = metric_time_zone

        @builtins.property
        def excluded_time_ranges(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.RangeProperty"]]]]:
            '''Specifies an array of time ranges to exclude from use when the anomaly detection model is trained and updated.

            Use this to make sure that events that could cause unusual values for the metric, such as deployments, aren't used when CloudWatch creates or updates the model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html#cfn-cloudwatch-anomalydetector-configuration-excludedtimeranges
            '''
            result = self._values.get("excluded_time_ranges")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.RangeProperty"]]]], result)

        @builtins.property
        def metric_time_zone(self) -> typing.Optional[builtins.str]:
            '''The time zone to use for the metric.

            This is useful to enable the model to automatically account for daylight savings time changes if the metric is sensitive to such time changes.

            To specify a time zone, use the name of the time zone as specified in the standard tz database. For more information, see `tz database <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Tz_database>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html#cfn-cloudwatch-anomalydetector-configuration-metrictimezone
            '''
            result = self._values.get("metric_time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class DimensionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A dimension is a name/value pair that is part of the identity of a metric.

            Because dimensions are part of the unique identifier for a metric, whenever you add a unique name/value pair to one of your metrics, you are creating a new variation of that metric. For example, many Amazon EC2 metrics publish ``InstanceId`` as a dimension name, and the actual instance ID as the value for that dimension.

            You can assign up to 30 dimensions to a metric.

            :param name: The name of the dimension.
            :param value: The value of the dimension. Dimension values must contain only ASCII characters and must include at least one non-whitespace character. ASCII control characters are not supported as part of dimension values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                dimension_property = cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8736477fa6691e4b5b7e65f5f392fb2a4c7f4054fd6df1786e7aba5795d9a504)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html#cfn-cloudwatch-anomalydetector-dimension-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the dimension.

            Dimension values must contain only ASCII characters and must include at least one non-whitespace character. ASCII control characters are not supported as part of dimension values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html#cfn-cloudwatch-anomalydetector-dimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorPropsMixin.MetricCharacteristicsProperty",
        jsii_struct_bases=[],
        name_mapping={"periodic_spikes": "periodicSpikes"},
    )
    class MetricCharacteristicsProperty:
        def __init__(
            self,
            *,
            periodic_spikes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''This object includes parameters that you can use to provide information to CloudWatch to help it build more accurate anomaly detection models.

            :param periodic_spikes: Set this parameter to true if values for this metric consistently include spikes that should not be considered to be anomalies. With this set to true, CloudWatch will expect to see spikes that occurred consistently during the model training period, and won't flag future similar spikes as anomalies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metriccharacteristics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_characteristics_property = cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricCharacteristicsProperty(
                    periodic_spikes=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bafa2caed05e2e444fbd3a80ef54672b78ded63c503fdcb3e6446d004d160cd0)
                check_type(argname="argument periodic_spikes", value=periodic_spikes, expected_type=type_hints["periodic_spikes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if periodic_spikes is not None:
                self._values["periodic_spikes"] = periodic_spikes

        @builtins.property
        def periodic_spikes(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this parameter to true if values for this metric consistently include spikes that should not be considered to be anomalies.

            With this set to true, CloudWatch will expect to see spikes that occurred consistently during the model training period, and won't flag future similar spikes as anomalies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metriccharacteristics.html#cfn-cloudwatch-anomalydetector-metriccharacteristics-periodicspikes
            '''
            result = self._values.get("periodic_spikes")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricCharacteristicsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorPropsMixin.MetricDataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "expression": "expression",
            "id": "id",
            "label": "label",
            "metric_stat": "metricStat",
            "period": "period",
            "return_data": "returnData",
        },
    )
    class MetricDataQueryProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            expression: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            label: typing.Optional[builtins.str] = None,
            metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.MetricStatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            period: typing.Optional[jsii.Number] = None,
            return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''This structure is used in both ``GetMetricData`` and ``PutMetricAlarm`` .

            The supported use of this structure is different for those two operations.

            When used in ``GetMetricData`` , it indicates the metric data to return, and whether this call is just retrieving a batch set of data for one metric, or is performing a Metrics Insights query or a math expression. A single ``GetMetricData`` call can include up to 500 ``MetricDataQuery`` structures.

            When used in ``PutMetricAlarm`` , it enables you to create an alarm based on a metric math expression. Each ``MetricDataQuery`` in the array specifies either a metric to retrieve, or a math expression to be performed on retrieved metrics. A single ``PutMetricAlarm`` call can include up to 20 ``MetricDataQuery`` structures in the array. The 20 structures can include as many as 10 structures that contain a ``MetricStat`` parameter to retrieve a metric, and as many as 10 structures that contain the ``Expression`` parameter to perform a math expression. Of those ``Expression`` structures, one must have ``true`` as the value for ``ReturnData`` . The result of this expression is the value the alarm watches.

            Any expression used in a ``PutMetricAlarm`` operation must return a single time series. For more information, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* .

            Some of the parameters of this structure also have different uses whether you are using this structure in a ``GetMetricData`` operation or a ``PutMetricAlarm`` operation. These differences are explained in the following parameter list.

            :param account_id: The ID of the account where the metrics are located. If you are performing a ``GetMetricData`` operation in a monitoring account, use this to specify which account to retrieve this metric from. If you are performing a ``PutMetricAlarm`` operation, use this to specify which account contains the metric that the alarm is watching.
            :param expression: This field can contain either a Metrics Insights query, or a metric math expression to be performed on the returned data. For more information about Metrics Insights queries, see `Metrics Insights query components and syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-metrics-insights-querylanguage>`_ in the *Amazon CloudWatch User Guide* . A math expression can use the ``Id`` of the other metrics or queries to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. For more information about metric math expressions, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* . Within each MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.
            :param id: A short name used to tie this object to the results in the response. This name must be unique within a single call to ``GetMetricData`` . If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscore. The first character must be a lowercase letter.
            :param label: A human-readable label for this metric or expression. This is especially useful if this is an expression, so that you know what the value represents. If the metric or expression is shown in a CloudWatch dashboard widget, the label is shown. If Label is omitted, CloudWatch generates a default. You can put dynamic expressions into a label, so that it is more descriptive. For more information, see `Using Dynamic Labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ .
            :param metric_stat: The metric to be returned, along with statistics, period, and units. Use this parameter only if this object is retrieving a metric and not performing a math expression on returned data. Within one MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.
            :param period: The granularity, in seconds, of the returned data points. For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 20, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` operation that includes a ``StorageResolution of 1 second`` .
            :param return_data: When used in ``GetMetricData`` , this option indicates whether to return the timestamps and raw data values of this metric. If you are performing this call just to do math expressions and do not also need the raw data returned, you can specify ``false`` . If you omit this, the default of ``true`` is used. When used in ``PutMetricAlarm`` , specify ``true`` for the one expression result to use as the alarm. For all other metrics and expressions in the same ``PutMetricAlarm`` operation, specify ``ReturnData`` as False.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_data_query_property = cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricDataQueryProperty(
                    account_id="accountId",
                    expression="expression",
                    id="id",
                    label="label",
                    metric_stat=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricStatProperty(
                        metric=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricProperty(
                            dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        period=123,
                        stat="stat",
                        unit="unit"
                    ),
                    period=123,
                    return_data=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ea68a68069eb87d7e212651a19ce11de383b941541cad00ba521c611a6325d1)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if expression is not None:
                self._values["expression"] = expression
            if id is not None:
                self._values["id"] = id
            if label is not None:
                self._values["label"] = label
            if metric_stat is not None:
                self._values["metric_stat"] = metric_stat
            if period is not None:
                self._values["period"] = period
            if return_data is not None:
                self._values["return_data"] = return_data

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the account where the metrics are located.

            If you are performing a ``GetMetricData`` operation in a monitoring account, use this to specify which account to retrieve this metric from.

            If you are performing a ``PutMetricAlarm`` operation, use this to specify which account contains the metric that the alarm is watching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''This field can contain either a Metrics Insights query, or a metric math expression to be performed on the returned data.

            For more information about Metrics Insights queries, see `Metrics Insights query components and syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-metrics-insights-querylanguage>`_ in the *Amazon CloudWatch User Guide* .

            A math expression can use the ``Id`` of the other metrics or queries to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. For more information about metric math expressions, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* .

            Within each MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A short name used to tie this object to the results in the response.

            This name must be unique within a single call to ``GetMetricData`` . If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscore. The first character must be a lowercase letter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''A human-readable label for this metric or expression.

            This is especially useful if this is an expression, so that you know what the value represents. If the metric or expression is shown in a CloudWatch dashboard widget, the label is shown. If Label is omitted, CloudWatch generates a default.

            You can put dynamic expressions into a label, so that it is more descriptive. For more information, see `Using Dynamic Labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_stat(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricStatProperty"]]:
            '''The metric to be returned, along with statistics, period, and units.

            Use this parameter only if this object is retrieving a metric and not performing a math expression on returned data.

            Within one MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-metricstat
            '''
            result = self._values.get("metric_stat")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricStatProperty"]], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The granularity, in seconds, of the returned data points.

            For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 20, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` operation that includes a ``StorageResolution of 1 second`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def return_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When used in ``GetMetricData`` , this option indicates whether to return the timestamps and raw data values of this metric.

            If you are performing this call just to do math expressions and do not also need the raw data returned, you can specify ``false`` . If you omit this, the default of ``true`` is used.

            When used in ``PutMetricAlarm`` , specify ``true`` for the one expression result to use as the alarm. For all other metrics and expressions in the same ``PutMetricAlarm`` operation, specify ``ReturnData`` as False.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-returndata
            '''
            result = self._values.get("return_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorPropsMixin.MetricMathAnomalyDetectorProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_data_queries": "metricDataQueries"},
    )
    class MetricMathAnomalyDetectorProperty:
        def __init__(
            self,
            *,
            metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Indicates the CloudWatch math expression that provides the time series the anomaly detector uses as input.

            The designated math expression must return a single time series.

            :param metric_data_queries: An array of metric data query structures that enables you to create an anomaly detector based on the result of a metric math expression. Each item in ``MetricDataQueries`` gets a metric or performs a math expression. One item in ``MetricDataQueries`` is the expression that provides the time series that the anomaly detector uses as input. Designate the expression by setting ``ReturnData`` to ``true`` for this object in the array. For all other expressions and metrics, set ``ReturnData`` to ``false`` . The designated expression must return a single time series.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricmathanomalydetector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_math_anomaly_detector_property = cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricMathAnomalyDetectorProperty(
                    metric_data_queries=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricDataQueryProperty(
                        account_id="accountId",
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricStatProperty(
                            metric=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricProperty(
                                dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            period=123,
                            stat="stat",
                            unit="unit"
                        ),
                        period=123,
                        return_data=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ee8d8cee3ffdaed4e0144b73386be621df864348fc024e1e2e48faa0e640561)
                check_type(argname="argument metric_data_queries", value=metric_data_queries, expected_type=type_hints["metric_data_queries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_data_queries is not None:
                self._values["metric_data_queries"] = metric_data_queries

        @builtins.property
        def metric_data_queries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricDataQueryProperty"]]]]:
            '''An array of metric data query structures that enables you to create an anomaly detector based on the result of a metric math expression.

            Each item in ``MetricDataQueries`` gets a metric or performs a math expression. One item in ``MetricDataQueries`` is the expression that provides the time series that the anomaly detector uses as input. Designate the expression by setting ``ReturnData`` to ``true`` for this object in the array. For all other expressions and metrics, set ``ReturnData`` to ``false`` . The designated expression must return a single time series.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricmathanomalydetector.html#cfn-cloudwatch-anomalydetector-metricmathanomalydetector-metricdataqueries
            '''
            result = self._values.get("metric_data_queries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricDataQueryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricMathAnomalyDetectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorPropsMixin.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "namespace": "namespace",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a specific metric.

            :param dimensions: The dimensions for the metric.
            :param metric_name: The name of the metric. This is a required field.
            :param namespace: The namespace of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_property = cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricProperty(
                    dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be582ac4934c01422c10b2721bb0a1db16a6a342fbce6d285469306d9f684517)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.DimensionProperty"]]]]:
            '''The dimensions for the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metric.html#cfn-cloudwatch-anomalydetector-metric-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.DimensionProperty"]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric.

            This is a required field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metric.html#cfn-cloudwatch-anomalydetector-metric-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metric.html#cfn-cloudwatch-anomalydetector-metric-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorPropsMixin.MetricStatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric": "metric",
            "period": "period",
            "stat": "stat",
            "unit": "unit",
        },
    )
    class MetricStatProperty:
        def __init__(
            self,
            *,
            metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.MetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            period: typing.Optional[jsii.Number] = None,
            stat: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines the metric to be returned, along with the statistics, period, and units.

            :param metric: The metric to return, including the metric name, namespace, and dimensions.
            :param period: The granularity, in seconds, of the returned data points. For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 20, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` call that includes a ``StorageResolution`` of 1 second. If the ``StartTime`` parameter specifies a time stamp that is greater than 3 hours ago, you must specify the period as follows or no data points in that time range is returned: - Start time between 3 hours and 15 days ago - Use a multiple of 60 seconds (1 minute). - Start time between 15 and 63 days ago - Use a multiple of 300 seconds (5 minutes). - Start time greater than 63 days ago - Use a multiple of 3600 seconds (1 hour).
            :param stat: The statistic to return. It can include any CloudWatch statistic or extended statistic.
            :param unit: When you are using a ``Put`` operation, this defines what unit you want to use when storing the metric. In a ``Get`` operation, if you omit ``Unit`` then all data that was collected with any unit is returned, along with the corresponding units that were specified when the data was reported to CloudWatch. If you specify a unit, the operation returns only data that was collected with that unit specified. If you specify a unit that does not match the data collected, the results of the operation are null. CloudWatch does not perform unit conversions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricstat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_stat_property = cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricStatProperty(
                    metric=cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.MetricProperty(
                        dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        namespace="namespace"
                    ),
                    period=123,
                    stat="stat",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74d5faef4789ac931665f79ef4dd89d6fdbf8371d62ca31d03ac03b7235feb4e)
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric is not None:
                self._values["metric"] = metric
            if period is not None:
                self._values["period"] = period
            if stat is not None:
                self._values["stat"] = stat
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricProperty"]]:
            '''The metric to return, including the metric name, namespace, and dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricstat.html#cfn-cloudwatch-anomalydetector-metricstat-metric
            '''
            result = self._values.get("metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricProperty"]], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The granularity, in seconds, of the returned data points.

            For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 20, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` call that includes a ``StorageResolution`` of 1 second.

            If the ``StartTime`` parameter specifies a time stamp that is greater than 3 hours ago, you must specify the period as follows or no data points in that time range is returned:

            - Start time between 3 hours and 15 days ago - Use a multiple of 60 seconds (1 minute).
            - Start time between 15 and 63 days ago - Use a multiple of 300 seconds (5 minutes).
            - Start time greater than 63 days ago - Use a multiple of 3600 seconds (1 hour).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricstat.html#cfn-cloudwatch-anomalydetector-metricstat-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stat(self) -> typing.Optional[builtins.str]:
            '''The statistic to return.

            It can include any CloudWatch statistic or extended statistic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricstat.html#cfn-cloudwatch-anomalydetector-metricstat-stat
            '''
            result = self._values.get("stat")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''When you are using a ``Put`` operation, this defines what unit you want to use when storing the metric.

            In a ``Get`` operation, if you omit ``Unit`` then all data that was collected with any unit is returned, along with the corresponding units that were specified when the data was reported to CloudWatch. If you specify a unit, the operation returns only data that was collected with that unit specified. If you specify a unit that does not match the data collected, the results of the operation are null. CloudWatch does not perform unit conversions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricstat.html#cfn-cloudwatch-anomalydetector-metricstat-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorPropsMixin.RangeProperty",
        jsii_struct_bases=[],
        name_mapping={"end_time": "endTime", "start_time": "startTime"},
    )
    class RangeProperty:
        def __init__(
            self,
            *,
            end_time: typing.Optional[builtins.str] = None,
            start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Each ``Range`` specifies one range of days or times to exclude from use for training or updating an anomaly detection model.

            :param end_time: The end time of the range to exclude. The format is ``yyyy-MM-dd'T'HH:mm:ss`` . For example, ``2019-07-01T23:59:59`` .
            :param start_time: The start time of the range to exclude. The format is ``yyyy-MM-dd'T'HH:mm:ss`` . For example, ``2019-07-01T23:59:59`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                range_property = cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.RangeProperty(
                    end_time="endTime",
                    start_time="startTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab59f509ed010171933a6171c4e087888b5185ddfd6752c9495692c1437f5cb3)
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_time is not None:
                self._values["end_time"] = end_time
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def end_time(self) -> typing.Optional[builtins.str]:
            '''The end time of the range to exclude.

            The format is ``yyyy-MM-dd'T'HH:mm:ss`` . For example, ``2019-07-01T23:59:59`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html#cfn-cloudwatch-anomalydetector-range-endtime
            '''
            result = self._values.get("end_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            '''The start time of the range to exclude.

            The format is ``yyyy-MM-dd'T'HH:mm:ss`` . For example, ``2019-07-01T23:59:59`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html#cfn-cloudwatch-anomalydetector-range-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnAnomalyDetectorPropsMixin.SingleMetricAnomalyDetectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "namespace": "namespace",
            "stat": "stat",
        },
    )
    class SingleMetricAnomalyDetectorProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
            stat: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Designates the CloudWatch metric and statistic that provides the time series the anomaly detector uses as input.

            If you have enabled unified cross-account observability, and this account is a monitoring account, the metric can be in the same account or a source account.

            :param account_id: If the CloudWatch metric that provides the time series that the anomaly detector uses as input is in another account, specify that account ID here. If you omit this parameter, the current account is used.
            :param dimensions: The metric dimensions to create the anomaly detection model for.
            :param metric_name: The name of the metric to create the anomaly detection model for.
            :param namespace: The namespace of the metric to create the anomaly detection model for.
            :param stat: The statistic to use for the metric and anomaly detection model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                single_metric_anomaly_detector_property = cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.SingleMetricAnomalyDetectorProperty(
                    account_id="accountId",
                    dimensions=[cloudwatch_mixins.CfnAnomalyDetectorPropsMixin.DimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace",
                    stat="stat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12166715c22359c39556d562729d89e4db972708f219bbe365bab488c257a2ee)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace
            if stat is not None:
                self._values["stat"] = stat

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''If the CloudWatch metric that provides the time series that the anomaly detector uses as input is in another account, specify that account ID here.

            If you omit this parameter, the current account is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.DimensionProperty"]]]]:
            '''The metric dimensions to create the anomaly detection model for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.DimensionProperty"]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric to create the anomaly detection model for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric to create the anomaly detection model for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stat(self) -> typing.Optional[builtins.str]:
            '''The statistic to use for the metric and anomaly detection model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector-stat
            '''
            result = self._values.get("stat")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingleMetricAnomalyDetectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnCompositeAlarmMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions_enabled": "actionsEnabled",
        "actions_suppressor": "actionsSuppressor",
        "actions_suppressor_extension_period": "actionsSuppressorExtensionPeriod",
        "actions_suppressor_wait_period": "actionsSuppressorWaitPeriod",
        "alarm_actions": "alarmActions",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "alarm_rule": "alarmRule",
        "insufficient_data_actions": "insufficientDataActions",
        "ok_actions": "okActions",
        "tags": "tags",
    },
)
class CfnCompositeAlarmMixinProps:
    def __init__(
        self,
        *,
        actions_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        actions_suppressor: typing.Optional[builtins.str] = None,
        actions_suppressor_extension_period: typing.Optional[jsii.Number] = None,
        actions_suppressor_wait_period: typing.Optional[jsii.Number] = None,
        alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        alarm_rule: typing.Optional[builtins.str] = None,
        insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCompositeAlarmPropsMixin.

        :param actions_enabled: Indicates whether actions should be executed during any changes to the alarm state of the composite alarm. The default is TRUE.
        :param actions_suppressor: Actions will be suppressed if the suppressor alarm is in the ``ALARM`` state. ``ActionsSuppressor`` can be an AlarmName or an Amazon Resource Name (ARN) from an existing alarm.
        :param actions_suppressor_extension_period: The maximum time in seconds that the composite alarm waits after suppressor alarm goes out of the ``ALARM`` state. After this time, the composite alarm performs its actions. .. epigraph:: ``ExtensionPeriod`` is required only when ``ActionsSuppressor`` is specified.
        :param actions_suppressor_wait_period: The maximum time in seconds that the composite alarm waits for the suppressor alarm to go into the ``ALARM`` state. After this time, the composite alarm performs its actions. .. epigraph:: ``WaitPeriod`` is required only when ``ActionsSuppressor`` is specified.
        :param alarm_actions: The actions to execute when this alarm transitions to the ALARM state from any other state. Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param alarm_description: The description for the composite alarm.
        :param alarm_name: The name for the composite alarm. This name must be unique within your AWS account.
        :param alarm_rule: An expression that specifies which other alarms are to be evaluated to determine this composite alarm's state. For each alarm that you reference, you designate a function that specifies whether that alarm needs to be in ALARM state, OK state, or INSUFFICIENT_DATA state. You can use operators (AND, OR and NOT) to combine multiple functions in a single expression. You can use parenthesis to logically group the functions in your expression. You can use either alarm names or ARNs to reference the other alarms that are to be evaluated. Functions can include the following: - ALARM("alarm-name or alarm-ARN") is TRUE if the named alarm is in ALARM state. - OK("alarm-name or alarm-ARN") is TRUE if the named alarm is in OK state. - INSUFFICIENT_DATA("alarm-name or alarm-ARN") is TRUE if the named alarm is in INSUFFICIENT_DATA state. - TRUE always evaluates to TRUE. - FALSE always evaluates to FALSE. TRUE and FALSE are useful for testing a complex AlarmRule structure, and for testing your alarm actions. For more information about ``AlarmRule`` syntax, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param insufficient_data_actions: The actions to execute when this alarm transitions to the INSUFFICIENT_DATA state from any other state. Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param ok_actions: The actions to execute when this alarm transitions to the OK state from any other state. Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param tags: A list of key-value pairs to associate with the alarm. You can associate as many as 50 tags with an alarm. To be able to associate tags with the alarm when you create the alarm, you must have the ``cloudwatch:TagResource`` permission. Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
            
            cfn_composite_alarm_mixin_props = cloudwatch_mixins.CfnCompositeAlarmMixinProps(
                actions_enabled=False,
                actions_suppressor="actionsSuppressor",
                actions_suppressor_extension_period=123,
                actions_suppressor_wait_period=123,
                alarm_actions=["alarmActions"],
                alarm_description="alarmDescription",
                alarm_name="alarmName",
                alarm_rule="alarmRule",
                insufficient_data_actions=["insufficientDataActions"],
                ok_actions=["okActions"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f895cf57acc3908f7e0975765fd505cf38b212b5fcdf0efb935833608bdd3da)
            check_type(argname="argument actions_enabled", value=actions_enabled, expected_type=type_hints["actions_enabled"])
            check_type(argname="argument actions_suppressor", value=actions_suppressor, expected_type=type_hints["actions_suppressor"])
            check_type(argname="argument actions_suppressor_extension_period", value=actions_suppressor_extension_period, expected_type=type_hints["actions_suppressor_extension_period"])
            check_type(argname="argument actions_suppressor_wait_period", value=actions_suppressor_wait_period, expected_type=type_hints["actions_suppressor_wait_period"])
            check_type(argname="argument alarm_actions", value=alarm_actions, expected_type=type_hints["alarm_actions"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument alarm_rule", value=alarm_rule, expected_type=type_hints["alarm_rule"])
            check_type(argname="argument insufficient_data_actions", value=insufficient_data_actions, expected_type=type_hints["insufficient_data_actions"])
            check_type(argname="argument ok_actions", value=ok_actions, expected_type=type_hints["ok_actions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if actions_suppressor is not None:
            self._values["actions_suppressor"] = actions_suppressor
        if actions_suppressor_extension_period is not None:
            self._values["actions_suppressor_extension_period"] = actions_suppressor_extension_period
        if actions_suppressor_wait_period is not None:
            self._values["actions_suppressor_wait_period"] = actions_suppressor_wait_period
        if alarm_actions is not None:
            self._values["alarm_actions"] = alarm_actions
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if alarm_rule is not None:
            self._values["alarm_rule"] = alarm_rule
        if insufficient_data_actions is not None:
            self._values["insufficient_data_actions"] = insufficient_data_actions
        if ok_actions is not None:
            self._values["ok_actions"] = ok_actions
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def actions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether actions should be executed during any changes to the alarm state of the composite alarm.

        The default is TRUE.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionsenabled
        '''
        result = self._values.get("actions_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def actions_suppressor(self) -> typing.Optional[builtins.str]:
        '''Actions will be suppressed if the suppressor alarm is in the ``ALARM`` state.

        ``ActionsSuppressor`` can be an AlarmName or an Amazon Resource Name (ARN) from an existing alarm.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionssuppressor
        '''
        result = self._values.get("actions_suppressor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def actions_suppressor_extension_period(self) -> typing.Optional[jsii.Number]:
        '''The maximum time in seconds that the composite alarm waits after suppressor alarm goes out of the ``ALARM`` state.

        After this time, the composite alarm performs its actions.
        .. epigraph::

           ``ExtensionPeriod`` is required only when ``ActionsSuppressor`` is specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionssuppressorextensionperiod
        '''
        result = self._values.get("actions_suppressor_extension_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def actions_suppressor_wait_period(self) -> typing.Optional[jsii.Number]:
        '''The maximum time in seconds that the composite alarm waits for the suppressor alarm to go into the ``ALARM`` state.

        After this time, the composite alarm performs its actions.
        .. epigraph::

           ``WaitPeriod`` is required only when ``ActionsSuppressor`` is specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionssuppressorwaitperiod
        '''
        result = self._values.get("actions_suppressor_wait_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the ALARM state from any other state.

        Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmactions
        '''
        result = self._values.get("alarm_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description for the composite alarm.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmdescription
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The name for the composite alarm.

        This name must be unique within your AWS account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmname
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_rule(self) -> typing.Optional[builtins.str]:
        '''An expression that specifies which other alarms are to be evaluated to determine this composite alarm's state.

        For each alarm that you reference, you designate a function that specifies whether that alarm needs to be in ALARM state, OK state, or INSUFFICIENT_DATA state. You can use operators (AND, OR and NOT) to combine multiple functions in a single expression. You can use parenthesis to logically group the functions in your expression.

        You can use either alarm names or ARNs to reference the other alarms that are to be evaluated.

        Functions can include the following:

        - ALARM("alarm-name or alarm-ARN") is TRUE if the named alarm is in ALARM state.
        - OK("alarm-name or alarm-ARN") is TRUE if the named alarm is in OK state.
        - INSUFFICIENT_DATA("alarm-name or alarm-ARN") is TRUE if the named alarm is in INSUFFICIENT_DATA state.
        - TRUE always evaluates to TRUE.
        - FALSE always evaluates to FALSE.

        TRUE and FALSE are useful for testing a complex AlarmRule structure, and for testing your alarm actions.

        For more information about ``AlarmRule`` syntax, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmrule
        '''
        result = self._values.get("alarm_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insufficient_data_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the INSUFFICIENT_DATA state from any other state.

        Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-insufficientdataactions
        '''
        result = self._values.get("insufficient_data_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the OK state from any other state.

        Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-okactions
        '''
        result = self._values.get("ok_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs to associate with the alarm.

        You can associate as many as 50 tags with an alarm. To be able to associate tags with the alarm when you create the alarm, you must have the ``cloudwatch:TagResource`` permission.

        Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCompositeAlarmMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCompositeAlarmPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnCompositeAlarmPropsMixin",
):
    '''The ``AWS::CloudWatch::CompositeAlarm`` type creates or updates a composite alarm.

    When you create a composite alarm, you specify a rule expression for the alarm that takes into account the alarm states of other alarms that you have created. The composite alarm goes into ALARM state only if all conditions of the rule are met.

    The alarms specified in a composite alarm's rule expression can include metric alarms and other composite alarms.

    Using composite alarms can reduce alarm noise. You can create multiple metric alarms, and also create a composite alarm and set up alerts only for the composite alarm. For example, you could create a composite alarm that goes into ALARM state only when more than one of the underlying metric alarms are in ALARM state.

    When this operation creates an alarm, the alarm state is immediately set to INSUFFICIENT_DATA. The alarm is then evaluated and its state is set appropriately. Any actions associated with the new state are then executed. For a composite alarm, this initial time after creation is the only time that the alarm can be in INSUFFICIENT_DATA state.

    When you update an existing alarm, its state is left unchanged, but the update completely overwrites the previous configuration of the alarm.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html
    :cloudformationResource: AWS::CloudWatch::CompositeAlarm
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
        
        cfn_composite_alarm_props_mixin = cloudwatch_mixins.CfnCompositeAlarmPropsMixin(cloudwatch_mixins.CfnCompositeAlarmMixinProps(
            actions_enabled=False,
            actions_suppressor="actionsSuppressor",
            actions_suppressor_extension_period=123,
            actions_suppressor_wait_period=123,
            alarm_actions=["alarmActions"],
            alarm_description="alarmDescription",
            alarm_name="alarmName",
            alarm_rule="alarmRule",
            insufficient_data_actions=["insufficientDataActions"],
            ok_actions=["okActions"],
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
        props: typing.Union[CfnCompositeAlarmMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudWatch::CompositeAlarm``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a1f27ef1713a0c9b448a12fc287d4f9835b6e7c6c8a9e813db8f8729c4b4c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11e01e53e1ed6cfd77bf900f8d1b594b97bb0a6b0e240a9c5b4b9e4920c71250)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c026e82710a2366c2ca4e373269291c02d1626658d55a9d852b9a3858b6d8a22)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCompositeAlarmMixinProps:
        return typing.cast(CfnCompositeAlarmMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnDashboardMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_body": "dashboardBody",
        "dashboard_name": "dashboardName",
    },
)
class CfnDashboardMixinProps:
    def __init__(
        self,
        *,
        dashboard_body: typing.Optional[builtins.str] = None,
        dashboard_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDashboardPropsMixin.

        :param dashboard_body: The detailed information about the dashboard in JSON format, including the widgets to include and their location on the dashboard. This parameter is required. For more information about the syntax, see `Dashboard Body Structure and Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html>`_ .
        :param dashboard_name: The name of the dashboard. The name must be between 1 and 255 characters. If you do not specify a name, one will be generated automatically.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
            
            cfn_dashboard_mixin_props = cloudwatch_mixins.CfnDashboardMixinProps(
                dashboard_body="dashboardBody",
                dashboard_name="dashboardName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4bf6fc71115bddc269c1d13599af2c9d054b93aeffcaf18ba9d149b3c6c2d38)
            check_type(argname="argument dashboard_body", value=dashboard_body, expected_type=type_hints["dashboard_body"])
            check_type(argname="argument dashboard_name", value=dashboard_name, expected_type=type_hints["dashboard_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dashboard_body is not None:
            self._values["dashboard_body"] = dashboard_body
        if dashboard_name is not None:
            self._values["dashboard_name"] = dashboard_name

    @builtins.property
    def dashboard_body(self) -> typing.Optional[builtins.str]:
        '''The detailed information about the dashboard in JSON format, including the widgets to include and their location on the dashboard.

        This parameter is required.

        For more information about the syntax, see `Dashboard Body Structure and Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardbody
        '''
        result = self._values.get("dashboard_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dashboard_name(self) -> typing.Optional[builtins.str]:
        '''The name of the dashboard.

        The name must be between 1 and 255 characters. If you do not specify a name, one will be generated automatically.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardname
        '''
        result = self._values.get("dashboard_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDashboardMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDashboardPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnDashboardPropsMixin",
):
    '''The ``AWS::CloudWatch::Dashboard`` resource specifies an Amazon CloudWatch dashboard.

    A dashboard is a customizable home page in the CloudWatch console that you can use to monitor your AWS resources in a single view.

    All dashboards in your account are global, not region-specific.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html
    :cloudformationResource: AWS::CloudWatch::Dashboard
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
        
        cfn_dashboard_props_mixin = cloudwatch_mixins.CfnDashboardPropsMixin(cloudwatch_mixins.CfnDashboardMixinProps(
            dashboard_body="dashboardBody",
            dashboard_name="dashboardName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDashboardMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudWatch::Dashboard``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0529aaf326468461e6182fa9e8c6c27954948c83990741ebb990a449f1251dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4df93eff06815cab763642b6f9b3aa8cbbe848da56a903b89a2d49f79caf0afe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1401201024e59633f570080b95243be8f3d0135391629e29ec29e5bf2b2da12)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDashboardMixinProps:
        return typing.cast(CfnDashboardMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnInsightRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "apply_on_transformed_logs": "applyOnTransformedLogs",
        "rule_body": "ruleBody",
        "rule_name": "ruleName",
        "rule_state": "ruleState",
        "tags": "tags",
    },
)
class CfnInsightRuleMixinProps:
    def __init__(
        self,
        *,
        apply_on_transformed_logs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        rule_body: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
        rule_state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnInsightRulePropsMixin.

        :param apply_on_transformed_logs: Determines whether the rules is evaluated on transformed versions of logs. Valid values are ``TRUE`` and ``FALSE`` .
        :param rule_body: The definition of the rule, as a JSON object. For details about the syntax, see `Contributor Insights Rule Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights-RuleSyntax.html>`_ in the *Amazon CloudWatch User Guide* .
        :param rule_name: The name of the rule.
        :param rule_state: The current state of the rule. Valid values are ``ENABLED`` and ``DISABLED`` .
        :param tags: A list of key-value pairs to associate with the Contributor Insights rule. You can associate as many as 50 tags with a rule. Tags can help you organize and categorize your resources. For more information, see `Tagging Your Amazon CloudWatch Resources <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Tagging.html>`_ . To be able to associate tags with a rule, you must have the ``cloudwatch:TagResource`` permission in addition to the ``cloudwatch:PutInsightRule`` permission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
            
            cfn_insight_rule_mixin_props = cloudwatch_mixins.CfnInsightRuleMixinProps(
                apply_on_transformed_logs=False,
                rule_body="ruleBody",
                rule_name="ruleName",
                rule_state="ruleState",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c8f6500c3f3631cadf09b6d6e797ad99919dd580ae4b723f622f1fa9f5cb79)
            check_type(argname="argument apply_on_transformed_logs", value=apply_on_transformed_logs, expected_type=type_hints["apply_on_transformed_logs"])
            check_type(argname="argument rule_body", value=rule_body, expected_type=type_hints["rule_body"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument rule_state", value=rule_state, expected_type=type_hints["rule_state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apply_on_transformed_logs is not None:
            self._values["apply_on_transformed_logs"] = apply_on_transformed_logs
        if rule_body is not None:
            self._values["rule_body"] = rule_body
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if rule_state is not None:
            self._values["rule_state"] = rule_state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def apply_on_transformed_logs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Determines whether the rules is evaluated on transformed versions of logs.

        Valid values are ``TRUE`` and ``FALSE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-applyontransformedlogs
        '''
        result = self._values.get("apply_on_transformed_logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def rule_body(self) -> typing.Optional[builtins.str]:
        '''The definition of the rule, as a JSON object.

        For details about the syntax, see `Contributor Insights Rule Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights-RuleSyntax.html>`_ in the *Amazon CloudWatch User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulebody
        '''
        result = self._values.get("rule_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulename
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_state(self) -> typing.Optional[builtins.str]:
        '''The current state of the rule.

        Valid values are ``ENABLED`` and ``DISABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulestate
        '''
        result = self._values.get("rule_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs to associate with the Contributor Insights rule.

        You can associate as many as 50 tags with a rule.

        Tags can help you organize and categorize your resources. For more information, see `Tagging Your Amazon CloudWatch Resources <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Tagging.html>`_ .

        To be able to associate tags with a rule, you must have the ``cloudwatch:TagResource`` permission in addition to the ``cloudwatch:PutInsightRule`` permission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInsightRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInsightRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnInsightRulePropsMixin",
):
    '''Creates or updates a Contributor Insights rule.

    Rules evaluate log events in a CloudWatch Logs log group, enabling you to find contributor data for the log events in that log group. For more information, see `Using Contributor Insights to Analyze High-Cardinality Data <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights.html>`_ in the *Amazon CloudWatch User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html
    :cloudformationResource: AWS::CloudWatch::InsightRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
        
        cfn_insight_rule_props_mixin = cloudwatch_mixins.CfnInsightRulePropsMixin(cloudwatch_mixins.CfnInsightRuleMixinProps(
            apply_on_transformed_logs=False,
            rule_body="ruleBody",
            rule_name="ruleName",
            rule_state="ruleState",
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
        props: typing.Union[CfnInsightRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudWatch::InsightRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557b9f0bebc488e535c8d45c8e59928812e2e4b1565856f9125562e41bdb2f14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fd3a018de123b109ceca54de7b8392a20d868e8bbcf6ad24965056f661e4265)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19d1a0dd6aaf0067907a780776d9a6f1def4354236ac1c15e37af73f84a86e8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInsightRuleMixinProps:
        return typing.cast(CfnInsightRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnMetricStreamMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_filters": "excludeFilters",
        "firehose_arn": "firehoseArn",
        "include_filters": "includeFilters",
        "include_linked_accounts_metrics": "includeLinkedAccountsMetrics",
        "name": "name",
        "output_format": "outputFormat",
        "role_arn": "roleArn",
        "statistics_configurations": "statisticsConfigurations",
        "tags": "tags",
    },
)
class CfnMetricStreamMixinProps:
    def __init__(
        self,
        *,
        exclude_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMetricStreamPropsMixin.MetricStreamFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        firehose_arn: typing.Optional[builtins.str] = None,
        include_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMetricStreamPropsMixin.MetricStreamFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        include_linked_accounts_metrics: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        output_format: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        statistics_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMetricStreamPropsMixin.MetricStreamStatisticsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMetricStreamPropsMixin.

        :param exclude_filters: If you specify this parameter, the stream sends metrics from all metric namespaces except for the namespaces that you specify here. You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream. When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.
        :param firehose_arn: The ARN of the Amazon Kinesis Firehose delivery stream to use for this metric stream. This Amazon Kinesis Firehose delivery stream must already exist and must be in the same account as the metric stream.
        :param include_filters: If you specify this parameter, the stream sends only the metrics from the metric namespaces that you specify here. You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream. When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.
        :param include_linked_accounts_metrics: If you are creating a metric stream in a monitoring account, specify ``true`` to include metrics from source accounts that are linked to this monitoring account, in the metric stream. The default is ``false`` . For more information about linking accounts, see `CloudWatch cross-account observability <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html>`_
        :param name: If you are creating a new metric stream, this is the name for the new stream. The name must be different than the names of other metric streams in this account and Region. If you are updating a metric stream, specify the name of that stream here.
        :param output_format: The output format for the stream. Valid values are ``json`` , ``opentelemetry1.0`` and ``opentelemetry0.7`` For more information about metric stream output formats, see `Metric streams output formats <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-metric-streams-formats.html>`_ . This parameter is required.
        :param role_arn: The ARN of an IAM role that this metric stream will use to access Amazon Kinesis Firehose resources. This IAM role must already exist and must be in the same account as the metric stream. This IAM role must include the ``firehose:PutRecord`` and ``firehose:PutRecordBatch`` permissions.
        :param statistics_configurations: By default, a metric stream always sends the MAX, MIN, SUM, and SAMPLECOUNT statistics for each metric that is streamed. You can use this parameter to have the metric stream also send additional statistics in the stream. This array can have up to 100 members. For each entry in this array, you specify one or more metrics and the list of additional statistics to stream for those metrics. The additional statistics that you can stream depend on the stream's ``OutputFormat`` . If the ``OutputFormat`` is ``json`` , you can stream any additional statistic that is supported by CloudWatch , listed in `CloudWatch statistics definitions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html>`_ . If the ``OutputFormat`` is OpenTelemetry, you can stream percentile statistics.
        :param tags: An array of key-value pairs to apply to the metric stream. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
            
            cfn_metric_stream_mixin_props = cloudwatch_mixins.CfnMetricStreamMixinProps(
                exclude_filters=[cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamFilterProperty(
                    metric_names=["metricNames"],
                    namespace="namespace"
                )],
                firehose_arn="firehoseArn",
                include_filters=[cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamFilterProperty(
                    metric_names=["metricNames"],
                    namespace="namespace"
                )],
                include_linked_accounts_metrics=False,
                name="name",
                output_format="outputFormat",
                role_arn="roleArn",
                statistics_configurations=[cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamStatisticsConfigurationProperty(
                    additional_statistics=["additionalStatistics"],
                    include_metrics=[cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamStatisticsMetricProperty(
                        metric_name="metricName",
                        namespace="namespace"
                    )]
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fbea7f6fbb186f5bc92895a68ec5c6d6a5fae0d085683bf22b1d062f41deca)
            check_type(argname="argument exclude_filters", value=exclude_filters, expected_type=type_hints["exclude_filters"])
            check_type(argname="argument firehose_arn", value=firehose_arn, expected_type=type_hints["firehose_arn"])
            check_type(argname="argument include_filters", value=include_filters, expected_type=type_hints["include_filters"])
            check_type(argname="argument include_linked_accounts_metrics", value=include_linked_accounts_metrics, expected_type=type_hints["include_linked_accounts_metrics"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument statistics_configurations", value=statistics_configurations, expected_type=type_hints["statistics_configurations"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_filters is not None:
            self._values["exclude_filters"] = exclude_filters
        if firehose_arn is not None:
            self._values["firehose_arn"] = firehose_arn
        if include_filters is not None:
            self._values["include_filters"] = include_filters
        if include_linked_accounts_metrics is not None:
            self._values["include_linked_accounts_metrics"] = include_linked_accounts_metrics
        if name is not None:
            self._values["name"] = name
        if output_format is not None:
            self._values["output_format"] = output_format
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if statistics_configurations is not None:
            self._values["statistics_configurations"] = statistics_configurations
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def exclude_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricStreamPropsMixin.MetricStreamFilterProperty"]]]]:
        '''If you specify this parameter, the stream sends metrics from all metric namespaces except for the namespaces that you specify here.

        You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream.

        When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-excludefilters
        '''
        result = self._values.get("exclude_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricStreamPropsMixin.MetricStreamFilterProperty"]]]], result)

    @builtins.property
    def firehose_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the Amazon Kinesis Firehose delivery stream to use for this metric stream.

        This Amazon Kinesis Firehose delivery stream must already exist and must be in the same account as the metric stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-firehosearn
        '''
        result = self._values.get("firehose_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricStreamPropsMixin.MetricStreamFilterProperty"]]]]:
        '''If you specify this parameter, the stream sends only the metrics from the metric namespaces that you specify here.

        You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream.

        When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-includefilters
        '''
        result = self._values.get("include_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricStreamPropsMixin.MetricStreamFilterProperty"]]]], result)

    @builtins.property
    def include_linked_accounts_metrics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If you are creating a metric stream in a monitoring account, specify ``true`` to include metrics from source accounts that are linked to this monitoring account, in the metric stream.

        The default is ``false`` .

        For more information about linking accounts, see `CloudWatch cross-account observability <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-includelinkedaccountsmetrics
        '''
        result = self._values.get("include_linked_accounts_metrics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''If you are creating a new metric stream, this is the name for the new stream.

        The name must be different than the names of other metric streams in this account and Region.

        If you are updating a metric stream, specify the name of that stream here.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_format(self) -> typing.Optional[builtins.str]:
        '''The output format for the stream.

        Valid values are ``json`` , ``opentelemetry1.0`` and ``opentelemetry0.7`` For more information about metric stream output formats, see `Metric streams output formats <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-metric-streams-formats.html>`_ .

        This parameter is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-outputformat
        '''
        result = self._values.get("output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role that this metric stream will use to access Amazon Kinesis Firehose resources.

        This IAM role must already exist and must be in the same account as the metric stream. This IAM role must include the ``firehose:PutRecord`` and ``firehose:PutRecordBatch`` permissions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistics_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricStreamPropsMixin.MetricStreamStatisticsConfigurationProperty"]]]]:
        '''By default, a metric stream always sends the MAX, MIN, SUM, and SAMPLECOUNT statistics for each metric that is streamed.

        You can use this parameter to have the metric stream also send additional statistics in the stream. This array can have up to 100 members.

        For each entry in this array, you specify one or more metrics and the list of additional statistics to stream for those metrics. The additional statistics that you can stream depend on the stream's ``OutputFormat`` . If the ``OutputFormat`` is ``json`` , you can stream any additional statistic that is supported by CloudWatch , listed in `CloudWatch statistics definitions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html>`_ . If the ``OutputFormat`` is OpenTelemetry, you can stream percentile statistics.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-statisticsconfigurations
        '''
        result = self._values.get("statistics_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricStreamPropsMixin.MetricStreamStatisticsConfigurationProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to the metric stream.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMetricStreamMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMetricStreamPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnMetricStreamPropsMixin",
):
    '''Creates or updates a metric stream.

    Metrics streams can automatically stream CloudWatch metrics to AWS destinations including Amazon S3 and to many third-party solutions. For more information, see `Metric streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Metric-Streams.html>`_ .

    To create a metric stream, you must be logged on to an account that has the ``iam:PassRole`` permission and either the *CloudWatchFullAccess* policy or the ``cloudwatch:PutMetricStream`` permission.

    When you create or update a metric stream, you choose one of the following:

    - Stream metrics from all metric namespaces in the account.
    - Stream metrics from all metric namespaces in the account, except for the namespaces that you list in ``ExcludeFilters`` .
    - Stream metrics from only the metric namespaces that you list in ``IncludeFilters`` .

    When you create a metric stream, the stream is created in the ``running`` state. If you update an existing metric stream, the state does not change.

    If you create a metric stream in an account that has been set up as a monitoring account in CloudWatch cross-account observability, you can choose whether to include metrics from linked source accounts in the metric stream.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html
    :cloudformationResource: AWS::CloudWatch::MetricStream
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
        
        cfn_metric_stream_props_mixin = cloudwatch_mixins.CfnMetricStreamPropsMixin(cloudwatch_mixins.CfnMetricStreamMixinProps(
            exclude_filters=[cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamFilterProperty(
                metric_names=["metricNames"],
                namespace="namespace"
            )],
            firehose_arn="firehoseArn",
            include_filters=[cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamFilterProperty(
                metric_names=["metricNames"],
                namespace="namespace"
            )],
            include_linked_accounts_metrics=False,
            name="name",
            output_format="outputFormat",
            role_arn="roleArn",
            statistics_configurations=[cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamStatisticsConfigurationProperty(
                additional_statistics=["additionalStatistics"],
                include_metrics=[cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamStatisticsMetricProperty(
                    metric_name="metricName",
                    namespace="namespace"
                )]
            )],
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
        props: typing.Union[CfnMetricStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudWatch::MetricStream``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8944c0469cc1c3629cf0e5cef99829a8b2eb33beca764b0f8e539eee2a7630f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16d251fa3df0aeb8a3b4078aec2b3b6a1c5aa968c924c52ea1d302b4d6dc1d84)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fd7fb8b08c659fe468c422f5a730f6b6bb6b38dd0cd49415a88208004f4fb7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMetricStreamMixinProps:
        return typing.cast(CfnMetricStreamMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnMetricStreamPropsMixin.MetricStreamFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_names": "metricNames", "namespace": "namespace"},
    )
    class MetricStreamFilterProperty:
        def __init__(
            self,
            *,
            metric_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure contains a metric namespace and optionally, a list of metric names, to either include in a metric ' stream or exclude from a metric stream.

            A metric stream's filters can include up to 1000 total names. This limit applies to the sum of namespace names and metric names in the filters. For example, this could include 10 metric namespace filters with 99 metrics each, or 20 namespace filters with 49 metrics specified in each filter.

            :param metric_names: The names of the metrics to either include or exclude from the metric stream. If you omit this parameter, all metrics in the namespace are included or excluded, depending on whether this filter is specified as an exclude filter or an include filter. Each metric name can contain only ASCII printable characters (ASCII range 32 through 126). Each metric name must contain at least one non-whitespace character.
            :param namespace: The name of the metric namespace in the filter. The namespace can contain only ASCII printable characters (ASCII range 32 through 126). It must contain at least one non-whitespace character.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_stream_filter_property = cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamFilterProperty(
                    metric_names=["metricNames"],
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73f12ebe88dfa874603b7956ae3c10d8e8dccd1e1c8e01f3b5eb1fe7e36e016d)
                check_type(argname="argument metric_names", value=metric_names, expected_type=type_hints["metric_names"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_names is not None:
                self._values["metric_names"] = metric_names
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def metric_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The names of the metrics to either include or exclude from the metric stream.

            If you omit this parameter, all metrics in the namespace are included or excluded, depending on whether this filter is specified as an exclude filter or an include filter.

            Each metric name can contain only ASCII printable characters (ASCII range 32 through 126). Each metric name must contain at least one non-whitespace character.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamfilter.html#cfn-cloudwatch-metricstream-metricstreamfilter-metricnames
            '''
            result = self._values.get("metric_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The name of the metric namespace in the filter.

            The namespace can contain only ASCII printable characters (ASCII range 32 through 126). It must contain at least one non-whitespace character.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamfilter.html#cfn-cloudwatch-metricstream-metricstreamfilter-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStreamFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnMetricStreamPropsMixin.MetricStreamStatisticsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_statistics": "additionalStatistics",
            "include_metrics": "includeMetrics",
        },
    )
    class MetricStreamStatisticsConfigurationProperty:
        def __init__(
            self,
            *,
            additional_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
            include_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMetricStreamPropsMixin.MetricStreamStatisticsMetricProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''This structure specifies a list of additional statistics to stream, and the metrics to stream those additional statistics for.

            All metrics that match the combination of metric name and namespace will be streamed with the additional statistics, no matter their dimensions.

            :param additional_statistics: The additional statistics to stream for the metrics listed in ``IncludeMetrics`` .
            :param include_metrics: An array that defines the metrics that are to have additional statistics streamed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_stream_statistics_configuration_property = cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamStatisticsConfigurationProperty(
                    additional_statistics=["additionalStatistics"],
                    include_metrics=[cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamStatisticsMetricProperty(
                        metric_name="metricName",
                        namespace="namespace"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26aac0bfabfabab23cb587d96efc970af05aa74d72efc7a0c18de060306ca999)
                check_type(argname="argument additional_statistics", value=additional_statistics, expected_type=type_hints["additional_statistics"])
                check_type(argname="argument include_metrics", value=include_metrics, expected_type=type_hints["include_metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_statistics is not None:
                self._values["additional_statistics"] = additional_statistics
            if include_metrics is not None:
                self._values["include_metrics"] = include_metrics

        @builtins.property
        def additional_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The additional statistics to stream for the metrics listed in ``IncludeMetrics`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsconfiguration.html#cfn-cloudwatch-metricstream-metricstreamstatisticsconfiguration-additionalstatistics
            '''
            result = self._values.get("additional_statistics")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricStreamPropsMixin.MetricStreamStatisticsMetricProperty"]]]]:
            '''An array that defines the metrics that are to have additional statistics streamed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsconfiguration.html#cfn-cloudwatch-metricstream-metricstreamstatisticsconfiguration-includemetrics
            '''
            result = self._values.get("include_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricStreamPropsMixin.MetricStreamStatisticsMetricProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStreamStatisticsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.mixins.CfnMetricStreamPropsMixin.MetricStreamStatisticsMetricProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_name": "metricName", "namespace": "namespace"},
    )
    class MetricStreamStatisticsMetricProperty:
        def __init__(
            self,
            *,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that specifies the metric name and namespace for one metric that is going to have additional statistics included in the stream.

            :param metric_name: The name of the metric.
            :param namespace: The namespace of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudwatch import mixins as cloudwatch_mixins
                
                metric_stream_statistics_metric_property = cloudwatch_mixins.CfnMetricStreamPropsMixin.MetricStreamStatisticsMetricProperty(
                    metric_name="metricName",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b391ee0e2c6a42ade2805100eae5105da6fb3b32c202cbc5704fc1ab0861cfdd)
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsmetric.html#cfn-cloudwatch-metricstream-metricstreamstatisticsmetric-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsmetric.html#cfn-cloudwatch-metricstream-metricstreamstatisticsmetric-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStreamStatisticsMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAlarmMixinProps",
    "CfnAlarmPropsMixin",
    "CfnAnomalyDetectorMixinProps",
    "CfnAnomalyDetectorPropsMixin",
    "CfnCompositeAlarmMixinProps",
    "CfnCompositeAlarmPropsMixin",
    "CfnDashboardMixinProps",
    "CfnDashboardPropsMixin",
    "CfnInsightRuleMixinProps",
    "CfnInsightRulePropsMixin",
    "CfnMetricStreamMixinProps",
    "CfnMetricStreamPropsMixin",
]

publication.publish()

def _typecheckingstub__8b488250c806abadbacc97410fe1dd8e7394fff83b8a94c03b191b5dc3cad79b(
    *,
    actions_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    comparison_operator: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmPropsMixin.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    extended_statistic: typing.Optional[builtins.str] = None,
    insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmPropsMixin.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    namespace: typing.Optional[builtins.str] = None,
    ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    period: typing.Optional[jsii.Number] = None,
    statistic: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    threshold: typing.Optional[jsii.Number] = None,
    threshold_metric_id: typing.Optional[builtins.str] = None,
    treat_missing_data: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343d3a7244cfdd02b43743a4fde04969313158d8b843b7e4697dd63ac45a8483(
    props: typing.Union[CfnAlarmMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b5d80090a3a2c800531e93edb14f17def89eeabf51433c280e98acee19dde4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3adc0535a2f1874b04f5c63909e1303e3fefcc2fd42074796e675410d7bae97b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e566726e76eac48e5e384233e24b0ffc4417e864c4d41a41f42df2a0cf624b33(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cf7b0e5ce11ffdc8705522d5cb6b4d26f3e7d2ad1324e12d953167e44701e1(
    *,
    account_id: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmPropsMixin.MetricStatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    period: typing.Optional[jsii.Number] = None,
    return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e83b20a6531e2706341516bd09f926d8b4a4199c847e6aa7668ab1b3bfa7771(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmPropsMixin.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd062229b7b3bc664dfcd5ed204b7c2920c2eacc08b996aa32b378536586c38(
    *,
    metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmPropsMixin.MetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    period: typing.Optional[jsii.Number] = None,
    stat: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecba4636969c85aeee29cc6948ace6e56a281231555a9705d6decf5206caadc(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_characteristics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.MetricCharacteristicsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metric_math_anomaly_detector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.MetricMathAnomalyDetectorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    single_metric_anomaly_detector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.SingleMetricAnomalyDetectorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stat: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0383645e7aa5da97e96df45f86f3716887fc5c6779b891c48368e99f5a60a1b4(
    props: typing.Union[CfnAnomalyDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac4fce888ec7125836002a82c931a552c12f7924b5c50c661e1bc77e682282a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d274c369e27c704dd46beec3f9dfdd88a472b13ab9b134761842e222f969db(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea215bb0479410afd8fece46dc08fbd12361c855f9e93f57b9d4f1b03363d1bb(
    *,
    excluded_time_ranges: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.RangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8736477fa6691e4b5b7e65f5f392fb2a4c7f4054fd6df1786e7aba5795d9a504(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafa2caed05e2e444fbd3a80ef54672b78ded63c503fdcb3e6446d004d160cd0(
    *,
    periodic_spikes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea68a68069eb87d7e212651a19ce11de383b941541cad00ba521c611a6325d1(
    *,
    account_id: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.MetricStatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    period: typing.Optional[jsii.Number] = None,
    return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee8d8cee3ffdaed4e0144b73386be621df864348fc024e1e2e48faa0e640561(
    *,
    metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be582ac4934c01422c10b2721bb0a1db16a6a342fbce6d285469306d9f684517(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d5faef4789ac931665f79ef4dd89d6fdbf8371d62ca31d03ac03b7235feb4e(
    *,
    metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.MetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    period: typing.Optional[jsii.Number] = None,
    stat: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab59f509ed010171933a6171c4e087888b5185ddfd6752c9495692c1437f5cb3(
    *,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12166715c22359c39556d562729d89e4db972708f219bbe365bab488c257a2ee(
    *,
    account_id: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    stat: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f895cf57acc3908f7e0975765fd505cf38b212b5fcdf0efb935833608bdd3da(
    *,
    actions_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    actions_suppressor: typing.Optional[builtins.str] = None,
    actions_suppressor_extension_period: typing.Optional[jsii.Number] = None,
    actions_suppressor_wait_period: typing.Optional[jsii.Number] = None,
    alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    alarm_rule: typing.Optional[builtins.str] = None,
    insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a1f27ef1713a0c9b448a12fc287d4f9835b6e7c6c8a9e813db8f8729c4b4c6(
    props: typing.Union[CfnCompositeAlarmMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e01e53e1ed6cfd77bf900f8d1b594b97bb0a6b0e240a9c5b4b9e4920c71250(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c026e82710a2366c2ca4e373269291c02d1626658d55a9d852b9a3858b6d8a22(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bf6fc71115bddc269c1d13599af2c9d054b93aeffcaf18ba9d149b3c6c2d38(
    *,
    dashboard_body: typing.Optional[builtins.str] = None,
    dashboard_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0529aaf326468461e6182fa9e8c6c27954948c83990741ebb990a449f1251dd(
    props: typing.Union[CfnDashboardMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df93eff06815cab763642b6f9b3aa8cbbe848da56a903b89a2d49f79caf0afe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1401201024e59633f570080b95243be8f3d0135391629e29ec29e5bf2b2da12(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c8f6500c3f3631cadf09b6d6e797ad99919dd580ae4b723f622f1fa9f5cb79(
    *,
    apply_on_transformed_logs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    rule_body: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    rule_state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557b9f0bebc488e535c8d45c8e59928812e2e4b1565856f9125562e41bdb2f14(
    props: typing.Union[CfnInsightRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd3a018de123b109ceca54de7b8392a20d868e8bbcf6ad24965056f661e4265(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19d1a0dd6aaf0067907a780776d9a6f1def4354236ac1c15e37af73f84a86e8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fbea7f6fbb186f5bc92895a68ec5c6d6a5fae0d085683bf22b1d062f41deca(
    *,
    exclude_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMetricStreamPropsMixin.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    firehose_arn: typing.Optional[builtins.str] = None,
    include_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMetricStreamPropsMixin.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include_linked_accounts_metrics: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    output_format: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    statistics_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMetricStreamPropsMixin.MetricStreamStatisticsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8944c0469cc1c3629cf0e5cef99829a8b2eb33beca764b0f8e539eee2a7630f(
    props: typing.Union[CfnMetricStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d251fa3df0aeb8a3b4078aec2b3b6a1c5aa968c924c52ea1d302b4d6dc1d84(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fd7fb8b08c659fe468c422f5a730f6b6bb6b38dd0cd49415a88208004f4fb7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f12ebe88dfa874603b7956ae3c10d8e8dccd1e1c8e01f3b5eb1fe7e36e016d(
    *,
    metric_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26aac0bfabfabab23cb587d96efc970af05aa74d72efc7a0c18de060306ca999(
    *,
    additional_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMetricStreamPropsMixin.MetricStreamStatisticsMetricProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b391ee0e2c6a42ade2805100eae5105da6fb3b32c202cbc5704fc1ab0861cfdd(
    *,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
