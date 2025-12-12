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
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisvideo.mixins.CfnSignalingChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "message_ttl_seconds": "messageTtlSeconds",
        "name": "name",
        "tags": "tags",
        "type": "type",
    },
)
class CfnSignalingChannelMixinProps:
    def __init__(
        self,
        *,
        message_ttl_seconds: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSignalingChannelPropsMixin.

        :param message_ttl_seconds: The period of time (in seconds) a signaling channel retains undelivered messages before they are discarded. Use ``API_UpdateSignalingChannel`` to update this value.
        :param name: A name for the signaling channel that you are creating. It must be unique for each AWS account and AWS Region .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: A type of the signaling channel that you are creating. Currently, ``SINGLE_MASTER`` is the only supported channel type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesisvideo import mixins as kinesisvideo_mixins
            
            cfn_signaling_channel_mixin_props = kinesisvideo_mixins.CfnSignalingChannelMixinProps(
                message_ttl_seconds=123,
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d25f15c9cf285c90c98b29c2a9bcdcf733e85beca8f58e35e19eb32b57fbb2)
            check_type(argname="argument message_ttl_seconds", value=message_ttl_seconds, expected_type=type_hints["message_ttl_seconds"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message_ttl_seconds is not None:
            self._values["message_ttl_seconds"] = message_ttl_seconds
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def message_ttl_seconds(self) -> typing.Optional[jsii.Number]:
        '''The period of time (in seconds) a signaling channel retains undelivered messages before they are discarded.

        Use ``API_UpdateSignalingChannel`` to update this value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-messagettlseconds
        '''
        result = self._values.get("message_ttl_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the signaling channel that you are creating.

        It must be unique for each AWS account and AWS Region .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''A type of the signaling channel that you are creating.

        Currently, ``SINGLE_MASTER`` is the only supported channel type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSignalingChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSignalingChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisvideo.mixins.CfnSignalingChannelPropsMixin",
):
    '''Specifies a signaling channel.

    ``CreateSignalingChannel`` is an asynchronous operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html
    :cloudformationResource: AWS::KinesisVideo::SignalingChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesisvideo import mixins as kinesisvideo_mixins
        
        cfn_signaling_channel_props_mixin = kinesisvideo_mixins.CfnSignalingChannelPropsMixin(kinesisvideo_mixins.CfnSignalingChannelMixinProps(
            message_ttl_seconds=123,
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSignalingChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KinesisVideo::SignalingChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faf7ea0d3f3130584b4bf402541478c5d97277cefd2fdd8d30f5a3d3be6922c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8fd97673232a38209c0bd84aba501cc5155b9fd6f6f5332979fe117d331ee84)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87395d4874ee3b7117c0d6ee5faedf40be6341116ead41ceca49dfc15ab3a55)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSignalingChannelMixinProps:
        return typing.cast(CfnSignalingChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisvideo.mixins.CfnStreamMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_retention_in_hours": "dataRetentionInHours",
        "device_name": "deviceName",
        "kms_key_id": "kmsKeyId",
        "media_type": "mediaType",
        "name": "name",
        "stream_storage_configuration": "streamStorageConfiguration",
        "tags": "tags",
    },
)
class CfnStreamMixinProps:
    def __init__(
        self,
        *,
        data_retention_in_hours: typing.Optional[jsii.Number] = None,
        device_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        media_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        stream_storage_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamPropsMixin.StreamStorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStreamPropsMixin.

        :param data_retention_in_hours: How long the stream retains data, in hours.
        :param device_name: The name of the device that is associated with the stream.
        :param kms_key_id: The ID of the AWS Key Management Service ( AWS ) key that Kinesis Video Streams uses to encrypt data on the stream.
        :param media_type: The ``MediaType`` of the stream.
        :param name: The name of the stream.
        :param stream_storage_configuration: The configuration for stream storage, including the default storage tier for stream data. This configuration determines how stream data is stored and accessed, with different tiers offering varying levels of performance and cost optimization.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesisvideo import mixins as kinesisvideo_mixins
            
            cfn_stream_mixin_props = kinesisvideo_mixins.CfnStreamMixinProps(
                data_retention_in_hours=123,
                device_name="deviceName",
                kms_key_id="kmsKeyId",
                media_type="mediaType",
                name="name",
                stream_storage_configuration=kinesisvideo_mixins.CfnStreamPropsMixin.StreamStorageConfigurationProperty(
                    default_storage_tier="defaultStorageTier"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37974d7b3ef015aad51e56e99a4a73cba4a683f2100860d2b695d00e8742a1cc)
            check_type(argname="argument data_retention_in_hours", value=data_retention_in_hours, expected_type=type_hints["data_retention_in_hours"])
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument media_type", value=media_type, expected_type=type_hints["media_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stream_storage_configuration", value=stream_storage_configuration, expected_type=type_hints["stream_storage_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_retention_in_hours is not None:
            self._values["data_retention_in_hours"] = data_retention_in_hours
        if device_name is not None:
            self._values["device_name"] = device_name
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if media_type is not None:
            self._values["media_type"] = media_type
        if name is not None:
            self._values["name"] = name
        if stream_storage_configuration is not None:
            self._values["stream_storage_configuration"] = stream_storage_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_retention_in_hours(self) -> typing.Optional[jsii.Number]:
        '''How long the stream retains data, in hours.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-dataretentioninhours
        '''
        result = self._values.get("data_retention_in_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''The name of the device that is associated with the stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-devicename
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS Key Management Service ( AWS  ) key that Kinesis Video Streams uses to encrypt data on the stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def media_type(self) -> typing.Optional[builtins.str]:
        '''The ``MediaType`` of the stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-mediatype
        '''
        result = self._values.get("media_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream_storage_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamPropsMixin.StreamStorageConfigurationProperty"]]:
        '''The configuration for stream storage, including the default storage tier for stream data.

        This configuration determines how stream data is stored and accessed, with different tiers offering varying levels of performance and cost optimization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-streamstorageconfiguration
        '''
        result = self._values.get("stream_storage_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamPropsMixin.StreamStorageConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStreamPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisvideo.mixins.CfnStreamPropsMixin",
):
    '''Specifies a new Kinesis video stream.

    When you create a new stream, Kinesis Video Streams assigns it a version number. When you change the stream's metadata, Kinesis Video Streams updates the version.

    ``CreateStream`` is an asynchronous operation.

    For information about how the service works, see `How it Works <https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/how-it-works.html>`_ .

    You must have permissions for the ``KinesisVideo:CreateStream`` action.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html
    :cloudformationResource: AWS::KinesisVideo::Stream
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesisvideo import mixins as kinesisvideo_mixins
        
        cfn_stream_props_mixin = kinesisvideo_mixins.CfnStreamPropsMixin(kinesisvideo_mixins.CfnStreamMixinProps(
            data_retention_in_hours=123,
            device_name="deviceName",
            kms_key_id="kmsKeyId",
            media_type="mediaType",
            name="name",
            stream_storage_configuration=kinesisvideo_mixins.CfnStreamPropsMixin.StreamStorageConfigurationProperty(
                default_storage_tier="defaultStorageTier"
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
        props: typing.Union[CfnStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KinesisVideo::Stream``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0540efcf6ed06fe14ee1da1ae42f82b796641f2e91261ecfe7fea11cc52c4f54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2aedb96b814613fbf2bfd9252226d3fd415a9f88c2ed441f814c38a4a57b8413)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6efaee0d4fcd07538a362785e96164c48cd02e742ea42eb825477a447b0690)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStreamMixinProps:
        return typing.cast(CfnStreamMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisvideo.mixins.CfnStreamPropsMixin.StreamStorageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"default_storage_tier": "defaultStorageTier"},
    )
    class StreamStorageConfigurationProperty:
        def __init__(
            self,
            *,
            default_storage_tier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for stream storage, including the default storage tier for stream data.

            This configuration determines how stream data is stored and accessed, with different tiers offering varying levels of performance and cost optimization.

            :param default_storage_tier: The default storage tier for the stream data. This setting determines the storage class used for stream data, affecting both performance characteristics and storage costs. Available storage tiers: - ``HOT`` - Optimized for frequent access with the lowest latency and highest performance. Ideal for real-time applications and frequently accessed data. - ``WARM`` - Balanced performance and cost for moderately accessed data. Suitable for data that is accessed regularly but not continuously. Default: - "HOT"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisvideo-stream-streamstorageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisvideo import mixins as kinesisvideo_mixins
                
                stream_storage_configuration_property = kinesisvideo_mixins.CfnStreamPropsMixin.StreamStorageConfigurationProperty(
                    default_storage_tier="defaultStorageTier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__66a33ffa7061635552ec36b80ab361df4ced067e9986902a36d6a99592fea971)
                check_type(argname="argument default_storage_tier", value=default_storage_tier, expected_type=type_hints["default_storage_tier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_storage_tier is not None:
                self._values["default_storage_tier"] = default_storage_tier

        @builtins.property
        def default_storage_tier(self) -> typing.Optional[builtins.str]:
            '''The default storage tier for the stream data.

            This setting determines the storage class used for stream data, affecting both performance characteristics and storage costs.

            Available storage tiers:

            - ``HOT`` - Optimized for frequent access with the lowest latency and highest performance. Ideal for real-time applications and frequently accessed data.
            - ``WARM`` - Balanced performance and cost for moderately accessed data. Suitable for data that is accessed regularly but not continuously.

            :default: - "HOT"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisvideo-stream-streamstorageconfiguration.html#cfn-kinesisvideo-stream-streamstorageconfiguration-defaultstoragetier
            '''
            result = self._values.get("default_storage_tier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamStorageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnSignalingChannelMixinProps",
    "CfnSignalingChannelPropsMixin",
    "CfnStreamMixinProps",
    "CfnStreamPropsMixin",
]

publication.publish()

def _typecheckingstub__75d25f15c9cf285c90c98b29c2a9bcdcf733e85beca8f58e35e19eb32b57fbb2(
    *,
    message_ttl_seconds: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf7ea0d3f3130584b4bf402541478c5d97277cefd2fdd8d30f5a3d3be6922c7(
    props: typing.Union[CfnSignalingChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fd97673232a38209c0bd84aba501cc5155b9fd6f6f5332979fe117d331ee84(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87395d4874ee3b7117c0d6ee5faedf40be6341116ead41ceca49dfc15ab3a55(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37974d7b3ef015aad51e56e99a4a73cba4a683f2100860d2b695d00e8742a1cc(
    *,
    data_retention_in_hours: typing.Optional[jsii.Number] = None,
    device_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    media_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    stream_storage_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamPropsMixin.StreamStorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0540efcf6ed06fe14ee1da1ae42f82b796641f2e91261ecfe7fea11cc52c4f54(
    props: typing.Union[CfnStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aedb96b814613fbf2bfd9252226d3fd415a9f88c2ed441f814c38a4a57b8413(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6efaee0d4fcd07538a362785e96164c48cd02e742ea42eb825477a447b0690(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a33ffa7061635552ec36b80ab361df4ced067e9986902a36d6a99592fea971(
    *,
    default_storage_tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
