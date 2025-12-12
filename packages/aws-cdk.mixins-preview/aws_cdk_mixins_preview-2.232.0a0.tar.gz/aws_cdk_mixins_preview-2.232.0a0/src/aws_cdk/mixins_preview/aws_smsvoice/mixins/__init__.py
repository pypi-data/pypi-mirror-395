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
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnConfigurationSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_set_name": "configurationSetName",
        "default_sender_id": "defaultSenderId",
        "event_destinations": "eventDestinations",
        "message_feedback_enabled": "messageFeedbackEnabled",
        "protect_configuration_id": "protectConfigurationId",
        "tags": "tags",
    },
)
class CfnConfigurationSetMixinProps:
    def __init__(
        self,
        *,
        configuration_set_name: typing.Optional[builtins.str] = None,
        default_sender_id: typing.Optional[builtins.str] = None,
        event_destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.EventDestinationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        message_feedback_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        protect_configuration_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfigurationSetPropsMixin.

        :param configuration_set_name: The name of the ConfigurationSet.
        :param default_sender_id: The default sender ID used by the ConfigurationSet.
        :param event_destinations: An array of EventDestination objects that describe any events to log and where to log them.
        :param message_feedback_enabled: Set to true to enable feedback for the message.
        :param protect_configuration_id: The unique identifier for the protect configuration.
        :param tags: An array of key and value pair tags that's associated with the new configuration set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-configurationset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
            
            cfn_configuration_set_mixin_props = smsvoice_mixins.CfnConfigurationSetMixinProps(
                configuration_set_name="configurationSetName",
                default_sender_id="defaultSenderId",
                event_destinations=[smsvoice_mixins.CfnConfigurationSetPropsMixin.EventDestinationProperty(
                    cloud_watch_logs_destination=smsvoice_mixins.CfnConfigurationSetPropsMixin.CloudWatchLogsDestinationProperty(
                        iam_role_arn="iamRoleArn",
                        log_group_arn="logGroupArn"
                    ),
                    enabled=False,
                    event_destination_name="eventDestinationName",
                    kinesis_firehose_destination=smsvoice_mixins.CfnConfigurationSetPropsMixin.KinesisFirehoseDestinationProperty(
                        delivery_stream_arn="deliveryStreamArn",
                        iam_role_arn="iamRoleArn"
                    ),
                    matching_event_types=["matchingEventTypes"],
                    sns_destination=smsvoice_mixins.CfnConfigurationSetPropsMixin.SnsDestinationProperty(
                        topic_arn="topicArn"
                    )
                )],
                message_feedback_enabled=False,
                protect_configuration_id="protectConfigurationId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848d025486a637ceb43b72efed624f17dd6aabd02f778bceaa57f5394c164127)
            check_type(argname="argument configuration_set_name", value=configuration_set_name, expected_type=type_hints["configuration_set_name"])
            check_type(argname="argument default_sender_id", value=default_sender_id, expected_type=type_hints["default_sender_id"])
            check_type(argname="argument event_destinations", value=event_destinations, expected_type=type_hints["event_destinations"])
            check_type(argname="argument message_feedback_enabled", value=message_feedback_enabled, expected_type=type_hints["message_feedback_enabled"])
            check_type(argname="argument protect_configuration_id", value=protect_configuration_id, expected_type=type_hints["protect_configuration_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration_set_name is not None:
            self._values["configuration_set_name"] = configuration_set_name
        if default_sender_id is not None:
            self._values["default_sender_id"] = default_sender_id
        if event_destinations is not None:
            self._values["event_destinations"] = event_destinations
        if message_feedback_enabled is not None:
            self._values["message_feedback_enabled"] = message_feedback_enabled
        if protect_configuration_id is not None:
            self._values["protect_configuration_id"] = protect_configuration_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the ConfigurationSet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-configurationset.html#cfn-smsvoice-configurationset-configurationsetname
        '''
        result = self._values.get("configuration_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_sender_id(self) -> typing.Optional[builtins.str]:
        '''The default sender ID used by the ConfigurationSet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-configurationset.html#cfn-smsvoice-configurationset-defaultsenderid
        '''
        result = self._values.get("default_sender_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_destinations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.EventDestinationProperty"]]]]:
        '''An array of EventDestination objects that describe any events to log and where to log them.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-configurationset.html#cfn-smsvoice-configurationset-eventdestinations
        '''
        result = self._values.get("event_destinations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.EventDestinationProperty"]]]], result)

    @builtins.property
    def message_feedback_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Set to true to enable feedback for the message.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-configurationset.html#cfn-smsvoice-configurationset-messagefeedbackenabled
        '''
        result = self._values.get("message_feedback_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def protect_configuration_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the protect configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-configurationset.html#cfn-smsvoice-configurationset-protectconfigurationid
        '''
        result = self._values.get("protect_configuration_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key and value pair tags that's associated with the new configuration set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-configurationset.html#cfn-smsvoice-configurationset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnConfigurationSetPropsMixin",
):
    '''Creates a new configuration set.

    After you create the configuration set, you can add one or more event destinations to it.

    A configuration set is a set of rules that you apply to the SMS and voice messages that you send.

    When you send a message, you can optionally specify a single configuration set.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-configurationset.html
    :cloudformationResource: AWS::SMSVOICE::ConfigurationSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
        
        cfn_configuration_set_props_mixin = smsvoice_mixins.CfnConfigurationSetPropsMixin(smsvoice_mixins.CfnConfigurationSetMixinProps(
            configuration_set_name="configurationSetName",
            default_sender_id="defaultSenderId",
            event_destinations=[smsvoice_mixins.CfnConfigurationSetPropsMixin.EventDestinationProperty(
                cloud_watch_logs_destination=smsvoice_mixins.CfnConfigurationSetPropsMixin.CloudWatchLogsDestinationProperty(
                    iam_role_arn="iamRoleArn",
                    log_group_arn="logGroupArn"
                ),
                enabled=False,
                event_destination_name="eventDestinationName",
                kinesis_firehose_destination=smsvoice_mixins.CfnConfigurationSetPropsMixin.KinesisFirehoseDestinationProperty(
                    delivery_stream_arn="deliveryStreamArn",
                    iam_role_arn="iamRoleArn"
                ),
                matching_event_types=["matchingEventTypes"],
                sns_destination=smsvoice_mixins.CfnConfigurationSetPropsMixin.SnsDestinationProperty(
                    topic_arn="topicArn"
                )
            )],
            message_feedback_enabled=False,
            protect_configuration_id="protectConfigurationId",
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
        props: typing.Union[CfnConfigurationSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SMSVOICE::ConfigurationSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0188581aced88312d339a1948c7b55d4f4987b3fcfdd9112e7d360b2065559)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab586677ddc3bea4c918642a92e2f3c656279dfdcd76d1cc5407c94a6518177c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86988af13a41e58ecd563410eb8ef58215dd1a58ef7b3569b406285768b695e7)
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
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnConfigurationSetPropsMixin.CloudWatchLogsDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"iam_role_arn": "iamRoleArn", "log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogsDestinationProperty:
        def __init__(
            self,
            *,
            iam_role_arn: typing.Optional[builtins.str] = None,
            log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the destination configuration to use when publishing message sending events.

            :param iam_role_arn: The Amazon Resource Name (ARN) of an AWS Identity and Access Management role that is able to write event data to an Amazon CloudWatch destination.
            :param log_group_arn: The name of the Amazon CloudWatch log group that you want to record events in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-cloudwatchlogsdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                cloud_watch_logs_destination_property = smsvoice_mixins.CfnConfigurationSetPropsMixin.CloudWatchLogsDestinationProperty(
                    iam_role_arn="iamRoleArn",
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb62299fd86c1ea8e7e0a89c202a71400cf2e489f4acd887bdfc978d4e42270a)
                check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iam_role_arn is not None:
                self._values["iam_role_arn"] = iam_role_arn
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn

        @builtins.property
        def iam_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Identity and Access Management role that is able to write event data to an Amazon CloudWatch destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-cloudwatchlogsdestination.html#cfn-smsvoice-configurationset-cloudwatchlogsdestination-iamrolearn
            '''
            result = self._values.get("iam_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon CloudWatch log group that you want to record events in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-cloudwatchlogsdestination.html#cfn-smsvoice-configurationset-cloudwatchlogsdestination-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnConfigurationSetPropsMixin.EventDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_destination": "cloudWatchLogsDestination",
            "enabled": "enabled",
            "event_destination_name": "eventDestinationName",
            "kinesis_firehose_destination": "kinesisFirehoseDestination",
            "matching_event_types": "matchingEventTypes",
            "sns_destination": "snsDestination",
        },
    )
    class EventDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.CloudWatchLogsDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            event_destination_name: typing.Optional[builtins.str] = None,
            kinesis_firehose_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.KinesisFirehoseDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            matching_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            sns_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationSetPropsMixin.SnsDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about an event destination.

            Event destinations are associated with configuration sets, which enable you to publish message sending events to CloudWatch, Firehose, or Amazon SNS.

            :param cloud_watch_logs_destination: An object that contains information about an event destination that sends logging events to Amazon CloudWatch logs.
            :param enabled: When set to true events will be logged.
            :param event_destination_name: The name of the EventDestination.
            :param kinesis_firehose_destination: An object that contains information about an event destination for logging to Amazon Data Firehose.
            :param matching_event_types: An array of event types that determine which events to log. .. epigraph:: The ``TEXT_SENT`` event type is not supported.
            :param sns_destination: An object that contains information about an event destination that sends logging events to Amazon SNS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-eventdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                event_destination_property = smsvoice_mixins.CfnConfigurationSetPropsMixin.EventDestinationProperty(
                    cloud_watch_logs_destination=smsvoice_mixins.CfnConfigurationSetPropsMixin.CloudWatchLogsDestinationProperty(
                        iam_role_arn="iamRoleArn",
                        log_group_arn="logGroupArn"
                    ),
                    enabled=False,
                    event_destination_name="eventDestinationName",
                    kinesis_firehose_destination=smsvoice_mixins.CfnConfigurationSetPropsMixin.KinesisFirehoseDestinationProperty(
                        delivery_stream_arn="deliveryStreamArn",
                        iam_role_arn="iamRoleArn"
                    ),
                    matching_event_types=["matchingEventTypes"],
                    sns_destination=smsvoice_mixins.CfnConfigurationSetPropsMixin.SnsDestinationProperty(
                        topic_arn="topicArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__771c11cfeb2bfff769d8d9ab5d12775925919dde3ce558501006b0286595cbe7)
                check_type(argname="argument cloud_watch_logs_destination", value=cloud_watch_logs_destination, expected_type=type_hints["cloud_watch_logs_destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument event_destination_name", value=event_destination_name, expected_type=type_hints["event_destination_name"])
                check_type(argname="argument kinesis_firehose_destination", value=kinesis_firehose_destination, expected_type=type_hints["kinesis_firehose_destination"])
                check_type(argname="argument matching_event_types", value=matching_event_types, expected_type=type_hints["matching_event_types"])
                check_type(argname="argument sns_destination", value=sns_destination, expected_type=type_hints["sns_destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_destination is not None:
                self._values["cloud_watch_logs_destination"] = cloud_watch_logs_destination
            if enabled is not None:
                self._values["enabled"] = enabled
            if event_destination_name is not None:
                self._values["event_destination_name"] = event_destination_name
            if kinesis_firehose_destination is not None:
                self._values["kinesis_firehose_destination"] = kinesis_firehose_destination
            if matching_event_types is not None:
                self._values["matching_event_types"] = matching_event_types
            if sns_destination is not None:
                self._values["sns_destination"] = sns_destination

        @builtins.property
        def cloud_watch_logs_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.CloudWatchLogsDestinationProperty"]]:
            '''An object that contains information about an event destination that sends logging events to Amazon CloudWatch logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-eventdestination.html#cfn-smsvoice-configurationset-eventdestination-cloudwatchlogsdestination
            '''
            result = self._values.get("cloud_watch_logs_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.CloudWatchLogsDestinationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to true events will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-eventdestination.html#cfn-smsvoice-configurationset-eventdestination-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def event_destination_name(self) -> typing.Optional[builtins.str]:
            '''The name of the EventDestination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-eventdestination.html#cfn-smsvoice-configurationset-eventdestination-eventdestinationname
            '''
            result = self._values.get("event_destination_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kinesis_firehose_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.KinesisFirehoseDestinationProperty"]]:
            '''An object that contains information about an event destination for logging to Amazon Data Firehose.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-eventdestination.html#cfn-smsvoice-configurationset-eventdestination-kinesisfirehosedestination
            '''
            result = self._values.get("kinesis_firehose_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.KinesisFirehoseDestinationProperty"]], result)

        @builtins.property
        def matching_event_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of event types that determine which events to log.

            .. epigraph::

               The ``TEXT_SENT`` event type is not supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-eventdestination.html#cfn-smsvoice-configurationset-eventdestination-matchingeventtypes
            '''
            result = self._values.get("matching_event_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def sns_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.SnsDestinationProperty"]]:
            '''An object that contains information about an event destination that sends logging events to Amazon SNS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-eventdestination.html#cfn-smsvoice-configurationset-eventdestination-snsdestination
            '''
            result = self._values.get("sns_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationSetPropsMixin.SnsDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnConfigurationSetPropsMixin.KinesisFirehoseDestinationProperty",
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
            '''Contains the delivery stream Amazon Resource Name (ARN), and the ARN of the AWS Identity and Access Management (IAM) role associated with a Firehose event destination.

            Event destinations, such as Firehose, are associated with configuration sets, which enable you to publish message sending events.

            :param delivery_stream_arn: The Amazon Resource Name (ARN) of the delivery stream.
            :param iam_role_arn: The ARN of an AWS Identity and Access Management role that is able to write event data to an Amazon Data Firehose destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-kinesisfirehosedestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                kinesis_firehose_destination_property = smsvoice_mixins.CfnConfigurationSetPropsMixin.KinesisFirehoseDestinationProperty(
                    delivery_stream_arn="deliveryStreamArn",
                    iam_role_arn="iamRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e7a9125a1693fcb10848630ccd45c002de62fb44e86c36d8470cb82566fc340)
                check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
                check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_stream_arn is not None:
                self._values["delivery_stream_arn"] = delivery_stream_arn
            if iam_role_arn is not None:
                self._values["iam_role_arn"] = iam_role_arn

        @builtins.property
        def delivery_stream_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-kinesisfirehosedestination.html#cfn-smsvoice-configurationset-kinesisfirehosedestination-deliverystreamarn
            '''
            result = self._values.get("delivery_stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iam_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an AWS Identity and Access Management role that is able to write event data to an Amazon Data Firehose destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-kinesisfirehosedestination.html#cfn-smsvoice-configurationset-kinesisfirehosedestination-iamrolearn
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
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnConfigurationSetPropsMixin.SnsDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_arn": "topicArn"},
    )
    class SnsDestinationProperty:
        def __init__(self, *, topic_arn: typing.Optional[builtins.str] = None) -> None:
            '''An object that defines an Amazon SNS destination for events.

            You can use Amazon SNS to send notification when certain events occur.

            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic that you want to publish events to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-snsdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                sns_destination_property = smsvoice_mixins.CfnConfigurationSetPropsMixin.SnsDestinationProperty(
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df3336dbbae966f3ff0e9c754a747ff8650ed495a2c75679d9e3b9890d244ecc)
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic that you want to publish events to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-configurationset-snsdestination.html#cfn-smsvoice-configurationset-snsdestination-topicarn
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
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnOptOutListMixinProps",
    jsii_struct_bases=[],
    name_mapping={"opt_out_list_name": "optOutListName", "tags": "tags"},
)
class CfnOptOutListMixinProps:
    def __init__(
        self,
        *,
        opt_out_list_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOptOutListPropsMixin.

        :param opt_out_list_name: The name of the OptOutList.
        :param tags: An array of tags (key and value pairs) to associate with the new OptOutList.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-optoutlist.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
            
            cfn_opt_out_list_mixin_props = smsvoice_mixins.CfnOptOutListMixinProps(
                opt_out_list_name="optOutListName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90dec4175b76ec19945dc9f8a30e0853d67d21262532207eb0b319cf1bb50ad)
            check_type(argname="argument opt_out_list_name", value=opt_out_list_name, expected_type=type_hints["opt_out_list_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if opt_out_list_name is not None:
            self._values["opt_out_list_name"] = opt_out_list_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def opt_out_list_name(self) -> typing.Optional[builtins.str]:
        '''The name of the OptOutList.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-optoutlist.html#cfn-smsvoice-optoutlist-optoutlistname
        '''
        result = self._values.get("opt_out_list_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of tags (key and value pairs) to associate with the new OptOutList.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-optoutlist.html#cfn-smsvoice-optoutlist-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOptOutListMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOptOutListPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnOptOutListPropsMixin",
):
    '''Creates a new opt-out list.

    If the opt-out list name already exists, an error is returned.

    An opt-out list is a list of phone numbers that are opted out, meaning you can't send SMS or voice messages to them. If end user replies with the keyword "STOP," an entry for the phone number is added to the opt-out list. In addition to STOP, your recipients can use any supported opt-out keyword, such as CANCEL or OPTOUT. For a list of supported opt-out keywords, see `SMS opt out <https://docs.aws.amazon.com/sms-voice/latest/userguide/opt-out-list-keywords.html>`_ in the End User Messaging  User Guide.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-optoutlist.html
    :cloudformationResource: AWS::SMSVOICE::OptOutList
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
        
        cfn_opt_out_list_props_mixin = smsvoice_mixins.CfnOptOutListPropsMixin(smsvoice_mixins.CfnOptOutListMixinProps(
            opt_out_list_name="optOutListName",
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
        props: typing.Union[CfnOptOutListMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SMSVOICE::OptOutList``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac61ab03459ef477146805efd61a230287d6531df80c198ea2d128a48a69f57c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47078d626030b6ee880f54a82531b57f8848605a94e8000b10aac76c26a67bc9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad94ffd3f7d0beb973d9d5599b7edc96b81eb1bed768109b4be160f6ae4cd402)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOptOutListMixinProps:
        return typing.cast(CfnOptOutListMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPhoneNumberMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "iso_country_code": "isoCountryCode",
        "mandatory_keywords": "mandatoryKeywords",
        "number_capabilities": "numberCapabilities",
        "number_type": "numberType",
        "optional_keywords": "optionalKeywords",
        "opt_out_list_name": "optOutListName",
        "self_managed_opt_outs_enabled": "selfManagedOptOutsEnabled",
        "tags": "tags",
        "two_way": "twoWay",
    },
)
class CfnPhoneNumberMixinProps:
    def __init__(
        self,
        *,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        iso_country_code: typing.Optional[builtins.str] = None,
        mandatory_keywords: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPhoneNumberPropsMixin.MandatoryKeywordsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        number_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        number_type: typing.Optional[builtins.str] = None,
        optional_keywords: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPhoneNumberPropsMixin.OptionalKeywordProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        opt_out_list_name: typing.Optional[builtins.str] = None,
        self_managed_opt_outs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        two_way: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPhoneNumberPropsMixin.TwoWayProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPhoneNumberPropsMixin.

        :param deletion_protection_enabled: By default this is set to false. When set to true the phone number can't be deleted.
        :param iso_country_code: The two-character code, in ISO 3166-1 alpha-2 format, for the country or region.
        :param mandatory_keywords: Creates or updates a ``MandatoryKeyword`` configuration on an origination phone number For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging User Guide.
        :param number_capabilities: Indicates if the phone number will be used for text messages, voice messages, or both.
        :param number_type: The type of phone number to request. .. epigraph:: The ``ShortCode`` number type is not supported in AWS CloudFormation .
        :param optional_keywords: A keyword is a word that you can search for on a particular phone number or pool. It is also a specific word or phrase that an end user can send to your number to elicit a response, such as an informational message or a special offer. When your number receives a message that begins with a keyword, End User Messaging responds with a customizable message. Optional keywords are differentiated from mandatory keywords. For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging User Guide.
        :param opt_out_list_name: The name of the OptOutList associated with the phone number.
        :param self_managed_opt_outs_enabled: When set to false and an end recipient sends a message that begins with HELP or STOP to one of your dedicated numbers, End User Messaging automatically replies with a customizable message and adds the end recipient to the OptOutList. When set to true you're responsible for responding to HELP and STOP requests. You're also responsible for tracking and honoring opt-out request. For more information see `Self-managed opt-outs <https://docs.aws.amazon.com/sms-voice/latest/userguide/opt-out-list-self-managed.html>`_
        :param tags: An array of tags (key and value pairs) to associate with the requested phone number.
        :param two_way: Describes the two-way SMS configuration for a phone number. For more information, see `Two-way SMS messaging <https://docs.aws.amazon.com/sms-voice/latest/userguide/two-way-sms.html>`_ in the End User Messaging User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
            
            cfn_phone_number_mixin_props = smsvoice_mixins.CfnPhoneNumberMixinProps(
                deletion_protection_enabled=False,
                iso_country_code="isoCountryCode",
                mandatory_keywords=smsvoice_mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordsProperty(
                    help=smsvoice_mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordProperty(
                        message="message"
                    ),
                    stop=smsvoice_mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordProperty(
                        message="message"
                    )
                ),
                number_capabilities=["numberCapabilities"],
                number_type="numberType",
                optional_keywords=[smsvoice_mixins.CfnPhoneNumberPropsMixin.OptionalKeywordProperty(
                    action="action",
                    keyword="keyword",
                    message="message"
                )],
                opt_out_list_name="optOutListName",
                self_managed_opt_outs_enabled=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                two_way=smsvoice_mixins.CfnPhoneNumberPropsMixin.TwoWayProperty(
                    channel_arn="channelArn",
                    channel_role="channelRole",
                    enabled=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976ab8aaf05dcb7fad769dc075033092e2d8f86206cc562d80765ddd1a972437)
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument iso_country_code", value=iso_country_code, expected_type=type_hints["iso_country_code"])
            check_type(argname="argument mandatory_keywords", value=mandatory_keywords, expected_type=type_hints["mandatory_keywords"])
            check_type(argname="argument number_capabilities", value=number_capabilities, expected_type=type_hints["number_capabilities"])
            check_type(argname="argument number_type", value=number_type, expected_type=type_hints["number_type"])
            check_type(argname="argument optional_keywords", value=optional_keywords, expected_type=type_hints["optional_keywords"])
            check_type(argname="argument opt_out_list_name", value=opt_out_list_name, expected_type=type_hints["opt_out_list_name"])
            check_type(argname="argument self_managed_opt_outs_enabled", value=self_managed_opt_outs_enabled, expected_type=type_hints["self_managed_opt_outs_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument two_way", value=two_way, expected_type=type_hints["two_way"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if iso_country_code is not None:
            self._values["iso_country_code"] = iso_country_code
        if mandatory_keywords is not None:
            self._values["mandatory_keywords"] = mandatory_keywords
        if number_capabilities is not None:
            self._values["number_capabilities"] = number_capabilities
        if number_type is not None:
            self._values["number_type"] = number_type
        if optional_keywords is not None:
            self._values["optional_keywords"] = optional_keywords
        if opt_out_list_name is not None:
            self._values["opt_out_list_name"] = opt_out_list_name
        if self_managed_opt_outs_enabled is not None:
            self._values["self_managed_opt_outs_enabled"] = self_managed_opt_outs_enabled
        if tags is not None:
            self._values["tags"] = tags
        if two_way is not None:
            self._values["two_way"] = two_way

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''By default this is set to false.

        When set to true the phone number can't be deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html#cfn-smsvoice-phonenumber-deletionprotectionenabled
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def iso_country_code(self) -> typing.Optional[builtins.str]:
        '''The two-character code, in ISO 3166-1 alpha-2 format, for the country or region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html#cfn-smsvoice-phonenumber-isocountrycode
        '''
        result = self._values.get("iso_country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mandatory_keywords(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPhoneNumberPropsMixin.MandatoryKeywordsProperty"]]:
        '''Creates or updates a ``MandatoryKeyword`` configuration on an origination phone number For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html#cfn-smsvoice-phonenumber-mandatorykeywords
        '''
        result = self._values.get("mandatory_keywords")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPhoneNumberPropsMixin.MandatoryKeywordsProperty"]], result)

    @builtins.property
    def number_capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Indicates if the phone number will be used for text messages, voice messages, or both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html#cfn-smsvoice-phonenumber-numbercapabilities
        '''
        result = self._values.get("number_capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def number_type(self) -> typing.Optional[builtins.str]:
        '''The type of phone number to request.

        .. epigraph::

           The ``ShortCode`` number type is not supported in AWS CloudFormation .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html#cfn-smsvoice-phonenumber-numbertype
        '''
        result = self._values.get("number_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional_keywords(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPhoneNumberPropsMixin.OptionalKeywordProperty"]]]]:
        '''A keyword is a word that you can search for on a particular phone number or pool.

        It is also a specific word or phrase that an end user can send to your number to elicit a response, such as an informational message or a special offer. When your number receives a message that begins with a keyword, End User Messaging  responds with a customizable message. Optional keywords are differentiated from mandatory keywords. For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html#cfn-smsvoice-phonenumber-optionalkeywords
        '''
        result = self._values.get("optional_keywords")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPhoneNumberPropsMixin.OptionalKeywordProperty"]]]], result)

    @builtins.property
    def opt_out_list_name(self) -> typing.Optional[builtins.str]:
        '''The name of the OptOutList associated with the phone number.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html#cfn-smsvoice-phonenumber-optoutlistname
        '''
        result = self._values.get("opt_out_list_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def self_managed_opt_outs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When set to false and an end recipient sends a message that begins with HELP or STOP to one of your dedicated numbers, End User Messaging  automatically replies with a customizable message and adds the end recipient to the OptOutList.

        When set to true you're responsible for responding to HELP and STOP requests. You're also responsible for tracking and honoring opt-out request. For more information see `Self-managed opt-outs <https://docs.aws.amazon.com/sms-voice/latest/userguide/opt-out-list-self-managed.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html#cfn-smsvoice-phonenumber-selfmanagedoptoutsenabled
        '''
        result = self._values.get("self_managed_opt_outs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of tags (key and value pairs) to associate with the requested phone number.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html#cfn-smsvoice-phonenumber-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def two_way(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPhoneNumberPropsMixin.TwoWayProperty"]]:
        '''Describes the two-way SMS configuration for a phone number.

        For more information, see `Two-way SMS messaging <https://docs.aws.amazon.com/sms-voice/latest/userguide/two-way-sms.html>`_ in the End User Messaging  User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html#cfn-smsvoice-phonenumber-twoway
        '''
        result = self._values.get("two_way")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPhoneNumberPropsMixin.TwoWayProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPhoneNumberMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPhoneNumberPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPhoneNumberPropsMixin",
):
    '''Request an origination phone number for use in your account.

    For more information on phone number request see `Request a phone number <https://docs.aws.amazon.com/sms-voice/latest/userguide/phone-numbers-request.html>`_ in the *End User Messaging  User Guide* .
    .. epigraph::

       Registering phone numbers is not supported by AWS CloudFormation . You can import phone numbers and sender IDs that are automatically provisioned at registration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-phonenumber.html
    :cloudformationResource: AWS::SMSVOICE::PhoneNumber
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
        
        cfn_phone_number_props_mixin = smsvoice_mixins.CfnPhoneNumberPropsMixin(smsvoice_mixins.CfnPhoneNumberMixinProps(
            deletion_protection_enabled=False,
            iso_country_code="isoCountryCode",
            mandatory_keywords=smsvoice_mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordsProperty(
                help=smsvoice_mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordProperty(
                    message="message"
                ),
                stop=smsvoice_mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordProperty(
                    message="message"
                )
            ),
            number_capabilities=["numberCapabilities"],
            number_type="numberType",
            optional_keywords=[smsvoice_mixins.CfnPhoneNumberPropsMixin.OptionalKeywordProperty(
                action="action",
                keyword="keyword",
                message="message"
            )],
            opt_out_list_name="optOutListName",
            self_managed_opt_outs_enabled=False,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            two_way=smsvoice_mixins.CfnPhoneNumberPropsMixin.TwoWayProperty(
                channel_arn="channelArn",
                channel_role="channelRole",
                enabled=False
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPhoneNumberMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SMSVOICE::PhoneNumber``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16fd33fc198dde3f0279aa5b277549e9b71ce658594b66d1479cbb878257f55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d99f2a0e1c751b1ef5e31a04e71ef27b80b76267a2db7d4283947f3df4bde4c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d519ae428ac3c33d0d26e546bf100757a9d6dd59819ede4b3a577ada41a12ee0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPhoneNumberMixinProps:
        return typing.cast(CfnPhoneNumberMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordProperty",
        jsii_struct_bases=[],
        name_mapping={"message": "message"},
    )
    class MandatoryKeywordProperty:
        def __init__(self, *, message: typing.Optional[builtins.str] = None) -> None:
            '''The keywords ``HELP`` and ``STOP`` are mandatory keywords that each phone number must have.

            For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

            :param message: The message associated with the keyword.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-mandatorykeyword.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                mandatory_keyword_property = smsvoice_mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordProperty(
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4538a11877e70edffd4bc1def5be9e717fc9051dad83e03baf9dff020378ccca)
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''The message associated with the keyword.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-mandatorykeyword.html#cfn-smsvoice-phonenumber-mandatorykeyword-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MandatoryKeywordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordsProperty",
        jsii_struct_bases=[],
        name_mapping={"help": "help", "stop": "stop"},
    )
    class MandatoryKeywordsProperty:
        def __init__(
            self,
            *,
            help: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPhoneNumberPropsMixin.MandatoryKeywordProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stop: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPhoneNumberPropsMixin.MandatoryKeywordProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The keywords ``HELP`` and ``STOP`` are mandatory keywords that each phone number must have.

            For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

            :param help: Specifies the ``HELP`` keyword that customers use to obtain customer support for this phone number. For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging User Guide.
            :param stop: Specifies the ``STOP`` keyword that customers use to opt out of receiving messages from this phone number. For more information, see `Required opt-out keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords-required.html>`_ in the End User Messaging User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-mandatorykeywords.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                mandatory_keywords_property = smsvoice_mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordsProperty(
                    help=smsvoice_mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordProperty(
                        message="message"
                    ),
                    stop=smsvoice_mixins.CfnPhoneNumberPropsMixin.MandatoryKeywordProperty(
                        message="message"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d640f13b8d5b69addf93502bf81436f3a0283db9a5d115233082dc5fb066f39)
                check_type(argname="argument help", value=help, expected_type=type_hints["help"])
                check_type(argname="argument stop", value=stop, expected_type=type_hints["stop"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if help is not None:
                self._values["help"] = help
            if stop is not None:
                self._values["stop"] = stop

        @builtins.property
        def help(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPhoneNumberPropsMixin.MandatoryKeywordProperty"]]:
            '''Specifies the ``HELP`` keyword that customers use to obtain customer support for this phone number.

            For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-mandatorykeywords.html#cfn-smsvoice-phonenumber-mandatorykeywords-help
            '''
            result = self._values.get("help")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPhoneNumberPropsMixin.MandatoryKeywordProperty"]], result)

        @builtins.property
        def stop(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPhoneNumberPropsMixin.MandatoryKeywordProperty"]]:
            '''Specifies the ``STOP`` keyword that customers use to opt out of receiving messages from this phone number.

            For more information, see `Required opt-out keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords-required.html>`_ in the End User Messaging  User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-mandatorykeywords.html#cfn-smsvoice-phonenumber-mandatorykeywords-stop
            '''
            result = self._values.get("stop")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPhoneNumberPropsMixin.MandatoryKeywordProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MandatoryKeywordsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPhoneNumberPropsMixin.OptionalKeywordProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "keyword": "keyword", "message": "message"},
    )
    class OptionalKeywordProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            keyword: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``OptionalKeyword`` configuration.

            For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

            :param action: The action to perform when the keyword is used.
            :param keyword: The new keyword to add.
            :param message: The message associated with the keyword.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-optionalkeyword.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                optional_keyword_property = smsvoice_mixins.CfnPhoneNumberPropsMixin.OptionalKeywordProperty(
                    action="action",
                    keyword="keyword",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f8d3f32673869782cb40a129d9b1d7aeb4eb0e9a19450b32c0adc0eac3ecbe9)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument keyword", value=keyword, expected_type=type_hints["keyword"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if keyword is not None:
                self._values["keyword"] = keyword
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to perform when the keyword is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-optionalkeyword.html#cfn-smsvoice-phonenumber-optionalkeyword-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def keyword(self) -> typing.Optional[builtins.str]:
            '''The new keyword to add.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-optionalkeyword.html#cfn-smsvoice-phonenumber-optionalkeyword-keyword
            '''
            result = self._values.get("keyword")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''The message associated with the keyword.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-optionalkeyword.html#cfn-smsvoice-phonenumber-optionalkeyword-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionalKeywordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPhoneNumberPropsMixin.TwoWayProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_arn": "channelArn",
            "channel_role": "channelRole",
            "enabled": "enabled",
        },
    )
    class TwoWayProperty:
        def __init__(
            self,
            *,
            channel_arn: typing.Optional[builtins.str] = None,
            channel_role: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The phone number's two-way SMS configuration object.

            :param channel_arn: The Amazon Resource Name (ARN) of the two way channel.
            :param channel_role: An optional IAM Role Arn for a service to assume, to be able to post inbound SMS messages.
            :param enabled: By default this is set to false. When set to true you can receive incoming text messages from your end recipients using the TwoWayChannelArn.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-twoway.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                two_way_property = smsvoice_mixins.CfnPhoneNumberPropsMixin.TwoWayProperty(
                    channel_arn="channelArn",
                    channel_role="channelRole",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0621adb44df8517352e42af5852a6bfd22e635f5bf70c2a8e66c28b79400fed2)
                check_type(argname="argument channel_arn", value=channel_arn, expected_type=type_hints["channel_arn"])
                check_type(argname="argument channel_role", value=channel_role, expected_type=type_hints["channel_role"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_arn is not None:
                self._values["channel_arn"] = channel_arn
            if channel_role is not None:
                self._values["channel_role"] = channel_role
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def channel_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the two way channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-twoway.html#cfn-smsvoice-phonenumber-twoway-channelarn
            '''
            result = self._values.get("channel_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def channel_role(self) -> typing.Optional[builtins.str]:
            '''An optional IAM Role Arn for a service to assume, to be able to post inbound SMS messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-twoway.html#cfn-smsvoice-phonenumber-twoway-channelrole
            '''
            result = self._values.get("channel_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''By default this is set to false.

            When set to true you can receive incoming text messages from your end recipients using the TwoWayChannelArn.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-phonenumber-twoway.html#cfn-smsvoice-phonenumber-twoway-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TwoWayProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPoolMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "mandatory_keywords": "mandatoryKeywords",
        "optional_keywords": "optionalKeywords",
        "opt_out_list_name": "optOutListName",
        "origination_identities": "originationIdentities",
        "self_managed_opt_outs_enabled": "selfManagedOptOutsEnabled",
        "shared_routes_enabled": "sharedRoutesEnabled",
        "tags": "tags",
        "two_way": "twoWay",
    },
)
class CfnPoolMixinProps:
    def __init__(
        self,
        *,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        mandatory_keywords: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPoolPropsMixin.MandatoryKeywordsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        optional_keywords: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPoolPropsMixin.OptionalKeywordProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        opt_out_list_name: typing.Optional[builtins.str] = None,
        origination_identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        self_managed_opt_outs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        shared_routes_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        two_way: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPoolPropsMixin.TwoWayProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPoolPropsMixin.

        :param deletion_protection_enabled: When set to true the pool can't be deleted.
        :param mandatory_keywords: Creates or updates the pool's ``MandatoryKeyword`` configuration. For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging User Guide.
        :param optional_keywords: Specifies any optional keywords to associate with the pool. For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging User Guide.
        :param opt_out_list_name: The name of the OptOutList associated with the pool.
        :param origination_identities: The list of origination identities to apply to the pool, either ``PhoneNumberArn`` or ``SenderIdArn`` . For more information, see `Registrations <https://docs.aws.amazon.com/sms-voice/latest/userguide/registrations.html>`_ in the End User Messaging User Guide. .. epigraph:: If you are using a shared End User Messaging resource then you must use the full Amazon Resource Name (ARN).
        :param self_managed_opt_outs_enabled: When set to false, an end recipient sends a message that begins with HELP or STOP to one of your dedicated numbers, End User Messaging automatically replies with a customizable message and adds the end recipient to the OptOutList. When set to true you're responsible for responding to HELP and STOP requests. You're also responsible for tracking and honoring opt-out requests. For more information see `Self-managed opt-outs <https://docs.aws.amazon.com//pinpoint/latest/userguide/settings-sms-managing.html#settings-account-sms-self-managed-opt-out>`_
        :param shared_routes_enabled: Allows you to enable shared routes on your pool. By default, this is set to ``False`` . If you set this value to ``True`` , your messages are sent using phone numbers or sender IDs (depending on the country) that are shared with other users. In some countries, such as the United States, senders aren't allowed to use shared routes and must use a dedicated phone number or short code.
        :param tags: An array of tags (key and value pairs) associated with the pool.
        :param two_way: Describes the two-way SMS configuration for a phone number. For more information, see `Two-way SMS messaging <https://docs.aws.amazon.com/sms-voice/latest/userguide/two-way-sms.html>`_ in the End User Messaging User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
            
            cfn_pool_mixin_props = smsvoice_mixins.CfnPoolMixinProps(
                deletion_protection_enabled=False,
                mandatory_keywords=smsvoice_mixins.CfnPoolPropsMixin.MandatoryKeywordsProperty(
                    help=smsvoice_mixins.CfnPoolPropsMixin.MandatoryKeywordProperty(
                        message="message"
                    ),
                    stop=smsvoice_mixins.CfnPoolPropsMixin.MandatoryKeywordProperty(
                        message="message"
                    )
                ),
                optional_keywords=[smsvoice_mixins.CfnPoolPropsMixin.OptionalKeywordProperty(
                    action="action",
                    keyword="keyword",
                    message="message"
                )],
                opt_out_list_name="optOutListName",
                origination_identities=["originationIdentities"],
                self_managed_opt_outs_enabled=False,
                shared_routes_enabled=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                two_way=smsvoice_mixins.CfnPoolPropsMixin.TwoWayProperty(
                    channel_arn="channelArn",
                    channel_role="channelRole",
                    enabled=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e981a25a63a4a4c36645da4101db15f6819b6aaa256542e483aa1ff13cdb8268)
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument mandatory_keywords", value=mandatory_keywords, expected_type=type_hints["mandatory_keywords"])
            check_type(argname="argument optional_keywords", value=optional_keywords, expected_type=type_hints["optional_keywords"])
            check_type(argname="argument opt_out_list_name", value=opt_out_list_name, expected_type=type_hints["opt_out_list_name"])
            check_type(argname="argument origination_identities", value=origination_identities, expected_type=type_hints["origination_identities"])
            check_type(argname="argument self_managed_opt_outs_enabled", value=self_managed_opt_outs_enabled, expected_type=type_hints["self_managed_opt_outs_enabled"])
            check_type(argname="argument shared_routes_enabled", value=shared_routes_enabled, expected_type=type_hints["shared_routes_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument two_way", value=two_way, expected_type=type_hints["two_way"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if mandatory_keywords is not None:
            self._values["mandatory_keywords"] = mandatory_keywords
        if optional_keywords is not None:
            self._values["optional_keywords"] = optional_keywords
        if opt_out_list_name is not None:
            self._values["opt_out_list_name"] = opt_out_list_name
        if origination_identities is not None:
            self._values["origination_identities"] = origination_identities
        if self_managed_opt_outs_enabled is not None:
            self._values["self_managed_opt_outs_enabled"] = self_managed_opt_outs_enabled
        if shared_routes_enabled is not None:
            self._values["shared_routes_enabled"] = shared_routes_enabled
        if tags is not None:
            self._values["tags"] = tags
        if two_way is not None:
            self._values["two_way"] = two_way

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When set to true the pool can't be deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html#cfn-smsvoice-pool-deletionprotectionenabled
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def mandatory_keywords(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPoolPropsMixin.MandatoryKeywordsProperty"]]:
        '''Creates or updates the pool's ``MandatoryKeyword`` configuration.

        For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html#cfn-smsvoice-pool-mandatorykeywords
        '''
        result = self._values.get("mandatory_keywords")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPoolPropsMixin.MandatoryKeywordsProperty"]], result)

    @builtins.property
    def optional_keywords(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPoolPropsMixin.OptionalKeywordProperty"]]]]:
        '''Specifies any optional keywords to associate with the pool.

        For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html#cfn-smsvoice-pool-optionalkeywords
        '''
        result = self._values.get("optional_keywords")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPoolPropsMixin.OptionalKeywordProperty"]]]], result)

    @builtins.property
    def opt_out_list_name(self) -> typing.Optional[builtins.str]:
        '''The name of the OptOutList associated with the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html#cfn-smsvoice-pool-optoutlistname
        '''
        result = self._values.get("opt_out_list_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origination_identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of origination identities to apply to the pool, either ``PhoneNumberArn`` or ``SenderIdArn`` .

        For more information, see `Registrations <https://docs.aws.amazon.com/sms-voice/latest/userguide/registrations.html>`_ in the End User Messaging  User Guide.
        .. epigraph::

           If you are using a shared End User Messaging  resource then you must use the full Amazon Resource Name (ARN).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html#cfn-smsvoice-pool-originationidentities
        '''
        result = self._values.get("origination_identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def self_managed_opt_outs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When set to false, an end recipient sends a message that begins with HELP or STOP to one of your dedicated numbers, End User Messaging  automatically replies with a customizable message and adds the end recipient to the OptOutList.

        When set to true you're responsible for responding to HELP and STOP requests. You're also responsible for tracking and honoring opt-out requests. For more information see `Self-managed opt-outs <https://docs.aws.amazon.com//pinpoint/latest/userguide/settings-sms-managing.html#settings-account-sms-self-managed-opt-out>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html#cfn-smsvoice-pool-selfmanagedoptoutsenabled
        '''
        result = self._values.get("self_managed_opt_outs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def shared_routes_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Allows you to enable shared routes on your pool.

        By default, this is set to ``False`` . If you set this value to ``True`` , your messages are sent using phone numbers or sender IDs (depending on the country) that are shared with other users. In some countries, such as the United States, senders aren't allowed to use shared routes and must use a dedicated phone number or short code.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html#cfn-smsvoice-pool-sharedroutesenabled
        '''
        result = self._values.get("shared_routes_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of tags (key and value pairs) associated with the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html#cfn-smsvoice-pool-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def two_way(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPoolPropsMixin.TwoWayProperty"]]:
        '''Describes the two-way SMS configuration for a phone number.

        For more information, see `Two-way SMS messaging <https://docs.aws.amazon.com/sms-voice/latest/userguide/two-way-sms.html>`_ in the End User Messaging  User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html#cfn-smsvoice-pool-twoway
        '''
        result = self._values.get("two_way")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPoolPropsMixin.TwoWayProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPoolMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPoolPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPoolPropsMixin",
):
    '''Creates a new pool and associates the specified origination identity to the pool.

    A pool can include one or more phone numbers and SenderIds that are associated with your AWS account.

    The new pool inherits its configuration from the specified origination identity. This includes keywords, message type, opt-out list, two-way configuration, and self-managed opt-out configuration. Deletion protection isn't inherited from the origination identity and defaults to false.

    If the origination identity is a phone number and is already associated with another pool, an error is returned. A sender ID can be associated with multiple pools.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-pool.html
    :cloudformationResource: AWS::SMSVOICE::Pool
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
        
        cfn_pool_props_mixin = smsvoice_mixins.CfnPoolPropsMixin(smsvoice_mixins.CfnPoolMixinProps(
            deletion_protection_enabled=False,
            mandatory_keywords=smsvoice_mixins.CfnPoolPropsMixin.MandatoryKeywordsProperty(
                help=smsvoice_mixins.CfnPoolPropsMixin.MandatoryKeywordProperty(
                    message="message"
                ),
                stop=smsvoice_mixins.CfnPoolPropsMixin.MandatoryKeywordProperty(
                    message="message"
                )
            ),
            optional_keywords=[smsvoice_mixins.CfnPoolPropsMixin.OptionalKeywordProperty(
                action="action",
                keyword="keyword",
                message="message"
            )],
            opt_out_list_name="optOutListName",
            origination_identities=["originationIdentities"],
            self_managed_opt_outs_enabled=False,
            shared_routes_enabled=False,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            two_way=smsvoice_mixins.CfnPoolPropsMixin.TwoWayProperty(
                channel_arn="channelArn",
                channel_role="channelRole",
                enabled=False
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SMSVOICE::Pool``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12add5e705484a3d36ba61ff3df00186994eaee33dd83f8506b452f50a34fd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd9b2bf53a6d31c55d98e1265f83a02394ab00cbac67cda4e7febc174cb3f849)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453ad7950cde0b93bc4189969a1e691677154f8b304df7bfafbbcf23de89707a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPoolMixinProps:
        return typing.cast(CfnPoolMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPoolPropsMixin.MandatoryKeywordProperty",
        jsii_struct_bases=[],
        name_mapping={"message": "message"},
    )
    class MandatoryKeywordProperty:
        def __init__(self, *, message: typing.Optional[builtins.str] = None) -> None:
            '''The keywords ``HELP`` and ``STOP`` are mandatory keywords that each phone number must have.

            For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

            :param message: The message associated with the keyword.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-mandatorykeyword.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                mandatory_keyword_property = smsvoice_mixins.CfnPoolPropsMixin.MandatoryKeywordProperty(
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3983319a1d9d654bbf87584d02bbb9d2ce72825653f90a9f90eb18bdfdf3a79a)
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''The message associated with the keyword.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-mandatorykeyword.html#cfn-smsvoice-pool-mandatorykeyword-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MandatoryKeywordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPoolPropsMixin.MandatoryKeywordsProperty",
        jsii_struct_bases=[],
        name_mapping={"help": "help", "stop": "stop"},
    )
    class MandatoryKeywordsProperty:
        def __init__(
            self,
            *,
            help: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPoolPropsMixin.MandatoryKeywordProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stop: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPoolPropsMixin.MandatoryKeywordProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The manadatory keywords, ``HELP`` and ``STOP`` to add to the pool.

            For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

            :param help: Specifies the pool's ``HELP`` keyword. For more information, see `Opt out list required keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/opt-out-list-keywords.html>`_ in the End User Messaging User Guide.
            :param stop: Specifies the pool's opt-out keyword. For more information, see `Required opt-out keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords-required.html>`_ in the End User Messaging User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-mandatorykeywords.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                mandatory_keywords_property = smsvoice_mixins.CfnPoolPropsMixin.MandatoryKeywordsProperty(
                    help=smsvoice_mixins.CfnPoolPropsMixin.MandatoryKeywordProperty(
                        message="message"
                    ),
                    stop=smsvoice_mixins.CfnPoolPropsMixin.MandatoryKeywordProperty(
                        message="message"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd1302d89148d6a269833275dd4a66db7b29103c9b490ecd6a62e4e9828d184e)
                check_type(argname="argument help", value=help, expected_type=type_hints["help"])
                check_type(argname="argument stop", value=stop, expected_type=type_hints["stop"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if help is not None:
                self._values["help"] = help
            if stop is not None:
                self._values["stop"] = stop

        @builtins.property
        def help(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPoolPropsMixin.MandatoryKeywordProperty"]]:
            '''Specifies the pool's ``HELP`` keyword.

            For more information, see `Opt out list required keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/opt-out-list-keywords.html>`_ in the End User Messaging  User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-mandatorykeywords.html#cfn-smsvoice-pool-mandatorykeywords-help
            '''
            result = self._values.get("help")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPoolPropsMixin.MandatoryKeywordProperty"]], result)

        @builtins.property
        def stop(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPoolPropsMixin.MandatoryKeywordProperty"]]:
            '''Specifies the pool's opt-out keyword.

            For more information, see `Required opt-out keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords-required.html>`_ in the End User Messaging  User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-mandatorykeywords.html#cfn-smsvoice-pool-mandatorykeywords-stop
            '''
            result = self._values.get("stop")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPoolPropsMixin.MandatoryKeywordProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MandatoryKeywordsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPoolPropsMixin.OptionalKeywordProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "keyword": "keyword", "message": "message"},
    )
    class OptionalKeywordProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            keyword: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The pool's ``OptionalKeyword`` configuration.

            For more information, see `Keywords <https://docs.aws.amazon.com/sms-voice/latest/userguide/keywords.html>`_ in the End User Messaging  User Guide.

            :param action: The action to perform when the keyword is used.
            :param keyword: The new keyword to add.
            :param message: The message associated with the keyword.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-optionalkeyword.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                optional_keyword_property = smsvoice_mixins.CfnPoolPropsMixin.OptionalKeywordProperty(
                    action="action",
                    keyword="keyword",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7e728041cbef76a9622c9b181e87495f9bdfe0571921f03f9de5a4c02001092)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument keyword", value=keyword, expected_type=type_hints["keyword"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if keyword is not None:
                self._values["keyword"] = keyword
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to perform when the keyword is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-optionalkeyword.html#cfn-smsvoice-pool-optionalkeyword-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def keyword(self) -> typing.Optional[builtins.str]:
            '''The new keyword to add.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-optionalkeyword.html#cfn-smsvoice-pool-optionalkeyword-keyword
            '''
            result = self._values.get("keyword")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''The message associated with the keyword.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-optionalkeyword.html#cfn-smsvoice-pool-optionalkeyword-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionalKeywordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnPoolPropsMixin.TwoWayProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_arn": "channelArn",
            "channel_role": "channelRole",
            "enabled": "enabled",
        },
    )
    class TwoWayProperty:
        def __init__(
            self,
            *,
            channel_arn: typing.Optional[builtins.str] = None,
            channel_role: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The pool's two-way SMS configuration object.

            :param channel_arn: The Amazon Resource Name (ARN) of the two way channel.
            :param channel_role: An optional IAM Role Arn for a service to assume, to be able to post inbound SMS messages.
            :param enabled: By default this is set to false. When set to true you can receive incoming text messages from your end recipients using the TwoWayChannelArn.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-twoway.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                two_way_property = smsvoice_mixins.CfnPoolPropsMixin.TwoWayProperty(
                    channel_arn="channelArn",
                    channel_role="channelRole",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79f3a8e4bb1a61fb6e92a7be5c44d750ed6429b9016502f89becc0b04cb1dfb1)
                check_type(argname="argument channel_arn", value=channel_arn, expected_type=type_hints["channel_arn"])
                check_type(argname="argument channel_role", value=channel_role, expected_type=type_hints["channel_role"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_arn is not None:
                self._values["channel_arn"] = channel_arn
            if channel_role is not None:
                self._values["channel_role"] = channel_role
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def channel_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the two way channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-twoway.html#cfn-smsvoice-pool-twoway-channelarn
            '''
            result = self._values.get("channel_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def channel_role(self) -> typing.Optional[builtins.str]:
            '''An optional IAM Role Arn for a service to assume, to be able to post inbound SMS messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-twoway.html#cfn-smsvoice-pool-twoway-channelrole
            '''
            result = self._values.get("channel_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''By default this is set to false.

            When set to true you can receive incoming text messages from your end recipients using the TwoWayChannelArn.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-pool-twoway.html#cfn-smsvoice-pool-twoway-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TwoWayProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnProtectConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "country_rule_set": "countryRuleSet",
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "tags": "tags",
    },
)
class CfnProtectConfigurationMixinProps:
    def __init__(
        self,
        *,
        country_rule_set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProtectConfigurationPropsMixin.CountryRuleSetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProtectConfigurationPropsMixin.

        :param country_rule_set: The set of ``CountryRules`` you specify to control which countries End User Messaging can send your messages to.
        :param deletion_protection_enabled: The status of deletion protection for the protect configuration. When set to true deletion protection is enabled. By default this is set to false.
        :param tags: An array of key and value pair tags that are associated with the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-protectconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
            
            cfn_protect_configuration_mixin_props = smsvoice_mixins.CfnProtectConfigurationMixinProps(
                country_rule_set=smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleSetProperty(
                    mms=[smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty(
                        country_code="countryCode",
                        protect_status="protectStatus"
                    )],
                    sms=[smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty(
                        country_code="countryCode",
                        protect_status="protectStatus"
                    )],
                    voice=[smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty(
                        country_code="countryCode",
                        protect_status="protectStatus"
                    )]
                ),
                deletion_protection_enabled=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e883a6cd58779a48213350242f8f0f9a0175122df3466ddecb283939d0e2c66)
            check_type(argname="argument country_rule_set", value=country_rule_set, expected_type=type_hints["country_rule_set"])
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if country_rule_set is not None:
            self._values["country_rule_set"] = country_rule_set
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def country_rule_set(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectConfigurationPropsMixin.CountryRuleSetProperty"]]:
        '''The set of ``CountryRules`` you specify to control which countries End User Messaging  can send your messages to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-protectconfiguration.html#cfn-smsvoice-protectconfiguration-countryruleset
        '''
        result = self._values.get("country_rule_set")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectConfigurationPropsMixin.CountryRuleSetProperty"]], result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The status of deletion protection for the protect configuration.

        When set to true deletion protection is enabled. By default this is set to false.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-protectconfiguration.html#cfn-smsvoice-protectconfiguration-deletionprotectionenabled
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key and value pair tags that are associated with the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-protectconfiguration.html#cfn-smsvoice-protectconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProtectConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProtectConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnProtectConfigurationPropsMixin",
):
    '''Create a new protect configuration.

    By default all country rule sets for each capability are set to ``ALLOW`` . A protect configurations name is stored as a Tag with the key set to ``Name`` and value as the name of the protect configuration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-protectconfiguration.html
    :cloudformationResource: AWS::SMSVOICE::ProtectConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
        
        cfn_protect_configuration_props_mixin = smsvoice_mixins.CfnProtectConfigurationPropsMixin(smsvoice_mixins.CfnProtectConfigurationMixinProps(
            country_rule_set=smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleSetProperty(
                mms=[smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty(
                    country_code="countryCode",
                    protect_status="protectStatus"
                )],
                sms=[smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty(
                    country_code="countryCode",
                    protect_status="protectStatus"
                )],
                voice=[smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty(
                    country_code="countryCode",
                    protect_status="protectStatus"
                )]
            ),
            deletion_protection_enabled=False,
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
        props: typing.Union[CfnProtectConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SMSVOICE::ProtectConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcfc7d7cb2cb19ef912cf9c8df6f5b8f938cda7fb479142fb4d76fdb5b1dc0a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af52217205c3882e293b93be16f8f08989ff6e444578e357cd2a12bc246789c6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a6699de6728ec6fd3b988b1c48f3d2f3185c3d6a0af303bd5fafce0cf60ec26)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProtectConfigurationMixinProps:
        return typing.cast(CfnProtectConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "country_code": "countryCode",
            "protect_status": "protectStatus",
        },
    )
    class CountryRuleProperty:
        def __init__(
            self,
            *,
            country_code: typing.Optional[builtins.str] = None,
            protect_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the type of protection to use for a country.

            For example, to set Canada as allowed, the ``CountryRule`` would be formatted as follows:

            ``{ "CountryCode": "CA", "ProtectStatus": "ALLOW" }``

            :param country_code: The two-character code, in ISO 3166-1 alpha-2 format, for the country or region.
            :param protect_status: The types of protection that can be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-protectconfiguration-countryrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                country_rule_property = smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty(
                    country_code="countryCode",
                    protect_status="protectStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef393092fa94c184331bca8a4c94a8abd194d56c170e0633a5655047835bd28e)
                check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
                check_type(argname="argument protect_status", value=protect_status, expected_type=type_hints["protect_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if country_code is not None:
                self._values["country_code"] = country_code
            if protect_status is not None:
                self._values["protect_status"] = protect_status

        @builtins.property
        def country_code(self) -> typing.Optional[builtins.str]:
            '''The two-character code, in ISO 3166-1 alpha-2 format, for the country or region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-protectconfiguration-countryrule.html#cfn-smsvoice-protectconfiguration-countryrule-countrycode
            '''
            result = self._values.get("country_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protect_status(self) -> typing.Optional[builtins.str]:
            '''The types of protection that can be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-protectconfiguration-countryrule.html#cfn-smsvoice-protectconfiguration-countryrule-protectstatus
            '''
            result = self._values.get("protect_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CountryRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnProtectConfigurationPropsMixin.CountryRuleSetProperty",
        jsii_struct_bases=[],
        name_mapping={"mms": "mms", "sms": "sms", "voice": "voice"},
    )
    class CountryRuleSetProperty:
        def __init__(
            self,
            *,
            mms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProtectConfigurationPropsMixin.CountryRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            sms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProtectConfigurationPropsMixin.CountryRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            voice: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProtectConfigurationPropsMixin.CountryRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The set of ``CountryRules`` you specify to control which countries End User Messaging  can send your messages to.

            .. epigraph::

               If you don't specify all available ISO country codes in the ``CountryRuleSet`` for each number capability, the CloudFormation drift detection feature will detect drift. This is because End User Messaging  always returns all country codes.

            :param mms: The set of ``CountryRule`` s to control which destination countries End User Messaging can send your MMS messages to.
            :param sms: The set of ``CountryRule`` s to control which destination countries End User Messaging can send your SMS messages to.
            :param voice: The set of ``CountryRule`` s to control which destination countries End User Messaging can send your VOICE messages to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-protectconfiguration-countryruleset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
                
                country_rule_set_property = smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleSetProperty(
                    mms=[smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty(
                        country_code="countryCode",
                        protect_status="protectStatus"
                    )],
                    sms=[smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty(
                        country_code="countryCode",
                        protect_status="protectStatus"
                    )],
                    voice=[smsvoice_mixins.CfnProtectConfigurationPropsMixin.CountryRuleProperty(
                        country_code="countryCode",
                        protect_status="protectStatus"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef9d20308f9fb367bffe262a08e9d075c1b914412f96cf8fcf894aeba556da03)
                check_type(argname="argument mms", value=mms, expected_type=type_hints["mms"])
                check_type(argname="argument sms", value=sms, expected_type=type_hints["sms"])
                check_type(argname="argument voice", value=voice, expected_type=type_hints["voice"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mms is not None:
                self._values["mms"] = mms
            if sms is not None:
                self._values["sms"] = sms
            if voice is not None:
                self._values["voice"] = voice

        @builtins.property
        def mms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectConfigurationPropsMixin.CountryRuleProperty"]]]]:
            '''The set of ``CountryRule`` s to control which destination countries End User Messaging  can send your MMS messages to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-protectconfiguration-countryruleset.html#cfn-smsvoice-protectconfiguration-countryruleset-mms
            '''
            result = self._values.get("mms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectConfigurationPropsMixin.CountryRuleProperty"]]]], result)

        @builtins.property
        def sms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectConfigurationPropsMixin.CountryRuleProperty"]]]]:
            '''The set of ``CountryRule`` s to control which destination countries End User Messaging  can send your SMS messages to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-protectconfiguration-countryruleset.html#cfn-smsvoice-protectconfiguration-countryruleset-sms
            '''
            result = self._values.get("sms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectConfigurationPropsMixin.CountryRuleProperty"]]]], result)

        @builtins.property
        def voice(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectConfigurationPropsMixin.CountryRuleProperty"]]]]:
            '''The set of ``CountryRule`` s to control which destination countries End User Messaging  can send your VOICE messages to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-smsvoice-protectconfiguration-countryruleset.html#cfn-smsvoice-protectconfiguration-countryruleset-voice
            '''
            result = self._values.get("voice")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProtectConfigurationPropsMixin.CountryRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CountryRuleSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnResourcePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "resource_arn": "resourceArn"},
)
class CfnResourcePolicyMixinProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any = None,
        resource_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourcePolicyPropsMixin.

        :param policy_document: The JSON formatted resource-based policy to attach.
        :param resource_arn: The Amazon Resource Name (ARN) of the End User Messaging resource attached to the resource-based policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
            
            # policy_document: Any
            
            cfn_resource_policy_mixin_props = smsvoice_mixins.CfnResourcePolicyMixinProps(
                policy_document=policy_document,
                resource_arn="resourceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad577ad2a83d42b3e0d9b9133c724b83a40c7560d91ff008f6c2e41553fcf9b)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''The JSON formatted resource-based policy to attach.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-resourcepolicy.html#cfn-smsvoice-resourcepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the End User Messaging  resource attached to the resource-based policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-resourcepolicy.html#cfn-smsvoice-resourcepolicy-resourcearn
        '''
        result = self._values.get("resource_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourcePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnResourcePolicyPropsMixin",
):
    '''Attaches a resource-based policy to a End User Messaging  resource(phone number, sender Id, phone poll, or opt-out list) that is used for sharing the resource.

    A shared resource can be a Pool, Opt-out list, Sender Id, or Phone number. For more information about resource-based policies, see `Working with shared resources <https://docs.aws.amazon.com/sms-voice/latest/userguide/shared-resources.html>`_ in the *End User Messaging  User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-resourcepolicy.html
    :cloudformationResource: AWS::SMSVOICE::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
        
        # policy_document: Any
        
        cfn_resource_policy_props_mixin = smsvoice_mixins.CfnResourcePolicyPropsMixin(smsvoice_mixins.CfnResourcePolicyMixinProps(
            policy_document=policy_document,
            resource_arn="resourceArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SMSVOICE::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2b2e3074d8abd46e1e5e120acce92cb1763418a79d20aaf7b43526e75f6348)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9065b2d4c19efa6bf65ba09bd3591a0f7b10e252a6039e251dee17f73f6673a8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939a9c07368f391526fb2bce8a63b923b034a967f0b10658107b726c8e4cb981)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourcePolicyMixinProps:
        return typing.cast(CfnResourcePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnSenderIdMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "iso_country_code": "isoCountryCode",
        "sender_id": "senderId",
        "tags": "tags",
    },
)
class CfnSenderIdMixinProps:
    def __init__(
        self,
        *,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        iso_country_code: typing.Optional[builtins.str] = None,
        sender_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSenderIdPropsMixin.

        :param deletion_protection_enabled: By default this is set to false. When set to true the sender ID can't be deleted.
        :param iso_country_code: The two-character code, in ISO 3166-1 alpha-2 format, for the country or region.
        :param sender_id: The sender ID string to request.
        :param tags: An array of tags (key and value pairs) to associate with the sender ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-senderid.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
            
            cfn_sender_id_mixin_props = smsvoice_mixins.CfnSenderIdMixinProps(
                deletion_protection_enabled=False,
                iso_country_code="isoCountryCode",
                sender_id="senderId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cd210f68c16d1d14ab4b0408f0cbe5fe9deda425f4e151405e137ad275e8f4)
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument iso_country_code", value=iso_country_code, expected_type=type_hints["iso_country_code"])
            check_type(argname="argument sender_id", value=sender_id, expected_type=type_hints["sender_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if iso_country_code is not None:
            self._values["iso_country_code"] = iso_country_code
        if sender_id is not None:
            self._values["sender_id"] = sender_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''By default this is set to false.

        When set to true the sender ID can't be deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-senderid.html#cfn-smsvoice-senderid-deletionprotectionenabled
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def iso_country_code(self) -> typing.Optional[builtins.str]:
        '''The two-character code, in ISO 3166-1 alpha-2 format, for the country or region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-senderid.html#cfn-smsvoice-senderid-isocountrycode
        '''
        result = self._values.get("iso_country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sender_id(self) -> typing.Optional[builtins.str]:
        '''The sender ID string to request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-senderid.html#cfn-smsvoice-senderid-senderid
        '''
        result = self._values.get("sender_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of tags (key and value pairs) to associate with the sender ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-senderid.html#cfn-smsvoice-senderid-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSenderIdMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSenderIdPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_smsvoice.mixins.CfnSenderIdPropsMixin",
):
    '''Request a new sender ID that doesn't require registration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-smsvoice-senderid.html
    :cloudformationResource: AWS::SMSVOICE::SenderId
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_smsvoice import mixins as smsvoice_mixins
        
        cfn_sender_id_props_mixin = smsvoice_mixins.CfnSenderIdPropsMixin(smsvoice_mixins.CfnSenderIdMixinProps(
            deletion_protection_enabled=False,
            iso_country_code="isoCountryCode",
            sender_id="senderId",
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
        props: typing.Union[CfnSenderIdMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SMSVOICE::SenderId``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b9c81b10271ead31061db9092dbd821a5b3092d3cc96847a2d7d72eb0cdc6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59ba60038c43d834f58eac8c03181e54d5e7406eed9de8311bbe82e9ad7a0875)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae624646d9dd32b2f3d5c94cf9fc043e08edd9ea0d42a0e368095efd723f735a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSenderIdMixinProps:
        return typing.cast(CfnSenderIdMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnConfigurationSetMixinProps",
    "CfnConfigurationSetPropsMixin",
    "CfnOptOutListMixinProps",
    "CfnOptOutListPropsMixin",
    "CfnPhoneNumberMixinProps",
    "CfnPhoneNumberPropsMixin",
    "CfnPoolMixinProps",
    "CfnPoolPropsMixin",
    "CfnProtectConfigurationMixinProps",
    "CfnProtectConfigurationPropsMixin",
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
    "CfnSenderIdMixinProps",
    "CfnSenderIdPropsMixin",
]

publication.publish()

def _typecheckingstub__848d025486a637ceb43b72efed624f17dd6aabd02f778bceaa57f5394c164127(
    *,
    configuration_set_name: typing.Optional[builtins.str] = None,
    default_sender_id: typing.Optional[builtins.str] = None,
    event_destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.EventDestinationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    message_feedback_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    protect_configuration_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0188581aced88312d339a1948c7b55d4f4987b3fcfdd9112e7d360b2065559(
    props: typing.Union[CfnConfigurationSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab586677ddc3bea4c918642a92e2f3c656279dfdcd76d1cc5407c94a6518177c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86988af13a41e58ecd563410eb8ef58215dd1a58ef7b3569b406285768b695e7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb62299fd86c1ea8e7e0a89c202a71400cf2e489f4acd887bdfc978d4e42270a(
    *,
    iam_role_arn: typing.Optional[builtins.str] = None,
    log_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771c11cfeb2bfff769d8d9ab5d12775925919dde3ce558501006b0286595cbe7(
    *,
    cloud_watch_logs_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.CloudWatchLogsDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    event_destination_name: typing.Optional[builtins.str] = None,
    kinesis_firehose_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.KinesisFirehoseDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    matching_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    sns_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationSetPropsMixin.SnsDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7a9125a1693fcb10848630ccd45c002de62fb44e86c36d8470cb82566fc340(
    *,
    delivery_stream_arn: typing.Optional[builtins.str] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3336dbbae966f3ff0e9c754a747ff8650ed495a2c75679d9e3b9890d244ecc(
    *,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90dec4175b76ec19945dc9f8a30e0853d67d21262532207eb0b319cf1bb50ad(
    *,
    opt_out_list_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac61ab03459ef477146805efd61a230287d6531df80c198ea2d128a48a69f57c(
    props: typing.Union[CfnOptOutListMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47078d626030b6ee880f54a82531b57f8848605a94e8000b10aac76c26a67bc9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad94ffd3f7d0beb973d9d5599b7edc96b81eb1bed768109b4be160f6ae4cd402(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976ab8aaf05dcb7fad769dc075033092e2d8f86206cc562d80765ddd1a972437(
    *,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iso_country_code: typing.Optional[builtins.str] = None,
    mandatory_keywords: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPhoneNumberPropsMixin.MandatoryKeywordsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    number_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    number_type: typing.Optional[builtins.str] = None,
    optional_keywords: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPhoneNumberPropsMixin.OptionalKeywordProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    opt_out_list_name: typing.Optional[builtins.str] = None,
    self_managed_opt_outs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    two_way: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPhoneNumberPropsMixin.TwoWayProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16fd33fc198dde3f0279aa5b277549e9b71ce658594b66d1479cbb878257f55(
    props: typing.Union[CfnPhoneNumberMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d99f2a0e1c751b1ef5e31a04e71ef27b80b76267a2db7d4283947f3df4bde4c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d519ae428ac3c33d0d26e546bf100757a9d6dd59819ede4b3a577ada41a12ee0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4538a11877e70edffd4bc1def5be9e717fc9051dad83e03baf9dff020378ccca(
    *,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d640f13b8d5b69addf93502bf81436f3a0283db9a5d115233082dc5fb066f39(
    *,
    help: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPhoneNumberPropsMixin.MandatoryKeywordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stop: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPhoneNumberPropsMixin.MandatoryKeywordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8d3f32673869782cb40a129d9b1d7aeb4eb0e9a19450b32c0adc0eac3ecbe9(
    *,
    action: typing.Optional[builtins.str] = None,
    keyword: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0621adb44df8517352e42af5852a6bfd22e635f5bf70c2a8e66c28b79400fed2(
    *,
    channel_arn: typing.Optional[builtins.str] = None,
    channel_role: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e981a25a63a4a4c36645da4101db15f6819b6aaa256542e483aa1ff13cdb8268(
    *,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    mandatory_keywords: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPoolPropsMixin.MandatoryKeywordsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    optional_keywords: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPoolPropsMixin.OptionalKeywordProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    opt_out_list_name: typing.Optional[builtins.str] = None,
    origination_identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    self_managed_opt_outs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    shared_routes_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    two_way: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPoolPropsMixin.TwoWayProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12add5e705484a3d36ba61ff3df00186994eaee33dd83f8506b452f50a34fd1(
    props: typing.Union[CfnPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9b2bf53a6d31c55d98e1265f83a02394ab00cbac67cda4e7febc174cb3f849(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453ad7950cde0b93bc4189969a1e691677154f8b304df7bfafbbcf23de89707a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3983319a1d9d654bbf87584d02bbb9d2ce72825653f90a9f90eb18bdfdf3a79a(
    *,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1302d89148d6a269833275dd4a66db7b29103c9b490ecd6a62e4e9828d184e(
    *,
    help: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPoolPropsMixin.MandatoryKeywordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stop: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPoolPropsMixin.MandatoryKeywordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e728041cbef76a9622c9b181e87495f9bdfe0571921f03f9de5a4c02001092(
    *,
    action: typing.Optional[builtins.str] = None,
    keyword: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f3a8e4bb1a61fb6e92a7be5c44d750ed6429b9016502f89becc0b04cb1dfb1(
    *,
    channel_arn: typing.Optional[builtins.str] = None,
    channel_role: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e883a6cd58779a48213350242f8f0f9a0175122df3466ddecb283939d0e2c66(
    *,
    country_rule_set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProtectConfigurationPropsMixin.CountryRuleSetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfc7d7cb2cb19ef912cf9c8df6f5b8f938cda7fb479142fb4d76fdb5b1dc0a2(
    props: typing.Union[CfnProtectConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af52217205c3882e293b93be16f8f08989ff6e444578e357cd2a12bc246789c6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6699de6728ec6fd3b988b1c48f3d2f3185c3d6a0af303bd5fafce0cf60ec26(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef393092fa94c184331bca8a4c94a8abd194d56c170e0633a5655047835bd28e(
    *,
    country_code: typing.Optional[builtins.str] = None,
    protect_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9d20308f9fb367bffe262a08e9d075c1b914412f96cf8fcf894aeba556da03(
    *,
    mms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProtectConfigurationPropsMixin.CountryRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    sms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProtectConfigurationPropsMixin.CountryRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    voice: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProtectConfigurationPropsMixin.CountryRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad577ad2a83d42b3e0d9b9133c724b83a40c7560d91ff008f6c2e41553fcf9b(
    *,
    policy_document: typing.Any = None,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2b2e3074d8abd46e1e5e120acce92cb1763418a79d20aaf7b43526e75f6348(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9065b2d4c19efa6bf65ba09bd3591a0f7b10e252a6039e251dee17f73f6673a8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939a9c07368f391526fb2bce8a63b923b034a967f0b10658107b726c8e4cb981(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cd210f68c16d1d14ab4b0408f0cbe5fe9deda425f4e151405e137ad275e8f4(
    *,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iso_country_code: typing.Optional[builtins.str] = None,
    sender_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b9c81b10271ead31061db9092dbd821a5b3092d3cc96847a2d7d72eb0cdc6a(
    props: typing.Union[CfnSenderIdMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ba60038c43d834f58eac8c03181e54d5e7406eed9de8311bbe82e9ad7a0875(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae624646d9dd32b2f3d5c94cf9fc043e08edd9ea0d42a0e368095efd723f735a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
