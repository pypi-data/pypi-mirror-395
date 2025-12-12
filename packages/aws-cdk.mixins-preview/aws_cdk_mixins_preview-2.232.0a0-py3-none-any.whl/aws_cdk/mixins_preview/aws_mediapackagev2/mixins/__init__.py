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


class CfnChannelGroupEgressAccessLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelGroupEgressAccessLogs",
):
    '''Builder for CfnChannelGroupLogsMixin to generate EGRESS_ACCESS_LOGS for CfnChannelGroup.

    :cloudformationResource: AWS::MediaPackageV2::ChannelGroup
    :logType: EGRESS_ACCESS_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
        
        cfn_channel_group_egress_access_logs = mediapackagev2_mixins.CfnChannelGroupEgressAccessLogs()
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
    ) -> "CfnChannelGroupLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696024da3bf568d08005e3641147133c17b2da51832cb4acac82fcd5bae720a5)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnChannelGroupLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnChannelGroupLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b92e944d56a610a0d455ef72b8a50bff2e60ef061c4ad5f0c00e03a8b7bf316)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnChannelGroupLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnChannelGroupLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f61a6e590606f957cc1efc500e3aa79a3b15cad35d7735ef0a54d3f97343ee5)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnChannelGroupLogsMixin", jsii.invoke(self, "toS3", [bucket]))


class CfnChannelGroupIngressAccessLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelGroupIngressAccessLogs",
):
    '''Builder for CfnChannelGroupLogsMixin to generate INGRESS_ACCESS_LOGS for CfnChannelGroup.

    :cloudformationResource: AWS::MediaPackageV2::ChannelGroup
    :logType: INGRESS_ACCESS_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
        
        cfn_channel_group_ingress_access_logs = mediapackagev2_mixins.CfnChannelGroupIngressAccessLogs()
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
    ) -> "CfnChannelGroupLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35378aa91fe75f7be0fc2b133055e0bf5037441cbb9b8d9388966ccaed7fe12d)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnChannelGroupLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnChannelGroupLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640f5546e33e0871f75939fe236d7c2d08969b8c1e5d5cc2d8f1eb6ff222b8df)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnChannelGroupLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnChannelGroupLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4696583a30f96440821b1f840c1b2d5f8f911bb402718799a6be02b6a81d0491)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnChannelGroupLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnChannelGroupLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelGroupLogsMixin",
):
    '''Specifies the configuration for a MediaPackage V2 channel group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelgroup.html
    :cloudformationResource: AWS::MediaPackageV2::ChannelGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_channel_group_logs_mixin = mediapackagev2_mixins.CfnChannelGroupLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::MediaPackageV2::ChannelGroup``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b966161b6358e8d029275ec64e0c48271684c08346b9b4df34e09ea3e65891bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__388b2cbf1da1f4af7b079323a407e71471f82ebd06fbdf6de08065bf47dca3c5)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d042100ed9ef842d42eaee767403fb82d0b7ade41884205949a19f4b393dba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EGRESS_ACCESS_LOGS")
    def EGRESS_ACCESS_LOGS(cls) -> CfnChannelGroupEgressAccessLogs:
        return typing.cast(CfnChannelGroupEgressAccessLogs, jsii.sget(cls, "EGRESS_ACCESS_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INGRESS_ACCESS_LOGS")
    def INGRESS_ACCESS_LOGS(cls) -> CfnChannelGroupIngressAccessLogs:
        return typing.cast(CfnChannelGroupIngressAccessLogs, jsii.sget(cls, "INGRESS_ACCESS_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_group_name": "channelGroupName",
        "description": "description",
        "tags": "tags",
    },
)
class CfnChannelGroupMixinProps:
    def __init__(
        self,
        *,
        channel_group_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnChannelGroupPropsMixin.

        :param channel_group_name: The name of the channel group.
        :param description: The configuration for a MediaPackage V2 channel group.
        :param tags: The tags associated with the channel group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
            
            cfn_channel_group_mixin_props = mediapackagev2_mixins.CfnChannelGroupMixinProps(
                channel_group_name="channelGroupName",
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e675591417927dcc0a373a80f57a65cf17fad5f7588b2ffb258934b718420f3)
            check_type(argname="argument channel_group_name", value=channel_group_name, expected_type=type_hints["channel_group_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_group_name is not None:
            self._values["channel_group_name"] = channel_group_name
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelgroup.html#cfn-mediapackagev2-channelgroup-channelgroupname
        '''
        result = self._values.get("channel_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The configuration for a MediaPackage V2 channel group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelgroup.html#cfn-mediapackagev2-channelgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags associated with the channel group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelgroup.html#cfn-mediapackagev2-channelgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnChannelGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelGroupPropsMixin",
):
    '''Specifies the configuration for a MediaPackage V2 channel group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelgroup.html
    :cloudformationResource: AWS::MediaPackageV2::ChannelGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
        
        cfn_channel_group_props_mixin = mediapackagev2_mixins.CfnChannelGroupPropsMixin(mediapackagev2_mixins.CfnChannelGroupMixinProps(
            channel_group_name="channelGroupName",
            description="description",
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
        props: typing.Union[CfnChannelGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaPackageV2::ChannelGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d5e0cd366132627dd482843337ba0470c4774cc915cc81b3e4286c12ffe521)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3384cfd60e00ce83d638cc5d507bb41bc788cfceacc76aaa444ee089aa70fc1d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada6151db95592497f05115a980b022a93a12b6229c4f0a58bbef3fa0996a363)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnChannelGroupMixinProps:
        return typing.cast(CfnChannelGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_group_name": "channelGroupName",
        "channel_name": "channelName",
        "description": "description",
        "input_switch_configuration": "inputSwitchConfiguration",
        "input_type": "inputType",
        "output_header_configuration": "outputHeaderConfiguration",
        "tags": "tags",
    },
)
class CfnChannelMixinProps:
    def __init__(
        self,
        *,
        channel_group_name: typing.Optional[builtins.str] = None,
        channel_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        input_switch_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.InputSwitchConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        input_type: typing.Optional[builtins.str] = None,
        output_header_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.OutputHeaderConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnChannelPropsMixin.

        :param channel_group_name: The name of the channel group associated with the channel configuration.
        :param channel_name: The name of the channel.
        :param description: The description of the channel.
        :param input_switch_configuration: The configuration for input switching based on the media quality confidence score (MQCS) as provided from AWS Elemental MediaLive.
        :param input_type: The input type will be an immutable field which will be used to define whether the channel will allow CMAF ingest or HLS ingest. If unprovided, it will default to HLS to preserve current behavior. The allowed values are: - ``HLS`` - The HLS streaming specification (which defines M3U8 manifests and TS segments). - ``CMAF`` - The DASH-IF CMAF Ingest specification (which defines CMAF segments with optional DASH manifests).
        :param output_header_configuration: The settings for what common media server data (CMSD) headers AWS Elemental MediaPackage includes in responses to the CDN.
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
            
            cfn_channel_mixin_props = mediapackagev2_mixins.CfnChannelMixinProps(
                channel_group_name="channelGroupName",
                channel_name="channelName",
                description="description",
                input_switch_configuration=mediapackagev2_mixins.CfnChannelPropsMixin.InputSwitchConfigurationProperty(
                    mqcs_input_switching=False,
                    preferred_input=123
                ),
                input_type="inputType",
                output_header_configuration=mediapackagev2_mixins.CfnChannelPropsMixin.OutputHeaderConfigurationProperty(
                    publish_mqcs=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b4bc50f853020584976311b8bcf2e3ad8873b6fe82b9aea5a0b862fda807fa)
            check_type(argname="argument channel_group_name", value=channel_group_name, expected_type=type_hints["channel_group_name"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument input_switch_configuration", value=input_switch_configuration, expected_type=type_hints["input_switch_configuration"])
            check_type(argname="argument input_type", value=input_type, expected_type=type_hints["input_type"])
            check_type(argname="argument output_header_configuration", value=output_header_configuration, expected_type=type_hints["output_header_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_group_name is not None:
            self._values["channel_group_name"] = channel_group_name
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if description is not None:
            self._values["description"] = description
        if input_switch_configuration is not None:
            self._values["input_switch_configuration"] = input_switch_configuration
        if input_type is not None:
            self._values["input_type"] = input_type
        if output_header_configuration is not None:
            self._values["output_header_configuration"] = output_header_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel group associated with the channel configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channel.html#cfn-mediapackagev2-channel-channelgroupname
        '''
        result = self._values.get("channel_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channel.html#cfn-mediapackagev2-channel-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channel.html#cfn-mediapackagev2-channel-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_switch_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.InputSwitchConfigurationProperty"]]:
        '''The configuration for input switching based on the media quality confidence score (MQCS) as provided from AWS Elemental MediaLive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channel.html#cfn-mediapackagev2-channel-inputswitchconfiguration
        '''
        result = self._values.get("input_switch_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.InputSwitchConfigurationProperty"]], result)

    @builtins.property
    def input_type(self) -> typing.Optional[builtins.str]:
        '''The input type will be an immutable field which will be used to define whether the channel will allow CMAF ingest or HLS ingest.

        If unprovided, it will default to HLS to preserve current behavior.

        The allowed values are:

        - ``HLS`` - The HLS streaming specification (which defines M3U8 manifests and TS segments).
        - ``CMAF`` - The DASH-IF CMAF Ingest specification (which defines CMAF segments with optional DASH manifests).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channel.html#cfn-mediapackagev2-channel-inputtype
        '''
        result = self._values.get("input_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_header_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.OutputHeaderConfigurationProperty"]]:
        '''The settings for what common media server data (CMSD) headers AWS Elemental MediaPackage includes in responses to the CDN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channel.html#cfn-mediapackagev2-channel-outputheaderconfiguration
        '''
        result = self._values.get("output_header_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.OutputHeaderConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channel.html#cfn-mediapackagev2-channel-tags
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


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_group_name": "channelGroupName",
        "channel_name": "channelName",
        "policy": "policy",
    },
)
class CfnChannelPolicyMixinProps:
    def __init__(
        self,
        *,
        channel_group_name: typing.Optional[builtins.str] = None,
        channel_name: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
    ) -> None:
        '''Properties for CfnChannelPolicyPropsMixin.

        :param channel_group_name: The name of the channel group associated with the channel policy.
        :param channel_name: The name of the channel associated with the channel policy.
        :param policy: The policy associated with the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
            
            # policy: Any
            
            cfn_channel_policy_mixin_props = mediapackagev2_mixins.CfnChannelPolicyMixinProps(
                channel_group_name="channelGroupName",
                channel_name="channelName",
                policy=policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d583866a74455534800f1ab39c5c38072f5d5246ec376c8c7f9ea976979fd0a)
            check_type(argname="argument channel_group_name", value=channel_group_name, expected_type=type_hints["channel_group_name"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_group_name is not None:
            self._values["channel_group_name"] = channel_group_name
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def channel_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel group associated with the channel policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelpolicy.html#cfn-mediapackagev2-channelpolicy-channelgroupname
        '''
        result = self._values.get("channel_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel associated with the channel policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelpolicy.html#cfn-mediapackagev2-channelpolicy-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''The policy associated with the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelpolicy.html#cfn-mediapackagev2-channelpolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnChannelPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelPolicyPropsMixin",
):
    '''Specifies the configuration parameters of a MediaPackage V2 channel policy.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channelpolicy.html
    :cloudformationResource: AWS::MediaPackageV2::ChannelPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
        
        # policy: Any
        
        cfn_channel_policy_props_mixin = mediapackagev2_mixins.CfnChannelPolicyPropsMixin(mediapackagev2_mixins.CfnChannelPolicyMixinProps(
            channel_group_name="channelGroupName",
            channel_name="channelName",
            policy=policy
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnChannelPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaPackageV2::ChannelPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991ff5e63752909bcc29f5a1d38fa3448a13c6185b168405d941db455275ecf3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f798376c8f14093b95f1bed721ac9e89de4c045324efe064bf839c432df9642)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e9d66c7fdd4ec4868a4286790980a268dd535b36b7d0009b62bb9e8d793273)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnChannelPolicyMixinProps:
        return typing.cast(CfnChannelPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelPropsMixin",
):
    '''Creates a channel to receive content.

    After it's created, a channel provides static input URLs. These URLs remain the same throughout the lifetime of the channel, regardless of any failures or upgrades that might occur. Use these URLs to configure the outputs of your upstream encoder.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-channel.html
    :cloudformationResource: AWS::MediaPackageV2::Channel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
        
        cfn_channel_props_mixin = mediapackagev2_mixins.CfnChannelPropsMixin(mediapackagev2_mixins.CfnChannelMixinProps(
            channel_group_name="channelGroupName",
            channel_name="channelName",
            description="description",
            input_switch_configuration=mediapackagev2_mixins.CfnChannelPropsMixin.InputSwitchConfigurationProperty(
                mqcs_input_switching=False,
                preferred_input=123
            ),
            input_type="inputType",
            output_header_configuration=mediapackagev2_mixins.CfnChannelPropsMixin.OutputHeaderConfigurationProperty(
                publish_mqcs=False
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
        '''Create a mixin to apply properties to ``AWS::MediaPackageV2::Channel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4d435acfc17a38503a16f25433a0dc36b9b3bd5d439e0d08e79cc5eae79f42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e0037b4c22f70b68e1b81b12adf3d51a80151c8b79a54d6b118258049254d0f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc6dc51effca8437d415a18bf4830212aba35e3722c427aa826d07f22832f38)
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
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelPropsMixin.IngestEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "url": "url"},
    )
    class IngestEndpointProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The input URL where the source stream should be sent.

            :param id: The identifier associated with the ingest endpoint of the channel.
            :param url: The URL associated with the ingest endpoint of the channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-channel-ingestendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                ingest_endpoint_property = mediapackagev2_mixins.CfnChannelPropsMixin.IngestEndpointProperty(
                    id="id",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__426db355924e1d267137718440d51bb36fa83bab6d320ee31d3114c25e8508f4)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The identifier associated with the ingest endpoint of the channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-channel-ingestendpoint.html#cfn-mediapackagev2-channel-ingestendpoint-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL associated with the ingest endpoint of the channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-channel-ingestendpoint.html#cfn-mediapackagev2-channel-ingestendpoint-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngestEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelPropsMixin.InputSwitchConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mqcs_input_switching": "mqcsInputSwitching",
            "preferred_input": "preferredInput",
        },
    )
    class InputSwitchConfigurationProperty:
        def __init__(
            self,
            *,
            mqcs_input_switching: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            preferred_input: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration for input switching based on the media quality confidence score (MQCS) as provided from AWS Elemental MediaLive.

            :param mqcs_input_switching: When true, AWS Elemental MediaPackage performs input switching based on the MQCS. Default is false. This setting is valid only when ``InputType`` is ``CMAF`` .
            :param preferred_input: For CMAF inputs, indicates which input MediaPackage should prefer when both inputs have equal MQCS scores. Select ``1`` to prefer the first ingest endpoint, or ``2`` to prefer the second ingest endpoint. If you don't specify a preferred input, MediaPackage uses its default switching behavior when MQCS scores are equal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-channel-inputswitchconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                input_switch_configuration_property = mediapackagev2_mixins.CfnChannelPropsMixin.InputSwitchConfigurationProperty(
                    mqcs_input_switching=False,
                    preferred_input=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79667e1ba0957489df64225b4942e4437f5def44b805041f460350af1fc04956)
                check_type(argname="argument mqcs_input_switching", value=mqcs_input_switching, expected_type=type_hints["mqcs_input_switching"])
                check_type(argname="argument preferred_input", value=preferred_input, expected_type=type_hints["preferred_input"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mqcs_input_switching is not None:
                self._values["mqcs_input_switching"] = mqcs_input_switching
            if preferred_input is not None:
                self._values["preferred_input"] = preferred_input

        @builtins.property
        def mqcs_input_switching(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true, AWS Elemental MediaPackage performs input switching based on the MQCS.

            Default is false. This setting is valid only when ``InputType`` is ``CMAF`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-channel-inputswitchconfiguration.html#cfn-mediapackagev2-channel-inputswitchconfiguration-mqcsinputswitching
            '''
            result = self._values.get("mqcs_input_switching")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def preferred_input(self) -> typing.Optional[jsii.Number]:
            '''For CMAF inputs, indicates which input MediaPackage should prefer when both inputs have equal MQCS scores.

            Select ``1`` to prefer the first ingest endpoint, or ``2`` to prefer the second ingest endpoint. If you don't specify a preferred input, MediaPackage uses its default switching behavior when MQCS scores are equal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-channel-inputswitchconfiguration.html#cfn-mediapackagev2-channel-inputswitchconfiguration-preferredinput
            '''
            result = self._values.get("preferred_input")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputSwitchConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnChannelPropsMixin.OutputHeaderConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"publish_mqcs": "publishMqcs"},
    )
    class OutputHeaderConfigurationProperty:
        def __init__(
            self,
            *,
            publish_mqcs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The settings for what common media server data (CMSD) headers AWS Elemental MediaPackage includes in responses to the CDN.

            :param publish_mqcs: When true, AWS Elemental MediaPackage includes the MQCS in responses to the CDN. This setting is valid only when ``InputType`` is ``CMAF`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-channel-outputheaderconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                output_header_configuration_property = mediapackagev2_mixins.CfnChannelPropsMixin.OutputHeaderConfigurationProperty(
                    publish_mqcs=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d008b1ad488eb9e6786baaf58a43b11c91de661bdb7156759a75cfc68413b32f)
                check_type(argname="argument publish_mqcs", value=publish_mqcs, expected_type=type_hints["publish_mqcs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if publish_mqcs is not None:
                self._values["publish_mqcs"] = publish_mqcs

        @builtins.property
        def publish_mqcs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true, AWS Elemental MediaPackage includes the MQCS in responses to the CDN.

            This setting is valid only when ``InputType`` is ``CMAF`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-channel-outputheaderconfiguration.html#cfn-mediapackagev2-channel-outputheaderconfiguration-publishmqcs
            '''
            result = self._values.get("publish_mqcs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputHeaderConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_group_name": "channelGroupName",
        "channel_name": "channelName",
        "container_type": "containerType",
        "dash_manifests": "dashManifests",
        "description": "description",
        "force_endpoint_error_configuration": "forceEndpointErrorConfiguration",
        "hls_manifests": "hlsManifests",
        "low_latency_hls_manifests": "lowLatencyHlsManifests",
        "mss_manifests": "mssManifests",
        "origin_endpoint_name": "originEndpointName",
        "segment": "segment",
        "startover_window_seconds": "startoverWindowSeconds",
        "tags": "tags",
    },
)
class CfnOriginEndpointMixinProps:
    def __init__(
        self,
        *,
        channel_group_name: typing.Optional[builtins.str] = None,
        channel_name: typing.Optional[builtins.str] = None,
        container_type: typing.Optional[builtins.str] = None,
        dash_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashManifestConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        force_endpoint_error_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.ForceEndpointErrorConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        hls_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.HlsManifestConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        low_latency_hls_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.LowLatencyHlsManifestConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        mss_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.MssManifestConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        origin_endpoint_name: typing.Optional[builtins.str] = None,
        segment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.SegmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        startover_window_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOriginEndpointPropsMixin.

        :param channel_group_name: The name of the channel group associated with the origin endpoint configuration.
        :param channel_name: The channel name associated with the origin endpoint.
        :param container_type: The container type associated with the origin endpoint configuration.
        :param dash_manifests: A DASH manifest configuration.
        :param description: The description associated with the origin endpoint.
        :param force_endpoint_error_configuration: The failover settings for the endpoint.
        :param hls_manifests: The HLS manifests associated with the origin endpoint configuration.
        :param low_latency_hls_manifests: The low-latency HLS (LL-HLS) manifests associated with the origin endpoint.
        :param mss_manifests: A list of Microsoft Smooth Streaming (MSS) manifest configurations associated with the origin endpoint. Each configuration represents a different MSS streaming option available from this endpoint.
        :param origin_endpoint_name: The name of the origin endpoint associated with the origin endpoint configuration.
        :param segment: The segment associated with the origin endpoint.
        :param startover_window_seconds: The size of the window (in seconds) to specify a window of the live stream that's available for on-demand viewing. Viewers can start-over or catch-up on content that falls within the window.
        :param tags: The tags associated with the origin endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
            
            cfn_origin_endpoint_mixin_props = mediapackagev2_mixins.CfnOriginEndpointMixinProps(
                channel_group_name="channelGroupName",
                channel_name="channelName",
                container_type="containerType",
                dash_manifests=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashManifestConfigurationProperty(
                    base_urls=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashBaseUrlProperty(
                        dvb_priority=123,
                        dvb_weight=123,
                        service_location="serviceLocation",
                        url="url"
                    )],
                    compactness="compactness",
                    drm_signaling="drmSignaling",
                    dvb_settings=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbSettingsProperty(
                        error_metrics=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbMetricsReportingProperty(
                            probability=123,
                            reporting_url="reportingUrl"
                        )],
                        font_download=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbFontDownloadProperty(
                            font_family="fontFamily",
                            mime_type="mimeType",
                            url="url"
                        )
                    ),
                    filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                        clip_start_time="clipStartTime",
                        end="end",
                        manifest_filter="manifestFilter",
                        start="start",
                        time_delay_seconds=123
                    ),
                    manifest_name="manifestName",
                    manifest_window_seconds=123,
                    min_buffer_time_seconds=123,
                    min_update_period_seconds=123,
                    period_triggers=["periodTriggers"],
                    profiles=["profiles"],
                    program_information=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashProgramInformationProperty(
                        copyright="copyright",
                        language_code="languageCode",
                        more_information_url="moreInformationUrl",
                        source="source",
                        title="title"
                    ),
                    scte_dash=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteDashProperty(
                        ad_marker_dash="adMarkerDash"
                    ),
                    segment_template_format="segmentTemplateFormat",
                    subtitle_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashSubtitleConfigurationProperty(
                        ttml_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashTtmlConfigurationProperty(
                            ttml_profile="ttmlProfile"
                        )
                    ),
                    suggested_presentation_delay_seconds=123,
                    utc_timing=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashUtcTimingProperty(
                        timing_mode="timingMode",
                        timing_source="timingSource"
                    )
                )],
                description="description",
                force_endpoint_error_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ForceEndpointErrorConfigurationProperty(
                    endpoint_error_conditions=["endpointErrorConditions"]
                ),
                hls_manifests=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.HlsManifestConfigurationProperty(
                    child_manifest_name="childManifestName",
                    filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                        clip_start_time="clipStartTime",
                        end="end",
                        manifest_filter="manifestFilter",
                        start="start",
                        time_delay_seconds=123
                    ),
                    manifest_name="manifestName",
                    manifest_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    scte_hls=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteHlsProperty(
                        ad_marker_hls="adMarkerHls"
                    ),
                    start_tag=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.StartTagProperty(
                        precise=False,
                        time_offset=123
                    ),
                    url="url",
                    url_encode_child_manifest=False
                )],
                low_latency_hls_manifests=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.LowLatencyHlsManifestConfigurationProperty(
                    child_manifest_name="childManifestName",
                    filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                        clip_start_time="clipStartTime",
                        end="end",
                        manifest_filter="manifestFilter",
                        start="start",
                        time_delay_seconds=123
                    ),
                    manifest_name="manifestName",
                    manifest_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    scte_hls=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteHlsProperty(
                        ad_marker_hls="adMarkerHls"
                    ),
                    start_tag=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.StartTagProperty(
                        precise=False,
                        time_offset=123
                    ),
                    url="url",
                    url_encode_child_manifest=False
                )],
                mss_manifests=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.MssManifestConfigurationProperty(
                    filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                        clip_start_time="clipStartTime",
                        end="end",
                        manifest_filter="manifestFilter",
                        start="start",
                        time_delay_seconds=123
                    ),
                    manifest_layout="manifestLayout",
                    manifest_name="manifestName",
                    manifest_window_seconds=123
                )],
                origin_endpoint_name="originEndpointName",
                segment=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.SegmentProperty(
                    encryption=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionProperty(
                        cmaf_exclude_segment_drm_metadata=False,
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionMethodProperty(
                            cmaf_encryption_method="cmafEncryptionMethod",
                            ism_encryption_method="ismEncryptionMethod",
                            ts_encryption_method="tsEncryptionMethod"
                        ),
                        key_rotation_interval_seconds=123,
                        speke_key_provider=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                            drm_systems=["drmSystems"],
                            encryption_contract_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            resource_id="resourceId",
                            role_arn="roleArn",
                            url="url"
                        )
                    ),
                    include_iframe_only_streams=False,
                    scte=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteProperty(
                        scte_filter=["scteFilter"]
                    ),
                    segment_duration_seconds=123,
                    segment_name="segmentName",
                    ts_include_dvb_subtitles=False,
                    ts_use_audio_rendition_group=False
                ),
                startover_window_seconds=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e34374b7953480d3926e99db2e6179beb1cb4bb530c8ddb586c3dd2a193d11b)
            check_type(argname="argument channel_group_name", value=channel_group_name, expected_type=type_hints["channel_group_name"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument container_type", value=container_type, expected_type=type_hints["container_type"])
            check_type(argname="argument dash_manifests", value=dash_manifests, expected_type=type_hints["dash_manifests"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument force_endpoint_error_configuration", value=force_endpoint_error_configuration, expected_type=type_hints["force_endpoint_error_configuration"])
            check_type(argname="argument hls_manifests", value=hls_manifests, expected_type=type_hints["hls_manifests"])
            check_type(argname="argument low_latency_hls_manifests", value=low_latency_hls_manifests, expected_type=type_hints["low_latency_hls_manifests"])
            check_type(argname="argument mss_manifests", value=mss_manifests, expected_type=type_hints["mss_manifests"])
            check_type(argname="argument origin_endpoint_name", value=origin_endpoint_name, expected_type=type_hints["origin_endpoint_name"])
            check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
            check_type(argname="argument startover_window_seconds", value=startover_window_seconds, expected_type=type_hints["startover_window_seconds"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_group_name is not None:
            self._values["channel_group_name"] = channel_group_name
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if container_type is not None:
            self._values["container_type"] = container_type
        if dash_manifests is not None:
            self._values["dash_manifests"] = dash_manifests
        if description is not None:
            self._values["description"] = description
        if force_endpoint_error_configuration is not None:
            self._values["force_endpoint_error_configuration"] = force_endpoint_error_configuration
        if hls_manifests is not None:
            self._values["hls_manifests"] = hls_manifests
        if low_latency_hls_manifests is not None:
            self._values["low_latency_hls_manifests"] = low_latency_hls_manifests
        if mss_manifests is not None:
            self._values["mss_manifests"] = mss_manifests
        if origin_endpoint_name is not None:
            self._values["origin_endpoint_name"] = origin_endpoint_name
        if segment is not None:
            self._values["segment"] = segment
        if startover_window_seconds is not None:
            self._values["startover_window_seconds"] = startover_window_seconds
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel group associated with the origin endpoint configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-channelgroupname
        '''
        result = self._values.get("channel_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The channel name associated with the origin endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_type(self) -> typing.Optional[builtins.str]:
        '''The container type associated with the origin endpoint configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-containertype
        '''
        result = self._values.get("container_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dash_manifests(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashManifestConfigurationProperty"]]]]:
        '''A DASH manifest configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-dashmanifests
        '''
        result = self._values.get("dash_manifests")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashManifestConfigurationProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description associated with the origin endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_endpoint_error_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.ForceEndpointErrorConfigurationProperty"]]:
        '''The failover settings for the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-forceendpointerrorconfiguration
        '''
        result = self._values.get("force_endpoint_error_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.ForceEndpointErrorConfigurationProperty"]], result)

    @builtins.property
    def hls_manifests(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.HlsManifestConfigurationProperty"]]]]:
        '''The HLS manifests associated with the origin endpoint configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-hlsmanifests
        '''
        result = self._values.get("hls_manifests")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.HlsManifestConfigurationProperty"]]]], result)

    @builtins.property
    def low_latency_hls_manifests(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.LowLatencyHlsManifestConfigurationProperty"]]]]:
        '''The low-latency HLS (LL-HLS) manifests associated with the origin endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-lowlatencyhlsmanifests
        '''
        result = self._values.get("low_latency_hls_manifests")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.LowLatencyHlsManifestConfigurationProperty"]]]], result)

    @builtins.property
    def mss_manifests(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.MssManifestConfigurationProperty"]]]]:
        '''A list of Microsoft Smooth Streaming (MSS) manifest configurations associated with the origin endpoint.

        Each configuration represents a different MSS streaming option available from this endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-mssmanifests
        '''
        result = self._values.get("mss_manifests")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.MssManifestConfigurationProperty"]]]], result)

    @builtins.property
    def origin_endpoint_name(self) -> typing.Optional[builtins.str]:
        '''The name of the origin endpoint associated with the origin endpoint configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-originendpointname
        '''
        result = self._values.get("origin_endpoint_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SegmentProperty"]]:
        '''The segment associated with the origin endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-segment
        '''
        result = self._values.get("segment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SegmentProperty"]], result)

    @builtins.property
    def startover_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''The size of the window (in seconds) to specify a window of the live stream that's available for on-demand viewing.

        Viewers can start-over or catch-up on content that falls within the window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-startoverwindowseconds
        '''
        result = self._values.get("startover_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags associated with the origin endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html#cfn-mediapackagev2-originendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOriginEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cdn_auth_configuration": "cdnAuthConfiguration",
        "channel_group_name": "channelGroupName",
        "channel_name": "channelName",
        "origin_endpoint_name": "originEndpointName",
        "policy": "policy",
    },
)
class CfnOriginEndpointPolicyMixinProps:
    def __init__(
        self,
        *,
        cdn_auth_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPolicyPropsMixin.CdnAuthConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        channel_group_name: typing.Optional[builtins.str] = None,
        channel_name: typing.Optional[builtins.str] = None,
        origin_endpoint_name: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
    ) -> None:
        '''Properties for CfnOriginEndpointPolicyPropsMixin.

        :param cdn_auth_configuration: The settings to enable CDN authorization headers in MediaPackage.
        :param channel_group_name: The name of the channel group associated with the origin endpoint policy.
        :param channel_name: The channel name associated with the origin endpoint policy.
        :param origin_endpoint_name: The name of the origin endpoint associated with the origin endpoint policy.
        :param policy: The policy associated with the origin endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpointpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
            
            # policy: Any
            
            cfn_origin_endpoint_policy_mixin_props = mediapackagev2_mixins.CfnOriginEndpointPolicyMixinProps(
                cdn_auth_configuration=mediapackagev2_mixins.CfnOriginEndpointPolicyPropsMixin.CdnAuthConfigurationProperty(
                    cdn_identifier_secret_arns=["cdnIdentifierSecretArns"],
                    secrets_role_arn="secretsRoleArn"
                ),
                channel_group_name="channelGroupName",
                channel_name="channelName",
                origin_endpoint_name="originEndpointName",
                policy=policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2467be87cb8237515ca5b6104ed3e7a745207d31425881505ad91459b4ba2e80)
            check_type(argname="argument cdn_auth_configuration", value=cdn_auth_configuration, expected_type=type_hints["cdn_auth_configuration"])
            check_type(argname="argument channel_group_name", value=channel_group_name, expected_type=type_hints["channel_group_name"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument origin_endpoint_name", value=origin_endpoint_name, expected_type=type_hints["origin_endpoint_name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cdn_auth_configuration is not None:
            self._values["cdn_auth_configuration"] = cdn_auth_configuration
        if channel_group_name is not None:
            self._values["channel_group_name"] = channel_group_name
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if origin_endpoint_name is not None:
            self._values["origin_endpoint_name"] = origin_endpoint_name
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def cdn_auth_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPolicyPropsMixin.CdnAuthConfigurationProperty"]]:
        '''The settings to enable CDN authorization headers in MediaPackage.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpointpolicy.html#cfn-mediapackagev2-originendpointpolicy-cdnauthconfiguration
        '''
        result = self._values.get("cdn_auth_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPolicyPropsMixin.CdnAuthConfigurationProperty"]], result)

    @builtins.property
    def channel_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel group associated with the origin endpoint policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpointpolicy.html#cfn-mediapackagev2-originendpointpolicy-channelgroupname
        '''
        result = self._values.get("channel_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The channel name associated with the origin endpoint policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpointpolicy.html#cfn-mediapackagev2-originendpointpolicy-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_endpoint_name(self) -> typing.Optional[builtins.str]:
        '''The name of the origin endpoint associated with the origin endpoint policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpointpolicy.html#cfn-mediapackagev2-originendpointpolicy-originendpointname
        '''
        result = self._values.get("origin_endpoint_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''The policy associated with the origin endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpointpolicy.html#cfn-mediapackagev2-originendpointpolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOriginEndpointPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOriginEndpointPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPolicyPropsMixin",
):
    '''Specifies the configuration parameters of a policy associated with a MediaPackage V2 origin endpoint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpointpolicy.html
    :cloudformationResource: AWS::MediaPackageV2::OriginEndpointPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
        
        # policy: Any
        
        cfn_origin_endpoint_policy_props_mixin = mediapackagev2_mixins.CfnOriginEndpointPolicyPropsMixin(mediapackagev2_mixins.CfnOriginEndpointPolicyMixinProps(
            cdn_auth_configuration=mediapackagev2_mixins.CfnOriginEndpointPolicyPropsMixin.CdnAuthConfigurationProperty(
                cdn_identifier_secret_arns=["cdnIdentifierSecretArns"],
                secrets_role_arn="secretsRoleArn"
            ),
            channel_group_name="channelGroupName",
            channel_name="channelName",
            origin_endpoint_name="originEndpointName",
            policy=policy
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOriginEndpointPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaPackageV2::OriginEndpointPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__481bee070afe98057b619c99d401d46a8f167b379fa59fd0c81ed6ed2a113321)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93b91a5289499aae0caa16bce921796b00e88fe57a963063d3fd305abb453846)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e49786037215f13a5775ec76e1bbedcddb650aa929109af9bd46ac8b3100955)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOriginEndpointPolicyMixinProps:
        return typing.cast(CfnOriginEndpointPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPolicyPropsMixin.CdnAuthConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cdn_identifier_secret_arns": "cdnIdentifierSecretArns",
            "secrets_role_arn": "secretsRoleArn",
        },
    )
    class CdnAuthConfigurationProperty:
        def __init__(
            self,
            *,
            cdn_identifier_secret_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            secrets_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings to enable CDN authorization headers in MediaPackage.

            :param cdn_identifier_secret_arns: The ARN for the secret in Secrets Manager that your CDN uses for authorization to access the endpoint.
            :param secrets_role_arn: The ARN for the IAM role that gives MediaPackage read access to Secrets Manager and AWS for CDN authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpointpolicy-cdnauthconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                cdn_auth_configuration_property = mediapackagev2_mixins.CfnOriginEndpointPolicyPropsMixin.CdnAuthConfigurationProperty(
                    cdn_identifier_secret_arns=["cdnIdentifierSecretArns"],
                    secrets_role_arn="secretsRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42ec8c57153be3063532df5d9e0241218689296bba7a2385fa2031e3ea195646)
                check_type(argname="argument cdn_identifier_secret_arns", value=cdn_identifier_secret_arns, expected_type=type_hints["cdn_identifier_secret_arns"])
                check_type(argname="argument secrets_role_arn", value=secrets_role_arn, expected_type=type_hints["secrets_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cdn_identifier_secret_arns is not None:
                self._values["cdn_identifier_secret_arns"] = cdn_identifier_secret_arns
            if secrets_role_arn is not None:
                self._values["secrets_role_arn"] = secrets_role_arn

        @builtins.property
        def cdn_identifier_secret_arns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The ARN for the secret in Secrets Manager that your CDN uses for authorization to access the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpointpolicy-cdnauthconfiguration.html#cfn-mediapackagev2-originendpointpolicy-cdnauthconfiguration-cdnidentifiersecretarns
            '''
            result = self._values.get("cdn_identifier_secret_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def secrets_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN for the IAM role that gives MediaPackage read access to Secrets Manager and AWS  for CDN authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpointpolicy-cdnauthconfiguration.html#cfn-mediapackagev2-originendpointpolicy-cdnauthconfiguration-secretsrolearn
            '''
            result = self._values.get("secrets_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CdnAuthConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnOriginEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin",
):
    '''Specifies the configuration parameters for a MediaPackage V2 origin endpoint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackagev2-originendpoint.html
    :cloudformationResource: AWS::MediaPackageV2::OriginEndpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
        
        cfn_origin_endpoint_props_mixin = mediapackagev2_mixins.CfnOriginEndpointPropsMixin(mediapackagev2_mixins.CfnOriginEndpointMixinProps(
            channel_group_name="channelGroupName",
            channel_name="channelName",
            container_type="containerType",
            dash_manifests=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashManifestConfigurationProperty(
                base_urls=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashBaseUrlProperty(
                    dvb_priority=123,
                    dvb_weight=123,
                    service_location="serviceLocation",
                    url="url"
                )],
                compactness="compactness",
                drm_signaling="drmSignaling",
                dvb_settings=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbSettingsProperty(
                    error_metrics=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbMetricsReportingProperty(
                        probability=123,
                        reporting_url="reportingUrl"
                    )],
                    font_download=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbFontDownloadProperty(
                        font_family="fontFamily",
                        mime_type="mimeType",
                        url="url"
                    )
                ),
                filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                    clip_start_time="clipStartTime",
                    end="end",
                    manifest_filter="manifestFilter",
                    start="start",
                    time_delay_seconds=123
                ),
                manifest_name="manifestName",
                manifest_window_seconds=123,
                min_buffer_time_seconds=123,
                min_update_period_seconds=123,
                period_triggers=["periodTriggers"],
                profiles=["profiles"],
                program_information=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashProgramInformationProperty(
                    copyright="copyright",
                    language_code="languageCode",
                    more_information_url="moreInformationUrl",
                    source="source",
                    title="title"
                ),
                scte_dash=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteDashProperty(
                    ad_marker_dash="adMarkerDash"
                ),
                segment_template_format="segmentTemplateFormat",
                subtitle_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashSubtitleConfigurationProperty(
                    ttml_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashTtmlConfigurationProperty(
                        ttml_profile="ttmlProfile"
                    )
                ),
                suggested_presentation_delay_seconds=123,
                utc_timing=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashUtcTimingProperty(
                    timing_mode="timingMode",
                    timing_source="timingSource"
                )
            )],
            description="description",
            force_endpoint_error_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ForceEndpointErrorConfigurationProperty(
                endpoint_error_conditions=["endpointErrorConditions"]
            ),
            hls_manifests=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.HlsManifestConfigurationProperty(
                child_manifest_name="childManifestName",
                filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                    clip_start_time="clipStartTime",
                    end="end",
                    manifest_filter="manifestFilter",
                    start="start",
                    time_delay_seconds=123
                ),
                manifest_name="manifestName",
                manifest_window_seconds=123,
                program_date_time_interval_seconds=123,
                scte_hls=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteHlsProperty(
                    ad_marker_hls="adMarkerHls"
                ),
                start_tag=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.StartTagProperty(
                    precise=False,
                    time_offset=123
                ),
                url="url",
                url_encode_child_manifest=False
            )],
            low_latency_hls_manifests=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.LowLatencyHlsManifestConfigurationProperty(
                child_manifest_name="childManifestName",
                filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                    clip_start_time="clipStartTime",
                    end="end",
                    manifest_filter="manifestFilter",
                    start="start",
                    time_delay_seconds=123
                ),
                manifest_name="manifestName",
                manifest_window_seconds=123,
                program_date_time_interval_seconds=123,
                scte_hls=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteHlsProperty(
                    ad_marker_hls="adMarkerHls"
                ),
                start_tag=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.StartTagProperty(
                    precise=False,
                    time_offset=123
                ),
                url="url",
                url_encode_child_manifest=False
            )],
            mss_manifests=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.MssManifestConfigurationProperty(
                filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                    clip_start_time="clipStartTime",
                    end="end",
                    manifest_filter="manifestFilter",
                    start="start",
                    time_delay_seconds=123
                ),
                manifest_layout="manifestLayout",
                manifest_name="manifestName",
                manifest_window_seconds=123
            )],
            origin_endpoint_name="originEndpointName",
            segment=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.SegmentProperty(
                encryption=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionProperty(
                    cmaf_exclude_segment_drm_metadata=False,
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionMethodProperty(
                        cmaf_encryption_method="cmafEncryptionMethod",
                        ism_encryption_method="ismEncryptionMethod",
                        ts_encryption_method="tsEncryptionMethod"
                    ),
                    key_rotation_interval_seconds=123,
                    speke_key_provider=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                        drm_systems=["drmSystems"],
                        encryption_contract_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        resource_id="resourceId",
                        role_arn="roleArn",
                        url="url"
                    )
                ),
                include_iframe_only_streams=False,
                scte=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteProperty(
                    scte_filter=["scteFilter"]
                ),
                segment_duration_seconds=123,
                segment_name="segmentName",
                ts_include_dvb_subtitles=False,
                ts_use_audio_rendition_group=False
            ),
            startover_window_seconds=123,
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
        props: typing.Union[CfnOriginEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaPackageV2::OriginEndpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4126516c3e149c91a30d5049a86dece491b5bdad44d7c272c0d663156cbe93f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba7892ff51ad1193b011e169484f66bc169210c9eec01dec65c37e79c3c517b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e9f0a671f9190ca88935736383089d471d93a51a35132794e5aa398b4d7e985)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOriginEndpointMixinProps:
        return typing.cast(CfnOriginEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.DashBaseUrlProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dvb_priority": "dvbPriority",
            "dvb_weight": "dvbWeight",
            "service_location": "serviceLocation",
            "url": "url",
        },
    )
    class DashBaseUrlProperty:
        def __init__(
            self,
            *,
            dvb_priority: typing.Optional[jsii.Number] = None,
            dvb_weight: typing.Optional[jsii.Number] = None,
            service_location: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The base URLs to use for retrieving segments.

            You can specify multiple locations and indicate the priority and weight for when each should be used, for use in mutli-CDN workflows.

            :param dvb_priority: For use with DVB-DASH profiles only. The priority of this location for servings segments. The lower the number, the higher the priority.
            :param dvb_weight: For use with DVB-DASH profiles only. The weighting for source locations that have the same priority.
            :param service_location: The name of the source location.
            :param url: A source location for segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashbaseurl.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                dash_base_url_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashBaseUrlProperty(
                    dvb_priority=123,
                    dvb_weight=123,
                    service_location="serviceLocation",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__beab719409ecad40b96d00a01b877f0ac0f0908889f98f4c0750a9744315db88)
                check_type(argname="argument dvb_priority", value=dvb_priority, expected_type=type_hints["dvb_priority"])
                check_type(argname="argument dvb_weight", value=dvb_weight, expected_type=type_hints["dvb_weight"])
                check_type(argname="argument service_location", value=service_location, expected_type=type_hints["service_location"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dvb_priority is not None:
                self._values["dvb_priority"] = dvb_priority
            if dvb_weight is not None:
                self._values["dvb_weight"] = dvb_weight
            if service_location is not None:
                self._values["service_location"] = service_location
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def dvb_priority(self) -> typing.Optional[jsii.Number]:
            '''For use with DVB-DASH profiles only.

            The priority of this location for servings segments. The lower the number, the higher the priority.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashbaseurl.html#cfn-mediapackagev2-originendpoint-dashbaseurl-dvbpriority
            '''
            result = self._values.get("dvb_priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dvb_weight(self) -> typing.Optional[jsii.Number]:
            '''For use with DVB-DASH profiles only.

            The weighting for source locations that have the same priority.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashbaseurl.html#cfn-mediapackagev2-originendpoint-dashbaseurl-dvbweight
            '''
            result = self._values.get("dvb_weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def service_location(self) -> typing.Optional[builtins.str]:
            '''The name of the source location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashbaseurl.html#cfn-mediapackagev2-originendpoint-dashbaseurl-servicelocation
            '''
            result = self._values.get("service_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''A source location for segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashbaseurl.html#cfn-mediapackagev2-originendpoint-dashbaseurl-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashBaseUrlProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.DashDvbFontDownloadProperty",
        jsii_struct_bases=[],
        name_mapping={
            "font_family": "fontFamily",
            "mime_type": "mimeType",
            "url": "url",
        },
    )
    class DashDvbFontDownloadProperty:
        def __init__(
            self,
            *,
            font_family: typing.Optional[builtins.str] = None,
            mime_type: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''For use with DVB-DASH profiles only.

            The settings for font downloads that you want AWS Elemental MediaPackage to pass through to the manifest.

            :param font_family: The ``fontFamily`` name for subtitles, as described in `EBU-TT-D Subtitling Distribution Format <https://docs.aws.amazon.com/https://tech.ebu.ch/publications/tech3380>`_ .
            :param mime_type: The ``mimeType`` of the resource that's at the font download URL. For information about font MIME types, see the `MPEG-DASH Profile for Transport of ISO BMFF Based DVB Services over IP Based Networks <https://docs.aws.amazon.com/https://dvb.org/wp-content/uploads/2021/06/A168r4_MPEG-DASH-Profile-for-Transport-of-ISO-BMFF-Based-DVB-Services_Draft-ts_103-285-v140_November_2021.pdf>`_ document.
            :param url: The URL for downloading fonts for subtitles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashdvbfontdownload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                dash_dvb_font_download_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbFontDownloadProperty(
                    font_family="fontFamily",
                    mime_type="mimeType",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbb8cfefb0cd382dc0271b3e1fc2b5de7eab5cac8c28df55b8e20d9838f13b05)
                check_type(argname="argument font_family", value=font_family, expected_type=type_hints["font_family"])
                check_type(argname="argument mime_type", value=mime_type, expected_type=type_hints["mime_type"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if font_family is not None:
                self._values["font_family"] = font_family
            if mime_type is not None:
                self._values["mime_type"] = mime_type
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def font_family(self) -> typing.Optional[builtins.str]:
            '''The ``fontFamily`` name for subtitles, as described in `EBU-TT-D Subtitling Distribution Format <https://docs.aws.amazon.com/https://tech.ebu.ch/publications/tech3380>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashdvbfontdownload.html#cfn-mediapackagev2-originendpoint-dashdvbfontdownload-fontfamily
            '''
            result = self._values.get("font_family")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mime_type(self) -> typing.Optional[builtins.str]:
            '''The ``mimeType`` of the resource that's at the font download URL.

            For information about font MIME types, see the `MPEG-DASH Profile for Transport of ISO BMFF Based DVB Services over IP Based Networks <https://docs.aws.amazon.com/https://dvb.org/wp-content/uploads/2021/06/A168r4_MPEG-DASH-Profile-for-Transport-of-ISO-BMFF-Based-DVB-Services_Draft-ts_103-285-v140_November_2021.pdf>`_ document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashdvbfontdownload.html#cfn-mediapackagev2-originendpoint-dashdvbfontdownload-mimetype
            '''
            result = self._values.get("mime_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL for downloading fonts for subtitles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashdvbfontdownload.html#cfn-mediapackagev2-originendpoint-dashdvbfontdownload-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashDvbFontDownloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.DashDvbMetricsReportingProperty",
        jsii_struct_bases=[],
        name_mapping={"probability": "probability", "reporting_url": "reportingUrl"},
    )
    class DashDvbMetricsReportingProperty:
        def __init__(
            self,
            *,
            probability: typing.Optional[jsii.Number] = None,
            reporting_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''For use with DVB-DASH profiles only.

            The settings for error reporting from the playback device that you want AWS Elemental MediaPackage to pass through to the manifest.

            :param probability: The number of playback devices per 1000 that will send error reports to the reporting URL. This represents the probability that a playback device will be a reporting player for this session.
            :param reporting_url: The URL where playback devices send error reports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashdvbmetricsreporting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                dash_dvb_metrics_reporting_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbMetricsReportingProperty(
                    probability=123,
                    reporting_url="reportingUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2133d2d2b35fe2fff50ec1be2a567389625249a5da09bfae1cdfa7584c2298a)
                check_type(argname="argument probability", value=probability, expected_type=type_hints["probability"])
                check_type(argname="argument reporting_url", value=reporting_url, expected_type=type_hints["reporting_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if probability is not None:
                self._values["probability"] = probability
            if reporting_url is not None:
                self._values["reporting_url"] = reporting_url

        @builtins.property
        def probability(self) -> typing.Optional[jsii.Number]:
            '''The number of playback devices per 1000 that will send error reports to the reporting URL.

            This represents the probability that a playback device will be a reporting player for this session.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashdvbmetricsreporting.html#cfn-mediapackagev2-originendpoint-dashdvbmetricsreporting-probability
            '''
            result = self._values.get("probability")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def reporting_url(self) -> typing.Optional[builtins.str]:
            '''The URL where playback devices send error reports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashdvbmetricsreporting.html#cfn-mediapackagev2-originendpoint-dashdvbmetricsreporting-reportingurl
            '''
            result = self._values.get("reporting_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashDvbMetricsReportingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.DashDvbSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "error_metrics": "errorMetrics",
            "font_download": "fontDownload",
        },
    )
    class DashDvbSettingsProperty:
        def __init__(
            self,
            *,
            error_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashDvbMetricsReportingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            font_download: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashDvbFontDownloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''For endpoints that use the DVB-DASH profile only.

            The font download and error reporting information that you want MediaPackage to pass through to the manifest.

            :param error_metrics: Playback device error reporting settings.
            :param font_download: Subtitle font settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashdvbsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                dash_dvb_settings_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbSettingsProperty(
                    error_metrics=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbMetricsReportingProperty(
                        probability=123,
                        reporting_url="reportingUrl"
                    )],
                    font_download=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbFontDownloadProperty(
                        font_family="fontFamily",
                        mime_type="mimeType",
                        url="url"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd55debb5e0e9878e82c531547def56d48981e21b29d5bb5f244612a6623334c)
                check_type(argname="argument error_metrics", value=error_metrics, expected_type=type_hints["error_metrics"])
                check_type(argname="argument font_download", value=font_download, expected_type=type_hints["font_download"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_metrics is not None:
                self._values["error_metrics"] = error_metrics
            if font_download is not None:
                self._values["font_download"] = font_download

        @builtins.property
        def error_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashDvbMetricsReportingProperty"]]]]:
            '''Playback device error reporting settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashdvbsettings.html#cfn-mediapackagev2-originendpoint-dashdvbsettings-errormetrics
            '''
            result = self._values.get("error_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashDvbMetricsReportingProperty"]]]], result)

        @builtins.property
        def font_download(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashDvbFontDownloadProperty"]]:
            '''Subtitle font settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashdvbsettings.html#cfn-mediapackagev2-originendpoint-dashdvbsettings-fontdownload
            '''
            result = self._values.get("font_download")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashDvbFontDownloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashDvbSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.DashManifestConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_urls": "baseUrls",
            "compactness": "compactness",
            "drm_signaling": "drmSignaling",
            "dvb_settings": "dvbSettings",
            "filter_configuration": "filterConfiguration",
            "manifest_name": "manifestName",
            "manifest_window_seconds": "manifestWindowSeconds",
            "min_buffer_time_seconds": "minBufferTimeSeconds",
            "min_update_period_seconds": "minUpdatePeriodSeconds",
            "period_triggers": "periodTriggers",
            "profiles": "profiles",
            "program_information": "programInformation",
            "scte_dash": "scteDash",
            "segment_template_format": "segmentTemplateFormat",
            "subtitle_configuration": "subtitleConfiguration",
            "suggested_presentation_delay_seconds": "suggestedPresentationDelaySeconds",
            "utc_timing": "utcTiming",
        },
    )
    class DashManifestConfigurationProperty:
        def __init__(
            self,
            *,
            base_urls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashBaseUrlProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compactness: typing.Optional[builtins.str] = None,
            drm_signaling: typing.Optional[builtins.str] = None,
            dvb_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashDvbSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.FilterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            manifest_window_seconds: typing.Optional[jsii.Number] = None,
            min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
            min_update_period_seconds: typing.Optional[jsii.Number] = None,
            period_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
            program_information: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashProgramInformationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scte_dash: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.ScteDashProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            segment_template_format: typing.Optional[builtins.str] = None,
            subtitle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashSubtitleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            suggested_presentation_delay_seconds: typing.Optional[jsii.Number] = None,
            utc_timing: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashUtcTimingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The DASH manifest configuration associated with the origin endpoint.

            :param base_urls: The base URLs to use for retrieving segments.
            :param compactness: The layout of the DASH manifest that MediaPackage produces. ``STANDARD`` indicates a default manifest, which is compacted. ``NONE`` indicates a full manifest. For information about compactness, see `DASH manifest compactness <https://docs.aws.amazon.com/mediapackage/latest/userguide/compacted.html>`_ in the *AWS Elemental MediaPackage v2 User Guide* .
            :param drm_signaling: Determines how the DASH manifest signals the DRM content.
            :param dvb_settings: For endpoints that use the DVB-DASH profile only. The font download and error reporting information that you want MediaPackage to pass through to the manifest.
            :param filter_configuration: Filter configuration includes settings for manifest filtering, start and end times, and time delay that apply to all of your egress requests for this manifest.
            :param manifest_name: A short string that's appended to the endpoint URL. The child manifest name creates a unique path to this endpoint.
            :param manifest_window_seconds: The total duration (in seconds) of the manifest's content.
            :param min_buffer_time_seconds: Minimum amount of content (in seconds) that a player must keep available in the buffer.
            :param min_update_period_seconds: Minimum amount of time (in seconds) that the player should wait before requesting updates to the manifest.
            :param period_triggers: A list of triggers that controls when AWS Elemental MediaPackage separates the MPEG-DASH manifest into multiple periods. Type ``ADS`` to indicate that AWS Elemental MediaPackage must create periods in the output manifest that correspond to SCTE-35 ad markers in the input source. Leave this value empty to indicate that the manifest is contained all in one period. For more information about periods in the DASH manifest, see `Multi-period DASH in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/userguide/multi-period.html>`_ .
            :param profiles: The profile that the output is compliant with.
            :param program_information: Details about the content that you want MediaPackage to pass through in the manifest to the playback device.
            :param scte_dash: The SCTE configuration.
            :param segment_template_format: Determines the type of variable used in the ``media`` URL of the ``SegmentTemplate`` tag in the manifest. Also specifies if segment timeline information is included in ``SegmentTimeline`` or ``SegmentTemplate`` . Value description: - ``NUMBER_WITH_TIMELINE`` - The ``$Number$`` variable is used in the ``media`` URL. The value of this variable is the sequential number of the segment. A full ``SegmentTimeline`` object is presented in each ``SegmentTemplate`` .
            :param subtitle_configuration: The configuration for DASH subtitles.
            :param suggested_presentation_delay_seconds: The amount of time (in seconds) that the player should be from the end of the manifest.
            :param utc_timing: Determines the type of UTC timing included in the DASH Media Presentation Description (MPD).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                dash_manifest_configuration_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashManifestConfigurationProperty(
                    base_urls=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashBaseUrlProperty(
                        dvb_priority=123,
                        dvb_weight=123,
                        service_location="serviceLocation",
                        url="url"
                    )],
                    compactness="compactness",
                    drm_signaling="drmSignaling",
                    dvb_settings=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbSettingsProperty(
                        error_metrics=[mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbMetricsReportingProperty(
                            probability=123,
                            reporting_url="reportingUrl"
                        )],
                        font_download=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashDvbFontDownloadProperty(
                            font_family="fontFamily",
                            mime_type="mimeType",
                            url="url"
                        )
                    ),
                    filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                        clip_start_time="clipStartTime",
                        end="end",
                        manifest_filter="manifestFilter",
                        start="start",
                        time_delay_seconds=123
                    ),
                    manifest_name="manifestName",
                    manifest_window_seconds=123,
                    min_buffer_time_seconds=123,
                    min_update_period_seconds=123,
                    period_triggers=["periodTriggers"],
                    profiles=["profiles"],
                    program_information=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashProgramInformationProperty(
                        copyright="copyright",
                        language_code="languageCode",
                        more_information_url="moreInformationUrl",
                        source="source",
                        title="title"
                    ),
                    scte_dash=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteDashProperty(
                        ad_marker_dash="adMarkerDash"
                    ),
                    segment_template_format="segmentTemplateFormat",
                    subtitle_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashSubtitleConfigurationProperty(
                        ttml_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashTtmlConfigurationProperty(
                            ttml_profile="ttmlProfile"
                        )
                    ),
                    suggested_presentation_delay_seconds=123,
                    utc_timing=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashUtcTimingProperty(
                        timing_mode="timingMode",
                        timing_source="timingSource"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce0c0c82051d9369b2b9a5131f3ce9edf8a0fec21d18b3aaf1205f72ce80c673)
                check_type(argname="argument base_urls", value=base_urls, expected_type=type_hints["base_urls"])
                check_type(argname="argument compactness", value=compactness, expected_type=type_hints["compactness"])
                check_type(argname="argument drm_signaling", value=drm_signaling, expected_type=type_hints["drm_signaling"])
                check_type(argname="argument dvb_settings", value=dvb_settings, expected_type=type_hints["dvb_settings"])
                check_type(argname="argument filter_configuration", value=filter_configuration, expected_type=type_hints["filter_configuration"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument manifest_window_seconds", value=manifest_window_seconds, expected_type=type_hints["manifest_window_seconds"])
                check_type(argname="argument min_buffer_time_seconds", value=min_buffer_time_seconds, expected_type=type_hints["min_buffer_time_seconds"])
                check_type(argname="argument min_update_period_seconds", value=min_update_period_seconds, expected_type=type_hints["min_update_period_seconds"])
                check_type(argname="argument period_triggers", value=period_triggers, expected_type=type_hints["period_triggers"])
                check_type(argname="argument profiles", value=profiles, expected_type=type_hints["profiles"])
                check_type(argname="argument program_information", value=program_information, expected_type=type_hints["program_information"])
                check_type(argname="argument scte_dash", value=scte_dash, expected_type=type_hints["scte_dash"])
                check_type(argname="argument segment_template_format", value=segment_template_format, expected_type=type_hints["segment_template_format"])
                check_type(argname="argument subtitle_configuration", value=subtitle_configuration, expected_type=type_hints["subtitle_configuration"])
                check_type(argname="argument suggested_presentation_delay_seconds", value=suggested_presentation_delay_seconds, expected_type=type_hints["suggested_presentation_delay_seconds"])
                check_type(argname="argument utc_timing", value=utc_timing, expected_type=type_hints["utc_timing"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_urls is not None:
                self._values["base_urls"] = base_urls
            if compactness is not None:
                self._values["compactness"] = compactness
            if drm_signaling is not None:
                self._values["drm_signaling"] = drm_signaling
            if dvb_settings is not None:
                self._values["dvb_settings"] = dvb_settings
            if filter_configuration is not None:
                self._values["filter_configuration"] = filter_configuration
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if manifest_window_seconds is not None:
                self._values["manifest_window_seconds"] = manifest_window_seconds
            if min_buffer_time_seconds is not None:
                self._values["min_buffer_time_seconds"] = min_buffer_time_seconds
            if min_update_period_seconds is not None:
                self._values["min_update_period_seconds"] = min_update_period_seconds
            if period_triggers is not None:
                self._values["period_triggers"] = period_triggers
            if profiles is not None:
                self._values["profiles"] = profiles
            if program_information is not None:
                self._values["program_information"] = program_information
            if scte_dash is not None:
                self._values["scte_dash"] = scte_dash
            if segment_template_format is not None:
                self._values["segment_template_format"] = segment_template_format
            if subtitle_configuration is not None:
                self._values["subtitle_configuration"] = subtitle_configuration
            if suggested_presentation_delay_seconds is not None:
                self._values["suggested_presentation_delay_seconds"] = suggested_presentation_delay_seconds
            if utc_timing is not None:
                self._values["utc_timing"] = utc_timing

        @builtins.property
        def base_urls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashBaseUrlProperty"]]]]:
            '''The base URLs to use for retrieving segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-baseurls
            '''
            result = self._values.get("base_urls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashBaseUrlProperty"]]]], result)

        @builtins.property
        def compactness(self) -> typing.Optional[builtins.str]:
            '''The layout of the DASH manifest that MediaPackage produces.

            ``STANDARD`` indicates a default manifest, which is compacted. ``NONE`` indicates a full manifest.

            For information about compactness, see `DASH manifest compactness <https://docs.aws.amazon.com/mediapackage/latest/userguide/compacted.html>`_ in the *AWS Elemental MediaPackage v2 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-compactness
            '''
            result = self._values.get("compactness")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def drm_signaling(self) -> typing.Optional[builtins.str]:
            '''Determines how the DASH manifest signals the DRM content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-drmsignaling
            '''
            result = self._values.get("drm_signaling")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dvb_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashDvbSettingsProperty"]]:
            '''For endpoints that use the DVB-DASH profile only.

            The font download and error reporting information that you want MediaPackage to pass through to the manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-dvbsettings
            '''
            result = self._values.get("dvb_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashDvbSettingsProperty"]], result)

        @builtins.property
        def filter_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.FilterConfigurationProperty"]]:
            '''Filter configuration includes settings for manifest filtering, start and end times, and time delay that apply to all of your egress requests for this manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-filterconfiguration
            '''
            result = self._values.get("filter_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.FilterConfigurationProperty"]], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''A short string that's appended to the endpoint URL.

            The child manifest name creates a unique path to this endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''The total duration (in seconds) of the manifest's content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-manifestwindowseconds
            '''
            result = self._values.get("manifest_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_buffer_time_seconds(self) -> typing.Optional[jsii.Number]:
            '''Minimum amount of content (in seconds) that a player must keep available in the buffer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-minbuffertimeseconds
            '''
            result = self._values.get("min_buffer_time_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_update_period_seconds(self) -> typing.Optional[jsii.Number]:
            '''Minimum amount of time (in seconds) that the player should wait before requesting updates to the manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-minupdateperiodseconds
            '''
            result = self._values.get("min_update_period_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def period_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of triggers that controls when AWS Elemental MediaPackage separates the MPEG-DASH manifest into multiple periods.

            Type ``ADS`` to indicate that AWS Elemental MediaPackage must create periods in the output manifest that correspond to SCTE-35 ad markers in the input source. Leave this value empty to indicate that the manifest is contained all in one period. For more information about periods in the DASH manifest, see `Multi-period DASH in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/userguide/multi-period.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-periodtriggers
            '''
            result = self._values.get("period_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def profiles(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The profile that the output is compliant with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-profiles
            '''
            result = self._values.get("profiles")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def program_information(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashProgramInformationProperty"]]:
            '''Details about the content that you want MediaPackage to pass through in the manifest to the playback device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-programinformation
            '''
            result = self._values.get("program_information")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashProgramInformationProperty"]], result)

        @builtins.property
        def scte_dash(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.ScteDashProperty"]]:
            '''The SCTE configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-sctedash
            '''
            result = self._values.get("scte_dash")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.ScteDashProperty"]], result)

        @builtins.property
        def segment_template_format(self) -> typing.Optional[builtins.str]:
            '''Determines the type of variable used in the ``media`` URL of the ``SegmentTemplate`` tag in the manifest.

            Also specifies if segment timeline information is included in ``SegmentTimeline`` or ``SegmentTemplate`` .

            Value description:

            - ``NUMBER_WITH_TIMELINE`` - The ``$Number$`` variable is used in the ``media`` URL. The value of this variable is the sequential number of the segment. A full ``SegmentTimeline`` object is presented in each ``SegmentTemplate`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-segmenttemplateformat
            '''
            result = self._values.get("segment_template_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subtitle_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashSubtitleConfigurationProperty"]]:
            '''The configuration for DASH subtitles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-subtitleconfiguration
            '''
            result = self._values.get("subtitle_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashSubtitleConfigurationProperty"]], result)

        @builtins.property
        def suggested_presentation_delay_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time (in seconds) that the player should be from the end of the manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-suggestedpresentationdelayseconds
            '''
            result = self._values.get("suggested_presentation_delay_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def utc_timing(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashUtcTimingProperty"]]:
            '''Determines the type of UTC timing included in the DASH Media Presentation Description (MPD).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-dashmanifestconfiguration-utctiming
            '''
            result = self._values.get("utc_timing")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashUtcTimingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashManifestConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.DashProgramInformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "copyright": "copyright",
            "language_code": "languageCode",
            "more_information_url": "moreInformationUrl",
            "source": "source",
            "title": "title",
        },
    )
    class DashProgramInformationProperty:
        def __init__(
            self,
            *,
            copyright: typing.Optional[builtins.str] = None,
            language_code: typing.Optional[builtins.str] = None,
            more_information_url: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details about the content that you want MediaPackage to pass through in the manifest to the playback device.

            :param copyright: A copyright statement about the content.
            :param language_code: The language code for this manifest.
            :param more_information_url: An absolute URL that contains more information about this content.
            :param source: Information about the content provider.
            :param title: The title for the manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashprograminformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                dash_program_information_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashProgramInformationProperty(
                    copyright="copyright",
                    language_code="languageCode",
                    more_information_url="moreInformationUrl",
                    source="source",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2cb3dcb46775e00a1a1f0b07a3558648a0d7ddf733741efa5a51b97c2b089840)
                check_type(argname="argument copyright", value=copyright, expected_type=type_hints["copyright"])
                check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
                check_type(argname="argument more_information_url", value=more_information_url, expected_type=type_hints["more_information_url"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if copyright is not None:
                self._values["copyright"] = copyright
            if language_code is not None:
                self._values["language_code"] = language_code
            if more_information_url is not None:
                self._values["more_information_url"] = more_information_url
            if source is not None:
                self._values["source"] = source
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def copyright(self) -> typing.Optional[builtins.str]:
            '''A copyright statement about the content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashprograminformation.html#cfn-mediapackagev2-originendpoint-dashprograminformation-copyright
            '''
            result = self._values.get("copyright")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def language_code(self) -> typing.Optional[builtins.str]:
            '''The language code for this manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashprograminformation.html#cfn-mediapackagev2-originendpoint-dashprograminformation-languagecode
            '''
            result = self._values.get("language_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def more_information_url(self) -> typing.Optional[builtins.str]:
            '''An absolute URL that contains more information about this content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashprograminformation.html#cfn-mediapackagev2-originendpoint-dashprograminformation-moreinformationurl
            '''
            result = self._values.get("more_information_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''Information about the content provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashprograminformation.html#cfn-mediapackagev2-originendpoint-dashprograminformation-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title for the manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashprograminformation.html#cfn-mediapackagev2-originendpoint-dashprograminformation-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashProgramInformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.DashSubtitleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"ttml_configuration": "ttmlConfiguration"},
    )
    class DashSubtitleConfigurationProperty:
        def __init__(
            self,
            *,
            ttml_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.DashTtmlConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for DASH subtitles.

            :param ttml_configuration: Settings for TTML subtitles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashsubtitleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                dash_subtitle_configuration_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashSubtitleConfigurationProperty(
                    ttml_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashTtmlConfigurationProperty(
                        ttml_profile="ttmlProfile"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4aa23a6bda26122ab3fa53a219c71a2c2a5042b6317b657322c1b88a1ed10513)
                check_type(argname="argument ttml_configuration", value=ttml_configuration, expected_type=type_hints["ttml_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ttml_configuration is not None:
                self._values["ttml_configuration"] = ttml_configuration

        @builtins.property
        def ttml_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashTtmlConfigurationProperty"]]:
            '''Settings for TTML subtitles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashsubtitleconfiguration.html#cfn-mediapackagev2-originendpoint-dashsubtitleconfiguration-ttmlconfiguration
            '''
            result = self._values.get("ttml_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.DashTtmlConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashSubtitleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.DashTtmlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"ttml_profile": "ttmlProfile"},
    )
    class DashTtmlConfigurationProperty:
        def __init__(
            self,
            *,
            ttml_profile: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for TTML subtitles.

            :param ttml_profile: The profile that MediaPackage uses when signaling subtitles in the manifest. ``IMSC`` is the default profile. ``EBU-TT-D`` produces subtitles that are compliant with the EBU-TT-D TTML profile. MediaPackage passes through subtitle styles to the manifest. For more information about EBU-TT-D subtitles, see `EBU-TT-D Subtitling Distribution Format <https://docs.aws.amazon.com/https://tech.ebu.ch/publications/tech3380>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashttmlconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                dash_ttml_configuration_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashTtmlConfigurationProperty(
                    ttml_profile="ttmlProfile"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f8e02ac42e26a2449aebdd6c27790886895a44d2b31ba429bda30096abdec31)
                check_type(argname="argument ttml_profile", value=ttml_profile, expected_type=type_hints["ttml_profile"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ttml_profile is not None:
                self._values["ttml_profile"] = ttml_profile

        @builtins.property
        def ttml_profile(self) -> typing.Optional[builtins.str]:
            '''The profile that MediaPackage uses when signaling subtitles in the manifest.

            ``IMSC`` is the default profile. ``EBU-TT-D`` produces subtitles that are compliant with the EBU-TT-D TTML profile. MediaPackage passes through subtitle styles to the manifest. For more information about EBU-TT-D subtitles, see `EBU-TT-D Subtitling Distribution Format <https://docs.aws.amazon.com/https://tech.ebu.ch/publications/tech3380>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashttmlconfiguration.html#cfn-mediapackagev2-originendpoint-dashttmlconfiguration-ttmlprofile
            '''
            result = self._values.get("ttml_profile")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashTtmlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.DashUtcTimingProperty",
        jsii_struct_bases=[],
        name_mapping={"timing_mode": "timingMode", "timing_source": "timingSource"},
    )
    class DashUtcTimingProperty:
        def __init__(
            self,
            *,
            timing_mode: typing.Optional[builtins.str] = None,
            timing_source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Determines the type of UTC timing included in the DASH Media Presentation Description (MPD).

            :param timing_mode: The UTC timing mode.
            :param timing_source: The the method that the player uses to synchronize to coordinated universal time (UTC) wall clock time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashutctiming.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                dash_utc_timing_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.DashUtcTimingProperty(
                    timing_mode="timingMode",
                    timing_source="timingSource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e303344fd691280b0c3d0d31c6f78353b63d3ba7c8ad54680f8fa820c318466f)
                check_type(argname="argument timing_mode", value=timing_mode, expected_type=type_hints["timing_mode"])
                check_type(argname="argument timing_source", value=timing_source, expected_type=type_hints["timing_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if timing_mode is not None:
                self._values["timing_mode"] = timing_mode
            if timing_source is not None:
                self._values["timing_source"] = timing_source

        @builtins.property
        def timing_mode(self) -> typing.Optional[builtins.str]:
            '''The UTC timing mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashutctiming.html#cfn-mediapackagev2-originendpoint-dashutctiming-timingmode
            '''
            result = self._values.get("timing_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timing_source(self) -> typing.Optional[builtins.str]:
            '''The the method that the player uses to synchronize to coordinated universal time (UTC) wall clock time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-dashutctiming.html#cfn-mediapackagev2-originendpoint-dashutctiming-timingsource
            '''
            result = self._values.get("timing_source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashUtcTimingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "preset_speke20_audio": "presetSpeke20Audio",
            "preset_speke20_video": "presetSpeke20Video",
        },
    )
    class EncryptionContractConfigurationProperty:
        def __init__(
            self,
            *,
            preset_speke20_audio: typing.Optional[builtins.str] = None,
            preset_speke20_video: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines which content keys are used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use.

            :param preset_speke20_audio: A collection of audio encryption presets. Value description: - ``PRESET-AUDIO-1`` - Use one content key to encrypt all of the audio tracks in your stream. - ``PRESET-AUDIO-2`` - Use one content key to encrypt all of the stereo audio tracks and one content key to encrypt all of the multichannel audio tracks. - ``PRESET-AUDIO-3`` - Use one content key to encrypt all of the stereo audio tracks, one content key to encrypt all of the multichannel audio tracks with 3 to 6 channels, and one content key to encrypt all of the multichannel audio tracks with more than 6 channels. - ``SHARED`` - Use the same content key for all of the audio and video tracks in your stream. - ``UNENCRYPTED`` - Don't encrypt any of the audio tracks in your stream.
            :param preset_speke20_video: The SPEKE Version 2.0 preset video associated with the encryption contract configuration of the origin endpoint. A collection of video encryption presets. Value description: - ``PRESET-VIDEO-1`` - Use one content key to encrypt all of the video tracks in your stream. - ``PRESET-VIDEO-2`` - Use one content key to encrypt all of the SD video tracks and one content key for all HD and higher resolutions video tracks. - ``PRESET-VIDEO-3`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-4`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``PRESET-VIDEO-5`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``PRESET-VIDEO-6`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-7`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-8`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``SHARED`` - Use the same content key for all of the video and audio tracks in your stream. - ``UNENCRYPTED`` - Don't encrypt any of the video tracks in your stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryptioncontractconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                encryption_contract_configuration_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                    preset_speke20_audio="presetSpeke20Audio",
                    preset_speke20_video="presetSpeke20Video"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3ec1c047a7ff8e0cdf626a427c81fb2e93fe27822632f8b15415a16292c0474)
                check_type(argname="argument preset_speke20_audio", value=preset_speke20_audio, expected_type=type_hints["preset_speke20_audio"])
                check_type(argname="argument preset_speke20_video", value=preset_speke20_video, expected_type=type_hints["preset_speke20_video"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if preset_speke20_audio is not None:
                self._values["preset_speke20_audio"] = preset_speke20_audio
            if preset_speke20_video is not None:
                self._values["preset_speke20_video"] = preset_speke20_video

        @builtins.property
        def preset_speke20_audio(self) -> typing.Optional[builtins.str]:
            '''A collection of audio encryption presets.

            Value description:

            - ``PRESET-AUDIO-1`` - Use one content key to encrypt all of the audio tracks in your stream.
            - ``PRESET-AUDIO-2`` - Use one content key to encrypt all of the stereo audio tracks and one content key to encrypt all of the multichannel audio tracks.
            - ``PRESET-AUDIO-3`` - Use one content key to encrypt all of the stereo audio tracks, one content key to encrypt all of the multichannel audio tracks with 3 to 6 channels, and one content key to encrypt all of the multichannel audio tracks with more than 6 channels.
            - ``SHARED`` - Use the same content key for all of the audio and video tracks in your stream.
            - ``UNENCRYPTED`` - Don't encrypt any of the audio tracks in your stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryptioncontractconfiguration.html#cfn-mediapackagev2-originendpoint-encryptioncontractconfiguration-presetspeke20audio
            '''
            result = self._values.get("preset_speke20_audio")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preset_speke20_video(self) -> typing.Optional[builtins.str]:
            '''The SPEKE Version 2.0 preset video associated with the encryption contract configuration of the origin endpoint.

            A collection of video encryption presets.

            Value description:

            - ``PRESET-VIDEO-1`` - Use one content key to encrypt all of the video tracks in your stream.
            - ``PRESET-VIDEO-2`` - Use one content key to encrypt all of the SD video tracks and one content key for all HD and higher resolutions video tracks.
            - ``PRESET-VIDEO-3`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-4`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``PRESET-VIDEO-5`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``PRESET-VIDEO-6`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-7`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-8`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``SHARED`` - Use the same content key for all of the video and audio tracks in your stream.
            - ``UNENCRYPTED`` - Don't encrypt any of the video tracks in your stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryptioncontractconfiguration.html#cfn-mediapackagev2-originendpoint-encryptioncontractconfiguration-presetspeke20video
            '''
            result = self._values.get("preset_speke20_video")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionContractConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.EncryptionMethodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cmaf_encryption_method": "cmafEncryptionMethod",
            "ism_encryption_method": "ismEncryptionMethod",
            "ts_encryption_method": "tsEncryptionMethod",
        },
    )
    class EncryptionMethodProperty:
        def __init__(
            self,
            *,
            cmaf_encryption_method: typing.Optional[builtins.str] = None,
            ism_encryption_method: typing.Optional[builtins.str] = None,
            ts_encryption_method: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The encryption method associated with the origin endpoint.

            :param cmaf_encryption_method: The encryption method to use.
            :param ism_encryption_method: The encryption method used for Microsoft Smooth Streaming (MSS) content. This specifies how the MSS segments are encrypted to protect the content during delivery to client players.
            :param ts_encryption_method: The encryption method to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryptionmethod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                encryption_method_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionMethodProperty(
                    cmaf_encryption_method="cmafEncryptionMethod",
                    ism_encryption_method="ismEncryptionMethod",
                    ts_encryption_method="tsEncryptionMethod"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6031cb0f031776a2f8ab3f2412c73423286d57c89d0f2f057ebc4b9c936e94b)
                check_type(argname="argument cmaf_encryption_method", value=cmaf_encryption_method, expected_type=type_hints["cmaf_encryption_method"])
                check_type(argname="argument ism_encryption_method", value=ism_encryption_method, expected_type=type_hints["ism_encryption_method"])
                check_type(argname="argument ts_encryption_method", value=ts_encryption_method, expected_type=type_hints["ts_encryption_method"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cmaf_encryption_method is not None:
                self._values["cmaf_encryption_method"] = cmaf_encryption_method
            if ism_encryption_method is not None:
                self._values["ism_encryption_method"] = ism_encryption_method
            if ts_encryption_method is not None:
                self._values["ts_encryption_method"] = ts_encryption_method

        @builtins.property
        def cmaf_encryption_method(self) -> typing.Optional[builtins.str]:
            '''The encryption method to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryptionmethod.html#cfn-mediapackagev2-originendpoint-encryptionmethod-cmafencryptionmethod
            '''
            result = self._values.get("cmaf_encryption_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ism_encryption_method(self) -> typing.Optional[builtins.str]:
            '''The encryption method used for Microsoft Smooth Streaming (MSS) content.

            This specifies how the MSS segments are encrypted to protect the content during delivery to client players.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryptionmethod.html#cfn-mediapackagev2-originendpoint-encryptionmethod-ismencryptionmethod
            '''
            result = self._values.get("ism_encryption_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ts_encryption_method(self) -> typing.Optional[builtins.str]:
            '''The encryption method to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryptionmethod.html#cfn-mediapackagev2-originendpoint-encryptionmethod-tsencryptionmethod
            '''
            result = self._values.get("ts_encryption_method")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionMethodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cmaf_exclude_segment_drm_metadata": "cmafExcludeSegmentDrmMetadata",
            "constant_initialization_vector": "constantInitializationVector",
            "encryption_method": "encryptionMethod",
            "key_rotation_interval_seconds": "keyRotationIntervalSeconds",
            "speke_key_provider": "spekeKeyProvider",
        },
    )
    class EncryptionProperty:
        def __init__(
            self,
            *,
            cmaf_exclude_segment_drm_metadata: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            encryption_method: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.EncryptionMethodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
            speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The parameters for encrypting content.

            :param cmaf_exclude_segment_drm_metadata: Excludes SEIG and SGPD boxes from segment metadata in CMAF containers. When set to ``true`` , MediaPackage omits these DRM metadata boxes from CMAF segments, which can improve compatibility with certain devices and players that don't support these boxes. Important considerations: - This setting only affects CMAF container formats - Key rotation can still be handled through media playlist signaling - PSSH and TENC boxes remain unaffected - Default behavior is preserved when this setting is disabled Valid values: ``true`` | ``false`` Default: ``false``
            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, used in conjunction with the key for encrypting content. If you don't specify a value, then MediaPackage creates the constant initialization vector (IV).
            :param encryption_method: The encryption method to use.
            :param key_rotation_interval_seconds: The interval, in seconds, to rotate encryption keys for the origin endpoint.
            :param speke_key_provider: The SPEKE key provider to use for encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                encryption_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionProperty(
                    cmaf_exclude_segment_drm_metadata=False,
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionMethodProperty(
                        cmaf_encryption_method="cmafEncryptionMethod",
                        ism_encryption_method="ismEncryptionMethod",
                        ts_encryption_method="tsEncryptionMethod"
                    ),
                    key_rotation_interval_seconds=123,
                    speke_key_provider=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                        drm_systems=["drmSystems"],
                        encryption_contract_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        ),
                        resource_id="resourceId",
                        role_arn="roleArn",
                        url="url"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0af418adfd66eecf6bb59f4fa12d495f18db6bd1a7404a36793293487dfe5071)
                check_type(argname="argument cmaf_exclude_segment_drm_metadata", value=cmaf_exclude_segment_drm_metadata, expected_type=type_hints["cmaf_exclude_segment_drm_metadata"])
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument encryption_method", value=encryption_method, expected_type=type_hints["encryption_method"])
                check_type(argname="argument key_rotation_interval_seconds", value=key_rotation_interval_seconds, expected_type=type_hints["key_rotation_interval_seconds"])
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cmaf_exclude_segment_drm_metadata is not None:
                self._values["cmaf_exclude_segment_drm_metadata"] = cmaf_exclude_segment_drm_metadata
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if encryption_method is not None:
                self._values["encryption_method"] = encryption_method
            if key_rotation_interval_seconds is not None:
                self._values["key_rotation_interval_seconds"] = key_rotation_interval_seconds
            if speke_key_provider is not None:
                self._values["speke_key_provider"] = speke_key_provider

        @builtins.property
        def cmaf_exclude_segment_drm_metadata(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Excludes SEIG and SGPD boxes from segment metadata in CMAF containers.

            When set to ``true`` , MediaPackage omits these DRM metadata boxes from CMAF segments, which can improve compatibility with certain devices and players that don't support these boxes.

            Important considerations:

            - This setting only affects CMAF container formats
            - Key rotation can still be handled through media playlist signaling
            - PSSH and TENC boxes remain unaffected
            - Default behavior is preserved when this setting is disabled

            Valid values: ``true`` | ``false``

            Default: ``false``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryption.html#cfn-mediapackagev2-originendpoint-encryption-cmafexcludesegmentdrmmetadata
            '''
            result = self._values.get("cmaf_exclude_segment_drm_metadata")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, used in conjunction with the key for encrypting content.

            If you don't specify a value, then MediaPackage creates the constant initialization vector (IV).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryption.html#cfn-mediapackagev2-originendpoint-encryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_method(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.EncryptionMethodProperty"]]:
            '''The encryption method to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryption.html#cfn-mediapackagev2-originendpoint-encryption-encryptionmethod
            '''
            result = self._values.get("encryption_method")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.EncryptionMethodProperty"]], result)

        @builtins.property
        def key_rotation_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''The interval, in seconds, to rotate encryption keys for the origin endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryption.html#cfn-mediapackagev2-originendpoint-encryption-keyrotationintervalseconds
            '''
            result = self._values.get("key_rotation_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty"]]:
            '''The SPEKE key provider to use for encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-encryption.html#cfn-mediapackagev2-originendpoint-encryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "clip_start_time": "clipStartTime",
            "end": "end",
            "manifest_filter": "manifestFilter",
            "start": "start",
            "time_delay_seconds": "timeDelaySeconds",
        },
    )
    class FilterConfigurationProperty:
        def __init__(
            self,
            *,
            clip_start_time: typing.Optional[builtins.str] = None,
            end: typing.Optional[builtins.str] = None,
            manifest_filter: typing.Optional[builtins.str] = None,
            start: typing.Optional[builtins.str] = None,
            time_delay_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Filter configuration includes settings for manifest filtering, start and end times, and time delay that apply to all of your egress requests for this manifest.

            :param clip_start_time: Optionally specify the clip start time for all of your manifest egress requests. When you include clip start time, note that you cannot use clip start time query parameters for this manifest's endpoint URL.
            :param end: Optionally specify the end time for all of your manifest egress requests. When you include end time, note that you cannot use end time query parameters for this manifest's endpoint URL.
            :param manifest_filter: Optionally specify one or more manifest filters for all of your manifest egress requests. When you include a manifest filter, note that you cannot use an identical manifest filter query parameter for this manifest's endpoint URL.
            :param start: Optionally specify the start time for all of your manifest egress requests. When you include start time, note that you cannot use start time query parameters for this manifest's endpoint URL.
            :param time_delay_seconds: Optionally specify the time delay for all of your manifest egress requests. Enter a value that is smaller than your endpoint's startover window. When you include time delay, note that you cannot use time delay query parameters for this manifest's endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-filterconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                filter_configuration_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                    clip_start_time="clipStartTime",
                    end="end",
                    manifest_filter="manifestFilter",
                    start="start",
                    time_delay_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1290eaa7d5791f3ea9080910bfc1f75dbd06db2b9d0427336f29940295cef02)
                check_type(argname="argument clip_start_time", value=clip_start_time, expected_type=type_hints["clip_start_time"])
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument manifest_filter", value=manifest_filter, expected_type=type_hints["manifest_filter"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
                check_type(argname="argument time_delay_seconds", value=time_delay_seconds, expected_type=type_hints["time_delay_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if clip_start_time is not None:
                self._values["clip_start_time"] = clip_start_time
            if end is not None:
                self._values["end"] = end
            if manifest_filter is not None:
                self._values["manifest_filter"] = manifest_filter
            if start is not None:
                self._values["start"] = start
            if time_delay_seconds is not None:
                self._values["time_delay_seconds"] = time_delay_seconds

        @builtins.property
        def clip_start_time(self) -> typing.Optional[builtins.str]:
            '''Optionally specify the clip start time for all of your manifest egress requests.

            When you include clip start time, note that you cannot use clip start time query parameters for this manifest's endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-filterconfiguration.html#cfn-mediapackagev2-originendpoint-filterconfiguration-clipstarttime
            '''
            result = self._values.get("clip_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def end(self) -> typing.Optional[builtins.str]:
            '''Optionally specify the end time for all of your manifest egress requests.

            When you include end time, note that you cannot use end time query parameters for this manifest's endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-filterconfiguration.html#cfn-mediapackagev2-originendpoint-filterconfiguration-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_filter(self) -> typing.Optional[builtins.str]:
            '''Optionally specify one or more manifest filters for all of your manifest egress requests.

            When you include a manifest filter, note that you cannot use an identical manifest filter query parameter for this manifest's endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-filterconfiguration.html#cfn-mediapackagev2-originendpoint-filterconfiguration-manifestfilter
            '''
            result = self._values.get("manifest_filter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start(self) -> typing.Optional[builtins.str]:
            '''Optionally specify the start time for all of your manifest egress requests.

            When you include start time, note that you cannot use start time query parameters for this manifest's endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-filterconfiguration.html#cfn-mediapackagev2-originendpoint-filterconfiguration-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_delay_seconds(self) -> typing.Optional[jsii.Number]:
            '''Optionally specify the time delay for all of your manifest egress requests.

            Enter a value that is smaller than your endpoint's startover window. When you include time delay, note that you cannot use time delay query parameters for this manifest's endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-filterconfiguration.html#cfn-mediapackagev2-originendpoint-filterconfiguration-timedelayseconds
            '''
            result = self._values.get("time_delay_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.ForceEndpointErrorConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_error_conditions": "endpointErrorConditions"},
    )
    class ForceEndpointErrorConfigurationProperty:
        def __init__(
            self,
            *,
            endpoint_error_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The failover settings for the endpoint.

            :param endpoint_error_conditions: The failover conditions for the endpoint. The options are:. - ``STALE_MANIFEST`` - The manifest stalled and there are no new segments or parts. - ``INCOMPLETE_MANIFEST`` - There is a gap in the manifest. - ``MISSING_DRM_KEY`` - Key rotation is enabled but we're unable to fetch the key for the current key period. - ``SLATE_INPUT`` - The segments which contain slate content are considered to be missing content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-forceendpointerrorconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                force_endpoint_error_configuration_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ForceEndpointErrorConfigurationProperty(
                    endpoint_error_conditions=["endpointErrorConditions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a138aa60f361c8ca6a3410ca59b89cfea0daef749926330643599dacdd94b298)
                check_type(argname="argument endpoint_error_conditions", value=endpoint_error_conditions, expected_type=type_hints["endpoint_error_conditions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint_error_conditions is not None:
                self._values["endpoint_error_conditions"] = endpoint_error_conditions

        @builtins.property
        def endpoint_error_conditions(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The failover conditions for the endpoint. The options are:.

            - ``STALE_MANIFEST`` - The manifest stalled and there are no new segments or parts.
            - ``INCOMPLETE_MANIFEST`` - There is a gap in the manifest.
            - ``MISSING_DRM_KEY`` - Key rotation is enabled but we're unable to fetch the key for the current key period.
            - ``SLATE_INPUT`` - The segments which contain slate content are considered to be missing content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-forceendpointerrorconfiguration.html#cfn-mediapackagev2-originendpoint-forceendpointerrorconfiguration-endpointerrorconditions
            '''
            result = self._values.get("endpoint_error_conditions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForceEndpointErrorConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.HlsManifestConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "child_manifest_name": "childManifestName",
            "filter_configuration": "filterConfiguration",
            "manifest_name": "manifestName",
            "manifest_window_seconds": "manifestWindowSeconds",
            "program_date_time_interval_seconds": "programDateTimeIntervalSeconds",
            "scte_hls": "scteHls",
            "start_tag": "startTag",
            "url": "url",
            "url_encode_child_manifest": "urlEncodeChildManifest",
        },
    )
    class HlsManifestConfigurationProperty:
        def __init__(
            self,
            *,
            child_manifest_name: typing.Optional[builtins.str] = None,
            filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.FilterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            manifest_window_seconds: typing.Optional[jsii.Number] = None,
            program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
            scte_hls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.ScteHlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            start_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.StartTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            url: typing.Optional[builtins.str] = None,
            url_encode_child_manifest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The HLS manifest configuration associated with the origin endpoint.

            :param child_manifest_name: The name of the child manifest associated with the HLS manifest configuration.
            :param filter_configuration: Filter configuration includes settings for manifest filtering, start and end times, and time delay that apply to all of your egress requests for this manifest.
            :param manifest_name: The name of the manifest associated with the HLS manifest configuration.
            :param manifest_window_seconds: The duration of the manifest window, in seconds, for the HLS manifest configuration.
            :param program_date_time_interval_seconds: The ``EXT-X-PROGRAM-DATE-TIME`` interval, in seconds, associated with the HLS manifest configuration.
            :param scte_hls: THE SCTE-35 HLS configuration associated with the HLS manifest configuration.
            :param start_tag: To insert an EXT-X-START tag in your HLS playlist, specify a StartTag configuration object with a valid TimeOffset. When you do, you can also optionally specify whether to include a PRECISE value in the EXT-X-START tag.
            :param url: The URL of the HLS manifest configuration.
            :param url_encode_child_manifest: When enabled, MediaPackage URL-encodes the query string for API requests for HLS child manifests to comply with AWS Signature Version 4 (SigV4) signature signing protocol. For more information, see `AWS Signature Version 4 for API requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html>`_ in *AWS Identity and Access Management User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-hlsmanifestconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                hls_manifest_configuration_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.HlsManifestConfigurationProperty(
                    child_manifest_name="childManifestName",
                    filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                        clip_start_time="clipStartTime",
                        end="end",
                        manifest_filter="manifestFilter",
                        start="start",
                        time_delay_seconds=123
                    ),
                    manifest_name="manifestName",
                    manifest_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    scte_hls=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteHlsProperty(
                        ad_marker_hls="adMarkerHls"
                    ),
                    start_tag=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.StartTagProperty(
                        precise=False,
                        time_offset=123
                    ),
                    url="url",
                    url_encode_child_manifest=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a16bb5707710c545bb6f1c1157f10ae97c5effcac7817c459d33b5410ec37fd)
                check_type(argname="argument child_manifest_name", value=child_manifest_name, expected_type=type_hints["child_manifest_name"])
                check_type(argname="argument filter_configuration", value=filter_configuration, expected_type=type_hints["filter_configuration"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument manifest_window_seconds", value=manifest_window_seconds, expected_type=type_hints["manifest_window_seconds"])
                check_type(argname="argument program_date_time_interval_seconds", value=program_date_time_interval_seconds, expected_type=type_hints["program_date_time_interval_seconds"])
                check_type(argname="argument scte_hls", value=scte_hls, expected_type=type_hints["scte_hls"])
                check_type(argname="argument start_tag", value=start_tag, expected_type=type_hints["start_tag"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument url_encode_child_manifest", value=url_encode_child_manifest, expected_type=type_hints["url_encode_child_manifest"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if child_manifest_name is not None:
                self._values["child_manifest_name"] = child_manifest_name
            if filter_configuration is not None:
                self._values["filter_configuration"] = filter_configuration
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if manifest_window_seconds is not None:
                self._values["manifest_window_seconds"] = manifest_window_seconds
            if program_date_time_interval_seconds is not None:
                self._values["program_date_time_interval_seconds"] = program_date_time_interval_seconds
            if scte_hls is not None:
                self._values["scte_hls"] = scte_hls
            if start_tag is not None:
                self._values["start_tag"] = start_tag
            if url is not None:
                self._values["url"] = url
            if url_encode_child_manifest is not None:
                self._values["url_encode_child_manifest"] = url_encode_child_manifest

        @builtins.property
        def child_manifest_name(self) -> typing.Optional[builtins.str]:
            '''The name of the child manifest associated with the HLS manifest configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-hlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-hlsmanifestconfiguration-childmanifestname
            '''
            result = self._values.get("child_manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.FilterConfigurationProperty"]]:
            '''Filter configuration includes settings for manifest filtering, start and end times, and time delay that apply to all of your egress requests for this manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-hlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-hlsmanifestconfiguration-filterconfiguration
            '''
            result = self._values.get("filter_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.FilterConfigurationProperty"]], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''The name of the manifest associated with the HLS manifest configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-hlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-hlsmanifestconfiguration-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''The duration of the manifest window, in seconds, for the HLS manifest configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-hlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-hlsmanifestconfiguration-manifestwindowseconds
            '''
            result = self._values.get("manifest_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def program_date_time_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''The ``EXT-X-PROGRAM-DATE-TIME`` interval, in seconds, associated with the HLS manifest configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-hlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-hlsmanifestconfiguration-programdatetimeintervalseconds
            '''
            result = self._values.get("program_date_time_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scte_hls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.ScteHlsProperty"]]:
            '''THE SCTE-35 HLS configuration associated with the HLS manifest configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-hlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-hlsmanifestconfiguration-sctehls
            '''
            result = self._values.get("scte_hls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.ScteHlsProperty"]], result)

        @builtins.property
        def start_tag(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StartTagProperty"]]:
            '''To insert an EXT-X-START tag in your HLS playlist, specify a StartTag configuration object with a valid TimeOffset.

            When you do, you can also optionally specify whether to include a PRECISE value in the EXT-X-START tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-hlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-hlsmanifestconfiguration-starttag
            '''
            result = self._values.get("start_tag")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StartTagProperty"]], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL of the HLS manifest configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-hlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-hlsmanifestconfiguration-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url_encode_child_manifest(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When enabled, MediaPackage URL-encodes the query string for API requests for HLS child manifests to comply with AWS Signature Version 4 (SigV4) signature signing protocol.

            For more information, see `AWS Signature Version 4 for API requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html>`_ in *AWS Identity and Access Management User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-hlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-hlsmanifestconfiguration-urlencodechildmanifest
            '''
            result = self._values.get("url_encode_child_manifest")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsManifestConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.LowLatencyHlsManifestConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "child_manifest_name": "childManifestName",
            "filter_configuration": "filterConfiguration",
            "manifest_name": "manifestName",
            "manifest_window_seconds": "manifestWindowSeconds",
            "program_date_time_interval_seconds": "programDateTimeIntervalSeconds",
            "scte_hls": "scteHls",
            "start_tag": "startTag",
            "url": "url",
            "url_encode_child_manifest": "urlEncodeChildManifest",
        },
    )
    class LowLatencyHlsManifestConfigurationProperty:
        def __init__(
            self,
            *,
            child_manifest_name: typing.Optional[builtins.str] = None,
            filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.FilterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            manifest_window_seconds: typing.Optional[jsii.Number] = None,
            program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
            scte_hls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.ScteHlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            start_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.StartTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            url: typing.Optional[builtins.str] = None,
            url_encode_child_manifest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specify a low-latency HTTP live streaming (LL-HLS) manifest configuration.

            :param child_manifest_name: The name of the child manifest associated with the low-latency HLS (LL-HLS) manifest configuration of the origin endpoint.
            :param filter_configuration: Filter configuration includes settings for manifest filtering, start and end times, and time delay that apply to all of your egress requests for this manifest.
            :param manifest_name: A short string that's appended to the endpoint URL. The manifest name creates a unique path to this endpoint. If you don't enter a value, MediaPackage uses the default manifest name, ``index`` . MediaPackage automatically inserts the format extension, such as ``.m3u8`` . You can't use the same manifest name if you use HLS manifest and low-latency HLS manifest. The ``manifestName`` on the ``HLSManifest`` object overrides the ``manifestName`` you provided on the ``originEndpoint`` object.
            :param manifest_window_seconds: The total duration (in seconds) of the manifest's content.
            :param program_date_time_interval_seconds: Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify. If you don't enter an interval, ``EXT-X-PROGRAM-DATE-TIME`` tags aren't included in the manifest. The tags sync the stream to the wall clock so that viewers can seek to a specific time in the playback timeline on the player. Irrespective of this parameter, if any ``ID3Timed`` metadata is in the HLS input, MediaPackage passes through that metadata to the HLS output.
            :param scte_hls: The SCTE-35 HLS configuration associated with the low-latency HLS (LL-HLS) manifest configuration of the origin endpoint.
            :param start_tag: To insert an EXT-X-START tag in your HLS playlist, specify a StartTag configuration object with a valid TimeOffset. When you do, you can also optionally specify whether to include a PRECISE value in the EXT-X-START tag.
            :param url: The URL of the low-latency HLS (LL-HLS) manifest configuration of the origin endpoint.
            :param url_encode_child_manifest: When enabled, MediaPackage URL-encodes the query string for API requests for LL-HLS child manifests to comply with AWS Signature Version 4 (SigV4) signature signing protocol. For more information, see `AWS Signature Version 4 for API requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html>`_ in *AWS Identity and Access Management User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                low_latency_hls_manifest_configuration_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.LowLatencyHlsManifestConfigurationProperty(
                    child_manifest_name="childManifestName",
                    filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                        clip_start_time="clipStartTime",
                        end="end",
                        manifest_filter="manifestFilter",
                        start="start",
                        time_delay_seconds=123
                    ),
                    manifest_name="manifestName",
                    manifest_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    scte_hls=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteHlsProperty(
                        ad_marker_hls="adMarkerHls"
                    ),
                    start_tag=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.StartTagProperty(
                        precise=False,
                        time_offset=123
                    ),
                    url="url",
                    url_encode_child_manifest=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__602154144ad86bc5ceb2b17ec0187491e1641d88add81c4971aed8745f38eb71)
                check_type(argname="argument child_manifest_name", value=child_manifest_name, expected_type=type_hints["child_manifest_name"])
                check_type(argname="argument filter_configuration", value=filter_configuration, expected_type=type_hints["filter_configuration"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument manifest_window_seconds", value=manifest_window_seconds, expected_type=type_hints["manifest_window_seconds"])
                check_type(argname="argument program_date_time_interval_seconds", value=program_date_time_interval_seconds, expected_type=type_hints["program_date_time_interval_seconds"])
                check_type(argname="argument scte_hls", value=scte_hls, expected_type=type_hints["scte_hls"])
                check_type(argname="argument start_tag", value=start_tag, expected_type=type_hints["start_tag"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument url_encode_child_manifest", value=url_encode_child_manifest, expected_type=type_hints["url_encode_child_manifest"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if child_manifest_name is not None:
                self._values["child_manifest_name"] = child_manifest_name
            if filter_configuration is not None:
                self._values["filter_configuration"] = filter_configuration
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if manifest_window_seconds is not None:
                self._values["manifest_window_seconds"] = manifest_window_seconds
            if program_date_time_interval_seconds is not None:
                self._values["program_date_time_interval_seconds"] = program_date_time_interval_seconds
            if scte_hls is not None:
                self._values["scte_hls"] = scte_hls
            if start_tag is not None:
                self._values["start_tag"] = start_tag
            if url is not None:
                self._values["url"] = url
            if url_encode_child_manifest is not None:
                self._values["url_encode_child_manifest"] = url_encode_child_manifest

        @builtins.property
        def child_manifest_name(self) -> typing.Optional[builtins.str]:
            '''The name of the child manifest associated with the low-latency HLS (LL-HLS) manifest configuration of the origin endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration-childmanifestname
            '''
            result = self._values.get("child_manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.FilterConfigurationProperty"]]:
            '''Filter configuration includes settings for manifest filtering, start and end times, and time delay that apply to all of your egress requests for this manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration-filterconfiguration
            '''
            result = self._values.get("filter_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.FilterConfigurationProperty"]], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''A short string that's appended to the endpoint URL.

            The manifest name creates a unique path to this endpoint. If you don't enter a value, MediaPackage uses the default manifest name, ``index`` . MediaPackage automatically inserts the format extension, such as ``.m3u8`` . You can't use the same manifest name if you use HLS manifest and low-latency HLS manifest. The ``manifestName`` on the ``HLSManifest`` object overrides the ``manifestName`` you provided on the ``originEndpoint`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''The total duration (in seconds) of the manifest's content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration-manifestwindowseconds
            '''
            result = self._values.get("manifest_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def program_date_time_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify.

            If you don't enter an interval, ``EXT-X-PROGRAM-DATE-TIME`` tags aren't included in the manifest. The tags sync the stream to the wall clock so that viewers can seek to a specific time in the playback timeline on the player.

            Irrespective of this parameter, if any ``ID3Timed`` metadata is in the HLS input, MediaPackage passes through that metadata to the HLS output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration-programdatetimeintervalseconds
            '''
            result = self._values.get("program_date_time_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scte_hls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.ScteHlsProperty"]]:
            '''The SCTE-35 HLS configuration associated with the low-latency HLS (LL-HLS) manifest configuration of the origin endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration-sctehls
            '''
            result = self._values.get("scte_hls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.ScteHlsProperty"]], result)

        @builtins.property
        def start_tag(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StartTagProperty"]]:
            '''To insert an EXT-X-START tag in your HLS playlist, specify a StartTag configuration object with a valid TimeOffset.

            When you do, you can also optionally specify whether to include a PRECISE value in the EXT-X-START tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration-starttag
            '''
            result = self._values.get("start_tag")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.StartTagProperty"]], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL of the low-latency HLS (LL-HLS) manifest configuration of the origin endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url_encode_child_manifest(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When enabled, MediaPackage URL-encodes the query string for API requests for LL-HLS child manifests to comply with AWS Signature Version 4 (SigV4) signature signing protocol.

            For more information, see `AWS Signature Version 4 for API requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html>`_ in *AWS Identity and Access Management User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-lowlatencyhlsmanifestconfiguration-urlencodechildmanifest
            '''
            result = self._values.get("url_encode_child_manifest")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LowLatencyHlsManifestConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.MssManifestConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "filter_configuration": "filterConfiguration",
            "manifest_layout": "manifestLayout",
            "manifest_name": "manifestName",
            "manifest_window_seconds": "manifestWindowSeconds",
        },
    )
    class MssManifestConfigurationProperty:
        def __init__(
            self,
            *,
            filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.FilterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            manifest_layout: typing.Optional[builtins.str] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            manifest_window_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            This includes all the settings and properties that define how the MSS content is packaged and delivered.

            :param filter_configuration:  
            :param manifest_layout: 
            :param manifest_name:  This name is appended to the origin endpoint URL to create the unique path for accessing this specific MSS manifest.
            :param manifest_window_seconds:  This represents the total amount of content available in the manifest at any given time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-mssmanifestconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                mss_manifest_configuration_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.MssManifestConfigurationProperty(
                    filter_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.FilterConfigurationProperty(
                        clip_start_time="clipStartTime",
                        end="end",
                        manifest_filter="manifestFilter",
                        start="start",
                        time_delay_seconds=123
                    ),
                    manifest_layout="manifestLayout",
                    manifest_name="manifestName",
                    manifest_window_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d258999f542e9697f1a8db03483747b7beacc8993e60bc1a8b42a269b680fc67)
                check_type(argname="argument filter_configuration", value=filter_configuration, expected_type=type_hints["filter_configuration"])
                check_type(argname="argument manifest_layout", value=manifest_layout, expected_type=type_hints["manifest_layout"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument manifest_window_seconds", value=manifest_window_seconds, expected_type=type_hints["manifest_window_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter_configuration is not None:
                self._values["filter_configuration"] = filter_configuration
            if manifest_layout is not None:
                self._values["manifest_layout"] = manifest_layout
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if manifest_window_seconds is not None:
                self._values["manifest_window_seconds"] = manifest_window_seconds

        @builtins.property
        def filter_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.FilterConfigurationProperty"]]:
            '''

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-mssmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-mssmanifestconfiguration-filterconfiguration
            '''
            result = self._values.get("filter_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.FilterConfigurationProperty"]], result)

        @builtins.property
        def manifest_layout(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-mssmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-mssmanifestconfiguration-manifestlayout
            '''
            result = self._values.get("manifest_layout")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''
            This name is appended to the origin endpoint URL to create the unique path for accessing this specific MSS manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-mssmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-mssmanifestconfiguration-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''
            This represents the total amount of content available in the manifest at any given time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-mssmanifestconfiguration.html#cfn-mediapackagev2-originendpoint-mssmanifestconfiguration-manifestwindowseconds
            '''
            result = self._values.get("manifest_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssManifestConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.ScteDashProperty",
        jsii_struct_bases=[],
        name_mapping={"ad_marker_dash": "adMarkerDash"},
    )
    class ScteDashProperty:
        def __init__(
            self,
            *,
            ad_marker_dash: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The SCTE configuration.

            :param ad_marker_dash: Choose how ad markers are included in the packaged content. If you include ad markers in the content stream in your upstream encoders, then you need to inform MediaPackage what to do with the ad markers in the output. Value description: - ``Binary`` - The SCTE-35 marker is expressed as a hex-string (Base64 string) rather than full XML. - ``XML`` - The SCTE marker is expressed fully in XML.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-sctedash.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                scte_dash_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteDashProperty(
                    ad_marker_dash="adMarkerDash"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__069845d8374a5d6fb7771e6099024215591837c8087b9806b162b4c0d75a355e)
                check_type(argname="argument ad_marker_dash", value=ad_marker_dash, expected_type=type_hints["ad_marker_dash"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_marker_dash is not None:
                self._values["ad_marker_dash"] = ad_marker_dash

        @builtins.property
        def ad_marker_dash(self) -> typing.Optional[builtins.str]:
            '''Choose how ad markers are included in the packaged content.

            If you include ad markers in the content stream in your upstream encoders, then you need to inform MediaPackage what to do with the ad markers in the output.

            Value description:

            - ``Binary`` - The SCTE-35 marker is expressed as a hex-string (Base64 string) rather than full XML.
            - ``XML`` - The SCTE marker is expressed fully in XML.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-sctedash.html#cfn-mediapackagev2-originendpoint-sctedash-admarkerdash
            '''
            result = self._values.get("ad_marker_dash")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScteDashProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.ScteHlsProperty",
        jsii_struct_bases=[],
        name_mapping={"ad_marker_hls": "adMarkerHls"},
    )
    class ScteHlsProperty:
        def __init__(
            self,
            *,
            ad_marker_hls: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The SCTE-35 HLS configuration associated with the origin endpoint.

            :param ad_marker_hls: The SCTE-35 HLS ad-marker configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-sctehls.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                scte_hls_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteHlsProperty(
                    ad_marker_hls="adMarkerHls"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a323916f82e35a5e9cd6c71d4b925f98a383de121def775f9b389e5ed7fa4714)
                check_type(argname="argument ad_marker_hls", value=ad_marker_hls, expected_type=type_hints["ad_marker_hls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_marker_hls is not None:
                self._values["ad_marker_hls"] = ad_marker_hls

        @builtins.property
        def ad_marker_hls(self) -> typing.Optional[builtins.str]:
            '''The SCTE-35 HLS ad-marker configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-sctehls.html#cfn-mediapackagev2-originendpoint-sctehls-admarkerhls
            '''
            result = self._values.get("ad_marker_hls")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScteHlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.ScteProperty",
        jsii_struct_bases=[],
        name_mapping={"scte_filter": "scteFilter"},
    )
    class ScteProperty:
        def __init__(
            self,
            *,
            scte_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The SCTE-35 configuration associated with the origin endpoint.

            :param scte_filter: The filter associated with the SCTE-35 configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-scte.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                scte_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteProperty(
                    scte_filter=["scteFilter"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__001ae2d35ff90efb73c2d88aa5a33debb02c8e6ecc8862702b61694405fc74c2)
                check_type(argname="argument scte_filter", value=scte_filter, expected_type=type_hints["scte_filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if scte_filter is not None:
                self._values["scte_filter"] = scte_filter

        @builtins.property
        def scte_filter(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The filter associated with the SCTE-35 configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-scte.html#cfn-mediapackagev2-originendpoint-scte-sctefilter
            '''
            result = self._values.get("scte_filter")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.SegmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption": "encryption",
            "include_iframe_only_streams": "includeIframeOnlyStreams",
            "scte": "scte",
            "segment_duration_seconds": "segmentDurationSeconds",
            "segment_name": "segmentName",
            "ts_include_dvb_subtitles": "tsIncludeDvbSubtitles",
            "ts_use_audio_rendition_group": "tsUseAudioRenditionGroup",
        },
    )
    class SegmentProperty:
        def __init__(
            self,
            *,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.EncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            include_iframe_only_streams: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            scte: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.ScteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            segment_name: typing.Optional[builtins.str] = None,
            ts_include_dvb_subtitles: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ts_use_audio_rendition_group: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The segment configuration, including the segment name, duration, and other configuration values.

            :param encryption: Whether to use encryption for the segment.
            :param include_iframe_only_streams: Whether the segment includes I-frame-only streams.
            :param scte: The SCTE-35 configuration associated with the segment.
            :param segment_duration_seconds: The duration of the segment, in seconds.
            :param segment_name: The name of the segment associated with the origin endpoint.
            :param ts_include_dvb_subtitles: Whether the segment includes DVB subtitles.
            :param ts_use_audio_rendition_group: Whether the segment is an audio rendition group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-segment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                segment_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.SegmentProperty(
                    encryption=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionProperty(
                        cmaf_exclude_segment_drm_metadata=False,
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionMethodProperty(
                            cmaf_encryption_method="cmafEncryptionMethod",
                            ism_encryption_method="ismEncryptionMethod",
                            ts_encryption_method="tsEncryptionMethod"
                        ),
                        key_rotation_interval_seconds=123,
                        speke_key_provider=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                            drm_systems=["drmSystems"],
                            encryption_contract_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            ),
                            resource_id="resourceId",
                            role_arn="roleArn",
                            url="url"
                        )
                    ),
                    include_iframe_only_streams=False,
                    scte=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.ScteProperty(
                        scte_filter=["scteFilter"]
                    ),
                    segment_duration_seconds=123,
                    segment_name="segmentName",
                    ts_include_dvb_subtitles=False,
                    ts_use_audio_rendition_group=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__96d917b4effa1a8d6fa5b335396bc814dcecd1668cd845cfdf1778edc3e6a03c)
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument include_iframe_only_streams", value=include_iframe_only_streams, expected_type=type_hints["include_iframe_only_streams"])
                check_type(argname="argument scte", value=scte, expected_type=type_hints["scte"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
                check_type(argname="argument ts_include_dvb_subtitles", value=ts_include_dvb_subtitles, expected_type=type_hints["ts_include_dvb_subtitles"])
                check_type(argname="argument ts_use_audio_rendition_group", value=ts_use_audio_rendition_group, expected_type=type_hints["ts_use_audio_rendition_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption is not None:
                self._values["encryption"] = encryption
            if include_iframe_only_streams is not None:
                self._values["include_iframe_only_streams"] = include_iframe_only_streams
            if scte is not None:
                self._values["scte"] = scte
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if segment_name is not None:
                self._values["segment_name"] = segment_name
            if ts_include_dvb_subtitles is not None:
                self._values["ts_include_dvb_subtitles"] = ts_include_dvb_subtitles
            if ts_use_audio_rendition_group is not None:
                self._values["ts_use_audio_rendition_group"] = ts_use_audio_rendition_group

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.EncryptionProperty"]]:
            '''Whether to use encryption for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-segment.html#cfn-mediapackagev2-originendpoint-segment-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.EncryptionProperty"]], result)

        @builtins.property
        def include_iframe_only_streams(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the segment includes I-frame-only streams.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-segment.html#cfn-mediapackagev2-originendpoint-segment-includeiframeonlystreams
            '''
            result = self._values.get("include_iframe_only_streams")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def scte(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.ScteProperty"]]:
            '''The SCTE-35 configuration associated with the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-segment.html#cfn-mediapackagev2-originendpoint-segment-scte
            '''
            result = self._values.get("scte")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.ScteProperty"]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''The duration of the segment, in seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-segment.html#cfn-mediapackagev2-originendpoint-segment-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the segment associated with the origin endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-segment.html#cfn-mediapackagev2-originendpoint-segment-segmentname
            '''
            result = self._values.get("segment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ts_include_dvb_subtitles(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the segment includes DVB subtitles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-segment.html#cfn-mediapackagev2-originendpoint-segment-tsincludedvbsubtitles
            '''
            result = self._values.get("ts_include_dvb_subtitles")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ts_use_audio_rendition_group(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the segment is an audio rendition group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-segment.html#cfn-mediapackagev2-originendpoint-segment-tsuseaudiorenditiongroup
            '''
            result = self._values.get("ts_use_audio_rendition_group")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "drm_systems": "drmSystems",
            "encryption_contract_configuration": "encryptionContractConfiguration",
            "resource_id": "resourceId",
            "role_arn": "roleArn",
            "url": "url",
        },
    )
    class SpekeKeyProviderProperty:
        def __init__(
            self,
            *,
            drm_systems: typing.Optional[typing.Sequence[builtins.str]] = None,
            encryption_contract_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for the SPEKE key provider.

            :param drm_systems: The DRM solution provider you're using to protect your content during distribution.
            :param encryption_contract_configuration: The encryption contract configuration associated with the SPEKE key provider.
            :param resource_id: The unique identifier for the content. The service sends this identifier to the key server to identify the current endpoint. How unique you make this identifier depends on how fine-grained you want access controls to be. The service does not permit you to use the same ID for two simultaneous encryption processes. The resource ID is also known as the content ID. The following example shows a resource ID: ``MovieNight20171126093045``
            :param role_arn: The ARN for the IAM role granted by the key provider that provides access to the key provider API. This role must have a trust policy that allows MediaPackage to assume the role, and it must have a sufficient permissions policy to allow access to the specific key retrieval URL. Get this from your DRM solution provider. Valid format: ``arn:aws:iam::{accountID}:role/{name}`` . The following example shows a role ARN: ``arn:aws:iam::444455556666:role/SpekeAccess``
            :param url: The URL of the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-spekekeyprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                speke_key_provider_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty(
                    drm_systems=["drmSystems"],
                    encryption_contract_configuration=mediapackagev2_mixins.CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty(
                        preset_speke20_audio="presetSpeke20Audio",
                        preset_speke20_video="presetSpeke20Video"
                    ),
                    resource_id="resourceId",
                    role_arn="roleArn",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa43dbd545fd1336ccdc315a15f0272542e815992691015117ea19c1649adef8)
                check_type(argname="argument drm_systems", value=drm_systems, expected_type=type_hints["drm_systems"])
                check_type(argname="argument encryption_contract_configuration", value=encryption_contract_configuration, expected_type=type_hints["encryption_contract_configuration"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if drm_systems is not None:
                self._values["drm_systems"] = drm_systems
            if encryption_contract_configuration is not None:
                self._values["encryption_contract_configuration"] = encryption_contract_configuration
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def drm_systems(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The DRM solution provider you're using to protect your content during distribution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-spekekeyprovider.html#cfn-mediapackagev2-originendpoint-spekekeyprovider-drmsystems
            '''
            result = self._values.get("drm_systems")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def encryption_contract_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty"]]:
            '''The encryption contract configuration associated with the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-spekekeyprovider.html#cfn-mediapackagev2-originendpoint-spekekeyprovider-encryptioncontractconfiguration
            '''
            result = self._values.get("encryption_contract_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty"]], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the content.

            The service sends this identifier to the key server to identify the current endpoint. How unique you make this identifier depends on how fine-grained you want access controls to be. The service does not permit you to use the same ID for two simultaneous encryption processes. The resource ID is also known as the content ID.

            The following example shows a resource ID: ``MovieNight20171126093045``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-spekekeyprovider.html#cfn-mediapackagev2-originendpoint-spekekeyprovider-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN for the IAM role granted by the key provider that provides access to the key provider API.

            This role must have a trust policy that allows MediaPackage to assume the role, and it must have a sufficient permissions policy to allow access to the specific key retrieval URL. Get this from your DRM solution provider.

            Valid format: ``arn:aws:iam::{accountID}:role/{name}`` . The following example shows a role ARN: ``arn:aws:iam::444455556666:role/SpekeAccess``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-spekekeyprovider.html#cfn-mediapackagev2-originendpoint-spekekeyprovider-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL of the SPEKE key provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-spekekeyprovider.html#cfn-mediapackagev2-originendpoint-spekekeyprovider-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpekeKeyProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackagev2.mixins.CfnOriginEndpointPropsMixin.StartTagProperty",
        jsii_struct_bases=[],
        name_mapping={"precise": "precise", "time_offset": "timeOffset"},
    )
    class StartTagProperty:
        def __init__(
            self,
            *,
            precise: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            time_offset: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''To insert an EXT-X-START tag in your HLS playlist, specify a StartTag configuration object with a valid TimeOffset.

            When you do, you can also optionally specify whether to include a PRECISE value in the EXT-X-START tag.

            :param precise: Specify the value for PRECISE within your EXT-X-START tag. Leave blank, or choose false, to use the default value NO. Choose yes to use the value YES.
            :param time_offset: Specify the value for TIME-OFFSET within your EXT-X-START tag. Enter a signed floating point value which, if positive, must be less than the configured manifest duration minus three times the configured segment target duration. If negative, the absolute value must be larger than three times the configured segment target duration, and the absolute value must be smaller than the configured manifest duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-starttag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediapackagev2 import mixins as mediapackagev2_mixins
                
                start_tag_property = mediapackagev2_mixins.CfnOriginEndpointPropsMixin.StartTagProperty(
                    precise=False,
                    time_offset=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e3b1000120e1ead450e051655bec5eb3ee328a0d9eede8d843678a67b65aae7)
                check_type(argname="argument precise", value=precise, expected_type=type_hints["precise"])
                check_type(argname="argument time_offset", value=time_offset, expected_type=type_hints["time_offset"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if precise is not None:
                self._values["precise"] = precise
            if time_offset is not None:
                self._values["time_offset"] = time_offset

        @builtins.property
        def precise(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify the value for PRECISE within your EXT-X-START tag.

            Leave blank, or choose false, to use the default value NO. Choose yes to use the value YES.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-starttag.html#cfn-mediapackagev2-originendpoint-starttag-precise
            '''
            result = self._values.get("precise")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def time_offset(self) -> typing.Optional[jsii.Number]:
            '''Specify the value for TIME-OFFSET within your EXT-X-START tag.

            Enter a signed floating point value which, if positive, must be less than the configured manifest duration minus three times the configured segment target duration. If negative, the absolute value must be larger than three times the configured segment target duration, and the absolute value must be smaller than the configured manifest duration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackagev2-originendpoint-starttag.html#cfn-mediapackagev2-originendpoint-starttag-timeoffset
            '''
            result = self._values.get("time_offset")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StartTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnChannelGroupEgressAccessLogs",
    "CfnChannelGroupIngressAccessLogs",
    "CfnChannelGroupLogsMixin",
    "CfnChannelGroupMixinProps",
    "CfnChannelGroupPropsMixin",
    "CfnChannelMixinProps",
    "CfnChannelPolicyMixinProps",
    "CfnChannelPolicyPropsMixin",
    "CfnChannelPropsMixin",
    "CfnOriginEndpointMixinProps",
    "CfnOriginEndpointPolicyMixinProps",
    "CfnOriginEndpointPolicyPropsMixin",
    "CfnOriginEndpointPropsMixin",
]

publication.publish()

def _typecheckingstub__696024da3bf568d08005e3641147133c17b2da51832cb4acac82fcd5bae720a5(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b92e944d56a610a0d455ef72b8a50bff2e60ef061c4ad5f0c00e03a8b7bf316(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f61a6e590606f957cc1efc500e3aa79a3b15cad35d7735ef0a54d3f97343ee5(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35378aa91fe75f7be0fc2b133055e0bf5037441cbb9b8d9388966ccaed7fe12d(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640f5546e33e0871f75939fe236d7c2d08969b8c1e5d5cc2d8f1eb6ff222b8df(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4696583a30f96440821b1f840c1b2d5f8f911bb402718799a6be02b6a81d0491(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b966161b6358e8d029275ec64e0c48271684c08346b9b4df34e09ea3e65891bc(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388b2cbf1da1f4af7b079323a407e71471f82ebd06fbdf6de08065bf47dca3c5(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d042100ed9ef842d42eaee767403fb82d0b7ade41884205949a19f4b393dba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e675591417927dcc0a373a80f57a65cf17fad5f7588b2ffb258934b718420f3(
    *,
    channel_group_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d5e0cd366132627dd482843337ba0470c4774cc915cc81b3e4286c12ffe521(
    props: typing.Union[CfnChannelGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3384cfd60e00ce83d638cc5d507bb41bc788cfceacc76aaa444ee089aa70fc1d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada6151db95592497f05115a980b022a93a12b6229c4f0a58bbef3fa0996a363(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b4bc50f853020584976311b8bcf2e3ad8873b6fe82b9aea5a0b862fda807fa(
    *,
    channel_group_name: typing.Optional[builtins.str] = None,
    channel_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    input_switch_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.InputSwitchConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_type: typing.Optional[builtins.str] = None,
    output_header_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.OutputHeaderConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d583866a74455534800f1ab39c5c38072f5d5246ec376c8c7f9ea976979fd0a(
    *,
    channel_group_name: typing.Optional[builtins.str] = None,
    channel_name: typing.Optional[builtins.str] = None,
    policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991ff5e63752909bcc29f5a1d38fa3448a13c6185b168405d941db455275ecf3(
    props: typing.Union[CfnChannelPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f798376c8f14093b95f1bed721ac9e89de4c045324efe064bf839c432df9642(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e9d66c7fdd4ec4868a4286790980a268dd535b36b7d0009b62bb9e8d793273(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4d435acfc17a38503a16f25433a0dc36b9b3bd5d439e0d08e79cc5eae79f42(
    props: typing.Union[CfnChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0037b4c22f70b68e1b81b12adf3d51a80151c8b79a54d6b118258049254d0f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc6dc51effca8437d415a18bf4830212aba35e3722c427aa826d07f22832f38(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426db355924e1d267137718440d51bb36fa83bab6d320ee31d3114c25e8508f4(
    *,
    id: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79667e1ba0957489df64225b4942e4437f5def44b805041f460350af1fc04956(
    *,
    mqcs_input_switching: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    preferred_input: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d008b1ad488eb9e6786baaf58a43b11c91de661bdb7156759a75cfc68413b32f(
    *,
    publish_mqcs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e34374b7953480d3926e99db2e6179beb1cb4bb530c8ddb586c3dd2a193d11b(
    *,
    channel_group_name: typing.Optional[builtins.str] = None,
    channel_name: typing.Optional[builtins.str] = None,
    container_type: typing.Optional[builtins.str] = None,
    dash_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashManifestConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    force_endpoint_error_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.ForceEndpointErrorConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hls_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.HlsManifestConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    low_latency_hls_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.LowLatencyHlsManifestConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    mss_manifests: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.MssManifestConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    origin_endpoint_name: typing.Optional[builtins.str] = None,
    segment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.SegmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    startover_window_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2467be87cb8237515ca5b6104ed3e7a745207d31425881505ad91459b4ba2e80(
    *,
    cdn_auth_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPolicyPropsMixin.CdnAuthConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    channel_group_name: typing.Optional[builtins.str] = None,
    channel_name: typing.Optional[builtins.str] = None,
    origin_endpoint_name: typing.Optional[builtins.str] = None,
    policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481bee070afe98057b619c99d401d46a8f167b379fa59fd0c81ed6ed2a113321(
    props: typing.Union[CfnOriginEndpointPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b91a5289499aae0caa16bce921796b00e88fe57a963063d3fd305abb453846(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e49786037215f13a5775ec76e1bbedcddb650aa929109af9bd46ac8b3100955(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ec8c57153be3063532df5d9e0241218689296bba7a2385fa2031e3ea195646(
    *,
    cdn_identifier_secret_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    secrets_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4126516c3e149c91a30d5049a86dece491b5bdad44d7c272c0d663156cbe93f(
    props: typing.Union[CfnOriginEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7892ff51ad1193b011e169484f66bc169210c9eec01dec65c37e79c3c517b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e9f0a671f9190ca88935736383089d471d93a51a35132794e5aa398b4d7e985(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beab719409ecad40b96d00a01b877f0ac0f0908889f98f4c0750a9744315db88(
    *,
    dvb_priority: typing.Optional[jsii.Number] = None,
    dvb_weight: typing.Optional[jsii.Number] = None,
    service_location: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb8cfefb0cd382dc0271b3e1fc2b5de7eab5cac8c28df55b8e20d9838f13b05(
    *,
    font_family: typing.Optional[builtins.str] = None,
    mime_type: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2133d2d2b35fe2fff50ec1be2a567389625249a5da09bfae1cdfa7584c2298a(
    *,
    probability: typing.Optional[jsii.Number] = None,
    reporting_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd55debb5e0e9878e82c531547def56d48981e21b29d5bb5f244612a6623334c(
    *,
    error_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashDvbMetricsReportingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    font_download: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashDvbFontDownloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0c0c82051d9369b2b9a5131f3ce9edf8a0fec21d18b3aaf1205f72ce80c673(
    *,
    base_urls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashBaseUrlProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compactness: typing.Optional[builtins.str] = None,
    drm_signaling: typing.Optional[builtins.str] = None,
    dvb_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashDvbSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.FilterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    manifest_window_seconds: typing.Optional[jsii.Number] = None,
    min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
    min_update_period_seconds: typing.Optional[jsii.Number] = None,
    period_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
    program_information: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashProgramInformationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scte_dash: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.ScteDashProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    segment_template_format: typing.Optional[builtins.str] = None,
    subtitle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashSubtitleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    suggested_presentation_delay_seconds: typing.Optional[jsii.Number] = None,
    utc_timing: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashUtcTimingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb3dcb46775e00a1a1f0b07a3558648a0d7ddf733741efa5a51b97c2b089840(
    *,
    copyright: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    more_information_url: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa23a6bda26122ab3fa53a219c71a2c2a5042b6317b657322c1b88a1ed10513(
    *,
    ttml_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.DashTtmlConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8e02ac42e26a2449aebdd6c27790886895a44d2b31ba429bda30096abdec31(
    *,
    ttml_profile: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e303344fd691280b0c3d0d31c6f78353b63d3ba7c8ad54680f8fa820c318466f(
    *,
    timing_mode: typing.Optional[builtins.str] = None,
    timing_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ec1c047a7ff8e0cdf626a427c81fb2e93fe27822632f8b15415a16292c0474(
    *,
    preset_speke20_audio: typing.Optional[builtins.str] = None,
    preset_speke20_video: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6031cb0f031776a2f8ab3f2412c73423286d57c89d0f2f057ebc4b9c936e94b(
    *,
    cmaf_encryption_method: typing.Optional[builtins.str] = None,
    ism_encryption_method: typing.Optional[builtins.str] = None,
    ts_encryption_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af418adfd66eecf6bb59f4fa12d495f18db6bd1a7404a36793293487dfe5071(
    *,
    cmaf_exclude_segment_drm_metadata: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    encryption_method: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.EncryptionMethodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
    speke_key_provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1290eaa7d5791f3ea9080910bfc1f75dbd06db2b9d0427336f29940295cef02(
    *,
    clip_start_time: typing.Optional[builtins.str] = None,
    end: typing.Optional[builtins.str] = None,
    manifest_filter: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
    time_delay_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a138aa60f361c8ca6a3410ca59b89cfea0daef749926330643599dacdd94b298(
    *,
    endpoint_error_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a16bb5707710c545bb6f1c1157f10ae97c5effcac7817c459d33b5410ec37fd(
    *,
    child_manifest_name: typing.Optional[builtins.str] = None,
    filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.FilterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    manifest_window_seconds: typing.Optional[jsii.Number] = None,
    program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
    scte_hls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.ScteHlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.StartTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    url: typing.Optional[builtins.str] = None,
    url_encode_child_manifest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602154144ad86bc5ceb2b17ec0187491e1641d88add81c4971aed8745f38eb71(
    *,
    child_manifest_name: typing.Optional[builtins.str] = None,
    filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.FilterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    manifest_window_seconds: typing.Optional[jsii.Number] = None,
    program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
    scte_hls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.ScteHlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.StartTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    url: typing.Optional[builtins.str] = None,
    url_encode_child_manifest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d258999f542e9697f1a8db03483747b7beacc8993e60bc1a8b42a269b680fc67(
    *,
    filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.FilterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    manifest_layout: typing.Optional[builtins.str] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    manifest_window_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069845d8374a5d6fb7771e6099024215591837c8087b9806b162b4c0d75a355e(
    *,
    ad_marker_dash: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a323916f82e35a5e9cd6c71d4b925f98a383de121def775f9b389e5ed7fa4714(
    *,
    ad_marker_hls: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001ae2d35ff90efb73c2d88aa5a33debb02c8e6ecc8862702b61694405fc74c2(
    *,
    scte_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d917b4effa1a8d6fa5b335396bc814dcecd1668cd845cfdf1778edc3e6a03c(
    *,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.EncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_iframe_only_streams: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    scte: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.ScteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    segment_name: typing.Optional[builtins.str] = None,
    ts_include_dvb_subtitles: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ts_use_audio_rendition_group: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa43dbd545fd1336ccdc315a15f0272542e815992691015117ea19c1649adef8(
    *,
    drm_systems: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption_contract_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOriginEndpointPropsMixin.EncryptionContractConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3b1000120e1ead450e051655bec5eb3ee328a0d9eede8d843678a67b65aae7(
    *,
    precise: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    time_offset: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
