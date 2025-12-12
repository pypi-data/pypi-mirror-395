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
    jsii_type="@aws-cdk/mixins-preview.aws_internetmonitor.mixins.CfnMonitorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "health_events_config": "healthEventsConfig",
        "include_linked_accounts": "includeLinkedAccounts",
        "internet_measurements_log_delivery": "internetMeasurementsLogDelivery",
        "linked_account_id": "linkedAccountId",
        "max_city_networks_to_monitor": "maxCityNetworksToMonitor",
        "monitor_name": "monitorName",
        "resources": "resources",
        "resources_to_add": "resourcesToAdd",
        "resources_to_remove": "resourcesToRemove",
        "status": "status",
        "tags": "tags",
        "traffic_percentage_to_monitor": "trafficPercentageToMonitor",
    },
)
class CfnMonitorMixinProps:
    def __init__(
        self,
        *,
        health_events_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMonitorPropsMixin.HealthEventsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        include_linked_accounts: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        internet_measurements_log_delivery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMonitorPropsMixin.InternetMeasurementsLogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        linked_account_id: typing.Optional[builtins.str] = None,
        max_city_networks_to_monitor: typing.Optional[jsii.Number] = None,
        monitor_name: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources_to_add: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources_to_remove: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        traffic_percentage_to_monitor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnMonitorPropsMixin.

        :param health_events_config: A complex type with the configuration information that determines the threshold and other conditions for when Internet Monitor creates a health event for an overall performance or availability issue, across an application's geographies. Defines the percentages, for overall performance scores and availability scores for an application, that are the thresholds for when Internet Monitor creates a health event. You can override the defaults to set a custom threshold for overall performance or availability scores, or both. You can also set thresholds for local health scores,, where Internet Monitor creates a health event when scores cross a threshold for one or more city-networks, in addition to creating an event when an overall score crosses a threshold. If you don't set a health event threshold, the default value is 95%. For local thresholds, you also set a minimum percentage of overall traffic that is impacted by an issue before Internet Monitor creates an event. In addition, you can disable local thresholds, for performance scores, availability scores, or both. For more information, see `Change health event thresholds <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-IM-overview.html#IMUpdateThresholdFromOverview>`_ in the Internet Monitor section of the *CloudWatch User Guide* .
        :param include_linked_accounts: A boolean option that you can set to ``TRUE`` to include monitors for linked accounts in a list of monitors, when you've set up cross-account sharing in Internet Monitor. You configure cross-account sharing by using Amazon CloudWatch Observability Access Manager. For more information, see `Internet Monitor cross-account observability <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cwim-cross-account.html>`_ in the Amazon CloudWatch User Guide.
        :param internet_measurements_log_delivery: Publish internet measurements for a monitor for all city-networks (up to the 500,000 service limit) to another location, such as an Amazon S3 bucket. Measurements are also published to Amazon CloudWatch Logs for the first 500 (by traffic volume) city-networks (client locations and ASNs, typically internet service providers or ISPs).
        :param linked_account_id: The account ID for an account that you've set up cross-account sharing for in Internet Monitor. You configure cross-account sharing by using Amazon CloudWatch Observability Access Manager. For more information, see `Internet Monitor cross-account observability <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cwim-cross-account.html>`_ in the Amazon CloudWatch User Guide.
        :param max_city_networks_to_monitor: The maximum number of city-networks to monitor for your resources. A city-network is the location (city) where clients access your application resources from and the network, such as an internet service provider, that clients access the resources through. For more information, see `Choosing a city-network maximum value <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/IMCityNetworksMaximum.html>`_ in *Using Amazon CloudWatch Internet Monitor* .
        :param monitor_name: The name of the monitor. A monitor name can contain only alphanumeric characters, dashes (-), periods (.), and underscores (_).
        :param resources: The resources that have been added for the monitor, listed by their Amazon Resource Names (ARNs). Use this option to add or remove resources when making an update. .. epigraph:: Be aware that if you include content in the ``Resources`` field when you update a monitor, the ``ResourcesToAdd`` and ``ResourcesToRemove`` fields must be empty.
        :param resources_to_add: The resources to include in a monitor, which you provide as a set of Amazon Resource Names (ARNs). Resources can be Amazon Virtual Private Cloud VPCs, Network Load Balancers (NLBs), Amazon CloudFront distributions, or Amazon WorkSpaces directories. You can add a combination of VPCs and CloudFront distributions, or you can add WorkSpaces directories, or you can add NLBs. You can't add NLBs or WorkSpaces directories together with any other resources. If you add only VPC resources, at least one VPC must have an Internet Gateway attached to it, to make sure that it has internet connectivity. .. epigraph:: You can specify this field for a monitor update only if the ``Resources`` field is empty.
        :param resources_to_remove: The resources to remove from a monitor, which you provide as a set of Amazon Resource Names (ARNs). .. epigraph:: You can specify this field for a monitor update only if the ``Resources`` field is empty.
        :param status: The status of a monitor. The accepted values that you can specify for ``Status`` are ``ACTIVE`` and ``INACTIVE`` .
        :param tags: The tags for a monitor, listed as a set of *key:value* pairs.
        :param traffic_percentage_to_monitor: The percentage of the internet-facing traffic for your application that you want to monitor. You can also, optionally, set a limit for the number of city-networks (client locations and ASNs, typically internet service providers) that Internet Monitor will monitor traffic for. The city-networks maximum limit caps the number of city-networks that Internet Monitor monitors for your application, regardless of the percentage of traffic that you choose to monitor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_internetmonitor import mixins as internetmonitor_mixins
            
            cfn_monitor_mixin_props = internetmonitor_mixins.CfnMonitorMixinProps(
                health_events_config=internetmonitor_mixins.CfnMonitorPropsMixin.HealthEventsConfigProperty(
                    availability_local_health_events_config=internetmonitor_mixins.CfnMonitorPropsMixin.LocalHealthEventsConfigProperty(
                        health_score_threshold=123,
                        min_traffic_impact=123,
                        status="status"
                    ),
                    availability_score_threshold=123,
                    performance_local_health_events_config=internetmonitor_mixins.CfnMonitorPropsMixin.LocalHealthEventsConfigProperty(
                        health_score_threshold=123,
                        min_traffic_impact=123,
                        status="status"
                    ),
                    performance_score_threshold=123
                ),
                include_linked_accounts=False,
                internet_measurements_log_delivery=internetmonitor_mixins.CfnMonitorPropsMixin.InternetMeasurementsLogDeliveryProperty(
                    s3_config=internetmonitor_mixins.CfnMonitorPropsMixin.S3ConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        log_delivery_status="logDeliveryStatus"
                    )
                ),
                linked_account_id="linkedAccountId",
                max_city_networks_to_monitor=123,
                monitor_name="monitorName",
                resources=["resources"],
                resources_to_add=["resourcesToAdd"],
                resources_to_remove=["resourcesToRemove"],
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                traffic_percentage_to_monitor=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ebe990da2592ec81629f030c87d0eee1805c1021ad581be8fe77dfce40b616)
            check_type(argname="argument health_events_config", value=health_events_config, expected_type=type_hints["health_events_config"])
            check_type(argname="argument include_linked_accounts", value=include_linked_accounts, expected_type=type_hints["include_linked_accounts"])
            check_type(argname="argument internet_measurements_log_delivery", value=internet_measurements_log_delivery, expected_type=type_hints["internet_measurements_log_delivery"])
            check_type(argname="argument linked_account_id", value=linked_account_id, expected_type=type_hints["linked_account_id"])
            check_type(argname="argument max_city_networks_to_monitor", value=max_city_networks_to_monitor, expected_type=type_hints["max_city_networks_to_monitor"])
            check_type(argname="argument monitor_name", value=monitor_name, expected_type=type_hints["monitor_name"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument resources_to_add", value=resources_to_add, expected_type=type_hints["resources_to_add"])
            check_type(argname="argument resources_to_remove", value=resources_to_remove, expected_type=type_hints["resources_to_remove"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument traffic_percentage_to_monitor", value=traffic_percentage_to_monitor, expected_type=type_hints["traffic_percentage_to_monitor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if health_events_config is not None:
            self._values["health_events_config"] = health_events_config
        if include_linked_accounts is not None:
            self._values["include_linked_accounts"] = include_linked_accounts
        if internet_measurements_log_delivery is not None:
            self._values["internet_measurements_log_delivery"] = internet_measurements_log_delivery
        if linked_account_id is not None:
            self._values["linked_account_id"] = linked_account_id
        if max_city_networks_to_monitor is not None:
            self._values["max_city_networks_to_monitor"] = max_city_networks_to_monitor
        if monitor_name is not None:
            self._values["monitor_name"] = monitor_name
        if resources is not None:
            self._values["resources"] = resources
        if resources_to_add is not None:
            self._values["resources_to_add"] = resources_to_add
        if resources_to_remove is not None:
            self._values["resources_to_remove"] = resources_to_remove
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if traffic_percentage_to_monitor is not None:
            self._values["traffic_percentage_to_monitor"] = traffic_percentage_to_monitor

    @builtins.property
    def health_events_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMonitorPropsMixin.HealthEventsConfigProperty"]]:
        '''A complex type with the configuration information that determines the threshold and other conditions for when Internet Monitor creates a health event for an overall performance or availability issue, across an application's geographies.

        Defines the percentages, for overall performance scores and availability scores for an application, that are the thresholds for when Internet Monitor creates a health event. You can override the defaults to set a custom threshold for overall performance or availability scores, or both.

        You can also set thresholds for local health scores,, where Internet Monitor creates a health event when scores cross a threshold for one or more city-networks, in addition to creating an event when an overall score crosses a threshold.

        If you don't set a health event threshold, the default value is 95%.

        For local thresholds, you also set a minimum percentage of overall traffic that is impacted by an issue before Internet Monitor creates an event. In addition, you can disable local thresholds, for performance scores, availability scores, or both.

        For more information, see `Change health event thresholds <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-IM-overview.html#IMUpdateThresholdFromOverview>`_ in the Internet Monitor section of the *CloudWatch User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-healtheventsconfig
        '''
        result = self._values.get("health_events_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMonitorPropsMixin.HealthEventsConfigProperty"]], result)

    @builtins.property
    def include_linked_accounts(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A boolean option that you can set to ``TRUE`` to include monitors for linked accounts in a list of monitors, when you've set up cross-account sharing in Internet Monitor.

        You configure cross-account sharing by using Amazon CloudWatch Observability Access Manager. For more information, see `Internet Monitor cross-account observability <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cwim-cross-account.html>`_ in the Amazon CloudWatch User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-includelinkedaccounts
        '''
        result = self._values.get("include_linked_accounts")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def internet_measurements_log_delivery(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMonitorPropsMixin.InternetMeasurementsLogDeliveryProperty"]]:
        '''Publish internet measurements for a monitor for all city-networks (up to the 500,000 service limit) to another location, such as an Amazon S3 bucket.

        Measurements are also published to Amazon CloudWatch Logs for the first 500 (by traffic volume) city-networks (client locations and ASNs, typically internet service providers or ISPs).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-internetmeasurementslogdelivery
        '''
        result = self._values.get("internet_measurements_log_delivery")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMonitorPropsMixin.InternetMeasurementsLogDeliveryProperty"]], result)

    @builtins.property
    def linked_account_id(self) -> typing.Optional[builtins.str]:
        '''The account ID for an account that you've set up cross-account sharing for in Internet Monitor.

        You configure cross-account sharing by using Amazon CloudWatch Observability Access Manager. For more information, see `Internet Monitor cross-account observability <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cwim-cross-account.html>`_ in the Amazon CloudWatch User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-linkedaccountid
        '''
        result = self._values.get("linked_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_city_networks_to_monitor(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of city-networks to monitor for your resources.

        A city-network is the location (city) where clients access your application resources from and the network, such as an internet service provider, that clients access the resources through.

        For more information, see `Choosing a city-network maximum value <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/IMCityNetworksMaximum.html>`_ in *Using Amazon CloudWatch Internet Monitor* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-maxcitynetworkstomonitor
        '''
        result = self._values.get("max_city_networks_to_monitor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitor_name(self) -> typing.Optional[builtins.str]:
        '''The name of the monitor.

        A monitor name can contain only alphanumeric characters, dashes (-), periods (.), and underscores (_).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-monitorname
        '''
        result = self._values.get("monitor_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources that have been added for the monitor, listed by their Amazon Resource Names (ARNs).

        Use this option to add or remove resources when making an update.
        .. epigraph::

           Be aware that if you include content in the ``Resources`` field when you update a monitor, the ``ResourcesToAdd`` and ``ResourcesToRemove`` fields must be empty.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resources_to_add(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to include in a monitor, which you provide as a set of Amazon Resource Names (ARNs).

        Resources can be Amazon Virtual Private Cloud VPCs, Network Load Balancers (NLBs), Amazon CloudFront distributions, or Amazon WorkSpaces directories.

        You can add a combination of VPCs and CloudFront distributions, or you can add WorkSpaces directories, or you can add NLBs. You can't add NLBs or WorkSpaces directories together with any other resources.

        If you add only VPC resources, at least one VPC must have an Internet Gateway attached to it, to make sure that it has internet connectivity.
        .. epigraph::

           You can specify this field for a monitor update only if the ``Resources`` field is empty.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-resourcestoadd
        '''
        result = self._values.get("resources_to_add")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resources_to_remove(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to remove from a monitor, which you provide as a set of Amazon Resource Names (ARNs).

        .. epigraph::

           You can specify this field for a monitor update only if the ``Resources`` field is empty.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-resourcestoremove
        '''
        result = self._values.get("resources_to_remove")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of a monitor.

        The accepted values that you can specify for ``Status`` are ``ACTIVE`` and ``INACTIVE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for a monitor, listed as a set of *key:value* pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def traffic_percentage_to_monitor(self) -> typing.Optional[jsii.Number]:
        '''The percentage of the internet-facing traffic for your application that you want to monitor.

        You can also, optionally, set a limit for the number of city-networks (client locations and ASNs, typically internet service providers) that Internet Monitor will monitor traffic for. The city-networks maximum limit caps the number of city-networks that Internet Monitor monitors for your application, regardless of the percentage of traffic that you choose to monitor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-trafficpercentagetomonitor
        '''
        result = self._values.get("traffic_percentage_to_monitor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMonitorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMonitorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_internetmonitor.mixins.CfnMonitorPropsMixin",
):
    '''The ``AWS::InternetMonitor::Monitor`` resource is an Internet Monitor resource type that contains information about how you create a monitor in Amazon CloudWatch Internet Monitor.

    A monitor in Internet Monitor provides visibility into performance and availability between your applications hosted on AWS and your end users, using a traffic profile that it creates based on the application resources that you add: Virtual Private Clouds (VPCs), Amazon CloudFront distributions, or WorkSpaces directories.

    Internet Monitor also alerts you to internet issues that impact your application in the city-networks (geographies and networks) where your end users use it. With Internet Monitor, you can quickly pinpoint the locations and providers that are affected, so that you can address the issue.

    For more information, see `Using Amazon CloudWatch Internet Monitor <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-InternetMonitor.html>`_ in the *Amazon CloudWatch User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html
    :cloudformationResource: AWS::InternetMonitor::Monitor
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_internetmonitor import mixins as internetmonitor_mixins
        
        cfn_monitor_props_mixin = internetmonitor_mixins.CfnMonitorPropsMixin(internetmonitor_mixins.CfnMonitorMixinProps(
            health_events_config=internetmonitor_mixins.CfnMonitorPropsMixin.HealthEventsConfigProperty(
                availability_local_health_events_config=internetmonitor_mixins.CfnMonitorPropsMixin.LocalHealthEventsConfigProperty(
                    health_score_threshold=123,
                    min_traffic_impact=123,
                    status="status"
                ),
                availability_score_threshold=123,
                performance_local_health_events_config=internetmonitor_mixins.CfnMonitorPropsMixin.LocalHealthEventsConfigProperty(
                    health_score_threshold=123,
                    min_traffic_impact=123,
                    status="status"
                ),
                performance_score_threshold=123
            ),
            include_linked_accounts=False,
            internet_measurements_log_delivery=internetmonitor_mixins.CfnMonitorPropsMixin.InternetMeasurementsLogDeliveryProperty(
                s3_config=internetmonitor_mixins.CfnMonitorPropsMixin.S3ConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    log_delivery_status="logDeliveryStatus"
                )
            ),
            linked_account_id="linkedAccountId",
            max_city_networks_to_monitor=123,
            monitor_name="monitorName",
            resources=["resources"],
            resources_to_add=["resourcesToAdd"],
            resources_to_remove=["resourcesToRemove"],
            status="status",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            traffic_percentage_to_monitor=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMonitorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::InternetMonitor::Monitor``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5650b18ed9174e03a2bbda81f4773144553fb13069008350c1bc2e1f7644d99a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa9e79f72919f9418495979463e1120a50cd5652ff69051455ab63a0a660290e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f530c1c91761e92bd5dc67a276c08e749c45da849075ecf5bdc86055cf3c8d0d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMonitorMixinProps:
        return typing.cast(CfnMonitorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_internetmonitor.mixins.CfnMonitorPropsMixin.HealthEventsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_local_health_events_config": "availabilityLocalHealthEventsConfig",
            "availability_score_threshold": "availabilityScoreThreshold",
            "performance_local_health_events_config": "performanceLocalHealthEventsConfig",
            "performance_score_threshold": "performanceScoreThreshold",
        },
    )
    class HealthEventsConfigProperty:
        def __init__(
            self,
            *,
            availability_local_health_events_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMonitorPropsMixin.LocalHealthEventsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            availability_score_threshold: typing.Optional[jsii.Number] = None,
            performance_local_health_events_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMonitorPropsMixin.LocalHealthEventsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            performance_score_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Define the health event threshold percentages for the performance score and availability score for your application's monitor.

            Amazon CloudWatch Internet Monitor creates a health event when there's an internet issue that affects your application end users where a health score percentage is at or below a set threshold.

            If you don't set a health event threshold, the default value is 95%.

            :param availability_local_health_events_config: The configuration that determines the threshold and other conditions for when Internet Monitor creates a health event for a local availability issue.
            :param availability_score_threshold: The health event threshold percentage set for availability scores. When the overall availability score is at or below this percentage, Internet Monitor creates a health event.
            :param performance_local_health_events_config: The configuration that determines the threshold and other conditions for when Internet Monitor creates a health event for a local performance issue.
            :param performance_score_threshold: The health event threshold percentage set for performance scores. When the overall performance score is at or below this percentage, Internet Monitor creates a health event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-healtheventsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_internetmonitor import mixins as internetmonitor_mixins
                
                health_events_config_property = internetmonitor_mixins.CfnMonitorPropsMixin.HealthEventsConfigProperty(
                    availability_local_health_events_config=internetmonitor_mixins.CfnMonitorPropsMixin.LocalHealthEventsConfigProperty(
                        health_score_threshold=123,
                        min_traffic_impact=123,
                        status="status"
                    ),
                    availability_score_threshold=123,
                    performance_local_health_events_config=internetmonitor_mixins.CfnMonitorPropsMixin.LocalHealthEventsConfigProperty(
                        health_score_threshold=123,
                        min_traffic_impact=123,
                        status="status"
                    ),
                    performance_score_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__449c492f8a81d167cc6dd4c203d8e37b524a9895c12091d845562183725c1a8e)
                check_type(argname="argument availability_local_health_events_config", value=availability_local_health_events_config, expected_type=type_hints["availability_local_health_events_config"])
                check_type(argname="argument availability_score_threshold", value=availability_score_threshold, expected_type=type_hints["availability_score_threshold"])
                check_type(argname="argument performance_local_health_events_config", value=performance_local_health_events_config, expected_type=type_hints["performance_local_health_events_config"])
                check_type(argname="argument performance_score_threshold", value=performance_score_threshold, expected_type=type_hints["performance_score_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_local_health_events_config is not None:
                self._values["availability_local_health_events_config"] = availability_local_health_events_config
            if availability_score_threshold is not None:
                self._values["availability_score_threshold"] = availability_score_threshold
            if performance_local_health_events_config is not None:
                self._values["performance_local_health_events_config"] = performance_local_health_events_config
            if performance_score_threshold is not None:
                self._values["performance_score_threshold"] = performance_score_threshold

        @builtins.property
        def availability_local_health_events_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMonitorPropsMixin.LocalHealthEventsConfigProperty"]]:
            '''The configuration that determines the threshold and other conditions for when Internet Monitor creates a health event for a local availability issue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-healtheventsconfig.html#cfn-internetmonitor-monitor-healtheventsconfig-availabilitylocalhealtheventsconfig
            '''
            result = self._values.get("availability_local_health_events_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMonitorPropsMixin.LocalHealthEventsConfigProperty"]], result)

        @builtins.property
        def availability_score_threshold(self) -> typing.Optional[jsii.Number]:
            '''The health event threshold percentage set for availability scores.

            When the overall availability score is at or below this percentage, Internet Monitor creates a health event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-healtheventsconfig.html#cfn-internetmonitor-monitor-healtheventsconfig-availabilityscorethreshold
            '''
            result = self._values.get("availability_score_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def performance_local_health_events_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMonitorPropsMixin.LocalHealthEventsConfigProperty"]]:
            '''The configuration that determines the threshold and other conditions for when Internet Monitor creates a health event for a local performance issue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-healtheventsconfig.html#cfn-internetmonitor-monitor-healtheventsconfig-performancelocalhealtheventsconfig
            '''
            result = self._values.get("performance_local_health_events_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMonitorPropsMixin.LocalHealthEventsConfigProperty"]], result)

        @builtins.property
        def performance_score_threshold(self) -> typing.Optional[jsii.Number]:
            '''The health event threshold percentage set for performance scores.

            When the overall performance score is at or below this percentage, Internet Monitor creates a health event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-healtheventsconfig.html#cfn-internetmonitor-monitor-healtheventsconfig-performancescorethreshold
            '''
            result = self._values.get("performance_score_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthEventsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_internetmonitor.mixins.CfnMonitorPropsMixin.InternetMeasurementsLogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_config": "s3Config"},
    )
    class InternetMeasurementsLogDeliveryProperty:
        def __init__(
            self,
            *,
            s3_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMonitorPropsMixin.S3ConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Publish internet measurements to an Amazon S3 bucket in addition to CloudWatch Logs.

            :param s3_config: The configuration for publishing Amazon CloudWatch Internet Monitor internet measurements to Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-internetmeasurementslogdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_internetmonitor import mixins as internetmonitor_mixins
                
                internet_measurements_log_delivery_property = internetmonitor_mixins.CfnMonitorPropsMixin.InternetMeasurementsLogDeliveryProperty(
                    s3_config=internetmonitor_mixins.CfnMonitorPropsMixin.S3ConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        log_delivery_status="logDeliveryStatus"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4fed45a4587b26e7ba9d89e5a1c2c6503426d490d9ed86cc965ef559f59ba15f)
                check_type(argname="argument s3_config", value=s3_config, expected_type=type_hints["s3_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_config is not None:
                self._values["s3_config"] = s3_config

        @builtins.property
        def s3_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMonitorPropsMixin.S3ConfigProperty"]]:
            '''The configuration for publishing Amazon CloudWatch Internet Monitor internet measurements to Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-internetmeasurementslogdelivery.html#cfn-internetmonitor-monitor-internetmeasurementslogdelivery-s3config
            '''
            result = self._values.get("s3_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMonitorPropsMixin.S3ConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InternetMeasurementsLogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_internetmonitor.mixins.CfnMonitorPropsMixin.LocalHealthEventsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "health_score_threshold": "healthScoreThreshold",
            "min_traffic_impact": "minTrafficImpact",
            "status": "status",
        },
    )
    class LocalHealthEventsConfigProperty:
        def __init__(
            self,
            *,
            health_score_threshold: typing.Optional[jsii.Number] = None,
            min_traffic_impact: typing.Optional[jsii.Number] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information that determines the threshold and other conditions for when Internet Monitor creates a health event for a local performance or availability issue, when scores cross a threshold for one or more city-networks.

            Defines the percentages, for performance scores or availability scores, that are the local thresholds for when Amazon CloudWatch Internet Monitor creates a health event. Also defines whether a local threshold is enabled or disabled, and the minimum percentage of overall traffic that must be impacted by an issue before Internet Monitor creates an event when a	threshold is crossed for a local health score.

            If you don't set a local health event threshold, the default value is 60%.

            For more information, see `Change health event thresholds <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-IM-overview.html#IMUpdateThresholdFromOverview>`_ in the Internet Monitor section of the *Amazon CloudWatch User Guide* .

            :param health_score_threshold: The health event threshold percentage set for a local health score.
            :param min_traffic_impact: The minimum percentage of overall traffic for an application that must be impacted by an issue before Internet Monitor creates an event when a threshold is crossed for a local health score. If you don't set a minimum traffic impact threshold, the default value is 0.01%.
            :param status: The status of whether Internet Monitor creates a health event based on a threshold percentage set for a local health score. The status can be ``ENABLED`` or ``DISABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-localhealtheventsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_internetmonitor import mixins as internetmonitor_mixins
                
                local_health_events_config_property = internetmonitor_mixins.CfnMonitorPropsMixin.LocalHealthEventsConfigProperty(
                    health_score_threshold=123,
                    min_traffic_impact=123,
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__994ac1cd0c8d57953f4471424bb8808ff8e2117a6b3597929b7d7605552fb1aa)
                check_type(argname="argument health_score_threshold", value=health_score_threshold, expected_type=type_hints["health_score_threshold"])
                check_type(argname="argument min_traffic_impact", value=min_traffic_impact, expected_type=type_hints["min_traffic_impact"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if health_score_threshold is not None:
                self._values["health_score_threshold"] = health_score_threshold
            if min_traffic_impact is not None:
                self._values["min_traffic_impact"] = min_traffic_impact
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def health_score_threshold(self) -> typing.Optional[jsii.Number]:
            '''The health event threshold percentage set for a local health score.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-localhealtheventsconfig.html#cfn-internetmonitor-monitor-localhealtheventsconfig-healthscorethreshold
            '''
            result = self._values.get("health_score_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_traffic_impact(self) -> typing.Optional[jsii.Number]:
            '''The minimum percentage of overall traffic for an application that must be impacted by an issue before Internet Monitor creates an event when a threshold is crossed for a local health score.

            If you don't set a minimum traffic impact threshold, the default value is 0.01%.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-localhealtheventsconfig.html#cfn-internetmonitor-monitor-localhealtheventsconfig-mintrafficimpact
            '''
            result = self._values.get("min_traffic_impact")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of whether Internet Monitor creates a health event based on a threshold percentage set for a local health score.

            The status can be ``ENABLED`` or ``DISABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-localhealtheventsconfig.html#cfn-internetmonitor-monitor-localhealtheventsconfig-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalHealthEventsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_internetmonitor.mixins.CfnMonitorPropsMixin.S3ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "log_delivery_status": "logDeliveryStatus",
        },
    )
    class S3ConfigProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            log_delivery_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for publishing Amazon CloudWatch Internet Monitor internet measurements to Amazon S3.

            The configuration includes the bucket name and (optionally) bucket prefix for the S3 bucket to store the measurements, and the delivery status. The delivery status is ``ENABLED`` if you choose to deliver internet measurements to S3 logs, and ``DISABLED`` otherwise.

            The measurements are also published to Amazon CloudWatch Logs.

            :param bucket_name: The Amazon S3 bucket name for internet measurements publishing.
            :param bucket_prefix: An optional Amazon S3 bucket prefix for internet measurements publishing.
            :param log_delivery_status: The status of publishing Internet Monitor internet measurements to an Amazon S3 bucket. The delivery status is ``ENABLED`` if you choose to deliver internet measurements to an S3 bucket, and ``DISABLED`` otherwise.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-s3config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_internetmonitor import mixins as internetmonitor_mixins
                
                s3_config_property = internetmonitor_mixins.CfnMonitorPropsMixin.S3ConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    log_delivery_status="logDeliveryStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef33ad017da1d620c5a7141ff74bc6ee618ef1a002095e9173c25a99bb52ad22)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument log_delivery_status", value=log_delivery_status, expected_type=type_hints["log_delivery_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if log_delivery_status is not None:
                self._values["log_delivery_status"] = log_delivery_status

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket name for internet measurements publishing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-s3config.html#cfn-internetmonitor-monitor-s3config-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''An optional Amazon S3 bucket prefix for internet measurements publishing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-s3config.html#cfn-internetmonitor-monitor-s3config-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_delivery_status(self) -> typing.Optional[builtins.str]:
            '''The status of publishing Internet Monitor internet measurements to an Amazon S3 bucket.

            The delivery status is ``ENABLED`` if you choose to deliver internet measurements to an S3 bucket, and ``DISABLED`` otherwise.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-internetmonitor-monitor-s3config.html#cfn-internetmonitor-monitor-s3config-logdeliverystatus
            '''
            result = self._values.get("log_delivery_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnMonitorMixinProps",
    "CfnMonitorPropsMixin",
]

publication.publish()

def _typecheckingstub__72ebe990da2592ec81629f030c87d0eee1805c1021ad581be8fe77dfce40b616(
    *,
    health_events_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMonitorPropsMixin.HealthEventsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_linked_accounts: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    internet_measurements_log_delivery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMonitorPropsMixin.InternetMeasurementsLogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    linked_account_id: typing.Optional[builtins.str] = None,
    max_city_networks_to_monitor: typing.Optional[jsii.Number] = None,
    monitor_name: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources_to_add: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources_to_remove: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    traffic_percentage_to_monitor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5650b18ed9174e03a2bbda81f4773144553fb13069008350c1bc2e1f7644d99a(
    props: typing.Union[CfnMonitorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9e79f72919f9418495979463e1120a50cd5652ff69051455ab63a0a660290e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f530c1c91761e92bd5dc67a276c08e749c45da849075ecf5bdc86055cf3c8d0d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449c492f8a81d167cc6dd4c203d8e37b524a9895c12091d845562183725c1a8e(
    *,
    availability_local_health_events_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMonitorPropsMixin.LocalHealthEventsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    availability_score_threshold: typing.Optional[jsii.Number] = None,
    performance_local_health_events_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMonitorPropsMixin.LocalHealthEventsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    performance_score_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fed45a4587b26e7ba9d89e5a1c2c6503426d490d9ed86cc965ef559f59ba15f(
    *,
    s3_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMonitorPropsMixin.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994ac1cd0c8d57953f4471424bb8808ff8e2117a6b3597929b7d7605552fb1aa(
    *,
    health_score_threshold: typing.Optional[jsii.Number] = None,
    min_traffic_impact: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef33ad017da1d620c5a7141ff74bc6ee618ef1a002095e9173c25a99bb52ad22(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    log_delivery_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
