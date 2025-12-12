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
    jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_name": "channelName",
        "channel_storage": "channelStorage",
        "retention_period": "retentionPeriod",
        "tags": "tags",
    },
)
class CfnChannelMixinProps:
    def __init__(
        self,
        *,
        channel_name: typing.Optional[builtins.str] = None,
        channel_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.ChannelStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        retention_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.RetentionPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnChannelPropsMixin.

        :param channel_name: The name of the channel.
        :param channel_storage: Where channel data is stored.
        :param retention_period: How long, in days, message data is kept for the channel.
        :param tags: Metadata which can be used to manage the channel. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
            
            # service_managed_s3: Any
            
            cfn_channel_mixin_props = iotanalytics_mixins.CfnChannelMixinProps(
                channel_name="channelName",
                channel_storage=iotanalytics_mixins.CfnChannelPropsMixin.ChannelStorageProperty(
                    customer_managed_s3=iotanalytics_mixins.CfnChannelPropsMixin.CustomerManagedS3Property(
                        bucket="bucket",
                        key_prefix="keyPrefix",
                        role_arn="roleArn"
                    ),
                    service_managed_s3=service_managed_s3
                ),
                retention_period=iotanalytics_mixins.CfnChannelPropsMixin.RetentionPeriodProperty(
                    number_of_days=123,
                    unlimited=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f8e27d38bcc140badd0a57bf414295162b53fe0dbc87ea8c6454424e1ec3c6)
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument channel_storage", value=channel_storage, expected_type=type_hints["channel_storage"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if channel_storage is not None:
            self._values["channel_storage"] = channel_storage
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channel_storage(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.ChannelStorageProperty"]]:
        '''Where channel data is stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-channelstorage
        '''
        result = self._values.get("channel_storage")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.ChannelStorageProperty"]], result)

    @builtins.property
    def retention_period(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.RetentionPeriodProperty"]]:
        '''How long, in days, message data is kept for the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-retentionperiod
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.RetentionPeriodProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata which can be used to manage the channel.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnChannelPropsMixin",
):
    '''The AWS::IoTAnalytics::Channel resource collects data from an MQTT topic and archives the raw, unprocessed messages before publishing the data to a pipeline.

    For more information, see `How to Use AWS IoT Analytics <https://docs.aws.amazon.com/iotanalytics/latest/userguide/welcome.html#aws-iot-analytics-how>`_ in the *AWS IoT Analytics User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html
    :cloudformationResource: AWS::IoTAnalytics::Channel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
        
        # service_managed_s3: Any
        
        cfn_channel_props_mixin = iotanalytics_mixins.CfnChannelPropsMixin(iotanalytics_mixins.CfnChannelMixinProps(
            channel_name="channelName",
            channel_storage=iotanalytics_mixins.CfnChannelPropsMixin.ChannelStorageProperty(
                customer_managed_s3=iotanalytics_mixins.CfnChannelPropsMixin.CustomerManagedS3Property(
                    bucket="bucket",
                    key_prefix="keyPrefix",
                    role_arn="roleArn"
                ),
                service_managed_s3=service_managed_s3
            ),
            retention_period=iotanalytics_mixins.CfnChannelPropsMixin.RetentionPeriodProperty(
                number_of_days=123,
                unlimited=False
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
        props: typing.Union[CfnChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTAnalytics::Channel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef344f8e7ce27f11c73da05e5111a9df775ec09e9320f888f6d5f33ab97b73a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c5f9cd143fb25595c21fc41931e6170967829107335b615208efcdbbcbce138)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6611f1b8a588a843ccc3c4394bb82855cfd1d7e29e473db8ce4107d6de92e26b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnChannelMixinProps:
        return typing.cast(CfnChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnChannelPropsMixin.ChannelStorageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_managed_s3": "customerManagedS3",
            "service_managed_s3": "serviceManagedS3",
        },
    )
    class ChannelStorageProperty:
        def __init__(
            self,
            *,
            customer_managed_s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.CustomerManagedS3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_managed_s3: typing.Any = None,
        ) -> None:
            '''Where channel data is stored.

            You may choose one of ``serviceManagedS3`` , ``customerManagedS3`` storage. If not specified, the default is ``serviceManagedS3`` . This can't be changed after creation of the channel.

            :param customer_managed_s3: Used to store channel data in an S3 bucket that you manage. If customer managed storage is selected, the ``retentionPeriod`` parameter is ignored. You can't change the choice of S3 storage after the data store is created.
            :param service_managed_s3: Used to store channel data in an S3 bucket managed by AWS IoT Analytics . You can't change the choice of S3 storage after the data store is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-channelstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                # service_managed_s3: Any
                
                channel_storage_property = iotanalytics_mixins.CfnChannelPropsMixin.ChannelStorageProperty(
                    customer_managed_s3=iotanalytics_mixins.CfnChannelPropsMixin.CustomerManagedS3Property(
                        bucket="bucket",
                        key_prefix="keyPrefix",
                        role_arn="roleArn"
                    ),
                    service_managed_s3=service_managed_s3
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f143154be19135037fe63eff78c141e426ac3caf7ca3dd060a3164025978d6c)
                check_type(argname="argument customer_managed_s3", value=customer_managed_s3, expected_type=type_hints["customer_managed_s3"])
                check_type(argname="argument service_managed_s3", value=service_managed_s3, expected_type=type_hints["service_managed_s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_managed_s3 is not None:
                self._values["customer_managed_s3"] = customer_managed_s3
            if service_managed_s3 is not None:
                self._values["service_managed_s3"] = service_managed_s3

        @builtins.property
        def customer_managed_s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.CustomerManagedS3Property"]]:
            '''Used to store channel data in an S3 bucket that you manage.

            If customer managed storage is selected, the ``retentionPeriod`` parameter is ignored. You can't change the choice of S3 storage after the data store is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-channelstorage.html#cfn-iotanalytics-channel-channelstorage-customermanageds3
            '''
            result = self._values.get("customer_managed_s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.CustomerManagedS3Property"]], result)

        @builtins.property
        def service_managed_s3(self) -> typing.Any:
            '''Used to store channel data in an S3 bucket managed by AWS IoT Analytics .

            You can't change the choice of S3 storage after the data store is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-channelstorage.html#cfn-iotanalytics-channel-channelstorage-servicemanageds3
            '''
            result = self._values.get("service_managed_s3")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnChannelPropsMixin.CustomerManagedS3Property",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key_prefix": "keyPrefix",
            "role_arn": "roleArn",
        },
    )
    class CustomerManagedS3Property:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key_prefix: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used to store channel data in an S3 bucket that you manage.

            :param bucket: The name of the S3 bucket in which channel data is stored.
            :param key_prefix: (Optional) The prefix used to create the keys of the channel data objects. Each object in an S3 bucket has a key that is its unique identifier within the bucket (each object in a bucket has exactly one key). The prefix must end with a forward slash (/).
            :param role_arn: The ARN of the role that grants AWS IoT Analytics permission to interact with your Amazon S3 resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-customermanageds3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                customer_managed_s3_property = iotanalytics_mixins.CfnChannelPropsMixin.CustomerManagedS3Property(
                    bucket="bucket",
                    key_prefix="keyPrefix",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__354d5a36352656917d5d9133944fce6737e8249689042080ea9dd6abe74616e0)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key_prefix is not None:
                self._values["key_prefix"] = key_prefix
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket in which channel data is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-customermanageds3.html#cfn-iotanalytics-channel-customermanageds3-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_prefix(self) -> typing.Optional[builtins.str]:
            '''(Optional) The prefix used to create the keys of the channel data objects.

            Each object in an S3 bucket has a key that is its unique identifier within the bucket (each object in a bucket has exactly one key). The prefix must end with a forward slash (/).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-customermanageds3.html#cfn-iotanalytics-channel-customermanageds3-keyprefix
            '''
            result = self._values.get("key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that grants AWS IoT Analytics permission to interact with your Amazon S3 resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-customermanageds3.html#cfn-iotanalytics-channel-customermanageds3-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerManagedS3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnChannelPropsMixin.RetentionPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"number_of_days": "numberOfDays", "unlimited": "unlimited"},
    )
    class RetentionPeriodProperty:
        def __init__(
            self,
            *,
            number_of_days: typing.Optional[jsii.Number] = None,
            unlimited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''How long, in days, message data is kept.

            :param number_of_days: The number of days that message data is kept. The ``unlimited`` parameter must be false.
            :param unlimited: If true, message data is kept indefinitely.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-retentionperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                retention_period_property = iotanalytics_mixins.CfnChannelPropsMixin.RetentionPeriodProperty(
                    number_of_days=123,
                    unlimited=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc5e321365eaf618a11ee8d7352df06797351f189b5c9397d3061a7290412701)
                check_type(argname="argument number_of_days", value=number_of_days, expected_type=type_hints["number_of_days"])
                check_type(argname="argument unlimited", value=unlimited, expected_type=type_hints["unlimited"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if number_of_days is not None:
                self._values["number_of_days"] = number_of_days
            if unlimited is not None:
                self._values["unlimited"] = unlimited

        @builtins.property
        def number_of_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days that message data is kept.

            The ``unlimited`` parameter must be false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-retentionperiod.html#cfn-iotanalytics-channel-retentionperiod-numberofdays
            '''
            result = self._values.get("number_of_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unlimited(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If true, message data is kept indefinitely.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-retentionperiod.html#cfn-iotanalytics-channel-retentionperiod-unlimited
            '''
            result = self._values.get("unlimited")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "content_delivery_rules": "contentDeliveryRules",
        "dataset_name": "datasetName",
        "late_data_rules": "lateDataRules",
        "retention_period": "retentionPeriod",
        "tags": "tags",
        "triggers": "triggers",
        "versioning_configuration": "versioningConfiguration",
    },
)
class CfnDatasetMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        content_delivery_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DatasetContentDeliveryRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        dataset_name: typing.Optional[builtins.str] = None,
        late_data_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.LateDataRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        retention_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.RetentionPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        triggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.TriggerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        versioning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.VersioningConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDatasetPropsMixin.

        :param actions: The ``DatasetAction`` objects that automatically create the dataset contents.
        :param content_delivery_rules: When dataset contents are created they are delivered to destinations specified here.
        :param dataset_name: The name of the dataset.
        :param late_data_rules: A list of data rules that send notifications to CloudWatch, when data arrives late. To specify ``lateDataRules`` , the dataset must use a `DeltaTimer <https://docs.aws.amazon.com/iotanalytics/latest/APIReference/API_DeltaTime.html>`_ filter.
        :param retention_period: Optional. How long, in days, message data is kept for the dataset.
        :param tags: Metadata which can be used to manage the data set. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param triggers: The ``DatasetTrigger`` objects that specify when the dataset is automatically updated.
        :param versioning_configuration: Optional. How many versions of dataset contents are kept. If not specified or set to null, only the latest version plus the latest succeeded version (if they are different) are kept for the time period specified by the ``retentionPeriod`` parameter. For more information, see `Keeping Multiple Versions of AWS IoT Analytics datasets <https://docs.aws.amazon.com/iotanalytics/latest/userguide/getting-started.html#aws-iot-analytics-dataset-versions>`_ in the *AWS IoT Analytics User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
            
            cfn_dataset_mixin_props = iotanalytics_mixins.CfnDatasetMixinProps(
                actions=[iotanalytics_mixins.CfnDatasetPropsMixin.ActionProperty(
                    action_name="actionName",
                    container_action=iotanalytics_mixins.CfnDatasetPropsMixin.ContainerActionProperty(
                        execution_role_arn="executionRoleArn",
                        image="image",
                        resource_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.ResourceConfigurationProperty(
                            compute_type="computeType",
                            volume_size_in_gb=123
                        ),
                        variables=[iotanalytics_mixins.CfnDatasetPropsMixin.VariableProperty(
                            dataset_content_version_value=iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentVersionValueProperty(
                                dataset_name="datasetName"
                            ),
                            double_value=123,
                            output_file_uri_value=iotanalytics_mixins.CfnDatasetPropsMixin.OutputFileUriValueProperty(
                                file_name="fileName"
                            ),
                            string_value="stringValue",
                            variable_name="variableName"
                        )]
                    ),
                    query_action=iotanalytics_mixins.CfnDatasetPropsMixin.QueryActionProperty(
                        filters=[iotanalytics_mixins.CfnDatasetPropsMixin.FilterProperty(
                            delta_time=iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeProperty(
                                offset_seconds=123,
                                time_expression="timeExpression"
                            )
                        )],
                        sql_query="sqlQuery"
                    )
                )],
                content_delivery_rules=[iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentDeliveryRuleProperty(
                    destination=iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentDeliveryRuleDestinationProperty(
                        iot_events_destination_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.IotEventsDestinationConfigurationProperty(
                            input_name="inputName",
                            role_arn="roleArn"
                        ),
                        s3_destination_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.S3DestinationConfigurationProperty(
                            bucket="bucket",
                            glue_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.GlueConfigurationProperty(
                                database_name="databaseName",
                                table_name="tableName"
                            ),
                            key="key",
                            role_arn="roleArn"
                        )
                    ),
                    entry_name="entryName"
                )],
                dataset_name="datasetName",
                late_data_rules=[iotanalytics_mixins.CfnDatasetPropsMixin.LateDataRuleProperty(
                    rule_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.LateDataRuleConfigurationProperty(
                        delta_time_session_window_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeSessionWindowConfigurationProperty(
                            timeout_in_minutes=123
                        )
                    ),
                    rule_name="ruleName"
                )],
                retention_period=iotanalytics_mixins.CfnDatasetPropsMixin.RetentionPeriodProperty(
                    number_of_days=123,
                    unlimited=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                triggers=[iotanalytics_mixins.CfnDatasetPropsMixin.TriggerProperty(
                    schedule=iotanalytics_mixins.CfnDatasetPropsMixin.ScheduleProperty(
                        schedule_expression="scheduleExpression"
                    ),
                    triggering_dataset=iotanalytics_mixins.CfnDatasetPropsMixin.TriggeringDatasetProperty(
                        dataset_name="datasetName"
                    )
                )],
                versioning_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.VersioningConfigurationProperty(
                    max_versions=123,
                    unlimited=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf172f8d1d995cfb26cb76bcd1c8d908e8042e3628e9e896fda41b121e4fe7b0)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument content_delivery_rules", value=content_delivery_rules, expected_type=type_hints["content_delivery_rules"])
            check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
            check_type(argname="argument late_data_rules", value=late_data_rules, expected_type=type_hints["late_data_rules"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
            check_type(argname="argument versioning_configuration", value=versioning_configuration, expected_type=type_hints["versioning_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if content_delivery_rules is not None:
            self._values["content_delivery_rules"] = content_delivery_rules
        if dataset_name is not None:
            self._values["dataset_name"] = dataset_name
        if late_data_rules is not None:
            self._values["late_data_rules"] = late_data_rules
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if tags is not None:
            self._values["tags"] = tags
        if triggers is not None:
            self._values["triggers"] = triggers
        if versioning_configuration is not None:
            self._values["versioning_configuration"] = versioning_configuration

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.ActionProperty"]]]]:
        '''The ``DatasetAction`` objects that automatically create the dataset contents.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.ActionProperty"]]]], result)

    @builtins.property
    def content_delivery_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetContentDeliveryRuleProperty"]]]]:
        '''When dataset contents are created they are delivered to destinations specified here.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-contentdeliveryrules
        '''
        result = self._values.get("content_delivery_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetContentDeliveryRuleProperty"]]]], result)

    @builtins.property
    def dataset_name(self) -> typing.Optional[builtins.str]:
        '''The name of the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-datasetname
        '''
        result = self._values.get("dataset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def late_data_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.LateDataRuleProperty"]]]]:
        '''A list of data rules that send notifications to CloudWatch, when data arrives late.

        To specify ``lateDataRules`` , the dataset must use a `DeltaTimer <https://docs.aws.amazon.com/iotanalytics/latest/APIReference/API_DeltaTime.html>`_ filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-latedatarules
        '''
        result = self._values.get("late_data_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.LateDataRuleProperty"]]]], result)

    @builtins.property
    def retention_period(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.RetentionPeriodProperty"]]:
        '''Optional.

        How long, in days, message data is kept for the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-retentionperiod
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.RetentionPeriodProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata which can be used to manage the data set.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def triggers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.TriggerProperty"]]]]:
        '''The ``DatasetTrigger`` objects that specify when the dataset is automatically updated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-triggers
        '''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.TriggerProperty"]]]], result)

    @builtins.property
    def versioning_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.VersioningConfigurationProperty"]]:
        '''Optional.

        How many versions of dataset contents are kept. If not specified or set to null, only the latest version plus the latest succeeded version (if they are different) are kept for the time period specified by the ``retentionPeriod`` parameter. For more information, see `Keeping Multiple Versions of AWS IoT Analytics datasets <https://docs.aws.amazon.com/iotanalytics/latest/userguide/getting-started.html#aws-iot-analytics-dataset-versions>`_ in the *AWS IoT Analytics User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-versioningconfiguration
        '''
        result = self._values.get("versioning_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.VersioningConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDatasetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin",
):
    '''The AWS::IoTAnalytics::Dataset resource stores data retrieved from a data store by applying a ``queryAction`` (an SQL query) or a ``containerAction`` (executing a containerized application).

    The data set can be populated manually by calling ``CreateDatasetContent`` or automatically according to a ``trigger`` you specify. For more information, see `How to Use AWS IoT Analytics <https://docs.aws.amazon.com/iotanalytics/latest/userguide/welcome.html#aws-iot-analytics-how>`_ in the *AWS IoT Analytics User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html
    :cloudformationResource: AWS::IoTAnalytics::Dataset
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
        
        cfn_dataset_props_mixin = iotanalytics_mixins.CfnDatasetPropsMixin(iotanalytics_mixins.CfnDatasetMixinProps(
            actions=[iotanalytics_mixins.CfnDatasetPropsMixin.ActionProperty(
                action_name="actionName",
                container_action=iotanalytics_mixins.CfnDatasetPropsMixin.ContainerActionProperty(
                    execution_role_arn="executionRoleArn",
                    image="image",
                    resource_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.ResourceConfigurationProperty(
                        compute_type="computeType",
                        volume_size_in_gb=123
                    ),
                    variables=[iotanalytics_mixins.CfnDatasetPropsMixin.VariableProperty(
                        dataset_content_version_value=iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentVersionValueProperty(
                            dataset_name="datasetName"
                        ),
                        double_value=123,
                        output_file_uri_value=iotanalytics_mixins.CfnDatasetPropsMixin.OutputFileUriValueProperty(
                            file_name="fileName"
                        ),
                        string_value="stringValue",
                        variable_name="variableName"
                    )]
                ),
                query_action=iotanalytics_mixins.CfnDatasetPropsMixin.QueryActionProperty(
                    filters=[iotanalytics_mixins.CfnDatasetPropsMixin.FilterProperty(
                        delta_time=iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeProperty(
                            offset_seconds=123,
                            time_expression="timeExpression"
                        )
                    )],
                    sql_query="sqlQuery"
                )
            )],
            content_delivery_rules=[iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentDeliveryRuleProperty(
                destination=iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentDeliveryRuleDestinationProperty(
                    iot_events_destination_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.IotEventsDestinationConfigurationProperty(
                        input_name="inputName",
                        role_arn="roleArn"
                    ),
                    s3_destination_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.S3DestinationConfigurationProperty(
                        bucket="bucket",
                        glue_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.GlueConfigurationProperty(
                            database_name="databaseName",
                            table_name="tableName"
                        ),
                        key="key",
                        role_arn="roleArn"
                    )
                ),
                entry_name="entryName"
            )],
            dataset_name="datasetName",
            late_data_rules=[iotanalytics_mixins.CfnDatasetPropsMixin.LateDataRuleProperty(
                rule_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.LateDataRuleConfigurationProperty(
                    delta_time_session_window_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeSessionWindowConfigurationProperty(
                        timeout_in_minutes=123
                    )
                ),
                rule_name="ruleName"
            )],
            retention_period=iotanalytics_mixins.CfnDatasetPropsMixin.RetentionPeriodProperty(
                number_of_days=123,
                unlimited=False
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            triggers=[iotanalytics_mixins.CfnDatasetPropsMixin.TriggerProperty(
                schedule=iotanalytics_mixins.CfnDatasetPropsMixin.ScheduleProperty(
                    schedule_expression="scheduleExpression"
                ),
                triggering_dataset=iotanalytics_mixins.CfnDatasetPropsMixin.TriggeringDatasetProperty(
                    dataset_name="datasetName"
                )
            )],
            versioning_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.VersioningConfigurationProperty(
                max_versions=123,
                unlimited=False
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTAnalytics::Dataset``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf6f89b8c14212170fcd4160573b43c2e2cafeb32ce768374095ca6eeb567c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e046d450189de573e65c06137b6de447a75ab1603dbb2b2eb20ab6a12cf0795c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9565f55fe367dad4c7879a5525c039d88b4ebda5161f6de0be9a60a48b99b3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDatasetMixinProps:
        return typing.cast(CfnDatasetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_name": "actionName",
            "container_action": "containerAction",
            "query_action": "queryAction",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            action_name: typing.Optional[builtins.str] = None,
            container_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.ContainerActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            query_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.QueryActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information needed to run the "containerAction" to produce data set contents.

            :param action_name: The name of the data set action by which data set contents are automatically created.
            :param container_action: Information which allows the system to run a containerized application in order to create the data set contents. The application must be in a Docker container along with any needed support libraries.
            :param query_action: An "SqlQueryDatasetAction" object that uses an SQL query to automatically create data set contents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                action_property = iotanalytics_mixins.CfnDatasetPropsMixin.ActionProperty(
                    action_name="actionName",
                    container_action=iotanalytics_mixins.CfnDatasetPropsMixin.ContainerActionProperty(
                        execution_role_arn="executionRoleArn",
                        image="image",
                        resource_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.ResourceConfigurationProperty(
                            compute_type="computeType",
                            volume_size_in_gb=123
                        ),
                        variables=[iotanalytics_mixins.CfnDatasetPropsMixin.VariableProperty(
                            dataset_content_version_value=iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentVersionValueProperty(
                                dataset_name="datasetName"
                            ),
                            double_value=123,
                            output_file_uri_value=iotanalytics_mixins.CfnDatasetPropsMixin.OutputFileUriValueProperty(
                                file_name="fileName"
                            ),
                            string_value="stringValue",
                            variable_name="variableName"
                        )]
                    ),
                    query_action=iotanalytics_mixins.CfnDatasetPropsMixin.QueryActionProperty(
                        filters=[iotanalytics_mixins.CfnDatasetPropsMixin.FilterProperty(
                            delta_time=iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeProperty(
                                offset_seconds=123,
                                time_expression="timeExpression"
                            )
                        )],
                        sql_query="sqlQuery"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0dc1b632148f786a7d67ce6df0392e1a6cce9170baf09f1b7c3536226f257681)
                check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
                check_type(argname="argument container_action", value=container_action, expected_type=type_hints["container_action"])
                check_type(argname="argument query_action", value=query_action, expected_type=type_hints["query_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_name is not None:
                self._values["action_name"] = action_name
            if container_action is not None:
                self._values["container_action"] = container_action
            if query_action is not None:
                self._values["query_action"] = query_action

        @builtins.property
        def action_name(self) -> typing.Optional[builtins.str]:
            '''The name of the data set action by which data set contents are automatically created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html#cfn-iotanalytics-dataset-action-actionname
            '''
            result = self._values.get("action_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def container_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.ContainerActionProperty"]]:
            '''Information which allows the system to run a containerized application in order to create the data set contents.

            The application must be in a Docker container along with any needed support libraries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html#cfn-iotanalytics-dataset-action-containeraction
            '''
            result = self._values.get("container_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.ContainerActionProperty"]], result)

        @builtins.property
        def query_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.QueryActionProperty"]]:
            '''An "SqlQueryDatasetAction" object that uses an SQL query to automatically create data set contents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html#cfn-iotanalytics-dataset-action-queryaction
            '''
            result = self._values.get("query_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.QueryActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.ContainerActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "execution_role_arn": "executionRoleArn",
            "image": "image",
            "resource_configuration": "resourceConfiguration",
            "variables": "variables",
        },
    )
    class ContainerActionProperty:
        def __init__(
            self,
            *,
            execution_role_arn: typing.Optional[builtins.str] = None,
            image: typing.Optional[builtins.str] = None,
            resource_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.ResourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.VariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information needed to run the "containerAction" to produce data set contents.

            :param execution_role_arn: The ARN of the role which gives permission to the system to access needed resources in order to run the "containerAction". This includes, at minimum, permission to retrieve the data set contents which are the input to the containerized application.
            :param image: The ARN of the Docker container stored in your account. The Docker container contains an application and needed support libraries and is used to generate data set contents.
            :param resource_configuration: Configuration of the resource which executes the "containerAction".
            :param variables: The values of variables used within the context of the execution of the containerized application (basically, parameters passed to the application). Each variable must have a name and a value given by one of "stringValue", "datasetContentVersionValue", or "outputFileUriValue".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                container_action_property = iotanalytics_mixins.CfnDatasetPropsMixin.ContainerActionProperty(
                    execution_role_arn="executionRoleArn",
                    image="image",
                    resource_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.ResourceConfigurationProperty(
                        compute_type="computeType",
                        volume_size_in_gb=123
                    ),
                    variables=[iotanalytics_mixins.CfnDatasetPropsMixin.VariableProperty(
                        dataset_content_version_value=iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentVersionValueProperty(
                            dataset_name="datasetName"
                        ),
                        double_value=123,
                        output_file_uri_value=iotanalytics_mixins.CfnDatasetPropsMixin.OutputFileUriValueProperty(
                            file_name="fileName"
                        ),
                        string_value="stringValue",
                        variable_name="variableName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e4017760bb4b7d5c4f700fac0ef8c1069343492358a37c1c53c5376099ebe79)
                check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
                check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                check_type(argname="argument resource_configuration", value=resource_configuration, expected_type=type_hints["resource_configuration"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if execution_role_arn is not None:
                self._values["execution_role_arn"] = execution_role_arn
            if image is not None:
                self._values["image"] = image
            if resource_configuration is not None:
                self._values["resource_configuration"] = resource_configuration
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def execution_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role which gives permission to the system to access needed resources in order to run the "containerAction".

            This includes, at minimum, permission to retrieve the data set contents which are the input to the containerized application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-executionrolearn
            '''
            result = self._values.get("execution_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Docker container stored in your account.

            The Docker container contains an application and needed support libraries and is used to generate data set contents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-image
            '''
            result = self._values.get("image")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.ResourceConfigurationProperty"]]:
            '''Configuration of the resource which executes the "containerAction".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-resourceconfiguration
            '''
            result = self._values.get("resource_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.ResourceConfigurationProperty"]], result)

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.VariableProperty"]]]]:
            '''The values of variables used within the context of the execution of the containerized application (basically, parameters passed to the application).

            Each variable must have a name and a value given by one of "stringValue", "datasetContentVersionValue", or "outputFileUriValue".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.VariableProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.DatasetContentDeliveryRuleDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "iot_events_destination_configuration": "iotEventsDestinationConfiguration",
            "s3_destination_configuration": "s3DestinationConfiguration",
        },
    )
    class DatasetContentDeliveryRuleDestinationProperty:
        def __init__(
            self,
            *,
            iot_events_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.IotEventsDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The destination to which dataset contents are delivered.

            :param iot_events_destination_configuration: Configuration information for delivery of dataset contents to AWS IoT Events .
            :param s3_destination_configuration: Configuration information for delivery of dataset contents to Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryruledestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                dataset_content_delivery_rule_destination_property = iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentDeliveryRuleDestinationProperty(
                    iot_events_destination_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.IotEventsDestinationConfigurationProperty(
                        input_name="inputName",
                        role_arn="roleArn"
                    ),
                    s3_destination_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.S3DestinationConfigurationProperty(
                        bucket="bucket",
                        glue_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.GlueConfigurationProperty(
                            database_name="databaseName",
                            table_name="tableName"
                        ),
                        key="key",
                        role_arn="roleArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__025683e9e537c0849a47606bf24a547471e99b2c1d77ddbf65824b6e10bebce8)
                check_type(argname="argument iot_events_destination_configuration", value=iot_events_destination_configuration, expected_type=type_hints["iot_events_destination_configuration"])
                check_type(argname="argument s3_destination_configuration", value=s3_destination_configuration, expected_type=type_hints["s3_destination_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iot_events_destination_configuration is not None:
                self._values["iot_events_destination_configuration"] = iot_events_destination_configuration
            if s3_destination_configuration is not None:
                self._values["s3_destination_configuration"] = s3_destination_configuration

        @builtins.property
        def iot_events_destination_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.IotEventsDestinationConfigurationProperty"]]:
            '''Configuration information for delivery of dataset contents to AWS IoT Events .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryruledestination.html#cfn-iotanalytics-dataset-datasetcontentdeliveryruledestination-ioteventsdestinationconfiguration
            '''
            result = self._values.get("iot_events_destination_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.IotEventsDestinationConfigurationProperty"]], result)

        @builtins.property
        def s3_destination_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.S3DestinationConfigurationProperty"]]:
            '''Configuration information for delivery of dataset contents to Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryruledestination.html#cfn-iotanalytics-dataset-datasetcontentdeliveryruledestination-s3destinationconfiguration
            '''
            result = self._values.get("s3_destination_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.S3DestinationConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetContentDeliveryRuleDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.DatasetContentDeliveryRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "entry_name": "entryName"},
    )
    class DatasetContentDeliveryRuleProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DatasetContentDeliveryRuleDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            entry_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When dataset contents are created, they are delivered to destination specified here.

            :param destination: The destination to which dataset contents are delivered.
            :param entry_name: The name of the dataset content delivery rules entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                dataset_content_delivery_rule_property = iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentDeliveryRuleProperty(
                    destination=iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentDeliveryRuleDestinationProperty(
                        iot_events_destination_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.IotEventsDestinationConfigurationProperty(
                            input_name="inputName",
                            role_arn="roleArn"
                        ),
                        s3_destination_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.S3DestinationConfigurationProperty(
                            bucket="bucket",
                            glue_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.GlueConfigurationProperty(
                                database_name="databaseName",
                                table_name="tableName"
                            ),
                            key="key",
                            role_arn="roleArn"
                        )
                    ),
                    entry_name="entryName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0a6e28dcc726370dc127cd694ba9afc57f3246f618f25030dee98fb685e8556)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument entry_name", value=entry_name, expected_type=type_hints["entry_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if entry_name is not None:
                self._values["entry_name"] = entry_name

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetContentDeliveryRuleDestinationProperty"]]:
            '''The destination to which dataset contents are delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryrule.html#cfn-iotanalytics-dataset-datasetcontentdeliveryrule-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetContentDeliveryRuleDestinationProperty"]], result)

        @builtins.property
        def entry_name(self) -> typing.Optional[builtins.str]:
            '''The name of the dataset content delivery rules entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryrule.html#cfn-iotanalytics-dataset-datasetcontentdeliveryrule-entryname
            '''
            result = self._values.get("entry_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetContentDeliveryRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.DatasetContentVersionValueProperty",
        jsii_struct_bases=[],
        name_mapping={"dataset_name": "datasetName"},
    )
    class DatasetContentVersionValueProperty:
        def __init__(
            self,
            *,
            dataset_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The dataset whose latest contents are used as input to the notebook or application.

            :param dataset_name: The name of the dataset whose latest contents are used as input to the notebook or application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentversionvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                dataset_content_version_value_property = iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentVersionValueProperty(
                    dataset_name="datasetName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ec6a0f80b32c93ff838b05d5f90c5fb390a50fe25b01948561dd167c6753875)
                check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dataset_name is not None:
                self._values["dataset_name"] = dataset_name

        @builtins.property
        def dataset_name(self) -> typing.Optional[builtins.str]:
            '''The name of the dataset whose latest contents are used as input to the notebook or application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentversionvalue.html#cfn-iotanalytics-dataset-datasetcontentversionvalue-datasetname
            '''
            result = self._values.get("dataset_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetContentVersionValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.DeltaTimeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "offset_seconds": "offsetSeconds",
            "time_expression": "timeExpression",
        },
    )
    class DeltaTimeProperty:
        def __init__(
            self,
            *,
            offset_seconds: typing.Optional[jsii.Number] = None,
            time_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used to limit data to that which has arrived since the last execution of the action.

            :param offset_seconds: The number of seconds of estimated in-flight lag time of message data. When you create dataset contents using message data from a specified timeframe, some message data might still be in flight when processing begins, and so do not arrive in time to be processed. Use this field to make allowances for the in flight time of your message data, so that data not processed from a previous timeframe is included with the next timeframe. Otherwise, missed message data would be excluded from processing during the next timeframe too, because its timestamp places it within the previous timeframe.
            :param time_expression: An expression by which the time of the message data might be determined. This can be the name of a timestamp field or a SQL expression that is used to derive the time the message data was generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                delta_time_property = iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeProperty(
                    offset_seconds=123,
                    time_expression="timeExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__128239e956d4164b3e1ae145e0653df84fa46b85d87cb607795c4b2d90886bd3)
                check_type(argname="argument offset_seconds", value=offset_seconds, expected_type=type_hints["offset_seconds"])
                check_type(argname="argument time_expression", value=time_expression, expected_type=type_hints["time_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if offset_seconds is not None:
                self._values["offset_seconds"] = offset_seconds
            if time_expression is not None:
                self._values["time_expression"] = time_expression

        @builtins.property
        def offset_seconds(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds of estimated in-flight lag time of message data.

            When you create dataset contents using message data from a specified timeframe, some message data might still be in flight when processing begins, and so do not arrive in time to be processed. Use this field to make allowances for the in flight time of your message data, so that data not processed from a previous timeframe is included with the next timeframe. Otherwise, missed message data would be excluded from processing during the next timeframe too, because its timestamp places it within the previous timeframe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatime.html#cfn-iotanalytics-dataset-deltatime-offsetseconds
            '''
            result = self._values.get("offset_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def time_expression(self) -> typing.Optional[builtins.str]:
            '''An expression by which the time of the message data might be determined.

            This can be the name of a timestamp field or a SQL expression that is used to derive the time the message data was generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatime.html#cfn-iotanalytics-dataset-deltatime-timeexpression
            '''
            result = self._values.get("time_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeltaTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.DeltaTimeSessionWindowConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"timeout_in_minutes": "timeoutInMinutes"},
    )
    class DeltaTimeSessionWindowConfigurationProperty:
        def __init__(
            self,
            *,
            timeout_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A structure that contains the configuration information of a delta time session window.

            ```DeltaTime`` <https://docs.aws.amazon.com/iotanalytics/latest/APIReference/API_DeltaTime.html>`_ specifies a time interval. You can use ``DeltaTime`` to create dataset contents with data that has arrived in the data store since the last execution. For an example of ``DeltaTime`` , see `Creating a SQL dataset with a delta window (CLI) <https://docs.aws.amazon.com/iotanalytics/latest/userguide/automate-create-dataset.html#automate-example6>`_ in the *AWS IoT Analytics User Guide* .

            :param timeout_in_minutes: A time interval. You can use ``timeoutInMinutes`` so that AWS IoT Analytics can batch up late data notifications that have been generated since the last execution. AWS IoT Analytics sends one batch of notifications to Amazon CloudWatch Events at one time. For more information about how to write a timestamp expression, see `Date and Time Functions and Operators <https://docs.aws.amazon.com/https://prestodb.io/docs/current/functions/datetime.html>`_ , in the *Presto 0.172 Documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatimesessionwindowconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                delta_time_session_window_configuration_property = iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeSessionWindowConfigurationProperty(
                    timeout_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f4e0c385c9f40e6ea6cf145d18405f051ac402dbc7440cb8474717271ede2dd)
                check_type(argname="argument timeout_in_minutes", value=timeout_in_minutes, expected_type=type_hints["timeout_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if timeout_in_minutes is not None:
                self._values["timeout_in_minutes"] = timeout_in_minutes

        @builtins.property
        def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''A time interval.

            You can use ``timeoutInMinutes`` so that AWS IoT Analytics can batch up late data notifications that have been generated since the last execution. AWS IoT Analytics sends one batch of notifications to Amazon CloudWatch Events at one time.

            For more information about how to write a timestamp expression, see `Date and Time Functions and Operators <https://docs.aws.amazon.com/https://prestodb.io/docs/current/functions/datetime.html>`_ , in the *Presto 0.172 Documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatimesessionwindowconfiguration.html#cfn-iotanalytics-dataset-deltatimesessionwindowconfiguration-timeoutinminutes
            '''
            result = self._values.get("timeout_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeltaTimeSessionWindowConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"delta_time": "deltaTime"},
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            delta_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DeltaTimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information which is used to filter message data, to segregate it according to the time frame in which it arrives.

            :param delta_time: Used to limit data to that which has arrived since the last execution of the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                filter_property = iotanalytics_mixins.CfnDatasetPropsMixin.FilterProperty(
                    delta_time=iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeProperty(
                        offset_seconds=123,
                        time_expression="timeExpression"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cec55b10392ceafd17007015be0804f127249bf007ab8518eb1bc4e5b3e92859)
                check_type(argname="argument delta_time", value=delta_time, expected_type=type_hints["delta_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delta_time is not None:
                self._values["delta_time"] = delta_time

        @builtins.property
        def delta_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DeltaTimeProperty"]]:
            '''Used to limit data to that which has arrived since the last execution of the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-filter.html#cfn-iotanalytics-dataset-filter-deltatime
            '''
            result = self._values.get("delta_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DeltaTimeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.GlueConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"database_name": "databaseName", "table_name": "tableName"},
    )
    class GlueConfigurationProperty:
        def __init__(
            self,
            *,
            database_name: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information for coordination with AWS Glue , a fully managed extract, transform and load (ETL) service.

            :param database_name: The name of the database in your AWS Glue Data Catalog in which the table is located. An AWS Glue Data Catalog database contains metadata tables.
            :param table_name: The name of the table in your AWS Glue Data Catalog that is used to perform the ETL operations. An AWS Glue Data Catalog table contains partitioned data and descriptions of data sources and targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-glueconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                glue_configuration_property = iotanalytics_mixins.CfnDatasetPropsMixin.GlueConfigurationProperty(
                    database_name="databaseName",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__431fd53b28240e972e2ed79d0852e4f0fc08da703b11903c11bab0e239f75999)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_name is not None:
                self._values["database_name"] = database_name
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database in your AWS Glue Data Catalog in which the table is located.

            An AWS Glue Data Catalog database contains metadata tables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-glueconfiguration.html#cfn-iotanalytics-dataset-glueconfiguration-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the table in your AWS Glue Data Catalog that is used to perform the ETL operations.

            An AWS Glue Data Catalog table contains partitioned data and descriptions of data sources and targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-glueconfiguration.html#cfn-iotanalytics-dataset-glueconfiguration-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.IotEventsDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"input_name": "inputName", "role_arn": "roleArn"},
    )
    class IotEventsDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            input_name: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information for delivery of dataset contents to AWS IoT Events .

            :param input_name: The name of the AWS IoT Events input to which dataset contents are delivered.
            :param role_arn: The ARN of the role that grants AWS IoT Analytics permission to deliver dataset contents to an AWS IoT Events input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-ioteventsdestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                iot_events_destination_configuration_property = iotanalytics_mixins.CfnDatasetPropsMixin.IotEventsDestinationConfigurationProperty(
                    input_name="inputName",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__963e75b26b2906ad19cf6c7b1ce050a3caa6ba26f86c8143350e421700aabdce)
                check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_name is not None:
                self._values["input_name"] = input_name
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def input_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS IoT Events input to which dataset contents are delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-ioteventsdestinationconfiguration.html#cfn-iotanalytics-dataset-ioteventsdestinationconfiguration-inputname
            '''
            result = self._values.get("input_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that grants AWS IoT Analytics permission to deliver dataset contents to an AWS IoT Events input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-ioteventsdestinationconfiguration.html#cfn-iotanalytics-dataset-ioteventsdestinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotEventsDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.LateDataRuleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delta_time_session_window_configuration": "deltaTimeSessionWindowConfiguration",
        },
    )
    class LateDataRuleConfigurationProperty:
        def __init__(
            self,
            *,
            delta_time_session_window_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DeltaTimeSessionWindowConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The information needed to configure a delta time session window.

            :param delta_time_session_window_configuration: The information needed to configure a delta time session window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-latedataruleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                late_data_rule_configuration_property = iotanalytics_mixins.CfnDatasetPropsMixin.LateDataRuleConfigurationProperty(
                    delta_time_session_window_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeSessionWindowConfigurationProperty(
                        timeout_in_minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf6d41a2ce4f6e5da4b44a623788de449ace4c0ff3da762b010cf1d5aab5239c)
                check_type(argname="argument delta_time_session_window_configuration", value=delta_time_session_window_configuration, expected_type=type_hints["delta_time_session_window_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delta_time_session_window_configuration is not None:
                self._values["delta_time_session_window_configuration"] = delta_time_session_window_configuration

        @builtins.property
        def delta_time_session_window_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DeltaTimeSessionWindowConfigurationProperty"]]:
            '''The information needed to configure a delta time session window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-latedataruleconfiguration.html#cfn-iotanalytics-dataset-latedataruleconfiguration-deltatimesessionwindowconfiguration
            '''
            result = self._values.get("delta_time_session_window_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DeltaTimeSessionWindowConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LateDataRuleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.LateDataRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rule_configuration": "ruleConfiguration",
            "rule_name": "ruleName",
        },
    )
    class LateDataRuleProperty:
        def __init__(
            self,
            *,
            rule_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.LateDataRuleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rule_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains the name and configuration information of a late data rule.

            :param rule_configuration: The information needed to configure the late data rule.
            :param rule_name: The name of the late data rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-latedatarule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                late_data_rule_property = iotanalytics_mixins.CfnDatasetPropsMixin.LateDataRuleProperty(
                    rule_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.LateDataRuleConfigurationProperty(
                        delta_time_session_window_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeSessionWindowConfigurationProperty(
                            timeout_in_minutes=123
                        )
                    ),
                    rule_name="ruleName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__358fb54bc1603828f06990777332120d0d29f6485f5e6484bafe7be312da0f0d)
                check_type(argname="argument rule_configuration", value=rule_configuration, expected_type=type_hints["rule_configuration"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rule_configuration is not None:
                self._values["rule_configuration"] = rule_configuration
            if rule_name is not None:
                self._values["rule_name"] = rule_name

        @builtins.property
        def rule_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.LateDataRuleConfigurationProperty"]]:
            '''The information needed to configure the late data rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-latedatarule.html#cfn-iotanalytics-dataset-latedatarule-ruleconfiguration
            '''
            result = self._values.get("rule_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.LateDataRuleConfigurationProperty"]], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''The name of the late data rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-latedatarule.html#cfn-iotanalytics-dataset-latedatarule-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LateDataRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.OutputFileUriValueProperty",
        jsii_struct_bases=[],
        name_mapping={"file_name": "fileName"},
    )
    class OutputFileUriValueProperty:
        def __init__(self, *, file_name: typing.Optional[builtins.str] = None) -> None:
            '''The value of the variable as a structure that specifies an output file URI.

            :param file_name: The URI of the location where dataset contents are stored, usually the URI of a file in an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-outputfileurivalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                output_file_uri_value_property = iotanalytics_mixins.CfnDatasetPropsMixin.OutputFileUriValueProperty(
                    file_name="fileName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a78d67e4e332acb3c9c8edb5a3d1d279812385ba6520282a34e40a41bc46c22)
                check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file_name is not None:
                self._values["file_name"] = file_name

        @builtins.property
        def file_name(self) -> typing.Optional[builtins.str]:
            '''The URI of the location where dataset contents are stored, usually the URI of a file in an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-outputfileurivalue.html#cfn-iotanalytics-dataset-outputfileurivalue-filename
            '''
            result = self._values.get("file_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputFileUriValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.QueryActionProperty",
        jsii_struct_bases=[],
        name_mapping={"filters": "filters", "sql_query": "sqlQuery"},
    )
    class QueryActionProperty:
        def __init__(
            self,
            *,
            filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.FilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            sql_query: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An "SqlQueryDatasetAction" object that uses an SQL query to automatically create data set contents.

            :param filters: Pre-filters applied to message data.
            :param sql_query: An "SqlQueryDatasetAction" object that uses an SQL query to automatically create data set contents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-queryaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                query_action_property = iotanalytics_mixins.CfnDatasetPropsMixin.QueryActionProperty(
                    filters=[iotanalytics_mixins.CfnDatasetPropsMixin.FilterProperty(
                        delta_time=iotanalytics_mixins.CfnDatasetPropsMixin.DeltaTimeProperty(
                            offset_seconds=123,
                            time_expression="timeExpression"
                        )
                    )],
                    sql_query="sqlQuery"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31a5cd8af2d27237ab4ef850ddb1e9ab0ff46f5f4693f5fecbc633ba0cf5aae3)
                check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
                check_type(argname="argument sql_query", value=sql_query, expected_type=type_hints["sql_query"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filters is not None:
                self._values["filters"] = filters
            if sql_query is not None:
                self._values["sql_query"] = sql_query

        @builtins.property
        def filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FilterProperty"]]]]:
            '''Pre-filters applied to message data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-queryaction.html#cfn-iotanalytics-dataset-queryaction-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FilterProperty"]]]], result)

        @builtins.property
        def sql_query(self) -> typing.Optional[builtins.str]:
            '''An "SqlQueryDatasetAction" object that uses an SQL query to automatically create data set contents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-queryaction.html#cfn-iotanalytics-dataset-queryaction-sqlquery
            '''
            result = self._values.get("sql_query")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.ResourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_type": "computeType",
            "volume_size_in_gb": "volumeSizeInGb",
        },
    )
    class ResourceConfigurationProperty:
        def __init__(
            self,
            *,
            compute_type: typing.Optional[builtins.str] = None,
            volume_size_in_gb: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration of the resource used to execute the ``containerAction`` .

            :param compute_type: The type of the compute resource used to execute the ``containerAction`` . Possible values are: ``ACU_1`` (vCPU=4, memory=16 GiB) or ``ACU_2`` (vCPU=8, memory=32 GiB).
            :param volume_size_in_gb: The size, in GB, of the persistent storage available to the resource instance used to execute the ``containerAction`` (min: 1, max: 50).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-resourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                resource_configuration_property = iotanalytics_mixins.CfnDatasetPropsMixin.ResourceConfigurationProperty(
                    compute_type="computeType",
                    volume_size_in_gb=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae234006d61f854dc598cdd309d833ab588fc4903a8c6f54e6748162524ebcea)
                check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
                check_type(argname="argument volume_size_in_gb", value=volume_size_in_gb, expected_type=type_hints["volume_size_in_gb"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_type is not None:
                self._values["compute_type"] = compute_type
            if volume_size_in_gb is not None:
                self._values["volume_size_in_gb"] = volume_size_in_gb

        @builtins.property
        def compute_type(self) -> typing.Optional[builtins.str]:
            '''The type of the compute resource used to execute the ``containerAction`` .

            Possible values are: ``ACU_1`` (vCPU=4, memory=16 GiB) or ``ACU_2`` (vCPU=8, memory=32 GiB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-resourceconfiguration.html#cfn-iotanalytics-dataset-resourceconfiguration-computetype
            '''
            result = self._values.get("compute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def volume_size_in_gb(self) -> typing.Optional[jsii.Number]:
            '''The size, in GB, of the persistent storage available to the resource instance used to execute the ``containerAction`` (min: 1, max: 50).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-resourceconfiguration.html#cfn-iotanalytics-dataset-resourceconfiguration-volumesizeingb
            '''
            result = self._values.get("volume_size_in_gb")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.RetentionPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"number_of_days": "numberOfDays", "unlimited": "unlimited"},
    )
    class RetentionPeriodProperty:
        def __init__(
            self,
            *,
            number_of_days: typing.Optional[jsii.Number] = None,
            unlimited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''How long, in days, message data is kept.

            :param number_of_days: The number of days that message data is kept. The ``unlimited`` parameter must be false.
            :param unlimited: If true, message data is kept indefinitely.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-retentionperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                retention_period_property = iotanalytics_mixins.CfnDatasetPropsMixin.RetentionPeriodProperty(
                    number_of_days=123,
                    unlimited=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a79edda129c1b099feab7c440a1fd225c8de10e00d8babc98e71f7be93f64760)
                check_type(argname="argument number_of_days", value=number_of_days, expected_type=type_hints["number_of_days"])
                check_type(argname="argument unlimited", value=unlimited, expected_type=type_hints["unlimited"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if number_of_days is not None:
                self._values["number_of_days"] = number_of_days
            if unlimited is not None:
                self._values["unlimited"] = unlimited

        @builtins.property
        def number_of_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days that message data is kept.

            The ``unlimited`` parameter must be false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-retentionperiod.html#cfn-iotanalytics-dataset-retentionperiod-numberofdays
            '''
            result = self._values.get("number_of_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unlimited(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If true, message data is kept indefinitely.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-retentionperiod.html#cfn-iotanalytics-dataset-retentionperiod-unlimited
            '''
            result = self._values.get("unlimited")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.S3DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "glue_configuration": "glueConfiguration",
            "key": "key",
            "role_arn": "roleArn",
        },
    )
    class S3DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            glue_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.GlueConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            key: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information for delivery of dataset contents to Amazon Simple Storage Service (Amazon S3).

            :param bucket: The name of the S3 bucket to which dataset contents are delivered.
            :param glue_configuration: Configuration information for coordination with AWS Glue , a fully managed extract, transform and load (ETL) service.
            :param key: The key of the dataset contents object in an S3 bucket. Each object has a key that is a unique identifier. Each object has exactly one key. You can create a unique key with the following options: - Use ``!{iotanalytics:scheduleTime}`` to insert the time of a scheduled SQL query run. - Use ``!{iotanalytics:versionId}`` to insert a unique hash that identifies a dataset content. - Use ``!{iotanalytics:creationTime}`` to insert the creation time of a dataset content. The following example creates a unique key for a CSV file: ``dataset/mydataset/!{iotanalytics:scheduleTime}/!{iotanalytics:versionId}.csv`` .. epigraph:: If you don't use ``!{iotanalytics:versionId}`` to specify the key, you might get duplicate keys. For example, you might have two dataset contents with the same ``scheduleTime`` but different ``versionId`` s. This means that one dataset content overwrites the other.
            :param role_arn: The ARN of the role that grants AWS IoT Analytics permission to interact with your Amazon S3 and AWS Glue resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-s3destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                s3_destination_configuration_property = iotanalytics_mixins.CfnDatasetPropsMixin.S3DestinationConfigurationProperty(
                    bucket="bucket",
                    glue_configuration=iotanalytics_mixins.CfnDatasetPropsMixin.GlueConfigurationProperty(
                        database_name="databaseName",
                        table_name="tableName"
                    ),
                    key="key",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e55a6303a322b63ed2e9c60600396e0308bb706fb2c935c791c9cc55ad2ebd85)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument glue_configuration", value=glue_configuration, expected_type=type_hints["glue_configuration"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if glue_configuration is not None:
                self._values["glue_configuration"] = glue_configuration
            if key is not None:
                self._values["key"] = key
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket to which dataset contents are delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-s3destinationconfiguration.html#cfn-iotanalytics-dataset-s3destinationconfiguration-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def glue_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.GlueConfigurationProperty"]]:
            '''Configuration information for coordination with AWS Glue , a fully managed extract, transform and load (ETL) service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-s3destinationconfiguration.html#cfn-iotanalytics-dataset-s3destinationconfiguration-glueconfiguration
            '''
            result = self._values.get("glue_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.GlueConfigurationProperty"]], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of the dataset contents object in an S3 bucket.

            Each object has a key that is a unique identifier. Each object has exactly one key.

            You can create a unique key with the following options:

            - Use ``!{iotanalytics:scheduleTime}`` to insert the time of a scheduled SQL query run.
            - Use ``!{iotanalytics:versionId}`` to insert a unique hash that identifies a dataset content.
            - Use ``!{iotanalytics:creationTime}`` to insert the creation time of a dataset content.

            The following example creates a unique key for a CSV file: ``dataset/mydataset/!{iotanalytics:scheduleTime}/!{iotanalytics:versionId}.csv``
            .. epigraph::

               If you don't use ``!{iotanalytics:versionId}`` to specify the key, you might get duplicate keys. For example, you might have two dataset contents with the same ``scheduleTime`` but different ``versionId`` s. This means that one dataset content overwrites the other.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-s3destinationconfiguration.html#cfn-iotanalytics-dataset-s3destinationconfiguration-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that grants AWS IoT Analytics permission to interact with your Amazon S3 and AWS Glue resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-s3destinationconfiguration.html#cfn-iotanalytics-dataset-s3destinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule_expression": "scheduleExpression"},
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            schedule_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The schedule for when to trigger an update.

            :param schedule_expression: The expression that defines when to trigger an update. For more information, see `Schedule Expressions for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch documentation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                schedule_property = iotanalytics_mixins.CfnDatasetPropsMixin.ScheduleProperty(
                    schedule_expression="scheduleExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45ea45d566a9bba3a4308f01668d6d5add2c0d86feb4697a4a6477d57c2317aa)
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''The expression that defines when to trigger an update.

            For more information, see `Schedule Expressions for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch documentation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-schedule.html#cfn-iotanalytics-dataset-schedule-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.TriggerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "schedule": "schedule",
            "triggering_dataset": "triggeringDataset",
        },
    )
    class TriggerProperty:
        def __init__(
            self,
            *,
            schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            triggering_dataset: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.TriggeringDatasetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The "DatasetTrigger" that specifies when the data set is automatically updated.

            :param schedule: The "Schedule" when the trigger is initiated.
            :param triggering_dataset: Information about the data set whose content generation triggers the new data set content generation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                trigger_property = iotanalytics_mixins.CfnDatasetPropsMixin.TriggerProperty(
                    schedule=iotanalytics_mixins.CfnDatasetPropsMixin.ScheduleProperty(
                        schedule_expression="scheduleExpression"
                    ),
                    triggering_dataset=iotanalytics_mixins.CfnDatasetPropsMixin.TriggeringDatasetProperty(
                        dataset_name="datasetName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ceb68d49b3538b76d6ab7c6eabf5d6e2de1be360275661dff62252f78c35eb6)
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
                check_type(argname="argument triggering_dataset", value=triggering_dataset, expected_type=type_hints["triggering_dataset"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schedule is not None:
                self._values["schedule"] = schedule
            if triggering_dataset is not None:
                self._values["triggering_dataset"] = triggering_dataset

        @builtins.property
        def schedule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.ScheduleProperty"]]:
            '''The "Schedule" when the trigger is initiated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger.html#cfn-iotanalytics-dataset-trigger-schedule
            '''
            result = self._values.get("schedule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.ScheduleProperty"]], result)

        @builtins.property
        def triggering_dataset(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.TriggeringDatasetProperty"]]:
            '''Information about the data set whose content generation triggers the new data set content generation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger.html#cfn-iotanalytics-dataset-trigger-triggeringdataset
            '''
            result = self._values.get("triggering_dataset")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.TriggeringDatasetProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.TriggeringDatasetProperty",
        jsii_struct_bases=[],
        name_mapping={"dataset_name": "datasetName"},
    )
    class TriggeringDatasetProperty:
        def __init__(
            self,
            *,
            dataset_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the dataset whose content generation triggers the new dataset content generation.

            :param dataset_name: The name of the data set whose content generation triggers the new data set content generation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-triggeringdataset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                triggering_dataset_property = iotanalytics_mixins.CfnDatasetPropsMixin.TriggeringDatasetProperty(
                    dataset_name="datasetName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ca0eb3c573b14bc914dc46e7b7bb44220b9c63a95a0bbd8e622fae36c39c782)
                check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dataset_name is not None:
                self._values["dataset_name"] = dataset_name

        @builtins.property
        def dataset_name(self) -> typing.Optional[builtins.str]:
            '''The name of the data set whose content generation triggers the new data set content generation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-triggeringdataset.html#cfn-iotanalytics-dataset-triggeringdataset-datasetname
            '''
            result = self._values.get("dataset_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggeringDatasetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.VariableProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dataset_content_version_value": "datasetContentVersionValue",
            "double_value": "doubleValue",
            "output_file_uri_value": "outputFileUriValue",
            "string_value": "stringValue",
            "variable_name": "variableName",
        },
    )
    class VariableProperty:
        def __init__(
            self,
            *,
            dataset_content_version_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DatasetContentVersionValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            output_file_uri_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.OutputFileUriValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            string_value: typing.Optional[builtins.str] = None,
            variable_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An instance of a variable to be passed to the ``containerAction`` execution.

            Each variable must have a name and a value given by one of ``stringValue`` , ``datasetContentVersionValue`` , or ``outputFileUriValue`` .

            :param dataset_content_version_value: The value of the variable as a structure that specifies a dataset content version.
            :param double_value: The value of the variable as a double (numeric).
            :param output_file_uri_value: The value of the variable as a structure that specifies an output file URI.
            :param string_value: The value of the variable as a string.
            :param variable_name: The name of the variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                variable_property = iotanalytics_mixins.CfnDatasetPropsMixin.VariableProperty(
                    dataset_content_version_value=iotanalytics_mixins.CfnDatasetPropsMixin.DatasetContentVersionValueProperty(
                        dataset_name="datasetName"
                    ),
                    double_value=123,
                    output_file_uri_value=iotanalytics_mixins.CfnDatasetPropsMixin.OutputFileUriValueProperty(
                        file_name="fileName"
                    ),
                    string_value="stringValue",
                    variable_name="variableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__168933c4b44bbfca010fa9f7ed848f5ff445c9127583a0f3f6289dd624de4974)
                check_type(argname="argument dataset_content_version_value", value=dataset_content_version_value, expected_type=type_hints["dataset_content_version_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument output_file_uri_value", value=output_file_uri_value, expected_type=type_hints["output_file_uri_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
                check_type(argname="argument variable_name", value=variable_name, expected_type=type_hints["variable_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dataset_content_version_value is not None:
                self._values["dataset_content_version_value"] = dataset_content_version_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if output_file_uri_value is not None:
                self._values["output_file_uri_value"] = output_file_uri_value
            if string_value is not None:
                self._values["string_value"] = string_value
            if variable_name is not None:
                self._values["variable_name"] = variable_name

        @builtins.property
        def dataset_content_version_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetContentVersionValueProperty"]]:
            '''The value of the variable as a structure that specifies a dataset content version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-datasetcontentversionvalue
            '''
            result = self._values.get("dataset_content_version_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetContentVersionValueProperty"]], result)

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            '''The value of the variable as a double (numeric).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def output_file_uri_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.OutputFileUriValueProperty"]]:
            '''The value of the variable as a structure that specifies an output file URI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-outputfileurivalue
            '''
            result = self._values.get("output_file_uri_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.OutputFileUriValueProperty"]], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''The value of the variable as a string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variable_name(self) -> typing.Optional[builtins.str]:
            '''The name of the variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-variablename
            '''
            result = self._values.get("variable_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatasetPropsMixin.VersioningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"max_versions": "maxVersions", "unlimited": "unlimited"},
    )
    class VersioningConfigurationProperty:
        def __init__(
            self,
            *,
            max_versions: typing.Optional[jsii.Number] = None,
            unlimited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Information about the versioning of dataset contents.

            :param max_versions: How many versions of dataset contents are kept. The ``unlimited`` parameter must be ``false`` .
            :param unlimited: If true, unlimited versions of dataset contents are kept.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-versioningconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                versioning_configuration_property = iotanalytics_mixins.CfnDatasetPropsMixin.VersioningConfigurationProperty(
                    max_versions=123,
                    unlimited=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__62da840eca6e7c206c25cd0630c4ac0a9fb982adf2a5595c62ba8ced98025cd7)
                check_type(argname="argument max_versions", value=max_versions, expected_type=type_hints["max_versions"])
                check_type(argname="argument unlimited", value=unlimited, expected_type=type_hints["unlimited"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_versions is not None:
                self._values["max_versions"] = max_versions
            if unlimited is not None:
                self._values["unlimited"] = unlimited

        @builtins.property
        def max_versions(self) -> typing.Optional[jsii.Number]:
            '''How many versions of dataset contents are kept.

            The ``unlimited`` parameter must be ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-versioningconfiguration.html#cfn-iotanalytics-dataset-versioningconfiguration-maxversions
            '''
            result = self._values.get("max_versions")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unlimited(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If true, unlimited versions of dataset contents are kept.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-versioningconfiguration.html#cfn-iotanalytics-dataset-versioningconfiguration-unlimited
            '''
            result = self._values.get("unlimited")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VersioningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastoreMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "datastore_name": "datastoreName",
        "datastore_partitions": "datastorePartitions",
        "datastore_storage": "datastoreStorage",
        "file_format_configuration": "fileFormatConfiguration",
        "retention_period": "retentionPeriod",
        "tags": "tags",
    },
)
class CfnDatastoreMixinProps:
    def __init__(
        self,
        *,
        datastore_name: typing.Optional[builtins.str] = None,
        datastore_partitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.DatastorePartitionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        datastore_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.DatastoreStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        file_format_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.FileFormatConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        retention_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.RetentionPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDatastorePropsMixin.

        :param datastore_name: The name of the data store.
        :param datastore_partitions: Information about the partition dimensions in a data store.
        :param datastore_storage: Where data store data is stored.
        :param file_format_configuration: Contains the configuration information of file formats. AWS IoT Analytics data stores support JSON and `Parquet <https://docs.aws.amazon.com/https://parquet.apache.org/>`_ . The default file format is JSON. You can specify only one format. You can't change the file format after you create the data store.
        :param retention_period: How long, in days, message data is kept for the data store. When ``customerManagedS3`` storage is selected, this parameter is ignored.
        :param tags: Metadata which can be used to manage the data store. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
            
            # json_configuration: Any
            # service_managed_s3: Any
            
            cfn_datastore_mixin_props = iotanalytics_mixins.CfnDatastoreMixinProps(
                datastore_name="datastoreName",
                datastore_partitions=iotanalytics_mixins.CfnDatastorePropsMixin.DatastorePartitionsProperty(
                    partitions=[iotanalytics_mixins.CfnDatastorePropsMixin.DatastorePartitionProperty(
                        partition=iotanalytics_mixins.CfnDatastorePropsMixin.PartitionProperty(
                            attribute_name="attributeName"
                        ),
                        timestamp_partition=iotanalytics_mixins.CfnDatastorePropsMixin.TimestampPartitionProperty(
                            attribute_name="attributeName",
                            timestamp_format="timestampFormat"
                        )
                    )]
                ),
                datastore_storage=iotanalytics_mixins.CfnDatastorePropsMixin.DatastoreStorageProperty(
                    customer_managed_s3=iotanalytics_mixins.CfnDatastorePropsMixin.CustomerManagedS3Property(
                        bucket="bucket",
                        key_prefix="keyPrefix",
                        role_arn="roleArn"
                    ),
                    iot_site_wise_multi_layer_storage=iotanalytics_mixins.CfnDatastorePropsMixin.IotSiteWiseMultiLayerStorageProperty(
                        customer_managed_s3_storage=iotanalytics_mixins.CfnDatastorePropsMixin.CustomerManagedS3StorageProperty(
                            bucket="bucket",
                            key_prefix="keyPrefix"
                        )
                    ),
                    service_managed_s3=service_managed_s3
                ),
                file_format_configuration=iotanalytics_mixins.CfnDatastorePropsMixin.FileFormatConfigurationProperty(
                    json_configuration=json_configuration,
                    parquet_configuration=iotanalytics_mixins.CfnDatastorePropsMixin.ParquetConfigurationProperty(
                        schema_definition=iotanalytics_mixins.CfnDatastorePropsMixin.SchemaDefinitionProperty(
                            columns=[iotanalytics_mixins.CfnDatastorePropsMixin.ColumnProperty(
                                name="name",
                                type="type"
                            )]
                        )
                    )
                ),
                retention_period=iotanalytics_mixins.CfnDatastorePropsMixin.RetentionPeriodProperty(
                    number_of_days=123,
                    unlimited=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2531678c39bf8733364948ef4e5ec694fb33a59eb0ac5de33038b89445e9290e)
            check_type(argname="argument datastore_name", value=datastore_name, expected_type=type_hints["datastore_name"])
            check_type(argname="argument datastore_partitions", value=datastore_partitions, expected_type=type_hints["datastore_partitions"])
            check_type(argname="argument datastore_storage", value=datastore_storage, expected_type=type_hints["datastore_storage"])
            check_type(argname="argument file_format_configuration", value=file_format_configuration, expected_type=type_hints["file_format_configuration"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if datastore_name is not None:
            self._values["datastore_name"] = datastore_name
        if datastore_partitions is not None:
            self._values["datastore_partitions"] = datastore_partitions
        if datastore_storage is not None:
            self._values["datastore_storage"] = datastore_storage
        if file_format_configuration is not None:
            self._values["file_format_configuration"] = file_format_configuration
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def datastore_name(self) -> typing.Optional[builtins.str]:
        '''The name of the data store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-datastorename
        '''
        result = self._values.get("datastore_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datastore_partitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.DatastorePartitionsProperty"]]:
        '''Information about the partition dimensions in a data store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-datastorepartitions
        '''
        result = self._values.get("datastore_partitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.DatastorePartitionsProperty"]], result)

    @builtins.property
    def datastore_storage(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.DatastoreStorageProperty"]]:
        '''Where data store data is stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-datastorestorage
        '''
        result = self._values.get("datastore_storage")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.DatastoreStorageProperty"]], result)

    @builtins.property
    def file_format_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.FileFormatConfigurationProperty"]]:
        '''Contains the configuration information of file formats. AWS IoT Analytics data stores support JSON and `Parquet <https://docs.aws.amazon.com/https://parquet.apache.org/>`_ .

        The default file format is JSON. You can specify only one format.

        You can't change the file format after you create the data store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-fileformatconfiguration
        '''
        result = self._values.get("file_format_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.FileFormatConfigurationProperty"]], result)

    @builtins.property
    def retention_period(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.RetentionPeriodProperty"]]:
        '''How long, in days, message data is kept for the data store.

        When ``customerManagedS3`` storage is selected, this parameter is ignored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-retentionperiod
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.RetentionPeriodProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata which can be used to manage the data store.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatastoreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDatastorePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin",
):
    '''AWS::IoTAnalytics::Datastore resource is a repository for messages.

    For more information, see `How to Use AWS IoT Analytics <https://docs.aws.amazon.com/iotanalytics/latest/userguide/welcome.html#aws-iot-analytics-how>`_ in the *AWS IoT Analytics User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html
    :cloudformationResource: AWS::IoTAnalytics::Datastore
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
        
        # json_configuration: Any
        # service_managed_s3: Any
        
        cfn_datastore_props_mixin = iotanalytics_mixins.CfnDatastorePropsMixin(iotanalytics_mixins.CfnDatastoreMixinProps(
            datastore_name="datastoreName",
            datastore_partitions=iotanalytics_mixins.CfnDatastorePropsMixin.DatastorePartitionsProperty(
                partitions=[iotanalytics_mixins.CfnDatastorePropsMixin.DatastorePartitionProperty(
                    partition=iotanalytics_mixins.CfnDatastorePropsMixin.PartitionProperty(
                        attribute_name="attributeName"
                    ),
                    timestamp_partition=iotanalytics_mixins.CfnDatastorePropsMixin.TimestampPartitionProperty(
                        attribute_name="attributeName",
                        timestamp_format="timestampFormat"
                    )
                )]
            ),
            datastore_storage=iotanalytics_mixins.CfnDatastorePropsMixin.DatastoreStorageProperty(
                customer_managed_s3=iotanalytics_mixins.CfnDatastorePropsMixin.CustomerManagedS3Property(
                    bucket="bucket",
                    key_prefix="keyPrefix",
                    role_arn="roleArn"
                ),
                iot_site_wise_multi_layer_storage=iotanalytics_mixins.CfnDatastorePropsMixin.IotSiteWiseMultiLayerStorageProperty(
                    customer_managed_s3_storage=iotanalytics_mixins.CfnDatastorePropsMixin.CustomerManagedS3StorageProperty(
                        bucket="bucket",
                        key_prefix="keyPrefix"
                    )
                ),
                service_managed_s3=service_managed_s3
            ),
            file_format_configuration=iotanalytics_mixins.CfnDatastorePropsMixin.FileFormatConfigurationProperty(
                json_configuration=json_configuration,
                parquet_configuration=iotanalytics_mixins.CfnDatastorePropsMixin.ParquetConfigurationProperty(
                    schema_definition=iotanalytics_mixins.CfnDatastorePropsMixin.SchemaDefinitionProperty(
                        columns=[iotanalytics_mixins.CfnDatastorePropsMixin.ColumnProperty(
                            name="name",
                            type="type"
                        )]
                    )
                )
            ),
            retention_period=iotanalytics_mixins.CfnDatastorePropsMixin.RetentionPeriodProperty(
                number_of_days=123,
                unlimited=False
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
        props: typing.Union[CfnDatastoreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTAnalytics::Datastore``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4193dea9e816294bcf36efd314f36ca3a9af406826e4d27a07f2eb2a83f148)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5880381c3827b7968b462e245fefe0ed88a446b0682fe35e65819e98266f0c7c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e03177b1a85340f0903852443f74cd51c0cea2658acf3cda110a9787db17cdb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDatastoreMixinProps:
        return typing.cast(CfnDatastoreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.ColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "type": "type"},
    )
    class ColumnProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a column that stores your data.

            :param name: The name of the column.
            :param type: The type of data. For more information about the supported data types, see `Common data types <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-common.html>`_ in the *AWS Glue Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-column.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                column_property = iotanalytics_mixins.CfnDatastorePropsMixin.ColumnProperty(
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee5f3f753d3689a4def067b2f2ae0b45fc027fe5c320cdac53841f0003648a3e)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-column.html#cfn-iotanalytics-datastore-column-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of data.

            For more information about the supported data types, see `Common data types <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-common.html>`_ in the *AWS Glue Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-column.html#cfn-iotanalytics-datastore-column-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.CustomerManagedS3Property",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key_prefix": "keyPrefix",
            "role_arn": "roleArn",
        },
    )
    class CustomerManagedS3Property:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key_prefix: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''S3-customer-managed;

            When you choose customer-managed storage, the ``retentionPeriod`` parameter is ignored. You can't change the choice of Amazon S3 storage after your data store is created.

            :param bucket: The name of the Amazon S3 bucket where your data is stored.
            :param key_prefix: (Optional) The prefix used to create the keys of the data store data objects. Each object in an Amazon S3 bucket has a key that is its unique identifier in the bucket. Each object in a bucket has exactly one key. The prefix must end with a forward slash (/).
            :param role_arn: The ARN of the role that grants AWS IoT Analytics permission to interact with your Amazon S3 resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                customer_managed_s3_property = iotanalytics_mixins.CfnDatastorePropsMixin.CustomerManagedS3Property(
                    bucket="bucket",
                    key_prefix="keyPrefix",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a566abb89c42bd3c0d98baf07cebb5f917ed46cb4bc1d527b0d765814bd90a1f)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key_prefix is not None:
                self._values["key_prefix"] = key_prefix
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket where your data is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3.html#cfn-iotanalytics-datastore-customermanageds3-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_prefix(self) -> typing.Optional[builtins.str]:
            '''(Optional) The prefix used to create the keys of the data store data objects.

            Each object in an Amazon S3 bucket has a key that is its unique identifier in the bucket. Each object in a bucket has exactly one key. The prefix must end with a forward slash (/).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3.html#cfn-iotanalytics-datastore-customermanageds3-keyprefix
            '''
            result = self._values.get("key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that grants AWS IoT Analytics permission to interact with your Amazon S3 resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3.html#cfn-iotanalytics-datastore-customermanageds3-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerManagedS3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.CustomerManagedS3StorageProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key_prefix": "keyPrefix"},
    )
    class CustomerManagedS3StorageProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Amazon S3 -customer-managed;

            When you choose customer-managed storage, the ``retentionPeriod`` parameter is ignored. You can't change the choice of Amazon S3 storage after your data store is created.

            :param bucket: The name of the Amazon S3 bucket where your data is stored.
            :param key_prefix: (Optional) The prefix used to create the keys of the data store data objects. Each object in an Amazon S3 bucket has a key that is its unique identifier in the bucket. Each object in a bucket has exactly one key. The prefix must end with a forward slash (/).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3storage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                customer_managed_s3_storage_property = iotanalytics_mixins.CfnDatastorePropsMixin.CustomerManagedS3StorageProperty(
                    bucket="bucket",
                    key_prefix="keyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0b9be96b91db13d4cef38d6b4207168be1fee61ae4885aa71feae520c0952f0)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key_prefix is not None:
                self._values["key_prefix"] = key_prefix

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket where your data is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3storage.html#cfn-iotanalytics-datastore-customermanageds3storage-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_prefix(self) -> typing.Optional[builtins.str]:
            '''(Optional) The prefix used to create the keys of the data store data objects.

            Each object in an Amazon S3 bucket has a key that is its unique identifier in the bucket. Each object in a bucket has exactly one key. The prefix must end with a forward slash (/).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3storage.html#cfn-iotanalytics-datastore-customermanageds3storage-keyprefix
            '''
            result = self._values.get("key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerManagedS3StorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.DatastorePartitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "partition": "partition",
            "timestamp_partition": "timestampPartition",
        },
    )
    class DatastorePartitionProperty:
        def __init__(
            self,
            *,
            partition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.PartitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timestamp_partition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.TimestampPartitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A single dimension to partition a data store.

            The dimension must be an ``AttributePartition`` or a ``TimestampPartition`` .

            :param partition: A partition dimension defined by an attribute.
            :param timestamp_partition: A partition dimension defined by a timestamp attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorepartition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                datastore_partition_property = iotanalytics_mixins.CfnDatastorePropsMixin.DatastorePartitionProperty(
                    partition=iotanalytics_mixins.CfnDatastorePropsMixin.PartitionProperty(
                        attribute_name="attributeName"
                    ),
                    timestamp_partition=iotanalytics_mixins.CfnDatastorePropsMixin.TimestampPartitionProperty(
                        attribute_name="attributeName",
                        timestamp_format="timestampFormat"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__117171690192e88eb6907964cc6b222fc71fce2a498d4450f2f2a21e21264b49)
                check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
                check_type(argname="argument timestamp_partition", value=timestamp_partition, expected_type=type_hints["timestamp_partition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if partition is not None:
                self._values["partition"] = partition
            if timestamp_partition is not None:
                self._values["timestamp_partition"] = timestamp_partition

        @builtins.property
        def partition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.PartitionProperty"]]:
            '''A partition dimension defined by an attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorepartition.html#cfn-iotanalytics-datastore-datastorepartition-partition
            '''
            result = self._values.get("partition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.PartitionProperty"]], result)

        @builtins.property
        def timestamp_partition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.TimestampPartitionProperty"]]:
            '''A partition dimension defined by a timestamp attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorepartition.html#cfn-iotanalytics-datastore-datastorepartition-timestamppartition
            '''
            result = self._values.get("timestamp_partition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.TimestampPartitionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatastorePartitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.DatastorePartitionsProperty",
        jsii_struct_bases=[],
        name_mapping={"partitions": "partitions"},
    )
    class DatastorePartitionsProperty:
        def __init__(
            self,
            *,
            partitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.DatastorePartitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information about the partition dimensions in a data store.

            :param partitions: A list of partition dimensions in a data store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorepartitions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                datastore_partitions_property = iotanalytics_mixins.CfnDatastorePropsMixin.DatastorePartitionsProperty(
                    partitions=[iotanalytics_mixins.CfnDatastorePropsMixin.DatastorePartitionProperty(
                        partition=iotanalytics_mixins.CfnDatastorePropsMixin.PartitionProperty(
                            attribute_name="attributeName"
                        ),
                        timestamp_partition=iotanalytics_mixins.CfnDatastorePropsMixin.TimestampPartitionProperty(
                            attribute_name="attributeName",
                            timestamp_format="timestampFormat"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1ff35f10242fd368dc4b4da7ebce7c8b2cfeb637fc39cbee7ddb74e40f039e2)
                check_type(argname="argument partitions", value=partitions, expected_type=type_hints["partitions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if partitions is not None:
                self._values["partitions"] = partitions

        @builtins.property
        def partitions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.DatastorePartitionProperty"]]]]:
            '''A list of partition dimensions in a data store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorepartitions.html#cfn-iotanalytics-datastore-datastorepartitions-partitions
            '''
            result = self._values.get("partitions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.DatastorePartitionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatastorePartitionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.DatastoreStorageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_managed_s3": "customerManagedS3",
            "iot_site_wise_multi_layer_storage": "iotSiteWiseMultiLayerStorage",
            "service_managed_s3": "serviceManagedS3",
        },
    )
    class DatastoreStorageProperty:
        def __init__(
            self,
            *,
            customer_managed_s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.CustomerManagedS3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_site_wise_multi_layer_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.IotSiteWiseMultiLayerStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_managed_s3: typing.Any = None,
        ) -> None:
            '''Where data store data is stored.

            :param customer_managed_s3: Use this to store data store data in an S3 bucket that you manage. The choice of service-managed or customer-managed S3 storage cannot be changed after creation of the data store.
            :param iot_site_wise_multi_layer_storage: Use this to store data used by AWS IoT SiteWise in an Amazon S3 bucket that you manage. You can't change the choice of Amazon S3 storage after your data store is created.
            :param service_managed_s3: Use this to store data store data in an S3 bucket managed by the AWS IoT Analytics service. The choice of service-managed or customer-managed S3 storage cannot be changed after creation of the data store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorestorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                # service_managed_s3: Any
                
                datastore_storage_property = iotanalytics_mixins.CfnDatastorePropsMixin.DatastoreStorageProperty(
                    customer_managed_s3=iotanalytics_mixins.CfnDatastorePropsMixin.CustomerManagedS3Property(
                        bucket="bucket",
                        key_prefix="keyPrefix",
                        role_arn="roleArn"
                    ),
                    iot_site_wise_multi_layer_storage=iotanalytics_mixins.CfnDatastorePropsMixin.IotSiteWiseMultiLayerStorageProperty(
                        customer_managed_s3_storage=iotanalytics_mixins.CfnDatastorePropsMixin.CustomerManagedS3StorageProperty(
                            bucket="bucket",
                            key_prefix="keyPrefix"
                        )
                    ),
                    service_managed_s3=service_managed_s3
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58728b597c5cae9a1e2422d1e01b051e0717dceb40d0f0b60449184d3c64bd34)
                check_type(argname="argument customer_managed_s3", value=customer_managed_s3, expected_type=type_hints["customer_managed_s3"])
                check_type(argname="argument iot_site_wise_multi_layer_storage", value=iot_site_wise_multi_layer_storage, expected_type=type_hints["iot_site_wise_multi_layer_storage"])
                check_type(argname="argument service_managed_s3", value=service_managed_s3, expected_type=type_hints["service_managed_s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_managed_s3 is not None:
                self._values["customer_managed_s3"] = customer_managed_s3
            if iot_site_wise_multi_layer_storage is not None:
                self._values["iot_site_wise_multi_layer_storage"] = iot_site_wise_multi_layer_storage
            if service_managed_s3 is not None:
                self._values["service_managed_s3"] = service_managed_s3

        @builtins.property
        def customer_managed_s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.CustomerManagedS3Property"]]:
            '''Use this to store data store data in an S3 bucket that you manage.

            The choice of service-managed or customer-managed S3 storage cannot be changed after creation of the data store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorestorage.html#cfn-iotanalytics-datastore-datastorestorage-customermanageds3
            '''
            result = self._values.get("customer_managed_s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.CustomerManagedS3Property"]], result)

        @builtins.property
        def iot_site_wise_multi_layer_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.IotSiteWiseMultiLayerStorageProperty"]]:
            '''Use this to store data used by AWS IoT SiteWise in an Amazon S3 bucket that you manage.

            You can't change the choice of Amazon S3 storage after your data store is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorestorage.html#cfn-iotanalytics-datastore-datastorestorage-iotsitewisemultilayerstorage
            '''
            result = self._values.get("iot_site_wise_multi_layer_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.IotSiteWiseMultiLayerStorageProperty"]], result)

        @builtins.property
        def service_managed_s3(self) -> typing.Any:
            '''Use this to store data store data in an S3 bucket managed by the AWS IoT Analytics service.

            The choice of service-managed or customer-managed S3 storage cannot be changed after creation of the data store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorestorage.html#cfn-iotanalytics-datastore-datastorestorage-servicemanageds3
            '''
            result = self._values.get("service_managed_s3")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatastoreStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.FileFormatConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "json_configuration": "jsonConfiguration",
            "parquet_configuration": "parquetConfiguration",
        },
    )
    class FileFormatConfigurationProperty:
        def __init__(
            self,
            *,
            json_configuration: typing.Any = None,
            parquet_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.ParquetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains the configuration information of file formats. AWS IoT Analytics data stores support JSON and `Parquet <https://docs.aws.amazon.com/https://parquet.apache.org/>`_ .

            The default file format is JSON. You can specify only one format.

            You can't change the file format after you create the data store.

            :param json_configuration: Contains the configuration information of the JSON format.
            :param parquet_configuration: Contains the configuration information of the Parquet format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-fileformatconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                # json_configuration: Any
                
                file_format_configuration_property = iotanalytics_mixins.CfnDatastorePropsMixin.FileFormatConfigurationProperty(
                    json_configuration=json_configuration,
                    parquet_configuration=iotanalytics_mixins.CfnDatastorePropsMixin.ParquetConfigurationProperty(
                        schema_definition=iotanalytics_mixins.CfnDatastorePropsMixin.SchemaDefinitionProperty(
                            columns=[iotanalytics_mixins.CfnDatastorePropsMixin.ColumnProperty(
                                name="name",
                                type="type"
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85e600824934a36af319ea068ced88bfcf573d66921d592acbedab92a6ee0913)
                check_type(argname="argument json_configuration", value=json_configuration, expected_type=type_hints["json_configuration"])
                check_type(argname="argument parquet_configuration", value=parquet_configuration, expected_type=type_hints["parquet_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if json_configuration is not None:
                self._values["json_configuration"] = json_configuration
            if parquet_configuration is not None:
                self._values["parquet_configuration"] = parquet_configuration

        @builtins.property
        def json_configuration(self) -> typing.Any:
            '''Contains the configuration information of the JSON format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-fileformatconfiguration.html#cfn-iotanalytics-datastore-fileformatconfiguration-jsonconfiguration
            '''
            result = self._values.get("json_configuration")
            return typing.cast(typing.Any, result)

        @builtins.property
        def parquet_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.ParquetConfigurationProperty"]]:
            '''Contains the configuration information of the Parquet format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-fileformatconfiguration.html#cfn-iotanalytics-datastore-fileformatconfiguration-parquetconfiguration
            '''
            result = self._values.get("parquet_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.ParquetConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileFormatConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.IotSiteWiseMultiLayerStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"customer_managed_s3_storage": "customerManagedS3Storage"},
    )
    class IotSiteWiseMultiLayerStorageProperty:
        def __init__(
            self,
            *,
            customer_managed_s3_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.CustomerManagedS3StorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Stores data used by AWS IoT SiteWise in an Amazon S3 bucket that you manage.

            You can't change the choice of Amazon S3 storage after your data store is created.

            :param customer_managed_s3_storage: Stores data used by AWS IoT SiteWise in an Amazon S3 bucket that you manage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-iotsitewisemultilayerstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                iot_site_wise_multi_layer_storage_property = iotanalytics_mixins.CfnDatastorePropsMixin.IotSiteWiseMultiLayerStorageProperty(
                    customer_managed_s3_storage=iotanalytics_mixins.CfnDatastorePropsMixin.CustomerManagedS3StorageProperty(
                        bucket="bucket",
                        key_prefix="keyPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da5032464eb5f2c96e8ac9cc2b8caa5097e4dd130195aa229fd69b26315e0f07)
                check_type(argname="argument customer_managed_s3_storage", value=customer_managed_s3_storage, expected_type=type_hints["customer_managed_s3_storage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_managed_s3_storage is not None:
                self._values["customer_managed_s3_storage"] = customer_managed_s3_storage

        @builtins.property
        def customer_managed_s3_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.CustomerManagedS3StorageProperty"]]:
            '''Stores data used by AWS IoT SiteWise in an Amazon S3 bucket that you manage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-iotsitewisemultilayerstorage.html#cfn-iotanalytics-datastore-iotsitewisemultilayerstorage-customermanageds3storage
            '''
            result = self._values.get("customer_managed_s3_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.CustomerManagedS3StorageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotSiteWiseMultiLayerStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.ParquetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"schema_definition": "schemaDefinition"},
    )
    class ParquetConfigurationProperty:
        def __init__(
            self,
            *,
            schema_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.SchemaDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains the configuration information of the Parquet format.

            :param schema_definition: Information needed to define a schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-parquetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                parquet_configuration_property = iotanalytics_mixins.CfnDatastorePropsMixin.ParquetConfigurationProperty(
                    schema_definition=iotanalytics_mixins.CfnDatastorePropsMixin.SchemaDefinitionProperty(
                        columns=[iotanalytics_mixins.CfnDatastorePropsMixin.ColumnProperty(
                            name="name",
                            type="type"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9001c1a8719f0418c7d3496afe9ffcb57e29481cf758ef21fe3e5876b60dcafb)
                check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schema_definition is not None:
                self._values["schema_definition"] = schema_definition

        @builtins.property
        def schema_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.SchemaDefinitionProperty"]]:
            '''Information needed to define a schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-parquetconfiguration.html#cfn-iotanalytics-datastore-parquetconfiguration-schemadefinition
            '''
            result = self._values.get("schema_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.SchemaDefinitionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParquetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.PartitionProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_name": "attributeName"},
    )
    class PartitionProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A single dimension to partition a data store.

            The dimension must be an ``AttributePartition`` or a ``TimestampPartition`` .

            :param attribute_name: The name of the attribute that defines a partition dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-partition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                partition_property = iotanalytics_mixins.CfnDatastorePropsMixin.PartitionProperty(
                    attribute_name="attributeName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2072106c73686ffc28a7f0695606e3229a060821d2d1438d189268ab54a9025b)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute that defines a partition dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-partition.html#cfn-iotanalytics-datastore-partition-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PartitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.RetentionPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"number_of_days": "numberOfDays", "unlimited": "unlimited"},
    )
    class RetentionPeriodProperty:
        def __init__(
            self,
            *,
            number_of_days: typing.Optional[jsii.Number] = None,
            unlimited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''How long, in days, message data is kept.

            :param number_of_days: The number of days that message data is kept. The ``unlimited`` parameter must be false.
            :param unlimited: If true, message data is kept indefinitely.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-retentionperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                retention_period_property = iotanalytics_mixins.CfnDatastorePropsMixin.RetentionPeriodProperty(
                    number_of_days=123,
                    unlimited=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77415cfd7d7c7371f1f78540b47cc3a6f9b509404a070751dc08bbc809c7fecd)
                check_type(argname="argument number_of_days", value=number_of_days, expected_type=type_hints["number_of_days"])
                check_type(argname="argument unlimited", value=unlimited, expected_type=type_hints["unlimited"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if number_of_days is not None:
                self._values["number_of_days"] = number_of_days
            if unlimited is not None:
                self._values["unlimited"] = unlimited

        @builtins.property
        def number_of_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days that message data is kept.

            The ``unlimited`` parameter must be false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-retentionperiod.html#cfn-iotanalytics-datastore-retentionperiod-numberofdays
            '''
            result = self._values.get("number_of_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unlimited(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If true, message data is kept indefinitely.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-retentionperiod.html#cfn-iotanalytics-datastore-retentionperiod-unlimited
            '''
            result = self._values.get("unlimited")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.SchemaDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"columns": "columns"},
    )
    class SchemaDefinitionProperty:
        def __init__(
            self,
            *,
            columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatastorePropsMixin.ColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information needed to define a schema.

            :param columns: Specifies one or more columns that store your data. Each schema can have up to 100 columns. Each column can have up to 100 nested types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-schemadefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                schema_definition_property = iotanalytics_mixins.CfnDatastorePropsMixin.SchemaDefinitionProperty(
                    columns=[iotanalytics_mixins.CfnDatastorePropsMixin.ColumnProperty(
                        name="name",
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0527e77f7c27f03ca8e449c55af6c9eadf95ced951dcb24bb7cf5243108a2ae)
                check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if columns is not None:
                self._values["columns"] = columns

        @builtins.property
        def columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.ColumnProperty"]]]]:
            '''Specifies one or more columns that store your data.

            Each schema can have up to 100 columns. Each column can have up to 100 nested types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-schemadefinition.html#cfn-iotanalytics-datastore-schemadefinition-columns
            '''
            result = self._values.get("columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatastorePropsMixin.ColumnProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnDatastorePropsMixin.TimestampPartitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "timestamp_format": "timestampFormat",
        },
    )
    class TimestampPartitionProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            timestamp_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A partition dimension defined by a timestamp attribute.

            :param attribute_name: The attribute name of the partition defined by a timestamp.
            :param timestamp_format: The timestamp format of a partition defined by a timestamp. The default format is seconds since epoch (January 1, 1970 at midnight UTC time).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-timestamppartition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                timestamp_partition_property = iotanalytics_mixins.CfnDatastorePropsMixin.TimestampPartitionProperty(
                    attribute_name="attributeName",
                    timestamp_format="timestampFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ddf0a8ef04fa2c0f8de5c55548dddbb8786cb0a49bbf845e4994a4b4e738cf46)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument timestamp_format", value=timestamp_format, expected_type=type_hints["timestamp_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if timestamp_format is not None:
                self._values["timestamp_format"] = timestamp_format

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''The attribute name of the partition defined by a timestamp.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-timestamppartition.html#cfn-iotanalytics-datastore-timestamppartition-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp_format(self) -> typing.Optional[builtins.str]:
            '''The timestamp format of a partition defined by a timestamp.

            The default format is seconds since epoch (January 1, 1970 at midnight UTC time).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-timestamppartition.html#cfn-iotanalytics-datastore-timestamppartition-timestampformat
            '''
            result = self._values.get("timestamp_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimestampPartitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelineMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "pipeline_activities": "pipelineActivities",
        "pipeline_name": "pipelineName",
        "tags": "tags",
    },
)
class CfnPipelineMixinProps:
    def __init__(
        self,
        *,
        pipeline_activities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ActivityProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPipelinePropsMixin.

        :param pipeline_activities: A list of "PipelineActivity" objects. Activities perform transformations on your messages, such as removing, renaming or adding message attributes; filtering messages based on attribute values; invoking your Lambda functions on messages for advanced processing; or performing mathematical transformations to normalize device data. The list can be 2-25 *PipelineActivity* objects and must contain both a ``channel`` and a ``datastore`` activity. Each entry in the list must contain only one activity, for example: ``pipelineActivities = [ { "channel": { ... } }, { "lambda": { ... } }, ... ]``
        :param pipeline_name: The name of the pipeline.
        :param tags: Metadata which can be used to manage the pipeline. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
            
            cfn_pipeline_mixin_props = iotanalytics_mixins.CfnPipelineMixinProps(
                pipeline_activities=[iotanalytics_mixins.CfnPipelinePropsMixin.ActivityProperty(
                    add_attributes=iotanalytics_mixins.CfnPipelinePropsMixin.AddAttributesProperty(
                        attributes={
                            "attributes_key": "attributes"
                        },
                        name="name",
                        next="next"
                    ),
                    channel=iotanalytics_mixins.CfnPipelinePropsMixin.ChannelProperty(
                        channel_name="channelName",
                        name="name",
                        next="next"
                    ),
                    datastore=iotanalytics_mixins.CfnPipelinePropsMixin.DatastoreProperty(
                        datastore_name="datastoreName",
                        name="name"
                    ),
                    device_registry_enrich=iotanalytics_mixins.CfnPipelinePropsMixin.DeviceRegistryEnrichProperty(
                        attribute="attribute",
                        name="name",
                        next="next",
                        role_arn="roleArn",
                        thing_name="thingName"
                    ),
                    device_shadow_enrich=iotanalytics_mixins.CfnPipelinePropsMixin.DeviceShadowEnrichProperty(
                        attribute="attribute",
                        name="name",
                        next="next",
                        role_arn="roleArn",
                        thing_name="thingName"
                    ),
                    filter=iotanalytics_mixins.CfnPipelinePropsMixin.FilterProperty(
                        filter="filter",
                        name="name",
                        next="next"
                    ),
                    lambda_=iotanalytics_mixins.CfnPipelinePropsMixin.LambdaProperty(
                        batch_size=123,
                        lambda_name="lambdaName",
                        name="name",
                        next="next"
                    ),
                    math=iotanalytics_mixins.CfnPipelinePropsMixin.MathProperty(
                        attribute="attribute",
                        math="math",
                        name="name",
                        next="next"
                    ),
                    remove_attributes=iotanalytics_mixins.CfnPipelinePropsMixin.RemoveAttributesProperty(
                        attributes=["attributes"],
                        name="name",
                        next="next"
                    ),
                    select_attributes=iotanalytics_mixins.CfnPipelinePropsMixin.SelectAttributesProperty(
                        attributes=["attributes"],
                        name="name",
                        next="next"
                    )
                )],
                pipeline_name="pipelineName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80dbc3408ffeb82612c0b94050fff8ba1025781b6840cbdbbbc8b62557b9d66)
            check_type(argname="argument pipeline_activities", value=pipeline_activities, expected_type=type_hints["pipeline_activities"])
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pipeline_activities is not None:
            self._values["pipeline_activities"] = pipeline_activities
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def pipeline_activities(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ActivityProperty"]]]]:
        '''A list of "PipelineActivity" objects.

        Activities perform transformations on your messages, such as removing, renaming or adding message attributes; filtering messages based on attribute values; invoking your Lambda functions on messages for advanced processing; or performing mathematical transformations to normalize device data.

        The list can be 2-25 *PipelineActivity* objects and must contain both a ``channel`` and a ``datastore`` activity. Each entry in the list must contain only one activity, for example:

        ``pipelineActivities = [ { "channel": { ... } }, { "lambda": { ... } }, ... ]``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-pipelineactivities
        '''
        result = self._values.get("pipeline_activities")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ActivityProperty"]]]], result)

    @builtins.property
    def pipeline_name(self) -> typing.Optional[builtins.str]:
        '''The name of the pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-pipelinename
        '''
        result = self._values.get("pipeline_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata which can be used to manage the pipeline.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPipelineMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPipelinePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin",
):
    '''The AWS::IoTAnalytics::Pipeline resource consumes messages from one or more channels and allows you to process the messages before storing them in a data store.

    You must specify both a ``channel`` and a ``datastore`` activity and, optionally, as many as 23 additional activities in the ``pipelineActivities`` array. For more information, see `How to Use AWS IoT Analytics <https://docs.aws.amazon.com/iotanalytics/latest/userguide/welcome.html#aws-iot-analytics-how>`_ in the *AWS IoT Analytics User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html
    :cloudformationResource: AWS::IoTAnalytics::Pipeline
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
        
        cfn_pipeline_props_mixin = iotanalytics_mixins.CfnPipelinePropsMixin(iotanalytics_mixins.CfnPipelineMixinProps(
            pipeline_activities=[iotanalytics_mixins.CfnPipelinePropsMixin.ActivityProperty(
                add_attributes=iotanalytics_mixins.CfnPipelinePropsMixin.AddAttributesProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    name="name",
                    next="next"
                ),
                channel=iotanalytics_mixins.CfnPipelinePropsMixin.ChannelProperty(
                    channel_name="channelName",
                    name="name",
                    next="next"
                ),
                datastore=iotanalytics_mixins.CfnPipelinePropsMixin.DatastoreProperty(
                    datastore_name="datastoreName",
                    name="name"
                ),
                device_registry_enrich=iotanalytics_mixins.CfnPipelinePropsMixin.DeviceRegistryEnrichProperty(
                    attribute="attribute",
                    name="name",
                    next="next",
                    role_arn="roleArn",
                    thing_name="thingName"
                ),
                device_shadow_enrich=iotanalytics_mixins.CfnPipelinePropsMixin.DeviceShadowEnrichProperty(
                    attribute="attribute",
                    name="name",
                    next="next",
                    role_arn="roleArn",
                    thing_name="thingName"
                ),
                filter=iotanalytics_mixins.CfnPipelinePropsMixin.FilterProperty(
                    filter="filter",
                    name="name",
                    next="next"
                ),
                lambda_=iotanalytics_mixins.CfnPipelinePropsMixin.LambdaProperty(
                    batch_size=123,
                    lambda_name="lambdaName",
                    name="name",
                    next="next"
                ),
                math=iotanalytics_mixins.CfnPipelinePropsMixin.MathProperty(
                    attribute="attribute",
                    math="math",
                    name="name",
                    next="next"
                ),
                remove_attributes=iotanalytics_mixins.CfnPipelinePropsMixin.RemoveAttributesProperty(
                    attributes=["attributes"],
                    name="name",
                    next="next"
                ),
                select_attributes=iotanalytics_mixins.CfnPipelinePropsMixin.SelectAttributesProperty(
                    attributes=["attributes"],
                    name="name",
                    next="next"
                )
            )],
            pipeline_name="pipelineName",
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
        props: typing.Union[CfnPipelineMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTAnalytics::Pipeline``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf28979c71ad66213d13acb323577355e68a3ae80b9ffc8bc597657fd31e2aff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__557f7c9f9c7ffa795378bccf95f072322a7faf96bb17a694cb1b6ded7cc9b5d5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc68b7d194dc7f50565ef5424f90d507bc6f745f6e373a2a1782a58dce3a149)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPipelineMixinProps:
        return typing.cast(CfnPipelineMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.ActivityProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_attributes": "addAttributes",
            "channel": "channel",
            "datastore": "datastore",
            "device_registry_enrich": "deviceRegistryEnrich",
            "device_shadow_enrich": "deviceShadowEnrich",
            "filter": "filter",
            "lambda_": "lambda",
            "math": "math",
            "remove_attributes": "removeAttributes",
            "select_attributes": "selectAttributes",
        },
    )
    class ActivityProperty:
        def __init__(
            self,
            *,
            add_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.AddAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            channel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ChannelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            datastore: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.DatastoreProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            device_registry_enrich: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.DeviceRegistryEnrichProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            device_shadow_enrich: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.DeviceShadowEnrichProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.FilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.LambdaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            math: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.MathProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            remove_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.RemoveAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            select_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.SelectAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An activity that performs a transformation on a message.

            :param add_attributes: Adds other attributes based on existing attributes in the message.
            :param channel: Determines the source of the messages to be processed.
            :param datastore: Specifies where to store the processed message data.
            :param device_registry_enrich: Adds data from the AWS IoT device registry to your message.
            :param device_shadow_enrich: Adds information from the AWS IoT Device Shadows service to a message.
            :param filter: Filters a message based on its attributes.
            :param lambda_: Runs a Lambda function to modify the message.
            :param math: Computes an arithmetic expression using the message's attributes and adds it to the message.
            :param remove_attributes: Removes attributes from a message.
            :param select_attributes: Creates a new message using only the specified attributes from the original message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                activity_property = iotanalytics_mixins.CfnPipelinePropsMixin.ActivityProperty(
                    add_attributes=iotanalytics_mixins.CfnPipelinePropsMixin.AddAttributesProperty(
                        attributes={
                            "attributes_key": "attributes"
                        },
                        name="name",
                        next="next"
                    ),
                    channel=iotanalytics_mixins.CfnPipelinePropsMixin.ChannelProperty(
                        channel_name="channelName",
                        name="name",
                        next="next"
                    ),
                    datastore=iotanalytics_mixins.CfnPipelinePropsMixin.DatastoreProperty(
                        datastore_name="datastoreName",
                        name="name"
                    ),
                    device_registry_enrich=iotanalytics_mixins.CfnPipelinePropsMixin.DeviceRegistryEnrichProperty(
                        attribute="attribute",
                        name="name",
                        next="next",
                        role_arn="roleArn",
                        thing_name="thingName"
                    ),
                    device_shadow_enrich=iotanalytics_mixins.CfnPipelinePropsMixin.DeviceShadowEnrichProperty(
                        attribute="attribute",
                        name="name",
                        next="next",
                        role_arn="roleArn",
                        thing_name="thingName"
                    ),
                    filter=iotanalytics_mixins.CfnPipelinePropsMixin.FilterProperty(
                        filter="filter",
                        name="name",
                        next="next"
                    ),
                    lambda_=iotanalytics_mixins.CfnPipelinePropsMixin.LambdaProperty(
                        batch_size=123,
                        lambda_name="lambdaName",
                        name="name",
                        next="next"
                    ),
                    math=iotanalytics_mixins.CfnPipelinePropsMixin.MathProperty(
                        attribute="attribute",
                        math="math",
                        name="name",
                        next="next"
                    ),
                    remove_attributes=iotanalytics_mixins.CfnPipelinePropsMixin.RemoveAttributesProperty(
                        attributes=["attributes"],
                        name="name",
                        next="next"
                    ),
                    select_attributes=iotanalytics_mixins.CfnPipelinePropsMixin.SelectAttributesProperty(
                        attributes=["attributes"],
                        name="name",
                        next="next"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04ab8ac97bfa78d6c75b3696c19ce0d780a4a5bb3d1cfddfd91c4de146900f69)
                check_type(argname="argument add_attributes", value=add_attributes, expected_type=type_hints["add_attributes"])
                check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
                check_type(argname="argument datastore", value=datastore, expected_type=type_hints["datastore"])
                check_type(argname="argument device_registry_enrich", value=device_registry_enrich, expected_type=type_hints["device_registry_enrich"])
                check_type(argname="argument device_shadow_enrich", value=device_shadow_enrich, expected_type=type_hints["device_shadow_enrich"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
                check_type(argname="argument math", value=math, expected_type=type_hints["math"])
                check_type(argname="argument remove_attributes", value=remove_attributes, expected_type=type_hints["remove_attributes"])
                check_type(argname="argument select_attributes", value=select_attributes, expected_type=type_hints["select_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_attributes is not None:
                self._values["add_attributes"] = add_attributes
            if channel is not None:
                self._values["channel"] = channel
            if datastore is not None:
                self._values["datastore"] = datastore
            if device_registry_enrich is not None:
                self._values["device_registry_enrich"] = device_registry_enrich
            if device_shadow_enrich is not None:
                self._values["device_shadow_enrich"] = device_shadow_enrich
            if filter is not None:
                self._values["filter"] = filter
            if lambda_ is not None:
                self._values["lambda_"] = lambda_
            if math is not None:
                self._values["math"] = math
            if remove_attributes is not None:
                self._values["remove_attributes"] = remove_attributes
            if select_attributes is not None:
                self._values["select_attributes"] = select_attributes

        @builtins.property
        def add_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.AddAttributesProperty"]]:
            '''Adds other attributes based on existing attributes in the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-addattributes
            '''
            result = self._values.get("add_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.AddAttributesProperty"]], result)

        @builtins.property
        def channel(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ChannelProperty"]]:
            '''Determines the source of the messages to be processed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-channel
            '''
            result = self._values.get("channel")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ChannelProperty"]], result)

        @builtins.property
        def datastore(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.DatastoreProperty"]]:
            '''Specifies where to store the processed message data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-datastore
            '''
            result = self._values.get("datastore")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.DatastoreProperty"]], result)

        @builtins.property
        def device_registry_enrich(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.DeviceRegistryEnrichProperty"]]:
            '''Adds data from the AWS IoT device registry to your message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-deviceregistryenrich
            '''
            result = self._values.get("device_registry_enrich")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.DeviceRegistryEnrichProperty"]], result)

        @builtins.property
        def device_shadow_enrich(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.DeviceShadowEnrichProperty"]]:
            '''Adds information from the AWS IoT Device Shadows service to a message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-deviceshadowenrich
            '''
            result = self._values.get("device_shadow_enrich")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.DeviceShadowEnrichProperty"]], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.FilterProperty"]]:
            '''Filters a message based on its attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.FilterProperty"]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.LambdaProperty"]]:
            '''Runs a Lambda function to modify the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.LambdaProperty"]], result)

        @builtins.property
        def math(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.MathProperty"]]:
            '''Computes an arithmetic expression using the message's attributes and adds it to the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-math
            '''
            result = self._values.get("math")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.MathProperty"]], result)

        @builtins.property
        def remove_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.RemoveAttributesProperty"]]:
            '''Removes attributes from a message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-removeattributes
            '''
            result = self._values.get("remove_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.RemoveAttributesProperty"]], result)

        @builtins.property
        def select_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.SelectAttributesProperty"]]:
            '''Creates a new message using only the specified attributes from the original message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-selectattributes
            '''
            result = self._values.get("select_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.SelectAttributesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActivityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.AddAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "name": "name", "next": "next"},
    )
    class AddAttributesProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
            next: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An activity that adds other attributes based on existing attributes in the message.

            :param attributes: A list of 1-50 "AttributeNameMapping" objects that map an existing attribute to a new attribute. .. epigraph:: The existing attributes remain in the message, so if you want to remove the originals, use "RemoveAttributeActivity".
            :param name: The name of the 'addAttributes' activity.
            :param next: The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                add_attributes_property = iotanalytics_mixins.CfnPipelinePropsMixin.AddAttributesProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    name="name",
                    next="next"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2dc95d91ca86d44d58980162feb21d5aa26a520bb9d4c05b4f57063102c821eb)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument next", value=next, expected_type=type_hints["next"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A list of 1-50 "AttributeNameMapping" objects that map an existing attribute to a new attribute.

            .. epigraph::

               The existing attributes remain in the message, so if you want to remove the originals, use "RemoveAttributeActivity".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html#cfn-iotanalytics-pipeline-addattributes-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the 'addAttributes' activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html#cfn-iotanalytics-pipeline-addattributes-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next(self) -> typing.Optional[builtins.str]:
            '''The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html#cfn-iotanalytics-pipeline-addattributes-next
            '''
            result = self._values.get("next")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.ChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"channel_name": "channelName", "name": "name", "next": "next"},
    )
    class ChannelProperty:
        def __init__(
            self,
            *,
            channel_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            next: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Determines the source of the messages to be processed.

            :param channel_name: The name of the channel from which the messages are processed.
            :param name: The name of the 'channel' activity.
            :param next: The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                channel_property = iotanalytics_mixins.CfnPipelinePropsMixin.ChannelProperty(
                    channel_name="channelName",
                    name="name",
                    next="next"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__846e1ab1cd7905d85e802d6fd639aa29ea4bb0d52704e6fc2100f690689b5cbe)
                check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument next", value=next, expected_type=type_hints["next"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_name is not None:
                self._values["channel_name"] = channel_name
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def channel_name(self) -> typing.Optional[builtins.str]:
            '''The name of the channel from which the messages are processed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html#cfn-iotanalytics-pipeline-channel-channelname
            '''
            result = self._values.get("channel_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the 'channel' activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html#cfn-iotanalytics-pipeline-channel-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next(self) -> typing.Optional[builtins.str]:
            '''The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html#cfn-iotanalytics-pipeline-channel-next
            '''
            result = self._values.get("next")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.DatastoreProperty",
        jsii_struct_bases=[],
        name_mapping={"datastore_name": "datastoreName", "name": "name"},
    )
    class DatastoreProperty:
        def __init__(
            self,
            *,
            datastore_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The datastore activity that specifies where to store the processed data.

            :param datastore_name: The name of the data store where processed messages are stored.
            :param name: The name of the datastore activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-datastore.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                datastore_property = iotanalytics_mixins.CfnPipelinePropsMixin.DatastoreProperty(
                    datastore_name="datastoreName",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__028f7f6c8fbd980e035d36ed7d0946798af7d6825dfd367e6e9bb69c1e636fa3)
                check_type(argname="argument datastore_name", value=datastore_name, expected_type=type_hints["datastore_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if datastore_name is not None:
                self._values["datastore_name"] = datastore_name
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def datastore_name(self) -> typing.Optional[builtins.str]:
            '''The name of the data store where processed messages are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-datastore.html#cfn-iotanalytics-pipeline-datastore-datastorename
            '''
            result = self._values.get("datastore_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the datastore activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-datastore.html#cfn-iotanalytics-pipeline-datastore-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatastoreProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.DeviceRegistryEnrichProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute": "attribute",
            "name": "name",
            "next": "next",
            "role_arn": "roleArn",
            "thing_name": "thingName",
        },
    )
    class DeviceRegistryEnrichProperty:
        def __init__(
            self,
            *,
            attribute: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            next: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            thing_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An activity that adds data from the AWS IoT device registry to your message.

            :param attribute: The name of the attribute that is added to the message.
            :param name: The name of the 'deviceRegistryEnrich' activity.
            :param next: The next activity in the pipeline.
            :param role_arn: The ARN of the role that allows access to the device's registry information.
            :param thing_name: The name of the IoT device whose registry information is added to the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                device_registry_enrich_property = iotanalytics_mixins.CfnPipelinePropsMixin.DeviceRegistryEnrichProperty(
                    attribute="attribute",
                    name="name",
                    next="next",
                    role_arn="roleArn",
                    thing_name="thingName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f71a8dc6e36e7637a6952fd89d6b12170d18599ea28cb4c76c5067c6d11bc979)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument next", value=next, expected_type=type_hints["next"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument thing_name", value=thing_name, expected_type=type_hints["thing_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if thing_name is not None:
                self._values["thing_name"] = thing_name

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute that is added to the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the 'deviceRegistryEnrich' activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next(self) -> typing.Optional[builtins.str]:
            '''The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-next
            '''
            result = self._values.get("next")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that allows access to the device's registry information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def thing_name(self) -> typing.Optional[builtins.str]:
            '''The name of the IoT device whose registry information is added to the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-thingname
            '''
            result = self._values.get("thing_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceRegistryEnrichProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.DeviceShadowEnrichProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute": "attribute",
            "name": "name",
            "next": "next",
            "role_arn": "roleArn",
            "thing_name": "thingName",
        },
    )
    class DeviceShadowEnrichProperty:
        def __init__(
            self,
            *,
            attribute: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            next: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            thing_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An activity that adds information from the AWS IoT Device Shadows service to a message.

            :param attribute: The name of the attribute that is added to the message.
            :param name: The name of the 'deviceShadowEnrich' activity.
            :param next: The next activity in the pipeline.
            :param role_arn: The ARN of the role that allows access to the device's shadow.
            :param thing_name: The name of the IoT device whose shadow information is added to the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                device_shadow_enrich_property = iotanalytics_mixins.CfnPipelinePropsMixin.DeviceShadowEnrichProperty(
                    attribute="attribute",
                    name="name",
                    next="next",
                    role_arn="roleArn",
                    thing_name="thingName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f237ee750b9f0e76582495d9d79c8648fca4a57d454ee552ddd7af80326f533)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument next", value=next, expected_type=type_hints["next"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument thing_name", value=thing_name, expected_type=type_hints["thing_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if thing_name is not None:
                self._values["thing_name"] = thing_name

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute that is added to the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the 'deviceShadowEnrich' activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next(self) -> typing.Optional[builtins.str]:
            '''The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-next
            '''
            result = self._values.get("next")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that allows access to the device's shadow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def thing_name(self) -> typing.Optional[builtins.str]:
            '''The name of the IoT device whose shadow information is added to the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-thingname
            '''
            result = self._values.get("thing_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceShadowEnrichProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"filter": "filter", "name": "name", "next": "next"},
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            filter: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            next: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An activity that filters a message based on its attributes.

            :param filter: An expression that looks like an SQL WHERE clause that must return a Boolean value.
            :param name: The name of the 'filter' activity.
            :param next: The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                filter_property = iotanalytics_mixins.CfnPipelinePropsMixin.FilterProperty(
                    filter="filter",
                    name="name",
                    next="next"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16f8df9278e8d9f39044c386e80bd20cb2607b68dcd7c7aa720a40ce2c0e2e58)
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument next", value=next, expected_type=type_hints["next"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter is not None:
                self._values["filter"] = filter
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def filter(self) -> typing.Optional[builtins.str]:
            '''An expression that looks like an SQL WHERE clause that must return a Boolean value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html#cfn-iotanalytics-pipeline-filter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the 'filter' activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html#cfn-iotanalytics-pipeline-filter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next(self) -> typing.Optional[builtins.str]:
            '''The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html#cfn-iotanalytics-pipeline-filter-next
            '''
            result = self._values.get("next")
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
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.LambdaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "lambda_name": "lambdaName",
            "name": "name",
            "next": "next",
        },
    )
    class LambdaProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            lambda_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            next: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An activity that runs a Lambda function to modify the message.

            :param batch_size: The number of messages passed to the Lambda function for processing. The AWS Lambda function must be able to process all of these messages within five minutes, which is the maximum timeout duration for Lambda functions.
            :param lambda_name: The name of the Lambda function that is run on the message.
            :param name: The name of the 'lambda' activity.
            :param next: The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                lambda_property = iotanalytics_mixins.CfnPipelinePropsMixin.LambdaProperty(
                    batch_size=123,
                    lambda_name="lambdaName",
                    name="name",
                    next="next"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e12d601a7ae954949090fe0f259abc9214b92a976214bf16be70b4008012aba)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument lambda_name", value=lambda_name, expected_type=type_hints["lambda_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument next", value=next, expected_type=type_hints["next"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if lambda_name is not None:
                self._values["lambda_name"] = lambda_name
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''The number of messages passed to the Lambda function for processing.

            The AWS Lambda function must be able to process all of these messages within five minutes, which is the maximum timeout duration for Lambda functions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lambda_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Lambda function that is run on the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-lambdaname
            '''
            result = self._values.get("lambda_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the 'lambda' activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next(self) -> typing.Optional[builtins.str]:
            '''The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-next
            '''
            result = self._values.get("next")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.MathProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute": "attribute",
            "math": "math",
            "name": "name",
            "next": "next",
        },
    )
    class MathProperty:
        def __init__(
            self,
            *,
            attribute: typing.Optional[builtins.str] = None,
            math: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            next: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An activity that computes an arithmetic expression using the message's attributes.

            :param attribute: The name of the attribute that contains the result of the math operation.
            :param math: An expression that uses one or more existing attributes and must return an integer value.
            :param name: The name of the 'math' activity.
            :param next: The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                math_property = iotanalytics_mixins.CfnPipelinePropsMixin.MathProperty(
                    attribute="attribute",
                    math="math",
                    name="name",
                    next="next"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5bebbe8f809b429444833912ed79f6e2dd80c1c271040e09b33425c4a36cc7b)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument math", value=math, expected_type=type_hints["math"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument next", value=next, expected_type=type_hints["next"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute
            if math is not None:
                self._values["math"] = math
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute that contains the result of the math operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def math(self) -> typing.Optional[builtins.str]:
            '''An expression that uses one or more existing attributes and must return an integer value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-math
            '''
            result = self._values.get("math")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the 'math' activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next(self) -> typing.Optional[builtins.str]:
            '''The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-next
            '''
            result = self._values.get("next")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MathProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.RemoveAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "name": "name", "next": "next"},
    )
    class RemoveAttributesProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
            next: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An activity that removes attributes from a message.

            :param attributes: A list of 1-50 attributes to remove from the message.
            :param name: The name of the 'removeAttributes' activity.
            :param next: The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                remove_attributes_property = iotanalytics_mixins.CfnPipelinePropsMixin.RemoveAttributesProperty(
                    attributes=["attributes"],
                    name="name",
                    next="next"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__374f5f62312745f119fdc50dfee02fc118d0cd400c8e6156570a076487759be9)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument next", value=next, expected_type=type_hints["next"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def attributes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of 1-50 attributes to remove from the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html#cfn-iotanalytics-pipeline-removeattributes-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the 'removeAttributes' activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html#cfn-iotanalytics-pipeline-removeattributes-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next(self) -> typing.Optional[builtins.str]:
            '''The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html#cfn-iotanalytics-pipeline-removeattributes-next
            '''
            result = self._values.get("next")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RemoveAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.mixins.CfnPipelinePropsMixin.SelectAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "name": "name", "next": "next"},
    )
    class SelectAttributesProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
            next: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Creates a new message using only the specified attributes from the original message.

            :param attributes: A list of the attributes to select from the message.
            :param name: The name of the 'selectAttributes' activity.
            :param next: The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotanalytics import mixins as iotanalytics_mixins
                
                select_attributes_property = iotanalytics_mixins.CfnPipelinePropsMixin.SelectAttributesProperty(
                    attributes=["attributes"],
                    name="name",
                    next="next"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f5bccbc42c41a99580784827939b840b2d295744ace31915df6b53d895de929c)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument next", value=next, expected_type=type_hints["next"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def attributes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of the attributes to select from the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html#cfn-iotanalytics-pipeline-selectattributes-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the 'selectAttributes' activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html#cfn-iotanalytics-pipeline-selectattributes-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next(self) -> typing.Optional[builtins.str]:
            '''The next activity in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html#cfn-iotanalytics-pipeline-selectattributes-next
            '''
            result = self._values.get("next")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelectAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnChannelMixinProps",
    "CfnChannelPropsMixin",
    "CfnDatasetMixinProps",
    "CfnDatasetPropsMixin",
    "CfnDatastoreMixinProps",
    "CfnDatastorePropsMixin",
    "CfnPipelineMixinProps",
    "CfnPipelinePropsMixin",
]

publication.publish()

def _typecheckingstub__81f8e27d38bcc140badd0a57bf414295162b53fe0dbc87ea8c6454424e1ec3c6(
    *,
    channel_name: typing.Optional[builtins.str] = None,
    channel_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.ChannelStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retention_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.RetentionPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef344f8e7ce27f11c73da05e5111a9df775ec09e9320f888f6d5f33ab97b73a(
    props: typing.Union[CfnChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5f9cd143fb25595c21fc41931e6170967829107335b615208efcdbbcbce138(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6611f1b8a588a843ccc3c4394bb82855cfd1d7e29e473db8ce4107d6de92e26b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f143154be19135037fe63eff78c141e426ac3caf7ca3dd060a3164025978d6c(
    *,
    customer_managed_s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.CustomerManagedS3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_managed_s3: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354d5a36352656917d5d9133944fce6737e8249689042080ea9dd6abe74616e0(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key_prefix: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5e321365eaf618a11ee8d7352df06797351f189b5c9397d3061a7290412701(
    *,
    number_of_days: typing.Optional[jsii.Number] = None,
    unlimited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf172f8d1d995cfb26cb76bcd1c8d908e8042e3628e9e896fda41b121e4fe7b0(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    content_delivery_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DatasetContentDeliveryRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    dataset_name: typing.Optional[builtins.str] = None,
    late_data_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.LateDataRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    retention_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.RetentionPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    triggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.TriggerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    versioning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.VersioningConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf6f89b8c14212170fcd4160573b43c2e2cafeb32ce768374095ca6eeb567c5(
    props: typing.Union[CfnDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e046d450189de573e65c06137b6de447a75ab1603dbb2b2eb20ab6a12cf0795c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9565f55fe367dad4c7879a5525c039d88b4ebda5161f6de0be9a60a48b99b3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc1b632148f786a7d67ce6df0392e1a6cce9170baf09f1b7c3536226f257681(
    *,
    action_name: typing.Optional[builtins.str] = None,
    container_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.ContainerActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    query_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.QueryActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4017760bb4b7d5c4f700fac0ef8c1069343492358a37c1c53c5376099ebe79(
    *,
    execution_role_arn: typing.Optional[builtins.str] = None,
    image: typing.Optional[builtins.str] = None,
    resource_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.ResourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.VariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025683e9e537c0849a47606bf24a547471e99b2c1d77ddbf65824b6e10bebce8(
    *,
    iot_events_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.IotEventsDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a6e28dcc726370dc127cd694ba9afc57f3246f618f25030dee98fb685e8556(
    *,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DatasetContentDeliveryRuleDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    entry_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec6a0f80b32c93ff838b05d5f90c5fb390a50fe25b01948561dd167c6753875(
    *,
    dataset_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128239e956d4164b3e1ae145e0653df84fa46b85d87cb607795c4b2d90886bd3(
    *,
    offset_seconds: typing.Optional[jsii.Number] = None,
    time_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4e0c385c9f40e6ea6cf145d18405f051ac402dbc7440cb8474717271ede2dd(
    *,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec55b10392ceafd17007015be0804f127249bf007ab8518eb1bc4e5b3e92859(
    *,
    delta_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DeltaTimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431fd53b28240e972e2ed79d0852e4f0fc08da703b11903c11bab0e239f75999(
    *,
    database_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963e75b26b2906ad19cf6c7b1ce050a3caa6ba26f86c8143350e421700aabdce(
    *,
    input_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6d41a2ce4f6e5da4b44a623788de449ace4c0ff3da762b010cf1d5aab5239c(
    *,
    delta_time_session_window_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DeltaTimeSessionWindowConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358fb54bc1603828f06990777332120d0d29f6485f5e6484bafe7be312da0f0d(
    *,
    rule_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.LateDataRuleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a78d67e4e332acb3c9c8edb5a3d1d279812385ba6520282a34e40a41bc46c22(
    *,
    file_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a5cd8af2d27237ab4ef850ddb1e9ab0ff46f5f4693f5fecbc633ba0cf5aae3(
    *,
    filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.FilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    sql_query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae234006d61f854dc598cdd309d833ab588fc4903a8c6f54e6748162524ebcea(
    *,
    compute_type: typing.Optional[builtins.str] = None,
    volume_size_in_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79edda129c1b099feab7c440a1fd225c8de10e00d8babc98e71f7be93f64760(
    *,
    number_of_days: typing.Optional[jsii.Number] = None,
    unlimited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55a6303a322b63ed2e9c60600396e0308bb706fb2c935c791c9cc55ad2ebd85(
    *,
    bucket: typing.Optional[builtins.str] = None,
    glue_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.GlueConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ea45d566a9bba3a4308f01668d6d5add2c0d86feb4697a4a6477d57c2317aa(
    *,
    schedule_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ceb68d49b3538b76d6ab7c6eabf5d6e2de1be360275661dff62252f78c35eb6(
    *,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    triggering_dataset: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.TriggeringDatasetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca0eb3c573b14bc914dc46e7b7bb44220b9c63a95a0bbd8e622fae36c39c782(
    *,
    dataset_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168933c4b44bbfca010fa9f7ed848f5ff445c9127583a0f3f6289dd624de4974(
    *,
    dataset_content_version_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DatasetContentVersionValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    output_file_uri_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.OutputFileUriValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    string_value: typing.Optional[builtins.str] = None,
    variable_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62da840eca6e7c206c25cd0630c4ac0a9fb982adf2a5595c62ba8ced98025cd7(
    *,
    max_versions: typing.Optional[jsii.Number] = None,
    unlimited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2531678c39bf8733364948ef4e5ec694fb33a59eb0ac5de33038b89445e9290e(
    *,
    datastore_name: typing.Optional[builtins.str] = None,
    datastore_partitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.DatastorePartitionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    datastore_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.DatastoreStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file_format_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.FileFormatConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retention_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.RetentionPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4193dea9e816294bcf36efd314f36ca3a9af406826e4d27a07f2eb2a83f148(
    props: typing.Union[CfnDatastoreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5880381c3827b7968b462e245fefe0ed88a446b0682fe35e65819e98266f0c7c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e03177b1a85340f0903852443f74cd51c0cea2658acf3cda110a9787db17cdb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5f3f753d3689a4def067b2f2ae0b45fc027fe5c320cdac53841f0003648a3e(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a566abb89c42bd3c0d98baf07cebb5f917ed46cb4bc1d527b0d765814bd90a1f(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key_prefix: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b9be96b91db13d4cef38d6b4207168be1fee61ae4885aa71feae520c0952f0(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117171690192e88eb6907964cc6b222fc71fce2a498d4450f2f2a21e21264b49(
    *,
    partition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.PartitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timestamp_partition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.TimestampPartitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ff35f10242fd368dc4b4da7ebce7c8b2cfeb637fc39cbee7ddb74e40f039e2(
    *,
    partitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.DatastorePartitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58728b597c5cae9a1e2422d1e01b051e0717dceb40d0f0b60449184d3c64bd34(
    *,
    customer_managed_s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.CustomerManagedS3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_site_wise_multi_layer_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.IotSiteWiseMultiLayerStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_managed_s3: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e600824934a36af319ea068ced88bfcf573d66921d592acbedab92a6ee0913(
    *,
    json_configuration: typing.Any = None,
    parquet_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.ParquetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5032464eb5f2c96e8ac9cc2b8caa5097e4dd130195aa229fd69b26315e0f07(
    *,
    customer_managed_s3_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.CustomerManagedS3StorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9001c1a8719f0418c7d3496afe9ffcb57e29481cf758ef21fe3e5876b60dcafb(
    *,
    schema_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.SchemaDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2072106c73686ffc28a7f0695606e3229a060821d2d1438d189268ab54a9025b(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77415cfd7d7c7371f1f78540b47cc3a6f9b509404a070751dc08bbc809c7fecd(
    *,
    number_of_days: typing.Optional[jsii.Number] = None,
    unlimited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0527e77f7c27f03ca8e449c55af6c9eadf95ced951dcb24bb7cf5243108a2ae(
    *,
    columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatastorePropsMixin.ColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf0a8ef04fa2c0f8de5c55548dddbb8786cb0a49bbf845e4994a4b4e738cf46(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    timestamp_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80dbc3408ffeb82612c0b94050fff8ba1025781b6840cbdbbbc8b62557b9d66(
    *,
    pipeline_activities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ActivityProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf28979c71ad66213d13acb323577355e68a3ae80b9ffc8bc597657fd31e2aff(
    props: typing.Union[CfnPipelineMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557f7c9f9c7ffa795378bccf95f072322a7faf96bb17a694cb1b6ded7cc9b5d5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc68b7d194dc7f50565ef5424f90d507bc6f745f6e373a2a1782a58dce3a149(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ab8ac97bfa78d6c75b3696c19ce0d780a4a5bb3d1cfddfd91c4de146900f69(
    *,
    add_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.AddAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    channel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ChannelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    datastore: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.DatastoreProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    device_registry_enrich: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.DeviceRegistryEnrichProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    device_shadow_enrich: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.DeviceShadowEnrichProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.FilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.LambdaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    math: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.MathProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    remove_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.RemoveAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    select_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.SelectAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc95d91ca86d44d58980162feb21d5aa26a520bb9d4c05b4f57063102c821eb(
    *,
    attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    next: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846e1ab1cd7905d85e802d6fd639aa29ea4bb0d52704e6fc2100f690689b5cbe(
    *,
    channel_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    next: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028f7f6c8fbd980e035d36ed7d0946798af7d6825dfd367e6e9bb69c1e636fa3(
    *,
    datastore_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71a8dc6e36e7637a6952fd89d6b12170d18599ea28cb4c76c5067c6d11bc979(
    *,
    attribute: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    next: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    thing_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f237ee750b9f0e76582495d9d79c8648fca4a57d454ee552ddd7af80326f533(
    *,
    attribute: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    next: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    thing_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f8df9278e8d9f39044c386e80bd20cb2607b68dcd7c7aa720a40ce2c0e2e58(
    *,
    filter: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    next: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e12d601a7ae954949090fe0f259abc9214b92a976214bf16be70b4008012aba(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    lambda_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    next: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bebbe8f809b429444833912ed79f6e2dd80c1c271040e09b33425c4a36cc7b(
    *,
    attribute: typing.Optional[builtins.str] = None,
    math: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    next: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374f5f62312745f119fdc50dfee02fc118d0cd400c8e6156570a076487759be9(
    *,
    attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    next: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bccbc42c41a99580784827939b840b2d295744ace31915df6b53d895de929c(
    *,
    attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    next: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
