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
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "audiences": "audiences",
        "channel_name": "channelName",
        "filler_slate": "fillerSlate",
        "log_configuration": "logConfiguration",
        "outputs": "outputs",
        "playback_mode": "playbackMode",
        "tags": "tags",
        "tier": "tier",
        "time_shift_configuration": "timeShiftConfiguration",
    },
)
class CfnChannelMixinProps:
    def __init__(
        self,
        *,
        audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        channel_name: typing.Optional[builtins.str] = None,
        filler_slate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.SlateSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.LogConfigurationForChannelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.RequestOutputItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        playback_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tier: typing.Optional[builtins.str] = None,
        time_shift_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.TimeShiftConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnChannelPropsMixin.

        :param audiences: The list of audiences defined in channel.
        :param channel_name: The name of the channel.
        :param filler_slate: The slate used to fill gaps between programs in the schedule. You must configure filler slate if your channel uses the ``LINEAR`` ``PlaybackMode`` . MediaTailor doesn't support filler slate for channels using the ``LOOP`` ``PlaybackMode`` .
        :param log_configuration: The log configuration.
        :param outputs: The channel's output properties.
        :param playback_mode: The type of playback mode for this channel. ``LINEAR`` - Programs play back-to-back only once. ``LOOP`` - Programs play back-to-back in an endless loop. When the last program in the schedule plays, playback loops back to the first program in the schedule.
        :param tags: The tags to assign to the channel. Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see `Tagging AWS Elemental MediaTailor Resources <https://docs.aws.amazon.com/mediatailor/latest/ug/tagging.html>`_ .
        :param tier: The tier for this channel. STANDARD tier channels can contain live programs.
        :param time_shift_configuration: The configuration for time-shifted viewing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
            
            cfn_channel_mixin_props = mediatailor_mixins.CfnChannelMixinProps(
                audiences=["audiences"],
                channel_name="channelName",
                filler_slate=mediatailor_mixins.CfnChannelPropsMixin.SlateSourceProperty(
                    source_location_name="sourceLocationName",
                    vod_source_name="vodSourceName"
                ),
                log_configuration=mediatailor_mixins.CfnChannelPropsMixin.LogConfigurationForChannelProperty(
                    log_types=["logTypes"]
                ),
                outputs=[mediatailor_mixins.CfnChannelPropsMixin.RequestOutputItemProperty(
                    dash_playlist_settings=mediatailor_mixins.CfnChannelPropsMixin.DashPlaylistSettingsProperty(
                        manifest_window_seconds=123,
                        min_buffer_time_seconds=123,
                        min_update_period_seconds=123,
                        suggested_presentation_delay_seconds=123
                    ),
                    hls_playlist_settings=mediatailor_mixins.CfnChannelPropsMixin.HlsPlaylistSettingsProperty(
                        ad_markup_type=["adMarkupType"],
                        manifest_window_seconds=123
                    ),
                    manifest_name="manifestName",
                    source_group="sourceGroup"
                )],
                playback_mode="playbackMode",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tier="tier",
                time_shift_configuration=mediatailor_mixins.CfnChannelPropsMixin.TimeShiftConfigurationProperty(
                    max_time_delay_seconds=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5415afb81c2d023e0e7fb35386bc1e78c6469e1832821846b1fb2c96d52bcae)
            check_type(argname="argument audiences", value=audiences, expected_type=type_hints["audiences"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument filler_slate", value=filler_slate, expected_type=type_hints["filler_slate"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument playback_mode", value=playback_mode, expected_type=type_hints["playback_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument time_shift_configuration", value=time_shift_configuration, expected_type=type_hints["time_shift_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audiences is not None:
            self._values["audiences"] = audiences
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if filler_slate is not None:
            self._values["filler_slate"] = filler_slate
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if outputs is not None:
            self._values["outputs"] = outputs
        if playback_mode is not None:
            self._values["playback_mode"] = playback_mode
        if tags is not None:
            self._values["tags"] = tags
        if tier is not None:
            self._values["tier"] = tier
        if time_shift_configuration is not None:
            self._values["time_shift_configuration"] = time_shift_configuration

    @builtins.property
    def audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of audiences defined in channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html#cfn-mediatailor-channel-audiences
        '''
        result = self._values.get("audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html#cfn-mediatailor-channel-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filler_slate(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.SlateSourceProperty"]]:
        '''The slate used to fill gaps between programs in the schedule.

        You must configure filler slate if your channel uses the ``LINEAR`` ``PlaybackMode`` . MediaTailor doesn't support filler slate for channels using the ``LOOP`` ``PlaybackMode`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html#cfn-mediatailor-channel-fillerslate
        '''
        result = self._values.get("filler_slate")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.SlateSourceProperty"]], result)

    @builtins.property
    def log_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.LogConfigurationForChannelProperty"]]:
        '''The log configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html#cfn-mediatailor-channel-logconfiguration
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.LogConfigurationForChannelProperty"]], result)

    @builtins.property
    def outputs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.RequestOutputItemProperty"]]]]:
        '''The channel's output properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html#cfn-mediatailor-channel-outputs
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.RequestOutputItemProperty"]]]], result)

    @builtins.property
    def playback_mode(self) -> typing.Optional[builtins.str]:
        '''The type of playback mode for this channel.

        ``LINEAR`` - Programs play back-to-back only once.

        ``LOOP`` - Programs play back-to-back in an endless loop. When the last program in the schedule plays, playback loops back to the first program in the schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html#cfn-mediatailor-channel-playbackmode
        '''
        result = self._values.get("playback_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to the channel.

        Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see `Tagging AWS Elemental MediaTailor Resources <https://docs.aws.amazon.com/mediatailor/latest/ug/tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html#cfn-mediatailor-channel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The tier for this channel.

        STANDARD tier channels can contain live programs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html#cfn-mediatailor-channel-tier
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_shift_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.TimeShiftConfigurationProperty"]]:
        '''The configuration for time-shifted viewing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html#cfn-mediatailor-channel-timeshiftconfiguration
        '''
        result = self._values.get("time_shift_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.TimeShiftConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnChannelPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"channel_name": "channelName", "policy": "policy"},
)
class CfnChannelPolicyMixinProps:
    def __init__(
        self,
        *,
        channel_name: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
    ) -> None:
        '''Properties for CfnChannelPolicyPropsMixin.

        :param channel_name: The name of the channel associated with this Channel Policy.
        :param policy: The IAM policy for the channel. IAM policies are used to control access to your channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channelpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
            
            # policy: Any
            
            cfn_channel_policy_mixin_props = mediatailor_mixins.CfnChannelPolicyMixinProps(
                channel_name="channelName",
                policy=policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e81c5104a4fb2b995210f7950b3076943d527115681b83890fe0d90510c869)
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel associated with this Channel Policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channelpolicy.html#cfn-mediatailor-channelpolicy-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''The IAM policy for the channel.

        IAM policies are used to control access to your channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channelpolicy.html#cfn-mediatailor-channelpolicy-policy
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
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnChannelPolicyPropsMixin",
):
    '''Specifies an IAM policy for the channel.

    IAM policies are used to control access to your channel.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channelpolicy.html
    :cloudformationResource: AWS::MediaTailor::ChannelPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
        
        # policy: Any
        
        cfn_channel_policy_props_mixin = mediatailor_mixins.CfnChannelPolicyPropsMixin(mediatailor_mixins.CfnChannelPolicyMixinProps(
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
        '''Create a mixin to apply properties to ``AWS::MediaTailor::ChannelPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ac248c9a37a8a27574a2631b3dda383372cdc9f651c29f62422759a4446c82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__276f27480e032761112a99c03ce8c15c3c5679e6a3a7e312c713ee439a8fd96f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2423e072952f6717d11e37fdec6fc534d0fcf84c5c32418dfbaf5515f9b673)
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
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnChannelPropsMixin",
):
    '''The configuration parameters for a channel.

    For information about MediaTailor channels, see `Working with channels <https://docs.aws.amazon.com/mediatailor/latest/ug/channel-assembly-channels.html>`_ in the *MediaTailor User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-channel.html
    :cloudformationResource: AWS::MediaTailor::Channel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
        
        cfn_channel_props_mixin = mediatailor_mixins.CfnChannelPropsMixin(mediatailor_mixins.CfnChannelMixinProps(
            audiences=["audiences"],
            channel_name="channelName",
            filler_slate=mediatailor_mixins.CfnChannelPropsMixin.SlateSourceProperty(
                source_location_name="sourceLocationName",
                vod_source_name="vodSourceName"
            ),
            log_configuration=mediatailor_mixins.CfnChannelPropsMixin.LogConfigurationForChannelProperty(
                log_types=["logTypes"]
            ),
            outputs=[mediatailor_mixins.CfnChannelPropsMixin.RequestOutputItemProperty(
                dash_playlist_settings=mediatailor_mixins.CfnChannelPropsMixin.DashPlaylistSettingsProperty(
                    manifest_window_seconds=123,
                    min_buffer_time_seconds=123,
                    min_update_period_seconds=123,
                    suggested_presentation_delay_seconds=123
                ),
                hls_playlist_settings=mediatailor_mixins.CfnChannelPropsMixin.HlsPlaylistSettingsProperty(
                    ad_markup_type=["adMarkupType"],
                    manifest_window_seconds=123
                ),
                manifest_name="manifestName",
                source_group="sourceGroup"
            )],
            playback_mode="playbackMode",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tier="tier",
            time_shift_configuration=mediatailor_mixins.CfnChannelPropsMixin.TimeShiftConfigurationProperty(
                max_time_delay_seconds=123
            )
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
        '''Create a mixin to apply properties to ``AWS::MediaTailor::Channel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9cc21419bf96dbd8ec109cac7dbcd531ed2fbf967b4d94c9a84faeaf9fb6c0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fb56ddb44249f30b9b26cdb5fdf1bc5cdbad43043afcc8240acd4a31d366966)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c9e7b8906b29f2bfe0665d24776b42aa59f194003f906b51603e856073e623)
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
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnChannelPropsMixin.DashPlaylistSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "manifest_window_seconds": "manifestWindowSeconds",
            "min_buffer_time_seconds": "minBufferTimeSeconds",
            "min_update_period_seconds": "minUpdatePeriodSeconds",
            "suggested_presentation_delay_seconds": "suggestedPresentationDelaySeconds",
        },
    )
    class DashPlaylistSettingsProperty:
        def __init__(
            self,
            *,
            manifest_window_seconds: typing.Optional[jsii.Number] = None,
            min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
            min_update_period_seconds: typing.Optional[jsii.Number] = None,
            suggested_presentation_delay_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Dash manifest configuration parameters.

            :param manifest_window_seconds: The total duration (in seconds) of each manifest. Minimum value: ``30`` seconds. Maximum value: ``3600`` seconds.
            :param min_buffer_time_seconds: Minimum amount of content (measured in seconds) that a player must keep available in the buffer. Minimum value: ``2`` seconds. Maximum value: ``60`` seconds.
            :param min_update_period_seconds: Minimum amount of time (in seconds) that the player should wait before requesting updates to the manifest. Minimum value: ``2`` seconds. Maximum value: ``60`` seconds.
            :param suggested_presentation_delay_seconds: Amount of time (in seconds) that the player should be from the live point at the end of the manifest. Minimum value: ``2`` seconds. Maximum value: ``60`` seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-dashplaylistsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                dash_playlist_settings_property = mediatailor_mixins.CfnChannelPropsMixin.DashPlaylistSettingsProperty(
                    manifest_window_seconds=123,
                    min_buffer_time_seconds=123,
                    min_update_period_seconds=123,
                    suggested_presentation_delay_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__05e8c79dc4b4d41927f0beca0225128b08ad354ef67656dd0ad3faf724102675)
                check_type(argname="argument manifest_window_seconds", value=manifest_window_seconds, expected_type=type_hints["manifest_window_seconds"])
                check_type(argname="argument min_buffer_time_seconds", value=min_buffer_time_seconds, expected_type=type_hints["min_buffer_time_seconds"])
                check_type(argname="argument min_update_period_seconds", value=min_update_period_seconds, expected_type=type_hints["min_update_period_seconds"])
                check_type(argname="argument suggested_presentation_delay_seconds", value=suggested_presentation_delay_seconds, expected_type=type_hints["suggested_presentation_delay_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if manifest_window_seconds is not None:
                self._values["manifest_window_seconds"] = manifest_window_seconds
            if min_buffer_time_seconds is not None:
                self._values["min_buffer_time_seconds"] = min_buffer_time_seconds
            if min_update_period_seconds is not None:
                self._values["min_update_period_seconds"] = min_update_period_seconds
            if suggested_presentation_delay_seconds is not None:
                self._values["suggested_presentation_delay_seconds"] = suggested_presentation_delay_seconds

        @builtins.property
        def manifest_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''The total duration (in seconds) of each manifest.

            Minimum value: ``30`` seconds. Maximum value: ``3600`` seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-dashplaylistsettings.html#cfn-mediatailor-channel-dashplaylistsettings-manifestwindowseconds
            '''
            result = self._values.get("manifest_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_buffer_time_seconds(self) -> typing.Optional[jsii.Number]:
            '''Minimum amount of content (measured in seconds) that a player must keep available in the buffer.

            Minimum value: ``2`` seconds. Maximum value: ``60`` seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-dashplaylistsettings.html#cfn-mediatailor-channel-dashplaylistsettings-minbuffertimeseconds
            '''
            result = self._values.get("min_buffer_time_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_update_period_seconds(self) -> typing.Optional[jsii.Number]:
            '''Minimum amount of time (in seconds) that the player should wait before requesting updates to the manifest.

            Minimum value: ``2`` seconds. Maximum value: ``60`` seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-dashplaylistsettings.html#cfn-mediatailor-channel-dashplaylistsettings-minupdateperiodseconds
            '''
            result = self._values.get("min_update_period_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def suggested_presentation_delay_seconds(self) -> typing.Optional[jsii.Number]:
            '''Amount of time (in seconds) that the player should be from the live point at the end of the manifest.

            Minimum value: ``2`` seconds. Maximum value: ``60`` seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-dashplaylistsettings.html#cfn-mediatailor-channel-dashplaylistsettings-suggestedpresentationdelayseconds
            '''
            result = self._values.get("suggested_presentation_delay_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashPlaylistSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnChannelPropsMixin.HlsPlaylistSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_markup_type": "adMarkupType",
            "manifest_window_seconds": "manifestWindowSeconds",
        },
    )
    class HlsPlaylistSettingsProperty:
        def __init__(
            self,
            *,
            ad_markup_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            manifest_window_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''HLS playlist configuration parameters.

            :param ad_markup_type: Determines the type of SCTE 35 tags to use in ad markup. Specify ``DATERANGE`` to use ``DATERANGE`` tags (for live or VOD content). Specify ``SCTE35_ENHANCED`` to use ``EXT-X-CUE-OUT`` and ``EXT-X-CUE-IN`` tags (for VOD content only).
            :param manifest_window_seconds: The total duration (in seconds) of each manifest. Minimum value: ``30`` seconds. Maximum value: ``3600`` seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-hlsplaylistsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                hls_playlist_settings_property = mediatailor_mixins.CfnChannelPropsMixin.HlsPlaylistSettingsProperty(
                    ad_markup_type=["adMarkupType"],
                    manifest_window_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a097a2656809fa8cbaa6984f7719accd4fd4e9b41060ce5ecedbbe9d66d445f)
                check_type(argname="argument ad_markup_type", value=ad_markup_type, expected_type=type_hints["ad_markup_type"])
                check_type(argname="argument manifest_window_seconds", value=manifest_window_seconds, expected_type=type_hints["manifest_window_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_markup_type is not None:
                self._values["ad_markup_type"] = ad_markup_type
            if manifest_window_seconds is not None:
                self._values["manifest_window_seconds"] = manifest_window_seconds

        @builtins.property
        def ad_markup_type(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Determines the type of SCTE 35 tags to use in ad markup.

            Specify ``DATERANGE`` to use ``DATERANGE`` tags (for live or VOD content). Specify ``SCTE35_ENHANCED`` to use ``EXT-X-CUE-OUT`` and ``EXT-X-CUE-IN`` tags (for VOD content only).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-hlsplaylistsettings.html#cfn-mediatailor-channel-hlsplaylistsettings-admarkuptype
            '''
            result = self._values.get("ad_markup_type")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def manifest_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''The total duration (in seconds) of each manifest.

            Minimum value: ``30`` seconds. Maximum value: ``3600`` seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-hlsplaylistsettings.html#cfn-mediatailor-channel-hlsplaylistsettings-manifestwindowseconds
            '''
            result = self._values.get("manifest_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsPlaylistSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnChannelPropsMixin.LogConfigurationForChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"log_types": "logTypes"},
    )
    class LogConfigurationForChannelProperty:
        def __init__(
            self,
            *,
            log_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The log configuration for the channel.

            :param log_types: The log types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-logconfigurationforchannel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                log_configuration_for_channel_property = mediatailor_mixins.CfnChannelPropsMixin.LogConfigurationForChannelProperty(
                    log_types=["logTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33b85bca524f4b172c209f496a7a9c47e715524f8aff9dc399eb6b4ce0c45916)
                check_type(argname="argument log_types", value=log_types, expected_type=type_hints["log_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_types is not None:
                self._values["log_types"] = log_types

        @builtins.property
        def log_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The log types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-logconfigurationforchannel.html#cfn-mediatailor-channel-logconfigurationforchannel-logtypes
            '''
            result = self._values.get("log_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationForChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnChannelPropsMixin.RequestOutputItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dash_playlist_settings": "dashPlaylistSettings",
            "hls_playlist_settings": "hlsPlaylistSettings",
            "manifest_name": "manifestName",
            "source_group": "sourceGroup",
        },
    )
    class RequestOutputItemProperty:
        def __init__(
            self,
            *,
            dash_playlist_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.DashPlaylistSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hls_playlist_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.HlsPlaylistSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            source_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The output configuration for this channel.

            :param dash_playlist_settings: DASH manifest configuration parameters.
            :param hls_playlist_settings: HLS playlist configuration parameters.
            :param manifest_name: The name of the manifest for the channel. The name appears in the ``PlaybackUrl`` .
            :param source_group: A string used to match which ``HttpPackageConfiguration`` is used for each ``VodSource`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-requestoutputitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                request_output_item_property = mediatailor_mixins.CfnChannelPropsMixin.RequestOutputItemProperty(
                    dash_playlist_settings=mediatailor_mixins.CfnChannelPropsMixin.DashPlaylistSettingsProperty(
                        manifest_window_seconds=123,
                        min_buffer_time_seconds=123,
                        min_update_period_seconds=123,
                        suggested_presentation_delay_seconds=123
                    ),
                    hls_playlist_settings=mediatailor_mixins.CfnChannelPropsMixin.HlsPlaylistSettingsProperty(
                        ad_markup_type=["adMarkupType"],
                        manifest_window_seconds=123
                    ),
                    manifest_name="manifestName",
                    source_group="sourceGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fefd86399b0b6b817c3fc3e112996a715962c9fb26299e98afde686e8ab1d347)
                check_type(argname="argument dash_playlist_settings", value=dash_playlist_settings, expected_type=type_hints["dash_playlist_settings"])
                check_type(argname="argument hls_playlist_settings", value=hls_playlist_settings, expected_type=type_hints["hls_playlist_settings"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument source_group", value=source_group, expected_type=type_hints["source_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dash_playlist_settings is not None:
                self._values["dash_playlist_settings"] = dash_playlist_settings
            if hls_playlist_settings is not None:
                self._values["hls_playlist_settings"] = hls_playlist_settings
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if source_group is not None:
                self._values["source_group"] = source_group

        @builtins.property
        def dash_playlist_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.DashPlaylistSettingsProperty"]]:
            '''DASH manifest configuration parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-requestoutputitem.html#cfn-mediatailor-channel-requestoutputitem-dashplaylistsettings
            '''
            result = self._values.get("dash_playlist_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.DashPlaylistSettingsProperty"]], result)

        @builtins.property
        def hls_playlist_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.HlsPlaylistSettingsProperty"]]:
            '''HLS playlist configuration parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-requestoutputitem.html#cfn-mediatailor-channel-requestoutputitem-hlsplaylistsettings
            '''
            result = self._values.get("hls_playlist_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.HlsPlaylistSettingsProperty"]], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''The name of the manifest for the channel.

            The name appears in the ``PlaybackUrl`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-requestoutputitem.html#cfn-mediatailor-channel-requestoutputitem-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_group(self) -> typing.Optional[builtins.str]:
            '''A string used to match which ``HttpPackageConfiguration`` is used for each ``VodSource`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-requestoutputitem.html#cfn-mediatailor-channel-requestoutputitem-sourcegroup
            '''
            result = self._values.get("source_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequestOutputItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnChannelPropsMixin.SlateSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_location_name": "sourceLocationName",
            "vod_source_name": "vodSourceName",
        },
    )
    class SlateSourceProperty:
        def __init__(
            self,
            *,
            source_location_name: typing.Optional[builtins.str] = None,
            vod_source_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Slate VOD source configuration.

            :param source_location_name: The name of the source location where the slate VOD source is stored.
            :param vod_source_name: The slate VOD source name. The VOD source must already exist in a source location before it can be used for slate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-slatesource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                slate_source_property = mediatailor_mixins.CfnChannelPropsMixin.SlateSourceProperty(
                    source_location_name="sourceLocationName",
                    vod_source_name="vodSourceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73db29900f18d40347a0833d2fd45fcd0e91c85bc00ad5e337a5c010b2c727e4)
                check_type(argname="argument source_location_name", value=source_location_name, expected_type=type_hints["source_location_name"])
                check_type(argname="argument vod_source_name", value=vod_source_name, expected_type=type_hints["vod_source_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_location_name is not None:
                self._values["source_location_name"] = source_location_name
            if vod_source_name is not None:
                self._values["vod_source_name"] = vod_source_name

        @builtins.property
        def source_location_name(self) -> typing.Optional[builtins.str]:
            '''The name of the source location where the slate VOD source is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-slatesource.html#cfn-mediatailor-channel-slatesource-sourcelocationname
            '''
            result = self._values.get("source_location_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vod_source_name(self) -> typing.Optional[builtins.str]:
            '''The slate VOD source name.

            The VOD source must already exist in a source location before it can be used for slate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-slatesource.html#cfn-mediatailor-channel-slatesource-vodsourcename
            '''
            result = self._values.get("vod_source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlateSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnChannelPropsMixin.TimeShiftConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"max_time_delay_seconds": "maxTimeDelaySeconds"},
    )
    class TimeShiftConfigurationProperty:
        def __init__(
            self,
            *,
            max_time_delay_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration for time-shifted viewing.

            :param max_time_delay_seconds: The maximum time delay for time-shifted viewing. The minimum allowed maximum time delay is 0 seconds, and the maximum allowed maximum time delay is 21600 seconds (6 hours).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-timeshiftconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                time_shift_configuration_property = mediatailor_mixins.CfnChannelPropsMixin.TimeShiftConfigurationProperty(
                    max_time_delay_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11433fe731a80590e987bc4cf39a7fa8e753db5fb00715895a6609427e0096cb)
                check_type(argname="argument max_time_delay_seconds", value=max_time_delay_seconds, expected_type=type_hints["max_time_delay_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_time_delay_seconds is not None:
                self._values["max_time_delay_seconds"] = max_time_delay_seconds

        @builtins.property
        def max_time_delay_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum time delay for time-shifted viewing.

            The minimum allowed maximum time delay is 0 seconds, and the maximum allowed maximum time delay is 21600 seconds (6 hours).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-channel-timeshiftconfiguration.html#cfn-mediatailor-channel-timeshiftconfiguration-maxtimedelayseconds
            '''
            result = self._values.get("max_time_delay_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeShiftConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnLiveSourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "http_package_configurations": "httpPackageConfigurations",
        "live_source_name": "liveSourceName",
        "source_location_name": "sourceLocationName",
        "tags": "tags",
    },
)
class CfnLiveSourceMixinProps:
    def __init__(
        self,
        *,
        http_package_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLiveSourcePropsMixin.HttpPackageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        live_source_name: typing.Optional[builtins.str] = None,
        source_location_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLiveSourcePropsMixin.

        :param http_package_configurations: The HTTP package configurations for the live source.
        :param live_source_name: The name that's used to refer to a live source.
        :param source_location_name: The name of the source location.
        :param tags: The tags assigned to the live source. Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see `Tagging AWS Elemental MediaTailor Resources <https://docs.aws.amazon.com/mediatailor/latest/ug/tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-livesource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
            
            cfn_live_source_mixin_props = mediatailor_mixins.CfnLiveSourceMixinProps(
                http_package_configurations=[mediatailor_mixins.CfnLiveSourcePropsMixin.HttpPackageConfigurationProperty(
                    path="path",
                    source_group="sourceGroup",
                    type="type"
                )],
                live_source_name="liveSourceName",
                source_location_name="sourceLocationName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85aa1e71522700650a9e323c27f63d2c3a6df9c3991970b481bea13211be0ecb)
            check_type(argname="argument http_package_configurations", value=http_package_configurations, expected_type=type_hints["http_package_configurations"])
            check_type(argname="argument live_source_name", value=live_source_name, expected_type=type_hints["live_source_name"])
            check_type(argname="argument source_location_name", value=source_location_name, expected_type=type_hints["source_location_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_package_configurations is not None:
            self._values["http_package_configurations"] = http_package_configurations
        if live_source_name is not None:
            self._values["live_source_name"] = live_source_name
        if source_location_name is not None:
            self._values["source_location_name"] = source_location_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def http_package_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLiveSourcePropsMixin.HttpPackageConfigurationProperty"]]]]:
        '''The HTTP package configurations for the live source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-livesource.html#cfn-mediatailor-livesource-httppackageconfigurations
        '''
        result = self._values.get("http_package_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLiveSourcePropsMixin.HttpPackageConfigurationProperty"]]]], result)

    @builtins.property
    def live_source_name(self) -> typing.Optional[builtins.str]:
        '''The name that's used to refer to a live source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-livesource.html#cfn-mediatailor-livesource-livesourcename
        '''
        result = self._values.get("live_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_location_name(self) -> typing.Optional[builtins.str]:
        '''The name of the source location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-livesource.html#cfn-mediatailor-livesource-sourcelocationname
        '''
        result = self._values.get("source_location_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags assigned to the live source.

        Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see `Tagging AWS Elemental MediaTailor Resources <https://docs.aws.amazon.com/mediatailor/latest/ug/tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-livesource.html#cfn-mediatailor-livesource-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLiveSourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLiveSourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnLiveSourcePropsMixin",
):
    '''Live source configuration parameters.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-livesource.html
    :cloudformationResource: AWS::MediaTailor::LiveSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
        
        cfn_live_source_props_mixin = mediatailor_mixins.CfnLiveSourcePropsMixin(mediatailor_mixins.CfnLiveSourceMixinProps(
            http_package_configurations=[mediatailor_mixins.CfnLiveSourcePropsMixin.HttpPackageConfigurationProperty(
                path="path",
                source_group="sourceGroup",
                type="type"
            )],
            live_source_name="liveSourceName",
            source_location_name="sourceLocationName",
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
        props: typing.Union[CfnLiveSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaTailor::LiveSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34577fd59a072a532187d0f4a50343319df98689818687ea2e2e3f6bcb9a24cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__707748a2b131f5c78f00db8845451b8ac0059de4e8a4b05a3ad86134e8627ae3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa4514fcf806051e1919d669581d46817a89b8ab2930bceaeeb7b8179dcf583)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLiveSourceMixinProps:
        return typing.cast(CfnLiveSourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnLiveSourcePropsMixin.HttpPackageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path", "source_group": "sourceGroup", "type": "type"},
    )
    class HttpPackageConfigurationProperty:
        def __init__(
            self,
            *,
            path: typing.Optional[builtins.str] = None,
            source_group: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The HTTP package configuration properties for the requested VOD source.

            :param path: The relative path to the URL for this VOD source. This is combined with ``SourceLocation::HttpConfiguration::BaseUrl`` to form a valid URL.
            :param source_group: The name of the source group. This has to match one of the ``Channel::Outputs::SourceGroup`` .
            :param type: The streaming protocol for this package configuration. Supported values are ``HLS`` and ``DASH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-livesource-httppackageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                http_package_configuration_property = mediatailor_mixins.CfnLiveSourcePropsMixin.HttpPackageConfigurationProperty(
                    path="path",
                    source_group="sourceGroup",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fad498bff2b2af40630f3eb6bfe5a494a1d3f1a12829d9b7b19ea1199ccd6f38)
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument source_group", value=source_group, expected_type=type_hints["source_group"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if path is not None:
                self._values["path"] = path
            if source_group is not None:
                self._values["source_group"] = source_group
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The relative path to the URL for this VOD source.

            This is combined with ``SourceLocation::HttpConfiguration::BaseUrl`` to form a valid URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-livesource-httppackageconfiguration.html#cfn-mediatailor-livesource-httppackageconfiguration-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_group(self) -> typing.Optional[builtins.str]:
            '''The name of the source group.

            This has to match one of the ``Channel::Outputs::SourceGroup`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-livesource-httppackageconfiguration.html#cfn-mediatailor-livesource-httppackageconfiguration-sourcegroup
            '''
            result = self._values.get("source_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The streaming protocol for this package configuration.

            Supported values are ``HLS`` and ``DASH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-livesource-httppackageconfiguration.html#cfn-mediatailor-livesource-httppackageconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpPackageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnPlaybackConfigurationAdDecisionServerLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationAdDecisionServerLogs",
):
    '''Builder for CfnPlaybackConfigurationLogsMixin to generate AD_DECISION_SERVER_LOGS for CfnPlaybackConfiguration.

    :cloudformationResource: AWS::MediaTailor::PlaybackConfiguration
    :logType: AD_DECISION_SERVER_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
        
        cfn_playback_configuration_ad_decision_server_logs = mediatailor_mixins.CfnPlaybackConfigurationAdDecisionServerLogs()
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
    ) -> "CfnPlaybackConfigurationLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e86a052e20c8228bc093ef1e81663e21e26af1acdeb9ebd0590dc4ce4ef2b99)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnPlaybackConfigurationLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnPlaybackConfigurationLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a630ed534e9ef49e9fa722ba2673200de7833d9ce20ae36627f37365f9fa84ec)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnPlaybackConfigurationLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnPlaybackConfigurationLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08257b9b52bcc570545a1fda383c2af965d90755db227b2c6b2669a74fe72179)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnPlaybackConfigurationLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnPlaybackConfigurationLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationLogsMixin",
):
    '''Adds a new playback configuration to AWS Elemental MediaTailor .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html
    :cloudformationResource: AWS::MediaTailor::PlaybackConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_playback_configuration_logs_mixin = mediatailor_mixins.CfnPlaybackConfigurationLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::MediaTailor::PlaybackConfiguration``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be22dc5fdbd1bf53113a722cc11a9b40329325137f457b06c1a0e52a4e0453b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61be5ae7c09b88d8a3fae6f642df86bbdfadab120e49d7ce23b9ac0108b8f205)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ece1d228b98eb43999d1e5f071cce2aa5ba0d5b8637938930f2be61005ee29)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AD_DECISION_SERVER_LOGS")
    def AD_DECISION_SERVER_LOGS(cls) -> CfnPlaybackConfigurationAdDecisionServerLogs:
        return typing.cast(CfnPlaybackConfigurationAdDecisionServerLogs, jsii.sget(cls, "AD_DECISION_SERVER_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MANIFEST_SERVICE_LOGS")
    def MANIFEST_SERVICE_LOGS(cls) -> "CfnPlaybackConfigurationManifestServiceLogs":
        return typing.cast("CfnPlaybackConfigurationManifestServiceLogs", jsii.sget(cls, "MANIFEST_SERVICE_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TRANSCODE_LOGS")
    def TRANSCODE_LOGS(cls) -> "CfnPlaybackConfigurationTranscodeLogs":
        return typing.cast("CfnPlaybackConfigurationTranscodeLogs", jsii.sget(cls, "TRANSCODE_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


class CfnPlaybackConfigurationManifestServiceLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationManifestServiceLogs",
):
    '''Builder for CfnPlaybackConfigurationLogsMixin to generate MANIFEST_SERVICE_LOGS for CfnPlaybackConfiguration.

    :cloudformationResource: AWS::MediaTailor::PlaybackConfiguration
    :logType: MANIFEST_SERVICE_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
        
        cfn_playback_configuration_manifest_service_logs = mediatailor_mixins.CfnPlaybackConfigurationManifestServiceLogs()
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
    ) -> CfnPlaybackConfigurationLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__779bc1620506212603cd0bf2f441fc09f9538cdd5f24bc4a18f176705af08aa9)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnPlaybackConfigurationLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnPlaybackConfigurationLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885cfdc6db35b97c08c385af0249fa780966a96fe797af4141cf20392adcc5a6)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnPlaybackConfigurationLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnPlaybackConfigurationLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014a4750a71f835eca7d99b8d7e79bb5c2ecbdf8e2e3a2ea3109ee4208110f6b)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnPlaybackConfigurationLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ad_conditioning_configuration": "adConditioningConfiguration",
        "ad_decision_server_url": "adDecisionServerUrl",
        "avail_suppression": "availSuppression",
        "bumper": "bumper",
        "cdn_configuration": "cdnConfiguration",
        "configuration_aliases": "configurationAliases",
        "dash_configuration": "dashConfiguration",
        "hls_configuration": "hlsConfiguration",
        "insertion_mode": "insertionMode",
        "live_pre_roll_configuration": "livePreRollConfiguration",
        "log_configuration": "logConfiguration",
        "manifest_processing_rules": "manifestProcessingRules",
        "name": "name",
        "personalization_threshold_seconds": "personalizationThresholdSeconds",
        "slate_ad_url": "slateAdUrl",
        "tags": "tags",
        "transcode_profile_name": "transcodeProfileName",
        "video_content_source_url": "videoContentSourceUrl",
    },
)
class CfnPlaybackConfigurationMixinProps:
    def __init__(
        self,
        *,
        ad_conditioning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.AdConditioningConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ad_decision_server_url: typing.Optional[builtins.str] = None,
        avail_suppression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.AvailSuppressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        bumper: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.BumperProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cdn_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.CdnConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        configuration_aliases: typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
        dash_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.DashConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        hls_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.HlsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        insertion_mode: typing.Optional[builtins.str] = None,
        live_pre_roll_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.LivePreRollConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        manifest_processing_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.ManifestProcessingRulesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        personalization_threshold_seconds: typing.Optional[jsii.Number] = None,
        slate_ad_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        transcode_profile_name: typing.Optional[builtins.str] = None,
        video_content_source_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPlaybackConfigurationPropsMixin.

        :param ad_conditioning_configuration: The setting that indicates what conditioning MediaTailor will perform on ads that the ad decision server (ADS) returns, and what priority MediaTailor uses when inserting ads.
        :param ad_decision_server_url: The URL for the ad decision server (ADS). This includes the specification of static parameters and placeholders for dynamic parameters. AWS Elemental MediaTailor substitutes player-specific and session-specific parameters as needed when calling the ADS. Alternately, for testing you can provide a static VAST URL. The maximum length is 25,000 characters.
        :param avail_suppression: The configuration for avail suppression, also known as ad suppression. For more information about ad suppression, see `Ad Suppression <https://docs.aws.amazon.com/mediatailor/latest/ug/ad-behavior.html>`_ .
        :param bumper: The configuration for bumpers. Bumpers are short audio or video clips that play at the start or before the end of an ad break. To learn more about bumpers, see `Bumpers <https://docs.aws.amazon.com/mediatailor/latest/ug/bumpers.html>`_ .
        :param cdn_configuration: The configuration for using a content delivery network (CDN), like Amazon CloudFront, for content and ad segment management.
        :param configuration_aliases: The player parameters and aliases used as dynamic variables during session initialization. For more information, see `Domain Variables <https://docs.aws.amazon.com/mediatailor/latest/ug/variables-domain.html>`_ .
        :param dash_configuration: The configuration for a DASH source.
        :param hls_configuration: The configuration for HLS content.
        :param insertion_mode: The setting that controls whether players can use stitched or guided ad insertion. The default, ``STITCHED_ONLY`` , forces all player sessions to use stitched (server-side) ad insertion. Choosing ``PLAYER_SELECT`` allows players to select either stitched or guided ad insertion at session-initialization time. The default for players that do not specify an insertion mode is stitched.
        :param live_pre_roll_configuration: The configuration for pre-roll ad insertion.
        :param log_configuration: Defines where AWS Elemental MediaTailor sends logs for the playback configuration.
        :param manifest_processing_rules: The configuration for manifest processing rules. Manifest processing rules enable customization of the personalized manifests created by MediaTailor.
        :param name: The identifier for the playback configuration.
        :param personalization_threshold_seconds: Defines the maximum duration of underfilled ad time (in seconds) allowed in an ad break. If the duration of underfilled ad time exceeds the personalization threshold, then the personalization of the ad break is abandoned and the underlying content is shown. This feature applies to *ad replacement* in live and VOD streams, rather than ad insertion, because it relies on an underlying content stream. For more information about ad break behavior, including ad replacement and insertion, see `Ad Behavior in AWS Elemental MediaTailor <https://docs.aws.amazon.com/mediatailor/latest/ug/ad-behavior.html>`_ .
        :param slate_ad_url: The URL for a video asset to transcode and use to fill in time that's not used by ads. AWS Elemental MediaTailor shows the slate to fill in gaps in media content. Configuring the slate is optional for non-VPAID playback configurations. For VPAID, the slate is required because MediaTailor provides it in the slots designated for dynamic ad content. The slate must be a high-quality asset that contains both audio and video.
        :param tags: The tags to assign to the playback configuration. Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see `Tagging AWS Elemental MediaTailor Resources <https://docs.aws.amazon.com/mediatailor/latest/ug/tagging.html>`_ .
        :param transcode_profile_name: The name that is used to associate this playback configuration with a custom transcode profile. This overrides the dynamic transcoding defaults of MediaTailor. Use this only if you have already set up custom profiles with the help of AWS Support.
        :param video_content_source_url: The URL prefix for the parent manifest for the stream, minus the asset ID. The maximum length is 512 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
            
            # configuration_aliases: Any
            
            cfn_playback_configuration_mixin_props = mediatailor_mixins.CfnPlaybackConfigurationMixinProps(
                ad_conditioning_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdConditioningConfigurationProperty(
                    streaming_media_file_conditioning="streamingMediaFileConditioning"
                ),
                ad_decision_server_url="adDecisionServerUrl",
                avail_suppression=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AvailSuppressionProperty(
                    fill_policy="fillPolicy",
                    mode="mode",
                    value="value"
                ),
                bumper=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.BumperProperty(
                    end_url="endUrl",
                    start_url="startUrl"
                ),
                cdn_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.CdnConfigurationProperty(
                    ad_segment_url_prefix="adSegmentUrlPrefix",
                    content_segment_url_prefix="contentSegmentUrlPrefix"
                ),
                configuration_aliases={
                    "configuration_aliases_key": configuration_aliases
                },
                dash_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.DashConfigurationProperty(
                    manifest_endpoint_prefix="manifestEndpointPrefix",
                    mpd_location="mpdLocation",
                    origin_manifest_type="originManifestType"
                ),
                hls_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.HlsConfigurationProperty(
                    manifest_endpoint_prefix="manifestEndpointPrefix"
                ),
                insertion_mode="insertionMode",
                live_pre_roll_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.LivePreRollConfigurationProperty(
                    ad_decision_server_url="adDecisionServerUrl",
                    max_duration_seconds=123
                ),
                log_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.LogConfigurationProperty(
                    ads_interaction_log=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdsInteractionLogProperty(
                        exclude_event_types=["excludeEventTypes"],
                        publish_opt_in_event_types=["publishOptInEventTypes"]
                    ),
                    enabled_logging_strategies=["enabledLoggingStrategies"],
                    manifest_service_interaction_log=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.ManifestServiceInteractionLogProperty(
                        exclude_event_types=["excludeEventTypes"]
                    ),
                    percent_enabled=123
                ),
                manifest_processing_rules=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.ManifestProcessingRulesProperty(
                    ad_marker_passthrough=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdMarkerPassthroughProperty(
                        enabled=False
                    )
                ),
                name="name",
                personalization_threshold_seconds=123,
                slate_ad_url="slateAdUrl",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                transcode_profile_name="transcodeProfileName",
                video_content_source_url="videoContentSourceUrl"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4e0915d792d710443769766e32410b0213a19153a8b76c904d6bc433c44702)
            check_type(argname="argument ad_conditioning_configuration", value=ad_conditioning_configuration, expected_type=type_hints["ad_conditioning_configuration"])
            check_type(argname="argument ad_decision_server_url", value=ad_decision_server_url, expected_type=type_hints["ad_decision_server_url"])
            check_type(argname="argument avail_suppression", value=avail_suppression, expected_type=type_hints["avail_suppression"])
            check_type(argname="argument bumper", value=bumper, expected_type=type_hints["bumper"])
            check_type(argname="argument cdn_configuration", value=cdn_configuration, expected_type=type_hints["cdn_configuration"])
            check_type(argname="argument configuration_aliases", value=configuration_aliases, expected_type=type_hints["configuration_aliases"])
            check_type(argname="argument dash_configuration", value=dash_configuration, expected_type=type_hints["dash_configuration"])
            check_type(argname="argument hls_configuration", value=hls_configuration, expected_type=type_hints["hls_configuration"])
            check_type(argname="argument insertion_mode", value=insertion_mode, expected_type=type_hints["insertion_mode"])
            check_type(argname="argument live_pre_roll_configuration", value=live_pre_roll_configuration, expected_type=type_hints["live_pre_roll_configuration"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument manifest_processing_rules", value=manifest_processing_rules, expected_type=type_hints["manifest_processing_rules"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument personalization_threshold_seconds", value=personalization_threshold_seconds, expected_type=type_hints["personalization_threshold_seconds"])
            check_type(argname="argument slate_ad_url", value=slate_ad_url, expected_type=type_hints["slate_ad_url"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transcode_profile_name", value=transcode_profile_name, expected_type=type_hints["transcode_profile_name"])
            check_type(argname="argument video_content_source_url", value=video_content_source_url, expected_type=type_hints["video_content_source_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ad_conditioning_configuration is not None:
            self._values["ad_conditioning_configuration"] = ad_conditioning_configuration
        if ad_decision_server_url is not None:
            self._values["ad_decision_server_url"] = ad_decision_server_url
        if avail_suppression is not None:
            self._values["avail_suppression"] = avail_suppression
        if bumper is not None:
            self._values["bumper"] = bumper
        if cdn_configuration is not None:
            self._values["cdn_configuration"] = cdn_configuration
        if configuration_aliases is not None:
            self._values["configuration_aliases"] = configuration_aliases
        if dash_configuration is not None:
            self._values["dash_configuration"] = dash_configuration
        if hls_configuration is not None:
            self._values["hls_configuration"] = hls_configuration
        if insertion_mode is not None:
            self._values["insertion_mode"] = insertion_mode
        if live_pre_roll_configuration is not None:
            self._values["live_pre_roll_configuration"] = live_pre_roll_configuration
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if manifest_processing_rules is not None:
            self._values["manifest_processing_rules"] = manifest_processing_rules
        if name is not None:
            self._values["name"] = name
        if personalization_threshold_seconds is not None:
            self._values["personalization_threshold_seconds"] = personalization_threshold_seconds
        if slate_ad_url is not None:
            self._values["slate_ad_url"] = slate_ad_url
        if tags is not None:
            self._values["tags"] = tags
        if transcode_profile_name is not None:
            self._values["transcode_profile_name"] = transcode_profile_name
        if video_content_source_url is not None:
            self._values["video_content_source_url"] = video_content_source_url

    @builtins.property
    def ad_conditioning_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.AdConditioningConfigurationProperty"]]:
        '''The setting that indicates what conditioning MediaTailor will perform on ads that the ad decision server (ADS) returns, and what priority MediaTailor uses when inserting ads.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-adconditioningconfiguration
        '''
        result = self._values.get("ad_conditioning_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.AdConditioningConfigurationProperty"]], result)

    @builtins.property
    def ad_decision_server_url(self) -> typing.Optional[builtins.str]:
        '''The URL for the ad decision server (ADS).

        This includes the specification of static parameters and placeholders for dynamic parameters. AWS Elemental MediaTailor substitutes player-specific and session-specific parameters as needed when calling the ADS. Alternately, for testing you can provide a static VAST URL. The maximum length is 25,000 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-addecisionserverurl
        '''
        result = self._values.get("ad_decision_server_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def avail_suppression(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.AvailSuppressionProperty"]]:
        '''The configuration for avail suppression, also known as ad suppression.

        For more information about ad suppression, see `Ad Suppression <https://docs.aws.amazon.com/mediatailor/latest/ug/ad-behavior.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-availsuppression
        '''
        result = self._values.get("avail_suppression")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.AvailSuppressionProperty"]], result)

    @builtins.property
    def bumper(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.BumperProperty"]]:
        '''The configuration for bumpers.

        Bumpers are short audio or video clips that play at the start or before the end of an ad break. To learn more about bumpers, see `Bumpers <https://docs.aws.amazon.com/mediatailor/latest/ug/bumpers.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-bumper
        '''
        result = self._values.get("bumper")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.BumperProperty"]], result)

    @builtins.property
    def cdn_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.CdnConfigurationProperty"]]:
        '''The configuration for using a content delivery network (CDN), like Amazon CloudFront, for content and ad segment management.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-cdnconfiguration
        '''
        result = self._values.get("cdn_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.CdnConfigurationProperty"]], result)

    @builtins.property
    def configuration_aliases(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Any], _aws_cdk_ceddda9d.IResolvable]]:
        '''The player parameters and aliases used as dynamic variables during session initialization.

        For more information, see `Domain Variables <https://docs.aws.amazon.com/mediatailor/latest/ug/variables-domain.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-configurationaliases
        '''
        result = self._values.get("configuration_aliases")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Any], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def dash_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.DashConfigurationProperty"]]:
        '''The configuration for a DASH source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-dashconfiguration
        '''
        result = self._values.get("dash_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.DashConfigurationProperty"]], result)

    @builtins.property
    def hls_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.HlsConfigurationProperty"]]:
        '''The configuration for HLS content.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-hlsconfiguration
        '''
        result = self._values.get("hls_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.HlsConfigurationProperty"]], result)

    @builtins.property
    def insertion_mode(self) -> typing.Optional[builtins.str]:
        '''The setting that controls whether players can use stitched or guided ad insertion.

        The default, ``STITCHED_ONLY`` , forces all player sessions to use stitched (server-side) ad insertion. Choosing ``PLAYER_SELECT`` allows players to select either stitched or guided ad insertion at session-initialization time. The default for players that do not specify an insertion mode is stitched.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-insertionmode
        '''
        result = self._values.get("insertion_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def live_pre_roll_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.LivePreRollConfigurationProperty"]]:
        '''The configuration for pre-roll ad insertion.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-liveprerollconfiguration
        '''
        result = self._values.get("live_pre_roll_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.LivePreRollConfigurationProperty"]], result)

    @builtins.property
    def log_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.LogConfigurationProperty"]]:
        '''Defines where AWS Elemental MediaTailor sends logs for the playback configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-logconfiguration
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.LogConfigurationProperty"]], result)

    @builtins.property
    def manifest_processing_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.ManifestProcessingRulesProperty"]]:
        '''The configuration for manifest processing rules.

        Manifest processing rules enable customization of the personalized manifests created by MediaTailor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-manifestprocessingrules
        '''
        result = self._values.get("manifest_processing_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.ManifestProcessingRulesProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The identifier for the playback configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def personalization_threshold_seconds(self) -> typing.Optional[jsii.Number]:
        '''Defines the maximum duration of underfilled ad time (in seconds) allowed in an ad break.

        If the duration of underfilled ad time exceeds the personalization threshold, then the personalization of the ad break is abandoned and the underlying content is shown. This feature applies to *ad replacement* in live and VOD streams, rather than ad insertion, because it relies on an underlying content stream. For more information about ad break behavior, including ad replacement and insertion, see `Ad Behavior in AWS Elemental MediaTailor <https://docs.aws.amazon.com/mediatailor/latest/ug/ad-behavior.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-personalizationthresholdseconds
        '''
        result = self._values.get("personalization_threshold_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def slate_ad_url(self) -> typing.Optional[builtins.str]:
        '''The URL for a video asset to transcode and use to fill in time that's not used by ads.

        AWS Elemental MediaTailor shows the slate to fill in gaps in media content. Configuring the slate is optional for non-VPAID playback configurations. For VPAID, the slate is required because MediaTailor provides it in the slots designated for dynamic ad content. The slate must be a high-quality asset that contains both audio and video.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-slateadurl
        '''
        result = self._values.get("slate_ad_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to the playback configuration.

        Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see `Tagging AWS Elemental MediaTailor Resources <https://docs.aws.amazon.com/mediatailor/latest/ug/tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def transcode_profile_name(self) -> typing.Optional[builtins.str]:
        '''The name that is used to associate this playback configuration with a custom transcode profile.

        This overrides the dynamic transcoding defaults of MediaTailor. Use this only if you have already set up custom profiles with the help of AWS Support.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-transcodeprofilename
        '''
        result = self._values.get("transcode_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def video_content_source_url(self) -> typing.Optional[builtins.str]:
        '''The URL prefix for the parent manifest for the stream, minus the asset ID.

        The maximum length is 512 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-videocontentsourceurl
        '''
        result = self._values.get("video_content_source_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlaybackConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPlaybackConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin",
):
    '''Adds a new playback configuration to AWS Elemental MediaTailor .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html
    :cloudformationResource: AWS::MediaTailor::PlaybackConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
        
        # configuration_aliases: Any
        
        cfn_playback_configuration_props_mixin = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin(mediatailor_mixins.CfnPlaybackConfigurationMixinProps(
            ad_conditioning_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdConditioningConfigurationProperty(
                streaming_media_file_conditioning="streamingMediaFileConditioning"
            ),
            ad_decision_server_url="adDecisionServerUrl",
            avail_suppression=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AvailSuppressionProperty(
                fill_policy="fillPolicy",
                mode="mode",
                value="value"
            ),
            bumper=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.BumperProperty(
                end_url="endUrl",
                start_url="startUrl"
            ),
            cdn_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.CdnConfigurationProperty(
                ad_segment_url_prefix="adSegmentUrlPrefix",
                content_segment_url_prefix="contentSegmentUrlPrefix"
            ),
            configuration_aliases={
                "configuration_aliases_key": configuration_aliases
            },
            dash_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.DashConfigurationProperty(
                manifest_endpoint_prefix="manifestEndpointPrefix",
                mpd_location="mpdLocation",
                origin_manifest_type="originManifestType"
            ),
            hls_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.HlsConfigurationProperty(
                manifest_endpoint_prefix="manifestEndpointPrefix"
            ),
            insertion_mode="insertionMode",
            live_pre_roll_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.LivePreRollConfigurationProperty(
                ad_decision_server_url="adDecisionServerUrl",
                max_duration_seconds=123
            ),
            log_configuration=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.LogConfigurationProperty(
                ads_interaction_log=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdsInteractionLogProperty(
                    exclude_event_types=["excludeEventTypes"],
                    publish_opt_in_event_types=["publishOptInEventTypes"]
                ),
                enabled_logging_strategies=["enabledLoggingStrategies"],
                manifest_service_interaction_log=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.ManifestServiceInteractionLogProperty(
                    exclude_event_types=["excludeEventTypes"]
                ),
                percent_enabled=123
            ),
            manifest_processing_rules=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.ManifestProcessingRulesProperty(
                ad_marker_passthrough=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdMarkerPassthroughProperty(
                    enabled=False
                )
            ),
            name="name",
            personalization_threshold_seconds=123,
            slate_ad_url="slateAdUrl",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            transcode_profile_name="transcodeProfileName",
            video_content_source_url="videoContentSourceUrl"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPlaybackConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaTailor::PlaybackConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7be1974faebeb1232ec780232a7c52cc12ef3139bc0f35844797fbc68a76a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9391525138759126e336e5f4fd7ec222b2bfe404aa119d4f434588ee46a7163)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68e20409cbd820e6ddbccb5556c91bde9a4ed6cc6bfc5cebf0f46e992d134da)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPlaybackConfigurationMixinProps:
        return typing.cast(CfnPlaybackConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.AdConditioningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "streaming_media_file_conditioning": "streamingMediaFileConditioning",
        },
    )
    class AdConditioningConfigurationProperty:
        def __init__(
            self,
            *,
            streaming_media_file_conditioning: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The setting that indicates what conditioning MediaTailor will perform on ads that the ad decision server (ADS) returns.

            :param streaming_media_file_conditioning: For ads that have media files with streaming delivery and supported file extensions, indicates what transcoding action MediaTailor takes when it first receives these ads from the ADS. ``TRANSCODE`` indicates that MediaTailor must transcode the ads. ``NONE`` indicates that you have already transcoded the ads outside of MediaTailor and don't need them transcoded as part of the ad insertion workflow. For more information about ad conditioning see `Using preconditioned ads <https://docs.aws.amazon.com/mediatailor/latest/ug/precondition-ads.html>`_ in the AWS Elemental MediaTailor user guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-adconditioningconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                ad_conditioning_configuration_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdConditioningConfigurationProperty(
                    streaming_media_file_conditioning="streamingMediaFileConditioning"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a88050e638370f9f01c6dc3bc48f81b355bfb55969e44fa46303e8cec56fc661)
                check_type(argname="argument streaming_media_file_conditioning", value=streaming_media_file_conditioning, expected_type=type_hints["streaming_media_file_conditioning"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if streaming_media_file_conditioning is not None:
                self._values["streaming_media_file_conditioning"] = streaming_media_file_conditioning

        @builtins.property
        def streaming_media_file_conditioning(self) -> typing.Optional[builtins.str]:
            '''For ads that have media files with streaming delivery and supported file extensions, indicates what transcoding action MediaTailor takes when it first receives these ads from the ADS.

            ``TRANSCODE`` indicates that MediaTailor must transcode the ads. ``NONE`` indicates that you have already transcoded the ads outside of MediaTailor and don't need them transcoded as part of the ad insertion workflow. For more information about ad conditioning see `Using preconditioned ads <https://docs.aws.amazon.com/mediatailor/latest/ug/precondition-ads.html>`_ in the AWS Elemental MediaTailor user guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-adconditioningconfiguration.html#cfn-mediatailor-playbackconfiguration-adconditioningconfiguration-streamingmediafileconditioning
            '''
            result = self._values.get("streaming_media_file_conditioning")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdConditioningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.AdMarkerPassthroughProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class AdMarkerPassthroughProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''For HLS, when set to ``true`` , MediaTailor passes through ``EXT-X-CUE-IN`` , ``EXT-X-CUE-OUT`` , and ``EXT-X-SPLICEPOINT-SCTE35`` ad markers from the origin manifest to the MediaTailor personalized manifest.

            No logic is applied to these ad markers. For example, if ``EXT-X-CUE-OUT`` has a value of ``60`` , but no ads are filled for that ad break, MediaTailor will not set the value to ``0`` .

            :param enabled: Enables ad marker passthrough for your configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-admarkerpassthrough.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                ad_marker_passthrough_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdMarkerPassthroughProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d86ca02d9e7093565eee46c0beffc68000d1aa8f7ab63019d1a97faf0bbd11b)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables ad marker passthrough for your configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-admarkerpassthrough.html#cfn-mediatailor-playbackconfiguration-admarkerpassthrough-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdMarkerPassthroughProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.AdsInteractionLogProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_event_types": "excludeEventTypes",
            "publish_opt_in_event_types": "publishOptInEventTypes",
        },
    )
    class AdsInteractionLogProperty:
        def __init__(
            self,
            *,
            exclude_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            publish_opt_in_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Settings for customizing what events are included in logs for interactions with the ad decision server (ADS).

            For more information about ADS logs, inlcuding descriptions of the event types, see `MediaTailor ADS logs description and event types <https://docs.aws.amazon.com/mediatailor/latest/ug/ads-log-format.html>`_ in AWS Elemental MediaTailor User Guide.

            :param exclude_event_types: Indicates that MediaTailor won't emit the selected events in the logs for playback sessions that are initialized with this configuration.
            :param publish_opt_in_event_types: Indicates that MediaTailor emits ``RAW_ADS_RESPONSE`` logs for playback sessions that are initialized with this configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-adsinteractionlog.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                ads_interaction_log_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdsInteractionLogProperty(
                    exclude_event_types=["excludeEventTypes"],
                    publish_opt_in_event_types=["publishOptInEventTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__10563bbc541f982a32cde4bf56ed8e938d4f6173208e0e4e26f16da6bf4ed9ed)
                check_type(argname="argument exclude_event_types", value=exclude_event_types, expected_type=type_hints["exclude_event_types"])
                check_type(argname="argument publish_opt_in_event_types", value=publish_opt_in_event_types, expected_type=type_hints["publish_opt_in_event_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude_event_types is not None:
                self._values["exclude_event_types"] = exclude_event_types
            if publish_opt_in_event_types is not None:
                self._values["publish_opt_in_event_types"] = publish_opt_in_event_types

        @builtins.property
        def exclude_event_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates that MediaTailor won't emit the selected events in the logs for playback sessions that are initialized with this configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-adsinteractionlog.html#cfn-mediatailor-playbackconfiguration-adsinteractionlog-excludeeventtypes
            '''
            result = self._values.get("exclude_event_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def publish_opt_in_event_types(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates that MediaTailor emits ``RAW_ADS_RESPONSE`` logs for playback sessions that are initialized with this configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-adsinteractionlog.html#cfn-mediatailor-playbackconfiguration-adsinteractionlog-publishoptineventtypes
            '''
            result = self._values.get("publish_opt_in_event_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdsInteractionLogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.AvailSuppressionProperty",
        jsii_struct_bases=[],
        name_mapping={"fill_policy": "fillPolicy", "mode": "mode", "value": "value"},
    )
    class AvailSuppressionProperty:
        def __init__(
            self,
            *,
            fill_policy: typing.Optional[builtins.str] = None,
            mode: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for avail suppression, also known as ad suppression.

            For more information about ad suppression, see `Ad Suppression <https://docs.aws.amazon.com/mediatailor/latest/ug/ad-behavior.html>`_ .

            :param fill_policy: Defines the policy to apply to the avail suppression mode. ``BEHIND_LIVE_EDGE`` will always use the full avail suppression policy. ``AFTER_LIVE_EDGE`` mode can be used to invoke partial ad break fills when a session starts mid-break.
            :param mode: Sets the ad suppression mode. By default, ad suppression is off and all ad breaks are filled with ads or slate. When Mode is set to ``BEHIND_LIVE_EDGE`` , ad suppression is active and MediaTailor won't fill ad breaks on or behind the ad suppression Value time in the manifest lookback window. When Mode is set to ``AFTER_LIVE_EDGE`` , ad suppression is active and MediaTailor won't fill ad breaks that are within the live edge plus the avail suppression value.
            :param value: A live edge offset time in HH:MM:SS. MediaTailor won't fill ad breaks on or behind this time in the manifest lookback window. If Value is set to 00:00:00, it is in sync with the live edge, and MediaTailor won't fill any ad breaks on or behind the live edge. If you set a Value time, MediaTailor won't fill any ad breaks on or behind this time in the manifest lookback window. For example, if you set 00:45:00, then MediaTailor will fill ad breaks that occur within 45 minutes behind the live edge, but won't fill ad breaks on or behind 45 minutes behind the live edge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-availsuppression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                avail_suppression_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AvailSuppressionProperty(
                    fill_policy="fillPolicy",
                    mode="mode",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a8e624062e06214c310f853f44ebaea3a7a0bf9cd3dda3fc2b6aadda5d9eb1d)
                check_type(argname="argument fill_policy", value=fill_policy, expected_type=type_hints["fill_policy"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fill_policy is not None:
                self._values["fill_policy"] = fill_policy
            if mode is not None:
                self._values["mode"] = mode
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def fill_policy(self) -> typing.Optional[builtins.str]:
            '''Defines the policy to apply to the avail suppression mode.

            ``BEHIND_LIVE_EDGE`` will always use the full avail suppression policy. ``AFTER_LIVE_EDGE`` mode can be used to invoke partial ad break fills when a session starts mid-break.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-availsuppression.html#cfn-mediatailor-playbackconfiguration-availsuppression-fillpolicy
            '''
            result = self._values.get("fill_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''Sets the ad suppression mode.

            By default, ad suppression is off and all ad breaks are filled with ads or slate. When Mode is set to ``BEHIND_LIVE_EDGE`` , ad suppression is active and MediaTailor won't fill ad breaks on or behind the ad suppression Value time in the manifest lookback window. When Mode is set to ``AFTER_LIVE_EDGE`` , ad suppression is active and MediaTailor won't fill ad breaks that are within the live edge plus the avail suppression value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-availsuppression.html#cfn-mediatailor-playbackconfiguration-availsuppression-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A live edge offset time in HH:MM:SS.

            MediaTailor won't fill ad breaks on or behind this time in the manifest lookback window. If Value is set to 00:00:00, it is in sync with the live edge, and MediaTailor won't fill any ad breaks on or behind the live edge. If you set a Value time, MediaTailor won't fill any ad breaks on or behind this time in the manifest lookback window. For example, if you set 00:45:00, then MediaTailor will fill ad breaks that occur within 45 minutes behind the live edge, but won't fill ad breaks on or behind 45 minutes behind the live edge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-availsuppression.html#cfn-mediatailor-playbackconfiguration-availsuppression-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AvailSuppressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.BumperProperty",
        jsii_struct_bases=[],
        name_mapping={"end_url": "endUrl", "start_url": "startUrl"},
    )
    class BumperProperty:
        def __init__(
            self,
            *,
            end_url: typing.Optional[builtins.str] = None,
            start_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for bumpers.

            Bumpers are short audio or video clips that play at the start or before the end of an ad break. To learn more about bumpers, see `Bumpers <https://docs.aws.amazon.com/mediatailor/latest/ug/bumpers.html>`_ .

            :param end_url: The URL for the end bumper asset.
            :param start_url: The URL for the start bumper asset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-bumper.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                bumper_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.BumperProperty(
                    end_url="endUrl",
                    start_url="startUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ed629358d76c3d2947f4a0eceeab210bc1a5438c2d5502f7c049c6848fd0157)
                check_type(argname="argument end_url", value=end_url, expected_type=type_hints["end_url"])
                check_type(argname="argument start_url", value=start_url, expected_type=type_hints["start_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_url is not None:
                self._values["end_url"] = end_url
            if start_url is not None:
                self._values["start_url"] = start_url

        @builtins.property
        def end_url(self) -> typing.Optional[builtins.str]:
            '''The URL for the end bumper asset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-bumper.html#cfn-mediatailor-playbackconfiguration-bumper-endurl
            '''
            result = self._values.get("end_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_url(self) -> typing.Optional[builtins.str]:
            '''The URL for the start bumper asset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-bumper.html#cfn-mediatailor-playbackconfiguration-bumper-starturl
            '''
            result = self._values.get("start_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BumperProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.CdnConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_segment_url_prefix": "adSegmentUrlPrefix",
            "content_segment_url_prefix": "contentSegmentUrlPrefix",
        },
    )
    class CdnConfigurationProperty:
        def __init__(
            self,
            *,
            ad_segment_url_prefix: typing.Optional[builtins.str] = None,
            content_segment_url_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for using a content delivery network (CDN), like Amazon CloudFront, for content and ad segment management.

            :param ad_segment_url_prefix: A non-default content delivery network (CDN) to serve ad segments. By default, AWS Elemental MediaTailor uses Amazon CloudFront with default cache settings as its CDN for ad segments. To set up an alternate CDN, create a rule in your CDN for the origin ads.mediatailor. ** .amazonaws.com. Then specify the rule's name in this ``AdSegmentUrlPrefix`` . When AWS Elemental MediaTailor serves a manifest, it reports your CDN as the source for ad segments.
            :param content_segment_url_prefix: A content delivery network (CDN) to cache content segments, so that content requests don’t always have to go to the origin server. First, create a rule in your CDN for the content segment origin server. Then specify the rule's name in this ``ContentSegmentUrlPrefix`` . When AWS Elemental MediaTailor serves a manifest, it reports your CDN as the source for content segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-cdnconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                cdn_configuration_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.CdnConfigurationProperty(
                    ad_segment_url_prefix="adSegmentUrlPrefix",
                    content_segment_url_prefix="contentSegmentUrlPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1744fff035bb2f15d4e9d3e914a6b755c7690656779ace6a5072f9ffd172598b)
                check_type(argname="argument ad_segment_url_prefix", value=ad_segment_url_prefix, expected_type=type_hints["ad_segment_url_prefix"])
                check_type(argname="argument content_segment_url_prefix", value=content_segment_url_prefix, expected_type=type_hints["content_segment_url_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_segment_url_prefix is not None:
                self._values["ad_segment_url_prefix"] = ad_segment_url_prefix
            if content_segment_url_prefix is not None:
                self._values["content_segment_url_prefix"] = content_segment_url_prefix

        @builtins.property
        def ad_segment_url_prefix(self) -> typing.Optional[builtins.str]:
            '''A non-default content delivery network (CDN) to serve ad segments.

            By default, AWS Elemental MediaTailor uses Amazon CloudFront with default cache settings as its CDN for ad segments. To set up an alternate CDN, create a rule in your CDN for the origin ads.mediatailor. ** .amazonaws.com. Then specify the rule's name in this ``AdSegmentUrlPrefix`` . When AWS Elemental MediaTailor serves a manifest, it reports your CDN as the source for ad segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-cdnconfiguration.html#cfn-mediatailor-playbackconfiguration-cdnconfiguration-adsegmenturlprefix
            '''
            result = self._values.get("ad_segment_url_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def content_segment_url_prefix(self) -> typing.Optional[builtins.str]:
            '''A content delivery network (CDN) to cache content segments, so that content requests don’t always have to go to the origin server.

            First, create a rule in your CDN for the content segment origin server. Then specify the rule's name in this ``ContentSegmentUrlPrefix`` . When AWS Elemental MediaTailor serves a manifest, it reports your CDN as the source for content segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-cdnconfiguration.html#cfn-mediatailor-playbackconfiguration-cdnconfiguration-contentsegmenturlprefix
            '''
            result = self._values.get("content_segment_url_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CdnConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.DashConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "manifest_endpoint_prefix": "manifestEndpointPrefix",
            "mpd_location": "mpdLocation",
            "origin_manifest_type": "originManifestType",
        },
    )
    class DashConfigurationProperty:
        def __init__(
            self,
            *,
            manifest_endpoint_prefix: typing.Optional[builtins.str] = None,
            mpd_location: typing.Optional[builtins.str] = None,
            origin_manifest_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for DASH content.

            :param manifest_endpoint_prefix: The URL generated by MediaTailor to initiate a playback session. The session uses server-side reporting. This setting is ignored in PUT operations.
            :param mpd_location: The setting that controls whether MediaTailor includes the Location tag in DASH manifests. MediaTailor populates the Location tag with the URL for manifest update requests, to be used by players that don't support sticky redirects. Disable this if you have CDN routing rules set up for accessing MediaTailor manifests, and you are either using client-side reporting or your players support sticky HTTP redirects. Valid values are ``DISABLED`` and ``EMT_DEFAULT`` . The ``EMT_DEFAULT`` setting enables the inclusion of the tag and is the default value.
            :param origin_manifest_type: The setting that controls whether MediaTailor handles manifests from the origin server as multi-period manifests or single-period manifests. If your origin server produces single-period manifests, set this to ``SINGLE_PERIOD`` . The default setting is ``MULTI_PERIOD`` . For multi-period manifests, omit this setting or set it to ``MULTI_PERIOD`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-dashconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                dash_configuration_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.DashConfigurationProperty(
                    manifest_endpoint_prefix="manifestEndpointPrefix",
                    mpd_location="mpdLocation",
                    origin_manifest_type="originManifestType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3bb546d131215baef2043d19564ae6df67fc9f2f3584efe67e5459ea77c0ea0)
                check_type(argname="argument manifest_endpoint_prefix", value=manifest_endpoint_prefix, expected_type=type_hints["manifest_endpoint_prefix"])
                check_type(argname="argument mpd_location", value=mpd_location, expected_type=type_hints["mpd_location"])
                check_type(argname="argument origin_manifest_type", value=origin_manifest_type, expected_type=type_hints["origin_manifest_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if manifest_endpoint_prefix is not None:
                self._values["manifest_endpoint_prefix"] = manifest_endpoint_prefix
            if mpd_location is not None:
                self._values["mpd_location"] = mpd_location
            if origin_manifest_type is not None:
                self._values["origin_manifest_type"] = origin_manifest_type

        @builtins.property
        def manifest_endpoint_prefix(self) -> typing.Optional[builtins.str]:
            '''The URL generated by MediaTailor to initiate a playback session.

            The session uses server-side reporting. This setting is ignored in PUT operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-dashconfiguration.html#cfn-mediatailor-playbackconfiguration-dashconfiguration-manifestendpointprefix
            '''
            result = self._values.get("manifest_endpoint_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mpd_location(self) -> typing.Optional[builtins.str]:
            '''The setting that controls whether MediaTailor includes the Location tag in DASH manifests.

            MediaTailor populates the Location tag with the URL for manifest update requests, to be used by players that don't support sticky redirects. Disable this if you have CDN routing rules set up for accessing MediaTailor manifests, and you are either using client-side reporting or your players support sticky HTTP redirects. Valid values are ``DISABLED`` and ``EMT_DEFAULT`` . The ``EMT_DEFAULT`` setting enables the inclusion of the tag and is the default value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-dashconfiguration.html#cfn-mediatailor-playbackconfiguration-dashconfiguration-mpdlocation
            '''
            result = self._values.get("mpd_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def origin_manifest_type(self) -> typing.Optional[builtins.str]:
            '''The setting that controls whether MediaTailor handles manifests from the origin server as multi-period manifests or single-period manifests.

            If your origin server produces single-period manifests, set this to ``SINGLE_PERIOD`` . The default setting is ``MULTI_PERIOD`` . For multi-period manifests, omit this setting or set it to ``MULTI_PERIOD`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-dashconfiguration.html#cfn-mediatailor-playbackconfiguration-dashconfiguration-originmanifesttype
            '''
            result = self._values.get("origin_manifest_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.HlsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"manifest_endpoint_prefix": "manifestEndpointPrefix"},
    )
    class HlsConfigurationProperty:
        def __init__(
            self,
            *,
            manifest_endpoint_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for HLS content.

            :param manifest_endpoint_prefix: The URL that is used to initiate a playback session for devices that support Apple HLS. The session uses server-side reporting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-hlsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                hls_configuration_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.HlsConfigurationProperty(
                    manifest_endpoint_prefix="manifestEndpointPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__acf83506e20e29f9dea14bf5ac12cd3282ed646ee913fcc946ba6bee59a582d4)
                check_type(argname="argument manifest_endpoint_prefix", value=manifest_endpoint_prefix, expected_type=type_hints["manifest_endpoint_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if manifest_endpoint_prefix is not None:
                self._values["manifest_endpoint_prefix"] = manifest_endpoint_prefix

        @builtins.property
        def manifest_endpoint_prefix(self) -> typing.Optional[builtins.str]:
            '''The URL that is used to initiate a playback session for devices that support Apple HLS.

            The session uses server-side reporting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-hlsconfiguration.html#cfn-mediatailor-playbackconfiguration-hlsconfiguration-manifestendpointprefix
            '''
            result = self._values.get("manifest_endpoint_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.LivePreRollConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_decision_server_url": "adDecisionServerUrl",
            "max_duration_seconds": "maxDurationSeconds",
        },
    )
    class LivePreRollConfigurationProperty:
        def __init__(
            self,
            *,
            ad_decision_server_url: typing.Optional[builtins.str] = None,
            max_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration for pre-roll ad insertion.

            :param ad_decision_server_url: The URL for the ad decision server (ADS) for pre-roll ads. This includes the specification of static parameters and placeholders for dynamic parameters. AWS Elemental MediaTailor substitutes player-specific and session-specific parameters as needed when calling the ADS. Alternately, for testing, you can provide a static VAST URL. The maximum length is 25,000 characters.
            :param max_duration_seconds: The maximum allowed duration for the pre-roll ad avail. AWS Elemental MediaTailor won't play pre-roll ads to exceed this duration, regardless of the total duration of ads that the ADS returns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-liveprerollconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                live_pre_roll_configuration_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.LivePreRollConfigurationProperty(
                    ad_decision_server_url="adDecisionServerUrl",
                    max_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__123b272c4357828e6a77159b810c08d7aa3e178e560ec39a77156172b4f74ae9)
                check_type(argname="argument ad_decision_server_url", value=ad_decision_server_url, expected_type=type_hints["ad_decision_server_url"])
                check_type(argname="argument max_duration_seconds", value=max_duration_seconds, expected_type=type_hints["max_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_decision_server_url is not None:
                self._values["ad_decision_server_url"] = ad_decision_server_url
            if max_duration_seconds is not None:
                self._values["max_duration_seconds"] = max_duration_seconds

        @builtins.property
        def ad_decision_server_url(self) -> typing.Optional[builtins.str]:
            '''The URL for the ad decision server (ADS) for pre-roll ads.

            This includes the specification of static parameters and placeholders for dynamic parameters. AWS Elemental MediaTailor substitutes player-specific and session-specific parameters as needed when calling the ADS. Alternately, for testing, you can provide a static VAST URL. The maximum length is 25,000 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-liveprerollconfiguration.html#cfn-mediatailor-playbackconfiguration-liveprerollconfiguration-addecisionserverurl
            '''
            result = self._values.get("ad_decision_server_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum allowed duration for the pre-roll ad avail.

            AWS Elemental MediaTailor won't play pre-roll ads to exceed this duration, regardless of the total duration of ads that the ADS returns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-liveprerollconfiguration.html#cfn-mediatailor-playbackconfiguration-liveprerollconfiguration-maxdurationseconds
            '''
            result = self._values.get("max_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LivePreRollConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ads_interaction_log": "adsInteractionLog",
            "enabled_logging_strategies": "enabledLoggingStrategies",
            "manifest_service_interaction_log": "manifestServiceInteractionLog",
            "percent_enabled": "percentEnabled",
        },
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            ads_interaction_log: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.AdsInteractionLogProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled_logging_strategies: typing.Optional[typing.Sequence[builtins.str]] = None,
            manifest_service_interaction_log: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.ManifestServiceInteractionLogProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            percent_enabled: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines where AWS Elemental MediaTailor sends logs for the playback configuration.

            :param ads_interaction_log: Settings for customizing what events are included in logs for interactions with the ad decision server (ADS).
            :param enabled_logging_strategies: The method used for collecting logs from AWS Elemental MediaTailor. ``LEGACY_CLOUDWATCH`` indicates that MediaTailor is sending logs directly to Amazon CloudWatch Logs. ``VENDED_LOGS`` indicates that MediaTailor is sending logs to CloudWatch, which then vends the logs to your destination of choice. Supported destinations are CloudWatch Logs log group, Amazon S3 bucket, and Amazon Data Firehose stream.
            :param manifest_service_interaction_log: Settings for customizing what events are included in logs for interactions with the origin server.
            :param percent_enabled: The percentage of session logs that MediaTailor sends to your configured log destination. For example, if your playback configuration has 1000 sessions and ``percentEnabled`` is set to ``60`` , MediaTailor sends logs for 600 of the sessions to CloudWatch Logs. MediaTailor decides at random which of the playback configuration sessions to send logs for. If you want to view logs for a specific session, you can use the `debug log mode <https://docs.aws.amazon.com/mediatailor/latest/ug/debug-log-mode.html>`_ . Valid values: ``0`` - ``100``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                log_configuration_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.LogConfigurationProperty(
                    ads_interaction_log=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdsInteractionLogProperty(
                        exclude_event_types=["excludeEventTypes"],
                        publish_opt_in_event_types=["publishOptInEventTypes"]
                    ),
                    enabled_logging_strategies=["enabledLoggingStrategies"],
                    manifest_service_interaction_log=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.ManifestServiceInteractionLogProperty(
                        exclude_event_types=["excludeEventTypes"]
                    ),
                    percent_enabled=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f37a94403df6c498f5d4763d1ef6f763a25a69e84ea0a60b06f8b7aba0ed550f)
                check_type(argname="argument ads_interaction_log", value=ads_interaction_log, expected_type=type_hints["ads_interaction_log"])
                check_type(argname="argument enabled_logging_strategies", value=enabled_logging_strategies, expected_type=type_hints["enabled_logging_strategies"])
                check_type(argname="argument manifest_service_interaction_log", value=manifest_service_interaction_log, expected_type=type_hints["manifest_service_interaction_log"])
                check_type(argname="argument percent_enabled", value=percent_enabled, expected_type=type_hints["percent_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ads_interaction_log is not None:
                self._values["ads_interaction_log"] = ads_interaction_log
            if enabled_logging_strategies is not None:
                self._values["enabled_logging_strategies"] = enabled_logging_strategies
            if manifest_service_interaction_log is not None:
                self._values["manifest_service_interaction_log"] = manifest_service_interaction_log
            if percent_enabled is not None:
                self._values["percent_enabled"] = percent_enabled

        @builtins.property
        def ads_interaction_log(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.AdsInteractionLogProperty"]]:
            '''Settings for customizing what events are included in logs for interactions with the ad decision server (ADS).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-logconfiguration.html#cfn-mediatailor-playbackconfiguration-logconfiguration-adsinteractionlog
            '''
            result = self._values.get("ads_interaction_log")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.AdsInteractionLogProperty"]], result)

        @builtins.property
        def enabled_logging_strategies(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The method used for collecting logs from AWS Elemental MediaTailor.

            ``LEGACY_CLOUDWATCH`` indicates that MediaTailor is sending logs directly to Amazon CloudWatch Logs. ``VENDED_LOGS`` indicates that MediaTailor is sending logs to CloudWatch, which then vends the logs to your destination of choice. Supported destinations are CloudWatch Logs log group, Amazon S3 bucket, and Amazon Data Firehose stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-logconfiguration.html#cfn-mediatailor-playbackconfiguration-logconfiguration-enabledloggingstrategies
            '''
            result = self._values.get("enabled_logging_strategies")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def manifest_service_interaction_log(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.ManifestServiceInteractionLogProperty"]]:
            '''Settings for customizing what events are included in logs for interactions with the origin server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-logconfiguration.html#cfn-mediatailor-playbackconfiguration-logconfiguration-manifestserviceinteractionlog
            '''
            result = self._values.get("manifest_service_interaction_log")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.ManifestServiceInteractionLogProperty"]], result)

        @builtins.property
        def percent_enabled(self) -> typing.Optional[jsii.Number]:
            '''The percentage of session logs that MediaTailor sends to your configured log destination.

            For example, if your playback configuration has 1000 sessions and ``percentEnabled`` is set to ``60`` , MediaTailor sends logs for 600 of the sessions to CloudWatch Logs. MediaTailor decides at random which of the playback configuration sessions to send logs for. If you want to view logs for a specific session, you can use the `debug log mode <https://docs.aws.amazon.com/mediatailor/latest/ug/debug-log-mode.html>`_ .

            Valid values: ``0`` - ``100``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-logconfiguration.html#cfn-mediatailor-playbackconfiguration-logconfiguration-percentenabled
            '''
            result = self._values.get("percent_enabled")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.ManifestProcessingRulesProperty",
        jsii_struct_bases=[],
        name_mapping={"ad_marker_passthrough": "adMarkerPassthrough"},
    )
    class ManifestProcessingRulesProperty:
        def __init__(
            self,
            *,
            ad_marker_passthrough: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaybackConfigurationPropsMixin.AdMarkerPassthroughProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for manifest processing rules.

            Manifest processing rules enable customization of the personalized manifests created by MediaTailor.

            :param ad_marker_passthrough: For HLS, when set to ``true`` , MediaTailor passes through ``EXT-X-CUE-IN`` , ``EXT-X-CUE-OUT`` , and ``EXT-X-SPLICEPOINT-SCTE35`` ad markers from the origin manifest to the MediaTailor personalized manifest. No logic is applied to these ad markers. For example, if ``EXT-X-CUE-OUT`` has a value of ``60`` , but no ads are filled for that ad break, MediaTailor will not set the value to ``0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-manifestprocessingrules.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                manifest_processing_rules_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.ManifestProcessingRulesProperty(
                    ad_marker_passthrough=mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.AdMarkerPassthroughProperty(
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c241a75345c5c3fdffa134e0fdc521c4d7a2245c6c8df7891dfbc66a0d3207ea)
                check_type(argname="argument ad_marker_passthrough", value=ad_marker_passthrough, expected_type=type_hints["ad_marker_passthrough"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_marker_passthrough is not None:
                self._values["ad_marker_passthrough"] = ad_marker_passthrough

        @builtins.property
        def ad_marker_passthrough(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.AdMarkerPassthroughProperty"]]:
            '''For HLS, when set to ``true`` , MediaTailor passes through ``EXT-X-CUE-IN`` , ``EXT-X-CUE-OUT`` , and ``EXT-X-SPLICEPOINT-SCTE35`` ad markers from the origin manifest to the MediaTailor personalized manifest.

            No logic is applied to these ad markers. For example, if ``EXT-X-CUE-OUT`` has a value of ``60`` , but no ads are filled for that ad break, MediaTailor will not set the value to ``0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-manifestprocessingrules.html#cfn-mediatailor-playbackconfiguration-manifestprocessingrules-admarkerpassthrough
            '''
            result = self._values.get("ad_marker_passthrough")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaybackConfigurationPropsMixin.AdMarkerPassthroughProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManifestProcessingRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationPropsMixin.ManifestServiceInteractionLogProperty",
        jsii_struct_bases=[],
        name_mapping={"exclude_event_types": "excludeEventTypes"},
    )
    class ManifestServiceInteractionLogProperty:
        def __init__(
            self,
            *,
            exclude_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Settings for customizing what events are included in logs for interactions with the origin server.

            For more information about manifest service logs, including descriptions of the event types, see `MediaTailor manifest logs description and event types <https://docs.aws.amazon.com/mediatailor/latest/ug/log-types.html>`_ in AWS Elemental MediaTailor User Guide.

            :param exclude_event_types: Indicates that MediaTailor won't emit the selected events in the logs for playback sessions that are initialized with this configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-manifestserviceinteractionlog.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                manifest_service_interaction_log_property = mediatailor_mixins.CfnPlaybackConfigurationPropsMixin.ManifestServiceInteractionLogProperty(
                    exclude_event_types=["excludeEventTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbdedcefcea950a6db0bc475c2f2eca5581312709e220981fba655fd436c66de)
                check_type(argname="argument exclude_event_types", value=exclude_event_types, expected_type=type_hints["exclude_event_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude_event_types is not None:
                self._values["exclude_event_types"] = exclude_event_types

        @builtins.property
        def exclude_event_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates that MediaTailor won't emit the selected events in the logs for playback sessions that are initialized with this configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-manifestserviceinteractionlog.html#cfn-mediatailor-playbackconfiguration-manifestserviceinteractionlog-excludeeventtypes
            '''
            result = self._values.get("exclude_event_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManifestServiceInteractionLogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnPlaybackConfigurationTranscodeLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnPlaybackConfigurationTranscodeLogs",
):
    '''Builder for CfnPlaybackConfigurationLogsMixin to generate TRANSCODE_LOGS for CfnPlaybackConfiguration.

    :cloudformationResource: AWS::MediaTailor::PlaybackConfiguration
    :logType: TRANSCODE_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
        
        cfn_playback_configuration_transcode_logs = mediatailor_mixins.CfnPlaybackConfigurationTranscodeLogs()
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
    ) -> CfnPlaybackConfigurationLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c76eda0e1fe5ec05058a5ffa7f80b5cd93884499ec79a3de0568ba35bf8abd0)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnPlaybackConfigurationLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnPlaybackConfigurationLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73e62a7ad686ba4f0b391bd5eeda6e94450b2047158596df2b68252a46e26f3)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnPlaybackConfigurationLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnPlaybackConfigurationLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b08d6c53187e4f8a92d92d02cf0b185d11f64b2e9a6945f6b6b58117b3ae5a)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnPlaybackConfigurationLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnSourceLocationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_configuration": "accessConfiguration",
        "default_segment_delivery_configuration": "defaultSegmentDeliveryConfiguration",
        "http_configuration": "httpConfiguration",
        "segment_delivery_configurations": "segmentDeliveryConfigurations",
        "source_location_name": "sourceLocationName",
        "tags": "tags",
    },
)
class CfnSourceLocationMixinProps:
    def __init__(
        self,
        *,
        access_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSourceLocationPropsMixin.AccessConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_segment_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSourceLocationPropsMixin.DefaultSegmentDeliveryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        http_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSourceLocationPropsMixin.HttpConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        segment_delivery_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSourceLocationPropsMixin.SegmentDeliveryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        source_location_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSourceLocationPropsMixin.

        :param access_configuration: The access configuration for the source location.
        :param default_segment_delivery_configuration: The default segment delivery configuration.
        :param http_configuration: The HTTP configuration for the source location.
        :param segment_delivery_configurations: The segment delivery configurations for the source location.
        :param source_location_name: The name of the source location.
        :param tags: The tags assigned to the source location. Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see `Tagging AWS Elemental MediaTailor Resources <https://docs.aws.amazon.com/mediatailor/latest/ug/tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-sourcelocation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
            
            cfn_source_location_mixin_props = mediatailor_mixins.CfnSourceLocationMixinProps(
                access_configuration=mediatailor_mixins.CfnSourceLocationPropsMixin.AccessConfigurationProperty(
                    access_type="accessType",
                    secrets_manager_access_token_configuration=mediatailor_mixins.CfnSourceLocationPropsMixin.SecretsManagerAccessTokenConfigurationProperty(
                        header_name="headerName",
                        secret_arn="secretArn",
                        secret_string_key="secretStringKey"
                    )
                ),
                default_segment_delivery_configuration=mediatailor_mixins.CfnSourceLocationPropsMixin.DefaultSegmentDeliveryConfigurationProperty(
                    base_url="baseUrl"
                ),
                http_configuration=mediatailor_mixins.CfnSourceLocationPropsMixin.HttpConfigurationProperty(
                    base_url="baseUrl"
                ),
                segment_delivery_configurations=[mediatailor_mixins.CfnSourceLocationPropsMixin.SegmentDeliveryConfigurationProperty(
                    base_url="baseUrl",
                    name="name"
                )],
                source_location_name="sourceLocationName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3a19072851571dafd1ddb658a7d9010c3de007dcf7434b744c24cc4771fc7d)
            check_type(argname="argument access_configuration", value=access_configuration, expected_type=type_hints["access_configuration"])
            check_type(argname="argument default_segment_delivery_configuration", value=default_segment_delivery_configuration, expected_type=type_hints["default_segment_delivery_configuration"])
            check_type(argname="argument http_configuration", value=http_configuration, expected_type=type_hints["http_configuration"])
            check_type(argname="argument segment_delivery_configurations", value=segment_delivery_configurations, expected_type=type_hints["segment_delivery_configurations"])
            check_type(argname="argument source_location_name", value=source_location_name, expected_type=type_hints["source_location_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_configuration is not None:
            self._values["access_configuration"] = access_configuration
        if default_segment_delivery_configuration is not None:
            self._values["default_segment_delivery_configuration"] = default_segment_delivery_configuration
        if http_configuration is not None:
            self._values["http_configuration"] = http_configuration
        if segment_delivery_configurations is not None:
            self._values["segment_delivery_configurations"] = segment_delivery_configurations
        if source_location_name is not None:
            self._values["source_location_name"] = source_location_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceLocationPropsMixin.AccessConfigurationProperty"]]:
        '''The access configuration for the source location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-sourcelocation.html#cfn-mediatailor-sourcelocation-accessconfiguration
        '''
        result = self._values.get("access_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceLocationPropsMixin.AccessConfigurationProperty"]], result)

    @builtins.property
    def default_segment_delivery_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceLocationPropsMixin.DefaultSegmentDeliveryConfigurationProperty"]]:
        '''The default segment delivery configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-sourcelocation.html#cfn-mediatailor-sourcelocation-defaultsegmentdeliveryconfiguration
        '''
        result = self._values.get("default_segment_delivery_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceLocationPropsMixin.DefaultSegmentDeliveryConfigurationProperty"]], result)

    @builtins.property
    def http_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceLocationPropsMixin.HttpConfigurationProperty"]]:
        '''The HTTP configuration for the source location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-sourcelocation.html#cfn-mediatailor-sourcelocation-httpconfiguration
        '''
        result = self._values.get("http_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceLocationPropsMixin.HttpConfigurationProperty"]], result)

    @builtins.property
    def segment_delivery_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceLocationPropsMixin.SegmentDeliveryConfigurationProperty"]]]]:
        '''The segment delivery configurations for the source location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-sourcelocation.html#cfn-mediatailor-sourcelocation-segmentdeliveryconfigurations
        '''
        result = self._values.get("segment_delivery_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceLocationPropsMixin.SegmentDeliveryConfigurationProperty"]]]], result)

    @builtins.property
    def source_location_name(self) -> typing.Optional[builtins.str]:
        '''The name of the source location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-sourcelocation.html#cfn-mediatailor-sourcelocation-sourcelocationname
        '''
        result = self._values.get("source_location_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags assigned to the source location.

        Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see `Tagging AWS Elemental MediaTailor Resources <https://docs.aws.amazon.com/mediatailor/latest/ug/tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-sourcelocation.html#cfn-mediatailor-sourcelocation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSourceLocationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSourceLocationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnSourceLocationPropsMixin",
):
    '''A source location is a container for sources.

    For more information about source locations, see `Working with source locations <https://docs.aws.amazon.com/mediatailor/latest/ug/channel-assembly-source-locations.html>`_ in the *MediaTailor User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-sourcelocation.html
    :cloudformationResource: AWS::MediaTailor::SourceLocation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
        
        cfn_source_location_props_mixin = mediatailor_mixins.CfnSourceLocationPropsMixin(mediatailor_mixins.CfnSourceLocationMixinProps(
            access_configuration=mediatailor_mixins.CfnSourceLocationPropsMixin.AccessConfigurationProperty(
                access_type="accessType",
                secrets_manager_access_token_configuration=mediatailor_mixins.CfnSourceLocationPropsMixin.SecretsManagerAccessTokenConfigurationProperty(
                    header_name="headerName",
                    secret_arn="secretArn",
                    secret_string_key="secretStringKey"
                )
            ),
            default_segment_delivery_configuration=mediatailor_mixins.CfnSourceLocationPropsMixin.DefaultSegmentDeliveryConfigurationProperty(
                base_url="baseUrl"
            ),
            http_configuration=mediatailor_mixins.CfnSourceLocationPropsMixin.HttpConfigurationProperty(
                base_url="baseUrl"
            ),
            segment_delivery_configurations=[mediatailor_mixins.CfnSourceLocationPropsMixin.SegmentDeliveryConfigurationProperty(
                base_url="baseUrl",
                name="name"
            )],
            source_location_name="sourceLocationName",
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
        props: typing.Union[CfnSourceLocationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaTailor::SourceLocation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00fa3aff812649e7af5b898a32a965e19b3b85d140bb8161f3bcf8374c0ce1d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e09e350c9f340c98333cbae980ffbedf938959416d9140ce2abf00c2ae43f3c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa812875203347b0aeb580059b722db4d46a757f67973e25f8261226e40fa75d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSourceLocationMixinProps:
        return typing.cast(CfnSourceLocationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnSourceLocationPropsMixin.AccessConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_type": "accessType",
            "secrets_manager_access_token_configuration": "secretsManagerAccessTokenConfiguration",
        },
    )
    class AccessConfigurationProperty:
        def __init__(
            self,
            *,
            access_type: typing.Optional[builtins.str] = None,
            secrets_manager_access_token_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSourceLocationPropsMixin.SecretsManagerAccessTokenConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Access configuration parameters.

            :param access_type: The type of authentication used to access content from ``HttpConfiguration::BaseUrl`` on your source location. Accepted value: ``S3_SIGV4`` . ``S3_SIGV4`` - AWS Signature Version 4 authentication for Amazon S3 hosted virtual-style access. If your source location base URL is an Amazon S3 bucket, MediaTailor can use AWS Signature Version 4 (SigV4) authentication to access the bucket where your source content is stored. Your MediaTailor source location baseURL must follow the S3 virtual hosted-style request URL format. For example, https://bucket-name.s3.Region.amazonaws.com/key-name. Before you can use ``S3_SIGV4`` , you must meet these requirements: • You must allow MediaTailor to access your S3 bucket by granting mediatailor.amazonaws.com principal access in IAM. For information about configuring access in IAM, see Access management in the IAM User Guide. • The mediatailor.amazonaws.com service principal must have permissions to read all top level manifests referenced by the VodSource packaging configurations. • The caller of the API must have s3:GetObject IAM permissions to read all top level manifests referenced by your MediaTailor VodSource packaging configurations.
            :param secrets_manager_access_token_configuration: AWS Secrets Manager access token configuration parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-accessconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                access_configuration_property = mediatailor_mixins.CfnSourceLocationPropsMixin.AccessConfigurationProperty(
                    access_type="accessType",
                    secrets_manager_access_token_configuration=mediatailor_mixins.CfnSourceLocationPropsMixin.SecretsManagerAccessTokenConfigurationProperty(
                        header_name="headerName",
                        secret_arn="secretArn",
                        secret_string_key="secretStringKey"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2d822e4dd468f2115833d30942839dd321e70ee6f9904c1a34b6d8ad9186d4c)
                check_type(argname="argument access_type", value=access_type, expected_type=type_hints["access_type"])
                check_type(argname="argument secrets_manager_access_token_configuration", value=secrets_manager_access_token_configuration, expected_type=type_hints["secrets_manager_access_token_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_type is not None:
                self._values["access_type"] = access_type
            if secrets_manager_access_token_configuration is not None:
                self._values["secrets_manager_access_token_configuration"] = secrets_manager_access_token_configuration

        @builtins.property
        def access_type(self) -> typing.Optional[builtins.str]:
            '''The type of authentication used to access content from ``HttpConfiguration::BaseUrl`` on your source location. Accepted value: ``S3_SIGV4`` .

            ``S3_SIGV4`` - AWS Signature Version 4 authentication for Amazon S3 hosted virtual-style access. If your source location base URL is an Amazon S3 bucket, MediaTailor can use AWS Signature Version 4 (SigV4) authentication to access the bucket where your source content is stored. Your MediaTailor source location baseURL must follow the S3 virtual hosted-style request URL format. For example, https://bucket-name.s3.Region.amazonaws.com/key-name.

            Before you can use ``S3_SIGV4`` , you must meet these requirements:

            • You must allow MediaTailor to access your S3 bucket by granting mediatailor.amazonaws.com principal access in IAM. For information about configuring access in IAM, see Access management in the IAM User Guide.

            • The mediatailor.amazonaws.com service principal must have permissions to read all top level manifests referenced by the VodSource packaging configurations.

            • The caller of the API must have s3:GetObject IAM permissions to read all top level manifests referenced by your MediaTailor VodSource packaging configurations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-accessconfiguration.html#cfn-mediatailor-sourcelocation-accessconfiguration-accesstype
            '''
            result = self._values.get("access_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_access_token_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceLocationPropsMixin.SecretsManagerAccessTokenConfigurationProperty"]]:
            '''AWS Secrets Manager access token configuration parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-accessconfiguration.html#cfn-mediatailor-sourcelocation-accessconfiguration-secretsmanageraccesstokenconfiguration
            '''
            result = self._values.get("secrets_manager_access_token_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceLocationPropsMixin.SecretsManagerAccessTokenConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnSourceLocationPropsMixin.DefaultSegmentDeliveryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"base_url": "baseUrl"},
    )
    class DefaultSegmentDeliveryConfigurationProperty:
        def __init__(self, *, base_url: typing.Optional[builtins.str] = None) -> None:
            '''The optional configuration for a server that serves segments.

            Use this if you want the segment delivery server to be different from the source location server. For example, you can configure your source location server to be an origination server, such as MediaPackage, and the segment delivery server to be a content delivery network (CDN), such as CloudFront. If you don't specify a segment delivery server, then the source location server is used.

            :param base_url: The hostname of the server that will be used to serve segments. This string must include the protocol, such as *https://* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-defaultsegmentdeliveryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                default_segment_delivery_configuration_property = mediatailor_mixins.CfnSourceLocationPropsMixin.DefaultSegmentDeliveryConfigurationProperty(
                    base_url="baseUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fa4c9a77f4b6310f61206f6c57a900cb36da3dca7c56cff6b99a967dd187de0)
                check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_url is not None:
                self._values["base_url"] = base_url

        @builtins.property
        def base_url(self) -> typing.Optional[builtins.str]:
            '''The hostname of the server that will be used to serve segments.

            This string must include the protocol, such as *https://* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-defaultsegmentdeliveryconfiguration.html#cfn-mediatailor-sourcelocation-defaultsegmentdeliveryconfiguration-baseurl
            '''
            result = self._values.get("base_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultSegmentDeliveryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnSourceLocationPropsMixin.HttpConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"base_url": "baseUrl"},
    )
    class HttpConfigurationProperty:
        def __init__(self, *, base_url: typing.Optional[builtins.str] = None) -> None:
            '''The HTTP configuration for the source location.

            :param base_url: The base URL for the source location host server. This string must include the protocol, such as *https://* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-httpconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                http_configuration_property = mediatailor_mixins.CfnSourceLocationPropsMixin.HttpConfigurationProperty(
                    base_url="baseUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e73fb9f0499ec018b5fad78f73cb02f0a91b7576bdfd73c8380362f50ccbfe9)
                check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_url is not None:
                self._values["base_url"] = base_url

        @builtins.property
        def base_url(self) -> typing.Optional[builtins.str]:
            '''The base URL for the source location host server.

            This string must include the protocol, such as *https://* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-httpconfiguration.html#cfn-mediatailor-sourcelocation-httpconfiguration-baseurl
            '''
            result = self._values.get("base_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnSourceLocationPropsMixin.SecretsManagerAccessTokenConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "header_name": "headerName",
            "secret_arn": "secretArn",
            "secret_string_key": "secretStringKey",
        },
    )
    class SecretsManagerAccessTokenConfigurationProperty:
        def __init__(
            self,
            *,
            header_name: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            secret_string_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''AWS Secrets Manager access token configuration parameters.

            For information about Secrets Manager access token authentication, see `Working with AWS Secrets Manager access token authentication <https://docs.aws.amazon.com/mediatailor/latest/ug/channel-assembly-access-configuration-access-token.html>`_ .

            :param header_name: The name of the HTTP header used to supply the access token in requests to the source location.
            :param secret_arn: The Amazon Resource Name (ARN) of the AWS Secrets Manager secret that contains the access token.
            :param secret_string_key: The AWS Secrets Manager `SecretString <https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_CreateSecret.html#SecretsManager-CreateSecret-request-SecretString.html>`_ key associated with the access token. MediaTailor uses the key to look up SecretString key and value pair containing the access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-secretsmanageraccesstokenconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                secrets_manager_access_token_configuration_property = mediatailor_mixins.CfnSourceLocationPropsMixin.SecretsManagerAccessTokenConfigurationProperty(
                    header_name="headerName",
                    secret_arn="secretArn",
                    secret_string_key="secretStringKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__180c2bef8443381e3d0803949db6f46a3f4d0e35fd538f50611ae81cd1bf0ed0)
                check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument secret_string_key", value=secret_string_key, expected_type=type_hints["secret_string_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_name is not None:
                self._values["header_name"] = header_name
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if secret_string_key is not None:
                self._values["secret_string_key"] = secret_string_key

        @builtins.property
        def header_name(self) -> typing.Optional[builtins.str]:
            '''The name of the HTTP header used to supply the access token in requests to the source location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-secretsmanageraccesstokenconfiguration.html#cfn-mediatailor-sourcelocation-secretsmanageraccesstokenconfiguration-headername
            '''
            result = self._values.get("header_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Secrets Manager secret that contains the access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-secretsmanageraccesstokenconfiguration.html#cfn-mediatailor-sourcelocation-secretsmanageraccesstokenconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_string_key(self) -> typing.Optional[builtins.str]:
            '''The AWS Secrets Manager `SecretString <https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_CreateSecret.html#SecretsManager-CreateSecret-request-SecretString.html>`_ key associated with the access token. MediaTailor uses the key to look up SecretString key and value pair containing the access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-secretsmanageraccesstokenconfiguration.html#cfn-mediatailor-sourcelocation-secretsmanageraccesstokenconfiguration-secretstringkey
            '''
            result = self._values.get("secret_string_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerAccessTokenConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnSourceLocationPropsMixin.SegmentDeliveryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"base_url": "baseUrl", "name": "name"},
    )
    class SegmentDeliveryConfigurationProperty:
        def __init__(
            self,
            *,
            base_url: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The segment delivery configuration settings.

            :param base_url: The base URL of the host or path of the segment delivery server that you're using to serve segments. This is typically a content delivery network (CDN). The URL can be absolute or relative. To use an absolute URL include the protocol, such as ``https://example.com/some/path`` . To use a relative URL specify the relative path, such as ``/some/path*`` .
            :param name: A unique identifier used to distinguish between multiple segment delivery configurations in a source location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-segmentdeliveryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                segment_delivery_configuration_property = mediatailor_mixins.CfnSourceLocationPropsMixin.SegmentDeliveryConfigurationProperty(
                    base_url="baseUrl",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a424ceb29272ff1a90983a55b9cea25cb1841fc75109264e4144979600d2726f)
                check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_url is not None:
                self._values["base_url"] = base_url
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def base_url(self) -> typing.Optional[builtins.str]:
            '''The base URL of the host or path of the segment delivery server that you're using to serve segments.

            This is typically a content delivery network (CDN). The URL can be absolute or relative. To use an absolute URL include the protocol, such as ``https://example.com/some/path`` . To use a relative URL specify the relative path, such as ``/some/path*`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-segmentdeliveryconfiguration.html#cfn-mediatailor-sourcelocation-segmentdeliveryconfiguration-baseurl
            '''
            result = self._values.get("base_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A unique identifier used to distinguish between multiple segment delivery configurations in a source location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-sourcelocation-segmentdeliveryconfiguration.html#cfn-mediatailor-sourcelocation-segmentdeliveryconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentDeliveryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnVodSourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "http_package_configurations": "httpPackageConfigurations",
        "source_location_name": "sourceLocationName",
        "tags": "tags",
        "vod_source_name": "vodSourceName",
    },
)
class CfnVodSourceMixinProps:
    def __init__(
        self,
        *,
        http_package_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVodSourcePropsMixin.HttpPackageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        source_location_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vod_source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVodSourcePropsMixin.

        :param http_package_configurations: The HTTP package configurations for the VOD source.
        :param source_location_name: The name of the source location that the VOD source is associated with.
        :param tags: The tags assigned to the VOD source. Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see `Tagging AWS Elemental MediaTailor Resources <https://docs.aws.amazon.com/mediatailor/latest/ug/tagging.html>`_ .
        :param vod_source_name: The name of the VOD source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-vodsource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
            
            cfn_vod_source_mixin_props = mediatailor_mixins.CfnVodSourceMixinProps(
                http_package_configurations=[mediatailor_mixins.CfnVodSourcePropsMixin.HttpPackageConfigurationProperty(
                    path="path",
                    source_group="sourceGroup",
                    type="type"
                )],
                source_location_name="sourceLocationName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vod_source_name="vodSourceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2fff7206b3b05e852808ca41f74c0f25184cccb2440e77ecda3fd2346d0119)
            check_type(argname="argument http_package_configurations", value=http_package_configurations, expected_type=type_hints["http_package_configurations"])
            check_type(argname="argument source_location_name", value=source_location_name, expected_type=type_hints["source_location_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vod_source_name", value=vod_source_name, expected_type=type_hints["vod_source_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_package_configurations is not None:
            self._values["http_package_configurations"] = http_package_configurations
        if source_location_name is not None:
            self._values["source_location_name"] = source_location_name
        if tags is not None:
            self._values["tags"] = tags
        if vod_source_name is not None:
            self._values["vod_source_name"] = vod_source_name

    @builtins.property
    def http_package_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVodSourcePropsMixin.HttpPackageConfigurationProperty"]]]]:
        '''The HTTP package configurations for the VOD source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-vodsource.html#cfn-mediatailor-vodsource-httppackageconfigurations
        '''
        result = self._values.get("http_package_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVodSourcePropsMixin.HttpPackageConfigurationProperty"]]]], result)

    @builtins.property
    def source_location_name(self) -> typing.Optional[builtins.str]:
        '''The name of the source location that the VOD source is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-vodsource.html#cfn-mediatailor-vodsource-sourcelocationname
        '''
        result = self._values.get("source_location_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags assigned to the VOD source.

        Tags are key-value pairs that you can associate with Amazon resources to help with organization, access control, and cost tracking. For more information, see `Tagging AWS Elemental MediaTailor Resources <https://docs.aws.amazon.com/mediatailor/latest/ug/tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-vodsource.html#cfn-mediatailor-vodsource-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vod_source_name(self) -> typing.Optional[builtins.str]:
        '''The name of the VOD source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-vodsource.html#cfn-mediatailor-vodsource-vodsourcename
        '''
        result = self._values.get("vod_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVodSourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVodSourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnVodSourcePropsMixin",
):
    '''The VOD source configuration parameters.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-vodsource.html
    :cloudformationResource: AWS::MediaTailor::VodSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
        
        cfn_vod_source_props_mixin = mediatailor_mixins.CfnVodSourcePropsMixin(mediatailor_mixins.CfnVodSourceMixinProps(
            http_package_configurations=[mediatailor_mixins.CfnVodSourcePropsMixin.HttpPackageConfigurationProperty(
                path="path",
                source_group="sourceGroup",
                type="type"
            )],
            source_location_name="sourceLocationName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vod_source_name="vodSourceName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVodSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaTailor::VodSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f280df5bc7e272dcf6e2b0c4a402db3276a5bf3055fa2aca7ef190fe2cc8990b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e83343f4f26313a7a34ec9ed702d5a5b304fce5872f6d633e46bc95f2d28411a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fef0636579ef0736e24a2612396b1a4346e451344f30a85793b3954ada7f38)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVodSourceMixinProps:
        return typing.cast(CfnVodSourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediatailor.mixins.CfnVodSourcePropsMixin.HttpPackageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path", "source_group": "sourceGroup", "type": "type"},
    )
    class HttpPackageConfigurationProperty:
        def __init__(
            self,
            *,
            path: typing.Optional[builtins.str] = None,
            source_group: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The HTTP package configuration properties for the requested VOD source.

            :param path: The relative path to the URL for this VOD source. This is combined with ``SourceLocation::HttpConfiguration::BaseUrl`` to form a valid URL.
            :param source_group: The name of the source group. This has to match one of the ``Channel::Outputs::SourceGroup`` .
            :param type: The streaming protocol for this package configuration. Supported values are ``HLS`` and ``DASH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-vodsource-httppackageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediatailor import mixins as mediatailor_mixins
                
                http_package_configuration_property = mediatailor_mixins.CfnVodSourcePropsMixin.HttpPackageConfigurationProperty(
                    path="path",
                    source_group="sourceGroup",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d57dad3173d5a8ad55915ce40dead16310eee57fc1cffe6af9c64a2d39aa932)
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument source_group", value=source_group, expected_type=type_hints["source_group"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if path is not None:
                self._values["path"] = path
            if source_group is not None:
                self._values["source_group"] = source_group
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The relative path to the URL for this VOD source.

            This is combined with ``SourceLocation::HttpConfiguration::BaseUrl`` to form a valid URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-vodsource-httppackageconfiguration.html#cfn-mediatailor-vodsource-httppackageconfiguration-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_group(self) -> typing.Optional[builtins.str]:
            '''The name of the source group.

            This has to match one of the ``Channel::Outputs::SourceGroup`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-vodsource-httppackageconfiguration.html#cfn-mediatailor-vodsource-httppackageconfiguration-sourcegroup
            '''
            result = self._values.get("source_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The streaming protocol for this package configuration.

            Supported values are ``HLS`` and ``DASH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-vodsource-httppackageconfiguration.html#cfn-mediatailor-vodsource-httppackageconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpPackageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnChannelMixinProps",
    "CfnChannelPolicyMixinProps",
    "CfnChannelPolicyPropsMixin",
    "CfnChannelPropsMixin",
    "CfnLiveSourceMixinProps",
    "CfnLiveSourcePropsMixin",
    "CfnPlaybackConfigurationAdDecisionServerLogs",
    "CfnPlaybackConfigurationLogsMixin",
    "CfnPlaybackConfigurationManifestServiceLogs",
    "CfnPlaybackConfigurationMixinProps",
    "CfnPlaybackConfigurationPropsMixin",
    "CfnPlaybackConfigurationTranscodeLogs",
    "CfnSourceLocationMixinProps",
    "CfnSourceLocationPropsMixin",
    "CfnVodSourceMixinProps",
    "CfnVodSourcePropsMixin",
]

publication.publish()

def _typecheckingstub__a5415afb81c2d023e0e7fb35386bc1e78c6469e1832821846b1fb2c96d52bcae(
    *,
    audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    channel_name: typing.Optional[builtins.str] = None,
    filler_slate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.SlateSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.LogConfigurationForChannelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.RequestOutputItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    playback_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tier: typing.Optional[builtins.str] = None,
    time_shift_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.TimeShiftConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e81c5104a4fb2b995210f7950b3076943d527115681b83890fe0d90510c869(
    *,
    channel_name: typing.Optional[builtins.str] = None,
    policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ac248c9a37a8a27574a2631b3dda383372cdc9f651c29f62422759a4446c82(
    props: typing.Union[CfnChannelPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276f27480e032761112a99c03ce8c15c3c5679e6a3a7e312c713ee439a8fd96f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2423e072952f6717d11e37fdec6fc534d0fcf84c5c32418dfbaf5515f9b673(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cc21419bf96dbd8ec109cac7dbcd531ed2fbf967b4d94c9a84faeaf9fb6c0b(
    props: typing.Union[CfnChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb56ddb44249f30b9b26cdb5fdf1bc5cdbad43043afcc8240acd4a31d366966(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c9e7b8906b29f2bfe0665d24776b42aa59f194003f906b51603e856073e623(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e8c79dc4b4d41927f0beca0225128b08ad354ef67656dd0ad3faf724102675(
    *,
    manifest_window_seconds: typing.Optional[jsii.Number] = None,
    min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
    min_update_period_seconds: typing.Optional[jsii.Number] = None,
    suggested_presentation_delay_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a097a2656809fa8cbaa6984f7719accd4fd4e9b41060ce5ecedbbe9d66d445f(
    *,
    ad_markup_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    manifest_window_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b85bca524f4b172c209f496a7a9c47e715524f8aff9dc399eb6b4ce0c45916(
    *,
    log_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefd86399b0b6b817c3fc3e112996a715962c9fb26299e98afde686e8ab1d347(
    *,
    dash_playlist_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.DashPlaylistSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hls_playlist_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.HlsPlaylistSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    source_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73db29900f18d40347a0833d2fd45fcd0e91c85bc00ad5e337a5c010b2c727e4(
    *,
    source_location_name: typing.Optional[builtins.str] = None,
    vod_source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11433fe731a80590e987bc4cf39a7fa8e753db5fb00715895a6609427e0096cb(
    *,
    max_time_delay_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85aa1e71522700650a9e323c27f63d2c3a6df9c3991970b481bea13211be0ecb(
    *,
    http_package_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLiveSourcePropsMixin.HttpPackageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    live_source_name: typing.Optional[builtins.str] = None,
    source_location_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34577fd59a072a532187d0f4a50343319df98689818687ea2e2e3f6bcb9a24cb(
    props: typing.Union[CfnLiveSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707748a2b131f5c78f00db8845451b8ac0059de4e8a4b05a3ad86134e8627ae3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa4514fcf806051e1919d669581d46817a89b8ab2930bceaeeb7b8179dcf583(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad498bff2b2af40630f3eb6bfe5a494a1d3f1a12829d9b7b19ea1199ccd6f38(
    *,
    path: typing.Optional[builtins.str] = None,
    source_group: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e86a052e20c8228bc093ef1e81663e21e26af1acdeb9ebd0590dc4ce4ef2b99(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a630ed534e9ef49e9fa722ba2673200de7833d9ce20ae36627f37365f9fa84ec(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08257b9b52bcc570545a1fda383c2af965d90755db227b2c6b2669a74fe72179(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be22dc5fdbd1bf53113a722cc11a9b40329325137f457b06c1a0e52a4e0453b(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61be5ae7c09b88d8a3fae6f642df86bbdfadab120e49d7ce23b9ac0108b8f205(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ece1d228b98eb43999d1e5f071cce2aa5ba0d5b8637938930f2be61005ee29(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779bc1620506212603cd0bf2f441fc09f9538cdd5f24bc4a18f176705af08aa9(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885cfdc6db35b97c08c385af0249fa780966a96fe797af4141cf20392adcc5a6(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014a4750a71f835eca7d99b8d7e79bb5c2ecbdf8e2e3a2ea3109ee4208110f6b(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4e0915d792d710443769766e32410b0213a19153a8b76c904d6bc433c44702(
    *,
    ad_conditioning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.AdConditioningConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ad_decision_server_url: typing.Optional[builtins.str] = None,
    avail_suppression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.AvailSuppressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bumper: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.BumperProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cdn_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.CdnConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    configuration_aliases: typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
    dash_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.DashConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hls_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.HlsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    insertion_mode: typing.Optional[builtins.str] = None,
    live_pre_roll_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.LivePreRollConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    manifest_processing_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.ManifestProcessingRulesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    personalization_threshold_seconds: typing.Optional[jsii.Number] = None,
    slate_ad_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    transcode_profile_name: typing.Optional[builtins.str] = None,
    video_content_source_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7be1974faebeb1232ec780232a7c52cc12ef3139bc0f35844797fbc68a76a1(
    props: typing.Union[CfnPlaybackConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9391525138759126e336e5f4fd7ec222b2bfe404aa119d4f434588ee46a7163(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68e20409cbd820e6ddbccb5556c91bde9a4ed6cc6bfc5cebf0f46e992d134da(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88050e638370f9f01c6dc3bc48f81b355bfb55969e44fa46303e8cec56fc661(
    *,
    streaming_media_file_conditioning: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d86ca02d9e7093565eee46c0beffc68000d1aa8f7ab63019d1a97faf0bbd11b(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10563bbc541f982a32cde4bf56ed8e938d4f6173208e0e4e26f16da6bf4ed9ed(
    *,
    exclude_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    publish_opt_in_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8e624062e06214c310f853f44ebaea3a7a0bf9cd3dda3fc2b6aadda5d9eb1d(
    *,
    fill_policy: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed629358d76c3d2947f4a0eceeab210bc1a5438c2d5502f7c049c6848fd0157(
    *,
    end_url: typing.Optional[builtins.str] = None,
    start_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1744fff035bb2f15d4e9d3e914a6b755c7690656779ace6a5072f9ffd172598b(
    *,
    ad_segment_url_prefix: typing.Optional[builtins.str] = None,
    content_segment_url_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3bb546d131215baef2043d19564ae6df67fc9f2f3584efe67e5459ea77c0ea0(
    *,
    manifest_endpoint_prefix: typing.Optional[builtins.str] = None,
    mpd_location: typing.Optional[builtins.str] = None,
    origin_manifest_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf83506e20e29f9dea14bf5ac12cd3282ed646ee913fcc946ba6bee59a582d4(
    *,
    manifest_endpoint_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123b272c4357828e6a77159b810c08d7aa3e178e560ec39a77156172b4f74ae9(
    *,
    ad_decision_server_url: typing.Optional[builtins.str] = None,
    max_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37a94403df6c498f5d4763d1ef6f763a25a69e84ea0a60b06f8b7aba0ed550f(
    *,
    ads_interaction_log: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.AdsInteractionLogProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled_logging_strategies: typing.Optional[typing.Sequence[builtins.str]] = None,
    manifest_service_interaction_log: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.ManifestServiceInteractionLogProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    percent_enabled: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c241a75345c5c3fdffa134e0fdc521c4d7a2245c6c8df7891dfbc66a0d3207ea(
    *,
    ad_marker_passthrough: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaybackConfigurationPropsMixin.AdMarkerPassthroughProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdedcefcea950a6db0bc475c2f2eca5581312709e220981fba655fd436c66de(
    *,
    exclude_event_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c76eda0e1fe5ec05058a5ffa7f80b5cd93884499ec79a3de0568ba35bf8abd0(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73e62a7ad686ba4f0b391bd5eeda6e94450b2047158596df2b68252a46e26f3(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b08d6c53187e4f8a92d92d02cf0b185d11f64b2e9a6945f6b6b58117b3ae5a(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3a19072851571dafd1ddb658a7d9010c3de007dcf7434b744c24cc4771fc7d(
    *,
    access_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSourceLocationPropsMixin.AccessConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_segment_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSourceLocationPropsMixin.DefaultSegmentDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSourceLocationPropsMixin.HttpConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    segment_delivery_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSourceLocationPropsMixin.SegmentDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_location_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00fa3aff812649e7af5b898a32a965e19b3b85d140bb8161f3bcf8374c0ce1d7(
    props: typing.Union[CfnSourceLocationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e09e350c9f340c98333cbae980ffbedf938959416d9140ce2abf00c2ae43f3c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa812875203347b0aeb580059b722db4d46a757f67973e25f8261226e40fa75d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d822e4dd468f2115833d30942839dd321e70ee6f9904c1a34b6d8ad9186d4c(
    *,
    access_type: typing.Optional[builtins.str] = None,
    secrets_manager_access_token_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSourceLocationPropsMixin.SecretsManagerAccessTokenConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa4c9a77f4b6310f61206f6c57a900cb36da3dca7c56cff6b99a967dd187de0(
    *,
    base_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e73fb9f0499ec018b5fad78f73cb02f0a91b7576bdfd73c8380362f50ccbfe9(
    *,
    base_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180c2bef8443381e3d0803949db6f46a3f4d0e35fd538f50611ae81cd1bf0ed0(
    *,
    header_name: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    secret_string_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a424ceb29272ff1a90983a55b9cea25cb1841fc75109264e4144979600d2726f(
    *,
    base_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2fff7206b3b05e852808ca41f74c0f25184cccb2440e77ecda3fd2346d0119(
    *,
    http_package_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVodSourcePropsMixin.HttpPackageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_location_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vod_source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f280df5bc7e272dcf6e2b0c4a402db3276a5bf3055fa2aca7ef190fe2cc8990b(
    props: typing.Union[CfnVodSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83343f4f26313a7a34ec9ed702d5a5b304fce5872f6d633e46bc95f2d28411a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fef0636579ef0736e24a2612396b1a4346e451344f30a85793b3954ada7f38(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d57dad3173d5a8ad55915ce40dead16310eee57fc1cffe6af9c64a2d39aa932(
    *,
    path: typing.Optional[builtins.str] = None,
    source_group: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
