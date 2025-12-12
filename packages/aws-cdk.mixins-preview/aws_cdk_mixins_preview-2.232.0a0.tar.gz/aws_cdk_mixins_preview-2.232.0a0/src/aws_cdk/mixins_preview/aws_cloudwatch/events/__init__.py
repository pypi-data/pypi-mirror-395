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
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.interfaces.aws_cloudwatch as _aws_cdk_interfaces_aws_cloudwatch_ceddda9d


class AlarmEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents",
):
    '''(experimental) EventBridge event patterns for Alarm.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
        from aws_cdk.interfaces import aws_cloudwatch as interfaces_cloudwatch
        
        # alarm_ref: interfaces_cloudwatch.IAlarmRef
        
        alarm_events = cloudwatch_events.AlarmEvents.from_alarm(alarm_ref)
    '''

    @jsii.member(jsii_name="fromAlarm")
    @builtins.classmethod
    def from_alarm(
        cls,
        alarm_ref: _aws_cdk_interfaces_aws_cloudwatch_ceddda9d.IAlarmRef,
    ) -> "AlarmEvents":
        '''(experimental) Create AlarmEvents from a Alarm reference.

        :param alarm_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfedb8223a728c521f2f96cbc6b0a5a2f336b8264804d3fc51b8c64dfdd9f644)
            check_type(argname="argument alarm_ref", value=alarm_ref, expected_type=type_hints["alarm_ref"])
        return typing.cast("AlarmEvents", jsii.sinvoke(cls, "fromAlarm", [alarm_ref]))

    @jsii.member(jsii_name="cloudWatchAlarmConfigurationChangePattern")
    def cloud_watch_alarm_configuration_change_pattern(
        self,
        *,
        alarm_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmConfigurationChange.Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        operation: typing.Optional[typing.Sequence[builtins.str]] = None,
        state: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmConfigurationChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Alarm CloudWatch Alarm Configuration Change.

        :param alarm_name: (experimental) alarmName property. Specify an array of string values to match this event if the actual value of alarmName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param configuration: (experimental) configuration property. Specify an array of string values to match this event if the actual value of configuration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AlarmEvents.CloudWatchAlarmConfigurationChange.CloudWatchAlarmConfigurationChangeProps(
            alarm_name=alarm_name,
            configuration=configuration,
            event_metadata=event_metadata,
            operation=operation,
            state=state,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "cloudWatchAlarmConfigurationChangePattern", [options]))

    @jsii.member(jsii_name="cloudWatchAlarmStateChangePattern")
    def cloud_watch_alarm_state_change_pattern(
        self,
        *,
        alarm_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmStateChange.Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        previous_state: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmStateChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
        state: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmStateChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Alarm CloudWatch Alarm State Change.

        :param alarm_name: (experimental) alarmName property. Specify an array of string values to match this event if the actual value of alarmName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Alarm reference
        :param configuration: (experimental) configuration property. Specify an array of string values to match this event if the actual value of configuration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param previous_state: (experimental) previousState property. Specify an array of string values to match this event if the actual value of previousState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AlarmEvents.CloudWatchAlarmStateChange.CloudWatchAlarmStateChangeProps(
            alarm_name=alarm_name,
            configuration=configuration,
            event_metadata=event_metadata,
            previous_state=previous_state,
            state=state,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "cloudWatchAlarmStateChangePattern", [options]))

    class CloudWatchAlarmConfigurationChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmConfigurationChange",
    ):
        '''(experimental) aws.cloudwatch@CloudWatchAlarmConfigurationChange event types for Alarm.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
            
            cloud_watch_alarm_configuration_change = cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmConfigurationChange.CloudWatchAlarmConfigurationChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "alarm_name": "alarmName",
                "configuration": "configuration",
                "event_metadata": "eventMetadata",
                "operation": "operation",
                "state": "state",
            },
        )
        class CloudWatchAlarmConfigurationChangeProps:
            def __init__(
                self,
                *,
                alarm_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                configuration: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmConfigurationChange.Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                operation: typing.Optional[typing.Sequence[builtins.str]] = None,
                state: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmConfigurationChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Alarm aws.cloudwatch@CloudWatchAlarmConfigurationChange event.

                :param alarm_name: (experimental) alarmName property. Specify an array of string values to match this event if the actual value of alarmName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param configuration: (experimental) configuration property. Specify an array of string values to match this event if the actual value of configuration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    cloud_watch_alarm_configuration_change_props = cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.CloudWatchAlarmConfigurationChangeProps(
                        alarm_name=["alarmName"],
                        configuration=cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.Configuration(
                            actions_enabled=["actionsEnabled"],
                            actions_suppressor=["actionsSuppressor"],
                            actions_suppressor_extension_period=["actionsSuppressorExtensionPeriod"],
                            actions_suppressor_wait_period=["actionsSuppressorWaitPeriod"],
                            alarm_actions=["alarmActions"],
                            alarm_name=["alarmName"],
                            alarm_rule=["alarmRule"],
                            comparison_operator=["comparisonOperator"],
                            datapoints_to_alarm=["datapointsToAlarm"],
                            description=["description"],
                            evaluate_low_sample_count_percentile=["evaluateLowSampleCountPercentile"],
                            evaluation_periods=["evaluationPeriods"],
                            insufficient_data_actions=["insufficientDataActions"],
                            metrics=[cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.ConfigurationItem(
                                id=["id"],
                                metric_stat=cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.MetricStat(
                                    metric=cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.Metric(
                                        dimensions=["dimensions"],
                                        name=["name"],
                                        namespace=["namespace"]
                                    ),
                                    period=["period"],
                                    stat=["stat"]
                                ),
                                return_data=["returnData"]
                            )],
                            ok_actions=["okActions"],
                            threshold=["threshold"],
                            timestamp=["timestamp"],
                            treat_missing_data=["treatMissingData"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        operation=["operation"],
                        state=cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.State(
                            actions_suppressed_by=["actionsSuppressedBy"],
                            evaluation_state=["evaluationState"],
                            reason=["reason"],
                            reason_data=["reasonData"],
                            timestamp=["timestamp"],
                            value=["value"]
                        )
                    )
                '''
                if isinstance(configuration, dict):
                    configuration = AlarmEvents.CloudWatchAlarmConfigurationChange.Configuration(**configuration)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(state, dict):
                    state = AlarmEvents.CloudWatchAlarmConfigurationChange.State(**state)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__5c949f9d9cc04995a1acd74b0575f55b469dba8d9d009a92c793223851c375d1)
                    check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
                    check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                    check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if alarm_name is not None:
                    self._values["alarm_name"] = alarm_name
                if configuration is not None:
                    self._values["configuration"] = configuration
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if operation is not None:
                    self._values["operation"] = operation
                if state is not None:
                    self._values["state"] = state

            @builtins.property
            def alarm_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) alarmName property.

                Specify an array of string values to match this event if the actual value of alarmName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("alarm_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def configuration(
                self,
            ) -> typing.Optional["AlarmEvents.CloudWatchAlarmConfigurationChange.Configuration"]:
                '''(experimental) configuration property.

                Specify an array of string values to match this event if the actual value of configuration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("configuration")
                return typing.cast(typing.Optional["AlarmEvents.CloudWatchAlarmConfigurationChange.Configuration"], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def operation(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) operation property.

                Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("operation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def state(
                self,
            ) -> typing.Optional["AlarmEvents.CloudWatchAlarmConfigurationChange.State"]:
                '''(experimental) state property.

                Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("state")
                return typing.cast(typing.Optional["AlarmEvents.CloudWatchAlarmConfigurationChange.State"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CloudWatchAlarmConfigurationChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmConfigurationChange.Configuration",
            jsii_struct_bases=[],
            name_mapping={
                "actions_enabled": "actionsEnabled",
                "actions_suppressor": "actionsSuppressor",
                "actions_suppressor_extension_period": "actionsSuppressorExtensionPeriod",
                "actions_suppressor_wait_period": "actionsSuppressorWaitPeriod",
                "alarm_actions": "alarmActions",
                "alarm_name": "alarmName",
                "alarm_rule": "alarmRule",
                "comparison_operator": "comparisonOperator",
                "datapoints_to_alarm": "datapointsToAlarm",
                "description": "description",
                "evaluate_low_sample_count_percentile": "evaluateLowSampleCountPercentile",
                "evaluation_periods": "evaluationPeriods",
                "insufficient_data_actions": "insufficientDataActions",
                "metrics": "metrics",
                "ok_actions": "okActions",
                "threshold": "threshold",
                "timestamp": "timestamp",
                "treat_missing_data": "treatMissingData",
            },
        )
        class Configuration:
            def __init__(
                self,
                *,
                actions_enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
                actions_suppressor: typing.Optional[typing.Sequence[builtins.str]] = None,
                actions_suppressor_extension_period: typing.Optional[typing.Sequence[builtins.str]] = None,
                actions_suppressor_wait_period: typing.Optional[typing.Sequence[builtins.str]] = None,
                alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
                alarm_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                alarm_rule: typing.Optional[typing.Sequence[builtins.str]] = None,
                comparison_operator: typing.Optional[typing.Sequence[builtins.str]] = None,
                datapoints_to_alarm: typing.Optional[typing.Sequence[builtins.str]] = None,
                description: typing.Optional[typing.Sequence[builtins.str]] = None,
                evaluate_low_sample_count_percentile: typing.Optional[typing.Sequence[builtins.str]] = None,
                evaluation_periods: typing.Optional[typing.Sequence[builtins.str]] = None,
                insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
                metrics: typing.Optional[typing.Sequence[typing.Union["AlarmEvents.CloudWatchAlarmConfigurationChange.ConfigurationItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
                threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
                timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                treat_missing_data: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Configuration.

                :param actions_enabled: (experimental) actionsEnabled property. Specify an array of string values to match this event if the actual value of actionsEnabled is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param actions_suppressor: (experimental) actionsSuppressor property. Specify an array of string values to match this event if the actual value of actionsSuppressor is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param actions_suppressor_extension_period: (experimental) actionsSuppressorExtensionPeriod property. Specify an array of string values to match this event if the actual value of actionsSuppressorExtensionPeriod is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param actions_suppressor_wait_period: (experimental) actionsSuppressorWaitPeriod property. Specify an array of string values to match this event if the actual value of actionsSuppressorWaitPeriod is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param alarm_actions: (experimental) alarmActions property. Specify an array of string values to match this event if the actual value of alarmActions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param alarm_name: (experimental) alarmName property. Specify an array of string values to match this event if the actual value of alarmName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Alarm reference
                :param alarm_rule: (experimental) alarmRule property. Specify an array of string values to match this event if the actual value of alarmRule is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param comparison_operator: (experimental) comparisonOperator property. Specify an array of string values to match this event if the actual value of comparisonOperator is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param datapoints_to_alarm: (experimental) datapointsToAlarm property. Specify an array of string values to match this event if the actual value of datapointsToAlarm is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param description: (experimental) description property. Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param evaluate_low_sample_count_percentile: (experimental) evaluateLowSampleCountPercentile property. Specify an array of string values to match this event if the actual value of evaluateLowSampleCountPercentile is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param evaluation_periods: (experimental) evaluationPeriods property. Specify an array of string values to match this event if the actual value of evaluationPeriods is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param insufficient_data_actions: (experimental) insufficientDataActions property. Specify an array of string values to match this event if the actual value of insufficientDataActions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param metrics: (experimental) metrics property. Specify an array of string values to match this event if the actual value of metrics is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ok_actions: (experimental) okActions property. Specify an array of string values to match this event if the actual value of okActions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param threshold: (experimental) threshold property. Specify an array of string values to match this event if the actual value of threshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param timestamp: (experimental) timestamp property. Specify an array of string values to match this event if the actual value of timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param treat_missing_data: (experimental) treatMissingData property. Specify an array of string values to match this event if the actual value of treatMissingData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    configuration = cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.Configuration(
                        actions_enabled=["actionsEnabled"],
                        actions_suppressor=["actionsSuppressor"],
                        actions_suppressor_extension_period=["actionsSuppressorExtensionPeriod"],
                        actions_suppressor_wait_period=["actionsSuppressorWaitPeriod"],
                        alarm_actions=["alarmActions"],
                        alarm_name=["alarmName"],
                        alarm_rule=["alarmRule"],
                        comparison_operator=["comparisonOperator"],
                        datapoints_to_alarm=["datapointsToAlarm"],
                        description=["description"],
                        evaluate_low_sample_count_percentile=["evaluateLowSampleCountPercentile"],
                        evaluation_periods=["evaluationPeriods"],
                        insufficient_data_actions=["insufficientDataActions"],
                        metrics=[cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.ConfigurationItem(
                            id=["id"],
                            metric_stat=cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.MetricStat(
                                metric=cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.Metric(
                                    dimensions=["dimensions"],
                                    name=["name"],
                                    namespace=["namespace"]
                                ),
                                period=["period"],
                                stat=["stat"]
                            ),
                            return_data=["returnData"]
                        )],
                        ok_actions=["okActions"],
                        threshold=["threshold"],
                        timestamp=["timestamp"],
                        treat_missing_data=["treatMissingData"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9c790c20f69b305a4ac13bba65b1eac52cae96f3bd21af1feaf371b62b243e75)
                    check_type(argname="argument actions_enabled", value=actions_enabled, expected_type=type_hints["actions_enabled"])
                    check_type(argname="argument actions_suppressor", value=actions_suppressor, expected_type=type_hints["actions_suppressor"])
                    check_type(argname="argument actions_suppressor_extension_period", value=actions_suppressor_extension_period, expected_type=type_hints["actions_suppressor_extension_period"])
                    check_type(argname="argument actions_suppressor_wait_period", value=actions_suppressor_wait_period, expected_type=type_hints["actions_suppressor_wait_period"])
                    check_type(argname="argument alarm_actions", value=alarm_actions, expected_type=type_hints["alarm_actions"])
                    check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
                    check_type(argname="argument alarm_rule", value=alarm_rule, expected_type=type_hints["alarm_rule"])
                    check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                    check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
                    check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                    check_type(argname="argument evaluate_low_sample_count_percentile", value=evaluate_low_sample_count_percentile, expected_type=type_hints["evaluate_low_sample_count_percentile"])
                    check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
                    check_type(argname="argument insufficient_data_actions", value=insufficient_data_actions, expected_type=type_hints["insufficient_data_actions"])
                    check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
                    check_type(argname="argument ok_actions", value=ok_actions, expected_type=type_hints["ok_actions"])
                    check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
                    check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
                    check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
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
                if alarm_name is not None:
                    self._values["alarm_name"] = alarm_name
                if alarm_rule is not None:
                    self._values["alarm_rule"] = alarm_rule
                if comparison_operator is not None:
                    self._values["comparison_operator"] = comparison_operator
                if datapoints_to_alarm is not None:
                    self._values["datapoints_to_alarm"] = datapoints_to_alarm
                if description is not None:
                    self._values["description"] = description
                if evaluate_low_sample_count_percentile is not None:
                    self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
                if evaluation_periods is not None:
                    self._values["evaluation_periods"] = evaluation_periods
                if insufficient_data_actions is not None:
                    self._values["insufficient_data_actions"] = insufficient_data_actions
                if metrics is not None:
                    self._values["metrics"] = metrics
                if ok_actions is not None:
                    self._values["ok_actions"] = ok_actions
                if threshold is not None:
                    self._values["threshold"] = threshold
                if timestamp is not None:
                    self._values["timestamp"] = timestamp
                if treat_missing_data is not None:
                    self._values["treat_missing_data"] = treat_missing_data

            @builtins.property
            def actions_enabled(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionsEnabled property.

                Specify an array of string values to match this event if the actual value of actionsEnabled is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("actions_enabled")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def actions_suppressor(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionsSuppressor property.

                Specify an array of string values to match this event if the actual value of actionsSuppressor is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("actions_suppressor")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def actions_suppressor_extension_period(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionsSuppressorExtensionPeriod property.

                Specify an array of string values to match this event if the actual value of actionsSuppressorExtensionPeriod is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("actions_suppressor_extension_period")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def actions_suppressor_wait_period(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionsSuppressorWaitPeriod property.

                Specify an array of string values to match this event if the actual value of actionsSuppressorWaitPeriod is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("actions_suppressor_wait_period")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) alarmActions property.

                Specify an array of string values to match this event if the actual value of alarmActions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("alarm_actions")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def alarm_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) alarmName property.

                Specify an array of string values to match this event if the actual value of alarmName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Alarm reference

                :stability: experimental
                '''
                result = self._values.get("alarm_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def alarm_rule(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) alarmRule property.

                Specify an array of string values to match this event if the actual value of alarmRule is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("alarm_rule")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def comparison_operator(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) comparisonOperator property.

                Specify an array of string values to match this event if the actual value of comparisonOperator is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("comparison_operator")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datapoints_to_alarm(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datapointsToAlarm property.

                Specify an array of string values to match this event if the actual value of datapointsToAlarm is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datapoints_to_alarm")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) description property.

                Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def evaluate_low_sample_count_percentile(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) evaluateLowSampleCountPercentile property.

                Specify an array of string values to match this event if the actual value of evaluateLowSampleCountPercentile is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("evaluate_low_sample_count_percentile")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def evaluation_periods(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) evaluationPeriods property.

                Specify an array of string values to match this event if the actual value of evaluationPeriods is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("evaluation_periods")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def insufficient_data_actions(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) insufficientDataActions property.

                Specify an array of string values to match this event if the actual value of insufficientDataActions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("insufficient_data_actions")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def metrics(
                self,
            ) -> typing.Optional[typing.List["AlarmEvents.CloudWatchAlarmConfigurationChange.ConfigurationItem"]]:
                '''(experimental) metrics property.

                Specify an array of string values to match this event if the actual value of metrics is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("metrics")
                return typing.cast(typing.Optional[typing.List["AlarmEvents.CloudWatchAlarmConfigurationChange.ConfigurationItem"]], result)

            @builtins.property
            def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) okActions property.

                Specify an array of string values to match this event if the actual value of okActions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ok_actions")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def threshold(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) threshold property.

                Specify an array of string values to match this event if the actual value of threshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threshold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) timestamp property.

                Specify an array of string values to match this event if the actual value of timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def treat_missing_data(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) treatMissingData property.

                Specify an array of string values to match this event if the actual value of treatMissingData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("treat_missing_data")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Configuration(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmConfigurationChange.ConfigurationItem",
            jsii_struct_bases=[],
            name_mapping={
                "id": "id",
                "metric_stat": "metricStat",
                "return_data": "returnData",
            },
        )
        class ConfigurationItem:
            def __init__(
                self,
                *,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                metric_stat: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmConfigurationChange.MetricStat", typing.Dict[builtins.str, typing.Any]]] = None,
                return_data: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ConfigurationItem.

                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param metric_stat: (experimental) metricStat property. Specify an array of string values to match this event if the actual value of metricStat is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param return_data: (experimental) returnData property. Specify an array of string values to match this event if the actual value of returnData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    configuration_item = cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.ConfigurationItem(
                        id=["id"],
                        metric_stat=cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.MetricStat(
                            metric=cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.Metric(
                                dimensions=["dimensions"],
                                name=["name"],
                                namespace=["namespace"]
                            ),
                            period=["period"],
                            stat=["stat"]
                        ),
                        return_data=["returnData"]
                    )
                '''
                if isinstance(metric_stat, dict):
                    metric_stat = AlarmEvents.CloudWatchAlarmConfigurationChange.MetricStat(**metric_stat)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__89860ca8465d7cef68689e8f51ffcdc938017f70370f0ecc136eb6fad40f10ec)
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                    check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if id is not None:
                    self._values["id"] = id
                if metric_stat is not None:
                    self._values["metric_stat"] = metric_stat
                if return_data is not None:
                    self._values["return_data"] = return_data

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def metric_stat(
                self,
            ) -> typing.Optional["AlarmEvents.CloudWatchAlarmConfigurationChange.MetricStat"]:
                '''(experimental) metricStat property.

                Specify an array of string values to match this event if the actual value of metricStat is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("metric_stat")
                return typing.cast(typing.Optional["AlarmEvents.CloudWatchAlarmConfigurationChange.MetricStat"], result)

            @builtins.property
            def return_data(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) returnData property.

                Specify an array of string values to match this event if the actual value of returnData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("return_data")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ConfigurationItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmConfigurationChange.Metric",
            jsii_struct_bases=[],
            name_mapping={
                "dimensions": "dimensions",
                "name": "name",
                "namespace": "namespace",
            },
        )
        class Metric:
            def __init__(
                self,
                *,
                dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                namespace: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Metric.

                :param dimensions: (experimental) dimensions property. Specify an array of string values to match this event if the actual value of dimensions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param namespace: (experimental) namespace property. Specify an array of string values to match this event if the actual value of namespace is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    metric = cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.Metric(
                        dimensions=["dimensions"],
                        name=["name"],
                        namespace=["namespace"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3308f0c752817e082b18e7e8fe611acd993dd177e4575a482f8dfff4845cec68)
                    check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if dimensions is not None:
                    self._values["dimensions"] = dimensions
                if name is not None:
                    self._values["name"] = name
                if namespace is not None:
                    self._values["namespace"] = namespace

            @builtins.property
            def dimensions(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) dimensions property.

                Specify an array of string values to match this event if the actual value of dimensions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("dimensions")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def namespace(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) namespace property.

                Specify an array of string values to match this event if the actual value of namespace is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("namespace")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Metric(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmConfigurationChange.MetricStat",
            jsii_struct_bases=[],
            name_mapping={"metric": "metric", "period": "period", "stat": "stat"},
        )
        class MetricStat:
            def __init__(
                self,
                *,
                metric: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmConfigurationChange.Metric", typing.Dict[builtins.str, typing.Any]]] = None,
                period: typing.Optional[typing.Sequence[builtins.str]] = None,
                stat: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for MetricStat.

                :param metric: (experimental) metric property. Specify an array of string values to match this event if the actual value of metric is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param period: (experimental) period property. Specify an array of string values to match this event if the actual value of period is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param stat: (experimental) stat property. Specify an array of string values to match this event if the actual value of stat is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    metric_stat = cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.MetricStat(
                        metric=cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.Metric(
                            dimensions=["dimensions"],
                            name=["name"],
                            namespace=["namespace"]
                        ),
                        period=["period"],
                        stat=["stat"]
                    )
                '''
                if isinstance(metric, dict):
                    metric = AlarmEvents.CloudWatchAlarmConfigurationChange.Metric(**metric)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__86d23a40bfad6a396c253113929154661ae45e177d3bef018fde9a893320447c)
                    check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                    check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                    check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if metric is not None:
                    self._values["metric"] = metric
                if period is not None:
                    self._values["period"] = period
                if stat is not None:
                    self._values["stat"] = stat

            @builtins.property
            def metric(
                self,
            ) -> typing.Optional["AlarmEvents.CloudWatchAlarmConfigurationChange.Metric"]:
                '''(experimental) metric property.

                Specify an array of string values to match this event if the actual value of metric is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("metric")
                return typing.cast(typing.Optional["AlarmEvents.CloudWatchAlarmConfigurationChange.Metric"], result)

            @builtins.property
            def period(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) period property.

                Specify an array of string values to match this event if the actual value of period is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("period")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def stat(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) stat property.

                Specify an array of string values to match this event if the actual value of stat is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("stat")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "MetricStat(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmConfigurationChange.State",
            jsii_struct_bases=[],
            name_mapping={
                "actions_suppressed_by": "actionsSuppressedBy",
                "evaluation_state": "evaluationState",
                "reason": "reason",
                "reason_data": "reasonData",
                "timestamp": "timestamp",
                "value": "value",
            },
        )
        class State:
            def __init__(
                self,
                *,
                actions_suppressed_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                evaluation_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                reason_data: typing.Optional[typing.Sequence[builtins.str]] = None,
                timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for State.

                :param actions_suppressed_by: (experimental) actionsSuppressedBy property. Specify an array of string values to match this event if the actual value of actionsSuppressedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param evaluation_state: (experimental) evaluationState property. Specify an array of string values to match this event if the actual value of evaluationState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reason: (experimental) reason property. Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reason_data: (experimental) reasonData property. Specify an array of string values to match this event if the actual value of reasonData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param timestamp: (experimental) timestamp property. Specify an array of string values to match this event if the actual value of timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) value property. Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    state = cloudwatch_events.AlarmEvents.CloudWatchAlarmConfigurationChange.State(
                        actions_suppressed_by=["actionsSuppressedBy"],
                        evaluation_state=["evaluationState"],
                        reason=["reason"],
                        reason_data=["reasonData"],
                        timestamp=["timestamp"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__96bc1df6e51e53bd98de18565d400ab6daac354962d5250c87635e1fe269e673)
                    check_type(argname="argument actions_suppressed_by", value=actions_suppressed_by, expected_type=type_hints["actions_suppressed_by"])
                    check_type(argname="argument evaluation_state", value=evaluation_state, expected_type=type_hints["evaluation_state"])
                    check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                    check_type(argname="argument reason_data", value=reason_data, expected_type=type_hints["reason_data"])
                    check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if actions_suppressed_by is not None:
                    self._values["actions_suppressed_by"] = actions_suppressed_by
                if evaluation_state is not None:
                    self._values["evaluation_state"] = evaluation_state
                if reason is not None:
                    self._values["reason"] = reason
                if reason_data is not None:
                    self._values["reason_data"] = reason_data
                if timestamp is not None:
                    self._values["timestamp"] = timestamp
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def actions_suppressed_by(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionsSuppressedBy property.

                Specify an array of string values to match this event if the actual value of actionsSuppressedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("actions_suppressed_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def evaluation_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) evaluationState property.

                Specify an array of string values to match this event if the actual value of evaluationState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("evaluation_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reason(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) reason property.

                Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reason")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reason_data(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) reasonData property.

                Specify an array of string values to match this event if the actual value of reasonData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reason_data")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) timestamp property.

                Specify an array of string values to match this event if the actual value of timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) value property.

                Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "State(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class CloudWatchAlarmStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmStateChange",
    ):
        '''(experimental) aws.cloudwatch@CloudWatchAlarmStateChange event types for Alarm.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
            
            cloud_watch_alarm_state_change = cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmStateChange.CloudWatchAlarmStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "alarm_name": "alarmName",
                "configuration": "configuration",
                "event_metadata": "eventMetadata",
                "previous_state": "previousState",
                "state": "state",
            },
        )
        class CloudWatchAlarmStateChangeProps:
            def __init__(
                self,
                *,
                alarm_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                configuration: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmStateChange.Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                previous_state: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmStateChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
                state: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmStateChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Alarm aws.cloudwatch@CloudWatchAlarmStateChange event.

                :param alarm_name: (experimental) alarmName property. Specify an array of string values to match this event if the actual value of alarmName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Alarm reference
                :param configuration: (experimental) configuration property. Specify an array of string values to match this event if the actual value of configuration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param previous_state: (experimental) previousState property. Specify an array of string values to match this event if the actual value of previousState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    cloud_watch_alarm_state_change_props = cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.CloudWatchAlarmStateChangeProps(
                        alarm_name=["alarmName"],
                        configuration=cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.Configuration(
                            actions_suppressor=["actionsSuppressor"],
                            actions_suppressor_extension_period=["actionsSuppressorExtensionPeriod"],
                            actions_suppressor_wait_period=["actionsSuppressorWaitPeriod"],
                            alarm_rule=["alarmRule"],
                            description=["description"],
                            metrics=[cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.ConfigurationItem(
                                id=["id"],
                                metric_stat=cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.MetricStat(
                                    metric=cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.Metric(
                                        dimensions=["dimensions"],
                                        name=["name"],
                                        namespace=["namespace"]
                                    ),
                                    period=["period"],
                                    stat=["stat"]
                                ),
                                return_data=["returnData"]
                            )]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        previous_state=cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.State(
                            actions_suppressed_by=["actionsSuppressedBy"],
                            actions_suppressed_reason=["actionsSuppressedReason"],
                            evaluation_state=["evaluationState"],
                            reason=["reason"],
                            reason_data=["reasonData"],
                            timestamp=["timestamp"],
                            value=["value"]
                        ),
                        state=cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.State(
                            actions_suppressed_by=["actionsSuppressedBy"],
                            actions_suppressed_reason=["actionsSuppressedReason"],
                            evaluation_state=["evaluationState"],
                            reason=["reason"],
                            reason_data=["reasonData"],
                            timestamp=["timestamp"],
                            value=["value"]
                        )
                    )
                '''
                if isinstance(configuration, dict):
                    configuration = AlarmEvents.CloudWatchAlarmStateChange.Configuration(**configuration)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(previous_state, dict):
                    previous_state = AlarmEvents.CloudWatchAlarmStateChange.State(**previous_state)
                if isinstance(state, dict):
                    state = AlarmEvents.CloudWatchAlarmStateChange.State(**state)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8f62ec04dd9c0908f00fad9beaa3ed38baa800f01609cdbc55b74d8fab474383)
                    check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
                    check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument previous_state", value=previous_state, expected_type=type_hints["previous_state"])
                    check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if alarm_name is not None:
                    self._values["alarm_name"] = alarm_name
                if configuration is not None:
                    self._values["configuration"] = configuration
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if previous_state is not None:
                    self._values["previous_state"] = previous_state
                if state is not None:
                    self._values["state"] = state

            @builtins.property
            def alarm_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) alarmName property.

                Specify an array of string values to match this event if the actual value of alarmName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Alarm reference

                :stability: experimental
                '''
                result = self._values.get("alarm_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def configuration(
                self,
            ) -> typing.Optional["AlarmEvents.CloudWatchAlarmStateChange.Configuration"]:
                '''(experimental) configuration property.

                Specify an array of string values to match this event if the actual value of configuration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("configuration")
                return typing.cast(typing.Optional["AlarmEvents.CloudWatchAlarmStateChange.Configuration"], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def previous_state(
                self,
            ) -> typing.Optional["AlarmEvents.CloudWatchAlarmStateChange.State"]:
                '''(experimental) previousState property.

                Specify an array of string values to match this event if the actual value of previousState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("previous_state")
                return typing.cast(typing.Optional["AlarmEvents.CloudWatchAlarmStateChange.State"], result)

            @builtins.property
            def state(
                self,
            ) -> typing.Optional["AlarmEvents.CloudWatchAlarmStateChange.State"]:
                '''(experimental) state property.

                Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("state")
                return typing.cast(typing.Optional["AlarmEvents.CloudWatchAlarmStateChange.State"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CloudWatchAlarmStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmStateChange.Configuration",
            jsii_struct_bases=[],
            name_mapping={
                "actions_suppressor": "actionsSuppressor",
                "actions_suppressor_extension_period": "actionsSuppressorExtensionPeriod",
                "actions_suppressor_wait_period": "actionsSuppressorWaitPeriod",
                "alarm_rule": "alarmRule",
                "description": "description",
                "metrics": "metrics",
            },
        )
        class Configuration:
            def __init__(
                self,
                *,
                actions_suppressor: typing.Optional[typing.Sequence[builtins.str]] = None,
                actions_suppressor_extension_period: typing.Optional[typing.Sequence[builtins.str]] = None,
                actions_suppressor_wait_period: typing.Optional[typing.Sequence[builtins.str]] = None,
                alarm_rule: typing.Optional[typing.Sequence[builtins.str]] = None,
                description: typing.Optional[typing.Sequence[builtins.str]] = None,
                metrics: typing.Optional[typing.Sequence[typing.Union["AlarmEvents.CloudWatchAlarmStateChange.ConfigurationItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for Configuration.

                :param actions_suppressor: (experimental) actionsSuppressor property. Specify an array of string values to match this event if the actual value of actionsSuppressor is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param actions_suppressor_extension_period: (experimental) actionsSuppressorExtensionPeriod property. Specify an array of string values to match this event if the actual value of actionsSuppressorExtensionPeriod is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param actions_suppressor_wait_period: (experimental) actionsSuppressorWaitPeriod property. Specify an array of string values to match this event if the actual value of actionsSuppressorWaitPeriod is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param alarm_rule: (experimental) alarmRule property. Specify an array of string values to match this event if the actual value of alarmRule is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param description: (experimental) description property. Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param metrics: (experimental) metrics property. Specify an array of string values to match this event if the actual value of metrics is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    configuration = cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.Configuration(
                        actions_suppressor=["actionsSuppressor"],
                        actions_suppressor_extension_period=["actionsSuppressorExtensionPeriod"],
                        actions_suppressor_wait_period=["actionsSuppressorWaitPeriod"],
                        alarm_rule=["alarmRule"],
                        description=["description"],
                        metrics=[cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.ConfigurationItem(
                            id=["id"],
                            metric_stat=cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.MetricStat(
                                metric=cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.Metric(
                                    dimensions=["dimensions"],
                                    name=["name"],
                                    namespace=["namespace"]
                                ),
                                period=["period"],
                                stat=["stat"]
                            ),
                            return_data=["returnData"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ac14ebc2332b9422a1d9d94470c9b270a6f466cf4d4978e3fb51d643a8cf31f4)
                    check_type(argname="argument actions_suppressor", value=actions_suppressor, expected_type=type_hints["actions_suppressor"])
                    check_type(argname="argument actions_suppressor_extension_period", value=actions_suppressor_extension_period, expected_type=type_hints["actions_suppressor_extension_period"])
                    check_type(argname="argument actions_suppressor_wait_period", value=actions_suppressor_wait_period, expected_type=type_hints["actions_suppressor_wait_period"])
                    check_type(argname="argument alarm_rule", value=alarm_rule, expected_type=type_hints["alarm_rule"])
                    check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                    check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if actions_suppressor is not None:
                    self._values["actions_suppressor"] = actions_suppressor
                if actions_suppressor_extension_period is not None:
                    self._values["actions_suppressor_extension_period"] = actions_suppressor_extension_period
                if actions_suppressor_wait_period is not None:
                    self._values["actions_suppressor_wait_period"] = actions_suppressor_wait_period
                if alarm_rule is not None:
                    self._values["alarm_rule"] = alarm_rule
                if description is not None:
                    self._values["description"] = description
                if metrics is not None:
                    self._values["metrics"] = metrics

            @builtins.property
            def actions_suppressor(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionsSuppressor property.

                Specify an array of string values to match this event if the actual value of actionsSuppressor is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("actions_suppressor")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def actions_suppressor_extension_period(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionsSuppressorExtensionPeriod property.

                Specify an array of string values to match this event if the actual value of actionsSuppressorExtensionPeriod is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("actions_suppressor_extension_period")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def actions_suppressor_wait_period(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionsSuppressorWaitPeriod property.

                Specify an array of string values to match this event if the actual value of actionsSuppressorWaitPeriod is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("actions_suppressor_wait_period")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def alarm_rule(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) alarmRule property.

                Specify an array of string values to match this event if the actual value of alarmRule is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("alarm_rule")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) description property.

                Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def metrics(
                self,
            ) -> typing.Optional[typing.List["AlarmEvents.CloudWatchAlarmStateChange.ConfigurationItem"]]:
                '''(experimental) metrics property.

                Specify an array of string values to match this event if the actual value of metrics is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("metrics")
                return typing.cast(typing.Optional[typing.List["AlarmEvents.CloudWatchAlarmStateChange.ConfigurationItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Configuration(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmStateChange.ConfigurationItem",
            jsii_struct_bases=[],
            name_mapping={
                "id": "id",
                "metric_stat": "metricStat",
                "return_data": "returnData",
            },
        )
        class ConfigurationItem:
            def __init__(
                self,
                *,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                metric_stat: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmStateChange.MetricStat", typing.Dict[builtins.str, typing.Any]]] = None,
                return_data: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ConfigurationItem.

                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param metric_stat: (experimental) metricStat property. Specify an array of string values to match this event if the actual value of metricStat is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param return_data: (experimental) returnData property. Specify an array of string values to match this event if the actual value of returnData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    configuration_item = cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.ConfigurationItem(
                        id=["id"],
                        metric_stat=cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.MetricStat(
                            metric=cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.Metric(
                                dimensions=["dimensions"],
                                name=["name"],
                                namespace=["namespace"]
                            ),
                            period=["period"],
                            stat=["stat"]
                        ),
                        return_data=["returnData"]
                    )
                '''
                if isinstance(metric_stat, dict):
                    metric_stat = AlarmEvents.CloudWatchAlarmStateChange.MetricStat(**metric_stat)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b14dea84d55300835953891b421e63e39d16576747eaa49dc2c29d43f141238b)
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                    check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if id is not None:
                    self._values["id"] = id
                if metric_stat is not None:
                    self._values["metric_stat"] = metric_stat
                if return_data is not None:
                    self._values["return_data"] = return_data

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def metric_stat(
                self,
            ) -> typing.Optional["AlarmEvents.CloudWatchAlarmStateChange.MetricStat"]:
                '''(experimental) metricStat property.

                Specify an array of string values to match this event if the actual value of metricStat is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("metric_stat")
                return typing.cast(typing.Optional["AlarmEvents.CloudWatchAlarmStateChange.MetricStat"], result)

            @builtins.property
            def return_data(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) returnData property.

                Specify an array of string values to match this event if the actual value of returnData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("return_data")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ConfigurationItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmStateChange.Metric",
            jsii_struct_bases=[],
            name_mapping={
                "dimensions": "dimensions",
                "name": "name",
                "namespace": "namespace",
            },
        )
        class Metric:
            def __init__(
                self,
                *,
                dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                namespace: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Metric.

                :param dimensions: (experimental) dimensions property. Specify an array of string values to match this event if the actual value of dimensions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param namespace: (experimental) namespace property. Specify an array of string values to match this event if the actual value of namespace is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    metric = cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.Metric(
                        dimensions=["dimensions"],
                        name=["name"],
                        namespace=["namespace"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9b3dd4c2dc73f4580e4cf7412e80720a4fe7ea390f0a5add04e19484b0ef95d4)
                    check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if dimensions is not None:
                    self._values["dimensions"] = dimensions
                if name is not None:
                    self._values["name"] = name
                if namespace is not None:
                    self._values["namespace"] = namespace

            @builtins.property
            def dimensions(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) dimensions property.

                Specify an array of string values to match this event if the actual value of dimensions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("dimensions")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def namespace(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) namespace property.

                Specify an array of string values to match this event if the actual value of namespace is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("namespace")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Metric(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmStateChange.MetricStat",
            jsii_struct_bases=[],
            name_mapping={"metric": "metric", "period": "period", "stat": "stat"},
        )
        class MetricStat:
            def __init__(
                self,
                *,
                metric: typing.Optional[typing.Union["AlarmEvents.CloudWatchAlarmStateChange.Metric", typing.Dict[builtins.str, typing.Any]]] = None,
                period: typing.Optional[typing.Sequence[builtins.str]] = None,
                stat: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for MetricStat.

                :param metric: (experimental) metric property. Specify an array of string values to match this event if the actual value of metric is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param period: (experimental) period property. Specify an array of string values to match this event if the actual value of period is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param stat: (experimental) stat property. Specify an array of string values to match this event if the actual value of stat is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    metric_stat = cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.MetricStat(
                        metric=cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.Metric(
                            dimensions=["dimensions"],
                            name=["name"],
                            namespace=["namespace"]
                        ),
                        period=["period"],
                        stat=["stat"]
                    )
                '''
                if isinstance(metric, dict):
                    metric = AlarmEvents.CloudWatchAlarmStateChange.Metric(**metric)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2dd913b5a06e26531834f68b23e59196747963b0a8267b012e2e7bbab5cce539)
                    check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                    check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                    check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if metric is not None:
                    self._values["metric"] = metric
                if period is not None:
                    self._values["period"] = period
                if stat is not None:
                    self._values["stat"] = stat

            @builtins.property
            def metric(
                self,
            ) -> typing.Optional["AlarmEvents.CloudWatchAlarmStateChange.Metric"]:
                '''(experimental) metric property.

                Specify an array of string values to match this event if the actual value of metric is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("metric")
                return typing.cast(typing.Optional["AlarmEvents.CloudWatchAlarmStateChange.Metric"], result)

            @builtins.property
            def period(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) period property.

                Specify an array of string values to match this event if the actual value of period is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("period")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def stat(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) stat property.

                Specify an array of string values to match this event if the actual value of stat is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("stat")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "MetricStat(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_cloudwatch.events.AlarmEvents.CloudWatchAlarmStateChange.State",
            jsii_struct_bases=[],
            name_mapping={
                "actions_suppressed_by": "actionsSuppressedBy",
                "actions_suppressed_reason": "actionsSuppressedReason",
                "evaluation_state": "evaluationState",
                "reason": "reason",
                "reason_data": "reasonData",
                "timestamp": "timestamp",
                "value": "value",
            },
        )
        class State:
            def __init__(
                self,
                *,
                actions_suppressed_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                actions_suppressed_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                evaluation_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                reason_data: typing.Optional[typing.Sequence[builtins.str]] = None,
                timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for State.

                :param actions_suppressed_by: (experimental) actionsSuppressedBy property. Specify an array of string values to match this event if the actual value of actionsSuppressedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param actions_suppressed_reason: (experimental) actionsSuppressedReason property. Specify an array of string values to match this event if the actual value of actionsSuppressedReason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param evaluation_state: (experimental) evaluationState property. Specify an array of string values to match this event if the actual value of evaluationState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reason: (experimental) reason property. Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reason_data: (experimental) reasonData property. Specify an array of string values to match this event if the actual value of reasonData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param timestamp: (experimental) timestamp property. Specify an array of string values to match this event if the actual value of timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) value property. Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_cloudwatch import events as cloudwatch_events
                    
                    state = cloudwatch_events.AlarmEvents.CloudWatchAlarmStateChange.State(
                        actions_suppressed_by=["actionsSuppressedBy"],
                        actions_suppressed_reason=["actionsSuppressedReason"],
                        evaluation_state=["evaluationState"],
                        reason=["reason"],
                        reason_data=["reasonData"],
                        timestamp=["timestamp"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e23ae20487972ed250265c82a340c98f3715410bf02c9f5ec5e2c26abf9ff7fa)
                    check_type(argname="argument actions_suppressed_by", value=actions_suppressed_by, expected_type=type_hints["actions_suppressed_by"])
                    check_type(argname="argument actions_suppressed_reason", value=actions_suppressed_reason, expected_type=type_hints["actions_suppressed_reason"])
                    check_type(argname="argument evaluation_state", value=evaluation_state, expected_type=type_hints["evaluation_state"])
                    check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                    check_type(argname="argument reason_data", value=reason_data, expected_type=type_hints["reason_data"])
                    check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if actions_suppressed_by is not None:
                    self._values["actions_suppressed_by"] = actions_suppressed_by
                if actions_suppressed_reason is not None:
                    self._values["actions_suppressed_reason"] = actions_suppressed_reason
                if evaluation_state is not None:
                    self._values["evaluation_state"] = evaluation_state
                if reason is not None:
                    self._values["reason"] = reason
                if reason_data is not None:
                    self._values["reason_data"] = reason_data
                if timestamp is not None:
                    self._values["timestamp"] = timestamp
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def actions_suppressed_by(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionsSuppressedBy property.

                Specify an array of string values to match this event if the actual value of actionsSuppressedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("actions_suppressed_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def actions_suppressed_reason(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionsSuppressedReason property.

                Specify an array of string values to match this event if the actual value of actionsSuppressedReason is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("actions_suppressed_reason")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def evaluation_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) evaluationState property.

                Specify an array of string values to match this event if the actual value of evaluationState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("evaluation_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reason(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) reason property.

                Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reason")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reason_data(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) reasonData property.

                Specify an array of string values to match this event if the actual value of reasonData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reason_data")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) timestamp property.

                Specify an array of string values to match this event if the actual value of timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) value property.

                Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "State(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "AlarmEvents",
]

publication.publish()

def _typecheckingstub__dfedb8223a728c521f2f96cbc6b0a5a2f336b8264804d3fc51b8c64dfdd9f644(
    alarm_ref: _aws_cdk_interfaces_aws_cloudwatch_ceddda9d.IAlarmRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c949f9d9cc04995a1acd74b0575f55b469dba8d9d009a92c793223851c375d1(
    *,
    alarm_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[typing.Union[AlarmEvents.CloudWatchAlarmConfigurationChange.Configuration, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    operation: typing.Optional[typing.Sequence[builtins.str]] = None,
    state: typing.Optional[typing.Union[AlarmEvents.CloudWatchAlarmConfigurationChange.State, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c790c20f69b305a4ac13bba65b1eac52cae96f3bd21af1feaf371b62b243e75(
    *,
    actions_enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
    actions_suppressor: typing.Optional[typing.Sequence[builtins.str]] = None,
    actions_suppressor_extension_period: typing.Optional[typing.Sequence[builtins.str]] = None,
    actions_suppressor_wait_period: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_rule: typing.Optional[typing.Sequence[builtins.str]] = None,
    comparison_operator: typing.Optional[typing.Sequence[builtins.str]] = None,
    datapoints_to_alarm: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[typing.Sequence[builtins.str]] = None,
    evaluate_low_sample_count_percentile: typing.Optional[typing.Sequence[builtins.str]] = None,
    evaluation_periods: typing.Optional[typing.Sequence[builtins.str]] = None,
    insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics: typing.Optional[typing.Sequence[typing.Union[AlarmEvents.CloudWatchAlarmConfigurationChange.ConfigurationItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
    timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89860ca8465d7cef68689e8f51ffcdc938017f70370f0ecc136eb6fad40f10ec(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_stat: typing.Optional[typing.Union[AlarmEvents.CloudWatchAlarmConfigurationChange.MetricStat, typing.Dict[builtins.str, typing.Any]]] = None,
    return_data: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3308f0c752817e082b18e7e8fe611acd993dd177e4575a482f8dfff4845cec68(
    *,
    dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d23a40bfad6a396c253113929154661ae45e177d3bef018fde9a893320447c(
    *,
    metric: typing.Optional[typing.Union[AlarmEvents.CloudWatchAlarmConfigurationChange.Metric, typing.Dict[builtins.str, typing.Any]]] = None,
    period: typing.Optional[typing.Sequence[builtins.str]] = None,
    stat: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bc1df6e51e53bd98de18565d400ab6daac354962d5250c87635e1fe269e673(
    *,
    actions_suppressed_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    evaluation_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    reason_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f62ec04dd9c0908f00fad9beaa3ed38baa800f01609cdbc55b74d8fab474383(
    *,
    alarm_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[typing.Union[AlarmEvents.CloudWatchAlarmStateChange.Configuration, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    previous_state: typing.Optional[typing.Union[AlarmEvents.CloudWatchAlarmStateChange.State, typing.Dict[builtins.str, typing.Any]]] = None,
    state: typing.Optional[typing.Union[AlarmEvents.CloudWatchAlarmStateChange.State, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac14ebc2332b9422a1d9d94470c9b270a6f466cf4d4978e3fb51d643a8cf31f4(
    *,
    actions_suppressor: typing.Optional[typing.Sequence[builtins.str]] = None,
    actions_suppressor_extension_period: typing.Optional[typing.Sequence[builtins.str]] = None,
    actions_suppressor_wait_period: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_rule: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics: typing.Optional[typing.Sequence[typing.Union[AlarmEvents.CloudWatchAlarmStateChange.ConfigurationItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14dea84d55300835953891b421e63e39d16576747eaa49dc2c29d43f141238b(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_stat: typing.Optional[typing.Union[AlarmEvents.CloudWatchAlarmStateChange.MetricStat, typing.Dict[builtins.str, typing.Any]]] = None,
    return_data: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3dd4c2dc73f4580e4cf7412e80720a4fe7ea390f0a5add04e19484b0ef95d4(
    *,
    dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd913b5a06e26531834f68b23e59196747963b0a8267b012e2e7bbab5cce539(
    *,
    metric: typing.Optional[typing.Union[AlarmEvents.CloudWatchAlarmStateChange.Metric, typing.Dict[builtins.str, typing.Any]]] = None,
    period: typing.Optional[typing.Sequence[builtins.str]] = None,
    stat: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e23ae20487972ed250265c82a340c98f3715410bf02c9f5ec5e2c26abf9ff7fa(
    *,
    actions_suppressed_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    actions_suppressed_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    evaluation_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    reason_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
