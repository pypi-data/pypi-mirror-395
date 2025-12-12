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
import aws_cdk.interfaces.aws_kinesisfirehose as _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ...aws_logs import ILogsDelivery as _ILogsDelivery_0d3c9e29
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


@jsii.implements(_IMixin_11e4b965)
class CfnAppMonitorLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorLogsMixin",
):
    '''Creates a CloudWatch RUM app monitor, which you can use to collect telemetry data from your application and send it to CloudWatch RUM.

    The data includes performance and reliability information such as page load time, client-side errors, and user behavior.

    After you create an app monitor, sign in to the CloudWatch RUM console to get the JavaScript code snippet to add to your web application. For more information, see `How do I find a code snippet that I've already generated? <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-find-code-snippet.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html
    :cloudformationResource: AWS::RUM::AppMonitor
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_app_monitor_logs_mixin = rum_mixins.CfnAppMonitorLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::RUM::AppMonitor``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d3836331e6eb13fa0f29e06c22ead9769f7cacf605e38dcf20259bddca2e6f1)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06296afb9ae59fe025ea2733e156699dead7eea264d45a2df066799c51c4b174)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea36aa2c2fec6d3f647ff3d56d72694d72bc372f48cc3f14e2ae69b9fb0c31aa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RUM_OTEL_LOGS")
    def RUM_OTEL_LOGS(cls) -> "CfnAppMonitorRumOtelLogs":
        return typing.cast("CfnAppMonitorRumOtelLogs", jsii.sget(cls, "RUM_OTEL_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RUM_OTEL_SPANS")
    def RUM_OTEL_SPANS(cls) -> "CfnAppMonitorRumOtelSpans":
        return typing.cast("CfnAppMonitorRumOtelSpans", jsii.sget(cls, "RUM_OTEL_SPANS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RUM_TELEMETRY_LOGS")
    def RUM_TELEMETRY_LOGS(cls) -> "CfnAppMonitorRumTelemetryLogs":
        return typing.cast("CfnAppMonitorRumTelemetryLogs", jsii.sget(cls, "RUM_TELEMETRY_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_monitor_configuration": "appMonitorConfiguration",
        "custom_events": "customEvents",
        "cw_log_enabled": "cwLogEnabled",
        "deobfuscation_configuration": "deobfuscationConfiguration",
        "domain": "domain",
        "domain_list": "domainList",
        "name": "name",
        "platform": "platform",
        "resource_policy": "resourcePolicy",
        "tags": "tags",
    },
)
class CfnAppMonitorMixinProps:
    def __init__(
        self,
        *,
        app_monitor_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppMonitorPropsMixin.AppMonitorConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppMonitorPropsMixin.CustomEventsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cw_log_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        deobfuscation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppMonitorPropsMixin.DeobfuscationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppMonitorPropsMixin.ResourcePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAppMonitorPropsMixin.

        :param app_monitor_configuration: A structure that contains much of the configuration data for the app monitor. If you are using Amazon Cognito for authorization, you must include this structure in your request, and it must include the ID of the Amazon Cognito identity pool to use for authorization. If you don't include ``AppMonitorConfiguration`` , you must set up your own authorization method. For more information, see `Authorize your application to send data to AWS <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-get-started-authorization.html>`_ . If you omit this argument, the sample rate used for CloudWatch RUM is set to 10% of the user sessions.
        :param custom_events: Specifies whether this app monitor allows the web client to define and send custom events. If you omit this parameter, custom events are ``DISABLED`` .
        :param cw_log_enabled: Data collected by CloudWatch RUM is kept by RUM for 30 days and then deleted. This parameter specifies whether CloudWatch RUM sends a copy of this telemetry data to Amazon CloudWatch Logs in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur Amazon CloudWatch Logs charges. If you omit this parameter, the default is ``false`` .
        :param deobfuscation_configuration: A structure that contains the configuration for how an app monitor can deobfuscate stack traces.
        :param domain: The top-level internet domain name for which your application has administrative authority. This parameter or the ``DomainList`` parameter is required.
        :param domain_list: List the domain names for which your application has administrative authority. This parameter or the ``Domain`` parameter is required. You can have a minimum of 1 and a maximum of 5 ``Domain`` under ``DomainList`` . Each ``Domain`` must be a minimum length of 1 and a maximum of 253 characters.
        :param name: A name for the app monitor. This parameter is required.
        :param platform: 
        :param resource_policy: Use this structure to assign a resource-based policy to a CloudWatch RUM app monitor to control access to it. Each app monitor can have one resource-based policy. The maximum size of the policy is 4 KB. To learn more about using resource policies with RUM, see `Using resource-based policies with CloudWatch RUM <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-resource-policies.html>`_ .
        :param tags: Assigns one or more tags (key-value pairs) to the app monitor. Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values. Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters. You can associate as many as 50 tags with an app monitor. For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
            
            cfn_app_monitor_mixin_props = rum_mixins.CfnAppMonitorMixinProps(
                app_monitor_configuration=rum_mixins.CfnAppMonitorPropsMixin.AppMonitorConfigurationProperty(
                    allow_cookies=False,
                    enable_xRay=False,
                    excluded_pages=["excludedPages"],
                    favorite_pages=["favoritePages"],
                    guest_role_arn="guestRoleArn",
                    identity_pool_id="identityPoolId",
                    included_pages=["includedPages"],
                    metric_destinations=[rum_mixins.CfnAppMonitorPropsMixin.MetricDestinationProperty(
                        destination="destination",
                        destination_arn="destinationArn",
                        iam_role_arn="iamRoleArn",
                        metric_definitions=[rum_mixins.CfnAppMonitorPropsMixin.MetricDefinitionProperty(
                            dimension_keys={
                                "dimension_keys_key": "dimensionKeys"
                            },
                            event_pattern="eventPattern",
                            name="name",
                            namespace="namespace",
                            unit_label="unitLabel",
                            value_key="valueKey"
                        )]
                    )],
                    session_sample_rate=123,
                    telemetries=["telemetries"]
                ),
                custom_events=rum_mixins.CfnAppMonitorPropsMixin.CustomEventsProperty(
                    status="status"
                ),
                cw_log_enabled=False,
                deobfuscation_configuration=rum_mixins.CfnAppMonitorPropsMixin.DeobfuscationConfigurationProperty(
                    java_script_source_maps=rum_mixins.CfnAppMonitorPropsMixin.JavaScriptSourceMapsProperty(
                        s3_uri="s3Uri",
                        status="status"
                    )
                ),
                domain="domain",
                domain_list=["domainList"],
                name="name",
                platform="platform",
                resource_policy=rum_mixins.CfnAppMonitorPropsMixin.ResourcePolicyProperty(
                    policy_document="policyDocument",
                    policy_revision_id="policyRevisionId"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aea5f03a3a62d758a6d22dbf170eeda446c1114ef8f89277d610835b943fdf1)
            check_type(argname="argument app_monitor_configuration", value=app_monitor_configuration, expected_type=type_hints["app_monitor_configuration"])
            check_type(argname="argument custom_events", value=custom_events, expected_type=type_hints["custom_events"])
            check_type(argname="argument cw_log_enabled", value=cw_log_enabled, expected_type=type_hints["cw_log_enabled"])
            check_type(argname="argument deobfuscation_configuration", value=deobfuscation_configuration, expected_type=type_hints["deobfuscation_configuration"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument domain_list", value=domain_list, expected_type=type_hints["domain_list"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_monitor_configuration is not None:
            self._values["app_monitor_configuration"] = app_monitor_configuration
        if custom_events is not None:
            self._values["custom_events"] = custom_events
        if cw_log_enabled is not None:
            self._values["cw_log_enabled"] = cw_log_enabled
        if deobfuscation_configuration is not None:
            self._values["deobfuscation_configuration"] = deobfuscation_configuration
        if domain is not None:
            self._values["domain"] = domain
        if domain_list is not None:
            self._values["domain_list"] = domain_list
        if name is not None:
            self._values["name"] = name
        if platform is not None:
            self._values["platform"] = platform
        if resource_policy is not None:
            self._values["resource_policy"] = resource_policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_monitor_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.AppMonitorConfigurationProperty"]]:
        '''A structure that contains much of the configuration data for the app monitor.

        If you are using Amazon Cognito for authorization, you must include this structure in your request, and it must include the ID of the Amazon Cognito identity pool to use for authorization. If you don't include ``AppMonitorConfiguration`` , you must set up your own authorization method. For more information, see `Authorize your application to send data to AWS <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-get-started-authorization.html>`_ .

        If you omit this argument, the sample rate used for CloudWatch RUM is set to 10% of the user sessions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-appmonitorconfiguration
        '''
        result = self._values.get("app_monitor_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.AppMonitorConfigurationProperty"]], result)

    @builtins.property
    def custom_events(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.CustomEventsProperty"]]:
        '''Specifies whether this app monitor allows the web client to define and send custom events.

        If you omit this parameter, custom events are ``DISABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-customevents
        '''
        result = self._values.get("custom_events")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.CustomEventsProperty"]], result)

    @builtins.property
    def cw_log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Data collected by CloudWatch RUM is kept by RUM for 30 days and then deleted.

        This parameter specifies whether CloudWatch RUM sends a copy of this telemetry data to Amazon CloudWatch Logs in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur Amazon CloudWatch Logs charges.

        If you omit this parameter, the default is ``false`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-cwlogenabled
        '''
        result = self._values.get("cw_log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def deobfuscation_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.DeobfuscationConfigurationProperty"]]:
        '''A structure that contains the configuration for how an app monitor can deobfuscate stack traces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-deobfuscationconfiguration
        '''
        result = self._values.get("deobfuscation_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.DeobfuscationConfigurationProperty"]], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The top-level internet domain name for which your application has administrative authority.

        This parameter or the ``DomainList`` parameter is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List the domain names for which your application has administrative authority. This parameter or the ``Domain`` parameter is required.

        You can have a minimum of 1 and a maximum of 5 ``Domain`` under ``DomainList`` . Each ``Domain`` must be a minimum length of 1 and a maximum of 253 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-domainlist
        '''
        result = self._values.get("domain_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the app monitor.

        This parameter is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-platform
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.ResourcePolicyProperty"]]:
        '''Use this structure to assign a resource-based policy to a CloudWatch RUM app monitor to control access to it.

        Each app monitor can have one resource-based policy. The maximum size of the policy is 4 KB. To learn more about using resource policies with RUM, see `Using resource-based policies with CloudWatch RUM <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-resource-policies.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-resourcepolicy
        '''
        result = self._values.get("resource_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.ResourcePolicyProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Assigns one or more tags (key-value pairs) to the app monitor.

        Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters.

        You can associate as many as 50 tags with an app monitor.

        For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppMonitorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAppMonitorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorPropsMixin",
):
    '''Creates a CloudWatch RUM app monitor, which you can use to collect telemetry data from your application and send it to CloudWatch RUM.

    The data includes performance and reliability information such as page load time, client-side errors, and user behavior.

    After you create an app monitor, sign in to the CloudWatch RUM console to get the JavaScript code snippet to add to your web application. For more information, see `How do I find a code snippet that I've already generated? <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-find-code-snippet.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html
    :cloudformationResource: AWS::RUM::AppMonitor
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
        
        cfn_app_monitor_props_mixin = rum_mixins.CfnAppMonitorPropsMixin(rum_mixins.CfnAppMonitorMixinProps(
            app_monitor_configuration=rum_mixins.CfnAppMonitorPropsMixin.AppMonitorConfigurationProperty(
                allow_cookies=False,
                enable_xRay=False,
                excluded_pages=["excludedPages"],
                favorite_pages=["favoritePages"],
                guest_role_arn="guestRoleArn",
                identity_pool_id="identityPoolId",
                included_pages=["includedPages"],
                metric_destinations=[rum_mixins.CfnAppMonitorPropsMixin.MetricDestinationProperty(
                    destination="destination",
                    destination_arn="destinationArn",
                    iam_role_arn="iamRoleArn",
                    metric_definitions=[rum_mixins.CfnAppMonitorPropsMixin.MetricDefinitionProperty(
                        dimension_keys={
                            "dimension_keys_key": "dimensionKeys"
                        },
                        event_pattern="eventPattern",
                        name="name",
                        namespace="namespace",
                        unit_label="unitLabel",
                        value_key="valueKey"
                    )]
                )],
                session_sample_rate=123,
                telemetries=["telemetries"]
            ),
            custom_events=rum_mixins.CfnAppMonitorPropsMixin.CustomEventsProperty(
                status="status"
            ),
            cw_log_enabled=False,
            deobfuscation_configuration=rum_mixins.CfnAppMonitorPropsMixin.DeobfuscationConfigurationProperty(
                java_script_source_maps=rum_mixins.CfnAppMonitorPropsMixin.JavaScriptSourceMapsProperty(
                    s3_uri="s3Uri",
                    status="status"
                )
            ),
            domain="domain",
            domain_list=["domainList"],
            name="name",
            platform="platform",
            resource_policy=rum_mixins.CfnAppMonitorPropsMixin.ResourcePolicyProperty(
                policy_document="policyDocument",
                policy_revision_id="policyRevisionId"
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
        props: typing.Union[CfnAppMonitorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RUM::AppMonitor``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd9612aa9327e3cc08109c5f9382fcc5ee2b3e661f0b53a01be81b6f71db731)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aad32fb1d8bc0de8adec42f9d4fc5a8c3ad7f5694a1642668be72a760184ca5b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db480358d746e0a1d3cffa77c2428925553e10638867240daa2e0a538de4d2f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAppMonitorMixinProps:
        return typing.cast(CfnAppMonitorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorPropsMixin.AppMonitorConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_cookies": "allowCookies",
            "enable_x_ray": "enableXRay",
            "excluded_pages": "excludedPages",
            "favorite_pages": "favoritePages",
            "guest_role_arn": "guestRoleArn",
            "identity_pool_id": "identityPoolId",
            "included_pages": "includedPages",
            "metric_destinations": "metricDestinations",
            "session_sample_rate": "sessionSampleRate",
            "telemetries": "telemetries",
        },
    )
    class AppMonitorConfigurationProperty:
        def __init__(
            self,
            *,
            allow_cookies: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enable_x_ray: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            excluded_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
            favorite_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
            guest_role_arn: typing.Optional[builtins.str] = None,
            identity_pool_id: typing.Optional[builtins.str] = None,
            included_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
            metric_destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppMonitorPropsMixin.MetricDestinationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            session_sample_rate: typing.Optional[jsii.Number] = None,
            telemetries: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This structure contains much of the configuration data for the app monitor.

            :param allow_cookies: If you set this to ``true`` , the CloudWatch RUM web client sets two cookies, a session cookie and a user cookie. The cookies allow the CloudWatch RUM web client to collect data relating to the number of users an application has and the behavior of the application across a sequence of events. Cookies are stored in the top-level domain of the current page.
            :param enable_x_ray: If you set this to ``true`` , CloudWatch RUM sends client-side traces to X-Ray for each sampled session. You can then see traces and segments from these user sessions in the RUM dashboard and the CloudWatch ServiceLens console. For more information, see `What is AWS X-Ray ? <https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html>`_
            :param excluded_pages: A list of URLs in your website or application to exclude from RUM data collection. You can't include both ``ExcludedPages`` and ``IncludedPages`` in the same app monitor.
            :param favorite_pages: A list of pages in your application that are to be displayed with a "favorite" icon in the CloudWatch RUM console.
            :param guest_role_arn: The ARN of the guest IAM role that is attached to the Amazon Cognito identity pool that is used to authorize the sending of data to CloudWatch RUM.
            :param identity_pool_id: The ID of the Amazon Cognito identity pool that is used to authorize the sending of data to CloudWatch RUM.
            :param included_pages: If this app monitor is to collect data from only certain pages in your application, this structure lists those pages. You can't include both ``ExcludedPages`` and ``IncludedPages`` in the same app monitor.
            :param metric_destinations: An array of structures that each define a destination that this app monitor will send extended metrics to.
            :param session_sample_rate: Specifies the portion of user sessions to use for CloudWatch RUM data collection. Choosing a higher portion gives you more data but also incurs more costs. The range for this value is 0 to 1 inclusive. Setting this to 1 means that 100% of user sessions are sampled, and setting it to 0.1 means that 10% of user sessions are sampled. If you omit this parameter, the default of 0.1 is used, and 10% of sessions will be sampled.
            :param telemetries: An array that lists the types of telemetry data that this app monitor is to collect. - ``errors`` indicates that RUM collects data about unhandled JavaScript errors raised by your application. - ``performance`` indicates that RUM collects performance data about how your application and its resources are loaded and rendered. This includes Core Web Vitals. - ``http`` indicates that RUM collects data about HTTP errors thrown by your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
                
                app_monitor_configuration_property = rum_mixins.CfnAppMonitorPropsMixin.AppMonitorConfigurationProperty(
                    allow_cookies=False,
                    enable_xRay=False,
                    excluded_pages=["excludedPages"],
                    favorite_pages=["favoritePages"],
                    guest_role_arn="guestRoleArn",
                    identity_pool_id="identityPoolId",
                    included_pages=["includedPages"],
                    metric_destinations=[rum_mixins.CfnAppMonitorPropsMixin.MetricDestinationProperty(
                        destination="destination",
                        destination_arn="destinationArn",
                        iam_role_arn="iamRoleArn",
                        metric_definitions=[rum_mixins.CfnAppMonitorPropsMixin.MetricDefinitionProperty(
                            dimension_keys={
                                "dimension_keys_key": "dimensionKeys"
                            },
                            event_pattern="eventPattern",
                            name="name",
                            namespace="namespace",
                            unit_label="unitLabel",
                            value_key="valueKey"
                        )]
                    )],
                    session_sample_rate=123,
                    telemetries=["telemetries"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__165c37d4d682fc2c738531e076fc32181ddb7f7772a354e5ad2920a12ff4c46a)
                check_type(argname="argument allow_cookies", value=allow_cookies, expected_type=type_hints["allow_cookies"])
                check_type(argname="argument enable_x_ray", value=enable_x_ray, expected_type=type_hints["enable_x_ray"])
                check_type(argname="argument excluded_pages", value=excluded_pages, expected_type=type_hints["excluded_pages"])
                check_type(argname="argument favorite_pages", value=favorite_pages, expected_type=type_hints["favorite_pages"])
                check_type(argname="argument guest_role_arn", value=guest_role_arn, expected_type=type_hints["guest_role_arn"])
                check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
                check_type(argname="argument included_pages", value=included_pages, expected_type=type_hints["included_pages"])
                check_type(argname="argument metric_destinations", value=metric_destinations, expected_type=type_hints["metric_destinations"])
                check_type(argname="argument session_sample_rate", value=session_sample_rate, expected_type=type_hints["session_sample_rate"])
                check_type(argname="argument telemetries", value=telemetries, expected_type=type_hints["telemetries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_cookies is not None:
                self._values["allow_cookies"] = allow_cookies
            if enable_x_ray is not None:
                self._values["enable_x_ray"] = enable_x_ray
            if excluded_pages is not None:
                self._values["excluded_pages"] = excluded_pages
            if favorite_pages is not None:
                self._values["favorite_pages"] = favorite_pages
            if guest_role_arn is not None:
                self._values["guest_role_arn"] = guest_role_arn
            if identity_pool_id is not None:
                self._values["identity_pool_id"] = identity_pool_id
            if included_pages is not None:
                self._values["included_pages"] = included_pages
            if metric_destinations is not None:
                self._values["metric_destinations"] = metric_destinations
            if session_sample_rate is not None:
                self._values["session_sample_rate"] = session_sample_rate
            if telemetries is not None:
                self._values["telemetries"] = telemetries

        @builtins.property
        def allow_cookies(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If you set this to ``true`` , the CloudWatch RUM web client sets two cookies, a session cookie and a user cookie.

            The cookies allow the CloudWatch RUM web client to collect data relating to the number of users an application has and the behavior of the application across a sequence of events. Cookies are stored in the top-level domain of the current page.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-allowcookies
            '''
            result = self._values.get("allow_cookies")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_x_ray(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If you set this to ``true`` , CloudWatch RUM sends client-side traces to X-Ray for each sampled session.

            You can then see traces and segments from these user sessions in the RUM dashboard and the CloudWatch ServiceLens console. For more information, see `What is AWS X-Ray ? <https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-enablexray
            '''
            result = self._values.get("enable_x_ray")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def excluded_pages(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of URLs in your website or application to exclude from RUM data collection.

            You can't include both ``ExcludedPages`` and ``IncludedPages`` in the same app monitor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-excludedpages
            '''
            result = self._values.get("excluded_pages")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def favorite_pages(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of pages in your application that are to be displayed with a "favorite" icon in the CloudWatch RUM console.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-favoritepages
            '''
            result = self._values.get("favorite_pages")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def guest_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the guest IAM role that is attached to the Amazon Cognito identity pool that is used to authorize the sending of data to CloudWatch RUM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-guestrolearn
            '''
            result = self._values.get("guest_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identity_pool_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the Amazon Cognito identity pool that is used to authorize the sending of data to CloudWatch RUM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-identitypoolid
            '''
            result = self._values.get("identity_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def included_pages(self) -> typing.Optional[typing.List[builtins.str]]:
            '''If this app monitor is to collect data from only certain pages in your application, this structure lists those pages.

            You can't include both ``ExcludedPages`` and ``IncludedPages`` in the same app monitor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-includedpages
            '''
            result = self._values.get("included_pages")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def metric_destinations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.MetricDestinationProperty"]]]]:
            '''An array of structures that each define a destination that this app monitor will send extended metrics to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-metricdestinations
            '''
            result = self._values.get("metric_destinations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.MetricDestinationProperty"]]]], result)

        @builtins.property
        def session_sample_rate(self) -> typing.Optional[jsii.Number]:
            '''Specifies the portion of user sessions to use for CloudWatch RUM data collection.

            Choosing a higher portion gives you more data but also incurs more costs.

            The range for this value is 0 to 1 inclusive. Setting this to 1 means that 100% of user sessions are sampled, and setting it to 0.1 means that 10% of user sessions are sampled.

            If you omit this parameter, the default of 0.1 is used, and 10% of sessions will be sampled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-sessionsamplerate
            '''
            result = self._values.get("session_sample_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def telemetries(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array that lists the types of telemetry data that this app monitor is to collect.

            - ``errors`` indicates that RUM collects data about unhandled JavaScript errors raised by your application.
            - ``performance`` indicates that RUM collects performance data about how your application and its resources are loaded and rendered. This includes Core Web Vitals.
            - ``http`` indicates that RUM collects data about HTTP errors thrown by your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-telemetries
            '''
            result = self._values.get("telemetries")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppMonitorConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorPropsMixin.CustomEventsProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class CustomEventsProperty:
        def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
            '''This structure specifies whether this app monitor allows the web client to define and send custom events.

            :param status: Set this to ``ENABLED`` to allow the web client to send custom events for this app monitor. Valid values are ``ENABLED`` and ``DISABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-customevents.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
                
                custom_events_property = rum_mixins.CfnAppMonitorPropsMixin.CustomEventsProperty(
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c77a320fdacd5c47edd8fc096c0d35c0845dadd4141d02c7162909a6de0a99f)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Set this to ``ENABLED`` to allow the web client to send custom events for this app monitor.

            Valid values are ``ENABLED`` and ``DISABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-customevents.html#cfn-rum-appmonitor-customevents-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomEventsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorPropsMixin.DeobfuscationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"java_script_source_maps": "javaScriptSourceMaps"},
    )
    class DeobfuscationConfigurationProperty:
        def __init__(
            self,
            *,
            java_script_source_maps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppMonitorPropsMixin.JavaScriptSourceMapsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains the configuration for how an app monitor can deobfuscate stack traces.

            :param java_script_source_maps: A structure that contains the configuration for how an app monitor can unminify JavaScript error stack traces using source maps.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-deobfuscationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
                
                deobfuscation_configuration_property = rum_mixins.CfnAppMonitorPropsMixin.DeobfuscationConfigurationProperty(
                    java_script_source_maps=rum_mixins.CfnAppMonitorPropsMixin.JavaScriptSourceMapsProperty(
                        s3_uri="s3Uri",
                        status="status"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__924b2fbd473cbe541ecd2969d79306ad1a8a44190ae88e1e41519c5bf97cbcee)
                check_type(argname="argument java_script_source_maps", value=java_script_source_maps, expected_type=type_hints["java_script_source_maps"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if java_script_source_maps is not None:
                self._values["java_script_source_maps"] = java_script_source_maps

        @builtins.property
        def java_script_source_maps(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.JavaScriptSourceMapsProperty"]]:
            '''A structure that contains the configuration for how an app monitor can unminify JavaScript error stack traces using source maps.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-deobfuscationconfiguration.html#cfn-rum-appmonitor-deobfuscationconfiguration-javascriptsourcemaps
            '''
            result = self._values.get("java_script_source_maps")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.JavaScriptSourceMapsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeobfuscationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorPropsMixin.JavaScriptSourceMapsProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_uri": "s3Uri", "status": "status"},
    )
    class JavaScriptSourceMapsProperty:
        def __init__(
            self,
            *,
            s3_uri: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains the configuration for how an app monitor can unminify JavaScript error stack traces using source maps.

            :param s3_uri: The S3Uri of the bucket or folder that stores the source map files. It is required if status is ENABLED.
            :param status: Specifies whether JavaScript error stack traces should be unminified for this app monitor. The default is for JavaScript error stack trace unminification to be ``DISABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-javascriptsourcemaps.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
                
                java_script_source_maps_property = rum_mixins.CfnAppMonitorPropsMixin.JavaScriptSourceMapsProperty(
                    s3_uri="s3Uri",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f86bc7ef0312eb1c1f5ccb231c5818985ade7f60d90606696cbe8af3f25f189)
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_uri is not None:
                self._values["s3_uri"] = s3_uri
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def s3_uri(self) -> typing.Optional[builtins.str]:
            '''The S3Uri of the bucket or folder that stores the source map files.

            It is required if status is ENABLED.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-javascriptsourcemaps.html#cfn-rum-appmonitor-javascriptsourcemaps-s3uri
            '''
            result = self._values.get("s3_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Specifies whether JavaScript error stack traces should be unminified for this app monitor.

            The default is for JavaScript error stack trace unminification to be ``DISABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-javascriptsourcemaps.html#cfn-rum-appmonitor-javascriptsourcemaps-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JavaScriptSourceMapsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorPropsMixin.MetricDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimension_keys": "dimensionKeys",
            "event_pattern": "eventPattern",
            "name": "name",
            "namespace": "namespace",
            "unit_label": "unitLabel",
            "value_key": "valueKey",
        },
    )
    class MetricDefinitionProperty:
        def __init__(
            self,
            *,
            dimension_keys: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            event_pattern: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
            unit_label: typing.Optional[builtins.str] = None,
            value_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies one custom metric or extended metric that you want the CloudWatch RUM app monitor to send to a destination.

            Valid destinations include CloudWatch and Evidently.

            By default, RUM app monitors send some metrics to CloudWatch . These default metrics are listed in `CloudWatch metrics that you can collect. <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-metrics.html>`_

            In addition to these default metrics, you can choose to send extended metrics or custom metrics or both.

            - Extended metrics enable you to send metrics with additional dimensions not included in the default metrics. You can also send extended metrics to Evidently as well as CloudWatch . The valid dimension names for the additional dimensions for extended metrics are ``BrowserName`` , ``CountryCode`` , ``DeviceType`` , ``FileType`` , ``OSName`` , and ``PageId`` . For more information, see `Extended metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-vended-metrics.html>`_ .
            - Custom metrics are metrics that you define. You can send custom metrics to CloudWatch or to CloudWatch Evidently or to both. With custom metrics, you can use any metric name and namespace, and to derive the metrics you can use any custom events, built-in events, custom attributes, or default attributes.

            You can't send custom metrics to the ``AWS/RUM`` namespace. You must send custom metrics to a custom namespace that you define. The namespace that you use can't start with ``AWS/`` . CloudWatch RUM prepends ``RUM/CustomMetrics/`` to the custom namespace that you define, so the final namespace for your metrics in CloudWatch is ``RUM/CustomMetrics/ *your-custom-namespace*`` .

            For information about syntax rules for specifying custom metrics and extended metrics, see `MetridDefinitionRequest <https://docs.aws.amazon.com/cloudwatchrum/latest/APIReference/API_MetricDefinitionRequest.html>`_ in the *CloudWatch RUM API Reference* .

            The maximum number of metric definitions that one destination can contain is 2000.

            Extended metrics sent to CloudWatch and RUM custom metrics are charged as CloudWatch custom metrics. Each combination of additional dimension name and dimension value counts as a custom metric.

            If some metric definitions that you specify are not valid, then the operation will not modify any metric definitions even if other metric definitions specified are valid.

            :param dimension_keys: This field is a map of field paths to dimension names. It defines the dimensions to associate with this metric in CloudWatch . The value of this field is used only if the metric destination is ``CloudWatch`` . If the metric destination is ``Evidently`` , the value of ``DimensionKeys`` is ignored.
            :param event_pattern: The pattern that defines the metric. RUM checks events that happen in a user's session against the pattern, and events that match the pattern are sent to the metric destination. If the metrics destination is ``CloudWatch`` and the event also matches a value in ``DimensionKeys`` , then the metric is published with the specified dimensions.
            :param name: The name of the metric that is defined in this structure.
            :param namespace: If you are creating a custom metric instead of an extended metrics, use this parameter to define the metric namespace for that custom metric. Do not specify this parameter if you are creating an extended metric. You can't use any string that starts with ``AWS/`` for your namespace.
            :param unit_label: Use this field only if you are sending this metric to CloudWatch . It defines the CloudWatch metric unit that this metric is measured in.
            :param value_key: The field within the event object that the metric value is sourced from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
                
                metric_definition_property = rum_mixins.CfnAppMonitorPropsMixin.MetricDefinitionProperty(
                    dimension_keys={
                        "dimension_keys_key": "dimensionKeys"
                    },
                    event_pattern="eventPattern",
                    name="name",
                    namespace="namespace",
                    unit_label="unitLabel",
                    value_key="valueKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efa074427f7fb8fe52547e8c9fda8901d6b8d81962d89b376264d4798065eb79)
                check_type(argname="argument dimension_keys", value=dimension_keys, expected_type=type_hints["dimension_keys"])
                check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument unit_label", value=unit_label, expected_type=type_hints["unit_label"])
                check_type(argname="argument value_key", value=value_key, expected_type=type_hints["value_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_keys is not None:
                self._values["dimension_keys"] = dimension_keys
            if event_pattern is not None:
                self._values["event_pattern"] = event_pattern
            if name is not None:
                self._values["name"] = name
            if namespace is not None:
                self._values["namespace"] = namespace
            if unit_label is not None:
                self._values["unit_label"] = unit_label
            if value_key is not None:
                self._values["value_key"] = value_key

        @builtins.property
        def dimension_keys(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''This field is a map of field paths to dimension names.

            It defines the dimensions to associate with this metric in CloudWatch . The value of this field is used only if the metric destination is ``CloudWatch`` . If the metric destination is ``Evidently`` , the value of ``DimensionKeys`` is ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdefinition.html#cfn-rum-appmonitor-metricdefinition-dimensionkeys
            '''
            result = self._values.get("dimension_keys")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def event_pattern(self) -> typing.Optional[builtins.str]:
            '''The pattern that defines the metric.

            RUM checks events that happen in a user's session against the pattern, and events that match the pattern are sent to the metric destination.

            If the metrics destination is ``CloudWatch`` and the event also matches a value in ``DimensionKeys`` , then the metric is published with the specified dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdefinition.html#cfn-rum-appmonitor-metricdefinition-eventpattern
            '''
            result = self._values.get("event_pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric that is defined in this structure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdefinition.html#cfn-rum-appmonitor-metricdefinition-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''If you are creating a custom metric instead of an extended metrics, use this parameter to define the metric namespace for that custom metric.

            Do not specify this parameter if you are creating an extended metric.

            You can't use any string that starts with ``AWS/`` for your namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdefinition.html#cfn-rum-appmonitor-metricdefinition-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit_label(self) -> typing.Optional[builtins.str]:
            '''Use this field only if you are sending this metric to CloudWatch .

            It defines the CloudWatch metric unit that this metric is measured in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdefinition.html#cfn-rum-appmonitor-metricdefinition-unitlabel
            '''
            result = self._values.get("unit_label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_key(self) -> typing.Optional[builtins.str]:
            '''The field within the event object that the metric value is sourced from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdefinition.html#cfn-rum-appmonitor-metricdefinition-valuekey
            '''
            result = self._values.get("value_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorPropsMixin.MetricDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "destination_arn": "destinationArn",
            "iam_role_arn": "iamRoleArn",
            "metric_definitions": "metricDefinitions",
        },
    )
    class MetricDestinationProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
            destination_arn: typing.Optional[builtins.str] = None,
            iam_role_arn: typing.Optional[builtins.str] = None,
            metric_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppMonitorPropsMixin.MetricDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Creates or updates a destination to receive extended metrics from CloudWatch RUM.

            You can send extended metrics to CloudWatch or to a CloudWatch Evidently experiment.

            For more information about extended metrics, see `Extended metrics that you can send to CloudWatch and CloudWatch Evidently <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-vended-metrics.html>`_ .

            :param destination: Defines the destination to send the metrics to. Valid values are ``CloudWatch`` and ``Evidently`` . If you specify ``Evidently`` , you must also specify the ARN of the CloudWatch Evidently experiment that is to be the destination and an IAM role that has permission to write to the experiment.
            :param destination_arn: Use this parameter only if ``Destination`` is ``Evidently`` . This parameter specifies the ARN of the Evidently experiment that will receive the extended metrics.
            :param iam_role_arn: This parameter is required if ``Destination`` is ``Evidently`` . If ``Destination`` is ``CloudWatch`` , do not use this parameter. This parameter specifies the ARN of an IAM role that RUM will assume to write to the Evidently experiment that you are sending metrics to. This role must have permission to write to that experiment.
            :param metric_definitions: An array of structures which define the metrics that you want to send.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
                
                metric_destination_property = rum_mixins.CfnAppMonitorPropsMixin.MetricDestinationProperty(
                    destination="destination",
                    destination_arn="destinationArn",
                    iam_role_arn="iamRoleArn",
                    metric_definitions=[rum_mixins.CfnAppMonitorPropsMixin.MetricDefinitionProperty(
                        dimension_keys={
                            "dimension_keys_key": "dimensionKeys"
                        },
                        event_pattern="eventPattern",
                        name="name",
                        namespace="namespace",
                        unit_label="unitLabel",
                        value_key="valueKey"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b1908b4a55221efe27c6c725e9c0f1bcfe0025b623e98d83f8962f5669dcf6c)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
                check_type(argname="argument metric_definitions", value=metric_definitions, expected_type=type_hints["metric_definitions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if iam_role_arn is not None:
                self._values["iam_role_arn"] = iam_role_arn
            if metric_definitions is not None:
                self._values["metric_definitions"] = metric_definitions

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''Defines the destination to send the metrics to.

            Valid values are ``CloudWatch`` and ``Evidently`` . If you specify ``Evidently`` , you must also specify the ARN of the CloudWatch Evidently experiment that is to be the destination and an IAM role that has permission to write to the experiment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdestination.html#cfn-rum-appmonitor-metricdestination-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''Use this parameter only if ``Destination`` is ``Evidently`` .

            This parameter specifies the ARN of the Evidently experiment that will receive the extended metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdestination.html#cfn-rum-appmonitor-metricdestination-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iam_role_arn(self) -> typing.Optional[builtins.str]:
            '''This parameter is required if ``Destination`` is ``Evidently`` . If ``Destination`` is ``CloudWatch`` , do not use this parameter.

            This parameter specifies the ARN of an IAM role that RUM will assume to write to the Evidently experiment that you are sending metrics to. This role must have permission to write to that experiment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdestination.html#cfn-rum-appmonitor-metricdestination-iamrolearn
            '''
            result = self._values.get("iam_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_definitions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.MetricDefinitionProperty"]]]]:
            '''An array of structures which define the metrics that you want to send.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-metricdestination.html#cfn-rum-appmonitor-metricdestination-metricdefinitions
            '''
            result = self._values.get("metric_definitions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppMonitorPropsMixin.MetricDefinitionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorPropsMixin.ResourcePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_document": "policyDocument",
            "policy_revision_id": "policyRevisionId",
        },
    )
    class ResourcePolicyProperty:
        def __init__(
            self,
            *,
            policy_document: typing.Optional[builtins.str] = None,
            policy_revision_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure to assign a resource-based policy to a CloudWatch RUM app monitor to control access to it.

            Each app monitor can have one resource-based policy. The maximum size of the policy is 4 KB. To learn more about using resource policies with RUM, see `Using resource-based policies with CloudWatch RUM <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-resource-policies.html>`_ .

            :param policy_document: The JSON to use as the resource policy. The document can be up to 4 KB in size. For more information about the contents and syntax for this policy, see `Using resource-based policies with CloudWatch RUM <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-resource-policies.html>`_ .
            :param policy_revision_id: A string value that you can use to conditionally update your policy. You can provide the revision ID of your existing policy to make mutating requests against that policy. When you assign a policy revision ID, then later requests about that policy will be rejected with an ``InvalidPolicyRevisionIdException`` error if they don't provide the correct current revision ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-resourcepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
                
                resource_policy_property = rum_mixins.CfnAppMonitorPropsMixin.ResourcePolicyProperty(
                    policy_document="policyDocument",
                    policy_revision_id="policyRevisionId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ccbe49bed964f4d5e8a9226ab8233bc96ad2e4afa4f787c1082d715929549c7f)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
                check_type(argname="argument policy_revision_id", value=policy_revision_id, expected_type=type_hints["policy_revision_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_document is not None:
                self._values["policy_document"] = policy_document
            if policy_revision_id is not None:
                self._values["policy_revision_id"] = policy_revision_id

        @builtins.property
        def policy_document(self) -> typing.Optional[builtins.str]:
            '''The JSON to use as the resource policy.

            The document can be up to 4 KB in size. For more information about the contents and syntax for this policy, see `Using resource-based policies with CloudWatch RUM <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-RUM-resource-policies.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-resourcepolicy.html#cfn-rum-appmonitor-resourcepolicy-policydocument
            '''
            result = self._values.get("policy_document")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_revision_id(self) -> typing.Optional[builtins.str]:
            '''A string value that you can use to conditionally update your policy.

            You can provide the revision ID of your existing policy to make mutating requests against that policy.

            When you assign a policy revision ID, then later requests about that policy will be rejected with an ``InvalidPolicyRevisionIdException`` error if they don't provide the correct current revision ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-resourcepolicy.html#cfn-rum-appmonitor-resourcepolicy-policyrevisionid
            '''
            result = self._values.get("policy_revision_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourcePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnAppMonitorRumOtelLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorRumOtelLogs",
):
    '''Builder for CfnAppMonitorLogsMixin to generate RUM_OTEL_LOGS for CfnAppMonitor.

    :cloudformationResource: AWS::RUM::AppMonitor
    :logType: RUM_OTEL_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
        
        cfn_app_monitor_rum_otel_logs = rum_mixins.CfnAppMonitorRumOtelLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> CfnAppMonitorLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb4adf48afdc150077261501fa29c7812d6792812115224a1c595c7b0703995)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnAppMonitorLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnAppMonitorLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4129e5707fa493989ecd02be3c79c62cafd8aa366abd80c39ef18d7de0f44abb)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnAppMonitorLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnAppMonitorLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d6ea5aafe7769e6a14360a94c2e89f431397f55e7c0eef49904d512d608a52)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnAppMonitorLogsMixin, jsii.invoke(self, "toS3", [bucket]))


class CfnAppMonitorRumOtelSpans(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorRumOtelSpans",
):
    '''Builder for CfnAppMonitorLogsMixin to generate RUM_OTEL_SPANS for CfnAppMonitor.

    :cloudformationResource: AWS::RUM::AppMonitor
    :logType: RUM_OTEL_SPANS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
        
        cfn_app_monitor_rum_otel_spans = rum_mixins.CfnAppMonitorRumOtelSpans()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> CfnAppMonitorLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be0c51aa64d62b619b9e399cd5884bcbd0e104561a598485836ea1a650e21fa)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnAppMonitorLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnAppMonitorLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a070a10a66dc4f654c744ff7257a209e3b987fa48657e28f45a3c175da62806)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnAppMonitorLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnAppMonitorLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a417181ddc3193703e26d2cc1c5d3be8831f8849b65a321e8ec3b3ec98c24e31)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnAppMonitorLogsMixin, jsii.invoke(self, "toS3", [bucket]))


class CfnAppMonitorRumTelemetryLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rum.mixins.CfnAppMonitorRumTelemetryLogs",
):
    '''Builder for CfnAppMonitorLogsMixin to generate RUM_TELEMETRY_LOGS for CfnAppMonitor.

    :cloudformationResource: AWS::RUM::AppMonitor
    :logType: RUM_TELEMETRY_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_rum import mixins as rum_mixins
        
        cfn_app_monitor_rum_telemetry_logs = rum_mixins.CfnAppMonitorRumTelemetryLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> CfnAppMonitorLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7320632e1052a040b0f634acf58004d653285d653d31ae6b2fe55f228c481a30)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnAppMonitorLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnAppMonitorLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d33d00de3dbf5e2feda53a2320a4b275ff985b93177e2b23d9eb0555f24a61)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnAppMonitorLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnAppMonitorLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd751bcf014048324d33605395cee97b4b8085a0abaeb9a3a4111c2992185d4)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnAppMonitorLogsMixin, jsii.invoke(self, "toS3", [bucket]))


__all__ = [
    "CfnAppMonitorLogsMixin",
    "CfnAppMonitorMixinProps",
    "CfnAppMonitorPropsMixin",
    "CfnAppMonitorRumOtelLogs",
    "CfnAppMonitorRumOtelSpans",
    "CfnAppMonitorRumTelemetryLogs",
]

publication.publish()

def _typecheckingstub__5d3836331e6eb13fa0f29e06c22ead9769f7cacf605e38dcf20259bddca2e6f1(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06296afb9ae59fe025ea2733e156699dead7eea264d45a2df066799c51c4b174(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea36aa2c2fec6d3f647ff3d56d72694d72bc372f48cc3f14e2ae69b9fb0c31aa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aea5f03a3a62d758a6d22dbf170eeda446c1114ef8f89277d610835b943fdf1(
    *,
    app_monitor_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppMonitorPropsMixin.AppMonitorConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppMonitorPropsMixin.CustomEventsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cw_log_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    deobfuscation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppMonitorPropsMixin.DeobfuscationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain: typing.Optional[builtins.str] = None,
    domain_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppMonitorPropsMixin.ResourcePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd9612aa9327e3cc08109c5f9382fcc5ee2b3e661f0b53a01be81b6f71db731(
    props: typing.Union[CfnAppMonitorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad32fb1d8bc0de8adec42f9d4fc5a8c3ad7f5694a1642668be72a760184ca5b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db480358d746e0a1d3cffa77c2428925553e10638867240daa2e0a538de4d2f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165c37d4d682fc2c738531e076fc32181ddb7f7772a354e5ad2920a12ff4c46a(
    *,
    allow_cookies: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_x_ray: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    excluded_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
    favorite_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
    guest_role_arn: typing.Optional[builtins.str] = None,
    identity_pool_id: typing.Optional[builtins.str] = None,
    included_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppMonitorPropsMixin.MetricDestinationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    session_sample_rate: typing.Optional[jsii.Number] = None,
    telemetries: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c77a320fdacd5c47edd8fc096c0d35c0845dadd4141d02c7162909a6de0a99f(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924b2fbd473cbe541ecd2969d79306ad1a8a44190ae88e1e41519c5bf97cbcee(
    *,
    java_script_source_maps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppMonitorPropsMixin.JavaScriptSourceMapsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f86bc7ef0312eb1c1f5ccb231c5818985ade7f60d90606696cbe8af3f25f189(
    *,
    s3_uri: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa074427f7fb8fe52547e8c9fda8901d6b8d81962d89b376264d4798065eb79(
    *,
    dimension_keys: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    event_pattern: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    unit_label: typing.Optional[builtins.str] = None,
    value_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1908b4a55221efe27c6c725e9c0f1bcfe0025b623e98d83f8962f5669dcf6c(
    *,
    destination: typing.Optional[builtins.str] = None,
    destination_arn: typing.Optional[builtins.str] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    metric_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppMonitorPropsMixin.MetricDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbe49bed964f4d5e8a9226ab8233bc96ad2e4afa4f787c1082d715929549c7f(
    *,
    policy_document: typing.Optional[builtins.str] = None,
    policy_revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb4adf48afdc150077261501fa29c7812d6792812115224a1c595c7b0703995(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4129e5707fa493989ecd02be3c79c62cafd8aa366abd80c39ef18d7de0f44abb(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d6ea5aafe7769e6a14360a94c2e89f431397f55e7c0eef49904d512d608a52(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be0c51aa64d62b619b9e399cd5884bcbd0e104561a598485836ea1a650e21fa(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a070a10a66dc4f654c744ff7257a209e3b987fa48657e28f45a3c175da62806(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a417181ddc3193703e26d2cc1c5d3be8831f8849b65a321e8ec3b3ec98c24e31(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7320632e1052a040b0f634acf58004d653285d653d31ae6b2fe55f228c481a30(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d33d00de3dbf5e2feda53a2320a4b275ff985b93177e2b23d9eb0555f24a61(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd751bcf014048324d33605395cee97b4b8085a0abaeb9a3a4111c2992185d4(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass
