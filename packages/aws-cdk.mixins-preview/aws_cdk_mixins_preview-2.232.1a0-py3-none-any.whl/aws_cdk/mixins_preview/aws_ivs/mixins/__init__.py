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
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorized": "authorized",
        "container_format": "containerFormat",
        "insecure_ingest": "insecureIngest",
        "latency_mode": "latencyMode",
        "multitrack_input_configuration": "multitrackInputConfiguration",
        "name": "name",
        "preset": "preset",
        "recording_configuration_arn": "recordingConfigurationArn",
        "tags": "tags",
        "type": "type",
    },
)
class CfnChannelMixinProps:
    def __init__(
        self,
        *,
        authorized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        container_format: typing.Optional[builtins.str] = None,
        insecure_ingest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        latency_mode: typing.Optional[builtins.str] = None,
        multitrack_input_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.MultitrackInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        preset: typing.Optional[builtins.str] = None,
        recording_configuration_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnChannelPropsMixin.

        :param authorized: Whether the channel is authorized. *Default* : ``false`` Default: - false
        :param container_format: Indicates which content-packaging format is used (MPEG-TS or fMP4). If ``multitrackInputConfiguration`` is specified and ``enabled`` is ``true`` , then ``containerFormat`` is required and must be set to ``FRAGMENTED_MP4`` . Otherwise, ``containerFormat`` may be set to ``TS`` or ``FRAGMENTED_MP4`` . Default: ``TS`` . Default: - "TS"
        :param insecure_ingest: Whether the channel allows insecure RTMP ingest. *Default* : ``false`` Default: - false
        :param latency_mode: Channel latency mode. Valid values:. - ``NORMAL`` : Use NORMAL to broadcast and deliver live video up to Full HD. - ``LOW`` : Use LOW for near real-time interactions with viewers. .. epigraph:: In the console, ``LOW`` and ``NORMAL`` correspond to ``Ultra-low`` and ``Standard`` , respectively. *Default* : ``LOW`` Default: - "LOW"
        :param multitrack_input_configuration: Object specifying multitrack input configuration. Default: no multitrack input configuration is specified.
        :param name: Channel name. Default: - "-"
        :param preset: An optional transcode preset for the channel. This is selectable only for ``ADVANCED_HD`` and ``ADVANCED_SD`` channel types. For those channel types, the default preset is ``HIGHER_BANDWIDTH_DELIVERY`` . For other channel types ( ``BASIC`` and ``STANDARD`` ), ``preset`` is the empty string ("").
        :param recording_configuration_arn: The ARN of a RecordingConfiguration resource. An empty string indicates that recording is disabled for the channel. A RecordingConfiguration ARN indicates that recording is enabled using the specified recording configuration. See the `RecordingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html>`_ resource for more information and an example. *Default* : "" (empty string, recording is disabled) Default: - ""
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-channel-tag.html>`_ .
        :param type: The channel type, which determines the allowable resolution and bitrate. *If you exceed the allowable resolution or bitrate, the stream probably will disconnect immediately.* For details, see `Channel Types <https://docs.aws.amazon.com/ivs/latest/LowLatencyAPIReference/channel-types.html>`_ . *Default* : ``STANDARD`` Default: - "STANDARD"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
            
            cfn_channel_mixin_props = ivs_mixins.CfnChannelMixinProps(
                authorized=False,
                container_format="containerFormat",
                insecure_ingest=False,
                latency_mode="latencyMode",
                multitrack_input_configuration=ivs_mixins.CfnChannelPropsMixin.MultitrackInputConfigurationProperty(
                    enabled=False,
                    maximum_resolution="maximumResolution",
                    policy="policy"
                ),
                name="name",
                preset="preset",
                recording_configuration_arn="recordingConfigurationArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb288a205d6b870bd353ff2843a561b6de4c1705f00e238802a91acd0a2b2653)
            check_type(argname="argument authorized", value=authorized, expected_type=type_hints["authorized"])
            check_type(argname="argument container_format", value=container_format, expected_type=type_hints["container_format"])
            check_type(argname="argument insecure_ingest", value=insecure_ingest, expected_type=type_hints["insecure_ingest"])
            check_type(argname="argument latency_mode", value=latency_mode, expected_type=type_hints["latency_mode"])
            check_type(argname="argument multitrack_input_configuration", value=multitrack_input_configuration, expected_type=type_hints["multitrack_input_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
            check_type(argname="argument recording_configuration_arn", value=recording_configuration_arn, expected_type=type_hints["recording_configuration_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorized is not None:
            self._values["authorized"] = authorized
        if container_format is not None:
            self._values["container_format"] = container_format
        if insecure_ingest is not None:
            self._values["insecure_ingest"] = insecure_ingest
        if latency_mode is not None:
            self._values["latency_mode"] = latency_mode
        if multitrack_input_configuration is not None:
            self._values["multitrack_input_configuration"] = multitrack_input_configuration
        if name is not None:
            self._values["name"] = name
        if preset is not None:
            self._values["preset"] = preset
        if recording_configuration_arn is not None:
            self._values["recording_configuration_arn"] = recording_configuration_arn
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def authorized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether the channel is authorized.

        *Default* : ``false``

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-authorized
        '''
        result = self._values.get("authorized")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def container_format(self) -> typing.Optional[builtins.str]:
        '''Indicates which content-packaging format is used (MPEG-TS or fMP4).

        If ``multitrackInputConfiguration`` is specified and ``enabled`` is ``true`` , then ``containerFormat`` is required and must be set to ``FRAGMENTED_MP4`` . Otherwise, ``containerFormat`` may be set to ``TS`` or ``FRAGMENTED_MP4`` . Default: ``TS`` .

        :default: - "TS"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-containerformat
        '''
        result = self._values.get("container_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_ingest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether the channel allows insecure RTMP ingest.

        *Default* : ``false``

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-insecureingest
        '''
        result = self._values.get("insecure_ingest")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def latency_mode(self) -> typing.Optional[builtins.str]:
        '''Channel latency mode. Valid values:.

        - ``NORMAL`` : Use NORMAL to broadcast and deliver live video up to Full HD.
        - ``LOW`` : Use LOW for near real-time interactions with viewers.

        .. epigraph::

           In the  console, ``LOW`` and ``NORMAL`` correspond to ``Ultra-low`` and ``Standard`` , respectively.

        *Default* : ``LOW``

        :default: - "LOW"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-latencymode
        '''
        result = self._values.get("latency_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multitrack_input_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.MultitrackInputConfigurationProperty"]]:
        '''Object specifying multitrack input configuration.

        Default: no multitrack input configuration is specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-multitrackinputconfiguration
        '''
        result = self._values.get("multitrack_input_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.MultitrackInputConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Channel name.

        :default: - "-"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preset(self) -> typing.Optional[builtins.str]:
        '''An optional transcode preset for the channel.

        This is selectable only for ``ADVANCED_HD`` and ``ADVANCED_SD`` channel types. For those channel types, the default preset is ``HIGHER_BANDWIDTH_DELIVERY`` . For other channel types ( ``BASIC`` and ``STANDARD`` ), ``preset`` is the empty string ("").

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-preset
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recording_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of a RecordingConfiguration resource.

        An empty string indicates that recording is disabled for the channel. A RecordingConfiguration ARN indicates that recording is enabled using the specified recording configuration. See the `RecordingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html>`_ resource for more information and an example.

        *Default* : "" (empty string, recording is disabled)

        :default: - ""

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-recordingconfigurationarn
        '''
        result = self._values.get("recording_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-channel-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The channel type, which determines the allowable resolution and bitrate.

        *If you exceed the allowable resolution or bitrate, the stream probably will disconnect immediately.* For details, see `Channel Types <https://docs.aws.amazon.com/ivs/latest/LowLatencyAPIReference/channel-types.html>`_ .

        *Default* : ``STANDARD``

        :default: - "STANDARD"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnChannelPropsMixin",
):
    '''The ``AWS::IVS::Channel`` resource specifies an  channel.

    A channel stores configuration information related to your live stream. For more information, see `CreateChannel <https://docs.aws.amazon.com/ivs/latest/LowLatencyAPIReference/API_CreateChannel.html>`_ in the *Amazon IVS Low-Latency Streaming API Reference* .
    .. epigraph::

       By default, the IVS API CreateChannel endpoint creates a stream key in addition to a channel. The  Channel resource *does not* create a stream key; to create a stream key, use the StreamKey resource instead.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html
    :cloudformationResource: AWS::IVS::Channel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
        
        cfn_channel_props_mixin = ivs_mixins.CfnChannelPropsMixin(ivs_mixins.CfnChannelMixinProps(
            authorized=False,
            container_format="containerFormat",
            insecure_ingest=False,
            latency_mode="latencyMode",
            multitrack_input_configuration=ivs_mixins.CfnChannelPropsMixin.MultitrackInputConfigurationProperty(
                enabled=False,
                maximum_resolution="maximumResolution",
                policy="policy"
            ),
            name="name",
            preset="preset",
            recording_configuration_arn="recordingConfigurationArn",
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
        props: typing.Union[CfnChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVS::Channel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f002787fcf1844145f12b0f02ad68ae1f3d191fa3f1aecb772b3dac913e6f99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e29775cbf9bcad1d9cc5dd618fa2adf510848f55d0a33455c389d3df7f7c70ba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4ded844637d178f24d55d7d3f5410ba592ddaea67313ae196d29a10af04dc2)
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
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnChannelPropsMixin.MultitrackInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "maximum_resolution": "maximumResolution",
            "policy": "policy",
        },
    )
    class MultitrackInputConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            maximum_resolution: typing.Optional[builtins.str] = None,
            policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that specifies multitrack input configuration.

            :param enabled: Indicates whether multitrack input is enabled. Can be set to ``true`` only if channel type is ``STANDARD`` . Setting ``enabled`` to ``true`` with any other channel type will cause an exception. If ``true`` , then ``policy`` , ``maximumResolution`` , and ``containerFormat`` are required, and ``containerFormat`` must be set to ``FRAGMENTED_MP4`` . Default: ``false`` . Default: - false
            :param maximum_resolution: Maximum resolution for multitrack input. Required if ``enabled`` is ``true`` .
            :param policy: Indicates whether multitrack input is allowed or required. Required if ``enabled`` is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-channel-multitrackinputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                multitrack_input_configuration_property = ivs_mixins.CfnChannelPropsMixin.MultitrackInputConfigurationProperty(
                    enabled=False,
                    maximum_resolution="maximumResolution",
                    policy="policy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2c0d3ed8dd0658ce18af59be010168ecef0e4805fd3bcaf49435f4cfd37ee11)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument maximum_resolution", value=maximum_resolution, expected_type=type_hints["maximum_resolution"])
                check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if maximum_resolution is not None:
                self._values["maximum_resolution"] = maximum_resolution
            if policy is not None:
                self._values["policy"] = policy

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether multitrack input is enabled.

            Can be set to ``true`` only if channel type is ``STANDARD`` . Setting ``enabled`` to ``true`` with any other channel type will cause an exception. If ``true`` , then ``policy`` , ``maximumResolution`` , and ``containerFormat`` are required, and ``containerFormat`` must be set to ``FRAGMENTED_MP4`` . Default: ``false`` .

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-channel-multitrackinputconfiguration.html#cfn-ivs-channel-multitrackinputconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def maximum_resolution(self) -> typing.Optional[builtins.str]:
            '''Maximum resolution for multitrack input.

            Required if ``enabled`` is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-channel-multitrackinputconfiguration.html#cfn-ivs-channel-multitrackinputconfiguration-maximumresolution
            '''
            result = self._values.get("maximum_resolution")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy(self) -> typing.Optional[builtins.str]:
            '''Indicates whether multitrack input is allowed or required.

            Required if ``enabled`` is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-channel-multitrackinputconfiguration.html#cfn-ivs-channel-multitrackinputconfiguration-policy
            '''
            result = self._values.get("policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultitrackInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnEncoderConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags", "video": "video"},
)
class CfnEncoderConfigurationMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        video: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEncoderConfigurationPropsMixin.VideoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEncoderConfigurationPropsMixin.

        :param name: Encoder cnfiguration name.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-encoderconfiguration-tag.html>`_ .
        :param video: Video configuration. Default: video resolution 1280x720, bitrate 2500 kbps, 30 fps. See the `Video <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-encoderconfiguration-video.html>`_ property type for more information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-encoderconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
            
            cfn_encoder_configuration_mixin_props = ivs_mixins.CfnEncoderConfigurationMixinProps(
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                video=ivs_mixins.CfnEncoderConfigurationPropsMixin.VideoProperty(
                    bitrate=123,
                    framerate=123,
                    height=123,
                    width=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b0fd21c6c7a2f4d9f3da423c8ed9cc22c24dd74f88345e958ba5526ad4f116c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument video", value=video, expected_type=type_hints["video"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if video is not None:
            self._values["video"] = video

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Encoder cnfiguration name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-encoderconfiguration.html#cfn-ivs-encoderconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-encoderconfiguration-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-encoderconfiguration.html#cfn-ivs-encoderconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def video(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEncoderConfigurationPropsMixin.VideoProperty"]]:
        '''Video configuration.

        Default: video resolution 1280x720, bitrate 2500 kbps, 30 fps. See the `Video <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-encoderconfiguration-video.html>`_ property type for more information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-encoderconfiguration.html#cfn-ivs-encoderconfiguration-video
        '''
        result = self._values.get("video")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEncoderConfigurationPropsMixin.VideoProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEncoderConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEncoderConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnEncoderConfigurationPropsMixin",
):
    '''The ``AWS::IVS::EncoderConfiguration`` resource specifies an  encoder configuration.

    An encoder configuration describes a stream’s video configuration. For more information, see `Streaming Configuration <https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/streaming-config.html>`_ in the *Amazon IVS Low-Latency Streaming User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-encoderconfiguration.html
    :cloudformationResource: AWS::IVS::EncoderConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
        
        cfn_encoder_configuration_props_mixin = ivs_mixins.CfnEncoderConfigurationPropsMixin(ivs_mixins.CfnEncoderConfigurationMixinProps(
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            video=ivs_mixins.CfnEncoderConfigurationPropsMixin.VideoProperty(
                bitrate=123,
                framerate=123,
                height=123,
                width=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEncoderConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVS::EncoderConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef92066b01c2eb9e4ce2ebb736da338bc2709fe82bfc8484693855e4e813430)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c649b61b4217cac708c5446eb9ecaa8ab83853615dc8fcdc340e2a468f9bb113)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562f6aa4a27e8257aeab66ae2db16ddd87c1341d7e4f80a14dde2515ab31833d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEncoderConfigurationMixinProps:
        return typing.cast(CfnEncoderConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnEncoderConfigurationPropsMixin.VideoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bitrate": "bitrate",
            "framerate": "framerate",
            "height": "height",
            "width": "width",
        },
    )
    class VideoProperty:
        def __init__(
            self,
            *,
            bitrate: typing.Optional[jsii.Number] = None,
            framerate: typing.Optional[jsii.Number] = None,
            height: typing.Optional[jsii.Number] = None,
            width: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The Video property type describes a stream's video configuration.

            :param bitrate: Bitrate for generated output, in bps. Default: 2500000. Default: - 2500000
            :param framerate: Video frame rate, in fps. Default: 30. Default: - 30
            :param height: Video-resolution height. Note that the maximum value is determined by width times height, such that the maximum total pixels is 2073600 (1920x1080 or 1080x1920). Default: 720. Default: - 720
            :param width: Video-resolution width. Note that the maximum value is determined by width times height, such that the maximum total pixels is 2073600 (1920x1080 or 1080x1920). Default: 1280. Default: - 1280

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-encoderconfiguration-video.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                video_property = ivs_mixins.CfnEncoderConfigurationPropsMixin.VideoProperty(
                    bitrate=123,
                    framerate=123,
                    height=123,
                    width=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8ddd263df1cc3d436bdfee93ceea3d23b1f11e51af4724ce841de269fa41c9b)
                check_type(argname="argument bitrate", value=bitrate, expected_type=type_hints["bitrate"])
                check_type(argname="argument framerate", value=framerate, expected_type=type_hints["framerate"])
                check_type(argname="argument height", value=height, expected_type=type_hints["height"])
                check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bitrate is not None:
                self._values["bitrate"] = bitrate
            if framerate is not None:
                self._values["framerate"] = framerate
            if height is not None:
                self._values["height"] = height
            if width is not None:
                self._values["width"] = width

        @builtins.property
        def bitrate(self) -> typing.Optional[jsii.Number]:
            '''Bitrate for generated output, in bps.

            Default: 2500000.

            :default: - 2500000

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-encoderconfiguration-video.html#cfn-ivs-encoderconfiguration-video-bitrate
            '''
            result = self._values.get("bitrate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def framerate(self) -> typing.Optional[jsii.Number]:
            '''Video frame rate, in fps.

            Default: 30.

            :default: - 30

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-encoderconfiguration-video.html#cfn-ivs-encoderconfiguration-video-framerate
            '''
            result = self._values.get("framerate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def height(self) -> typing.Optional[jsii.Number]:
            '''Video-resolution height.

            Note that the maximum value is determined by width times height, such that the maximum total pixels is 2073600 (1920x1080 or 1080x1920). Default: 720.

            :default: - 720

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-encoderconfiguration-video.html#cfn-ivs-encoderconfiguration-video-height
            '''
            result = self._values.get("height")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def width(self) -> typing.Optional[jsii.Number]:
            '''Video-resolution width.

            Note that the maximum value is determined by width times height, such that the maximum total pixels is 2073600 (1920x1080 or 1080x1920). Default: 1280.

            :default: - 1280

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-encoderconfiguration-video.html#cfn-ivs-encoderconfiguration-video-width
            '''
            result = self._values.get("width")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VideoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnIngestConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ingest_protocol": "ingestProtocol",
        "insecure_ingest": "insecureIngest",
        "name": "name",
        "stage_arn": "stageArn",
        "tags": "tags",
        "user_id": "userId",
    },
)
class CfnIngestConfigurationMixinProps:
    def __init__(
        self,
        *,
        ingest_protocol: typing.Optional[builtins.str] = None,
        insecure_ingest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        stage_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIngestConfigurationPropsMixin.

        :param ingest_protocol: Type of ingest protocol that the user employs for broadcasting. Default: - "RTMPS"
        :param insecure_ingest: Whether the channel allows insecure RTMP ingest. Default: ``false`` . Default: - false
        :param name: Ingest name. Default: - "-"
        :param stage_arn: ARN of the stage with which the IngestConfiguration is associated. Default: - ""
        :param tags: An array of key-value pairs to apply to this resource.
        :param user_id: Customer-assigned name to help identify the participant using the IngestConfiguration; this can be used to link a participant to a user in the customer’s own systems. This can be any UTF-8 encoded text. *This field is exposed to all stage participants and should not be used for personally identifying, confidential, or sensitive information.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-ingestconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
            
            cfn_ingest_configuration_mixin_props = ivs_mixins.CfnIngestConfigurationMixinProps(
                ingest_protocol="ingestProtocol",
                insecure_ingest=False,
                name="name",
                stage_arn="stageArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_id="userId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14bf9162144d285d1b872b97a31f3ddf8cf0b4155b1f6cc76a8089358e558ba0)
            check_type(argname="argument ingest_protocol", value=ingest_protocol, expected_type=type_hints["ingest_protocol"])
            check_type(argname="argument insecure_ingest", value=insecure_ingest, expected_type=type_hints["insecure_ingest"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stage_arn", value=stage_arn, expected_type=type_hints["stage_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ingest_protocol is not None:
            self._values["ingest_protocol"] = ingest_protocol
        if insecure_ingest is not None:
            self._values["insecure_ingest"] = insecure_ingest
        if name is not None:
            self._values["name"] = name
        if stage_arn is not None:
            self._values["stage_arn"] = stage_arn
        if tags is not None:
            self._values["tags"] = tags
        if user_id is not None:
            self._values["user_id"] = user_id

    @builtins.property
    def ingest_protocol(self) -> typing.Optional[builtins.str]:
        '''Type of ingest protocol that the user employs for broadcasting.

        :default: - "RTMPS"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-ingestconfiguration.html#cfn-ivs-ingestconfiguration-ingestprotocol
        '''
        result = self._values.get("ingest_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_ingest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether the channel allows insecure RTMP ingest.

        Default: ``false`` .

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-ingestconfiguration.html#cfn-ivs-ingestconfiguration-insecureingest
        '''
        result = self._values.get("insecure_ingest")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Ingest name.

        :default: - "-"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-ingestconfiguration.html#cfn-ivs-ingestconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_arn(self) -> typing.Optional[builtins.str]:
        '''ARN of the stage with which the IngestConfiguration is associated.

        :default: - ""

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-ingestconfiguration.html#cfn-ivs-ingestconfiguration-stagearn
        '''
        result = self._values.get("stage_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-ingestconfiguration.html#cfn-ivs-ingestconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''Customer-assigned name to help identify the participant using the IngestConfiguration;

        this can be used to link a participant to a user in the customer’s own systems. This can be any UTF-8 encoded text. *This field is exposed to all stage participants and should not be used for personally identifying, confidential, or sensitive information.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-ingestconfiguration.html#cfn-ivs-ingestconfiguration-userid
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIngestConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIngestConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnIngestConfigurationPropsMixin",
):
    '''The ``AWS::IVS::IngestConfiguration`` resource specifies an ingest protocol to be used for a stage.

    For more information, see `Stream Ingest <https://docs.aws.amazon.com/ivs/latest/RealTimeUserGuide/rt-stream-ingest.html>`_ in the *Amazon IVS Real-Time Streaming User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-ingestconfiguration.html
    :cloudformationResource: AWS::IVS::IngestConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
        
        cfn_ingest_configuration_props_mixin = ivs_mixins.CfnIngestConfigurationPropsMixin(ivs_mixins.CfnIngestConfigurationMixinProps(
            ingest_protocol="ingestProtocol",
            insecure_ingest=False,
            name="name",
            stage_arn="stageArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_id="userId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIngestConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVS::IngestConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1908e018b38045146b9a4f92af1532c05ee5f97c533e81479297c2b6159948)
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
            type_hints = typing.get_type_hints(_typecheckingstub__779463aa659da184e9f5e392160dadca06c76e42ddd1dca37cb848faed0a769c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c488a6526e89d2719a3b94989f834fda513a03728f5bd3c82eb716177651b9f0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIngestConfigurationMixinProps:
        return typing.cast(CfnIngestConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnPlaybackKeyPairMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "public_key_material": "publicKeyMaterial",
        "tags": "tags",
    },
)
class CfnPlaybackKeyPairMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        public_key_material: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPlaybackKeyPairPropsMixin.

        :param name: Playback-key-pair name. The value does not need to be unique.
        :param public_key_material: The public portion of a customer-generated key pair. Note that this field is required to create the AWS::IVS::PlaybackKeyPair resource.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-playbackkeypair-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
            
            cfn_playback_key_pair_mixin_props = ivs_mixins.CfnPlaybackKeyPairMixinProps(
                name="name",
                public_key_material="publicKeyMaterial",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ccac3562d547e4f85efb8e6228094cb51f3b298dc27219cd52127005822646a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument public_key_material", value=public_key_material, expected_type=type_hints["public_key_material"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if public_key_material is not None:
            self._values["public_key_material"] = public_key_material
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Playback-key-pair name.

        The value does not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key_material(self) -> typing.Optional[builtins.str]:
        '''The public portion of a customer-generated key pair.

        Note that this field is required to create the AWS::IVS::PlaybackKeyPair resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-publickeymaterial
        '''
        result = self._values.get("public_key_material")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-playbackkeypair-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlaybackKeyPairMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPlaybackKeyPairPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnPlaybackKeyPairPropsMixin",
):
    '''The ``AWS::IVS::PlaybackKeyPair`` resource specifies an  playback key pair.

    uses a public playback key to validate playback tokens that have been signed with the corresponding private key. For more information, see `Setting Up Private Channels <https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/private-channels.html>`_ in the *Amazon IVS Low-Latency Streaming User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html
    :cloudformationResource: AWS::IVS::PlaybackKeyPair
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
        
        cfn_playback_key_pair_props_mixin = ivs_mixins.CfnPlaybackKeyPairPropsMixin(ivs_mixins.CfnPlaybackKeyPairMixinProps(
            name="name",
            public_key_material="publicKeyMaterial",
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
        props: typing.Union[CfnPlaybackKeyPairMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVS::PlaybackKeyPair``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2511dab19dd0d0230a311d8547ac2b3fe94d53d5bfb03e6142718d97eded8586)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdfa2ff0a6223f24af43258fbf848b554fe3ec64fe05391d0fe04dfd2e1f08f8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46672831e48de4ffbfc5d82945c27f2872875cac032e5a323d74e9fe570c4216)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPlaybackKeyPairMixinProps:
        return typing.cast(CfnPlaybackKeyPairMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnPlaybackRestrictionPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_countries": "allowedCountries",
        "allowed_origins": "allowedOrigins",
        "enable_strict_origin_enforcement": "enableStrictOriginEnforcement",
        "name": "name",
        "tags": "tags",
    },
)
class CfnPlaybackRestrictionPolicyMixinProps:
    def __init__(
        self,
        *,
        allowed_countries: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_strict_origin_enforcement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPlaybackRestrictionPolicyPropsMixin.

        :param allowed_countries: A list of country codes that control geoblocking restrictions. Allowed values are the officially assigned ISO 3166-1 alpha-2 codes. Default: All countries (an empty array).
        :param allowed_origins: A list of origin sites that control CORS restriction. Allowed values are the same as valid values of the Origin header defined at `https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin" <https://docs.aws.amazon.com/https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin>`_
        :param enable_strict_origin_enforcement: Whether channel playback is constrained by the origin site. Default: - false
        :param name: Playback-restriction-policy name.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-playbackrestrictionpolicy-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackrestrictionpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
            
            cfn_playback_restriction_policy_mixin_props = ivs_mixins.CfnPlaybackRestrictionPolicyMixinProps(
                allowed_countries=["allowedCountries"],
                allowed_origins=["allowedOrigins"],
                enable_strict_origin_enforcement=False,
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23cf58f3689b7b82d19ee2a733f3cc4aae66f4a317e8a39d87e2477ffaf3b3fb)
            check_type(argname="argument allowed_countries", value=allowed_countries, expected_type=type_hints["allowed_countries"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument enable_strict_origin_enforcement", value=enable_strict_origin_enforcement, expected_type=type_hints["enable_strict_origin_enforcement"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_countries is not None:
            self._values["allowed_countries"] = allowed_countries
        if allowed_origins is not None:
            self._values["allowed_origins"] = allowed_origins
        if enable_strict_origin_enforcement is not None:
            self._values["enable_strict_origin_enforcement"] = enable_strict_origin_enforcement
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allowed_countries(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of country codes that control geoblocking restrictions.

        Allowed values are the officially assigned ISO 3166-1 alpha-2 codes. Default: All countries (an empty array).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackrestrictionpolicy.html#cfn-ivs-playbackrestrictionpolicy-allowedcountries
        '''
        result = self._values.get("allowed_countries")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of origin sites that control CORS restriction.

        Allowed values are the same as valid values of the Origin header defined at `https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin" <https://docs.aws.amazon.com/https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackrestrictionpolicy.html#cfn-ivs-playbackrestrictionpolicy-allowedorigins
        '''
        result = self._values.get("allowed_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_strict_origin_enforcement(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether channel playback is constrained by the origin site.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackrestrictionpolicy.html#cfn-ivs-playbackrestrictionpolicy-enablestrictoriginenforcement
        '''
        result = self._values.get("enable_strict_origin_enforcement")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Playback-restriction-policy name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackrestrictionpolicy.html#cfn-ivs-playbackrestrictionpolicy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-playbackrestrictionpolicy-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackrestrictionpolicy.html#cfn-ivs-playbackrestrictionpolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlaybackRestrictionPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPlaybackRestrictionPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnPlaybackRestrictionPolicyPropsMixin",
):
    '''The ``AWS::IVS::PlaybackRestrictionPolicy`` resource specifies an  playback restriction policy.

    A playback restriction policy constrains playback by country and/or origin sites. For more information, see `Undesired Content and Viewers <https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/undesired-content.html>`_ in the *Amazon IVS Low-Latency Streaming User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackrestrictionpolicy.html
    :cloudformationResource: AWS::IVS::PlaybackRestrictionPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
        
        cfn_playback_restriction_policy_props_mixin = ivs_mixins.CfnPlaybackRestrictionPolicyPropsMixin(ivs_mixins.CfnPlaybackRestrictionPolicyMixinProps(
            allowed_countries=["allowedCountries"],
            allowed_origins=["allowedOrigins"],
            enable_strict_origin_enforcement=False,
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
        props: typing.Union[CfnPlaybackRestrictionPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVS::PlaybackRestrictionPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b71ee2fde21ec6f2994a127a1ed64d53c3017b16f645e1d0b82ca297e89103ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee98fc8b0886205e85e29e29904234be9887b821cfbc4c695c0d6704f0b00921)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef710d5f8996007a66967eca6740693ce73287d96a9cb8eb51d3ddc0b0403e2e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPlaybackRestrictionPolicyMixinProps:
        return typing.cast(CfnPlaybackRestrictionPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnPublicKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "public_key_material": "publicKeyMaterial",
        "tags": "tags",
    },
)
class CfnPublicKeyMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        public_key_material: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPublicKeyPropsMixin.

        :param name: Public key name. The value does not need to be unique.
        :param public_key_material: The public portion of a customer-generated key pair. Note that this field is required to create the AWS::IVS::PublicKey resource.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-publickey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
            
            cfn_public_key_mixin_props = ivs_mixins.CfnPublicKeyMixinProps(
                name="name",
                public_key_material="publicKeyMaterial",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9292aa3b99825f60d95a59be3809a1696b1aaf8317dae24041b066493a189e88)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument public_key_material", value=public_key_material, expected_type=type_hints["public_key_material"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if public_key_material is not None:
            self._values["public_key_material"] = public_key_material
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Public key name.

        The value does not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-publickey.html#cfn-ivs-publickey-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key_material(self) -> typing.Optional[builtins.str]:
        '''The public portion of a customer-generated key pair.

        Note that this field is required to create the AWS::IVS::PublicKey resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-publickey.html#cfn-ivs-publickey-publickeymaterial
        '''
        result = self._values.get("public_key_material")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-publickey.html#cfn-ivs-publickey-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublicKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPublicKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnPublicKeyPropsMixin",
):
    '''The ``AWS::IVS::PublicKey`` resource specifies an Amazon IVS public key used to sign stage participant tokens.

    For more information, see `Distribute Participant Tokens <https://docs.aws.amazon.com/ivs/latest/RealTimeUserGuide/getting-started-distribute-tokens.html>`_ in the *Amazon IVS Real-Time Streaming User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-publickey.html
    :cloudformationResource: AWS::IVS::PublicKey
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
        
        cfn_public_key_props_mixin = ivs_mixins.CfnPublicKeyPropsMixin(ivs_mixins.CfnPublicKeyMixinProps(
            name="name",
            public_key_material="publicKeyMaterial",
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
        props: typing.Union[CfnPublicKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVS::PublicKey``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac14b93b241227a2968e677754a327f39d0536c20b2cab1b859799bd4622f227)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3f39d3519361ec90d61f3dc12ffcade768fd883b592af7957c7d89d253a37a8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b08ee31de0c11c2e068806af80bcad79c3b6160e0fad47ab827d0691a0aaf83)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPublicKeyMixinProps:
        return typing.cast(CfnPublicKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnRecordingConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_configuration": "destinationConfiguration",
        "name": "name",
        "recording_reconnect_window_seconds": "recordingReconnectWindowSeconds",
        "rendition_configuration": "renditionConfiguration",
        "tags": "tags",
        "thumbnail_configuration": "thumbnailConfiguration",
    },
)
class CfnRecordingConfigurationMixinProps:
    def __init__(
        self,
        *,
        destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordingConfigurationPropsMixin.DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        recording_reconnect_window_seconds: typing.Optional[jsii.Number] = None,
        rendition_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordingConfigurationPropsMixin.RenditionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        thumbnail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordingConfigurationPropsMixin.ThumbnailConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRecordingConfigurationPropsMixin.

        :param destination_configuration: A destination configuration describes an S3 bucket where recorded video will be stored. See the DestinationConfiguration property type for more information.
        :param name: Recording-configuration name. The value does not need to be unique.
        :param recording_reconnect_window_seconds: If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together. *Default* : ``0`` Default: - 0
        :param rendition_configuration: A rendition configuration describes which renditions should be recorded for a stream. See the RenditionConfiguration property type for more information.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-tag.html>`_ .
        :param thumbnail_configuration: A thumbnail configuration enables/disables the recording of thumbnails for a live session and controls the interval at which thumbnails are generated for the live session. See the ThumbnailConfiguration property type for more information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
            
            cfn_recording_configuration_mixin_props = ivs_mixins.CfnRecordingConfigurationMixinProps(
                destination_configuration=ivs_mixins.CfnRecordingConfigurationPropsMixin.DestinationConfigurationProperty(
                    s3=ivs_mixins.CfnRecordingConfigurationPropsMixin.S3DestinationConfigurationProperty(
                        bucket_name="bucketName"
                    )
                ),
                name="name",
                recording_reconnect_window_seconds=123,
                rendition_configuration=ivs_mixins.CfnRecordingConfigurationPropsMixin.RenditionConfigurationProperty(
                    renditions=["renditions"],
                    rendition_selection="renditionSelection"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                thumbnail_configuration=ivs_mixins.CfnRecordingConfigurationPropsMixin.ThumbnailConfigurationProperty(
                    recording_mode="recordingMode",
                    resolution="resolution",
                    storage=["storage"],
                    target_interval_seconds=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d402fdc1696a7df42b8e7f0f9e57876bbaa2adf96a74f47c6dfd7fdbce4b7bb)
            check_type(argname="argument destination_configuration", value=destination_configuration, expected_type=type_hints["destination_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recording_reconnect_window_seconds", value=recording_reconnect_window_seconds, expected_type=type_hints["recording_reconnect_window_seconds"])
            check_type(argname="argument rendition_configuration", value=rendition_configuration, expected_type=type_hints["rendition_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument thumbnail_configuration", value=thumbnail_configuration, expected_type=type_hints["thumbnail_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_configuration is not None:
            self._values["destination_configuration"] = destination_configuration
        if name is not None:
            self._values["name"] = name
        if recording_reconnect_window_seconds is not None:
            self._values["recording_reconnect_window_seconds"] = recording_reconnect_window_seconds
        if rendition_configuration is not None:
            self._values["rendition_configuration"] = rendition_configuration
        if tags is not None:
            self._values["tags"] = tags
        if thumbnail_configuration is not None:
            self._values["thumbnail_configuration"] = thumbnail_configuration

    @builtins.property
    def destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordingConfigurationPropsMixin.DestinationConfigurationProperty"]]:
        '''A destination configuration describes an S3 bucket where recorded video will be stored.

        See the DestinationConfiguration property type for more information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-destinationconfiguration
        '''
        result = self._values.get("destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordingConfigurationPropsMixin.DestinationConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Recording-configuration name.

        The value does not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recording_reconnect_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together.

        *Default* : ``0``

        :default: - 0

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-recordingreconnectwindowseconds
        '''
        result = self._values.get("recording_reconnect_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rendition_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordingConfigurationPropsMixin.RenditionConfigurationProperty"]]:
        '''A rendition configuration describes which renditions should be recorded for a stream.

        See the RenditionConfiguration property type for more information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-renditionconfiguration
        '''
        result = self._values.get("rendition_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordingConfigurationPropsMixin.RenditionConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def thumbnail_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordingConfigurationPropsMixin.ThumbnailConfigurationProperty"]]:
        '''A thumbnail configuration enables/disables the recording of thumbnails for a live session and controls the interval at which thumbnails are generated for the live session.

        See the ThumbnailConfiguration property type for more information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration
        '''
        result = self._values.get("thumbnail_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordingConfigurationPropsMixin.ThumbnailConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRecordingConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRecordingConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnRecordingConfigurationPropsMixin",
):
    '''The ``AWS::IVS::RecordingConfiguration`` resource specifies an  recording configuration.

    A recording configuration enables the recording of a channel’s live streams to a data store. Multiple channels can reference the same recording configuration. For more information, see `RecordingConfiguration <https://docs.aws.amazon.com/ivs/latest/LowLatencyAPIReference/API_RecordingConfiguration.html>`_ in the *Amazon IVS Low-Latency Streaming API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html
    :cloudformationResource: AWS::IVS::RecordingConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
        
        cfn_recording_configuration_props_mixin = ivs_mixins.CfnRecordingConfigurationPropsMixin(ivs_mixins.CfnRecordingConfigurationMixinProps(
            destination_configuration=ivs_mixins.CfnRecordingConfigurationPropsMixin.DestinationConfigurationProperty(
                s3=ivs_mixins.CfnRecordingConfigurationPropsMixin.S3DestinationConfigurationProperty(
                    bucket_name="bucketName"
                )
            ),
            name="name",
            recording_reconnect_window_seconds=123,
            rendition_configuration=ivs_mixins.CfnRecordingConfigurationPropsMixin.RenditionConfigurationProperty(
                renditions=["renditions"],
                rendition_selection="renditionSelection"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            thumbnail_configuration=ivs_mixins.CfnRecordingConfigurationPropsMixin.ThumbnailConfigurationProperty(
                recording_mode="recordingMode",
                resolution="resolution",
                storage=["storage"],
                target_interval_seconds=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRecordingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVS::RecordingConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb85a5b540c63b05986d02fa1d3058d2b0ed6355b724d7a2dd55bf33fee7389)
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
            type_hints = typing.get_type_hints(_typecheckingstub__382c462de7281cfad3825065a63d5ee62a7e595688a2bbbe6cbe48718f05445f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b83983aa8e010fe27a47a95a25adcc123469bee815aef438804aefd5f8a0e5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRecordingConfigurationMixinProps:
        return typing.cast(CfnRecordingConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnRecordingConfigurationPropsMixin.DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordingConfigurationPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The DestinationConfiguration property type describes the location where recorded videos will be stored.

            Each member represents a type of destination configuration. For recording, you define one and only one type of destination configuration.

            :param s3: An S3 destination configuration where recorded videos will be stored. See the `S3DestinationConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-s3destinationconfiguration.html>`_ property type for more information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                destination_configuration_property = ivs_mixins.CfnRecordingConfigurationPropsMixin.DestinationConfigurationProperty(
                    s3=ivs_mixins.CfnRecordingConfigurationPropsMixin.S3DestinationConfigurationProperty(
                        bucket_name="bucketName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__030921f545f69ea68f6ad6f4493e3331f8f097f636b012b71be4d92cad44f8b3)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordingConfigurationPropsMixin.S3DestinationConfigurationProperty"]]:
            '''An S3 destination configuration where recorded videos will be stored.

            See the `S3DestinationConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-s3destinationconfiguration.html>`_ property type for more information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-destinationconfiguration.html#cfn-ivs-recordingconfiguration-destinationconfiguration-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordingConfigurationPropsMixin.S3DestinationConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnRecordingConfigurationPropsMixin.RenditionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "renditions": "renditions",
            "rendition_selection": "renditionSelection",
        },
    )
    class RenditionConfigurationProperty:
        def __init__(
            self,
            *,
            renditions: typing.Optional[typing.Sequence[builtins.str]] = None,
            rendition_selection: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The RenditionConfiguration property type describes which renditions should be recorded for a stream.

            :param renditions: A list of which renditions are recorded for a stream, if ``renditionSelection`` is ``CUSTOM`` ; otherwise, this field is irrelevant. The selected renditions are recorded if they are available during the stream. If a selected rendition is unavailable, the best available rendition is recorded. For details on the resolution dimensions of each rendition, see `Auto-Record to Amazon S3 <https://docs.aws.amazon.com//ivs/latest/LowLatencyUserGuide/record-to-s3.html>`_ .
            :param rendition_selection: The set of renditions are recorded for a stream. For ``BASIC`` channels, the ``CUSTOM`` value has no effect. If ``CUSTOM`` is specified, a set of renditions can be specified in the ``renditions`` field. Default: ``ALL`` . Default: - "ALL"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-renditionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                rendition_configuration_property = ivs_mixins.CfnRecordingConfigurationPropsMixin.RenditionConfigurationProperty(
                    renditions=["renditions"],
                    rendition_selection="renditionSelection"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a922519ed6bb8a6bd81d19fc99d5fc48e34d77c1839b8b9789838ecfc7fad46f)
                check_type(argname="argument renditions", value=renditions, expected_type=type_hints["renditions"])
                check_type(argname="argument rendition_selection", value=rendition_selection, expected_type=type_hints["rendition_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if renditions is not None:
                self._values["renditions"] = renditions
            if rendition_selection is not None:
                self._values["rendition_selection"] = rendition_selection

        @builtins.property
        def renditions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of which renditions are recorded for a stream, if ``renditionSelection`` is ``CUSTOM`` ;

            otherwise, this field is irrelevant. The selected renditions are recorded if they are available during the stream. If a selected rendition is unavailable, the best available rendition is recorded. For details on the resolution dimensions of each rendition, see `Auto-Record to Amazon S3 <https://docs.aws.amazon.com//ivs/latest/LowLatencyUserGuide/record-to-s3.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-renditionconfiguration.html#cfn-ivs-recordingconfiguration-renditionconfiguration-renditions
            '''
            result = self._values.get("renditions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def rendition_selection(self) -> typing.Optional[builtins.str]:
            '''The set of renditions are recorded for a stream.

            For ``BASIC`` channels, the ``CUSTOM`` value has no effect. If ``CUSTOM`` is specified, a set of renditions can be specified in the ``renditions`` field. Default: ``ALL`` .

            :default: - "ALL"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-renditionconfiguration.html#cfn-ivs-recordingconfiguration-renditionconfiguration-renditionselection
            '''
            result = self._values.get("rendition_selection")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RenditionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnRecordingConfigurationPropsMixin.S3DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName"},
    )
    class S3DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3DestinationConfiguration property type describes an S3 location where recorded videos will be stored.

            :param bucket_name: Location (S3 bucket name) where recorded videos will be stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-s3destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                s3_destination_configuration_property = ivs_mixins.CfnRecordingConfigurationPropsMixin.S3DestinationConfigurationProperty(
                    bucket_name="bucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b7d02168b6df9f98049c7b9ec2f5015e9dbb39fbf639e127df11a6aaa3fb035)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Location (S3 bucket name) where recorded videos will be stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-s3destinationconfiguration.html#cfn-ivs-recordingconfiguration-s3destinationconfiguration-bucketname
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

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnRecordingConfigurationPropsMixin.ThumbnailConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "recording_mode": "recordingMode",
            "resolution": "resolution",
            "storage": "storage",
            "target_interval_seconds": "targetIntervalSeconds",
        },
    )
    class ThumbnailConfigurationProperty:
        def __init__(
            self,
            *,
            recording_mode: typing.Optional[builtins.str] = None,
            resolution: typing.Optional[builtins.str] = None,
            storage: typing.Optional[typing.Sequence[builtins.str]] = None,
            target_interval_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ThumbnailConfiguration property type describes a configuration of thumbnails for recorded video.

            :param recording_mode: Thumbnail recording mode. Valid values:. - ``DISABLED`` : Use DISABLED to disable the generation of thumbnails for recorded video. - ``INTERVAL`` : Use INTERVAL to enable the generation of thumbnails for recorded video at a time interval controlled by the `TargetIntervalSeconds <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-targetintervalseconds>`_ property. *Default* : ``INTERVAL`` Default: - "INTERVAL"
            :param resolution: The desired resolution of recorded thumbnails for a stream. Thumbnails are recorded at the selected resolution if the corresponding rendition is available during the stream; otherwise, they are recorded at source resolution. For more information about resolution values and their corresponding height and width dimensions, see `Auto-Record to Amazon S3 <https://docs.aws.amazon.com//ivs/latest/LowLatencyUserGuide/record-to-s3.html>`_ .
            :param storage: The format in which thumbnails are recorded for a stream. ``SEQUENTIAL`` records all generated thumbnails in a serial manner, to the media/thumbnails directory. ``LATEST`` saves the latest thumbnail in media/thumbnails/latest/thumb.jpg and overwrites it at the interval specified by ``targetIntervalSeconds`` . You can enable both ``SEQUENTIAL`` and ``LATEST`` . Default: ``SEQUENTIAL`` .
            :param target_interval_seconds: The targeted thumbnail-generation interval in seconds. This is configurable (and required) only if `RecordingMode <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-recordingmode>`_ is ``INTERVAL`` . .. epigraph:: Setting a value for ``TargetIntervalSeconds`` does not guarantee that thumbnails are generated at the specified interval. For thumbnails to be generated at the ``TargetIntervalSeconds`` interval, the ``IDR/Keyframe`` value for the input video must be less than the ``TargetIntervalSeconds`` value. See `Amazon IVS Streaming Configuration <https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/streaming-config.html>`_ for information on setting ``IDR/Keyframe`` to the recommended value in video-encoder settings. *Default* : 60 Default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                thumbnail_configuration_property = ivs_mixins.CfnRecordingConfigurationPropsMixin.ThumbnailConfigurationProperty(
                    recording_mode="recordingMode",
                    resolution="resolution",
                    storage=["storage"],
                    target_interval_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8033851f9b49b4323328e48bf3b026bf5d0c85a9e2e813a0c7227764f4055163)
                check_type(argname="argument recording_mode", value=recording_mode, expected_type=type_hints["recording_mode"])
                check_type(argname="argument resolution", value=resolution, expected_type=type_hints["resolution"])
                check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
                check_type(argname="argument target_interval_seconds", value=target_interval_seconds, expected_type=type_hints["target_interval_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if recording_mode is not None:
                self._values["recording_mode"] = recording_mode
            if resolution is not None:
                self._values["resolution"] = resolution
            if storage is not None:
                self._values["storage"] = storage
            if target_interval_seconds is not None:
                self._values["target_interval_seconds"] = target_interval_seconds

        @builtins.property
        def recording_mode(self) -> typing.Optional[builtins.str]:
            '''Thumbnail recording mode. Valid values:.

            - ``DISABLED`` : Use DISABLED to disable the generation of thumbnails for recorded video.
            - ``INTERVAL`` : Use INTERVAL to enable the generation of thumbnails for recorded video at a time interval controlled by the `TargetIntervalSeconds <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-targetintervalseconds>`_ property.

            *Default* : ``INTERVAL``

            :default: - "INTERVAL"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-recordingmode
            '''
            result = self._values.get("recording_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resolution(self) -> typing.Optional[builtins.str]:
            '''The desired resolution of recorded thumbnails for a stream.

            Thumbnails are recorded at the selected resolution if the corresponding rendition is available during the stream; otherwise, they are recorded at source resolution. For more information about resolution values and their corresponding height and width dimensions, see `Auto-Record to Amazon S3 <https://docs.aws.amazon.com//ivs/latest/LowLatencyUserGuide/record-to-s3.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-resolution
            '''
            result = self._values.get("resolution")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def storage(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The format in which thumbnails are recorded for a stream.

            ``SEQUENTIAL`` records all generated thumbnails in a serial manner, to the media/thumbnails directory. ``LATEST`` saves the latest thumbnail in media/thumbnails/latest/thumb.jpg and overwrites it at the interval specified by ``targetIntervalSeconds`` . You can enable both ``SEQUENTIAL`` and ``LATEST`` . Default: ``SEQUENTIAL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-storage
            '''
            result = self._values.get("storage")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def target_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''The targeted thumbnail-generation interval in seconds. This is configurable (and required) only if `RecordingMode <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-recordingmode>`_ is ``INTERVAL`` .

            .. epigraph::

               Setting a value for ``TargetIntervalSeconds`` does not guarantee that thumbnails are generated at the specified interval. For thumbnails to be generated at the ``TargetIntervalSeconds`` interval, the ``IDR/Keyframe`` value for the input video must be less than the ``TargetIntervalSeconds`` value. See `Amazon IVS Streaming Configuration <https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/streaming-config.html>`_ for information on setting ``IDR/Keyframe`` to the recommended value in video-encoder settings.

            *Default* : 60

            :default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-targetintervalseconds
            '''
            result = self._values.get("target_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThumbnailConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStageMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_participant_recording_configuration": "autoParticipantRecordingConfiguration",
        "name": "name",
        "tags": "tags",
    },
)
class CfnStageMixinProps:
    def __init__(
        self,
        *,
        auto_participant_recording_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStagePropsMixin.AutoParticipantRecordingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStagePropsMixin.

        :param auto_participant_recording_configuration: Configuration object for individual participant recording.
        :param name: Stage name.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-stage.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
            
            cfn_stage_mixin_props = ivs_mixins.CfnStageMixinProps(
                auto_participant_recording_configuration=ivs_mixins.CfnStagePropsMixin.AutoParticipantRecordingConfigurationProperty(
                    hls_configuration=ivs_mixins.CfnStagePropsMixin.HlsConfigurationProperty(
                        participant_recording_hls_configuration=ivs_mixins.CfnStagePropsMixin.ParticipantRecordingHlsConfigurationProperty(
                            target_segment_duration_seconds=123
                        )
                    ),
                    media_types=["mediaTypes"],
                    recording_reconnect_window_seconds=123,
                    storage_configuration_arn="storageConfigurationArn",
                    thumbnail_configuration=ivs_mixins.CfnStagePropsMixin.ThumbnailConfigurationProperty(
                        participant_thumbnail_configuration=ivs_mixins.CfnStagePropsMixin.ParticipantThumbnailConfigurationProperty(
                            recording_mode="recordingMode",
                            storage=["storage"],
                            target_interval_seconds=123
                        )
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f27afa87e21e666a02703f7bf0dc526e17ec24fc48cfa754f0d856990165654)
            check_type(argname="argument auto_participant_recording_configuration", value=auto_participant_recording_configuration, expected_type=type_hints["auto_participant_recording_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_participant_recording_configuration is not None:
            self._values["auto_participant_recording_configuration"] = auto_participant_recording_configuration
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auto_participant_recording_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.AutoParticipantRecordingConfigurationProperty"]]:
        '''Configuration object for individual participant recording.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-stage.html#cfn-ivs-stage-autoparticipantrecordingconfiguration
        '''
        result = self._values.get("auto_participant_recording_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.AutoParticipantRecordingConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Stage name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-stage.html#cfn-ivs-stage-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-stage.html#cfn-ivs-stage-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStageMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStagePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStagePropsMixin",
):
    '''The ``AWS::IVS::Stage`` resource specifies an  stage.

    A stage is a virtual space where participants can exchange video in real time. For more information, see `CreateStage <https://docs.aws.amazon.com/ivs/latest/RealTimeAPIReference/API_CreateStage.html>`_ in the *Amazon IVS Real-Time Streaming API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-stage.html
    :cloudformationResource: AWS::IVS::Stage
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
        
        cfn_stage_props_mixin = ivs_mixins.CfnStagePropsMixin(ivs_mixins.CfnStageMixinProps(
            auto_participant_recording_configuration=ivs_mixins.CfnStagePropsMixin.AutoParticipantRecordingConfigurationProperty(
                hls_configuration=ivs_mixins.CfnStagePropsMixin.HlsConfigurationProperty(
                    participant_recording_hls_configuration=ivs_mixins.CfnStagePropsMixin.ParticipantRecordingHlsConfigurationProperty(
                        target_segment_duration_seconds=123
                    )
                ),
                media_types=["mediaTypes"],
                recording_reconnect_window_seconds=123,
                storage_configuration_arn="storageConfigurationArn",
                thumbnail_configuration=ivs_mixins.CfnStagePropsMixin.ThumbnailConfigurationProperty(
                    participant_thumbnail_configuration=ivs_mixins.CfnStagePropsMixin.ParticipantThumbnailConfigurationProperty(
                        recording_mode="recordingMode",
                        storage=["storage"],
                        target_interval_seconds=123
                    )
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
        props: typing.Union[CfnStageMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVS::Stage``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7630b9eabe77c15ab801cdb128525ee15c8ed2c05213f9fd0f7fe55969d48c45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb965a1590e701cb9c8d44aea53dcbfe2b05a153bf98e167ca3955cd2579e5b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5628c2ed58de34d17a5990e99f95f6b65ce21886a1845f3681b8eb55b8f7f1c2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStageMixinProps:
        return typing.cast(CfnStageMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStagePropsMixin.AutoParticipantRecordingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hls_configuration": "hlsConfiguration",
            "media_types": "mediaTypes",
            "recording_reconnect_window_seconds": "recordingReconnectWindowSeconds",
            "storage_configuration_arn": "storageConfigurationArn",
            "thumbnail_configuration": "thumbnailConfiguration",
        },
    )
    class AutoParticipantRecordingConfigurationProperty:
        def __init__(
            self,
            *,
            hls_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStagePropsMixin.HlsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            recording_reconnect_window_seconds: typing.Optional[jsii.Number] = None,
            storage_configuration_arn: typing.Optional[builtins.str] = None,
            thumbnail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStagePropsMixin.ThumbnailConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``AWS::IVS::AutoParticipantRecordingConfiguration`` property type describes a configuration for individual participant recording.

            :param hls_configuration: HLS configuration object for individual participant recording.
            :param media_types: Types of media to be recorded. Default: ``AUDIO_VIDEO`` .
            :param recording_reconnect_window_seconds: If a stage publisher disconnects and then reconnects within the specified interval, the multiple recordings will be considered a single recording and merged together. The default value is 0, which disables merging. Default: - 0
            :param storage_configuration_arn: ARN of the StorageConfiguration resource to use for individual participant recording. Default: "" (empty string, no storage configuration is specified). Individual participant recording cannot be started unless a storage configuration is specified, when a Stage is created or updated.
            :param thumbnail_configuration: A complex type that allows you to enable/disable the recording of thumbnails for individual participant recording and modify the interval at which thumbnails are generated for the live session.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-autoparticipantrecordingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                auto_participant_recording_configuration_property = ivs_mixins.CfnStagePropsMixin.AutoParticipantRecordingConfigurationProperty(
                    hls_configuration=ivs_mixins.CfnStagePropsMixin.HlsConfigurationProperty(
                        participant_recording_hls_configuration=ivs_mixins.CfnStagePropsMixin.ParticipantRecordingHlsConfigurationProperty(
                            target_segment_duration_seconds=123
                        )
                    ),
                    media_types=["mediaTypes"],
                    recording_reconnect_window_seconds=123,
                    storage_configuration_arn="storageConfigurationArn",
                    thumbnail_configuration=ivs_mixins.CfnStagePropsMixin.ThumbnailConfigurationProperty(
                        participant_thumbnail_configuration=ivs_mixins.CfnStagePropsMixin.ParticipantThumbnailConfigurationProperty(
                            recording_mode="recordingMode",
                            storage=["storage"],
                            target_interval_seconds=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9e2c20d642d0066e2eaf0d0a258aa4238e2476f9a2fa6bdef0c1bff283c4939)
                check_type(argname="argument hls_configuration", value=hls_configuration, expected_type=type_hints["hls_configuration"])
                check_type(argname="argument media_types", value=media_types, expected_type=type_hints["media_types"])
                check_type(argname="argument recording_reconnect_window_seconds", value=recording_reconnect_window_seconds, expected_type=type_hints["recording_reconnect_window_seconds"])
                check_type(argname="argument storage_configuration_arn", value=storage_configuration_arn, expected_type=type_hints["storage_configuration_arn"])
                check_type(argname="argument thumbnail_configuration", value=thumbnail_configuration, expected_type=type_hints["thumbnail_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hls_configuration is not None:
                self._values["hls_configuration"] = hls_configuration
            if media_types is not None:
                self._values["media_types"] = media_types
            if recording_reconnect_window_seconds is not None:
                self._values["recording_reconnect_window_seconds"] = recording_reconnect_window_seconds
            if storage_configuration_arn is not None:
                self._values["storage_configuration_arn"] = storage_configuration_arn
            if thumbnail_configuration is not None:
                self._values["thumbnail_configuration"] = thumbnail_configuration

        @builtins.property
        def hls_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.HlsConfigurationProperty"]]:
            '''HLS configuration object for individual participant recording.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-autoparticipantrecordingconfiguration.html#cfn-ivs-stage-autoparticipantrecordingconfiguration-hlsconfiguration
            '''
            result = self._values.get("hls_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.HlsConfigurationProperty"]], result)

        @builtins.property
        def media_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Types of media to be recorded.

            Default: ``AUDIO_VIDEO`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-autoparticipantrecordingconfiguration.html#cfn-ivs-stage-autoparticipantrecordingconfiguration-mediatypes
            '''
            result = self._values.get("media_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def recording_reconnect_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''If a stage publisher disconnects and then reconnects within the specified interval, the multiple recordings will be considered a single recording and merged together.

            The default value is 0, which disables merging.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-autoparticipantrecordingconfiguration.html#cfn-ivs-stage-autoparticipantrecordingconfiguration-recordingreconnectwindowseconds
            '''
            result = self._values.get("recording_reconnect_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def storage_configuration_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the StorageConfiguration resource to use for individual participant recording.

            Default: "" (empty string, no storage configuration is specified). Individual participant recording cannot be started unless a storage configuration is specified, when a Stage is created or updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-autoparticipantrecordingconfiguration.html#cfn-ivs-stage-autoparticipantrecordingconfiguration-storageconfigurationarn
            '''
            result = self._values.get("storage_configuration_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def thumbnail_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.ThumbnailConfigurationProperty"]]:
            '''A complex type that allows you to enable/disable the recording of thumbnails for individual participant recording and modify the interval at which thumbnails are generated for the live session.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-autoparticipantrecordingconfiguration.html#cfn-ivs-stage-autoparticipantrecordingconfiguration-thumbnailconfiguration
            '''
            result = self._values.get("thumbnail_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.ThumbnailConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoParticipantRecordingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStagePropsMixin.HlsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "participant_recording_hls_configuration": "participantRecordingHlsConfiguration",
        },
    )
    class HlsConfigurationProperty:
        def __init__(
            self,
            *,
            participant_recording_hls_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStagePropsMixin.ParticipantRecordingHlsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Object specifying an HLS configuration for individual participant recording.

            :param participant_recording_hls_configuration: Object specifying a configuration of participant HLS recordings for individual participant recording.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-hlsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                hls_configuration_property = ivs_mixins.CfnStagePropsMixin.HlsConfigurationProperty(
                    participant_recording_hls_configuration=ivs_mixins.CfnStagePropsMixin.ParticipantRecordingHlsConfigurationProperty(
                        target_segment_duration_seconds=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b03f96e454ac00d928a094c5a73d93a344f1a4f1d0cb47efe497592f233acd0c)
                check_type(argname="argument participant_recording_hls_configuration", value=participant_recording_hls_configuration, expected_type=type_hints["participant_recording_hls_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if participant_recording_hls_configuration is not None:
                self._values["participant_recording_hls_configuration"] = participant_recording_hls_configuration

        @builtins.property
        def participant_recording_hls_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.ParticipantRecordingHlsConfigurationProperty"]]:
            '''Object specifying a configuration of participant HLS recordings for individual participant recording.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-hlsconfiguration.html#cfn-ivs-stage-hlsconfiguration-participantrecordinghlsconfiguration
            '''
            result = self._values.get("participant_recording_hls_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.ParticipantRecordingHlsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStagePropsMixin.ParticipantRecordingHlsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_segment_duration_seconds": "targetSegmentDurationSeconds",
        },
    )
    class ParticipantRecordingHlsConfigurationProperty:
        def __init__(
            self,
            *,
            target_segment_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Object specifying a configuration of participant HLS recordings for individual participant recording.

            :param target_segment_duration_seconds: Defines the target duration for recorded segments generated when recording a stage participant. Segments may have durations longer than the specified value when needed to ensure each segment begins with a keyframe. Default: 6. Default: - 6

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-participantrecordinghlsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                participant_recording_hls_configuration_property = ivs_mixins.CfnStagePropsMixin.ParticipantRecordingHlsConfigurationProperty(
                    target_segment_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6f42daaf959e9b80cb77c58b97cb4e10ad35522b985b1a27ab5f8f7f40fe8b8)
                check_type(argname="argument target_segment_duration_seconds", value=target_segment_duration_seconds, expected_type=type_hints["target_segment_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_segment_duration_seconds is not None:
                self._values["target_segment_duration_seconds"] = target_segment_duration_seconds

        @builtins.property
        def target_segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Defines the target duration for recorded segments generated when recording a stage participant.

            Segments may have durations longer than the specified value when needed to ensure each segment begins with a keyframe. Default: 6.

            :default: - 6

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-participantrecordinghlsconfiguration.html#cfn-ivs-stage-participantrecordinghlsconfiguration-targetsegmentdurationseconds
            '''
            result = self._values.get("target_segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParticipantRecordingHlsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStagePropsMixin.ParticipantThumbnailConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "recording_mode": "recordingMode",
            "storage": "storage",
            "target_interval_seconds": "targetIntervalSeconds",
        },
    )
    class ParticipantThumbnailConfigurationProperty:
        def __init__(
            self,
            *,
            recording_mode: typing.Optional[builtins.str] = None,
            storage: typing.Optional[typing.Sequence[builtins.str]] = None,
            target_interval_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Object specifying a configuration of thumbnails for recorded video from an individual participant.

            :param recording_mode: Thumbnail recording mode. Default: ``DISABLED`` . Default: - "DISABLED"
            :param storage: Indicates the format in which thumbnails are recorded. ``SEQUENTIAL`` records all generated thumbnails in a serial manner, to the media/thumbnails/high directory. ``LATEST`` saves the latest thumbnail in media/latest_thumbnail/high/thumb.jpg and overwrites it at the interval specified by ``targetIntervalSeconds`` . You can enable both ``SEQUENTIAL`` and ``LATEST`` . Default: ``SEQUENTIAL`` .
            :param target_interval_seconds: The targeted thumbnail-generation interval in seconds. This is configurable only if ``recordingMode`` is ``INTERVAL`` . Default: 60. Default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-participantthumbnailconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                participant_thumbnail_configuration_property = ivs_mixins.CfnStagePropsMixin.ParticipantThumbnailConfigurationProperty(
                    recording_mode="recordingMode",
                    storage=["storage"],
                    target_interval_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b60391b3d141bd41c75829189bbc195aee07dd78f23cead4c0222035c5def792)
                check_type(argname="argument recording_mode", value=recording_mode, expected_type=type_hints["recording_mode"])
                check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
                check_type(argname="argument target_interval_seconds", value=target_interval_seconds, expected_type=type_hints["target_interval_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if recording_mode is not None:
                self._values["recording_mode"] = recording_mode
            if storage is not None:
                self._values["storage"] = storage
            if target_interval_seconds is not None:
                self._values["target_interval_seconds"] = target_interval_seconds

        @builtins.property
        def recording_mode(self) -> typing.Optional[builtins.str]:
            '''Thumbnail recording mode.

            Default: ``DISABLED`` .

            :default: - "DISABLED"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-participantthumbnailconfiguration.html#cfn-ivs-stage-participantthumbnailconfiguration-recordingmode
            '''
            result = self._values.get("recording_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def storage(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates the format in which thumbnails are recorded.

            ``SEQUENTIAL`` records all generated thumbnails in a serial manner, to the media/thumbnails/high directory. ``LATEST`` saves the latest thumbnail in media/latest_thumbnail/high/thumb.jpg and overwrites it at the interval specified by ``targetIntervalSeconds`` . You can enable both ``SEQUENTIAL`` and ``LATEST`` . Default: ``SEQUENTIAL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-participantthumbnailconfiguration.html#cfn-ivs-stage-participantthumbnailconfiguration-storage
            '''
            result = self._values.get("storage")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def target_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''The targeted thumbnail-generation interval in seconds.

            This is configurable only if ``recordingMode`` is ``INTERVAL`` . Default: 60.

            :default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-participantthumbnailconfiguration.html#cfn-ivs-stage-participantthumbnailconfiguration-targetintervalseconds
            '''
            result = self._values.get("target_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParticipantThumbnailConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStagePropsMixin.ThumbnailConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "participant_thumbnail_configuration": "participantThumbnailConfiguration",
        },
    )
    class ThumbnailConfigurationProperty:
        def __init__(
            self,
            *,
            participant_thumbnail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStagePropsMixin.ParticipantThumbnailConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object representing a configuration of thumbnails for recorded video.

            :param participant_thumbnail_configuration: Object specifying a configuration of thumbnails for recorded video from an individual participant.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-thumbnailconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                thumbnail_configuration_property = ivs_mixins.CfnStagePropsMixin.ThumbnailConfigurationProperty(
                    participant_thumbnail_configuration=ivs_mixins.CfnStagePropsMixin.ParticipantThumbnailConfigurationProperty(
                        recording_mode="recordingMode",
                        storage=["storage"],
                        target_interval_seconds=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a672a2774f086b368602f8033fe1bcb3b11fbd2a03e4a88caab4fcac77dc7223)
                check_type(argname="argument participant_thumbnail_configuration", value=participant_thumbnail_configuration, expected_type=type_hints["participant_thumbnail_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if participant_thumbnail_configuration is not None:
                self._values["participant_thumbnail_configuration"] = participant_thumbnail_configuration

        @builtins.property
        def participant_thumbnail_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.ParticipantThumbnailConfigurationProperty"]]:
            '''Object specifying a configuration of thumbnails for recorded video from an individual participant.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-stage-thumbnailconfiguration.html#cfn-ivs-stage-thumbnailconfiguration-participantthumbnailconfiguration
            '''
            result = self._values.get("participant_thumbnail_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.ParticipantThumbnailConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThumbnailConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStorageConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "s3": "s3", "tags": "tags"},
)
class CfnStorageConfigurationMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageConfigurationPropsMixin.S3StorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStorageConfigurationPropsMixin.

        :param name: Storage cnfiguration name.
        :param s3: An S3 storage configuration contains information about where recorded video will be stored. See the `S3StorageConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-storageconfiguration-s3storageconfiguration.html>`_ property type for more information.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-storageconfiguration-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-storageconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
            
            cfn_storage_configuration_mixin_props = ivs_mixins.CfnStorageConfigurationMixinProps(
                name="name",
                s3=ivs_mixins.CfnStorageConfigurationPropsMixin.S3StorageConfigurationProperty(
                    bucket_name="bucketName"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b63814b2aa57f289e9298727b99f592c2b783e01bc1c58de92117f9965f691f2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if s3 is not None:
            self._values["s3"] = s3
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Storage cnfiguration name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-storageconfiguration.html#cfn-ivs-storageconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageConfigurationPropsMixin.S3StorageConfigurationProperty"]]:
        '''An S3 storage configuration contains information about where recorded video will be stored.

        See the `S3StorageConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-storageconfiguration-s3storageconfiguration.html>`_ property type for more information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-storageconfiguration.html#cfn-ivs-storageconfiguration-s3
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageConfigurationPropsMixin.S3StorageConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-storageconfiguration-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-storageconfiguration.html#cfn-ivs-storageconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStorageConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStorageConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStorageConfigurationPropsMixin",
):
    '''The ``AWS::IVS::StorageConfiguration`` resource specifies an  storage configuration.

    A storage configuration describes an S3 location where recorded videos will be stored. For more information, see `Auto-Record to Amazon S3 (Low-Latency Streaming) <https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/record-to-s3.html>`_ in the *Amazon IVS Low-Latency Streaming User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-storageconfiguration.html
    :cloudformationResource: AWS::IVS::StorageConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
        
        cfn_storage_configuration_props_mixin = ivs_mixins.CfnStorageConfigurationPropsMixin(ivs_mixins.CfnStorageConfigurationMixinProps(
            name="name",
            s3=ivs_mixins.CfnStorageConfigurationPropsMixin.S3StorageConfigurationProperty(
                bucket_name="bucketName"
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
        props: typing.Union[CfnStorageConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVS::StorageConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3dd79a6eab7afa9b1551fd60da0281a11d2b202a45feaf87b66c69f63125175)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b99cf90ef36279ddd2125ce8ce5ff69ce76963e6edb0639574aca03d5c9988f1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44369e7563052dd77aa34e3cce83142b0d006599378b90140e7d653aee68ed0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStorageConfigurationMixinProps:
        return typing.cast(CfnStorageConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStorageConfigurationPropsMixin.S3StorageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName"},
    )
    class S3StorageConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3StorageConfiguration property type describes an S3 location where recorded videos will be stored.

            :param bucket_name: Name of the S3 bucket where recorded video will be stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-storageconfiguration-s3storageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
                
                s3_storage_configuration_property = ivs_mixins.CfnStorageConfigurationPropsMixin.S3StorageConfigurationProperty(
                    bucket_name="bucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f50cf47597ffeb91a8a7c33ea891c7bb83edccf9d6f636f20ebdf86869fc62fc)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Name of the S3 bucket where recorded video will be stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-storageconfiguration-s3storageconfiguration.html#cfn-ivs-storageconfiguration-s3storageconfiguration-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3StorageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStreamKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"channel_arn": "channelArn", "tags": "tags"},
)
class CfnStreamKeyMixinProps:
    def __init__(
        self,
        *,
        channel_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStreamKeyPropsMixin.

        :param channel_arn: Channel ARN for the stream.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-streamkey-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
            
            cfn_stream_key_mixin_props = ivs_mixins.CfnStreamKeyMixinProps(
                channel_arn="channelArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ae8a035a64f2d26c54b8a5429bad3a80443f25cd77319e64a4038c93a34821)
            check_type(argname="argument channel_arn", value=channel_arn, expected_type=type_hints["channel_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_arn is not None:
            self._values["channel_arn"] = channel_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_arn(self) -> typing.Optional[builtins.str]:
        '''Channel ARN for the stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html#cfn-ivs-streamkey-channelarn
        '''
        result = self._values.get("channel_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-streamkey-tag.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html#cfn-ivs-streamkey-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStreamKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ivs.mixins.CfnStreamKeyPropsMixin",
):
    '''The ``AWS::IVS::StreamKey`` resource specifies an  stream key associated with the referenced channel.

    Use a stream key to initiate a live stream.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html
    :cloudformationResource: AWS::IVS::StreamKey
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ivs import mixins as ivs_mixins
        
        cfn_stream_key_props_mixin = ivs_mixins.CfnStreamKeyPropsMixin(ivs_mixins.CfnStreamKeyMixinProps(
            channel_arn="channelArn",
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
        props: typing.Union[CfnStreamKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IVS::StreamKey``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9a97c9135f5c42eec0b8d3fda7bd172bf633cc1e686b81b0a6e2033b6111ce3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34795a39963e2ce56f69cb6f62935a69c05188a2dd0447dccb0ac5c576c2bc3e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d96b5416cd4c8491650c6fe3bbede49fe15e51f6552e1964849219a35f818f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStreamKeyMixinProps:
        return typing.cast(CfnStreamKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnChannelMixinProps",
    "CfnChannelPropsMixin",
    "CfnEncoderConfigurationMixinProps",
    "CfnEncoderConfigurationPropsMixin",
    "CfnIngestConfigurationMixinProps",
    "CfnIngestConfigurationPropsMixin",
    "CfnPlaybackKeyPairMixinProps",
    "CfnPlaybackKeyPairPropsMixin",
    "CfnPlaybackRestrictionPolicyMixinProps",
    "CfnPlaybackRestrictionPolicyPropsMixin",
    "CfnPublicKeyMixinProps",
    "CfnPublicKeyPropsMixin",
    "CfnRecordingConfigurationMixinProps",
    "CfnRecordingConfigurationPropsMixin",
    "CfnStageMixinProps",
    "CfnStagePropsMixin",
    "CfnStorageConfigurationMixinProps",
    "CfnStorageConfigurationPropsMixin",
    "CfnStreamKeyMixinProps",
    "CfnStreamKeyPropsMixin",
]

publication.publish()

def _typecheckingstub__cb288a205d6b870bd353ff2843a561b6de4c1705f00e238802a91acd0a2b2653(
    *,
    authorized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    container_format: typing.Optional[builtins.str] = None,
    insecure_ingest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    latency_mode: typing.Optional[builtins.str] = None,
    multitrack_input_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.MultitrackInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    preset: typing.Optional[builtins.str] = None,
    recording_configuration_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f002787fcf1844145f12b0f02ad68ae1f3d191fa3f1aecb772b3dac913e6f99(
    props: typing.Union[CfnChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29775cbf9bcad1d9cc5dd618fa2adf510848f55d0a33455c389d3df7f7c70ba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4ded844637d178f24d55d7d3f5410ba592ddaea67313ae196d29a10af04dc2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c0d3ed8dd0658ce18af59be010168ecef0e4805fd3bcaf49435f4cfd37ee11(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    maximum_resolution: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b0fd21c6c7a2f4d9f3da423c8ed9cc22c24dd74f88345e958ba5526ad4f116c(
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    video: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEncoderConfigurationPropsMixin.VideoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef92066b01c2eb9e4ce2ebb736da338bc2709fe82bfc8484693855e4e813430(
    props: typing.Union[CfnEncoderConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c649b61b4217cac708c5446eb9ecaa8ab83853615dc8fcdc340e2a468f9bb113(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562f6aa4a27e8257aeab66ae2db16ddd87c1341d7e4f80a14dde2515ab31833d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ddd263df1cc3d436bdfee93ceea3d23b1f11e51af4724ce841de269fa41c9b(
    *,
    bitrate: typing.Optional[jsii.Number] = None,
    framerate: typing.Optional[jsii.Number] = None,
    height: typing.Optional[jsii.Number] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14bf9162144d285d1b872b97a31f3ddf8cf0b4155b1f6cc76a8089358e558ba0(
    *,
    ingest_protocol: typing.Optional[builtins.str] = None,
    insecure_ingest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    stage_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1908e018b38045146b9a4f92af1532c05ee5f97c533e81479297c2b6159948(
    props: typing.Union[CfnIngestConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779463aa659da184e9f5e392160dadca06c76e42ddd1dca37cb848faed0a769c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c488a6526e89d2719a3b94989f834fda513a03728f5bd3c82eb716177651b9f0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ccac3562d547e4f85efb8e6228094cb51f3b298dc27219cd52127005822646a(
    *,
    name: typing.Optional[builtins.str] = None,
    public_key_material: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2511dab19dd0d0230a311d8547ac2b3fe94d53d5bfb03e6142718d97eded8586(
    props: typing.Union[CfnPlaybackKeyPairMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfa2ff0a6223f24af43258fbf848b554fe3ec64fe05391d0fe04dfd2e1f08f8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46672831e48de4ffbfc5d82945c27f2872875cac032e5a323d74e9fe570c4216(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23cf58f3689b7b82d19ee2a733f3cc4aae66f4a317e8a39d87e2477ffaf3b3fb(
    *,
    allowed_countries: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_strict_origin_enforcement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71ee2fde21ec6f2994a127a1ed64d53c3017b16f645e1d0b82ca297e89103ae(
    props: typing.Union[CfnPlaybackRestrictionPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee98fc8b0886205e85e29e29904234be9887b821cfbc4c695c0d6704f0b00921(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef710d5f8996007a66967eca6740693ce73287d96a9cb8eb51d3ddc0b0403e2e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9292aa3b99825f60d95a59be3809a1696b1aaf8317dae24041b066493a189e88(
    *,
    name: typing.Optional[builtins.str] = None,
    public_key_material: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac14b93b241227a2968e677754a327f39d0536c20b2cab1b859799bd4622f227(
    props: typing.Union[CfnPublicKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f39d3519361ec90d61f3dc12ffcade768fd883b592af7957c7d89d253a37a8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b08ee31de0c11c2e068806af80bcad79c3b6160e0fad47ab827d0691a0aaf83(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d402fdc1696a7df42b8e7f0f9e57876bbaa2adf96a74f47c6dfd7fdbce4b7bb(
    *,
    destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordingConfigurationPropsMixin.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    recording_reconnect_window_seconds: typing.Optional[jsii.Number] = None,
    rendition_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordingConfigurationPropsMixin.RenditionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    thumbnail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordingConfigurationPropsMixin.ThumbnailConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb85a5b540c63b05986d02fa1d3058d2b0ed6355b724d7a2dd55bf33fee7389(
    props: typing.Union[CfnRecordingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382c462de7281cfad3825065a63d5ee62a7e595688a2bbbe6cbe48718f05445f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b83983aa8e010fe27a47a95a25adcc123469bee815aef438804aefd5f8a0e5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030921f545f69ea68f6ad6f4493e3331f8f097f636b012b71be4d92cad44f8b3(
    *,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordingConfigurationPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a922519ed6bb8a6bd81d19fc99d5fc48e34d77c1839b8b9789838ecfc7fad46f(
    *,
    renditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    rendition_selection: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7d02168b6df9f98049c7b9ec2f5015e9dbb39fbf639e127df11a6aaa3fb035(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8033851f9b49b4323328e48bf3b026bf5d0c85a9e2e813a0c7227764f4055163(
    *,
    recording_mode: typing.Optional[builtins.str] = None,
    resolution: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_interval_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f27afa87e21e666a02703f7bf0dc526e17ec24fc48cfa754f0d856990165654(
    *,
    auto_participant_recording_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStagePropsMixin.AutoParticipantRecordingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7630b9eabe77c15ab801cdb128525ee15c8ed2c05213f9fd0f7fe55969d48c45(
    props: typing.Union[CfnStageMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb965a1590e701cb9c8d44aea53dcbfe2b05a153bf98e167ca3955cd2579e5b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5628c2ed58de34d17a5990e99f95f6b65ce21886a1845f3681b8eb55b8f7f1c2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e2c20d642d0066e2eaf0d0a258aa4238e2476f9a2fa6bdef0c1bff283c4939(
    *,
    hls_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStagePropsMixin.HlsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    recording_reconnect_window_seconds: typing.Optional[jsii.Number] = None,
    storage_configuration_arn: typing.Optional[builtins.str] = None,
    thumbnail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStagePropsMixin.ThumbnailConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03f96e454ac00d928a094c5a73d93a344f1a4f1d0cb47efe497592f233acd0c(
    *,
    participant_recording_hls_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStagePropsMixin.ParticipantRecordingHlsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f42daaf959e9b80cb77c58b97cb4e10ad35522b985b1a27ab5f8f7f40fe8b8(
    *,
    target_segment_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60391b3d141bd41c75829189bbc195aee07dd78f23cead4c0222035c5def792(
    *,
    recording_mode: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_interval_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a672a2774f086b368602f8033fe1bcb3b11fbd2a03e4a88caab4fcac77dc7223(
    *,
    participant_thumbnail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStagePropsMixin.ParticipantThumbnailConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63814b2aa57f289e9298727b99f592c2b783e01bc1c58de92117f9965f691f2(
    *,
    name: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageConfigurationPropsMixin.S3StorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3dd79a6eab7afa9b1551fd60da0281a11d2b202a45feaf87b66c69f63125175(
    props: typing.Union[CfnStorageConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99cf90ef36279ddd2125ce8ce5ff69ce76963e6edb0639574aca03d5c9988f1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44369e7563052dd77aa34e3cce83142b0d006599378b90140e7d653aee68ed0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50cf47597ffeb91a8a7c33ea891c7bb83edccf9d6f636f20ebdf86869fc62fc(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ae8a035a64f2d26c54b8a5429bad3a80443f25cd77319e64a4038c93a34821(
    *,
    channel_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a97c9135f5c42eec0b8d3fda7bd172bf633cc1e686b81b0a6e2033b6111ce3(
    props: typing.Union[CfnStreamKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34795a39963e2ce56f69cb6f62935a69c05188a2dd0447dccb0ac5c576c2bc3e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d96b5416cd4c8491650c6fe3bbede49fe15e51f6552e1964849219a35f818f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
