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
    jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnLoggingConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_configuration": "destinationConfiguration",
        "name": "name",
        "tags": "tags",
    },
)
class CfnLoggingConfigurationMixinProps:
    def __init__(
        self,
        *,
        destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoggingConfigurationPropsMixin.DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLoggingConfigurationPropsMixin.

        :param destination_configuration: The DestinationConfiguration is a complex type that contains information about where chat content will be logged.
        :param name: Logging-configuration name. The value does not need to be unique.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
            
            cfn_logging_configuration_mixin_props = ivschat_mixins.CfnLoggingConfigurationMixinProps(
                destination_configuration=ivschat_mixins.CfnLoggingConfigurationPropsMixin.DestinationConfigurationProperty(
                    cloud_watch_logs=ivschat_mixins.CfnLoggingConfigurationPropsMixin.CloudWatchLogsDestinationConfigurationProperty(
                        log_group_name="logGroupName"
                    ),
                    firehose=ivschat_mixins.CfnLoggingConfigurationPropsMixin.FirehoseDestinationConfigurationProperty(
                        delivery_stream_name="deliveryStreamName"
                    ),
                    s3=ivschat_mixins.CfnLoggingConfigurationPropsMixin.S3DestinationConfigurationProperty(
                        bucket_name="bucketName"
                    )
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48a001194d657629cb55f128088adf74e99bbed088a5054e172bb9272cae5866)
            check_type(argname="argument destination_configuration", value=destination_configuration, expected_type=type_hints["destination_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_configuration is not None:
            self._values["destination_configuration"] = destination_configuration
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.DestinationConfigurationProperty"]]:
        '''The DestinationConfiguration is a complex type that contains information about where chat content will be logged.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration
        '''
        result = self._values.get("destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.DestinationConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Logging-configuration name.

        The value does not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoggingConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLoggingConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnLoggingConfigurationPropsMixin",
):
    '''The ``AWS::IVSChat::LoggingConfiguration`` resource specifies an  logging configuration that allows clients to store and record sent messages.

    For more information, see `CreateLoggingConfiguration <https://docs.aws.amazon.com/ivs/latest/ChatAPIReference/API_CreateLoggingConfiguration.html>`_ in the *Amazon Interactive Video Service Chat API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html
    :cloudformationResource: AWS::IVSChat::LoggingConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
        
        cfn_logging_configuration_props_mixin = ivschat_mixins.CfnLoggingConfigurationPropsMixin(ivschat_mixins.CfnLoggingConfigurationMixinProps(
            destination_configuration=ivschat_mixins.CfnLoggingConfigurationPropsMixin.DestinationConfigurationProperty(
                cloud_watch_logs=ivschat_mixins.CfnLoggingConfigurationPropsMixin.CloudWatchLogsDestinationConfigurationProperty(
                    log_group_name="logGroupName"
                ),
                firehose=ivschat_mixins.CfnLoggingConfigurationPropsMixin.FirehoseDestinationConfigurationProperty(
                    delivery_stream_name="deliveryStreamName"
                ),
                s3=ivschat_mixins.CfnLoggingConfigurationPropsMixin.S3DestinationConfigurationProperty(
                    bucket_name="bucketName"
                )
            ),
            name="name",
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
        props: typing.Union[CfnLoggingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVSChat::LoggingConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c789bfc796fcadeb4e102290ae4142cda039df63e20a00d2eb4d128fce26782)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40a01937d68fedf737ccbac825d63f53fded904539af6e0bd3c55b7ef67c1f26)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1013e66f8fc9b21204b8154edbc889cc5da5f7ce797fc2cdf5ce271331cad3a7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLoggingConfigurationMixinProps:
        return typing.cast(CfnLoggingConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnLoggingConfigurationPropsMixin.CloudWatchLogsDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class CloudWatchLogsDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The CloudWatchLogsDestinationConfiguration property type specifies a CloudWatch Logs location where chat logs will be stored.

            :param log_group_name: Name of the Amazon Cloudwatch Logs destination where chat activity will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-cloudwatchlogsdestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
                
                cloud_watch_logs_destination_configuration_property = ivschat_mixins.CfnLoggingConfigurationPropsMixin.CloudWatchLogsDestinationConfigurationProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6a0ee2ad83bbff1deda2b4ebf070ccb29773ae99865ec85a2e5105c55c593ed)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''Name of the Amazon Cloudwatch Logs destination where chat activity will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-cloudwatchlogsdestinationconfiguration.html#cfn-ivschat-loggingconfiguration-cloudwatchlogsdestinationconfiguration-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnLoggingConfigurationPropsMixin.DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs": "cloudWatchLogs",
            "firehose": "firehose",
            "s3": "s3",
        },
    )
    class DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoggingConfigurationPropsMixin.CloudWatchLogsDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            firehose: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoggingConfigurationPropsMixin.FirehoseDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoggingConfigurationPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The DestinationConfiguration property type describes a location where chat logs will be stored.

            Each member represents the configuration of one log destination. For logging, you define only one type of destination.

            :param cloud_watch_logs: An Amazon CloudWatch Logs destination configuration where chat activity will be logged.
            :param firehose: An Amazon Kinesis Data Firehose destination configuration where chat activity will be logged.
            :param s3: An Amazon S3 destination configuration where chat activity will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
                
                destination_configuration_property = ivschat_mixins.CfnLoggingConfigurationPropsMixin.DestinationConfigurationProperty(
                    cloud_watch_logs=ivschat_mixins.CfnLoggingConfigurationPropsMixin.CloudWatchLogsDestinationConfigurationProperty(
                        log_group_name="logGroupName"
                    ),
                    firehose=ivschat_mixins.CfnLoggingConfigurationPropsMixin.FirehoseDestinationConfigurationProperty(
                        delivery_stream_name="deliveryStreamName"
                    ),
                    s3=ivschat_mixins.CfnLoggingConfigurationPropsMixin.S3DestinationConfigurationProperty(
                        bucket_name="bucketName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71d347f6a2f147dcf14d941d56c2c041497466f8b5d151cf8e50d1b92eb27f44)
                check_type(argname="argument cloud_watch_logs", value=cloud_watch_logs, expected_type=type_hints["cloud_watch_logs"])
                check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs is not None:
                self._values["cloud_watch_logs"] = cloud_watch_logs
            if firehose is not None:
                self._values["firehose"] = firehose
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def cloud_watch_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.CloudWatchLogsDestinationConfigurationProperty"]]:
            '''An Amazon CloudWatch Logs destination configuration where chat activity will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration-cloudwatchlogs
            '''
            result = self._values.get("cloud_watch_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.CloudWatchLogsDestinationConfigurationProperty"]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.FirehoseDestinationConfigurationProperty"]]:
            '''An Amazon Kinesis Data Firehose destination configuration where chat activity will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.FirehoseDestinationConfigurationProperty"]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.S3DestinationConfigurationProperty"]]:
            '''An Amazon S3 destination configuration where chat activity will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.S3DestinationConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnLoggingConfigurationPropsMixin.FirehoseDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_stream_name": "deliveryStreamName"},
    )
    class FirehoseDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            delivery_stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The FirehoseDestinationConfiguration property type specifies a Kinesis Firehose location where chat logs will be stored.

            :param delivery_stream_name: Name of the Amazon Kinesis Firehose delivery stream where chat activity will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-firehosedestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
                
                firehose_destination_configuration_property = ivschat_mixins.CfnLoggingConfigurationPropsMixin.FirehoseDestinationConfigurationProperty(
                    delivery_stream_name="deliveryStreamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fde4f24d787f6a4bc2225637926ceecafb0c44b20465d921d966640fdfd36cf1)
                check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_stream_name is not None:
                self._values["delivery_stream_name"] = delivery_stream_name

        @builtins.property
        def delivery_stream_name(self) -> typing.Optional[builtins.str]:
            '''Name of the Amazon Kinesis Firehose delivery stream where chat activity will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-firehosedestinationconfiguration.html#cfn-ivschat-loggingconfiguration-firehosedestinationconfiguration-deliverystreamname
            '''
            result = self._values.get("delivery_stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnLoggingConfigurationPropsMixin.S3DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName"},
    )
    class S3DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3DestinationConfiguration property type specifies an S3 location where chat logs will be stored.

            :param bucket_name: Name of the Amazon S3 bucket where chat activity will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-s3destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
                
                s3_destination_configuration_property = ivschat_mixins.CfnLoggingConfigurationPropsMixin.S3DestinationConfigurationProperty(
                    bucket_name="bucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__391b6737da3ab6604a1a7689630a583c324ea7e69b28f823af760017deb97871)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Name of the Amazon S3 bucket where chat activity will be logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-s3destinationconfiguration.html#cfn-ivschat-loggingconfiguration-s3destinationconfiguration-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnRoomIvsChatLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnRoomIvsChatLogs",
):
    '''Builder for CfnRoomLogsMixin to generate IVS_CHAT_LOGS for CfnRoom.

    :cloudformationResource: AWS::IVSChat::Room
    :logType: IVS_CHAT_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
        
        cfn_room_ivs_chat_logs = ivschat_mixins.CfnRoomIvsChatLogs()
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
    ) -> "CfnRoomLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964fc065f8d788030bd87553c517f5dd179e29d5e920baba712a1b8d97e16cae)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnRoomLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnRoomLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf16885d07c2e2034c56d635f34c77e5c53eb26f133f46bf59faffdb9d93c258)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnRoomLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnRoomLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__239334597e3950c1c8a4096b06b85d6e56488f7088b4dcfd0146b8be851664b5)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnRoomLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnRoomLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnRoomLogsMixin",
):
    '''The ``AWS::IVSChat::Room`` resource specifies an  room that allows clients to connect and pass messages.

    For more information, see `CreateRoom <https://docs.aws.amazon.com/ivs/latest/ChatAPIReference/API_CreateRoom.html>`_ in the *Amazon Interactive Video Service Chat API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html
    :cloudformationResource: AWS::IVSChat::Room
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_room_logs_mixin = ivschat_mixins.CfnRoomLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::IVSChat::Room``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d096f6313b36083a367b6f143d55894b9d3786e937e89b182804a65e438da8c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbb9c982365bc47dcf9869ea5bb93bd2a69f8eb47c081ae008c189bcf47cbf17)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ef08afd0dc0d163df2d4696463b9537ac8c720dd4224685f91b4fc956b4672)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IVS_CHAT_LOGS")
    def IVS_CHAT_LOGS(cls) -> CfnRoomIvsChatLogs:
        return typing.cast(CfnRoomIvsChatLogs, jsii.sget(cls, "IVS_CHAT_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnRoomMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "logging_configuration_identifiers": "loggingConfigurationIdentifiers",
        "maximum_message_length": "maximumMessageLength",
        "maximum_message_rate_per_second": "maximumMessageRatePerSecond",
        "message_review_handler": "messageReviewHandler",
        "name": "name",
        "tags": "tags",
    },
)
class CfnRoomMixinProps:
    def __init__(
        self,
        *,
        logging_configuration_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        maximum_message_length: typing.Optional[jsii.Number] = None,
        maximum_message_rate_per_second: typing.Optional[jsii.Number] = None,
        message_review_handler: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoomPropsMixin.MessageReviewHandlerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRoomPropsMixin.

        :param logging_configuration_identifiers: List of logging-configuration identifiers attached to the room.
        :param maximum_message_length: Maximum number of characters in a single message. Messages are expected to be UTF-8 encoded and this limit applies specifically to rune/code-point count, not number of bytes. Default: - 500
        :param maximum_message_rate_per_second: Maximum number of messages per second that can be sent to the room (by all clients). Default: - 10
        :param message_review_handler: Configuration information for optional review of messages.
        :param name: Room name. The value does not need to be unique.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-room-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
            
            cfn_room_mixin_props = ivschat_mixins.CfnRoomMixinProps(
                logging_configuration_identifiers=["loggingConfigurationIdentifiers"],
                maximum_message_length=123,
                maximum_message_rate_per_second=123,
                message_review_handler=ivschat_mixins.CfnRoomPropsMixin.MessageReviewHandlerProperty(
                    fallback_result="fallbackResult",
                    uri="uri"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd2990ac5b0d833ef3f7bc9b52d0e221ab8383274683b0c4d26e4b71c2ae158)
            check_type(argname="argument logging_configuration_identifiers", value=logging_configuration_identifiers, expected_type=type_hints["logging_configuration_identifiers"])
            check_type(argname="argument maximum_message_length", value=maximum_message_length, expected_type=type_hints["maximum_message_length"])
            check_type(argname="argument maximum_message_rate_per_second", value=maximum_message_rate_per_second, expected_type=type_hints["maximum_message_rate_per_second"])
            check_type(argname="argument message_review_handler", value=message_review_handler, expected_type=type_hints["message_review_handler"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if logging_configuration_identifiers is not None:
            self._values["logging_configuration_identifiers"] = logging_configuration_identifiers
        if maximum_message_length is not None:
            self._values["maximum_message_length"] = maximum_message_length
        if maximum_message_rate_per_second is not None:
            self._values["maximum_message_rate_per_second"] = maximum_message_rate_per_second
        if message_review_handler is not None:
            self._values["message_review_handler"] = message_review_handler
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def logging_configuration_identifiers(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''List of logging-configuration identifiers attached to the room.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-loggingconfigurationidentifiers
        '''
        result = self._values.get("logging_configuration_identifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def maximum_message_length(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of characters in a single message.

        Messages are expected to be UTF-8 encoded and this limit applies specifically to rune/code-point count, not number of bytes.

        :default: - 500

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-maximummessagelength
        '''
        result = self._values.get("maximum_message_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_message_rate_per_second(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of messages per second that can be sent to the room (by all clients).

        :default: - 10

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-maximummessageratepersecond
        '''
        result = self._values.get("maximum_message_rate_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def message_review_handler(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoomPropsMixin.MessageReviewHandlerProperty"]]:
        '''Configuration information for optional review of messages.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-messagereviewhandler
        '''
        result = self._values.get("message_review_handler")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoomPropsMixin.MessageReviewHandlerProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Room name.

        The value does not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-room-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRoomMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRoomPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnRoomPropsMixin",
):
    '''The ``AWS::IVSChat::Room`` resource specifies an  room that allows clients to connect and pass messages.

    For more information, see `CreateRoom <https://docs.aws.amazon.com/ivs/latest/ChatAPIReference/API_CreateRoom.html>`_ in the *Amazon Interactive Video Service Chat API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html
    :cloudformationResource: AWS::IVSChat::Room
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
        
        cfn_room_props_mixin = ivschat_mixins.CfnRoomPropsMixin(ivschat_mixins.CfnRoomMixinProps(
            logging_configuration_identifiers=["loggingConfigurationIdentifiers"],
            maximum_message_length=123,
            maximum_message_rate_per_second=123,
            message_review_handler=ivschat_mixins.CfnRoomPropsMixin.MessageReviewHandlerProperty(
                fallback_result="fallbackResult",
                uri="uri"
            ),
            name="name",
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
        props: typing.Union[CfnRoomMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVSChat::Room``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a441d47d5dbf4fcc90ac7e48961e585307874074a947973fceb4944d4f6ac84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32643ff32c5d7e333d0d0d903c4973d33da6881f840feb21c18dab1b2c4eeb49)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ada8a9ad4ab34855b1e6097324cb085c698894f09008677a59b84c27d64317)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRoomMixinProps:
        return typing.cast(CfnRoomMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivschat.mixins.CfnRoomPropsMixin.MessageReviewHandlerProperty",
        jsii_struct_bases=[],
        name_mapping={"fallback_result": "fallbackResult", "uri": "uri"},
    )
    class MessageReviewHandlerProperty:
        def __init__(
            self,
            *,
            fallback_result: typing.Optional[builtins.str] = None,
            uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The MessageReviewHandler property type specifies configuration information for optional message review.

            :param fallback_result: Specifies the fallback behavior (whether the message is allowed or denied) if the handler does not return a valid response, encounters an error, or times out. (For the timeout period, see `Service Quotas <https://docs.aws.amazon.com/ivs/latest/userguide/service-quotas.html>`_ .) If allowed, the message is delivered with returned content to all users connected to the room. If denied, the message is not delivered to any user. *Default* : ``ALLOW`` Default: - "ALLOW"
            :param uri: Identifier of the message review handler. Currently this must be an ARN of a lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-room-messagereviewhandler.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivschat import mixins as ivschat_mixins
                
                message_review_handler_property = ivschat_mixins.CfnRoomPropsMixin.MessageReviewHandlerProperty(
                    fallback_result="fallbackResult",
                    uri="uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2a66ad526391dec7db2cb40635a2ee141c047a220fde8ee9aa23f748aa39ba5)
                check_type(argname="argument fallback_result", value=fallback_result, expected_type=type_hints["fallback_result"])
                check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fallback_result is not None:
                self._values["fallback_result"] = fallback_result
            if uri is not None:
                self._values["uri"] = uri

        @builtins.property
        def fallback_result(self) -> typing.Optional[builtins.str]:
            '''Specifies the fallback behavior (whether the message is allowed or denied) if the handler does not return a valid response, encounters an error, or times out.

            (For the timeout period, see `Service Quotas <https://docs.aws.amazon.com/ivs/latest/userguide/service-quotas.html>`_ .) If allowed, the message is delivered with returned content to all users connected to the room. If denied, the message is not delivered to any user.

            *Default* : ``ALLOW``

            :default: - "ALLOW"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-room-messagereviewhandler.html#cfn-ivschat-room-messagereviewhandler-fallbackresult
            '''
            result = self._values.get("fallback_result")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uri(self) -> typing.Optional[builtins.str]:
            '''Identifier of the message review handler.

            Currently this must be an ARN of a lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-room-messagereviewhandler.html#cfn-ivschat-room-messagereviewhandler-uri
            '''
            result = self._values.get("uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageReviewHandlerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnLoggingConfigurationMixinProps",
    "CfnLoggingConfigurationPropsMixin",
    "CfnRoomIvsChatLogs",
    "CfnRoomLogsMixin",
    "CfnRoomMixinProps",
    "CfnRoomPropsMixin",
]

publication.publish()

def _typecheckingstub__48a001194d657629cb55f128088adf74e99bbed088a5054e172bb9272cae5866(
    *,
    destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoggingConfigurationPropsMixin.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c789bfc796fcadeb4e102290ae4142cda039df63e20a00d2eb4d128fce26782(
    props: typing.Union[CfnLoggingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a01937d68fedf737ccbac825d63f53fded904539af6e0bd3c55b7ef67c1f26(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1013e66f8fc9b21204b8154edbc889cc5da5f7ce797fc2cdf5ce271331cad3a7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a0ee2ad83bbff1deda2b4ebf070ccb29773ae99865ec85a2e5105c55c593ed(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d347f6a2f147dcf14d941d56c2c041497466f8b5d151cf8e50d1b92eb27f44(
    *,
    cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoggingConfigurationPropsMixin.CloudWatchLogsDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    firehose: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoggingConfigurationPropsMixin.FirehoseDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoggingConfigurationPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde4f24d787f6a4bc2225637926ceecafb0c44b20465d921d966640fdfd36cf1(
    *,
    delivery_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391b6737da3ab6604a1a7689630a583c324ea7e69b28f823af760017deb97871(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964fc065f8d788030bd87553c517f5dd179e29d5e920baba712a1b8d97e16cae(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf16885d07c2e2034c56d635f34c77e5c53eb26f133f46bf59faffdb9d93c258(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239334597e3950c1c8a4096b06b85d6e56488f7088b4dcfd0146b8be851664b5(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d096f6313b36083a367b6f143d55894b9d3786e937e89b182804a65e438da8c1(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb9c982365bc47dcf9869ea5bb93bd2a69f8eb47c081ae008c189bcf47cbf17(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ef08afd0dc0d163df2d4696463b9537ac8c720dd4224685f91b4fc956b4672(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd2990ac5b0d833ef3f7bc9b52d0e221ab8383274683b0c4d26e4b71c2ae158(
    *,
    logging_configuration_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_message_length: typing.Optional[jsii.Number] = None,
    maximum_message_rate_per_second: typing.Optional[jsii.Number] = None,
    message_review_handler: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoomPropsMixin.MessageReviewHandlerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a441d47d5dbf4fcc90ac7e48961e585307874074a947973fceb4944d4f6ac84(
    props: typing.Union[CfnRoomMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32643ff32c5d7e333d0d0d903c4973d33da6881f840feb21c18dab1b2c4eeb49(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ada8a9ad4ab34855b1e6097324cb085c698894f09008677a59b84c27d64317(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a66ad526391dec7db2cb40635a2ee141c047a220fde8ee9aa23f748aa39ba5(
    *,
    fallback_result: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
