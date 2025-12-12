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


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetEventDestinationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_set_name": "configurationSetName",
        "event_destination": "eventDestination",
    },
)
class CfnConfigurationSetEventDestinationMixinProps:
    def __init__(
        self,
        *,
        configuration_set_name: typing.Optional[builtins.str] = None,
        event_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetEventDestinationPropsMixin.EventDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfigurationSetEventDestinationPropsMixin.

        :param configuration_set_name: The name of the configuration set that contains the event destination.
        :param event_destination: An object that defines the event destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_configuration_set_event_destination_mixin_props = ses_mixins.CfnConfigurationSetEventDestinationMixinProps(
                configuration_set_name="configurationSetName",
                event_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.EventDestinationProperty(
                    cloud_watch_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.CloudWatchDestinationProperty(
                        dimension_configurations=[ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.DimensionConfigurationProperty(
                            default_dimension_value="defaultDimensionValue",
                            dimension_name="dimensionName",
                            dimension_value_source="dimensionValueSource"
                        )]
                    ),
                    enabled=False,
                    event_bridge_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.EventBridgeDestinationProperty(
                        event_bus_arn="eventBusArn"
                    ),
                    kinesis_firehose_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.KinesisFirehoseDestinationProperty(
                        delivery_stream_arn="deliveryStreamArn",
                        iam_role_arn="iamRoleArn"
                    ),
                    matching_event_types=["matchingEventTypes"],
                    name="name",
                    sns_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.SnsDestinationProperty(
                        topic_arn="topicArn"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e27e225a3b2cd33099995b321b2376f94e3c40ed3e856d4e9825192a4e445e)
            check_type(argname="argument configuration_set_name", value=configuration_set_name, expected_type=type_hints["configuration_set_name"])
            check_type(argname="argument event_destination", value=event_destination, expected_type=type_hints["event_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration_set_name is not None:
            self._values["configuration_set_name"] = configuration_set_name
        if event_destination is not None:
            self._values["event_destination"] = event_destination

    @builtins.property
    def configuration_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration set that contains the event destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html#cfn-ses-configurationseteventdestination-configurationsetname
        '''
        result = self._values.get("configuration_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_destination(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.EventDestinationProperty"]]:
        '''An object that defines the event destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html#cfn-ses-configurationseteventdestination-eventdestination
        '''
        result = self._values.get("event_destination")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.EventDestinationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationSetEventDestinationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigurationSetEventDestinationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetEventDestinationPropsMixin",
):
    '''Specifies a configuration set event destination.

    *Events* include message sends, deliveries, opens, clicks, bounces, and complaints. *Event destinations* are places that you can send information about these events to. For example, you can send event data to Amazon SNS to receive notifications when you receive bounces or complaints, or you can use Amazon Kinesis Data Firehose to stream data to Amazon S3 for long-term storage.

    A single configuration set can include more than one event destination.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html
    :cloudformationResource: AWS::SES::ConfigurationSetEventDestination
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_configuration_set_event_destination_props_mixin = ses_mixins.CfnConfigurationSetEventDestinationPropsMixin(ses_mixins.CfnConfigurationSetEventDestinationMixinProps(
            configuration_set_name="configurationSetName",
            event_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.EventDestinationProperty(
                cloud_watch_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.CloudWatchDestinationProperty(
                    dimension_configurations=[ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.DimensionConfigurationProperty(
                        default_dimension_value="defaultDimensionValue",
                        dimension_name="dimensionName",
                        dimension_value_source="dimensionValueSource"
                    )]
                ),
                enabled=False,
                event_bridge_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.EventBridgeDestinationProperty(
                    event_bus_arn="eventBusArn"
                ),
                kinesis_firehose_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.KinesisFirehoseDestinationProperty(
                    delivery_stream_arn="deliveryStreamArn",
                    iam_role_arn="iamRoleArn"
                ),
                matching_event_types=["matchingEventTypes"],
                name="name",
                sns_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.SnsDestinationProperty(
                    topic_arn="topicArn"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConfigurationSetEventDestinationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::ConfigurationSetEventDestination``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cff2f522e543bfbe6b36e5de1e7b022956fe4bc19f279eacbe6d77c679a14b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0224b8ca9b4ad8bb8979bc81cdaae7f528cb9c713ce20a171387807d2be68c1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198d7be1100c0ae85086623f125dd8a4405a5b66918d2d3a4d9094255fbbcb3e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigurationSetEventDestinationMixinProps:
        return typing.cast(CfnConfigurationSetEventDestinationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetEventDestinationPropsMixin.CloudWatchDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_configurations": "dimensionConfigurations"},
    )
    class CloudWatchDestinationProperty:
        def __init__(
            self,
            *,
            dimension_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetEventDestinationPropsMixin.DimensionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that defines an Amazon CloudWatch destination for email events.

            You can use Amazon CloudWatch to monitor and gain insights on your email sending metrics.

            :param dimension_configurations: An array of objects that define the dimensions to use when you send email events to Amazon CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-cloudwatchdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                cloud_watch_destination_property = ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.CloudWatchDestinationProperty(
                    dimension_configurations=[ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.DimensionConfigurationProperty(
                        default_dimension_value="defaultDimensionValue",
                        dimension_name="dimensionName",
                        dimension_value_source="dimensionValueSource"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__278c7203c8277b28601e3ab834f7e607e97ee4fba0a30d0b35e67a563bb79861)
                check_type(argname="argument dimension_configurations", value=dimension_configurations, expected_type=type_hints["dimension_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_configurations is not None:
                self._values["dimension_configurations"] = dimension_configurations

        @builtins.property
        def dimension_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.DimensionConfigurationProperty"]]]]:
            '''An array of objects that define the dimensions to use when you send email events to Amazon CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-cloudwatchdestination.html#cfn-ses-configurationseteventdestination-cloudwatchdestination-dimensionconfigurations
            '''
            result = self._values.get("dimension_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.DimensionConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetEventDestinationPropsMixin.DimensionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_dimension_value": "defaultDimensionValue",
            "dimension_name": "dimensionName",
            "dimension_value_source": "dimensionValueSource",
        },
    )
    class DimensionConfigurationProperty:
        def __init__(
            self,
            *,
            default_dimension_value: typing.Optional[builtins.str] = None,
            dimension_name: typing.Optional[builtins.str] = None,
            dimension_value_source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that defines the dimension configuration to use when you send email events to Amazon CloudWatch.

            :param default_dimension_value: The default value of the dimension that is published to Amazon CloudWatch if you don't provide the value of the dimension when you send an email. This value has to meet the following criteria: - Can only contain ASCII letters (a–z, A–Z), numbers (0–9), underscores (_), or dashes (-), at signs (@), and periods (.). - It can contain no more than 256 characters.
            :param dimension_name: The name of an Amazon CloudWatch dimension associated with an email sending metric. The name has to meet the following criteria: - It can only contain ASCII letters (a–z, A–Z), numbers (0–9), underscores (_), or dashes (-). - It can contain no more than 256 characters.
            :param dimension_value_source: The location where the Amazon SES API v2 finds the value of a dimension to publish to Amazon CloudWatch. To use the message tags that you specify using an ``X-SES-MESSAGE-TAGS`` header or a parameter to the ``SendEmail`` or ``SendRawEmail`` API, choose ``messageTag`` . To use your own email headers, choose ``emailHeader`` . To use link tags, choose ``linkTag`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                dimension_configuration_property = ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.DimensionConfigurationProperty(
                    default_dimension_value="defaultDimensionValue",
                    dimension_name="dimensionName",
                    dimension_value_source="dimensionValueSource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38ee73240cfe3db024238cac7961a819c7a8e4a7eeaec76a0d9a933fd5da0a58)
                check_type(argname="argument default_dimension_value", value=default_dimension_value, expected_type=type_hints["default_dimension_value"])
                check_type(argname="argument dimension_name", value=dimension_name, expected_type=type_hints["dimension_name"])
                check_type(argname="argument dimension_value_source", value=dimension_value_source, expected_type=type_hints["dimension_value_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_dimension_value is not None:
                self._values["default_dimension_value"] = default_dimension_value
            if dimension_name is not None:
                self._values["dimension_name"] = dimension_name
            if dimension_value_source is not None:
                self._values["dimension_value_source"] = dimension_value_source

        @builtins.property
        def default_dimension_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the dimension that is published to Amazon CloudWatch if you don't provide the value of the dimension when you send an email.

            This value has to meet the following criteria:

            - Can only contain ASCII letters (a–z, A–Z), numbers (0–9), underscores (_), or dashes (-), at signs (@), and periods (.).
            - It can contain no more than 256 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html#cfn-ses-configurationseteventdestination-dimensionconfiguration-defaultdimensionvalue
            '''
            result = self._values.get("default_dimension_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dimension_name(self) -> typing.Optional[builtins.str]:
            '''The name of an Amazon CloudWatch dimension associated with an email sending metric.

            The name has to meet the following criteria:

            - It can only contain ASCII letters (a–z, A–Z), numbers (0–9), underscores (_), or dashes (-).
            - It can contain no more than 256 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html#cfn-ses-configurationseteventdestination-dimensionconfiguration-dimensionname
            '''
            result = self._values.get("dimension_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dimension_value_source(self) -> typing.Optional[builtins.str]:
            '''The location where the Amazon SES API v2 finds the value of a dimension to publish to Amazon CloudWatch.

            To use the message tags that you specify using an ``X-SES-MESSAGE-TAGS`` header or a parameter to the ``SendEmail`` or ``SendRawEmail`` API, choose ``messageTag`` . To use your own email headers, choose ``emailHeader`` . To use link tags, choose ``linkTag`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html#cfn-ses-configurationseteventdestination-dimensionconfiguration-dimensionvaluesource
            '''
            result = self._values.get("dimension_value_source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetEventDestinationPropsMixin.EventBridgeDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"event_bus_arn": "eventBusArn"},
    )
    class EventBridgeDestinationProperty:
        def __init__(
            self,
            *,
            event_bus_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that defines an Amazon EventBridge destination for email events.

            You can use Amazon EventBridge to send notifications when certain email events occur.

            :param event_bus_arn: The Amazon Resource Name (ARN) of the Amazon EventBridge bus to publish email events to. Only the default bus is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventbridgedestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                event_bridge_destination_property = ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.EventBridgeDestinationProperty(
                    event_bus_arn="eventBusArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3ad668f98df765e5eea436e0d2380c9720d6432e00117a7f8e118ec1f07f098)
                check_type(argname="argument event_bus_arn", value=event_bus_arn, expected_type=type_hints["event_bus_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_bus_arn is not None:
                self._values["event_bus_arn"] = event_bus_arn

        @builtins.property
        def event_bus_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon EventBridge bus to publish email events to.

            Only the default bus is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventbridgedestination.html#cfn-ses-configurationseteventdestination-eventbridgedestination-eventbusarn
            '''
            result = self._values.get("event_bus_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetEventDestinationPropsMixin.EventDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_destination": "cloudWatchDestination",
            "enabled": "enabled",
            "event_bridge_destination": "eventBridgeDestination",
            "kinesis_firehose_destination": "kinesisFirehoseDestination",
            "matching_event_types": "matchingEventTypes",
            "name": "name",
            "sns_destination": "snsDestination",
        },
    )
    class EventDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetEventDestinationPropsMixin.CloudWatchDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            event_bridge_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetEventDestinationPropsMixin.EventBridgeDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_firehose_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetEventDestinationPropsMixin.KinesisFirehoseDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            matching_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
            sns_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetEventDestinationPropsMixin.SnsDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''In the Amazon SES API v2, *events* include message sends, deliveries, opens, clicks, bounces, complaints and delivery delays.

            *Event destinations* are places that you can send information about these events to. For example, you can send event data to Amazon SNS to receive notifications when you receive bounces or complaints, or you can use Amazon Kinesis Data Firehose to stream data to Amazon S3 for long-term storage.

            :param cloud_watch_destination: An object that defines an Amazon CloudWatch destination for email events. You can use Amazon CloudWatch to monitor and gain insights on your email sending metrics.
            :param enabled: If ``true`` , the event destination is enabled. When the event destination is enabled, the specified event types are sent to the destinations in this ``EventDestinationDefinition`` . If ``false`` , the event destination is disabled. When the event destination is disabled, events aren't sent to the specified destinations.
            :param event_bridge_destination: An object that defines an Amazon EventBridge destination for email events. You can use Amazon EventBridge to send notifications when certain email events occur.
            :param kinesis_firehose_destination: An object that contains the delivery stream ARN and the IAM role ARN associated with an Amazon Kinesis Firehose event destination.
            :param matching_event_types: The types of events that Amazon SES sends to the specified event destinations. - ``SEND`` - The send request was successful and SES will attempt to deliver the message to the recipient’s mail server. (If account-level or global suppression is being used, SES will still count it as a send, but delivery is suppressed.) - ``REJECT`` - SES accepted the email, but determined that it contained a virus and didn’t attempt to deliver it to the recipient’s mail server. - ``BOUNCE`` - ( *Hard bounce* ) The recipient's mail server permanently rejected the email. ( *Soft bounces* are only included when SES fails to deliver the email after retrying for a period of time.) - ``COMPLAINT`` - The email was successfully delivered to the recipient’s mail server, but the recipient marked it as spam. - ``DELIVERY`` - SES successfully delivered the email to the recipient's mail server. - ``OPEN`` - The recipient received the message and opened it in their email client. - ``CLICK`` - The recipient clicked one or more links in the email. - ``RENDERING_FAILURE`` - The email wasn't sent because of a template rendering issue. This event type can occur when template data is missing, or when there is a mismatch between template parameters and data. (This event type only occurs when you send email using the ```SendEmail`` <https://docs.aws.amazon.com/ses/latest/APIReference-V2/API_SendEmail.html>`_ or ```SendBulkEmail`` <https://docs.aws.amazon.com/ses/latest/APIReference-V2/API_SendBulkEmail.html>`_ API operations.) - ``DELIVERY_DELAY`` - The email couldn't be delivered to the recipient’s mail server because a temporary issue occurred. Delivery delays can occur, for example, when the recipient's inbox is full, or when the receiving email server experiences a transient issue. - ``SUBSCRIPTION`` - The email was successfully delivered, but the recipient updated their subscription preferences by clicking on an *unsubscribe* link as part of your `subscription management <https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html>`_ .
            :param name: The name of the event destination. The name must meet the following requirements:. - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-). - Contain 64 characters or fewer.
            :param sns_destination: An object that contains the topic ARN associated with an Amazon Simple Notification Service (Amazon SNS) event destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                event_destination_property = ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.EventDestinationProperty(
                    cloud_watch_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.CloudWatchDestinationProperty(
                        dimension_configurations=[ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.DimensionConfigurationProperty(
                            default_dimension_value="defaultDimensionValue",
                            dimension_name="dimensionName",
                            dimension_value_source="dimensionValueSource"
                        )]
                    ),
                    enabled=False,
                    event_bridge_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.EventBridgeDestinationProperty(
                        event_bus_arn="eventBusArn"
                    ),
                    kinesis_firehose_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.KinesisFirehoseDestinationProperty(
                        delivery_stream_arn="deliveryStreamArn",
                        iam_role_arn="iamRoleArn"
                    ),
                    matching_event_types=["matchingEventTypes"],
                    name="name",
                    sns_destination=ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.SnsDestinationProperty(
                        topic_arn="topicArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54fb086fb4c28ea2aea987e2fb8953f5adeffbf1b141b35d5c23b3026cc895ed)
                check_type(argname="argument cloud_watch_destination", value=cloud_watch_destination, expected_type=type_hints["cloud_watch_destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument event_bridge_destination", value=event_bridge_destination, expected_type=type_hints["event_bridge_destination"])
                check_type(argname="argument kinesis_firehose_destination", value=kinesis_firehose_destination, expected_type=type_hints["kinesis_firehose_destination"])
                check_type(argname="argument matching_event_types", value=matching_event_types, expected_type=type_hints["matching_event_types"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument sns_destination", value=sns_destination, expected_type=type_hints["sns_destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_destination is not None:
                self._values["cloud_watch_destination"] = cloud_watch_destination
            if enabled is not None:
                self._values["enabled"] = enabled
            if event_bridge_destination is not None:
                self._values["event_bridge_destination"] = event_bridge_destination
            if kinesis_firehose_destination is not None:
                self._values["kinesis_firehose_destination"] = kinesis_firehose_destination
            if matching_event_types is not None:
                self._values["matching_event_types"] = matching_event_types
            if name is not None:
                self._values["name"] = name
            if sns_destination is not None:
                self._values["sns_destination"] = sns_destination

        @builtins.property
        def cloud_watch_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.CloudWatchDestinationProperty"]]:
            '''An object that defines an Amazon CloudWatch destination for email events.

            You can use Amazon CloudWatch to monitor and gain insights on your email sending metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-cloudwatchdestination
            '''
            result = self._values.get("cloud_watch_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.CloudWatchDestinationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If ``true`` , the event destination is enabled.

            When the event destination is enabled, the specified event types are sent to the destinations in this ``EventDestinationDefinition`` .

            If ``false`` , the event destination is disabled. When the event destination is disabled, events aren't sent to the specified destinations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def event_bridge_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.EventBridgeDestinationProperty"]]:
            '''An object that defines an Amazon EventBridge destination for email events.

            You can use Amazon EventBridge to send notifications when certain email events occur.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-eventbridgedestination
            '''
            result = self._values.get("event_bridge_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.EventBridgeDestinationProperty"]], result)

        @builtins.property
        def kinesis_firehose_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.KinesisFirehoseDestinationProperty"]]:
            '''An object that contains the delivery stream ARN and the IAM role ARN associated with an Amazon Kinesis Firehose event destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-kinesisfirehosedestination
            '''
            result = self._values.get("kinesis_firehose_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.KinesisFirehoseDestinationProperty"]], result)

        @builtins.property
        def matching_event_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The types of events that Amazon SES sends to the specified event destinations.

            - ``SEND`` - The send request was successful and SES will attempt to deliver the message to the recipient’s mail server. (If account-level or global suppression is being used, SES will still count it as a send, but delivery is suppressed.)
            - ``REJECT`` - SES accepted the email, but determined that it contained a virus and didn’t attempt to deliver it to the recipient’s mail server.
            - ``BOUNCE`` - ( *Hard bounce* ) The recipient's mail server permanently rejected the email. ( *Soft bounces* are only included when SES fails to deliver the email after retrying for a period of time.)
            - ``COMPLAINT`` - The email was successfully delivered to the recipient’s mail server, but the recipient marked it as spam.
            - ``DELIVERY`` - SES successfully delivered the email to the recipient's mail server.
            - ``OPEN`` - The recipient received the message and opened it in their email client.
            - ``CLICK`` - The recipient clicked one or more links in the email.
            - ``RENDERING_FAILURE`` - The email wasn't sent because of a template rendering issue. This event type can occur when template data is missing, or when there is a mismatch between template parameters and data. (This event type only occurs when you send email using the ```SendEmail`` <https://docs.aws.amazon.com/ses/latest/APIReference-V2/API_SendEmail.html>`_ or ```SendBulkEmail`` <https://docs.aws.amazon.com/ses/latest/APIReference-V2/API_SendBulkEmail.html>`_ API operations.)
            - ``DELIVERY_DELAY`` - The email couldn't be delivered to the recipient’s mail server because a temporary issue occurred. Delivery delays can occur, for example, when the recipient's inbox is full, or when the receiving email server experiences a transient issue.
            - ``SUBSCRIPTION`` - The email was successfully delivered, but the recipient updated their subscription preferences by clicking on an *unsubscribe* link as part of your `subscription management <https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-matchingeventtypes
            '''
            result = self._values.get("matching_event_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the event destination. The name must meet the following requirements:.

            - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-).
            - Contain 64 characters or fewer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sns_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.SnsDestinationProperty"]]:
            '''An object that contains the topic ARN associated with an Amazon Simple Notification Service (Amazon SNS) event destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-snsdestination
            '''
            result = self._values.get("sns_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetEventDestinationPropsMixin.SnsDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetEventDestinationPropsMixin.KinesisFirehoseDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delivery_stream_arn": "deliveryStreamArn",
            "iam_role_arn": "iamRoleArn",
        },
    )
    class KinesisFirehoseDestinationProperty:
        def __init__(
            self,
            *,
            delivery_stream_arn: typing.Optional[builtins.str] = None,
            iam_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that defines an Amazon Kinesis Data Firehose destination for email events.

            You can use Amazon Kinesis Data Firehose to stream data to other services, such as Amazon S3 and Amazon Redshift.

            :param delivery_stream_arn: The ARN of the Amazon Kinesis Firehose stream that email sending events should be published to.
            :param iam_role_arn: The Amazon Resource Name (ARN) of the IAM role that the Amazon SES API v2 uses to send email events to the Amazon Kinesis Data Firehose stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-kinesisfirehosedestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                kinesis_firehose_destination_property = ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.KinesisFirehoseDestinationProperty(
                    delivery_stream_arn="deliveryStreamArn",
                    iam_role_arn="iamRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a0498dc4f87c224b8a16cc6b6137a482e12ed88848acae5c964ea9a89e3b9318)
                check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
                check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_stream_arn is not None:
                self._values["delivery_stream_arn"] = delivery_stream_arn
            if iam_role_arn is not None:
                self._values["iam_role_arn"] = iam_role_arn

        @builtins.property
        def delivery_stream_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon Kinesis Firehose stream that email sending events should be published to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-kinesisfirehosedestination.html#cfn-ses-configurationseteventdestination-kinesisfirehosedestination-deliverystreamarn
            '''
            result = self._values.get("delivery_stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iam_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role that the Amazon SES API v2 uses to send email events to the Amazon Kinesis Data Firehose stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-kinesisfirehosedestination.html#cfn-ses-configurationseteventdestination-kinesisfirehosedestination-iamrolearn
            '''
            result = self._values.get("iam_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetEventDestinationPropsMixin.SnsDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_arn": "topicArn"},
    )
    class SnsDestinationProperty:
        def __init__(self, *, topic_arn: typing.Optional[builtins.str] = None) -> None:
            '''Contains the topic ARN associated with an Amazon Simple Notification Service (Amazon SNS) event destination.

            Event destinations, such as Amazon SNS, are associated with configuration sets, which enable you to publish email sending events. For information about using configuration sets, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/monitor-sending-activity.html>`_ .

            :param topic_arn: The ARN of the Amazon SNS topic for email sending events. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ Amazon SNS operation. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-snsdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                sns_destination_property = ses_mixins.CfnConfigurationSetEventDestinationPropsMixin.SnsDestinationProperty(
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b318c3f2bdc1dc9b533ead761e35a46873300407a0efa18349c5388adf0e9f0)
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon SNS topic for email sending events.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ Amazon SNS operation.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-snsdestination.html#cfn-ses-configurationseteventdestination-snsdestination-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_options": "deliveryOptions",
        "name": "name",
        "reputation_options": "reputationOptions",
        "sending_options": "sendingOptions",
        "suppression_options": "suppressionOptions",
        "tags": "tags",
        "tracking_options": "trackingOptions",
        "vdm_options": "vdmOptions",
    },
)
class CfnConfigurationSetMixinProps:
    def __init__(
        self,
        *,
        delivery_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.DeliveryOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        reputation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.ReputationOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sending_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.SendingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        suppression_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.SuppressionOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tracking_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.TrackingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vdm_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.VdmOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfigurationSetPropsMixin.

        :param delivery_options: Specifies the name of the dedicated IP pool to associate with the configuration set and whether messages that use the configuration set are required to use Transport Layer Security (TLS).
        :param name: The name of the configuration set. The name must meet the following requirements:. - Contain only letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-). - Contain 64 characters or fewer.
        :param reputation_options: An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        :param sending_options: An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        :param suppression_options: An object that contains information about the suppression list preferences for your account.
        :param tags: An array of objects that define the tags (keys and values) that are associated with the configuration set.
        :param tracking_options: An object that defines the open and click tracking options for emails that you send using the configuration set.
        :param vdm_options: The Virtual Deliverability Manager (VDM) options that apply to the configuration set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_configuration_set_mixin_props = ses_mixins.CfnConfigurationSetMixinProps(
                delivery_options=ses_mixins.CfnConfigurationSetPropsMixin.DeliveryOptionsProperty(
                    max_delivery_seconds=123,
                    sending_pool_name="sendingPoolName",
                    tls_policy="tlsPolicy"
                ),
                name="name",
                reputation_options=ses_mixins.CfnConfigurationSetPropsMixin.ReputationOptionsProperty(
                    reputation_metrics_enabled=False
                ),
                sending_options=ses_mixins.CfnConfigurationSetPropsMixin.SendingOptionsProperty(
                    sending_enabled=False
                ),
                suppression_options=ses_mixins.CfnConfigurationSetPropsMixin.SuppressionOptionsProperty(
                    suppressed_reasons=["suppressedReasons"]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tracking_options=ses_mixins.CfnConfigurationSetPropsMixin.TrackingOptionsProperty(
                    custom_redirect_domain="customRedirectDomain",
                    https_policy="httpsPolicy"
                ),
                vdm_options=ses_mixins.CfnConfigurationSetPropsMixin.VdmOptionsProperty(
                    dashboard_options=ses_mixins.CfnConfigurationSetPropsMixin.DashboardOptionsProperty(
                        engagement_metrics="engagementMetrics"
                    ),
                    guardian_options=ses_mixins.CfnConfigurationSetPropsMixin.GuardianOptionsProperty(
                        optimized_shared_delivery="optimizedSharedDelivery"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfe5f4131c768a95350383a6faed15f1a8d5fba9be2a0a5f7d9ea40cb6d246d)
            check_type(argname="argument delivery_options", value=delivery_options, expected_type=type_hints["delivery_options"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument reputation_options", value=reputation_options, expected_type=type_hints["reputation_options"])
            check_type(argname="argument sending_options", value=sending_options, expected_type=type_hints["sending_options"])
            check_type(argname="argument suppression_options", value=suppression_options, expected_type=type_hints["suppression_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracking_options", value=tracking_options, expected_type=type_hints["tracking_options"])
            check_type(argname="argument vdm_options", value=vdm_options, expected_type=type_hints["vdm_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delivery_options is not None:
            self._values["delivery_options"] = delivery_options
        if name is not None:
            self._values["name"] = name
        if reputation_options is not None:
            self._values["reputation_options"] = reputation_options
        if sending_options is not None:
            self._values["sending_options"] = sending_options
        if suppression_options is not None:
            self._values["suppression_options"] = suppression_options
        if tags is not None:
            self._values["tags"] = tags
        if tracking_options is not None:
            self._values["tracking_options"] = tracking_options
        if vdm_options is not None:
            self._values["vdm_options"] = vdm_options

    @builtins.property
    def delivery_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.DeliveryOptionsProperty"]]:
        '''Specifies the name of the dedicated IP pool to associate with the configuration set and whether messages that use the configuration set are required to use Transport Layer Security (TLS).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-deliveryoptions
        '''
        result = self._values.get("delivery_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.DeliveryOptionsProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration set. The name must meet the following requirements:.

        - Contain only letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-).
        - Contain 64 characters or fewer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reputation_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.ReputationOptionsProperty"]]:
        '''An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-reputationoptions
        '''
        result = self._values.get("reputation_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.ReputationOptionsProperty"]], result)

    @builtins.property
    def sending_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.SendingOptionsProperty"]]:
        '''An object that defines whether or not Amazon SES can send email that you send using the configuration set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-sendingoptions
        '''
        result = self._values.get("sending_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.SendingOptionsProperty"]], result)

    @builtins.property
    def suppression_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.SuppressionOptionsProperty"]]:
        '''An object that contains information about the suppression list preferences for your account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-suppressionoptions
        '''
        result = self._values.get("suppression_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.SuppressionOptionsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of objects that define the tags (keys and values) that are associated with the configuration set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tracking_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.TrackingOptionsProperty"]]:
        '''An object that defines the open and click tracking options for emails that you send using the configuration set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-trackingoptions
        '''
        result = self._values.get("tracking_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.TrackingOptionsProperty"]], result)

    @builtins.property
    def vdm_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.VdmOptionsProperty"]]:
        '''The Virtual Deliverability Manager (VDM) options that apply to the configuration set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-vdmoptions
        '''
        result = self._values.get("vdm_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.VdmOptionsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigurationSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetPropsMixin",
):
    '''Configuration sets let you create groups of rules that you can apply to the emails you send using Amazon SES.

    For more information about using configuration sets, see `Using Amazon SES Configuration Sets <https://docs.aws.amazon.com/ses/latest/dg/using-configuration-sets.html>`_ in the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/>`_ .
    .. epigraph::

       *Required permissions:*

       To apply any of the resource options, you will need to have the corresponding AWS Identity and Access Management (IAM) SES API v2 permissions:

       - ``ses:GetConfigurationSet``
       - (This permission is replacing the v1 *ses:DescribeConfigurationSet* permission which will not work with these v2 resource options.)
       - ``ses:PutConfigurationSetDeliveryOptions``
       - ``ses:PutConfigurationSetReputationOptions``
       - ``ses:PutConfigurationSetSendingOptions``
       - ``ses:PutConfigurationSetSuppressionOptions``
       - ``ses:PutConfigurationSetTrackingOptions``

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html
    :cloudformationResource: AWS::SES::ConfigurationSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_configuration_set_props_mixin = ses_mixins.CfnConfigurationSetPropsMixin(ses_mixins.CfnConfigurationSetMixinProps(
            delivery_options=ses_mixins.CfnConfigurationSetPropsMixin.DeliveryOptionsProperty(
                max_delivery_seconds=123,
                sending_pool_name="sendingPoolName",
                tls_policy="tlsPolicy"
            ),
            name="name",
            reputation_options=ses_mixins.CfnConfigurationSetPropsMixin.ReputationOptionsProperty(
                reputation_metrics_enabled=False
            ),
            sending_options=ses_mixins.CfnConfigurationSetPropsMixin.SendingOptionsProperty(
                sending_enabled=False
            ),
            suppression_options=ses_mixins.CfnConfigurationSetPropsMixin.SuppressionOptionsProperty(
                suppressed_reasons=["suppressedReasons"]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tracking_options=ses_mixins.CfnConfigurationSetPropsMixin.TrackingOptionsProperty(
                custom_redirect_domain="customRedirectDomain",
                https_policy="httpsPolicy"
            ),
            vdm_options=ses_mixins.CfnConfigurationSetPropsMixin.VdmOptionsProperty(
                dashboard_options=ses_mixins.CfnConfigurationSetPropsMixin.DashboardOptionsProperty(
                    engagement_metrics="engagementMetrics"
                ),
                guardian_options=ses_mixins.CfnConfigurationSetPropsMixin.GuardianOptionsProperty(
                    optimized_shared_delivery="optimizedSharedDelivery"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConfigurationSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::ConfigurationSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e0da0fa237490c518232b5713153dd3565d3a1683274dd231d4ab676c93a823)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d97332fe975642265c6d6601eccf5f863a6befac2953235a24d23794a9f6629)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b915e344d1c6e5f975472fc35ea3c5b6a3729515de716cef74424929b9842f95)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigurationSetMixinProps:
        return typing.cast(CfnConfigurationSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetPropsMixin.DashboardOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"engagement_metrics": "engagementMetrics"},
    )
    class DashboardOptionsProperty:
        def __init__(
            self,
            *,
            engagement_metrics: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing additional settings for your VDM configuration as applicable to the Dashboard.

            :param engagement_metrics: Specifies the status of your VDM engagement metrics collection. Can be one of the following:. - ``ENABLED`` – Amazon SES enables engagement metrics for the configuration set. - ``DISABLED`` – Amazon SES disables engagement metrics for the configuration set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-dashboardoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                dashboard_options_property = ses_mixins.CfnConfigurationSetPropsMixin.DashboardOptionsProperty(
                    engagement_metrics="engagementMetrics"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a399aa1957e9a9458169527d7b871087041bfa1e9afae18fabc150e9f6d5b183)
                check_type(argname="argument engagement_metrics", value=engagement_metrics, expected_type=type_hints["engagement_metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if engagement_metrics is not None:
                self._values["engagement_metrics"] = engagement_metrics

        @builtins.property
        def engagement_metrics(self) -> typing.Optional[builtins.str]:
            '''Specifies the status of your VDM engagement metrics collection. Can be one of the following:.

            - ``ENABLED`` – Amazon SES enables engagement metrics for the configuration set.
            - ``DISABLED`` – Amazon SES disables engagement metrics for the configuration set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-dashboardoptions.html#cfn-ses-configurationset-dashboardoptions-engagementmetrics
            '''
            result = self._values.get("engagement_metrics")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashboardOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetPropsMixin.DeliveryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_delivery_seconds": "maxDeliverySeconds",
            "sending_pool_name": "sendingPoolName",
            "tls_policy": "tlsPolicy",
        },
    )
    class DeliveryOptionsProperty:
        def __init__(
            self,
            *,
            max_delivery_seconds: typing.Optional[jsii.Number] = None,
            sending_pool_name: typing.Optional[builtins.str] = None,
            tls_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the name of the dedicated IP pool to associate with the configuration set and whether messages that use the configuration set are required to use Transport Layer Security (TLS).

            :param max_delivery_seconds: The name of the configuration set used when sent through a configuration set with archiving enabled.
            :param sending_pool_name: The name of the dedicated IP pool to associate with the configuration set.
            :param tls_policy: Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS). If the value is ``REQUIRE`` , messages are only delivered if a TLS connection can be established. If the value is ``OPTIONAL`` , messages can be delivered in plain text if a TLS connection can't be established. Valid Values: ``REQUIRE | OPTIONAL``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-deliveryoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                delivery_options_property = ses_mixins.CfnConfigurationSetPropsMixin.DeliveryOptionsProperty(
                    max_delivery_seconds=123,
                    sending_pool_name="sendingPoolName",
                    tls_policy="tlsPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50c964ff9625c41ecde6e6f95fafb5c7edaed767ec9843a21c015eee83f96ab1)
                check_type(argname="argument max_delivery_seconds", value=max_delivery_seconds, expected_type=type_hints["max_delivery_seconds"])
                check_type(argname="argument sending_pool_name", value=sending_pool_name, expected_type=type_hints["sending_pool_name"])
                check_type(argname="argument tls_policy", value=tls_policy, expected_type=type_hints["tls_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_delivery_seconds is not None:
                self._values["max_delivery_seconds"] = max_delivery_seconds
            if sending_pool_name is not None:
                self._values["sending_pool_name"] = sending_pool_name
            if tls_policy is not None:
                self._values["tls_policy"] = tls_policy

        @builtins.property
        def max_delivery_seconds(self) -> typing.Optional[jsii.Number]:
            '''The name of the configuration set used when sent through a configuration set with archiving enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-deliveryoptions.html#cfn-ses-configurationset-deliveryoptions-maxdeliveryseconds
            '''
            result = self._values.get("max_delivery_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def sending_pool_name(self) -> typing.Optional[builtins.str]:
            '''The name of the dedicated IP pool to associate with the configuration set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-deliveryoptions.html#cfn-ses-configurationset-deliveryoptions-sendingpoolname
            '''
            result = self._values.get("sending_pool_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tls_policy(self) -> typing.Optional[builtins.str]:
            '''Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS).

            If the value is ``REQUIRE`` , messages are only delivered if a TLS connection can be established. If the value is ``OPTIONAL`` , messages can be delivered in plain text if a TLS connection can't be established.

            Valid Values: ``REQUIRE | OPTIONAL``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-deliveryoptions.html#cfn-ses-configurationset-deliveryoptions-tlspolicy
            '''
            result = self._values.get("tls_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeliveryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetPropsMixin.GuardianOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"optimized_shared_delivery": "optimizedSharedDelivery"},
    )
    class GuardianOptionsProperty:
        def __init__(
            self,
            *,
            optimized_shared_delivery: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing additional settings for your VDM configuration as applicable to the Guardian.

            :param optimized_shared_delivery: Specifies the status of your VDM optimized shared delivery. Can be one of the following:. - ``ENABLED`` – Amazon SES enables optimized shared delivery for the configuration set. - ``DISABLED`` – Amazon SES disables optimized shared delivery for the configuration set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-guardianoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                guardian_options_property = ses_mixins.CfnConfigurationSetPropsMixin.GuardianOptionsProperty(
                    optimized_shared_delivery="optimizedSharedDelivery"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__393285cb084b941b0dc5f69c3333db8ecfc65c5ac992d463f4b1db64e074ecb3)
                check_type(argname="argument optimized_shared_delivery", value=optimized_shared_delivery, expected_type=type_hints["optimized_shared_delivery"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if optimized_shared_delivery is not None:
                self._values["optimized_shared_delivery"] = optimized_shared_delivery

        @builtins.property
        def optimized_shared_delivery(self) -> typing.Optional[builtins.str]:
            '''Specifies the status of your VDM optimized shared delivery. Can be one of the following:.

            - ``ENABLED`` – Amazon SES enables optimized shared delivery for the configuration set.
            - ``DISABLED`` – Amazon SES disables optimized shared delivery for the configuration set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-guardianoptions.html#cfn-ses-configurationset-guardianoptions-optimizedshareddelivery
            '''
            result = self._values.get("optimized_shared_delivery")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardianOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetPropsMixin.ReputationOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"reputation_metrics_enabled": "reputationMetricsEnabled"},
    )
    class ReputationOptionsProperty:
        def __init__(
            self,
            *,
            reputation_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Enable or disable collection of reputation metrics for emails that you send using this configuration set in the current AWS Region.

            :param reputation_metrics_enabled: If ``true`` , tracking of reputation metrics is enabled for the configuration set. If ``false`` , tracking of reputation metrics is disabled for the configuration set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-reputationoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                reputation_options_property = ses_mixins.CfnConfigurationSetPropsMixin.ReputationOptionsProperty(
                    reputation_metrics_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00c52f046a0e97726bc814822ba1bae83c18b99e016bd937d30481641c2ac4eb)
                check_type(argname="argument reputation_metrics_enabled", value=reputation_metrics_enabled, expected_type=type_hints["reputation_metrics_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reputation_metrics_enabled is not None:
                self._values["reputation_metrics_enabled"] = reputation_metrics_enabled

        @builtins.property
        def reputation_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If ``true`` , tracking of reputation metrics is enabled for the configuration set.

            If ``false`` , tracking of reputation metrics is disabled for the configuration set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-reputationoptions.html#cfn-ses-configurationset-reputationoptions-reputationmetricsenabled
            '''
            result = self._values.get("reputation_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReputationOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetPropsMixin.SendingOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"sending_enabled": "sendingEnabled"},
    )
    class SendingOptionsProperty:
        def __init__(
            self,
            *,
            sending_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Used to enable or disable email sending for messages that use this configuration set in the current AWS Region.

            :param sending_enabled: If ``true`` , email sending is enabled for the configuration set. If ``false`` , email sending is disabled for the configuration set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-sendingoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                sending_options_property = ses_mixins.CfnConfigurationSetPropsMixin.SendingOptionsProperty(
                    sending_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09b9b1a7882721560036414aa16e92da29911e13e7ed11dca4057f43fb8db5fd)
                check_type(argname="argument sending_enabled", value=sending_enabled, expected_type=type_hints["sending_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sending_enabled is not None:
                self._values["sending_enabled"] = sending_enabled

        @builtins.property
        def sending_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If ``true`` , email sending is enabled for the configuration set.

            If ``false`` , email sending is disabled for the configuration set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-sendingoptions.html#cfn-ses-configurationset-sendingoptions-sendingenabled
            '''
            result = self._values.get("sending_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SendingOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetPropsMixin.SuppressionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"suppressed_reasons": "suppressedReasons"},
    )
    class SuppressionOptionsProperty:
        def __init__(
            self,
            *,
            suppressed_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that contains information about the suppression list preferences for your account.

            :param suppressed_reasons: A list that contains the reasons that email addresses are automatically added to the suppression list for your account. This list can contain any or all of the following: - ``COMPLAINT`` – Amazon SES adds an email address to the suppression list for your account when a message sent to that address results in a complaint. - ``BOUNCE`` – Amazon SES adds an email address to the suppression list for your account when a message sent to that address results in a hard bounce.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-suppressionoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                suppression_options_property = ses_mixins.CfnConfigurationSetPropsMixin.SuppressionOptionsProperty(
                    suppressed_reasons=["suppressedReasons"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17b29add32d7cb5588d64c58feeacf5d61806c1b8ffef4938ad84ba39964c642)
                check_type(argname="argument suppressed_reasons", value=suppressed_reasons, expected_type=type_hints["suppressed_reasons"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if suppressed_reasons is not None:
                self._values["suppressed_reasons"] = suppressed_reasons

        @builtins.property
        def suppressed_reasons(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list that contains the reasons that email addresses are automatically added to the suppression list for your account.

            This list can contain any or all of the following:

            - ``COMPLAINT`` – Amazon SES adds an email address to the suppression list for your account when a message sent to that address results in a complaint.
            - ``BOUNCE`` – Amazon SES adds an email address to the suppression list for your account when a message sent to that address results in a hard bounce.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-suppressionoptions.html#cfn-ses-configurationset-suppressionoptions-suppressedreasons
            '''
            result = self._values.get("suppressed_reasons")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SuppressionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetPropsMixin.TrackingOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_redirect_domain": "customRedirectDomain",
            "https_policy": "httpsPolicy",
        },
    )
    class TrackingOptionsProperty:
        def __init__(
            self,
            *,
            custom_redirect_domain: typing.Optional[builtins.str] = None,
            https_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that defines the tracking options for a configuration set.

            When you use the Amazon SES API v2 to send an email, it contains an invisible image that's used to track when recipients open your email. If your email contains links, those links are changed slightly in order to track when recipients click them.

            You can optionally configure a custom subdomain that is used to redirect email recipients to an Amazon SES-operated domain. This domain captures open and click events generated by Amazon SES emails.

            For more information, see `Configuring Custom Domains to Handle Open and Click Tracking <https://docs.aws.amazon.com/ses/latest/dg/configure-custom-open-click-domains.html>`_ in the *Amazon SES Developer Guide* .

            :param custom_redirect_domain: The custom subdomain that is used to redirect email recipients to the Amazon SES event tracking domain.
            :param https_policy: The name of the configuration set used when sent through a configuration set with archiving enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-trackingoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                tracking_options_property = ses_mixins.CfnConfigurationSetPropsMixin.TrackingOptionsProperty(
                    custom_redirect_domain="customRedirectDomain",
                    https_policy="httpsPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb1126cfc00387531c4390aa17715d5da33c2b4a86fdb358e9a1a91ab4a806e9)
                check_type(argname="argument custom_redirect_domain", value=custom_redirect_domain, expected_type=type_hints["custom_redirect_domain"])
                check_type(argname="argument https_policy", value=https_policy, expected_type=type_hints["https_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_redirect_domain is not None:
                self._values["custom_redirect_domain"] = custom_redirect_domain
            if https_policy is not None:
                self._values["https_policy"] = https_policy

        @builtins.property
        def custom_redirect_domain(self) -> typing.Optional[builtins.str]:
            '''The custom subdomain that is used to redirect email recipients to the Amazon SES event tracking domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-trackingoptions.html#cfn-ses-configurationset-trackingoptions-customredirectdomain
            '''
            result = self._values.get("custom_redirect_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def https_policy(self) -> typing.Optional[builtins.str]:
            '''The name of the configuration set used when sent through a configuration set with archiving enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-trackingoptions.html#cfn-ses-configurationset-trackingoptions-httpspolicy
            '''
            result = self._values.get("https_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrackingOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnConfigurationSetPropsMixin.VdmOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dashboard_options": "dashboardOptions",
            "guardian_options": "guardianOptions",
        },
    )
    class VdmOptionsProperty:
        def __init__(
            self,
            *,
            dashboard_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.DashboardOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            guardian_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.GuardianOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The Virtual Deliverability Manager (VDM) options that apply to a configuration set.

            :param dashboard_options: Specifies additional settings for your VDM configuration as applicable to the Dashboard.
            :param guardian_options: Specifies additional settings for your VDM configuration as applicable to the Guardian.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-vdmoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                vdm_options_property = ses_mixins.CfnConfigurationSetPropsMixin.VdmOptionsProperty(
                    dashboard_options=ses_mixins.CfnConfigurationSetPropsMixin.DashboardOptionsProperty(
                        engagement_metrics="engagementMetrics"
                    ),
                    guardian_options=ses_mixins.CfnConfigurationSetPropsMixin.GuardianOptionsProperty(
                        optimized_shared_delivery="optimizedSharedDelivery"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5db758467ad6757257bb7ccaa53d945afb5884b49db08f78de05238a9205d29)
                check_type(argname="argument dashboard_options", value=dashboard_options, expected_type=type_hints["dashboard_options"])
                check_type(argname="argument guardian_options", value=guardian_options, expected_type=type_hints["guardian_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dashboard_options is not None:
                self._values["dashboard_options"] = dashboard_options
            if guardian_options is not None:
                self._values["guardian_options"] = guardian_options

        @builtins.property
        def dashboard_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.DashboardOptionsProperty"]]:
            '''Specifies additional settings for your VDM configuration as applicable to the Dashboard.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-vdmoptions.html#cfn-ses-configurationset-vdmoptions-dashboardoptions
            '''
            result = self._values.get("dashboard_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.DashboardOptionsProperty"]], result)

        @builtins.property
        def guardian_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.GuardianOptionsProperty"]]:
            '''Specifies additional settings for your VDM configuration as applicable to the Guardian.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-vdmoptions.html#cfn-ses-configurationset-vdmoptions-guardianoptions
            '''
            result = self._values.get("guardian_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.GuardianOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VdmOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnContactListMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "contact_list_name": "contactListName",
        "description": "description",
        "tags": "tags",
        "topics": "topics",
    },
)
class CfnContactListMixinProps:
    def __init__(
        self,
        *,
        contact_list_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        topics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContactListPropsMixin.TopicProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnContactListPropsMixin.

        :param contact_list_name: The name of the contact list.
        :param description: A description of what the contact list is about.
        :param tags: The tags associated with a contact list.
        :param topics: An interest group, theme, or label within a list. A contact list can have multiple topics.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_contact_list_mixin_props = ses_mixins.CfnContactListMixinProps(
                contact_list_name="contactListName",
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                topics=[ses_mixins.CfnContactListPropsMixin.TopicProperty(
                    default_subscription_status="defaultSubscriptionStatus",
                    description="description",
                    display_name="displayName",
                    topic_name="topicName"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7e2f3268dffd898f8884ad57c24a0c710bb7df0f461194cb92d2d8ce0b975ae)
            check_type(argname="argument contact_list_name", value=contact_list_name, expected_type=type_hints["contact_list_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contact_list_name is not None:
            self._values["contact_list_name"] = contact_list_name
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags
        if topics is not None:
            self._values["topics"] = topics

    @builtins.property
    def contact_list_name(self) -> typing.Optional[builtins.str]:
        '''The name of the contact list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-contactlistname
        '''
        result = self._values.get("contact_list_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of what the contact list is about.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags associated with a contact list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def topics(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContactListPropsMixin.TopicProperty"]]]]:
        '''An interest group, theme, or label within a list.

        A contact list can have multiple topics.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-topics
        '''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContactListPropsMixin.TopicProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactListMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnContactListPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnContactListPropsMixin",
):
    '''A list that contains contacts that have subscribed to a particular topic or topics.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html
    :cloudformationResource: AWS::SES::ContactList
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_contact_list_props_mixin = ses_mixins.CfnContactListPropsMixin(ses_mixins.CfnContactListMixinProps(
            contact_list_name="contactListName",
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            topics=[ses_mixins.CfnContactListPropsMixin.TopicProperty(
                default_subscription_status="defaultSubscriptionStatus",
                description="description",
                display_name="displayName",
                topic_name="topicName"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnContactListMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::ContactList``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8a409b460930a63cf945198a7c5531cc685bde4cc81f167d4d788d491229ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cc91b412eb5cb3c677190bf068705a6431f29fda44c50a4a18e1d6d3a86081c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f083c67507749a24799113e49b3b349c5725caa5256fc80b12a94670262828)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContactListMixinProps:
        return typing.cast(CfnContactListMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnContactListPropsMixin.TopicProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_subscription_status": "defaultSubscriptionStatus",
            "description": "description",
            "display_name": "displayName",
            "topic_name": "topicName",
        },
    )
    class TopicProperty:
        def __init__(
            self,
            *,
            default_subscription_status: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            display_name: typing.Optional[builtins.str] = None,
            topic_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An interest group, theme, or label within a list.

            Lists can have multiple topics.

            :param default_subscription_status: The default subscription status to be applied to a contact if the contact has not noted their preference for subscribing to a topic.
            :param description: A description of what the topic is about, which the contact will see.
            :param display_name: The name of the topic the contact will see.
            :param topic_name: The name of the topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-contactlist-topic.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                topic_property = ses_mixins.CfnContactListPropsMixin.TopicProperty(
                    default_subscription_status="defaultSubscriptionStatus",
                    description="description",
                    display_name="displayName",
                    topic_name="topicName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b782a6ca6957118c69dc3d464e4ce72cd607cb05c141a525ee153cca66d1e9f)
                check_type(argname="argument default_subscription_status", value=default_subscription_status, expected_type=type_hints["default_subscription_status"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
                check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_subscription_status is not None:
                self._values["default_subscription_status"] = default_subscription_status
            if description is not None:
                self._values["description"] = description
            if display_name is not None:
                self._values["display_name"] = display_name
            if topic_name is not None:
                self._values["topic_name"] = topic_name

        @builtins.property
        def default_subscription_status(self) -> typing.Optional[builtins.str]:
            '''The default subscription status to be applied to a contact if the contact has not noted their preference for subscribing to a topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-contactlist-topic.html#cfn-ses-contactlist-topic-defaultsubscriptionstatus
            '''
            result = self._values.get("default_subscription_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of what the topic is about, which the contact will see.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-contactlist-topic.html#cfn-ses-contactlist-topic-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def display_name(self) -> typing.Optional[builtins.str]:
            '''The name of the topic the contact will see.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-contactlist-topic.html#cfn-ses-contactlist-topic-displayname
            '''
            result = self._values.get("display_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_name(self) -> typing.Optional[builtins.str]:
            '''The name of the topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-contactlist-topic.html#cfn-ses-contactlist-topic-topicname
            '''
            result = self._values.get("topic_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TopicProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnDedicatedIpPoolMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "pool_name": "poolName",
        "scaling_mode": "scalingMode",
        "tags": "tags",
    },
)
class CfnDedicatedIpPoolMixinProps:
    def __init__(
        self,
        *,
        pool_name: typing.Optional[builtins.str] = None,
        scaling_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDedicatedIpPoolPropsMixin.

        :param pool_name: The name of the dedicated IP pool that the IP address is associated with.
        :param scaling_mode: The type of scaling mode. The following options are available: - ``STANDARD`` - The customer controls which IPs are part of the dedicated IP pool. - ``MANAGED`` - The reputation and number of IPs are automatically managed by Amazon SES . The ``STANDARD`` option is selected by default if no value is specified. .. epigraph:: Updating *ScalingMode* doesn't require a replacement if you're updating its value from ``STANDARD`` to ``MANAGED`` . However, updating *ScalingMode* from ``MANAGED`` to ``STANDARD`` is not supported.
        :param tags: An object that defines the tags (keys and values) that you want to associate with the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_dedicated_ip_pool_mixin_props = ses_mixins.CfnDedicatedIpPoolMixinProps(
                pool_name="poolName",
                scaling_mode="scalingMode",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ec841c109b7a5ba1655ddc48d1093c0a167f2c508fe85df2178ef14d672eef)
            check_type(argname="argument pool_name", value=pool_name, expected_type=type_hints["pool_name"])
            check_type(argname="argument scaling_mode", value=scaling_mode, expected_type=type_hints["scaling_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pool_name is not None:
            self._values["pool_name"] = pool_name
        if scaling_mode is not None:
            self._values["scaling_mode"] = scaling_mode
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def pool_name(self) -> typing.Optional[builtins.str]:
        '''The name of the dedicated IP pool that the IP address is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html#cfn-ses-dedicatedippool-poolname
        '''
        result = self._values.get("pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_mode(self) -> typing.Optional[builtins.str]:
        '''The type of scaling mode.

        The following options are available:

        - ``STANDARD`` - The customer controls which IPs are part of the dedicated IP pool.
        - ``MANAGED`` - The reputation and number of IPs are automatically managed by Amazon SES .

        The ``STANDARD`` option is selected by default if no value is specified.
        .. epigraph::

           Updating *ScalingMode* doesn't require a replacement if you're updating its value from ``STANDARD`` to ``MANAGED`` . However, updating *ScalingMode* from ``MANAGED`` to ``STANDARD`` is not supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html#cfn-ses-dedicatedippool-scalingmode
        '''
        result = self._values.get("scaling_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An object that defines the tags (keys and values) that you want to associate with the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html#cfn-ses-dedicatedippool-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDedicatedIpPoolMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDedicatedIpPoolPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnDedicatedIpPoolPropsMixin",
):
    '''Create a new pool of dedicated IP addresses.

    A pool can include one or more dedicated IP addresses that are associated with your AWS account . You can associate a pool with a configuration set. When you send an email that uses that configuration set, the message is sent from one of the addresses in the associated pool.
    .. epigraph::

       You can't delete dedicated IP pools that have a ``STANDARD`` scaling mode with one or more dedicated IP addresses. This constraint doesn't apply to dedicated IP pools that have a ``MANAGED`` scaling mode.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html
    :cloudformationResource: AWS::SES::DedicatedIpPool
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_dedicated_ip_pool_props_mixin = ses_mixins.CfnDedicatedIpPoolPropsMixin(ses_mixins.CfnDedicatedIpPoolMixinProps(
            pool_name="poolName",
            scaling_mode="scalingMode",
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
        props: typing.Union[CfnDedicatedIpPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::DedicatedIpPool``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd0755e5a38cd06e1f4164b92b97f58ef092f8433e92ccc5abdfea065b02b7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa873bd70332a6f50787ed270b709a9809c073a8aa00ca64b351197d9d231df6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b7b9b33c2fe521a279f206ff5c1df9a7218c448c2d8689906fe4ccfe39efca)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDedicatedIpPoolMixinProps:
        return typing.cast(CfnDedicatedIpPoolMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnEmailIdentityMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_set_attributes": "configurationSetAttributes",
        "dkim_attributes": "dkimAttributes",
        "dkim_signing_attributes": "dkimSigningAttributes",
        "email_identity": "emailIdentity",
        "feedback_attributes": "feedbackAttributes",
        "mail_from_attributes": "mailFromAttributes",
        "tags": "tags",
    },
)
class CfnEmailIdentityMixinProps:
    def __init__(
        self,
        *,
        configuration_set_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEmailIdentityPropsMixin.ConfigurationSetAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dkim_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEmailIdentityPropsMixin.DkimAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dkim_signing_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEmailIdentityPropsMixin.DkimSigningAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        email_identity: typing.Optional[builtins.str] = None,
        feedback_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEmailIdentityPropsMixin.FeedbackAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        mail_from_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEmailIdentityPropsMixin.MailFromAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEmailIdentityPropsMixin.

        :param configuration_set_attributes: Used to associate a configuration set with an email identity.
        :param dkim_attributes: An object that contains information about the DKIM attributes for the identity.
        :param dkim_signing_attributes: If your request includes this object, Amazon SES configures the identity to use Bring Your Own DKIM (BYODKIM) for DKIM authentication purposes, or, configures the key length to be used for `Easy DKIM <https://docs.aws.amazon.com/ses/latest/DeveloperGuide/easy-dkim.html>`_ . You can only specify this object if the email identity is a domain, as opposed to an address.
        :param email_identity: The email address or domain to verify.
        :param feedback_attributes: Used to enable or disable feedback forwarding for an identity.
        :param mail_from_attributes: Used to enable or disable the custom Mail-From domain configuration for an email identity.
        :param tags: An array of objects that define the tags (keys and values) to associate with the email identity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_email_identity_mixin_props = ses_mixins.CfnEmailIdentityMixinProps(
                configuration_set_attributes=ses_mixins.CfnEmailIdentityPropsMixin.ConfigurationSetAttributesProperty(
                    configuration_set_name="configurationSetName"
                ),
                dkim_attributes=ses_mixins.CfnEmailIdentityPropsMixin.DkimAttributesProperty(
                    signing_enabled=False
                ),
                dkim_signing_attributes=ses_mixins.CfnEmailIdentityPropsMixin.DkimSigningAttributesProperty(
                    domain_signing_private_key="domainSigningPrivateKey",
                    domain_signing_selector="domainSigningSelector",
                    next_signing_key_length="nextSigningKeyLength"
                ),
                email_identity="emailIdentity",
                feedback_attributes=ses_mixins.CfnEmailIdentityPropsMixin.FeedbackAttributesProperty(
                    email_forwarding_enabled=False
                ),
                mail_from_attributes=ses_mixins.CfnEmailIdentityPropsMixin.MailFromAttributesProperty(
                    behavior_on_mx_failure="behaviorOnMxFailure",
                    mail_from_domain="mailFromDomain"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80baf74598b411a412c862527a56d9ed550a26c16dac281e18f52f928421616)
            check_type(argname="argument configuration_set_attributes", value=configuration_set_attributes, expected_type=type_hints["configuration_set_attributes"])
            check_type(argname="argument dkim_attributes", value=dkim_attributes, expected_type=type_hints["dkim_attributes"])
            check_type(argname="argument dkim_signing_attributes", value=dkim_signing_attributes, expected_type=type_hints["dkim_signing_attributes"])
            check_type(argname="argument email_identity", value=email_identity, expected_type=type_hints["email_identity"])
            check_type(argname="argument feedback_attributes", value=feedback_attributes, expected_type=type_hints["feedback_attributes"])
            check_type(argname="argument mail_from_attributes", value=mail_from_attributes, expected_type=type_hints["mail_from_attributes"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration_set_attributes is not None:
            self._values["configuration_set_attributes"] = configuration_set_attributes
        if dkim_attributes is not None:
            self._values["dkim_attributes"] = dkim_attributes
        if dkim_signing_attributes is not None:
            self._values["dkim_signing_attributes"] = dkim_signing_attributes
        if email_identity is not None:
            self._values["email_identity"] = email_identity
        if feedback_attributes is not None:
            self._values["feedback_attributes"] = feedback_attributes
        if mail_from_attributes is not None:
            self._values["mail_from_attributes"] = mail_from_attributes
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration_set_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailIdentityPropsMixin.ConfigurationSetAttributesProperty"]]:
        '''Used to associate a configuration set with an email identity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-configurationsetattributes
        '''
        result = self._values.get("configuration_set_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailIdentityPropsMixin.ConfigurationSetAttributesProperty"]], result)

    @builtins.property
    def dkim_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailIdentityPropsMixin.DkimAttributesProperty"]]:
        '''An object that contains information about the DKIM attributes for the identity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-dkimattributes
        '''
        result = self._values.get("dkim_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailIdentityPropsMixin.DkimAttributesProperty"]], result)

    @builtins.property
    def dkim_signing_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailIdentityPropsMixin.DkimSigningAttributesProperty"]]:
        '''If your request includes this object, Amazon SES configures the identity to use Bring Your Own DKIM (BYODKIM) for DKIM authentication purposes, or, configures the key length to be used for `Easy DKIM <https://docs.aws.amazon.com/ses/latest/DeveloperGuide/easy-dkim.html>`_ .

        You can only specify this object if the email identity is a domain, as opposed to an address.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-dkimsigningattributes
        '''
        result = self._values.get("dkim_signing_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailIdentityPropsMixin.DkimSigningAttributesProperty"]], result)

    @builtins.property
    def email_identity(self) -> typing.Optional[builtins.str]:
        '''The email address or domain to verify.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-emailidentity
        '''
        result = self._values.get("email_identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feedback_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailIdentityPropsMixin.FeedbackAttributesProperty"]]:
        '''Used to enable or disable feedback forwarding for an identity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-feedbackattributes
        '''
        result = self._values.get("feedback_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailIdentityPropsMixin.FeedbackAttributesProperty"]], result)

    @builtins.property
    def mail_from_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailIdentityPropsMixin.MailFromAttributesProperty"]]:
        '''Used to enable or disable the custom Mail-From domain configuration for an email identity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-mailfromattributes
        '''
        result = self._values.get("mail_from_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailIdentityPropsMixin.MailFromAttributesProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of objects that define the tags (keys and values) to associate with the email identity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailIdentityMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEmailIdentityPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnEmailIdentityPropsMixin",
):
    '''Specifies an identity for using within SES.

    An identity is an email address or domain that you use when you send email. Before you can use an identity to send email, you first have to verify it. By verifying an identity, you demonstrate that you're the owner of the identity, and that you've given Amazon SES API v2 permission to send email from the identity.

    When you verify an email address, SES sends an email to the address. Your email address is verified as soon as you follow the link in the verification email. When you verify a domain without specifying the ``DkimSigningAttributes`` properties, OR only the ``NextSigningKeyLength`` property of ``DkimSigningAttributes`` , this resource provides a set of CNAME token names and values ( *DkimDNSTokenName1* , *DkimDNSTokenValue1* , *DkimDNSTokenName2* , *DkimDNSTokenValue2* , *DkimDNSTokenName3* , *DkimDNSTokenValue3* ) as outputs. You can then add these to the DNS configuration for your domain. Your domain is verified when Amazon SES detects these records in the DNS configuration for your domain. This verification method is known as Easy DKIM.

    Alternatively, you can perform the verification process by providing your own public-private key pair. This verification method is known as Bring Your Own DKIM (BYODKIM). To use BYODKIM, your resource must include ``DkimSigningAttributes`` properties ``DomainSigningSelector`` and ``DomainSigningPrivateKey`` . When you specify this object, you provide a selector ( ``DomainSigningSelector`` ) (a component of the DNS record name that identifies the public key to use for DKIM authentication) and a private key ( ``DomainSigningPrivateKey`` ).

    Additionally, you can associate an existing configuration set with the email identity that you're verifying.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html
    :cloudformationResource: AWS::SES::EmailIdentity
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_email_identity_props_mixin = ses_mixins.CfnEmailIdentityPropsMixin(ses_mixins.CfnEmailIdentityMixinProps(
            configuration_set_attributes=ses_mixins.CfnEmailIdentityPropsMixin.ConfigurationSetAttributesProperty(
                configuration_set_name="configurationSetName"
            ),
            dkim_attributes=ses_mixins.CfnEmailIdentityPropsMixin.DkimAttributesProperty(
                signing_enabled=False
            ),
            dkim_signing_attributes=ses_mixins.CfnEmailIdentityPropsMixin.DkimSigningAttributesProperty(
                domain_signing_private_key="domainSigningPrivateKey",
                domain_signing_selector="domainSigningSelector",
                next_signing_key_length="nextSigningKeyLength"
            ),
            email_identity="emailIdentity",
            feedback_attributes=ses_mixins.CfnEmailIdentityPropsMixin.FeedbackAttributesProperty(
                email_forwarding_enabled=False
            ),
            mail_from_attributes=ses_mixins.CfnEmailIdentityPropsMixin.MailFromAttributesProperty(
                behavior_on_mx_failure="behaviorOnMxFailure",
                mail_from_domain="mailFromDomain"
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
        props: typing.Union[CfnEmailIdentityMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::EmailIdentity``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f9d5c0b190a2a20282bbee89d907848706043ffb9360d65225b6bb3f9af113)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f35123219a3fec6d5b641e0e2050a7d0bd007032bdeffc1b28d4e53e169d094c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14d3b59a92a2885d6631b375ec1fe30425d732d23697dbe4196bd34fa57a534)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEmailIdentityMixinProps:
        return typing.cast(CfnEmailIdentityMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnEmailIdentityPropsMixin.ConfigurationSetAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"configuration_set_name": "configurationSetName"},
    )
    class ConfigurationSetAttributesProperty:
        def __init__(
            self,
            *,
            configuration_set_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used to associate a configuration set with an email identity.

            :param configuration_set_name: The configuration set to associate with an email identity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-configurationsetattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                configuration_set_attributes_property = ses_mixins.CfnEmailIdentityPropsMixin.ConfigurationSetAttributesProperty(
                    configuration_set_name="configurationSetName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4daf03e8aea164f4d7b9e33291fe55c1453b4f148276092140b53cb856875545)
                check_type(argname="argument configuration_set_name", value=configuration_set_name, expected_type=type_hints["configuration_set_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration_set_name is not None:
                self._values["configuration_set_name"] = configuration_set_name

        @builtins.property
        def configuration_set_name(self) -> typing.Optional[builtins.str]:
            '''The configuration set to associate with an email identity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-configurationsetattributes.html#cfn-ses-emailidentity-configurationsetattributes-configurationsetname
            '''
            result = self._values.get("configuration_set_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationSetAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnEmailIdentityPropsMixin.DkimAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"signing_enabled": "signingEnabled"},
    )
    class DkimAttributesProperty:
        def __init__(
            self,
            *,
            signing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Used to enable or disable DKIM authentication for an email identity.

            :param signing_enabled: Sets the DKIM signing configuration for the identity. When you set this value ``true`` , then the messages that are sent from the identity are signed using DKIM. If you set this value to ``false`` , your messages are sent without DKIM signing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                dkim_attributes_property = ses_mixins.CfnEmailIdentityPropsMixin.DkimAttributesProperty(
                    signing_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eea54957e5cfa58e9513fa97116d093a30e2953c88c507149365e83d35b8b019)
                check_type(argname="argument signing_enabled", value=signing_enabled, expected_type=type_hints["signing_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if signing_enabled is not None:
                self._values["signing_enabled"] = signing_enabled

        @builtins.property
        def signing_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Sets the DKIM signing configuration for the identity.

            When you set this value ``true`` , then the messages that are sent from the identity are signed using DKIM. If you set this value to ``false`` , your messages are sent without DKIM signing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimattributes.html#cfn-ses-emailidentity-dkimattributes-signingenabled
            '''
            result = self._values.get("signing_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DkimAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnEmailIdentityPropsMixin.DkimSigningAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_signing_private_key": "domainSigningPrivateKey",
            "domain_signing_selector": "domainSigningSelector",
            "next_signing_key_length": "nextSigningKeyLength",
        },
    )
    class DkimSigningAttributesProperty:
        def __init__(
            self,
            *,
            domain_signing_private_key: typing.Optional[builtins.str] = None,
            domain_signing_selector: typing.Optional[builtins.str] = None,
            next_signing_key_length: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used to configure or change the DKIM authentication settings for an email domain identity.

            You can use this operation to do any of the following:

            - Update the signing attributes for an identity that uses Bring Your Own DKIM (BYODKIM).
            - Update the key length that should be used for Easy DKIM.
            - Change from using no DKIM authentication to using Easy DKIM.
            - Change from using no DKIM authentication to using BYODKIM.
            - Change from using Easy DKIM to using BYODKIM.
            - Change from using BYODKIM to using Easy DKIM.

            :param domain_signing_private_key: [Bring Your Own DKIM] A private key that's used to generate a DKIM signature. The private key must use 1024 or 2048-bit RSA encryption, and must be encoded using base64 encoding. .. epigraph:: Rather than embedding sensitive information directly in your CFN templates, we recommend you use dynamic parameters in the stack template to reference sensitive information that is stored and managed outside of CFN, such as in the AWS Systems Manager Parameter Store or AWS Secrets Manager. For more information, see the `Do not embed credentials in your templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ best practice.
            :param domain_signing_selector: [Bring Your Own DKIM] A string that's used to identify a public key in the DNS configuration for a domain.
            :param next_signing_key_length: [Easy DKIM] The key length of the future DKIM key pair to be generated. This can be changed at most once per day. Valid Values: ``RSA_1024_BIT | RSA_2048_BIT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimsigningattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                dkim_signing_attributes_property = ses_mixins.CfnEmailIdentityPropsMixin.DkimSigningAttributesProperty(
                    domain_signing_private_key="domainSigningPrivateKey",
                    domain_signing_selector="domainSigningSelector",
                    next_signing_key_length="nextSigningKeyLength"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6544bc4d4099a8b30dc8af2c8d9022d88ac50ef8f8b51e5c75a2190e095d3b67)
                check_type(argname="argument domain_signing_private_key", value=domain_signing_private_key, expected_type=type_hints["domain_signing_private_key"])
                check_type(argname="argument domain_signing_selector", value=domain_signing_selector, expected_type=type_hints["domain_signing_selector"])
                check_type(argname="argument next_signing_key_length", value=next_signing_key_length, expected_type=type_hints["next_signing_key_length"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_signing_private_key is not None:
                self._values["domain_signing_private_key"] = domain_signing_private_key
            if domain_signing_selector is not None:
                self._values["domain_signing_selector"] = domain_signing_selector
            if next_signing_key_length is not None:
                self._values["next_signing_key_length"] = next_signing_key_length

        @builtins.property
        def domain_signing_private_key(self) -> typing.Optional[builtins.str]:
            '''[Bring Your Own DKIM] A private key that's used to generate a DKIM signature.

            The private key must use 1024 or 2048-bit RSA encryption, and must be encoded using base64 encoding.
            .. epigraph::

               Rather than embedding sensitive information directly in your CFN templates, we recommend you use dynamic parameters in the stack template to reference sensitive information that is stored and managed outside of CFN, such as in the AWS Systems Manager Parameter Store or AWS Secrets Manager.

               For more information, see the `Do not embed credentials in your templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ best practice.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimsigningattributes.html#cfn-ses-emailidentity-dkimsigningattributes-domainsigningprivatekey
            '''
            result = self._values.get("domain_signing_private_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domain_signing_selector(self) -> typing.Optional[builtins.str]:
            '''[Bring Your Own DKIM] A string that's used to identify a public key in the DNS configuration for a domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimsigningattributes.html#cfn-ses-emailidentity-dkimsigningattributes-domainsigningselector
            '''
            result = self._values.get("domain_signing_selector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next_signing_key_length(self) -> typing.Optional[builtins.str]:
            '''[Easy DKIM] The key length of the future DKIM key pair to be generated.

            This can be changed at most once per day.

            Valid Values: ``RSA_1024_BIT | RSA_2048_BIT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimsigningattributes.html#cfn-ses-emailidentity-dkimsigningattributes-nextsigningkeylength
            '''
            result = self._values.get("next_signing_key_length")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DkimSigningAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnEmailIdentityPropsMixin.FeedbackAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"email_forwarding_enabled": "emailForwardingEnabled"},
    )
    class FeedbackAttributesProperty:
        def __init__(
            self,
            *,
            email_forwarding_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Used to enable or disable feedback forwarding for an identity.

            This setting determines what happens when an identity is used to send an email that results in a bounce or complaint event.

            :param email_forwarding_enabled: Sets the feedback forwarding configuration for the identity. If the value is ``true`` , you receive email notifications when bounce or complaint events occur. These notifications are sent to the address that you specified in the ``Return-Path`` header of the original email. You're required to have a method of tracking bounces and complaints. If you haven't set up another mechanism for receiving bounce or complaint notifications (for example, by setting up an event destination), you receive an email notification when these events occur (even if this setting is disabled).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-feedbackattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                feedback_attributes_property = ses_mixins.CfnEmailIdentityPropsMixin.FeedbackAttributesProperty(
                    email_forwarding_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__52f23ec482368055e2d836776cf885e9a83fb56688275f54905dc5705e68793a)
                check_type(argname="argument email_forwarding_enabled", value=email_forwarding_enabled, expected_type=type_hints["email_forwarding_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email_forwarding_enabled is not None:
                self._values["email_forwarding_enabled"] = email_forwarding_enabled

        @builtins.property
        def email_forwarding_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Sets the feedback forwarding configuration for the identity.

            If the value is ``true`` , you receive email notifications when bounce or complaint events occur. These notifications are sent to the address that you specified in the ``Return-Path`` header of the original email.

            You're required to have a method of tracking bounces and complaints. If you haven't set up another mechanism for receiving bounce or complaint notifications (for example, by setting up an event destination), you receive an email notification when these events occur (even if this setting is disabled).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-feedbackattributes.html#cfn-ses-emailidentity-feedbackattributes-emailforwardingenabled
            '''
            result = self._values.get("email_forwarding_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FeedbackAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnEmailIdentityPropsMixin.MailFromAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "behavior_on_mx_failure": "behaviorOnMxFailure",
            "mail_from_domain": "mailFromDomain",
        },
    )
    class MailFromAttributesProperty:
        def __init__(
            self,
            *,
            behavior_on_mx_failure: typing.Optional[builtins.str] = None,
            mail_from_domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used to enable or disable the custom Mail-From domain configuration for an email identity.

            :param behavior_on_mx_failure: The action to take if the required MX record isn't found when you send an email. When you set this value to ``USE_DEFAULT_VALUE`` , the mail is sent using *amazonses.com* as the MAIL FROM domain. When you set this value to ``REJECT_MESSAGE`` , the Amazon SES API v2 returns a ``MailFromDomainNotVerified`` error, and doesn't attempt to deliver the email. These behaviors are taken when the custom MAIL FROM domain configuration is in the ``Pending`` , ``Failed`` , and ``TemporaryFailure`` states. Valid Values: ``USE_DEFAULT_VALUE | REJECT_MESSAGE``
            :param mail_from_domain: The custom MAIL FROM domain that you want the verified identity to use. The MAIL FROM domain must meet the following criteria: - It has to be a subdomain of the verified identity. - It can't be used to receive email. - It can't be used in a "From" address if the MAIL FROM domain is a destination for feedback forwarding emails.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-mailfromattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                mail_from_attributes_property = ses_mixins.CfnEmailIdentityPropsMixin.MailFromAttributesProperty(
                    behavior_on_mx_failure="behaviorOnMxFailure",
                    mail_from_domain="mailFromDomain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78993d12b65a26772c6e5898e08a7fd560e1e2d1b5d5993a41efaaffd00af643)
                check_type(argname="argument behavior_on_mx_failure", value=behavior_on_mx_failure, expected_type=type_hints["behavior_on_mx_failure"])
                check_type(argname="argument mail_from_domain", value=mail_from_domain, expected_type=type_hints["mail_from_domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if behavior_on_mx_failure is not None:
                self._values["behavior_on_mx_failure"] = behavior_on_mx_failure
            if mail_from_domain is not None:
                self._values["mail_from_domain"] = mail_from_domain

        @builtins.property
        def behavior_on_mx_failure(self) -> typing.Optional[builtins.str]:
            '''The action to take if the required MX record isn't found when you send an email.

            When you set this value to ``USE_DEFAULT_VALUE`` , the mail is sent using *amazonses.com* as the MAIL FROM domain. When you set this value to ``REJECT_MESSAGE`` , the Amazon SES API v2 returns a ``MailFromDomainNotVerified`` error, and doesn't attempt to deliver the email.

            These behaviors are taken when the custom MAIL FROM domain configuration is in the ``Pending`` , ``Failed`` , and ``TemporaryFailure`` states.

            Valid Values: ``USE_DEFAULT_VALUE | REJECT_MESSAGE``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-mailfromattributes.html#cfn-ses-emailidentity-mailfromattributes-behavioronmxfailure
            '''
            result = self._values.get("behavior_on_mx_failure")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mail_from_domain(self) -> typing.Optional[builtins.str]:
            '''The custom MAIL FROM domain that you want the verified identity to use.

            The MAIL FROM domain must meet the following criteria:

            - It has to be a subdomain of the verified identity.
            - It can't be used to receive email.
            - It can't be used in a "From" address if the MAIL FROM domain is a destination for feedback forwarding emails.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-mailfromattributes.html#cfn-ses-emailidentity-mailfromattributes-mailfromdomain
            '''
            result = self._values.get("mail_from_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MailFromAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerAddonInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={"addon_subscription_id": "addonSubscriptionId", "tags": "tags"},
)
class CfnMailManagerAddonInstanceMixinProps:
    def __init__(
        self,
        *,
        addon_subscription_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMailManagerAddonInstancePropsMixin.

        :param addon_subscription_id: The subscription ID for the instance.
        :param tags: The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddoninstance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_mail_manager_addon_instance_mixin_props = ses_mixins.CfnMailManagerAddonInstanceMixinProps(
                addon_subscription_id="addonSubscriptionId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129bdeef175fb86109b065004ddc627392c2cf1e0a472746c17e0186c42d4e94)
            check_type(argname="argument addon_subscription_id", value=addon_subscription_id, expected_type=type_hints["addon_subscription_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if addon_subscription_id is not None:
            self._values["addon_subscription_id"] = addon_subscription_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def addon_subscription_id(self) -> typing.Optional[builtins.str]:
        '''The subscription ID for the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddoninstance.html#cfn-ses-mailmanageraddoninstance-addonsubscriptionid
        '''
        result = self._values.get("addon_subscription_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for the resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddoninstance.html#cfn-ses-mailmanageraddoninstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMailManagerAddonInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMailManagerAddonInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerAddonInstancePropsMixin",
):
    '''Creates an Add On instance for the subscription indicated in the request.

    The resulting Amazon Resource Name (ARN) can be used in a conditional statement for a rule set or traffic policy.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddoninstance.html
    :cloudformationResource: AWS::SES::MailManagerAddonInstance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_mail_manager_addon_instance_props_mixin = ses_mixins.CfnMailManagerAddonInstancePropsMixin(ses_mixins.CfnMailManagerAddonInstanceMixinProps(
            addon_subscription_id="addonSubscriptionId",
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
        props: typing.Union[CfnMailManagerAddonInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::MailManagerAddonInstance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256e5b34474c400c053d9b33586852010984d80e992bae780184cb607c5d442d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26734697e9e95331bb6367f4fab86b9446fa61dfcef318255247c848f8d5d639)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6312ae4fc076deb9baffeeffc0edc4badd0a3384c30a86d2fd01e22265caac)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMailManagerAddonInstanceMixinProps:
        return typing.cast(CfnMailManagerAddonInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerAddonSubscriptionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"addon_name": "addonName", "tags": "tags"},
)
class CfnMailManagerAddonSubscriptionMixinProps:
    def __init__(
        self,
        *,
        addon_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMailManagerAddonSubscriptionPropsMixin.

        :param addon_name: The name of the Add On to subscribe to. You can only have one subscription for each Add On name. Valid Values: ``TRENDMICRO_VSAPI | SPAMHAUS_DBL | ABUSIX_MAIL_INTELLIGENCE | VADE_ADVANCED_EMAIL_SECURITY``
        :param tags: The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddonsubscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_mail_manager_addon_subscription_mixin_props = ses_mixins.CfnMailManagerAddonSubscriptionMixinProps(
                addon_name="addonName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89cba6ab1468134e4f1a4c4d220074c84afafc7d9dd39269f9e067cc77b48ba9)
            check_type(argname="argument addon_name", value=addon_name, expected_type=type_hints["addon_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if addon_name is not None:
            self._values["addon_name"] = addon_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def addon_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Add On to subscribe to.

        You can only have one subscription for each Add On name.

        Valid Values: ``TRENDMICRO_VSAPI | SPAMHAUS_DBL | ABUSIX_MAIL_INTELLIGENCE | VADE_ADVANCED_EMAIL_SECURITY``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddonsubscription.html#cfn-ses-mailmanageraddonsubscription-addonname
        '''
        result = self._values.get("addon_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for the resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddonsubscription.html#cfn-ses-mailmanageraddonsubscription-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMailManagerAddonSubscriptionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMailManagerAddonSubscriptionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerAddonSubscriptionPropsMixin",
):
    '''Creates a subscription for an Add On representing the acceptance of its terms of use and additional pricing.

    The subscription can then be used to create an instance for use in rule sets or traffic policies.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddonsubscription.html
    :cloudformationResource: AWS::SES::MailManagerAddonSubscription
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_mail_manager_addon_subscription_props_mixin = ses_mixins.CfnMailManagerAddonSubscriptionPropsMixin(ses_mixins.CfnMailManagerAddonSubscriptionMixinProps(
            addon_name="addonName",
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
        props: typing.Union[CfnMailManagerAddonSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::MailManagerAddonSubscription``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c5baee62a572b692f772971d7e2bf864dd1414ed505dc6109622e9ed07f63b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cede7c0138c28df3dd937162127b6460d2e345b108cc411df96597d6381ca90)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2db6e74506d7f5d61892d5f8418a4a76128318d59a10b224683fbd6824987d2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMailManagerAddonSubscriptionMixinProps:
        return typing.cast(CfnMailManagerAddonSubscriptionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerAddressListMixinProps",
    jsii_struct_bases=[],
    name_mapping={"address_list_name": "addressListName", "tags": "tags"},
)
class CfnMailManagerAddressListMixinProps:
    def __init__(
        self,
        *,
        address_list_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMailManagerAddressListPropsMixin.

        :param address_list_name: A user-friendly name for the address list.
        :param tags: The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddresslist.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_mail_manager_address_list_mixin_props = ses_mixins.CfnMailManagerAddressListMixinProps(
                address_list_name="addressListName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf608eaf78616f65482735ae0e5b1c5554a95502a5b70389828eafff1f1241e)
            check_type(argname="argument address_list_name", value=address_list_name, expected_type=type_hints["address_list_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address_list_name is not None:
            self._values["address_list_name"] = address_list_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def address_list_name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly name for the address list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddresslist.html#cfn-ses-mailmanageraddresslist-addresslistname
        '''
        result = self._values.get("address_list_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for the resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddresslist.html#cfn-ses-mailmanageraddresslist-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMailManagerAddressListMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMailManagerAddressListPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerAddressListPropsMixin",
):
    '''The structure representing the address lists and address list attribute that will be used in evaluation of boolean expression.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageraddresslist.html
    :cloudformationResource: AWS::SES::MailManagerAddressList
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_mail_manager_address_list_props_mixin = ses_mixins.CfnMailManagerAddressListPropsMixin(ses_mixins.CfnMailManagerAddressListMixinProps(
            address_list_name="addressListName",
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
        props: typing.Union[CfnMailManagerAddressListMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::MailManagerAddressList``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23f11e552915a4db53622722b03190e687fbb1e17bd0a5d2f0e8c50c3a15de7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b3f0fe3c4dfd6de611e8084b29281ca9618f4542ea306ffc6d48d14107fb618)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9664679023f727c7fca0089bc1359fe65e7246c2bf7976a54d14fb73125dac9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMailManagerAddressListMixinProps:
        return typing.cast(CfnMailManagerAddressListMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerArchiveMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "archive_name": "archiveName",
        "kms_key_arn": "kmsKeyArn",
        "retention": "retention",
        "tags": "tags",
    },
)
class CfnMailManagerArchiveMixinProps:
    def __init__(
        self,
        *,
        archive_name: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        retention: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerArchivePropsMixin.ArchiveRetentionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMailManagerArchivePropsMixin.

        :param archive_name: A unique name for the new archive.
        :param kms_key_arn: The Amazon Resource Name (ARN) of the KMS key for encrypting emails in the archive.
        :param retention: The period for retaining emails in the archive before automatic deletion.
        :param tags: The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerarchive.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_mail_manager_archive_mixin_props = ses_mixins.CfnMailManagerArchiveMixinProps(
                archive_name="archiveName",
                kms_key_arn="kmsKeyArn",
                retention=ses_mixins.CfnMailManagerArchivePropsMixin.ArchiveRetentionProperty(
                    retention_period="retentionPeriod"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdb34781a0afa1e6778f7e1d11f662b14684bb3de8468db0492b73223d26e75)
            check_type(argname="argument archive_name", value=archive_name, expected_type=type_hints["archive_name"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_name is not None:
            self._values["archive_name"] = archive_name
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if retention is not None:
            self._values["retention"] = retention
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def archive_name(self) -> typing.Optional[builtins.str]:
        '''A unique name for the new archive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerarchive.html#cfn-ses-mailmanagerarchive-archivename
        '''
        result = self._values.get("archive_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the KMS key for encrypting emails in the archive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerarchive.html#cfn-ses-mailmanagerarchive-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerArchivePropsMixin.ArchiveRetentionProperty"]]:
        '''The period for retaining emails in the archive before automatic deletion.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerarchive.html#cfn-ses-mailmanagerarchive-retention
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerArchivePropsMixin.ArchiveRetentionProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for the resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerarchive.html#cfn-ses-mailmanagerarchive-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMailManagerArchiveMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMailManagerArchivePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerArchivePropsMixin",
):
    '''Creates a new email archive resource for storing and retaining emails.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerarchive.html
    :cloudformationResource: AWS::SES::MailManagerArchive
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_mail_manager_archive_props_mixin = ses_mixins.CfnMailManagerArchivePropsMixin(ses_mixins.CfnMailManagerArchiveMixinProps(
            archive_name="archiveName",
            kms_key_arn="kmsKeyArn",
            retention=ses_mixins.CfnMailManagerArchivePropsMixin.ArchiveRetentionProperty(
                retention_period="retentionPeriod"
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
        props: typing.Union[CfnMailManagerArchiveMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::MailManagerArchive``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b01055708c59f220ffafb83a5711195f0fd4ecfc745df2c286c0a721ac6deb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d66cb83c9fdefe719b4d20295ce777957a0de242ddc0318db06ff14669285b95)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c45b6d712b67305f816e34e1f746126b9ecc205db24b2b5b905bcfa9c2c2d8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMailManagerArchiveMixinProps:
        return typing.cast(CfnMailManagerArchiveMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerArchivePropsMixin.ArchiveRetentionProperty",
        jsii_struct_bases=[],
        name_mapping={"retention_period": "retentionPeriod"},
    )
    class ArchiveRetentionProperty:
        def __init__(
            self,
            *,
            retention_period: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The retention policy for an email archive that specifies how long emails are kept before being automatically deleted.

            :param retention_period: The enum value sets the period for retaining emails in an archive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerarchive-archiveretention.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                archive_retention_property = ses_mixins.CfnMailManagerArchivePropsMixin.ArchiveRetentionProperty(
                    retention_period="retentionPeriod"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab61f52fcb2edf32bf747cfa0f8fb3ed5a4d2d421672d16ed27c7b95edcedef7)
                check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if retention_period is not None:
                self._values["retention_period"] = retention_period

        @builtins.property
        def retention_period(self) -> typing.Optional[builtins.str]:
            '''The enum value sets the period for retaining emails in an archive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerarchive-archiveretention.html#cfn-ses-mailmanagerarchive-archiveretention-retentionperiod
            '''
            result = self._values.get("retention_period")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArchiveRetentionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnMailManagerIngressPointApplicationLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerIngressPointApplicationLogs",
):
    '''Builder for CfnMailManagerIngressPointLogsMixin to generate APPLICATION_LOGS for CfnMailManagerIngressPoint.

    :cloudformationResource: AWS::SES::MailManagerIngressPoint
    :logType: APPLICATION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_mail_manager_ingress_point_application_logs = ses_mixins.CfnMailManagerIngressPointApplicationLogs()
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
    ) -> "CfnMailManagerIngressPointLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78aa685beb92a7b16017fb26939ae5b16b5ecfb43ca09b94c50a38d91229db2)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnMailManagerIngressPointLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnMailManagerIngressPointLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa0f4958446455a53f3f095141d0e11ca8344caffadba14d487a55eb75ff9e7)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnMailManagerIngressPointLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnMailManagerIngressPointLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8db046685f3ebbea9d865cd39e0082220cf76e7802b29f6dbf9c5405dff4520)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnMailManagerIngressPointLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnMailManagerIngressPointLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerIngressPointLogsMixin",
):
    '''Resource to provision an ingress endpoint for receiving email.

    An ingress endpoint serves as the entry point for incoming emails, allowing you to define how emails are received and processed within your AWS environment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html
    :cloudformationResource: AWS::SES::MailManagerIngressPoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_mail_manager_ingress_point_logs_mixin = ses_mixins.CfnMailManagerIngressPointLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::SES::MailManagerIngressPoint``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a6fcbb34a2c10891de86d0385859a8bebbf3ae97fb87a3e3f216648008b8172)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e615252dbc0f8508c0d606c357357d1513e80be8a063576eb523aa4ae5dae30)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf0481f80d967c4bc56a19e0dc7ea6ea6817835d7d2d767e38be69d94da197b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPLICATION_LOGS")
    def APPLICATION_LOGS(cls) -> CfnMailManagerIngressPointApplicationLogs:
        return typing.cast(CfnMailManagerIngressPointApplicationLogs, jsii.sget(cls, "APPLICATION_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TRAFFIC_POLICY_DEBUG_LOGS")
    def TRAFFIC_POLICY_DEBUG_LOGS(
        cls,
    ) -> "CfnMailManagerIngressPointTrafficPolicyDebugLogs":
        return typing.cast("CfnMailManagerIngressPointTrafficPolicyDebugLogs", jsii.sget(cls, "TRAFFIC_POLICY_DEBUG_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerIngressPointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_point_configuration": "ingressPointConfiguration",
        "ingress_point_name": "ingressPointName",
        "network_configuration": "networkConfiguration",
        "rule_set_id": "ruleSetId",
        "status_to_update": "statusToUpdate",
        "tags": "tags",
        "traffic_policy_id": "trafficPolicyId",
        "type": "type",
    },
)
class CfnMailManagerIngressPointMixinProps:
    def __init__(
        self,
        *,
        ingress_point_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerIngressPointPropsMixin.IngressPointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ingress_point_name: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerIngressPointPropsMixin.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_set_id: typing.Optional[builtins.str] = None,
        status_to_update: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        traffic_policy_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMailManagerIngressPointPropsMixin.

        :param ingress_point_configuration: The configuration of the ingress endpoint resource.
        :param ingress_point_name: A user friendly name for an ingress endpoint resource.
        :param network_configuration: The network type (IPv4-only, Dual-Stack, PrivateLink) of the ingress endpoint resource.
        :param rule_set_id: The identifier of an existing rule set that you attach to an ingress endpoint resource.
        :param status_to_update: The update status of an ingress endpoint.
        :param tags: The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        :param traffic_policy_id: The identifier of an existing traffic policy that you attach to an ingress endpoint resource.
        :param type: The type of the ingress endpoint to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_mail_manager_ingress_point_mixin_props = ses_mixins.CfnMailManagerIngressPointMixinProps(
                ingress_point_configuration=ses_mixins.CfnMailManagerIngressPointPropsMixin.IngressPointConfigurationProperty(
                    secret_arn="secretArn",
                    smtp_password="smtpPassword"
                ),
                ingress_point_name="ingressPointName",
                network_configuration=ses_mixins.CfnMailManagerIngressPointPropsMixin.NetworkConfigurationProperty(
                    private_network_configuration=ses_mixins.CfnMailManagerIngressPointPropsMixin.PrivateNetworkConfigurationProperty(
                        vpc_endpoint_id="vpcEndpointId"
                    ),
                    public_network_configuration=ses_mixins.CfnMailManagerIngressPointPropsMixin.PublicNetworkConfigurationProperty(
                        ip_type="ipType"
                    )
                ),
                rule_set_id="ruleSetId",
                status_to_update="statusToUpdate",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                traffic_policy_id="trafficPolicyId",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dbd94d5dd9e97bf382a5ccd9f09a4c5bb820797e9b7aef16dd6a7188a0a4980)
            check_type(argname="argument ingress_point_configuration", value=ingress_point_configuration, expected_type=type_hints["ingress_point_configuration"])
            check_type(argname="argument ingress_point_name", value=ingress_point_name, expected_type=type_hints["ingress_point_name"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument rule_set_id", value=rule_set_id, expected_type=type_hints["rule_set_id"])
            check_type(argname="argument status_to_update", value=status_to_update, expected_type=type_hints["status_to_update"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument traffic_policy_id", value=traffic_policy_id, expected_type=type_hints["traffic_policy_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ingress_point_configuration is not None:
            self._values["ingress_point_configuration"] = ingress_point_configuration
        if ingress_point_name is not None:
            self._values["ingress_point_name"] = ingress_point_name
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if rule_set_id is not None:
            self._values["rule_set_id"] = rule_set_id
        if status_to_update is not None:
            self._values["status_to_update"] = status_to_update
        if tags is not None:
            self._values["tags"] = tags
        if traffic_policy_id is not None:
            self._values["traffic_policy_id"] = traffic_policy_id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def ingress_point_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerIngressPointPropsMixin.IngressPointConfigurationProperty"]]:
        '''The configuration of the ingress endpoint resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html#cfn-ses-mailmanageringresspoint-ingresspointconfiguration
        '''
        result = self._values.get("ingress_point_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerIngressPointPropsMixin.IngressPointConfigurationProperty"]], result)

    @builtins.property
    def ingress_point_name(self) -> typing.Optional[builtins.str]:
        '''A user friendly name for an ingress endpoint resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html#cfn-ses-mailmanageringresspoint-ingresspointname
        '''
        result = self._values.get("ingress_point_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerIngressPointPropsMixin.NetworkConfigurationProperty"]]:
        '''The network type (IPv4-only, Dual-Stack, PrivateLink) of the ingress endpoint resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html#cfn-ses-mailmanageringresspoint-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerIngressPointPropsMixin.NetworkConfigurationProperty"]], result)

    @builtins.property
    def rule_set_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of an existing rule set that you attach to an ingress endpoint resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html#cfn-ses-mailmanageringresspoint-rulesetid
        '''
        result = self._values.get("rule_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_to_update(self) -> typing.Optional[builtins.str]:
        '''The update status of an ingress endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html#cfn-ses-mailmanageringresspoint-statustoupdate
        '''
        result = self._values.get("status_to_update")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for the resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html#cfn-ses-mailmanageringresspoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def traffic_policy_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of an existing traffic policy that you attach to an ingress endpoint resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html#cfn-ses-mailmanageringresspoint-trafficpolicyid
        '''
        result = self._values.get("traffic_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the ingress endpoint to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html#cfn-ses-mailmanageringresspoint-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMailManagerIngressPointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMailManagerIngressPointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerIngressPointPropsMixin",
):
    '''Resource to provision an ingress endpoint for receiving email.

    An ingress endpoint serves as the entry point for incoming emails, allowing you to define how emails are received and processed within your AWS environment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanageringresspoint.html
    :cloudformationResource: AWS::SES::MailManagerIngressPoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_mail_manager_ingress_point_props_mixin = ses_mixins.CfnMailManagerIngressPointPropsMixin(ses_mixins.CfnMailManagerIngressPointMixinProps(
            ingress_point_configuration=ses_mixins.CfnMailManagerIngressPointPropsMixin.IngressPointConfigurationProperty(
                secret_arn="secretArn",
                smtp_password="smtpPassword"
            ),
            ingress_point_name="ingressPointName",
            network_configuration=ses_mixins.CfnMailManagerIngressPointPropsMixin.NetworkConfigurationProperty(
                private_network_configuration=ses_mixins.CfnMailManagerIngressPointPropsMixin.PrivateNetworkConfigurationProperty(
                    vpc_endpoint_id="vpcEndpointId"
                ),
                public_network_configuration=ses_mixins.CfnMailManagerIngressPointPropsMixin.PublicNetworkConfigurationProperty(
                    ip_type="ipType"
                )
            ),
            rule_set_id="ruleSetId",
            status_to_update="statusToUpdate",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            traffic_policy_id="trafficPolicyId",
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMailManagerIngressPointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::MailManagerIngressPoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d185df3c4a480bdc61864cc8f86ce2d828769529a55949ca23cec1cc93531566)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dfaa7fd203d0826c4b5968c9c26bbdd733b6d8ab603ec8ddd0a656b3146e053)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa74a250225fc01872702d3e4e97c86645187d5afb0a6430bb1c927c54a0e1d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMailManagerIngressPointMixinProps:
        return typing.cast(CfnMailManagerIngressPointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerIngressPointPropsMixin.IngressPointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_arn": "secretArn", "smtp_password": "smtpPassword"},
    )
    class IngressPointConfigurationProperty:
        def __init__(
            self,
            *,
            secret_arn: typing.Optional[builtins.str] = None,
            smtp_password: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of the ingress endpoint resource.

            .. epigraph::

               This data type is a UNION, so only one of the following members can be specified when used or returned.

            :param secret_arn: The SecretsManager::Secret ARN of the ingress endpoint resource.
            :param smtp_password: The password of the ingress endpoint resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanageringresspoint-ingresspointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_point_configuration_property = ses_mixins.CfnMailManagerIngressPointPropsMixin.IngressPointConfigurationProperty(
                    secret_arn="secretArn",
                    smtp_password="smtpPassword"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f558beef22f9d75a1f17398f1bf91879b351e08b7ba6dfd6022d1f8f79b910f1)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument smtp_password", value=smtp_password, expected_type=type_hints["smtp_password"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if smtp_password is not None:
                self._values["smtp_password"] = smtp_password

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The SecretsManager::Secret ARN of the ingress endpoint resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanageringresspoint-ingresspointconfiguration.html#cfn-ses-mailmanageringresspoint-ingresspointconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def smtp_password(self) -> typing.Optional[builtins.str]:
            '''The password of the ingress endpoint resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanageringresspoint-ingresspointconfiguration.html#cfn-ses-mailmanageringresspoint-ingresspointconfiguration-smtppassword
            '''
            result = self._values.get("smtp_password")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressPointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerIngressPointPropsMixin.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "private_network_configuration": "privateNetworkConfiguration",
            "public_network_configuration": "publicNetworkConfiguration",
        },
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            private_network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerIngressPointPropsMixin.PrivateNetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            public_network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerIngressPointPropsMixin.PublicNetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The network type (IPv4-only, Dual-Stack, PrivateLink) of the ingress endpoint resource.

            :param private_network_configuration: Specifies the network configuration for the private ingress point.
            :param public_network_configuration: Specifies the network configuration for the public ingress point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanageringresspoint-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                network_configuration_property = ses_mixins.CfnMailManagerIngressPointPropsMixin.NetworkConfigurationProperty(
                    private_network_configuration=ses_mixins.CfnMailManagerIngressPointPropsMixin.PrivateNetworkConfigurationProperty(
                        vpc_endpoint_id="vpcEndpointId"
                    ),
                    public_network_configuration=ses_mixins.CfnMailManagerIngressPointPropsMixin.PublicNetworkConfigurationProperty(
                        ip_type="ipType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd61acdba018c44201e64acd8650e767d22fd36b3ca474f41e1570573d49aefb)
                check_type(argname="argument private_network_configuration", value=private_network_configuration, expected_type=type_hints["private_network_configuration"])
                check_type(argname="argument public_network_configuration", value=public_network_configuration, expected_type=type_hints["public_network_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if private_network_configuration is not None:
                self._values["private_network_configuration"] = private_network_configuration
            if public_network_configuration is not None:
                self._values["public_network_configuration"] = public_network_configuration

        @builtins.property
        def private_network_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerIngressPointPropsMixin.PrivateNetworkConfigurationProperty"]]:
            '''Specifies the network configuration for the private ingress point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanageringresspoint-networkconfiguration.html#cfn-ses-mailmanageringresspoint-networkconfiguration-privatenetworkconfiguration
            '''
            result = self._values.get("private_network_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerIngressPointPropsMixin.PrivateNetworkConfigurationProperty"]], result)

        @builtins.property
        def public_network_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerIngressPointPropsMixin.PublicNetworkConfigurationProperty"]]:
            '''Specifies the network configuration for the public ingress point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanageringresspoint-networkconfiguration.html#cfn-ses-mailmanageringresspoint-networkconfiguration-publicnetworkconfiguration
            '''
            result = self._values.get("public_network_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerIngressPointPropsMixin.PublicNetworkConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerIngressPointPropsMixin.PrivateNetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_endpoint_id": "vpcEndpointId"},
    )
    class PrivateNetworkConfigurationProperty:
        def __init__(
            self,
            *,
            vpc_endpoint_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the network configuration for the private ingress point.

            :param vpc_endpoint_id: The identifier of the VPC endpoint to associate with this private ingress point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanageringresspoint-privatenetworkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                private_network_configuration_property = ses_mixins.CfnMailManagerIngressPointPropsMixin.PrivateNetworkConfigurationProperty(
                    vpc_endpoint_id="vpcEndpointId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d75750eeb900636d7fbdb780bf46dea69eeaba1e3b7b151f0ec87b973f9d958f)
                check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_endpoint_id is not None:
                self._values["vpc_endpoint_id"] = vpc_endpoint_id

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the VPC endpoint to associate with this private ingress point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanageringresspoint-privatenetworkconfiguration.html#cfn-ses-mailmanageringresspoint-privatenetworkconfiguration-vpcendpointid
            '''
            result = self._values.get("vpc_endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateNetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerIngressPointPropsMixin.PublicNetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_type": "ipType"},
    )
    class PublicNetworkConfigurationProperty:
        def __init__(self, *, ip_type: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the network configuration for the public ingress point.

            :param ip_type: The IP address type for the public ingress point. Valid values are IPV4 and DUAL_STACK.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanageringresspoint-publicnetworkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                public_network_configuration_property = ses_mixins.CfnMailManagerIngressPointPropsMixin.PublicNetworkConfigurationProperty(
                    ip_type="ipType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f2a8a9a2a1176155d2f90735a160b39b4b871111305b79016aaa05e1d8574a3)
                check_type(argname="argument ip_type", value=ip_type, expected_type=type_hints["ip_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_type is not None:
                self._values["ip_type"] = ip_type

        @builtins.property
        def ip_type(self) -> typing.Optional[builtins.str]:
            '''The IP address type for the public ingress point.

            Valid values are IPV4 and DUAL_STACK.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanageringresspoint-publicnetworkconfiguration.html#cfn-ses-mailmanageringresspoint-publicnetworkconfiguration-iptype
            '''
            result = self._values.get("ip_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicNetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnMailManagerIngressPointTrafficPolicyDebugLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerIngressPointTrafficPolicyDebugLogs",
):
    '''Builder for CfnMailManagerIngressPointLogsMixin to generate TRAFFIC_POLICY_DEBUG_LOGS for CfnMailManagerIngressPoint.

    :cloudformationResource: AWS::SES::MailManagerIngressPoint
    :logType: TRAFFIC_POLICY_DEBUG_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_mail_manager_ingress_point_traffic_policy_debug_logs = ses_mixins.CfnMailManagerIngressPointTrafficPolicyDebugLogs()
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
    ) -> CfnMailManagerIngressPointLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bddc7a91c1124e7c6727457873214e0da3206362918bf4d622f05be6a9891c2)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnMailManagerIngressPointLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnMailManagerIngressPointLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37c1531e36b25221fe58b18d015ca0bae514fb9b39a59729275d5dca6bd3fc8)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnMailManagerIngressPointLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnMailManagerIngressPointLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2380c9270fbf6e609973d7bf68619def6423c4c9e5e3aaf376cad71f703a8b73)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnMailManagerIngressPointLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRelayMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication": "authentication",
        "relay_name": "relayName",
        "server_name": "serverName",
        "server_port": "serverPort",
        "tags": "tags",
    },
)
class CfnMailManagerRelayMixinProps:
    def __init__(
        self,
        *,
        authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRelayPropsMixin.RelayAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        relay_name: typing.Optional[builtins.str] = None,
        server_name: typing.Optional[builtins.str] = None,
        server_port: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMailManagerRelayPropsMixin.

        :param authentication: Authentication for the relay destination server—specify the secretARN where the SMTP credentials are stored.
        :param relay_name: The unique relay name.
        :param server_name: The destination relay server address.
        :param server_port: The destination relay server port.
        :param tags: The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerrelay.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            # no_authentication: Any
            
            cfn_mail_manager_relay_mixin_props = ses_mixins.CfnMailManagerRelayMixinProps(
                authentication=ses_mixins.CfnMailManagerRelayPropsMixin.RelayAuthenticationProperty(
                    no_authentication=no_authentication,
                    secret_arn="secretArn"
                ),
                relay_name="relayName",
                server_name="serverName",
                server_port=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40548dccf99429568349c7532fcea9258b0955f1fa46cfac45aee25e8bddf6c)
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument relay_name", value=relay_name, expected_type=type_hints["relay_name"])
            check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
            check_type(argname="argument server_port", value=server_port, expected_type=type_hints["server_port"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication is not None:
            self._values["authentication"] = authentication
        if relay_name is not None:
            self._values["relay_name"] = relay_name
        if server_name is not None:
            self._values["server_name"] = server_name
        if server_port is not None:
            self._values["server_port"] = server_port
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRelayPropsMixin.RelayAuthenticationProperty"]]:
        '''Authentication for the relay destination server—specify the secretARN where the SMTP credentials are stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerrelay.html#cfn-ses-mailmanagerrelay-authentication
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRelayPropsMixin.RelayAuthenticationProperty"]], result)

    @builtins.property
    def relay_name(self) -> typing.Optional[builtins.str]:
        '''The unique relay name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerrelay.html#cfn-ses-mailmanagerrelay-relayname
        '''
        result = self._values.get("relay_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_name(self) -> typing.Optional[builtins.str]:
        '''The destination relay server address.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerrelay.html#cfn-ses-mailmanagerrelay-servername
        '''
        result = self._values.get("server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_port(self) -> typing.Optional[jsii.Number]:
        '''The destination relay server port.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerrelay.html#cfn-ses-mailmanagerrelay-serverport
        '''
        result = self._values.get("server_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for the resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerrelay.html#cfn-ses-mailmanagerrelay-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMailManagerRelayMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMailManagerRelayPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRelayPropsMixin",
):
    '''Resource to create an SMTP relay, which can be used within a Mail Manager rule set to forward incoming emails to defined relay destinations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerrelay.html
    :cloudformationResource: AWS::SES::MailManagerRelay
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        # no_authentication: Any
        
        cfn_mail_manager_relay_props_mixin = ses_mixins.CfnMailManagerRelayPropsMixin(ses_mixins.CfnMailManagerRelayMixinProps(
            authentication=ses_mixins.CfnMailManagerRelayPropsMixin.RelayAuthenticationProperty(
                no_authentication=no_authentication,
                secret_arn="secretArn"
            ),
            relay_name="relayName",
            server_name="serverName",
            server_port=123,
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
        props: typing.Union[CfnMailManagerRelayMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::MailManagerRelay``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa721654e021d803b6653b3b96ec4dfa39df3f8c0e7ba005b021e31b980c4ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff3aed66003adc78a6b01d59d872135f6ca58b3fbf7fdfaed85a205cbe360099)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd115989e40a18c4cba1d1fc0a7fefc6485a9d3ebb991a4e293c15cedc25f947)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMailManagerRelayMixinProps:
        return typing.cast(CfnMailManagerRelayMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRelayPropsMixin.RelayAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "no_authentication": "noAuthentication",
            "secret_arn": "secretArn",
        },
    )
    class RelayAuthenticationProperty:
        def __init__(
            self,
            *,
            no_authentication: typing.Any = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Authentication for the relay destination server—specify the secretARN where the SMTP credentials are stored, or specify an empty NoAuthentication structure if the relay destination server does not require SMTP credential authentication.

            .. epigraph::

               This data type is a UNION, so only one of the following members can be specified when used or returned.

            :param no_authentication: Keep an empty structure if the relay destination server does not require SMTP credential authentication.
            :param secret_arn: The ARN of the secret created in secrets manager where the relay server's SMTP credentials are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerrelay-relayauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                # no_authentication: Any
                
                relay_authentication_property = ses_mixins.CfnMailManagerRelayPropsMixin.RelayAuthenticationProperty(
                    no_authentication=no_authentication,
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eda8cf6aaa3b149a03f696f1ae6ee59802b573f249005654ad8455ca74799da5)
                check_type(argname="argument no_authentication", value=no_authentication, expected_type=type_hints["no_authentication"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if no_authentication is not None:
                self._values["no_authentication"] = no_authentication
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def no_authentication(self) -> typing.Any:
            '''Keep an empty structure if the relay destination server does not require SMTP credential authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerrelay-relayauthentication.html#cfn-ses-mailmanagerrelay-relayauthentication-noauthentication
            '''
            result = self._values.get("no_authentication")
            return typing.cast(typing.Any, result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret created in secrets manager where the relay server's SMTP credentials are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerrelay-relayauthentication.html#cfn-ses-mailmanagerrelay-relayauthentication-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelayAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnMailManagerRuleSetApplicationLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetApplicationLogs",
):
    '''Builder for CfnMailManagerRuleSetLogsMixin to generate APPLICATION_LOGS for CfnMailManagerRuleSet.

    :cloudformationResource: AWS::SES::MailManagerRuleSet
    :logType: APPLICATION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_mail_manager_rule_set_application_logs = ses_mixins.CfnMailManagerRuleSetApplicationLogs()
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
    ) -> "CfnMailManagerRuleSetLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507ee61d1f659b529ea98b45ec90f54fcb911b533196b77ed51f8b7061dad2ff)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnMailManagerRuleSetLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnMailManagerRuleSetLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af63b89dde5af81422232cbe9a7491b18e2492110916181a86e590eda27a2c8e)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnMailManagerRuleSetLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnMailManagerRuleSetLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba42cd9c38a01c1c2755d72c555181b7f11e0b7e3edaa14e2f279ef694945bcd)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnMailManagerRuleSetLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnMailManagerRuleSetLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetLogsMixin",
):
    '''Resource to create a rule set for a Mail Manager ingress endpoint which contains a list of rules that are evaluated sequentially for each email.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerruleset.html
    :cloudformationResource: AWS::SES::MailManagerRuleSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_mail_manager_rule_set_logs_mixin = ses_mixins.CfnMailManagerRuleSetLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::SES::MailManagerRuleSet``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff89b8f63f89d085b1abcb636f0902e76e4098e335c876b71c0d193438537b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61b38d36ae58c8b66349ef0f4827f7625ee95642391d3bfa544124c373f987ba)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4aa4944bf1b27534b2a4ee50aa909d323569ee2296cdb959148a34f76bfa9c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPLICATION_LOGS")
    def APPLICATION_LOGS(cls) -> CfnMailManagerRuleSetApplicationLogs:
        return typing.cast(CfnMailManagerRuleSetApplicationLogs, jsii.sget(cls, "APPLICATION_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules", "rule_set_name": "ruleSetName", "tags": "tags"},
)
class CfnMailManagerRuleSetMixinProps:
    def __init__(
        self,
        *,
        rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        rule_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMailManagerRuleSetPropsMixin.

        :param rules: Conditional rules that are evaluated for determining actions on email.
        :param rule_set_name: A user-friendly name for the rule set.
        :param tags: The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerruleset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            # drop: Any
            
            cfn_mail_manager_rule_set_mixin_props = ses_mixins.CfnMailManagerRuleSetMixinProps(
                rules=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleProperty(
                    actions=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleActionProperty(
                        add_header=ses_mixins.CfnMailManagerRuleSetPropsMixin.AddHeaderActionProperty(
                            header_name="headerName",
                            header_value="headerValue"
                        ),
                        archive=ses_mixins.CfnMailManagerRuleSetPropsMixin.ArchiveActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            target_archive="targetArchive"
                        ),
                        deliver_to_mailbox=ses_mixins.CfnMailManagerRuleSetPropsMixin.DeliverToMailboxActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            mailbox_arn="mailboxArn",
                            role_arn="roleArn"
                        ),
                        deliver_to_qBusiness=ses_mixins.CfnMailManagerRuleSetPropsMixin.DeliverToQBusinessActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            application_id="applicationId",
                            index_id="indexId",
                            role_arn="roleArn"
                        ),
                        drop=drop,
                        publish_to_sns=ses_mixins.CfnMailManagerRuleSetPropsMixin.SnsActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            encoding="encoding",
                            payload_type="payloadType",
                            role_arn="roleArn",
                            topic_arn="topicArn"
                        ),
                        relay=ses_mixins.CfnMailManagerRuleSetPropsMixin.RelayActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            mail_from="mailFrom",
                            relay="relay"
                        ),
                        replace_recipient=ses_mixins.CfnMailManagerRuleSetPropsMixin.ReplaceRecipientActionProperty(
                            replace_with=["replaceWith"]
                        ),
                        send=ses_mixins.CfnMailManagerRuleSetPropsMixin.SendActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            role_arn="roleArn"
                        ),
                        write_to_s3=ses_mixins.CfnMailManagerRuleSetPropsMixin.S3ActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            role_arn="roleArn",
                            s3_bucket="s3Bucket",
                            s3_prefix="s3Prefix",
                            s3_sse_kms_key_id="s3SseKmsKeyId"
                        )
                    )],
                    conditions=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleConditionProperty(
                        boolean_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute",
                                is_in_address_list=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty(
                                    address_lists=["addressLists"],
                                    attribute="attribute"
                                )
                            ),
                            operator="operator"
                        ),
                        dmarc_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty(
                            operator="operator",
                            values=["values"]
                        ),
                        ip_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        number_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            value=123
                        ),
                        string_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute",
                                mime_header_attribute="mimeHeaderAttribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        verdict_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        )
                    )],
                    name="name",
                    unless=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleConditionProperty(
                        boolean_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute",
                                is_in_address_list=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty(
                                    address_lists=["addressLists"],
                                    attribute="attribute"
                                )
                            ),
                            operator="operator"
                        ),
                        dmarc_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty(
                            operator="operator",
                            values=["values"]
                        ),
                        ip_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        number_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            value=123
                        ),
                        string_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute",
                                mime_header_attribute="mimeHeaderAttribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        verdict_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        )
                    )]
                )],
                rule_set_name="ruleSetName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4d5dff7d48ff49f0f2296fc46693cee1aced720a9d5f0fafa031c8b7dafc20)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument rule_set_name", value=rule_set_name, expected_type=type_hints["rule_set_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rules is not None:
            self._values["rules"] = rules
        if rule_set_name is not None:
            self._values["rule_set_name"] = rule_set_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleProperty"]]]]:
        '''Conditional rules that are evaluated for determining actions on email.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerruleset.html#cfn-ses-mailmanagerruleset-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleProperty"]]]], result)

    @builtins.property
    def rule_set_name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly name for the rule set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerruleset.html#cfn-ses-mailmanagerruleset-rulesetname
        '''
        result = self._values.get("rule_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for the resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerruleset.html#cfn-ses-mailmanagerruleset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMailManagerRuleSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMailManagerRuleSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin",
):
    '''Resource to create a rule set for a Mail Manager ingress endpoint which contains a list of rules that are evaluated sequentially for each email.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagerruleset.html
    :cloudformationResource: AWS::SES::MailManagerRuleSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        # drop: Any
        
        cfn_mail_manager_rule_set_props_mixin = ses_mixins.CfnMailManagerRuleSetPropsMixin(ses_mixins.CfnMailManagerRuleSetMixinProps(
            rules=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleProperty(
                actions=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleActionProperty(
                    add_header=ses_mixins.CfnMailManagerRuleSetPropsMixin.AddHeaderActionProperty(
                        header_name="headerName",
                        header_value="headerValue"
                    ),
                    archive=ses_mixins.CfnMailManagerRuleSetPropsMixin.ArchiveActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        target_archive="targetArchive"
                    ),
                    deliver_to_mailbox=ses_mixins.CfnMailManagerRuleSetPropsMixin.DeliverToMailboxActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        mailbox_arn="mailboxArn",
                        role_arn="roleArn"
                    ),
                    deliver_to_qBusiness=ses_mixins.CfnMailManagerRuleSetPropsMixin.DeliverToQBusinessActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        application_id="applicationId",
                        index_id="indexId",
                        role_arn="roleArn"
                    ),
                    drop=drop,
                    publish_to_sns=ses_mixins.CfnMailManagerRuleSetPropsMixin.SnsActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        encoding="encoding",
                        payload_type="payloadType",
                        role_arn="roleArn",
                        topic_arn="topicArn"
                    ),
                    relay=ses_mixins.CfnMailManagerRuleSetPropsMixin.RelayActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        mail_from="mailFrom",
                        relay="relay"
                    ),
                    replace_recipient=ses_mixins.CfnMailManagerRuleSetPropsMixin.ReplaceRecipientActionProperty(
                        replace_with=["replaceWith"]
                    ),
                    send=ses_mixins.CfnMailManagerRuleSetPropsMixin.SendActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        role_arn="roleArn"
                    ),
                    write_to_s3=ses_mixins.CfnMailManagerRuleSetPropsMixin.S3ActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        role_arn="roleArn",
                        s3_bucket="s3Bucket",
                        s3_prefix="s3Prefix",
                        s3_sse_kms_key_id="s3SseKmsKeyId"
                    )
                )],
                conditions=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleConditionProperty(
                    boolean_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute",
                            is_in_address_list=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty(
                                address_lists=["addressLists"],
                                attribute="attribute"
                            )
                        ),
                        operator="operator"
                    ),
                    dmarc_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty(
                        operator="operator",
                        values=["values"]
                    ),
                    ip_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    number_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        value=123
                    ),
                    string_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute",
                            mime_header_attribute="mimeHeaderAttribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    verdict_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    )
                )],
                name="name",
                unless=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleConditionProperty(
                    boolean_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute",
                            is_in_address_list=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty(
                                address_lists=["addressLists"],
                                attribute="attribute"
                            )
                        ),
                        operator="operator"
                    ),
                    dmarc_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty(
                        operator="operator",
                        values=["values"]
                    ),
                    ip_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    number_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        value=123
                    ),
                    string_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute",
                            mime_header_attribute="mimeHeaderAttribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    verdict_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    )
                )]
            )],
            rule_set_name="ruleSetName",
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
        props: typing.Union[CfnMailManagerRuleSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::MailManagerRuleSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450858f974a3371e31d62a900dadfd4dd2a0194f3bfa41e243fbd655131f00c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c61c9ad02c983f488c6ecdca81a74af3073fe34a2f318a870197aa12b5ddc3d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1753e267f41feb506b2b1f5c86c72e147157c7c47ee006500879875adf751a60)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMailManagerRuleSetMixinProps:
        return typing.cast(CfnMailManagerRuleSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.AddHeaderActionProperty",
        jsii_struct_bases=[],
        name_mapping={"header_name": "headerName", "header_value": "headerValue"},
    )
    class AddHeaderActionProperty:
        def __init__(
            self,
            *,
            header_name: typing.Optional[builtins.str] = None,
            header_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The action to add a header to a message.

            When executed, this action will add the given header to the message.

            :param header_name: The name of the header to add to an email. The header must be prefixed with "X-". Headers are added regardless of whether the header name pre-existed in the email.
            :param header_value: The value of the header to add to the email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-addheaderaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                add_header_action_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.AddHeaderActionProperty(
                    header_name="headerName",
                    header_value="headerValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__862959ab5d09a96a5c91f70589bdbdf72428f667b97ce246c83a45b6cee0ba2a)
                check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
                check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_name is not None:
                self._values["header_name"] = header_name
            if header_value is not None:
                self._values["header_value"] = header_value

        @builtins.property
        def header_name(self) -> typing.Optional[builtins.str]:
            '''The name of the header to add to an email.

            The header must be prefixed with "X-". Headers are added regardless of whether the header name pre-existed in the email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-addheaderaction.html#cfn-ses-mailmanagerruleset-addheaderaction-headername
            '''
            result = self._values.get("header_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header_value(self) -> typing.Optional[builtins.str]:
            '''The value of the header to add to the email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-addheaderaction.html#cfn-ses-mailmanagerruleset-addheaderaction-headervalue
            '''
            result = self._values.get("header_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddHeaderActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty",
        jsii_struct_bases=[],
        name_mapping={"analyzer": "analyzer", "result_field": "resultField"},
    )
    class AnalysisProperty:
        def __init__(
            self,
            *,
            analyzer: typing.Optional[builtins.str] = None,
            result_field: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The result of an analysis can be used in conditions to trigger actions.

            Analyses can inspect the email content and report a certain aspect of the email.

            :param analyzer: The Amazon Resource Name (ARN) of an Add On.
            :param result_field: The returned value from an Add On.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-analysis.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                analysis_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                    analyzer="analyzer",
                    result_field="resultField"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41a1ca7fc3625765cae1781d58b109a6e2c94d4a3d1f44ff22cd015b62f4e3f6)
                check_type(argname="argument analyzer", value=analyzer, expected_type=type_hints["analyzer"])
                check_type(argname="argument result_field", value=result_field, expected_type=type_hints["result_field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if analyzer is not None:
                self._values["analyzer"] = analyzer
            if result_field is not None:
                self._values["result_field"] = result_field

        @builtins.property
        def analyzer(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an Add On.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-analysis.html#cfn-ses-mailmanagerruleset-analysis-analyzer
            '''
            result = self._values.get("analyzer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def result_field(self) -> typing.Optional[builtins.str]:
            '''The returned value from an Add On.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-analysis.html#cfn-ses-mailmanagerruleset-analysis-resultfield
            '''
            result = self._values.get("result_field")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.ArchiveActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_failure_policy": "actionFailurePolicy",
            "target_archive": "targetArchive",
        },
    )
    class ArchiveActionProperty:
        def __init__(
            self,
            *,
            action_failure_policy: typing.Optional[builtins.str] = None,
            target_archive: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The action to archive the email by delivering the email to an Amazon SES archive.

            :param action_failure_policy: A policy that states what to do in the case of failure. The action will fail if there are configuration errors. For example, the specified archive has been deleted.
            :param target_archive: The identifier of the archive to send the email to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-archiveaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                archive_action_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.ArchiveActionProperty(
                    action_failure_policy="actionFailurePolicy",
                    target_archive="targetArchive"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f046815fa0b8cb179e2396dcc8e40f1f6a762cb3e05d916d106bd9e606e92b9)
                check_type(argname="argument action_failure_policy", value=action_failure_policy, expected_type=type_hints["action_failure_policy"])
                check_type(argname="argument target_archive", value=target_archive, expected_type=type_hints["target_archive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_failure_policy is not None:
                self._values["action_failure_policy"] = action_failure_policy
            if target_archive is not None:
                self._values["target_archive"] = target_archive

        @builtins.property
        def action_failure_policy(self) -> typing.Optional[builtins.str]:
            '''A policy that states what to do in the case of failure.

            The action will fail if there are configuration errors. For example, the specified archive has been deleted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-archiveaction.html#cfn-ses-mailmanagerruleset-archiveaction-actionfailurepolicy
            '''
            result = self._values.get("action_failure_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_archive(self) -> typing.Optional[builtins.str]:
            '''The identifier of the archive to send the email to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-archiveaction.html#cfn-ses-mailmanagerruleset-archiveaction-targetarchive
            '''
            result = self._values.get("target_archive")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArchiveActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.DeliverToMailboxActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_failure_policy": "actionFailurePolicy",
            "mailbox_arn": "mailboxArn",
            "role_arn": "roleArn",
        },
    )
    class DeliverToMailboxActionProperty:
        def __init__(
            self,
            *,
            action_failure_policy: typing.Optional[builtins.str] = None,
            mailbox_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This action to delivers an email to a mailbox.

            :param action_failure_policy: A policy that states what to do in the case of failure. The action will fail if there are configuration errors. For example, the mailbox ARN is no longer valid.
            :param mailbox_arn: The Amazon Resource Name (ARN) of a WorkMail organization to deliver the email to.
            :param role_arn: The Amazon Resource Name (ARN) of an IAM role to use to execute this action. The role must have access to the workmail:DeliverToMailbox API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-delivertomailboxaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                deliver_to_mailbox_action_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.DeliverToMailboxActionProperty(
                    action_failure_policy="actionFailurePolicy",
                    mailbox_arn="mailboxArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b8a93be45f61f8dae7d5f41a757ddd855dc80396eff6b7e2ef477a758185a98)
                check_type(argname="argument action_failure_policy", value=action_failure_policy, expected_type=type_hints["action_failure_policy"])
                check_type(argname="argument mailbox_arn", value=mailbox_arn, expected_type=type_hints["mailbox_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_failure_policy is not None:
                self._values["action_failure_policy"] = action_failure_policy
            if mailbox_arn is not None:
                self._values["mailbox_arn"] = mailbox_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def action_failure_policy(self) -> typing.Optional[builtins.str]:
            '''A policy that states what to do in the case of failure.

            The action will fail if there are configuration errors. For example, the mailbox ARN is no longer valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-delivertomailboxaction.html#cfn-ses-mailmanagerruleset-delivertomailboxaction-actionfailurepolicy
            '''
            result = self._values.get("action_failure_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailbox_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of a WorkMail organization to deliver the email to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-delivertomailboxaction.html#cfn-ses-mailmanagerruleset-delivertomailboxaction-mailboxarn
            '''
            result = self._values.get("mailbox_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an IAM role to use to execute this action.

            The role must have access to the workmail:DeliverToMailbox API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-delivertomailboxaction.html#cfn-ses-mailmanagerruleset-delivertomailboxaction-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeliverToMailboxActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.DeliverToQBusinessActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_failure_policy": "actionFailurePolicy",
            "application_id": "applicationId",
            "index_id": "indexId",
            "role_arn": "roleArn",
        },
    )
    class DeliverToQBusinessActionProperty:
        def __init__(
            self,
            *,
            action_failure_policy: typing.Optional[builtins.str] = None,
            application_id: typing.Optional[builtins.str] = None,
            index_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The action to deliver incoming emails to an Amazon Q Business application for indexing.

            :param action_failure_policy: A policy that states what to do in the case of failure. The action will fail if there are configuration errors. For example, the specified application has been deleted or the role lacks necessary permissions to call the ``qbusiness:BatchPutDocument`` API.
            :param application_id: The unique identifier of the Amazon Q Business application instance where the email content will be delivered.
            :param index_id: The identifier of the knowledge base index within the Amazon Q Business application where the email content will be stored and indexed.
            :param role_arn: The Amazon Resource Name (ARN) of the IAM Role to use while delivering to Amazon Q Business. This role must have access to the ``qbusiness:BatchPutDocument`` API for the given application and index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-delivertoqbusinessaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                deliver_to_qBusiness_action_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.DeliverToQBusinessActionProperty(
                    action_failure_policy="actionFailurePolicy",
                    application_id="applicationId",
                    index_id="indexId",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__963e0e8940deb2ada0b1a1bc81c80b21feca95d47873f94710d3871bf285023f)
                check_type(argname="argument action_failure_policy", value=action_failure_policy, expected_type=type_hints["action_failure_policy"])
                check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
                check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_failure_policy is not None:
                self._values["action_failure_policy"] = action_failure_policy
            if application_id is not None:
                self._values["application_id"] = application_id
            if index_id is not None:
                self._values["index_id"] = index_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def action_failure_policy(self) -> typing.Optional[builtins.str]:
            '''A policy that states what to do in the case of failure.

            The action will fail if there are configuration errors. For example, the specified application has been deleted or the role lacks necessary permissions to call the ``qbusiness:BatchPutDocument`` API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-delivertoqbusinessaction.html#cfn-ses-mailmanagerruleset-delivertoqbusinessaction-actionfailurepolicy
            '''
            result = self._values.get("action_failure_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def application_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the Amazon Q Business application instance where the email content will be delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-delivertoqbusinessaction.html#cfn-ses-mailmanagerruleset-delivertoqbusinessaction-applicationid
            '''
            result = self._values.get("application_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the knowledge base index within the Amazon Q Business application where the email content will be stored and indexed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-delivertoqbusinessaction.html#cfn-ses-mailmanagerruleset-delivertoqbusinessaction-indexid
            '''
            result = self._values.get("index_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM Role to use while delivering to Amazon Q Business.

            This role must have access to the ``qbusiness:BatchPutDocument`` API for the given application and index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-delivertoqbusinessaction.html#cfn-ses-mailmanagerruleset-delivertoqbusinessaction-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeliverToQBusinessActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RelayActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_failure_policy": "actionFailurePolicy",
            "mail_from": "mailFrom",
            "relay": "relay",
        },
    )
    class RelayActionProperty:
        def __init__(
            self,
            *,
            action_failure_policy: typing.Optional[builtins.str] = None,
            mail_from: typing.Optional[builtins.str] = None,
            relay: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The action relays the email via SMTP to another specific SMTP server.

            :param action_failure_policy: A policy that states what to do in the case of failure. The action will fail if there are configuration errors. For example, the specified relay has been deleted.
            :param mail_from: This action specifies whether to preserve or replace original mail from address while relaying received emails to a destination server.
            :param relay: The identifier of the relay resource to be used when relaying an email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-relayaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                relay_action_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RelayActionProperty(
                    action_failure_policy="actionFailurePolicy",
                    mail_from="mailFrom",
                    relay="relay"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b83d5c547195eb09e689202535fba0c5635c06f3a18040b884d45b01025caa78)
                check_type(argname="argument action_failure_policy", value=action_failure_policy, expected_type=type_hints["action_failure_policy"])
                check_type(argname="argument mail_from", value=mail_from, expected_type=type_hints["mail_from"])
                check_type(argname="argument relay", value=relay, expected_type=type_hints["relay"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_failure_policy is not None:
                self._values["action_failure_policy"] = action_failure_policy
            if mail_from is not None:
                self._values["mail_from"] = mail_from
            if relay is not None:
                self._values["relay"] = relay

        @builtins.property
        def action_failure_policy(self) -> typing.Optional[builtins.str]:
            '''A policy that states what to do in the case of failure.

            The action will fail if there are configuration errors. For example, the specified relay has been deleted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-relayaction.html#cfn-ses-mailmanagerruleset-relayaction-actionfailurepolicy
            '''
            result = self._values.get("action_failure_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mail_from(self) -> typing.Optional[builtins.str]:
            '''This action specifies whether to preserve or replace original mail from address while relaying received emails to a destination server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-relayaction.html#cfn-ses-mailmanagerruleset-relayaction-mailfrom
            '''
            result = self._values.get("mail_from")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def relay(self) -> typing.Optional[builtins.str]:
            '''The identifier of the relay resource to be used when relaying an email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-relayaction.html#cfn-ses-mailmanagerruleset-relayaction-relay
            '''
            result = self._values.get("relay")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelayActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.ReplaceRecipientActionProperty",
        jsii_struct_bases=[],
        name_mapping={"replace_with": "replaceWith"},
    )
    class ReplaceRecipientActionProperty:
        def __init__(
            self,
            *,
            replace_with: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This action replaces the email envelope recipients with the given list of recipients.

            If the condition of this action applies only to a subset of recipients, only those recipients are replaced with the recipients specified in the action. The message contents and headers are unaffected by this action, only the envelope recipients are updated.

            :param replace_with: This action specifies the replacement recipient email addresses to insert.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-replacerecipientaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                replace_recipient_action_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.ReplaceRecipientActionProperty(
                    replace_with=["replaceWith"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9b0fe452db1acf25aced5d8fdea528b6f137ffee14b0d4e11a0b24262bf531b)
                check_type(argname="argument replace_with", value=replace_with, expected_type=type_hints["replace_with"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if replace_with is not None:
                self._values["replace_with"] = replace_with

        @builtins.property
        def replace_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This action specifies the replacement recipient email addresses to insert.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-replacerecipientaction.html#cfn-ses-mailmanagerruleset-replacerecipientaction-replacewith
            '''
            result = self._values.get("replace_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplaceRecipientActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_header": "addHeader",
            "archive": "archive",
            "deliver_to_mailbox": "deliverToMailbox",
            "deliver_to_q_business": "deliverToQBusiness",
            "drop": "drop",
            "publish_to_sns": "publishToSns",
            "relay": "relay",
            "replace_recipient": "replaceRecipient",
            "send": "send",
            "write_to_s3": "writeToS3",
        },
    )
    class RuleActionProperty:
        def __init__(
            self,
            *,
            add_header: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.AddHeaderActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            archive: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.ArchiveActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            deliver_to_mailbox: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.DeliverToMailboxActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            deliver_to_q_business: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.DeliverToQBusinessActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            drop: typing.Any = None,
            publish_to_sns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.SnsActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            relay: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RelayActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            replace_recipient: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.ReplaceRecipientActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            send: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.SendActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            write_to_s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.S3ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The action for a rule to take. Only one of the contained actions can be set.

            .. epigraph::

               This data type is a UNION, so only one of the following members can be specified when used or returned.

            :param add_header: This action adds a header. This can be used to add arbitrary email headers.
            :param archive: This action archives the email. This can be used to deliver an email to an archive.
            :param deliver_to_mailbox: This action delivers an email to a WorkMail mailbox.
            :param deliver_to_q_business: This action delivers an email to an Amazon Q Business application for ingestion into its knowledge base.
            :param drop: This action terminates the evaluation of rules in the rule set.
            :param publish_to_sns: This action publishes the email content to an Amazon SNS topic.
            :param relay: This action relays the email to another SMTP server.
            :param replace_recipient: The action replaces certain or all recipients with a different set of recipients.
            :param send: This action sends the email to the internet.
            :param write_to_s3: This action writes the MIME content of the email to an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                # drop: Any
                
                rule_action_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleActionProperty(
                    add_header=ses_mixins.CfnMailManagerRuleSetPropsMixin.AddHeaderActionProperty(
                        header_name="headerName",
                        header_value="headerValue"
                    ),
                    archive=ses_mixins.CfnMailManagerRuleSetPropsMixin.ArchiveActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        target_archive="targetArchive"
                    ),
                    deliver_to_mailbox=ses_mixins.CfnMailManagerRuleSetPropsMixin.DeliverToMailboxActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        mailbox_arn="mailboxArn",
                        role_arn="roleArn"
                    ),
                    deliver_to_qBusiness=ses_mixins.CfnMailManagerRuleSetPropsMixin.DeliverToQBusinessActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        application_id="applicationId",
                        index_id="indexId",
                        role_arn="roleArn"
                    ),
                    drop=drop,
                    publish_to_sns=ses_mixins.CfnMailManagerRuleSetPropsMixin.SnsActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        encoding="encoding",
                        payload_type="payloadType",
                        role_arn="roleArn",
                        topic_arn="topicArn"
                    ),
                    relay=ses_mixins.CfnMailManagerRuleSetPropsMixin.RelayActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        mail_from="mailFrom",
                        relay="relay"
                    ),
                    replace_recipient=ses_mixins.CfnMailManagerRuleSetPropsMixin.ReplaceRecipientActionProperty(
                        replace_with=["replaceWith"]
                    ),
                    send=ses_mixins.CfnMailManagerRuleSetPropsMixin.SendActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        role_arn="roleArn"
                    ),
                    write_to_s3=ses_mixins.CfnMailManagerRuleSetPropsMixin.S3ActionProperty(
                        action_failure_policy="actionFailurePolicy",
                        role_arn="roleArn",
                        s3_bucket="s3Bucket",
                        s3_prefix="s3Prefix",
                        s3_sse_kms_key_id="s3SseKmsKeyId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e9b570285bb8d7f4f8d34e5b6de8cc486cb8d5bd5bce047e716877adcc9f468)
                check_type(argname="argument add_header", value=add_header, expected_type=type_hints["add_header"])
                check_type(argname="argument archive", value=archive, expected_type=type_hints["archive"])
                check_type(argname="argument deliver_to_mailbox", value=deliver_to_mailbox, expected_type=type_hints["deliver_to_mailbox"])
                check_type(argname="argument deliver_to_q_business", value=deliver_to_q_business, expected_type=type_hints["deliver_to_q_business"])
                check_type(argname="argument drop", value=drop, expected_type=type_hints["drop"])
                check_type(argname="argument publish_to_sns", value=publish_to_sns, expected_type=type_hints["publish_to_sns"])
                check_type(argname="argument relay", value=relay, expected_type=type_hints["relay"])
                check_type(argname="argument replace_recipient", value=replace_recipient, expected_type=type_hints["replace_recipient"])
                check_type(argname="argument send", value=send, expected_type=type_hints["send"])
                check_type(argname="argument write_to_s3", value=write_to_s3, expected_type=type_hints["write_to_s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_header is not None:
                self._values["add_header"] = add_header
            if archive is not None:
                self._values["archive"] = archive
            if deliver_to_mailbox is not None:
                self._values["deliver_to_mailbox"] = deliver_to_mailbox
            if deliver_to_q_business is not None:
                self._values["deliver_to_q_business"] = deliver_to_q_business
            if drop is not None:
                self._values["drop"] = drop
            if publish_to_sns is not None:
                self._values["publish_to_sns"] = publish_to_sns
            if relay is not None:
                self._values["relay"] = relay
            if replace_recipient is not None:
                self._values["replace_recipient"] = replace_recipient
            if send is not None:
                self._values["send"] = send
            if write_to_s3 is not None:
                self._values["write_to_s3"] = write_to_s3

        @builtins.property
        def add_header(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.AddHeaderActionProperty"]]:
            '''This action adds a header.

            This can be used to add arbitrary email headers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html#cfn-ses-mailmanagerruleset-ruleaction-addheader
            '''
            result = self._values.get("add_header")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.AddHeaderActionProperty"]], result)

        @builtins.property
        def archive(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.ArchiveActionProperty"]]:
            '''This action archives the email.

            This can be used to deliver an email to an archive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html#cfn-ses-mailmanagerruleset-ruleaction-archive
            '''
            result = self._values.get("archive")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.ArchiveActionProperty"]], result)

        @builtins.property
        def deliver_to_mailbox(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.DeliverToMailboxActionProperty"]]:
            '''This action delivers an email to a WorkMail mailbox.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html#cfn-ses-mailmanagerruleset-ruleaction-delivertomailbox
            '''
            result = self._values.get("deliver_to_mailbox")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.DeliverToMailboxActionProperty"]], result)

        @builtins.property
        def deliver_to_q_business(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.DeliverToQBusinessActionProperty"]]:
            '''This action delivers an email to an Amazon Q Business application for ingestion into its knowledge base.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html#cfn-ses-mailmanagerruleset-ruleaction-delivertoqbusiness
            '''
            result = self._values.get("deliver_to_q_business")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.DeliverToQBusinessActionProperty"]], result)

        @builtins.property
        def drop(self) -> typing.Any:
            '''This action terminates the evaluation of rules in the rule set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html#cfn-ses-mailmanagerruleset-ruleaction-drop
            '''
            result = self._values.get("drop")
            return typing.cast(typing.Any, result)

        @builtins.property
        def publish_to_sns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.SnsActionProperty"]]:
            '''This action publishes the email content to an Amazon SNS topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html#cfn-ses-mailmanagerruleset-ruleaction-publishtosns
            '''
            result = self._values.get("publish_to_sns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.SnsActionProperty"]], result)

        @builtins.property
        def relay(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RelayActionProperty"]]:
            '''This action relays the email to another SMTP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html#cfn-ses-mailmanagerruleset-ruleaction-relay
            '''
            result = self._values.get("relay")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RelayActionProperty"]], result)

        @builtins.property
        def replace_recipient(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.ReplaceRecipientActionProperty"]]:
            '''The action replaces certain or all recipients with a different set of recipients.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html#cfn-ses-mailmanagerruleset-ruleaction-replacerecipient
            '''
            result = self._values.get("replace_recipient")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.ReplaceRecipientActionProperty"]], result)

        @builtins.property
        def send(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.SendActionProperty"]]:
            '''This action sends the email to the internet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html#cfn-ses-mailmanagerruleset-ruleaction-send
            '''
            result = self._values.get("send")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.SendActionProperty"]], result)

        @builtins.property
        def write_to_s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.S3ActionProperty"]]:
            '''This action writes the MIME content of the email to an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleaction.html#cfn-ses-mailmanagerruleset-ruleaction-writetos3
            '''
            result = self._values.get("write_to_s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.S3ActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={"evaluate": "evaluate", "operator": "operator"},
    )
    class RuleBooleanExpressionProperty:
        def __init__(
            self,
            *,
            evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A boolean expression to be used in a rule condition.

            :param evaluate: The operand on which to perform a boolean condition operation.
            :param operator: The matching operator for a boolean condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulebooleanexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_boolean_expression_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty(
                    evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty(
                        analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                            analyzer="analyzer",
                            result_field="resultField"
                        ),
                        attribute="attribute",
                        is_in_address_list=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty(
                            address_lists=["addressLists"],
                            attribute="attribute"
                        )
                    ),
                    operator="operator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1d83a5201ffedb02f734622b40303dcb2ef162e224de56e7a9d07a9c97171eb)
                check_type(argname="argument evaluate", value=evaluate, expected_type=type_hints["evaluate"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluate is not None:
                self._values["evaluate"] = evaluate
            if operator is not None:
                self._values["operator"] = operator

        @builtins.property
        def evaluate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty"]]:
            '''The operand on which to perform a boolean condition operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulebooleanexpression.html#cfn-ses-mailmanagerruleset-rulebooleanexpression-evaluate
            '''
            result = self._values.get("evaluate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The matching operator for a boolean condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulebooleanexpression.html#cfn-ses-mailmanagerruleset-rulebooleanexpression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleBooleanExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "analysis": "analysis",
            "attribute": "attribute",
            "is_in_address_list": "isInAddressList",
        },
    )
    class RuleBooleanToEvaluateProperty:
        def __init__(
            self,
            *,
            analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.AnalysisProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            attribute: typing.Optional[builtins.str] = None,
            is_in_address_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The union type representing the allowed types of operands for a boolean condition.

            :param analysis: The Add On ARN and its returned value to evaluate in a boolean condition expression.
            :param attribute: The boolean type representing the allowed attribute types for an email.
            :param is_in_address_list: The structure representing the address lists and address list attribute that will be used in evaluation of boolean expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulebooleantoevaluate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_boolean_to_evaluate_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty(
                    analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                        analyzer="analyzer",
                        result_field="resultField"
                    ),
                    attribute="attribute",
                    is_in_address_list=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty(
                        address_lists=["addressLists"],
                        attribute="attribute"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3fc31108e22582a8ea4be55f27f901d5c01f586e57cc4d34cb546941508d9e3)
                check_type(argname="argument analysis", value=analysis, expected_type=type_hints["analysis"])
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument is_in_address_list", value=is_in_address_list, expected_type=type_hints["is_in_address_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if analysis is not None:
                self._values["analysis"] = analysis
            if attribute is not None:
                self._values["attribute"] = attribute
            if is_in_address_list is not None:
                self._values["is_in_address_list"] = is_in_address_list

        @builtins.property
        def analysis(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.AnalysisProperty"]]:
            '''The Add On ARN and its returned value to evaluate in a boolean condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulebooleantoevaluate.html#cfn-ses-mailmanagerruleset-rulebooleantoevaluate-analysis
            '''
            result = self._values.get("analysis")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.AnalysisProperty"]], result)

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The boolean type representing the allowed attribute types for an email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulebooleantoevaluate.html#cfn-ses-mailmanagerruleset-rulebooleantoevaluate-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_in_address_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty"]]:
            '''The structure representing the address lists and address list attribute that will be used in evaluation of boolean expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulebooleantoevaluate.html#cfn-ses-mailmanagerruleset-rulebooleantoevaluate-isinaddresslist
            '''
            result = self._values.get("is_in_address_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleBooleanToEvaluateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_expression": "booleanExpression",
            "dmarc_expression": "dmarcExpression",
            "ip_expression": "ipExpression",
            "number_expression": "numberExpression",
            "string_expression": "stringExpression",
            "verdict_expression": "verdictExpression",
        },
    )
    class RuleConditionProperty:
        def __init__(
            self,
            *,
            boolean_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dmarc_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            number_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            string_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            verdict_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The conditional expression used to evaluate an email for determining if a rule action should be taken.

            .. epigraph::

               This data type is a UNION, so only one of the following members can be specified when used or returned.

            :param boolean_expression: The condition applies to a boolean expression passed in this field.
            :param dmarc_expression: The condition applies to a DMARC policy expression passed in this field.
            :param ip_expression: The condition applies to an IP address expression passed in this field.
            :param number_expression: The condition applies to a number expression passed in this field.
            :param string_expression: The condition applies to a string expression passed in this field.
            :param verdict_expression: The condition applies to a verdict expression passed in this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulecondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_condition_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleConditionProperty(
                    boolean_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute",
                            is_in_address_list=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty(
                                address_lists=["addressLists"],
                                attribute="attribute"
                            )
                        ),
                        operator="operator"
                    ),
                    dmarc_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty(
                        operator="operator",
                        values=["values"]
                    ),
                    ip_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    number_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        value=123
                    ),
                    string_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute",
                            mime_header_attribute="mimeHeaderAttribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    verdict_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6196b22c832d4b0e6d02afb6c57386231a9d82e7cdbedd1ac5032d7ea80ee3ed)
                check_type(argname="argument boolean_expression", value=boolean_expression, expected_type=type_hints["boolean_expression"])
                check_type(argname="argument dmarc_expression", value=dmarc_expression, expected_type=type_hints["dmarc_expression"])
                check_type(argname="argument ip_expression", value=ip_expression, expected_type=type_hints["ip_expression"])
                check_type(argname="argument number_expression", value=number_expression, expected_type=type_hints["number_expression"])
                check_type(argname="argument string_expression", value=string_expression, expected_type=type_hints["string_expression"])
                check_type(argname="argument verdict_expression", value=verdict_expression, expected_type=type_hints["verdict_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_expression is not None:
                self._values["boolean_expression"] = boolean_expression
            if dmarc_expression is not None:
                self._values["dmarc_expression"] = dmarc_expression
            if ip_expression is not None:
                self._values["ip_expression"] = ip_expression
            if number_expression is not None:
                self._values["number_expression"] = number_expression
            if string_expression is not None:
                self._values["string_expression"] = string_expression
            if verdict_expression is not None:
                self._values["verdict_expression"] = verdict_expression

        @builtins.property
        def boolean_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty"]]:
            '''The condition applies to a boolean expression passed in this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulecondition.html#cfn-ses-mailmanagerruleset-rulecondition-booleanexpression
            '''
            result = self._values.get("boolean_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty"]], result)

        @builtins.property
        def dmarc_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty"]]:
            '''The condition applies to a DMARC policy expression passed in this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulecondition.html#cfn-ses-mailmanagerruleset-rulecondition-dmarcexpression
            '''
            result = self._values.get("dmarc_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty"]], result)

        @builtins.property
        def ip_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty"]]:
            '''The condition applies to an IP address expression passed in this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulecondition.html#cfn-ses-mailmanagerruleset-rulecondition-ipexpression
            '''
            result = self._values.get("ip_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty"]], result)

        @builtins.property
        def number_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty"]]:
            '''The condition applies to a number expression passed in this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulecondition.html#cfn-ses-mailmanagerruleset-rulecondition-numberexpression
            '''
            result = self._values.get("number_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty"]], result)

        @builtins.property
        def string_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty"]]:
            '''The condition applies to a string expression passed in this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulecondition.html#cfn-ses-mailmanagerruleset-rulecondition-stringexpression
            '''
            result = self._values.get("string_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty"]], result)

        @builtins.property
        def verdict_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty"]]:
            '''The condition applies to a verdict expression passed in this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulecondition.html#cfn-ses-mailmanagerruleset-rulecondition-verdictexpression
            '''
            result = self._values.get("verdict_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={"operator": "operator", "values": "values"},
    )
    class RuleDmarcExpressionProperty:
        def __init__(
            self,
            *,
            operator: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A DMARC policy expression.

            The condition matches if the given DMARC policy matches that of the incoming email.

            :param operator: The operator to apply to the DMARC policy of the incoming email.
            :param values: The values to use for the given DMARC policy operator. For the operator EQUALS, if multiple values are given, they are evaluated as an OR. That is, if any of the given values match, the condition is deemed to match. For the operator NOT_EQUALS, if multiple values are given, they are evaluated as an AND. That is, only if the email's DMARC policy is not equal to any of the given values, then the condition is deemed to match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruledmarcexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_dmarc_expression_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty(
                    operator="operator",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a89f78f3397616c90b21b1c5fb29d1790b71f1b95ad843a7d2f9c8ee751cfeb9)
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if operator is not None:
                self._values["operator"] = operator
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The operator to apply to the DMARC policy of the incoming email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruledmarcexpression.html#cfn-ses-mailmanagerruleset-ruledmarcexpression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values to use for the given DMARC policy operator.

            For the operator EQUALS, if multiple values are given, they are evaluated as an OR. That is, if any of the given values match, the condition is deemed to match. For the operator NOT_EQUALS, if multiple values are given, they are evaluated as an AND. That is, only if the email's DMARC policy is not equal to any of the given values, then the condition is deemed to match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruledmarcexpression.html#cfn-ses-mailmanagerruleset-ruledmarcexpression-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleDmarcExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "evaluate": "evaluate",
            "operator": "operator",
            "values": "values",
        },
    )
    class RuleIpExpressionProperty:
        def __init__(
            self,
            *,
            evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An IP address expression matching certain IP addresses within a given range of IP addresses.

            :param evaluate: The IP address to evaluate in this condition.
            :param operator: The operator to evaluate the IP address.
            :param values: The IP CIDR blocks in format "x.y.z.w/n" (eg 10.0.0.0/8) to match with the email's IP address. For the operator CIDR_MATCHES, if multiple values are given, they are evaluated as an OR. That is, if the IP address is contained within any of the given CIDR ranges, the condition is deemed to match. For NOT_CIDR_MATCHES, if multiple CIDR ranges are given, the condition is deemed to match if the IP address is not contained in any of the given CIDR ranges.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleipexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_ip_expression_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty(
                    evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty(
                        attribute="attribute"
                    ),
                    operator="operator",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__872076428b139116c030050c49831f6feed29663b923e88213e51114d2965a99)
                check_type(argname="argument evaluate", value=evaluate, expected_type=type_hints["evaluate"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluate is not None:
                self._values["evaluate"] = evaluate
            if operator is not None:
                self._values["operator"] = operator
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def evaluate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty"]]:
            '''The IP address to evaluate in this condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleipexpression.html#cfn-ses-mailmanagerruleset-ruleipexpression-evaluate
            '''
            result = self._values.get("evaluate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The operator to evaluate the IP address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleipexpression.html#cfn-ses-mailmanagerruleset-ruleipexpression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IP CIDR blocks in format "x.y.z.w/n" (eg 10.0.0.0/8) to match with the email's IP address. For the operator CIDR_MATCHES, if multiple values are given, they are evaluated as an OR. That is, if the IP address is contained within any of the given CIDR ranges, the condition is deemed to match. For NOT_CIDR_MATCHES, if multiple CIDR ranges are given, the condition is deemed to match if the IP address is not contained in any of the given CIDR ranges.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleipexpression.html#cfn-ses-mailmanagerruleset-ruleipexpression-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleIpExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute": "attribute"},
    )
    class RuleIpToEvaluateProperty:
        def __init__(self, *, attribute: typing.Optional[builtins.str] = None) -> None:
            '''The IP address to evaluate for this condition.

            :param attribute: The attribute of the email to evaluate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleiptoevaluate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_ip_to_evaluate_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty(
                    attribute="attribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa6f81bcaa74bebfd4b7441514d71014b15f308eaf5116b906af8811a446dcb1)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The attribute of the email to evaluate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleiptoevaluate.html#cfn-ses-mailmanagerruleset-ruleiptoevaluate-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleIpToEvaluateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty",
        jsii_struct_bases=[],
        name_mapping={"address_lists": "addressLists", "attribute": "attribute"},
    )
    class RuleIsInAddressListProperty:
        def __init__(
            self,
            *,
            address_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
            attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The structure type for a boolean condition that provides the address lists and address list attribute to evaluate.

            :param address_lists: The address lists that will be used for evaluation.
            :param attribute: The email attribute that needs to be evaluated against the address list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleisinaddresslist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_is_in_address_list_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty(
                    address_lists=["addressLists"],
                    attribute="attribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__545d98a332fa5b8a7fb9621df9dd39fdef72d0fb7c72c9bdbba6398537bb2a33)
                check_type(argname="argument address_lists", value=address_lists, expected_type=type_hints["address_lists"])
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address_lists is not None:
                self._values["address_lists"] = address_lists
            if attribute is not None:
                self._values["attribute"] = attribute

        @builtins.property
        def address_lists(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The address lists that will be used for evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleisinaddresslist.html#cfn-ses-mailmanagerruleset-ruleisinaddresslist-addresslists
            '''
            result = self._values.get("address_lists")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The email attribute that needs to be evaluated against the address list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleisinaddresslist.html#cfn-ses-mailmanagerruleset-ruleisinaddresslist-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleIsInAddressListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "evaluate": "evaluate",
            "operator": "operator",
            "value": "value",
        },
    )
    class RuleNumberExpressionProperty:
        def __init__(
            self,
            *,
            evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A number expression to match numeric conditions with integers from the incoming email.

            :param evaluate: The number to evaluate in a numeric condition expression.
            :param operator: The operator for a numeric condition expression.
            :param value: The value to evaluate in a numeric condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulenumberexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_number_expression_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty(
                    evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty(
                        attribute="attribute"
                    ),
                    operator="operator",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63263a9c28c9cdee511c3fbb1b9d64ca53c15a4676db6fa721ae7beb328b0943)
                check_type(argname="argument evaluate", value=evaluate, expected_type=type_hints["evaluate"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluate is not None:
                self._values["evaluate"] = evaluate
            if operator is not None:
                self._values["operator"] = operator
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def evaluate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty"]]:
            '''The number to evaluate in a numeric condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulenumberexpression.html#cfn-ses-mailmanagerruleset-rulenumberexpression-evaluate
            '''
            result = self._values.get("evaluate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The operator for a numeric condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulenumberexpression.html#cfn-ses-mailmanagerruleset-rulenumberexpression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value to evaluate in a numeric condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulenumberexpression.html#cfn-ses-mailmanagerruleset-rulenumberexpression-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleNumberExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute": "attribute"},
    )
    class RuleNumberToEvaluateProperty:
        def __init__(self, *, attribute: typing.Optional[builtins.str] = None) -> None:
            '''The number to evaluate in a numeric condition expression.

            :param attribute: An email attribute that is used as the number to evaluate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulenumbertoevaluate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_number_to_evaluate_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty(
                    attribute="attribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4963e97053c5d6958992092714899b87cb3642cfdec56f02cdc7ae6f8c6697e)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''An email attribute that is used as the number to evaluate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulenumbertoevaluate.html#cfn-ses-mailmanagerruleset-rulenumbertoevaluate-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleNumberToEvaluateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "conditions": "conditions",
            "name": "name",
            "unless": "unless",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
            unless: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A rule contains conditions, "unless conditions" and actions.

            For each envelope recipient of an email, if all conditions match and none of the "unless conditions" match, then all of the actions are executed sequentially. If no conditions are provided, the rule always applies and the actions are implicitly executed. If only "unless conditions" are provided, the rule applies if the email does not match the evaluation of the "unless conditions".

            :param actions: The list of actions to execute when the conditions match the incoming email, and none of the "unless conditions" match.
            :param conditions: The conditions of this rule. All conditions must match the email for the actions to be executed. An empty list of conditions means that all emails match, but are still subject to any "unless conditions"
            :param name: The user-friendly name of the rule.
            :param unless: The "unless conditions" of this rule. None of the conditions can match the email for the actions to be executed. If any of these conditions do match the email, then the actions are not executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                # drop: Any
                
                rule_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleProperty(
                    actions=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleActionProperty(
                        add_header=ses_mixins.CfnMailManagerRuleSetPropsMixin.AddHeaderActionProperty(
                            header_name="headerName",
                            header_value="headerValue"
                        ),
                        archive=ses_mixins.CfnMailManagerRuleSetPropsMixin.ArchiveActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            target_archive="targetArchive"
                        ),
                        deliver_to_mailbox=ses_mixins.CfnMailManagerRuleSetPropsMixin.DeliverToMailboxActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            mailbox_arn="mailboxArn",
                            role_arn="roleArn"
                        ),
                        deliver_to_qBusiness=ses_mixins.CfnMailManagerRuleSetPropsMixin.DeliverToQBusinessActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            application_id="applicationId",
                            index_id="indexId",
                            role_arn="roleArn"
                        ),
                        drop=drop,
                        publish_to_sns=ses_mixins.CfnMailManagerRuleSetPropsMixin.SnsActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            encoding="encoding",
                            payload_type="payloadType",
                            role_arn="roleArn",
                            topic_arn="topicArn"
                        ),
                        relay=ses_mixins.CfnMailManagerRuleSetPropsMixin.RelayActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            mail_from="mailFrom",
                            relay="relay"
                        ),
                        replace_recipient=ses_mixins.CfnMailManagerRuleSetPropsMixin.ReplaceRecipientActionProperty(
                            replace_with=["replaceWith"]
                        ),
                        send=ses_mixins.CfnMailManagerRuleSetPropsMixin.SendActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            role_arn="roleArn"
                        ),
                        write_to_s3=ses_mixins.CfnMailManagerRuleSetPropsMixin.S3ActionProperty(
                            action_failure_policy="actionFailurePolicy",
                            role_arn="roleArn",
                            s3_bucket="s3Bucket",
                            s3_prefix="s3Prefix",
                            s3_sse_kms_key_id="s3SseKmsKeyId"
                        )
                    )],
                    conditions=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleConditionProperty(
                        boolean_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute",
                                is_in_address_list=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty(
                                    address_lists=["addressLists"],
                                    attribute="attribute"
                                )
                            ),
                            operator="operator"
                        ),
                        dmarc_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty(
                            operator="operator",
                            values=["values"]
                        ),
                        ip_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        number_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            value=123
                        ),
                        string_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute",
                                mime_header_attribute="mimeHeaderAttribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        verdict_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        )
                    )],
                    name="name",
                    unless=[ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleConditionProperty(
                        boolean_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute",
                                is_in_address_list=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty(
                                    address_lists=["addressLists"],
                                    attribute="attribute"
                                )
                            ),
                            operator="operator"
                        ),
                        dmarc_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty(
                            operator="operator",
                            values=["values"]
                        ),
                        ip_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        number_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            value=123
                        ),
                        string_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute",
                                mime_header_attribute="mimeHeaderAttribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        verdict_expression=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f16092d1166c386a42ccd75df5e672a486ab88f7f8dfaa924d7a28335f5c9db)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument unless", value=unless, expected_type=type_hints["unless"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if conditions is not None:
                self._values["conditions"] = conditions
            if name is not None:
                self._values["name"] = name
            if unless is not None:
                self._values["unless"] = unless

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleActionProperty"]]]]:
            '''The list of actions to execute when the conditions match the incoming email, and none of the "unless conditions" match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rule.html#cfn-ses-mailmanagerruleset-rule-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleActionProperty"]]]], result)

        @builtins.property
        def conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleConditionProperty"]]]]:
            '''The conditions of this rule.

            All conditions must match the email for the actions to be executed. An empty list of conditions means that all emails match, but are still subject to any "unless conditions"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rule.html#cfn-ses-mailmanagerruleset-rule-conditions
            '''
            result = self._values.get("conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleConditionProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The user-friendly name of the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rule.html#cfn-ses-mailmanagerruleset-rule-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unless(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleConditionProperty"]]]]:
            '''The "unless conditions" of this rule.

            None of the conditions can match the email for the actions to be executed. If any of these conditions do match the email, then the actions are not executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rule.html#cfn-ses-mailmanagerruleset-rule-unless
            '''
            result = self._values.get("unless")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleConditionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "evaluate": "evaluate",
            "operator": "operator",
            "values": "values",
        },
    )
    class RuleStringExpressionProperty:
        def __init__(
            self,
            *,
            evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A string expression is evaluated against strings or substrings of the email.

            :param evaluate: The string to evaluate in a string condition expression.
            :param operator: The matching operator for a string condition expression.
            :param values: The string(s) to be evaluated in a string condition expression. For all operators, except for NOT_EQUALS, if multiple values are given, the values are processed as an OR. That is, if any of the values match the email's string using the given operator, the condition is deemed to match. However, for NOT_EQUALS, the condition is only deemed to match if none of the given strings match the email's string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulestringexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_string_expression_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty(
                    evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty(
                        analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                            analyzer="analyzer",
                            result_field="resultField"
                        ),
                        attribute="attribute",
                        mime_header_attribute="mimeHeaderAttribute"
                    ),
                    operator="operator",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3648af57425d2a875f88cd89fcd68b9476fc25cf70e99df55c9e37ba81e7891a)
                check_type(argname="argument evaluate", value=evaluate, expected_type=type_hints["evaluate"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluate is not None:
                self._values["evaluate"] = evaluate
            if operator is not None:
                self._values["operator"] = operator
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def evaluate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty"]]:
            '''The string to evaluate in a string condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulestringexpression.html#cfn-ses-mailmanagerruleset-rulestringexpression-evaluate
            '''
            result = self._values.get("evaluate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The matching operator for a string condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulestringexpression.html#cfn-ses-mailmanagerruleset-rulestringexpression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The string(s) to be evaluated in a string condition expression.

            For all operators, except for NOT_EQUALS, if multiple values are given, the values are processed as an OR. That is, if any of the values match the email's string using the given operator, the condition is deemed to match. However, for NOT_EQUALS, the condition is only deemed to match if none of the given strings match the email's string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulestringexpression.html#cfn-ses-mailmanagerruleset-rulestringexpression-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleStringExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "analysis": "analysis",
            "attribute": "attribute",
            "mime_header_attribute": "mimeHeaderAttribute",
        },
    )
    class RuleStringToEvaluateProperty:
        def __init__(
            self,
            *,
            analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.AnalysisProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            attribute: typing.Optional[builtins.str] = None,
            mime_header_attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The string to evaluate in a string condition expression.

            .. epigraph::

               This data type is a UNION, so only one of the following members can be specified when used or returned.

            :param analysis: The Add On ARN and its returned value to evaluate in a string condition expression.
            :param attribute: The email attribute to evaluate in a string condition expression.
            :param mime_header_attribute: The email MIME X-Header attribute to evaluate in a string condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulestringtoevaluate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_string_to_evaluate_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty(
                    analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                        analyzer="analyzer",
                        result_field="resultField"
                    ),
                    attribute="attribute",
                    mime_header_attribute="mimeHeaderAttribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b2ef0323caed6ea0980d16efb19813ced51d4829bd99cd462bc496c98e5456f)
                check_type(argname="argument analysis", value=analysis, expected_type=type_hints["analysis"])
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument mime_header_attribute", value=mime_header_attribute, expected_type=type_hints["mime_header_attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if analysis is not None:
                self._values["analysis"] = analysis
            if attribute is not None:
                self._values["attribute"] = attribute
            if mime_header_attribute is not None:
                self._values["mime_header_attribute"] = mime_header_attribute

        @builtins.property
        def analysis(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.AnalysisProperty"]]:
            '''The Add On ARN and its returned value to evaluate in a string condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulestringtoevaluate.html#cfn-ses-mailmanagerruleset-rulestringtoevaluate-analysis
            '''
            result = self._values.get("analysis")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.AnalysisProperty"]], result)

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The email attribute to evaluate in a string condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulestringtoevaluate.html#cfn-ses-mailmanagerruleset-rulestringtoevaluate-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mime_header_attribute(self) -> typing.Optional[builtins.str]:
            '''The email MIME X-Header attribute to evaluate in a string condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-rulestringtoevaluate.html#cfn-ses-mailmanagerruleset-rulestringtoevaluate-mimeheaderattribute
            '''
            result = self._values.get("mime_header_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleStringToEvaluateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "evaluate": "evaluate",
            "operator": "operator",
            "values": "values",
        },
    )
    class RuleVerdictExpressionProperty:
        def __init__(
            self,
            *,
            evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A verdict expression is evaluated against verdicts of the email.

            :param evaluate: The verdict to evaluate in a verdict condition expression.
            :param operator: The matching operator for a verdict condition expression.
            :param values: The values to match with the email's verdict using the given operator. For the EQUALS operator, if multiple values are given, the condition is deemed to match if any of the given verdicts match that of the email. For the NOT_EQUALS operator, if multiple values are given, the condition is deemed to match of none of the given verdicts match the verdict of the email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleverdictexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_verdict_expression_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty(
                    evaluate=ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty(
                        analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                            analyzer="analyzer",
                            result_field="resultField"
                        ),
                        attribute="attribute"
                    ),
                    operator="operator",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a7150924ac60453219f032d26681626a948cc5127327961637188659b0a7ee7)
                check_type(argname="argument evaluate", value=evaluate, expected_type=type_hints["evaluate"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluate is not None:
                self._values["evaluate"] = evaluate
            if operator is not None:
                self._values["operator"] = operator
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def evaluate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty"]]:
            '''The verdict to evaluate in a verdict condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleverdictexpression.html#cfn-ses-mailmanagerruleset-ruleverdictexpression-evaluate
            '''
            result = self._values.get("evaluate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The matching operator for a verdict condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleverdictexpression.html#cfn-ses-mailmanagerruleset-ruleverdictexpression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values to match with the email's verdict using the given operator.

            For the EQUALS operator, if multiple values are given, the condition is deemed to match if any of the given verdicts match that of the email. For the NOT_EQUALS operator, if multiple values are given, the condition is deemed to match of none of the given verdicts match the verdict of the email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleverdictexpression.html#cfn-ses-mailmanagerruleset-ruleverdictexpression-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleVerdictExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty",
        jsii_struct_bases=[],
        name_mapping={"analysis": "analysis", "attribute": "attribute"},
    )
    class RuleVerdictToEvaluateProperty:
        def __init__(
            self,
            *,
            analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerRuleSetPropsMixin.AnalysisProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The verdict to evaluate in a verdict condition expression.

            .. epigraph::

               This data type is a UNION, so only one of the following members can be specified when used or returned.

            :param analysis: The Add On ARN and its returned value to evaluate in a verdict condition expression.
            :param attribute: The email verdict attribute to evaluate in a string verdict expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleverdicttoevaluate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_verdict_to_evaluate_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty(
                    analysis=ses_mixins.CfnMailManagerRuleSetPropsMixin.AnalysisProperty(
                        analyzer="analyzer",
                        result_field="resultField"
                    ),
                    attribute="attribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1fee130870cc83564b2db3d84012be4e685c71f7aa7db1249d091c36cb5deb7c)
                check_type(argname="argument analysis", value=analysis, expected_type=type_hints["analysis"])
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if analysis is not None:
                self._values["analysis"] = analysis
            if attribute is not None:
                self._values["attribute"] = attribute

        @builtins.property
        def analysis(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.AnalysisProperty"]]:
            '''The Add On ARN and its returned value to evaluate in a verdict condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleverdicttoevaluate.html#cfn-ses-mailmanagerruleset-ruleverdicttoevaluate-analysis
            '''
            result = self._values.get("analysis")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerRuleSetPropsMixin.AnalysisProperty"]], result)

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The email verdict attribute to evaluate in a string verdict expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-ruleverdicttoevaluate.html#cfn-ses-mailmanagerruleset-ruleverdicttoevaluate-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleVerdictToEvaluateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.S3ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_failure_policy": "actionFailurePolicy",
            "role_arn": "roleArn",
            "s3_bucket": "s3Bucket",
            "s3_prefix": "s3Prefix",
            "s3_sse_kms_key_id": "s3SseKmsKeyId",
        },
    )
    class S3ActionProperty:
        def __init__(
            self,
            *,
            action_failure_policy: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_prefix: typing.Optional[builtins.str] = None,
            s3_sse_kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Writes the MIME content of the email to an S3 bucket.

            :param action_failure_policy: A policy that states what to do in the case of failure. The action will fail if there are configuration errors. For example, the specified the bucket has been deleted.
            :param role_arn: The Amazon Resource Name (ARN) of the IAM Role to use while writing to S3. This role must have access to the s3:PutObject, kms:Encrypt, and kms:GenerateDataKey APIs for the given bucket.
            :param s3_bucket: The bucket name of the S3 bucket to write to.
            :param s3_prefix: The S3 prefix to use for the write to the s3 bucket.
            :param s3_sse_kms_key_id: The KMS Key ID to use to encrypt the message in S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-s3action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                s3_action_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.S3ActionProperty(
                    action_failure_policy="actionFailurePolicy",
                    role_arn="roleArn",
                    s3_bucket="s3Bucket",
                    s3_prefix="s3Prefix",
                    s3_sse_kms_key_id="s3SseKmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__566ed051d8c4bdc8d51cf143299e4298e508390e789158e7800a1cf56de74dbb)
                check_type(argname="argument action_failure_policy", value=action_failure_policy, expected_type=type_hints["action_failure_policy"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
                check_type(argname="argument s3_sse_kms_key_id", value=s3_sse_kms_key_id, expected_type=type_hints["s3_sse_kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_failure_policy is not None:
                self._values["action_failure_policy"] = action_failure_policy
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_prefix is not None:
                self._values["s3_prefix"] = s3_prefix
            if s3_sse_kms_key_id is not None:
                self._values["s3_sse_kms_key_id"] = s3_sse_kms_key_id

        @builtins.property
        def action_failure_policy(self) -> typing.Optional[builtins.str]:
            '''A policy that states what to do in the case of failure.

            The action will fail if there are configuration errors. For example, the specified the bucket has been deleted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-s3action.html#cfn-ses-mailmanagerruleset-s3action-actionfailurepolicy
            '''
            result = self._values.get("action_failure_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM Role to use while writing to S3.

            This role must have access to the s3:PutObject, kms:Encrypt, and kms:GenerateDataKey APIs for the given bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-s3action.html#cfn-ses-mailmanagerruleset-s3action-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The bucket name of the S3 bucket to write to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-s3action.html#cfn-ses-mailmanagerruleset-s3action-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 prefix to use for the write to the s3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-s3action.html#cfn-ses-mailmanagerruleset-s3action-s3prefix
            '''
            result = self._values.get("s3_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_sse_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The KMS Key ID to use to encrypt the message in S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-s3action.html#cfn-ses-mailmanagerruleset-s3action-s3ssekmskeyid
            '''
            result = self._values.get("s3_sse_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.SendActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_failure_policy": "actionFailurePolicy",
            "role_arn": "roleArn",
        },
    )
    class SendActionProperty:
        def __init__(
            self,
            *,
            action_failure_policy: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sends the email to the internet using the ses:SendRawEmail API.

            :param action_failure_policy: A policy that states what to do in the case of failure. The action will fail if there are configuration errors. For example, the caller does not have the permissions to call the sendRawEmail API.
            :param role_arn: The Amazon Resource Name (ARN) of the role to use for this action. This role must have access to the ses:SendRawEmail API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-sendaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                send_action_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.SendActionProperty(
                    action_failure_policy="actionFailurePolicy",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb66d3f3bbdede6507d521066f0177ac8b0ad0b96649f7cc00fb6e207b4b7c5e)
                check_type(argname="argument action_failure_policy", value=action_failure_policy, expected_type=type_hints["action_failure_policy"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_failure_policy is not None:
                self._values["action_failure_policy"] = action_failure_policy
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def action_failure_policy(self) -> typing.Optional[builtins.str]:
            '''A policy that states what to do in the case of failure.

            The action will fail if there are configuration errors. For example, the caller does not have the permissions to call the sendRawEmail API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-sendaction.html#cfn-ses-mailmanagerruleset-sendaction-actionfailurepolicy
            '''
            result = self._values.get("action_failure_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the role to use for this action.

            This role must have access to the ses:SendRawEmail API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-sendaction.html#cfn-ses-mailmanagerruleset-sendaction-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SendActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerRuleSetPropsMixin.SnsActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_failure_policy": "actionFailurePolicy",
            "encoding": "encoding",
            "payload_type": "payloadType",
            "role_arn": "roleArn",
            "topic_arn": "topicArn",
        },
    )
    class SnsActionProperty:
        def __init__(
            self,
            *,
            action_failure_policy: typing.Optional[builtins.str] = None,
            encoding: typing.Optional[builtins.str] = None,
            payload_type: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The action to publish the email content to an Amazon SNS topic.

            When executed, this action will send the email as a notification to the specified SNS topic.

            :param action_failure_policy: A policy that states what to do in the case of failure. The action will fail if there are configuration errors. For example, specified SNS topic has been deleted or the role lacks necessary permissions to call the ``sns:Publish`` API.
            :param encoding: The encoding to use for the email within the Amazon SNS notification. The default value is ``UTF-8`` . Use ``BASE64`` if you need to preserve all special characters, especially when the original message uses a different encoding format.
            :param payload_type: The expected payload type within the Amazon SNS notification. ``CONTENT`` attempts to publish the full email content with 20KB of headers content. ``HEADERS`` extracts up to 100KB of header content to include in the notification, email content will not be included to the notification. The default value is ``CONTENT`` .
            :param role_arn: The Amazon Resource Name (ARN) of the IAM Role to use while writing to Amazon SNS. This role must have access to the ``sns:Publish`` API for the given topic.
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS Topic to which notification for the email received will be published.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-snsaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                sns_action_property = ses_mixins.CfnMailManagerRuleSetPropsMixin.SnsActionProperty(
                    action_failure_policy="actionFailurePolicy",
                    encoding="encoding",
                    payload_type="payloadType",
                    role_arn="roleArn",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8405def5b39a4a8f44725e4f71852182744c6019c9119008e9f97be26edc8ad)
                check_type(argname="argument action_failure_policy", value=action_failure_policy, expected_type=type_hints["action_failure_policy"])
                check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
                check_type(argname="argument payload_type", value=payload_type, expected_type=type_hints["payload_type"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_failure_policy is not None:
                self._values["action_failure_policy"] = action_failure_policy
            if encoding is not None:
                self._values["encoding"] = encoding
            if payload_type is not None:
                self._values["payload_type"] = payload_type
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def action_failure_policy(self) -> typing.Optional[builtins.str]:
            '''A policy that states what to do in the case of failure.

            The action will fail if there are configuration errors. For example, specified SNS topic has been deleted or the role lacks necessary permissions to call the ``sns:Publish`` API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-snsaction.html#cfn-ses-mailmanagerruleset-snsaction-actionfailurepolicy
            '''
            result = self._values.get("action_failure_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encoding(self) -> typing.Optional[builtins.str]:
            '''The encoding to use for the email within the Amazon SNS notification.

            The default value is ``UTF-8`` . Use ``BASE64`` if you need to preserve all special characters, especially when the original message uses a different encoding format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-snsaction.html#cfn-ses-mailmanagerruleset-snsaction-encoding
            '''
            result = self._values.get("encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload_type(self) -> typing.Optional[builtins.str]:
            '''The expected payload type within the Amazon SNS notification.

            ``CONTENT`` attempts to publish the full email content with 20KB of headers content. ``HEADERS`` extracts up to 100KB of header content to include in the notification, email content will not be included to the notification. The default value is ``CONTENT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-snsaction.html#cfn-ses-mailmanagerruleset-snsaction-payloadtype
            '''
            result = self._values.get("payload_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM Role to use while writing to Amazon SNS.

            This role must have access to the ``sns:Publish`` API for the given topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-snsaction.html#cfn-ses-mailmanagerruleset-snsaction-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS Topic to which notification for the email received will be published.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagerruleset-snsaction.html#cfn-ses-mailmanagerruleset-snsaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_action": "defaultAction",
        "max_message_size_bytes": "maxMessageSizeBytes",
        "policy_statements": "policyStatements",
        "tags": "tags",
        "traffic_policy_name": "trafficPolicyName",
    },
)
class CfnMailManagerTrafficPolicyMixinProps:
    def __init__(
        self,
        *,
        default_action: typing.Optional[builtins.str] = None,
        max_message_size_bytes: typing.Optional[jsii.Number] = None,
        policy_statements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.PolicyStatementProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        traffic_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMailManagerTrafficPolicyPropsMixin.

        :param default_action: Default action instructs the traﬃc policy to either Allow or Deny (block) messages that fall outside of (or not addressed by) the conditions of your policy statements.
        :param max_message_size_bytes: The maximum message size in bytes of email which is allowed in by this traffic policy—anything larger will be blocked.
        :param policy_statements: Conditional statements for filtering email traffic.
        :param tags: The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        :param traffic_policy_name: The name of the policy. The policy name cannot exceed 64 characters and can only include alphanumeric characters, dashes, and underscores.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagertrafficpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_mail_manager_traffic_policy_mixin_props = ses_mixins.CfnMailManagerTrafficPolicyMixinProps(
                default_action="defaultAction",
                max_message_size_bytes=123,
                policy_statements=[ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.PolicyStatementProperty(
                    action="action",
                    conditions=[ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.PolicyConditionProperty(
                        boolean_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                is_in_address_list=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty(
                                    address_lists=["addressLists"],
                                    attribute="attribute"
                                )
                            ),
                            operator="operator"
                        ),
                        ip_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv4ExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        ipv6_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        string_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        tls_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            value="value"
                        )
                    )]
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                traffic_policy_name="trafficPolicyName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a29a92deededc5a374f9f94f7bd1d2927294f626953a9c6e973314547f65c1)
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument max_message_size_bytes", value=max_message_size_bytes, expected_type=type_hints["max_message_size_bytes"])
            check_type(argname="argument policy_statements", value=policy_statements, expected_type=type_hints["policy_statements"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument traffic_policy_name", value=traffic_policy_name, expected_type=type_hints["traffic_policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_action is not None:
            self._values["default_action"] = default_action
        if max_message_size_bytes is not None:
            self._values["max_message_size_bytes"] = max_message_size_bytes
        if policy_statements is not None:
            self._values["policy_statements"] = policy_statements
        if tags is not None:
            self._values["tags"] = tags
        if traffic_policy_name is not None:
            self._values["traffic_policy_name"] = traffic_policy_name

    @builtins.property
    def default_action(self) -> typing.Optional[builtins.str]:
        '''Default action instructs the traﬃc policy to either Allow or Deny (block) messages that fall outside of (or not addressed by) the conditions of your policy statements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagertrafficpolicy.html#cfn-ses-mailmanagertrafficpolicy-defaultaction
        '''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_message_size_bytes(self) -> typing.Optional[jsii.Number]:
        '''The maximum message size in bytes of email which is allowed in by this traffic policy—anything larger will be blocked.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagertrafficpolicy.html#cfn-ses-mailmanagertrafficpolicy-maxmessagesizebytes
        '''
        result = self._values.get("max_message_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def policy_statements(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.PolicyStatementProperty"]]]]:
        '''Conditional statements for filtering email traffic.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagertrafficpolicy.html#cfn-ses-mailmanagertrafficpolicy-policystatements
        '''
        result = self._values.get("policy_statements")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.PolicyStatementProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for the resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagertrafficpolicy.html#cfn-ses-mailmanagertrafficpolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def traffic_policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy.

        The policy name cannot exceed 64 characters and can only include alphanumeric characters, dashes, and underscores.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagertrafficpolicy.html#cfn-ses-mailmanagertrafficpolicy-trafficpolicyname
        '''
        result = self._values.get("traffic_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMailManagerTrafficPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMailManagerTrafficPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin",
):
    '''Resource to create a traffic policy for a Mail Manager ingress endpoint which contains policy statements used to evaluate whether incoming emails should be allowed or denied.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-mailmanagertrafficpolicy.html
    :cloudformationResource: AWS::SES::MailManagerTrafficPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_mail_manager_traffic_policy_props_mixin = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin(ses_mixins.CfnMailManagerTrafficPolicyMixinProps(
            default_action="defaultAction",
            max_message_size_bytes=123,
            policy_statements=[ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.PolicyStatementProperty(
                action="action",
                conditions=[ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.PolicyConditionProperty(
                    boolean_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            is_in_address_list=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty(
                                address_lists=["addressLists"],
                                attribute="attribute"
                            )
                        ),
                        operator="operator"
                    ),
                    ip_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv4ExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    ipv6_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    string_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    tls_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        value="value"
                    )
                )]
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            traffic_policy_name="trafficPolicyName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMailManagerTrafficPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::MailManagerTrafficPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7144801b7263083cc91daab69d392dbcce67a594a52b88c575e6abcc3f366c88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80c70b8a287dfdbe919da6888b34512911847d52a06c26b5737451abd662d6eb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191fdaa9bd8c9fbcb9d9306f9e51ca5ce497f091ad90f222686ac9499e1899c8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMailManagerTrafficPolicyMixinProps:
        return typing.cast(CfnMailManagerTrafficPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty",
        jsii_struct_bases=[],
        name_mapping={"analyzer": "analyzer", "result_field": "resultField"},
    )
    class IngressAnalysisProperty:
        def __init__(
            self,
            *,
            analyzer: typing.Optional[builtins.str] = None,
            result_field: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Add On ARN and its returned value that is evaluated in a policy statement's conditional expression to either deny or block the incoming email.

            :param analyzer: The Amazon Resource Name (ARN) of an Add On.
            :param result_field: The returned value from an Add On.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressanalysis.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_analysis_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                    analyzer="analyzer",
                    result_field="resultField"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__909d5b19725b4cb02f91cc84e9827a9daff4d6748b933ee8d55b007cfdff1072)
                check_type(argname="argument analyzer", value=analyzer, expected_type=type_hints["analyzer"])
                check_type(argname="argument result_field", value=result_field, expected_type=type_hints["result_field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if analyzer is not None:
                self._values["analyzer"] = analyzer
            if result_field is not None:
                self._values["result_field"] = result_field

        @builtins.property
        def analyzer(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an Add On.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressanalysis.html#cfn-ses-mailmanagertrafficpolicy-ingressanalysis-analyzer
            '''
            result = self._values.get("analyzer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def result_field(self) -> typing.Optional[builtins.str]:
            '''The returned value from an Add On.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressanalysis.html#cfn-ses-mailmanagertrafficpolicy-ingressanalysis-resultfield
            '''
            result = self._values.get("result_field")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressAnalysisProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={"evaluate": "evaluate", "operator": "operator"},
    )
    class IngressBooleanExpressionProperty:
        def __init__(
            self,
            *,
            evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The structure for a boolean condition matching on the incoming mail.

            :param evaluate: The operand on which to perform a boolean condition operation.
            :param operator: The matching operator for a boolean condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressbooleanexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_boolean_expression_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanExpressionProperty(
                    evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty(
                        analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                            analyzer="analyzer",
                            result_field="resultField"
                        ),
                        is_in_address_list=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty(
                            address_lists=["addressLists"],
                            attribute="attribute"
                        )
                    ),
                    operator="operator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e07e97e2c648d4b817d03c886b97568dac9bf0f118a6a02ee0e6b0c06a31931)
                check_type(argname="argument evaluate", value=evaluate, expected_type=type_hints["evaluate"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluate is not None:
                self._values["evaluate"] = evaluate
            if operator is not None:
                self._values["operator"] = operator

        @builtins.property
        def evaluate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty"]]:
            '''The operand on which to perform a boolean condition operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressbooleanexpression.html#cfn-ses-mailmanagertrafficpolicy-ingressbooleanexpression-evaluate
            '''
            result = self._values.get("evaluate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The matching operator for a boolean condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressbooleanexpression.html#cfn-ses-mailmanagertrafficpolicy-ingressbooleanexpression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressBooleanExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty",
        jsii_struct_bases=[],
        name_mapping={"analysis": "analysis", "is_in_address_list": "isInAddressList"},
    )
    class IngressBooleanToEvaluateProperty:
        def __init__(
            self,
            *,
            analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_in_address_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The union type representing the allowed types of operands for a boolean condition.

            :param analysis: The structure type for a boolean condition stating the Add On ARN and its returned value.
            :param is_in_address_list: The structure type for a boolean condition that provides the address lists to evaluate incoming traffic on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressbooleantoevaluate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_boolean_to_evaluate_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty(
                    analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                        analyzer="analyzer",
                        result_field="resultField"
                    ),
                    is_in_address_list=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty(
                        address_lists=["addressLists"],
                        attribute="attribute"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__490c5d658fb2c59c899fe02184faa1ceb6794a1f7968d7b80b901161bfbdde20)
                check_type(argname="argument analysis", value=analysis, expected_type=type_hints["analysis"])
                check_type(argname="argument is_in_address_list", value=is_in_address_list, expected_type=type_hints["is_in_address_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if analysis is not None:
                self._values["analysis"] = analysis
            if is_in_address_list is not None:
                self._values["is_in_address_list"] = is_in_address_list

        @builtins.property
        def analysis(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty"]]:
            '''The structure type for a boolean condition stating the Add On ARN and its returned value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressbooleantoevaluate.html#cfn-ses-mailmanagertrafficpolicy-ingressbooleantoevaluate-analysis
            '''
            result = self._values.get("analysis")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty"]], result)

        @builtins.property
        def is_in_address_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty"]]:
            '''The structure type for a boolean condition that provides the address lists to evaluate incoming traffic on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressbooleantoevaluate.html#cfn-ses-mailmanagertrafficpolicy-ingressbooleantoevaluate-isinaddresslist
            '''
            result = self._values.get("is_in_address_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressBooleanToEvaluateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute": "attribute"},
    )
    class IngressIpToEvaluateProperty:
        def __init__(self, *, attribute: typing.Optional[builtins.str] = None) -> None:
            '''The structure for an IP based condition matching on the incoming mail.

            :param attribute: An enum type representing the allowed attribute types for an IP condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressiptoevaluate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_ip_to_evaluate_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty(
                    attribute="attribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3060689fec824b1d217f6e8faea8d0bb5463bfb8874f1aefafcd6f0ea645b14f)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''An enum type representing the allowed attribute types for an IP condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressiptoevaluate.html#cfn-ses-mailmanagertrafficpolicy-ingressiptoevaluate-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressIpToEvaluateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv4ExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "evaluate": "evaluate",
            "operator": "operator",
            "values": "values",
        },
    )
    class IngressIpv4ExpressionProperty:
        def __init__(
            self,
            *,
            evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The union type representing the allowed types for the left hand side of an IP condition.

            :param evaluate: The left hand side argument of an IP condition expression.
            :param operator: The matching operator for an IP condition expression.
            :param values: The right hand side argument of an IP condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressipv4expression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_ipv4_expression_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv4ExpressionProperty(
                    evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty(
                        attribute="attribute"
                    ),
                    operator="operator",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__144d6b4e7d5ea283bf003e6e73645b24f8af64965f8755362ab326bcf0e27877)
                check_type(argname="argument evaluate", value=evaluate, expected_type=type_hints["evaluate"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluate is not None:
                self._values["evaluate"] = evaluate
            if operator is not None:
                self._values["operator"] = operator
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def evaluate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty"]]:
            '''The left hand side argument of an IP condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressipv4expression.html#cfn-ses-mailmanagertrafficpolicy-ingressipv4expression-evaluate
            '''
            result = self._values.get("evaluate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The matching operator for an IP condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressipv4expression.html#cfn-ses-mailmanagertrafficpolicy-ingressipv4expression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The right hand side argument of an IP condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressipv4expression.html#cfn-ses-mailmanagertrafficpolicy-ingressipv4expression-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressIpv4ExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "evaluate": "evaluate",
            "operator": "operator",
            "values": "values",
        },
    )
    class IngressIpv6ExpressionProperty:
        def __init__(
            self,
            *,
            evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The union type representing the allowed types for the left hand side of an IPv6 condition.

            :param evaluate: The left hand side argument of an IPv6 condition expression.
            :param operator: The matching operator for an IPv6 condition expression.
            :param values: The right hand side argument of an IPv6 condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressipv6expression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_ipv6_expression_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ExpressionProperty(
                    evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty(
                        attribute="attribute"
                    ),
                    operator="operator",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__21a2472fab341e68074edffbe107dc6469b9317b1d4a75d3dcfa0bca43bbee94)
                check_type(argname="argument evaluate", value=evaluate, expected_type=type_hints["evaluate"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluate is not None:
                self._values["evaluate"] = evaluate
            if operator is not None:
                self._values["operator"] = operator
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def evaluate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty"]]:
            '''The left hand side argument of an IPv6 condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressipv6expression.html#cfn-ses-mailmanagertrafficpolicy-ingressipv6expression-evaluate
            '''
            result = self._values.get("evaluate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The matching operator for an IPv6 condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressipv6expression.html#cfn-ses-mailmanagertrafficpolicy-ingressipv6expression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The right hand side argument of an IPv6 condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressipv6expression.html#cfn-ses-mailmanagertrafficpolicy-ingressipv6expression-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressIpv6ExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute": "attribute"},
    )
    class IngressIpv6ToEvaluateProperty:
        def __init__(self, *, attribute: typing.Optional[builtins.str] = None) -> None:
            '''The structure for an IPv6 based condition matching on the incoming mail.

            :param attribute: An enum type representing the allowed attribute types for an IPv6 condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressipv6toevaluate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_ipv6_to_evaluate_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty(
                    attribute="attribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73396557b1140fefa6e5b21f9ab88c694765ea3bbf48535ece4bd1a97ecd07ff)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''An enum type representing the allowed attribute types for an IPv6 condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressipv6toevaluate.html#cfn-ses-mailmanagertrafficpolicy-ingressipv6toevaluate-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressIpv6ToEvaluateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty",
        jsii_struct_bases=[],
        name_mapping={"address_lists": "addressLists", "attribute": "attribute"},
    )
    class IngressIsInAddressListProperty:
        def __init__(
            self,
            *,
            address_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
            attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The address lists and the address list attribute value that is evaluated in a policy statement's conditional expression to either deny or block the incoming email.

            :param address_lists: The address lists that will be used for evaluation.
            :param attribute: The email attribute that needs to be evaluated against the address list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressisinaddresslist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_is_in_address_list_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty(
                    address_lists=["addressLists"],
                    attribute="attribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8509c5b3b7c1443279c6b3fdfdc88da2fb76b03e93319215c5f6a350c7e50a19)
                check_type(argname="argument address_lists", value=address_lists, expected_type=type_hints["address_lists"])
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address_lists is not None:
                self._values["address_lists"] = address_lists
            if attribute is not None:
                self._values["attribute"] = attribute

        @builtins.property
        def address_lists(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The address lists that will be used for evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressisinaddresslist.html#cfn-ses-mailmanagertrafficpolicy-ingressisinaddresslist-addresslists
            '''
            result = self._values.get("address_lists")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The email attribute that needs to be evaluated against the address list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressisinaddresslist.html#cfn-ses-mailmanagertrafficpolicy-ingressisinaddresslist-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressIsInAddressListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "evaluate": "evaluate",
            "operator": "operator",
            "values": "values",
        },
    )
    class IngressStringExpressionProperty:
        def __init__(
            self,
            *,
            evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The structure for a string based condition matching on the incoming mail.

            :param evaluate: The left hand side argument of a string condition expression.
            :param operator: 
            :param values: The right hand side argument of a string condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressstringexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_string_expression_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringExpressionProperty(
                    evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty(
                        analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                            analyzer="analyzer",
                            result_field="resultField"
                        ),
                        attribute="attribute"
                    ),
                    operator="operator",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9e9d061de221d1c76af47f9e5777328c398883921088737ef53b9dadb122ae4)
                check_type(argname="argument evaluate", value=evaluate, expected_type=type_hints["evaluate"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluate is not None:
                self._values["evaluate"] = evaluate
            if operator is not None:
                self._values["operator"] = operator
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def evaluate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty"]]:
            '''The left hand side argument of a string condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressstringexpression.html#cfn-ses-mailmanagertrafficpolicy-ingressstringexpression-evaluate
            '''
            result = self._values.get("evaluate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressstringexpression.html#cfn-ses-mailmanagertrafficpolicy-ingressstringexpression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The right hand side argument of a string condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressstringexpression.html#cfn-ses-mailmanagertrafficpolicy-ingressstringexpression-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressStringExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty",
        jsii_struct_bases=[],
        name_mapping={"analysis": "analysis", "attribute": "attribute"},
    )
    class IngressStringToEvaluateProperty:
        def __init__(
            self,
            *,
            analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The union type representing the allowed types for the left hand side of a string condition.

            :param analysis: The structure type for a string condition stating the Add On ARN and its returned value.
            :param attribute: The enum type representing the allowed attribute types for a string condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressstringtoevaluate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_string_to_evaluate_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty(
                    analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                        analyzer="analyzer",
                        result_field="resultField"
                    ),
                    attribute="attribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d82b326396745b75e4567d882ffaaef1591789b156f48ef3afd53b2b9e461cb)
                check_type(argname="argument analysis", value=analysis, expected_type=type_hints["analysis"])
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if analysis is not None:
                self._values["analysis"] = analysis
            if attribute is not None:
                self._values["attribute"] = attribute

        @builtins.property
        def analysis(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty"]]:
            '''The structure type for a string condition stating the Add On ARN and its returned value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressstringtoevaluate.html#cfn-ses-mailmanagertrafficpolicy-ingressstringtoevaluate-analysis
            '''
            result = self._values.get("analysis")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty"]], result)

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The enum type representing the allowed attribute types for a string condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingressstringtoevaluate.html#cfn-ses-mailmanagertrafficpolicy-ingressstringtoevaluate-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressStringToEvaluateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "evaluate": "evaluate",
            "operator": "operator",
            "value": "value",
        },
    )
    class IngressTlsProtocolExpressionProperty:
        def __init__(
            self,
            *,
            evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The structure for a TLS related condition matching on the incoming mail.

            :param evaluate: The left hand side argument of a TLS condition expression.
            :param operator: The matching operator for a TLS condition expression.
            :param value: The right hand side argument of a TLS condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingresstlsprotocolexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_tls_protocol_expression_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolExpressionProperty(
                    evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty(
                        attribute="attribute"
                    ),
                    operator="operator",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be58f6d26ed1e605e6d8a01233985357f18fdb6444e6ee6ce5883167a021a1c7)
                check_type(argname="argument evaluate", value=evaluate, expected_type=type_hints["evaluate"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluate is not None:
                self._values["evaluate"] = evaluate
            if operator is not None:
                self._values["operator"] = operator
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def evaluate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty"]]:
            '''The left hand side argument of a TLS condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingresstlsprotocolexpression.html#cfn-ses-mailmanagertrafficpolicy-ingresstlsprotocolexpression-evaluate
            '''
            result = self._values.get("evaluate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The matching operator for a TLS condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingresstlsprotocolexpression.html#cfn-ses-mailmanagertrafficpolicy-ingresstlsprotocolexpression-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The right hand side argument of a TLS condition expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingresstlsprotocolexpression.html#cfn-ses-mailmanagertrafficpolicy-ingresstlsprotocolexpression-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressTlsProtocolExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute": "attribute"},
    )
    class IngressTlsProtocolToEvaluateProperty:
        def __init__(self, *, attribute: typing.Optional[builtins.str] = None) -> None:
            '''The union type representing the allowed types for the left hand side of a TLS condition.

            :param attribute: The enum type representing the allowed attribute types for the TLS condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingresstlsprotocoltoevaluate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ingress_tls_protocol_to_evaluate_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty(
                    attribute="attribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4d28710a38ede59efe9470a83c081684d7d514d22f4db4cb7b67db3a60ed150)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The enum type representing the allowed attribute types for the TLS condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-ingresstlsprotocoltoevaluate.html#cfn-ses-mailmanagertrafficpolicy-ingresstlsprotocoltoevaluate-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressTlsProtocolToEvaluateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.PolicyConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_expression": "booleanExpression",
            "ip_expression": "ipExpression",
            "ipv6_expression": "ipv6Expression",
            "string_expression": "stringExpression",
            "tls_expression": "tlsExpression",
        },
    )
    class PolicyConditionProperty:
        def __init__(
            self,
            *,
            boolean_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressIpv4ExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ipv6_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            string_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressStringExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tls_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The email traffic filtering conditions which are contained in a traffic policy resource.

            .. epigraph::

               This data type is a UNION, so only one of the following members can be specified when used or returned.

            :param boolean_expression: This represents a boolean type condition matching on the incoming mail. It performs the boolean operation configured in 'Operator' and evaluates the 'Protocol' object against the 'Value'.
            :param ip_expression: This represents an IP based condition matching on the incoming mail. It performs the operation configured in 'Operator' and evaluates the 'Protocol' object against the 'Value'.
            :param ipv6_expression: This represents an IPv6 based condition matching on the incoming mail. It performs the operation configured in 'Operator' and evaluates the 'Protocol' object against the 'Value'.
            :param string_expression: This represents a string based condition matching on the incoming mail. It performs the string operation configured in 'Operator' and evaluates the 'Protocol' object against the 'Value'.
            :param tls_expression: This represents a TLS based condition matching on the incoming mail. It performs the operation configured in 'Operator' and evaluates the 'Protocol' object against the 'Value'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-policycondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                policy_condition_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.PolicyConditionProperty(
                    boolean_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            is_in_address_list=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty(
                                address_lists=["addressLists"],
                                attribute="attribute"
                            )
                        ),
                        operator="operator"
                    ),
                    ip_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv4ExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    ipv6_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    string_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty(
                            analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                                analyzer="analyzer",
                                result_field="resultField"
                            ),
                            attribute="attribute"
                        ),
                        operator="operator",
                        values=["values"]
                    ),
                    tls_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolExpressionProperty(
                        evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty(
                            attribute="attribute"
                        ),
                        operator="operator",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6170c880171e0b933fedafc2167034d4bc58a0945c5212f47b80d9134406dd39)
                check_type(argname="argument boolean_expression", value=boolean_expression, expected_type=type_hints["boolean_expression"])
                check_type(argname="argument ip_expression", value=ip_expression, expected_type=type_hints["ip_expression"])
                check_type(argname="argument ipv6_expression", value=ipv6_expression, expected_type=type_hints["ipv6_expression"])
                check_type(argname="argument string_expression", value=string_expression, expected_type=type_hints["string_expression"])
                check_type(argname="argument tls_expression", value=tls_expression, expected_type=type_hints["tls_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_expression is not None:
                self._values["boolean_expression"] = boolean_expression
            if ip_expression is not None:
                self._values["ip_expression"] = ip_expression
            if ipv6_expression is not None:
                self._values["ipv6_expression"] = ipv6_expression
            if string_expression is not None:
                self._values["string_expression"] = string_expression
            if tls_expression is not None:
                self._values["tls_expression"] = tls_expression

        @builtins.property
        def boolean_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanExpressionProperty"]]:
            '''This represents a boolean type condition matching on the incoming mail.

            It performs the boolean operation configured in 'Operator' and evaluates the 'Protocol' object against the 'Value'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-policycondition.html#cfn-ses-mailmanagertrafficpolicy-policycondition-booleanexpression
            '''
            result = self._values.get("boolean_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanExpressionProperty"]], result)

        @builtins.property
        def ip_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressIpv4ExpressionProperty"]]:
            '''This represents an IP based condition matching on the incoming mail.

            It performs the operation configured in 'Operator' and evaluates the 'Protocol' object against the 'Value'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-policycondition.html#cfn-ses-mailmanagertrafficpolicy-policycondition-ipexpression
            '''
            result = self._values.get("ip_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressIpv4ExpressionProperty"]], result)

        @builtins.property
        def ipv6_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ExpressionProperty"]]:
            '''This represents an IPv6 based condition matching on the incoming mail.

            It performs the operation configured in 'Operator' and evaluates the 'Protocol' object against the 'Value'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-policycondition.html#cfn-ses-mailmanagertrafficpolicy-policycondition-ipv6expression
            '''
            result = self._values.get("ipv6_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ExpressionProperty"]], result)

        @builtins.property
        def string_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressStringExpressionProperty"]]:
            '''This represents a string based condition matching on the incoming mail.

            It performs the string operation configured in 'Operator' and evaluates the 'Protocol' object against the 'Value'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-policycondition.html#cfn-ses-mailmanagertrafficpolicy-policycondition-stringexpression
            '''
            result = self._values.get("string_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressStringExpressionProperty"]], result)

        @builtins.property
        def tls_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolExpressionProperty"]]:
            '''This represents a TLS based condition matching on the incoming mail.

            It performs the operation configured in 'Operator' and evaluates the 'Protocol' object against the 'Value'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-policycondition.html#cfn-ses-mailmanagertrafficpolicy-policycondition-tlsexpression
            '''
            result = self._values.get("tls_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolExpressionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMailManagerTrafficPolicyPropsMixin.PolicyStatementProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "conditions": "conditions"},
    )
    class PolicyStatementProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMailManagerTrafficPolicyPropsMixin.PolicyConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The structure containing traffic policy conditions and actions.

            :param action: The action that informs a traffic policy resource to either allow or block the email if it matches a condition in the policy statement.
            :param conditions: The list of conditions to apply to incoming messages for filtering email traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-policystatement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                policy_statement_property = ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.PolicyStatementProperty(
                    action="action",
                    conditions=[ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.PolicyConditionProperty(
                        boolean_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                is_in_address_list=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty(
                                    address_lists=["addressLists"],
                                    attribute="attribute"
                                )
                            ),
                            operator="operator"
                        ),
                        ip_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv4ExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        ipv6_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        string_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty(
                                analysis=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty(
                                    analyzer="analyzer",
                                    result_field="resultField"
                                ),
                                attribute="attribute"
                            ),
                            operator="operator",
                            values=["values"]
                        ),
                        tls_expression=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolExpressionProperty(
                            evaluate=ses_mixins.CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty(
                                attribute="attribute"
                            ),
                            operator="operator",
                            value="value"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d0e45eee896bbd32127418a3e22672d9ed990736e5cc7f4677b032f98582c95)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if conditions is not None:
                self._values["conditions"] = conditions

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action that informs a traffic policy resource to either allow or block the email if it matches a condition in the policy statement.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-policystatement.html#cfn-ses-mailmanagertrafficpolicy-policystatement-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.PolicyConditionProperty"]]]]:
            '''The list of conditions to apply to incoming messages for filtering email traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-mailmanagertrafficpolicy-policystatement.html#cfn-ses-mailmanagertrafficpolicy-policystatement-conditions
            '''
            result = self._values.get("conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMailManagerTrafficPolicyPropsMixin.PolicyConditionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMultiRegionEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "details": "details",
        "endpoint_name": "endpointName",
        "tags": "tags",
    },
)
class CfnMultiRegionEndpointMixinProps:
    def __init__(
        self,
        *,
        details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMultiRegionEndpointPropsMixin.DetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        endpoint_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMultiRegionEndpointPropsMixin.

        :param details: Contains details of a multi-region endpoint (global-endpoint) being created.
        :param endpoint_name: The name of the multi-region endpoint (global-endpoint).
        :param tags: An array of objects that define the tags (keys and values) to associate with the multi-region endpoint (global-endpoint).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-multiregionendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_multi_region_endpoint_mixin_props = ses_mixins.CfnMultiRegionEndpointMixinProps(
                details=ses_mixins.CfnMultiRegionEndpointPropsMixin.DetailsProperty(
                    route_details=[ses_mixins.CfnMultiRegionEndpointPropsMixin.RouteDetailsItemsProperty(
                        region="region"
                    )]
                ),
                endpoint_name="endpointName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a871fd20cc36ff088be673b1b8639fe0fe2206fbb7a6b9115c1290f8c2c7d46f)
            check_type(argname="argument details", value=details, expected_type=type_hints["details"])
            check_type(argname="argument endpoint_name", value=endpoint_name, expected_type=type_hints["endpoint_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if details is not None:
            self._values["details"] = details
        if endpoint_name is not None:
            self._values["endpoint_name"] = endpoint_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMultiRegionEndpointPropsMixin.DetailsProperty"]]:
        '''Contains details of a multi-region endpoint (global-endpoint) being created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-multiregionendpoint.html#cfn-ses-multiregionendpoint-details
        '''
        result = self._values.get("details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMultiRegionEndpointPropsMixin.DetailsProperty"]], result)

    @builtins.property
    def endpoint_name(self) -> typing.Optional[builtins.str]:
        '''The name of the multi-region endpoint (global-endpoint).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-multiregionendpoint.html#cfn-ses-multiregionendpoint-endpointname
        '''
        result = self._values.get("endpoint_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of objects that define the tags (keys and values) to associate with the multi-region endpoint (global-endpoint).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-multiregionendpoint.html#cfn-ses-multiregionendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMultiRegionEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMultiRegionEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMultiRegionEndpointPropsMixin",
):
    '''Creates a multi-region endpoint (global-endpoint).

    The primary region is going to be the AWS-Region where the operation is executed. The secondary region has to be provided in request's parameters. From the data flow standpoint there is no difference between primary and secondary regions - sending traffic will be split equally between the two. The primary region is the region where the resource has been created and where it can be managed.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-multiregionendpoint.html
    :cloudformationResource: AWS::SES::MultiRegionEndpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_multi_region_endpoint_props_mixin = ses_mixins.CfnMultiRegionEndpointPropsMixin(ses_mixins.CfnMultiRegionEndpointMixinProps(
            details=ses_mixins.CfnMultiRegionEndpointPropsMixin.DetailsProperty(
                route_details=[ses_mixins.CfnMultiRegionEndpointPropsMixin.RouteDetailsItemsProperty(
                    region="region"
                )]
            ),
            endpoint_name="endpointName",
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
        props: typing.Union[CfnMultiRegionEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::MultiRegionEndpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ee209e6a269a478cbcdf71c07588912ef31a432a6e6366f07c6d9f84aa8220)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40e85092416e820668311375643cedbc1b08567f9447733c3296c884e5f111b9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037bbad86283faa565f54c09dd4f928fd346570b27c23487ffe8e346f0e2fe9a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMultiRegionEndpointMixinProps:
        return typing.cast(CfnMultiRegionEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMultiRegionEndpointPropsMixin.DetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"route_details": "routeDetails"},
    )
    class DetailsProperty:
        def __init__(
            self,
            *,
            route_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMultiRegionEndpointPropsMixin.RouteDetailsItemsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that contains configuration details of multi-region endpoint (global-endpoint).

            :param route_details: A list of route configuration details. Must contain exactly one route configuration

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-multiregionendpoint-details.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                details_property = ses_mixins.CfnMultiRegionEndpointPropsMixin.DetailsProperty(
                    route_details=[ses_mixins.CfnMultiRegionEndpointPropsMixin.RouteDetailsItemsProperty(
                        region="region"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fce69c6b40ac3c5f9001a06e735cc3d3be85be2b36fed22ae9db809a6461efca)
                check_type(argname="argument route_details", value=route_details, expected_type=type_hints["route_details"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if route_details is not None:
                self._values["route_details"] = route_details

        @builtins.property
        def route_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMultiRegionEndpointPropsMixin.RouteDetailsItemsProperty"]]]]:
            '''A list of route configuration details.

            Must contain exactly one route configuration

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-multiregionendpoint-details.html#cfn-ses-multiregionendpoint-details-routedetails
            '''
            result = self._values.get("route_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMultiRegionEndpointPropsMixin.RouteDetailsItemsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnMultiRegionEndpointPropsMixin.RouteDetailsItemsProperty",
        jsii_struct_bases=[],
        name_mapping={"region": "region"},
    )
    class RouteDetailsItemsProperty:
        def __init__(self, *, region: typing.Optional[builtins.str] = None) -> None:
            '''
            :param region: The name of an AWS-Region to be a secondary region for the multi-region endpoint (global-endpoint).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-multiregionendpoint-routedetailsitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                route_details_items_property = ses_mixins.CfnMultiRegionEndpointPropsMixin.RouteDetailsItemsProperty(
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49766420ba90eb571427152de585931a0fc27a980e63d329599d6358c437f827)
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The name of an AWS-Region to be a secondary region for the multi-region endpoint (global-endpoint).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-multiregionendpoint-routedetailsitems.html#cfn-ses-multiregionendpoint-routedetailsitems-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteDetailsItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptFilterMixinProps",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter"},
)
class CfnReceiptFilterMixinProps:
    def __init__(
        self,
        *,
        filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptFilterPropsMixin.FilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnReceiptFilterPropsMixin.

        :param filter: A data structure that describes the IP address filter to create, which consists of a name, an IP address range, and whether to allow or block mail from it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_receipt_filter_mixin_props = ses_mixins.CfnReceiptFilterMixinProps(
                filter=ses_mixins.CfnReceiptFilterPropsMixin.FilterProperty(
                    ip_filter=ses_mixins.CfnReceiptFilterPropsMixin.IpFilterProperty(
                        cidr="cidr",
                        policy="policy"
                    ),
                    name="name"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf3084140b378671c678cd74853f9e614b424ce200720f5e49267323db4d967)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptFilterPropsMixin.FilterProperty"]]:
        '''A data structure that describes the IP address filter to create, which consists of a name, an IP address range, and whether to allow or block mail from it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptfilter.html#cfn-ses-receiptfilter-filter
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptFilterPropsMixin.FilterProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReceiptFilterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReceiptFilterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptFilterPropsMixin",
):
    '''Specify a new IP address filter.

    You use IP address filters when you receive email with Amazon SES.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptfilter.html
    :cloudformationResource: AWS::SES::ReceiptFilter
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_receipt_filter_props_mixin = ses_mixins.CfnReceiptFilterPropsMixin(ses_mixins.CfnReceiptFilterMixinProps(
            filter=ses_mixins.CfnReceiptFilterPropsMixin.FilterProperty(
                ip_filter=ses_mixins.CfnReceiptFilterPropsMixin.IpFilterProperty(
                    cidr="cidr",
                    policy="policy"
                ),
                name="name"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReceiptFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::ReceiptFilter``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95579bb5aeb8b808d3653372f1739b53a452efe268e88175f1b77c7f7f062720)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a238f2d456ccb1c37f223106ec8c554c80eb1cf6fa0a65e8eb0cbc662d4f722)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592213f6d4c1d69073337e3f3bf48207cc0820677e6c0f8802fca8ed2a8cec06)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReceiptFilterMixinProps:
        return typing.cast(CfnReceiptFilterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptFilterPropsMixin.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_filter": "ipFilter", "name": "name"},
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            ip_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptFilterPropsMixin.IpFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an IP address filter.

            :param ip_filter: A structure that provides the IP addresses to block or allow, and whether to block or allow incoming mail from them.
            :param name: The name of the IP address filter. The name must meet the following requirements:. - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-). - Start and end with a letter or number. - Contain 64 characters or fewer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                filter_property = ses_mixins.CfnReceiptFilterPropsMixin.FilterProperty(
                    ip_filter=ses_mixins.CfnReceiptFilterPropsMixin.IpFilterProperty(
                        cidr="cidr",
                        policy="policy"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a577ffe595807c7e9fffadf284cabbd57aab30ef6128a9fb235250cc19d1b9b8)
                check_type(argname="argument ip_filter", value=ip_filter, expected_type=type_hints["ip_filter"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_filter is not None:
                self._values["ip_filter"] = ip_filter
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def ip_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptFilterPropsMixin.IpFilterProperty"]]:
            '''A structure that provides the IP addresses to block or allow, and whether to block or allow incoming mail from them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-filter.html#cfn-ses-receiptfilter-filter-ipfilter
            '''
            result = self._values.get("ip_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptFilterPropsMixin.IpFilterProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the IP address filter. The name must meet the following requirements:.

            - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-).
            - Start and end with a letter or number.
            - Contain 64 characters or fewer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-filter.html#cfn-ses-receiptfilter-filter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptFilterPropsMixin.IpFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"cidr": "cidr", "policy": "policy"},
    )
    class IpFilterProperty:
        def __init__(
            self,
            *,
            cidr: typing.Optional[builtins.str] = None,
            policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A receipt IP address filter enables you to specify whether to accept or reject mail originating from an IP address or range of IP addresses.

            For information about setting up IP address filters, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-ip-filtering-console-walkthrough.html>`_ .

            :param cidr: A single IP address or a range of IP addresses to block or allow, specified in Classless Inter-Domain Routing (CIDR) notation. An example of a single email address is 10.0.0.1. An example of a range of IP addresses is 10.0.0.1/24. For more information about CIDR notation, see `RFC 2317 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc2317>`_ .
            :param policy: Indicates whether to block or allow incoming mail from the specified IP addresses.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-ipfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                ip_filter_property = ses_mixins.CfnReceiptFilterPropsMixin.IpFilterProperty(
                    cidr="cidr",
                    policy="policy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f9d383f7f5f4ea5b9c12e4c387ca7e01e43a610710f93dcbc60f383a05a9b98)
                check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
                check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidr is not None:
                self._values["cidr"] = cidr
            if policy is not None:
                self._values["policy"] = policy

        @builtins.property
        def cidr(self) -> typing.Optional[builtins.str]:
            '''A single IP address or a range of IP addresses to block or allow, specified in Classless Inter-Domain Routing (CIDR) notation.

            An example of a single email address is 10.0.0.1. An example of a range of IP addresses is 10.0.0.1/24. For more information about CIDR notation, see `RFC 2317 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc2317>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-ipfilter.html#cfn-ses-receiptfilter-ipfilter-cidr
            '''
            result = self._values.get("cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy(self) -> typing.Optional[builtins.str]:
            '''Indicates whether to block or allow incoming mail from the specified IP addresses.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-ipfilter.html#cfn-ses-receiptfilter-ipfilter-policy
            '''
            result = self._values.get("policy")
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
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={"after": "after", "rule": "rule", "rule_set_name": "ruleSetName"},
)
class CfnReceiptRuleMixinProps:
    def __init__(
        self,
        *,
        after: typing.Optional[builtins.str] = None,
        rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptRulePropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_set_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnReceiptRulePropsMixin.

        :param after: The name of an existing rule after which the new rule is placed. If this parameter is null, the new rule is inserted at the beginning of the rule list.
        :param rule: A data structure that contains the specified rule's name, actions, recipients, domains, enabled status, scan status, and TLS policy.
        :param rule_set_name: The name of the rule set where the receipt rule is added.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_receipt_rule_mixin_props = ses_mixins.CfnReceiptRuleMixinProps(
                after="after",
                rule=ses_mixins.CfnReceiptRulePropsMixin.RuleProperty(
                    actions=[ses_mixins.CfnReceiptRulePropsMixin.ActionProperty(
                        add_header_action=ses_mixins.CfnReceiptRulePropsMixin.AddHeaderActionProperty(
                            header_name="headerName",
                            header_value="headerValue"
                        ),
                        bounce_action=ses_mixins.CfnReceiptRulePropsMixin.BounceActionProperty(
                            message="message",
                            sender="sender",
                            smtp_reply_code="smtpReplyCode",
                            status_code="statusCode",
                            topic_arn="topicArn"
                        ),
                        connect_action=ses_mixins.CfnReceiptRulePropsMixin.ConnectActionProperty(
                            iam_role_arn="iamRoleArn",
                            instance_arn="instanceArn"
                        ),
                        lambda_action=ses_mixins.CfnReceiptRulePropsMixin.LambdaActionProperty(
                            function_arn="functionArn",
                            invocation_type="invocationType",
                            topic_arn="topicArn"
                        ),
                        s3_action=ses_mixins.CfnReceiptRulePropsMixin.S3ActionProperty(
                            bucket_name="bucketName",
                            iam_role_arn="iamRoleArn",
                            kms_key_arn="kmsKeyArn",
                            object_key_prefix="objectKeyPrefix",
                            topic_arn="topicArn"
                        ),
                        sns_action=ses_mixins.CfnReceiptRulePropsMixin.SNSActionProperty(
                            encoding="encoding",
                            topic_arn="topicArn"
                        ),
                        stop_action=ses_mixins.CfnReceiptRulePropsMixin.StopActionProperty(
                            scope="scope",
                            topic_arn="topicArn"
                        ),
                        workmail_action=ses_mixins.CfnReceiptRulePropsMixin.WorkmailActionProperty(
                            organization_arn="organizationArn",
                            topic_arn="topicArn"
                        )
                    )],
                    enabled=False,
                    name="name",
                    recipients=["recipients"],
                    scan_enabled=False,
                    tls_policy="tlsPolicy"
                ),
                rule_set_name="ruleSetName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae64b6b855b6a5dc864b51b138f7183f0ba01bf4716e381417e16165c2fde976)
            check_type(argname="argument after", value=after, expected_type=type_hints["after"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument rule_set_name", value=rule_set_name, expected_type=type_hints["rule_set_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if after is not None:
            self._values["after"] = after
        if rule is not None:
            self._values["rule"] = rule
        if rule_set_name is not None:
            self._values["rule_set_name"] = rule_set_name

    @builtins.property
    def after(self) -> typing.Optional[builtins.str]:
        '''The name of an existing rule after which the new rule is placed.

        If this parameter is null, the new rule is inserted at the beginning of the rule list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-after
        '''
        result = self._values.get("after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.RuleProperty"]]:
        '''A data structure that contains the specified rule's name, actions, recipients, domains, enabled status, scan status, and TLS policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-rule
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.RuleProperty"]], result)

    @builtins.property
    def rule_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule set where the receipt rule is added.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-rulesetname
        '''
        result = self._values.get("rule_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReceiptRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReceiptRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin",
):
    '''Specifies a receipt rule.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html
    :cloudformationResource: AWS::SES::ReceiptRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_receipt_rule_props_mixin = ses_mixins.CfnReceiptRulePropsMixin(ses_mixins.CfnReceiptRuleMixinProps(
            after="after",
            rule=ses_mixins.CfnReceiptRulePropsMixin.RuleProperty(
                actions=[ses_mixins.CfnReceiptRulePropsMixin.ActionProperty(
                    add_header_action=ses_mixins.CfnReceiptRulePropsMixin.AddHeaderActionProperty(
                        header_name="headerName",
                        header_value="headerValue"
                    ),
                    bounce_action=ses_mixins.CfnReceiptRulePropsMixin.BounceActionProperty(
                        message="message",
                        sender="sender",
                        smtp_reply_code="smtpReplyCode",
                        status_code="statusCode",
                        topic_arn="topicArn"
                    ),
                    connect_action=ses_mixins.CfnReceiptRulePropsMixin.ConnectActionProperty(
                        iam_role_arn="iamRoleArn",
                        instance_arn="instanceArn"
                    ),
                    lambda_action=ses_mixins.CfnReceiptRulePropsMixin.LambdaActionProperty(
                        function_arn="functionArn",
                        invocation_type="invocationType",
                        topic_arn="topicArn"
                    ),
                    s3_action=ses_mixins.CfnReceiptRulePropsMixin.S3ActionProperty(
                        bucket_name="bucketName",
                        iam_role_arn="iamRoleArn",
                        kms_key_arn="kmsKeyArn",
                        object_key_prefix="objectKeyPrefix",
                        topic_arn="topicArn"
                    ),
                    sns_action=ses_mixins.CfnReceiptRulePropsMixin.SNSActionProperty(
                        encoding="encoding",
                        topic_arn="topicArn"
                    ),
                    stop_action=ses_mixins.CfnReceiptRulePropsMixin.StopActionProperty(
                        scope="scope",
                        topic_arn="topicArn"
                    ),
                    workmail_action=ses_mixins.CfnReceiptRulePropsMixin.WorkmailActionProperty(
                        organization_arn="organizationArn",
                        topic_arn="topicArn"
                    )
                )],
                enabled=False,
                name="name",
                recipients=["recipients"],
                scan_enabled=False,
                tls_policy="tlsPolicy"
            ),
            rule_set_name="ruleSetName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReceiptRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::ReceiptRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe418f81d0daf101f0dcb619b9ad8d74cc3e8132a8de07591d81d98f14684dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__976d85d149722b729cf097db7e968411403df20fecd0e168e70eee7e4a3b048a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489b7e4176ff822e3c8c5fbd42bdae6df1582bd63bea23a02431d4c1fbae836f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReceiptRuleMixinProps:
        return typing.cast(CfnReceiptRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_header_action": "addHeaderAction",
            "bounce_action": "bounceAction",
            "connect_action": "connectAction",
            "lambda_action": "lambdaAction",
            "s3_action": "s3Action",
            "sns_action": "snsAction",
            "stop_action": "stopAction",
            "workmail_action": "workmailAction",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            add_header_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptRulePropsMixin.AddHeaderActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            bounce_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptRulePropsMixin.BounceActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            connect_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptRulePropsMixin.ConnectActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptRulePropsMixin.LambdaActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptRulePropsMixin.S3ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptRulePropsMixin.SNSActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stop_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptRulePropsMixin.StopActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            workmail_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptRulePropsMixin.WorkmailActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An action that Amazon SES can take when it receives an email on behalf of one or more email addresses or domains that you own.

            An instance of this data type can represent only one action.

            For information about setting up receipt rules, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-receipt-rules-console-walkthrough.html>`_ .

            :param add_header_action: Adds a header to the received email.
            :param bounce_action: Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).
            :param connect_action: The action that informs a traffic policy resource to either allow or block the email if it matches a condition in the policy statement.
            :param lambda_action: Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS.
            :param s3_action: Saves the received message to an Amazon Simple Storage Service (Amazon S3) bucket and, optionally, publishes a notification to Amazon SNS.
            :param sns_action: Publishes the email content within a notification to Amazon SNS.
            :param stop_action: Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS.
            :param workmail_action: Calls Amazon WorkMail and, optionally, publishes a notification to Amazon SNS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                action_property = ses_mixins.CfnReceiptRulePropsMixin.ActionProperty(
                    add_header_action=ses_mixins.CfnReceiptRulePropsMixin.AddHeaderActionProperty(
                        header_name="headerName",
                        header_value="headerValue"
                    ),
                    bounce_action=ses_mixins.CfnReceiptRulePropsMixin.BounceActionProperty(
                        message="message",
                        sender="sender",
                        smtp_reply_code="smtpReplyCode",
                        status_code="statusCode",
                        topic_arn="topicArn"
                    ),
                    connect_action=ses_mixins.CfnReceiptRulePropsMixin.ConnectActionProperty(
                        iam_role_arn="iamRoleArn",
                        instance_arn="instanceArn"
                    ),
                    lambda_action=ses_mixins.CfnReceiptRulePropsMixin.LambdaActionProperty(
                        function_arn="functionArn",
                        invocation_type="invocationType",
                        topic_arn="topicArn"
                    ),
                    s3_action=ses_mixins.CfnReceiptRulePropsMixin.S3ActionProperty(
                        bucket_name="bucketName",
                        iam_role_arn="iamRoleArn",
                        kms_key_arn="kmsKeyArn",
                        object_key_prefix="objectKeyPrefix",
                        topic_arn="topicArn"
                    ),
                    sns_action=ses_mixins.CfnReceiptRulePropsMixin.SNSActionProperty(
                        encoding="encoding",
                        topic_arn="topicArn"
                    ),
                    stop_action=ses_mixins.CfnReceiptRulePropsMixin.StopActionProperty(
                        scope="scope",
                        topic_arn="topicArn"
                    ),
                    workmail_action=ses_mixins.CfnReceiptRulePropsMixin.WorkmailActionProperty(
                        organization_arn="organizationArn",
                        topic_arn="topicArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eec1a0e0da76fa3808f5a70ab49e2b53dfed490f4de68e1937c95adb62b88817)
                check_type(argname="argument add_header_action", value=add_header_action, expected_type=type_hints["add_header_action"])
                check_type(argname="argument bounce_action", value=bounce_action, expected_type=type_hints["bounce_action"])
                check_type(argname="argument connect_action", value=connect_action, expected_type=type_hints["connect_action"])
                check_type(argname="argument lambda_action", value=lambda_action, expected_type=type_hints["lambda_action"])
                check_type(argname="argument s3_action", value=s3_action, expected_type=type_hints["s3_action"])
                check_type(argname="argument sns_action", value=sns_action, expected_type=type_hints["sns_action"])
                check_type(argname="argument stop_action", value=stop_action, expected_type=type_hints["stop_action"])
                check_type(argname="argument workmail_action", value=workmail_action, expected_type=type_hints["workmail_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_header_action is not None:
                self._values["add_header_action"] = add_header_action
            if bounce_action is not None:
                self._values["bounce_action"] = bounce_action
            if connect_action is not None:
                self._values["connect_action"] = connect_action
            if lambda_action is not None:
                self._values["lambda_action"] = lambda_action
            if s3_action is not None:
                self._values["s3_action"] = s3_action
            if sns_action is not None:
                self._values["sns_action"] = sns_action
            if stop_action is not None:
                self._values["stop_action"] = stop_action
            if workmail_action is not None:
                self._values["workmail_action"] = workmail_action

        @builtins.property
        def add_header_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.AddHeaderActionProperty"]]:
            '''Adds a header to the received email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-addheaderaction
            '''
            result = self._values.get("add_header_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.AddHeaderActionProperty"]], result)

        @builtins.property
        def bounce_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.BounceActionProperty"]]:
            '''Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-bounceaction
            '''
            result = self._values.get("bounce_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.BounceActionProperty"]], result)

        @builtins.property
        def connect_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.ConnectActionProperty"]]:
            '''The action that informs a traffic policy resource to either allow or block the email if it matches a condition in the policy statement.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-connectaction
            '''
            result = self._values.get("connect_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.ConnectActionProperty"]], result)

        @builtins.property
        def lambda_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.LambdaActionProperty"]]:
            '''Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-lambdaaction
            '''
            result = self._values.get("lambda_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.LambdaActionProperty"]], result)

        @builtins.property
        def s3_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.S3ActionProperty"]]:
            '''Saves the received message to an Amazon Simple Storage Service (Amazon S3) bucket and, optionally, publishes a notification to Amazon SNS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-s3action
            '''
            result = self._values.get("s3_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.S3ActionProperty"]], result)

        @builtins.property
        def sns_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.SNSActionProperty"]]:
            '''Publishes the email content within a notification to Amazon SNS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-snsaction
            '''
            result = self._values.get("sns_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.SNSActionProperty"]], result)

        @builtins.property
        def stop_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.StopActionProperty"]]:
            '''Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-stopaction
            '''
            result = self._values.get("stop_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.StopActionProperty"]], result)

        @builtins.property
        def workmail_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.WorkmailActionProperty"]]:
            '''Calls Amazon WorkMail and, optionally, publishes a notification to Amazon SNS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-workmailaction
            '''
            result = self._values.get("workmail_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.WorkmailActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin.AddHeaderActionProperty",
        jsii_struct_bases=[],
        name_mapping={"header_name": "headerName", "header_value": "headerValue"},
    )
    class AddHeaderActionProperty:
        def __init__(
            self,
            *,
            header_name: typing.Optional[builtins.str] = None,
            header_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action adds a header to the received email.

            For information about adding a header using a receipt rule, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-receipt-rules-console-walkthrough.html>`_ .

            :param header_name: The name of the header to add to the incoming message. The name must contain at least one character, and can contain up to 50 characters. It consists of alphanumeric ( ``a–z, A–Z, 0–9`` ) characters and dashes.
            :param header_value: The content to include in the header. This value can contain up to 2048 characters. It can't contain newline ( ``\\n`` ) or carriage return ( ``\\r`` ) characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                add_header_action_property = ses_mixins.CfnReceiptRulePropsMixin.AddHeaderActionProperty(
                    header_name="headerName",
                    header_value="headerValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__424ba99092f8d6450755f502d12b664c56e6460d027140062d33516e8af591f7)
                check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
                check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_name is not None:
                self._values["header_name"] = header_name
            if header_value is not None:
                self._values["header_value"] = header_value

        @builtins.property
        def header_name(self) -> typing.Optional[builtins.str]:
            '''The name of the header to add to the incoming message.

            The name must contain at least one character, and can contain up to 50 characters. It consists of alphanumeric ( ``a–z, A–Z, 0–9`` ) characters and dashes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html#cfn-ses-receiptrule-addheaderaction-headername
            '''
            result = self._values.get("header_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header_value(self) -> typing.Optional[builtins.str]:
            '''The content to include in the header.

            This value can contain up to 2048 characters. It can't contain newline ( ``\\n`` ) or carriage return ( ``\\r`` ) characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html#cfn-ses-receiptrule-addheaderaction-headervalue
            '''
            result = self._values.get("header_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddHeaderActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin.BounceActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "message": "message",
            "sender": "sender",
            "smtp_reply_code": "smtpReplyCode",
            "status_code": "statusCode",
            "topic_arn": "topicArn",
        },
    )
    class BounceActionProperty:
        def __init__(
            self,
            *,
            message: typing.Optional[builtins.str] = None,
            sender: typing.Optional[builtins.str] = None,
            smtp_reply_code: typing.Optional[builtins.str] = None,
            status_code: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            For information about sending a bounce message in response to a received email, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-bounce.html>`_ .

            :param message: Human-readable text to include in the bounce message.
            :param sender: The email address of the sender of the bounced email. This is the address from which the bounce message is sent.
            :param smtp_reply_code: The SMTP reply code, as defined by `RFC 5321 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5321>`_ .
            :param status_code: The SMTP enhanced status code, as defined by `RFC 3463 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc3463>`_ .
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the bounce action is taken. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                bounce_action_property = ses_mixins.CfnReceiptRulePropsMixin.BounceActionProperty(
                    message="message",
                    sender="sender",
                    smtp_reply_code="smtpReplyCode",
                    status_code="statusCode",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f7aad486946005452ea382d62c068db53cb8cd77efc0411a73bcc43b4be624c)
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                check_type(argname="argument sender", value=sender, expected_type=type_hints["sender"])
                check_type(argname="argument smtp_reply_code", value=smtp_reply_code, expected_type=type_hints["smtp_reply_code"])
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message is not None:
                self._values["message"] = message
            if sender is not None:
                self._values["sender"] = sender
            if smtp_reply_code is not None:
                self._values["smtp_reply_code"] = smtp_reply_code
            if status_code is not None:
                self._values["status_code"] = status_code
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''Human-readable text to include in the bounce message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sender(self) -> typing.Optional[builtins.str]:
            '''The email address of the sender of the bounced email.

            This is the address from which the bounce message is sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-sender
            '''
            result = self._values.get("sender")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def smtp_reply_code(self) -> typing.Optional[builtins.str]:
            '''The SMTP reply code, as defined by `RFC 5321 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5321>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-smtpreplycode
            '''
            result = self._values.get("smtp_reply_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_code(self) -> typing.Optional[builtins.str]:
            '''The SMTP enhanced status code, as defined by `RFC 3463 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc3463>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the bounce action is taken.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BounceActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin.ConnectActionProperty",
        jsii_struct_bases=[],
        name_mapping={"iam_role_arn": "iamRoleArn", "instance_arn": "instanceArn"},
    )
    class ConnectActionProperty:
        def __init__(
            self,
            *,
            iam_role_arn: typing.Optional[builtins.str] = None,
            instance_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action parses the received message and starts an email contact in Amazon Connect on your behalf.

            .. epigraph::

               When you receive emails, the maximum email size (including headers) is 40 MB. Additionally, emails may only have up to 10 attachments. Emails larger than 40 MB or with more than 10 attachments will be bounced.

            We recommend that you configure this action via Amazon Connect.

            :param iam_role_arn: The Amazon Resource Name (ARN) of the IAM role to be used by Amazon Simple Email Service while starting email contacts to the Amazon Connect instance. This role should have permission to invoke ``connect:StartEmailContact`` for the given Amazon Connect instance.
            :param instance_arn: The Amazon Resource Name (ARN) for the Amazon Connect instance that Amazon SES integrates with for starting email contacts. For more information about Amazon Connect instances, see the `Amazon Connect Administrator Guide <https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-instances.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-connectaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                connect_action_property = ses_mixins.CfnReceiptRulePropsMixin.ConnectActionProperty(
                    iam_role_arn="iamRoleArn",
                    instance_arn="instanceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a609b41e66c991897bef90d07392d4620392c21d08a54f6ff83b8c236c05c406)
                check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
                check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iam_role_arn is not None:
                self._values["iam_role_arn"] = iam_role_arn
            if instance_arn is not None:
                self._values["instance_arn"] = instance_arn

        @builtins.property
        def iam_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role to be used by Amazon Simple Email Service while starting email contacts to the Amazon Connect instance.

            This role should have permission to invoke ``connect:StartEmailContact`` for the given Amazon Connect instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-connectaction.html#cfn-ses-receiptrule-connectaction-iamrolearn
            '''
            result = self._values.get("iam_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the Amazon Connect instance that Amazon SES integrates with for starting email contacts.

            For more information about Amazon Connect instances, see the `Amazon Connect Administrator Guide <https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-instances.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-connectaction.html#cfn-ses-receiptrule-connectaction-instancearn
            '''
            result = self._values.get("instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin.LambdaActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "function_arn": "functionArn",
            "invocation_type": "invocationType",
            "topic_arn": "topicArn",
        },
    )
    class LambdaActionProperty:
        def __init__(
            self,
            *,
            function_arn: typing.Optional[builtins.str] = None,
            invocation_type: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action calls an AWS Lambda function and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            To enable Amazon SES to call your AWS Lambda function or to publish to an Amazon SNS topic of another account, Amazon SES must have permission to access those resources. For information about giving permissions, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-permissions.html>`_ .

            For information about using AWS Lambda actions in receipt rules, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-lambda.html>`_ .

            :param function_arn: The Amazon Resource Name (ARN) of the AWS Lambda function. An example of an AWS Lambda function ARN is ``arn:aws:lambda:us-west-2:account-id:function:MyFunction`` . For more information about AWS Lambda, see the `AWS Lambda Developer Guide <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>`_ .
            :param invocation_type: The invocation type of the AWS Lambda function. An invocation type of ``RequestResponse`` means that the execution of the function immediately results in a response, and a value of ``Event`` means that the function is invoked asynchronously. The default value is ``Event`` . For information about AWS Lambda invocation types, see the `AWS Lambda Developer Guide <https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html>`_ . .. epigraph:: There is a 30-second timeout on ``RequestResponse`` invocations. You should use ``Event`` invocation in most cases. Use ``RequestResponse`` only to make a mail flow decision, such as whether to stop the receipt rule or the receipt rule set.
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the Lambda action is executed. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                lambda_action_property = ses_mixins.CfnReceiptRulePropsMixin.LambdaActionProperty(
                    function_arn="functionArn",
                    invocation_type="invocationType",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be3632ae4fe479d5e95d874e843c04d6a3dace3ec50a03401ea7dcb046c298a7)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if function_arn is not None:
                self._values["function_arn"] = function_arn
            if invocation_type is not None:
                self._values["invocation_type"] = invocation_type
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def function_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Lambda function.

            An example of an AWS Lambda function ARN is ``arn:aws:lambda:us-west-2:account-id:function:MyFunction`` . For more information about AWS Lambda, see the `AWS Lambda Developer Guide <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-functionarn
            '''
            result = self._values.get("function_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def invocation_type(self) -> typing.Optional[builtins.str]:
            '''The invocation type of the AWS Lambda function.

            An invocation type of ``RequestResponse`` means that the execution of the function immediately results in a response, and a value of ``Event`` means that the function is invoked asynchronously. The default value is ``Event`` . For information about AWS Lambda invocation types, see the `AWS Lambda Developer Guide <https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html>`_ .
            .. epigraph::

               There is a 30-second timeout on ``RequestResponse`` invocations. You should use ``Event`` invocation in most cases. Use ``RequestResponse`` only to make a mail flow decision, such as whether to stop the receipt rule or the receipt rule set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-invocationtype
            '''
            result = self._values.get("invocation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the Lambda action is executed.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "enabled": "enabled",
            "name": "name",
            "recipients": "recipients",
            "scan_enabled": "scanEnabled",
            "tls_policy": "tlsPolicy",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReceiptRulePropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
            recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
            scan_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            tls_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Receipt rules enable you to specify which actions Amazon SES should take when it receives mail on behalf of one or more email addresses or domains that you own.

            Each receipt rule defines a set of email addresses or domains that it applies to. If the email addresses or domains match at least one recipient address of the message, Amazon SES executes all of the receipt rule's actions on the message.

            For information about setting up receipt rules, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-receipt-rules-console-walkthrough.html>`_ .

            :param actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule.
            :param enabled: If ``true`` , the receipt rule is active. The default value is ``false`` .
            :param name: The name of the receipt rule. The name must meet the following requirements:. - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), dashes (-), or periods (.). - Start and end with a letter or number. - Contain 64 characters or fewer.
            :param recipients: The recipient domains and email addresses that the receipt rule applies to. If this field is not specified, this rule matches all recipients on all verified domains.
            :param scan_enabled: If ``true`` , then messages that this receipt rule applies to are scanned for spam and viruses. The default value is ``false`` .
            :param tls_policy: Specifies whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). If this parameter is set to ``Require`` , Amazon SES bounces emails that are not received over TLS. The default is ``Optional`` . Valid Values: ``Require | Optional``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                rule_property = ses_mixins.CfnReceiptRulePropsMixin.RuleProperty(
                    actions=[ses_mixins.CfnReceiptRulePropsMixin.ActionProperty(
                        add_header_action=ses_mixins.CfnReceiptRulePropsMixin.AddHeaderActionProperty(
                            header_name="headerName",
                            header_value="headerValue"
                        ),
                        bounce_action=ses_mixins.CfnReceiptRulePropsMixin.BounceActionProperty(
                            message="message",
                            sender="sender",
                            smtp_reply_code="smtpReplyCode",
                            status_code="statusCode",
                            topic_arn="topicArn"
                        ),
                        connect_action=ses_mixins.CfnReceiptRulePropsMixin.ConnectActionProperty(
                            iam_role_arn="iamRoleArn",
                            instance_arn="instanceArn"
                        ),
                        lambda_action=ses_mixins.CfnReceiptRulePropsMixin.LambdaActionProperty(
                            function_arn="functionArn",
                            invocation_type="invocationType",
                            topic_arn="topicArn"
                        ),
                        s3_action=ses_mixins.CfnReceiptRulePropsMixin.S3ActionProperty(
                            bucket_name="bucketName",
                            iam_role_arn="iamRoleArn",
                            kms_key_arn="kmsKeyArn",
                            object_key_prefix="objectKeyPrefix",
                            topic_arn="topicArn"
                        ),
                        sns_action=ses_mixins.CfnReceiptRulePropsMixin.SNSActionProperty(
                            encoding="encoding",
                            topic_arn="topicArn"
                        ),
                        stop_action=ses_mixins.CfnReceiptRulePropsMixin.StopActionProperty(
                            scope="scope",
                            topic_arn="topicArn"
                        ),
                        workmail_action=ses_mixins.CfnReceiptRulePropsMixin.WorkmailActionProperty(
                            organization_arn="organizationArn",
                            topic_arn="topicArn"
                        )
                    )],
                    enabled=False,
                    name="name",
                    recipients=["recipients"],
                    scan_enabled=False,
                    tls_policy="tlsPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3da2e7b9e942269ad4a144e7cb18439b75b32c0d4862ebaa5333f9ab1a7d5ac6)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument recipients", value=recipients, expected_type=type_hints["recipients"])
                check_type(argname="argument scan_enabled", value=scan_enabled, expected_type=type_hints["scan_enabled"])
                check_type(argname="argument tls_policy", value=tls_policy, expected_type=type_hints["tls_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if enabled is not None:
                self._values["enabled"] = enabled
            if name is not None:
                self._values["name"] = name
            if recipients is not None:
                self._values["recipients"] = recipients
            if scan_enabled is not None:
                self._values["scan_enabled"] = scan_enabled
            if tls_policy is not None:
                self._values["tls_policy"] = tls_policy

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.ActionProperty"]]]]:
            '''An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReceiptRulePropsMixin.ActionProperty"]]]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If ``true`` , the receipt rule is active.

            The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the receipt rule. The name must meet the following requirements:.

            - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), dashes (-), or periods (.).
            - Start and end with a letter or number.
            - Contain 64 characters or fewer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The recipient domains and email addresses that the receipt rule applies to.

            If this field is not specified, this rule matches all recipients on all verified domains.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-recipients
            '''
            result = self._values.get("recipients")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def scan_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If ``true`` , then messages that this receipt rule applies to are scanned for spam and viruses.

            The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-scanenabled
            '''
            result = self._values.get("scan_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def tls_policy(self) -> typing.Optional[builtins.str]:
            '''Specifies whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS).

            If this parameter is set to ``Require`` , Amazon SES bounces emails that are not received over TLS. The default is ``Optional`` .

            Valid Values: ``Require | Optional``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-tlspolicy
            '''
            result = self._values.get("tls_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin.S3ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "iam_role_arn": "iamRoleArn",
            "kms_key_arn": "kmsKeyArn",
            "object_key_prefix": "objectKeyPrefix",
            "topic_arn": "topicArn",
        },
    )
    class S3ActionProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            iam_role_arn: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
            object_key_prefix: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action saves the received message to an Amazon Simple Storage Service (Amazon S3) bucket and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            To enable Amazon SES to write emails to your Amazon S3 bucket, use an AWS KMS key to encrypt your emails, or publish to an Amazon SNS topic of another account, Amazon SES must have permission to access those resources. For information about granting permissions, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-permissions.html>`_ .
            .. epigraph::

               When you save your emails to an Amazon S3 bucket, the maximum email size (including headers) is 30 MB. Emails larger than that bounces.

            For information about specifying Amazon S3 actions in receipt rules, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-s3.html>`_ .

            :param bucket_name: The name of the Amazon S3 bucket for incoming email.
            :param iam_role_arn: The ARN of the IAM role to be used by Amazon Simple Email Service while writing to the Amazon S3 bucket, optionally encrypting your mail via the provided customer managed key, and publishing to the Amazon SNS topic. This role should have access to the following APIs: - ``s3:PutObject`` , ``kms:Encrypt`` and ``kms:GenerateDataKey`` for the given Amazon S3 bucket. - ``kms:GenerateDataKey`` for the given AWS KMS customer managed key. - ``sns:Publish`` for the given Amazon SNS topic. .. epigraph:: If an IAM role ARN is provided, the role (and only the role) is used to access all the given resources (Amazon S3 bucket, AWS KMS customer managed key and Amazon SNS topic). Therefore, setting up individual resource access permissions is not required.
            :param kms_key_arn: The customer managed key that Amazon SES should use to encrypt your emails before saving them to the Amazon S3 bucket. You can use the AWS managed key or a customer managed key that you created in AWS KMS as follows: - To use the AWS managed key, provide an ARN in the form of ``arn:aws:kms:REGION:ACCOUNT-ID-WITHOUT-HYPHENS:alias/aws/ses`` . For example, if your AWS account ID is 123456789012 and you want to use the AWS managed key in the US West (Oregon) Region, the ARN of the AWS managed key would be ``arn:aws:kms:us-west-2:123456789012:alias/aws/ses`` . If you use the AWS managed key, you don't need to perform any extra steps to give Amazon SES permission to use the key. - To use a customer managed key that you created in AWS KMS, provide the ARN of the customer managed key and ensure that you add a statement to your key's policy to give Amazon SES permission to use it. For more information about giving permissions, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-permissions.html>`_ . For more information about key policies, see the `AWS KMS Developer Guide <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html>`_ . If you do not specify an AWS KMS key, Amazon SES does not encrypt your emails. .. epigraph:: Your mail is encrypted by Amazon SES using the Amazon S3 encryption client before the mail is submitted to Amazon S3 for storage. It is not encrypted using Amazon S3 server-side encryption. This means that you must use the Amazon S3 encryption client to decrypt the email after retrieving it from Amazon S3, as the service has no access to use your AWS KMS keys for decryption. This encryption client is currently available with the `AWS SDK for Java <https://docs.aws.amazon.com/sdk-for-java/>`_ and `AWS SDK for Ruby <https://docs.aws.amazon.com/sdk-for-ruby/>`_ only. For more information about client-side encryption using AWS KMS managed keys, see the `Amazon S3 Developer Guide <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html>`_ .
            :param object_key_prefix: The key prefix of the Amazon S3 bucket. The key prefix is similar to a directory name that enables you to store similar data under the same directory in a bucket.
            :param topic_arn: The ARN of the Amazon SNS topic to notify when the message is saved to the Amazon S3 bucket. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                s3_action_property = ses_mixins.CfnReceiptRulePropsMixin.S3ActionProperty(
                    bucket_name="bucketName",
                    iam_role_arn="iamRoleArn",
                    kms_key_arn="kmsKeyArn",
                    object_key_prefix="objectKeyPrefix",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2eaaef6768e4a3c1db52bdfb175f8b4f759bff6606b629a81dcb4f562bfda93d)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if iam_role_arn is not None:
                self._values["iam_role_arn"] = iam_role_arn
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if object_key_prefix is not None:
                self._values["object_key_prefix"] = object_key_prefix
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket for incoming email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iam_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role to be used by Amazon Simple Email Service while writing to the Amazon S3 bucket, optionally encrypting your mail via the provided customer managed key, and publishing to the Amazon SNS topic.

            This role should have access to the following APIs:

            - ``s3:PutObject`` , ``kms:Encrypt`` and ``kms:GenerateDataKey`` for the given Amazon S3 bucket.
            - ``kms:GenerateDataKey`` for the given AWS KMS customer managed key.
            - ``sns:Publish`` for the given Amazon SNS topic.

            .. epigraph::

               If an IAM role ARN is provided, the role (and only the role) is used to access all the given resources (Amazon S3 bucket, AWS KMS customer managed key and Amazon SNS topic). Therefore, setting up individual resource access permissions is not required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-iamrolearn
            '''
            result = self._values.get("iam_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The customer managed key that Amazon SES should use to encrypt your emails before saving them to the Amazon S3 bucket.

            You can use the AWS managed key or a customer managed key that you created in AWS KMS as follows:

            - To use the AWS managed key, provide an ARN in the form of ``arn:aws:kms:REGION:ACCOUNT-ID-WITHOUT-HYPHENS:alias/aws/ses`` . For example, if your AWS account ID is 123456789012 and you want to use the AWS managed key in the US West (Oregon) Region, the ARN of the AWS managed key would be ``arn:aws:kms:us-west-2:123456789012:alias/aws/ses`` . If you use the AWS managed key, you don't need to perform any extra steps to give Amazon SES permission to use the key.
            - To use a customer managed key that you created in AWS KMS, provide the ARN of the customer managed key and ensure that you add a statement to your key's policy to give Amazon SES permission to use it. For more information about giving permissions, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-permissions.html>`_ .

            For more information about key policies, see the `AWS KMS Developer Guide <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html>`_ . If you do not specify an AWS KMS key, Amazon SES does not encrypt your emails.
            .. epigraph::

               Your mail is encrypted by Amazon SES using the Amazon S3 encryption client before the mail is submitted to Amazon S3 for storage. It is not encrypted using Amazon S3 server-side encryption. This means that you must use the Amazon S3 encryption client to decrypt the email after retrieving it from Amazon S3, as the service has no access to use your AWS KMS keys for decryption. This encryption client is currently available with the `AWS SDK for Java <https://docs.aws.amazon.com/sdk-for-java/>`_ and `AWS SDK for Ruby <https://docs.aws.amazon.com/sdk-for-ruby/>`_ only. For more information about client-side encryption using AWS KMS managed keys, see the `Amazon S3 Developer Guide <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The key prefix of the Amazon S3 bucket.

            The key prefix is similar to a directory name that enables you to store similar data under the same directory in a bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-objectkeyprefix
            '''
            result = self._values.get("object_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon SNS topic to notify when the message is saved to the Amazon S3 bucket.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin.SNSActionProperty",
        jsii_struct_bases=[],
        name_mapping={"encoding": "encoding", "topic_arn": "topicArn"},
    )
    class SNSActionProperty:
        def __init__(
            self,
            *,
            encoding: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The action to publish the email content to an Amazon SNS topic.

            When executed, this action will send the email as a notification to the specified SNS topic.

            :param encoding: The encoding to use for the email within the Amazon SNS notification. The default value is ``UTF-8`` . Use ``BASE64`` if you need to preserve all special characters, especially when the original message uses a different encoding format.
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS Topic to which notification for the email received will be published.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                s_nSAction_property = ses_mixins.CfnReceiptRulePropsMixin.SNSActionProperty(
                    encoding="encoding",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ad7475e95cc219dd77715cbc061bdd1f2e4b43a0e8c3a5a27006686fa0f08ce)
                check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encoding is not None:
                self._values["encoding"] = encoding
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def encoding(self) -> typing.Optional[builtins.str]:
            '''The encoding to use for the email within the Amazon SNS notification.

            The default value is ``UTF-8`` . Use ``BASE64`` if you need to preserve all special characters, especially when the original message uses a different encoding format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html#cfn-ses-receiptrule-snsaction-encoding
            '''
            result = self._values.get("encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS Topic to which notification for the email received will be published.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html#cfn-ses-receiptrule-snsaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SNSActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin.StopActionProperty",
        jsii_struct_bases=[],
        name_mapping={"scope": "scope", "topic_arn": "topicArn"},
    )
    class StopActionProperty:
        def __init__(
            self,
            *,
            scope: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action terminates the evaluation of the receipt rule set and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            For information about setting a stop action in a receipt rule, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-stop.html>`_ .

            :param scope: The scope of the StopAction. The only acceptable value is ``RuleSet`` .
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the stop action is taken. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ Amazon SNS operation. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                stop_action_property = ses_mixins.CfnReceiptRulePropsMixin.StopActionProperty(
                    scope="scope",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6a0b6505c8eb3d498f6baca47e5baecd7c36b9aceea0432aebcd32330cf8ba6)
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if scope is not None:
                self._values["scope"] = scope
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The scope of the StopAction.

            The only acceptable value is ``RuleSet`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html#cfn-ses-receiptrule-stopaction-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the stop action is taken.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ Amazon SNS operation.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html#cfn-ses-receiptrule-stopaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StopActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRulePropsMixin.WorkmailActionProperty",
        jsii_struct_bases=[],
        name_mapping={"organization_arn": "organizationArn", "topic_arn": "topicArn"},
    )
    class WorkmailActionProperty:
        def __init__(
            self,
            *,
            organization_arn: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action calls Amazon WorkMail and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            It usually isn't necessary to set this up manually, because Amazon WorkMail adds the rule automatically during its setup procedure.

            For information using a receipt rule to call Amazon WorkMail, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-workmail.html>`_ .

            :param organization_arn: The Amazon Resource Name (ARN) of the Amazon WorkMail organization. Amazon WorkMail ARNs use the following format:. ``arn:aws:workmail:<region>:<awsAccountId>:organization/<workmailOrganizationId>`` You can find the ID of your organization by using the `ListOrganizations <https://docs.aws.amazon.com/workmail/latest/APIReference/API_ListOrganizations.html>`_ operation in Amazon WorkMail. Amazon WorkMail organization IDs begin with " ``m-`` ", followed by a string of alphanumeric characters. For information about Amazon WorkMail organizations, see the `Amazon WorkMail Administrator Guide <https://docs.aws.amazon.com/workmail/latest/adminguide/organizations_overview.html>`_ .
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the WorkMail action is called. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                workmail_action_property = ses_mixins.CfnReceiptRulePropsMixin.WorkmailActionProperty(
                    organization_arn="organizationArn",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40260240ca6189e89d6b0ca315c1059825bf87bd73748dae260cba54480ae9d7)
                check_type(argname="argument organization_arn", value=organization_arn, expected_type=type_hints["organization_arn"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if organization_arn is not None:
                self._values["organization_arn"] = organization_arn
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def organization_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon WorkMail organization. Amazon WorkMail ARNs use the following format:.

            ``arn:aws:workmail:<region>:<awsAccountId>:organization/<workmailOrganizationId>``

            You can find the ID of your organization by using the `ListOrganizations <https://docs.aws.amazon.com/workmail/latest/APIReference/API_ListOrganizations.html>`_ operation in Amazon WorkMail. Amazon WorkMail organization IDs begin with " ``m-`` ", followed by a string of alphanumeric characters.

            For information about Amazon WorkMail organizations, see the `Amazon WorkMail Administrator Guide <https://docs.aws.amazon.com/workmail/latest/adminguide/organizations_overview.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html#cfn-ses-receiptrule-workmailaction-organizationarn
            '''
            result = self._values.get("organization_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the WorkMail action is called.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html#cfn-ses-receiptrule-workmailaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkmailActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRuleSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={"rule_set_name": "ruleSetName"},
)
class CfnReceiptRuleSetMixinProps:
    def __init__(self, *, rule_set_name: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnReceiptRuleSetPropsMixin.

        :param rule_set_name: The name of the receipt rule set to make active. Setting this value to null disables all email receiving.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptruleset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_receipt_rule_set_mixin_props = ses_mixins.CfnReceiptRuleSetMixinProps(
                rule_set_name="ruleSetName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3d3f96af92457d71a726e569716136e34b4fbd6d42341538bb59988b548907)
            check_type(argname="argument rule_set_name", value=rule_set_name, expected_type=type_hints["rule_set_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rule_set_name is not None:
            self._values["rule_set_name"] = rule_set_name

    @builtins.property
    def rule_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the receipt rule set to make active.

        Setting this value to null disables all email receiving.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptruleset.html#cfn-ses-receiptruleset-rulesetname
        '''
        result = self._values.get("rule_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReceiptRuleSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReceiptRuleSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnReceiptRuleSetPropsMixin",
):
    '''Creates an empty receipt rule set.

    For information about setting up receipt rule sets, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-concepts.html#receiving-email-concepts-rules>`_ .

    You can execute this operation no more than once per second.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptruleset.html
    :cloudformationResource: AWS::SES::ReceiptRuleSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_receipt_rule_set_props_mixin = ses_mixins.CfnReceiptRuleSetPropsMixin(ses_mixins.CfnReceiptRuleSetMixinProps(
            rule_set_name="ruleSetName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReceiptRuleSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::ReceiptRuleSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137e73c5a6413e353b81d50aafbfed8357ccc5af15deedb9becb7d2f79f6ff51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbb136509015b9c778253115ace5db17690688d62f34f4f58e7c0b2dfa332659)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9afc9d0614e4a0ed1ef052c0ae5b222856d664ad934230426a1ecaa7daa7bc86)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReceiptRuleSetMixinProps:
        return typing.cast(CfnReceiptRuleSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={"template": "template"},
)
class CfnTemplateMixinProps:
    def __init__(
        self,
        *,
        template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.TemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTemplatePropsMixin.

        :param template: The content of the email, composed of a subject line and either an HTML part or a text-only part.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-template.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_template_mixin_props = ses_mixins.CfnTemplateMixinProps(
                template=ses_mixins.CfnTemplatePropsMixin.TemplateProperty(
                    html_part="htmlPart",
                    subject_part="subjectPart",
                    template_name="templateName",
                    text_part="textPart"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd577f976de68e4e03cade3504c4570da0859bc70e2105614c278efe11e2c7b)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.TemplateProperty"]]:
        '''The content of the email, composed of a subject line and either an HTML part or a text-only part.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-template.html#cfn-ses-template-template
        '''
        result = self._values.get("template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.TemplateProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnTemplatePropsMixin",
):
    '''Specifies an email template.

    Email templates enable you to send personalized email to one or more destinations in a single API operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-template.html
    :cloudformationResource: AWS::SES::Template
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_template_props_mixin = ses_mixins.CfnTemplatePropsMixin(ses_mixins.CfnTemplateMixinProps(
            template=ses_mixins.CfnTemplatePropsMixin.TemplateProperty(
                html_part="htmlPart",
                subject_part="subjectPart",
                template_name="templateName",
                text_part="textPart"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::Template``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c1c650f42996d74231317c8fb53be26262ba487f845679829a69f42ceb7e19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbf2af43c02c6048aaa895aa2a5b7630647f2f7dae46f36118831bd1a4d74ac6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a5b4c1196c09fce6bfaae6bcedb24f24c9bb1e11d79e2c6638412b5cd96555)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTemplateMixinProps:
        return typing.cast(CfnTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnTemplatePropsMixin.TemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "html_part": "htmlPart",
            "subject_part": "subjectPart",
            "template_name": "templateName",
            "text_part": "textPart",
        },
    )
    class TemplateProperty:
        def __init__(
            self,
            *,
            html_part: typing.Optional[builtins.str] = None,
            subject_part: typing.Optional[builtins.str] = None,
            template_name: typing.Optional[builtins.str] = None,
            text_part: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that defines the email template to use for an email message, and the values to use for any message variables in that template.

            An *email template* is a type of message template that contains content that you want to reuse in email messages that you send. You can specifiy the email template by providing the name or ARN of an *email template* previously saved in your Amazon SES account or by providing the full template content.

            :param html_part: The HTML body of the email.
            :param subject_part: The subject line of the email.
            :param template_name: The name of the template. You will refer to this name when you send email using the ``SendEmail`` or ``SendBulkEmail`` operations.
            :param text_part: The email body that is visible to recipients whose email clients do not display HTML content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                template_property = ses_mixins.CfnTemplatePropsMixin.TemplateProperty(
                    html_part="htmlPart",
                    subject_part="subjectPart",
                    template_name="templateName",
                    text_part="textPart"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__08780633b04f33dee932e57c05978c5c24b9fc9bcb0f7243ca5cf7f54f356f67)
                check_type(argname="argument html_part", value=html_part, expected_type=type_hints["html_part"])
                check_type(argname="argument subject_part", value=subject_part, expected_type=type_hints["subject_part"])
                check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
                check_type(argname="argument text_part", value=text_part, expected_type=type_hints["text_part"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if html_part is not None:
                self._values["html_part"] = html_part
            if subject_part is not None:
                self._values["subject_part"] = subject_part
            if template_name is not None:
                self._values["template_name"] = template_name
            if text_part is not None:
                self._values["text_part"] = text_part

        @builtins.property
        def html_part(self) -> typing.Optional[builtins.str]:
            '''The HTML body of the email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-htmlpart
            '''
            result = self._values.get("html_part")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subject_part(self) -> typing.Optional[builtins.str]:
            '''The subject line of the email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-subjectpart
            '''
            result = self._values.get("subject_part")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def template_name(self) -> typing.Optional[builtins.str]:
            '''The name of the template.

            You will refer to this name when you send email using the ``SendEmail`` or ``SendBulkEmail`` operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-templatename
            '''
            result = self._values.get("template_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_part(self) -> typing.Optional[builtins.str]:
            '''The email body that is visible to recipients whose email clients do not display HTML content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-textpart
            '''
            result = self._values.get("text_part")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnVdmAttributesMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_attributes": "dashboardAttributes",
        "guardian_attributes": "guardianAttributes",
    },
)
class CfnVdmAttributesMixinProps:
    def __init__(
        self,
        *,
        dashboard_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVdmAttributesPropsMixin.DashboardAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        guardian_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVdmAttributesPropsMixin.GuardianAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnVdmAttributesPropsMixin.

        :param dashboard_attributes: Specifies additional settings for your VDM configuration as applicable to the Dashboard.
        :param guardian_attributes: Specifies additional settings for your VDM configuration as applicable to the Guardian.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-vdmattributes.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
            
            cfn_vdm_attributes_mixin_props = ses_mixins.CfnVdmAttributesMixinProps(
                dashboard_attributes=ses_mixins.CfnVdmAttributesPropsMixin.DashboardAttributesProperty(
                    engagement_metrics="engagementMetrics"
                ),
                guardian_attributes=ses_mixins.CfnVdmAttributesPropsMixin.GuardianAttributesProperty(
                    optimized_shared_delivery="optimizedSharedDelivery"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b244a8c6cfa7f433c8d96217607ec0d6749edea792ce0ac9a8f6e50808e62ca)
            check_type(argname="argument dashboard_attributes", value=dashboard_attributes, expected_type=type_hints["dashboard_attributes"])
            check_type(argname="argument guardian_attributes", value=guardian_attributes, expected_type=type_hints["guardian_attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dashboard_attributes is not None:
            self._values["dashboard_attributes"] = dashboard_attributes
        if guardian_attributes is not None:
            self._values["guardian_attributes"] = guardian_attributes

    @builtins.property
    def dashboard_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVdmAttributesPropsMixin.DashboardAttributesProperty"]]:
        '''Specifies additional settings for your VDM configuration as applicable to the Dashboard.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-vdmattributes.html#cfn-ses-vdmattributes-dashboardattributes
        '''
        result = self._values.get("dashboard_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVdmAttributesPropsMixin.DashboardAttributesProperty"]], result)

    @builtins.property
    def guardian_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVdmAttributesPropsMixin.GuardianAttributesProperty"]]:
        '''Specifies additional settings for your VDM configuration as applicable to the Guardian.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-vdmattributes.html#cfn-ses-vdmattributes-guardianattributes
        '''
        result = self._values.get("guardian_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVdmAttributesPropsMixin.GuardianAttributesProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVdmAttributesMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVdmAttributesPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnVdmAttributesPropsMixin",
):
    '''The Virtual Deliverability Manager (VDM) attributes that apply to your Amazon SES account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-vdmattributes.html
    :cloudformationResource: AWS::SES::VdmAttributes
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
        
        cfn_vdm_attributes_props_mixin = ses_mixins.CfnVdmAttributesPropsMixin(ses_mixins.CfnVdmAttributesMixinProps(
            dashboard_attributes=ses_mixins.CfnVdmAttributesPropsMixin.DashboardAttributesProperty(
                engagement_metrics="engagementMetrics"
            ),
            guardian_attributes=ses_mixins.CfnVdmAttributesPropsMixin.GuardianAttributesProperty(
                optimized_shared_delivery="optimizedSharedDelivery"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVdmAttributesMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SES::VdmAttributes``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e785de7a555cddaa007095dfce3edc9d05aa5578132bb7d000ee48ed908367)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21c4ef5beaef00946f201360438f66d6dbbbf1c0ecf9253112d540d5e0729b3d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e2e4a0735639afaf7f90e2fdfb832e4fd8024b05a5ec13c888bdda2e527191)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVdmAttributesMixinProps:
        return typing.cast(CfnVdmAttributesMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnVdmAttributesPropsMixin.DashboardAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"engagement_metrics": "engagementMetrics"},
    )
    class DashboardAttributesProperty:
        def __init__(
            self,
            *,
            engagement_metrics: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing additional settings for your VDM configuration as applicable to the Dashboard.

            :param engagement_metrics: Specifies the status of your VDM engagement metrics collection. Can be one of the following:. - ``ENABLED`` – Amazon SES enables engagement metrics for your account. - ``DISABLED`` – Amazon SES disables engagement metrics for your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-vdmattributes-dashboardattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                dashboard_attributes_property = ses_mixins.CfnVdmAttributesPropsMixin.DashboardAttributesProperty(
                    engagement_metrics="engagementMetrics"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a7128442bc1a82a39ad83408c6c677edcea6c32852b2baf176b2c8f2fbb16908)
                check_type(argname="argument engagement_metrics", value=engagement_metrics, expected_type=type_hints["engagement_metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if engagement_metrics is not None:
                self._values["engagement_metrics"] = engagement_metrics

        @builtins.property
        def engagement_metrics(self) -> typing.Optional[builtins.str]:
            '''Specifies the status of your VDM engagement metrics collection. Can be one of the following:.

            - ``ENABLED`` – Amazon SES enables engagement metrics for your account.
            - ``DISABLED`` – Amazon SES disables engagement metrics for your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-vdmattributes-dashboardattributes.html#cfn-ses-vdmattributes-dashboardattributes-engagementmetrics
            '''
            result = self._values.get("engagement_metrics")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashboardAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ses.mixins.CfnVdmAttributesPropsMixin.GuardianAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"optimized_shared_delivery": "optimizedSharedDelivery"},
    )
    class GuardianAttributesProperty:
        def __init__(
            self,
            *,
            optimized_shared_delivery: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing additional settings for your VDM configuration as applicable to the Guardian.

            :param optimized_shared_delivery: Specifies the status of your VDM optimized shared delivery. Can be one of the following:. - ``ENABLED`` – Amazon SES enables optimized shared delivery for your account. - ``DISABLED`` – Amazon SES disables optimized shared delivery for your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-vdmattributes-guardianattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ses import mixins as ses_mixins
                
                guardian_attributes_property = ses_mixins.CfnVdmAttributesPropsMixin.GuardianAttributesProperty(
                    optimized_shared_delivery="optimizedSharedDelivery"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f5fe979dbe901cea5c050e199f9354a27f1558109898fe581f58bf1771446bce)
                check_type(argname="argument optimized_shared_delivery", value=optimized_shared_delivery, expected_type=type_hints["optimized_shared_delivery"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if optimized_shared_delivery is not None:
                self._values["optimized_shared_delivery"] = optimized_shared_delivery

        @builtins.property
        def optimized_shared_delivery(self) -> typing.Optional[builtins.str]:
            '''Specifies the status of your VDM optimized shared delivery. Can be one of the following:.

            - ``ENABLED`` – Amazon SES enables optimized shared delivery for your account.
            - ``DISABLED`` – Amazon SES disables optimized shared delivery for your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-vdmattributes-guardianattributes.html#cfn-ses-vdmattributes-guardianattributes-optimizedshareddelivery
            '''
            result = self._values.get("optimized_shared_delivery")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardianAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnConfigurationSetEventDestinationMixinProps",
    "CfnConfigurationSetEventDestinationPropsMixin",
    "CfnConfigurationSetMixinProps",
    "CfnConfigurationSetPropsMixin",
    "CfnContactListMixinProps",
    "CfnContactListPropsMixin",
    "CfnDedicatedIpPoolMixinProps",
    "CfnDedicatedIpPoolPropsMixin",
    "CfnEmailIdentityMixinProps",
    "CfnEmailIdentityPropsMixin",
    "CfnMailManagerAddonInstanceMixinProps",
    "CfnMailManagerAddonInstancePropsMixin",
    "CfnMailManagerAddonSubscriptionMixinProps",
    "CfnMailManagerAddonSubscriptionPropsMixin",
    "CfnMailManagerAddressListMixinProps",
    "CfnMailManagerAddressListPropsMixin",
    "CfnMailManagerArchiveMixinProps",
    "CfnMailManagerArchivePropsMixin",
    "CfnMailManagerIngressPointApplicationLogs",
    "CfnMailManagerIngressPointLogsMixin",
    "CfnMailManagerIngressPointMixinProps",
    "CfnMailManagerIngressPointPropsMixin",
    "CfnMailManagerIngressPointTrafficPolicyDebugLogs",
    "CfnMailManagerRelayMixinProps",
    "CfnMailManagerRelayPropsMixin",
    "CfnMailManagerRuleSetApplicationLogs",
    "CfnMailManagerRuleSetLogsMixin",
    "CfnMailManagerRuleSetMixinProps",
    "CfnMailManagerRuleSetPropsMixin",
    "CfnMailManagerTrafficPolicyMixinProps",
    "CfnMailManagerTrafficPolicyPropsMixin",
    "CfnMultiRegionEndpointMixinProps",
    "CfnMultiRegionEndpointPropsMixin",
    "CfnReceiptFilterMixinProps",
    "CfnReceiptFilterPropsMixin",
    "CfnReceiptRuleMixinProps",
    "CfnReceiptRulePropsMixin",
    "CfnReceiptRuleSetMixinProps",
    "CfnReceiptRuleSetPropsMixin",
    "CfnTemplateMixinProps",
    "CfnTemplatePropsMixin",
    "CfnVdmAttributesMixinProps",
    "CfnVdmAttributesPropsMixin",
]

publication.publish()

def _typecheckingstub__b6e27e225a3b2cd33099995b321b2376f94e3c40ed3e856d4e9825192a4e445e(
    *,
    configuration_set_name: typing.Optional[builtins.str] = None,
    event_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetEventDestinationPropsMixin.EventDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cff2f522e543bfbe6b36e5de1e7b022956fe4bc19f279eacbe6d77c679a14b2(
    props: typing.Union[CfnConfigurationSetEventDestinationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0224b8ca9b4ad8bb8979bc81cdaae7f528cb9c713ce20a171387807d2be68c1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198d7be1100c0ae85086623f125dd8a4405a5b66918d2d3a4d9094255fbbcb3e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278c7203c8277b28601e3ab834f7e607e97ee4fba0a30d0b35e67a563bb79861(
    *,
    dimension_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetEventDestinationPropsMixin.DimensionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ee73240cfe3db024238cac7961a819c7a8e4a7eeaec76a0d9a933fd5da0a58(
    *,
    default_dimension_value: typing.Optional[builtins.str] = None,
    dimension_name: typing.Optional[builtins.str] = None,
    dimension_value_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ad668f98df765e5eea436e0d2380c9720d6432e00117a7f8e118ec1f07f098(
    *,
    event_bus_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fb086fb4c28ea2aea987e2fb8953f5adeffbf1b141b35d5c23b3026cc895ed(
    *,
    cloud_watch_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetEventDestinationPropsMixin.CloudWatchDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    event_bridge_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetEventDestinationPropsMixin.EventBridgeDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_firehose_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetEventDestinationPropsMixin.KinesisFirehoseDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    matching_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    sns_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetEventDestinationPropsMixin.SnsDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0498dc4f87c224b8a16cc6b6137a482e12ed88848acae5c964ea9a89e3b9318(
    *,
    delivery_stream_arn: typing.Optional[builtins.str] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b318c3f2bdc1dc9b533ead761e35a46873300407a0efa18349c5388adf0e9f0(
    *,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfe5f4131c768a95350383a6faed15f1a8d5fba9be2a0a5f7d9ea40cb6d246d(
    *,
    delivery_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.DeliveryOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    reputation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.ReputationOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sending_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.SendingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    suppression_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.SuppressionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tracking_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.TrackingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vdm_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.VdmOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0da0fa237490c518232b5713153dd3565d3a1683274dd231d4ab676c93a823(
    props: typing.Union[CfnConfigurationSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d97332fe975642265c6d6601eccf5f863a6befac2953235a24d23794a9f6629(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b915e344d1c6e5f975472fc35ea3c5b6a3729515de716cef74424929b9842f95(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a399aa1957e9a9458169527d7b871087041bfa1e9afae18fabc150e9f6d5b183(
    *,
    engagement_metrics: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c964ff9625c41ecde6e6f95fafb5c7edaed767ec9843a21c015eee83f96ab1(
    *,
    max_delivery_seconds: typing.Optional[jsii.Number] = None,
    sending_pool_name: typing.Optional[builtins.str] = None,
    tls_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393285cb084b941b0dc5f69c3333db8ecfc65c5ac992d463f4b1db64e074ecb3(
    *,
    optimized_shared_delivery: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c52f046a0e97726bc814822ba1bae83c18b99e016bd937d30481641c2ac4eb(
    *,
    reputation_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b9b1a7882721560036414aa16e92da29911e13e7ed11dca4057f43fb8db5fd(
    *,
    sending_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b29add32d7cb5588d64c58feeacf5d61806c1b8ffef4938ad84ba39964c642(
    *,
    suppressed_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1126cfc00387531c4390aa17715d5da33c2b4a86fdb358e9a1a91ab4a806e9(
    *,
    custom_redirect_domain: typing.Optional[builtins.str] = None,
    https_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5db758467ad6757257bb7ccaa53d945afb5884b49db08f78de05238a9205d29(
    *,
    dashboard_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.DashboardOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    guardian_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.GuardianOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e2f3268dffd898f8884ad57c24a0c710bb7df0f461194cb92d2d8ce0b975ae(
    *,
    contact_list_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    topics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContactListPropsMixin.TopicProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8a409b460930a63cf945198a7c5531cc685bde4cc81f167d4d788d491229ec(
    props: typing.Union[CfnContactListMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc91b412eb5cb3c677190bf068705a6431f29fda44c50a4a18e1d6d3a86081c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f083c67507749a24799113e49b3b349c5725caa5256fc80b12a94670262828(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b782a6ca6957118c69dc3d464e4ce72cd607cb05c141a525ee153cca66d1e9f(
    *,
    default_subscription_status: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    topic_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ec841c109b7a5ba1655ddc48d1093c0a167f2c508fe85df2178ef14d672eef(
    *,
    pool_name: typing.Optional[builtins.str] = None,
    scaling_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd0755e5a38cd06e1f4164b92b97f58ef092f8433e92ccc5abdfea065b02b7c(
    props: typing.Union[CfnDedicatedIpPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa873bd70332a6f50787ed270b709a9809c073a8aa00ca64b351197d9d231df6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b7b9b33c2fe521a279f206ff5c1df9a7218c448c2d8689906fe4ccfe39efca(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80baf74598b411a412c862527a56d9ed550a26c16dac281e18f52f928421616(
    *,
    configuration_set_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEmailIdentityPropsMixin.ConfigurationSetAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dkim_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEmailIdentityPropsMixin.DkimAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dkim_signing_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEmailIdentityPropsMixin.DkimSigningAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    email_identity: typing.Optional[builtins.str] = None,
    feedback_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEmailIdentityPropsMixin.FeedbackAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mail_from_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEmailIdentityPropsMixin.MailFromAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f9d5c0b190a2a20282bbee89d907848706043ffb9360d65225b6bb3f9af113(
    props: typing.Union[CfnEmailIdentityMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35123219a3fec6d5b641e0e2050a7d0bd007032bdeffc1b28d4e53e169d094c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14d3b59a92a2885d6631b375ec1fe30425d732d23697dbe4196bd34fa57a534(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4daf03e8aea164f4d7b9e33291fe55c1453b4f148276092140b53cb856875545(
    *,
    configuration_set_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea54957e5cfa58e9513fa97116d093a30e2953c88c507149365e83d35b8b019(
    *,
    signing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6544bc4d4099a8b30dc8af2c8d9022d88ac50ef8f8b51e5c75a2190e095d3b67(
    *,
    domain_signing_private_key: typing.Optional[builtins.str] = None,
    domain_signing_selector: typing.Optional[builtins.str] = None,
    next_signing_key_length: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f23ec482368055e2d836776cf885e9a83fb56688275f54905dc5705e68793a(
    *,
    email_forwarding_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78993d12b65a26772c6e5898e08a7fd560e1e2d1b5d5993a41efaaffd00af643(
    *,
    behavior_on_mx_failure: typing.Optional[builtins.str] = None,
    mail_from_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129bdeef175fb86109b065004ddc627392c2cf1e0a472746c17e0186c42d4e94(
    *,
    addon_subscription_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256e5b34474c400c053d9b33586852010984d80e992bae780184cb607c5d442d(
    props: typing.Union[CfnMailManagerAddonInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26734697e9e95331bb6367f4fab86b9446fa61dfcef318255247c848f8d5d639(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6312ae4fc076deb9baffeeffc0edc4badd0a3384c30a86d2fd01e22265caac(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cba6ab1468134e4f1a4c4d220074c84afafc7d9dd39269f9e067cc77b48ba9(
    *,
    addon_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c5baee62a572b692f772971d7e2bf864dd1414ed505dc6109622e9ed07f63b(
    props: typing.Union[CfnMailManagerAddonSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cede7c0138c28df3dd937162127b6460d2e345b108cc411df96597d6381ca90(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2db6e74506d7f5d61892d5f8418a4a76128318d59a10b224683fbd6824987d2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf608eaf78616f65482735ae0e5b1c5554a95502a5b70389828eafff1f1241e(
    *,
    address_list_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23f11e552915a4db53622722b03190e687fbb1e17bd0a5d2f0e8c50c3a15de7(
    props: typing.Union[CfnMailManagerAddressListMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3f0fe3c4dfd6de611e8084b29281ca9618f4542ea306ffc6d48d14107fb618(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9664679023f727c7fca0089bc1359fe65e7246c2bf7976a54d14fb73125dac9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdb34781a0afa1e6778f7e1d11f662b14684bb3de8468db0492b73223d26e75(
    *,
    archive_name: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    retention: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerArchivePropsMixin.ArchiveRetentionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b01055708c59f220ffafb83a5711195f0fd4ecfc745df2c286c0a721ac6deb(
    props: typing.Union[CfnMailManagerArchiveMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66cb83c9fdefe719b4d20295ce777957a0de242ddc0318db06ff14669285b95(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c45b6d712b67305f816e34e1f746126b9ecc205db24b2b5b905bcfa9c2c2d8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab61f52fcb2edf32bf747cfa0f8fb3ed5a4d2d421672d16ed27c7b95edcedef7(
    *,
    retention_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78aa685beb92a7b16017fb26939ae5b16b5ecfb43ca09b94c50a38d91229db2(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa0f4958446455a53f3f095141d0e11ca8344caffadba14d487a55eb75ff9e7(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8db046685f3ebbea9d865cd39e0082220cf76e7802b29f6dbf9c5405dff4520(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a6fcbb34a2c10891de86d0385859a8bebbf3ae97fb87a3e3f216648008b8172(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e615252dbc0f8508c0d606c357357d1513e80be8a063576eb523aa4ae5dae30(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf0481f80d967c4bc56a19e0dc7ea6ea6817835d7d2d767e38be69d94da197b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dbd94d5dd9e97bf382a5ccd9f09a4c5bb820797e9b7aef16dd6a7188a0a4980(
    *,
    ingress_point_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerIngressPointPropsMixin.IngressPointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ingress_point_name: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerIngressPointPropsMixin.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_set_id: typing.Optional[builtins.str] = None,
    status_to_update: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    traffic_policy_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d185df3c4a480bdc61864cc8f86ce2d828769529a55949ca23cec1cc93531566(
    props: typing.Union[CfnMailManagerIngressPointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfaa7fd203d0826c4b5968c9c26bbdd733b6d8ab603ec8ddd0a656b3146e053(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa74a250225fc01872702d3e4e97c86645187d5afb0a6430bb1c927c54a0e1d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f558beef22f9d75a1f17398f1bf91879b351e08b7ba6dfd6022d1f8f79b910f1(
    *,
    secret_arn: typing.Optional[builtins.str] = None,
    smtp_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd61acdba018c44201e64acd8650e767d22fd36b3ca474f41e1570573d49aefb(
    *,
    private_network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerIngressPointPropsMixin.PrivateNetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    public_network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerIngressPointPropsMixin.PublicNetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75750eeb900636d7fbdb780bf46dea69eeaba1e3b7b151f0ec87b973f9d958f(
    *,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2a8a9a2a1176155d2f90735a160b39b4b871111305b79016aaa05e1d8574a3(
    *,
    ip_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bddc7a91c1124e7c6727457873214e0da3206362918bf4d622f05be6a9891c2(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37c1531e36b25221fe58b18d015ca0bae514fb9b39a59729275d5dca6bd3fc8(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2380c9270fbf6e609973d7bf68619def6423c4c9e5e3aaf376cad71f703a8b73(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40548dccf99429568349c7532fcea9258b0955f1fa46cfac45aee25e8bddf6c(
    *,
    authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRelayPropsMixin.RelayAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    relay_name: typing.Optional[builtins.str] = None,
    server_name: typing.Optional[builtins.str] = None,
    server_port: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa721654e021d803b6653b3b96ec4dfa39df3f8c0e7ba005b021e31b980c4ce(
    props: typing.Union[CfnMailManagerRelayMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3aed66003adc78a6b01d59d872135f6ca58b3fbf7fdfaed85a205cbe360099(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd115989e40a18c4cba1d1fc0a7fefc6485a9d3ebb991a4e293c15cedc25f947(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda8cf6aaa3b149a03f696f1ae6ee59802b573f249005654ad8455ca74799da5(
    *,
    no_authentication: typing.Any = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507ee61d1f659b529ea98b45ec90f54fcb911b533196b77ed51f8b7061dad2ff(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af63b89dde5af81422232cbe9a7491b18e2492110916181a86e590eda27a2c8e(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba42cd9c38a01c1c2755d72c555181b7f11e0b7e3edaa14e2f279ef694945bcd(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff89b8f63f89d085b1abcb636f0902e76e4098e335c876b71c0d193438537b8(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b38d36ae58c8b66349ef0f4827f7625ee95642391d3bfa544124c373f987ba(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4aa4944bf1b27534b2a4ee50aa909d323569ee2296cdb959148a34f76bfa9c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4d5dff7d48ff49f0f2296fc46693cee1aced720a9d5f0fafa031c8b7dafc20(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    rule_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450858f974a3371e31d62a900dadfd4dd2a0194f3bfa41e243fbd655131f00c4(
    props: typing.Union[CfnMailManagerRuleSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c61c9ad02c983f488c6ecdca81a74af3073fe34a2f318a870197aa12b5ddc3d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1753e267f41feb506b2b1f5c86c72e147157c7c47ee006500879875adf751a60(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862959ab5d09a96a5c91f70589bdbdf72428f667b97ce246c83a45b6cee0ba2a(
    *,
    header_name: typing.Optional[builtins.str] = None,
    header_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a1ca7fc3625765cae1781d58b109a6e2c94d4a3d1f44ff22cd015b62f4e3f6(
    *,
    analyzer: typing.Optional[builtins.str] = None,
    result_field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f046815fa0b8cb179e2396dcc8e40f1f6a762cb3e05d916d106bd9e606e92b9(
    *,
    action_failure_policy: typing.Optional[builtins.str] = None,
    target_archive: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8a93be45f61f8dae7d5f41a757ddd855dc80396eff6b7e2ef477a758185a98(
    *,
    action_failure_policy: typing.Optional[builtins.str] = None,
    mailbox_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963e0e8940deb2ada0b1a1bc81c80b21feca95d47873f94710d3871bf285023f(
    *,
    action_failure_policy: typing.Optional[builtins.str] = None,
    application_id: typing.Optional[builtins.str] = None,
    index_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83d5c547195eb09e689202535fba0c5635c06f3a18040b884d45b01025caa78(
    *,
    action_failure_policy: typing.Optional[builtins.str] = None,
    mail_from: typing.Optional[builtins.str] = None,
    relay: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b0fe452db1acf25aced5d8fdea528b6f137ffee14b0d4e11a0b24262bf531b(
    *,
    replace_with: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9b570285bb8d7f4f8d34e5b6de8cc486cb8d5bd5bce047e716877adcc9f468(
    *,
    add_header: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.AddHeaderActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    archive: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.ArchiveActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deliver_to_mailbox: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.DeliverToMailboxActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deliver_to_q_business: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.DeliverToQBusinessActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    drop: typing.Any = None,
    publish_to_sns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.SnsActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    relay: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RelayActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    replace_recipient: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.ReplaceRecipientActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    send: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.SendActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    write_to_s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.S3ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d83a5201ffedb02f734622b40303dcb2ef162e224de56e7a9d07a9c97171eb(
    *,
    evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleBooleanToEvaluateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fc31108e22582a8ea4be55f27f901d5c01f586e57cc4d34cb546941508d9e3(
    *,
    analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.AnalysisProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    attribute: typing.Optional[builtins.str] = None,
    is_in_address_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleIsInAddressListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6196b22c832d4b0e6d02afb6c57386231a9d82e7cdbedd1ac5032d7ea80ee3ed(
    *,
    boolean_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleBooleanExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dmarc_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleDmarcExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleIpExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    number_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleNumberExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    string_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleStringExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    verdict_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleVerdictExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89f78f3397616c90b21b1c5fb29d1790b71f1b95ad843a7d2f9c8ee751cfeb9(
    *,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872076428b139116c030050c49831f6feed29663b923e88213e51114d2965a99(
    *,
    evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleIpToEvaluateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6f81bcaa74bebfd4b7441514d71014b15f308eaf5116b906af8811a446dcb1(
    *,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545d98a332fa5b8a7fb9621df9dd39fdef72d0fb7c72c9bdbba6398537bb2a33(
    *,
    address_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63263a9c28c9cdee511c3fbb1b9d64ca53c15a4676db6fa721ae7beb328b0943(
    *,
    evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleNumberToEvaluateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4963e97053c5d6958992092714899b87cb3642cfdec56f02cdc7ae6f8c6697e(
    *,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f16092d1166c386a42ccd75df5e672a486ab88f7f8dfaa924d7a28335f5c9db(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    unless: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3648af57425d2a875f88cd89fcd68b9476fc25cf70e99df55c9e37ba81e7891a(
    *,
    evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleStringToEvaluateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2ef0323caed6ea0980d16efb19813ced51d4829bd99cd462bc496c98e5456f(
    *,
    analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.AnalysisProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    attribute: typing.Optional[builtins.str] = None,
    mime_header_attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7150924ac60453219f032d26681626a948cc5127327961637188659b0a7ee7(
    *,
    evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.RuleVerdictToEvaluateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fee130870cc83564b2db3d84012be4e685c71f7aa7db1249d091c36cb5deb7c(
    *,
    analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerRuleSetPropsMixin.AnalysisProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566ed051d8c4bdc8d51cf143299e4298e508390e789158e7800a1cf56de74dbb(
    *,
    action_failure_policy: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_prefix: typing.Optional[builtins.str] = None,
    s3_sse_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb66d3f3bbdede6507d521066f0177ac8b0ad0b96649f7cc00fb6e207b4b7c5e(
    *,
    action_failure_policy: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8405def5b39a4a8f44725e4f71852182744c6019c9119008e9f97be26edc8ad(
    *,
    action_failure_policy: typing.Optional[builtins.str] = None,
    encoding: typing.Optional[builtins.str] = None,
    payload_type: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a29a92deededc5a374f9f94f7bd1d2927294f626953a9c6e973314547f65c1(
    *,
    default_action: typing.Optional[builtins.str] = None,
    max_message_size_bytes: typing.Optional[jsii.Number] = None,
    policy_statements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.PolicyStatementProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    traffic_policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7144801b7263083cc91daab69d392dbcce67a594a52b88c575e6abcc3f366c88(
    props: typing.Union[CfnMailManagerTrafficPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c70b8a287dfdbe919da6888b34512911847d52a06c26b5737451abd662d6eb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191fdaa9bd8c9fbcb9d9306f9e51ca5ce497f091ad90f222686ac9499e1899c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909d5b19725b4cb02f91cc84e9827a9daff4d6748b933ee8d55b007cfdff1072(
    *,
    analyzer: typing.Optional[builtins.str] = None,
    result_field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e07e97e2c648d4b817d03c886b97568dac9bf0f118a6a02ee0e6b0c06a31931(
    *,
    evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanToEvaluateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490c5d658fb2c59c899fe02184faa1ceb6794a1f7968d7b80b901161bfbdde20(
    *,
    analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_in_address_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressIsInAddressListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3060689fec824b1d217f6e8faea8d0bb5463bfb8874f1aefafcd6f0ea645b14f(
    *,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144d6b4e7d5ea283bf003e6e73645b24f8af64965f8755362ab326bcf0e27877(
    *,
    evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressIpToEvaluateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a2472fab341e68074edffbe107dc6469b9317b1d4a75d3dcfa0bca43bbee94(
    *,
    evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ToEvaluateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73396557b1140fefa6e5b21f9ab88c694765ea3bbf48535ece4bd1a97ecd07ff(
    *,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8509c5b3b7c1443279c6b3fdfdc88da2fb76b03e93319215c5f6a350c7e50a19(
    *,
    address_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e9d061de221d1c76af47f9e5777328c398883921088737ef53b9dadb122ae4(
    *,
    evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressStringToEvaluateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d82b326396745b75e4567d882ffaaef1591789b156f48ef3afd53b2b9e461cb(
    *,
    analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressAnalysisProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be58f6d26ed1e605e6d8a01233985357f18fdb6444e6ee6ce5883167a021a1c7(
    *,
    evaluate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolToEvaluateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d28710a38ede59efe9470a83c081684d7d514d22f4db4cb7b67db3a60ed150(
    *,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6170c880171e0b933fedafc2167034d4bc58a0945c5212f47b80d9134406dd39(
    *,
    boolean_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressBooleanExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressIpv4ExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ipv6_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressIpv6ExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    string_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressStringExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.IngressTlsProtocolExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0e45eee896bbd32127418a3e22672d9ed990736e5cc7f4677b032f98582c95(
    *,
    action: typing.Optional[builtins.str] = None,
    conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMailManagerTrafficPolicyPropsMixin.PolicyConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a871fd20cc36ff088be673b1b8639fe0fe2206fbb7a6b9115c1290f8c2c7d46f(
    *,
    details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMultiRegionEndpointPropsMixin.DetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ee209e6a269a478cbcdf71c07588912ef31a432a6e6366f07c6d9f84aa8220(
    props: typing.Union[CfnMultiRegionEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e85092416e820668311375643cedbc1b08567f9447733c3296c884e5f111b9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037bbad86283faa565f54c09dd4f928fd346570b27c23487ffe8e346f0e2fe9a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce69c6b40ac3c5f9001a06e735cc3d3be85be2b36fed22ae9db809a6461efca(
    *,
    route_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMultiRegionEndpointPropsMixin.RouteDetailsItemsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49766420ba90eb571427152de585931a0fc27a980e63d329599d6358c437f827(
    *,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf3084140b378671c678cd74853f9e614b424ce200720f5e49267323db4d967(
    *,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptFilterPropsMixin.FilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95579bb5aeb8b808d3653372f1739b53a452efe268e88175f1b77c7f7f062720(
    props: typing.Union[CfnReceiptFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a238f2d456ccb1c37f223106ec8c554c80eb1cf6fa0a65e8eb0cbc662d4f722(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592213f6d4c1d69073337e3f3bf48207cc0820677e6c0f8802fca8ed2a8cec06(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a577ffe595807c7e9fffadf284cabbd57aab30ef6128a9fb235250cc19d1b9b8(
    *,
    ip_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptFilterPropsMixin.IpFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9d383f7f5f4ea5b9c12e4c387ca7e01e43a610710f93dcbc60f383a05a9b98(
    *,
    cidr: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae64b6b855b6a5dc864b51b138f7183f0ba01bf4716e381417e16165c2fde976(
    *,
    after: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptRulePropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_set_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe418f81d0daf101f0dcb619b9ad8d74cc3e8132a8de07591d81d98f14684dc(
    props: typing.Union[CfnReceiptRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976d85d149722b729cf097db7e968411403df20fecd0e168e70eee7e4a3b048a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489b7e4176ff822e3c8c5fbd42bdae6df1582bd63bea23a02431d4c1fbae836f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec1a0e0da76fa3808f5a70ab49e2b53dfed490f4de68e1937c95adb62b88817(
    *,
    add_header_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptRulePropsMixin.AddHeaderActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bounce_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptRulePropsMixin.BounceActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connect_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptRulePropsMixin.ConnectActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptRulePropsMixin.LambdaActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptRulePropsMixin.S3ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptRulePropsMixin.SNSActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stop_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptRulePropsMixin.StopActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    workmail_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptRulePropsMixin.WorkmailActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424ba99092f8d6450755f502d12b664c56e6460d027140062d33516e8af591f7(
    *,
    header_name: typing.Optional[builtins.str] = None,
    header_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7aad486946005452ea382d62c068db53cb8cd77efc0411a73bcc43b4be624c(
    *,
    message: typing.Optional[builtins.str] = None,
    sender: typing.Optional[builtins.str] = None,
    smtp_reply_code: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a609b41e66c991897bef90d07392d4620392c21d08a54f6ff83b8c236c05c406(
    *,
    iam_role_arn: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3632ae4fe479d5e95d874e843c04d6a3dace3ec50a03401ea7dcb046c298a7(
    *,
    function_arn: typing.Optional[builtins.str] = None,
    invocation_type: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da2e7b9e942269ad4a144e7cb18439b75b32c0d4862ebaa5333f9ab1a7d5ac6(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReceiptRulePropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tls_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eaaef6768e4a3c1db52bdfb175f8b4f759bff6606b629a81dcb4f562bfda93d(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    object_key_prefix: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad7475e95cc219dd77715cbc061bdd1f2e4b43a0e8c3a5a27006686fa0f08ce(
    *,
    encoding: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a0b6505c8eb3d498f6baca47e5baecd7c36b9aceea0432aebcd32330cf8ba6(
    *,
    scope: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40260240ca6189e89d6b0ca315c1059825bf87bd73748dae260cba54480ae9d7(
    *,
    organization_arn: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3d3f96af92457d71a726e569716136e34b4fbd6d42341538bb59988b548907(
    *,
    rule_set_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137e73c5a6413e353b81d50aafbfed8357ccc5af15deedb9becb7d2f79f6ff51(
    props: typing.Union[CfnReceiptRuleSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb136509015b9c778253115ace5db17690688d62f34f4f58e7c0b2dfa332659(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9afc9d0614e4a0ed1ef052c0ae5b222856d664ad934230426a1ecaa7daa7bc86(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd577f976de68e4e03cade3504c4570da0859bc70e2105614c278efe11e2c7b(
    *,
    template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c1c650f42996d74231317c8fb53be26262ba487f845679829a69f42ceb7e19(
    props: typing.Union[CfnTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf2af43c02c6048aaa895aa2a5b7630647f2f7dae46f36118831bd1a4d74ac6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a5b4c1196c09fce6bfaae6bcedb24f24c9bb1e11d79e2c6638412b5cd96555(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08780633b04f33dee932e57c05978c5c24b9fc9bcb0f7243ca5cf7f54f356f67(
    *,
    html_part: typing.Optional[builtins.str] = None,
    subject_part: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
    text_part: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b244a8c6cfa7f433c8d96217607ec0d6749edea792ce0ac9a8f6e50808e62ca(
    *,
    dashboard_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVdmAttributesPropsMixin.DashboardAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    guardian_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVdmAttributesPropsMixin.GuardianAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e785de7a555cddaa007095dfce3edc9d05aa5578132bb7d000ee48ed908367(
    props: typing.Union[CfnVdmAttributesMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c4ef5beaef00946f201360438f66d6dbbbf1c0ecf9253112d540d5e0729b3d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e2e4a0735639afaf7f90e2fdfb832e4fd8024b05a5ec13c888bdda2e527191(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7128442bc1a82a39ad83408c6c677edcea6c32852b2baf176b2c8f2fbb16908(
    *,
    engagement_metrics: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5fe979dbe901cea5c050e199f9354a27f1558109898fe581f58bf1771446bce(
    *,
    optimized_shared_delivery: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
