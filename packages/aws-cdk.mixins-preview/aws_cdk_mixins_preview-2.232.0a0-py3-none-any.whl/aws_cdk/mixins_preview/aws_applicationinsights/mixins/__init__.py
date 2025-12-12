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
    jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attach_missing_permission": "attachMissingPermission",
        "auto_configuration_enabled": "autoConfigurationEnabled",
        "component_monitoring_settings": "componentMonitoringSettings",
        "custom_components": "customComponents",
        "cwe_monitor_enabled": "cweMonitorEnabled",
        "grouping_type": "groupingType",
        "log_pattern_sets": "logPatternSets",
        "ops_center_enabled": "opsCenterEnabled",
        "ops_item_sns_topic_arn": "opsItemSnsTopicArn",
        "resource_group_name": "resourceGroupName",
        "sns_notification_arn": "snsNotificationArn",
        "tags": "tags",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        attach_missing_permission: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        auto_configuration_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        component_monitoring_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ComponentMonitoringSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        custom_components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.CustomComponentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        cwe_monitor_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        grouping_type: typing.Optional[builtins.str] = None,
        log_pattern_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.LogPatternSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ops_center_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ops_item_sns_topic_arn: typing.Optional[builtins.str] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
        sns_notification_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param attach_missing_permission: If set to true, the managed policies for SSM and CW will be attached to the instance roles if they are missing.
        :param auto_configuration_enabled: If set to ``true`` , the application components will be configured with the monitoring configuration recommended by Application Insights.
        :param component_monitoring_settings: The monitoring settings of the components. Not required to set up default monitoring for all components. To set up default monitoring for all components, set ``AutoConfigurationEnabled`` to ``true`` .
        :param custom_components: Describes a custom component by grouping similar standalone instances to monitor.
        :param cwe_monitor_enabled: Indicates whether Application Insights can listen to CloudWatch events for the application resources, such as ``instance terminated`` , ``failed deployment`` , and others.
        :param grouping_type: Application Insights can create applications based on a resource group or on an account. To create an account-based application using all of the resources in the account, set this parameter to ``ACCOUNT_BASED`` .
        :param log_pattern_sets: The log pattern sets.
        :param ops_center_enabled: Indicates whether Application Insights will create OpsItems for any problem that is detected by Application Insights for an application.
        :param ops_item_sns_topic_arn: The SNS topic provided to Application Insights that is associated with the created OpsItems to receive SNS notifications for opsItem updates.
        :param resource_group_name: The name of the resource group used for the application.
        :param sns_notification_arn: The SNS topic ARN that is associated with SNS notifications for updates or issues.
        :param tags: An array of ``Tags`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
            
            cfn_application_mixin_props = applicationinsights_mixins.CfnApplicationMixinProps(
                attach_missing_permission=False,
                auto_configuration_enabled=False,
                component_monitoring_settings=[applicationinsights_mixins.CfnApplicationPropsMixin.ComponentMonitoringSettingProperty(
                    component_arn="componentArn",
                    component_configuration_mode="componentConfigurationMode",
                    component_name="componentName",
                    custom_component_configuration=applicationinsights_mixins.CfnApplicationPropsMixin.ComponentConfigurationProperty(
                        configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.ConfigurationDetailsProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            alarms=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmProperty(
                                alarm_name="alarmName",
                                severity="severity"
                            )],
                            ha_cluster_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty(
                                prometheus_port="prometheusPort"
                            ),
                            hana_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HANAPrometheusExporterProperty(
                                agree_to_install_hanadb_client=False,
                                hana_port="hanaPort",
                                hana_secret_name="hanaSecretName",
                                hanasid="hanasid",
                                prometheus_port="prometheusPort"
                            ),
                            jmx_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.JMXPrometheusExporterProperty(
                                host_port="hostPort",
                                jmxurl="jmxurl",
                                prometheus_port="prometheusPort"
                            ),
                            logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                encoding="encoding",
                                log_group_name="logGroupName",
                                log_path="logPath",
                                log_type="logType",
                                pattern_set="patternSet"
                            )],
                            net_weaver_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty(
                                instance_numbers=["instanceNumbers"],
                                prometheus_port="prometheusPort",
                                sapsid="sapsid"
                            ),
                            processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                process_name="processName"
                            )],
                            sql_server_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty(
                                prometheus_port="prometheusPort",
                                sql_secret_name="sqlSecretName"
                            ),
                            windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                event_levels=["eventLevels"],
                                event_name="eventName",
                                log_group_name="logGroupName",
                                pattern_set="patternSet"
                            )]
                        ),
                        sub_component_type_configurations=[applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty(
                            sub_component_configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                    encoding="encoding",
                                    log_group_name="logGroupName",
                                    log_path="logPath",
                                    log_type="logType",
                                    pattern_set="patternSet"
                                )],
                                processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                    alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                        alarm_metric_name="alarmMetricName"
                                    )],
                                    process_name="processName"
                                )],
                                windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                    event_levels=["eventLevels"],
                                    event_name="eventName",
                                    log_group_name="logGroupName",
                                    pattern_set="patternSet"
                                )]
                            ),
                            sub_component_type="subComponentType"
                        )]
                    ),
                    default_overwrite_component_configuration=applicationinsights_mixins.CfnApplicationPropsMixin.ComponentConfigurationProperty(
                        configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.ConfigurationDetailsProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            alarms=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmProperty(
                                alarm_name="alarmName",
                                severity="severity"
                            )],
                            ha_cluster_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty(
                                prometheus_port="prometheusPort"
                            ),
                            hana_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HANAPrometheusExporterProperty(
                                agree_to_install_hanadb_client=False,
                                hana_port="hanaPort",
                                hana_secret_name="hanaSecretName",
                                hanasid="hanasid",
                                prometheus_port="prometheusPort"
                            ),
                            jmx_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.JMXPrometheusExporterProperty(
                                host_port="hostPort",
                                jmxurl="jmxurl",
                                prometheus_port="prometheusPort"
                            ),
                            logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                encoding="encoding",
                                log_group_name="logGroupName",
                                log_path="logPath",
                                log_type="logType",
                                pattern_set="patternSet"
                            )],
                            net_weaver_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty(
                                instance_numbers=["instanceNumbers"],
                                prometheus_port="prometheusPort",
                                sapsid="sapsid"
                            ),
                            processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                process_name="processName"
                            )],
                            sql_server_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty(
                                prometheus_port="prometheusPort",
                                sql_secret_name="sqlSecretName"
                            ),
                            windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                event_levels=["eventLevels"],
                                event_name="eventName",
                                log_group_name="logGroupName",
                                pattern_set="patternSet"
                            )]
                        ),
                        sub_component_type_configurations=[applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty(
                            sub_component_configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                    encoding="encoding",
                                    log_group_name="logGroupName",
                                    log_path="logPath",
                                    log_type="logType",
                                    pattern_set="patternSet"
                                )],
                                processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                    alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                        alarm_metric_name="alarmMetricName"
                                    )],
                                    process_name="processName"
                                )],
                                windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                    event_levels=["eventLevels"],
                                    event_name="eventName",
                                    log_group_name="logGroupName",
                                    pattern_set="patternSet"
                                )]
                            ),
                            sub_component_type="subComponentType"
                        )]
                    ),
                    tier="tier"
                )],
                custom_components=[applicationinsights_mixins.CfnApplicationPropsMixin.CustomComponentProperty(
                    component_name="componentName",
                    resource_list=["resourceList"]
                )],
                cwe_monitor_enabled=False,
                grouping_type="groupingType",
                log_pattern_sets=[applicationinsights_mixins.CfnApplicationPropsMixin.LogPatternSetProperty(
                    log_patterns=[applicationinsights_mixins.CfnApplicationPropsMixin.LogPatternProperty(
                        pattern="pattern",
                        pattern_name="patternName",
                        rank=123
                    )],
                    pattern_set_name="patternSetName"
                )],
                ops_center_enabled=False,
                ops_item_sns_topic_arn="opsItemSnsTopicArn",
                resource_group_name="resourceGroupName",
                sns_notification_arn="snsNotificationArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e3fde3cc8b2dde899af2d49c09bba109a1797c9096254438145bc385782fb3)
            check_type(argname="argument attach_missing_permission", value=attach_missing_permission, expected_type=type_hints["attach_missing_permission"])
            check_type(argname="argument auto_configuration_enabled", value=auto_configuration_enabled, expected_type=type_hints["auto_configuration_enabled"])
            check_type(argname="argument component_monitoring_settings", value=component_monitoring_settings, expected_type=type_hints["component_monitoring_settings"])
            check_type(argname="argument custom_components", value=custom_components, expected_type=type_hints["custom_components"])
            check_type(argname="argument cwe_monitor_enabled", value=cwe_monitor_enabled, expected_type=type_hints["cwe_monitor_enabled"])
            check_type(argname="argument grouping_type", value=grouping_type, expected_type=type_hints["grouping_type"])
            check_type(argname="argument log_pattern_sets", value=log_pattern_sets, expected_type=type_hints["log_pattern_sets"])
            check_type(argname="argument ops_center_enabled", value=ops_center_enabled, expected_type=type_hints["ops_center_enabled"])
            check_type(argname="argument ops_item_sns_topic_arn", value=ops_item_sns_topic_arn, expected_type=type_hints["ops_item_sns_topic_arn"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sns_notification_arn", value=sns_notification_arn, expected_type=type_hints["sns_notification_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attach_missing_permission is not None:
            self._values["attach_missing_permission"] = attach_missing_permission
        if auto_configuration_enabled is not None:
            self._values["auto_configuration_enabled"] = auto_configuration_enabled
        if component_monitoring_settings is not None:
            self._values["component_monitoring_settings"] = component_monitoring_settings
        if custom_components is not None:
            self._values["custom_components"] = custom_components
        if cwe_monitor_enabled is not None:
            self._values["cwe_monitor_enabled"] = cwe_monitor_enabled
        if grouping_type is not None:
            self._values["grouping_type"] = grouping_type
        if log_pattern_sets is not None:
            self._values["log_pattern_sets"] = log_pattern_sets
        if ops_center_enabled is not None:
            self._values["ops_center_enabled"] = ops_center_enabled
        if ops_item_sns_topic_arn is not None:
            self._values["ops_item_sns_topic_arn"] = ops_item_sns_topic_arn
        if resource_group_name is not None:
            self._values["resource_group_name"] = resource_group_name
        if sns_notification_arn is not None:
            self._values["sns_notification_arn"] = sns_notification_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def attach_missing_permission(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If set to true, the managed policies for SSM and CW will be attached to the instance roles if they are missing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-attachmissingpermission
        '''
        result = self._values.get("attach_missing_permission")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def auto_configuration_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If set to ``true`` , the application components will be configured with the monitoring configuration recommended by Application Insights.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-autoconfigurationenabled
        '''
        result = self._values.get("auto_configuration_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def component_monitoring_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ComponentMonitoringSettingProperty"]]]]:
        '''The monitoring settings of the components.

        Not required to set up default monitoring for all components. To set up default monitoring for all components, set ``AutoConfigurationEnabled`` to ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-componentmonitoringsettings
        '''
        result = self._values.get("component_monitoring_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ComponentMonitoringSettingProperty"]]]], result)

    @builtins.property
    def custom_components(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CustomComponentProperty"]]]]:
        '''Describes a custom component by grouping similar standalone instances to monitor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-customcomponents
        '''
        result = self._values.get("custom_components")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CustomComponentProperty"]]]], result)

    @builtins.property
    def cwe_monitor_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether Application Insights can listen to CloudWatch events for the application resources, such as ``instance terminated`` , ``failed deployment`` , and others.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-cwemonitorenabled
        '''
        result = self._values.get("cwe_monitor_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def grouping_type(self) -> typing.Optional[builtins.str]:
        '''Application Insights can create applications based on a resource group or on an account.

        To create an account-based application using all of the resources in the account, set this parameter to ``ACCOUNT_BASED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-groupingtype
        '''
        result = self._values.get("grouping_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_pattern_sets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.LogPatternSetProperty"]]]]:
        '''The log pattern sets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-logpatternsets
        '''
        result = self._values.get("log_pattern_sets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.LogPatternSetProperty"]]]], result)

    @builtins.property
    def ops_center_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether Application Insights will create OpsItems for any problem that is detected by Application Insights for an application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-opscenterenabled
        '''
        result = self._values.get("ops_center_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def ops_item_sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The SNS topic provided to Application Insights that is associated with the created OpsItems to receive SNS notifications for opsItem updates.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-opsitemsnstopicarn
        '''
        result = self._values.get("ops_item_sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource group used for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-resourcegroupname
        '''
        result = self._values.get("resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_notification_arn(self) -> typing.Optional[builtins.str]:
        '''The SNS topic ARN that is associated with SNS notifications for updates or issues.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-snsnotificationarn
        '''
        result = self._values.get("sns_notification_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of ``Tags`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin",
):
    '''The ``AWS::ApplicationInsights::Application`` resource adds an application that is created from a resource group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html
    :cloudformationResource: AWS::ApplicationInsights::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
        
        cfn_application_props_mixin = applicationinsights_mixins.CfnApplicationPropsMixin(applicationinsights_mixins.CfnApplicationMixinProps(
            attach_missing_permission=False,
            auto_configuration_enabled=False,
            component_monitoring_settings=[applicationinsights_mixins.CfnApplicationPropsMixin.ComponentMonitoringSettingProperty(
                component_arn="componentArn",
                component_configuration_mode="componentConfigurationMode",
                component_name="componentName",
                custom_component_configuration=applicationinsights_mixins.CfnApplicationPropsMixin.ComponentConfigurationProperty(
                    configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.ConfigurationDetailsProperty(
                        alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                            alarm_metric_name="alarmMetricName"
                        )],
                        alarms=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmProperty(
                            alarm_name="alarmName",
                            severity="severity"
                        )],
                        ha_cluster_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty(
                            prometheus_port="prometheusPort"
                        ),
                        hana_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HANAPrometheusExporterProperty(
                            agree_to_install_hanadb_client=False,
                            hana_port="hanaPort",
                            hana_secret_name="hanaSecretName",
                            hanasid="hanasid",
                            prometheus_port="prometheusPort"
                        ),
                        jmx_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.JMXPrometheusExporterProperty(
                            host_port="hostPort",
                            jmxurl="jmxurl",
                            prometheus_port="prometheusPort"
                        ),
                        logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                            encoding="encoding",
                            log_group_name="logGroupName",
                            log_path="logPath",
                            log_type="logType",
                            pattern_set="patternSet"
                        )],
                        net_weaver_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty(
                            instance_numbers=["instanceNumbers"],
                            prometheus_port="prometheusPort",
                            sapsid="sapsid"
                        ),
                        processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            process_name="processName"
                        )],
                        sql_server_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty(
                            prometheus_port="prometheusPort",
                            sql_secret_name="sqlSecretName"
                        ),
                        windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                            event_levels=["eventLevels"],
                            event_name="eventName",
                            log_group_name="logGroupName",
                            pattern_set="patternSet"
                        )]
                    ),
                    sub_component_type_configurations=[applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty(
                        sub_component_configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                encoding="encoding",
                                log_group_name="logGroupName",
                                log_path="logPath",
                                log_type="logType",
                                pattern_set="patternSet"
                            )],
                            processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                process_name="processName"
                            )],
                            windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                event_levels=["eventLevels"],
                                event_name="eventName",
                                log_group_name="logGroupName",
                                pattern_set="patternSet"
                            )]
                        ),
                        sub_component_type="subComponentType"
                    )]
                ),
                default_overwrite_component_configuration=applicationinsights_mixins.CfnApplicationPropsMixin.ComponentConfigurationProperty(
                    configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.ConfigurationDetailsProperty(
                        alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                            alarm_metric_name="alarmMetricName"
                        )],
                        alarms=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmProperty(
                            alarm_name="alarmName",
                            severity="severity"
                        )],
                        ha_cluster_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty(
                            prometheus_port="prometheusPort"
                        ),
                        hana_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HANAPrometheusExporterProperty(
                            agree_to_install_hanadb_client=False,
                            hana_port="hanaPort",
                            hana_secret_name="hanaSecretName",
                            hanasid="hanasid",
                            prometheus_port="prometheusPort"
                        ),
                        jmx_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.JMXPrometheusExporterProperty(
                            host_port="hostPort",
                            jmxurl="jmxurl",
                            prometheus_port="prometheusPort"
                        ),
                        logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                            encoding="encoding",
                            log_group_name="logGroupName",
                            log_path="logPath",
                            log_type="logType",
                            pattern_set="patternSet"
                        )],
                        net_weaver_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty(
                            instance_numbers=["instanceNumbers"],
                            prometheus_port="prometheusPort",
                            sapsid="sapsid"
                        ),
                        processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            process_name="processName"
                        )],
                        sql_server_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty(
                            prometheus_port="prometheusPort",
                            sql_secret_name="sqlSecretName"
                        ),
                        windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                            event_levels=["eventLevels"],
                            event_name="eventName",
                            log_group_name="logGroupName",
                            pattern_set="patternSet"
                        )]
                    ),
                    sub_component_type_configurations=[applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty(
                        sub_component_configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                encoding="encoding",
                                log_group_name="logGroupName",
                                log_path="logPath",
                                log_type="logType",
                                pattern_set="patternSet"
                            )],
                            processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                process_name="processName"
                            )],
                            windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                event_levels=["eventLevels"],
                                event_name="eventName",
                                log_group_name="logGroupName",
                                pattern_set="patternSet"
                            )]
                        ),
                        sub_component_type="subComponentType"
                    )]
                ),
                tier="tier"
            )],
            custom_components=[applicationinsights_mixins.CfnApplicationPropsMixin.CustomComponentProperty(
                component_name="componentName",
                resource_list=["resourceList"]
            )],
            cwe_monitor_enabled=False,
            grouping_type="groupingType",
            log_pattern_sets=[applicationinsights_mixins.CfnApplicationPropsMixin.LogPatternSetProperty(
                log_patterns=[applicationinsights_mixins.CfnApplicationPropsMixin.LogPatternProperty(
                    pattern="pattern",
                    pattern_name="patternName",
                    rank=123
                )],
                pattern_set_name="patternSetName"
            )],
            ops_center_enabled=False,
            ops_item_sns_topic_arn="opsItemSnsTopicArn",
            resource_group_name="resourceGroupName",
            sns_notification_arn="snsNotificationArn",
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
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApplicationInsights::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85dab4dea343662add15b4e49a1491a295ec7410f225eb3f5a0d6f14bafff05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c20fe79b5f2cd79201740b369008868c9bafff9d07abcadd2faa7d7a8e1c95ed)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57ca457a7fcda7c2ba5e410e279076bc9ce8011cb4eb01afde641a5313ea115)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationMixinProps:
        return typing.cast(CfnApplicationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.AlarmMetricProperty",
        jsii_struct_bases=[],
        name_mapping={"alarm_metric_name": "alarmMetricName"},
    )
    class AlarmMetricProperty:
        def __init__(
            self,
            *,
            alarm_metric_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application AlarmMetric`` property type defines a metric to monitor for the component.

            :param alarm_metric_name: The name of the metric to be monitored for the component. For metrics supported by Application Insights, see `Logs and metrics supported by Amazon CloudWatch Application Insights <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/appinsights-logs-and-metrics.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-alarmmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                alarm_metric_property = applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                    alarm_metric_name="alarmMetricName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa6adf210ceb915eba02a6cb040001096a872593c12dee8492560ef5047a68ee)
                check_type(argname="argument alarm_metric_name", value=alarm_metric_name, expected_type=type_hints["alarm_metric_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_metric_name is not None:
                self._values["alarm_metric_name"] = alarm_metric_name

        @builtins.property
        def alarm_metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric to be monitored for the component.

            For metrics supported by Application Insights, see `Logs and metrics supported by Amazon CloudWatch Application Insights <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/appinsights-logs-and-metrics.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-alarmmetric.html#cfn-applicationinsights-application-alarmmetric-alarmmetricname
            '''
            result = self._values.get("alarm_metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.AlarmProperty",
        jsii_struct_bases=[],
        name_mapping={"alarm_name": "alarmName", "severity": "severity"},
    )
    class AlarmProperty:
        def __init__(
            self,
            *,
            alarm_name: typing.Optional[builtins.str] = None,
            severity: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application Alarm`` property type defines a CloudWatch alarm to be monitored for the component.

            :param alarm_name: The name of the CloudWatch alarm to be monitored for the component.
            :param severity: Indicates the degree of outage when the alarm goes off.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-alarm.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                alarm_property = applicationinsights_mixins.CfnApplicationPropsMixin.AlarmProperty(
                    alarm_name="alarmName",
                    severity="severity"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b9b6f3b11f51016f1b074f5e099780037fe9c7394c133247550548612d937f8)
                check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
                check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_name is not None:
                self._values["alarm_name"] = alarm_name
            if severity is not None:
                self._values["severity"] = severity

        @builtins.property
        def alarm_name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch alarm to be monitored for the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-alarm.html#cfn-applicationinsights-application-alarm-alarmname
            '''
            result = self._values.get("alarm_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def severity(self) -> typing.Optional[builtins.str]:
            '''Indicates the degree of outage when the alarm goes off.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-alarm.html#cfn-applicationinsights-application-alarm-severity
            '''
            result = self._values.get("severity")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.ComponentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration_details": "configurationDetails",
            "sub_component_type_configurations": "subComponentTypeConfigurations",
        },
    )
    class ComponentConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ConfigurationDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sub_component_type_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application ComponentConfiguration`` property type defines the configuration settings of the component.

            :param configuration_details: The configuration settings.
            :param sub_component_type_configurations: Sub-component configurations of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                component_configuration_property = applicationinsights_mixins.CfnApplicationPropsMixin.ComponentConfigurationProperty(
                    configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.ConfigurationDetailsProperty(
                        alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                            alarm_metric_name="alarmMetricName"
                        )],
                        alarms=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmProperty(
                            alarm_name="alarmName",
                            severity="severity"
                        )],
                        ha_cluster_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty(
                            prometheus_port="prometheusPort"
                        ),
                        hana_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HANAPrometheusExporterProperty(
                            agree_to_install_hanadb_client=False,
                            hana_port="hanaPort",
                            hana_secret_name="hanaSecretName",
                            hanasid="hanasid",
                            prometheus_port="prometheusPort"
                        ),
                        jmx_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.JMXPrometheusExporterProperty(
                            host_port="hostPort",
                            jmxurl="jmxurl",
                            prometheus_port="prometheusPort"
                        ),
                        logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                            encoding="encoding",
                            log_group_name="logGroupName",
                            log_path="logPath",
                            log_type="logType",
                            pattern_set="patternSet"
                        )],
                        net_weaver_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty(
                            instance_numbers=["instanceNumbers"],
                            prometheus_port="prometheusPort",
                            sapsid="sapsid"
                        ),
                        processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            process_name="processName"
                        )],
                        sql_server_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty(
                            prometheus_port="prometheusPort",
                            sql_secret_name="sqlSecretName"
                        ),
                        windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                            event_levels=["eventLevels"],
                            event_name="eventName",
                            log_group_name="logGroupName",
                            pattern_set="patternSet"
                        )]
                    ),
                    sub_component_type_configurations=[applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty(
                        sub_component_configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                encoding="encoding",
                                log_group_name="logGroupName",
                                log_path="logPath",
                                log_type="logType",
                                pattern_set="patternSet"
                            )],
                            processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                process_name="processName"
                            )],
                            windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                event_levels=["eventLevels"],
                                event_name="eventName",
                                log_group_name="logGroupName",
                                pattern_set="patternSet"
                            )]
                        ),
                        sub_component_type="subComponentType"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14550e0ef50e809d77347856fd90499e813f34a093389ed252e9263bc2685055)
                check_type(argname="argument configuration_details", value=configuration_details, expected_type=type_hints["configuration_details"])
                check_type(argname="argument sub_component_type_configurations", value=sub_component_type_configurations, expected_type=type_hints["sub_component_type_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration_details is not None:
                self._values["configuration_details"] = configuration_details
            if sub_component_type_configurations is not None:
                self._values["sub_component_type_configurations"] = sub_component_type_configurations

        @builtins.property
        def configuration_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ConfigurationDetailsProperty"]]:
            '''The configuration settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentconfiguration.html#cfn-applicationinsights-application-componentconfiguration-configurationdetails
            '''
            result = self._values.get("configuration_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ConfigurationDetailsProperty"]], result)

        @builtins.property
        def sub_component_type_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty"]]]]:
            '''Sub-component configurations of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentconfiguration.html#cfn-applicationinsights-application-componentconfiguration-subcomponenttypeconfigurations
            '''
            result = self._values.get("sub_component_type_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.ComponentMonitoringSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_arn": "componentArn",
            "component_configuration_mode": "componentConfigurationMode",
            "component_name": "componentName",
            "custom_component_configuration": "customComponentConfiguration",
            "default_overwrite_component_configuration": "defaultOverwriteComponentConfiguration",
            "tier": "tier",
        },
    )
    class ComponentMonitoringSettingProperty:
        def __init__(
            self,
            *,
            component_arn: typing.Optional[builtins.str] = None,
            component_configuration_mode: typing.Optional[builtins.str] = None,
            component_name: typing.Optional[builtins.str] = None,
            custom_component_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ComponentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_overwrite_component_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ComponentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application ComponentMonitoringSetting`` property type defines the monitoring setting of the component.

            :param component_arn: The ARN of the component. Either the component ARN or the component name is required.
            :param component_configuration_mode: Component monitoring can be configured in one of the following three modes:. - ``DEFAULT`` : The component will be configured with the recommended default monitoring settings of the selected ``Tier`` . - ``CUSTOM`` : The component will be configured with the customized monitoring settings that are specified in ``CustomComponentConfiguration`` . If used, ``CustomComponentConfiguration`` must be provided. - ``DEFAULT_WITH_OVERWRITE`` : The component will be configured with the recommended default monitoring settings of the selected ``Tier`` , and merged with customized overwrite settings that are specified in ``DefaultOverwriteComponentConfiguration`` . If used, ``DefaultOverwriteComponentConfiguration`` must be provided.
            :param component_name: The name of the component. Either the component ARN or the component name is required.
            :param custom_component_configuration: Customized monitoring settings. Required if CUSTOM mode is configured in ``ComponentConfigurationMode`` .
            :param default_overwrite_component_configuration: Customized overwrite monitoring settings. Required if CUSTOM mode is configured in ``ComponentConfigurationMode`` .
            :param tier: The tier of the application component. Supported tiers include ``DOT_NET_CORE`` , ``DOT_NET_WORKER`` , ``DOT_NET_WEB`` , ``SQL_SERVER`` , ``SQL_SERVER_ALWAYSON_AVAILABILITY_GROUP`` , ``SQL_SERVER_FAILOVER_CLUSTER_INSTANCE`` , ``MYSQL`` , ``POSTGRESQL`` , ``JAVA_JMX`` , ``ORACLE`` , ``SAP_HANA_MULTI_NODE`` , ``SAP_HANA_SINGLE_NODE`` , ``SAP_HANA_HIGH_AVAILABILITY`` , ``SHAREPOINT`` . ``ACTIVE_DIRECTORY`` , and ``DEFAULT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                component_monitoring_setting_property = applicationinsights_mixins.CfnApplicationPropsMixin.ComponentMonitoringSettingProperty(
                    component_arn="componentArn",
                    component_configuration_mode="componentConfigurationMode",
                    component_name="componentName",
                    custom_component_configuration=applicationinsights_mixins.CfnApplicationPropsMixin.ComponentConfigurationProperty(
                        configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.ConfigurationDetailsProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            alarms=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmProperty(
                                alarm_name="alarmName",
                                severity="severity"
                            )],
                            ha_cluster_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty(
                                prometheus_port="prometheusPort"
                            ),
                            hana_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HANAPrometheusExporterProperty(
                                agree_to_install_hanadb_client=False,
                                hana_port="hanaPort",
                                hana_secret_name="hanaSecretName",
                                hanasid="hanasid",
                                prometheus_port="prometheusPort"
                            ),
                            jmx_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.JMXPrometheusExporterProperty(
                                host_port="hostPort",
                                jmxurl="jmxurl",
                                prometheus_port="prometheusPort"
                            ),
                            logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                encoding="encoding",
                                log_group_name="logGroupName",
                                log_path="logPath",
                                log_type="logType",
                                pattern_set="patternSet"
                            )],
                            net_weaver_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty(
                                instance_numbers=["instanceNumbers"],
                                prometheus_port="prometheusPort",
                                sapsid="sapsid"
                            ),
                            processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                process_name="processName"
                            )],
                            sql_server_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty(
                                prometheus_port="prometheusPort",
                                sql_secret_name="sqlSecretName"
                            ),
                            windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                event_levels=["eventLevels"],
                                event_name="eventName",
                                log_group_name="logGroupName",
                                pattern_set="patternSet"
                            )]
                        ),
                        sub_component_type_configurations=[applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty(
                            sub_component_configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                    encoding="encoding",
                                    log_group_name="logGroupName",
                                    log_path="logPath",
                                    log_type="logType",
                                    pattern_set="patternSet"
                                )],
                                processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                    alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                        alarm_metric_name="alarmMetricName"
                                    )],
                                    process_name="processName"
                                )],
                                windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                    event_levels=["eventLevels"],
                                    event_name="eventName",
                                    log_group_name="logGroupName",
                                    pattern_set="patternSet"
                                )]
                            ),
                            sub_component_type="subComponentType"
                        )]
                    ),
                    default_overwrite_component_configuration=applicationinsights_mixins.CfnApplicationPropsMixin.ComponentConfigurationProperty(
                        configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.ConfigurationDetailsProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            alarms=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmProperty(
                                alarm_name="alarmName",
                                severity="severity"
                            )],
                            ha_cluster_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty(
                                prometheus_port="prometheusPort"
                            ),
                            hana_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HANAPrometheusExporterProperty(
                                agree_to_install_hanadb_client=False,
                                hana_port="hanaPort",
                                hana_secret_name="hanaSecretName",
                                hanasid="hanasid",
                                prometheus_port="prometheusPort"
                            ),
                            jmx_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.JMXPrometheusExporterProperty(
                                host_port="hostPort",
                                jmxurl="jmxurl",
                                prometheus_port="prometheusPort"
                            ),
                            logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                encoding="encoding",
                                log_group_name="logGroupName",
                                log_path="logPath",
                                log_type="logType",
                                pattern_set="patternSet"
                            )],
                            net_weaver_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty(
                                instance_numbers=["instanceNumbers"],
                                prometheus_port="prometheusPort",
                                sapsid="sapsid"
                            ),
                            processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                process_name="processName"
                            )],
                            sql_server_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty(
                                prometheus_port="prometheusPort",
                                sql_secret_name="sqlSecretName"
                            ),
                            windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                event_levels=["eventLevels"],
                                event_name="eventName",
                                log_group_name="logGroupName",
                                pattern_set="patternSet"
                            )]
                        ),
                        sub_component_type_configurations=[applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty(
                            sub_component_configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty(
                                alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                    alarm_metric_name="alarmMetricName"
                                )],
                                logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                                    encoding="encoding",
                                    log_group_name="logGroupName",
                                    log_path="logPath",
                                    log_type="logType",
                                    pattern_set="patternSet"
                                )],
                                processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                                    alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                        alarm_metric_name="alarmMetricName"
                                    )],
                                    process_name="processName"
                                )],
                                windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                                    event_levels=["eventLevels"],
                                    event_name="eventName",
                                    log_group_name="logGroupName",
                                    pattern_set="patternSet"
                                )]
                            ),
                            sub_component_type="subComponentType"
                        )]
                    ),
                    tier="tier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e34eea997c7e0698894f939dfc555db45f64eefaa8921bc0a4ecf664b6ce8572)
                check_type(argname="argument component_arn", value=component_arn, expected_type=type_hints["component_arn"])
                check_type(argname="argument component_configuration_mode", value=component_configuration_mode, expected_type=type_hints["component_configuration_mode"])
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument custom_component_configuration", value=custom_component_configuration, expected_type=type_hints["custom_component_configuration"])
                check_type(argname="argument default_overwrite_component_configuration", value=default_overwrite_component_configuration, expected_type=type_hints["default_overwrite_component_configuration"])
                check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_arn is not None:
                self._values["component_arn"] = component_arn
            if component_configuration_mode is not None:
                self._values["component_configuration_mode"] = component_configuration_mode
            if component_name is not None:
                self._values["component_name"] = component_name
            if custom_component_configuration is not None:
                self._values["custom_component_configuration"] = custom_component_configuration
            if default_overwrite_component_configuration is not None:
                self._values["default_overwrite_component_configuration"] = default_overwrite_component_configuration
            if tier is not None:
                self._values["tier"] = tier

        @builtins.property
        def component_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the component.

            Either the component ARN or the component name is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-componentarn
            '''
            result = self._values.get("component_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def component_configuration_mode(self) -> typing.Optional[builtins.str]:
            '''Component monitoring can be configured in one of the following three modes:.

            - ``DEFAULT`` : The component will be configured with the recommended default monitoring settings of the selected ``Tier`` .
            - ``CUSTOM`` : The component will be configured with the customized monitoring settings that are specified in ``CustomComponentConfiguration`` . If used, ``CustomComponentConfiguration`` must be provided.
            - ``DEFAULT_WITH_OVERWRITE`` : The component will be configured with the recommended default monitoring settings of the selected ``Tier`` , and merged with customized overwrite settings that are specified in ``DefaultOverwriteComponentConfiguration`` . If used, ``DefaultOverwriteComponentConfiguration`` must be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-componentconfigurationmode
            '''
            result = self._values.get("component_configuration_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component.

            Either the component ARN or the component name is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_component_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ComponentConfigurationProperty"]]:
            '''Customized monitoring settings.

            Required if CUSTOM mode is configured in ``ComponentConfigurationMode`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-customcomponentconfiguration
            '''
            result = self._values.get("custom_component_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ComponentConfigurationProperty"]], result)

        @builtins.property
        def default_overwrite_component_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ComponentConfigurationProperty"]]:
            '''Customized overwrite monitoring settings.

            Required if CUSTOM mode is configured in ``ComponentConfigurationMode`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-defaultoverwritecomponentconfiguration
            '''
            result = self._values.get("default_overwrite_component_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ComponentConfigurationProperty"]], result)

        @builtins.property
        def tier(self) -> typing.Optional[builtins.str]:
            '''The tier of the application component.

            Supported tiers include ``DOT_NET_CORE`` , ``DOT_NET_WORKER`` , ``DOT_NET_WEB`` , ``SQL_SERVER`` , ``SQL_SERVER_ALWAYSON_AVAILABILITY_GROUP`` , ``SQL_SERVER_FAILOVER_CLUSTER_INSTANCE`` , ``MYSQL`` , ``POSTGRESQL`` , ``JAVA_JMX`` , ``ORACLE`` , ``SAP_HANA_MULTI_NODE`` , ``SAP_HANA_SINGLE_NODE`` , ``SAP_HANA_HIGH_AVAILABILITY`` , ``SHAREPOINT`` . ``ACTIVE_DIRECTORY`` , and ``DEFAULT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-tier
            '''
            result = self._values.get("tier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentMonitoringSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.ConfigurationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarm_metrics": "alarmMetrics",
            "alarms": "alarms",
            "ha_cluster_prometheus_exporter": "haClusterPrometheusExporter",
            "hana_prometheus_exporter": "hanaPrometheusExporter",
            "jmx_prometheus_exporter": "jmxPrometheusExporter",
            "logs": "logs",
            "net_weaver_prometheus_exporter": "netWeaverPrometheusExporter",
            "processes": "processes",
            "sql_server_prometheus_exporter": "sqlServerPrometheusExporter",
            "windows_events": "windowsEvents",
        },
    )
    class ConfigurationDetailsProperty:
        def __init__(
            self,
            *,
            alarm_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.AlarmMetricProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            alarms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.AlarmProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ha_cluster_prometheus_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hana_prometheus_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.HANAPrometheusExporterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            jmx_prometheus_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.JMXPrometheusExporterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.LogProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            net_weaver_prometheus_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            processes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ProcessProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            sql_server_prometheus_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            windows_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.WindowsEventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application ConfigurationDetails`` property type specifies the configuration settings.

            :param alarm_metrics: A list of metrics to monitor for the component. All component types can use ``AlarmMetrics`` .
            :param alarms: A list of alarms to monitor for the component. All component types can use ``Alarm`` .
            :param ha_cluster_prometheus_exporter: The HA cluster Prometheus Exporter settings.
            :param hana_prometheus_exporter: The HANA DB Prometheus Exporter settings.
            :param jmx_prometheus_exporter: A list of Java metrics to monitor for the component.
            :param logs: A list of logs to monitor for the component. Only Amazon EC2 instances can use ``Logs`` .
            :param net_weaver_prometheus_exporter: The NetWeaver Prometheus Exporter Settings.
            :param processes: A list of processes to monitor for the component. Only Windows EC2 instances can have a processes section.
            :param sql_server_prometheus_exporter: The SQL prometheus exporter settings.
            :param windows_events: A list of Windows Events to monitor for the component. Only Amazon EC2 instances running on Windows can use ``WindowsEvents`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                configuration_details_property = applicationinsights_mixins.CfnApplicationPropsMixin.ConfigurationDetailsProperty(
                    alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                        alarm_metric_name="alarmMetricName"
                    )],
                    alarms=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmProperty(
                        alarm_name="alarmName",
                        severity="severity"
                    )],
                    ha_cluster_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty(
                        prometheus_port="prometheusPort"
                    ),
                    hana_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.HANAPrometheusExporterProperty(
                        agree_to_install_hanadb_client=False,
                        hana_port="hanaPort",
                        hana_secret_name="hanaSecretName",
                        hanasid="hanasid",
                        prometheus_port="prometheusPort"
                    ),
                    jmx_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.JMXPrometheusExporterProperty(
                        host_port="hostPort",
                        jmxurl="jmxurl",
                        prometheus_port="prometheusPort"
                    ),
                    logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                        encoding="encoding",
                        log_group_name="logGroupName",
                        log_path="logPath",
                        log_type="logType",
                        pattern_set="patternSet"
                    )],
                    net_weaver_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty(
                        instance_numbers=["instanceNumbers"],
                        prometheus_port="prometheusPort",
                        sapsid="sapsid"
                    ),
                    processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                        alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                            alarm_metric_name="alarmMetricName"
                        )],
                        process_name="processName"
                    )],
                    sql_server_prometheus_exporter=applicationinsights_mixins.CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty(
                        prometheus_port="prometheusPort",
                        sql_secret_name="sqlSecretName"
                    ),
                    windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                        event_levels=["eventLevels"],
                        event_name="eventName",
                        log_group_name="logGroupName",
                        pattern_set="patternSet"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6c7713ac24e97562db7158acb26683bfbf7b907c0202fcef833d42c465e7d4c)
                check_type(argname="argument alarm_metrics", value=alarm_metrics, expected_type=type_hints["alarm_metrics"])
                check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
                check_type(argname="argument ha_cluster_prometheus_exporter", value=ha_cluster_prometheus_exporter, expected_type=type_hints["ha_cluster_prometheus_exporter"])
                check_type(argname="argument hana_prometheus_exporter", value=hana_prometheus_exporter, expected_type=type_hints["hana_prometheus_exporter"])
                check_type(argname="argument jmx_prometheus_exporter", value=jmx_prometheus_exporter, expected_type=type_hints["jmx_prometheus_exporter"])
                check_type(argname="argument logs", value=logs, expected_type=type_hints["logs"])
                check_type(argname="argument net_weaver_prometheus_exporter", value=net_weaver_prometheus_exporter, expected_type=type_hints["net_weaver_prometheus_exporter"])
                check_type(argname="argument processes", value=processes, expected_type=type_hints["processes"])
                check_type(argname="argument sql_server_prometheus_exporter", value=sql_server_prometheus_exporter, expected_type=type_hints["sql_server_prometheus_exporter"])
                check_type(argname="argument windows_events", value=windows_events, expected_type=type_hints["windows_events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_metrics is not None:
                self._values["alarm_metrics"] = alarm_metrics
            if alarms is not None:
                self._values["alarms"] = alarms
            if ha_cluster_prometheus_exporter is not None:
                self._values["ha_cluster_prometheus_exporter"] = ha_cluster_prometheus_exporter
            if hana_prometheus_exporter is not None:
                self._values["hana_prometheus_exporter"] = hana_prometheus_exporter
            if jmx_prometheus_exporter is not None:
                self._values["jmx_prometheus_exporter"] = jmx_prometheus_exporter
            if logs is not None:
                self._values["logs"] = logs
            if net_weaver_prometheus_exporter is not None:
                self._values["net_weaver_prometheus_exporter"] = net_weaver_prometheus_exporter
            if processes is not None:
                self._values["processes"] = processes
            if sql_server_prometheus_exporter is not None:
                self._values["sql_server_prometheus_exporter"] = sql_server_prometheus_exporter
            if windows_events is not None:
                self._values["windows_events"] = windows_events

        @builtins.property
        def alarm_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AlarmMetricProperty"]]]]:
            '''A list of metrics to monitor for the component.

            All component types can use ``AlarmMetrics`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-alarmmetrics
            '''
            result = self._values.get("alarm_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AlarmMetricProperty"]]]], result)

        @builtins.property
        def alarms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AlarmProperty"]]]]:
            '''A list of alarms to monitor for the component.

            All component types can use ``Alarm`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-alarms
            '''
            result = self._values.get("alarms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AlarmProperty"]]]], result)

        @builtins.property
        def ha_cluster_prometheus_exporter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty"]]:
            '''The HA cluster Prometheus Exporter settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-haclusterprometheusexporter
            '''
            result = self._values.get("ha_cluster_prometheus_exporter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty"]], result)

        @builtins.property
        def hana_prometheus_exporter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.HANAPrometheusExporterProperty"]]:
            '''The HANA DB Prometheus Exporter settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-hanaprometheusexporter
            '''
            result = self._values.get("hana_prometheus_exporter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.HANAPrometheusExporterProperty"]], result)

        @builtins.property
        def jmx_prometheus_exporter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.JMXPrometheusExporterProperty"]]:
            '''A list of Java metrics to monitor for the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-jmxprometheusexporter
            '''
            result = self._values.get("jmx_prometheus_exporter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.JMXPrometheusExporterProperty"]], result)

        @builtins.property
        def logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.LogProperty"]]]]:
            '''A list of logs to monitor for the component.

            Only Amazon EC2 instances can use ``Logs`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-logs
            '''
            result = self._values.get("logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.LogProperty"]]]], result)

        @builtins.property
        def net_weaver_prometheus_exporter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty"]]:
            '''The NetWeaver Prometheus Exporter Settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-netweaverprometheusexporter
            '''
            result = self._values.get("net_weaver_prometheus_exporter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty"]], result)

        @builtins.property
        def processes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ProcessProperty"]]]]:
            '''A list of processes to monitor for the component.

            Only Windows EC2 instances can have a processes section.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-processes
            '''
            result = self._values.get("processes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ProcessProperty"]]]], result)

        @builtins.property
        def sql_server_prometheus_exporter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty"]]:
            '''The SQL prometheus exporter settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-sqlserverprometheusexporter
            '''
            result = self._values.get("sql_server_prometheus_exporter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty"]], result)

        @builtins.property
        def windows_events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.WindowsEventProperty"]]]]:
            '''A list of Windows Events to monitor for the component.

            Only Amazon EC2 instances running on Windows can use ``WindowsEvents`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-windowsevents
            '''
            result = self._values.get("windows_events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.WindowsEventProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.CustomComponentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_name": "componentName",
            "resource_list": "resourceList",
        },
    )
    class CustomComponentProperty:
        def __init__(
            self,
            *,
            component_name: typing.Optional[builtins.str] = None,
            resource_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application CustomComponent`` property type describes a custom component by grouping similar standalone instances to monitor.

            :param component_name: The name of the component.
            :param resource_list: The list of resource ARNs that belong to the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-customcomponent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                custom_component_property = applicationinsights_mixins.CfnApplicationPropsMixin.CustomComponentProperty(
                    component_name="componentName",
                    resource_list=["resourceList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__daacc2d873a165fb5f2e4d9c45287b2965111ed45068aa730750a7dbbd188a97)
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument resource_list", value=resource_list, expected_type=type_hints["resource_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_name is not None:
                self._values["component_name"] = component_name
            if resource_list is not None:
                self._values["resource_list"] = resource_list

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-customcomponent.html#cfn-applicationinsights-application-customcomponent-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of resource ARNs that belong to the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-customcomponent.html#cfn-applicationinsights-application-customcomponent-resourcelist
            '''
            result = self._values.get("resource_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomComponentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty",
        jsii_struct_bases=[],
        name_mapping={"prometheus_port": "prometheusPort"},
    )
    class HAClusterPrometheusExporterProperty:
        def __init__(
            self,
            *,
            prometheus_port: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application HAClusterPrometheusExporter`` property type defines the HA cluster Prometheus Exporter settings.

            For more information, see the `component configuration <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/component-config-sections.html#component-configuration-prometheus>`_ in the CloudWatch Application Insights documentation.

            :param prometheus_port: The target port to which Prometheus sends metrics. If not specified, the default port 9668 is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-haclusterprometheusexporter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                h_aCluster_prometheus_exporter_property = applicationinsights_mixins.CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty(
                    prometheus_port="prometheusPort"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cbd2203e6ff9f31888e8a29118f4f7b7f41dd36c4a1087bb996320cd58323a49)
                check_type(argname="argument prometheus_port", value=prometheus_port, expected_type=type_hints["prometheus_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if prometheus_port is not None:
                self._values["prometheus_port"] = prometheus_port

        @builtins.property
        def prometheus_port(self) -> typing.Optional[builtins.str]:
            '''The target port to which Prometheus sends metrics.

            If not specified, the default port 9668 is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-haclusterprometheusexporter.html#cfn-applicationinsights-application-haclusterprometheusexporter-prometheusport
            '''
            result = self._values.get("prometheus_port")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HAClusterPrometheusExporterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.HANAPrometheusExporterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "agree_to_install_hanadb_client": "agreeToInstallHanadbClient",
            "hana_port": "hanaPort",
            "hana_secret_name": "hanaSecretName",
            "hanasid": "hanasid",
            "prometheus_port": "prometheusPort",
        },
    )
    class HANAPrometheusExporterProperty:
        def __init__(
            self,
            *,
            agree_to_install_hanadb_client: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            hana_port: typing.Optional[builtins.str] = None,
            hana_secret_name: typing.Optional[builtins.str] = None,
            hanasid: typing.Optional[builtins.str] = None,
            prometheus_port: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application HANAPrometheusExporter`` property type defines the HANA DB Prometheus Exporter settings.

            For more information, see the `component configuration <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/component-config-sections.html#component-configuration-prometheus>`_ in the CloudWatch Application Insights documentation.

            :param agree_to_install_hanadb_client: Designates whether you agree to install the HANA DB client.
            :param hana_port: The HANA database port by which the exporter will query HANA metrics.
            :param hana_secret_name: The AWS Secrets Manager secret that stores HANA monitoring user credentials. The HANA Prometheus exporter uses these credentials to connect to the database and query HANA metrics.
            :param hanasid: The three-character SAP system ID (SID) of the SAP HANA system.
            :param prometheus_port: The target port to which Prometheus sends metrics. If not specified, the default port 9668 is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-hanaprometheusexporter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                h_aNAPrometheus_exporter_property = applicationinsights_mixins.CfnApplicationPropsMixin.HANAPrometheusExporterProperty(
                    agree_to_install_hanadb_client=False,
                    hana_port="hanaPort",
                    hana_secret_name="hanaSecretName",
                    hanasid="hanasid",
                    prometheus_port="prometheusPort"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b32d9c703d80c2a6a82172107cf08da270d32b865c8043c109a53586f8833419)
                check_type(argname="argument agree_to_install_hanadb_client", value=agree_to_install_hanadb_client, expected_type=type_hints["agree_to_install_hanadb_client"])
                check_type(argname="argument hana_port", value=hana_port, expected_type=type_hints["hana_port"])
                check_type(argname="argument hana_secret_name", value=hana_secret_name, expected_type=type_hints["hana_secret_name"])
                check_type(argname="argument hanasid", value=hanasid, expected_type=type_hints["hanasid"])
                check_type(argname="argument prometheus_port", value=prometheus_port, expected_type=type_hints["prometheus_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if agree_to_install_hanadb_client is not None:
                self._values["agree_to_install_hanadb_client"] = agree_to_install_hanadb_client
            if hana_port is not None:
                self._values["hana_port"] = hana_port
            if hana_secret_name is not None:
                self._values["hana_secret_name"] = hana_secret_name
            if hanasid is not None:
                self._values["hanasid"] = hanasid
            if prometheus_port is not None:
                self._values["prometheus_port"] = prometheus_port

        @builtins.property
        def agree_to_install_hanadb_client(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Designates whether you agree to install the HANA DB client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-hanaprometheusexporter.html#cfn-applicationinsights-application-hanaprometheusexporter-agreetoinstallhanadbclient
            '''
            result = self._values.get("agree_to_install_hanadb_client")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def hana_port(self) -> typing.Optional[builtins.str]:
            '''The HANA database port by which the exporter will query HANA metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-hanaprometheusexporter.html#cfn-applicationinsights-application-hanaprometheusexporter-hanaport
            '''
            result = self._values.get("hana_port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hana_secret_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Secrets Manager secret that stores HANA monitoring user credentials.

            The HANA Prometheus exporter uses these credentials to connect to the database and query HANA metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-hanaprometheusexporter.html#cfn-applicationinsights-application-hanaprometheusexporter-hanasecretname
            '''
            result = self._values.get("hana_secret_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hanasid(self) -> typing.Optional[builtins.str]:
            '''The three-character SAP system ID (SID) of the SAP HANA system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-hanaprometheusexporter.html#cfn-applicationinsights-application-hanaprometheusexporter-hanasid
            '''
            result = self._values.get("hanasid")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prometheus_port(self) -> typing.Optional[builtins.str]:
            '''The target port to which Prometheus sends metrics.

            If not specified, the default port 9668 is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-hanaprometheusexporter.html#cfn-applicationinsights-application-hanaprometheusexporter-prometheusport
            '''
            result = self._values.get("prometheus_port")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HANAPrometheusExporterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.JMXPrometheusExporterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "host_port": "hostPort",
            "jmxurl": "jmxurl",
            "prometheus_port": "prometheusPort",
        },
    )
    class JMXPrometheusExporterProperty:
        def __init__(
            self,
            *,
            host_port: typing.Optional[builtins.str] = None,
            jmxurl: typing.Optional[builtins.str] = None,
            prometheus_port: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application JMXPrometheusExporter`` property type defines the JMXPrometheus Exporter configuration.

            For more information, see the `component configuration <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/component-config-sections.html#component-configuration-prometheus>`_ in the CloudWatch Application Insights documentation.

            :param host_port: The host and port to connect to through remote JMX. Only one of ``jmxURL`` and ``hostPort`` can be specified.
            :param jmxurl: The complete JMX URL to connect to.
            :param prometheus_port: The target port to send Prometheus metrics to. If not specified, the default port ``9404`` is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-jmxprometheusexporter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                j_mXPrometheus_exporter_property = applicationinsights_mixins.CfnApplicationPropsMixin.JMXPrometheusExporterProperty(
                    host_port="hostPort",
                    jmxurl="jmxurl",
                    prometheus_port="prometheusPort"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e81cea9bb7a339d83e3b693a1c7f3baf77003bec74ab79065568d5f58c877e4)
                check_type(argname="argument host_port", value=host_port, expected_type=type_hints["host_port"])
                check_type(argname="argument jmxurl", value=jmxurl, expected_type=type_hints["jmxurl"])
                check_type(argname="argument prometheus_port", value=prometheus_port, expected_type=type_hints["prometheus_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if host_port is not None:
                self._values["host_port"] = host_port
            if jmxurl is not None:
                self._values["jmxurl"] = jmxurl
            if prometheus_port is not None:
                self._values["prometheus_port"] = prometheus_port

        @builtins.property
        def host_port(self) -> typing.Optional[builtins.str]:
            '''The host and port to connect to through remote JMX.

            Only one of ``jmxURL`` and ``hostPort`` can be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-jmxprometheusexporter.html#cfn-applicationinsights-application-jmxprometheusexporter-hostport
            '''
            result = self._values.get("host_port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def jmxurl(self) -> typing.Optional[builtins.str]:
            '''The complete JMX URL to connect to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-jmxprometheusexporter.html#cfn-applicationinsights-application-jmxprometheusexporter-jmxurl
            '''
            result = self._values.get("jmxurl")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prometheus_port(self) -> typing.Optional[builtins.str]:
            '''The target port to send Prometheus metrics to.

            If not specified, the default port ``9404`` is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-jmxprometheusexporter.html#cfn-applicationinsights-application-jmxprometheusexporter-prometheusport
            '''
            result = self._values.get("prometheus_port")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JMXPrometheusExporterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.LogPatternProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "pattern_name": "patternName",
            "rank": "rank",
        },
    )
    class LogPatternProperty:
        def __init__(
            self,
            *,
            pattern: typing.Optional[builtins.str] = None,
            pattern_name: typing.Optional[builtins.str] = None,
            rank: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application LogPattern`` property type specifies an object that defines the log patterns that belong to a ``LogPatternSet`` .

            :param pattern: A regular expression that defines the log pattern. A log pattern can contain up to 50 characters, and it cannot be empty.
            :param pattern_name: The name of the log pattern. A log pattern name can contain up to 50 characters, and it cannot be empty. The characters can be Unicode letters, digits, or one of the following symbols: period, dash, underscore.
            :param rank: The rank of the log pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpattern.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                log_pattern_property = applicationinsights_mixins.CfnApplicationPropsMixin.LogPatternProperty(
                    pattern="pattern",
                    pattern_name="patternName",
                    rank=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c9f14d103e5c8b6f242befe7cfce91442581800fa54c7c135bc79f45acc5bcb)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
                check_type(argname="argument pattern_name", value=pattern_name, expected_type=type_hints["pattern_name"])
                check_type(argname="argument rank", value=rank, expected_type=type_hints["rank"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pattern is not None:
                self._values["pattern"] = pattern
            if pattern_name is not None:
                self._values["pattern_name"] = pattern_name
            if rank is not None:
                self._values["rank"] = rank

        @builtins.property
        def pattern(self) -> typing.Optional[builtins.str]:
            '''A regular expression that defines the log pattern.

            A log pattern can contain up to 50 characters, and it cannot be empty.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpattern.html#cfn-applicationinsights-application-logpattern-pattern
            '''
            result = self._values.get("pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern_name(self) -> typing.Optional[builtins.str]:
            '''The name of the log pattern.

            A log pattern name can contain up to 50 characters, and it cannot be empty. The characters can be Unicode letters, digits, or one of the following symbols: period, dash, underscore.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpattern.html#cfn-applicationinsights-application-logpattern-patternname
            '''
            result = self._values.get("pattern_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rank(self) -> typing.Optional[jsii.Number]:
            '''The rank of the log pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpattern.html#cfn-applicationinsights-application-logpattern-rank
            '''
            result = self._values.get("rank")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogPatternProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.LogPatternSetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_patterns": "logPatterns",
            "pattern_set_name": "patternSetName",
        },
    )
    class LogPatternSetProperty:
        def __init__(
            self,
            *,
            log_patterns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.LogPatternProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            pattern_set_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application LogPatternSet`` property type specifies the log pattern set.

            :param log_patterns: A list of objects that define the log patterns that belong to ``LogPatternSet`` .
            :param pattern_set_name: The name of the log pattern. A log pattern name can contain up to 30 characters, and it cannot be empty. The characters can be Unicode letters, digits, or one of the following symbols: period, dash, underscore.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpatternset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                log_pattern_set_property = applicationinsights_mixins.CfnApplicationPropsMixin.LogPatternSetProperty(
                    log_patterns=[applicationinsights_mixins.CfnApplicationPropsMixin.LogPatternProperty(
                        pattern="pattern",
                        pattern_name="patternName",
                        rank=123
                    )],
                    pattern_set_name="patternSetName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34ec901581d5736b15f70ecaceb53849ec97ed1be2e09a718734f1baa2c48267)
                check_type(argname="argument log_patterns", value=log_patterns, expected_type=type_hints["log_patterns"])
                check_type(argname="argument pattern_set_name", value=pattern_set_name, expected_type=type_hints["pattern_set_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_patterns is not None:
                self._values["log_patterns"] = log_patterns
            if pattern_set_name is not None:
                self._values["pattern_set_name"] = pattern_set_name

        @builtins.property
        def log_patterns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.LogPatternProperty"]]]]:
            '''A list of objects that define the log patterns that belong to ``LogPatternSet`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpatternset.html#cfn-applicationinsights-application-logpatternset-logpatterns
            '''
            result = self._values.get("log_patterns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.LogPatternProperty"]]]], result)

        @builtins.property
        def pattern_set_name(self) -> typing.Optional[builtins.str]:
            '''The name of the log pattern.

            A log pattern name can contain up to 30 characters, and it cannot be empty. The characters can be Unicode letters, digits, or one of the following symbols: period, dash, underscore.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpatternset.html#cfn-applicationinsights-application-logpatternset-patternsetname
            '''
            result = self._values.get("pattern_set_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogPatternSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.LogProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encoding": "encoding",
            "log_group_name": "logGroupName",
            "log_path": "logPath",
            "log_type": "logType",
            "pattern_set": "patternSet",
        },
    )
    class LogProperty:
        def __init__(
            self,
            *,
            encoding: typing.Optional[builtins.str] = None,
            log_group_name: typing.Optional[builtins.str] = None,
            log_path: typing.Optional[builtins.str] = None,
            log_type: typing.Optional[builtins.str] = None,
            pattern_set: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application Log`` property type specifies a log to monitor for the component.

            :param encoding: The type of encoding of the logs to be monitored. The specified encoding should be included in the list of CloudWatch agent supported encodings. If not provided, CloudWatch Application Insights uses the default encoding type for the log type: - ``APPLICATION/DEFAULT`` : utf-8 encoding - ``SQL_SERVER`` : utf-16 encoding - ``IIS`` : ascii encoding
            :param log_group_name: The CloudWatch log group name to be associated with the monitored log.
            :param log_path: The path of the logs to be monitored. The log path must be an absolute Windows or Linux system file path. For more information, see `CloudWatch Agent Configuration File: Logs Section <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html#CloudWatch-Agent-Configuration-File-Logssection>`_ .
            :param log_type: The log type decides the log patterns against which Application Insights analyzes the log. The log type is selected from the following: ``SQL_SERVER`` , ``MYSQL`` , ``MYSQL_SLOW_QUERY`` , ``POSTGRESQL`` , ``ORACLE_ALERT`` , ``ORACLE_LISTENER`` , ``IIS`` , ``APPLICATION`` , ``WINDOWS_EVENTS`` , ``WINDOWS_EVENTS_ACTIVE_DIRECTORY`` , ``WINDOWS_EVENTS_DNS`` , ``WINDOWS_EVENTS_IIS`` , ``WINDOWS_EVENTS_SHAREPOINT`` , ``SQL_SERVER_ALWAYSON_AVAILABILITY_GROUP`` , ``SQL_SERVER_FAILOVER_CLUSTER_INSTANCE`` , ``STEP_FUNCTION`` , ``API_GATEWAY_ACCESS`` , ``API_GATEWAY_EXECUTION`` , ``SAP_HANA_LOGS`` , ``SAP_HANA_TRACE`` , ``SAP_HANA_HIGH_AVAILABILITY`` , and ``DEFAULT`` .
            :param pattern_set: The log pattern set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                log_property = applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                    encoding="encoding",
                    log_group_name="logGroupName",
                    log_path="logPath",
                    log_type="logType",
                    pattern_set="patternSet"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e77b1460b427399f4d38e2f5432a723a40661f8459b090b297629b6d5eaf1b20)
                check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                check_type(argname="argument log_path", value=log_path, expected_type=type_hints["log_path"])
                check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
                check_type(argname="argument pattern_set", value=pattern_set, expected_type=type_hints["pattern_set"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encoding is not None:
                self._values["encoding"] = encoding
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_path is not None:
                self._values["log_path"] = log_path
            if log_type is not None:
                self._values["log_type"] = log_type
            if pattern_set is not None:
                self._values["pattern_set"] = pattern_set

        @builtins.property
        def encoding(self) -> typing.Optional[builtins.str]:
            '''The type of encoding of the logs to be monitored.

            The specified encoding should be included in the list of CloudWatch agent supported encodings. If not provided, CloudWatch Application Insights uses the default encoding type for the log type:

            - ``APPLICATION/DEFAULT`` : utf-8 encoding
            - ``SQL_SERVER`` : utf-16 encoding
            - ``IIS`` : ascii encoding

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html#cfn-applicationinsights-application-log-encoding
            '''
            result = self._values.get("encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The CloudWatch log group name to be associated with the monitored log.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html#cfn-applicationinsights-application-log-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_path(self) -> typing.Optional[builtins.str]:
            '''The path of the logs to be monitored.

            The log path must be an absolute Windows or Linux system file path. For more information, see `CloudWatch Agent Configuration File: Logs Section <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html#CloudWatch-Agent-Configuration-File-Logssection>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html#cfn-applicationinsights-application-log-logpath
            '''
            result = self._values.get("log_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_type(self) -> typing.Optional[builtins.str]:
            '''The log type decides the log patterns against which Application Insights analyzes the log.

            The log type is selected from the following: ``SQL_SERVER`` , ``MYSQL`` , ``MYSQL_SLOW_QUERY`` , ``POSTGRESQL`` , ``ORACLE_ALERT`` , ``ORACLE_LISTENER`` , ``IIS`` , ``APPLICATION`` , ``WINDOWS_EVENTS`` , ``WINDOWS_EVENTS_ACTIVE_DIRECTORY`` , ``WINDOWS_EVENTS_DNS`` , ``WINDOWS_EVENTS_IIS`` , ``WINDOWS_EVENTS_SHAREPOINT`` , ``SQL_SERVER_ALWAYSON_AVAILABILITY_GROUP`` , ``SQL_SERVER_FAILOVER_CLUSTER_INSTANCE`` , ``STEP_FUNCTION`` , ``API_GATEWAY_ACCESS`` , ``API_GATEWAY_EXECUTION`` , ``SAP_HANA_LOGS`` , ``SAP_HANA_TRACE`` , ``SAP_HANA_HIGH_AVAILABILITY`` , and ``DEFAULT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html#cfn-applicationinsights-application-log-logtype
            '''
            result = self._values.get("log_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern_set(self) -> typing.Optional[builtins.str]:
            '''The log pattern set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html#cfn-applicationinsights-application-log-patternset
            '''
            result = self._values.get("pattern_set")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_numbers": "instanceNumbers",
            "prometheus_port": "prometheusPort",
            "sapsid": "sapsid",
        },
    )
    class NetWeaverPrometheusExporterProperty:
        def __init__(
            self,
            *,
            instance_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
            prometheus_port: typing.Optional[builtins.str] = None,
            sapsid: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The NetWeaver Prometheus Exporter Settings.

            :param instance_numbers: SAP instance numbers for ASCS, ERS, and App Servers.
            :param prometheus_port: Prometheus exporter port.
            :param sapsid: SAP NetWeaver SID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-netweaverprometheusexporter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                net_weaver_prometheus_exporter_property = applicationinsights_mixins.CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty(
                    instance_numbers=["instanceNumbers"],
                    prometheus_port="prometheusPort",
                    sapsid="sapsid"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b736c127f5328f28cb73f30b977af1512b7fa11e18b6274c014719cddfff4c3b)
                check_type(argname="argument instance_numbers", value=instance_numbers, expected_type=type_hints["instance_numbers"])
                check_type(argname="argument prometheus_port", value=prometheus_port, expected_type=type_hints["prometheus_port"])
                check_type(argname="argument sapsid", value=sapsid, expected_type=type_hints["sapsid"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_numbers is not None:
                self._values["instance_numbers"] = instance_numbers
            if prometheus_port is not None:
                self._values["prometheus_port"] = prometheus_port
            if sapsid is not None:
                self._values["sapsid"] = sapsid

        @builtins.property
        def instance_numbers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''SAP instance numbers for ASCS, ERS, and App Servers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-netweaverprometheusexporter.html#cfn-applicationinsights-application-netweaverprometheusexporter-instancenumbers
            '''
            result = self._values.get("instance_numbers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def prometheus_port(self) -> typing.Optional[builtins.str]:
            '''Prometheus exporter port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-netweaverprometheusexporter.html#cfn-applicationinsights-application-netweaverprometheusexporter-prometheusport
            '''
            result = self._values.get("prometheus_port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sapsid(self) -> typing.Optional[builtins.str]:
            '''SAP NetWeaver SID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-netweaverprometheusexporter.html#cfn-applicationinsights-application-netweaverprometheusexporter-sapsid
            '''
            result = self._values.get("sapsid")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetWeaverPrometheusExporterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.ProcessProperty",
        jsii_struct_bases=[],
        name_mapping={"alarm_metrics": "alarmMetrics", "process_name": "processName"},
    )
    class ProcessProperty:
        def __init__(
            self,
            *,
            alarm_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.AlarmMetricProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            process_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A process to be monitored for the component.

            :param alarm_metrics: A list of metrics to monitor for the component.
            :param process_name: The name of the process to be monitored for the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-process.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                process_property = applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                    alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                        alarm_metric_name="alarmMetricName"
                    )],
                    process_name="processName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e761ea749f4d131dc45630fbcbaca7cc736e83707b5d9c18e3c96d865d4c74fb)
                check_type(argname="argument alarm_metrics", value=alarm_metrics, expected_type=type_hints["alarm_metrics"])
                check_type(argname="argument process_name", value=process_name, expected_type=type_hints["process_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_metrics is not None:
                self._values["alarm_metrics"] = alarm_metrics
            if process_name is not None:
                self._values["process_name"] = process_name

        @builtins.property
        def alarm_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AlarmMetricProperty"]]]]:
            '''A list of metrics to monitor for the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-process.html#cfn-applicationinsights-application-process-alarmmetrics
            '''
            result = self._values.get("alarm_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AlarmMetricProperty"]]]], result)

        @builtins.property
        def process_name(self) -> typing.Optional[builtins.str]:
            '''The name of the process to be monitored for the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-process.html#cfn-applicationinsights-application-process-processname
            '''
            result = self._values.get("process_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "prometheus_port": "prometheusPort",
            "sql_secret_name": "sqlSecretName",
        },
    )
    class SQLServerPrometheusExporterProperty:
        def __init__(
            self,
            *,
            prometheus_port: typing.Optional[builtins.str] = None,
            sql_secret_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The SQL prometheus exporter settings.

            :param prometheus_port: Prometheus exporter port.
            :param sql_secret_name: Secret name which managers SQL exporter connection. e.g. {"data_source_name": "sqlserver://:@localhost:1433"}

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-sqlserverprometheusexporter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                s_qLServer_prometheus_exporter_property = applicationinsights_mixins.CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty(
                    prometheus_port="prometheusPort",
                    sql_secret_name="sqlSecretName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5897898d6c83caf6881880d7a934ee2ce2c9001154c11053989d6408f41a2285)
                check_type(argname="argument prometheus_port", value=prometheus_port, expected_type=type_hints["prometheus_port"])
                check_type(argname="argument sql_secret_name", value=sql_secret_name, expected_type=type_hints["sql_secret_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if prometheus_port is not None:
                self._values["prometheus_port"] = prometheus_port
            if sql_secret_name is not None:
                self._values["sql_secret_name"] = sql_secret_name

        @builtins.property
        def prometheus_port(self) -> typing.Optional[builtins.str]:
            '''Prometheus exporter port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-sqlserverprometheusexporter.html#cfn-applicationinsights-application-sqlserverprometheusexporter-prometheusport
            '''
            result = self._values.get("prometheus_port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sql_secret_name(self) -> typing.Optional[builtins.str]:
            '''Secret name which managers SQL exporter connection.

            e.g. {"data_source_name": "sqlserver://:@localhost:1433"}

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-sqlserverprometheusexporter.html#cfn-applicationinsights-application-sqlserverprometheusexporter-sqlsecretname
            '''
            result = self._values.get("sql_secret_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SQLServerPrometheusExporterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarm_metrics": "alarmMetrics",
            "logs": "logs",
            "processes": "processes",
            "windows_events": "windowsEvents",
        },
    )
    class SubComponentConfigurationDetailsProperty:
        def __init__(
            self,
            *,
            alarm_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.AlarmMetricProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.LogProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            processes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ProcessProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            windows_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.WindowsEventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application SubComponentConfigurationDetails`` property type specifies the configuration settings of the sub-components.

            :param alarm_metrics: A list of metrics to monitor for the component. All component types can use ``AlarmMetrics`` .
            :param logs: A list of logs to monitor for the component. Only Amazon EC2 instances can use ``Logs`` .
            :param processes: A list of processes to monitor for the component. Only Windows EC2 instances can have a processes section.
            :param windows_events: A list of Windows Events to monitor for the component. Only Amazon EC2 instances running on Windows can use ``WindowsEvents`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponentconfigurationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                sub_component_configuration_details_property = applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty(
                    alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                        alarm_metric_name="alarmMetricName"
                    )],
                    logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                        encoding="encoding",
                        log_group_name="logGroupName",
                        log_path="logPath",
                        log_type="logType",
                        pattern_set="patternSet"
                    )],
                    processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                        alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                            alarm_metric_name="alarmMetricName"
                        )],
                        process_name="processName"
                    )],
                    windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                        event_levels=["eventLevels"],
                        event_name="eventName",
                        log_group_name="logGroupName",
                        pattern_set="patternSet"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27152ed48b0dcf07427b37b6d76914598bc3f143899b3f30160295612fb12aa9)
                check_type(argname="argument alarm_metrics", value=alarm_metrics, expected_type=type_hints["alarm_metrics"])
                check_type(argname="argument logs", value=logs, expected_type=type_hints["logs"])
                check_type(argname="argument processes", value=processes, expected_type=type_hints["processes"])
                check_type(argname="argument windows_events", value=windows_events, expected_type=type_hints["windows_events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_metrics is not None:
                self._values["alarm_metrics"] = alarm_metrics
            if logs is not None:
                self._values["logs"] = logs
            if processes is not None:
                self._values["processes"] = processes
            if windows_events is not None:
                self._values["windows_events"] = windows_events

        @builtins.property
        def alarm_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AlarmMetricProperty"]]]]:
            '''A list of metrics to monitor for the component.

            All component types can use ``AlarmMetrics`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponentconfigurationdetails.html#cfn-applicationinsights-application-subcomponentconfigurationdetails-alarmmetrics
            '''
            result = self._values.get("alarm_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AlarmMetricProperty"]]]], result)

        @builtins.property
        def logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.LogProperty"]]]]:
            '''A list of logs to monitor for the component.

            Only Amazon EC2 instances can use ``Logs`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponentconfigurationdetails.html#cfn-applicationinsights-application-subcomponentconfigurationdetails-logs
            '''
            result = self._values.get("logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.LogProperty"]]]], result)

        @builtins.property
        def processes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ProcessProperty"]]]]:
            '''A list of processes to monitor for the component.

            Only Windows EC2 instances can have a processes section.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponentconfigurationdetails.html#cfn-applicationinsights-application-subcomponentconfigurationdetails-processes
            '''
            result = self._values.get("processes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ProcessProperty"]]]], result)

        @builtins.property
        def windows_events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.WindowsEventProperty"]]]]:
            '''A list of Windows Events to monitor for the component.

            Only Amazon EC2 instances running on Windows can use ``WindowsEvents`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponentconfigurationdetails.html#cfn-applicationinsights-application-subcomponentconfigurationdetails-windowsevents
            '''
            result = self._values.get("windows_events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.WindowsEventProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubComponentConfigurationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "sub_component_configuration_details": "subComponentConfigurationDetails",
            "sub_component_type": "subComponentType",
        },
    )
    class SubComponentTypeConfigurationProperty:
        def __init__(
            self,
            *,
            sub_component_configuration_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sub_component_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application SubComponentTypeConfiguration`` property type specifies the sub-component configurations for a component.

            :param sub_component_configuration_details: The configuration settings of the sub-components.
            :param sub_component_type: The sub-component type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponenttypeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                sub_component_type_configuration_property = applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty(
                    sub_component_configuration_details=applicationinsights_mixins.CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty(
                        alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                            alarm_metric_name="alarmMetricName"
                        )],
                        logs=[applicationinsights_mixins.CfnApplicationPropsMixin.LogProperty(
                            encoding="encoding",
                            log_group_name="logGroupName",
                            log_path="logPath",
                            log_type="logType",
                            pattern_set="patternSet"
                        )],
                        processes=[applicationinsights_mixins.CfnApplicationPropsMixin.ProcessProperty(
                            alarm_metrics=[applicationinsights_mixins.CfnApplicationPropsMixin.AlarmMetricProperty(
                                alarm_metric_name="alarmMetricName"
                            )],
                            process_name="processName"
                        )],
                        windows_events=[applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                            event_levels=["eventLevels"],
                            event_name="eventName",
                            log_group_name="logGroupName",
                            pattern_set="patternSet"
                        )]
                    ),
                    sub_component_type="subComponentType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd82bf1bd7e328e8dd14dfc20adaf5085881655775b889fa61d7239d1c53eb72)
                check_type(argname="argument sub_component_configuration_details", value=sub_component_configuration_details, expected_type=type_hints["sub_component_configuration_details"])
                check_type(argname="argument sub_component_type", value=sub_component_type, expected_type=type_hints["sub_component_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sub_component_configuration_details is not None:
                self._values["sub_component_configuration_details"] = sub_component_configuration_details
            if sub_component_type is not None:
                self._values["sub_component_type"] = sub_component_type

        @builtins.property
        def sub_component_configuration_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty"]]:
            '''The configuration settings of the sub-components.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponenttypeconfiguration.html#cfn-applicationinsights-application-subcomponenttypeconfiguration-subcomponentconfigurationdetails
            '''
            result = self._values.get("sub_component_configuration_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty"]], result)

        @builtins.property
        def sub_component_type(self) -> typing.Optional[builtins.str]:
            '''The sub-component type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponenttypeconfiguration.html#cfn-applicationinsights-application-subcomponenttypeconfiguration-subcomponenttype
            '''
            result = self._values.get("sub_component_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubComponentTypeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationinsights.mixins.CfnApplicationPropsMixin.WindowsEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_levels": "eventLevels",
            "event_name": "eventName",
            "log_group_name": "logGroupName",
            "pattern_set": "patternSet",
        },
    )
    class WindowsEventProperty:
        def __init__(
            self,
            *,
            event_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
            event_name: typing.Optional[builtins.str] = None,
            log_group_name: typing.Optional[builtins.str] = None,
            pattern_set: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWS::ApplicationInsights::Application WindowsEvent`` property type specifies a Windows Event to monitor for the component.

            :param event_levels: The levels of event to log. You must specify each level to log. Possible values include ``INFORMATION`` , ``WARNING`` , ``ERROR`` , ``CRITICAL`` , and ``VERBOSE`` . This field is required for each type of Windows Event to log.
            :param event_name: The type of Windows Events to log, equivalent to the Windows Event log channel name. For example, System, Security, CustomEventName, and so on. This field is required for each type of Windows event to log.
            :param log_group_name: The CloudWatch log group name to be associated with the monitored log.
            :param pattern_set: The log pattern set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-windowsevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationinsights import mixins as applicationinsights_mixins
                
                windows_event_property = applicationinsights_mixins.CfnApplicationPropsMixin.WindowsEventProperty(
                    event_levels=["eventLevels"],
                    event_name="eventName",
                    log_group_name="logGroupName",
                    pattern_set="patternSet"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__356b2040949e079de5b80d44d6e381c7562603444c591e82bfbc00927e82fcdb)
                check_type(argname="argument event_levels", value=event_levels, expected_type=type_hints["event_levels"])
                check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                check_type(argname="argument pattern_set", value=pattern_set, expected_type=type_hints["pattern_set"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_levels is not None:
                self._values["event_levels"] = event_levels
            if event_name is not None:
                self._values["event_name"] = event_name
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if pattern_set is not None:
                self._values["pattern_set"] = pattern_set

        @builtins.property
        def event_levels(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The levels of event to log.

            You must specify each level to log. Possible values include ``INFORMATION`` , ``WARNING`` , ``ERROR`` , ``CRITICAL`` , and ``VERBOSE`` . This field is required for each type of Windows Event to log.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-windowsevent.html#cfn-applicationinsights-application-windowsevent-eventlevels
            '''
            result = self._values.get("event_levels")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def event_name(self) -> typing.Optional[builtins.str]:
            '''The type of Windows Events to log, equivalent to the Windows Event log channel name.

            For example, System, Security, CustomEventName, and so on. This field is required for each type of Windows event to log.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-windowsevent.html#cfn-applicationinsights-application-windowsevent-eventname
            '''
            result = self._values.get("event_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The CloudWatch log group name to be associated with the monitored log.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-windowsevent.html#cfn-applicationinsights-application-windowsevent-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern_set(self) -> typing.Optional[builtins.str]:
            '''The log pattern set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-windowsevent.html#cfn-applicationinsights-application-windowsevent-patternset
            '''
            result = self._values.get("pattern_set")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WindowsEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
]

publication.publish()

def _typecheckingstub__e8e3fde3cc8b2dde899af2d49c09bba109a1797c9096254438145bc385782fb3(
    *,
    attach_missing_permission: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    auto_configuration_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    component_monitoring_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ComponentMonitoringSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.CustomComponentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    cwe_monitor_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    grouping_type: typing.Optional[builtins.str] = None,
    log_pattern_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.LogPatternSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ops_center_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ops_item_sns_topic_arn: typing.Optional[builtins.str] = None,
    resource_group_name: typing.Optional[builtins.str] = None,
    sns_notification_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85dab4dea343662add15b4e49a1491a295ec7410f225eb3f5a0d6f14bafff05(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20fe79b5f2cd79201740b369008868c9bafff9d07abcadd2faa7d7a8e1c95ed(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57ca457a7fcda7c2ba5e410e279076bc9ce8011cb4eb01afde641a5313ea115(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6adf210ceb915eba02a6cb040001096a872593c12dee8492560ef5047a68ee(
    *,
    alarm_metric_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9b6f3b11f51016f1b074f5e099780037fe9c7394c133247550548612d937f8(
    *,
    alarm_name: typing.Optional[builtins.str] = None,
    severity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14550e0ef50e809d77347856fd90499e813f34a093389ed252e9263bc2685055(
    *,
    configuration_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ConfigurationDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sub_component_type_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.SubComponentTypeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34eea997c7e0698894f939dfc555db45f64eefaa8921bc0a4ecf664b6ce8572(
    *,
    component_arn: typing.Optional[builtins.str] = None,
    component_configuration_mode: typing.Optional[builtins.str] = None,
    component_name: typing.Optional[builtins.str] = None,
    custom_component_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ComponentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_overwrite_component_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ComponentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c7713ac24e97562db7158acb26683bfbf7b907c0202fcef833d42c465e7d4c(
    *,
    alarm_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.AlarmMetricProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    alarms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.AlarmProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ha_cluster_prometheus_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.HAClusterPrometheusExporterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hana_prometheus_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.HANAPrometheusExporterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    jmx_prometheus_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.JMXPrometheusExporterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.LogProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    net_weaver_prometheus_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.NetWeaverPrometheusExporterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    processes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ProcessProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    sql_server_prometheus_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.SQLServerPrometheusExporterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    windows_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.WindowsEventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daacc2d873a165fb5f2e4d9c45287b2965111ed45068aa730750a7dbbd188a97(
    *,
    component_name: typing.Optional[builtins.str] = None,
    resource_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd2203e6ff9f31888e8a29118f4f7b7f41dd36c4a1087bb996320cd58323a49(
    *,
    prometheus_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32d9c703d80c2a6a82172107cf08da270d32b865c8043c109a53586f8833419(
    *,
    agree_to_install_hanadb_client: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    hana_port: typing.Optional[builtins.str] = None,
    hana_secret_name: typing.Optional[builtins.str] = None,
    hanasid: typing.Optional[builtins.str] = None,
    prometheus_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e81cea9bb7a339d83e3b693a1c7f3baf77003bec74ab79065568d5f58c877e4(
    *,
    host_port: typing.Optional[builtins.str] = None,
    jmxurl: typing.Optional[builtins.str] = None,
    prometheus_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9f14d103e5c8b6f242befe7cfce91442581800fa54c7c135bc79f45acc5bcb(
    *,
    pattern: typing.Optional[builtins.str] = None,
    pattern_name: typing.Optional[builtins.str] = None,
    rank: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ec901581d5736b15f70ecaceb53849ec97ed1be2e09a718734f1baa2c48267(
    *,
    log_patterns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.LogPatternProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    pattern_set_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77b1460b427399f4d38e2f5432a723a40661f8459b090b297629b6d5eaf1b20(
    *,
    encoding: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_path: typing.Optional[builtins.str] = None,
    log_type: typing.Optional[builtins.str] = None,
    pattern_set: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b736c127f5328f28cb73f30b977af1512b7fa11e18b6274c014719cddfff4c3b(
    *,
    instance_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    prometheus_port: typing.Optional[builtins.str] = None,
    sapsid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e761ea749f4d131dc45630fbcbaca7cc736e83707b5d9c18e3c96d865d4c74fb(
    *,
    alarm_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.AlarmMetricProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    process_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5897898d6c83caf6881880d7a934ee2ce2c9001154c11053989d6408f41a2285(
    *,
    prometheus_port: typing.Optional[builtins.str] = None,
    sql_secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27152ed48b0dcf07427b37b6d76914598bc3f143899b3f30160295612fb12aa9(
    *,
    alarm_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.AlarmMetricProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.LogProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    processes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ProcessProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    windows_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.WindowsEventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd82bf1bd7e328e8dd14dfc20adaf5085881655775b889fa61d7239d1c53eb72(
    *,
    sub_component_configuration_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.SubComponentConfigurationDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sub_component_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356b2040949e079de5b80d44d6e381c7562603444c591e82bfbc00927e82fcdb(
    *,
    event_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_name: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    pattern_set: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
