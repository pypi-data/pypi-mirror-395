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
    jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bot_alias_locale_settings": "botAliasLocaleSettings",
        "bot_alias_name": "botAliasName",
        "bot_alias_tags": "botAliasTags",
        "bot_id": "botId",
        "bot_version": "botVersion",
        "conversation_log_settings": "conversationLogSettings",
        "description": "description",
        "sentiment_analysis_settings": "sentimentAnalysisSettings",
    },
)
class CfnBotAliasMixinProps:
    def __init__(
        self,
        *,
        bot_alias_locale_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.BotAliasLocaleSettingsItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        bot_alias_name: typing.Optional[builtins.str] = None,
        bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        bot_id: typing.Optional[builtins.str] = None,
        bot_version: typing.Optional[builtins.str] = None,
        conversation_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.ConversationLogSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        sentiment_analysis_settings: typing.Any = None,
    ) -> None:
        '''Properties for CfnBotAliasPropsMixin.

        :param bot_alias_locale_settings: Specifies settings that are unique to a locale. For example, you can use different Lambda function depending on the bot's locale.
        :param bot_alias_name: The name of the bot alias.
        :param bot_alias_tags: An array of key-value pairs to apply to this resource. You can only add tags when you specify an alias. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param bot_id: The unique identifier of the bot.
        :param bot_version: The version of the bot that the bot alias references.
        :param conversation_log_settings: Specifies whether Amazon Lex logs text and audio for conversations with the bot. When you enable conversation logs, text logs store text input, transcripts of audio input, and associated metadata in Amazon CloudWatch logs. Audio logs store input in Amazon S3 .
        :param description: The description of the bot alias.
        :param sentiment_analysis_settings: Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
            
            # sentiment_analysis_settings: Any
            
            cfn_bot_alias_mixin_props = lex_mixins.CfnBotAliasMixinProps(
                bot_alias_locale_settings=[lex_mixins.CfnBotAliasPropsMixin.BotAliasLocaleSettingsItemProperty(
                    bot_alias_locale_setting=lex_mixins.CfnBotAliasPropsMixin.BotAliasLocaleSettingsProperty(
                        code_hook_specification=lex_mixins.CfnBotAliasPropsMixin.CodeHookSpecificationProperty(
                            lambda_code_hook=lex_mixins.CfnBotAliasPropsMixin.LambdaCodeHookProperty(
                                code_hook_interface_version="codeHookInterfaceVersion",
                                lambda_arn="lambdaArn"
                            )
                        ),
                        enabled=False
                    ),
                    locale_id="localeId"
                )],
                bot_alias_name="botAliasName",
                bot_alias_tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                bot_id="botId",
                bot_version="botVersion",
                conversation_log_settings=lex_mixins.CfnBotAliasPropsMixin.ConversationLogSettingsProperty(
                    audio_log_settings=[lex_mixins.CfnBotAliasPropsMixin.AudioLogSettingProperty(
                        destination=lex_mixins.CfnBotAliasPropsMixin.AudioLogDestinationProperty(
                            s3_bucket=lex_mixins.CfnBotAliasPropsMixin.S3BucketLogDestinationProperty(
                                kms_key_arn="kmsKeyArn",
                                log_prefix="logPrefix",
                                s3_bucket_arn="s3BucketArn"
                            )
                        ),
                        enabled=False
                    )],
                    text_log_settings=[lex_mixins.CfnBotAliasPropsMixin.TextLogSettingProperty(
                        destination=lex_mixins.CfnBotAliasPropsMixin.TextLogDestinationProperty(
                            cloud_watch=lex_mixins.CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                                log_prefix="logPrefix"
                            )
                        ),
                        enabled=False
                    )]
                ),
                description="description",
                sentiment_analysis_settings=sentiment_analysis_settings
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6079d85d5535c384e30d8c597d5dd7fabe1a6d01a77b9d493efaf7442c071263)
            check_type(argname="argument bot_alias_locale_settings", value=bot_alias_locale_settings, expected_type=type_hints["bot_alias_locale_settings"])
            check_type(argname="argument bot_alias_name", value=bot_alias_name, expected_type=type_hints["bot_alias_name"])
            check_type(argname="argument bot_alias_tags", value=bot_alias_tags, expected_type=type_hints["bot_alias_tags"])
            check_type(argname="argument bot_id", value=bot_id, expected_type=type_hints["bot_id"])
            check_type(argname="argument bot_version", value=bot_version, expected_type=type_hints["bot_version"])
            check_type(argname="argument conversation_log_settings", value=conversation_log_settings, expected_type=type_hints["conversation_log_settings"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument sentiment_analysis_settings", value=sentiment_analysis_settings, expected_type=type_hints["sentiment_analysis_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bot_alias_locale_settings is not None:
            self._values["bot_alias_locale_settings"] = bot_alias_locale_settings
        if bot_alias_name is not None:
            self._values["bot_alias_name"] = bot_alias_name
        if bot_alias_tags is not None:
            self._values["bot_alias_tags"] = bot_alias_tags
        if bot_id is not None:
            self._values["bot_id"] = bot_id
        if bot_version is not None:
            self._values["bot_version"] = bot_version
        if conversation_log_settings is not None:
            self._values["conversation_log_settings"] = conversation_log_settings
        if description is not None:
            self._values["description"] = description
        if sentiment_analysis_settings is not None:
            self._values["sentiment_analysis_settings"] = sentiment_analysis_settings

    @builtins.property
    def bot_alias_locale_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.BotAliasLocaleSettingsItemProperty"]]]]:
        '''Specifies settings that are unique to a locale.

        For example, you can use different Lambda function depending on the bot's locale.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliaslocalesettings
        '''
        result = self._values.get("bot_alias_locale_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.BotAliasLocaleSettingsItemProperty"]]]], result)

    @builtins.property
    def bot_alias_name(self) -> typing.Optional[builtins.str]:
        '''The name of the bot alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliasname
        '''
        result = self._values.get("bot_alias_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bot_alias_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
        '''An array of key-value pairs to apply to this resource.

        You can only add tags when you specify an alias.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliastags
        '''
        result = self._values.get("bot_alias_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

    @builtins.property
    def bot_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the bot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botid
        '''
        result = self._values.get("bot_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bot_version(self) -> typing.Optional[builtins.str]:
        '''The version of the bot that the bot alias references.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botversion
        '''
        result = self._values.get("bot_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conversation_log_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.ConversationLogSettingsProperty"]]:
        '''Specifies whether Amazon Lex logs text and audio for conversations with the bot.

        When you enable conversation logs, text logs store text input, transcripts of audio input, and associated metadata in Amazon CloudWatch logs. Audio logs store input in Amazon S3 .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-conversationlogsettings
        '''
        result = self._values.get("conversation_log_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.ConversationLogSettingsProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the bot alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sentiment_analysis_settings(self) -> typing.Any:
        '''Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-sentimentanalysissettings
        '''
        result = self._values.get("sentiment_analysis_settings")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBotAliasMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBotAliasPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin",
):
    '''.. epigraph::

   Amazon Lex V2 is the only supported version in CloudFormation .

    Specifies an alias for the specified version of a bot. Use an alias to enable you to change the version of a bot without updating applications that use the bot.

    For example, you can specify an alias called "PROD" that your applications use to call the Amazon Lex bot.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html
    :cloudformationResource: AWS::Lex::BotAlias
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
        
        # sentiment_analysis_settings: Any
        
        cfn_bot_alias_props_mixin = lex_mixins.CfnBotAliasPropsMixin(lex_mixins.CfnBotAliasMixinProps(
            bot_alias_locale_settings=[lex_mixins.CfnBotAliasPropsMixin.BotAliasLocaleSettingsItemProperty(
                bot_alias_locale_setting=lex_mixins.CfnBotAliasPropsMixin.BotAliasLocaleSettingsProperty(
                    code_hook_specification=lex_mixins.CfnBotAliasPropsMixin.CodeHookSpecificationProperty(
                        lambda_code_hook=lex_mixins.CfnBotAliasPropsMixin.LambdaCodeHookProperty(
                            code_hook_interface_version="codeHookInterfaceVersion",
                            lambda_arn="lambdaArn"
                        )
                    ),
                    enabled=False
                ),
                locale_id="localeId"
            )],
            bot_alias_name="botAliasName",
            bot_alias_tags=[CfnTag(
                key="key",
                value="value"
            )],
            bot_id="botId",
            bot_version="botVersion",
            conversation_log_settings=lex_mixins.CfnBotAliasPropsMixin.ConversationLogSettingsProperty(
                audio_log_settings=[lex_mixins.CfnBotAliasPropsMixin.AudioLogSettingProperty(
                    destination=lex_mixins.CfnBotAliasPropsMixin.AudioLogDestinationProperty(
                        s3_bucket=lex_mixins.CfnBotAliasPropsMixin.S3BucketLogDestinationProperty(
                            kms_key_arn="kmsKeyArn",
                            log_prefix="logPrefix",
                            s3_bucket_arn="s3BucketArn"
                        )
                    ),
                    enabled=False
                )],
                text_log_settings=[lex_mixins.CfnBotAliasPropsMixin.TextLogSettingProperty(
                    destination=lex_mixins.CfnBotAliasPropsMixin.TextLogDestinationProperty(
                        cloud_watch=lex_mixins.CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                            cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                            log_prefix="logPrefix"
                        )
                    ),
                    enabled=False
                )]
            ),
            description="description",
            sentiment_analysis_settings=sentiment_analysis_settings
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBotAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lex::BotAlias``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a2da524674a6a01c96e3d2a38a8868f8c1e9224a3674ca288aec940a1ec578)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d09ecbc7ee9804e201de495189e09d28d96f96da5c00a884265f607c94a62f7d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3190f32c765700f1fb75bf551f9d0440736c0cf334570089fd93c9730561beb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBotAliasMixinProps:
        return typing.cast(CfnBotAliasMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.AudioLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket"},
    )
    class AudioLogDestinationProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.S3BucketLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the S3 bucket location where audio logs are stored.

            :param s3_bucket: The S3 bucket location where audio logs are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                audio_log_destination_property = lex_mixins.CfnBotAliasPropsMixin.AudioLogDestinationProperty(
                    s3_bucket=lex_mixins.CfnBotAliasPropsMixin.S3BucketLogDestinationProperty(
                        kms_key_arn="kmsKeyArn",
                        log_prefix="logPrefix",
                        s3_bucket_arn="s3BucketArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c1d90832be5701f13f7f952a08cdc22d03c3f3c9d9c3c051f35fc32b9345f8da)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket

        @builtins.property
        def s3_bucket(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.S3BucketLogDestinationProperty"]]:
            '''The S3 bucket location where audio logs are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologdestination.html#cfn-lex-botalias-audiologdestination-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.S3BucketLogDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.AudioLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "enabled": "enabled"},
    )
    class AudioLogSettingProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.AudioLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Settings for logging audio of conversations between Amazon Lex and a user.

            You specify whether to log audio and the Amazon S3 bucket where the audio file is stored.

            :param destination: The location of audio log files collected when conversation logging is enabled for a bot.
            :param enabled: Determines whether audio logging in enabled for the bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                audio_log_setting_property = lex_mixins.CfnBotAliasPropsMixin.AudioLogSettingProperty(
                    destination=lex_mixins.CfnBotAliasPropsMixin.AudioLogDestinationProperty(
                        s3_bucket=lex_mixins.CfnBotAliasPropsMixin.S3BucketLogDestinationProperty(
                            kms_key_arn="kmsKeyArn",
                            log_prefix="logPrefix",
                            s3_bucket_arn="s3BucketArn"
                        )
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__deff21b209b3fe3bbe7eb50443e04a454edaeaf54e7df10487a9fcfb203cd8a9)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.AudioLogDestinationProperty"]]:
            '''The location of audio log files collected when conversation logging is enabled for a bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologsetting.html#cfn-lex-botalias-audiologsetting-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.AudioLogDestinationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether audio logging in enabled for the bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologsetting.html#cfn-lex-botalias-audiologsetting-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.BotAliasLocaleSettingsItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bot_alias_locale_setting": "botAliasLocaleSetting",
            "locale_id": "localeId",
        },
    )
    class BotAliasLocaleSettingsItemProperty:
        def __init__(
            self,
            *,
            bot_alias_locale_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.BotAliasLocaleSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            locale_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies settings that are unique to a locale.

            For example, you can use different Lambda function depending on the bot's locale.

            :param bot_alias_locale_setting: Specifies settings that are unique to a locale.
            :param locale_id: The unique identifier of the locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettingsitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bot_alias_locale_settings_item_property = lex_mixins.CfnBotAliasPropsMixin.BotAliasLocaleSettingsItemProperty(
                    bot_alias_locale_setting=lex_mixins.CfnBotAliasPropsMixin.BotAliasLocaleSettingsProperty(
                        code_hook_specification=lex_mixins.CfnBotAliasPropsMixin.CodeHookSpecificationProperty(
                            lambda_code_hook=lex_mixins.CfnBotAliasPropsMixin.LambdaCodeHookProperty(
                                code_hook_interface_version="codeHookInterfaceVersion",
                                lambda_arn="lambdaArn"
                            )
                        ),
                        enabled=False
                    ),
                    locale_id="localeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c48f67a05123c3bf05595dc0fa5fc9bcf8306a8e58bc6d57618e48bd6395bb9a)
                check_type(argname="argument bot_alias_locale_setting", value=bot_alias_locale_setting, expected_type=type_hints["bot_alias_locale_setting"])
                check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bot_alias_locale_setting is not None:
                self._values["bot_alias_locale_setting"] = bot_alias_locale_setting
            if locale_id is not None:
                self._values["locale_id"] = locale_id

        @builtins.property
        def bot_alias_locale_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.BotAliasLocaleSettingsProperty"]]:
            '''Specifies settings that are unique to a locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettingsitem.html#cfn-lex-botalias-botaliaslocalesettingsitem-botaliaslocalesetting
            '''
            result = self._values.get("bot_alias_locale_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.BotAliasLocaleSettingsProperty"]], result)

        @builtins.property
        def locale_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettingsitem.html#cfn-lex-botalias-botaliaslocalesettingsitem-localeid
            '''
            result = self._values.get("locale_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotAliasLocaleSettingsItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.BotAliasLocaleSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_hook_specification": "codeHookSpecification",
            "enabled": "enabled",
        },
    )
    class BotAliasLocaleSettingsProperty:
        def __init__(
            self,
            *,
            code_hook_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.CodeHookSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies settings that are unique to a locale.

            For example, you can use different Lambda function depending on the bot's locale.

            :param code_hook_specification: Specifies the Lambda function that should be used in the locale.
            :param enabled: Determines whether the locale is enabled for the bot. If the value is ``false`` , the locale isn't available for use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bot_alias_locale_settings_property = lex_mixins.CfnBotAliasPropsMixin.BotAliasLocaleSettingsProperty(
                    code_hook_specification=lex_mixins.CfnBotAliasPropsMixin.CodeHookSpecificationProperty(
                        lambda_code_hook=lex_mixins.CfnBotAliasPropsMixin.LambdaCodeHookProperty(
                            code_hook_interface_version="codeHookInterfaceVersion",
                            lambda_arn="lambdaArn"
                        )
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc4b3643d7b1fcb39a7c028b7560a10068b97c72af2b2e141a82e44986c46e28)
                check_type(argname="argument code_hook_specification", value=code_hook_specification, expected_type=type_hints["code_hook_specification"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_hook_specification is not None:
                self._values["code_hook_specification"] = code_hook_specification
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def code_hook_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.CodeHookSpecificationProperty"]]:
            '''Specifies the Lambda function that should be used in the locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettings.html#cfn-lex-botalias-botaliaslocalesettings-codehookspecification
            '''
            result = self._values.get("code_hook_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.CodeHookSpecificationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the locale is enabled for the bot.

            If the value is ``false`` , the locale isn't available for use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettings.html#cfn-lex-botalias-botaliaslocalesettings-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotAliasLocaleSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
            "log_prefix": "logPrefix",
        },
    )
    class CloudWatchLogGroupLogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
            log_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon CloudWatch Logs log group where the text and metadata logs are delivered.

            The log group must exist before you enable logging.

            :param cloud_watch_log_group_arn: The Amazon Resource Name (ARN) of the log group where text and metadata logs are delivered.
            :param log_prefix: The prefix of the log stream name within the log group that you specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-cloudwatchloggrouplogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                cloud_watch_log_group_log_destination_property = lex_mixins.CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    log_prefix="logPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cad37fface3c3411fc449d82424b14f27a363a2966bae32724507d84a547d08b)
                check_type(argname="argument cloud_watch_log_group_arn", value=cloud_watch_log_group_arn, expected_type=type_hints["cloud_watch_log_group_arn"])
                check_type(argname="argument log_prefix", value=log_prefix, expected_type=type_hints["log_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_log_group_arn is not None:
                self._values["cloud_watch_log_group_arn"] = cloud_watch_log_group_arn
            if log_prefix is not None:
                self._values["log_prefix"] = log_prefix

        @builtins.property
        def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the log group where text and metadata logs are delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-cloudwatchloggrouplogdestination.html#cfn-lex-botalias-cloudwatchloggrouplogdestination-cloudwatchloggrouparn
            '''
            result = self._values.get("cloud_watch_log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix of the log stream name within the log group that you specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-cloudwatchloggrouplogdestination.html#cfn-lex-botalias-cloudwatchloggrouplogdestination-logprefix
            '''
            result = self._values.get("log_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogGroupLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.CodeHookSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_code_hook": "lambdaCodeHook"},
    )
    class CodeHookSpecificationProperty:
        def __init__(
            self,
            *,
            lambda_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.LambdaCodeHookProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about code hooks that Amazon Lex calls during a conversation.

            :param lambda_code_hook: Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-codehookspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                code_hook_specification_property = lex_mixins.CfnBotAliasPropsMixin.CodeHookSpecificationProperty(
                    lambda_code_hook=lex_mixins.CfnBotAliasPropsMixin.LambdaCodeHookProperty(
                        code_hook_interface_version="codeHookInterfaceVersion",
                        lambda_arn="lambdaArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6479f0fe12e9c75039408671ec26a2f1b077d9f7f7962f60e8ee421999943bb3)
                check_type(argname="argument lambda_code_hook", value=lambda_code_hook, expected_type=type_hints["lambda_code_hook"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_code_hook is not None:
                self._values["lambda_code_hook"] = lambda_code_hook

        @builtins.property
        def lambda_code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.LambdaCodeHookProperty"]]:
            '''Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-codehookspecification.html#cfn-lex-botalias-codehookspecification-lambdacodehook
            '''
            result = self._values.get("lambda_code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.LambdaCodeHookProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeHookSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.ConversationLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audio_log_settings": "audioLogSettings",
            "text_log_settings": "textLogSettings",
        },
    )
    class ConversationLogSettingsProperty:
        def __init__(
            self,
            *,
            audio_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.AudioLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            text_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.TextLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configures conversation logging that saves audio, text, and metadata for the conversations with your users.

            :param audio_log_settings: The Amazon S3 settings for logging audio to an S3 bucket.
            :param text_log_settings: The Amazon CloudWatch Logs settings for logging text and metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-conversationlogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                conversation_log_settings_property = lex_mixins.CfnBotAliasPropsMixin.ConversationLogSettingsProperty(
                    audio_log_settings=[lex_mixins.CfnBotAliasPropsMixin.AudioLogSettingProperty(
                        destination=lex_mixins.CfnBotAliasPropsMixin.AudioLogDestinationProperty(
                            s3_bucket=lex_mixins.CfnBotAliasPropsMixin.S3BucketLogDestinationProperty(
                                kms_key_arn="kmsKeyArn",
                                log_prefix="logPrefix",
                                s3_bucket_arn="s3BucketArn"
                            )
                        ),
                        enabled=False
                    )],
                    text_log_settings=[lex_mixins.CfnBotAliasPropsMixin.TextLogSettingProperty(
                        destination=lex_mixins.CfnBotAliasPropsMixin.TextLogDestinationProperty(
                            cloud_watch=lex_mixins.CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                                log_prefix="logPrefix"
                            )
                        ),
                        enabled=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9bf94cfd7cd760dd12f0b11ff76a8b51994f1fe18a799da64ba5def60c123da)
                check_type(argname="argument audio_log_settings", value=audio_log_settings, expected_type=type_hints["audio_log_settings"])
                check_type(argname="argument text_log_settings", value=text_log_settings, expected_type=type_hints["text_log_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audio_log_settings is not None:
                self._values["audio_log_settings"] = audio_log_settings
            if text_log_settings is not None:
                self._values["text_log_settings"] = text_log_settings

        @builtins.property
        def audio_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.AudioLogSettingProperty"]]]]:
            '''The Amazon S3 settings for logging audio to an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-conversationlogsettings.html#cfn-lex-botalias-conversationlogsettings-audiologsettings
            '''
            result = self._values.get("audio_log_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.AudioLogSettingProperty"]]]], result)

        @builtins.property
        def text_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.TextLogSettingProperty"]]]]:
            '''The Amazon CloudWatch Logs settings for logging text and metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-conversationlogsettings.html#cfn-lex-botalias-conversationlogsettings-textlogsettings
            '''
            result = self._values.get("text_log_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.TextLogSettingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConversationLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.LambdaCodeHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_hook_interface_version": "codeHookInterfaceVersion",
            "lambda_arn": "lambdaArn",
        },
    )
    class LambdaCodeHookProperty:
        def __init__(
            self,
            *,
            code_hook_interface_version: typing.Optional[builtins.str] = None,
            lambda_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :param code_hook_interface_version: The version of the request-response that you want Amazon Lex to use to invoke your Lambda function.
            :param lambda_arn: The Amazon Resource Name (ARN) of the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-lambdacodehook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                lambda_code_hook_property = lex_mixins.CfnBotAliasPropsMixin.LambdaCodeHookProperty(
                    code_hook_interface_version="codeHookInterfaceVersion",
                    lambda_arn="lambdaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__510cf49d7edc2082a0485f1317f4d11448d47e422b9866747b49fe3c932d9da3)
                check_type(argname="argument code_hook_interface_version", value=code_hook_interface_version, expected_type=type_hints["code_hook_interface_version"])
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_hook_interface_version is not None:
                self._values["code_hook_interface_version"] = code_hook_interface_version
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn

        @builtins.property
        def code_hook_interface_version(self) -> typing.Optional[builtins.str]:
            '''The version of the request-response that you want Amazon Lex to use to invoke your Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-lambdacodehook.html#cfn-lex-botalias-lambdacodehook-codehookinterfaceversion
            '''
            result = self._values.get("code_hook_interface_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-lambdacodehook.html#cfn-lex-botalias-lambdacodehook-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaCodeHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.S3BucketLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_key_arn": "kmsKeyArn",
            "log_prefix": "logPrefix",
            "s3_bucket_arn": "s3BucketArn",
        },
    )
    class S3BucketLogDestinationProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            log_prefix: typing.Optional[builtins.str] = None,
            s3_bucket_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an Amazon S3 bucket for logging audio conversations.

            :param kms_key_arn: The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key for encrypting audio log files stored in an Amazon S3 bucket.
            :param log_prefix: The S3 prefix to assign to audio log files.
            :param s3_bucket_arn: The Amazon Resource Name (ARN) of an Amazon S3 bucket where audio log files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                s3_bucket_log_destination_property = lex_mixins.CfnBotAliasPropsMixin.S3BucketLogDestinationProperty(
                    kms_key_arn="kmsKeyArn",
                    log_prefix="logPrefix",
                    s3_bucket_arn="s3BucketArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__340b02752f604b7faeffda18cb5fb1c33994c2743cc921e6f775471e211eefc9)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument log_prefix", value=log_prefix, expected_type=type_hints["log_prefix"])
                check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if log_prefix is not None:
                self._values["log_prefix"] = log_prefix
            if s3_bucket_arn is not None:
                self._values["s3_bucket_arn"] = s3_bucket_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key for encrypting audio log files stored in an Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html#cfn-lex-botalias-s3bucketlogdestination-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 prefix to assign to audio log files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html#cfn-lex-botalias-s3bucketlogdestination-logprefix
            '''
            result = self._values.get("log_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an Amazon S3 bucket where audio log files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html#cfn-lex-botalias-s3bucketlogdestination-s3bucketarn
            '''
            result = self._values.get("s3_bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.SentimentAnalysisSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"detect_sentiment": "detectSentiment"},
    )
    class SentimentAnalysisSettingsProperty:
        def __init__(
            self,
            *,
            detect_sentiment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.

            :param detect_sentiment: Sets whether Amazon Lex uses Amazon Comprehend to detect the sentiment of user utterances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-sentimentanalysissettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                sentiment_analysis_settings_property = lex_mixins.CfnBotAliasPropsMixin.SentimentAnalysisSettingsProperty(
                    detect_sentiment=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dfddf9a59cb60489978bba2af4978abd91049c87bfa2d6e03bc17556ce5ebdc3)
                check_type(argname="argument detect_sentiment", value=detect_sentiment, expected_type=type_hints["detect_sentiment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if detect_sentiment is not None:
                self._values["detect_sentiment"] = detect_sentiment

        @builtins.property
        def detect_sentiment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Sets whether Amazon Lex uses Amazon Comprehend to detect the sentiment of user utterances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-sentimentanalysissettings.html#cfn-lex-botalias-sentimentanalysissettings-detectsentiment
            '''
            result = self._values.get("detect_sentiment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SentimentAnalysisSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.TextLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch": "cloudWatch"},
    )
    class TextLogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines the Amazon CloudWatch Logs destination log group for conversation text logs.

            :param cloud_watch: Defines the Amazon CloudWatch Logs log group where text and metadata logs are delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                text_log_destination_property = lex_mixins.CfnBotAliasPropsMixin.TextLogDestinationProperty(
                    cloud_watch=lex_mixins.CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        log_prefix="logPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33a8281d0f49a02512996e751eb35c29b06b033ef5a529c0a3a58d6794b70be0)
                check_type(argname="argument cloud_watch", value=cloud_watch, expected_type=type_hints["cloud_watch"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch is not None:
                self._values["cloud_watch"] = cloud_watch

        @builtins.property
        def cloud_watch(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty"]]:
            '''Defines the Amazon CloudWatch Logs log group where text and metadata logs are delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogdestination.html#cfn-lex-botalias-textlogdestination-cloudwatch
            '''
            result = self._values.get("cloud_watch")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotAliasPropsMixin.TextLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "enabled": "enabled"},
    )
    class TextLogSettingProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotAliasPropsMixin.TextLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Defines settings to enable text conversation logs.

            :param destination: Defines the Amazon CloudWatch Logs destination log group for conversation text logs.
            :param enabled: Determines whether conversation logs should be stored for an alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                text_log_setting_property = lex_mixins.CfnBotAliasPropsMixin.TextLogSettingProperty(
                    destination=lex_mixins.CfnBotAliasPropsMixin.TextLogDestinationProperty(
                        cloud_watch=lex_mixins.CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                            cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                            log_prefix="logPrefix"
                        )
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc6c629db12a08bcbed282c8567199be27b25d5174326f8da9c7b4002d1fa872)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.TextLogDestinationProperty"]]:
            '''Defines the Amazon CloudWatch Logs destination log group for conversation text logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogsetting.html#cfn-lex-botalias-textlogsetting-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotAliasPropsMixin.TextLogDestinationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether conversation logs should be stored for an alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogsetting.html#cfn-lex-botalias-textlogsetting-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_build_bot_locales": "autoBuildBotLocales",
        "bot_file_s3_location": "botFileS3Location",
        "bot_locales": "botLocales",
        "bot_tags": "botTags",
        "data_privacy": "dataPrivacy",
        "description": "description",
        "error_log_settings": "errorLogSettings",
        "idle_session_ttl_in_seconds": "idleSessionTtlInSeconds",
        "name": "name",
        "replication": "replication",
        "role_arn": "roleArn",
        "test_bot_alias_settings": "testBotAliasSettings",
        "test_bot_alias_tags": "testBotAliasTags",
    },
)
class CfnBotMixinProps:
    def __init__(
        self,
        *,
        auto_build_bot_locales: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        bot_file_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        bot_locales: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BotLocaleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        bot_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        data_privacy: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        error_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ErrorLogSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        idle_session_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        replication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ReplicationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        test_bot_alias_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.TestBotAliasSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        test_bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnBotPropsMixin.

        :param auto_build_bot_locales: Indicates whether Amazon Lex V2 should automatically build the locales for the bot after a change.
        :param bot_file_s3_location: The Amazon S3 location of files used to import a bot. The files must be in the import format specified in `JSON format for importing and exporting <https://docs.aws.amazon.com/lexv2/latest/dg/import-export-format.html>`_ in the *Amazon Lex developer guide.*
        :param bot_locales: A list of locales for the bot.
        :param bot_tags: A list of tags to add to the bot. You can only add tags when you import a bot. You can't use the ``UpdateBot`` operation to update tags. To update tags, use the ``TagResource`` operation.
        :param data_privacy: By default, data stored by Amazon Lex is encrypted. The ``DataPrivacy`` structure provides settings that determine how Amazon Lex handles special cases of securing the data for your bot.
        :param description: The description of the version.
        :param error_log_settings: 
        :param idle_session_ttl_in_seconds: The time, in seconds, that Amazon Lex should keep information about a user's conversation with the bot. A user interaction remains active for the amount of time specified. If no conversation occurs during this time, the session expires and Amazon Lex deletes any data provided before the timeout. You can specify between 60 (1 minute) and 86,400 (24 hours) seconds.
        :param name: The name of the bot locale.
        :param replication: 
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role used to build and run the bot.
        :param test_bot_alias_settings: Specifies configuration settings for the alias used to test the bot. If the ``TestBotAliasSettings`` property is not specified, the settings are configured with default values.
        :param test_bot_alias_tags: A list of tags to add to the test alias for a bot. You can only add tags when you import a bot. You can't use the ``UpdateAlias`` operation to update tags. To update tags on the test alias, use the ``TagResource`` operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html
        :exampleMetadata: fixture=_generated

        Example::

            
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac4a5f33e7bcb194db79dade839c925e94f2ed71707f811e1264cd03da7331a)
            check_type(argname="argument auto_build_bot_locales", value=auto_build_bot_locales, expected_type=type_hints["auto_build_bot_locales"])
            check_type(argname="argument bot_file_s3_location", value=bot_file_s3_location, expected_type=type_hints["bot_file_s3_location"])
            check_type(argname="argument bot_locales", value=bot_locales, expected_type=type_hints["bot_locales"])
            check_type(argname="argument bot_tags", value=bot_tags, expected_type=type_hints["bot_tags"])
            check_type(argname="argument data_privacy", value=data_privacy, expected_type=type_hints["data_privacy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument error_log_settings", value=error_log_settings, expected_type=type_hints["error_log_settings"])
            check_type(argname="argument idle_session_ttl_in_seconds", value=idle_session_ttl_in_seconds, expected_type=type_hints["idle_session_ttl_in_seconds"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument replication", value=replication, expected_type=type_hints["replication"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument test_bot_alias_settings", value=test_bot_alias_settings, expected_type=type_hints["test_bot_alias_settings"])
            check_type(argname="argument test_bot_alias_tags", value=test_bot_alias_tags, expected_type=type_hints["test_bot_alias_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_build_bot_locales is not None:
            self._values["auto_build_bot_locales"] = auto_build_bot_locales
        if bot_file_s3_location is not None:
            self._values["bot_file_s3_location"] = bot_file_s3_location
        if bot_locales is not None:
            self._values["bot_locales"] = bot_locales
        if bot_tags is not None:
            self._values["bot_tags"] = bot_tags
        if data_privacy is not None:
            self._values["data_privacy"] = data_privacy
        if description is not None:
            self._values["description"] = description
        if error_log_settings is not None:
            self._values["error_log_settings"] = error_log_settings
        if idle_session_ttl_in_seconds is not None:
            self._values["idle_session_ttl_in_seconds"] = idle_session_ttl_in_seconds
        if name is not None:
            self._values["name"] = name
        if replication is not None:
            self._values["replication"] = replication
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if test_bot_alias_settings is not None:
            self._values["test_bot_alias_settings"] = test_bot_alias_settings
        if test_bot_alias_tags is not None:
            self._values["test_bot_alias_tags"] = test_bot_alias_tags

    @builtins.property
    def auto_build_bot_locales(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether Amazon Lex V2 should automatically build the locales for the bot after a change.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-autobuildbotlocales
        '''
        result = self._values.get("auto_build_bot_locales")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def bot_file_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.S3LocationProperty"]]:
        '''The Amazon S3 location of files used to import a bot.

        The files must be in the import format specified in `JSON format for importing and exporting <https://docs.aws.amazon.com/lexv2/latest/dg/import-export-format.html>`_ in the *Amazon Lex developer guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-botfiles3location
        '''
        result = self._values.get("bot_file_s3_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def bot_locales(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BotLocaleProperty"]]]]:
        '''A list of locales for the bot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-botlocales
        '''
        result = self._values.get("bot_locales")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BotLocaleProperty"]]]], result)

    @builtins.property
    def bot_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
        '''A list of tags to add to the bot.

        You can only add tags when you import a bot. You can't use the ``UpdateBot`` operation to update tags. To update tags, use the ``TagResource`` operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-bottags
        '''
        result = self._values.get("bot_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

    @builtins.property
    def data_privacy(self) -> typing.Any:
        '''By default, data stored by Amazon Lex is encrypted.

        The ``DataPrivacy`` structure provides settings that determine how Amazon Lex handles special cases of securing the data for your bot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-dataprivacy
        '''
        result = self._values.get("data_privacy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_log_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ErrorLogSettingsProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-errorlogsettings
        '''
        result = self._values.get("error_log_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ErrorLogSettingsProperty"]], result)

    @builtins.property
    def idle_session_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The time, in seconds, that Amazon Lex should keep information about a user's conversation with the bot.

        A user interaction remains active for the amount of time specified. If no conversation occurs during this time, the session expires and Amazon Lex deletes any data provided before the timeout.

        You can specify between 60 (1 minute) and 86,400 (24 hours) seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-idlesessionttlinseconds
        '''
        result = self._values.get("idle_session_ttl_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bot locale.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ReplicationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-replication
        '''
        result = self._values.get("replication")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ReplicationProperty"]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role used to build and run the bot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_bot_alias_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.TestBotAliasSettingsProperty"]]:
        '''Specifies configuration settings for the alias used to test the bot.

        If the ``TestBotAliasSettings`` property is not specified, the settings are configured with default values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-testbotaliassettings
        '''
        result = self._values.get("test_bot_alias_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.TestBotAliasSettingsProperty"]], result)

    @builtins.property
    def test_bot_alias_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
        '''A list of tags to add to the test alias for a bot.

        You can only add tags when you import a bot. You can't use the ``UpdateAlias`` operation to update tags. To update tags on the test alias, use the ``TagResource`` operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-testbotaliastags
        '''
        result = self._values.get("test_bot_alias_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBotMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBotPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin",
):
    '''.. epigraph::

   Amazon Lex V2 is the only supported version in CloudFormation .

    Specifies an Amazon Lex conversational bot.

    You must configure an intent based on the ``AMAZON.FallbackIntent`` built-in intent. If you don't add one, creating the bot will fail.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html
    :cloudformationResource: AWS::Lex::Bot
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        
    '''

    def __init__(
        self,
        props: typing.Union[CfnBotMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lex::Bot``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a72e8cef14da203cbe64e3cdee10c62ee8d0c1280398eea76fb0d4c3ba784d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f010adfc261d26131b656df83cf25b09dea5ab528d8c10653d8eb4698bf03496)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84c20790560b99ec7c13569f060c9a24d86f85d417daee6a29736ec4e440c7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBotMixinProps:
        return typing.cast(CfnBotMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.AdvancedRecognitionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"audio_recognition_strategy": "audioRecognitionStrategy"},
    )
    class AdvancedRecognitionSettingProperty:
        def __init__(
            self,
            *,
            audio_recognition_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides settings that enable advanced recognition settings for slot values.

            :param audio_recognition_strategy: Enables using the slot values as a custom vocabulary for recognizing user utterances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-advancedrecognitionsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                advanced_recognition_setting_property = lex_mixins.CfnBotPropsMixin.AdvancedRecognitionSettingProperty(
                    audio_recognition_strategy="audioRecognitionStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38c0c24e0e67a695c82627d95be037d05d2365b0d7eee65ec23e450301de8924)
                check_type(argname="argument audio_recognition_strategy", value=audio_recognition_strategy, expected_type=type_hints["audio_recognition_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audio_recognition_strategy is not None:
                self._values["audio_recognition_strategy"] = audio_recognition_strategy

        @builtins.property
        def audio_recognition_strategy(self) -> typing.Optional[builtins.str]:
            '''Enables using the slot values as a custom vocabulary for recognizing user utterances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-advancedrecognitionsetting.html#cfn-lex-bot-advancedrecognitionsetting-audiorecognitionstrategy
            '''
            result = self._values.get("audio_recognition_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedRecognitionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.AllowedInputTypesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_audio_input": "allowAudioInput",
            "allow_dtmf_input": "allowDtmfInput",
        },
    )
    class AllowedInputTypesProperty:
        def __init__(
            self,
            *,
            allow_audio_input: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            allow_dtmf_input: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies the allowed input types.

            :param allow_audio_input: Indicates whether audio input is allowed.
            :param allow_dtmf_input: Indicates whether DTMF input is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-allowedinputtypes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                allowed_input_types_property = lex_mixins.CfnBotPropsMixin.AllowedInputTypesProperty(
                    allow_audio_input=False,
                    allow_dtmf_input=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db718b6a1127bddbf4f3f8c9a58c249b627856a20570d8af9409008bf31fab37)
                check_type(argname="argument allow_audio_input", value=allow_audio_input, expected_type=type_hints["allow_audio_input"])
                check_type(argname="argument allow_dtmf_input", value=allow_dtmf_input, expected_type=type_hints["allow_dtmf_input"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_audio_input is not None:
                self._values["allow_audio_input"] = allow_audio_input
            if allow_dtmf_input is not None:
                self._values["allow_dtmf_input"] = allow_dtmf_input

        @builtins.property
        def allow_audio_input(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether audio input is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-allowedinputtypes.html#cfn-lex-bot-allowedinputtypes-allowaudioinput
            '''
            result = self._values.get("allow_audio_input")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def allow_dtmf_input(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether DTMF input is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-allowedinputtypes.html#cfn-lex-bot-allowedinputtypes-allowdtmfinput
            '''
            result = self._values.get("allow_dtmf_input")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AllowedInputTypesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audio_specification": "audioSpecification",
            "dtmf_specification": "dtmfSpecification",
            "start_timeout_ms": "startTimeoutMs",
        },
    )
    class AudioAndDTMFInputSpecificationProperty:
        def __init__(
            self,
            *,
            audio_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.AudioSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dtmf_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DTMFSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            start_timeout_ms: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the audio and DTMF input specification.

            :param audio_specification: Specifies the settings on audio input.
            :param dtmf_specification: Specifies the settings on DTMF input.
            :param start_timeout_ms: Time for which a bot waits before assuming that the customer isn't going to speak or press a key. This timeout is shared between Audio and DTMF inputs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audioanddtmfinputspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                audio_and_dTMFInput_specification_property = lex_mixins.CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty(
                    audio_specification=lex_mixins.CfnBotPropsMixin.AudioSpecificationProperty(
                        end_timeout_ms=123,
                        max_length_ms=123
                    ),
                    dtmf_specification=lex_mixins.CfnBotPropsMixin.DTMFSpecificationProperty(
                        deletion_character="deletionCharacter",
                        end_character="endCharacter",
                        end_timeout_ms=123,
                        max_length=123
                    ),
                    start_timeout_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eebd7e13b0d7e1091e72d60c2f3252e8a83e558c66cb44e5d3e77e17c3db2775)
                check_type(argname="argument audio_specification", value=audio_specification, expected_type=type_hints["audio_specification"])
                check_type(argname="argument dtmf_specification", value=dtmf_specification, expected_type=type_hints["dtmf_specification"])
                check_type(argname="argument start_timeout_ms", value=start_timeout_ms, expected_type=type_hints["start_timeout_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audio_specification is not None:
                self._values["audio_specification"] = audio_specification
            if dtmf_specification is not None:
                self._values["dtmf_specification"] = dtmf_specification
            if start_timeout_ms is not None:
                self._values["start_timeout_ms"] = start_timeout_ms

        @builtins.property
        def audio_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AudioSpecificationProperty"]]:
            '''Specifies the settings on audio input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audioanddtmfinputspecification.html#cfn-lex-bot-audioanddtmfinputspecification-audiospecification
            '''
            result = self._values.get("audio_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AudioSpecificationProperty"]], result)

        @builtins.property
        def dtmf_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DTMFSpecificationProperty"]]:
            '''Specifies the settings on DTMF input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audioanddtmfinputspecification.html#cfn-lex-bot-audioanddtmfinputspecification-dtmfspecification
            '''
            result = self._values.get("dtmf_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DTMFSpecificationProperty"]], result)

        @builtins.property
        def start_timeout_ms(self) -> typing.Optional[jsii.Number]:
            '''Time for which a bot waits before assuming that the customer isn't going to speak or press a key.

            This timeout is shared between Audio and DTMF inputs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audioanddtmfinputspecification.html#cfn-lex-bot-audioanddtmfinputspecification-starttimeoutms
            '''
            result = self._values.get("start_timeout_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioAndDTMFInputSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.AudioLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket"},
    )
    class AudioLogDestinationProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.S3BucketLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The location of audio log files collected when conversation logging is enabled for a bot.

            :param s3_bucket: Specifies the Amazon S3 bucket where the audio files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiologdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                audio_log_destination_property = lex_mixins.CfnBotPropsMixin.AudioLogDestinationProperty(
                    s3_bucket=lex_mixins.CfnBotPropsMixin.S3BucketLogDestinationProperty(
                        kms_key_arn="kmsKeyArn",
                        log_prefix="logPrefix",
                        s3_bucket_arn="s3BucketArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89f15742a318baf397d12e9b34cf81cdbf3b2663f5f307195a9a26794152033d)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket

        @builtins.property
        def s3_bucket(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.S3BucketLogDestinationProperty"]]:
            '''Specifies the Amazon S3 bucket where the audio files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiologdestination.html#cfn-lex-bot-audiologdestination-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.S3BucketLogDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.AudioLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "enabled": "enabled"},
    )
    class AudioLogSettingProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.AudioLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Settings for logging audio of conversations between Amazon Lex and a user.

            You specify whether to log audio and the Amazon S3 bucket where the audio file is stored.

            :param destination: Specifies the location of the audio log files collected when conversation logging is enabled for a bot.
            :param enabled: Determines whether audio logging in enabled for the bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiologsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                audio_log_setting_property = lex_mixins.CfnBotPropsMixin.AudioLogSettingProperty(
                    destination=lex_mixins.CfnBotPropsMixin.AudioLogDestinationProperty(
                        s3_bucket=lex_mixins.CfnBotPropsMixin.S3BucketLogDestinationProperty(
                            kms_key_arn="kmsKeyArn",
                            log_prefix="logPrefix",
                            s3_bucket_arn="s3BucketArn"
                        )
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__492df9a0be37577091f5ca90cf7273ee66d12cb52bb0f58a8f16044f2b9d5d32)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AudioLogDestinationProperty"]]:
            '''Specifies the location of the audio log files collected when conversation logging is enabled for a bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiologsetting.html#cfn-lex-bot-audiologsetting-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AudioLogDestinationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether audio logging in enabled for the bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiologsetting.html#cfn-lex-bot-audiologsetting-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.AudioSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_timeout_ms": "endTimeoutMs",
            "max_length_ms": "maxLengthMs",
        },
    )
    class AudioSpecificationProperty:
        def __init__(
            self,
            *,
            end_timeout_ms: typing.Optional[jsii.Number] = None,
            max_length_ms: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the audio input specifications.

            :param end_timeout_ms: Time for which a bot waits after the customer stops speaking to assume the utterance is finished.
            :param max_length_ms: Time for how long Amazon Lex waits before speech input is truncated and the speech is returned to application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiospecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                audio_specification_property = lex_mixins.CfnBotPropsMixin.AudioSpecificationProperty(
                    end_timeout_ms=123,
                    max_length_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b72d80dee15336a528f96ef836b2893e1d6e2ae3f970220859f0beadb41ec41)
                check_type(argname="argument end_timeout_ms", value=end_timeout_ms, expected_type=type_hints["end_timeout_ms"])
                check_type(argname="argument max_length_ms", value=max_length_ms, expected_type=type_hints["max_length_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_timeout_ms is not None:
                self._values["end_timeout_ms"] = end_timeout_ms
            if max_length_ms is not None:
                self._values["max_length_ms"] = max_length_ms

        @builtins.property
        def end_timeout_ms(self) -> typing.Optional[jsii.Number]:
            '''Time for which a bot waits after the customer stops speaking to assume the utterance is finished.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiospecification.html#cfn-lex-bot-audiospecification-endtimeoutms
            '''
            result = self._values.get("end_timeout_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_length_ms(self) -> typing.Optional[jsii.Number]:
            '''Time for how long Amazon Lex waits before speech input is truncated and the speech is returned to application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiospecification.html#cfn-lex-bot-audiospecification-maxlengthms
            '''
            result = self._values.get("max_length_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BKBExactResponseFieldsProperty",
        jsii_struct_bases=[],
        name_mapping={"answer_field": "answerField"},
    )
    class BKBExactResponseFieldsProperty:
        def __init__(
            self,
            *,
            answer_field: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param answer_field: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bkbexactresponsefields.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                b_kBExact_response_fields_property = lex_mixins.CfnBotPropsMixin.BKBExactResponseFieldsProperty(
                    answer_field="answerField"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3366b6d616c8610541175c5fa439ebb0948d9ca21c73eac6f72061667400d29)
                check_type(argname="argument answer_field", value=answer_field, expected_type=type_hints["answer_field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_field is not None:
                self._values["answer_field"] = answer_field

        @builtins.property
        def answer_field(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bkbexactresponsefields.html#cfn-lex-bot-bkbexactresponsefields-answerfield
            '''
            result = self._values.get("answer_field")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BKBExactResponseFieldsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BedrockAgentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_agent_alias_id": "bedrockAgentAliasId",
            "bedrock_agent_id": "bedrockAgentId",
        },
    )
    class BedrockAgentConfigurationProperty:
        def __init__(
            self,
            *,
            bedrock_agent_alias_id: typing.Optional[builtins.str] = None,
            bedrock_agent_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bedrock_agent_alias_id: 
            :param bedrock_agent_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockagentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bedrock_agent_configuration_property = lex_mixins.CfnBotPropsMixin.BedrockAgentConfigurationProperty(
                    bedrock_agent_alias_id="bedrockAgentAliasId",
                    bedrock_agent_id="bedrockAgentId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dab7eb2b33dbad5e3932abb44e75d3a903e4e3292e55739cd6c8693863e3db3f)
                check_type(argname="argument bedrock_agent_alias_id", value=bedrock_agent_alias_id, expected_type=type_hints["bedrock_agent_alias_id"])
                check_type(argname="argument bedrock_agent_id", value=bedrock_agent_id, expected_type=type_hints["bedrock_agent_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_agent_alias_id is not None:
                self._values["bedrock_agent_alias_id"] = bedrock_agent_alias_id
            if bedrock_agent_id is not None:
                self._values["bedrock_agent_id"] = bedrock_agent_id

        @builtins.property
        def bedrock_agent_alias_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockagentconfiguration.html#cfn-lex-bot-bedrockagentconfiguration-bedrockagentaliasid
            '''
            result = self._values.get("bedrock_agent_alias_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bedrock_agent_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockagentconfiguration.html#cfn-lex-bot-bedrockagentconfiguration-bedrockagentid
            '''
            result = self._values.get("bedrock_agent_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BedrockAgentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BedrockAgentIntentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_agent_configuration": "bedrockAgentConfiguration",
            "bedrock_agent_intent_knowledge_base_configuration": "bedrockAgentIntentKnowledgeBaseConfiguration",
        },
    )
    class BedrockAgentIntentConfigurationProperty:
        def __init__(
            self,
            *,
            bedrock_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BedrockAgentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            bedrock_agent_intent_knowledge_base_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BedrockAgentIntentKnowledgeBaseConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param bedrock_agent_configuration: 
            :param bedrock_agent_intent_knowledge_base_configuration: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockagentintentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bedrock_agent_intent_configuration_property = lex_mixins.CfnBotPropsMixin.BedrockAgentIntentConfigurationProperty(
                    bedrock_agent_configuration=lex_mixins.CfnBotPropsMixin.BedrockAgentConfigurationProperty(
                        bedrock_agent_alias_id="bedrockAgentAliasId",
                        bedrock_agent_id="bedrockAgentId"
                    ),
                    bedrock_agent_intent_knowledge_base_configuration=lex_mixins.CfnBotPropsMixin.BedrockAgentIntentKnowledgeBaseConfigurationProperty(
                        bedrock_knowledge_base_arn="bedrockKnowledgeBaseArn",
                        bedrock_model_configuration=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                            bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                                bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                                bedrock_guardrail_version="bedrockGuardrailVersion"
                            ),
                            bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                            bedrock_trace_status="bedrockTraceStatus",
                            model_arn="modelArn"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__35591dafaa33a797121ef28b53474e4cd4717d9087fa7fed06fe5a7264b4a8cd)
                check_type(argname="argument bedrock_agent_configuration", value=bedrock_agent_configuration, expected_type=type_hints["bedrock_agent_configuration"])
                check_type(argname="argument bedrock_agent_intent_knowledge_base_configuration", value=bedrock_agent_intent_knowledge_base_configuration, expected_type=type_hints["bedrock_agent_intent_knowledge_base_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_agent_configuration is not None:
                self._values["bedrock_agent_configuration"] = bedrock_agent_configuration
            if bedrock_agent_intent_knowledge_base_configuration is not None:
                self._values["bedrock_agent_intent_knowledge_base_configuration"] = bedrock_agent_intent_knowledge_base_configuration

        @builtins.property
        def bedrock_agent_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockAgentConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockagentintentconfiguration.html#cfn-lex-bot-bedrockagentintentconfiguration-bedrockagentconfiguration
            '''
            result = self._values.get("bedrock_agent_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockAgentConfigurationProperty"]], result)

        @builtins.property
        def bedrock_agent_intent_knowledge_base_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockAgentIntentKnowledgeBaseConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockagentintentconfiguration.html#cfn-lex-bot-bedrockagentintentconfiguration-bedrockagentintentknowledgebaseconfiguration
            '''
            result = self._values.get("bedrock_agent_intent_knowledge_base_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockAgentIntentKnowledgeBaseConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BedrockAgentIntentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BedrockAgentIntentKnowledgeBaseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_knowledge_base_arn": "bedrockKnowledgeBaseArn",
            "bedrock_model_configuration": "bedrockModelConfiguration",
        },
    )
    class BedrockAgentIntentKnowledgeBaseConfigurationProperty:
        def __init__(
            self,
            *,
            bedrock_knowledge_base_arn: typing.Optional[builtins.str] = None,
            bedrock_model_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BedrockModelSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param bedrock_knowledge_base_arn: 
            :param bedrock_model_configuration: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockagentintentknowledgebaseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bedrock_agent_intent_knowledge_base_configuration_property = lex_mixins.CfnBotPropsMixin.BedrockAgentIntentKnowledgeBaseConfigurationProperty(
                    bedrock_knowledge_base_arn="bedrockKnowledgeBaseArn",
                    bedrock_model_configuration=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                        bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                            bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                            bedrock_guardrail_version="bedrockGuardrailVersion"
                        ),
                        bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                        bedrock_trace_status="bedrockTraceStatus",
                        model_arn="modelArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2df08bfc9575cf7f6b561aacd127b8bbc920209a5b931a79e6b7face9cc48080)
                check_type(argname="argument bedrock_knowledge_base_arn", value=bedrock_knowledge_base_arn, expected_type=type_hints["bedrock_knowledge_base_arn"])
                check_type(argname="argument bedrock_model_configuration", value=bedrock_model_configuration, expected_type=type_hints["bedrock_model_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_knowledge_base_arn is not None:
                self._values["bedrock_knowledge_base_arn"] = bedrock_knowledge_base_arn
            if bedrock_model_configuration is not None:
                self._values["bedrock_model_configuration"] = bedrock_model_configuration

        @builtins.property
        def bedrock_knowledge_base_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockagentintentknowledgebaseconfiguration.html#cfn-lex-bot-bedrockagentintentknowledgebaseconfiguration-bedrockknowledgebasearn
            '''
            result = self._values.get("bedrock_knowledge_base_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bedrock_model_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockModelSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockagentintentknowledgebaseconfiguration.html#cfn-lex-bot-bedrockagentintentknowledgebaseconfiguration-bedrockmodelconfiguration
            '''
            result = self._values.get("bedrock_model_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockModelSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BedrockAgentIntentKnowledgeBaseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_guardrail_identifier": "bedrockGuardrailIdentifier",
            "bedrock_guardrail_version": "bedrockGuardrailVersion",
        },
    )
    class BedrockGuardrailConfigurationProperty:
        def __init__(
            self,
            *,
            bedrock_guardrail_identifier: typing.Optional[builtins.str] = None,
            bedrock_guardrail_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details on the Bedrock guardrail configuration.

            :param bedrock_guardrail_identifier: 
            :param bedrock_guardrail_version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockguardrailconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bedrock_guardrail_configuration_property = lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                    bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                    bedrock_guardrail_version="bedrockGuardrailVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6c8e4bb8569909355e9c8e82810c046ddbc12d4d77aa6b525f97006d392d0fa)
                check_type(argname="argument bedrock_guardrail_identifier", value=bedrock_guardrail_identifier, expected_type=type_hints["bedrock_guardrail_identifier"])
                check_type(argname="argument bedrock_guardrail_version", value=bedrock_guardrail_version, expected_type=type_hints["bedrock_guardrail_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_guardrail_identifier is not None:
                self._values["bedrock_guardrail_identifier"] = bedrock_guardrail_identifier
            if bedrock_guardrail_version is not None:
                self._values["bedrock_guardrail_version"] = bedrock_guardrail_version

        @builtins.property
        def bedrock_guardrail_identifier(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockguardrailconfiguration.html#cfn-lex-bot-bedrockguardrailconfiguration-bedrockguardrailidentifier
            '''
            result = self._values.get("bedrock_guardrail_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bedrock_guardrail_version(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockguardrailconfiguration.html#cfn-lex-bot-bedrockguardrailconfiguration-bedrockguardrailversion
            '''
            result = self._values.get("bedrock_guardrail_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BedrockGuardrailConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BedrockKnowledgeStoreConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_knowledge_base_arn": "bedrockKnowledgeBaseArn",
            "bkb_exact_response_fields": "bkbExactResponseFields",
            "exact_response": "exactResponse",
        },
    )
    class BedrockKnowledgeStoreConfigurationProperty:
        def __init__(
            self,
            *,
            bedrock_knowledge_base_arn: typing.Optional[builtins.str] = None,
            bkb_exact_response_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BKBExactResponseFieldsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exact_response: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains details about the configuration of a Amazon Bedrock knowledge base.

            :param bedrock_knowledge_base_arn: The base ARN of the knowledge base used.
            :param bkb_exact_response_fields: 
            :param exact_response: Specifies whether to return an exact response, or to return an answer generated by the model, using the fields you specify from the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockknowledgestoreconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bedrock_knowledge_store_configuration_property = lex_mixins.CfnBotPropsMixin.BedrockKnowledgeStoreConfigurationProperty(
                    bedrock_knowledge_base_arn="bedrockKnowledgeBaseArn",
                    bkb_exact_response_fields=lex_mixins.CfnBotPropsMixin.BKBExactResponseFieldsProperty(
                        answer_field="answerField"
                    ),
                    exact_response=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__659010913dacf5dc1afa2280f7c714558e3e52213f0a82ac4ddf7f2d7a573673)
                check_type(argname="argument bedrock_knowledge_base_arn", value=bedrock_knowledge_base_arn, expected_type=type_hints["bedrock_knowledge_base_arn"])
                check_type(argname="argument bkb_exact_response_fields", value=bkb_exact_response_fields, expected_type=type_hints["bkb_exact_response_fields"])
                check_type(argname="argument exact_response", value=exact_response, expected_type=type_hints["exact_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_knowledge_base_arn is not None:
                self._values["bedrock_knowledge_base_arn"] = bedrock_knowledge_base_arn
            if bkb_exact_response_fields is not None:
                self._values["bkb_exact_response_fields"] = bkb_exact_response_fields
            if exact_response is not None:
                self._values["exact_response"] = exact_response

        @builtins.property
        def bedrock_knowledge_base_arn(self) -> typing.Optional[builtins.str]:
            '''The base ARN of the knowledge base used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockknowledgestoreconfiguration.html#cfn-lex-bot-bedrockknowledgestoreconfiguration-bedrockknowledgebasearn
            '''
            result = self._values.get("bedrock_knowledge_base_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bkb_exact_response_fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BKBExactResponseFieldsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockknowledgestoreconfiguration.html#cfn-lex-bot-bedrockknowledgestoreconfiguration-bkbexactresponsefields
            '''
            result = self._values.get("bkb_exact_response_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BKBExactResponseFieldsProperty"]], result)

        @builtins.property
        def exact_response(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to return an exact response, or to return an answer generated by the model, using the fields you specify from the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockknowledgestoreconfiguration.html#cfn-lex-bot-bedrockknowledgestoreconfiguration-exactresponse
            '''
            result = self._values.get("exact_response")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BedrockKnowledgeStoreConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_guardrail_configuration": "bedrockGuardrailConfiguration",
            "bedrock_model_custom_prompt": "bedrockModelCustomPrompt",
            "bedrock_trace_status": "bedrockTraceStatus",
            "model_arn": "modelArn",
        },
    )
    class BedrockModelSpecificationProperty:
        def __init__(
            self,
            *,
            bedrock_guardrail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BedrockGuardrailConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            bedrock_model_custom_prompt: typing.Optional[builtins.str] = None,
            bedrock_trace_status: typing.Optional[builtins.str] = None,
            model_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the Amazon Bedrock model used to interpret the prompt used in descriptive bot building.

            :param bedrock_guardrail_configuration: 
            :param bedrock_model_custom_prompt: 
            :param bedrock_trace_status: 
            :param model_arn: The ARN of the foundation model used in descriptive bot building.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockmodelspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bedrock_model_specification_property = lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                    bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                        bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                        bedrock_guardrail_version="bedrockGuardrailVersion"
                    ),
                    bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                    bedrock_trace_status="bedrockTraceStatus",
                    model_arn="modelArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49fb56b72b629e63eb7265407b77e6d7c0d666a6e4a034e85646530feacbb10e)
                check_type(argname="argument bedrock_guardrail_configuration", value=bedrock_guardrail_configuration, expected_type=type_hints["bedrock_guardrail_configuration"])
                check_type(argname="argument bedrock_model_custom_prompt", value=bedrock_model_custom_prompt, expected_type=type_hints["bedrock_model_custom_prompt"])
                check_type(argname="argument bedrock_trace_status", value=bedrock_trace_status, expected_type=type_hints["bedrock_trace_status"])
                check_type(argname="argument model_arn", value=model_arn, expected_type=type_hints["model_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_guardrail_configuration is not None:
                self._values["bedrock_guardrail_configuration"] = bedrock_guardrail_configuration
            if bedrock_model_custom_prompt is not None:
                self._values["bedrock_model_custom_prompt"] = bedrock_model_custom_prompt
            if bedrock_trace_status is not None:
                self._values["bedrock_trace_status"] = bedrock_trace_status
            if model_arn is not None:
                self._values["model_arn"] = model_arn

        @builtins.property
        def bedrock_guardrail_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockGuardrailConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockmodelspecification.html#cfn-lex-bot-bedrockmodelspecification-bedrockguardrailconfiguration
            '''
            result = self._values.get("bedrock_guardrail_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockGuardrailConfigurationProperty"]], result)

        @builtins.property
        def bedrock_model_custom_prompt(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockmodelspecification.html#cfn-lex-bot-bedrockmodelspecification-bedrockmodelcustomprompt
            '''
            result = self._values.get("bedrock_model_custom_prompt")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bedrock_trace_status(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockmodelspecification.html#cfn-lex-bot-bedrockmodelspecification-bedrocktracestatus
            '''
            result = self._values.get("bedrock_trace_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the foundation model used in descriptive bot building.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-bedrockmodelspecification.html#cfn-lex-bot-bedrockmodelspecification-modelarn
            '''
            result = self._values.get("model_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BedrockModelSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BotAliasLocaleSettingsItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bot_alias_locale_setting": "botAliasLocaleSetting",
            "locale_id": "localeId",
        },
    )
    class BotAliasLocaleSettingsItemProperty:
        def __init__(
            self,
            *,
            bot_alias_locale_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BotAliasLocaleSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            locale_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies locale settings for a single locale.

            :param bot_alias_locale_setting: Specifies locale settings for a locale.
            :param locale_id: Specifies the locale that the settings apply to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettingsitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bot_alias_locale_settings_item_property = lex_mixins.CfnBotPropsMixin.BotAliasLocaleSettingsItemProperty(
                    bot_alias_locale_setting=lex_mixins.CfnBotPropsMixin.BotAliasLocaleSettingsProperty(
                        code_hook_specification=lex_mixins.CfnBotPropsMixin.CodeHookSpecificationProperty(
                            lambda_code_hook=lex_mixins.CfnBotPropsMixin.LambdaCodeHookProperty(
                                code_hook_interface_version="codeHookInterfaceVersion",
                                lambda_arn="lambdaArn"
                            )
                        ),
                        enabled=False
                    ),
                    locale_id="localeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38269c5ab5f29b10562472cb6d0c63741ec14908fc1e4ca80a27b4750867434f)
                check_type(argname="argument bot_alias_locale_setting", value=bot_alias_locale_setting, expected_type=type_hints["bot_alias_locale_setting"])
                check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bot_alias_locale_setting is not None:
                self._values["bot_alias_locale_setting"] = bot_alias_locale_setting
            if locale_id is not None:
                self._values["locale_id"] = locale_id

        @builtins.property
        def bot_alias_locale_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BotAliasLocaleSettingsProperty"]]:
            '''Specifies locale settings for a locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettingsitem.html#cfn-lex-bot-botaliaslocalesettingsitem-botaliaslocalesetting
            '''
            result = self._values.get("bot_alias_locale_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BotAliasLocaleSettingsProperty"]], result)

        @builtins.property
        def locale_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the locale that the settings apply to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettingsitem.html#cfn-lex-bot-botaliaslocalesettingsitem-localeid
            '''
            result = self._values.get("locale_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotAliasLocaleSettingsItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BotAliasLocaleSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_hook_specification": "codeHookSpecification",
            "enabled": "enabled",
        },
    )
    class BotAliasLocaleSettingsProperty:
        def __init__(
            self,
            *,
            code_hook_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.CodeHookSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies settings that are unique to a locale.

            For example, you can use different Lambda function depending on the bot's locale.

            :param code_hook_specification: Specifies the Lambda function that should be used in the locale.
            :param enabled: Determines whether the locale is enabled for the bot. If the value is ``false`` , the locale isn't available for use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bot_alias_locale_settings_property = lex_mixins.CfnBotPropsMixin.BotAliasLocaleSettingsProperty(
                    code_hook_specification=lex_mixins.CfnBotPropsMixin.CodeHookSpecificationProperty(
                        lambda_code_hook=lex_mixins.CfnBotPropsMixin.LambdaCodeHookProperty(
                            code_hook_interface_version="codeHookInterfaceVersion",
                            lambda_arn="lambdaArn"
                        )
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d1cde1bb50c6d19ef7f5eb02cfbe37e80b13cd1c3906fce7776f5e5414d4b8d)
                check_type(argname="argument code_hook_specification", value=code_hook_specification, expected_type=type_hints["code_hook_specification"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_hook_specification is not None:
                self._values["code_hook_specification"] = code_hook_specification
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def code_hook_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CodeHookSpecificationProperty"]]:
            '''Specifies the Lambda function that should be used in the locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettings.html#cfn-lex-bot-botaliaslocalesettings-codehookspecification
            '''
            result = self._values.get("code_hook_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CodeHookSpecificationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the locale is enabled for the bot.

            If the value is ``false`` , the locale isn't available for use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettings.html#cfn-lex-bot-botaliaslocalesettings-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotAliasLocaleSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BotLocaleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_vocabulary": "customVocabulary",
            "description": "description",
            "generative_ai_settings": "generativeAiSettings",
            "intents": "intents",
            "locale_id": "localeId",
            "nlu_confidence_threshold": "nluConfidenceThreshold",
            "slot_types": "slotTypes",
            "voice_settings": "voiceSettings",
        },
    )
    class BotLocaleProperty:
        def __init__(
            self,
            *,
            custom_vocabulary: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.CustomVocabularyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            generative_ai_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.GenerativeAISettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            intents: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.IntentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            locale_id: typing.Optional[builtins.str] = None,
            nlu_confidence_threshold: typing.Optional[jsii.Number] = None,
            slot_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            voice_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.VoiceSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides configuration information for a locale.

            :param custom_vocabulary: Specifies a custom vocabulary to use with a specific locale.
            :param description: A description of the bot locale. Use this to help identify the bot locale in lists.
            :param generative_ai_settings: 
            :param intents: One or more intents defined for the locale.
            :param locale_id: The identifier of the language and locale that the bot will be used in. The string must match one of the supported locales.
            :param nlu_confidence_threshold: Determines the threshold where Amazon Lex will insert the ``AMAZON.FallbackIntent`` , ``AMAZON.KendraSearchIntent`` , or both when returning alternative intents. You must configure an ``AMAZON.FallbackIntent`` . ``AMAZON.KendraSearchIntent`` is only inserted if it is configured for the bot.
            :param slot_types: One or more slot types defined for the locale.
            :param voice_settings: Defines settings for using an Amazon Polly voice to communicate with a user. Valid values include: - ``standard`` - ``neural`` - ``long-form`` - ``generative``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__10d36c996917176b42491668d78625d07102ace7655cecb2eeca1517b7479ce5)
                check_type(argname="argument custom_vocabulary", value=custom_vocabulary, expected_type=type_hints["custom_vocabulary"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument generative_ai_settings", value=generative_ai_settings, expected_type=type_hints["generative_ai_settings"])
                check_type(argname="argument intents", value=intents, expected_type=type_hints["intents"])
                check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
                check_type(argname="argument nlu_confidence_threshold", value=nlu_confidence_threshold, expected_type=type_hints["nlu_confidence_threshold"])
                check_type(argname="argument slot_types", value=slot_types, expected_type=type_hints["slot_types"])
                check_type(argname="argument voice_settings", value=voice_settings, expected_type=type_hints["voice_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_vocabulary is not None:
                self._values["custom_vocabulary"] = custom_vocabulary
            if description is not None:
                self._values["description"] = description
            if generative_ai_settings is not None:
                self._values["generative_ai_settings"] = generative_ai_settings
            if intents is not None:
                self._values["intents"] = intents
            if locale_id is not None:
                self._values["locale_id"] = locale_id
            if nlu_confidence_threshold is not None:
                self._values["nlu_confidence_threshold"] = nlu_confidence_threshold
            if slot_types is not None:
                self._values["slot_types"] = slot_types
            if voice_settings is not None:
                self._values["voice_settings"] = voice_settings

        @builtins.property
        def custom_vocabulary(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CustomVocabularyProperty"]]:
            '''Specifies a custom vocabulary to use with a specific locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-customvocabulary
            '''
            result = self._values.get("custom_vocabulary")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CustomVocabularyProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the bot locale.

            Use this to help identify the bot locale in lists.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def generative_ai_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.GenerativeAISettingsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-generativeaisettings
            '''
            result = self._values.get("generative_ai_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.GenerativeAISettingsProperty"]], result)

        @builtins.property
        def intents(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.IntentProperty"]]]]:
            '''One or more intents defined for the locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-intents
            '''
            result = self._values.get("intents")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.IntentProperty"]]]], result)

        @builtins.property
        def locale_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the language and locale that the bot will be used in.

            The string must match one of the supported locales.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-localeid
            '''
            result = self._values.get("locale_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nlu_confidence_threshold(self) -> typing.Optional[jsii.Number]:
            '''Determines the threshold where Amazon Lex will insert the ``AMAZON.FallbackIntent`` , ``AMAZON.KendraSearchIntent`` , or both when returning alternative intents. You must configure an ``AMAZON.FallbackIntent`` . ``AMAZON.KendraSearchIntent`` is only inserted if it is configured for the bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-nluconfidencethreshold
            '''
            result = self._values.get("nlu_confidence_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def slot_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotTypeProperty"]]]]:
            '''One or more slot types defined for the locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-slottypes
            '''
            result = self._values.get("slot_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotTypeProperty"]]]], result)

        @builtins.property
        def voice_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.VoiceSettingsProperty"]]:
            '''Defines settings for using an Amazon Polly voice to communicate with a user.

            Valid values include:

            - ``standard``
            - ``neural``
            - ``long-form``
            - ``generative``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-voicesettings
            '''
            result = self._values.get("voice_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.VoiceSettingsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotLocaleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.BuildtimeSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "descriptive_bot_builder_specification": "descriptiveBotBuilderSpecification",
            "sample_utterance_generation_specification": "sampleUtteranceGenerationSpecification",
        },
    )
    class BuildtimeSettingsProperty:
        def __init__(
            self,
            *,
            descriptive_bot_builder_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DescriptiveBotBuilderSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sample_utterance_generation_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SampleUtteranceGenerationSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains specifications about the Amazon Lex build time generative AI capabilities from Amazon Bedrock that you can turn on for your bot.

            :param descriptive_bot_builder_specification: 
            :param sample_utterance_generation_specification: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-buildtimesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                buildtime_settings_property = lex_mixins.CfnBotPropsMixin.BuildtimeSettingsProperty(
                    descriptive_bot_builder_specification=lex_mixins.CfnBotPropsMixin.DescriptiveBotBuilderSpecificationProperty(
                        bedrock_model_specification=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                            bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                                bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                                bedrock_guardrail_version="bedrockGuardrailVersion"
                            ),
                            bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                            bedrock_trace_status="bedrockTraceStatus",
                            model_arn="modelArn"
                        ),
                        enabled=False
                    ),
                    sample_utterance_generation_specification=lex_mixins.CfnBotPropsMixin.SampleUtteranceGenerationSpecificationProperty(
                        bedrock_model_specification=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                            bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                                bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                                bedrock_guardrail_version="bedrockGuardrailVersion"
                            ),
                            bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                            bedrock_trace_status="bedrockTraceStatus",
                            model_arn="modelArn"
                        ),
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9bdbb9be3e73758fee04ccc235043e7c59e6bb257c9c3d14067f8f414000b877)
                check_type(argname="argument descriptive_bot_builder_specification", value=descriptive_bot_builder_specification, expected_type=type_hints["descriptive_bot_builder_specification"])
                check_type(argname="argument sample_utterance_generation_specification", value=sample_utterance_generation_specification, expected_type=type_hints["sample_utterance_generation_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if descriptive_bot_builder_specification is not None:
                self._values["descriptive_bot_builder_specification"] = descriptive_bot_builder_specification
            if sample_utterance_generation_specification is not None:
                self._values["sample_utterance_generation_specification"] = sample_utterance_generation_specification

        @builtins.property
        def descriptive_bot_builder_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DescriptiveBotBuilderSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-buildtimesettings.html#cfn-lex-bot-buildtimesettings-descriptivebotbuilderspecification
            '''
            result = self._values.get("descriptive_bot_builder_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DescriptiveBotBuilderSpecificationProperty"]], result)

        @builtins.property
        def sample_utterance_generation_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleUtteranceGenerationSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-buildtimesettings.html#cfn-lex-bot-buildtimesettings-sampleutterancegenerationspecification
            '''
            result = self._values.get("sample_utterance_generation_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleUtteranceGenerationSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BuildtimeSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ButtonProperty",
        jsii_struct_bases=[],
        name_mapping={"text": "text", "value": "value"},
    )
    class ButtonProperty:
        def __init__(
            self,
            *,
            text: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a button to use on a response card used to gather slot values from a user.

            :param text: The text that appears on the button. Use this to tell the user what value is returned when they choose this button.
            :param value: The value returned to Amazon Lex when the user chooses this button. This must be one of the slot values configured for the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-button.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                button_property = lex_mixins.CfnBotPropsMixin.ButtonProperty(
                    text="text",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99fcbaa96157542656ba47f9b8dacba8ae8997d0c3f2bab638984a46b2b79255)
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if text is not None:
                self._values["text"] = text
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The text that appears on the button.

            Use this to tell the user what value is returned when they choose this button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-button.html#cfn-lex-bot-button-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value returned to Amazon Lex when the user chooses this button.

            This must be one of the slot values configured for the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-button.html#cfn-lex-bot-button-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ButtonProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.CloudWatchLogGroupLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
            "log_prefix": "logPrefix",
        },
    )
    class CloudWatchLogGroupLogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
            log_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon CloudWatch Logs log group where the text and metadata logs are delivered.

            The log group must exist before you enable logging.

            :param cloud_watch_log_group_arn: The Amazon Resource Name (ARN) of the log group where text and metadata logs are delivered.
            :param log_prefix: The prefix of the log stream name within the log group that you specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-cloudwatchloggrouplogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                cloud_watch_log_group_log_destination_property = lex_mixins.CfnBotPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    log_prefix="logPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94e60eb78e5ada2758cfe120ad0d042ef68da9062be8837c64c9af082f2b64ec)
                check_type(argname="argument cloud_watch_log_group_arn", value=cloud_watch_log_group_arn, expected_type=type_hints["cloud_watch_log_group_arn"])
                check_type(argname="argument log_prefix", value=log_prefix, expected_type=type_hints["log_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_log_group_arn is not None:
                self._values["cloud_watch_log_group_arn"] = cloud_watch_log_group_arn
            if log_prefix is not None:
                self._values["log_prefix"] = log_prefix

        @builtins.property
        def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the log group where text and metadata logs are delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-cloudwatchloggrouplogdestination.html#cfn-lex-bot-cloudwatchloggrouplogdestination-cloudwatchloggrouparn
            '''
            result = self._values.get("cloud_watch_log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix of the log stream name within the log group that you specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-cloudwatchloggrouplogdestination.html#cfn-lex-bot-cloudwatchloggrouplogdestination-logprefix
            '''
            result = self._values.get("log_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogGroupLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.CodeHookSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_code_hook": "lambdaCodeHook"},
    )
    class CodeHookSpecificationProperty:
        def __init__(
            self,
            *,
            lambda_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.LambdaCodeHookProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about code hooks that Amazon Lex calls during a conversation.

            :param lambda_code_hook: Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-codehookspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                code_hook_specification_property = lex_mixins.CfnBotPropsMixin.CodeHookSpecificationProperty(
                    lambda_code_hook=lex_mixins.CfnBotPropsMixin.LambdaCodeHookProperty(
                        code_hook_interface_version="codeHookInterfaceVersion",
                        lambda_arn="lambdaArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3bff33d8e74167e1325ebb90411ed92af1a71324991bac9bb176acef7dfd0e0)
                check_type(argname="argument lambda_code_hook", value=lambda_code_hook, expected_type=type_hints["lambda_code_hook"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_code_hook is not None:
                self._values["lambda_code_hook"] = lambda_code_hook

        @builtins.property
        def lambda_code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.LambdaCodeHookProperty"]]:
            '''Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-codehookspecification.html#cfn-lex-bot-codehookspecification-lambdacodehook
            '''
            result = self._values.get("lambda_code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.LambdaCodeHookProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeHookSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.CompositeSlotTypeSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"sub_slots": "subSlots"},
    )
    class CompositeSlotTypeSettingProperty:
        def __init__(
            self,
            *,
            sub_slots: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SubSlotTypeCompositionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A composite slot is a combination of two or more slots that capture multiple pieces of information in a single user input.

            :param sub_slots: Subslots in the composite slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-compositeslottypesetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                composite_slot_type_setting_property = lex_mixins.CfnBotPropsMixin.CompositeSlotTypeSettingProperty(
                    sub_slots=[lex_mixins.CfnBotPropsMixin.SubSlotTypeCompositionProperty(
                        name="name",
                        slot_type_id="slotTypeId"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c1fd1659b247fab888e597c395fb5a2b740c469ff11757eab22daa530b4efc4c)
                check_type(argname="argument sub_slots", value=sub_slots, expected_type=type_hints["sub_slots"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sub_slots is not None:
                self._values["sub_slots"] = sub_slots

        @builtins.property
        def sub_slots(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SubSlotTypeCompositionProperty"]]]]:
            '''Subslots in the composite slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-compositeslottypesetting.html#cfn-lex-bot-compositeslottypesetting-subslots
            '''
            result = self._values.get("sub_slots")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SubSlotTypeCompositionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CompositeSlotTypeSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"expression_string": "expressionString"},
    )
    class ConditionProperty:
        def __init__(
            self,
            *,
            expression_string: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides an expression that evaluates to true or false.

            :param expression_string: The expression string that is evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-condition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                condition_property = lex_mixins.CfnBotPropsMixin.ConditionProperty(
                    expression_string="expressionString"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ab749316927b3b54329167583d0ed1d3d12db16baf230f76c73639c5d448011)
                check_type(argname="argument expression_string", value=expression_string, expected_type=type_hints["expression_string"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression_string is not None:
                self._values["expression_string"] = expression_string

        @builtins.property
        def expression_string(self) -> typing.Optional[builtins.str]:
            '''The expression string that is evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-condition.html#cfn-lex-bot-condition-expressionstring
            '''
            result = self._values.get("expression_string")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ConditionalBranchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition": "condition",
            "name": "name",
            "next_step": "nextStep",
            "response": "response",
        },
    )
    class ConditionalBranchProperty:
        def __init__(
            self,
            *,
            condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A set of actions that Amazon Lex should run if the condition is matched.

            :param condition: Contains the expression to evaluate. If the condition is true, the branch's actions are taken.
            :param name: The name of the branch.
            :param next_step: The next step in the conversation.
            :param response: Specifies a list of message groups that Amazon Lex uses to respond the user input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conditionalbranch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                # slot_value_override_property_: lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty
                
                conditional_branch_property = lex_mixins.CfnBotPropsMixin.ConditionalBranchProperty(
                    condition=lex_mixins.CfnBotPropsMixin.ConditionProperty(
                        expression_string="expressionString"
                    ),
                    name="name",
                    next_step=lex_mixins.CfnBotPropsMixin.DialogStateProperty(
                        dialog_action=lex_mixins.CfnBotPropsMixin.DialogActionProperty(
                            slot_to_elicit="slotToElicit",
                            suppress_next_message=False,
                            type="type"
                        ),
                        intent=lex_mixins.CfnBotPropsMixin.IntentOverrideProperty(
                            name="name",
                            slots=[lex_mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty(
                                slot_name="slotName",
                                slot_value_override=lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                                    shape="shape",
                                    value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                                        interpreted_value="interpretedValue"
                                    ),
                                    values=[slot_value_override_property_]
                                )
                            )]
                        ),
                        session_attributes=[lex_mixins.CfnBotPropsMixin.SessionAttributeProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                        allow_interrupt=False,
                        message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b56c9ca08d611d28b7cfde0f282adcf40a6cfb2774e949ff7f23378842f3abe7)
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument next_step", value=next_step, expected_type=type_hints["next_step"])
                check_type(argname="argument response", value=response, expected_type=type_hints["response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition is not None:
                self._values["condition"] = condition
            if name is not None:
                self._values["name"] = name
            if next_step is not None:
                self._values["next_step"] = next_step
            if response is not None:
                self._values["response"] = response

        @builtins.property
        def condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionProperty"]]:
            '''Contains the expression to evaluate.

            If the condition is true, the branch's actions are taken.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conditionalbranch.html#cfn-lex-bot-conditionalbranch-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conditionalbranch.html#cfn-lex-bot-conditionalbranch-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''The next step in the conversation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conditionalbranch.html#cfn-lex-bot-conditionalbranch-nextstep
            '''
            result = self._values.get("next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond the user input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conditionalbranch.html#cfn-lex-bot-conditionalbranch-response
            '''
            result = self._values.get("response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionalBranchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ConditionalSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "conditional_branches": "conditionalBranches",
            "default_branch": "defaultBranch",
            "is_active": "isActive",
        },
    )
    class ConditionalSpecificationProperty:
        def __init__(
            self,
            *,
            conditional_branches: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalBranchProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            default_branch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DefaultConditionalBranchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Provides a list of conditional branches.

            Branches are evaluated in the order that they are entered in the list. The first branch with a condition that evaluates to true is executed. The last branch in the list is the default branch. The default branch should not have any condition expression. The default branch is executed if no other branch has a matching condition.

            :param conditional_branches: A list of conditional branches. A conditional branch is made up of a condition, a response and a next step. The response and next step are executed when the condition is true.
            :param default_branch: The conditional branch that should be followed when the conditions for other branches are not satisfied. A conditional branch is made up of a condition, a response and a next step.
            :param is_active: Determines whether a conditional branch is active. When ``IsActive`` is false, the conditions are not evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conditionalspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                # slot_value_override_property_: lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty
                
                conditional_specification_property = lex_mixins.CfnBotPropsMixin.ConditionalSpecificationProperty(
                    conditional_branches=[lex_mixins.CfnBotPropsMixin.ConditionalBranchProperty(
                        condition=lex_mixins.CfnBotPropsMixin.ConditionProperty(
                            expression_string="expressionString"
                        ),
                        name="name",
                        next_step=lex_mixins.CfnBotPropsMixin.DialogStateProperty(
                            dialog_action=lex_mixins.CfnBotPropsMixin.DialogActionProperty(
                                slot_to_elicit="slotToElicit",
                                suppress_next_message=False,
                                type="type"
                            ),
                            intent=lex_mixins.CfnBotPropsMixin.IntentOverrideProperty(
                                name="name",
                                slots=[lex_mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty(
                                    slot_name="slotName",
                                    slot_value_override=lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                                        shape="shape",
                                        value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                                            interpreted_value="interpretedValue"
                                        ),
                                        values=[slot_value_override_property_]
                                    )
                                )]
                            ),
                            session_attributes=[lex_mixins.CfnBotPropsMixin.SessionAttributeProperty(
                                key="key",
                                value="value"
                            )]
                        ),
                        response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                            allow_interrupt=False,
                            message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                                variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )]
                        )
                    )],
                    default_branch=lex_mixins.CfnBotPropsMixin.DefaultConditionalBranchProperty(
                        next_step=lex_mixins.CfnBotPropsMixin.DialogStateProperty(
                            dialog_action=lex_mixins.CfnBotPropsMixin.DialogActionProperty(
                                slot_to_elicit="slotToElicit",
                                suppress_next_message=False,
                                type="type"
                            ),
                            intent=lex_mixins.CfnBotPropsMixin.IntentOverrideProperty(
                                name="name",
                                slots=[lex_mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty(
                                    slot_name="slotName",
                                    slot_value_override=lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                                        shape="shape",
                                        value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                                            interpreted_value="interpretedValue"
                                        ),
                                        values=[slot_value_override_property_]
                                    )
                                )]
                            ),
                            session_attributes=[lex_mixins.CfnBotPropsMixin.SessionAttributeProperty(
                                key="key",
                                value="value"
                            )]
                        ),
                        response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                            allow_interrupt=False,
                            message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                                variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )]
                        )
                    ),
                    is_active=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6cb9ecab271de3afc2a8bde8f62c8387c28d60e0687ebfe275f2210a00f6f450)
                check_type(argname="argument conditional_branches", value=conditional_branches, expected_type=type_hints["conditional_branches"])
                check_type(argname="argument default_branch", value=default_branch, expected_type=type_hints["default_branch"])
                check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if conditional_branches is not None:
                self._values["conditional_branches"] = conditional_branches
            if default_branch is not None:
                self._values["default_branch"] = default_branch
            if is_active is not None:
                self._values["is_active"] = is_active

        @builtins.property
        def conditional_branches(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalBranchProperty"]]]]:
            '''A list of conditional branches.

            A conditional branch is made up of a condition, a response and a next step. The response and next step are executed when the condition is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conditionalspecification.html#cfn-lex-bot-conditionalspecification-conditionalbranches
            '''
            result = self._values.get("conditional_branches")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalBranchProperty"]]]], result)

        @builtins.property
        def default_branch(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DefaultConditionalBranchProperty"]]:
            '''The conditional branch that should be followed when the conditions for other branches are not satisfied.

            A conditional branch is made up of a condition, a response and a next step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conditionalspecification.html#cfn-lex-bot-conditionalspecification-defaultbranch
            '''
            result = self._values.get("default_branch")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DefaultConditionalBranchProperty"]], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether a conditional branch is active.

            When ``IsActive`` is false, the conditions are not evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conditionalspecification.html#cfn-lex-bot-conditionalspecification-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionalSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ConversationLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audio_log_settings": "audioLogSettings",
            "text_log_settings": "textLogSettings",
        },
    )
    class ConversationLogSettingsProperty:
        def __init__(
            self,
            *,
            audio_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.AudioLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            text_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.TextLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configures conversation logging that saves audio, text, and metadata for the conversations with your users.

            :param audio_log_settings: The Amazon S3 settings for logging audio to an S3 bucket.
            :param text_log_settings: The Amazon CloudWatch Logs settings for logging text and metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conversationlogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                conversation_log_settings_property = lex_mixins.CfnBotPropsMixin.ConversationLogSettingsProperty(
                    audio_log_settings=[lex_mixins.CfnBotPropsMixin.AudioLogSettingProperty(
                        destination=lex_mixins.CfnBotPropsMixin.AudioLogDestinationProperty(
                            s3_bucket=lex_mixins.CfnBotPropsMixin.S3BucketLogDestinationProperty(
                                kms_key_arn="kmsKeyArn",
                                log_prefix="logPrefix",
                                s3_bucket_arn="s3BucketArn"
                            )
                        ),
                        enabled=False
                    )],
                    text_log_settings=[lex_mixins.CfnBotPropsMixin.TextLogSettingProperty(
                        destination=lex_mixins.CfnBotPropsMixin.TextLogDestinationProperty(
                            cloud_watch=lex_mixins.CfnBotPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                                log_prefix="logPrefix"
                            )
                        ),
                        enabled=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__113c49f318bff2e0276e726a04305e636183bc48326a684cdf33eee8a8837497)
                check_type(argname="argument audio_log_settings", value=audio_log_settings, expected_type=type_hints["audio_log_settings"])
                check_type(argname="argument text_log_settings", value=text_log_settings, expected_type=type_hints["text_log_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audio_log_settings is not None:
                self._values["audio_log_settings"] = audio_log_settings
            if text_log_settings is not None:
                self._values["text_log_settings"] = text_log_settings

        @builtins.property
        def audio_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AudioLogSettingProperty"]]]]:
            '''The Amazon S3 settings for logging audio to an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conversationlogsettings.html#cfn-lex-bot-conversationlogsettings-audiologsettings
            '''
            result = self._values.get("audio_log_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AudioLogSettingProperty"]]]], result)

        @builtins.property
        def text_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.TextLogSettingProperty"]]]]:
            '''The Amazon CloudWatch Logs settings for logging text and metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conversationlogsettings.html#cfn-lex-bot-conversationlogsettings-textlogsettings
            '''
            result = self._values.get("text_log_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.TextLogSettingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConversationLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.CustomPayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class CustomPayloadProperty:
        def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
            '''A custom response string that Amazon Lex sends to your application.

            You define the content and structure the string.

            :param value: The string that is sent to your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-custompayload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                custom_payload_property = lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8366ef501a8b6378b6bc25efa5baf0f9e8bc9ca1e05f3fc82f6f2cbc861bd28b)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The string that is sent to your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-custompayload.html#cfn-lex-bot-custompayload-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.CustomVocabularyItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "display_as": "displayAs",
            "phrase": "phrase",
            "weight": "weight",
        },
    )
    class CustomVocabularyItemProperty:
        def __init__(
            self,
            *,
            display_as: typing.Optional[builtins.str] = None,
            phrase: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies an entry in a custom vocabulary.

            :param display_as: The DisplayAs value for the custom vocabulary item from the custom vocabulary list.
            :param phrase: Specifies 1 - 4 words that should be recognized.
            :param weight: Specifies the degree to which the phrase recognition is boosted. The default value is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabularyitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                custom_vocabulary_item_property = lex_mixins.CfnBotPropsMixin.CustomVocabularyItemProperty(
                    display_as="displayAs",
                    phrase="phrase",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de7784c746e0f3279a959afc9372a7f8a825c67ba086e6b0e673f843d701ae81)
                check_type(argname="argument display_as", value=display_as, expected_type=type_hints["display_as"])
                check_type(argname="argument phrase", value=phrase, expected_type=type_hints["phrase"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if display_as is not None:
                self._values["display_as"] = display_as
            if phrase is not None:
                self._values["phrase"] = phrase
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def display_as(self) -> typing.Optional[builtins.str]:
            '''The DisplayAs value for the custom vocabulary item from the custom vocabulary list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabularyitem.html#cfn-lex-bot-customvocabularyitem-displayas
            '''
            result = self._values.get("display_as")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def phrase(self) -> typing.Optional[builtins.str]:
            '''Specifies 1 - 4 words that should be recognized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabularyitem.html#cfn-lex-bot-customvocabularyitem-phrase
            '''
            result = self._values.get("phrase")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''Specifies the degree to which the phrase recognition is boosted.

            The default value is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabularyitem.html#cfn-lex-bot-customvocabularyitem-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomVocabularyItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.CustomVocabularyProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_vocabulary_items": "customVocabularyItems"},
    )
    class CustomVocabularyProperty:
        def __init__(
            self,
            *,
            custom_vocabulary_items: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.CustomVocabularyItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies a custom vocabulary.

            A custom vocabulary is a list of words that you expect to be used during a conversation with your bot.

            :param custom_vocabulary_items: Specifies a list of words that you expect to be used during a conversation with your bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabulary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                custom_vocabulary_property = lex_mixins.CfnBotPropsMixin.CustomVocabularyProperty(
                    custom_vocabulary_items=[lex_mixins.CfnBotPropsMixin.CustomVocabularyItemProperty(
                        display_as="displayAs",
                        phrase="phrase",
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__69a0a9b2e413a868854da1118ffd6c780002804c5eae16b26747ce4d79104459)
                check_type(argname="argument custom_vocabulary_items", value=custom_vocabulary_items, expected_type=type_hints["custom_vocabulary_items"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_vocabulary_items is not None:
                self._values["custom_vocabulary_items"] = custom_vocabulary_items

        @builtins.property
        def custom_vocabulary_items(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CustomVocabularyItemProperty"]]]]:
            '''Specifies a list of words that you expect to be used during a conversation with your bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabulary.html#cfn-lex-bot-customvocabulary-customvocabularyitems
            '''
            result = self._values.get("custom_vocabulary_items")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CustomVocabularyItemProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomVocabularyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.DTMFSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deletion_character": "deletionCharacter",
            "end_character": "endCharacter",
            "end_timeout_ms": "endTimeoutMs",
            "max_length": "maxLength",
        },
    )
    class DTMFSpecificationProperty:
        def __init__(
            self,
            *,
            deletion_character: typing.Optional[builtins.str] = None,
            end_character: typing.Optional[builtins.str] = None,
            end_timeout_ms: typing.Optional[jsii.Number] = None,
            max_length: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the DTMF input specifications.

            :param deletion_character: The DTMF character that clears the accumulated DTMF digits and immediately ends the input.
            :param end_character: The DTMF character that immediately ends input. If the user does not press this character, the input ends after the end timeout.
            :param end_timeout_ms: How long the bot should wait after the last DTMF character input before assuming that the input has concluded.
            :param max_length: The maximum number of DTMF digits allowed in an utterance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dtmfspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                d_tMFSpecification_property = lex_mixins.CfnBotPropsMixin.DTMFSpecificationProperty(
                    deletion_character="deletionCharacter",
                    end_character="endCharacter",
                    end_timeout_ms=123,
                    max_length=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c93b03e650f2344eb890ed8742ca1b0880d74b4cbff0d8e0445fa9c184c03c0)
                check_type(argname="argument deletion_character", value=deletion_character, expected_type=type_hints["deletion_character"])
                check_type(argname="argument end_character", value=end_character, expected_type=type_hints["end_character"])
                check_type(argname="argument end_timeout_ms", value=end_timeout_ms, expected_type=type_hints["end_timeout_ms"])
                check_type(argname="argument max_length", value=max_length, expected_type=type_hints["max_length"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deletion_character is not None:
                self._values["deletion_character"] = deletion_character
            if end_character is not None:
                self._values["end_character"] = end_character
            if end_timeout_ms is not None:
                self._values["end_timeout_ms"] = end_timeout_ms
            if max_length is not None:
                self._values["max_length"] = max_length

        @builtins.property
        def deletion_character(self) -> typing.Optional[builtins.str]:
            '''The DTMF character that clears the accumulated DTMF digits and immediately ends the input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dtmfspecification.html#cfn-lex-bot-dtmfspecification-deletioncharacter
            '''
            result = self._values.get("deletion_character")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def end_character(self) -> typing.Optional[builtins.str]:
            '''The DTMF character that immediately ends input.

            If the user does not press this character, the input ends after the end timeout.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dtmfspecification.html#cfn-lex-bot-dtmfspecification-endcharacter
            '''
            result = self._values.get("end_character")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def end_timeout_ms(self) -> typing.Optional[jsii.Number]:
            '''How long the bot should wait after the last DTMF character input before assuming that the input has concluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dtmfspecification.html#cfn-lex-bot-dtmfspecification-endtimeoutms
            '''
            result = self._values.get("end_timeout_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_length(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of DTMF digits allowed in an utterance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dtmfspecification.html#cfn-lex-bot-dtmfspecification-maxlength
            '''
            result = self._values.get("max_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DTMFSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.DataPrivacyProperty",
        jsii_struct_bases=[],
        name_mapping={"child_directed": "childDirected"},
    )
    class DataPrivacyProperty:
        def __init__(
            self,
            *,
            child_directed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''By default, data stored by Amazon Lex is encrypted.

            The ``DataPrivacy`` structure provides settings that determine how Amazon Lex handles special cases of securing the data for your bot.

            :param child_directed: For each Amazon Lex bot created with the Amazon Lex Model Building Service, you must specify whether your use of Amazon Lex is related to a website, program, or other application that is directed or targeted, in whole or in part, to children under age 13 and subject to the Children's Online Privacy Protection Act (COPPA) by specifying ``true`` or ``false`` in the ``childDirected`` field. By specifying ``true`` in the ``childDirected`` field, you confirm that your use of Amazon Lex *is* related to a website, program, or other application that is directed or targeted, in whole or in part, to children under age 13 and subject to COPPA. By specifying ``false`` in the ``childDirected`` field, you confirm that your use of Amazon Lex *is not* related to a website, program, or other application that is directed or targeted, in whole or in part, to children under age 13 and subject to COPPA. You may not specify a default value for the ``childDirected`` field that does not accurately reflect whether your use of Amazon Lex is related to a website, program, or other application that is directed or targeted, in whole or in part, to children under age 13 and subject to COPPA. If your use of Amazon Lex relates to a website, program, or other application that is directed in whole or in part, to children under age 13, you must obtain any required verifiable parental consent under COPPA. For information regarding the use of Amazon Lex in connection with websites, programs, or other applications that are directed or targeted, in whole or in part, to children under age 13, see the `Amazon Lex FAQ <https://docs.aws.amazon.com/lex/faqs#data-security>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dataprivacy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                data_privacy_property = lex_mixins.CfnBotPropsMixin.DataPrivacyProperty(
                    child_directed=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6fb3d810a57ac9798a6a9bcb0858d6e0908b9ccd4312253ebb92a97a5ea1302f)
                check_type(argname="argument child_directed", value=child_directed, expected_type=type_hints["child_directed"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if child_directed is not None:
                self._values["child_directed"] = child_directed

        @builtins.property
        def child_directed(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''For each Amazon Lex bot created with the Amazon Lex Model Building Service, you must specify whether your use of Amazon Lex is related to a website, program, or other application that is directed or targeted, in whole or in part, to children under age 13 and subject to the Children's Online Privacy Protection Act (COPPA) by specifying ``true`` or ``false`` in the ``childDirected`` field.

            By specifying ``true`` in the ``childDirected`` field, you confirm that your use of Amazon Lex *is* related to a website, program, or other application that is directed or targeted, in whole or in part, to children under age 13 and subject to COPPA. By specifying ``false`` in the ``childDirected`` field, you confirm that your use of Amazon Lex *is not* related to a website, program, or other application that is directed or targeted, in whole or in part, to children under age 13 and subject to COPPA. You may not specify a default value for the ``childDirected`` field that does not accurately reflect whether your use of Amazon Lex is related to a website, program, or other application that is directed or targeted, in whole or in part, to children under age 13 and subject to COPPA. If your use of Amazon Lex relates to a website, program, or other application that is directed in whole or in part, to children under age 13, you must obtain any required verifiable parental consent under COPPA. For information regarding the use of Amazon Lex in connection with websites, programs, or other applications that are directed or targeted, in whole or in part, to children under age 13, see the `Amazon Lex FAQ <https://docs.aws.amazon.com/lex/faqs#data-security>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dataprivacy.html#cfn-lex-bot-dataprivacy-childdirected
            '''
            result = self._values.get("child_directed")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataPrivacyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.DataSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_knowledge_store_configuration": "bedrockKnowledgeStoreConfiguration",
            "kendra_configuration": "kendraConfiguration",
            "opensearch_configuration": "opensearchConfiguration",
        },
    )
    class DataSourceConfigurationProperty:
        def __init__(
            self,
            *,
            bedrock_knowledge_store_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BedrockKnowledgeStoreConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kendra_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.QnAKendraConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            opensearch_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.OpensearchConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains details about the configuration of the knowledge store used for the ``AMAZON.QnAIntent`` . You must have already created the knowledge store and indexed the documents within it.

            :param bedrock_knowledge_store_configuration: Contains details about the configuration of the Amazon Bedrock knowledge base used for the ``AMAZON.QnAIntent`` . To set up a knowledge base, follow the steps at `Building a knowledge base <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html>`_ .
            :param kendra_configuration: Contains details about the configuration of the Amazon Kendra index used for the ``AMAZON.QnAIntent`` . To create a Amazon Kendra index, follow the steps at `Creating an index <https://docs.aws.amazon.com/kendra/latest/dg/create-index.html>`_ .
            :param opensearch_configuration: Contains details about the configuration of the Amazon OpenSearch Service database used for the ``AMAZON.QnAIntent`` . To create a domain, follow the steps at `Creating and managing Amazon OpenSearch Service domains <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-datasourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                data_source_configuration_property = lex_mixins.CfnBotPropsMixin.DataSourceConfigurationProperty(
                    bedrock_knowledge_store_configuration=lex_mixins.CfnBotPropsMixin.BedrockKnowledgeStoreConfigurationProperty(
                        bedrock_knowledge_base_arn="bedrockKnowledgeBaseArn",
                        bkb_exact_response_fields=lex_mixins.CfnBotPropsMixin.BKBExactResponseFieldsProperty(
                            answer_field="answerField"
                        ),
                        exact_response=False
                    ),
                    kendra_configuration=lex_mixins.CfnBotPropsMixin.QnAKendraConfigurationProperty(
                        exact_response=False,
                        kendra_index="kendraIndex",
                        query_filter_string="queryFilterString",
                        query_filter_string_enabled=False
                    ),
                    opensearch_configuration=lex_mixins.CfnBotPropsMixin.OpensearchConfigurationProperty(
                        domain_endpoint="domainEndpoint",
                        exact_response=False,
                        exact_response_fields=lex_mixins.CfnBotPropsMixin.ExactResponseFieldsProperty(
                            answer_field="answerField",
                            question_field="questionField"
                        ),
                        include_fields=["includeFields"],
                        index_name="indexName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8ad5b3a5060ea26a12ea230edddcfd6bafb3bdc8dfa530f9b1de26f2694d606)
                check_type(argname="argument bedrock_knowledge_store_configuration", value=bedrock_knowledge_store_configuration, expected_type=type_hints["bedrock_knowledge_store_configuration"])
                check_type(argname="argument kendra_configuration", value=kendra_configuration, expected_type=type_hints["kendra_configuration"])
                check_type(argname="argument opensearch_configuration", value=opensearch_configuration, expected_type=type_hints["opensearch_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_knowledge_store_configuration is not None:
                self._values["bedrock_knowledge_store_configuration"] = bedrock_knowledge_store_configuration
            if kendra_configuration is not None:
                self._values["kendra_configuration"] = kendra_configuration
            if opensearch_configuration is not None:
                self._values["opensearch_configuration"] = opensearch_configuration

        @builtins.property
        def bedrock_knowledge_store_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockKnowledgeStoreConfigurationProperty"]]:
            '''Contains details about the configuration of the Amazon Bedrock knowledge base used for the ``AMAZON.QnAIntent`` . To set up a knowledge base, follow the steps at `Building a knowledge base <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-datasourceconfiguration.html#cfn-lex-bot-datasourceconfiguration-bedrockknowledgestoreconfiguration
            '''
            result = self._values.get("bedrock_knowledge_store_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockKnowledgeStoreConfigurationProperty"]], result)

        @builtins.property
        def kendra_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.QnAKendraConfigurationProperty"]]:
            '''Contains details about the configuration of the Amazon Kendra index used for the ``AMAZON.QnAIntent`` . To create a Amazon Kendra index, follow the steps at `Creating an index <https://docs.aws.amazon.com/kendra/latest/dg/create-index.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-datasourceconfiguration.html#cfn-lex-bot-datasourceconfiguration-kendraconfiguration
            '''
            result = self._values.get("kendra_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.QnAKendraConfigurationProperty"]], result)

        @builtins.property
        def opensearch_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.OpensearchConfigurationProperty"]]:
            '''Contains details about the configuration of the Amazon OpenSearch Service database used for the ``AMAZON.QnAIntent`` . To create a domain, follow the steps at `Creating and managing Amazon OpenSearch Service domains <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-datasourceconfiguration.html#cfn-lex-bot-datasourceconfiguration-opensearchconfiguration
            '''
            result = self._values.get("opensearch_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.OpensearchConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.DefaultConditionalBranchProperty",
        jsii_struct_bases=[],
        name_mapping={"next_step": "nextStep", "response": "response"},
    )
    class DefaultConditionalBranchProperty:
        def __init__(
            self,
            *,
            next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A set of actions that Amazon Lex should run if none of the other conditions are met.

            :param next_step: The next step in the conversation.
            :param response: Specifies a list of message groups that Amazon Lex uses to respond the user input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-defaultconditionalbranch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                # slot_value_override_property_: lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty
                
                default_conditional_branch_property = lex_mixins.CfnBotPropsMixin.DefaultConditionalBranchProperty(
                    next_step=lex_mixins.CfnBotPropsMixin.DialogStateProperty(
                        dialog_action=lex_mixins.CfnBotPropsMixin.DialogActionProperty(
                            slot_to_elicit="slotToElicit",
                            suppress_next_message=False,
                            type="type"
                        ),
                        intent=lex_mixins.CfnBotPropsMixin.IntentOverrideProperty(
                            name="name",
                            slots=[lex_mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty(
                                slot_name="slotName",
                                slot_value_override=lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                                    shape="shape",
                                    value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                                        interpreted_value="interpretedValue"
                                    ),
                                    values=[slot_value_override_property_]
                                )
                            )]
                        ),
                        session_attributes=[lex_mixins.CfnBotPropsMixin.SessionAttributeProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                        allow_interrupt=False,
                        message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__059cf477d6f31f817dfc1035e3bd573c437589794a5a19a8a60de9954857fc0c)
                check_type(argname="argument next_step", value=next_step, expected_type=type_hints["next_step"])
                check_type(argname="argument response", value=response, expected_type=type_hints["response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if next_step is not None:
                self._values["next_step"] = next_step
            if response is not None:
                self._values["response"] = response

        @builtins.property
        def next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''The next step in the conversation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-defaultconditionalbranch.html#cfn-lex-bot-defaultconditionalbranch-nextstep
            '''
            result = self._values.get("next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond the user input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-defaultconditionalbranch.html#cfn-lex-bot-defaultconditionalbranch-response
            '''
            result = self._values.get("response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultConditionalBranchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.DescriptiveBotBuilderSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_model_specification": "bedrockModelSpecification",
            "enabled": "enabled",
        },
    )
    class DescriptiveBotBuilderSpecificationProperty:
        def __init__(
            self,
            *,
            bedrock_model_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BedrockModelSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains specifications for the descriptive bot building feature.

            :param bedrock_model_specification: An object containing information about the Amazon Bedrock model used to interpret the prompt used in descriptive bot building.
            :param enabled: Specifies whether the descriptive bot building feature is activated or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-descriptivebotbuilderspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                descriptive_bot_builder_specification_property = lex_mixins.CfnBotPropsMixin.DescriptiveBotBuilderSpecificationProperty(
                    bedrock_model_specification=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                        bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                            bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                            bedrock_guardrail_version="bedrockGuardrailVersion"
                        ),
                        bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                        bedrock_trace_status="bedrockTraceStatus",
                        model_arn="modelArn"
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1db4f05d8f5e87c14d2812d283dbbd2f4ec0ce2b5e578de5f79acc1bd9b1beef)
                check_type(argname="argument bedrock_model_specification", value=bedrock_model_specification, expected_type=type_hints["bedrock_model_specification"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_model_specification is not None:
                self._values["bedrock_model_specification"] = bedrock_model_specification
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def bedrock_model_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockModelSpecificationProperty"]]:
            '''An object containing information about the Amazon Bedrock model used to interpret the prompt used in descriptive bot building.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-descriptivebotbuilderspecification.html#cfn-lex-bot-descriptivebotbuilderspecification-bedrockmodelspecification
            '''
            result = self._values.get("bedrock_model_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockModelSpecificationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the descriptive bot building feature is activated or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-descriptivebotbuilderspecification.html#cfn-lex-bot-descriptivebotbuilderspecification-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DescriptiveBotBuilderSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.DialogActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "slot_to_elicit": "slotToElicit",
            "suppress_next_message": "suppressNextMessage",
            "type": "type",
        },
    )
    class DialogActionProperty:
        def __init__(
            self,
            *,
            slot_to_elicit: typing.Optional[builtins.str] = None,
            suppress_next_message: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the action that the bot executes at runtime when the conversation reaches this step.

            :param slot_to_elicit: If the dialog action is ``ElicitSlot`` , defines the slot to elicit from the user.
            :param suppress_next_message: When true the next message for the intent is not used.
            :param type: The action that the bot should execute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                dialog_action_property = lex_mixins.CfnBotPropsMixin.DialogActionProperty(
                    slot_to_elicit="slotToElicit",
                    suppress_next_message=False,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b875ee39716965e17b62c7b6d17fdfc8a09950f07c861e597405862f68b96630)
                check_type(argname="argument slot_to_elicit", value=slot_to_elicit, expected_type=type_hints["slot_to_elicit"])
                check_type(argname="argument suppress_next_message", value=suppress_next_message, expected_type=type_hints["suppress_next_message"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if slot_to_elicit is not None:
                self._values["slot_to_elicit"] = slot_to_elicit
            if suppress_next_message is not None:
                self._values["suppress_next_message"] = suppress_next_message
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def slot_to_elicit(self) -> typing.Optional[builtins.str]:
            '''If the dialog action is ``ElicitSlot`` , defines the slot to elicit from the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogaction.html#cfn-lex-bot-dialogaction-slottoelicit
            '''
            result = self._values.get("slot_to_elicit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def suppress_next_message(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true the next message for the intent is not used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogaction.html#cfn-lex-bot-dialogaction-suppressnextmessage
            '''
            result = self._values.get("suppress_next_message")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The action that the bot should execute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogaction.html#cfn-lex-bot-dialogaction-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DialogActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_code_hook_invocation": "enableCodeHookInvocation",
            "invocation_label": "invocationLabel",
            "is_active": "isActive",
            "post_code_hook_specification": "postCodeHookSpecification",
        },
    )
    class DialogCodeHookInvocationSettingProperty:
        def __init__(
            self,
            *,
            enable_code_hook_invocation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            invocation_label: typing.Optional[builtins.str] = None,
            is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            post_code_hook_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.PostDialogCodeHookInvocationSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings that specify the dialog code hook that is called by Amazon Lex at a step of the conversation.

            :param enable_code_hook_invocation: Indicates whether a Lambda function should be invoked for the dialog.
            :param invocation_label: A label that indicates the dialog step from which the dialog code hook is happening.
            :param is_active: Determines whether a dialog code hook is used when the intent is activated.
            :param post_code_hook_specification: Contains the responses and actions that Amazon Lex takes after the Lambda function is complete.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehookinvocationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f5c8449c0054556f25620d50ae04a518ff060369080f98a3bc23f7c36fac499)
                check_type(argname="argument enable_code_hook_invocation", value=enable_code_hook_invocation, expected_type=type_hints["enable_code_hook_invocation"])
                check_type(argname="argument invocation_label", value=invocation_label, expected_type=type_hints["invocation_label"])
                check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
                check_type(argname="argument post_code_hook_specification", value=post_code_hook_specification, expected_type=type_hints["post_code_hook_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_code_hook_invocation is not None:
                self._values["enable_code_hook_invocation"] = enable_code_hook_invocation
            if invocation_label is not None:
                self._values["invocation_label"] = invocation_label
            if is_active is not None:
                self._values["is_active"] = is_active
            if post_code_hook_specification is not None:
                self._values["post_code_hook_specification"] = post_code_hook_specification

        @builtins.property
        def enable_code_hook_invocation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether a Lambda function should be invoked for the dialog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehookinvocationsetting.html#cfn-lex-bot-dialogcodehookinvocationsetting-enablecodehookinvocation
            '''
            result = self._values.get("enable_code_hook_invocation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def invocation_label(self) -> typing.Optional[builtins.str]:
            '''A label that indicates the dialog step from which the dialog code hook is happening.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehookinvocationsetting.html#cfn-lex-bot-dialogcodehookinvocationsetting-invocationlabel
            '''
            result = self._values.get("invocation_label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether a dialog code hook is used when the intent is activated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehookinvocationsetting.html#cfn-lex-bot-dialogcodehookinvocationsetting-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def post_code_hook_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PostDialogCodeHookInvocationSpecificationProperty"]]:
            '''Contains the responses and actions that Amazon Lex takes after the Lambda function is complete.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehookinvocationsetting.html#cfn-lex-bot-dialogcodehookinvocationsetting-postcodehookspecification
            '''
            result = self._values.get("post_code_hook_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PostDialogCodeHookInvocationSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DialogCodeHookInvocationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.DialogCodeHookSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class DialogCodeHookSettingProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Settings that determine the Lambda function that Amazon Lex uses for processing user responses.

            :param enabled: Enables the dialog code hook so that it processes user requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehooksetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                dialog_code_hook_setting_property = lex_mixins.CfnBotPropsMixin.DialogCodeHookSettingProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a421ef9e9fe1c0361265b299e843b8d84936a9a83ba9031946cb3893910d9ef5)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables the dialog code hook so that it processes user requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehooksetting.html#cfn-lex-bot-dialogcodehooksetting-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DialogCodeHookSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.DialogStateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dialog_action": "dialogAction",
            "intent": "intent",
            "session_attributes": "sessionAttributes",
        },
    )
    class DialogStateProperty:
        def __init__(
            self,
            *,
            dialog_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            intent: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.IntentOverrideProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            session_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SessionAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The current state of the conversation with the user.

            :param dialog_action: Defines the action that the bot executes at runtime when the conversation reaches this step.
            :param intent: Override settings to configure the intent state.
            :param session_attributes: Map of key/value pairs representing session-specific context information. It contains application information passed between Amazon Lex and a client application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogstate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                # slot_value_override_property_: lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty
                
                dialog_state_property = lex_mixins.CfnBotPropsMixin.DialogStateProperty(
                    dialog_action=lex_mixins.CfnBotPropsMixin.DialogActionProperty(
                        slot_to_elicit="slotToElicit",
                        suppress_next_message=False,
                        type="type"
                    ),
                    intent=lex_mixins.CfnBotPropsMixin.IntentOverrideProperty(
                        name="name",
                        slots=[lex_mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty(
                            slot_name="slotName",
                            slot_value_override=lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                                shape="shape",
                                value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                                    interpreted_value="interpretedValue"
                                ),
                                values=[slot_value_override_property_]
                            )
                        )]
                    ),
                    session_attributes=[lex_mixins.CfnBotPropsMixin.SessionAttributeProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba0c0637863f78a3572bda1d772b247e0f042ee3b4cf63c45ea6c6cf6bb2fd7b)
                check_type(argname="argument dialog_action", value=dialog_action, expected_type=type_hints["dialog_action"])
                check_type(argname="argument intent", value=intent, expected_type=type_hints["intent"])
                check_type(argname="argument session_attributes", value=session_attributes, expected_type=type_hints["session_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dialog_action is not None:
                self._values["dialog_action"] = dialog_action
            if intent is not None:
                self._values["intent"] = intent
            if session_attributes is not None:
                self._values["session_attributes"] = session_attributes

        @builtins.property
        def dialog_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogActionProperty"]]:
            '''Defines the action that the bot executes at runtime when the conversation reaches this step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogstate.html#cfn-lex-bot-dialogstate-dialogaction
            '''
            result = self._values.get("dialog_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogActionProperty"]], result)

        @builtins.property
        def intent(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.IntentOverrideProperty"]]:
            '''Override settings to configure the intent state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogstate.html#cfn-lex-bot-dialogstate-intent
            '''
            result = self._values.get("intent")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.IntentOverrideProperty"]], result)

        @builtins.property
        def session_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SessionAttributeProperty"]]]]:
            '''Map of key/value pairs representing session-specific context information.

            It contains application information passed between Amazon Lex and a client application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogstate.html#cfn-lex-bot-dialogstate-sessionattributes
            '''
            result = self._values.get("session_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SessionAttributeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DialogStateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ElicitationCodeHookInvocationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_code_hook_invocation": "enableCodeHookInvocation",
            "invocation_label": "invocationLabel",
        },
    )
    class ElicitationCodeHookInvocationSettingProperty:
        def __init__(
            self,
            *,
            enable_code_hook_invocation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            invocation_label: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings that specify the dialog code hook that is called by Amazon Lex between eliciting slot values.

            :param enable_code_hook_invocation: Indicates whether a Lambda function should be invoked for the dialog.
            :param invocation_label: A label that indicates the dialog step from which the dialog code hook is happening.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-elicitationcodehookinvocationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                elicitation_code_hook_invocation_setting_property = lex_mixins.CfnBotPropsMixin.ElicitationCodeHookInvocationSettingProperty(
                    enable_code_hook_invocation=False,
                    invocation_label="invocationLabel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36de176b0f26ffe375e4a46f6f82085758072a64ee40a9a5006132e77a618c34)
                check_type(argname="argument enable_code_hook_invocation", value=enable_code_hook_invocation, expected_type=type_hints["enable_code_hook_invocation"])
                check_type(argname="argument invocation_label", value=invocation_label, expected_type=type_hints["invocation_label"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_code_hook_invocation is not None:
                self._values["enable_code_hook_invocation"] = enable_code_hook_invocation
            if invocation_label is not None:
                self._values["invocation_label"] = invocation_label

        @builtins.property
        def enable_code_hook_invocation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether a Lambda function should be invoked for the dialog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-elicitationcodehookinvocationsetting.html#cfn-lex-bot-elicitationcodehookinvocationsetting-enablecodehookinvocation
            '''
            result = self._values.get("enable_code_hook_invocation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def invocation_label(self) -> typing.Optional[builtins.str]:
            '''A label that indicates the dialog step from which the dialog code hook is happening.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-elicitationcodehookinvocationsetting.html#cfn-lex-bot-elicitationcodehookinvocationsetting-invocationlabel
            '''
            result = self._values.get("invocation_label")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElicitationCodeHookInvocationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ErrorLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class ErrorLogSettingsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param enabled: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-errorlogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                error_log_settings_property = lex_mixins.CfnBotPropsMixin.ErrorLogSettingsProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab659331081ac4e213b56b601033fc9c7842d266c1ecd4c3480eb00414d19490)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-errorlogsettings.html#cfn-lex-bot-errorlogsettings-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ExactResponseFieldsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "answer_field": "answerField",
            "question_field": "questionField",
        },
    )
    class ExactResponseFieldsProperty:
        def __init__(
            self,
            *,
            answer_field: typing.Optional[builtins.str] = None,
            question_field: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the names of the fields used for an exact response to the user.

            :param answer_field: The name of the field that contains the answer to the query made to the OpenSearch Service database.
            :param question_field: The name of the field that contains the query made to the OpenSearch Service database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-exactresponsefields.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                exact_response_fields_property = lex_mixins.CfnBotPropsMixin.ExactResponseFieldsProperty(
                    answer_field="answerField",
                    question_field="questionField"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8082251912df13afedc67c6b605721e88fc47f81033b35f5f90334abcaa03623)
                check_type(argname="argument answer_field", value=answer_field, expected_type=type_hints["answer_field"])
                check_type(argname="argument question_field", value=question_field, expected_type=type_hints["question_field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_field is not None:
                self._values["answer_field"] = answer_field
            if question_field is not None:
                self._values["question_field"] = question_field

        @builtins.property
        def answer_field(self) -> typing.Optional[builtins.str]:
            '''The name of the field that contains the answer to the query made to the OpenSearch Service database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-exactresponsefields.html#cfn-lex-bot-exactresponsefields-answerfield
            '''
            result = self._values.get("answer_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def question_field(self) -> typing.Optional[builtins.str]:
            '''The name of the field that contains the query made to the OpenSearch Service database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-exactresponsefields.html#cfn-lex-bot-exactresponsefields-questionfield
            '''
            result = self._values.get("question_field")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExactResponseFieldsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ExternalSourceSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"grammar_slot_type_setting": "grammarSlotTypeSetting"},
    )
    class ExternalSourceSettingProperty:
        def __init__(
            self,
            *,
            grammar_slot_type_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.GrammarSlotTypeSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information about the external source of the slot type's definition.

            :param grammar_slot_type_setting: Settings required for a slot type based on a grammar that you provide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-externalsourcesetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                external_source_setting_property = lex_mixins.CfnBotPropsMixin.ExternalSourceSettingProperty(
                    grammar_slot_type_setting=lex_mixins.CfnBotPropsMixin.GrammarSlotTypeSettingProperty(
                        source=lex_mixins.CfnBotPropsMixin.GrammarSlotTypeSourceProperty(
                            kms_key_arn="kmsKeyArn",
                            s3_bucket_name="s3BucketName",
                            s3_object_key="s3ObjectKey"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0f7d773ce964591c88fcb10a844b20cd010ff4bab91ff474edac8945bdba658)
                check_type(argname="argument grammar_slot_type_setting", value=grammar_slot_type_setting, expected_type=type_hints["grammar_slot_type_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if grammar_slot_type_setting is not None:
                self._values["grammar_slot_type_setting"] = grammar_slot_type_setting

        @builtins.property
        def grammar_slot_type_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.GrammarSlotTypeSettingProperty"]]:
            '''Settings required for a slot type based on a grammar that you provide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-externalsourcesetting.html#cfn-lex-bot-externalsourcesetting-grammarslottypesetting
            '''
            result = self._values.get("grammar_slot_type_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.GrammarSlotTypeSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExternalSourceSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.FulfillmentCodeHookSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "fulfillment_updates_specification": "fulfillmentUpdatesSpecification",
            "is_active": "isActive",
            "post_fulfillment_status_specification": "postFulfillmentStatusSpecification",
        },
    )
    class FulfillmentCodeHookSettingProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            fulfillment_updates_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.FulfillmentUpdatesSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            post_fulfillment_status_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.PostFulfillmentStatusSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Determines if a Lambda function should be invoked for a specific intent.

            :param enabled: Indicates whether a Lambda function should be invoked to fulfill a specific intent.
            :param fulfillment_updates_specification: Provides settings for update messages sent to the user for long-running Lambda fulfillment functions. Fulfillment updates can be used only with streaming conversations.
            :param is_active: Determines whether the fulfillment code hook is used. When ``active`` is false, the code hook doesn't run.
            :param post_fulfillment_status_specification: Provides settings for messages sent to the user for after the Lambda fulfillment function completes. Post-fulfillment messages can be sent for both streaming and non-streaming conversations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa0bc4b7c6f5b2dccaa3f8cc45f5e4383a7f77e96994a95fc8a47d67aa92fb76)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument fulfillment_updates_specification", value=fulfillment_updates_specification, expected_type=type_hints["fulfillment_updates_specification"])
                check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
                check_type(argname="argument post_fulfillment_status_specification", value=post_fulfillment_status_specification, expected_type=type_hints["post_fulfillment_status_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if fulfillment_updates_specification is not None:
                self._values["fulfillment_updates_specification"] = fulfillment_updates_specification
            if is_active is not None:
                self._values["is_active"] = is_active
            if post_fulfillment_status_specification is not None:
                self._values["post_fulfillment_status_specification"] = post_fulfillment_status_specification

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether a Lambda function should be invoked to fulfill a specific intent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html#cfn-lex-bot-fulfillmentcodehooksetting-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def fulfillment_updates_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.FulfillmentUpdatesSpecificationProperty"]]:
            '''Provides settings for update messages sent to the user for long-running Lambda fulfillment functions.

            Fulfillment updates can be used only with streaming conversations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html#cfn-lex-bot-fulfillmentcodehooksetting-fulfillmentupdatesspecification
            '''
            result = self._values.get("fulfillment_updates_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.FulfillmentUpdatesSpecificationProperty"]], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the fulfillment code hook is used.

            When ``active`` is false, the code hook doesn't run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html#cfn-lex-bot-fulfillmentcodehooksetting-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def post_fulfillment_status_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PostFulfillmentStatusSpecificationProperty"]]:
            '''Provides settings for messages sent to the user for after the Lambda fulfillment function completes.

            Post-fulfillment messages can be sent for both streaming and non-streaming conversations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html#cfn-lex-bot-fulfillmentcodehooksetting-postfulfillmentstatusspecification
            '''
            result = self._values.get("post_fulfillment_status_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PostFulfillmentStatusSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentCodeHookSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.FulfillmentStartResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_interrupt": "allowInterrupt",
            "delay_in_seconds": "delayInSeconds",
            "message_groups": "messageGroups",
        },
    )
    class FulfillmentStartResponseSpecificationProperty:
        def __init__(
            self,
            *,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            delay_in_seconds: typing.Optional[jsii.Number] = None,
            message_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.MessageGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides settings for a message that is sent to the user when a fulfillment Lambda function starts running.

            :param allow_interrupt: Determines whether the user can interrupt the start message while it is playing.
            :param delay_in_seconds: The delay between when the Lambda fulfillment function starts running and the start message is played. If the Lambda function returns before the delay is over, the start message isn't played.
            :param message_groups: 1 - 5 message groups that contain start messages. Amazon Lex chooses one of the messages to play to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                fulfillment_start_response_specification_property = lex_mixins.CfnBotPropsMixin.FulfillmentStartResponseSpecificationProperty(
                    allow_interrupt=False,
                    delay_in_seconds=123,
                    message_groups=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                        message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle",
                                title="title"
                            ),
                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                        variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle",
                                title="title"
                            ),
                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ecf62733b4d727ebfa9cc7347f0b8d2cf6e70ad18da2fc8f91ef32b722809722)
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
                check_type(argname="argument delay_in_seconds", value=delay_in_seconds, expected_type=type_hints["delay_in_seconds"])
                check_type(argname="argument message_groups", value=message_groups, expected_type=type_hints["message_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt
            if delay_in_seconds is not None:
                self._values["delay_in_seconds"] = delay_in_seconds
            if message_groups is not None:
                self._values["message_groups"] = message_groups

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the user can interrupt the start message while it is playing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html#cfn-lex-bot-fulfillmentstartresponsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def delay_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The delay between when the Lambda fulfillment function starts running and the start message is played.

            If the Lambda function returns before the delay is over, the start message isn't played.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html#cfn-lex-bot-fulfillmentstartresponsespecification-delayinseconds
            '''
            result = self._values.get("delay_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def message_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageGroupProperty"]]]]:
            '''1 - 5 message groups that contain start messages.

            Amazon Lex chooses one of the messages to play to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html#cfn-lex-bot-fulfillmentstartresponsespecification-messagegroups
            '''
            result = self._values.get("message_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageGroupProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentStartResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.FulfillmentUpdateResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_interrupt": "allowInterrupt",
            "frequency_in_seconds": "frequencyInSeconds",
            "message_groups": "messageGroups",
        },
    )
    class FulfillmentUpdateResponseSpecificationProperty:
        def __init__(
            self,
            *,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            frequency_in_seconds: typing.Optional[jsii.Number] = None,
            message_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.MessageGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides settings for a message that is sent periodically to the user while a fulfillment Lambda function is running.

            :param allow_interrupt: Determines whether the user can interrupt an update message while it is playing.
            :param frequency_in_seconds: The frequency that a message is sent to the user. When the period ends, Amazon Lex chooses a message from the message groups and plays it to the user. If the fulfillment Lambda returns before the first period ends, an update message is not played to the user.
            :param message_groups: 1 - 5 message groups that contain update messages. Amazon Lex chooses one of the messages to play to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                fulfillment_update_response_specification_property = lex_mixins.CfnBotPropsMixin.FulfillmentUpdateResponseSpecificationProperty(
                    allow_interrupt=False,
                    frequency_in_seconds=123,
                    message_groups=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                        message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle",
                                title="title"
                            ),
                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                        variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle",
                                title="title"
                            ),
                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ef548033d673ec60fba04a94fa33f6361c5a647efaa5dbacd1025f8d2656101)
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
                check_type(argname="argument frequency_in_seconds", value=frequency_in_seconds, expected_type=type_hints["frequency_in_seconds"])
                check_type(argname="argument message_groups", value=message_groups, expected_type=type_hints["message_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt
            if frequency_in_seconds is not None:
                self._values["frequency_in_seconds"] = frequency_in_seconds
            if message_groups is not None:
                self._values["message_groups"] = message_groups

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the user can interrupt an update message while it is playing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html#cfn-lex-bot-fulfillmentupdateresponsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def frequency_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The frequency that a message is sent to the user.

            When the period ends, Amazon Lex chooses a message from the message groups and plays it to the user. If the fulfillment Lambda returns before the first period ends, an update message is not played to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html#cfn-lex-bot-fulfillmentupdateresponsespecification-frequencyinseconds
            '''
            result = self._values.get("frequency_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def message_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageGroupProperty"]]]]:
            '''1 - 5 message groups that contain update messages.

            Amazon Lex chooses one of the messages to play to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html#cfn-lex-bot-fulfillmentupdateresponsespecification-messagegroups
            '''
            result = self._values.get("message_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageGroupProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentUpdateResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.FulfillmentUpdatesSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active": "active",
            "start_response": "startResponse",
            "timeout_in_seconds": "timeoutInSeconds",
            "update_response": "updateResponse",
        },
    )
    class FulfillmentUpdatesSpecificationProperty:
        def __init__(
            self,
            *,
            active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            start_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.FulfillmentStartResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
            update_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.FulfillmentUpdateResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information for updating the user on the progress of fulfilling an intent.

            :param active: Determines whether fulfillment updates are sent to the user. When this field is true, updates are sent. If the ``active`` field is set to true, the ``startResponse`` , ``updateResponse`` , and ``timeoutInSeconds`` fields are required.
            :param start_response: Provides configuration information for the message sent to users when the fulfillment Lambda functions starts running.
            :param timeout_in_seconds: The length of time that the fulfillment Lambda function should run before it times out.
            :param update_response: Provides configuration information for messages sent periodically to the user while the fulfillment Lambda function is running.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                fulfillment_updates_specification_property = lex_mixins.CfnBotPropsMixin.FulfillmentUpdatesSpecificationProperty(
                    active=False,
                    start_response=lex_mixins.CfnBotPropsMixin.FulfillmentStartResponseSpecificationProperty(
                        allow_interrupt=False,
                        delay_in_seconds=123,
                        message_groups=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )]
                    ),
                    timeout_in_seconds=123,
                    update_response=lex_mixins.CfnBotPropsMixin.FulfillmentUpdateResponseSpecificationProperty(
                        allow_interrupt=False,
                        frequency_in_seconds=123,
                        message_groups=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15be51185c33abd8b0a3624944c1cbe01f3ba29d2f583eb40bab8bc00cac40d8)
                check_type(argname="argument active", value=active, expected_type=type_hints["active"])
                check_type(argname="argument start_response", value=start_response, expected_type=type_hints["start_response"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
                check_type(argname="argument update_response", value=update_response, expected_type=type_hints["update_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if active is not None:
                self._values["active"] = active
            if start_response is not None:
                self._values["start_response"] = start_response
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds
            if update_response is not None:
                self._values["update_response"] = update_response

        @builtins.property
        def active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether fulfillment updates are sent to the user. When this field is true, updates are sent.

            If the ``active`` field is set to true, the ``startResponse`` , ``updateResponse`` , and ``timeoutInSeconds`` fields are required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-active
            '''
            result = self._values.get("active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def start_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.FulfillmentStartResponseSpecificationProperty"]]:
            '''Provides configuration information for the message sent to users when the fulfillment Lambda functions starts running.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-startresponse
            '''
            result = self._values.get("start_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.FulfillmentStartResponseSpecificationProperty"]], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The length of time that the fulfillment Lambda function should run before it times out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def update_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.FulfillmentUpdateResponseSpecificationProperty"]]:
            '''Provides configuration information for messages sent periodically to the user while the fulfillment Lambda function is running.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-updateresponse
            '''
            result = self._values.get("update_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.FulfillmentUpdateResponseSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentUpdatesSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.GenerativeAISettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "buildtime_settings": "buildtimeSettings",
            "runtime_settings": "runtimeSettings",
        },
    )
    class GenerativeAISettingsProperty:
        def __init__(
            self,
            *,
            buildtime_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BuildtimeSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            runtime_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.RuntimeSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains specifications about the generative AI capabilities from Amazon Bedrock that you can turn on for your bot.

            :param buildtime_settings: 
            :param runtime_settings: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-generativeaisettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                generative_aISettings_property = lex_mixins.CfnBotPropsMixin.GenerativeAISettingsProperty(
                    buildtime_settings=lex_mixins.CfnBotPropsMixin.BuildtimeSettingsProperty(
                        descriptive_bot_builder_specification=lex_mixins.CfnBotPropsMixin.DescriptiveBotBuilderSpecificationProperty(
                            bedrock_model_specification=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                                bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                                    bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                                    bedrock_guardrail_version="bedrockGuardrailVersion"
                                ),
                                bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                                bedrock_trace_status="bedrockTraceStatus",
                                model_arn="modelArn"
                            ),
                            enabled=False
                        ),
                        sample_utterance_generation_specification=lex_mixins.CfnBotPropsMixin.SampleUtteranceGenerationSpecificationProperty(
                            bedrock_model_specification=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                                bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                                    bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                                    bedrock_guardrail_version="bedrockGuardrailVersion"
                                ),
                                bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                                bedrock_trace_status="bedrockTraceStatus",
                                model_arn="modelArn"
                            ),
                            enabled=False
                        )
                    ),
                    runtime_settings=lex_mixins.CfnBotPropsMixin.RuntimeSettingsProperty(
                        nlu_improvement_specification=lex_mixins.CfnBotPropsMixin.NluImprovementSpecificationProperty(
                            enabled=False
                        ),
                        slot_resolution_improvement_specification=lex_mixins.CfnBotPropsMixin.SlotResolutionImprovementSpecificationProperty(
                            bedrock_model_specification=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                                bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                                    bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                                    bedrock_guardrail_version="bedrockGuardrailVersion"
                                ),
                                bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                                bedrock_trace_status="bedrockTraceStatus",
                                model_arn="modelArn"
                            ),
                            enabled=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a80e3e6df1d385566e495e03b3aab93f98b594c18661824afe466bcb6566a34)
                check_type(argname="argument buildtime_settings", value=buildtime_settings, expected_type=type_hints["buildtime_settings"])
                check_type(argname="argument runtime_settings", value=runtime_settings, expected_type=type_hints["runtime_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if buildtime_settings is not None:
                self._values["buildtime_settings"] = buildtime_settings
            if runtime_settings is not None:
                self._values["runtime_settings"] = runtime_settings

        @builtins.property
        def buildtime_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BuildtimeSettingsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-generativeaisettings.html#cfn-lex-bot-generativeaisettings-buildtimesettings
            '''
            result = self._values.get("buildtime_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BuildtimeSettingsProperty"]], result)

        @builtins.property
        def runtime_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.RuntimeSettingsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-generativeaisettings.html#cfn-lex-bot-generativeaisettings-runtimesettings
            '''
            result = self._values.get("runtime_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.RuntimeSettingsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GenerativeAISettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.GrammarSlotTypeSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class GrammarSlotTypeSettingProperty:
        def __init__(
            self,
            *,
            source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.GrammarSlotTypeSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings requried for a slot type based on a grammar that you provide.

            :param source: The source of the grammar used to create the slot type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                grammar_slot_type_setting_property = lex_mixins.CfnBotPropsMixin.GrammarSlotTypeSettingProperty(
                    source=lex_mixins.CfnBotPropsMixin.GrammarSlotTypeSourceProperty(
                        kms_key_arn="kmsKeyArn",
                        s3_bucket_name="s3BucketName",
                        s3_object_key="s3ObjectKey"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__360c21d74df59ee2ffb166c206ccadcb4536eccadedeb5bd70b5bf2b71ee76fe)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.GrammarSlotTypeSourceProperty"]]:
            '''The source of the grammar used to create the slot type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesetting.html#cfn-lex-bot-grammarslottypesetting-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.GrammarSlotTypeSourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrammarSlotTypeSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.GrammarSlotTypeSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_key_arn": "kmsKeyArn",
            "s3_bucket_name": "s3BucketName",
            "s3_object_key": "s3ObjectKey",
        },
    )
    class GrammarSlotTypeSourceProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
            s3_object_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the Amazon S3 bucket name and location for the grammar that is the source for the slot type.

            :param kms_key_arn: The AWS key required to decrypt the contents of the grammar, if any.
            :param s3_bucket_name: The name of the Amazon S3 bucket that contains the grammar source.
            :param s3_object_key: The path to the grammar in the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                grammar_slot_type_source_property = lex_mixins.CfnBotPropsMixin.GrammarSlotTypeSourceProperty(
                    kms_key_arn="kmsKeyArn",
                    s3_bucket_name="s3BucketName",
                    s3_object_key="s3ObjectKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8bb0e7e63285c76067688f00e4240eb16bbc00dc6505938c4898a9d3595ade0)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument s3_object_key", value=s3_object_key, expected_type=type_hints["s3_object_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name
            if s3_object_key is not None:
                self._values["s3_object_key"] = s3_object_key

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The AWS  key required to decrypt the contents of the grammar, if any.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html#cfn-lex-bot-grammarslottypesource-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket that contains the grammar source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html#cfn-lex-bot-grammarslottypesource-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_key(self) -> typing.Optional[builtins.str]:
            '''The path to the grammar in the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html#cfn-lex-bot-grammarslottypesource-s3objectkey
            '''
            result = self._values.get("s3_object_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrammarSlotTypeSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ImageResponseCardProperty",
        jsii_struct_bases=[],
        name_mapping={
            "buttons": "buttons",
            "image_url": "imageUrl",
            "subtitle": "subtitle",
            "title": "title",
        },
    )
    class ImageResponseCardProperty:
        def __init__(
            self,
            *,
            buttons: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ButtonProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            image_url: typing.Optional[builtins.str] = None,
            subtitle: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A card that is shown to the user by a messaging platform.

            You define the contents of the card, the card is displayed by the platform.

            When you use a response card, the response from the user is constrained to the text associated with a button on the card.

            :param buttons: A list of buttons that should be displayed on the response card. The arrangement of the buttons is determined by the platform that displays the button.
            :param image_url: The URL of an image to display on the response card. The image URL must be publicly available so that the platform displaying the response card has access to the image.
            :param subtitle: The subtitle to display on the response card. The format of the subtitle is determined by the platform displaying the response card.
            :param title: The title to display on the response card. The format of the title is determined by the platform displaying the response card.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                image_response_card_property = lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                        text="text",
                        value="value"
                    )],
                    image_url="imageUrl",
                    subtitle="subtitle",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40505c8cf59be20d31311744201fd37b0933075f3895acc6d51796a4fbe32c34)
                check_type(argname="argument buttons", value=buttons, expected_type=type_hints["buttons"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument subtitle", value=subtitle, expected_type=type_hints["subtitle"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if buttons is not None:
                self._values["buttons"] = buttons
            if image_url is not None:
                self._values["image_url"] = image_url
            if subtitle is not None:
                self._values["subtitle"] = subtitle
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def buttons(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ButtonProperty"]]]]:
            '''A list of buttons that should be displayed on the response card.

            The arrangement of the buttons is determined by the platform that displays the button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-buttons
            '''
            result = self._values.get("buttons")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ButtonProperty"]]]], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image to display on the response card.

            The image URL must be publicly available so that the platform displaying the response card has access to the image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subtitle(self) -> typing.Optional[builtins.str]:
            '''The subtitle to display on the response card.

            The format of the subtitle is determined by the platform displaying the response card.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-subtitle
            '''
            result = self._values.get("subtitle")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to display on the response card.

            The format of the title is determined by the platform displaying the response card.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageResponseCardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.InitialResponseSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_hook": "codeHook",
            "conditional": "conditional",
            "initial_response": "initialResponse",
            "next_step": "nextStep",
        },
    )
    class InitialResponseSettingProperty:
        def __init__(
            self,
            *,
            code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            initial_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration setting for a response sent to the user before Amazon Lex starts eliciting slots.

            :param code_hook: Settings that specify the dialog code hook that is called by Amazon Lex at a step of the conversation.
            :param conditional: Provides a list of conditional branches. Branches are evaluated in the order that they are entered in the list. The first branch with a condition that evaluates to true is executed. The last branch in the list is the default branch. The default branch should not have any condition expression. The default branch is executed if no other branch has a matching condition.
            :param initial_response: Specifies a list of message groups that Amazon Lex uses to respond the user input.
            :param next_step: The next step in the conversation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-initialresponsesetting.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4da8189b0690992713156d1c916794d5aa830b067c2d4420e79221d2a1d62243)
                check_type(argname="argument code_hook", value=code_hook, expected_type=type_hints["code_hook"])
                check_type(argname="argument conditional", value=conditional, expected_type=type_hints["conditional"])
                check_type(argname="argument initial_response", value=initial_response, expected_type=type_hints["initial_response"])
                check_type(argname="argument next_step", value=next_step, expected_type=type_hints["next_step"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_hook is not None:
                self._values["code_hook"] = code_hook
            if conditional is not None:
                self._values["conditional"] = conditional
            if initial_response is not None:
                self._values["initial_response"] = initial_response
            if next_step is not None:
                self._values["next_step"] = next_step

        @builtins.property
        def code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty"]]:
            '''Settings that specify the dialog code hook that is called by Amazon Lex at a step of the conversation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-initialresponsesetting.html#cfn-lex-bot-initialresponsesetting-codehook
            '''
            result = self._values.get("code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty"]], result)

        @builtins.property
        def conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''Provides a list of conditional branches.

            Branches are evaluated in the order that they are entered in the list. The first branch with a condition that evaluates to true is executed. The last branch in the list is the default branch. The default branch should not have any condition expression. The default branch is executed if no other branch has a matching condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-initialresponsesetting.html#cfn-lex-bot-initialresponsesetting-conditional
            '''
            result = self._values.get("conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def initial_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond the user input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-initialresponsesetting.html#cfn-lex-bot-initialresponsesetting-initialresponse
            '''
            result = self._values.get("initial_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''The next step in the conversation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-initialresponsesetting.html#cfn-lex-bot-initialresponsesetting-nextstep
            '''
            result = self._values.get("next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InitialResponseSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.InputContextProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class InputContextProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''A context that must be active for an intent to be selected by Amazon Lex.

            :param name: The name of the context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-inputcontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                input_context_property = lex_mixins.CfnBotPropsMixin.InputContextProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19113d1a9f5e477f3c0e3b08d988b3657244fc8f57f7e2731fcffe4fad11357b)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-inputcontext.html#cfn-lex-bot-inputcontext-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.IntentClosingSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "closing_response": "closingResponse",
            "conditional": "conditional",
            "is_active": "isActive",
            "next_step": "nextStep",
        },
    )
    class IntentClosingSettingProperty:
        def __init__(
            self,
            *,
            closing_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides a statement the Amazon Lex conveys to the user when the intent is successfully fulfilled.

            :param closing_response: The response that Amazon Lex sends to the user when the intent is complete.
            :param conditional: A list of conditional branches associated with the intent's closing response. These branches are executed when the ``nextStep`` attribute is set to ``EvalutateConditional`` .
            :param is_active: Specifies whether an intent's closing response is used. When this field is false, the closing response isn't sent to the user. If the ``IsActive`` field isn't specified, the default is true.
            :param next_step: Specifies the next step that the bot executes after playing the intent's closing response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                # slot_value_override_property_: lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty
                
                intent_closing_setting_property = lex_mixins.CfnBotPropsMixin.IntentClosingSettingProperty(
                    closing_response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                        allow_interrupt=False,
                        message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )]
                    ),
                    conditional=lex_mixins.CfnBotPropsMixin.ConditionalSpecificationProperty(
                        conditional_branches=[lex_mixins.CfnBotPropsMixin.ConditionalBranchProperty(
                            condition=lex_mixins.CfnBotPropsMixin.ConditionProperty(
                                expression_string="expressionString"
                            ),
                            name="name",
                            next_step=lex_mixins.CfnBotPropsMixin.DialogStateProperty(
                                dialog_action=lex_mixins.CfnBotPropsMixin.DialogActionProperty(
                                    slot_to_elicit="slotToElicit",
                                    suppress_next_message=False,
                                    type="type"
                                ),
                                intent=lex_mixins.CfnBotPropsMixin.IntentOverrideProperty(
                                    name="name",
                                    slots=[lex_mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty(
                                        slot_name="slotName",
                                        slot_value_override=lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                                            shape="shape",
                                            value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                                                interpreted_value="interpretedValue"
                                            ),
                                            values=[slot_value_override_property_]
                                        )
                                    )]
                                ),
                                session_attributes=[lex_mixins.CfnBotPropsMixin.SessionAttributeProperty(
                                    key="key",
                                    value="value"
                                )]
                            ),
                            response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                                allow_interrupt=False,
                                message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                    message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle",
                                            title="title"
                                        ),
                                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                                    variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle",
                                            title="title"
                                        ),
                                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )]
                            )
                        )],
                        default_branch=lex_mixins.CfnBotPropsMixin.DefaultConditionalBranchProperty(
                            next_step=lex_mixins.CfnBotPropsMixin.DialogStateProperty(
                                dialog_action=lex_mixins.CfnBotPropsMixin.DialogActionProperty(
                                    slot_to_elicit="slotToElicit",
                                    suppress_next_message=False,
                                    type="type"
                                ),
                                intent=lex_mixins.CfnBotPropsMixin.IntentOverrideProperty(
                                    name="name",
                                    slots=[lex_mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty(
                                        slot_name="slotName",
                                        slot_value_override=lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                                            shape="shape",
                                            value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                                                interpreted_value="interpretedValue"
                                            ),
                                            values=[slot_value_override_property_]
                                        )
                                    )]
                                ),
                                session_attributes=[lex_mixins.CfnBotPropsMixin.SessionAttributeProperty(
                                    key="key",
                                    value="value"
                                )]
                            ),
                            response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                                allow_interrupt=False,
                                message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                    message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle",
                                            title="title"
                                        ),
                                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                                    variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle",
                                            title="title"
                                        ),
                                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )]
                            )
                        ),
                        is_active=False
                    ),
                    is_active=False,
                    next_step=lex_mixins.CfnBotPropsMixin.DialogStateProperty(
                        dialog_action=lex_mixins.CfnBotPropsMixin.DialogActionProperty(
                            slot_to_elicit="slotToElicit",
                            suppress_next_message=False,
                            type="type"
                        ),
                        intent=lex_mixins.CfnBotPropsMixin.IntentOverrideProperty(
                            name="name",
                            slots=[lex_mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty(
                                slot_name="slotName",
                                slot_value_override=lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                                    shape="shape",
                                    value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                                        interpreted_value="interpretedValue"
                                    ),
                                    values=[slot_value_override_property_]
                                )
                            )]
                        ),
                        session_attributes=[lex_mixins.CfnBotPropsMixin.SessionAttributeProperty(
                            key="key",
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec4ae10c12927d6b59dd394c92bc766c45745408310c7889d71488d94382449d)
                check_type(argname="argument closing_response", value=closing_response, expected_type=type_hints["closing_response"])
                check_type(argname="argument conditional", value=conditional, expected_type=type_hints["conditional"])
                check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
                check_type(argname="argument next_step", value=next_step, expected_type=type_hints["next_step"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if closing_response is not None:
                self._values["closing_response"] = closing_response
            if conditional is not None:
                self._values["conditional"] = conditional
            if is_active is not None:
                self._values["is_active"] = is_active
            if next_step is not None:
                self._values["next_step"] = next_step

        @builtins.property
        def closing_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''The response that Amazon Lex sends to the user when the intent is complete.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html#cfn-lex-bot-intentclosingsetting-closingresponse
            '''
            result = self._values.get("closing_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches associated with the intent's closing response.

            These branches are executed when the ``nextStep`` attribute is set to ``EvalutateConditional`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html#cfn-lex-bot-intentclosingsetting-conditional
            '''
            result = self._values.get("conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether an intent's closing response is used.

            When this field is false, the closing response isn't sent to the user. If the ``IsActive`` field isn't specified, the default is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html#cfn-lex-bot-intentclosingsetting-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifies the next step that the bot executes after playing the intent's closing response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html#cfn-lex-bot-intentclosingsetting-nextstep
            '''
            result = self._values.get("next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntentClosingSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.IntentConfirmationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_hook": "codeHook",
            "confirmation_conditional": "confirmationConditional",
            "confirmation_next_step": "confirmationNextStep",
            "confirmation_response": "confirmationResponse",
            "declination_conditional": "declinationConditional",
            "declination_next_step": "declinationNextStep",
            "declination_response": "declinationResponse",
            "elicitation_code_hook": "elicitationCodeHook",
            "failure_conditional": "failureConditional",
            "failure_next_step": "failureNextStep",
            "failure_response": "failureResponse",
            "is_active": "isActive",
            "prompt_specification": "promptSpecification",
        },
    )
    class IntentConfirmationSettingProperty:
        def __init__(
            self,
            *,
            code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            confirmation_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            confirmation_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            confirmation_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            declination_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            declination_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            declination_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            elicitation_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ElicitationCodeHookInvocationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            prompt_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.PromptSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides a prompt for making sure that the user is ready for the intent to be fulfilled.

            :param code_hook: The ``DialogCodeHookInvocationSetting`` object associated with intent's confirmation step. The dialog code hook is triggered based on these invocation settings when the confirmation next step or declination next step or failure next step is ``InvokeDialogCodeHook`` .
            :param confirmation_conditional: A list of conditional branches to evaluate after the intent is closed.
            :param confirmation_next_step: Specifies the next step that the bot executes when the customer confirms the intent.
            :param confirmation_response: Specifies a list of message groups that Amazon Lex uses to respond the user input.
            :param declination_conditional: A list of conditional branches to evaluate after the intent is declined.
            :param declination_next_step: Specifies the next step that the bot executes when the customer declines the intent.
            :param declination_response: When the user answers "no" to the question defined in ``promptSpecification`` , Amazon Lex responds with this response to acknowledge that the intent was canceled.
            :param elicitation_code_hook: The ``DialogCodeHookInvocationSetting`` used when the code hook is invoked during confirmation prompt retries.
            :param failure_conditional: Provides a list of conditional branches. Branches are evaluated in the order that they are entered in the list. The first branch with a condition that evaluates to true is executed. The last branch in the list is the default branch. The default branch should not have any condition expression. The default branch is executed if no other branch has a matching condition.
            :param failure_next_step: The next step to take in the conversation if the confirmation step fails.
            :param failure_response: Specifies a list of message groups that Amazon Lex uses to respond the user input when the intent confirmation fails.
            :param is_active: Specifies whether the intent's confirmation is sent to the user. When this field is false, confirmation and declination responses aren't sent. If the ``IsActive`` field isn't specified, the default is true.
            :param prompt_specification: Prompts the user to confirm the intent. This question should have a yes or no answer. Amazon Lex uses this prompt to ensure that the user acknowledges that the intent is ready for fulfillment. For example, with the ``OrderPizza`` intent, you might want to confirm that the order is correct before placing it. For other intents, such as intents that simply respond to user questions, you might not need to ask the user for confirmation before providing the information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e32c3e61367112a0caee14981650918a0b46ddcf4cfb88c25c10e8d063fa73f4)
                check_type(argname="argument code_hook", value=code_hook, expected_type=type_hints["code_hook"])
                check_type(argname="argument confirmation_conditional", value=confirmation_conditional, expected_type=type_hints["confirmation_conditional"])
                check_type(argname="argument confirmation_next_step", value=confirmation_next_step, expected_type=type_hints["confirmation_next_step"])
                check_type(argname="argument confirmation_response", value=confirmation_response, expected_type=type_hints["confirmation_response"])
                check_type(argname="argument declination_conditional", value=declination_conditional, expected_type=type_hints["declination_conditional"])
                check_type(argname="argument declination_next_step", value=declination_next_step, expected_type=type_hints["declination_next_step"])
                check_type(argname="argument declination_response", value=declination_response, expected_type=type_hints["declination_response"])
                check_type(argname="argument elicitation_code_hook", value=elicitation_code_hook, expected_type=type_hints["elicitation_code_hook"])
                check_type(argname="argument failure_conditional", value=failure_conditional, expected_type=type_hints["failure_conditional"])
                check_type(argname="argument failure_next_step", value=failure_next_step, expected_type=type_hints["failure_next_step"])
                check_type(argname="argument failure_response", value=failure_response, expected_type=type_hints["failure_response"])
                check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
                check_type(argname="argument prompt_specification", value=prompt_specification, expected_type=type_hints["prompt_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_hook is not None:
                self._values["code_hook"] = code_hook
            if confirmation_conditional is not None:
                self._values["confirmation_conditional"] = confirmation_conditional
            if confirmation_next_step is not None:
                self._values["confirmation_next_step"] = confirmation_next_step
            if confirmation_response is not None:
                self._values["confirmation_response"] = confirmation_response
            if declination_conditional is not None:
                self._values["declination_conditional"] = declination_conditional
            if declination_next_step is not None:
                self._values["declination_next_step"] = declination_next_step
            if declination_response is not None:
                self._values["declination_response"] = declination_response
            if elicitation_code_hook is not None:
                self._values["elicitation_code_hook"] = elicitation_code_hook
            if failure_conditional is not None:
                self._values["failure_conditional"] = failure_conditional
            if failure_next_step is not None:
                self._values["failure_next_step"] = failure_next_step
            if failure_response is not None:
                self._values["failure_response"] = failure_response
            if is_active is not None:
                self._values["is_active"] = is_active
            if prompt_specification is not None:
                self._values["prompt_specification"] = prompt_specification

        @builtins.property
        def code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty"]]:
            '''The ``DialogCodeHookInvocationSetting`` object associated with intent's confirmation step.

            The dialog code hook is triggered based on these invocation settings when the confirmation next step or declination next step or failure next step is ``InvokeDialogCodeHook`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-codehook
            '''
            result = self._values.get("code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty"]], result)

        @builtins.property
        def confirmation_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches to evaluate after the intent is closed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-confirmationconditional
            '''
            result = self._values.get("confirmation_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def confirmation_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifies the next step that the bot executes when the customer confirms the intent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-confirmationnextstep
            '''
            result = self._values.get("confirmation_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def confirmation_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond the user input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-confirmationresponse
            '''
            result = self._values.get("confirmation_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def declination_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches to evaluate after the intent is declined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-declinationconditional
            '''
            result = self._values.get("declination_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def declination_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifies the next step that the bot executes when the customer declines the intent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-declinationnextstep
            '''
            result = self._values.get("declination_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def declination_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''When the user answers "no" to the question defined in ``promptSpecification`` , Amazon Lex responds with this response to acknowledge that the intent was canceled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-declinationresponse
            '''
            result = self._values.get("declination_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def elicitation_code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ElicitationCodeHookInvocationSettingProperty"]]:
            '''The ``DialogCodeHookInvocationSetting`` used when the code hook is invoked during confirmation prompt retries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-elicitationcodehook
            '''
            result = self._values.get("elicitation_code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ElicitationCodeHookInvocationSettingProperty"]], result)

        @builtins.property
        def failure_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''Provides a list of conditional branches.

            Branches are evaluated in the order that they are entered in the list. The first branch with a condition that evaluates to true is executed. The last branch in the list is the default branch. The default branch should not have any condition expression. The default branch is executed if no other branch has a matching condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-failureconditional
            '''
            result = self._values.get("failure_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def failure_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''The next step to take in the conversation if the confirmation step fails.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-failurenextstep
            '''
            result = self._values.get("failure_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def failure_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond the user input when the intent confirmation fails.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-failureresponse
            '''
            result = self._values.get("failure_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the intent's confirmation is sent to the user.

            When this field is false, confirmation and declination responses aren't sent. If the ``IsActive`` field isn't specified, the default is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def prompt_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PromptSpecificationProperty"]]:
            '''Prompts the user to confirm the intent. This question should have a yes or no answer.

            Amazon Lex uses this prompt to ensure that the user acknowledges that the intent is ready for fulfillment. For example, with the ``OrderPizza`` intent, you might want to confirm that the order is correct before placing it. For other intents, such as intents that simply respond to user questions, you might not need to ask the user for confirmation before providing the information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-promptspecification
            '''
            result = self._values.get("prompt_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PromptSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntentConfirmationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.IntentOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "slots": "slots"},
    )
    class IntentOverrideProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            slots: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotValueOverrideMapProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Override settings to configure the intent state.

            :param name: The name of the intent. Only required when you're switching intents.
            :param slots: A map of all of the slot value overrides for the intent. The name of the slot maps to the value of the slot. Slots that are not included in the map aren't overridden.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                # slot_value_override_property_: lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty
                
                intent_override_property = lex_mixins.CfnBotPropsMixin.IntentOverrideProperty(
                    name="name",
                    slots=[lex_mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty(
                        slot_name="slotName",
                        slot_value_override=lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                            shape="shape",
                            value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                                interpreted_value="interpretedValue"
                            ),
                            values=[slot_value_override_property_]
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b3cbe6cf71378db85833b271fee2cc414c522c861515c73f4fb3344491bf413)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument slots", value=slots, expected_type=type_hints["slots"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if slots is not None:
                self._values["slots"] = slots

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the intent.

            Only required when you're switching intents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentoverride.html#cfn-lex-bot-intentoverride-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slots(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueOverrideMapProperty"]]]]:
            '''A map of all of the slot value overrides for the intent.

            The name of the slot maps to the value of the slot. Slots that are not included in the map aren't overridden.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentoverride.html#cfn-lex-bot-intentoverride-slots
            '''
            result = self._values.get("slots")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueOverrideMapProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntentOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.IntentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_agent_intent_configuration": "bedrockAgentIntentConfiguration",
            "description": "description",
            "dialog_code_hook": "dialogCodeHook",
            "fulfillment_code_hook": "fulfillmentCodeHook",
            "initial_response_setting": "initialResponseSetting",
            "input_contexts": "inputContexts",
            "intent_closing_setting": "intentClosingSetting",
            "intent_confirmation_setting": "intentConfirmationSetting",
            "kendra_configuration": "kendraConfiguration",
            "name": "name",
            "output_contexts": "outputContexts",
            "parent_intent_signature": "parentIntentSignature",
            "q_in_connect_intent_configuration": "qInConnectIntentConfiguration",
            "qn_a_intent_configuration": "qnAIntentConfiguration",
            "sample_utterances": "sampleUtterances",
            "slot_priorities": "slotPriorities",
            "slots": "slots",
        },
    )
    class IntentProperty:
        def __init__(
            self,
            *,
            bedrock_agent_intent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BedrockAgentIntentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            dialog_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogCodeHookSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            fulfillment_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.FulfillmentCodeHookSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            initial_response_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.InitialResponseSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            input_contexts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.InputContextProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            intent_closing_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.IntentClosingSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            intent_confirmation_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.IntentConfirmationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kendra_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.KendraConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            output_contexts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.OutputContextProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            parent_intent_signature: typing.Optional[builtins.str] = None,
            q_in_connect_intent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.QInConnectIntentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            qn_a_intent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.QnAIntentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sample_utterances: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SampleUtteranceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            slot_priorities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotPriorityProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            slots: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Represents an action that the user wants to perform.

            :param bedrock_agent_intent_configuration: 
            :param description: A description of the intent. Use the description to help identify the intent in lists.
            :param dialog_code_hook: Specifies that Amazon Lex invokes the alias Lambda function for each user input. You can invoke this Lambda function to personalize user interaction.
            :param fulfillment_code_hook: Specifies that Amazon Lex invokes the alias Lambda function when the intent is ready for fulfillment. You can invoke this function to complete the bot's transaction with the user.
            :param initial_response_setting: Configuration setting for a response sent to the user before Amazon Lex starts eliciting slots.
            :param input_contexts: A list of contexts that must be active for this intent to be considered by Amazon Lex .
            :param intent_closing_setting: Sets the response that Amazon Lex sends to the user when the intent is closed.
            :param intent_confirmation_setting: Provides prompts that Amazon Lex sends to the user to confirm the completion of an intent. If the user answers "no," the settings contain a statement that is sent to the user to end the intent.
            :param kendra_configuration: Provides configuration information for the ``AMAZON.KendraSearchIntent`` intent. When you use this intent, Amazon Lex searches the specified Amazon Kendra index and returns documents from the index that match the user's utterance.
            :param name: The name of the intent. Intent names must be unique within the locale that contains the intent and can't match the name of any built-in intent.
            :param output_contexts: A list of contexts that the intent activates when it is fulfilled.
            :param parent_intent_signature: A unique identifier for the built-in intent to base this intent on.
            :param q_in_connect_intent_configuration: 
            :param qn_a_intent_configuration: 
            :param sample_utterances: A list of utterances that a user might say to signal the intent.
            :param slot_priorities: Indicates the priority for slots. Amazon Lex prompts the user for slot values in priority order.
            :param slots: A list of slots that the intent requires for fulfillment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__81f88d897d52eafda4e74a7892ba13638224db7c4b10233ae6015156b1c14eac)
                check_type(argname="argument bedrock_agent_intent_configuration", value=bedrock_agent_intent_configuration, expected_type=type_hints["bedrock_agent_intent_configuration"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument dialog_code_hook", value=dialog_code_hook, expected_type=type_hints["dialog_code_hook"])
                check_type(argname="argument fulfillment_code_hook", value=fulfillment_code_hook, expected_type=type_hints["fulfillment_code_hook"])
                check_type(argname="argument initial_response_setting", value=initial_response_setting, expected_type=type_hints["initial_response_setting"])
                check_type(argname="argument input_contexts", value=input_contexts, expected_type=type_hints["input_contexts"])
                check_type(argname="argument intent_closing_setting", value=intent_closing_setting, expected_type=type_hints["intent_closing_setting"])
                check_type(argname="argument intent_confirmation_setting", value=intent_confirmation_setting, expected_type=type_hints["intent_confirmation_setting"])
                check_type(argname="argument kendra_configuration", value=kendra_configuration, expected_type=type_hints["kendra_configuration"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument output_contexts", value=output_contexts, expected_type=type_hints["output_contexts"])
                check_type(argname="argument parent_intent_signature", value=parent_intent_signature, expected_type=type_hints["parent_intent_signature"])
                check_type(argname="argument q_in_connect_intent_configuration", value=q_in_connect_intent_configuration, expected_type=type_hints["q_in_connect_intent_configuration"])
                check_type(argname="argument qn_a_intent_configuration", value=qn_a_intent_configuration, expected_type=type_hints["qn_a_intent_configuration"])
                check_type(argname="argument sample_utterances", value=sample_utterances, expected_type=type_hints["sample_utterances"])
                check_type(argname="argument slot_priorities", value=slot_priorities, expected_type=type_hints["slot_priorities"])
                check_type(argname="argument slots", value=slots, expected_type=type_hints["slots"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_agent_intent_configuration is not None:
                self._values["bedrock_agent_intent_configuration"] = bedrock_agent_intent_configuration
            if description is not None:
                self._values["description"] = description
            if dialog_code_hook is not None:
                self._values["dialog_code_hook"] = dialog_code_hook
            if fulfillment_code_hook is not None:
                self._values["fulfillment_code_hook"] = fulfillment_code_hook
            if initial_response_setting is not None:
                self._values["initial_response_setting"] = initial_response_setting
            if input_contexts is not None:
                self._values["input_contexts"] = input_contexts
            if intent_closing_setting is not None:
                self._values["intent_closing_setting"] = intent_closing_setting
            if intent_confirmation_setting is not None:
                self._values["intent_confirmation_setting"] = intent_confirmation_setting
            if kendra_configuration is not None:
                self._values["kendra_configuration"] = kendra_configuration
            if name is not None:
                self._values["name"] = name
            if output_contexts is not None:
                self._values["output_contexts"] = output_contexts
            if parent_intent_signature is not None:
                self._values["parent_intent_signature"] = parent_intent_signature
            if q_in_connect_intent_configuration is not None:
                self._values["q_in_connect_intent_configuration"] = q_in_connect_intent_configuration
            if qn_a_intent_configuration is not None:
                self._values["qn_a_intent_configuration"] = qn_a_intent_configuration
            if sample_utterances is not None:
                self._values["sample_utterances"] = sample_utterances
            if slot_priorities is not None:
                self._values["slot_priorities"] = slot_priorities
            if slots is not None:
                self._values["slots"] = slots

        @builtins.property
        def bedrock_agent_intent_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockAgentIntentConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-bedrockagentintentconfiguration
            '''
            result = self._values.get("bedrock_agent_intent_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockAgentIntentConfigurationProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the intent.

            Use the description to help identify the intent in lists.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dialog_code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogCodeHookSettingProperty"]]:
            '''Specifies that Amazon Lex invokes the alias Lambda function for each user input.

            You can invoke this Lambda function to personalize user interaction.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-dialogcodehook
            '''
            result = self._values.get("dialog_code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogCodeHookSettingProperty"]], result)

        @builtins.property
        def fulfillment_code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.FulfillmentCodeHookSettingProperty"]]:
            '''Specifies that Amazon Lex invokes the alias Lambda function when the intent is ready for fulfillment.

            You can invoke this function to complete the bot's transaction with the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-fulfillmentcodehook
            '''
            result = self._values.get("fulfillment_code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.FulfillmentCodeHookSettingProperty"]], result)

        @builtins.property
        def initial_response_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.InitialResponseSettingProperty"]]:
            '''Configuration setting for a response sent to the user before Amazon Lex starts eliciting slots.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-initialresponsesetting
            '''
            result = self._values.get("initial_response_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.InitialResponseSettingProperty"]], result)

        @builtins.property
        def input_contexts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.InputContextProperty"]]]]:
            '''A list of contexts that must be active for this intent to be considered by Amazon Lex .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-inputcontexts
            '''
            result = self._values.get("input_contexts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.InputContextProperty"]]]], result)

        @builtins.property
        def intent_closing_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.IntentClosingSettingProperty"]]:
            '''Sets the response that Amazon Lex sends to the user when the intent is closed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-intentclosingsetting
            '''
            result = self._values.get("intent_closing_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.IntentClosingSettingProperty"]], result)

        @builtins.property
        def intent_confirmation_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.IntentConfirmationSettingProperty"]]:
            '''Provides prompts that Amazon Lex sends to the user to confirm the completion of an intent.

            If the user answers "no," the settings contain a statement that is sent to the user to end the intent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-intentconfirmationsetting
            '''
            result = self._values.get("intent_confirmation_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.IntentConfirmationSettingProperty"]], result)

        @builtins.property
        def kendra_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.KendraConfigurationProperty"]]:
            '''Provides configuration information for the ``AMAZON.KendraSearchIntent`` intent. When you use this intent, Amazon Lex searches the specified Amazon Kendra index and returns documents from the index that match the user's utterance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-kendraconfiguration
            '''
            result = self._values.get("kendra_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.KendraConfigurationProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the intent.

            Intent names must be unique within the locale that contains the intent and can't match the name of any built-in intent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_contexts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.OutputContextProperty"]]]]:
            '''A list of contexts that the intent activates when it is fulfilled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-outputcontexts
            '''
            result = self._values.get("output_contexts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.OutputContextProperty"]]]], result)

        @builtins.property
        def parent_intent_signature(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for the built-in intent to base this intent on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-parentintentsignature
            '''
            result = self._values.get("parent_intent_signature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def q_in_connect_intent_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.QInConnectIntentConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-qinconnectintentconfiguration
            '''
            result = self._values.get("q_in_connect_intent_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.QInConnectIntentConfigurationProperty"]], result)

        @builtins.property
        def qn_a_intent_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.QnAIntentConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-qnaintentconfiguration
            '''
            result = self._values.get("qn_a_intent_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.QnAIntentConfigurationProperty"]], result)

        @builtins.property
        def sample_utterances(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleUtteranceProperty"]]]]:
            '''A list of utterances that a user might say to signal the intent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-sampleutterances
            '''
            result = self._values.get("sample_utterances")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleUtteranceProperty"]]]], result)

        @builtins.property
        def slot_priorities(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotPriorityProperty"]]]]:
            '''Indicates the priority for slots.

            Amazon Lex prompts the user for slot values in priority order.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-slotpriorities
            '''
            result = self._values.get("slot_priorities")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotPriorityProperty"]]]], result)

        @builtins.property
        def slots(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotProperty"]]]]:
            '''A list of slots that the intent requires for fulfillment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-slots
            '''
            result = self._values.get("slots")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.KendraConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kendra_index": "kendraIndex",
            "query_filter_string": "queryFilterString",
            "query_filter_string_enabled": "queryFilterStringEnabled",
        },
    )
    class KendraConfigurationProperty:
        def __init__(
            self,
            *,
            kendra_index: typing.Optional[builtins.str] = None,
            query_filter_string: typing.Optional[builtins.str] = None,
            query_filter_string_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Provides configuration information for the ``AMAZON.KendraSearchIntent`` intent. When you use this intent, Amazon Lex searches the specified Amazon Kendra index and returns documents from the index that match the user's utterance.

            :param kendra_index: The Amazon Resource Name (ARN) of the Amazon Kendra index that you want the ``AMAZON.KendraSearchIntent`` intent to search. The index must be in the same account and Region as the Amazon Lex bot.
            :param query_filter_string: A query filter that Amazon Lex sends to Amazon Kendra to filter the response from a query. The filter is in the format defined by Amazon Kendra. For more information, see `Filtering queries <https://docs.aws.amazon.com/kendra/latest/dg/filtering.html>`_ .
            :param query_filter_string_enabled: Determines whether the ``AMAZON.KendraSearchIntent`` intent uses a custom query string to query the Amazon Kendra index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                kendra_configuration_property = lex_mixins.CfnBotPropsMixin.KendraConfigurationProperty(
                    kendra_index="kendraIndex",
                    query_filter_string="queryFilterString",
                    query_filter_string_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d05e0e9fe0e724ea0fb853c890ae2b54108a2b759f3d7015b55f620df5446812)
                check_type(argname="argument kendra_index", value=kendra_index, expected_type=type_hints["kendra_index"])
                check_type(argname="argument query_filter_string", value=query_filter_string, expected_type=type_hints["query_filter_string"])
                check_type(argname="argument query_filter_string_enabled", value=query_filter_string_enabled, expected_type=type_hints["query_filter_string_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kendra_index is not None:
                self._values["kendra_index"] = kendra_index
            if query_filter_string is not None:
                self._values["query_filter_string"] = query_filter_string
            if query_filter_string_enabled is not None:
                self._values["query_filter_string_enabled"] = query_filter_string_enabled

        @builtins.property
        def kendra_index(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon Kendra index that you want the ``AMAZON.KendraSearchIntent`` intent to search. The index must be in the same account and Region as the Amazon Lex bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html#cfn-lex-bot-kendraconfiguration-kendraindex
            '''
            result = self._values.get("kendra_index")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query_filter_string(self) -> typing.Optional[builtins.str]:
            '''A query filter that Amazon Lex sends to Amazon Kendra to filter the response from a query.

            The filter is in the format defined by Amazon Kendra. For more information, see `Filtering queries <https://docs.aws.amazon.com/kendra/latest/dg/filtering.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html#cfn-lex-bot-kendraconfiguration-queryfilterstring
            '''
            result = self._values.get("query_filter_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query_filter_string_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the ``AMAZON.KendraSearchIntent`` intent uses a custom query string to query the Amazon Kendra index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html#cfn-lex-bot-kendraconfiguration-queryfilterstringenabled
            '''
            result = self._values.get("query_filter_string_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KendraConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.LambdaCodeHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_hook_interface_version": "codeHookInterfaceVersion",
            "lambda_arn": "lambdaArn",
        },
    )
    class LambdaCodeHookProperty:
        def __init__(
            self,
            *,
            code_hook_interface_version: typing.Optional[builtins.str] = None,
            lambda_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :param code_hook_interface_version: The version of the request-response that you want Amazon Lex to use to invoke your Lambda function.
            :param lambda_arn: The Amazon Resource Name (ARN) of the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-lambdacodehook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                lambda_code_hook_property = lex_mixins.CfnBotPropsMixin.LambdaCodeHookProperty(
                    code_hook_interface_version="codeHookInterfaceVersion",
                    lambda_arn="lambdaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ffe74f5665440436863dffd772c6e38ab14afbc687428c64a84d9d2a46a9bec)
                check_type(argname="argument code_hook_interface_version", value=code_hook_interface_version, expected_type=type_hints["code_hook_interface_version"])
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_hook_interface_version is not None:
                self._values["code_hook_interface_version"] = code_hook_interface_version
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn

        @builtins.property
        def code_hook_interface_version(self) -> typing.Optional[builtins.str]:
            '''The version of the request-response that you want Amazon Lex to use to invoke your Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-lambdacodehook.html#cfn-lex-bot-lambdacodehook-codehookinterfaceversion
            '''
            result = self._values.get("code_hook_interface_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-lambdacodehook.html#cfn-lex-bot-lambdacodehook-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaCodeHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.MessageGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"message": "message", "variations": "variations"},
    )
    class MessageGroupProperty:
        def __init__(
            self,
            *,
            message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            variations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.MessageProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides one or more messages that Amazon Lex should send to the user.

            :param message: The primary message that Amazon Lex should send to the user.
            :param variations: Message variations to send to the user. When variations are defined, Amazon Lex chooses the primary message or one of the variations to send to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-messagegroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                message_group_property = lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                    message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                            value="value"
                        ),
                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                text="text",
                                value="value"
                            )],
                            image_url="imageUrl",
                            subtitle="subtitle",
                            title="title"
                        ),
                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                            value="value"
                        ),
                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                            value="value"
                        )
                    ),
                    variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                            value="value"
                        ),
                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                text="text",
                                value="value"
                            )],
                            image_url="imageUrl",
                            subtitle="subtitle",
                            title="title"
                        ),
                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                            value="value"
                        ),
                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                            value="value"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de68416995a7d0e740c8ce3690b6fe2958503b7a25a60bc302e2fa7fea3e9d6a)
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                check_type(argname="argument variations", value=variations, expected_type=type_hints["variations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message is not None:
                self._values["message"] = message
            if variations is not None:
                self._values["variations"] = variations

        @builtins.property
        def message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageProperty"]]:
            '''The primary message that Amazon Lex should send to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-messagegroup.html#cfn-lex-bot-messagegroup-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageProperty"]], result)

        @builtins.property
        def variations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageProperty"]]]]:
            '''Message variations to send to the user.

            When variations are defined, Amazon Lex chooses the primary message or one of the variations to send to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-messagegroup.html#cfn-lex-bot-messagegroup-variations
            '''
            result = self._values.get("variations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.MessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_payload": "customPayload",
            "image_response_card": "imageResponseCard",
            "plain_text_message": "plainTextMessage",
            "ssml_message": "ssmlMessage",
        },
    )
    class MessageProperty:
        def __init__(
            self,
            *,
            custom_payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.CustomPayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_response_card: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ImageResponseCardProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            plain_text_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.PlainTextMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ssml_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SSMLMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The object that provides message text and its type.

            :param custom_payload: A message in a custom format defined by the client application.
            :param image_response_card: A message that defines a response card that the client application can show to the user.
            :param plain_text_message: A message in plain text format.
            :param ssml_message: A message in Speech Synthesis Markup Language (SSML).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                message_property = lex_mixins.CfnBotPropsMixin.MessageProperty(
                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                        value="value"
                    ),
                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                            text="text",
                            value="value"
                        )],
                        image_url="imageUrl",
                        subtitle="subtitle",
                        title="title"
                    ),
                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                        value="value"
                    ),
                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__91fe24f2614c700234a6670ece931ab046dd65894f3ff64dd619d8110fe3934d)
                check_type(argname="argument custom_payload", value=custom_payload, expected_type=type_hints["custom_payload"])
                check_type(argname="argument image_response_card", value=image_response_card, expected_type=type_hints["image_response_card"])
                check_type(argname="argument plain_text_message", value=plain_text_message, expected_type=type_hints["plain_text_message"])
                check_type(argname="argument ssml_message", value=ssml_message, expected_type=type_hints["ssml_message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_payload is not None:
                self._values["custom_payload"] = custom_payload
            if image_response_card is not None:
                self._values["image_response_card"] = image_response_card
            if plain_text_message is not None:
                self._values["plain_text_message"] = plain_text_message
            if ssml_message is not None:
                self._values["ssml_message"] = ssml_message

        @builtins.property
        def custom_payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CustomPayloadProperty"]]:
            '''A message in a custom format defined by the client application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-custompayload
            '''
            result = self._values.get("custom_payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CustomPayloadProperty"]], result)

        @builtins.property
        def image_response_card(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ImageResponseCardProperty"]]:
            '''A message that defines a response card that the client application can show to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-imageresponsecard
            '''
            result = self._values.get("image_response_card")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ImageResponseCardProperty"]], result)

        @builtins.property
        def plain_text_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PlainTextMessageProperty"]]:
            '''A message in plain text format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-plaintextmessage
            '''
            result = self._values.get("plain_text_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PlainTextMessageProperty"]], result)

        @builtins.property
        def ssml_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SSMLMessageProperty"]]:
            '''A message in Speech Synthesis Markup Language (SSML).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-ssmlmessage
            '''
            result = self._values.get("ssml_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SSMLMessageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.MultipleValuesSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"allow_multiple_values": "allowMultipleValues"},
    )
    class MultipleValuesSettingProperty:
        def __init__(
            self,
            *,
            allow_multiple_values: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Indicates whether a slot can return multiple values.

            :param allow_multiple_values: Indicates whether a slot can return multiple values. When ``true`` , the slot may return more than one value in a response. When ``false`` , the slot returns only a single value. Multi-value slots are only available in the en-US locale. If you set this value to ``true`` in any other locale, Amazon Lex throws a ``ValidationException`` . If the ``allowMutlipleValues`` is not set, the default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-multiplevaluessetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                multiple_values_setting_property = lex_mixins.CfnBotPropsMixin.MultipleValuesSettingProperty(
                    allow_multiple_values=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5acc6b38461fc73a7d2c77daf1f5b9f46dafdd3375ed5d630e24b5fb2dae2567)
                check_type(argname="argument allow_multiple_values", value=allow_multiple_values, expected_type=type_hints["allow_multiple_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_multiple_values is not None:
                self._values["allow_multiple_values"] = allow_multiple_values

        @builtins.property
        def allow_multiple_values(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether a slot can return multiple values.

            When ``true`` , the slot may return more than one value in a response. When ``false`` , the slot returns only a single value.

            Multi-value slots are only available in the en-US locale. If you set this value to ``true`` in any other locale, Amazon Lex throws a ``ValidationException`` .

            If the ``allowMutlipleValues`` is not set, the default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-multiplevaluessetting.html#cfn-lex-bot-multiplevaluessetting-allowmultiplevalues
            '''
            result = self._values.get("allow_multiple_values")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultipleValuesSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.NluImprovementSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class NluImprovementSpecificationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Configures the Assisted Natural Language Understanding (NLU) feature for your bot.

            This specification determines whether enhanced intent recognition and utterance understanding capabilities are active.

            :param enabled: Determines whether the Assisted NLU feature is enabled for the bot. When set to ``true`` , Amazon Lex uses advanced models to improve intent recognition and slot resolution, with the default being ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-nluimprovementspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                nlu_improvement_specification_property = lex_mixins.CfnBotPropsMixin.NluImprovementSpecificationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa0a290ff304e57480e617ce5bdc0d56ce9c8369e1fdc7054e67601e5e6629e0)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the Assisted NLU feature is enabled for the bot.

            When set to ``true`` , Amazon Lex uses advanced models to improve intent recognition and slot resolution, with the default being ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-nluimprovementspecification.html#cfn-lex-bot-nluimprovementspecification-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NluImprovementSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ObfuscationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"obfuscation_setting_type": "obfuscationSettingType"},
    )
    class ObfuscationSettingProperty:
        def __init__(
            self,
            *,
            obfuscation_setting_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Determines whether Amazon Lex obscures slot values in conversation logs.

            :param obfuscation_setting_type: Value that determines whether Amazon Lex obscures slot values in conversation logs. The default is to obscure the values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-obfuscationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                obfuscation_setting_property = lex_mixins.CfnBotPropsMixin.ObfuscationSettingProperty(
                    obfuscation_setting_type="obfuscationSettingType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7a2701e94a821c99267294386b80741167e11044c45cde283804cc4e9575434)
                check_type(argname="argument obfuscation_setting_type", value=obfuscation_setting_type, expected_type=type_hints["obfuscation_setting_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if obfuscation_setting_type is not None:
                self._values["obfuscation_setting_type"] = obfuscation_setting_type

        @builtins.property
        def obfuscation_setting_type(self) -> typing.Optional[builtins.str]:
            '''Value that determines whether Amazon Lex obscures slot values in conversation logs.

            The default is to obscure the values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-obfuscationsetting.html#cfn-lex-bot-obfuscationsetting-obfuscationsettingtype
            '''
            result = self._values.get("obfuscation_setting_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObfuscationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.OpensearchConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_endpoint": "domainEndpoint",
            "exact_response": "exactResponse",
            "exact_response_fields": "exactResponseFields",
            "include_fields": "includeFields",
            "index_name": "indexName",
        },
    )
    class OpensearchConfigurationProperty:
        def __init__(
            self,
            *,
            domain_endpoint: typing.Optional[builtins.str] = None,
            exact_response: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exact_response_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ExactResponseFieldsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            include_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
            index_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains details about the configuration of the Amazon OpenSearch Service database used for the ``AMAZON.QnAIntent`` .

            :param domain_endpoint: The endpoint of the Amazon OpenSearch Service domain.
            :param exact_response: Specifies whether to return an exact response or to return an answer generated by the model using the fields you specify from the database.
            :param exact_response_fields: Contains the names of the fields used for an exact response to the user.
            :param include_fields: Contains a list of fields from the Amazon OpenSearch Service that the model can use to generate the answer to the query.
            :param index_name: The name of the Amazon OpenSearch Service index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-opensearchconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                opensearch_configuration_property = lex_mixins.CfnBotPropsMixin.OpensearchConfigurationProperty(
                    domain_endpoint="domainEndpoint",
                    exact_response=False,
                    exact_response_fields=lex_mixins.CfnBotPropsMixin.ExactResponseFieldsProperty(
                        answer_field="answerField",
                        question_field="questionField"
                    ),
                    include_fields=["includeFields"],
                    index_name="indexName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00d102228d13838a4d5c96d8d75b0854c295f8e72778e50de2cf8c471c492f36)
                check_type(argname="argument domain_endpoint", value=domain_endpoint, expected_type=type_hints["domain_endpoint"])
                check_type(argname="argument exact_response", value=exact_response, expected_type=type_hints["exact_response"])
                check_type(argname="argument exact_response_fields", value=exact_response_fields, expected_type=type_hints["exact_response_fields"])
                check_type(argname="argument include_fields", value=include_fields, expected_type=type_hints["include_fields"])
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_endpoint is not None:
                self._values["domain_endpoint"] = domain_endpoint
            if exact_response is not None:
                self._values["exact_response"] = exact_response
            if exact_response_fields is not None:
                self._values["exact_response_fields"] = exact_response_fields
            if include_fields is not None:
                self._values["include_fields"] = include_fields
            if index_name is not None:
                self._values["index_name"] = index_name

        @builtins.property
        def domain_endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint of the Amazon OpenSearch Service domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-opensearchconfiguration.html#cfn-lex-bot-opensearchconfiguration-domainendpoint
            '''
            result = self._values.get("domain_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exact_response(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to return an exact response or to return an answer generated by the model using the fields you specify from the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-opensearchconfiguration.html#cfn-lex-bot-opensearchconfiguration-exactresponse
            '''
            result = self._values.get("exact_response")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exact_response_fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ExactResponseFieldsProperty"]]:
            '''Contains the names of the fields used for an exact response to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-opensearchconfiguration.html#cfn-lex-bot-opensearchconfiguration-exactresponsefields
            '''
            result = self._values.get("exact_response_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ExactResponseFieldsProperty"]], result)

        @builtins.property
        def include_fields(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Contains a list of fields from the Amazon OpenSearch Service that the model can use to generate the answer to the query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-opensearchconfiguration.html#cfn-lex-bot-opensearchconfiguration-includefields
            '''
            result = self._values.get("include_fields")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def index_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon OpenSearch Service index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-opensearchconfiguration.html#cfn-lex-bot-opensearchconfiguration-indexname
            '''
            result = self._values.get("index_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpensearchConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.OutputContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "time_to_live_in_seconds": "timeToLiveInSeconds",
            "turns_to_live": "turnsToLive",
        },
    )
    class OutputContextProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            time_to_live_in_seconds: typing.Optional[jsii.Number] = None,
            turns_to_live: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes a session context that is activated when an intent is fulfilled.

            :param name: The name of the output context.
            :param time_to_live_in_seconds: The amount of time, in seconds, that the output context should remain active. The time is figured from the first time the context is sent to the user.
            :param turns_to_live: The number of conversation turns that the output context should remain active. The number of turns is counted from the first time that the context is sent to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                output_context_property = lex_mixins.CfnBotPropsMixin.OutputContextProperty(
                    name="name",
                    time_to_live_in_seconds=123,
                    turns_to_live=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1472a4f210d1fd3a23b6ae4fb7ce09dc84a4ca997f5ae72563562a35d8cf2901)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument time_to_live_in_seconds", value=time_to_live_in_seconds, expected_type=type_hints["time_to_live_in_seconds"])
                check_type(argname="argument turns_to_live", value=turns_to_live, expected_type=type_hints["turns_to_live"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if time_to_live_in_seconds is not None:
                self._values["time_to_live_in_seconds"] = time_to_live_in_seconds
            if turns_to_live is not None:
                self._values["turns_to_live"] = turns_to_live

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the output context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html#cfn-lex-bot-outputcontext-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_to_live_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, that the output context should remain active.

            The time is figured from the first time the context is sent to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html#cfn-lex-bot-outputcontext-timetoliveinseconds
            '''
            result = self._values.get("time_to_live_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def turns_to_live(self) -> typing.Optional[jsii.Number]:
            '''The number of conversation turns that the output context should remain active.

            The number of turns is counted from the first time that the context is sent to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html#cfn-lex-bot-outputcontext-turnstolive
            '''
            result = self._values.get("turns_to_live")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.PlainTextMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class PlainTextMessageProperty:
        def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
            '''Defines an ASCII text message to send to the user.

            :param value: The message to send to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-plaintextmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                plain_text_message_property = lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__565a99939706792555eafc800aec33f6bc83523e7aa8455df3cb3a957ce6b077)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The message to send to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-plaintextmessage.html#cfn-lex-bot-plaintextmessage-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlainTextMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.PostDialogCodeHookInvocationSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failure_conditional": "failureConditional",
            "failure_next_step": "failureNextStep",
            "failure_response": "failureResponse",
            "success_conditional": "successConditional",
            "success_next_step": "successNextStep",
            "success_response": "successResponse",
            "timeout_conditional": "timeoutConditional",
            "timeout_next_step": "timeoutNextStep",
            "timeout_response": "timeoutResponse",
        },
    )
    class PostDialogCodeHookInvocationSpecificationProperty:
        def __init__(
            self,
            *,
            failure_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            success_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            success_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            success_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies next steps to run after the dialog code hook finishes.

            :param failure_conditional: A list of conditional branches to evaluate after the dialog code hook throws an exception or returns with the ``State`` field of the ``Intent`` object set to ``Failed`` .
            :param failure_next_step: Specifies the next step the bot runs after the dialog code hook throws an exception or returns with the ``State`` field of the ``Intent`` object set to ``Failed`` .
            :param failure_response: Specifies a list of message groups that Amazon Lex uses to respond the user input when the code hook fails.
            :param success_conditional: A list of conditional branches to evaluate after the dialog code hook finishes successfully.
            :param success_next_step: Specifics the next step the bot runs after the dialog code hook finishes successfully.
            :param success_response: Specifies a list of message groups that Amazon Lex uses to respond when the code hook succeeds.
            :param timeout_conditional: A list of conditional branches to evaluate if the code hook times out.
            :param timeout_next_step: Specifies the next step that the bot runs when the code hook times out.
            :param timeout_response: Specifies a list of message groups that Amazon Lex uses to respond to the user input when the code hook times out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postdialogcodehookinvocationspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b899d468c4e74ddecfc34fc28da9adbf20a8c8ab833838e59db6877ed130ed2)
                check_type(argname="argument failure_conditional", value=failure_conditional, expected_type=type_hints["failure_conditional"])
                check_type(argname="argument failure_next_step", value=failure_next_step, expected_type=type_hints["failure_next_step"])
                check_type(argname="argument failure_response", value=failure_response, expected_type=type_hints["failure_response"])
                check_type(argname="argument success_conditional", value=success_conditional, expected_type=type_hints["success_conditional"])
                check_type(argname="argument success_next_step", value=success_next_step, expected_type=type_hints["success_next_step"])
                check_type(argname="argument success_response", value=success_response, expected_type=type_hints["success_response"])
                check_type(argname="argument timeout_conditional", value=timeout_conditional, expected_type=type_hints["timeout_conditional"])
                check_type(argname="argument timeout_next_step", value=timeout_next_step, expected_type=type_hints["timeout_next_step"])
                check_type(argname="argument timeout_response", value=timeout_response, expected_type=type_hints["timeout_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failure_conditional is not None:
                self._values["failure_conditional"] = failure_conditional
            if failure_next_step is not None:
                self._values["failure_next_step"] = failure_next_step
            if failure_response is not None:
                self._values["failure_response"] = failure_response
            if success_conditional is not None:
                self._values["success_conditional"] = success_conditional
            if success_next_step is not None:
                self._values["success_next_step"] = success_next_step
            if success_response is not None:
                self._values["success_response"] = success_response
            if timeout_conditional is not None:
                self._values["timeout_conditional"] = timeout_conditional
            if timeout_next_step is not None:
                self._values["timeout_next_step"] = timeout_next_step
            if timeout_response is not None:
                self._values["timeout_response"] = timeout_response

        @builtins.property
        def failure_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches to evaluate after the dialog code hook throws an exception or returns with the ``State`` field of the ``Intent`` object set to ``Failed`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postdialogcodehookinvocationspecification.html#cfn-lex-bot-postdialogcodehookinvocationspecification-failureconditional
            '''
            result = self._values.get("failure_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def failure_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifies the next step the bot runs after the dialog code hook throws an exception or returns with the ``State`` field of the ``Intent`` object set to ``Failed`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postdialogcodehookinvocationspecification.html#cfn-lex-bot-postdialogcodehookinvocationspecification-failurenextstep
            '''
            result = self._values.get("failure_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def failure_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond the user input when the code hook fails.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postdialogcodehookinvocationspecification.html#cfn-lex-bot-postdialogcodehookinvocationspecification-failureresponse
            '''
            result = self._values.get("failure_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def success_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches to evaluate after the dialog code hook finishes successfully.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postdialogcodehookinvocationspecification.html#cfn-lex-bot-postdialogcodehookinvocationspecification-successconditional
            '''
            result = self._values.get("success_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def success_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifics the next step the bot runs after the dialog code hook finishes successfully.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postdialogcodehookinvocationspecification.html#cfn-lex-bot-postdialogcodehookinvocationspecification-successnextstep
            '''
            result = self._values.get("success_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def success_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond when the code hook succeeds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postdialogcodehookinvocationspecification.html#cfn-lex-bot-postdialogcodehookinvocationspecification-successresponse
            '''
            result = self._values.get("success_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def timeout_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches to evaluate if the code hook times out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postdialogcodehookinvocationspecification.html#cfn-lex-bot-postdialogcodehookinvocationspecification-timeoutconditional
            '''
            result = self._values.get("timeout_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def timeout_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifies the next step that the bot runs when the code hook times out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postdialogcodehookinvocationspecification.html#cfn-lex-bot-postdialogcodehookinvocationspecification-timeoutnextstep
            '''
            result = self._values.get("timeout_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def timeout_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond to the user input when the code hook times out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postdialogcodehookinvocationspecification.html#cfn-lex-bot-postdialogcodehookinvocationspecification-timeoutresponse
            '''
            result = self._values.get("timeout_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PostDialogCodeHookInvocationSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.PostFulfillmentStatusSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failure_conditional": "failureConditional",
            "failure_next_step": "failureNextStep",
            "failure_response": "failureResponse",
            "success_conditional": "successConditional",
            "success_next_step": "successNextStep",
            "success_response": "successResponse",
            "timeout_conditional": "timeoutConditional",
            "timeout_next_step": "timeoutNextStep",
            "timeout_response": "timeoutResponse",
        },
    )
    class PostFulfillmentStatusSpecificationProperty:
        def __init__(
            self,
            *,
            failure_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            success_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            success_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            success_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides a setting that determines whether the post-fulfillment response is sent to the user.

            For more information, see ` <https://docs.aws.amazon.com/lexv2/latest/dg/streaming-progress.html#progress-complete>`_

            :param failure_conditional: A list of conditional branches to evaluate after the fulfillment code hook throws an exception or returns with the ``State`` field of the ``Intent`` object set to ``Failed`` .
            :param failure_next_step: Specifies the next step the bot runs after the fulfillment code hook throws an exception or returns with the ``State`` field of the ``Intent`` object set to ``Failed`` .
            :param failure_response: Specifies a list of message groups that Amazon Lex uses to respond when fulfillment isn't successful.
            :param success_conditional: A list of conditional branches to evaluate after the fulfillment code hook finishes successfully.
            :param success_next_step: Specifies the next step in the conversation that Amazon Lex invokes when the fulfillment code hook completes successfully.
            :param success_response: Specifies a list of message groups that Amazon Lex uses to respond when the fulfillment is successful.
            :param timeout_conditional: A list of conditional branches to evaluate if the fulfillment code hook times out.
            :param timeout_next_step: Specifies the next step that the bot runs when the fulfillment code hook times out.
            :param timeout_response: Specifies a list of message groups that Amazon Lex uses to respond when fulfillment isn't completed within the timeout period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e8de61f97f2842db249bc935e31e7940895ffbb6c30f775f83aeb11496efebc)
                check_type(argname="argument failure_conditional", value=failure_conditional, expected_type=type_hints["failure_conditional"])
                check_type(argname="argument failure_next_step", value=failure_next_step, expected_type=type_hints["failure_next_step"])
                check_type(argname="argument failure_response", value=failure_response, expected_type=type_hints["failure_response"])
                check_type(argname="argument success_conditional", value=success_conditional, expected_type=type_hints["success_conditional"])
                check_type(argname="argument success_next_step", value=success_next_step, expected_type=type_hints["success_next_step"])
                check_type(argname="argument success_response", value=success_response, expected_type=type_hints["success_response"])
                check_type(argname="argument timeout_conditional", value=timeout_conditional, expected_type=type_hints["timeout_conditional"])
                check_type(argname="argument timeout_next_step", value=timeout_next_step, expected_type=type_hints["timeout_next_step"])
                check_type(argname="argument timeout_response", value=timeout_response, expected_type=type_hints["timeout_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failure_conditional is not None:
                self._values["failure_conditional"] = failure_conditional
            if failure_next_step is not None:
                self._values["failure_next_step"] = failure_next_step
            if failure_response is not None:
                self._values["failure_response"] = failure_response
            if success_conditional is not None:
                self._values["success_conditional"] = success_conditional
            if success_next_step is not None:
                self._values["success_next_step"] = success_next_step
            if success_response is not None:
                self._values["success_response"] = success_response
            if timeout_conditional is not None:
                self._values["timeout_conditional"] = timeout_conditional
            if timeout_next_step is not None:
                self._values["timeout_next_step"] = timeout_next_step
            if timeout_response is not None:
                self._values["timeout_response"] = timeout_response

        @builtins.property
        def failure_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches to evaluate after the fulfillment code hook throws an exception or returns with the ``State`` field of the ``Intent`` object set to ``Failed`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-failureconditional
            '''
            result = self._values.get("failure_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def failure_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifies the next step the bot runs after the fulfillment code hook throws an exception or returns with the ``State`` field of the ``Intent`` object set to ``Failed`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-failurenextstep
            '''
            result = self._values.get("failure_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def failure_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond when fulfillment isn't successful.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-failureresponse
            '''
            result = self._values.get("failure_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def success_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches to evaluate after the fulfillment code hook finishes successfully.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-successconditional
            '''
            result = self._values.get("success_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def success_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifies the next step in the conversation that Amazon Lex invokes when the fulfillment code hook completes successfully.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-successnextstep
            '''
            result = self._values.get("success_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def success_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond when the fulfillment is successful.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-successresponse
            '''
            result = self._values.get("success_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def timeout_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches to evaluate if the fulfillment code hook times out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-timeoutconditional
            '''
            result = self._values.get("timeout_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def timeout_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifies the next step that the bot runs when the fulfillment code hook times out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-timeoutnextstep
            '''
            result = self._values.get("timeout_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def timeout_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond when fulfillment isn't completed within the timeout period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-timeoutresponse
            '''
            result = self._values.get("timeout_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PostFulfillmentStatusSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.PromptAttemptSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_input_types": "allowedInputTypes",
            "allow_interrupt": "allowInterrupt",
            "audio_and_dtmf_input_specification": "audioAndDtmfInputSpecification",
            "text_input_specification": "textInputSpecification",
        },
    )
    class PromptAttemptSpecificationProperty:
        def __init__(
            self,
            *,
            allowed_input_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.AllowedInputTypesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            audio_and_dtmf_input_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            text_input_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.TextInputSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the settings on a prompt attempt.

            :param allowed_input_types: Indicates the allowed input types of the prompt attempt.
            :param allow_interrupt: Indicates whether the user can interrupt a speech prompt attempt from the bot.
            :param audio_and_dtmf_input_specification: Specifies the settings on audio and DTMF input.
            :param text_input_specification: Specifies the settings on text input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptattemptspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                prompt_attempt_specification_property = lex_mixins.CfnBotPropsMixin.PromptAttemptSpecificationProperty(
                    allowed_input_types=lex_mixins.CfnBotPropsMixin.AllowedInputTypesProperty(
                        allow_audio_input=False,
                        allow_dtmf_input=False
                    ),
                    allow_interrupt=False,
                    audio_and_dtmf_input_specification=lex_mixins.CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty(
                        audio_specification=lex_mixins.CfnBotPropsMixin.AudioSpecificationProperty(
                            end_timeout_ms=123,
                            max_length_ms=123
                        ),
                        dtmf_specification=lex_mixins.CfnBotPropsMixin.DTMFSpecificationProperty(
                            deletion_character="deletionCharacter",
                            end_character="endCharacter",
                            end_timeout_ms=123,
                            max_length=123
                        ),
                        start_timeout_ms=123
                    ),
                    text_input_specification=lex_mixins.CfnBotPropsMixin.TextInputSpecificationProperty(
                        start_timeout_ms=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eedf16d9621b254ffb918447b2ad27a935b9c03d13f6f064006aa8eb3dc97ba2)
                check_type(argname="argument allowed_input_types", value=allowed_input_types, expected_type=type_hints["allowed_input_types"])
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
                check_type(argname="argument audio_and_dtmf_input_specification", value=audio_and_dtmf_input_specification, expected_type=type_hints["audio_and_dtmf_input_specification"])
                check_type(argname="argument text_input_specification", value=text_input_specification, expected_type=type_hints["text_input_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_input_types is not None:
                self._values["allowed_input_types"] = allowed_input_types
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt
            if audio_and_dtmf_input_specification is not None:
                self._values["audio_and_dtmf_input_specification"] = audio_and_dtmf_input_specification
            if text_input_specification is not None:
                self._values["text_input_specification"] = text_input_specification

        @builtins.property
        def allowed_input_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AllowedInputTypesProperty"]]:
            '''Indicates the allowed input types of the prompt attempt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptattemptspecification.html#cfn-lex-bot-promptattemptspecification-allowedinputtypes
            '''
            result = self._values.get("allowed_input_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AllowedInputTypesProperty"]], result)

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the user can interrupt a speech prompt attempt from the bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptattemptspecification.html#cfn-lex-bot-promptattemptspecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def audio_and_dtmf_input_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty"]]:
            '''Specifies the settings on audio and DTMF input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptattemptspecification.html#cfn-lex-bot-promptattemptspecification-audioanddtmfinputspecification
            '''
            result = self._values.get("audio_and_dtmf_input_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty"]], result)

        @builtins.property
        def text_input_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.TextInputSpecificationProperty"]]:
            '''Specifies the settings on text input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptattemptspecification.html#cfn-lex-bot-promptattemptspecification-textinputspecification
            '''
            result = self._values.get("text_input_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.TextInputSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PromptAttemptSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.PromptSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_interrupt": "allowInterrupt",
            "max_retries": "maxRetries",
            "message_groups_list": "messageGroupsList",
            "message_selection_strategy": "messageSelectionStrategy",
            "prompt_attempts_specification": "promptAttemptsSpecification",
        },
    )
    class PromptSpecificationProperty:
        def __init__(
            self,
            *,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_retries: typing.Optional[jsii.Number] = None,
            message_groups_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.MessageGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            message_selection_strategy: typing.Optional[builtins.str] = None,
            prompt_attempts_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.PromptAttemptSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies a list of message groups that Amazon Lex sends to a user to elicit a response.

            :param allow_interrupt: Indicates whether the user can interrupt a speech prompt from the bot.
            :param max_retries: The maximum number of times the bot tries to elicit a response from the user using this prompt.
            :param message_groups_list: A collection of messages that Amazon Lex can send to the user. Amazon Lex chooses the actual message to send at runtime.
            :param message_selection_strategy: Indicates how a message is selected from a message group among retries.
            :param prompt_attempts_specification: Specifies the advanced settings on each attempt of the prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                prompt_specification_property = lex_mixins.CfnBotPropsMixin.PromptSpecificationProperty(
                    allow_interrupt=False,
                    max_retries=123,
                    message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                        message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle",
                                title="title"
                            ),
                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                        variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle",
                                title="title"
                            ),
                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                    message_selection_strategy="messageSelectionStrategy",
                    prompt_attempts_specification={
                        "prompt_attempts_specification_key": lex_mixins.CfnBotPropsMixin.PromptAttemptSpecificationProperty(
                            allowed_input_types=lex_mixins.CfnBotPropsMixin.AllowedInputTypesProperty(
                                allow_audio_input=False,
                                allow_dtmf_input=False
                            ),
                            allow_interrupt=False,
                            audio_and_dtmf_input_specification=lex_mixins.CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty(
                                audio_specification=lex_mixins.CfnBotPropsMixin.AudioSpecificationProperty(
                                    end_timeout_ms=123,
                                    max_length_ms=123
                                ),
                                dtmf_specification=lex_mixins.CfnBotPropsMixin.DTMFSpecificationProperty(
                                    deletion_character="deletionCharacter",
                                    end_character="endCharacter",
                                    end_timeout_ms=123,
                                    max_length=123
                                ),
                                start_timeout_ms=123
                            ),
                            text_input_specification=lex_mixins.CfnBotPropsMixin.TextInputSpecificationProperty(
                                start_timeout_ms=123
                            )
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6afc681c475db307a7aca6ac5bbd72e1f5cc036e5ef3c9e868a9ccda1eade736)
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
                check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
                check_type(argname="argument message_groups_list", value=message_groups_list, expected_type=type_hints["message_groups_list"])
                check_type(argname="argument message_selection_strategy", value=message_selection_strategy, expected_type=type_hints["message_selection_strategy"])
                check_type(argname="argument prompt_attempts_specification", value=prompt_attempts_specification, expected_type=type_hints["prompt_attempts_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt
            if max_retries is not None:
                self._values["max_retries"] = max_retries
            if message_groups_list is not None:
                self._values["message_groups_list"] = message_groups_list
            if message_selection_strategy is not None:
                self._values["message_selection_strategy"] = message_selection_strategy
            if prompt_attempts_specification is not None:
                self._values["prompt_attempts_specification"] = prompt_attempts_specification

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the user can interrupt a speech prompt from the bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_retries(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of times the bot tries to elicit a response from the user using this prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-maxretries
            '''
            result = self._values.get("max_retries")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def message_groups_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageGroupProperty"]]]]:
            '''A collection of messages that Amazon Lex can send to the user.

            Amazon Lex chooses the actual message to send at runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-messagegroupslist
            '''
            result = self._values.get("message_groups_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageGroupProperty"]]]], result)

        @builtins.property
        def message_selection_strategy(self) -> typing.Optional[builtins.str]:
            '''Indicates how a message is selected from a message group among retries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-messageselectionstrategy
            '''
            result = self._values.get("message_selection_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prompt_attempts_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PromptAttemptSpecificationProperty"]]]]:
            '''Specifies the advanced settings on each attempt of the prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-promptattemptsspecification
            '''
            result = self._values.get("prompt_attempts_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PromptAttemptSpecificationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PromptSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.QInConnectAssistantConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"assistant_arn": "assistantArn"},
    )
    class QInConnectAssistantConfigurationProperty:
        def __init__(
            self,
            *,
            assistant_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param assistant_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qinconnectassistantconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                q_in_connect_assistant_configuration_property = lex_mixins.CfnBotPropsMixin.QInConnectAssistantConfigurationProperty(
                    assistant_arn="assistantArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49845c06facfd91dcd9619e8f0098989e82acff4ce64800a8d66c6d70800ad33)
                check_type(argname="argument assistant_arn", value=assistant_arn, expected_type=type_hints["assistant_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if assistant_arn is not None:
                self._values["assistant_arn"] = assistant_arn

        @builtins.property
        def assistant_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qinconnectassistantconfiguration.html#cfn-lex-bot-qinconnectassistantconfiguration-assistantarn
            '''
            result = self._values.get("assistant_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QInConnectAssistantConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.QInConnectIntentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "q_in_connect_assistant_configuration": "qInConnectAssistantConfiguration",
        },
    )
    class QInConnectIntentConfigurationProperty:
        def __init__(
            self,
            *,
            q_in_connect_assistant_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.QInConnectAssistantConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param q_in_connect_assistant_configuration: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qinconnectintentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                q_in_connect_intent_configuration_property = lex_mixins.CfnBotPropsMixin.QInConnectIntentConfigurationProperty(
                    q_in_connect_assistant_configuration=lex_mixins.CfnBotPropsMixin.QInConnectAssistantConfigurationProperty(
                        assistant_arn="assistantArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b25fe7a36e5d801900608655a42bb93883ddced423648863848b5491a4ebea7)
                check_type(argname="argument q_in_connect_assistant_configuration", value=q_in_connect_assistant_configuration, expected_type=type_hints["q_in_connect_assistant_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if q_in_connect_assistant_configuration is not None:
                self._values["q_in_connect_assistant_configuration"] = q_in_connect_assistant_configuration

        @builtins.property
        def q_in_connect_assistant_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.QInConnectAssistantConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qinconnectintentconfiguration.html#cfn-lex-bot-qinconnectintentconfiguration-qinconnectassistantconfiguration
            '''
            result = self._values.get("q_in_connect_assistant_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.QInConnectAssistantConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QInConnectIntentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.QnAIntentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_model_configuration": "bedrockModelConfiguration",
            "data_source_configuration": "dataSourceConfiguration",
        },
    )
    class QnAIntentConfigurationProperty:
        def __init__(
            self,
            *,
            bedrock_model_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BedrockModelSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            data_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DataSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Details about the the configuration of the built-in ``Amazon.QnAIntent`` .

            :param bedrock_model_configuration: 
            :param data_source_configuration: Contains details about the configuration of the data source used for the ``AMAZON.QnAIntent`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qnaintentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                qn_aIntent_configuration_property = lex_mixins.CfnBotPropsMixin.QnAIntentConfigurationProperty(
                    bedrock_model_configuration=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                        bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                            bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                            bedrock_guardrail_version="bedrockGuardrailVersion"
                        ),
                        bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                        bedrock_trace_status="bedrockTraceStatus",
                        model_arn="modelArn"
                    ),
                    data_source_configuration=lex_mixins.CfnBotPropsMixin.DataSourceConfigurationProperty(
                        bedrock_knowledge_store_configuration=lex_mixins.CfnBotPropsMixin.BedrockKnowledgeStoreConfigurationProperty(
                            bedrock_knowledge_base_arn="bedrockKnowledgeBaseArn",
                            bkb_exact_response_fields=lex_mixins.CfnBotPropsMixin.BKBExactResponseFieldsProperty(
                                answer_field="answerField"
                            ),
                            exact_response=False
                        ),
                        kendra_configuration=lex_mixins.CfnBotPropsMixin.QnAKendraConfigurationProperty(
                            exact_response=False,
                            kendra_index="kendraIndex",
                            query_filter_string="queryFilterString",
                            query_filter_string_enabled=False
                        ),
                        opensearch_configuration=lex_mixins.CfnBotPropsMixin.OpensearchConfigurationProperty(
                            domain_endpoint="domainEndpoint",
                            exact_response=False,
                            exact_response_fields=lex_mixins.CfnBotPropsMixin.ExactResponseFieldsProperty(
                                answer_field="answerField",
                                question_field="questionField"
                            ),
                            include_fields=["includeFields"],
                            index_name="indexName"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__140ec5fc6ebeef41ead0e6508639e5a1be82ca1471324e65a04493dbc49336b1)
                check_type(argname="argument bedrock_model_configuration", value=bedrock_model_configuration, expected_type=type_hints["bedrock_model_configuration"])
                check_type(argname="argument data_source_configuration", value=data_source_configuration, expected_type=type_hints["data_source_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_model_configuration is not None:
                self._values["bedrock_model_configuration"] = bedrock_model_configuration
            if data_source_configuration is not None:
                self._values["data_source_configuration"] = data_source_configuration

        @builtins.property
        def bedrock_model_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockModelSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qnaintentconfiguration.html#cfn-lex-bot-qnaintentconfiguration-bedrockmodelconfiguration
            '''
            result = self._values.get("bedrock_model_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockModelSpecificationProperty"]], result)

        @builtins.property
        def data_source_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DataSourceConfigurationProperty"]]:
            '''Contains details about the configuration of the data source used for the ``AMAZON.QnAIntent`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qnaintentconfiguration.html#cfn-lex-bot-qnaintentconfiguration-datasourceconfiguration
            '''
            result = self._values.get("data_source_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DataSourceConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QnAIntentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.QnAKendraConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exact_response": "exactResponse",
            "kendra_index": "kendraIndex",
            "query_filter_string": "queryFilterString",
            "query_filter_string_enabled": "queryFilterStringEnabled",
        },
    )
    class QnAKendraConfigurationProperty:
        def __init__(
            self,
            *,
            exact_response: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            kendra_index: typing.Optional[builtins.str] = None,
            query_filter_string: typing.Optional[builtins.str] = None,
            query_filter_string_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains details about the configuration of the Amazon Kendra index used for the ``AMAZON.QnAIntent`` .

            :param exact_response: Specifies whether to return an exact response from the Amazon Kendra index or to let the Amazon Bedrock model you select generate a response based on the results. To use this feature, you must first add FAQ questions to your index by following the steps at `Adding frequently asked questions (FAQs) to an index <https://docs.aws.amazon.com/kendra/latest/dg/in-creating-faq.html>`_ .
            :param kendra_index: The ARN of the Amazon Kendra index to use.
            :param query_filter_string: Contains the Amazon Kendra filter string to use if enabled. For more information on the Amazon Kendra search filter JSON format, see `Using document attributes to filter search results <https://docs.aws.amazon.com/kendra/latest/dg/filtering.html#search-filtering>`_ .
            :param query_filter_string_enabled: Specifies whether to enable an Amazon Kendra filter string or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qnakendraconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                qn_aKendra_configuration_property = lex_mixins.CfnBotPropsMixin.QnAKendraConfigurationProperty(
                    exact_response=False,
                    kendra_index="kendraIndex",
                    query_filter_string="queryFilterString",
                    query_filter_string_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6c02a0061ccbbf87713710ab615384211ad1e09823899eefcb92e7aac4e569e)
                check_type(argname="argument exact_response", value=exact_response, expected_type=type_hints["exact_response"])
                check_type(argname="argument kendra_index", value=kendra_index, expected_type=type_hints["kendra_index"])
                check_type(argname="argument query_filter_string", value=query_filter_string, expected_type=type_hints["query_filter_string"])
                check_type(argname="argument query_filter_string_enabled", value=query_filter_string_enabled, expected_type=type_hints["query_filter_string_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact_response is not None:
                self._values["exact_response"] = exact_response
            if kendra_index is not None:
                self._values["kendra_index"] = kendra_index
            if query_filter_string is not None:
                self._values["query_filter_string"] = query_filter_string
            if query_filter_string_enabled is not None:
                self._values["query_filter_string_enabled"] = query_filter_string_enabled

        @builtins.property
        def exact_response(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to return an exact response from the Amazon Kendra index or to let the Amazon Bedrock model you select generate a response based on the results.

            To use this feature, you must first add FAQ questions to your index by following the steps at `Adding frequently asked questions (FAQs) to an index <https://docs.aws.amazon.com/kendra/latest/dg/in-creating-faq.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qnakendraconfiguration.html#cfn-lex-bot-qnakendraconfiguration-exactresponse
            '''
            result = self._values.get("exact_response")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def kendra_index(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon Kendra index to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qnakendraconfiguration.html#cfn-lex-bot-qnakendraconfiguration-kendraindex
            '''
            result = self._values.get("kendra_index")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query_filter_string(self) -> typing.Optional[builtins.str]:
            '''Contains the Amazon Kendra filter string to use if enabled.

            For more information on the Amazon Kendra search filter JSON format, see `Using document attributes to filter search results <https://docs.aws.amazon.com/kendra/latest/dg/filtering.html#search-filtering>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qnakendraconfiguration.html#cfn-lex-bot-qnakendraconfiguration-queryfilterstring
            '''
            result = self._values.get("query_filter_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query_filter_string_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to enable an Amazon Kendra filter string or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-qnakendraconfiguration.html#cfn-lex-bot-qnakendraconfiguration-queryfilterstringenabled
            '''
            result = self._values.get("query_filter_string_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QnAKendraConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ReplicationProperty",
        jsii_struct_bases=[],
        name_mapping={"replica_regions": "replicaRegions"},
    )
    class ReplicationProperty:
        def __init__(
            self,
            *,
            replica_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param replica_regions: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-replication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                replication_property = lex_mixins.CfnBotPropsMixin.ReplicationProperty(
                    replica_regions=["replicaRegions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dbad0edd82d69d664c704e16caf8a4671e0aa4a89af09b8d557b21164b503c16)
                check_type(argname="argument replica_regions", value=replica_regions, expected_type=type_hints["replica_regions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if replica_regions is not None:
                self._values["replica_regions"] = replica_regions

        @builtins.property
        def replica_regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-replication.html#cfn-lex-bot-replication-replicaregions
            '''
            result = self._values.get("replica_regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.ResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_interrupt": "allowInterrupt",
            "message_groups_list": "messageGroupsList",
        },
    )
    class ResponseSpecificationProperty:
        def __init__(
            self,
            *,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            message_groups_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.MessageGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies a list of message groups that Amazon Lex uses to respond the user input.

            :param allow_interrupt: Indicates whether the user can interrupt a speech response from Amazon Lex.
            :param message_groups_list: A collection of responses that Amazon Lex can send to the user. Amazon Lex chooses the actual response to send at runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-responsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                response_specification_property = lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                    allow_interrupt=False,
                    message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                        message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle",
                                title="title"
                            ),
                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                        variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle",
                                title="title"
                            ),
                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f723381ec94360d7ebb69881c83d19e510b5826884d9d8ce0192c084feb5a577)
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
                check_type(argname="argument message_groups_list", value=message_groups_list, expected_type=type_hints["message_groups_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt
            if message_groups_list is not None:
                self._values["message_groups_list"] = message_groups_list

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the user can interrupt a speech response from Amazon Lex.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-responsespecification.html#cfn-lex-bot-responsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def message_groups_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageGroupProperty"]]]]:
            '''A collection of responses that Amazon Lex can send to the user.

            Amazon Lex chooses the actual response to send at runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-responsespecification.html#cfn-lex-bot-responsespecification-messagegroupslist
            '''
            result = self._values.get("message_groups_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageGroupProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.RuntimeSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "nlu_improvement_specification": "nluImprovementSpecification",
            "slot_resolution_improvement_specification": "slotResolutionImprovementSpecification",
        },
    )
    class RuntimeSettingsProperty:
        def __init__(
            self,
            *,
            nlu_improvement_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.NluImprovementSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            slot_resolution_improvement_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotResolutionImprovementSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains specifications about the Amazon Lex runtime generative AI capabilities from Amazon Bedrock that you can turn on for your bot.

            :param nlu_improvement_specification: 
            :param slot_resolution_improvement_specification: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-runtimesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                runtime_settings_property = lex_mixins.CfnBotPropsMixin.RuntimeSettingsProperty(
                    nlu_improvement_specification=lex_mixins.CfnBotPropsMixin.NluImprovementSpecificationProperty(
                        enabled=False
                    ),
                    slot_resolution_improvement_specification=lex_mixins.CfnBotPropsMixin.SlotResolutionImprovementSpecificationProperty(
                        bedrock_model_specification=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                            bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                                bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                                bedrock_guardrail_version="bedrockGuardrailVersion"
                            ),
                            bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                            bedrock_trace_status="bedrockTraceStatus",
                            model_arn="modelArn"
                        ),
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5567e184a7a4cfcbb80491aef2d02a77bc0847242b295e0d79743fc62b63b1aa)
                check_type(argname="argument nlu_improvement_specification", value=nlu_improvement_specification, expected_type=type_hints["nlu_improvement_specification"])
                check_type(argname="argument slot_resolution_improvement_specification", value=slot_resolution_improvement_specification, expected_type=type_hints["slot_resolution_improvement_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if nlu_improvement_specification is not None:
                self._values["nlu_improvement_specification"] = nlu_improvement_specification
            if slot_resolution_improvement_specification is not None:
                self._values["slot_resolution_improvement_specification"] = slot_resolution_improvement_specification

        @builtins.property
        def nlu_improvement_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.NluImprovementSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-runtimesettings.html#cfn-lex-bot-runtimesettings-nluimprovementspecification
            '''
            result = self._values.get("nlu_improvement_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.NluImprovementSpecificationProperty"]], result)

        @builtins.property
        def slot_resolution_improvement_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotResolutionImprovementSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-runtimesettings.html#cfn-lex-bot-runtimesettings-slotresolutionimprovementspecification
            '''
            result = self._values.get("slot_resolution_improvement_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotResolutionImprovementSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuntimeSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.S3BucketLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_key_arn": "kmsKeyArn",
            "log_prefix": "logPrefix",
            "s3_bucket_arn": "s3BucketArn",
        },
    )
    class S3BucketLogDestinationProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            log_prefix: typing.Optional[builtins.str] = None,
            s3_bucket_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an Amazon S3 bucket for logging audio conversations.

            :param kms_key_arn: The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key for encrypting audio log files stored in an Amazon S3 bucket.
            :param log_prefix: The S3 prefix to assign to audio log files.
            :param s3_bucket_arn: The Amazon Resource Name (ARN) of an Amazon S3 bucket where audio log files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3bucketlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                s3_bucket_log_destination_property = lex_mixins.CfnBotPropsMixin.S3BucketLogDestinationProperty(
                    kms_key_arn="kmsKeyArn",
                    log_prefix="logPrefix",
                    s3_bucket_arn="s3BucketArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__081f84e73f36dfcfe426ced5c283e205a0aeef6c5106884195da17b75c2b7fdf)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument log_prefix", value=log_prefix, expected_type=type_hints["log_prefix"])
                check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if log_prefix is not None:
                self._values["log_prefix"] = log_prefix
            if s3_bucket_arn is not None:
                self._values["s3_bucket_arn"] = s3_bucket_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key for encrypting audio log files stored in an Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3bucketlogdestination.html#cfn-lex-bot-s3bucketlogdestination-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 prefix to assign to audio log files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3bucketlogdestination.html#cfn-lex-bot-s3bucketlogdestination-logprefix
            '''
            result = self._values.get("log_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an Amazon S3 bucket where audio log files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3bucketlogdestination.html#cfn-lex-bot-s3bucketlogdestination-s3bucketarn
            '''
            result = self._values.get("s3_bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket": "s3Bucket",
            "s3_object_key": "s3ObjectKey",
            "s3_object_version": "s3ObjectVersion",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_object_key: typing.Optional[builtins.str] = None,
            s3_object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an Amazon S3 bucket location.

            :param s3_bucket: The S3 bucket name.
            :param s3_object_key: The path and file name to the object in the S3 bucket.
            :param s3_object_version: The version of the object in the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                s3_location_property = lex_mixins.CfnBotPropsMixin.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_object_key="s3ObjectKey",
                    s3_object_version="s3ObjectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__64a328f9a1251122a879b031d2325776910ff106c6668bfe5b0ee69323a29177)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_object_key", value=s3_object_key, expected_type=type_hints["s3_object_key"])
                check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_object_key is not None:
                self._values["s3_object_key"] = s3_object_key
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html#cfn-lex-bot-s3location-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_key(self) -> typing.Optional[builtins.str]:
            '''The path and file name to the object in the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html#cfn-lex-bot-s3location-s3objectkey
            '''
            result = self._values.get("s3_object_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_version(self) -> typing.Optional[builtins.str]:
            '''The version of the object in the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html#cfn-lex-bot-s3location-s3objectversion
            '''
            result = self._values.get("s3_object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SSMLMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class SSMLMessageProperty:
        def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
            '''Defines a Speech Synthesis Markup Language (SSML) prompt.

            :param value: The SSML text that defines the prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-ssmlmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                s_sMLMessage_property = lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3249e67130a741ff514fbd680fa66473665f225585b3a74cd4a708b1f059ac78)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The SSML text that defines the prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-ssmlmessage.html#cfn-lex-bot-ssmlmessage-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSMLMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SampleUtteranceGenerationSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_model_specification": "bedrockModelSpecification",
            "enabled": "enabled",
        },
    )
    class SampleUtteranceGenerationSpecificationProperty:
        def __init__(
            self,
            *,
            bedrock_model_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BedrockModelSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains specifications for the sample utterance generation feature.

            :param bedrock_model_specification: 
            :param enabled: Specifies whether to enable sample utterance generation or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sampleutterancegenerationspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                sample_utterance_generation_specification_property = lex_mixins.CfnBotPropsMixin.SampleUtteranceGenerationSpecificationProperty(
                    bedrock_model_specification=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                        bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                            bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                            bedrock_guardrail_version="bedrockGuardrailVersion"
                        ),
                        bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                        bedrock_trace_status="bedrockTraceStatus",
                        model_arn="modelArn"
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74ce0d0f89b5f51b10f45b5bc5da7b1b9f7503ba4a055c63c92d6be0d0baecc9)
                check_type(argname="argument bedrock_model_specification", value=bedrock_model_specification, expected_type=type_hints["bedrock_model_specification"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_model_specification is not None:
                self._values["bedrock_model_specification"] = bedrock_model_specification
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def bedrock_model_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockModelSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sampleutterancegenerationspecification.html#cfn-lex-bot-sampleutterancegenerationspecification-bedrockmodelspecification
            '''
            result = self._values.get("bedrock_model_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockModelSpecificationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to enable sample utterance generation or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sampleutterancegenerationspecification.html#cfn-lex-bot-sampleutterancegenerationspecification-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SampleUtteranceGenerationSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SampleUtteranceProperty",
        jsii_struct_bases=[],
        name_mapping={"utterance": "utterance"},
    )
    class SampleUtteranceProperty:
        def __init__(self, *, utterance: typing.Optional[builtins.str] = None) -> None:
            '''A sample utterance that invokes an intent or respond to a slot elicitation prompt.

            :param utterance: A sample utterance that invokes an intent or respond to a slot elicitation prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sampleutterance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                sample_utterance_property = lex_mixins.CfnBotPropsMixin.SampleUtteranceProperty(
                    utterance="utterance"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5357747a796b2a30aa99351d9fbf3eb5ec78f70141de59d20fbfa4b1db36c440)
                check_type(argname="argument utterance", value=utterance, expected_type=type_hints["utterance"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if utterance is not None:
                self._values["utterance"] = utterance

        @builtins.property
        def utterance(self) -> typing.Optional[builtins.str]:
            '''A sample utterance that invokes an intent or respond to a slot elicitation prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sampleutterance.html#cfn-lex-bot-sampleutterance-utterance
            '''
            result = self._values.get("utterance")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SampleUtteranceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SampleValueProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class SampleValueProperty:
        def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
            '''Defines one of the values for a slot type.

            :param value: The value that can be used for a slot type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-samplevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                sample_value_property = lex_mixins.CfnBotPropsMixin.SampleValueProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__532696af8055940c66022851d1d48e6dcaaa30f80fd56a04e47eddf5e1bbe0f2)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value that can be used for a slot type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-samplevalue.html#cfn-lex-bot-samplevalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SampleValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SessionAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class SessionAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A key/value pair representing session-specific context information.

            It contains application information passed between Amazon Lex V2 and a client application.

            :param key: The name of the session attribute.
            :param value: The session-specific context information for the session attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sessionattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                session_attribute_property = lex_mixins.CfnBotPropsMixin.SessionAttributeProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6312813cc88dda00de88e9b5615a28782a4c6f94e05eb1411bde09c1a0122bfc)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the session attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sessionattribute.html#cfn-lex-bot-sessionattribute-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The session-specific context information for the session attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sessionattribute.html#cfn-lex-bot-sessionattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SessionAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotCaptureSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capture_conditional": "captureConditional",
            "capture_next_step": "captureNextStep",
            "capture_response": "captureResponse",
            "code_hook": "codeHook",
            "elicitation_code_hook": "elicitationCodeHook",
            "failure_conditional": "failureConditional",
            "failure_next_step": "failureNextStep",
            "failure_response": "failureResponse",
        },
    )
    class SlotCaptureSettingProperty:
        def __init__(
            self,
            *,
            capture_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            capture_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            capture_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            elicitation_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ElicitationCodeHookInvocationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConditionalSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.DialogStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings used when Amazon Lex successfully captures a slot value from a user.

            :param capture_conditional: A list of conditional branches to evaluate after the slot value is captured.
            :param capture_next_step: Specifies the next step that the bot runs when the slot value is captured before the code hook times out.
            :param capture_response: Specifies a list of message groups that Amazon Lex uses to respond the user input.
            :param code_hook: Code hook called after Amazon Lex successfully captures a slot value.
            :param elicitation_code_hook: Code hook called when Amazon Lex doesn't capture a slot value.
            :param failure_conditional: A list of conditional branches to evaluate when the slot value isn't captured.
            :param failure_next_step: Specifies the next step that the bot runs when the slot value code is not recognized.
            :param failure_response: Specifies a list of message groups that Amazon Lex uses to respond the user input when the slot fails to be captured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotcapturesetting.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f8a4cb1c7d82e13904e8dc88e9981a9361e456f84266af9072df698d0e6ca55)
                check_type(argname="argument capture_conditional", value=capture_conditional, expected_type=type_hints["capture_conditional"])
                check_type(argname="argument capture_next_step", value=capture_next_step, expected_type=type_hints["capture_next_step"])
                check_type(argname="argument capture_response", value=capture_response, expected_type=type_hints["capture_response"])
                check_type(argname="argument code_hook", value=code_hook, expected_type=type_hints["code_hook"])
                check_type(argname="argument elicitation_code_hook", value=elicitation_code_hook, expected_type=type_hints["elicitation_code_hook"])
                check_type(argname="argument failure_conditional", value=failure_conditional, expected_type=type_hints["failure_conditional"])
                check_type(argname="argument failure_next_step", value=failure_next_step, expected_type=type_hints["failure_next_step"])
                check_type(argname="argument failure_response", value=failure_response, expected_type=type_hints["failure_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capture_conditional is not None:
                self._values["capture_conditional"] = capture_conditional
            if capture_next_step is not None:
                self._values["capture_next_step"] = capture_next_step
            if capture_response is not None:
                self._values["capture_response"] = capture_response
            if code_hook is not None:
                self._values["code_hook"] = code_hook
            if elicitation_code_hook is not None:
                self._values["elicitation_code_hook"] = elicitation_code_hook
            if failure_conditional is not None:
                self._values["failure_conditional"] = failure_conditional
            if failure_next_step is not None:
                self._values["failure_next_step"] = failure_next_step
            if failure_response is not None:
                self._values["failure_response"] = failure_response

        @builtins.property
        def capture_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches to evaluate after the slot value is captured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotcapturesetting.html#cfn-lex-bot-slotcapturesetting-captureconditional
            '''
            result = self._values.get("capture_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def capture_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifies the next step that the bot runs when the slot value is captured before the code hook times out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotcapturesetting.html#cfn-lex-bot-slotcapturesetting-capturenextstep
            '''
            result = self._values.get("capture_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def capture_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond the user input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotcapturesetting.html#cfn-lex-bot-slotcapturesetting-captureresponse
            '''
            result = self._values.get("capture_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty"]]:
            '''Code hook called after Amazon Lex successfully captures a slot value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotcapturesetting.html#cfn-lex-bot-slotcapturesetting-codehook
            '''
            result = self._values.get("code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty"]], result)

        @builtins.property
        def elicitation_code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ElicitationCodeHookInvocationSettingProperty"]]:
            '''Code hook called when Amazon Lex doesn't capture a slot value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotcapturesetting.html#cfn-lex-bot-slotcapturesetting-elicitationcodehook
            '''
            result = self._values.get("elicitation_code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ElicitationCodeHookInvocationSettingProperty"]], result)

        @builtins.property
        def failure_conditional(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]]:
            '''A list of conditional branches to evaluate when the slot value isn't captured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotcapturesetting.html#cfn-lex-bot-slotcapturesetting-failureconditional
            '''
            result = self._values.get("failure_conditional")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConditionalSpecificationProperty"]], result)

        @builtins.property
        def failure_next_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]]:
            '''Specifies the next step that the bot runs when the slot value code is not recognized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotcapturesetting.html#cfn-lex-bot-slotcapturesetting-failurenextstep
            '''
            result = self._values.get("failure_next_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.DialogStateProperty"]], result)

        @builtins.property
        def failure_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond the user input when the slot fails to be captured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotcapturesetting.html#cfn-lex-bot-slotcapturesetting-failureresponse
            '''
            result = self._values.get("failure_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotCaptureSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotDefaultValueProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue"},
    )
    class SlotDefaultValueProperty:
        def __init__(
            self,
            *,
            default_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the default value to use when a user doesn't provide a value for a slot.

            :param default_value: The default value to use when a user doesn't provide a value for a slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                slot_default_value_property = lex_mixins.CfnBotPropsMixin.SlotDefaultValueProperty(
                    default_value="defaultValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b085105fcccddae011aba2804d02726128c64256df2c3ed95253e1a0f8b07073)
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_value is not None:
                self._values["default_value"] = default_value

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value to use when a user doesn't provide a value for a slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvalue.html#cfn-lex-bot-slotdefaultvalue-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotDefaultValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotDefaultValueSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value_list": "defaultValueList"},
    )
    class SlotDefaultValueSpecificationProperty:
        def __init__(
            self,
            *,
            default_value_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotDefaultValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The default value to use when a user doesn't provide a value for a slot.

            :param default_value_list: A list of default values. Amazon Lex chooses the default value to use in the order that they are presented in the list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvaluespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                slot_default_value_specification_property = lex_mixins.CfnBotPropsMixin.SlotDefaultValueSpecificationProperty(
                    default_value_list=[lex_mixins.CfnBotPropsMixin.SlotDefaultValueProperty(
                        default_value="defaultValue"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc5660de403be1bf600d769ee088f82d679ad062280e19dc48f01f0330917874)
                check_type(argname="argument default_value_list", value=default_value_list, expected_type=type_hints["default_value_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_value_list is not None:
                self._values["default_value_list"] = default_value_list

        @builtins.property
        def default_value_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotDefaultValueProperty"]]]]:
            '''A list of default values.

            Amazon Lex chooses the default value to use in the order that they are presented in the list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvaluespecification.html#cfn-lex-bot-slotdefaultvaluespecification-defaultvaluelist
            '''
            result = self._values.get("default_value_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotDefaultValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotDefaultValueSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotPriorityProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "slot_name": "slotName"},
    )
    class SlotPriorityProperty:
        def __init__(
            self,
            *,
            priority: typing.Optional[jsii.Number] = None,
            slot_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sets the priority that Amazon Lex should use when eliciting slot values from a user.

            :param priority: The priority that Amazon Lex should apply to the slot.
            :param slot_name: The name of the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotpriority.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                slot_priority_property = lex_mixins.CfnBotPropsMixin.SlotPriorityProperty(
                    priority=123,
                    slot_name="slotName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd579b2a44a4cfe7b21b3216502a63b58aa84b52e33912d018fa5e2659c40e29)
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument slot_name", value=slot_name, expected_type=type_hints["slot_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if priority is not None:
                self._values["priority"] = priority
            if slot_name is not None:
                self._values["slot_name"] = slot_name

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The priority that Amazon Lex should apply to the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotpriority.html#cfn-lex-bot-slotpriority-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def slot_name(self) -> typing.Optional[builtins.str]:
            '''The name of the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotpriority.html#cfn-lex-bot-slotpriority-slotname
            '''
            result = self._values.get("slot_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotPriorityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "multiple_values_setting": "multipleValuesSetting",
            "name": "name",
            "obfuscation_setting": "obfuscationSetting",
            "slot_type_name": "slotTypeName",
            "sub_slot_setting": "subSlotSetting",
            "value_elicitation_setting": "valueElicitationSetting",
        },
    )
    class SlotProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            multiple_values_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.MultipleValuesSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            obfuscation_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ObfuscationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            slot_type_name: typing.Optional[builtins.str] = None,
            sub_slot_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SubSlotSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            value_elicitation_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotValueElicitationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the definition of a slot.

            Amazon Lex elicits slot values from uses to fulfill the user's intent.

            :param description: The description of the slot.
            :param multiple_values_setting: Indicates whether a slot can return multiple values.
            :param name: The name given to the slot.
            :param obfuscation_setting: Determines whether the contents of the slot are obfuscated in Amazon CloudWatch Logs logs. Use obfuscated slots to protect information such as personally identifiable information (PII) in logs.
            :param slot_type_name: The name of the slot type that this slot is based on. The slot type defines the acceptable values for the slot.
            :param sub_slot_setting: 
            :param value_elicitation_setting: Determines the slot resolution strategy that Amazon Lex uses to return slot type values. The field can be set to one of the following values: - ORIGINAL_VALUE - Returns the value entered by the user, if the user value is similar to a slot value. - TOP_RESOLUTION - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned. If you don't specify the ``valueSelectionStrategy`` , the default is ``ORIGINAL_VALUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd7a483dc93bb09e61b7e9ffdc58c77a946534e34e6d03f3e95bc339cfb8b979)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument multiple_values_setting", value=multiple_values_setting, expected_type=type_hints["multiple_values_setting"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument obfuscation_setting", value=obfuscation_setting, expected_type=type_hints["obfuscation_setting"])
                check_type(argname="argument slot_type_name", value=slot_type_name, expected_type=type_hints["slot_type_name"])
                check_type(argname="argument sub_slot_setting", value=sub_slot_setting, expected_type=type_hints["sub_slot_setting"])
                check_type(argname="argument value_elicitation_setting", value=value_elicitation_setting, expected_type=type_hints["value_elicitation_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if multiple_values_setting is not None:
                self._values["multiple_values_setting"] = multiple_values_setting
            if name is not None:
                self._values["name"] = name
            if obfuscation_setting is not None:
                self._values["obfuscation_setting"] = obfuscation_setting
            if slot_type_name is not None:
                self._values["slot_type_name"] = slot_type_name
            if sub_slot_setting is not None:
                self._values["sub_slot_setting"] = sub_slot_setting
            if value_elicitation_setting is not None:
                self._values["value_elicitation_setting"] = value_elicitation_setting

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multiple_values_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MultipleValuesSettingProperty"]]:
            '''Indicates whether a slot can return multiple values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-multiplevaluessetting
            '''
            result = self._values.get("multiple_values_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MultipleValuesSettingProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name given to the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def obfuscation_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ObfuscationSettingProperty"]]:
            '''Determines whether the contents of the slot are obfuscated in Amazon CloudWatch Logs logs.

            Use obfuscated slots to protect information such as personally identifiable information (PII) in logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-obfuscationsetting
            '''
            result = self._values.get("obfuscation_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ObfuscationSettingProperty"]], result)

        @builtins.property
        def slot_type_name(self) -> typing.Optional[builtins.str]:
            '''The name of the slot type that this slot is based on.

            The slot type defines the acceptable values for the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-slottypename
            '''
            result = self._values.get("slot_type_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sub_slot_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SubSlotSettingProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-subslotsetting
            '''
            result = self._values.get("sub_slot_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SubSlotSettingProperty"]], result)

        @builtins.property
        def value_elicitation_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueElicitationSettingProperty"]]:
            '''Determines the slot resolution strategy that Amazon Lex uses to return slot type values.

            The field can be set to one of the following values:

            - ORIGINAL_VALUE - Returns the value entered by the user, if the user value is similar to a slot value.
            - TOP_RESOLUTION - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned.

            If you don't specify the ``valueSelectionStrategy`` , the default is ``ORIGINAL_VALUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-valueelicitationsetting
            '''
            result = self._values.get("value_elicitation_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueElicitationSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotResolutionImprovementSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_model_specification": "bedrockModelSpecification",
            "enabled": "enabled",
        },
    )
    class SlotResolutionImprovementSpecificationProperty:
        def __init__(
            self,
            *,
            bedrock_model_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BedrockModelSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains specifications for the assisted slot resolution feature.

            :param bedrock_model_specification: An object containing information about the Amazon Bedrock model used to assist slot resolution.
            :param enabled: Specifies whether assisted slot resolution is turned on or off.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotresolutionimprovementspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                slot_resolution_improvement_specification_property = lex_mixins.CfnBotPropsMixin.SlotResolutionImprovementSpecificationProperty(
                    bedrock_model_specification=lex_mixins.CfnBotPropsMixin.BedrockModelSpecificationProperty(
                        bedrock_guardrail_configuration=lex_mixins.CfnBotPropsMixin.BedrockGuardrailConfigurationProperty(
                            bedrock_guardrail_identifier="bedrockGuardrailIdentifier",
                            bedrock_guardrail_version="bedrockGuardrailVersion"
                        ),
                        bedrock_model_custom_prompt="bedrockModelCustomPrompt",
                        bedrock_trace_status="bedrockTraceStatus",
                        model_arn="modelArn"
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f08c68b5de0020252e2289b3102723c4fc1641e18f3b3d6e382d94a597078410)
                check_type(argname="argument bedrock_model_specification", value=bedrock_model_specification, expected_type=type_hints["bedrock_model_specification"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_model_specification is not None:
                self._values["bedrock_model_specification"] = bedrock_model_specification
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def bedrock_model_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockModelSpecificationProperty"]]:
            '''An object containing information about the Amazon Bedrock model used to assist slot resolution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotresolutionimprovementspecification.html#cfn-lex-bot-slotresolutionimprovementspecification-bedrockmodelspecification
            '''
            result = self._values.get("bedrock_model_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BedrockModelSpecificationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether assisted slot resolution is turned on or off.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotresolutionimprovementspecification.html#cfn-lex-bot-slotresolutionimprovementspecification-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotResolutionImprovementSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "composite_slot_type_setting": "compositeSlotTypeSetting",
            "description": "description",
            "external_source_setting": "externalSourceSetting",
            "name": "name",
            "parent_slot_type_signature": "parentSlotTypeSignature",
            "slot_type_values": "slotTypeValues",
            "value_selection_setting": "valueSelectionSetting",
        },
    )
    class SlotTypeProperty:
        def __init__(
            self,
            *,
            composite_slot_type_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.CompositeSlotTypeSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            external_source_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ExternalSourceSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            parent_slot_type_signature: typing.Optional[builtins.str] = None,
            slot_type_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotTypeValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            value_selection_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotValueSelectionSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a slot type.

            :param composite_slot_type_setting: 
            :param description: A description of the slot type. Use the description to help identify the slot type in lists.
            :param external_source_setting: Sets the type of external information used to create the slot type.
            :param name: The name of the slot type. A slot type name must be unique withing the account.
            :param parent_slot_type_signature: The built-in slot type used as a parent of this slot type. When you define a parent slot type, the new slot type has the configuration of the parent lot type. Only ``AMAZON.AlphaNumeric`` is supported.
            :param slot_type_values: A list of SlotTypeValue objects that defines the values that the slot type can take. Each value can have a list of synonyms, additional values that help train the machine learning model about the values that it resolves for the slot.
            :param value_selection_setting: Determines the slot resolution strategy that Amazon Lex uses to return slot type values. The field can be set to one of the following values: - ``ORIGINAL_VALUE`` - Returns the value entered by the user, if the user value is similar to the slot value. - ``TOP_RESOLUTION`` - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned. If you don't specify the ``valueSelectionStrategy`` , the default is ``ORIGINAL_VALUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                slot_type_property = lex_mixins.CfnBotPropsMixin.SlotTypeProperty(
                    composite_slot_type_setting=lex_mixins.CfnBotPropsMixin.CompositeSlotTypeSettingProperty(
                        sub_slots=[lex_mixins.CfnBotPropsMixin.SubSlotTypeCompositionProperty(
                            name="name",
                            slot_type_id="slotTypeId"
                        )]
                    ),
                    description="description",
                    external_source_setting=lex_mixins.CfnBotPropsMixin.ExternalSourceSettingProperty(
                        grammar_slot_type_setting=lex_mixins.CfnBotPropsMixin.GrammarSlotTypeSettingProperty(
                            source=lex_mixins.CfnBotPropsMixin.GrammarSlotTypeSourceProperty(
                                kms_key_arn="kmsKeyArn",
                                s3_bucket_name="s3BucketName",
                                s3_object_key="s3ObjectKey"
                            )
                        )
                    ),
                    name="name",
                    parent_slot_type_signature="parentSlotTypeSignature",
                    slot_type_values=[lex_mixins.CfnBotPropsMixin.SlotTypeValueProperty(
                        sample_value=lex_mixins.CfnBotPropsMixin.SampleValueProperty(
                            value="value"
                        ),
                        synonyms=[lex_mixins.CfnBotPropsMixin.SampleValueProperty(
                            value="value"
                        )]
                    )],
                    value_selection_setting=lex_mixins.CfnBotPropsMixin.SlotValueSelectionSettingProperty(
                        advanced_recognition_setting=lex_mixins.CfnBotPropsMixin.AdvancedRecognitionSettingProperty(
                            audio_recognition_strategy="audioRecognitionStrategy"
                        ),
                        regex_filter=lex_mixins.CfnBotPropsMixin.SlotValueRegexFilterProperty(
                            pattern="pattern"
                        ),
                        resolution_strategy="resolutionStrategy"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84f0a5308d0ffbbec2fb32dc8d706c5644d80f7063bf6a53a8b75aad53d70765)
                check_type(argname="argument composite_slot_type_setting", value=composite_slot_type_setting, expected_type=type_hints["composite_slot_type_setting"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument external_source_setting", value=external_source_setting, expected_type=type_hints["external_source_setting"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument parent_slot_type_signature", value=parent_slot_type_signature, expected_type=type_hints["parent_slot_type_signature"])
                check_type(argname="argument slot_type_values", value=slot_type_values, expected_type=type_hints["slot_type_values"])
                check_type(argname="argument value_selection_setting", value=value_selection_setting, expected_type=type_hints["value_selection_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if composite_slot_type_setting is not None:
                self._values["composite_slot_type_setting"] = composite_slot_type_setting
            if description is not None:
                self._values["description"] = description
            if external_source_setting is not None:
                self._values["external_source_setting"] = external_source_setting
            if name is not None:
                self._values["name"] = name
            if parent_slot_type_signature is not None:
                self._values["parent_slot_type_signature"] = parent_slot_type_signature
            if slot_type_values is not None:
                self._values["slot_type_values"] = slot_type_values
            if value_selection_setting is not None:
                self._values["value_selection_setting"] = value_selection_setting

        @builtins.property
        def composite_slot_type_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CompositeSlotTypeSettingProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-compositeslottypesetting
            '''
            result = self._values.get("composite_slot_type_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CompositeSlotTypeSettingProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the slot type.

            Use the description to help identify the slot type in lists.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_source_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ExternalSourceSettingProperty"]]:
            '''Sets the type of external information used to create the slot type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-externalsourcesetting
            '''
            result = self._values.get("external_source_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ExternalSourceSettingProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the slot type.

            A slot type name must be unique withing the account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parent_slot_type_signature(self) -> typing.Optional[builtins.str]:
            '''The built-in slot type used as a parent of this slot type.

            When you define a parent slot type, the new slot type has the configuration of the parent lot type.

            Only ``AMAZON.AlphaNumeric`` is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-parentslottypesignature
            '''
            result = self._values.get("parent_slot_type_signature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slot_type_values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotTypeValueProperty"]]]]:
            '''A list of SlotTypeValue objects that defines the values that the slot type can take.

            Each value can have a list of synonyms, additional values that help train the machine learning model about the values that it resolves for the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-slottypevalues
            '''
            result = self._values.get("slot_type_values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotTypeValueProperty"]]]], result)

        @builtins.property
        def value_selection_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueSelectionSettingProperty"]]:
            '''Determines the slot resolution strategy that Amazon Lex uses to return slot type values.

            The field can be set to one of the following values:

            - ``ORIGINAL_VALUE`` - Returns the value entered by the user, if the user value is similar to the slot value.
            - ``TOP_RESOLUTION`` - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned.

            If you don't specify the ``valueSelectionStrategy`` , the default is ``ORIGINAL_VALUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-valueselectionsetting
            '''
            result = self._values.get("value_selection_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueSelectionSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotTypeValueProperty",
        jsii_struct_bases=[],
        name_mapping={"sample_value": "sampleValue", "synonyms": "synonyms"},
    )
    class SlotTypeValueProperty:
        def __init__(
            self,
            *,
            sample_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SampleValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            synonyms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SampleValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Each slot type can have a set of values.

            Each ``SlotTypeValue`` represents a value that the slot type can take.

            :param sample_value: The value of the slot type entry.
            :param synonyms: Additional values related to the slot type entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottypevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                slot_type_value_property = lex_mixins.CfnBotPropsMixin.SlotTypeValueProperty(
                    sample_value=lex_mixins.CfnBotPropsMixin.SampleValueProperty(
                        value="value"
                    ),
                    synonyms=[lex_mixins.CfnBotPropsMixin.SampleValueProperty(
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9d28b5c5134b7b57121fab62d5ddde29cce3070b37e45d16f0dcbbf2f0c79c9)
                check_type(argname="argument sample_value", value=sample_value, expected_type=type_hints["sample_value"])
                check_type(argname="argument synonyms", value=synonyms, expected_type=type_hints["synonyms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sample_value is not None:
                self._values["sample_value"] = sample_value
            if synonyms is not None:
                self._values["synonyms"] = synonyms

        @builtins.property
        def sample_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleValueProperty"]]:
            '''The value of the slot type entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottypevalue.html#cfn-lex-bot-slottypevalue-samplevalue
            '''
            result = self._values.get("sample_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleValueProperty"]], result)

        @builtins.property
        def synonyms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleValueProperty"]]]]:
            '''Additional values related to the slot type entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottypevalue.html#cfn-lex-bot-slottypevalue-synonyms
            '''
            result = self._values.get("synonyms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotTypeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotValueElicitationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_value_specification": "defaultValueSpecification",
            "prompt_specification": "promptSpecification",
            "sample_utterances": "sampleUtterances",
            "slot_capture_setting": "slotCaptureSetting",
            "slot_constraint": "slotConstraint",
            "wait_and_continue_specification": "waitAndContinueSpecification",
        },
    )
    class SlotValueElicitationSettingProperty:
        def __init__(
            self,
            *,
            default_value_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotDefaultValueSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            prompt_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.PromptSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sample_utterances: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SampleUtteranceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            slot_capture_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotCaptureSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            slot_constraint: typing.Optional[builtins.str] = None,
            wait_and_continue_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.WaitAndContinueSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the elicitation setting details eliciting a slot.

            :param default_value_specification: A list of default values for a slot. Default values are used when Amazon Lex hasn't determined a value for a slot. You can specify default values from context variables, session attributes, and defined values.
            :param prompt_specification: The prompt that Amazon Lex uses to elicit the slot value from the user.
            :param sample_utterances: If you know a specific pattern that users might respond to an Amazon Lex request for a slot value, you can provide those utterances to improve accuracy. This is optional. In most cases, Amazon Lex is capable of understanding user utterances.
            :param slot_capture_setting: Specifies the settings that Amazon Lex uses when a slot value is successfully entered by a user.
            :param slot_constraint: Specifies whether the slot is required or optional.
            :param wait_and_continue_specification: Specifies the prompts that Amazon Lex uses while a bot is waiting for customer input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae3279244dfa62342c89eb8fa1aca2d728b420a8b9864ba2bd72039dd6e8bf87)
                check_type(argname="argument default_value_specification", value=default_value_specification, expected_type=type_hints["default_value_specification"])
                check_type(argname="argument prompt_specification", value=prompt_specification, expected_type=type_hints["prompt_specification"])
                check_type(argname="argument sample_utterances", value=sample_utterances, expected_type=type_hints["sample_utterances"])
                check_type(argname="argument slot_capture_setting", value=slot_capture_setting, expected_type=type_hints["slot_capture_setting"])
                check_type(argname="argument slot_constraint", value=slot_constraint, expected_type=type_hints["slot_constraint"])
                check_type(argname="argument wait_and_continue_specification", value=wait_and_continue_specification, expected_type=type_hints["wait_and_continue_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_value_specification is not None:
                self._values["default_value_specification"] = default_value_specification
            if prompt_specification is not None:
                self._values["prompt_specification"] = prompt_specification
            if sample_utterances is not None:
                self._values["sample_utterances"] = sample_utterances
            if slot_capture_setting is not None:
                self._values["slot_capture_setting"] = slot_capture_setting
            if slot_constraint is not None:
                self._values["slot_constraint"] = slot_constraint
            if wait_and_continue_specification is not None:
                self._values["wait_and_continue_specification"] = wait_and_continue_specification

        @builtins.property
        def default_value_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotDefaultValueSpecificationProperty"]]:
            '''A list of default values for a slot.

            Default values are used when Amazon Lex hasn't determined a value for a slot. You can specify default values from context variables, session attributes, and defined values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-defaultvaluespecification
            '''
            result = self._values.get("default_value_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotDefaultValueSpecificationProperty"]], result)

        @builtins.property
        def prompt_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PromptSpecificationProperty"]]:
            '''The prompt that Amazon Lex uses to elicit the slot value from the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-promptspecification
            '''
            result = self._values.get("prompt_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PromptSpecificationProperty"]], result)

        @builtins.property
        def sample_utterances(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleUtteranceProperty"]]]]:
            '''If you know a specific pattern that users might respond to an Amazon Lex request for a slot value, you can provide those utterances to improve accuracy.

            This is optional. In most cases, Amazon Lex is capable of understanding user utterances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-sampleutterances
            '''
            result = self._values.get("sample_utterances")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleUtteranceProperty"]]]], result)

        @builtins.property
        def slot_capture_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotCaptureSettingProperty"]]:
            '''Specifies the settings that Amazon Lex uses when a slot value is successfully entered by a user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-slotcapturesetting
            '''
            result = self._values.get("slot_capture_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotCaptureSettingProperty"]], result)

        @builtins.property
        def slot_constraint(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the slot is required or optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-slotconstraint
            '''
            result = self._values.get("slot_constraint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def wait_and_continue_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.WaitAndContinueSpecificationProperty"]]:
            '''Specifies the prompts that Amazon Lex uses while a bot is waiting for customer input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-waitandcontinuespecification
            '''
            result = self._values.get("wait_and_continue_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.WaitAndContinueSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueElicitationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty",
        jsii_struct_bases=[],
        name_mapping={
            "slot_name": "slotName",
            "slot_value_override": "slotValueOverride",
        },
    )
    class SlotValueOverrideMapProperty:
        def __init__(
            self,
            *,
            slot_name: typing.Optional[builtins.str] = None,
            slot_value_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotValueOverrideProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Maps a slot name to the `SlotValueOverride <https://docs.aws.amazon.com/lexv2/latest/APIReference/API_SlotValueOverride.html>`_ object.

            :param slot_name: The name of the slot.
            :param slot_value_override: The SlotValueOverride object to which the slot name will be mapped.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueoverridemap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                # slot_value_override_property_: lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty
                
                slot_value_override_map_property = lex_mixins.CfnBotPropsMixin.SlotValueOverrideMapProperty(
                    slot_name="slotName",
                    slot_value_override=lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                        shape="shape",
                        value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                            interpreted_value="interpretedValue"
                        ),
                        values=[slot_value_override_property_]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3dd83ed701c5b2837dc440104e76be884cea2bcaa4bf034af2f6bd9630f3305e)
                check_type(argname="argument slot_name", value=slot_name, expected_type=type_hints["slot_name"])
                check_type(argname="argument slot_value_override", value=slot_value_override, expected_type=type_hints["slot_value_override"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if slot_name is not None:
                self._values["slot_name"] = slot_name
            if slot_value_override is not None:
                self._values["slot_value_override"] = slot_value_override

        @builtins.property
        def slot_name(self) -> typing.Optional[builtins.str]:
            '''The name of the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueoverridemap.html#cfn-lex-bot-slotvalueoverridemap-slotname
            '''
            result = self._values.get("slot_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slot_value_override(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueOverrideProperty"]]:
            '''The SlotValueOverride object to which the slot name will be mapped.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueoverridemap.html#cfn-lex-bot-slotvalueoverridemap-slotvalueoverride
            '''
            result = self._values.get("slot_value_override")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueOverrideProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueOverrideMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotValueOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"shape": "shape", "value": "value", "values": "values"},
    )
    class SlotValueOverrideProperty:
        def __init__(
            self,
            *,
            shape: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotValueOverrideProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The slot values that Amazon Lex uses when it sets slot values in a dialog step.

            :param shape: When the shape value is ``List`` , it indicates that the ``values`` field contains a list of slot values. When the value is ``Scalar`` , it indicates that the ``value`` field contains a single value.
            :param value: The current value of the slot.
            :param values: A list of one or more values that the user provided for the slot. For example, for a slot that elicits pizza toppings, the values might be "pepperoni" and "pineapple."

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                # slot_value_override_property_: lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty
                
                slot_value_override_property = lex_mixins.CfnBotPropsMixin.SlotValueOverrideProperty(
                    shape="shape",
                    value=lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                        interpreted_value="interpretedValue"
                    ),
                    values=[slot_value_override_property_]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f6191fceac735782077bdef6c412368d7fcbb2736a87cafcea2e9edcb3fc4a6)
                check_type(argname="argument shape", value=shape, expected_type=type_hints["shape"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if shape is not None:
                self._values["shape"] = shape
            if value is not None:
                self._values["value"] = value
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def shape(self) -> typing.Optional[builtins.str]:
            '''When the shape value is ``List`` , it indicates that the ``values`` field contains a list of slot values.

            When the value is ``Scalar`` , it indicates that the ``value`` field contains a single value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueoverride.html#cfn-lex-bot-slotvalueoverride-shape
            '''
            result = self._values.get("shape")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueProperty"]]:
            '''The current value of the slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueoverride.html#cfn-lex-bot-slotvalueoverride-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueProperty"]], result)

        @builtins.property
        def values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueOverrideProperty"]]]]:
            '''A list of one or more values that the user provided for the slot.

            For example, for a slot that elicits pizza toppings, the values might be "pepperoni" and "pineapple."

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueoverride.html#cfn-lex-bot-slotvalueoverride-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueOverrideProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotValueProperty",
        jsii_struct_bases=[],
        name_mapping={"interpreted_value": "interpretedValue"},
    )
    class SlotValueProperty:
        def __init__(
            self,
            *,
            interpreted_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The value to set in a slot.

            :param interpreted_value: The value that Amazon Lex determines for the slot. The actual value depends on the setting of the value selection strategy for the bot. You can choose to use the value entered by the user, or you can have Amazon Lex choose the first value in the ``resolvedValues`` list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                slot_value_property = lex_mixins.CfnBotPropsMixin.SlotValueProperty(
                    interpreted_value="interpretedValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d669e29951b9ae8f2c44d7cd7bb6b088a22b4b01231bd4dd467943c4dd694208)
                check_type(argname="argument interpreted_value", value=interpreted_value, expected_type=type_hints["interpreted_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interpreted_value is not None:
                self._values["interpreted_value"] = interpreted_value

        @builtins.property
        def interpreted_value(self) -> typing.Optional[builtins.str]:
            '''The value that Amazon Lex determines for the slot.

            The actual value depends on the setting of the value selection strategy for the bot. You can choose to use the value entered by the user, or you can have Amazon Lex choose the first value in the ``resolvedValues`` list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalue.html#cfn-lex-bot-slotvalue-interpretedvalue
            '''
            result = self._values.get("interpreted_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotValueRegexFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"pattern": "pattern"},
    )
    class SlotValueRegexFilterProperty:
        def __init__(self, *, pattern: typing.Optional[builtins.str] = None) -> None:
            '''Provides a regular expression used to validate the value of a slot.

            :param pattern: A regular expression used to validate the value of a slot. Use a standard regular expression. Amazon Lex supports the following characters in the regular expression: - A-Z, a-z - 0-9 - Unicode characters ("\\⁠u") Represent Unicode characters with four digits, for example "\\⁠u0041" or "\\⁠u005A". The following regular expression operators are not supported: - Infinite repeaters: *, +, or {x,} with no upper bound. - Wild card (.)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueregexfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                slot_value_regex_filter_property = lex_mixins.CfnBotPropsMixin.SlotValueRegexFilterProperty(
                    pattern="pattern"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15ea3a466a035d41b25d8936582ca55ae982748a289284b6a6f946c560e5d456)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pattern is not None:
                self._values["pattern"] = pattern

        @builtins.property
        def pattern(self) -> typing.Optional[builtins.str]:
            '''A regular expression used to validate the value of a slot.

            Use a standard regular expression. Amazon Lex supports the following characters in the regular expression:

            - A-Z, a-z
            - 0-9
            - Unicode characters ("\\⁠u")

            Represent Unicode characters with four digits, for example "\\⁠u0041" or "\\⁠u005A".

            The following regular expression operators are not supported:

            - Infinite repeaters: *, +, or {x,} with no upper bound.
            - Wild card (.)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueregexfilter.html#cfn-lex-bot-slotvalueregexfilter-pattern
            '''
            result = self._values.get("pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueRegexFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SlotValueSelectionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "advanced_recognition_setting": "advancedRecognitionSetting",
            "regex_filter": "regexFilter",
            "resolution_strategy": "resolutionStrategy",
        },
    )
    class SlotValueSelectionSettingProperty:
        def __init__(
            self,
            *,
            advanced_recognition_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.AdvancedRecognitionSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            regex_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotValueRegexFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resolution_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains settings used by Amazon Lex to select a slot value.

            :param advanced_recognition_setting: Provides settings that enable advanced recognition settings for slot values. You can use this to enable using slot values as a custom vocabulary for recognizing user utterances.
            :param regex_filter: A regular expression used to validate the value of a slot.
            :param resolution_strategy: Determines the slot resolution strategy that Amazon Lex uses to return slot type values. The field can be set to one of the following values: - ``ORIGINAL_VALUE`` - Returns the value entered by the user, if the user value is similar to the slot value. - ``TOP_RESOLUTION`` - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned. If you don't specify the ``valueSelectionStrategy`` , the default is ``ORIGINAL_VALUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                slot_value_selection_setting_property = lex_mixins.CfnBotPropsMixin.SlotValueSelectionSettingProperty(
                    advanced_recognition_setting=lex_mixins.CfnBotPropsMixin.AdvancedRecognitionSettingProperty(
                        audio_recognition_strategy="audioRecognitionStrategy"
                    ),
                    regex_filter=lex_mixins.CfnBotPropsMixin.SlotValueRegexFilterProperty(
                        pattern="pattern"
                    ),
                    resolution_strategy="resolutionStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6a636eac5be6a1130c83d63896c1bd4315750e12f0977c183816c0c9e2f6130)
                check_type(argname="argument advanced_recognition_setting", value=advanced_recognition_setting, expected_type=type_hints["advanced_recognition_setting"])
                check_type(argname="argument regex_filter", value=regex_filter, expected_type=type_hints["regex_filter"])
                check_type(argname="argument resolution_strategy", value=resolution_strategy, expected_type=type_hints["resolution_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if advanced_recognition_setting is not None:
                self._values["advanced_recognition_setting"] = advanced_recognition_setting
            if regex_filter is not None:
                self._values["regex_filter"] = regex_filter
            if resolution_strategy is not None:
                self._values["resolution_strategy"] = resolution_strategy

        @builtins.property
        def advanced_recognition_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AdvancedRecognitionSettingProperty"]]:
            '''Provides settings that enable advanced recognition settings for slot values.

            You can use this to enable using slot values as a custom vocabulary for recognizing user utterances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html#cfn-lex-bot-slotvalueselectionsetting-advancedrecognitionsetting
            '''
            result = self._values.get("advanced_recognition_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.AdvancedRecognitionSettingProperty"]], result)

        @builtins.property
        def regex_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueRegexFilterProperty"]]:
            '''A regular expression used to validate the value of a slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html#cfn-lex-bot-slotvalueselectionsetting-regexfilter
            '''
            result = self._values.get("regex_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotValueRegexFilterProperty"]], result)

        @builtins.property
        def resolution_strategy(self) -> typing.Optional[builtins.str]:
            '''Determines the slot resolution strategy that Amazon Lex uses to return slot type values.

            The field can be set to one of the following values:

            - ``ORIGINAL_VALUE`` - Returns the value entered by the user, if the user value is similar to the slot value.
            - ``TOP_RESOLUTION`` - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned.

            If you don't specify the ``valueSelectionStrategy`` , the default is ``ORIGINAL_VALUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html#cfn-lex-bot-slotvalueselectionsetting-resolutionstrategy
            '''
            result = self._values.get("resolution_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueSelectionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SpecificationsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "slot_type_id": "slotTypeId",
            "value_elicitation_setting": "valueElicitationSetting",
        },
    )
    class SpecificationsProperty:
        def __init__(
            self,
            *,
            slot_type_id: typing.Optional[builtins.str] = None,
            value_elicitation_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SubSlotValueElicitationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Subslot specifications.

            :param slot_type_id: The unique identifier assigned to the slot type.
            :param value_elicitation_setting: Specifies the elicitation setting details for constituent sub slots of a composite slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-specifications.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                specifications_property = lex_mixins.CfnBotPropsMixin.SpecificationsProperty(
                    slot_type_id="slotTypeId",
                    value_elicitation_setting=lex_mixins.CfnBotPropsMixin.SubSlotValueElicitationSettingProperty(
                        default_value_specification=lex_mixins.CfnBotPropsMixin.SlotDefaultValueSpecificationProperty(
                            default_value_list=[lex_mixins.CfnBotPropsMixin.SlotDefaultValueProperty(
                                default_value="defaultValue"
                            )]
                        ),
                        prompt_specification=lex_mixins.CfnBotPropsMixin.PromptSpecificationProperty(
                            allow_interrupt=False,
                            max_retries=123,
                            message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                                variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                            message_selection_strategy="messageSelectionStrategy",
                            prompt_attempts_specification={
                                "prompt_attempts_specification_key": lex_mixins.CfnBotPropsMixin.PromptAttemptSpecificationProperty(
                                    allowed_input_types=lex_mixins.CfnBotPropsMixin.AllowedInputTypesProperty(
                                        allow_audio_input=False,
                                        allow_dtmf_input=False
                                    ),
                                    allow_interrupt=False,
                                    audio_and_dtmf_input_specification=lex_mixins.CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty(
                                        audio_specification=lex_mixins.CfnBotPropsMixin.AudioSpecificationProperty(
                                            end_timeout_ms=123,
                                            max_length_ms=123
                                        ),
                                        dtmf_specification=lex_mixins.CfnBotPropsMixin.DTMFSpecificationProperty(
                                            deletion_character="deletionCharacter",
                                            end_character="endCharacter",
                                            end_timeout_ms=123,
                                            max_length=123
                                        ),
                                        start_timeout_ms=123
                                    ),
                                    text_input_specification=lex_mixins.CfnBotPropsMixin.TextInputSpecificationProperty(
                                        start_timeout_ms=123
                                    )
                                )
                            }
                        ),
                        sample_utterances=[lex_mixins.CfnBotPropsMixin.SampleUtteranceProperty(
                            utterance="utterance"
                        )],
                        wait_and_continue_specification=lex_mixins.CfnBotPropsMixin.WaitAndContinueSpecificationProperty(
                            continue_response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                                allow_interrupt=False,
                                message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                    message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle",
                                            title="title"
                                        ),
                                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                                    variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle",
                                            title="title"
                                        ),
                                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )]
                            ),
                            is_active=False,
                            still_waiting_response=lex_mixins.CfnBotPropsMixin.StillWaitingResponseSpecificationProperty(
                                allow_interrupt=False,
                                frequency_in_seconds=123,
                                message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                    message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle",
                                            title="title"
                                        ),
                                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                                    variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle",
                                            title="title"
                                        ),
                                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                                timeout_in_seconds=123
                            ),
                            waiting_response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                                allow_interrupt=False,
                                message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                    message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle",
                                            title="title"
                                        ),
                                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                                    variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                        custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                            buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle",
                                            title="title"
                                        ),
                                        plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )]
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ab89958e4e25fb39804c3df41bf036f2603561f6275bb26cf1a7775a0454af0)
                check_type(argname="argument slot_type_id", value=slot_type_id, expected_type=type_hints["slot_type_id"])
                check_type(argname="argument value_elicitation_setting", value=value_elicitation_setting, expected_type=type_hints["value_elicitation_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if slot_type_id is not None:
                self._values["slot_type_id"] = slot_type_id
            if value_elicitation_setting is not None:
                self._values["value_elicitation_setting"] = value_elicitation_setting

        @builtins.property
        def slot_type_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier assigned to the slot type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-specifications.html#cfn-lex-bot-specifications-slottypeid
            '''
            result = self._values.get("slot_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_elicitation_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SubSlotValueElicitationSettingProperty"]]:
            '''Specifies the elicitation setting details for constituent sub slots of a composite slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-specifications.html#cfn-lex-bot-specifications-valueelicitationsetting
            '''
            result = self._values.get("value_elicitation_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SubSlotValueElicitationSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpecificationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.StillWaitingResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_interrupt": "allowInterrupt",
            "frequency_in_seconds": "frequencyInSeconds",
            "message_groups_list": "messageGroupsList",
            "timeout_in_seconds": "timeoutInSeconds",
        },
    )
    class StillWaitingResponseSpecificationProperty:
        def __init__(
            self,
            *,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            frequency_in_seconds: typing.Optional[jsii.Number] = None,
            message_groups_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.MessageGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines the messages that Amazon Lex sends to a user to remind them that the bot is waiting for a response.

            :param allow_interrupt: Indicates that the user can interrupt the response by speaking while the message is being played.
            :param frequency_in_seconds: How often a message should be sent to the user. Minimum of 1 second, maximum of 5 minutes.
            :param message_groups_list: One or more message groups, each containing one or more messages, that define the prompts that Amazon Lex sends to the user.
            :param timeout_in_seconds: If Amazon Lex waits longer than this length of time for a response, it will stop sending messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                still_waiting_response_specification_property = lex_mixins.CfnBotPropsMixin.StillWaitingResponseSpecificationProperty(
                    allow_interrupt=False,
                    frequency_in_seconds=123,
                    message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                        message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle",
                                title="title"
                            ),
                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                        variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle",
                                title="title"
                            ),
                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                    timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c6b0bd695507fccfe55b0ce800ca8c48ee4744c2a773d7cdad25710ca2b85a5)
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
                check_type(argname="argument frequency_in_seconds", value=frequency_in_seconds, expected_type=type_hints["frequency_in_seconds"])
                check_type(argname="argument message_groups_list", value=message_groups_list, expected_type=type_hints["message_groups_list"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt
            if frequency_in_seconds is not None:
                self._values["frequency_in_seconds"] = frequency_in_seconds
            if message_groups_list is not None:
                self._values["message_groups_list"] = message_groups_list
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates that the user can interrupt the response by speaking while the message is being played.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def frequency_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''How often a message should be sent to the user.

            Minimum of 1 second, maximum of 5 minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-frequencyinseconds
            '''
            result = self._values.get("frequency_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def message_groups_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageGroupProperty"]]]]:
            '''One or more message groups, each containing one or more messages, that define the prompts that Amazon Lex sends to the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-messagegroupslist
            '''
            result = self._values.get("message_groups_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.MessageGroupProperty"]]]], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''If Amazon Lex waits longer than this length of time for a response, it will stop sending messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StillWaitingResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SubSlotSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "slot_specifications": "slotSpecifications",
        },
    )
    class SubSlotSettingProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            slot_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SpecificationsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifications for the constituent sub slots and the expression for the composite slot.

            :param expression: The expression text for defining the constituent sub slots in the composite slot using logical AND and OR operators.
            :param slot_specifications: Specifications for the constituent sub slots of a composite slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslotsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                sub_slot_setting_property = lex_mixins.CfnBotPropsMixin.SubSlotSettingProperty(
                    expression="expression",
                    slot_specifications={
                        "slot_specifications_key": lex_mixins.CfnBotPropsMixin.SpecificationsProperty(
                            slot_type_id="slotTypeId",
                            value_elicitation_setting=lex_mixins.CfnBotPropsMixin.SubSlotValueElicitationSettingProperty(
                                default_value_specification=lex_mixins.CfnBotPropsMixin.SlotDefaultValueSpecificationProperty(
                                    default_value_list=[lex_mixins.CfnBotPropsMixin.SlotDefaultValueProperty(
                                        default_value="defaultValue"
                                    )]
                                ),
                                prompt_specification=lex_mixins.CfnBotPropsMixin.PromptSpecificationProperty(
                                    allow_interrupt=False,
                                    max_retries=123,
                                    message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                        message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle",
                                                title="title"
                                            ),
                                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                                        variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                            custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                                buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle",
                                                title="title"
                                            ),
                                            plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                                    message_selection_strategy="messageSelectionStrategy",
                                    prompt_attempts_specification={
                                        "prompt_attempts_specification_key": lex_mixins.CfnBotPropsMixin.PromptAttemptSpecificationProperty(
                                            allowed_input_types=lex_mixins.CfnBotPropsMixin.AllowedInputTypesProperty(
                                                allow_audio_input=False,
                                                allow_dtmf_input=False
                                            ),
                                            allow_interrupt=False,
                                            audio_and_dtmf_input_specification=lex_mixins.CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty(
                                                audio_specification=lex_mixins.CfnBotPropsMixin.AudioSpecificationProperty(
                                                    end_timeout_ms=123,
                                                    max_length_ms=123
                                                ),
                                                dtmf_specification=lex_mixins.CfnBotPropsMixin.DTMFSpecificationProperty(
                                                    deletion_character="deletionCharacter",
                                                    end_character="endCharacter",
                                                    end_timeout_ms=123,
                                                    max_length=123
                                                ),
                                                start_timeout_ms=123
                                            ),
                                            text_input_specification=lex_mixins.CfnBotPropsMixin.TextInputSpecificationProperty(
                                                start_timeout_ms=123
                                            )
                                        )
                                    }
                                ),
                                sample_utterances=[lex_mixins.CfnBotPropsMixin.SampleUtteranceProperty(
                                    utterance="utterance"
                                )],
                                wait_and_continue_specification=lex_mixins.CfnBotPropsMixin.WaitAndContinueSpecificationProperty(
                                    continue_response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                                        allow_interrupt=False,
                                        message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle",
                                                    title="title"
                                                ),
                                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
                                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle",
                                                    title="title"
                                                ),
                                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )]
                                    ),
                                    is_active=False,
                                    still_waiting_response=lex_mixins.CfnBotPropsMixin.StillWaitingResponseSpecificationProperty(
                                        allow_interrupt=False,
                                        frequency_in_seconds=123,
                                        message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle",
                                                    title="title"
                                                ),
                                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
                                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle",
                                                    title="title"
                                                ),
                                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
                                        timeout_in_seconds=123
                                    ),
                                    waiting_response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                                        allow_interrupt=False,
                                        message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle",
                                                    title="title"
                                                ),
                                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
                                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle",
                                                    title="title"
                                                ),
                                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )]
                                    )
                                )
                            )
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d34900e32148623a9b989e0303eda0659dd8cb2630db428b666de131c19692e6)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument slot_specifications", value=slot_specifications, expected_type=type_hints["slot_specifications"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if slot_specifications is not None:
                self._values["slot_specifications"] = slot_specifications

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The expression text for defining the constituent sub slots in the composite slot using logical AND and OR operators.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslotsetting.html#cfn-lex-bot-subslotsetting-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slot_specifications(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SpecificationsProperty"]]]]:
            '''Specifications for the constituent sub slots of a composite slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslotsetting.html#cfn-lex-bot-subslotsetting-slotspecifications
            '''
            result = self._values.get("slot_specifications")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SpecificationsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubSlotSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SubSlotTypeCompositionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "slot_type_id": "slotTypeId"},
    )
    class SubSlotTypeCompositionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            slot_type_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Subslot type composition.

            :param name: Name of a constituent sub slot inside a composite slot.
            :param slot_type_id: The unique identifier assigned to a slot type. This refers to either a built-in slot type or the unique slotTypeId of a custom slot type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslottypecomposition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                sub_slot_type_composition_property = lex_mixins.CfnBotPropsMixin.SubSlotTypeCompositionProperty(
                    name="name",
                    slot_type_id="slotTypeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24a3499deee04a0e37b23ecc1bde2163f9aa5c788e32ad476a8fff901303615b)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument slot_type_id", value=slot_type_id, expected_type=type_hints["slot_type_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if slot_type_id is not None:
                self._values["slot_type_id"] = slot_type_id

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of a constituent sub slot inside a composite slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslottypecomposition.html#cfn-lex-bot-subslottypecomposition-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slot_type_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier assigned to a slot type.

            This refers to either a built-in slot type or the unique slotTypeId of a custom slot type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslottypecomposition.html#cfn-lex-bot-subslottypecomposition-slottypeid
            '''
            result = self._values.get("slot_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubSlotTypeCompositionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.SubSlotValueElicitationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_value_specification": "defaultValueSpecification",
            "prompt_specification": "promptSpecification",
            "sample_utterances": "sampleUtterances",
            "wait_and_continue_specification": "waitAndContinueSpecification",
        },
    )
    class SubSlotValueElicitationSettingProperty:
        def __init__(
            self,
            *,
            default_value_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SlotDefaultValueSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            prompt_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.PromptSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sample_utterances: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.SampleUtteranceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            wait_and_continue_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.WaitAndContinueSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Subslot elicitation settings.

            ``DefaultValueSpecification`` is a list of default values for a constituent sub slot in a composite slot. Default values are used when Amazon Lex hasn't determined a value for a slot. You can specify default values from context variables, session attributes, and defined values. This is similar to ``DefaultValueSpecification`` for slots.

            ``PromptSpecification`` is the prompt that Amazon Lex uses to elicit the sub slot value from the user. This is similar to ``PromptSpecification`` for slots.

            :param default_value_specification: 
            :param prompt_specification: 
            :param sample_utterances: If you know a specific pattern that users might respond to an Amazon Lex request for a sub slot value, you can provide those utterances to improve accuracy. This is optional. In most cases Amazon Lex is capable of understanding user utterances. This is similar to ``SampleUtterances`` for slots.
            :param wait_and_continue_specification: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslotvalueelicitationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                sub_slot_value_elicitation_setting_property = lex_mixins.CfnBotPropsMixin.SubSlotValueElicitationSettingProperty(
                    default_value_specification=lex_mixins.CfnBotPropsMixin.SlotDefaultValueSpecificationProperty(
                        default_value_list=[lex_mixins.CfnBotPropsMixin.SlotDefaultValueProperty(
                            default_value="defaultValue"
                        )]
                    ),
                    prompt_specification=lex_mixins.CfnBotPropsMixin.PromptSpecificationProperty(
                        allow_interrupt=False,
                        max_retries=123,
                        message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                        message_selection_strategy="messageSelectionStrategy",
                        prompt_attempts_specification={
                            "prompt_attempts_specification_key": lex_mixins.CfnBotPropsMixin.PromptAttemptSpecificationProperty(
                                allowed_input_types=lex_mixins.CfnBotPropsMixin.AllowedInputTypesProperty(
                                    allow_audio_input=False,
                                    allow_dtmf_input=False
                                ),
                                allow_interrupt=False,
                                audio_and_dtmf_input_specification=lex_mixins.CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty(
                                    audio_specification=lex_mixins.CfnBotPropsMixin.AudioSpecificationProperty(
                                        end_timeout_ms=123,
                                        max_length_ms=123
                                    ),
                                    dtmf_specification=lex_mixins.CfnBotPropsMixin.DTMFSpecificationProperty(
                                        deletion_character="deletionCharacter",
                                        end_character="endCharacter",
                                        end_timeout_ms=123,
                                        max_length=123
                                    ),
                                    start_timeout_ms=123
                                ),
                                text_input_specification=lex_mixins.CfnBotPropsMixin.TextInputSpecificationProperty(
                                    start_timeout_ms=123
                                )
                            )
                        }
                    ),
                    sample_utterances=[lex_mixins.CfnBotPropsMixin.SampleUtteranceProperty(
                        utterance="utterance"
                    )],
                    wait_and_continue_specification=lex_mixins.CfnBotPropsMixin.WaitAndContinueSpecificationProperty(
                        continue_response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                            allow_interrupt=False,
                            message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                                variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )]
                        ),
                        is_active=False,
                        still_waiting_response=lex_mixins.CfnBotPropsMixin.StillWaitingResponseSpecificationProperty(
                            allow_interrupt=False,
                            frequency_in_seconds=123,
                            message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                                variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                            timeout_in_seconds=123
                        ),
                        waiting_response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                            allow_interrupt=False,
                            message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                                message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                                variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                    custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                        buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle",
                                        title="title"
                                    ),
                                    plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2fe56ddb90b1a5ac3790448f4556c0750a94562d67a3e7f12b3c0cedb29cb562)
                check_type(argname="argument default_value_specification", value=default_value_specification, expected_type=type_hints["default_value_specification"])
                check_type(argname="argument prompt_specification", value=prompt_specification, expected_type=type_hints["prompt_specification"])
                check_type(argname="argument sample_utterances", value=sample_utterances, expected_type=type_hints["sample_utterances"])
                check_type(argname="argument wait_and_continue_specification", value=wait_and_continue_specification, expected_type=type_hints["wait_and_continue_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_value_specification is not None:
                self._values["default_value_specification"] = default_value_specification
            if prompt_specification is not None:
                self._values["prompt_specification"] = prompt_specification
            if sample_utterances is not None:
                self._values["sample_utterances"] = sample_utterances
            if wait_and_continue_specification is not None:
                self._values["wait_and_continue_specification"] = wait_and_continue_specification

        @builtins.property
        def default_value_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotDefaultValueSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslotvalueelicitationsetting.html#cfn-lex-bot-subslotvalueelicitationsetting-defaultvaluespecification
            '''
            result = self._values.get("default_value_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SlotDefaultValueSpecificationProperty"]], result)

        @builtins.property
        def prompt_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PromptSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslotvalueelicitationsetting.html#cfn-lex-bot-subslotvalueelicitationsetting-promptspecification
            '''
            result = self._values.get("prompt_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.PromptSpecificationProperty"]], result)

        @builtins.property
        def sample_utterances(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleUtteranceProperty"]]]]:
            '''If you know a specific pattern that users might respond to an Amazon Lex request for a sub slot value, you can provide those utterances to improve accuracy.

            This is optional. In most cases Amazon Lex is capable of understanding user utterances. This is similar to ``SampleUtterances`` for slots.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslotvalueelicitationsetting.html#cfn-lex-bot-subslotvalueelicitationsetting-sampleutterances
            '''
            result = self._values.get("sample_utterances")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.SampleUtteranceProperty"]]]], result)

        @builtins.property
        def wait_and_continue_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.WaitAndContinueSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-subslotvalueelicitationsetting.html#cfn-lex-bot-subslotvalueelicitationsetting-waitandcontinuespecification
            '''
            result = self._values.get("wait_and_continue_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.WaitAndContinueSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubSlotValueElicitationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.TestBotAliasSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bot_alias_locale_settings": "botAliasLocaleSettings",
            "conversation_log_settings": "conversationLogSettings",
            "description": "description",
            "sentiment_analysis_settings": "sentimentAnalysisSettings",
        },
    )
    class TestBotAliasSettingsProperty:
        def __init__(
            self,
            *,
            bot_alias_locale_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.BotAliasLocaleSettingsItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            conversation_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ConversationLogSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            sentiment_analysis_settings: typing.Any = None,
        ) -> None:
            '''Specifies configuration settings for the alias used to test the bot.

            If the ``TestBotAliasSettings`` property is not specified, the settings are configured with default values.

            :param bot_alias_locale_settings: Specifies settings that are unique to a locale. For example, you can use a different Lambda function depending on the bot's locale.
            :param conversation_log_settings: Specifies settings for conversation logs that save audio, text, and metadata information for conversations with your users.
            :param description: Specifies a description for the test bot alias.
            :param sentiment_analysis_settings: Specifies whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-testbotaliassettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                # sentiment_analysis_settings: Any
                
                test_bot_alias_settings_property = lex_mixins.CfnBotPropsMixin.TestBotAliasSettingsProperty(
                    bot_alias_locale_settings=[lex_mixins.CfnBotPropsMixin.BotAliasLocaleSettingsItemProperty(
                        bot_alias_locale_setting=lex_mixins.CfnBotPropsMixin.BotAliasLocaleSettingsProperty(
                            code_hook_specification=lex_mixins.CfnBotPropsMixin.CodeHookSpecificationProperty(
                                lambda_code_hook=lex_mixins.CfnBotPropsMixin.LambdaCodeHookProperty(
                                    code_hook_interface_version="codeHookInterfaceVersion",
                                    lambda_arn="lambdaArn"
                                )
                            ),
                            enabled=False
                        ),
                        locale_id="localeId"
                    )],
                    conversation_log_settings=lex_mixins.CfnBotPropsMixin.ConversationLogSettingsProperty(
                        audio_log_settings=[lex_mixins.CfnBotPropsMixin.AudioLogSettingProperty(
                            destination=lex_mixins.CfnBotPropsMixin.AudioLogDestinationProperty(
                                s3_bucket=lex_mixins.CfnBotPropsMixin.S3BucketLogDestinationProperty(
                                    kms_key_arn="kmsKeyArn",
                                    log_prefix="logPrefix",
                                    s3_bucket_arn="s3BucketArn"
                                )
                            ),
                            enabled=False
                        )],
                        text_log_settings=[lex_mixins.CfnBotPropsMixin.TextLogSettingProperty(
                            destination=lex_mixins.CfnBotPropsMixin.TextLogDestinationProperty(
                                cloud_watch=lex_mixins.CfnBotPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                                    log_prefix="logPrefix"
                                )
                            ),
                            enabled=False
                        )]
                    ),
                    description="description",
                    sentiment_analysis_settings=sentiment_analysis_settings
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e25855e553d9544abbc3ff607d7b06203d0eb6d03b6bf3202a437bf007b07275)
                check_type(argname="argument bot_alias_locale_settings", value=bot_alias_locale_settings, expected_type=type_hints["bot_alias_locale_settings"])
                check_type(argname="argument conversation_log_settings", value=conversation_log_settings, expected_type=type_hints["conversation_log_settings"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument sentiment_analysis_settings", value=sentiment_analysis_settings, expected_type=type_hints["sentiment_analysis_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bot_alias_locale_settings is not None:
                self._values["bot_alias_locale_settings"] = bot_alias_locale_settings
            if conversation_log_settings is not None:
                self._values["conversation_log_settings"] = conversation_log_settings
            if description is not None:
                self._values["description"] = description
            if sentiment_analysis_settings is not None:
                self._values["sentiment_analysis_settings"] = sentiment_analysis_settings

        @builtins.property
        def bot_alias_locale_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BotAliasLocaleSettingsItemProperty"]]]]:
            '''Specifies settings that are unique to a locale.

            For example, you can use a different Lambda function depending on the bot's locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-testbotaliassettings.html#cfn-lex-bot-testbotaliassettings-botaliaslocalesettings
            '''
            result = self._values.get("bot_alias_locale_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.BotAliasLocaleSettingsItemProperty"]]]], result)

        @builtins.property
        def conversation_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConversationLogSettingsProperty"]]:
            '''Specifies settings for conversation logs that save audio, text, and metadata information for conversations with your users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-testbotaliassettings.html#cfn-lex-bot-testbotaliassettings-conversationlogsettings
            '''
            result = self._values.get("conversation_log_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ConversationLogSettingsProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''Specifies a description for the test bot alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-testbotaliassettings.html#cfn-lex-bot-testbotaliassettings-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sentiment_analysis_settings(self) -> typing.Any:
            '''Specifies whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-testbotaliassettings.html#cfn-lex-bot-testbotaliassettings-sentimentanalysissettings
            '''
            result = self._values.get("sentiment_analysis_settings")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TestBotAliasSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.TextInputSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"start_timeout_ms": "startTimeoutMs"},
    )
    class TextInputSpecificationProperty:
        def __init__(
            self,
            *,
            start_timeout_ms: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the text input specifications.

            :param start_timeout_ms: Time for which a bot waits before re-prompting a customer for text input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textinputspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                text_input_specification_property = lex_mixins.CfnBotPropsMixin.TextInputSpecificationProperty(
                    start_timeout_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__730e40de73dfd22ba0db0d5c925c86a924d892b29915722c51234123e4cc932d)
                check_type(argname="argument start_timeout_ms", value=start_timeout_ms, expected_type=type_hints["start_timeout_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if start_timeout_ms is not None:
                self._values["start_timeout_ms"] = start_timeout_ms

        @builtins.property
        def start_timeout_ms(self) -> typing.Optional[jsii.Number]:
            '''Time for which a bot waits before re-prompting a customer for text input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textinputspecification.html#cfn-lex-bot-textinputspecification-starttimeoutms
            '''
            result = self._values.get("start_timeout_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextInputSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.TextLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch": "cloudWatch"},
    )
    class TextLogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.CloudWatchLogGroupLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines the Amazon CloudWatch Logs destination log group for conversation text logs.

            :param cloud_watch: Defines the Amazon CloudWatch Logs log group where text and metadata logs are delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                text_log_destination_property = lex_mixins.CfnBotPropsMixin.TextLogDestinationProperty(
                    cloud_watch=lex_mixins.CfnBotPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        log_prefix="logPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b5ab6863ebc126c74bf533b7eb4b6cf3264d672e48651e36555c8b21d91cc2e)
                check_type(argname="argument cloud_watch", value=cloud_watch, expected_type=type_hints["cloud_watch"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch is not None:
                self._values["cloud_watch"] = cloud_watch

        @builtins.property
        def cloud_watch(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CloudWatchLogGroupLogDestinationProperty"]]:
            '''Defines the Amazon CloudWatch Logs log group where text and metadata logs are delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textlogdestination.html#cfn-lex-bot-textlogdestination-cloudwatch
            '''
            result = self._values.get("cloud_watch")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.CloudWatchLogGroupLogDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.TextLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "enabled": "enabled"},
    )
    class TextLogSettingProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.TextLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Defines settings to enable text conversation logs.

            :param destination: Specifies the Amazon CloudWatch Logs destination log group for conversation text logs.
            :param enabled: Determines whether conversation logs should be stored for an alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textlogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                text_log_setting_property = lex_mixins.CfnBotPropsMixin.TextLogSettingProperty(
                    destination=lex_mixins.CfnBotPropsMixin.TextLogDestinationProperty(
                        cloud_watch=lex_mixins.CfnBotPropsMixin.CloudWatchLogGroupLogDestinationProperty(
                            cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                            log_prefix="logPrefix"
                        )
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2f31aed55ecf5fe2e73fc147f3479779cc988d04d423007554d9e27f2702942)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.TextLogDestinationProperty"]]:
            '''Specifies the Amazon CloudWatch Logs destination log group for conversation text logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textlogsetting.html#cfn-lex-bot-textlogsetting-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.TextLogDestinationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether conversation logs should be stored for an alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textlogsetting.html#cfn-lex-bot-textlogsetting-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.VoiceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"engine": "engine", "voice_id": "voiceId"},
    )
    class VoiceSettingsProperty:
        def __init__(
            self,
            *,
            engine: typing.Optional[builtins.str] = None,
            voice_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines settings for using an Amazon Polly voice to communicate with a user.

            Valid values include:

            - ``standard``
            - ``neural``
            - ``long-form``
            - ``generative``

            :param engine: Indicates the type of Amazon Polly voice that Amazon Lex should use for voice interaction with the user. For more information, see the ```engine`` parameter of the ``SynthesizeSpeech`` operation <https://docs.aws.amazon.com/polly/latest/dg/API_SynthesizeSpeech.html#polly-SynthesizeSpeech-request-Engine>`_ in the *Amazon Polly developer guide* . If you do not specify a value, the default is ``standard`` .
            :param voice_id: The identifier of the Amazon Polly voice to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-voicesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                voice_settings_property = lex_mixins.CfnBotPropsMixin.VoiceSettingsProperty(
                    engine="engine",
                    voice_id="voiceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__853f725c62e1d1d1c4402100fea573afd16d8874e9697d65d97e652dbb229c08)
                check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
                check_type(argname="argument voice_id", value=voice_id, expected_type=type_hints["voice_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if engine is not None:
                self._values["engine"] = engine
            if voice_id is not None:
                self._values["voice_id"] = voice_id

        @builtins.property
        def engine(self) -> typing.Optional[builtins.str]:
            '''Indicates the type of Amazon Polly voice that Amazon Lex should use for voice interaction with the user.

            For more information, see the ```engine`` parameter of the ``SynthesizeSpeech`` operation <https://docs.aws.amazon.com/polly/latest/dg/API_SynthesizeSpeech.html#polly-SynthesizeSpeech-request-Engine>`_ in the *Amazon Polly developer guide* .

            If you do not specify a value, the default is ``standard`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-voicesettings.html#cfn-lex-bot-voicesettings-engine
            '''
            result = self._values.get("engine")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def voice_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the Amazon Polly voice to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-voicesettings.html#cfn-lex-bot-voicesettings-voiceid
            '''
            result = self._values.get("voice_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VoiceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotPropsMixin.WaitAndContinueSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "continue_response": "continueResponse",
            "is_active": "isActive",
            "still_waiting_response": "stillWaitingResponse",
            "waiting_response": "waitingResponse",
        },
    )
    class WaitAndContinueSpecificationProperty:
        def __init__(
            self,
            *,
            continue_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            still_waiting_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.StillWaitingResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            waiting_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotPropsMixin.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the prompts that Amazon Lex uses while a bot is waiting for customer input.

            :param continue_response: The response that Amazon Lex sends to indicate that the bot is ready to continue the conversation.
            :param is_active: Specifies whether the bot will wait for a user to respond. When this field is false, wait and continue responses for a slot aren't used. If the ``IsActive`` field isn't specified, the default is true.
            :param still_waiting_response: A response that Amazon Lex sends periodically to the user to indicate that the bot is still waiting for input from the user.
            :param waiting_response: The response that Amazon Lex sends to indicate that the bot is waiting for the conversation to continue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                wait_and_continue_specification_property = lex_mixins.CfnBotPropsMixin.WaitAndContinueSpecificationProperty(
                    continue_response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                        allow_interrupt=False,
                        message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )]
                    ),
                    is_active=False,
                    still_waiting_response=lex_mixins.CfnBotPropsMixin.StillWaitingResponseSpecificationProperty(
                        allow_interrupt=False,
                        frequency_in_seconds=123,
                        message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                        timeout_in_seconds=123
                    ),
                    waiting_response=lex_mixins.CfnBotPropsMixin.ResponseSpecificationProperty(
                        allow_interrupt=False,
                        message_groups_list=[lex_mixins.CfnBotPropsMixin.MessageGroupProperty(
                            message=lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                            variations=[lex_mixins.CfnBotPropsMixin.MessageProperty(
                                custom_payload=lex_mixins.CfnBotPropsMixin.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex_mixins.CfnBotPropsMixin.ImageResponseCardProperty(
                                    buttons=[lex_mixins.CfnBotPropsMixin.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle",
                                    title="title"
                                ),
                                plain_text_message=lex_mixins.CfnBotPropsMixin.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex_mixins.CfnBotPropsMixin.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85e879ecad20eab89460be400c5243f9b9cc92c56839334b65624eddf66e0d1f)
                check_type(argname="argument continue_response", value=continue_response, expected_type=type_hints["continue_response"])
                check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
                check_type(argname="argument still_waiting_response", value=still_waiting_response, expected_type=type_hints["still_waiting_response"])
                check_type(argname="argument waiting_response", value=waiting_response, expected_type=type_hints["waiting_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if continue_response is not None:
                self._values["continue_response"] = continue_response
            if is_active is not None:
                self._values["is_active"] = is_active
            if still_waiting_response is not None:
                self._values["still_waiting_response"] = still_waiting_response
            if waiting_response is not None:
                self._values["waiting_response"] = waiting_response

        @builtins.property
        def continue_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''The response that Amazon Lex sends to indicate that the bot is ready to continue the conversation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-continueresponse
            '''
            result = self._values.get("continue_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the bot will wait for a user to respond.

            When this field is false, wait and continue responses for a slot aren't used. If the ``IsActive`` field isn't specified, the default is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def still_waiting_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.StillWaitingResponseSpecificationProperty"]]:
            '''A response that Amazon Lex sends periodically to the user to indicate that the bot is still waiting for input from the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-stillwaitingresponse
            '''
            result = self._values.get("still_waiting_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.StillWaitingResponseSpecificationProperty"]], result)

        @builtins.property
        def waiting_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]]:
            '''The response that Amazon Lex sends to indicate that the bot is waiting for the conversation to continue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-waitingresponse
            '''
            result = self._values.get("waiting_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotPropsMixin.ResponseSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WaitAndContinueSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bot_id": "botId",
        "bot_version_locale_specification": "botVersionLocaleSpecification",
        "description": "description",
    },
)
class CfnBotVersionMixinProps:
    def __init__(
        self,
        *,
        bot_id: typing.Optional[builtins.str] = None,
        bot_version_locale_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotVersionPropsMixin.BotVersionLocaleSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnBotVersionPropsMixin.

        :param bot_id: The unique identifier of the bot.
        :param bot_version_locale_specification: Specifies the locales that Amazon Lex adds to this version. You can choose the Draft version or any other previously published version for each locale. When you specify a source version, the locale data is copied from the source version to the new version.
        :param description: The description of the version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
            
            cfn_bot_version_mixin_props = lex_mixins.CfnBotVersionMixinProps(
                bot_id="botId",
                bot_version_locale_specification=[lex_mixins.CfnBotVersionPropsMixin.BotVersionLocaleSpecificationProperty(
                    bot_version_locale_details=lex_mixins.CfnBotVersionPropsMixin.BotVersionLocaleDetailsProperty(
                        source_bot_version="sourceBotVersion"
                    ),
                    locale_id="localeId"
                )],
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5dd01d1908aa20b3f906bc4bcbff840bbf729682dc515663490107b67025a64)
            check_type(argname="argument bot_id", value=bot_id, expected_type=type_hints["bot_id"])
            check_type(argname="argument bot_version_locale_specification", value=bot_version_locale_specification, expected_type=type_hints["bot_version_locale_specification"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bot_id is not None:
            self._values["bot_id"] = bot_id
        if bot_version_locale_specification is not None:
            self._values["bot_version_locale_specification"] = bot_version_locale_specification
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def bot_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the bot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-botid
        '''
        result = self._values.get("bot_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bot_version_locale_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotVersionPropsMixin.BotVersionLocaleSpecificationProperty"]]]]:
        '''Specifies the locales that Amazon Lex adds to this version.

        You can choose the Draft version or any other previously published version for each locale. When you specify a source version, the locale data is copied from the source version to the new version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-botversionlocalespecification
        '''
        result = self._values.get("bot_version_locale_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotVersionPropsMixin.BotVersionLocaleSpecificationProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBotVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBotVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotVersionPropsMixin",
):
    '''.. epigraph::

   Amazon Lex V2 is the only supported version in CloudFormation .

    Specifies a new version of the bot based on the ``DRAFT`` version. If the ``DRAFT`` version of this resource hasn't changed since you created the last version, Amazon Lex doesn't create a new version, it returns the last created version.

    When you specify the first version of a bot, Amazon Lex sets the version to 1. Subsequent versions increment by 1.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html
    :cloudformationResource: AWS::Lex::BotVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
        
        cfn_bot_version_props_mixin = lex_mixins.CfnBotVersionPropsMixin(lex_mixins.CfnBotVersionMixinProps(
            bot_id="botId",
            bot_version_locale_specification=[lex_mixins.CfnBotVersionPropsMixin.BotVersionLocaleSpecificationProperty(
                bot_version_locale_details=lex_mixins.CfnBotVersionPropsMixin.BotVersionLocaleDetailsProperty(
                    source_bot_version="sourceBotVersion"
                ),
                locale_id="localeId"
            )],
            description="description"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBotVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lex::BotVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ebe110ad87a505b7ff9153d90c875bc119467f482c69244d65eb05ea53af38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afa7ed129b9bdacdcf817852fd0c3510e781a5bd4324a0a46a0e0a8c07f25e48)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664137b46aa3bc80f62c0dd5880227a2635ad1ee2bd8d574982c6ca0dd9fd392)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBotVersionMixinProps:
        return typing.cast(CfnBotVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotVersionPropsMixin.BotVersionLocaleDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"source_bot_version": "sourceBotVersion"},
    )
    class BotVersionLocaleDetailsProperty:
        def __init__(
            self,
            *,
            source_bot_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The version of a bot used for a bot locale.

            :param source_bot_version: The version of a bot used for a bot locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocaledetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bot_version_locale_details_property = lex_mixins.CfnBotVersionPropsMixin.BotVersionLocaleDetailsProperty(
                    source_bot_version="sourceBotVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5bc6c25c5e5d601161fc02411f3b23df0fa4844fc4c39172240a8e8cf65c4236)
                check_type(argname="argument source_bot_version", value=source_bot_version, expected_type=type_hints["source_bot_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_bot_version is not None:
                self._values["source_bot_version"] = source_bot_version

        @builtins.property
        def source_bot_version(self) -> typing.Optional[builtins.str]:
            '''The version of a bot used for a bot locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocaledetails.html#cfn-lex-botversion-botversionlocaledetails-sourcebotversion
            '''
            result = self._values.get("source_bot_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotVersionLocaleDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnBotVersionPropsMixin.BotVersionLocaleSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bot_version_locale_details": "botVersionLocaleDetails",
            "locale_id": "localeId",
        },
    )
    class BotVersionLocaleSpecificationProperty:
        def __init__(
            self,
            *,
            bot_version_locale_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBotVersionPropsMixin.BotVersionLocaleDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            locale_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the locale that Amazon Lex adds to this version.

            You can choose the Draft version or any other previously published version for each locale. When you specify a source version, the locale data is copied from the source version to the new version.

            :param bot_version_locale_details: The version of a bot used for a bot locale.
            :param locale_id: The identifier of the locale to add to the version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocalespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
                
                bot_version_locale_specification_property = lex_mixins.CfnBotVersionPropsMixin.BotVersionLocaleSpecificationProperty(
                    bot_version_locale_details=lex_mixins.CfnBotVersionPropsMixin.BotVersionLocaleDetailsProperty(
                        source_bot_version="sourceBotVersion"
                    ),
                    locale_id="localeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6fb240622f5a216a0bc4790200f081aed446245f7bffcbcbf8216b376cf7afef)
                check_type(argname="argument bot_version_locale_details", value=bot_version_locale_details, expected_type=type_hints["bot_version_locale_details"])
                check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bot_version_locale_details is not None:
                self._values["bot_version_locale_details"] = bot_version_locale_details
            if locale_id is not None:
                self._values["locale_id"] = locale_id

        @builtins.property
        def bot_version_locale_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotVersionPropsMixin.BotVersionLocaleDetailsProperty"]]:
            '''The version of a bot used for a bot locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocalespecification.html#cfn-lex-botversion-botversionlocalespecification-botversionlocaledetails
            '''
            result = self._values.get("bot_version_locale_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBotVersionPropsMixin.BotVersionLocaleDetailsProperty"]], result)

        @builtins.property
        def locale_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the locale to add to the version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocalespecification.html#cfn-lex-botversion-botversionlocalespecification-localeid
            '''
            result = self._values.get("locale_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotVersionLocaleSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnResourcePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "resource_arn": "resourceArn"},
)
class CfnResourcePolicyMixinProps:
    def __init__(
        self,
        *,
        policy: typing.Any = None,
        resource_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourcePolicyPropsMixin.

        :param policy: A resource policy to add to the resource. The policy is a JSON structure that contains one or more statements that define the policy. The policy must follow IAM syntax. If the policy isn't valid, Amazon Lex returns a validation exception.
        :param resource_arn: The Amazon Resource Name (ARN) of the bot or bot alias that the resource policy is attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
            
            # policy: Any
            
            cfn_resource_policy_mixin_props = lex_mixins.CfnResourcePolicyMixinProps(
                policy=policy,
                resource_arn="resourceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b06977815ba1852e5c05d0c184d3fcf88f6c8737da31ab2f5e13eabfd7d01245)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn

    @builtins.property
    def policy(self) -> typing.Any:
        '''A resource policy to add to the resource.

        The policy is a JSON structure that contains one or more statements that define the policy. The policy must follow IAM syntax. If the policy isn't valid, Amazon Lex returns a validation exception.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html#cfn-lex-resourcepolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the bot or bot alias that the resource policy is attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html#cfn-lex-resourcepolicy-resourcearn
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
    jsii_type="@aws-cdk/mixins-preview.aws_lex.mixins.CfnResourcePolicyPropsMixin",
):
    '''.. epigraph::

   Amazon Lex V2 is the only supported version in CloudFormation .

    Specifies a new resource policy with the specified policy statements.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html
    :cloudformationResource: AWS::Lex::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lex import mixins as lex_mixins
        
        # policy: Any
        
        cfn_resource_policy_props_mixin = lex_mixins.CfnResourcePolicyPropsMixin(lex_mixins.CfnResourcePolicyMixinProps(
            policy=policy,
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
        '''Create a mixin to apply properties to ``AWS::Lex::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a2f13d349166b92a32a126bef13221e0cc43bf3d11009965507689d001b18c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c19e99b53cbb3417556a7a283cd06131bc56c71717d104f6eeee0de636b06d4d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a12595ef48c79f0fc575106bda6118a3357b71619f89d5e1348f76c4c18eaf07)
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


__all__ = [
    "CfnBotAliasMixinProps",
    "CfnBotAliasPropsMixin",
    "CfnBotMixinProps",
    "CfnBotPropsMixin",
    "CfnBotVersionMixinProps",
    "CfnBotVersionPropsMixin",
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
]

publication.publish()

def _typecheckingstub__6079d85d5535c384e30d8c597d5dd7fabe1a6d01a77b9d493efaf7442c071263(
    *,
    bot_alias_locale_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.BotAliasLocaleSettingsItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    bot_alias_name: typing.Optional[builtins.str] = None,
    bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    bot_id: typing.Optional[builtins.str] = None,
    bot_version: typing.Optional[builtins.str] = None,
    conversation_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.ConversationLogSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    sentiment_analysis_settings: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a2da524674a6a01c96e3d2a38a8868f8c1e9224a3674ca288aec940a1ec578(
    props: typing.Union[CfnBotAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09ecbc7ee9804e201de495189e09d28d96f96da5c00a884265f607c94a62f7d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3190f32c765700f1fb75bf551f9d0440736c0cf334570089fd93c9730561beb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d90832be5701f13f7f952a08cdc22d03c3f3c9d9c3c051f35fc32b9345f8da(
    *,
    s3_bucket: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.S3BucketLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deff21b209b3fe3bbe7eb50443e04a454edaeaf54e7df10487a9fcfb203cd8a9(
    *,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.AudioLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48f67a05123c3bf05595dc0fa5fc9bcf8306a8e58bc6d57618e48bd6395bb9a(
    *,
    bot_alias_locale_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.BotAliasLocaleSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    locale_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4b3643d7b1fcb39a7c028b7560a10068b97c72af2b2e141a82e44986c46e28(
    *,
    code_hook_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.CodeHookSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad37fface3c3411fc449d82424b14f27a363a2966bae32724507d84a547d08b(
    *,
    cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
    log_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6479f0fe12e9c75039408671ec26a2f1b077d9f7f7962f60e8ee421999943bb3(
    *,
    lambda_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.LambdaCodeHookProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bf94cfd7cd760dd12f0b11ff76a8b51994f1fe18a799da64ba5def60c123da(
    *,
    audio_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.AudioLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    text_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.TextLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510cf49d7edc2082a0485f1317f4d11448d47e422b9866747b49fe3c932d9da3(
    *,
    code_hook_interface_version: typing.Optional[builtins.str] = None,
    lambda_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340b02752f604b7faeffda18cb5fb1c33994c2743cc921e6f775471e211eefc9(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    log_prefix: typing.Optional[builtins.str] = None,
    s3_bucket_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfddf9a59cb60489978bba2af4978abd91049c87bfa2d6e03bc17556ce5ebdc3(
    *,
    detect_sentiment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a8281d0f49a02512996e751eb35c29b06b033ef5a529c0a3a58d6794b70be0(
    *,
    cloud_watch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.CloudWatchLogGroupLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6c629db12a08bcbed282c8567199be27b25d5174326f8da9c7b4002d1fa872(
    *,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotAliasPropsMixin.TextLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac4a5f33e7bcb194db79dade839c925e94f2ed71707f811e1264cd03da7331a(
    *,
    auto_build_bot_locales: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    bot_file_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bot_locales: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BotLocaleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    bot_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    data_privacy: typing.Any = None,
    description: typing.Optional[builtins.str] = None,
    error_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ErrorLogSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    idle_session_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    replication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ReplicationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    test_bot_alias_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.TestBotAliasSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    test_bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a72e8cef14da203cbe64e3cdee10c62ee8d0c1280398eea76fb0d4c3ba784d(
    props: typing.Union[CfnBotMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f010adfc261d26131b656df83cf25b09dea5ab528d8c10653d8eb4698bf03496(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84c20790560b99ec7c13569f060c9a24d86f85d417daee6a29736ec4e440c7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c0c24e0e67a695c82627d95be037d05d2365b0d7eee65ec23e450301de8924(
    *,
    audio_recognition_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db718b6a1127bddbf4f3f8c9a58c249b627856a20570d8af9409008bf31fab37(
    *,
    allow_audio_input: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    allow_dtmf_input: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebd7e13b0d7e1091e72d60c2f3252e8a83e558c66cb44e5d3e77e17c3db2775(
    *,
    audio_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.AudioSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dtmf_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DTMFSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_timeout_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f15742a318baf397d12e9b34cf81cdbf3b2663f5f307195a9a26794152033d(
    *,
    s3_bucket: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.S3BucketLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492df9a0be37577091f5ca90cf7273ee66d12cb52bb0f58a8f16044f2b9d5d32(
    *,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.AudioLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b72d80dee15336a528f96ef836b2893e1d6e2ae3f970220859f0beadb41ec41(
    *,
    end_timeout_ms: typing.Optional[jsii.Number] = None,
    max_length_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3366b6d616c8610541175c5fa439ebb0948d9ca21c73eac6f72061667400d29(
    *,
    answer_field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab7eb2b33dbad5e3932abb44e75d3a903e4e3292e55739cd6c8693863e3db3f(
    *,
    bedrock_agent_alias_id: typing.Optional[builtins.str] = None,
    bedrock_agent_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35591dafaa33a797121ef28b53474e4cd4717d9087fa7fed06fe5a7264b4a8cd(
    *,
    bedrock_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BedrockAgentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bedrock_agent_intent_knowledge_base_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BedrockAgentIntentKnowledgeBaseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df08bfc9575cf7f6b561aacd127b8bbc920209a5b931a79e6b7face9cc48080(
    *,
    bedrock_knowledge_base_arn: typing.Optional[builtins.str] = None,
    bedrock_model_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BedrockModelSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c8e4bb8569909355e9c8e82810c046ddbc12d4d77aa6b525f97006d392d0fa(
    *,
    bedrock_guardrail_identifier: typing.Optional[builtins.str] = None,
    bedrock_guardrail_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659010913dacf5dc1afa2280f7c714558e3e52213f0a82ac4ddf7f2d7a573673(
    *,
    bedrock_knowledge_base_arn: typing.Optional[builtins.str] = None,
    bkb_exact_response_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BKBExactResponseFieldsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exact_response: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fb56b72b629e63eb7265407b77e6d7c0d666a6e4a034e85646530feacbb10e(
    *,
    bedrock_guardrail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BedrockGuardrailConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bedrock_model_custom_prompt: typing.Optional[builtins.str] = None,
    bedrock_trace_status: typing.Optional[builtins.str] = None,
    model_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38269c5ab5f29b10562472cb6d0c63741ec14908fc1e4ca80a27b4750867434f(
    *,
    bot_alias_locale_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BotAliasLocaleSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    locale_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1cde1bb50c6d19ef7f5eb02cfbe37e80b13cd1c3906fce7776f5e5414d4b8d(
    *,
    code_hook_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.CodeHookSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d36c996917176b42491668d78625d07102ace7655cecb2eeca1517b7479ce5(
    *,
    custom_vocabulary: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.CustomVocabularyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    generative_ai_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.GenerativeAISettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    intents: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.IntentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    locale_id: typing.Optional[builtins.str] = None,
    nlu_confidence_threshold: typing.Optional[jsii.Number] = None,
    slot_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    voice_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.VoiceSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bdbb9be3e73758fee04ccc235043e7c59e6bb257c9c3d14067f8f414000b877(
    *,
    descriptive_bot_builder_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DescriptiveBotBuilderSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sample_utterance_generation_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SampleUtteranceGenerationSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99fcbaa96157542656ba47f9b8dacba8ae8997d0c3f2bab638984a46b2b79255(
    *,
    text: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e60eb78e5ada2758cfe120ad0d042ef68da9062be8837c64c9af082f2b64ec(
    *,
    cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
    log_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3bff33d8e74167e1325ebb90411ed92af1a71324991bac9bb176acef7dfd0e0(
    *,
    lambda_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.LambdaCodeHookProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fd1659b247fab888e597c395fb5a2b740c469ff11757eab22daa530b4efc4c(
    *,
    sub_slots: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SubSlotTypeCompositionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab749316927b3b54329167583d0ed1d3d12db16baf230f76c73639c5d448011(
    *,
    expression_string: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56c9ca08d611d28b7cfde0f282adcf40a6cfb2774e949ff7f23378842f3abe7(
    *,
    condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb9ecab271de3afc2a8bde8f62c8387c28d60e0687ebfe275f2210a00f6f450(
    *,
    conditional_branches: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalBranchProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    default_branch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DefaultConditionalBranchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113c49f318bff2e0276e726a04305e636183bc48326a684cdf33eee8a8837497(
    *,
    audio_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.AudioLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    text_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.TextLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8366ef501a8b6378b6bc25efa5baf0f9e8bc9ca1e05f3fc82f6f2cbc861bd28b(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7784c746e0f3279a959afc9372a7f8a825c67ba086e6b0e673f843d701ae81(
    *,
    display_as: typing.Optional[builtins.str] = None,
    phrase: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a0a9b2e413a868854da1118ffd6c780002804c5eae16b26747ce4d79104459(
    *,
    custom_vocabulary_items: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.CustomVocabularyItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c93b03e650f2344eb890ed8742ca1b0880d74b4cbff0d8e0445fa9c184c03c0(
    *,
    deletion_character: typing.Optional[builtins.str] = None,
    end_character: typing.Optional[builtins.str] = None,
    end_timeout_ms: typing.Optional[jsii.Number] = None,
    max_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb3d810a57ac9798a6a9bcb0858d6e0908b9ccd4312253ebb92a97a5ea1302f(
    *,
    child_directed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ad5b3a5060ea26a12ea230edddcfd6bafb3bdc8dfa530f9b1de26f2694d606(
    *,
    bedrock_knowledge_store_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BedrockKnowledgeStoreConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kendra_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.QnAKendraConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    opensearch_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.OpensearchConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059cf477d6f31f817dfc1035e3bd573c437589794a5a19a8a60de9954857fc0c(
    *,
    next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db4f05d8f5e87c14d2812d283dbbd2f4ec0ce2b5e578de5f79acc1bd9b1beef(
    *,
    bedrock_model_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BedrockModelSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b875ee39716965e17b62c7b6d17fdfc8a09950f07c861e597405862f68b96630(
    *,
    slot_to_elicit: typing.Optional[builtins.str] = None,
    suppress_next_message: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5c8449c0054556f25620d50ae04a518ff060369080f98a3bc23f7c36fac499(
    *,
    enable_code_hook_invocation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    invocation_label: typing.Optional[builtins.str] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    post_code_hook_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.PostDialogCodeHookInvocationSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a421ef9e9fe1c0361265b299e843b8d84936a9a83ba9031946cb3893910d9ef5(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0c0637863f78a3572bda1d772b247e0f042ee3b4cf63c45ea6c6cf6bb2fd7b(
    *,
    dialog_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    intent: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.IntentOverrideProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    session_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SessionAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36de176b0f26ffe375e4a46f6f82085758072a64ee40a9a5006132e77a618c34(
    *,
    enable_code_hook_invocation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    invocation_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab659331081ac4e213b56b601033fc9c7842d266c1ecd4c3480eb00414d19490(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8082251912df13afedc67c6b605721e88fc47f81033b35f5f90334abcaa03623(
    *,
    answer_field: typing.Optional[builtins.str] = None,
    question_field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f7d773ce964591c88fcb10a844b20cd010ff4bab91ff474edac8945bdba658(
    *,
    grammar_slot_type_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.GrammarSlotTypeSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0bc4b7c6f5b2dccaa3f8cc45f5e4383a7f77e96994a95fc8a47d67aa92fb76(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    fulfillment_updates_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.FulfillmentUpdatesSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    post_fulfillment_status_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.PostFulfillmentStatusSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf62733b4d727ebfa9cc7347f0b8d2cf6e70ad18da2fc8f91ef32b722809722(
    *,
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    delay_in_seconds: typing.Optional[jsii.Number] = None,
    message_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.MessageGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef548033d673ec60fba04a94fa33f6361c5a647efaa5dbacd1025f8d2656101(
    *,
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    frequency_in_seconds: typing.Optional[jsii.Number] = None,
    message_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.MessageGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15be51185c33abd8b0a3624944c1cbe01f3ba29d2f583eb40bab8bc00cac40d8(
    *,
    active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    start_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.FulfillmentStartResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
    update_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.FulfillmentUpdateResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a80e3e6df1d385566e495e03b3aab93f98b594c18661824afe466bcb6566a34(
    *,
    buildtime_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BuildtimeSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    runtime_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.RuntimeSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360c21d74df59ee2ffb166c206ccadcb4536eccadedeb5bd70b5bf2b71ee76fe(
    *,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.GrammarSlotTypeSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8bb0e7e63285c76067688f00e4240eb16bbc00dc6505938c4898a9d3595ade0(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_object_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40505c8cf59be20d31311744201fd37b0933075f3895acc6d51796a4fbe32c34(
    *,
    buttons: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ButtonProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    image_url: typing.Optional[builtins.str] = None,
    subtitle: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da8189b0690992713156d1c916794d5aa830b067c2d4420e79221d2a1d62243(
    *,
    code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    initial_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19113d1a9f5e477f3c0e3b08d988b3657244fc8f57f7e2731fcffe4fad11357b(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4ae10c12927d6b59dd394c92bc766c45745408310c7889d71488d94382449d(
    *,
    closing_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e32c3e61367112a0caee14981650918a0b46ddcf4cfb88c25c10e8d063fa73f4(
    *,
    code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    confirmation_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    confirmation_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    confirmation_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    declination_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    declination_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    declination_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    elicitation_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ElicitationCodeHookInvocationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    prompt_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.PromptSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3cbe6cf71378db85833b271fee2cc414c522c861515c73f4fb3344491bf413(
    *,
    name: typing.Optional[builtins.str] = None,
    slots: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotValueOverrideMapProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f88d897d52eafda4e74a7892ba13638224db7c4b10233ae6015156b1c14eac(
    *,
    bedrock_agent_intent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BedrockAgentIntentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dialog_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogCodeHookSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fulfillment_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.FulfillmentCodeHookSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    initial_response_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.InitialResponseSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_contexts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.InputContextProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    intent_closing_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.IntentClosingSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    intent_confirmation_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.IntentConfirmationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kendra_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.KendraConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    output_contexts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.OutputContextProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    parent_intent_signature: typing.Optional[builtins.str] = None,
    q_in_connect_intent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.QInConnectIntentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    qn_a_intent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.QnAIntentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sample_utterances: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SampleUtteranceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    slot_priorities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotPriorityProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    slots: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05e0e9fe0e724ea0fb853c890ae2b54108a2b759f3d7015b55f620df5446812(
    *,
    kendra_index: typing.Optional[builtins.str] = None,
    query_filter_string: typing.Optional[builtins.str] = None,
    query_filter_string_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffe74f5665440436863dffd772c6e38ab14afbc687428c64a84d9d2a46a9bec(
    *,
    code_hook_interface_version: typing.Optional[builtins.str] = None,
    lambda_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de68416995a7d0e740c8ce3690b6fe2958503b7a25a60bc302e2fa7fea3e9d6a(
    *,
    message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    variations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.MessageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fe24f2614c700234a6670ece931ab046dd65894f3ff64dd619d8110fe3934d(
    *,
    custom_payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.CustomPayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_response_card: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ImageResponseCardProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    plain_text_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.PlainTextMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ssml_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SSMLMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5acc6b38461fc73a7d2c77daf1f5b9f46dafdd3375ed5d630e24b5fb2dae2567(
    *,
    allow_multiple_values: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0a290ff304e57480e617ce5bdc0d56ce9c8369e1fdc7054e67601e5e6629e0(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a2701e94a821c99267294386b80741167e11044c45cde283804cc4e9575434(
    *,
    obfuscation_setting_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d102228d13838a4d5c96d8d75b0854c295f8e72778e50de2cf8c471c492f36(
    *,
    domain_endpoint: typing.Optional[builtins.str] = None,
    exact_response: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exact_response_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ExactResponseFieldsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    index_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1472a4f210d1fd3a23b6ae4fb7ce09dc84a4ca997f5ae72563562a35d8cf2901(
    *,
    name: typing.Optional[builtins.str] = None,
    time_to_live_in_seconds: typing.Optional[jsii.Number] = None,
    turns_to_live: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565a99939706792555eafc800aec33f6bc83523e7aa8455df3cb3a957ce6b077(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b899d468c4e74ddecfc34fc28da9adbf20a8c8ab833838e59db6877ed130ed2(
    *,
    failure_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    success_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    success_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    success_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8de61f97f2842db249bc935e31e7940895ffbb6c30f775f83aeb11496efebc(
    *,
    failure_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    success_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    success_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    success_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eedf16d9621b254ffb918447b2ad27a935b9c03d13f6f064006aa8eb3dc97ba2(
    *,
    allowed_input_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.AllowedInputTypesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    audio_and_dtmf_input_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.AudioAndDTMFInputSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    text_input_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.TextInputSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6afc681c475db307a7aca6ac5bbd72e1f5cc036e5ef3c9e868a9ccda1eade736(
    *,
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    message_groups_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.MessageGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    message_selection_strategy: typing.Optional[builtins.str] = None,
    prompt_attempts_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.PromptAttemptSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49845c06facfd91dcd9619e8f0098989e82acff4ce64800a8d66c6d70800ad33(
    *,
    assistant_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b25fe7a36e5d801900608655a42bb93883ddced423648863848b5491a4ebea7(
    *,
    q_in_connect_assistant_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.QInConnectAssistantConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140ec5fc6ebeef41ead0e6508639e5a1be82ca1471324e65a04493dbc49336b1(
    *,
    bedrock_model_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BedrockModelSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c02a0061ccbbf87713710ab615384211ad1e09823899eefcb92e7aac4e569e(
    *,
    exact_response: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kendra_index: typing.Optional[builtins.str] = None,
    query_filter_string: typing.Optional[builtins.str] = None,
    query_filter_string_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbad0edd82d69d664c704e16caf8a4671e0aa4a89af09b8d557b21164b503c16(
    *,
    replica_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f723381ec94360d7ebb69881c83d19e510b5826884d9d8ce0192c084feb5a577(
    *,
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    message_groups_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.MessageGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5567e184a7a4cfcbb80491aef2d02a77bc0847242b295e0d79743fc62b63b1aa(
    *,
    nlu_improvement_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.NluImprovementSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    slot_resolution_improvement_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotResolutionImprovementSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081f84e73f36dfcfe426ced5c283e205a0aeef6c5106884195da17b75c2b7fdf(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    log_prefix: typing.Optional[builtins.str] = None,
    s3_bucket_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a328f9a1251122a879b031d2325776910ff106c6668bfe5b0ee69323a29177(
    *,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_object_key: typing.Optional[builtins.str] = None,
    s3_object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3249e67130a741ff514fbd680fa66473665f225585b3a74cd4a708b1f059ac78(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ce0d0f89b5f51b10f45b5bc5da7b1b9f7503ba4a055c63c92d6be0d0baecc9(
    *,
    bedrock_model_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BedrockModelSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5357747a796b2a30aa99351d9fbf3eb5ec78f70141de59d20fbfa4b1db36c440(
    *,
    utterance: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532696af8055940c66022851d1d48e6dcaaa30f80fd56a04e47eddf5e1bbe0f2(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6312813cc88dda00de88e9b5615a28782a4c6f94e05eb1411bde09c1a0122bfc(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8a4cb1c7d82e13904e8dc88e9981a9361e456f84266af9072df698d0e6ca55(
    *,
    capture_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    capture_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    capture_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogCodeHookInvocationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    elicitation_code_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ElicitationCodeHookInvocationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_conditional: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConditionalSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_next_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.DialogStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b085105fcccddae011aba2804d02726128c64256df2c3ed95253e1a0f8b07073(
    *,
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5660de403be1bf600d769ee088f82d679ad062280e19dc48f01f0330917874(
    *,
    default_value_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotDefaultValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd579b2a44a4cfe7b21b3216502a63b58aa84b52e33912d018fa5e2659c40e29(
    *,
    priority: typing.Optional[jsii.Number] = None,
    slot_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7a483dc93bb09e61b7e9ffdc58c77a946534e34e6d03f3e95bc339cfb8b979(
    *,
    description: typing.Optional[builtins.str] = None,
    multiple_values_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.MultipleValuesSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    obfuscation_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ObfuscationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    slot_type_name: typing.Optional[builtins.str] = None,
    sub_slot_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SubSlotSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    value_elicitation_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotValueElicitationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08c68b5de0020252e2289b3102723c4fc1641e18f3b3d6e382d94a597078410(
    *,
    bedrock_model_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BedrockModelSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f0a5308d0ffbbec2fb32dc8d706c5644d80f7063bf6a53a8b75aad53d70765(
    *,
    composite_slot_type_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.CompositeSlotTypeSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    external_source_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ExternalSourceSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    parent_slot_type_signature: typing.Optional[builtins.str] = None,
    slot_type_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotTypeValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    value_selection_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotValueSelectionSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d28b5c5134b7b57121fab62d5ddde29cce3070b37e45d16f0dcbbf2f0c79c9(
    *,
    sample_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SampleValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    synonyms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SampleValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3279244dfa62342c89eb8fa1aca2d728b420a8b9864ba2bd72039dd6e8bf87(
    *,
    default_value_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotDefaultValueSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    prompt_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.PromptSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sample_utterances: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SampleUtteranceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    slot_capture_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotCaptureSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    slot_constraint: typing.Optional[builtins.str] = None,
    wait_and_continue_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.WaitAndContinueSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd83ed701c5b2837dc440104e76be884cea2bcaa4bf034af2f6bd9630f3305e(
    *,
    slot_name: typing.Optional[builtins.str] = None,
    slot_value_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotValueOverrideProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6191fceac735782077bdef6c412368d7fcbb2736a87cafcea2e9edcb3fc4a6(
    *,
    shape: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotValueOverrideProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d669e29951b9ae8f2c44d7cd7bb6b088a22b4b01231bd4dd467943c4dd694208(
    *,
    interpreted_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ea3a466a035d41b25d8936582ca55ae982748a289284b6a6f946c560e5d456(
    *,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a636eac5be6a1130c83d63896c1bd4315750e12f0977c183816c0c9e2f6130(
    *,
    advanced_recognition_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.AdvancedRecognitionSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotValueRegexFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resolution_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab89958e4e25fb39804c3df41bf036f2603561f6275bb26cf1a7775a0454af0(
    *,
    slot_type_id: typing.Optional[builtins.str] = None,
    value_elicitation_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SubSlotValueElicitationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6b0bd695507fccfe55b0ce800ca8c48ee4744c2a773d7cdad25710ca2b85a5(
    *,
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    frequency_in_seconds: typing.Optional[jsii.Number] = None,
    message_groups_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.MessageGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34900e32148623a9b989e0303eda0659dd8cb2630db428b666de131c19692e6(
    *,
    expression: typing.Optional[builtins.str] = None,
    slot_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SpecificationsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a3499deee04a0e37b23ecc1bde2163f9aa5c788e32ad476a8fff901303615b(
    *,
    name: typing.Optional[builtins.str] = None,
    slot_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe56ddb90b1a5ac3790448f4556c0750a94562d67a3e7f12b3c0cedb29cb562(
    *,
    default_value_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SlotDefaultValueSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    prompt_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.PromptSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sample_utterances: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.SampleUtteranceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    wait_and_continue_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.WaitAndContinueSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25855e553d9544abbc3ff607d7b06203d0eb6d03b6bf3202a437bf007b07275(
    *,
    bot_alias_locale_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.BotAliasLocaleSettingsItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    conversation_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ConversationLogSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    sentiment_analysis_settings: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730e40de73dfd22ba0db0d5c925c86a924d892b29915722c51234123e4cc932d(
    *,
    start_timeout_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5ab6863ebc126c74bf533b7eb4b6cf3264d672e48651e36555c8b21d91cc2e(
    *,
    cloud_watch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.CloudWatchLogGroupLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f31aed55ecf5fe2e73fc147f3479779cc988d04d423007554d9e27f2702942(
    *,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.TextLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853f725c62e1d1d1c4402100fea573afd16d8874e9697d65d97e652dbb229c08(
    *,
    engine: typing.Optional[builtins.str] = None,
    voice_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e879ecad20eab89460be400c5243f9b9cc92c56839334b65624eddf66e0d1f(
    *,
    continue_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    still_waiting_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.StillWaitingResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    waiting_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotPropsMixin.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5dd01d1908aa20b3f906bc4bcbff840bbf729682dc515663490107b67025a64(
    *,
    bot_id: typing.Optional[builtins.str] = None,
    bot_version_locale_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotVersionPropsMixin.BotVersionLocaleSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ebe110ad87a505b7ff9153d90c875bc119467f482c69244d65eb05ea53af38(
    props: typing.Union[CfnBotVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa7ed129b9bdacdcf817852fd0c3510e781a5bd4324a0a46a0e0a8c07f25e48(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664137b46aa3bc80f62c0dd5880227a2635ad1ee2bd8d574982c6ca0dd9fd392(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc6c25c5e5d601161fc02411f3b23df0fa4844fc4c39172240a8e8cf65c4236(
    *,
    source_bot_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb240622f5a216a0bc4790200f081aed446245f7bffcbcbf8216b376cf7afef(
    *,
    bot_version_locale_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBotVersionPropsMixin.BotVersionLocaleDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    locale_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06977815ba1852e5c05d0c184d3fcf88f6c8737da31ab2f5e13eabfd7d01245(
    *,
    policy: typing.Any = None,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a2f13d349166b92a32a126bef13221e0cc43bf3d11009965507689d001b18c(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19e99b53cbb3417556a7a283cd06131bc56c71717d104f6eeee0de636b06d4d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12595ef48c79f0fc575106bda6118a3357b71619f89d5e1348f76c4c18eaf07(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
