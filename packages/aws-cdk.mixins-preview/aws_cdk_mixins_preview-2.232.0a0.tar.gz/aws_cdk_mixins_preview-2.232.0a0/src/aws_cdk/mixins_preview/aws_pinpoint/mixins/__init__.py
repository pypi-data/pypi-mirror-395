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
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnADMChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "enabled": "enabled",
    },
)
class CfnADMChannelMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnADMChannelPropsMixin.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the ADM channel applies to.
        :param client_id: The Client ID that you received from Amazon to send messages by using ADM.
        :param client_secret: The Client Secret that you received from Amazon to send messages by using ADM.
        :param enabled: Specifies whether to enable the ADM channel for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_aDMChannel_mixin_props = pinpoint_mixins.CfnADMChannelMixinProps(
                application_id="applicationId",
                client_id="clientId",
                client_secret="clientSecret",
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd9aaddc35d0385416911df2379f7ada44ebee4c28281f27a5fa4535c8fe32a)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that the ADM channel applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The Client ID that you received from Amazon to send messages by using ADM.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientid
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The Client Secret that you received from Amazon to send messages by using ADM.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientsecret
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable the ADM channel for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnADMChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnADMChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnADMChannelPropsMixin",
):
    '''A *channel* is a type of platform that you can deliver messages to.

    You can use the ADM channel to send push notifications through the Amazon Device Messaging (ADM) service to apps that run on Amazon devices, such as Kindle Fire tablets. Before you can use Amazon Pinpoint to send messages to Amazon devices, you have to enable the ADM channel for an Amazon Pinpoint application.

    The ADMChannel resource represents the status and authentication settings for the ADM channel for an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html
    :cloudformationResource: AWS::Pinpoint::ADMChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_aDMChannel_props_mixin = pinpoint_mixins.CfnADMChannelPropsMixin(pinpoint_mixins.CfnADMChannelMixinProps(
            application_id="applicationId",
            client_id="clientId",
            client_secret="clientSecret",
            enabled=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnADMChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::ADMChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8473e5cf4df9904b17c4d495fa8e09fd3aecb24eb592dd7043390d25aceb9542)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22ce4ef4965fdf25cc0bc888d500e8a938be46c6fcd8777b38322dae02ecd688)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9df8762cce9bbf8b252a299a5206e1c0f9cce1e823bebc49c66a488f4424f32)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnADMChannelMixinProps:
        return typing.cast(CfnADMChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnAPNSChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSChannelMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAPNSChannelPropsMixin.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs channel for the application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_aPNSChannel_mixin_props = pinpoint_mixins.CfnAPNSChannelMixinProps(
                application_id="applicationId",
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc8d7f608458c01f5acac9da9852a83ee6aebb88121347dd44bda90e40250ca)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that the APNs channel applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable the APNs channel for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAPNSChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnAPNSChannelPropsMixin",
):
    '''A *channel* is a type of platform that you can deliver messages to.

    You can use the APNs channel to send push notification messages to the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send notifications to APNs, you have to enable the APNs channel for an Amazon Pinpoint application.

    The APNSChannel resource represents the status and authentication settings for the APNs channel for an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html
    :cloudformationResource: AWS::Pinpoint::APNSChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_aPNSChannel_props_mixin = pinpoint_mixins.CfnAPNSChannelPropsMixin(pinpoint_mixins.CfnAPNSChannelMixinProps(
            application_id="applicationId",
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAPNSChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::APNSChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0381bd02b7c3e926ca9ada83ed905dcff7c6293a19c98c715717e28f99da844)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fc6d56dd19d32bec1bc9a7e1bc7e7a643b7780477601eead712052fd3b0f2b5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3646761d54d51fe582cefacfeca585cf3a0413fa44520265ece033426623a1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAPNSChannelMixinProps:
        return typing.cast(CfnAPNSChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnAPNSSandboxChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSSandboxChannelMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAPNSSandboxChannelPropsMixin.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs sandbox channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs Sandbox channel for the Amazon Pinpoint application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_aPNSSandbox_channel_mixin_props = pinpoint_mixins.CfnAPNSSandboxChannelMixinProps(
                application_id="applicationId",
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b165a667eb6248aca8784274b7960b0794cd7023a017460473d825383f1c4b)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that the APNs sandbox channel applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable the APNs Sandbox channel for the Amazon Pinpoint application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSSandboxChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAPNSSandboxChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnAPNSSandboxChannelPropsMixin",
):
    '''A *channel* is a type of platform that you can deliver messages to.

    You can use the APNs sandbox channel to send push notification messages to the sandbox environment of the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send notifications to the APNs sandbox environment, you have to enable the APNs sandbox channel for an Amazon Pinpoint application.

    The APNSSandboxChannel resource represents the status and authentication settings of the APNs sandbox channel for an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html
    :cloudformationResource: AWS::Pinpoint::APNSSandboxChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_aPNSSandbox_channel_props_mixin = pinpoint_mixins.CfnAPNSSandboxChannelPropsMixin(pinpoint_mixins.CfnAPNSSandboxChannelMixinProps(
            application_id="applicationId",
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAPNSSandboxChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::APNSSandboxChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad32dbf8b1268208013e4e20244952c8f6b018f2b6e43e3fdd595947a5d560e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edf3031aecefa9800ff9206dfffd8b7cc09fa63443de5d448d960945ea4dd93c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5164447deca46281aa430dcf5efe8b0a13c0f78adf2090c107535994f4d7f68e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAPNSSandboxChannelMixinProps:
        return typing.cast(CfnAPNSSandboxChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnAPNSVoipChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSVoipChannelMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAPNSVoipChannelPropsMixin.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs VoIP channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs VoIP channel for the Amazon Pinpoint application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_aPNSVoip_channel_mixin_props = pinpoint_mixins.CfnAPNSVoipChannelMixinProps(
                application_id="applicationId",
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16903d719b59deb65b078d33eac5ab412c6b72ba09274f3c2c3e45e84abc1f0e)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that the APNs VoIP channel applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable the APNs VoIP channel for the Amazon Pinpoint application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSVoipChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAPNSVoipChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnAPNSVoipChannelPropsMixin",
):
    '''A *channel* is a type of platform that you can deliver messages to.

    You can use the APNs VoIP channel to send VoIP notification messages to the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send VoIP notifications to APNs, you have to enable the APNs VoIP channel for an Amazon Pinpoint application.

    The APNSVoipChannel resource represents the status and authentication settings of the APNs VoIP channel for an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html
    :cloudformationResource: AWS::Pinpoint::APNSVoipChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_aPNSVoip_channel_props_mixin = pinpoint_mixins.CfnAPNSVoipChannelPropsMixin(pinpoint_mixins.CfnAPNSVoipChannelMixinProps(
            application_id="applicationId",
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAPNSVoipChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::APNSVoipChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d76d69e4778dec3aeac9fb5a4265a25ba4678af7422c8ebd07fb25f3100d4ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef33ec8dd7ce1b34df8e7ae1c6f7c4e11089264241e8204fb450d680e882073c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60336d77c42ef655c91ba776467681f596d46ba0e0f6aee05a38a34effbd348b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAPNSVoipChannelMixinProps:
        return typing.cast(CfnAPNSVoipChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnAPNSVoipSandboxChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSVoipSandboxChannelMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAPNSVoipSandboxChannelPropsMixin.

        :param application_id: The unique identifier for the application that the APNs VoIP sandbox channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether the APNs VoIP sandbox channel is enabled for the application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with the APNs sandbox environment.
        :param team_id: The identifier that's assigned to your Apple developer account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_aPNSVoip_sandbox_channel_mixin_props = pinpoint_mixins.CfnAPNSVoipSandboxChannelMixinProps(
                application_id="applicationId",
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a6ac24da8053f25d433b758d19468fd03e7ab643da46af34db23f3b9fbb66b6)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the application that the APNs VoIP sandbox channel applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using an APNs certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the APNs VoIP sandbox channel is enabled for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with the APNs sandbox environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple developer account team.

        This identifier is used for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using APNs tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSVoipSandboxChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAPNSVoipSandboxChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnAPNSVoipSandboxChannelPropsMixin",
):
    '''A *channel* is a type of platform that you can deliver messages to.

    You can use the APNs VoIP sandbox channel to send VoIP notification messages to the sandbox environment of the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send VoIP notifications to the APNs sandbox environment, you have to enable the APNs VoIP sandbox channel for an Amazon Pinpoint application.

    The APNSVoipSandboxChannel resource represents the status and authentication settings of the APNs VoIP sandbox channel for an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html
    :cloudformationResource: AWS::Pinpoint::APNSVoipSandboxChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_aPNSVoip_sandbox_channel_props_mixin = pinpoint_mixins.CfnAPNSVoipSandboxChannelPropsMixin(pinpoint_mixins.CfnAPNSVoipSandboxChannelMixinProps(
            application_id="applicationId",
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAPNSVoipSandboxChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::APNSVoipSandboxChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__683281e55c7b65544c176020ab52ba1166b64ec53a5930aa30d844e0d9f63cbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__897b7ea05d6013b050f4e84a2d195e4886473b26336c895c4364f554d9d1e461)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35fa32e568b247badd1c8209709d12476c4289d6e7cfb3d14bd08326778ce4b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAPNSVoipSandboxChannelMixinProps:
        return typing.cast(CfnAPNSVoipSandboxChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnAppMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags"},
)
class CfnAppMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnAppPropsMixin.

        :param name: The display name of the application.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            # tags: Any
            
            cfn_app_mixin_props = pinpoint_mixins.CfnAppMixinProps(
                name="name",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36725735f25e88f9303233468d9af0c98a239c29a0e27de053bd0fa7c91407f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The display name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAppPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnAppPropsMixin",
):
    '''An *app* is an Amazon Pinpoint application, also referred to as a *project* .

    An application is a collection of related settings, customer information, segments, campaigns, and other types of Amazon Pinpoint resources.

    The App resource represents an Amazon Pinpoint application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html
    :cloudformationResource: AWS::Pinpoint::App
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        # tags: Any
        
        cfn_app_props_mixin = pinpoint_mixins.CfnAppPropsMixin(pinpoint_mixins.CfnAppMixinProps(
            name="name",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAppMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::App``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12906bbe11a3cc27828a64ba49fd3afae517fcde1a3d553986befb538f7e48c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f583d4b8d624135ee33bddec2038d5ad538ed994de8164c31fd8ef4655da457)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f643db60a88118870236b25f454d752e54044dc3aa3c79ce48c7278a10f04f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAppMixinProps:
        return typing.cast(CfnAppMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnApplicationSettingsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "campaign_hook": "campaignHook",
        "cloud_watch_metrics_enabled": "cloudWatchMetricsEnabled",
        "limits": "limits",
        "quiet_time": "quietTime",
    },
)
class CfnApplicationSettingsMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        campaign_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationSettingsPropsMixin.CampaignHookProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationSettingsPropsMixin.LimitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        quiet_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationSettingsPropsMixin.QuietTimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationSettingsPropsMixin.

        :param application_id: The unique identifier for the Amazon Pinpoint application.
        :param campaign_hook: The settings for the Lambda function to use by default as a code hook for campaigns in the application. To override these settings for a specific campaign, use the Campaign resource to define custom Lambda function settings for the campaign.
        :param cloud_watch_metrics_enabled: 
        :param limits: The default sending limits for campaigns in the application. To override these limits for a specific campaign, use the Campaign resource to define custom limits for the campaign.
        :param quiet_time: The default quiet time for campaigns in the application. Quiet time is a specific time range when campaigns don't send messages to endpoints, if all the following conditions are met: - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value. - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the application (or a campaign that has custom quiet time settings). - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the application (or a campaign that has custom quiet time settings). If any of the preceding conditions isn't met, the endpoint will receive messages from a campaign, even if quiet time is enabled. To override the default quiet time settings for a specific campaign, use the Campaign resource to define a custom quiet time for the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_application_settings_mixin_props = pinpoint_mixins.CfnApplicationSettingsMixinProps(
                application_id="applicationId",
                campaign_hook=pinpoint_mixins.CfnApplicationSettingsPropsMixin.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                ),
                cloud_watch_metrics_enabled=False,
                limits=pinpoint_mixins.CfnApplicationSettingsPropsMixin.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    total=123
                ),
                quiet_time=pinpoint_mixins.CfnApplicationSettingsPropsMixin.QuietTimeProperty(
                    end="end",
                    start="start"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9794cb7939c5fcd57b0cc93bbe379f36bde1d1e06501e34c4eb996682646da71)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument campaign_hook", value=campaign_hook, expected_type=type_hints["campaign_hook"])
            check_type(argname="argument cloud_watch_metrics_enabled", value=cloud_watch_metrics_enabled, expected_type=type_hints["cloud_watch_metrics_enabled"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument quiet_time", value=quiet_time, expected_type=type_hints["quiet_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if campaign_hook is not None:
            self._values["campaign_hook"] = campaign_hook
        if cloud_watch_metrics_enabled is not None:
            self._values["cloud_watch_metrics_enabled"] = cloud_watch_metrics_enabled
        if limits is not None:
            self._values["limits"] = limits
        if quiet_time is not None:
            self._values["quiet_time"] = quiet_time

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationSettingsPropsMixin.CampaignHookProperty"]]:
        '''The settings for the Lambda function to use by default as a code hook for campaigns in the application.

        To override these settings for a specific campaign, use the Campaign resource to define custom Lambda function settings for the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-campaignhook
        '''
        result = self._values.get("campaign_hook")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationSettingsPropsMixin.CampaignHookProperty"]], result)

    @builtins.property
    def cloud_watch_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-cloudwatchmetricsenabled
        '''
        result = self._values.get("cloud_watch_metrics_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationSettingsPropsMixin.LimitsProperty"]]:
        '''The default sending limits for campaigns in the application.

        To override these limits for a specific campaign, use the Campaign resource to define custom limits for the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-limits
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationSettingsPropsMixin.LimitsProperty"]], result)

    @builtins.property
    def quiet_time(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationSettingsPropsMixin.QuietTimeProperty"]]:
        '''The default quiet time for campaigns in the application.

        Quiet time is a specific time range when campaigns don't send messages to endpoints, if all the following conditions are met:

        - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value.
        - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the application (or a campaign that has custom quiet time settings).
        - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the application (or a campaign that has custom quiet time settings).

        If any of the preceding conditions isn't met, the endpoint will receive messages from a campaign, even if quiet time is enabled.

        To override the default quiet time settings for a specific campaign, use the Campaign resource to define a custom quiet time for the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-quiettime
        '''
        result = self._values.get("quiet_time")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationSettingsPropsMixin.QuietTimeProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationSettingsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationSettingsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnApplicationSettingsPropsMixin",
):
    '''Specifies the settings for an Amazon Pinpoint application.

    In Amazon Pinpoint, an *application* (also referred to as an *app* or *project* ) is a collection of related settings, customer information, segments, and campaigns, and other types of Amazon Pinpoint resources.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html
    :cloudformationResource: AWS::Pinpoint::ApplicationSettings
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_application_settings_props_mixin = pinpoint_mixins.CfnApplicationSettingsPropsMixin(pinpoint_mixins.CfnApplicationSettingsMixinProps(
            application_id="applicationId",
            campaign_hook=pinpoint_mixins.CfnApplicationSettingsPropsMixin.CampaignHookProperty(
                lambda_function_name="lambdaFunctionName",
                mode="mode",
                web_url="webUrl"
            ),
            cloud_watch_metrics_enabled=False,
            limits=pinpoint_mixins.CfnApplicationSettingsPropsMixin.LimitsProperty(
                daily=123,
                maximum_duration=123,
                messages_per_second=123,
                total=123
            ),
            quiet_time=pinpoint_mixins.CfnApplicationSettingsPropsMixin.QuietTimeProperty(
                end="end",
                start="start"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::ApplicationSettings``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c3ddd95f0b77fcc1d23ee0d204260ad0fe88a286c02fc5dd4d50d09367b323)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c31377c1cb8d24b8fab7c7078b99b8e9a54e3c792dde9534766f88d038d2a416)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d678a54f7350a2ad438688f4ae3631714bdeb561e49481fbdd043331a9844e17)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationSettingsMixinProps:
        return typing.cast(CfnApplicationSettingsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnApplicationSettingsPropsMixin.CampaignHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_function_name": "lambdaFunctionName",
            "mode": "mode",
            "web_url": "webUrl",
        },
    )
    class CampaignHookProperty:
        def __init__(
            self,
            *,
            lambda_function_name: typing.Optional[builtins.str] = None,
            mode: typing.Optional[builtins.str] = None,
            web_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Lambda function to use by default as a code hook for campaigns in the application.

            :param lambda_function_name: The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to send messages for campaigns in the application.
            :param mode: The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:. - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign. - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.
            :param web_url: The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                campaign_hook_property = pinpoint_mixins.CfnApplicationSettingsPropsMixin.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d20ae34bca941d286265d1848de5ffef21153f3f393b6e7f120e46d0828f1472)
                check_type(argname="argument lambda_function_name", value=lambda_function_name, expected_type=type_hints["lambda_function_name"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument web_url", value=web_url, expected_type=type_hints["web_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_function_name is not None:
                self._values["lambda_function_name"] = lambda_function_name
            if mode is not None:
                self._values["mode"] = mode
            if web_url is not None:
                self._values["web_url"] = web_url

        @builtins.property
        def lambda_function_name(self) -> typing.Optional[builtins.str]:
            '''The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to send messages for campaigns in the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-lambdafunctionname
            '''
            result = self._values.get("lambda_function_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:.

            - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign.
            - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def web_url(self) -> typing.Optional[builtins.str]:
            '''The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-weburl
            '''
            result = self._values.get("web_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnApplicationSettingsPropsMixin.LimitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "daily": "daily",
            "maximum_duration": "maximumDuration",
            "messages_per_second": "messagesPerSecond",
            "total": "total",
        },
    )
    class LimitsProperty:
        def __init__(
            self,
            *,
            daily: typing.Optional[jsii.Number] = None,
            maximum_duration: typing.Optional[jsii.Number] = None,
            messages_per_second: typing.Optional[jsii.Number] = None,
            total: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the default sending limits for campaigns in the application.

            :param daily: The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period. The maximum value is 100.
            :param maximum_duration: The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign. The minimum value is 60 seconds.
            :param messages_per_second: The maximum number of messages that a campaign can send each second. The minimum value is 1. The maximum value is 20,000.
            :param total: The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign. The maximum value is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                limits_property = pinpoint_mixins.CfnApplicationSettingsPropsMixin.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    total=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b44e38170b3251fbb2c8355e2701740349d3e882e6914b6a9c94c2ad7cf7b2f7)
                check_type(argname="argument daily", value=daily, expected_type=type_hints["daily"])
                check_type(argname="argument maximum_duration", value=maximum_duration, expected_type=type_hints["maximum_duration"])
                check_type(argname="argument messages_per_second", value=messages_per_second, expected_type=type_hints["messages_per_second"])
                check_type(argname="argument total", value=total, expected_type=type_hints["total"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if daily is not None:
                self._values["daily"] = daily
            if maximum_duration is not None:
                self._values["maximum_duration"] = maximum_duration
            if messages_per_second is not None:
                self._values["messages_per_second"] = messages_per_second
            if total is not None:
                self._values["total"] = total

        @builtins.property
        def daily(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period.

            The maximum value is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-daily
            '''
            result = self._values.get("daily")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_duration(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign.

            The minimum value is 60 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-maximumduration
            '''
            result = self._values.get("maximum_duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def messages_per_second(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send each second.

            The minimum value is 1. The maximum value is 20,000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-messagespersecond
            '''
            result = self._values.get("messages_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign.

            The maximum value is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-total
            '''
            result = self._values.get("total")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnApplicationSettingsPropsMixin.QuietTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class QuietTimeProperty:
        def __init__(
            self,
            *,
            end: typing.Optional[builtins.str] = None,
            start: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the start and end times that define a time range when messages aren't sent to endpoints.

            :param end: The specific time when quiet time ends. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.
            :param start: The specific time when quiet time begins. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                quiet_time_property = pinpoint_mixins.CfnApplicationSettingsPropsMixin.QuietTimeProperty(
                    end="end",
                    start="start"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98a97d0224652b8f9c5c04138bb332ff59d9e327d8a5b3bda069f61fb5e124a0)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end is not None:
                self._values["end"] = end
            if start is not None:
                self._values["start"] = start

        @builtins.property
        def end(self) -> typing.Optional[builtins.str]:
            '''The specific time when quiet time ends.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html#cfn-pinpoint-applicationsettings-quiettime-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start(self) -> typing.Optional[builtins.str]:
            '''The specific time when quiet time begins.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html#cfn-pinpoint-applicationsettings-quiettime-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuietTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnBaiduChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "application_id": "applicationId",
        "enabled": "enabled",
        "secret_key": "secretKey",
    },
)
class CfnBaiduChannelMixinProps:
    def __init__(
        self,
        *,
        api_key: typing.Optional[builtins.str] = None,
        application_id: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        secret_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnBaiduChannelPropsMixin.

        :param api_key: The API key that you received from the Baidu Cloud Push service to communicate with the service.
        :param application_id: The unique identifier for the Amazon Pinpoint application that you're configuring the Baidu channel for.
        :param enabled: Specifies whether to enable the Baidu channel for the application.
        :param secret_key: The secret key that you received from the Baidu Cloud Push service to communicate with the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_baidu_channel_mixin_props = pinpoint_mixins.CfnBaiduChannelMixinProps(
                api_key="apiKey",
                application_id="applicationId",
                enabled=False,
                secret_key="secretKey"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f53a69ea383f0ee41493e7a422b38a399e6d88f08d8dbcd34fb3f611850245)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_key is not None:
            self._values["api_key"] = api_key
        if application_id is not None:
            self._values["application_id"] = application_id
        if enabled is not None:
            self._values["enabled"] = enabled
        if secret_key is not None:
            self._values["secret_key"] = secret_key

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        '''The API key that you received from the Baidu Cloud Push service to communicate with the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-apikey
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that you're configuring the Baidu channel for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable the Baidu channel for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''The secret key that you received from the Baidu Cloud Push service to communicate with the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-secretkey
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBaiduChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBaiduChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnBaiduChannelPropsMixin",
):
    '''A *channel* is a type of platform that you can deliver messages to.

    You can use the Baidu channel to send notifications to the Baidu Cloud Push notification service. Before you can use Amazon Pinpoint to send notifications to the Baidu Cloud Push service, you have to enable the Baidu channel for an Amazon Pinpoint application.

    The BaiduChannel resource represents the status and authentication settings of the Baidu channel for an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html
    :cloudformationResource: AWS::Pinpoint::BaiduChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_baidu_channel_props_mixin = pinpoint_mixins.CfnBaiduChannelPropsMixin(pinpoint_mixins.CfnBaiduChannelMixinProps(
            api_key="apiKey",
            application_id="applicationId",
            enabled=False,
            secret_key="secretKey"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBaiduChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::BaiduChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed15c23cefc2cb368352b8cd444397da4ccd15776922cd1a225bf8522934ba6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__328c5ad3bb2831effd6e3dcc6ae2dba2aca150f93ef20e0667af1f5ac18fd0eb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63f2211443c5f823f7871a1bc3cc68e1aecd3932c0d22bf638f277c8b8fecfb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBaiduChannelMixinProps:
        return typing.cast(CfnBaiduChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_treatments": "additionalTreatments",
        "application_id": "applicationId",
        "campaign_hook": "campaignHook",
        "custom_delivery_configuration": "customDeliveryConfiguration",
        "description": "description",
        "holdout_percent": "holdoutPercent",
        "is_paused": "isPaused",
        "limits": "limits",
        "message_configuration": "messageConfiguration",
        "name": "name",
        "priority": "priority",
        "schedule": "schedule",
        "segment_id": "segmentId",
        "segment_version": "segmentVersion",
        "tags": "tags",
        "template_configuration": "templateConfiguration",
        "treatment_description": "treatmentDescription",
        "treatment_name": "treatmentName",
    },
)
class CfnCampaignMixinProps:
    def __init__(
        self,
        *,
        additional_treatments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.WriteTreatmentResourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        application_id: typing.Optional[builtins.str] = None,
        campaign_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CampaignHookProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        holdout_percent: typing.Optional[jsii.Number] = None,
        is_paused: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.LimitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        message_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.MessageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        segment_id: typing.Optional[builtins.str] = None,
        segment_version: typing.Optional[jsii.Number] = None,
        tags: typing.Any = None,
        template_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TemplateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        treatment_description: typing.Optional[builtins.str] = None,
        treatment_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCampaignPropsMixin.

        :param additional_treatments: An array of requests that defines additional treatments for the campaign, in addition to the default treatment for the campaign.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the campaign is associated with.
        :param campaign_hook: Specifies the Lambda function to use as a code hook for a campaign.
        :param custom_delivery_configuration: The delivery configuration settings for sending the treatment through a custom channel. This object is required if the ``MessageConfiguration`` object for the treatment specifies a ``CustomMessage`` object.
        :param description: A custom description of the campaign.
        :param holdout_percent: The allocated percentage of users (segment members) who shouldn't receive messages from the campaign.
        :param is_paused: Specifies whether to pause the campaign. A paused campaign doesn't run unless you resume it by changing this value to ``false`` . If you restart a campaign, the campaign restarts from the beginning and not at the point you paused it. If a campaign is running it will complete and then pause. Pause only pauses or skips the next run for a recurring future scheduled campaign. A campaign scheduled for immediate can't be paused.
        :param limits: The messaging limits for the campaign.
        :param message_configuration: The message configuration settings for the treatment.
        :param name: The name of the campaign.
        :param priority: An integer between 1 and 5, inclusive, that represents the priority of the in-app message campaign, where 1 is the highest priority and 5 is the lowest. If there are multiple messages scheduled to be displayed at the same time, the priority determines the order in which those messages are displayed.
        :param schedule: The schedule settings for the treatment.
        :param segment_id: The unique identifier for the segment to associate with the campaign.
        :param segment_version: The version of the segment to associate with the campaign.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_configuration: The message template to use for the treatment.
        :param treatment_description: A custom description of the treatment.
        :param treatment_name: A custom name for the treatment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            # attributes: Any
            # custom_config: Any
            # metrics: Any
            # tags: Any
            
            cfn_campaign_mixin_props = pinpoint_mixins.CfnCampaignMixinProps(
                additional_treatments=[pinpoint_mixins.CfnCampaignPropsMixin.WriteTreatmentResourceProperty(
                    custom_delivery_configuration=pinpoint_mixins.CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty(
                        delivery_uri="deliveryUri",
                        endpoint_types=["endpointTypes"]
                    ),
                    message_configuration=pinpoint_mixins.CfnCampaignPropsMixin.MessageConfigurationProperty(
                        adm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        apns_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        baidu_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        custom_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignCustomMessageProperty(
                            data="data"
                        ),
                        default_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        email_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEmailMessageProperty(
                            body="body",
                            from_address="fromAddress",
                            html_body="htmlBody",
                            title="title"
                        ),
                        gcm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        in_app_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignInAppMessageProperty(
                            content=[pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageContentProperty(
                                background_color="backgroundColor",
                                body_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageBodyConfigProperty(
                                    alignment="alignment",
                                    body="body",
                                    text_color="textColor"
                                ),
                                header_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty(
                                    alignment="alignment",
                                    header="header",
                                    text_color="textColor"
                                ),
                                image_url="imageUrl",
                                primary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                                    android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                ),
                                secondary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                                    android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                )
                            )],
                            custom_config=custom_config,
                            layout="layout"
                        ),
                        sms_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignSmsMessageProperty(
                            body="body",
                            entity_id="entityId",
                            message_type="messageType",
                            origination_number="originationNumber",
                            sender_id="senderId",
                            template_id="templateId"
                        )
                    ),
                    schedule=pinpoint_mixins.CfnCampaignPropsMixin.ScheduleProperty(
                        end_time="endTime",
                        event_filter=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEventFilterProperty(
                            dimensions=pinpoint_mixins.CfnCampaignPropsMixin.EventDimensionsProperty(
                                attributes=attributes,
                                event_type=pinpoint_mixins.CfnCampaignPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                metrics=metrics
                            ),
                            filter_type="filterType"
                        ),
                        frequency="frequency",
                        is_local_time=False,
                        quiet_time=pinpoint_mixins.CfnCampaignPropsMixin.QuietTimeProperty(
                            end="end",
                            start="start"
                        ),
                        start_time="startTime",
                        time_zone="timeZone"
                    ),
                    size_percent=123,
                    template_configuration=pinpoint_mixins.CfnCampaignPropsMixin.TemplateConfigurationProperty(
                        email_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        push_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        sms_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        voice_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                            name="name",
                            version="version"
                        )
                    ),
                    treatment_description="treatmentDescription",
                    treatment_name="treatmentName"
                )],
                application_id="applicationId",
                campaign_hook=pinpoint_mixins.CfnCampaignPropsMixin.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                ),
                custom_delivery_configuration=pinpoint_mixins.CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty(
                    delivery_uri="deliveryUri",
                    endpoint_types=["endpointTypes"]
                ),
                description="description",
                holdout_percent=123,
                is_paused=False,
                limits=pinpoint_mixins.CfnCampaignPropsMixin.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    session=123,
                    total=123
                ),
                message_configuration=pinpoint_mixins.CfnCampaignPropsMixin.MessageConfigurationProperty(
                    adm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    apns_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    baidu_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    custom_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignCustomMessageProperty(
                        data="data"
                    ),
                    default_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    email_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEmailMessageProperty(
                        body="body",
                        from_address="fromAddress",
                        html_body="htmlBody",
                        title="title"
                    ),
                    gcm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    in_app_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignInAppMessageProperty(
                        content=[pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageContentProperty(
                            background_color="backgroundColor",
                            body_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageBodyConfigProperty(
                                alignment="alignment",
                                body="body",
                                text_color="textColor"
                            ),
                            header_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty(
                                alignment="alignment",
                                header="header",
                                text_color="textColor"
                            ),
                            image_url="imageUrl",
                            primary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                                android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            ),
                            secondary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                                android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            )
                        )],
                        custom_config=custom_config,
                        layout="layout"
                    ),
                    sms_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignSmsMessageProperty(
                        body="body",
                        entity_id="entityId",
                        message_type="messageType",
                        origination_number="originationNumber",
                        sender_id="senderId",
                        template_id="templateId"
                    )
                ),
                name="name",
                priority=123,
                schedule=pinpoint_mixins.CfnCampaignPropsMixin.ScheduleProperty(
                    end_time="endTime",
                    event_filter=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEventFilterProperty(
                        dimensions=pinpoint_mixins.CfnCampaignPropsMixin.EventDimensionsProperty(
                            attributes=attributes,
                            event_type=pinpoint_mixins.CfnCampaignPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            metrics=metrics
                        ),
                        filter_type="filterType"
                    ),
                    frequency="frequency",
                    is_local_time=False,
                    quiet_time=pinpoint_mixins.CfnCampaignPropsMixin.QuietTimeProperty(
                        end="end",
                        start="start"
                    ),
                    start_time="startTime",
                    time_zone="timeZone"
                ),
                segment_id="segmentId",
                segment_version=123,
                tags=tags,
                template_configuration=pinpoint_mixins.CfnCampaignPropsMixin.TemplateConfigurationProperty(
                    email_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    push_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    sms_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    voice_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    )
                ),
                treatment_description="treatmentDescription",
                treatment_name="treatmentName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__753429197d419217949c08eeff09e2c672620a8b71618f0742d0c22490ff1b7c)
            check_type(argname="argument additional_treatments", value=additional_treatments, expected_type=type_hints["additional_treatments"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument campaign_hook", value=campaign_hook, expected_type=type_hints["campaign_hook"])
            check_type(argname="argument custom_delivery_configuration", value=custom_delivery_configuration, expected_type=type_hints["custom_delivery_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument holdout_percent", value=holdout_percent, expected_type=type_hints["holdout_percent"])
            check_type(argname="argument is_paused", value=is_paused, expected_type=type_hints["is_paused"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument message_configuration", value=message_configuration, expected_type=type_hints["message_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument segment_id", value=segment_id, expected_type=type_hints["segment_id"])
            check_type(argname="argument segment_version", value=segment_version, expected_type=type_hints["segment_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
            check_type(argname="argument treatment_description", value=treatment_description, expected_type=type_hints["treatment_description"])
            check_type(argname="argument treatment_name", value=treatment_name, expected_type=type_hints["treatment_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_treatments is not None:
            self._values["additional_treatments"] = additional_treatments
        if application_id is not None:
            self._values["application_id"] = application_id
        if campaign_hook is not None:
            self._values["campaign_hook"] = campaign_hook
        if custom_delivery_configuration is not None:
            self._values["custom_delivery_configuration"] = custom_delivery_configuration
        if description is not None:
            self._values["description"] = description
        if holdout_percent is not None:
            self._values["holdout_percent"] = holdout_percent
        if is_paused is not None:
            self._values["is_paused"] = is_paused
        if limits is not None:
            self._values["limits"] = limits
        if message_configuration is not None:
            self._values["message_configuration"] = message_configuration
        if name is not None:
            self._values["name"] = name
        if priority is not None:
            self._values["priority"] = priority
        if schedule is not None:
            self._values["schedule"] = schedule
        if segment_id is not None:
            self._values["segment_id"] = segment_id
        if segment_version is not None:
            self._values["segment_version"] = segment_version
        if tags is not None:
            self._values["tags"] = tags
        if template_configuration is not None:
            self._values["template_configuration"] = template_configuration
        if treatment_description is not None:
            self._values["treatment_description"] = treatment_description
        if treatment_name is not None:
            self._values["treatment_name"] = treatment_name

    @builtins.property
    def additional_treatments(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.WriteTreatmentResourceProperty"]]]]:
        '''An array of requests that defines additional treatments for the campaign, in addition to the default treatment for the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-additionaltreatments
        '''
        result = self._values.get("additional_treatments")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.WriteTreatmentResourceProperty"]]]], result)

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that the campaign is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignHookProperty"]]:
        '''Specifies the Lambda function to use as a code hook for a campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-campaignhook
        '''
        result = self._values.get("campaign_hook")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignHookProperty"]], result)

    @builtins.property
    def custom_delivery_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty"]]:
        '''The delivery configuration settings for sending the treatment through a custom channel.

        This object is required if the ``MessageConfiguration`` object for the treatment specifies a ``CustomMessage`` object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-customdeliveryconfiguration
        '''
        result = self._values.get("custom_delivery_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def holdout_percent(self) -> typing.Optional[jsii.Number]:
        '''The allocated percentage of users (segment members) who shouldn't receive messages from the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-holdoutpercent
        '''
        result = self._values.get("holdout_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def is_paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to pause the campaign.

        A paused campaign doesn't run unless you resume it by changing this value to ``false`` . If you restart a campaign, the campaign restarts from the beginning and not at the point you paused it. If a campaign is running it will complete and then pause. Pause only pauses or skips the next run for a recurring future scheduled campaign. A campaign scheduled for immediate can't be paused.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-ispaused
        '''
        result = self._values.get("is_paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.LimitsProperty"]]:
        '''The messaging limits for the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-limits
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.LimitsProperty"]], result)

    @builtins.property
    def message_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageConfigurationProperty"]]:
        '''The message configuration settings for the treatment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-messageconfiguration
        '''
        result = self._values.get("message_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''An integer between 1 and 5, inclusive, that represents the priority of the in-app message campaign, where 1 is the highest priority and 5 is the lowest.

        If there are multiple messages scheduled to be displayed at the same time, the priority determines the order in which those messages are displayed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ScheduleProperty"]]:
        '''The schedule settings for the treatment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ScheduleProperty"]], result)

    @builtins.property
    def segment_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the segment to associate with the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentid
        '''
        result = self._values.get("segment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_version(self) -> typing.Optional[jsii.Number]:
        '''The version of the segment to associate with the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentversion
        '''
        result = self._values.get("segment_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateConfigurationProperty"]]:
        '''The message template to use for the treatment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-templateconfiguration
        '''
        result = self._values.get("template_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateConfigurationProperty"]], result)

    @builtins.property
    def treatment_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the treatment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentdescription
        '''
        result = self._values.get("treatment_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def treatment_name(self) -> typing.Optional[builtins.str]:
        '''A custom name for the treatment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentname
        '''
        result = self._values.get("treatment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCampaignMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCampaignPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin",
):
    '''Specifies the settings for a campaign.

    A *campaign* is a messaging initiative that engages a specific segment of users for an Amazon Pinpoint application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html
    :cloudformationResource: AWS::Pinpoint::Campaign
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        # attributes: Any
        # custom_config: Any
        # metrics: Any
        # tags: Any
        
        cfn_campaign_props_mixin = pinpoint_mixins.CfnCampaignPropsMixin(pinpoint_mixins.CfnCampaignMixinProps(
            additional_treatments=[pinpoint_mixins.CfnCampaignPropsMixin.WriteTreatmentResourceProperty(
                custom_delivery_configuration=pinpoint_mixins.CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty(
                    delivery_uri="deliveryUri",
                    endpoint_types=["endpointTypes"]
                ),
                message_configuration=pinpoint_mixins.CfnCampaignPropsMixin.MessageConfigurationProperty(
                    adm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    apns_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    baidu_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    custom_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignCustomMessageProperty(
                        data="data"
                    ),
                    default_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    email_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEmailMessageProperty(
                        body="body",
                        from_address="fromAddress",
                        html_body="htmlBody",
                        title="title"
                    ),
                    gcm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    in_app_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignInAppMessageProperty(
                        content=[pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageContentProperty(
                            background_color="backgroundColor",
                            body_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageBodyConfigProperty(
                                alignment="alignment",
                                body="body",
                                text_color="textColor"
                            ),
                            header_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty(
                                alignment="alignment",
                                header="header",
                                text_color="textColor"
                            ),
                            image_url="imageUrl",
                            primary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                                android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            ),
                            secondary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                                android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            )
                        )],
                        custom_config=custom_config,
                        layout="layout"
                    ),
                    sms_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignSmsMessageProperty(
                        body="body",
                        entity_id="entityId",
                        message_type="messageType",
                        origination_number="originationNumber",
                        sender_id="senderId",
                        template_id="templateId"
                    )
                ),
                schedule=pinpoint_mixins.CfnCampaignPropsMixin.ScheduleProperty(
                    end_time="endTime",
                    event_filter=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEventFilterProperty(
                        dimensions=pinpoint_mixins.CfnCampaignPropsMixin.EventDimensionsProperty(
                            attributes=attributes,
                            event_type=pinpoint_mixins.CfnCampaignPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            metrics=metrics
                        ),
                        filter_type="filterType"
                    ),
                    frequency="frequency",
                    is_local_time=False,
                    quiet_time=pinpoint_mixins.CfnCampaignPropsMixin.QuietTimeProperty(
                        end="end",
                        start="start"
                    ),
                    start_time="startTime",
                    time_zone="timeZone"
                ),
                size_percent=123,
                template_configuration=pinpoint_mixins.CfnCampaignPropsMixin.TemplateConfigurationProperty(
                    email_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    push_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    sms_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    voice_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    )
                ),
                treatment_description="treatmentDescription",
                treatment_name="treatmentName"
            )],
            application_id="applicationId",
            campaign_hook=pinpoint_mixins.CfnCampaignPropsMixin.CampaignHookProperty(
                lambda_function_name="lambdaFunctionName",
                mode="mode",
                web_url="webUrl"
            ),
            custom_delivery_configuration=pinpoint_mixins.CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty(
                delivery_uri="deliveryUri",
                endpoint_types=["endpointTypes"]
            ),
            description="description",
            holdout_percent=123,
            is_paused=False,
            limits=pinpoint_mixins.CfnCampaignPropsMixin.LimitsProperty(
                daily=123,
                maximum_duration=123,
                messages_per_second=123,
                session=123,
                total=123
            ),
            message_configuration=pinpoint_mixins.CfnCampaignPropsMixin.MessageConfigurationProperty(
                adm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                apns_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                baidu_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                custom_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignCustomMessageProperty(
                    data="data"
                ),
                default_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                email_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEmailMessageProperty(
                    body="body",
                    from_address="fromAddress",
                    html_body="htmlBody",
                    title="title"
                ),
                gcm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                in_app_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignInAppMessageProperty(
                    content=[pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageContentProperty(
                        background_color="backgroundColor",
                        body_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageBodyConfigProperty(
                            alignment="alignment",
                            body="body",
                            text_color="textColor"
                        ),
                        header_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty(
                            alignment="alignment",
                            header="header",
                            text_color="textColor"
                        ),
                        image_url="imageUrl",
                        primary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                            android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        ),
                        secondary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                            android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        )
                    )],
                    custom_config=custom_config,
                    layout="layout"
                ),
                sms_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignSmsMessageProperty(
                    body="body",
                    entity_id="entityId",
                    message_type="messageType",
                    origination_number="originationNumber",
                    sender_id="senderId",
                    template_id="templateId"
                )
            ),
            name="name",
            priority=123,
            schedule=pinpoint_mixins.CfnCampaignPropsMixin.ScheduleProperty(
                end_time="endTime",
                event_filter=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEventFilterProperty(
                    dimensions=pinpoint_mixins.CfnCampaignPropsMixin.EventDimensionsProperty(
                        attributes=attributes,
                        event_type=pinpoint_mixins.CfnCampaignPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        metrics=metrics
                    ),
                    filter_type="filterType"
                ),
                frequency="frequency",
                is_local_time=False,
                quiet_time=pinpoint_mixins.CfnCampaignPropsMixin.QuietTimeProperty(
                    end="end",
                    start="start"
                ),
                start_time="startTime",
                time_zone="timeZone"
            ),
            segment_id="segmentId",
            segment_version=123,
            tags=tags,
            template_configuration=pinpoint_mixins.CfnCampaignPropsMixin.TemplateConfigurationProperty(
                email_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                    name="name",
                    version="version"
                ),
                push_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                    name="name",
                    version="version"
                ),
                sms_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                    name="name",
                    version="version"
                ),
                voice_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                    name="name",
                    version="version"
                )
            ),
            treatment_description="treatmentDescription",
            treatment_name="treatmentName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCampaignMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::Campaign``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3df051f1faf3b00d389160d92dcc1901cddee7ad83042fc1f4e23ce3799451)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f08edc80efc9880484c7437d1cb2b403357de4cc61a7c354bb6d7057a1f8aa68)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c1d2c9e0f5cf732828389989f982de131a7e884f5ae93710fc74d894d53309)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCampaignMixinProps:
        return typing.cast(CfnCampaignMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.CampaignCustomMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"data": "data"},
    )
    class CampaignCustomMessageProperty:
        def __init__(self, *, data: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the contents of a message that's sent through a custom channel to recipients of a campaign.

            :param data: The raw, JSON-formatted string to use as the payload for the message. The maximum size is 5 KB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigncustommessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                campaign_custom_message_property = pinpoint_mixins.CfnCampaignPropsMixin.CampaignCustomMessageProperty(
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__451d3c1cad3d4f79dd4398ce2bfae0618f30d34ba8bc7ba0553a3ec33983d21c)
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data is not None:
                self._values["data"] = data

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''The raw, JSON-formatted string to use as the payload for the message.

            The maximum size is 5 KB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigncustommessage.html#cfn-pinpoint-campaign-campaigncustommessage-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignCustomMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.CampaignEmailMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "body": "body",
            "from_address": "fromAddress",
            "html_body": "htmlBody",
            "title": "title",
        },
    )
    class CampaignEmailMessageProperty:
        def __init__(
            self,
            *,
            body: typing.Optional[builtins.str] = None,
            from_address: typing.Optional[builtins.str] = None,
            html_body: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the content and "From" address for an email message that's sent to recipients of a campaign.

            :param body: The body of the email for recipients whose email clients don't render HTML content.
            :param from_address: The verified email address to send the email from. The default address is the ``FromAddress`` specified for the email channel for the application.
            :param html_body: The body of the email, in HTML format, for recipients whose email clients render HTML content.
            :param title: The subject line, or title, of the email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                campaign_email_message_property = pinpoint_mixins.CfnCampaignPropsMixin.CampaignEmailMessageProperty(
                    body="body",
                    from_address="fromAddress",
                    html_body="htmlBody",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f181bd2ff162055f54ff2d351caf0c44f34de894e72af167ef7476191b72bc42)
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument from_address", value=from_address, expected_type=type_hints["from_address"])
                check_type(argname="argument html_body", value=html_body, expected_type=type_hints["html_body"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body
            if from_address is not None:
                self._values["from_address"] = from_address
            if html_body is not None:
                self._values["html_body"] = html_body
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The body of the email for recipients whose email clients don't render HTML content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def from_address(self) -> typing.Optional[builtins.str]:
            '''The verified email address to send the email from.

            The default address is the ``FromAddress`` specified for the email channel for the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-fromaddress
            '''
            result = self._values.get("from_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def html_body(self) -> typing.Optional[builtins.str]:
            '''The body of the email, in HTML format, for recipients whose email clients render HTML content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-htmlbody
            '''
            result = self._values.get("html_body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The subject line, or title, of the email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignEmailMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.CampaignEventFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions", "filter_type": "filterType"},
    )
    class CampaignEventFilterProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.EventDimensionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the settings for events that cause a campaign to be sent.

            :param dimensions: The dimension settings of the event filter for the campaign.
            :param filter_type: The type of event that causes the campaign to be sent. Valid values are: ``SYSTEM`` , sends the campaign when a system event occurs; and, ``ENDPOINT`` , sends the campaign when an endpoint event (Events resource) occurs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                # attributes: Any
                # metrics: Any
                
                campaign_event_filter_property = pinpoint_mixins.CfnCampaignPropsMixin.CampaignEventFilterProperty(
                    dimensions=pinpoint_mixins.CfnCampaignPropsMixin.EventDimensionsProperty(
                        attributes=attributes,
                        event_type=pinpoint_mixins.CfnCampaignPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        metrics=metrics
                    ),
                    filter_type="filterType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4754eba285099c12270f93e2cbc54d33e404e484902ae26c34f3f6859de0128)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if filter_type is not None:
                self._values["filter_type"] = filter_type

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.EventDimensionsProperty"]]:
            '''The dimension settings of the event filter for the campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html#cfn-pinpoint-campaign-campaigneventfilter-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.EventDimensionsProperty"]], result)

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            '''The type of event that causes the campaign to be sent.

            Valid values are: ``SYSTEM`` , sends the campaign when a system event occurs; and, ``ENDPOINT`` , sends the campaign when an endpoint event (Events resource) occurs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html#cfn-pinpoint-campaign-campaigneventfilter-filtertype
            '''
            result = self._values.get("filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignEventFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.CampaignHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_function_name": "lambdaFunctionName",
            "mode": "mode",
            "web_url": "webUrl",
        },
    )
    class CampaignHookProperty:
        def __init__(
            self,
            *,
            lambda_function_name: typing.Optional[builtins.str] = None,
            mode: typing.Optional[builtins.str] = None,
            web_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies settings for invoking an Lambda function that customizes a segment for a campaign.

            :param lambda_function_name: The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to customize a segment for a campaign.
            :param mode: The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:. - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign. - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.
            :param web_url: The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                campaign_hook_property = pinpoint_mixins.CfnCampaignPropsMixin.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4eaf61e1dc240fa7fa5eba2b6a4b337dcbee83170afee17f85ab807418791b9)
                check_type(argname="argument lambda_function_name", value=lambda_function_name, expected_type=type_hints["lambda_function_name"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument web_url", value=web_url, expected_type=type_hints["web_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_function_name is not None:
                self._values["lambda_function_name"] = lambda_function_name
            if mode is not None:
                self._values["mode"] = mode
            if web_url is not None:
                self._values["web_url"] = web_url

        @builtins.property
        def lambda_function_name(self) -> typing.Optional[builtins.str]:
            '''The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to customize a segment for a campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-lambdafunctionname
            '''
            result = self._values.get("lambda_function_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:.

            - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign.
            - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def web_url(self) -> typing.Optional[builtins.str]:
            '''The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-weburl
            '''
            result = self._values.get("web_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.CampaignInAppMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content": "content",
            "custom_config": "customConfig",
            "layout": "layout",
        },
    )
    class CampaignInAppMessageProperty:
        def __init__(
            self,
            *,
            content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.InAppMessageContentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            custom_config: typing.Any = None,
            layout: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the appearance of an in-app message, including the message type, the title and body text, text and background colors, and the configurations of buttons that appear in the message.

            :param content: An array that contains configurtion information about the in-app message for the campaign, including title and body text, text colors, background colors, image URLs, and button configurations.
            :param custom_config: Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.
            :param layout: A string that describes how the in-app message will appear. You can specify one of the following:. - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page. - ``TOP_BANNER`` – a message that appears as a banner at the top of the page. - ``OVERLAYS`` – a message that covers entire screen. - ``MOBILE_FEED`` – a message that appears in a window in front of the page. - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page. - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                # custom_config: Any
                
                campaign_in_app_message_property = pinpoint_mixins.CfnCampaignPropsMixin.CampaignInAppMessageProperty(
                    content=[pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageContentProperty(
                        background_color="backgroundColor",
                        body_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageBodyConfigProperty(
                            alignment="alignment",
                            body="body",
                            text_color="textColor"
                        ),
                        header_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty(
                            alignment="alignment",
                            header="header",
                            text_color="textColor"
                        ),
                        image_url="imageUrl",
                        primary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                            android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        ),
                        secondary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                            android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        )
                    )],
                    custom_config=custom_config,
                    layout="layout"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abb06c5184968a17c51382375ee6a0850f4977b0847f728699b25f5a2e7cfdc1)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument custom_config", value=custom_config, expected_type=type_hints["custom_config"])
                check_type(argname="argument layout", value=layout, expected_type=type_hints["layout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content
            if custom_config is not None:
                self._values["custom_config"] = custom_config
            if layout is not None:
                self._values["layout"] = layout

        @builtins.property
        def content(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.InAppMessageContentProperty"]]]]:
            '''An array that contains configurtion information about the in-app message for the campaign, including title and body text, text colors, background colors, image URLs, and button configurations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html#cfn-pinpoint-campaign-campaigninappmessage-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.InAppMessageContentProperty"]]]], result)

        @builtins.property
        def custom_config(self) -> typing.Any:
            '''Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html#cfn-pinpoint-campaign-campaigninappmessage-customconfig
            '''
            result = self._values.get("custom_config")
            return typing.cast(typing.Any, result)

        @builtins.property
        def layout(self) -> typing.Optional[builtins.str]:
            '''A string that describes how the in-app message will appear. You can specify one of the following:.

            - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page.
            - ``TOP_BANNER`` – a message that appears as a banner at the top of the page.
            - ``OVERLAYS`` – a message that covers entire screen.
            - ``MOBILE_FEED`` – a message that appears in a window in front of the page.
            - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page.
            - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html#cfn-pinpoint-campaign-campaigninappmessage-layout
            '''
            result = self._values.get("layout")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignInAppMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.CampaignSmsMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "body": "body",
            "entity_id": "entityId",
            "message_type": "messageType",
            "origination_number": "originationNumber",
            "sender_id": "senderId",
            "template_id": "templateId",
        },
    )
    class CampaignSmsMessageProperty:
        def __init__(
            self,
            *,
            body: typing.Optional[builtins.str] = None,
            entity_id: typing.Optional[builtins.str] = None,
            message_type: typing.Optional[builtins.str] = None,
            origination_number: typing.Optional[builtins.str] = None,
            sender_id: typing.Optional[builtins.str] = None,
            template_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the content and settings for an SMS message that's sent to recipients of a campaign.

            :param body: The body of the SMS message.
            :param entity_id: The entity ID or Principal Entity (PE) id received from the regulatory body for sending SMS in your country.
            :param message_type: The SMS message type. Valid values are ``TRANSACTIONAL`` (for messages that are critical or time-sensitive, such as a one-time passwords) and ``PROMOTIONAL`` (for messsages that aren't critical or time-sensitive, such as marketing messages).
            :param origination_number: The long code to send the SMS message from. This value should be one of the dedicated long codes that's assigned to your AWS account. Although it isn't required, we recommend that you specify the long code using an E.164 format to ensure prompt and accurate delivery of the message. For example, +12065550100.
            :param sender_id: The alphabetic Sender ID to display as the sender of the message on a recipient's device. Support for sender IDs varies by country or region. To specify a phone number as the sender, omit this parameter and use ``OriginationNumber`` instead. For more information about support for Sender ID by country, see the `Amazon Pinpoint User Guide <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ .
            :param template_id: The template ID received from the regulatory body for sending SMS in your country.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                campaign_sms_message_property = pinpoint_mixins.CfnCampaignPropsMixin.CampaignSmsMessageProperty(
                    body="body",
                    entity_id="entityId",
                    message_type="messageType",
                    origination_number="originationNumber",
                    sender_id="senderId",
                    template_id="templateId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a73699746dff574d227d0cb5236d91cc266c887c1a45d9d011c94d0e87c384a)
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
                check_type(argname="argument message_type", value=message_type, expected_type=type_hints["message_type"])
                check_type(argname="argument origination_number", value=origination_number, expected_type=type_hints["origination_number"])
                check_type(argname="argument sender_id", value=sender_id, expected_type=type_hints["sender_id"])
                check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body
            if entity_id is not None:
                self._values["entity_id"] = entity_id
            if message_type is not None:
                self._values["message_type"] = message_type
            if origination_number is not None:
                self._values["origination_number"] = origination_number
            if sender_id is not None:
                self._values["sender_id"] = sender_id
            if template_id is not None:
                self._values["template_id"] = template_id

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The body of the SMS message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entity_id(self) -> typing.Optional[builtins.str]:
            '''The entity ID or Principal Entity (PE) id received from the regulatory body for sending SMS in your country.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-entityid
            '''
            result = self._values.get("entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_type(self) -> typing.Optional[builtins.str]:
            '''The SMS message type.

            Valid values are ``TRANSACTIONAL`` (for messages that are critical or time-sensitive, such as a one-time passwords) and ``PROMOTIONAL`` (for messsages that aren't critical or time-sensitive, such as marketing messages).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-messagetype
            '''
            result = self._values.get("message_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def origination_number(self) -> typing.Optional[builtins.str]:
            '''The long code to send the SMS message from.

            This value should be one of the dedicated long codes that's assigned to your AWS account. Although it isn't required, we recommend that you specify the long code using an E.164 format to ensure prompt and accurate delivery of the message. For example, +12065550100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-originationnumber
            '''
            result = self._values.get("origination_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sender_id(self) -> typing.Optional[builtins.str]:
            '''The alphabetic Sender ID to display as the sender of the message on a recipient's device.

            Support for sender IDs varies by country or region. To specify a phone number as the sender, omit this parameter and use ``OriginationNumber`` instead. For more information about support for Sender ID by country, see the `Amazon Pinpoint User Guide <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-senderid
            '''
            result = self._values.get("sender_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def template_id(self) -> typing.Optional[builtins.str]:
            '''The template ID received from the regulatory body for sending SMS in your country.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-templateid
            '''
            result = self._values.get("template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignSmsMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delivery_uri": "deliveryUri",
            "endpoint_types": "endpointTypes",
        },
    )
    class CustomDeliveryConfigurationProperty:
        def __init__(
            self,
            *,
            delivery_uri: typing.Optional[builtins.str] = None,
            endpoint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the delivery configuration settings for sending a campaign or campaign treatment through a custom channel.

            This object is required if you use the ``CampaignCustomMessage`` object to define the message to send for the campaign or campaign treatment.

            :param delivery_uri: The destination to send the campaign or treatment to. This value can be one of the following:. - The name or Amazon Resource Name (ARN) of an AWS Lambda function to invoke to handle delivery of the campaign or treatment. - The URL for a web application or service that supports HTTPS and can receive the message. The URL has to be a full URL, including the HTTPS protocol.
            :param endpoint_types: The types of endpoints to send the campaign or treatment to. Each valid value maps to a type of channel that you can associate with an endpoint by using the ``ChannelType`` property of an endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-customdeliveryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                custom_delivery_configuration_property = pinpoint_mixins.CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty(
                    delivery_uri="deliveryUri",
                    endpoint_types=["endpointTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d27f04de53b58df77dd1c810188fdfa7baf64f54ecf97ca8fec381297b78938)
                check_type(argname="argument delivery_uri", value=delivery_uri, expected_type=type_hints["delivery_uri"])
                check_type(argname="argument endpoint_types", value=endpoint_types, expected_type=type_hints["endpoint_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_uri is not None:
                self._values["delivery_uri"] = delivery_uri
            if endpoint_types is not None:
                self._values["endpoint_types"] = endpoint_types

        @builtins.property
        def delivery_uri(self) -> typing.Optional[builtins.str]:
            '''The destination to send the campaign or treatment to. This value can be one of the following:.

            - The name or Amazon Resource Name (ARN) of an AWS Lambda function to invoke to handle delivery of the campaign or treatment.
            - The URL for a web application or service that supports HTTPS and can receive the message. The URL has to be a full URL, including the HTTPS protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-customdeliveryconfiguration.html#cfn-pinpoint-campaign-customdeliveryconfiguration-deliveryuri
            '''
            result = self._values.get("delivery_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The types of endpoints to send the campaign or treatment to.

            Each valid value maps to a type of channel that you can associate with an endpoint by using the ``ChannelType`` property of an endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-customdeliveryconfiguration.html#cfn-pinpoint-campaign-customdeliveryconfiguration-endpointtypes
            '''
            result = self._values.get("endpoint_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomDeliveryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "border_radius": "borderRadius",
            "button_action": "buttonAction",
            "link": "link",
            "text": "text",
            "text_color": "textColor",
        },
    )
    class DefaultButtonConfigurationProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            border_radius: typing.Optional[jsii.Number] = None,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
            text: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the default behavior for a button that appears in an in-app message.

            You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.

            :param background_color: The background color of a button, expressed as a hex color code (such as #000000 for black).
            :param border_radius: The border radius of a button.
            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.
            :param text: The text that appears on a button in an in-app message.
            :param text_color: The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                default_button_configuration_property = pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                    background_color="backgroundColor",
                    border_radius=123,
                    button_action="buttonAction",
                    link="link",
                    text="text",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__786d362f3693db41a80db78ef8057f82b0e0f758db853c3beff045e8e5ce1ca3)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument border_radius", value=border_radius, expected_type=type_hints["border_radius"])
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if border_radius is not None:
                self._values["border_radius"] = border_radius
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link
            if text is not None:
                self._values["text"] = text
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color of a button, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def border_radius(self) -> typing.Optional[jsii.Number]:
            '''The border radius of a button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-borderradius
            '''
            result = self._values.get("border_radius")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The text that appears on a button in an in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.EventDimensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "event_type": "eventType",
            "metrics": "metrics",
        },
    )
    class EventDimensionsProperty:
        def __init__(
            self,
            *,
            attributes: typing.Any = None,
            event_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metrics: typing.Any = None,
        ) -> None:
            '''Specifies the dimensions for an event filter that determines when a campaign is sent or a journey activity is performed.

            :param attributes: One or more custom attributes that your application reports to Amazon Pinpoint. You can use these attributes as selection criteria when you create an event filter.
            :param event_type: The name of the event that causes the campaign to be sent or the journey activity to be performed. This can be a standard event that Amazon Pinpoint generates, such as ``_email.delivered`` or ``_custom.delivered`` . For campaigns, this can also be a custom event that's specific to your application. For information about standard events, see `Streaming Amazon Pinpoint Events <https://docs.aws.amazon.com/pinpoint/latest/developerguide/event-streams.html>`_ in the *Amazon Pinpoint Developer Guide* .
            :param metrics: One or more custom metrics that your application reports to Amazon Pinpoint . You can use these metrics as selection criteria when you create an event filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                # attributes: Any
                # metrics: Any
                
                event_dimensions_property = pinpoint_mixins.CfnCampaignPropsMixin.EventDimensionsProperty(
                    attributes=attributes,
                    event_type=pinpoint_mixins.CfnCampaignPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    metrics=metrics
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb9de554e028d77723abd20b1c4ed56a12363dfd5ffc1bde5db6b7f8a8670257)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if event_type is not None:
                self._values["event_type"] = event_type
            if metrics is not None:
                self._values["metrics"] = metrics

        @builtins.property
        def attributes(self) -> typing.Any:
            '''One or more custom attributes that your application reports to Amazon Pinpoint.

            You can use these attributes as selection criteria when you create an event filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SetDimensionProperty"]]:
            '''The name of the event that causes the campaign to be sent or the journey activity to be performed.

            This can be a standard event that Amazon Pinpoint generates, such as ``_email.delivered`` or ``_custom.delivered`` . For campaigns, this can also be a custom event that's specific to your application. For information about standard events, see `Streaming Amazon Pinpoint Events <https://docs.aws.amazon.com/pinpoint/latest/developerguide/event-streams.html>`_ in the *Amazon Pinpoint Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-eventtype
            '''
            result = self._values.get("event_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SetDimensionProperty"]], result)

        @builtins.property
        def metrics(self) -> typing.Any:
            '''One or more custom metrics that your application reports to Amazon Pinpoint .

            You can use these metrics as selection criteria when you create an event filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventDimensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.InAppMessageBodyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "body": "body",
            "text_color": "textColor",
        },
    )
    class InAppMessageBodyConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of main body text of the in-app message.

            :param alignment: The text alignment of the main body text of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param body: The main body text of the message.
            :param text_color: The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                in_app_message_body_config_property = pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageBodyConfigProperty(
                    alignment="alignment",
                    body="body",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9bf42c083c2798dfe493d6231b7a67cdaae0953ce6827f14e3140b5a86cb306)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if body is not None:
                self._values["body"] = body
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the main body text of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html#cfn-pinpoint-campaign-inappmessagebodyconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The main body text of the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html#cfn-pinpoint-campaign-inappmessagebodyconfig-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html#cfn-pinpoint-campaign-inappmessagebodyconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageBodyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty",
        jsii_struct_bases=[],
        name_mapping={
            "android": "android",
            "default_config": "defaultConfig",
            "ios": "ios",
            "web": "web",
        },
    )
    class InAppMessageButtonProperty:
        def __init__(
            self,
            *,
            android: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.DefaultButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ios: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            web: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration of a button that appears in an in-app message.

            :param android: An object that defines the default behavior for a button in in-app messages sent to Android.
            :param default_config: An object that defines the default behavior for a button in an in-app message.
            :param ios: An object that defines the default behavior for a button in in-app messages sent to iOS devices.
            :param web: An object that defines the default behavior for a button in in-app messages for web applications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                in_app_message_button_property = pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                    android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1084d78b83d9eec8859eaf9f987080bc355cca685978cfe90c9f8f624d92a65a)
                check_type(argname="argument android", value=android, expected_type=type_hints["android"])
                check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
                check_type(argname="argument ios", value=ios, expected_type=type_hints["ios"])
                check_type(argname="argument web", value=web, expected_type=type_hints["web"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if android is not None:
                self._values["android"] = android
            if default_config is not None:
                self._values["default_config"] = default_config
            if ios is not None:
                self._values["ios"] = ios
            if web is not None:
                self._values["web"] = web

        @builtins.property
        def android(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.OverrideButtonConfigurationProperty"]]:
            '''An object that defines the default behavior for a button in in-app messages sent to Android.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-android
            '''
            result = self._values.get("android")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.OverrideButtonConfigurationProperty"]], result)

        @builtins.property
        def default_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DefaultButtonConfigurationProperty"]]:
            '''An object that defines the default behavior for a button in an in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-defaultconfig
            '''
            result = self._values.get("default_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DefaultButtonConfigurationProperty"]], result)

        @builtins.property
        def ios(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.OverrideButtonConfigurationProperty"]]:
            '''An object that defines the default behavior for a button in in-app messages sent to iOS devices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-ios
            '''
            result = self._values.get("ios")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.OverrideButtonConfigurationProperty"]], result)

        @builtins.property
        def web(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.OverrideButtonConfigurationProperty"]]:
            '''An object that defines the default behavior for a button in in-app messages for web applications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-web
            '''
            result = self._values.get("web")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.OverrideButtonConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageButtonProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.InAppMessageContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "body_config": "bodyConfig",
            "header_config": "headerConfig",
            "image_url": "imageUrl",
            "primary_btn": "primaryBtn",
            "secondary_btn": "secondaryBtn",
        },
    )
    class InAppMessageContentProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            body_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.InAppMessageBodyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            header_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_url: typing.Optional[builtins.str] = None,
            primary_btn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.InAppMessageButtonProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secondary_btn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.InAppMessageButtonProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration and contents of an in-app message.

            :param background_color: The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).
            :param body_config: Specifies the configuration of main body text in an in-app message template.
            :param header_config: Specifies the configuration and content of the header or title text of the in-app message.
            :param image_url: The URL of the image that appears on an in-app message banner.
            :param primary_btn: An object that contains configuration information about the primary button in an in-app message.
            :param secondary_btn: An object that contains configuration information about the secondary button in an in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                in_app_message_content_property = pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageContentProperty(
                    background_color="backgroundColor",
                    body_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageBodyConfigProperty(
                        alignment="alignment",
                        body="body",
                        text_color="textColor"
                    ),
                    header_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty(
                        alignment="alignment",
                        header="header",
                        text_color="textColor"
                    ),
                    image_url="imageUrl",
                    primary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                        android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    ),
                    secondary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                        android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2f89c4425ce0b15f158a4f5ed82bd14bb8f3f5589247683deba9e1dd1f1a63a)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument body_config", value=body_config, expected_type=type_hints["body_config"])
                check_type(argname="argument header_config", value=header_config, expected_type=type_hints["header_config"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument primary_btn", value=primary_btn, expected_type=type_hints["primary_btn"])
                check_type(argname="argument secondary_btn", value=secondary_btn, expected_type=type_hints["secondary_btn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if body_config is not None:
                self._values["body_config"] = body_config
            if header_config is not None:
                self._values["header_config"] = header_config
            if image_url is not None:
                self._values["image_url"] = image_url
            if primary_btn is not None:
                self._values["primary_btn"] = primary_btn
            if secondary_btn is not None:
                self._values["secondary_btn"] = secondary_btn

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.InAppMessageBodyConfigProperty"]]:
            '''Specifies the configuration of main body text in an in-app message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-bodyconfig
            '''
            result = self._values.get("body_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.InAppMessageBodyConfigProperty"]], result)

        @builtins.property
        def header_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty"]]:
            '''Specifies the configuration and content of the header or title text of the in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-headerconfig
            '''
            result = self._values.get("header_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty"]], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image that appears on an in-app message banner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_btn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.InAppMessageButtonProperty"]]:
            '''An object that contains configuration information about the primary button in an in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-primarybtn
            '''
            result = self._values.get("primary_btn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.InAppMessageButtonProperty"]], result)

        @builtins.property
        def secondary_btn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.InAppMessageButtonProperty"]]:
            '''An object that contains configuration information about the secondary button in an in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-secondarybtn
            '''
            result = self._values.get("secondary_btn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.InAppMessageButtonProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "header": "header",
            "text_color": "textColor",
        },
    )
    class InAppMessageHeaderConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            header: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration and content of the header or title text of the in-app message.

            :param alignment: The text alignment of the title of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param header: The header or title text of the in-app message.
            :param text_color: The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                in_app_message_header_config_property = pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty(
                    alignment="alignment",
                    header="header",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a95c9a234aaf80f423aea511787a609cfeafbf48f307de4877f9d4f0f83b1651)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument header", value=header, expected_type=type_hints["header"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if header is not None:
                self._values["header"] = header
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the title of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html#cfn-pinpoint-campaign-inappmessageheaderconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header(self) -> typing.Optional[builtins.str]:
            '''The header or title text of the in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html#cfn-pinpoint-campaign-inappmessageheaderconfig-header
            '''
            result = self._values.get("header")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html#cfn-pinpoint-campaign-inappmessageheaderconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageHeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.LimitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "daily": "daily",
            "maximum_duration": "maximumDuration",
            "messages_per_second": "messagesPerSecond",
            "session": "session",
            "total": "total",
        },
    )
    class LimitsProperty:
        def __init__(
            self,
            *,
            daily: typing.Optional[jsii.Number] = None,
            maximum_duration: typing.Optional[jsii.Number] = None,
            messages_per_second: typing.Optional[jsii.Number] = None,
            session: typing.Optional[jsii.Number] = None,
            total: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the limits on the messages that a campaign can send.

            :param daily: The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period. The maximum value is 100.
            :param maximum_duration: The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign. The minimum value is 60 seconds.
            :param messages_per_second: The maximum number of messages that a campaign can send each second. The minimum value is 1. The maximum value is 20,000.
            :param session: The maximum number of messages that the campaign can send per user session.
            :param total: The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign. The maximum value is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                limits_property = pinpoint_mixins.CfnCampaignPropsMixin.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    session=123,
                    total=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e84fa518555528b08422b0fef703c5e4f481af0933a0d34d45dacf174616b6e4)
                check_type(argname="argument daily", value=daily, expected_type=type_hints["daily"])
                check_type(argname="argument maximum_duration", value=maximum_duration, expected_type=type_hints["maximum_duration"])
                check_type(argname="argument messages_per_second", value=messages_per_second, expected_type=type_hints["messages_per_second"])
                check_type(argname="argument session", value=session, expected_type=type_hints["session"])
                check_type(argname="argument total", value=total, expected_type=type_hints["total"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if daily is not None:
                self._values["daily"] = daily
            if maximum_duration is not None:
                self._values["maximum_duration"] = maximum_duration
            if messages_per_second is not None:
                self._values["messages_per_second"] = messages_per_second
            if session is not None:
                self._values["session"] = session
            if total is not None:
                self._values["total"] = total

        @builtins.property
        def daily(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period.

            The maximum value is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-daily
            '''
            result = self._values.get("daily")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_duration(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign.

            The minimum value is 60 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-maximumduration
            '''
            result = self._values.get("maximum_duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def messages_per_second(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send each second.

            The minimum value is 1. The maximum value is 20,000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-messagespersecond
            '''
            result = self._values.get("messages_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def session(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that the campaign can send per user session.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-session
            '''
            result = self._values.get("session")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign.

            The maximum value is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-total
            '''
            result = self._values.get("total")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.MessageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "adm_message": "admMessage",
            "apns_message": "apnsMessage",
            "baidu_message": "baiduMessage",
            "custom_message": "customMessage",
            "default_message": "defaultMessage",
            "email_message": "emailMessage",
            "gcm_message": "gcmMessage",
            "in_app_message": "inAppMessage",
            "sms_message": "smsMessage",
        },
    )
    class MessageConfigurationProperty:
        def __init__(
            self,
            *,
            adm_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            apns_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            baidu_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CampaignCustomMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            email_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CampaignEmailMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            gcm_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.MessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            in_app_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CampaignInAppMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sms_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CampaignSmsMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the message configuration settings for a campaign.

            :param adm_message: The message that the campaign sends through the ADM (Amazon Device Messaging) channel. If specified, this message overrides the default message.
            :param apns_message: The message that the campaign sends through the APNs (Apple Push Notification service) channel. If specified, this message overrides the default message.
            :param baidu_message: The message that the campaign sends through the Baidu (Baidu Cloud Push) channel. If specified, this message overrides the default message.
            :param custom_message: The message that the campaign sends through a custom channel, as specified by the delivery configuration ( ``CustomDeliveryConfiguration`` ) settings for the campaign. If specified, this message overrides the default message.
            :param default_message: The default message that the campaign sends through all the channels that are configured for the campaign.
            :param email_message: The message that the campaign sends through the email channel. If specified, this message overrides the default message. .. epigraph:: The maximum email message size is 200 KB. You can use email templates to send larger email messages.
            :param gcm_message: The message that the campaign sends through the GCM channel, which enables Amazon Pinpoint to send push notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service. If specified, this message overrides the default message.
            :param in_app_message: The default message for the in-app messaging channel. This message overrides the default message ( ``DefaultMessage`` ).
            :param sms_message: The message that the campaign sends through the SMS channel. If specified, this message overrides the default message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                # custom_config: Any
                
                message_configuration_property = pinpoint_mixins.CfnCampaignPropsMixin.MessageConfigurationProperty(
                    adm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    apns_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    baidu_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    custom_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignCustomMessageProperty(
                        data="data"
                    ),
                    default_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    email_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEmailMessageProperty(
                        body="body",
                        from_address="fromAddress",
                        html_body="htmlBody",
                        title="title"
                    ),
                    gcm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    in_app_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignInAppMessageProperty(
                        content=[pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageContentProperty(
                            background_color="backgroundColor",
                            body_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageBodyConfigProperty(
                                alignment="alignment",
                                body="body",
                                text_color="textColor"
                            ),
                            header_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty(
                                alignment="alignment",
                                header="header",
                                text_color="textColor"
                            ),
                            image_url="imageUrl",
                            primary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                                android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            ),
                            secondary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                                android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            )
                        )],
                        custom_config=custom_config,
                        layout="layout"
                    ),
                    sms_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignSmsMessageProperty(
                        body="body",
                        entity_id="entityId",
                        message_type="messageType",
                        origination_number="originationNumber",
                        sender_id="senderId",
                        template_id="templateId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__91f1d516dbb2e652d8f6b56adea664fec5d0e54cf111be27727f61e796afc355)
                check_type(argname="argument adm_message", value=adm_message, expected_type=type_hints["adm_message"])
                check_type(argname="argument apns_message", value=apns_message, expected_type=type_hints["apns_message"])
                check_type(argname="argument baidu_message", value=baidu_message, expected_type=type_hints["baidu_message"])
                check_type(argname="argument custom_message", value=custom_message, expected_type=type_hints["custom_message"])
                check_type(argname="argument default_message", value=default_message, expected_type=type_hints["default_message"])
                check_type(argname="argument email_message", value=email_message, expected_type=type_hints["email_message"])
                check_type(argname="argument gcm_message", value=gcm_message, expected_type=type_hints["gcm_message"])
                check_type(argname="argument in_app_message", value=in_app_message, expected_type=type_hints["in_app_message"])
                check_type(argname="argument sms_message", value=sms_message, expected_type=type_hints["sms_message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if adm_message is not None:
                self._values["adm_message"] = adm_message
            if apns_message is not None:
                self._values["apns_message"] = apns_message
            if baidu_message is not None:
                self._values["baidu_message"] = baidu_message
            if custom_message is not None:
                self._values["custom_message"] = custom_message
            if default_message is not None:
                self._values["default_message"] = default_message
            if email_message is not None:
                self._values["email_message"] = email_message
            if gcm_message is not None:
                self._values["gcm_message"] = gcm_message
            if in_app_message is not None:
                self._values["in_app_message"] = in_app_message
            if sms_message is not None:
                self._values["sms_message"] = sms_message

        @builtins.property
        def adm_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageProperty"]]:
            '''The message that the campaign sends through the ADM (Amazon Device Messaging) channel.

            If specified, this message overrides the default message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-admmessage
            '''
            result = self._values.get("adm_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageProperty"]], result)

        @builtins.property
        def apns_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageProperty"]]:
            '''The message that the campaign sends through the APNs (Apple Push Notification service) channel.

            If specified, this message overrides the default message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-apnsmessage
            '''
            result = self._values.get("apns_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageProperty"]], result)

        @builtins.property
        def baidu_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageProperty"]]:
            '''The message that the campaign sends through the Baidu (Baidu Cloud Push) channel.

            If specified, this message overrides the default message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-baidumessage
            '''
            result = self._values.get("baidu_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageProperty"]], result)

        @builtins.property
        def custom_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignCustomMessageProperty"]]:
            '''The message that the campaign sends through a custom channel, as specified by the delivery configuration ( ``CustomDeliveryConfiguration`` ) settings for the campaign.

            If specified, this message overrides the default message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-custommessage
            '''
            result = self._values.get("custom_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignCustomMessageProperty"]], result)

        @builtins.property
        def default_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageProperty"]]:
            '''The default message that the campaign sends through all the channels that are configured for the campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-defaultmessage
            '''
            result = self._values.get("default_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageProperty"]], result)

        @builtins.property
        def email_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignEmailMessageProperty"]]:
            '''The message that the campaign sends through the email channel. If specified, this message overrides the default message.

            .. epigraph::

               The maximum email message size is 200 KB. You can use email templates to send larger email messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-emailmessage
            '''
            result = self._values.get("email_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignEmailMessageProperty"]], result)

        @builtins.property
        def gcm_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageProperty"]]:
            '''The message that the campaign sends through the GCM channel, which enables Amazon Pinpoint to send push notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service.

            If specified, this message overrides the default message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-gcmmessage
            '''
            result = self._values.get("gcm_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageProperty"]], result)

        @builtins.property
        def in_app_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignInAppMessageProperty"]]:
            '''The default message for the in-app messaging channel.

            This message overrides the default message ( ``DefaultMessage`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-inappmessage
            '''
            result = self._values.get("in_app_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignInAppMessageProperty"]], result)

        @builtins.property
        def sms_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignSmsMessageProperty"]]:
            '''The message that the campaign sends through the SMS channel.

            If specified, this message overrides the default message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-smsmessage
            '''
            result = self._values.get("sms_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignSmsMessageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.MessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "image_icon_url": "imageIconUrl",
            "image_small_icon_url": "imageSmallIconUrl",
            "image_url": "imageUrl",
            "json_body": "jsonBody",
            "media_url": "mediaUrl",
            "raw_content": "rawContent",
            "silent_push": "silentPush",
            "time_to_live": "timeToLive",
            "title": "title",
            "url": "url",
        },
    )
    class MessageProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            image_icon_url: typing.Optional[builtins.str] = None,
            image_small_icon_url: typing.Optional[builtins.str] = None,
            image_url: typing.Optional[builtins.str] = None,
            json_body: typing.Optional[builtins.str] = None,
            media_url: typing.Optional[builtins.str] = None,
            raw_content: typing.Optional[builtins.str] = None,
            silent_push: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            time_to_live: typing.Optional[jsii.Number] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the content and settings for a push notification that's sent to recipients of a campaign.

            :param action: The action to occur if a recipient taps the push notification. Valid values are:. - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of iOS and Android. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The body of the notification message. The maximum number of characters is 200.
            :param image_icon_url: The URL of the image to display as the push notification icon, such as the icon for the app.
            :param image_small_icon_url: The URL of the image to display as the small, push notification icon, such as a small version of the icon for the app.
            :param image_url: The URL of an image to display in the push notification.
            :param json_body: The JSON payload to use for a silent push notification.
            :param media_url: The URL of the image or video to display in the push notification.
            :param raw_content: The raw, JSON-formatted string to use as the payload for the notification message. If specified, this value overrides all other content for the message.
            :param silent_push: Specifies whether the notification is a silent push notification, which is a push notification that doesn't display on a recipient's device. Silent push notifications can be used for cases such as updating an app's configuration, displaying messages in an in-app message center, or supporting phone home functionality.
            :param time_to_live: The number of seconds that the push notification service should keep the message, if the service is unable to deliver the notification the first time. This value is converted to an expiration value when it's sent to a push notification service. If this value is ``0`` , the service treats the notification as if it expires immediately and the service doesn't store or try to deliver the notification again. This value doesn't apply to messages that are sent through the Amazon Device Messaging (ADM) service.
            :param title: The title to display above the notification message on a recipient's device.
            :param url: The URL to open in a recipient's default mobile browser, if a recipient taps the push notification and the value of the ``Action`` property is ``URL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                message_property = pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__744f2f6614f20bc8e8f5b252e7195b133edc97af1786280813dfbfb35a7c3869)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument image_icon_url", value=image_icon_url, expected_type=type_hints["image_icon_url"])
                check_type(argname="argument image_small_icon_url", value=image_small_icon_url, expected_type=type_hints["image_small_icon_url"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument json_body", value=json_body, expected_type=type_hints["json_body"])
                check_type(argname="argument media_url", value=media_url, expected_type=type_hints["media_url"])
                check_type(argname="argument raw_content", value=raw_content, expected_type=type_hints["raw_content"])
                check_type(argname="argument silent_push", value=silent_push, expected_type=type_hints["silent_push"])
                check_type(argname="argument time_to_live", value=time_to_live, expected_type=type_hints["time_to_live"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if image_icon_url is not None:
                self._values["image_icon_url"] = image_icon_url
            if image_small_icon_url is not None:
                self._values["image_small_icon_url"] = image_small_icon_url
            if image_url is not None:
                self._values["image_url"] = image_url
            if json_body is not None:
                self._values["json_body"] = json_body
            if media_url is not None:
                self._values["media_url"] = media_url
            if raw_content is not None:
                self._values["raw_content"] = raw_content
            if silent_push is not None:
                self._values["silent_push"] = silent_push
            if time_to_live is not None:
                self._values["time_to_live"] = time_to_live
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps the push notification. Valid values are:.

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of iOS and Android.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The body of the notification message.

            The maximum number of characters is 200.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image to display as the push notification icon, such as the icon for the app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imageiconurl
            '''
            result = self._values.get("image_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_small_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image to display as the small, push notification icon, such as a small version of the icon for the app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imagesmalliconurl
            '''
            result = self._values.get("image_small_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image to display in the push notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def json_body(self) -> typing.Optional[builtins.str]:
            '''The JSON payload to use for a silent push notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-jsonbody
            '''
            result = self._values.get("json_body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def media_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image or video to display in the push notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-mediaurl
            '''
            result = self._values.get("media_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def raw_content(self) -> typing.Optional[builtins.str]:
            '''The raw, JSON-formatted string to use as the payload for the notification message.

            If specified, this value overrides all other content for the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-rawcontent
            '''
            result = self._values.get("raw_content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def silent_push(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the notification is a silent push notification, which is a push notification that doesn't display on a recipient's device.

            Silent push notifications can be used for cases such as updating an app's configuration, displaying messages in an in-app message center, or supporting phone home functionality.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-silentpush
            '''
            result = self._values.get("silent_push")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def time_to_live(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds that the push notification service should keep the message, if the service is unable to deliver the notification the first time.

            This value is converted to an expiration value when it's sent to a push notification service. If this value is ``0`` , the service treats the notification as if it expires immediately and the service doesn't store or try to deliver the notification again.

            This value doesn't apply to messages that are sent through the Amazon Device Messaging (ADM) service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-timetolive
            '''
            result = self._values.get("time_to_live")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to display above the notification message on a recipient's device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in a recipient's default mobile browser, if a recipient taps the push notification and the value of the ``Action`` property is ``URL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"button_action": "buttonAction", "link": "link"},
    )
    class OverrideButtonConfigurationProperty:
        def __init__(
            self,
            *,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of a button with settings that are specific to a certain device type.

            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-overridebuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                override_button_configuration_property = pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                    button_action="buttonAction",
                    link="link"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c916cab6c5be94f92e7aad54cafe1f7d4d68bdb0f094f4f33da83607a99a08f)
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-overridebuttonconfiguration.html#cfn-pinpoint-campaign-overridebuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-overridebuttonconfiguration.html#cfn-pinpoint-campaign-overridebuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverrideButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.QuietTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class QuietTimeProperty:
        def __init__(
            self,
            *,
            end: typing.Optional[builtins.str] = None,
            start: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the start and end times that define a time range when messages aren't sent to endpoints.

            :param end: The specific time when quiet time ends. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.
            :param start: The specific time when quiet time begins. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-quiettime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                quiet_time_property = pinpoint_mixins.CfnCampaignPropsMixin.QuietTimeProperty(
                    end="end",
                    start="start"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__32e57d36ee7e92356d9eb5066d9f73f18f31af04088fd7088cc67f2559de9207)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end is not None:
                self._values["end"] = end
            if start is not None:
                self._values["start"] = start

        @builtins.property
        def end(self) -> typing.Optional[builtins.str]:
            '''The specific time when quiet time ends.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-quiettime.html#cfn-pinpoint-campaign-quiettime-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start(self) -> typing.Optional[builtins.str]:
            '''The specific time when quiet time begins.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-quiettime.html#cfn-pinpoint-campaign-quiettime-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuietTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_time": "endTime",
            "event_filter": "eventFilter",
            "frequency": "frequency",
            "is_local_time": "isLocalTime",
            "quiet_time": "quietTime",
            "start_time": "startTime",
            "time_zone": "timeZone",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            end_time: typing.Optional[builtins.str] = None,
            event_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CampaignEventFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            frequency: typing.Optional[builtins.str] = None,
            is_local_time: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            quiet_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.QuietTimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            start_time: typing.Optional[builtins.str] = None,
            time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the schedule settings for a campaign.

            :param end_time: The scheduled time, in ISO 8601 format, when the campaign ended or will end.
            :param event_filter: The type of event that causes the campaign to be sent, if the value of the ``Frequency`` property is ``EVENT`` .
            :param frequency: Specifies how often the campaign is sent or whether the campaign is sent in response to a specific event.
            :param is_local_time: Specifies whether the start and end times for the campaign schedule use each recipient's local time. To base the schedule on each recipient's local time, set this value to ``true`` .
            :param quiet_time: The default quiet time for the campaign. Quiet time is a specific time range when a campaign doesn't send messages to endpoints, if all the following conditions are met: - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value. - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the campaign. - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the campaign. If any of the preceding conditions isn't met, the endpoint will receive messages from the campaign, even if quiet time is enabled.
            :param start_time: The scheduled time when the campaign began or will begin. Valid values are: ``IMMEDIATE`` , to start the campaign immediately; or, a specific time in ISO 8601 format.
            :param time_zone: The starting UTC offset for the campaign schedule, if the value of the ``IsLocalTime`` property is ``true`` . Valid values are: ``UTC, UTC+01, UTC+02, UTC+03, UTC+03:30, UTC+04, UTC+04:30, UTC+05, UTC+05:30, UTC+05:45, UTC+06, UTC+06:30, UTC+07, UTC+08, UTC+09, UTC+09:30, UTC+10, UTC+10:30, UTC+11, UTC+12, UTC+13, UTC-02, UTC-03, UTC-04, UTC-05, UTC-06, UTC-07, UTC-08, UTC-09, UTC-10,`` and ``UTC-11`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                # attributes: Any
                # metrics: Any
                
                schedule_property = pinpoint_mixins.CfnCampaignPropsMixin.ScheduleProperty(
                    end_time="endTime",
                    event_filter=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEventFilterProperty(
                        dimensions=pinpoint_mixins.CfnCampaignPropsMixin.EventDimensionsProperty(
                            attributes=attributes,
                            event_type=pinpoint_mixins.CfnCampaignPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            metrics=metrics
                        ),
                        filter_type="filterType"
                    ),
                    frequency="frequency",
                    is_local_time=False,
                    quiet_time=pinpoint_mixins.CfnCampaignPropsMixin.QuietTimeProperty(
                        end="end",
                        start="start"
                    ),
                    start_time="startTime",
                    time_zone="timeZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d6727be0b4098b61be735b0f0e0814f072cc9815213377308b6e33dc3fb27b6)
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument event_filter", value=event_filter, expected_type=type_hints["event_filter"])
                check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
                check_type(argname="argument is_local_time", value=is_local_time, expected_type=type_hints["is_local_time"])
                check_type(argname="argument quiet_time", value=quiet_time, expected_type=type_hints["quiet_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
                check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_time is not None:
                self._values["end_time"] = end_time
            if event_filter is not None:
                self._values["event_filter"] = event_filter
            if frequency is not None:
                self._values["frequency"] = frequency
            if is_local_time is not None:
                self._values["is_local_time"] = is_local_time
            if quiet_time is not None:
                self._values["quiet_time"] = quiet_time
            if start_time is not None:
                self._values["start_time"] = start_time
            if time_zone is not None:
                self._values["time_zone"] = time_zone

        @builtins.property
        def end_time(self) -> typing.Optional[builtins.str]:
            '''The scheduled time, in ISO 8601 format, when the campaign ended or will end.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-endtime
            '''
            result = self._values.get("end_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignEventFilterProperty"]]:
            '''The type of event that causes the campaign to be sent, if the value of the ``Frequency`` property is ``EVENT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-eventfilter
            '''
            result = self._values.get("event_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CampaignEventFilterProperty"]], result)

        @builtins.property
        def frequency(self) -> typing.Optional[builtins.str]:
            '''Specifies how often the campaign is sent or whether the campaign is sent in response to a specific event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-frequency
            '''
            result = self._values.get("frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_local_time(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the start and end times for the campaign schedule use each recipient's local time.

            To base the schedule on each recipient's local time, set this value to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-islocaltime
            '''
            result = self._values.get("is_local_time")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def quiet_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.QuietTimeProperty"]]:
            '''The default quiet time for the campaign.

            Quiet time is a specific time range when a campaign doesn't send messages to endpoints, if all the following conditions are met:

            - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value.
            - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the campaign.
            - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the campaign.

            If any of the preceding conditions isn't met, the endpoint will receive messages from the campaign, even if quiet time is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-quiettime
            '''
            result = self._values.get("quiet_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.QuietTimeProperty"]], result)

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            '''The scheduled time when the campaign began or will begin.

            Valid values are: ``IMMEDIATE`` , to start the campaign immediately; or, a specific time in ISO 8601 format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_zone(self) -> typing.Optional[builtins.str]:
            '''The starting UTC offset for the campaign schedule, if the value of the ``IsLocalTime`` property is ``true`` .

            Valid values are: ``UTC, UTC+01, UTC+02, UTC+03, UTC+03:30, UTC+04, UTC+04:30, UTC+05, UTC+05:30, UTC+05:45, UTC+06, UTC+06:30, UTC+07, UTC+08, UTC+09, UTC+09:30, UTC+10, UTC+10:30, UTC+11, UTC+12, UTC+13, UTC-02, UTC-03, UTC-04, UTC-05, UTC-06, UTC-07, UTC-08, UTC-09, UTC-10,`` and ``UTC-11`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-timezone
            '''
            result = self._values.get("time_zone")
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
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.SetDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class SetDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the dimension type and values for a segment dimension.

            :param dimension_type: The type of segment dimension to use. Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.
            :param values: The criteria values to use for the segment dimension. Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                set_dimension_property = pinpoint_mixins.CfnCampaignPropsMixin.SetDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18acfce852144900828a5bd56dcd8232eeeac4e750382f369369f2243afd483d)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The type of segment dimension to use.

            Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html#cfn-pinpoint-campaign-setdimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The criteria values to use for the segment dimension.

            Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html#cfn-pinpoint-campaign-setdimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.TemplateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email_template": "emailTemplate",
            "push_template": "pushTemplate",
            "sms_template": "smsTemplate",
            "voice_template": "voiceTemplate",
        },
    )
    class TemplateConfigurationProperty:
        def __init__(
            self,
            *,
            email_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            push_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sms_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            voice_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the message template to use for the message, for each type of channel.

            :param email_template: The email template to use for the message.
            :param push_template: The push notification template to use for the message.
            :param sms_template: The SMS template to use for the message.
            :param voice_template: The voice template to use for the message. This object isn't supported for campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                template_configuration_property = pinpoint_mixins.CfnCampaignPropsMixin.TemplateConfigurationProperty(
                    email_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    push_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    sms_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    voice_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                        name="name",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50e25f02fdb6430dfad99f546b8a94f9fe423b9bd53f41eeb8ca78584d8a0d5b)
                check_type(argname="argument email_template", value=email_template, expected_type=type_hints["email_template"])
                check_type(argname="argument push_template", value=push_template, expected_type=type_hints["push_template"])
                check_type(argname="argument sms_template", value=sms_template, expected_type=type_hints["sms_template"])
                check_type(argname="argument voice_template", value=voice_template, expected_type=type_hints["voice_template"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email_template is not None:
                self._values["email_template"] = email_template
            if push_template is not None:
                self._values["push_template"] = push_template
            if sms_template is not None:
                self._values["sms_template"] = sms_template
            if voice_template is not None:
                self._values["voice_template"] = voice_template

        @builtins.property
        def email_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateProperty"]]:
            '''The email template to use for the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-emailtemplate
            '''
            result = self._values.get("email_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateProperty"]], result)

        @builtins.property
        def push_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateProperty"]]:
            '''The push notification template to use for the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-pushtemplate
            '''
            result = self._values.get("push_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateProperty"]], result)

        @builtins.property
        def sms_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateProperty"]]:
            '''The SMS template to use for the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-smstemplate
            '''
            result = self._values.get("sms_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateProperty"]], result)

        @builtins.property
        def voice_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateProperty"]]:
            '''The voice template to use for the message.

            This object isn't supported for campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-voicetemplate
            '''
            result = self._values.get("voice_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.TemplateProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class TemplateProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the name and version of the message template to use for the message.

            :param name: The name of the message template to use for the message. If specified, this value must match the name of an existing message template.
            :param version: The unique identifier for the version of the message template to use for the message. If specified, this value must match the identifier for an existing template version. To retrieve a list of versions and version identifiers for a template, use the `Template Versions <https://docs.aws.amazon.com/pinpoint/latest/apireference/templates-template-name-template-type-versions.html>`_ resource. If you don't specify a value for this property, Amazon Pinpoint uses the *active version* of the template. The *active version* is typically the version of a template that's been most recently reviewed and approved for use, depending on your workflow. It isn't necessarily the latest version of a template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-template.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                template_property = pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58697bafda66b00785decd7c3977a8cb8cbd51e3afec522ee5605a172e82c2c4)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the message template to use for the message.

            If specified, this value must match the name of an existing message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-template.html#cfn-pinpoint-campaign-template-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the version of the message template to use for the message.

            If specified, this value must match the identifier for an existing template version. To retrieve a list of versions and version identifiers for a template, use the `Template Versions <https://docs.aws.amazon.com/pinpoint/latest/apireference/templates-template-name-template-type-versions.html>`_ resource.

            If you don't specify a value for this property, Amazon Pinpoint uses the *active version* of the template. The *active version* is typically the version of a template that's been most recently reviewed and approved for use, depending on your workflow. It isn't necessarily the latest version of a template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-template.html#cfn-pinpoint-campaign-template-version
            '''
            result = self._values.get("version")
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
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnCampaignPropsMixin.WriteTreatmentResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_delivery_configuration": "customDeliveryConfiguration",
            "message_configuration": "messageConfiguration",
            "schedule": "schedule",
            "size_percent": "sizePercent",
            "template_configuration": "templateConfiguration",
            "treatment_description": "treatmentDescription",
            "treatment_name": "treatmentName",
        },
    )
    class WriteTreatmentResourceProperty:
        def __init__(
            self,
            *,
            custom_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            message_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.MessageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            size_percent: typing.Optional[jsii.Number] = None,
            template_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TemplateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            treatment_description: typing.Optional[builtins.str] = None,
            treatment_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the settings for a campaign treatment.

            A *treatment* is a variation of a campaign that's used for A/B testing of a campaign.

            :param custom_delivery_configuration: The delivery configuration settings for sending the treatment through a custom channel. This object is required if the ``MessageConfiguration`` object for the treatment specifies a ``CustomMessage`` object.
            :param message_configuration: The message configuration settings for the treatment.
            :param schedule: The schedule settings for the treatment.
            :param size_percent: The allocated percentage of users (segment members) to send the treatment to.
            :param template_configuration: The message template to use for the treatment.
            :param treatment_description: A custom description of the treatment.
            :param treatment_name: A custom name for the treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                # attributes: Any
                # custom_config: Any
                # metrics: Any
                
                write_treatment_resource_property = pinpoint_mixins.CfnCampaignPropsMixin.WriteTreatmentResourceProperty(
                    custom_delivery_configuration=pinpoint_mixins.CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty(
                        delivery_uri="deliveryUri",
                        endpoint_types=["endpointTypes"]
                    ),
                    message_configuration=pinpoint_mixins.CfnCampaignPropsMixin.MessageConfigurationProperty(
                        adm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        apns_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        baidu_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        custom_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignCustomMessageProperty(
                            data="data"
                        ),
                        default_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        email_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEmailMessageProperty(
                            body="body",
                            from_address="fromAddress",
                            html_body="htmlBody",
                            title="title"
                        ),
                        gcm_message=pinpoint_mixins.CfnCampaignPropsMixin.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        in_app_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignInAppMessageProperty(
                            content=[pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageContentProperty(
                                background_color="backgroundColor",
                                body_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageBodyConfigProperty(
                                    alignment="alignment",
                                    body="body",
                                    text_color="textColor"
                                ),
                                header_config=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty(
                                    alignment="alignment",
                                    header="header",
                                    text_color="textColor"
                                ),
                                image_url="imageUrl",
                                primary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                                    android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                ),
                                secondary_btn=pinpoint_mixins.CfnCampaignPropsMixin.InAppMessageButtonProperty(
                                    android=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint_mixins.CfnCampaignPropsMixin.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint_mixins.CfnCampaignPropsMixin.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                )
                            )],
                            custom_config=custom_config,
                            layout="layout"
                        ),
                        sms_message=pinpoint_mixins.CfnCampaignPropsMixin.CampaignSmsMessageProperty(
                            body="body",
                            entity_id="entityId",
                            message_type="messageType",
                            origination_number="originationNumber",
                            sender_id="senderId",
                            template_id="templateId"
                        )
                    ),
                    schedule=pinpoint_mixins.CfnCampaignPropsMixin.ScheduleProperty(
                        end_time="endTime",
                        event_filter=pinpoint_mixins.CfnCampaignPropsMixin.CampaignEventFilterProperty(
                            dimensions=pinpoint_mixins.CfnCampaignPropsMixin.EventDimensionsProperty(
                                attributes=attributes,
                                event_type=pinpoint_mixins.CfnCampaignPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                metrics=metrics
                            ),
                            filter_type="filterType"
                        ),
                        frequency="frequency",
                        is_local_time=False,
                        quiet_time=pinpoint_mixins.CfnCampaignPropsMixin.QuietTimeProperty(
                            end="end",
                            start="start"
                        ),
                        start_time="startTime",
                        time_zone="timeZone"
                    ),
                    size_percent=123,
                    template_configuration=pinpoint_mixins.CfnCampaignPropsMixin.TemplateConfigurationProperty(
                        email_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        push_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        sms_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        voice_template=pinpoint_mixins.CfnCampaignPropsMixin.TemplateProperty(
                            name="name",
                            version="version"
                        )
                    ),
                    treatment_description="treatmentDescription",
                    treatment_name="treatmentName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5bb9593bc3c501df9484d40adc1b657be47b04fbcd7c26ac0f7eb78265d81147)
                check_type(argname="argument custom_delivery_configuration", value=custom_delivery_configuration, expected_type=type_hints["custom_delivery_configuration"])
                check_type(argname="argument message_configuration", value=message_configuration, expected_type=type_hints["message_configuration"])
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
                check_type(argname="argument size_percent", value=size_percent, expected_type=type_hints["size_percent"])
                check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
                check_type(argname="argument treatment_description", value=treatment_description, expected_type=type_hints["treatment_description"])
                check_type(argname="argument treatment_name", value=treatment_name, expected_type=type_hints["treatment_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_delivery_configuration is not None:
                self._values["custom_delivery_configuration"] = custom_delivery_configuration
            if message_configuration is not None:
                self._values["message_configuration"] = message_configuration
            if schedule is not None:
                self._values["schedule"] = schedule
            if size_percent is not None:
                self._values["size_percent"] = size_percent
            if template_configuration is not None:
                self._values["template_configuration"] = template_configuration
            if treatment_description is not None:
                self._values["treatment_description"] = treatment_description
            if treatment_name is not None:
                self._values["treatment_name"] = treatment_name

        @builtins.property
        def custom_delivery_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty"]]:
            '''The delivery configuration settings for sending the treatment through a custom channel.

            This object is required if the ``MessageConfiguration`` object for the treatment specifies a ``CustomMessage`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-customdeliveryconfiguration
            '''
            result = self._values.get("custom_delivery_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty"]], result)

        @builtins.property
        def message_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageConfigurationProperty"]]:
            '''The message configuration settings for the treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-messageconfiguration
            '''
            result = self._values.get("message_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MessageConfigurationProperty"]], result)

        @builtins.property
        def schedule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ScheduleProperty"]]:
            '''The schedule settings for the treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-schedule
            '''
            result = self._values.get("schedule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ScheduleProperty"]], result)

        @builtins.property
        def size_percent(self) -> typing.Optional[jsii.Number]:
            '''The allocated percentage of users (segment members) to send the treatment to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-sizepercent
            '''
            result = self._values.get("size_percent")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def template_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateConfigurationProperty"]]:
            '''The message template to use for the treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-templateconfiguration
            '''
            result = self._values.get("template_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TemplateConfigurationProperty"]], result)

        @builtins.property
        def treatment_description(self) -> typing.Optional[builtins.str]:
            '''A custom description of the treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-treatmentdescription
            '''
            result = self._values.get("treatment_description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def treatment_name(self) -> typing.Optional[builtins.str]:
            '''A custom name for the treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-treatmentname
            '''
            result = self._values.get("treatment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WriteTreatmentResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnEmailChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "configuration_set": "configurationSet",
        "enabled": "enabled",
        "from_address": "fromAddress",
        "identity": "identity",
        "orchestration_sending_role_arn": "orchestrationSendingRoleArn",
        "role_arn": "roleArn",
    },
)
class CfnEmailChannelMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        configuration_set: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        from_address: typing.Optional[builtins.str] = None,
        identity: typing.Optional[builtins.str] = None,
        orchestration_sending_role_arn: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEmailChannelPropsMixin.

        :param application_id: The unique identifier for the Amazon Pinpoint application that you're specifying the email channel for.
        :param configuration_set: The `Amazon SES configuration set <https://docs.aws.amazon.com/ses/latest/APIReference/API_ConfigurationSet.html>`_ that you want to apply to messages that you send through the channel.
        :param enabled: Specifies whether to enable the email channel for the application.
        :param from_address: The verified email address that you want to send email from when you send email through the channel.
        :param identity: The Amazon Resource Name (ARN) of the identity, verified with Amazon Simple Email Service (Amazon SES), that you want to use when you send email through the channel.
        :param orchestration_sending_role_arn: The ARN of an IAM role for Amazon Pinpoint to use to send email from your campaigns or journeys through Amazon SES .
        :param role_arn: The ARN of the AWS Identity and Access Management (IAM) role that you want Amazon Pinpoint to use when it submits email-related event data for the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_email_channel_mixin_props = pinpoint_mixins.CfnEmailChannelMixinProps(
                application_id="applicationId",
                configuration_set="configurationSet",
                enabled=False,
                from_address="fromAddress",
                identity="identity",
                orchestration_sending_role_arn="orchestrationSendingRoleArn",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bf5efe1c44f4d4822fcb29a16505db7147755d8cc3aee683ecd60f3f852a8f)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument configuration_set", value=configuration_set, expected_type=type_hints["configuration_set"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument from_address", value=from_address, expected_type=type_hints["from_address"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument orchestration_sending_role_arn", value=orchestration_sending_role_arn, expected_type=type_hints["orchestration_sending_role_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if configuration_set is not None:
            self._values["configuration_set"] = configuration_set
        if enabled is not None:
            self._values["enabled"] = enabled
        if from_address is not None:
            self._values["from_address"] = from_address
        if identity is not None:
            self._values["identity"] = identity
        if orchestration_sending_role_arn is not None:
            self._values["orchestration_sending_role_arn"] = orchestration_sending_role_arn
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that you're specifying the email channel for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration_set(self) -> typing.Optional[builtins.str]:
        '''The `Amazon SES configuration set <https://docs.aws.amazon.com/ses/latest/APIReference/API_ConfigurationSet.html>`_ that you want to apply to messages that you send through the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-configurationset
        '''
        result = self._values.get("configuration_set")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable the email channel for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def from_address(self) -> typing.Optional[builtins.str]:
        '''The verified email address that you want to send email from when you send email through the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-fromaddress
        '''
        result = self._values.get("from_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the identity, verified with Amazon Simple Email Service (Amazon SES), that you want to use when you send email through the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-identity
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def orchestration_sending_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role for Amazon Pinpoint to use to send email from your campaigns or journeys through Amazon SES .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-orchestrationsendingrolearn
        '''
        result = self._values.get("orchestration_sending_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Identity and Access Management (IAM) role that you want Amazon Pinpoint to use when it submits email-related event data for the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEmailChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnEmailChannelPropsMixin",
):
    '''A *channel* is a type of platform that you can deliver messages to.

    You can use the email channel to send email to users. Before you can use Amazon Pinpoint to send email, you must enable the email channel for an Amazon Pinpoint application.

    The EmailChannel resource represents the status, identity, and other settings of the email channel for an application

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html
    :cloudformationResource: AWS::Pinpoint::EmailChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_email_channel_props_mixin = pinpoint_mixins.CfnEmailChannelPropsMixin(pinpoint_mixins.CfnEmailChannelMixinProps(
            application_id="applicationId",
            configuration_set="configurationSet",
            enabled=False,
            from_address="fromAddress",
            identity="identity",
            orchestration_sending_role_arn="orchestrationSendingRoleArn",
            role_arn="roleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEmailChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::EmailChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44a38596ffe5481c92374f39b4971beef85061d58bf30618b0879071c9863b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a92fb222d8f183220d8c5310db44543f0357d8d849527e91b5574190b6ca3f45)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0035014b0b5199fa23130934dc0d9e7f39297cd8841cf2c62f309a9263b736)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEmailChannelMixinProps:
        return typing.cast(CfnEmailChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnEmailTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_substitutions": "defaultSubstitutions",
        "html_part": "htmlPart",
        "subject": "subject",
        "tags": "tags",
        "template_description": "templateDescription",
        "template_name": "templateName",
        "text_part": "textPart",
    },
)
class CfnEmailTemplateMixinProps:
    def __init__(
        self,
        *,
        default_substitutions: typing.Optional[builtins.str] = None,
        html_part: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
        template_name: typing.Optional[builtins.str] = None,
        text_part: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEmailTemplatePropsMixin.

        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param html_part: The message body, in HTML format, to use in email messages that are based on the message template. We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.
        :param subject: The subject line, or title, to use in email messages that are based on the message template.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        :param template_name: The name of the message template.
        :param text_part: The message body, in plain text format, to use in email messages that are based on the message template. We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            # tags: Any
            
            cfn_email_template_mixin_props = pinpoint_mixins.CfnEmailTemplateMixinProps(
                default_substitutions="defaultSubstitutions",
                html_part="htmlPart",
                subject="subject",
                tags=tags,
                template_description="templateDescription",
                template_name="templateName",
                text_part="textPart"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a9b1632c75f56a79c5acaa7e9dd1ba95d19ebd367d793d1d4a1d7274ff0026)
            check_type(argname="argument default_substitutions", value=default_substitutions, expected_type=type_hints["default_substitutions"])
            check_type(argname="argument html_part", value=html_part, expected_type=type_hints["html_part"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument text_part", value=text_part, expected_type=type_hints["text_part"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if html_part is not None:
            self._values["html_part"] = html_part
        if subject is not None:
            self._values["subject"] = subject
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description
        if template_name is not None:
            self._values["template_name"] = template_name
        if text_part is not None:
            self._values["text_part"] = text_part

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-defaultsubstitutions
        '''
        result = self._values.get("default_substitutions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def html_part(self) -> typing.Optional[builtins.str]:
        '''The message body, in HTML format, to use in email messages that are based on the message template.

        We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-htmlpart
        '''
        result = self._values.get("html_part")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        '''The subject line, or title, to use in email messages that are based on the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-subject
        '''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatename
        '''
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text_part(self) -> typing.Optional[builtins.str]:
        '''The message body, in plain text format, to use in email messages that are based on the message template.

        We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-textpart
        '''
        result = self._values.get("text_part")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEmailTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnEmailTemplatePropsMixin",
):
    '''Creates a message template that you can use in messages that are sent through the email channel.

    A *message template* is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html
    :cloudformationResource: AWS::Pinpoint::EmailTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        # tags: Any
        
        cfn_email_template_props_mixin = pinpoint_mixins.CfnEmailTemplatePropsMixin(pinpoint_mixins.CfnEmailTemplateMixinProps(
            default_substitutions="defaultSubstitutions",
            html_part="htmlPart",
            subject="subject",
            tags=tags,
            template_description="templateDescription",
            template_name="templateName",
            text_part="textPart"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEmailTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::EmailTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16ef553798d8e177814f78a06d4ec641e4f2be2ec2a1bd60ed01e87c1b6658f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__824c69a4bbee0b26288c2d4ba0abe55ff8d3553d2d71489694b1123a8d512a36)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05f2b7e8b832032ed0ccd8966d0ba8c8edf173830a63842f016f0bb9369cc05)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEmailTemplateMixinProps:
        return typing.cast(CfnEmailTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnEventStreamMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "destination_stream_arn": "destinationStreamArn",
        "role_arn": "roleArn",
    },
)
class CfnEventStreamMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        destination_stream_arn: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEventStreamPropsMixin.

        :param application_id: The unique identifier for the Amazon Pinpoint application that you want to export data from.
        :param destination_stream_arn: The Amazon Resource Name (ARN) of the Amazon Kinesis Data Stream or Amazon Data Firehose delivery stream that you want to publish event data to. For a Kinesis Data Stream, the ARN format is: ``arn:aws:kinesis: region : account-id :stream/ stream_name`` For a Firehose delivery stream, the ARN format is: ``arn:aws:firehose: region : account-id :deliverystream/ stream_name``
        :param role_arn: The AWS Identity and Access Management (IAM) role that authorizes Amazon Pinpoint to publish event data to the stream in your AWS account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_event_stream_mixin_props = pinpoint_mixins.CfnEventStreamMixinProps(
                application_id="applicationId",
                destination_stream_arn="destinationStreamArn",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65eb52a33ff235d68fd046f0e9e557577da2bc9052492592abeac9aad4800dd4)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument destination_stream_arn", value=destination_stream_arn, expected_type=type_hints["destination_stream_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if destination_stream_arn is not None:
            self._values["destination_stream_arn"] = destination_stream_arn
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that you want to export data from.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_stream_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Kinesis Data Stream or Amazon Data Firehose delivery stream that you want to publish event data to.

        For a Kinesis Data Stream, the ARN format is: ``arn:aws:kinesis: region : account-id :stream/ stream_name``

        For a Firehose delivery stream, the ARN format is: ``arn:aws:firehose: region : account-id :deliverystream/ stream_name``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-destinationstreamarn
        '''
        result = self._values.get("destination_stream_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The AWS Identity and Access Management (IAM) role that authorizes Amazon Pinpoint to publish event data to the stream in your AWS account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventStreamMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEventStreamPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnEventStreamPropsMixin",
):
    '''Creates a new event stream for an application or updates the settings of an existing event stream for an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html
    :cloudformationResource: AWS::Pinpoint::EventStream
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_event_stream_props_mixin = pinpoint_mixins.CfnEventStreamPropsMixin(pinpoint_mixins.CfnEventStreamMixinProps(
            application_id="applicationId",
            destination_stream_arn="destinationStreamArn",
            role_arn="roleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEventStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::EventStream``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b4df4e03dfc9c943f3c9faabd6792441390a7bcf9631bd1099448a4c4502b3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80c28d66a9cceebc5a01c871572f1ceeb588202399c6fd98653cba270e7f759f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ed5e8dfc64f2d5a15095dea61705695028650eaf4c0bf75b86a70800e03b91)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEventStreamMixinProps:
        return typing.cast(CfnEventStreamMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnGCMChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "application_id": "applicationId",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "service_json": "serviceJson",
    },
)
class CfnGCMChannelMixinProps:
    def __init__(
        self,
        *,
        api_key: typing.Optional[builtins.str] = None,
        application_id: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        service_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnGCMChannelPropsMixin.

        :param api_key: The Web API key, also called the *server key* , that you received from Google to communicate with Google services.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the GCM channel applies to.
        :param default_authentication_method: The default authentication method used for GCM. Values are either "TOKEN" or "KEY". Defaults to "KEY".
        :param enabled: Specifies whether to enable the GCM channel for the Amazon Pinpoint application.
        :param service_json: The contents of the JSON file provided by Google during registration in order to generate an access token for authentication. For more information see `Migrate from legacy FCM APIs to HTTP v1 <https://docs.aws.amazon.com/https://firebase.google.com/docs/cloud-messaging/migrate-v1>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_gCMChannel_mixin_props = pinpoint_mixins.CfnGCMChannelMixinProps(
                api_key="apiKey",
                application_id="applicationId",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                service_json="serviceJson"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7305a7546dca84aaeaf15f3cf4b301450cf88730bf181c024dcb58b7f18c609)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument service_json", value=service_json, expected_type=type_hints["service_json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_key is not None:
            self._values["api_key"] = api_key
        if application_id is not None:
            self._values["application_id"] = application_id
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if service_json is not None:
            self._values["service_json"] = service_json

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        '''The Web API key, also called the *server key* , that you received from Google to communicate with Google services.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-apikey
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that the GCM channel applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method used for GCM.

        Values are either "TOKEN" or "KEY". Defaults to "KEY".

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable the GCM channel for the Amazon Pinpoint application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def service_json(self) -> typing.Optional[builtins.str]:
        '''The contents of the JSON file provided by Google during registration in order to generate an access token for authentication.

        For more information see `Migrate from legacy FCM APIs to HTTP v1 <https://docs.aws.amazon.com/https://firebase.google.com/docs/cloud-messaging/migrate-v1>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-servicejson
        '''
        result = self._values.get("service_json")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGCMChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGCMChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnGCMChannelPropsMixin",
):
    '''A *channel* is a type of platform that you can deliver messages to.

    You can use the GCM channel to send push notification messages to the Firebase Cloud Messaging (FCM) service, which replaced the Google Cloud Messaging (GCM) service. Before you use Amazon Pinpoint to send notifications to FCM, you have to enable the GCM channel for an Amazon Pinpoint application.

    The GCMChannel resource represents the status and authentication settings of the GCM channel for an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html
    :cloudformationResource: AWS::Pinpoint::GCMChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_gCMChannel_props_mixin = pinpoint_mixins.CfnGCMChannelPropsMixin(pinpoint_mixins.CfnGCMChannelMixinProps(
            api_key="apiKey",
            application_id="applicationId",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            service_json="serviceJson"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGCMChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::GCMChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e60ec568e317e069d5690858611273e400278e4212ae7b4ca86852ff94430c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2927a3935ef29fbcdadc0cec0eac51c404ea4cd656021dc45656a7463127605)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f930066e03b289ed967495821722491945ac9c95db5c662510a9aa90fe50df)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGCMChannelMixinProps:
        return typing.cast(CfnGCMChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnInAppTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "custom_config": "customConfig",
        "layout": "layout",
        "tags": "tags",
        "template_description": "templateDescription",
        "template_name": "templateName",
    },
)
class CfnInAppTemplateMixinProps:
    def __init__(
        self,
        *,
        content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInAppTemplatePropsMixin.InAppMessageContentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        custom_config: typing.Any = None,
        layout: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
        template_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnInAppTemplatePropsMixin.

        :param content: An object that contains information about the content of an in-app message, including its title and body text, text colors, background colors, images, buttons, and behaviors.
        :param custom_config: Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.
        :param layout: A string that determines the appearance of the in-app message. You can specify one of the following:. - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page. - ``TOP_BANNER`` – a message that appears as a banner at the top of the page. - ``OVERLAYS`` – a message that covers entire screen. - ``MOBILE_FEED`` – a message that appears in a window in front of the page. - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page. - ``CAROUSEL`` – a scrollable layout of up to five unique messages.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: An optional description of the in-app template.
        :param template_name: The name of the in-app message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            # custom_config: Any
            # tags: Any
            
            cfn_in_app_template_mixin_props = pinpoint_mixins.CfnInAppTemplateMixinProps(
                content=[pinpoint_mixins.CfnInAppTemplatePropsMixin.InAppMessageContentProperty(
                    background_color="backgroundColor",
                    body_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.BodyConfigProperty(
                        alignment="alignment",
                        body="body",
                        text_color="textColor"
                    ),
                    header_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.HeaderConfigProperty(
                        alignment="alignment",
                        header="header",
                        text_color="textColor"
                    ),
                    image_url="imageUrl",
                    primary_btn=pinpoint_mixins.CfnInAppTemplatePropsMixin.ButtonConfigProperty(
                        android=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    ),
                    secondary_btn=pinpoint_mixins.CfnInAppTemplatePropsMixin.ButtonConfigProperty(
                        android=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    )
                )],
                custom_config=custom_config,
                layout="layout",
                tags=tags,
                template_description="templateDescription",
                template_name="templateName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a34e3c907857fa18cc77baf3f122e12ac776a84dc6e5395c6506479eb2e3e63)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument custom_config", value=custom_config, expected_type=type_hints["custom_config"])
            check_type(argname="argument layout", value=layout, expected_type=type_hints["layout"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if custom_config is not None:
            self._values["custom_config"] = custom_config
        if layout is not None:
            self._values["layout"] = layout
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description
        if template_name is not None:
            self._values["template_name"] = template_name

    @builtins.property
    def content(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.InAppMessageContentProperty"]]]]:
        '''An object that contains information about the content of an in-app message, including its title and body text, text colors, background colors, images, buttons, and behaviors.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.InAppMessageContentProperty"]]]], result)

    @builtins.property
    def custom_config(self) -> typing.Any:
        '''Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-customconfig
        '''
        result = self._values.get("custom_config")
        return typing.cast(typing.Any, result)

    @builtins.property
    def layout(self) -> typing.Optional[builtins.str]:
        '''A string that determines the appearance of the in-app message. You can specify one of the following:.

        - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page.
        - ``TOP_BANNER`` – a message that appears as a banner at the top of the page.
        - ``OVERLAYS`` – a message that covers entire screen.
        - ``MOBILE_FEED`` – a message that appears in a window in front of the page.
        - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page.
        - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-layout
        '''
        result = self._values.get("layout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the in-app template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the in-app message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-templatename
        '''
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInAppTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInAppTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnInAppTemplatePropsMixin",
):
    '''Creates a message template that you can use to send in-app messages.

    A message template is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications. The In-App channel is unavailable in AWS GovCloud (US).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html
    :cloudformationResource: AWS::Pinpoint::InAppTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        # custom_config: Any
        # tags: Any
        
        cfn_in_app_template_props_mixin = pinpoint_mixins.CfnInAppTemplatePropsMixin(pinpoint_mixins.CfnInAppTemplateMixinProps(
            content=[pinpoint_mixins.CfnInAppTemplatePropsMixin.InAppMessageContentProperty(
                background_color="backgroundColor",
                body_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.BodyConfigProperty(
                    alignment="alignment",
                    body="body",
                    text_color="textColor"
                ),
                header_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.HeaderConfigProperty(
                    alignment="alignment",
                    header="header",
                    text_color="textColor"
                ),
                image_url="imageUrl",
                primary_btn=pinpoint_mixins.CfnInAppTemplatePropsMixin.ButtonConfigProperty(
                    android=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                ),
                secondary_btn=pinpoint_mixins.CfnInAppTemplatePropsMixin.ButtonConfigProperty(
                    android=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                )
            )],
            custom_config=custom_config,
            layout="layout",
            tags=tags,
            template_description="templateDescription",
            template_name="templateName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInAppTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::InAppTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c472843c6e49f8d8fdfadda4852087b75d5e87811dd41211aa87be5fc60e7d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a4f53f14277bcfdb7de73261fcdda068b2d228fa9820e26c314f1d655af4306)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__563360f5dab2e59e859c7178d041ca2dbda61661c2cea5f68ccf048a6b12857d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInAppTemplateMixinProps:
        return typing.cast(CfnInAppTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnInAppTemplatePropsMixin.BodyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "body": "body",
            "text_color": "textColor",
        },
    )
    class BodyConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of the main body text of the in-app message.

            :param alignment: The text alignment of the main body text of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param body: The main body text of the message.
            :param text_color: The color of the body text, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                body_config_property = pinpoint_mixins.CfnInAppTemplatePropsMixin.BodyConfigProperty(
                    alignment="alignment",
                    body="body",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a777e4cb215c4dcf140c11b4eb928dfeda970d6a89206209cd2c1f96af1a1b53)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if body is not None:
                self._values["body"] = body
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the main body text of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html#cfn-pinpoint-inapptemplate-bodyconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The main body text of the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html#cfn-pinpoint-inapptemplate-bodyconfig-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html#cfn-pinpoint-inapptemplate-bodyconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BodyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnInAppTemplatePropsMixin.ButtonConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "android": "android",
            "default_config": "defaultConfig",
            "ios": "ios",
            "web": "web",
        },
    )
    class ButtonConfigProperty:
        def __init__(
            self,
            *,
            android: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ios: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            web: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the behavior of buttons that appear in an in-app message template.

            :param android: Optional button configuration to use for in-app messages sent to Android devices. This button configuration overrides the default button configuration.
            :param default_config: Specifies the default behavior of a button that appears in an in-app message. You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.
            :param ios: Optional button configuration to use for in-app messages sent to iOS devices. This button configuration overrides the default button configuration.
            :param web: Optional button configuration to use for in-app messages sent to web applications. This button configuration overrides the default button configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                button_config_property = pinpoint_mixins.CfnInAppTemplatePropsMixin.ButtonConfigProperty(
                    android=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ee17eb5854db07fc6c6699b057d12536630f81681d658a5d16b69aea94ca6d5)
                check_type(argname="argument android", value=android, expected_type=type_hints["android"])
                check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
                check_type(argname="argument ios", value=ios, expected_type=type_hints["ios"])
                check_type(argname="argument web", value=web, expected_type=type_hints["web"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if android is not None:
                self._values["android"] = android
            if default_config is not None:
                self._values["default_config"] = default_config
            if ios is not None:
                self._values["ios"] = ios
            if web is not None:
                self._values["web"] = web

        @builtins.property
        def android(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty"]]:
            '''Optional button configuration to use for in-app messages sent to Android devices.

            This button configuration overrides the default button configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-android
            '''
            result = self._values.get("android")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty"]], result)

        @builtins.property
        def default_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty"]]:
            '''Specifies the default behavior of a button that appears in an in-app message.

            You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-defaultconfig
            '''
            result = self._values.get("default_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty"]], result)

        @builtins.property
        def ios(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty"]]:
            '''Optional button configuration to use for in-app messages sent to iOS devices.

            This button configuration overrides the default button configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-ios
            '''
            result = self._values.get("ios")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty"]], result)

        @builtins.property
        def web(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty"]]:
            '''Optional button configuration to use for in-app messages sent to web applications.

            This button configuration overrides the default button configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-web
            '''
            result = self._values.get("web")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ButtonConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "border_radius": "borderRadius",
            "button_action": "buttonAction",
            "link": "link",
            "text": "text",
            "text_color": "textColor",
        },
    )
    class DefaultButtonConfigurationProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            border_radius: typing.Optional[jsii.Number] = None,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
            text: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the default behavior of a button that appears in an in-app message.

            You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.

            :param background_color: The background color of a button, expressed as a hex color code (such as #000000 for black).
            :param border_radius: The border radius of a button.
            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.
            :param text: The text that appears on a button in an in-app message.
            :param text_color: The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                default_button_configuration_property = pinpoint_mixins.CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty(
                    background_color="backgroundColor",
                    border_radius=123,
                    button_action="buttonAction",
                    link="link",
                    text="text",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f161f518d24bbbbed257f6afa45c1b4b029d26d159c26247f3345b61c265bdf1)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument border_radius", value=border_radius, expected_type=type_hints["border_radius"])
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if border_radius is not None:
                self._values["border_radius"] = border_radius
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link
            if text is not None:
                self._values["text"] = text
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color of a button, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def border_radius(self) -> typing.Optional[jsii.Number]:
            '''The border radius of a button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-borderradius
            '''
            result = self._values.get("border_radius")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The text that appears on a button in an in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnInAppTemplatePropsMixin.HeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "header": "header",
            "text_color": "textColor",
        },
    )
    class HeaderConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            header: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration and content of the header or title text of the in-app message.

            :param alignment: The text alignment of the title of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param header: The title text of the in-app message.
            :param text_color: The color of the title text, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                header_config_property = pinpoint_mixins.CfnInAppTemplatePropsMixin.HeaderConfigProperty(
                    alignment="alignment",
                    header="header",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed1940e0aa991d2797b8dc4cc7115e9aa4f5b19f6ab81d8c1b8b6a9d945ce77c)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument header", value=header, expected_type=type_hints["header"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if header is not None:
                self._values["header"] = header
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the title of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html#cfn-pinpoint-inapptemplate-headerconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header(self) -> typing.Optional[builtins.str]:
            '''The title text of the in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html#cfn-pinpoint-inapptemplate-headerconfig-header
            '''
            result = self._values.get("header")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the title text, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html#cfn-pinpoint-inapptemplate-headerconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnInAppTemplatePropsMixin.InAppMessageContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "body_config": "bodyConfig",
            "header_config": "headerConfig",
            "image_url": "imageUrl",
            "primary_btn": "primaryBtn",
            "secondary_btn": "secondaryBtn",
        },
    )
    class InAppMessageContentProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            body_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInAppTemplatePropsMixin.BodyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            header_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInAppTemplatePropsMixin.HeaderConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_url: typing.Optional[builtins.str] = None,
            primary_btn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInAppTemplatePropsMixin.ButtonConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secondary_btn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInAppTemplatePropsMixin.ButtonConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration of an in-app message, including its header, body, buttons, colors, and images.

            :param background_color: The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).
            :param body_config: An object that contains configuration information about the header or title text of the in-app message.
            :param header_config: An object that contains configuration information about the header or title text of the in-app message.
            :param image_url: The URL of the image that appears on an in-app message banner.
            :param primary_btn: An object that contains configuration information about the primary button in an in-app message.
            :param secondary_btn: An object that contains configuration information about the secondary button in an in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                in_app_message_content_property = pinpoint_mixins.CfnInAppTemplatePropsMixin.InAppMessageContentProperty(
                    background_color="backgroundColor",
                    body_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.BodyConfigProperty(
                        alignment="alignment",
                        body="body",
                        text_color="textColor"
                    ),
                    header_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.HeaderConfigProperty(
                        alignment="alignment",
                        header="header",
                        text_color="textColor"
                    ),
                    image_url="imageUrl",
                    primary_btn=pinpoint_mixins.CfnInAppTemplatePropsMixin.ButtonConfigProperty(
                        android=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    ),
                    secondary_btn=pinpoint_mixins.CfnInAppTemplatePropsMixin.ButtonConfigProperty(
                        android=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint_mixins.CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d6e1fc6160581b6b83297ef105009fc1651d9b6c53502b12089dfe237b1e062)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument body_config", value=body_config, expected_type=type_hints["body_config"])
                check_type(argname="argument header_config", value=header_config, expected_type=type_hints["header_config"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument primary_btn", value=primary_btn, expected_type=type_hints["primary_btn"])
                check_type(argname="argument secondary_btn", value=secondary_btn, expected_type=type_hints["secondary_btn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if body_config is not None:
                self._values["body_config"] = body_config
            if header_config is not None:
                self._values["header_config"] = header_config
            if image_url is not None:
                self._values["image_url"] = image_url
            if primary_btn is not None:
                self._values["primary_btn"] = primary_btn
            if secondary_btn is not None:
                self._values["secondary_btn"] = secondary_btn

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.BodyConfigProperty"]]:
            '''An object that contains configuration information about the header or title text of the in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-bodyconfig
            '''
            result = self._values.get("body_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.BodyConfigProperty"]], result)

        @builtins.property
        def header_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.HeaderConfigProperty"]]:
            '''An object that contains configuration information about the header or title text of the in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-headerconfig
            '''
            result = self._values.get("header_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.HeaderConfigProperty"]], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image that appears on an in-app message banner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_btn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.ButtonConfigProperty"]]:
            '''An object that contains configuration information about the primary button in an in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-primarybtn
            '''
            result = self._values.get("primary_btn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.ButtonConfigProperty"]], result)

        @builtins.property
        def secondary_btn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.ButtonConfigProperty"]]:
            '''An object that contains configuration information about the secondary button in an in-app message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-secondarybtn
            '''
            result = self._values.get("secondary_btn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInAppTemplatePropsMixin.ButtonConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"button_action": "buttonAction", "link": "link"},
    )
    class OverrideButtonConfigurationProperty:
        def __init__(
            self,
            *,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of a button with settings that are specific to a certain device type.

            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-overridebuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                override_button_configuration_property = pinpoint_mixins.CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty(
                    button_action="buttonAction",
                    link="link"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02fccb4ffb54d9885de6de5d0730b539df768a88042e06822ae9a763f57e01e1)
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-overridebuttonconfiguration.html#cfn-pinpoint-inapptemplate-overridebuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-overridebuttonconfiguration.html#cfn-pinpoint-inapptemplate-overridebuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverrideButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnPushTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "adm": "adm",
        "apns": "apns",
        "baidu": "baidu",
        "default": "default",
        "default_substitutions": "defaultSubstitutions",
        "gcm": "gcm",
        "tags": "tags",
        "template_description": "templateDescription",
        "template_name": "templateName",
    },
)
class CfnPushTemplateMixinProps:
    def __init__(
        self,
        *,
        adm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        apns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPushTemplatePropsMixin.APNSPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        baidu: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        default: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPushTemplatePropsMixin.DefaultPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_substitutions: typing.Optional[builtins.str] = None,
        gcm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
        template_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPushTemplatePropsMixin.

        :param adm: The message template to use for the ADM (Amazon Device Messaging) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param apns: The message template to use for the APNs (Apple Push Notification service) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param baidu: The message template to use for the Baidu (Baidu Cloud Push) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param default: The default message template to use for push notification channels.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param gcm: The message template to use for the GCM channel, which is used to send notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        :param template_name: The name of the message template to use for the message. If specified, this value must match the name of an existing message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            # tags: Any
            
            cfn_push_template_mixin_props = pinpoint_mixins.CfnPushTemplateMixinProps(
                adm=pinpoint_mixins.CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                apns=pinpoint_mixins.CfnPushTemplatePropsMixin.APNSPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    media_url="mediaUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                baidu=pinpoint_mixins.CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                default=pinpoint_mixins.CfnPushTemplatePropsMixin.DefaultPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                default_substitutions="defaultSubstitutions",
                gcm=pinpoint_mixins.CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                tags=tags,
                template_description="templateDescription",
                template_name="templateName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc360cdbf06f07cb37910d5d6df4f2984a280abf9ee4cc47f76bcd0aba5b5db3)
            check_type(argname="argument adm", value=adm, expected_type=type_hints["adm"])
            check_type(argname="argument apns", value=apns, expected_type=type_hints["apns"])
            check_type(argname="argument baidu", value=baidu, expected_type=type_hints["baidu"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument default_substitutions", value=default_substitutions, expected_type=type_hints["default_substitutions"])
            check_type(argname="argument gcm", value=gcm, expected_type=type_hints["gcm"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if adm is not None:
            self._values["adm"] = adm
        if apns is not None:
            self._values["apns"] = apns
        if baidu is not None:
            self._values["baidu"] = baidu
        if default is not None:
            self._values["default"] = default
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if gcm is not None:
            self._values["gcm"] = gcm
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description
        if template_name is not None:
            self._values["template_name"] = template_name

    @builtins.property
    def adm(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty"]]:
        '''The message template to use for the ADM (Amazon Device Messaging) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-adm
        '''
        result = self._values.get("adm")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty"]], result)

    @builtins.property
    def apns(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPushTemplatePropsMixin.APNSPushNotificationTemplateProperty"]]:
        '''The message template to use for the APNs (Apple Push Notification service) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-apns
        '''
        result = self._values.get("apns")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPushTemplatePropsMixin.APNSPushNotificationTemplateProperty"]], result)

    @builtins.property
    def baidu(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty"]]:
        '''The message template to use for the Baidu (Baidu Cloud Push) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-baidu
        '''
        result = self._values.get("baidu")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty"]], result)

    @builtins.property
    def default(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPushTemplatePropsMixin.DefaultPushNotificationTemplateProperty"]]:
        '''The default message template to use for push notification channels.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-default
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPushTemplatePropsMixin.DefaultPushNotificationTemplateProperty"]], result)

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-defaultsubstitutions
        '''
        result = self._values.get("default_substitutions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcm(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty"]]:
        '''The message template to use for the GCM channel, which is used to send notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-gcm
        '''
        result = self._values.get("gcm")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the message template to use for the message.

        If specified, this value must match the name of an existing message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatename
        '''
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPushTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPushTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnPushTemplatePropsMixin",
):
    '''Creates a message template that you can use in messages that are sent through a push notification channel.

    A *message template* is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html
    :cloudformationResource: AWS::Pinpoint::PushTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        # tags: Any
        
        cfn_push_template_props_mixin = pinpoint_mixins.CfnPushTemplatePropsMixin(pinpoint_mixins.CfnPushTemplateMixinProps(
            adm=pinpoint_mixins.CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty(
                action="action",
                body="body",
                image_icon_url="imageIconUrl",
                image_url="imageUrl",
                small_image_icon_url="smallImageIconUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            apns=pinpoint_mixins.CfnPushTemplatePropsMixin.APNSPushNotificationTemplateProperty(
                action="action",
                body="body",
                media_url="mediaUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            baidu=pinpoint_mixins.CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty(
                action="action",
                body="body",
                image_icon_url="imageIconUrl",
                image_url="imageUrl",
                small_image_icon_url="smallImageIconUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            default=pinpoint_mixins.CfnPushTemplatePropsMixin.DefaultPushNotificationTemplateProperty(
                action="action",
                body="body",
                sound="sound",
                title="title",
                url="url"
            ),
            default_substitutions="defaultSubstitutions",
            gcm=pinpoint_mixins.CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty(
                action="action",
                body="body",
                image_icon_url="imageIconUrl",
                image_url="imageUrl",
                small_image_icon_url="smallImageIconUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            tags=tags,
            template_description="templateDescription",
            template_name="templateName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPushTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::PushTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3919970457bf4a81e91ded4fe1d52d0f92a0787f9857243e58bc9349d5fec8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cea071d1a0c5b227d96ce44e0f5088fca2743996a98ac7868a435f95ff843de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af1782419b173ca8339e9912f5a3f6bb953b50075dd6d154b8b0973ecede4da)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPushTemplateMixinProps:
        return typing.cast(CfnPushTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnPushTemplatePropsMixin.APNSPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "media_url": "mediaUrl",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class APNSPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            media_url: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies channel-specific content and settings for a message template that can be used in push notifications that are sent through the APNs (Apple Push Notification service) channel.

            :param action: The action to occur if a recipient taps a push notification that's based on the message template. Valid values are: - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS platform. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The message body to use in push notifications that are based on the message template.
            :param media_url: The URL of an image or video to display in push notifications that are based on the message template.
            :param sound: The key for the sound to play when the recipient receives a push notification that's based on the message template. The value for this key is the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.
            :param title: The title to use in push notifications that are based on the message template. This title appears above the notification message on a recipient's device.
            :param url: The URL to open in the recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                a_pNSPush_notification_template_property = pinpoint_mixins.CfnPushTemplatePropsMixin.APNSPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    media_url="mediaUrl",
                    sound="sound",
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__37687b0fded5962a8403469dc7acc3bb74275bfd84b89e65ff522f59ce30f0fb)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument media_url", value=media_url, expected_type=type_hints["media_url"])
                check_type(argname="argument sound", value=sound, expected_type=type_hints["sound"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if media_url is not None:
                self._values["media_url"] = media_url
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps a push notification that's based on the message template.

            Valid values are:

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS platform.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The message body to use in push notifications that are based on the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def media_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image or video to display in push notifications that are based on the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-mediaurl
            '''
            result = self._values.get("media_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            '''The key for the sound to play when the recipient receives a push notification that's based on the message template.

            The value for this key is the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-sound
            '''
            result = self._values.get("sound")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to use in push notifications that are based on the message template.

            This title appears above the notification message on a recipient's device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in the recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "APNSPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "image_icon_url": "imageIconUrl",
            "image_url": "imageUrl",
            "small_image_icon_url": "smallImageIconUrl",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class AndroidPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            image_icon_url: typing.Optional[builtins.str] = None,
            image_url: typing.Optional[builtins.str] = None,
            small_image_icon_url: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies channel-specific content and settings for a message template that can be used in push notifications that are sent through the ADM (Amazon Device Messaging), Baidu (Baidu Cloud Push), or GCM (Firebase Cloud Messaging, formerly Google Cloud Messaging) channel.

            :param action: The action to occur if a recipient taps a push notification that's based on the message template. Valid values are: - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This action uses the deep-linking features of the Android platform. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The message body to use in a push notification that's based on the message template.
            :param image_icon_url: The URL of the large icon image to display in the content view of a push notification that's based on the message template.
            :param image_url: The URL of an image to display in a push notification that's based on the message template.
            :param small_image_icon_url: The URL of the small icon image to display in the status bar and the content view of a push notification that's based on the message template.
            :param sound: The sound to play when a recipient receives a push notification that's based on the message template. You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` .
            :param title: The title to use in a push notification that's based on the message template. This title appears above the notification message on a recipient's device.
            :param url: The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                android_push_notification_template_property = pinpoint_mixins.CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15e52bd22a04b00a9e008e659a5d0314116329626228f82df9f784f9c15089b5)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument image_icon_url", value=image_icon_url, expected_type=type_hints["image_icon_url"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument small_image_icon_url", value=small_image_icon_url, expected_type=type_hints["small_image_icon_url"])
                check_type(argname="argument sound", value=sound, expected_type=type_hints["sound"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if image_icon_url is not None:
                self._values["image_icon_url"] = image_icon_url
            if image_url is not None:
                self._values["image_url"] = image_url
            if small_image_icon_url is not None:
                self._values["small_image_icon_url"] = small_image_icon_url
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps a push notification that's based on the message template.

            Valid values are:

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This action uses the deep-linking features of the Android platform.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The message body to use in a push notification that's based on the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the large icon image to display in the content view of a push notification that's based on the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-imageiconurl
            '''
            result = self._values.get("image_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image to display in a push notification that's based on the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def small_image_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the small icon image to display in the status bar and the content view of a push notification that's based on the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-smallimageiconurl
            '''
            result = self._values.get("small_image_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            '''The sound to play when a recipient receives a push notification that's based on the message template.

            You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-sound
            '''
            result = self._values.get("sound")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to use in a push notification that's based on the message template.

            This title appears above the notification message on a recipient's device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AndroidPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnPushTemplatePropsMixin.DefaultPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class DefaultPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the default settings and content for a message template that can be used in messages that are sent through a push notification channel.

            :param action: The action to occur if a recipient taps a push notification that's based on the message template. Valid values are: - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS and Android platforms. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The message body to use in push notifications that are based on the message template.
            :param sound: The sound to play when a recipient receives a push notification that's based on the message template. You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` . For an iOS platform, this value is the key for the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.
            :param title: The title to use in push notifications that are based on the message template. This title appears above the notification message on a recipient's device.
            :param url: The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                default_push_notification_template_property = pinpoint_mixins.CfnPushTemplatePropsMixin.DefaultPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    sound="sound",
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad920b6450be39fb3f60e0fd89c90a0a228b3a27f4164e36b167b35b66f1c0f7)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument sound", value=sound, expected_type=type_hints["sound"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps a push notification that's based on the message template.

            Valid values are:

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS and Android platforms.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The message body to use in push notifications that are based on the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            '''The sound to play when a recipient receives a push notification that's based on the message template.

            You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` .

            For an iOS platform, this value is the key for the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-sound
            '''
            result = self._values.get("sound")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to use in push notifications that are based on the message template.

            This title appears above the notification message on a recipient's device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSMSChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "enabled": "enabled",
        "sender_id": "senderId",
        "short_code": "shortCode",
    },
)
class CfnSMSChannelMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        sender_id: typing.Optional[builtins.str] = None,
        short_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSMSChannelPropsMixin.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the SMS channel applies to.
        :param enabled: Specifies whether to enable the SMS channel for the application.
        :param sender_id: The identity that you want to display on recipients' devices when they receive messages from the SMS channel. .. epigraph:: SenderIDs are only supported in certain countries and regions. For more information, see `Supported Countries and Regions <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ in the *Amazon Pinpoint User Guide* .
        :param short_code: The registered short code that you want to use when you send messages through the SMS channel. .. epigraph:: For information about obtaining a dedicated short code for sending SMS messages, see `Requesting Dedicated Short Codes for SMS Messaging with Amazon Pinpoint <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-awssupport-short-code.html>`_ in the *Amazon Pinpoint User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_sMSChannel_mixin_props = pinpoint_mixins.CfnSMSChannelMixinProps(
                application_id="applicationId",
                enabled=False,
                sender_id="senderId",
                short_code="shortCode"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4cceb113c845c823629fac850a547ac7b305c81b831d6470f270e9c8148b348)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument sender_id", value=sender_id, expected_type=type_hints["sender_id"])
            check_type(argname="argument short_code", value=short_code, expected_type=type_hints["short_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if enabled is not None:
            self._values["enabled"] = enabled
        if sender_id is not None:
            self._values["sender_id"] = sender_id
        if short_code is not None:
            self._values["short_code"] = short_code

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that the SMS channel applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable the SMS channel for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def sender_id(self) -> typing.Optional[builtins.str]:
        '''The identity that you want to display on recipients' devices when they receive messages from the SMS channel.

        .. epigraph::

           SenderIDs are only supported in certain countries and regions. For more information, see `Supported Countries and Regions <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ in the *Amazon Pinpoint User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-senderid
        '''
        result = self._values.get("sender_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def short_code(self) -> typing.Optional[builtins.str]:
        '''The registered short code that you want to use when you send messages through the SMS channel.

        .. epigraph::

           For information about obtaining a dedicated short code for sending SMS messages, see `Requesting Dedicated Short Codes for SMS Messaging with Amazon Pinpoint <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-awssupport-short-code.html>`_ in the *Amazon Pinpoint User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-shortcode
        '''
        result = self._values.get("short_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSMSChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSMSChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSMSChannelPropsMixin",
):
    '''A *channel* is a type of platform that you can deliver messages to.

    To send an SMS text message, you send the message through the SMS channel. Before you can use Amazon Pinpoint to send text messages, you have to enable the SMS channel for an Amazon Pinpoint application.

    The SMSChannel resource represents the status, sender ID, and other settings for the SMS channel for an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html
    :cloudformationResource: AWS::Pinpoint::SMSChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_sMSChannel_props_mixin = pinpoint_mixins.CfnSMSChannelPropsMixin(pinpoint_mixins.CfnSMSChannelMixinProps(
            application_id="applicationId",
            enabled=False,
            sender_id="senderId",
            short_code="shortCode"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSMSChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::SMSChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b02daf6ca3003a33f0a0a6f1c36f2e7068f68cbfbd96de629462c0ea20e434d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90f4fbbcee6bf031c0fdd5e93012e9931b3ac125c673f6fe656c084082414bcd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53ed908c2222289b87245ec87189cac2820869adb460301a6f15fb81592cf1a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSMSChannelMixinProps:
        return typing.cast(CfnSMSChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "dimensions": "dimensions",
        "name": "name",
        "segment_groups": "segmentGroups",
        "tags": "tags",
    },
)
class CfnSegmentMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SegmentDimensionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        segment_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SegmentGroupsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnSegmentPropsMixin.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the segment is associated with.
        :param dimensions: An array that defines the dimensions for the segment.
        :param name: The name of the segment. .. epigraph:: A segment must have a name otherwise it will not appear in the Amazon Pinpoint console.
        :param segment_groups: The segment group to use and the dimensions to apply to the group's base segments in order to build the segment. A segment group can consist of zero or more base segments. Your request can include only one segment group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            # attributes: Any
            # metrics: Any
            # tags: Any
            # user_attributes: Any
            
            cfn_segment_mixin_props = pinpoint_mixins.CfnSegmentMixinProps(
                application_id="applicationId",
                dimensions=pinpoint_mixins.CfnSegmentPropsMixin.SegmentDimensionsProperty(
                    attributes=attributes,
                    behavior=pinpoint_mixins.CfnSegmentPropsMixin.BehaviorProperty(
                        recency=pinpoint_mixins.CfnSegmentPropsMixin.RecencyProperty(
                            duration="duration",
                            recency_type="recencyType"
                        )
                    ),
                    demographic=pinpoint_mixins.CfnSegmentPropsMixin.DemographicProperty(
                        app_version=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        channel=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        device_type=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        make=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        model=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        platform=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    ),
                    location=pinpoint_mixins.CfnSegmentPropsMixin.LocationProperty(
                        country=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        gps_point=pinpoint_mixins.CfnSegmentPropsMixin.GPSPointProperty(
                            coordinates=pinpoint_mixins.CfnSegmentPropsMixin.CoordinatesProperty(
                                latitude=123,
                                longitude=123
                            ),
                            range_in_kilometers=123
                        )
                    ),
                    metrics=metrics,
                    user_attributes=user_attributes
                ),
                name="name",
                segment_groups=pinpoint_mixins.CfnSegmentPropsMixin.SegmentGroupsProperty(
                    groups=[pinpoint_mixins.CfnSegmentPropsMixin.GroupsProperty(
                        dimensions=[pinpoint_mixins.CfnSegmentPropsMixin.SegmentDimensionsProperty(
                            attributes=attributes,
                            behavior=pinpoint_mixins.CfnSegmentPropsMixin.BehaviorProperty(
                                recency=pinpoint_mixins.CfnSegmentPropsMixin.RecencyProperty(
                                    duration="duration",
                                    recency_type="recencyType"
                                )
                            ),
                            demographic=pinpoint_mixins.CfnSegmentPropsMixin.DemographicProperty(
                                app_version=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                channel=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                device_type=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                make=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                model=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                platform=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            location=pinpoint_mixins.CfnSegmentPropsMixin.LocationProperty(
                                country=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                gps_point=pinpoint_mixins.CfnSegmentPropsMixin.GPSPointProperty(
                                    coordinates=pinpoint_mixins.CfnSegmentPropsMixin.CoordinatesProperty(
                                        latitude=123,
                                        longitude=123
                                    ),
                                    range_in_kilometers=123
                                )
                            ),
                            metrics=metrics,
                            user_attributes=user_attributes
                        )],
                        source_segments=[pinpoint_mixins.CfnSegmentPropsMixin.SourceSegmentsProperty(
                            id="id",
                            version=123
                        )],
                        source_type="sourceType",
                        type="type"
                    )],
                    include="include"
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf5bccc93e00660e1ec67c69272e8fe86b3e31c43d5092e9a57ead21b66bf04)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument segment_groups", value=segment_groups, expected_type=type_hints["segment_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if name is not None:
            self._values["name"] = name
        if segment_groups is not None:
            self._values["segment_groups"] = segment_groups
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that the segment is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SegmentDimensionsProperty"]]:
        '''An array that defines the dimensions for the segment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-dimensions
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SegmentDimensionsProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the segment.

        .. epigraph::

           A segment must have a name otherwise it will not appear in the Amazon Pinpoint console.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_groups(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SegmentGroupsProperty"]]:
        '''The segment group to use and the dimensions to apply to the group's base segments in order to build the segment.

        A segment group can consist of zero or more base segments. Your request can include only one segment group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-segmentgroups
        '''
        result = self._values.get("segment_groups")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SegmentGroupsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSegmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSegmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin",
):
    '''Updates the configuration, dimension, and other settings for an existing segment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html
    :cloudformationResource: AWS::Pinpoint::Segment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        # attributes: Any
        # metrics: Any
        # tags: Any
        # user_attributes: Any
        
        cfn_segment_props_mixin = pinpoint_mixins.CfnSegmentPropsMixin(pinpoint_mixins.CfnSegmentMixinProps(
            application_id="applicationId",
            dimensions=pinpoint_mixins.CfnSegmentPropsMixin.SegmentDimensionsProperty(
                attributes=attributes,
                behavior=pinpoint_mixins.CfnSegmentPropsMixin.BehaviorProperty(
                    recency=pinpoint_mixins.CfnSegmentPropsMixin.RecencyProperty(
                        duration="duration",
                        recency_type="recencyType"
                    )
                ),
                demographic=pinpoint_mixins.CfnSegmentPropsMixin.DemographicProperty(
                    app_version=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    channel=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    device_type=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    make=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    model=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    platform=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    )
                ),
                location=pinpoint_mixins.CfnSegmentPropsMixin.LocationProperty(
                    country=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    gps_point=pinpoint_mixins.CfnSegmentPropsMixin.GPSPointProperty(
                        coordinates=pinpoint_mixins.CfnSegmentPropsMixin.CoordinatesProperty(
                            latitude=123,
                            longitude=123
                        ),
                        range_in_kilometers=123
                    )
                ),
                metrics=metrics,
                user_attributes=user_attributes
            ),
            name="name",
            segment_groups=pinpoint_mixins.CfnSegmentPropsMixin.SegmentGroupsProperty(
                groups=[pinpoint_mixins.CfnSegmentPropsMixin.GroupsProperty(
                    dimensions=[pinpoint_mixins.CfnSegmentPropsMixin.SegmentDimensionsProperty(
                        attributes=attributes,
                        behavior=pinpoint_mixins.CfnSegmentPropsMixin.BehaviorProperty(
                            recency=pinpoint_mixins.CfnSegmentPropsMixin.RecencyProperty(
                                duration="duration",
                                recency_type="recencyType"
                            )
                        ),
                        demographic=pinpoint_mixins.CfnSegmentPropsMixin.DemographicProperty(
                            app_version=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            channel=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            device_type=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            make=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            model=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            platform=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        ),
                        location=pinpoint_mixins.CfnSegmentPropsMixin.LocationProperty(
                            country=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            gps_point=pinpoint_mixins.CfnSegmentPropsMixin.GPSPointProperty(
                                coordinates=pinpoint_mixins.CfnSegmentPropsMixin.CoordinatesProperty(
                                    latitude=123,
                                    longitude=123
                                ),
                                range_in_kilometers=123
                            )
                        ),
                        metrics=metrics,
                        user_attributes=user_attributes
                    )],
                    source_segments=[pinpoint_mixins.CfnSegmentPropsMixin.SourceSegmentsProperty(
                        id="id",
                        version=123
                    )],
                    source_type="sourceType",
                    type="type"
                )],
                include="include"
            ),
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSegmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::Segment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d859b090913775364783816130ae920a75be6e262515aa87583a39ade38fcbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3fabfbad555b37487ef47d2657a38c565d1e2c1b305b63b571d4e65b6924692)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b4c83fc2eb2392ebe2e05776cbc93aede4924759f8afd108bafc3d76004e50)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSegmentMixinProps:
        return typing.cast(CfnSegmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.BehaviorProperty",
        jsii_struct_bases=[],
        name_mapping={"recency": "recency"},
    )
    class BehaviorProperty:
        def __init__(
            self,
            *,
            recency: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.RecencyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies behavior-based criteria for the segment, such as how recently users have used your app.

            :param recency: Specifies how recently segment members were active.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-behavior.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                behavior_property = pinpoint_mixins.CfnSegmentPropsMixin.BehaviorProperty(
                    recency=pinpoint_mixins.CfnSegmentPropsMixin.RecencyProperty(
                        duration="duration",
                        recency_type="recencyType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed354882c80eaef5421f892e58153c993c7121162442369bb25b2e4d9f7ed26c)
                check_type(argname="argument recency", value=recency, expected_type=type_hints["recency"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if recency is not None:
                self._values["recency"] = recency

        @builtins.property
        def recency(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.RecencyProperty"]]:
            '''Specifies how recently segment members were active.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-behavior.html#cfn-pinpoint-segment-behavior-recency
            '''
            result = self._values.get("recency")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.RecencyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BehaviorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.CoordinatesProperty",
        jsii_struct_bases=[],
        name_mapping={"latitude": "latitude", "longitude": "longitude"},
    )
    class CoordinatesProperty:
        def __init__(
            self,
            *,
            latitude: typing.Optional[jsii.Number] = None,
            longitude: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the GPS coordinates of a location.

            :param latitude: The latitude coordinate of the location.
            :param longitude: The longitude coordinate of the location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-coordinates.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                coordinates_property = pinpoint_mixins.CfnSegmentPropsMixin.CoordinatesProperty(
                    latitude=123,
                    longitude=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6917be5d090634f383b2c9616d783f5d6cbca0e79482cc0686056d6d3026d9fa)
                check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
                check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if latitude is not None:
                self._values["latitude"] = latitude
            if longitude is not None:
                self._values["longitude"] = longitude

        @builtins.property
        def latitude(self) -> typing.Optional[jsii.Number]:
            '''The latitude coordinate of the location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-coordinates.html#cfn-pinpoint-segment-coordinates-latitude
            '''
            result = self._values.get("latitude")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def longitude(self) -> typing.Optional[jsii.Number]:
            '''The longitude coordinate of the location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-coordinates.html#cfn-pinpoint-segment-coordinates-longitude
            '''
            result = self._values.get("longitude")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoordinatesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.DemographicProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_version": "appVersion",
            "channel": "channel",
            "device_type": "deviceType",
            "make": "make",
            "model": "model",
            "platform": "platform",
        },
    )
    class DemographicProperty:
        def __init__(
            self,
            *,
            app_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            channel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            device_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            make: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            model: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            platform: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies demographic-based criteria, such as device platform, for the segment.

            :param app_version: The app version criteria for the segment.
            :param channel: The channel criteria for the segment.
            :param device_type: The device type criteria for the segment.
            :param make: The device make criteria for the segment.
            :param model: The device model criteria for the segment.
            :param platform: The device platform criteria for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-demographic.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                demographic_property = pinpoint_mixins.CfnSegmentPropsMixin.DemographicProperty(
                    app_version=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    channel=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    device_type=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    make=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    model=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    platform=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__30b0bba6fcf634c61b672b5ce5057056d8775279948aafc5fcd65fe6039835e4)
                check_type(argname="argument app_version", value=app_version, expected_type=type_hints["app_version"])
                check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
                check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
                check_type(argname="argument make", value=make, expected_type=type_hints["make"])
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_version is not None:
                self._values["app_version"] = app_version
            if channel is not None:
                self._values["channel"] = channel
            if device_type is not None:
                self._values["device_type"] = device_type
            if make is not None:
                self._values["make"] = make
            if model is not None:
                self._values["model"] = model
            if platform is not None:
                self._values["platform"] = platform

        @builtins.property
        def app_version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]]:
            '''The app version criteria for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-demographic.html#cfn-pinpoint-segment-demographic-appversion
            '''
            result = self._values.get("app_version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]], result)

        @builtins.property
        def channel(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]]:
            '''The channel criteria for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-demographic.html#cfn-pinpoint-segment-demographic-channel
            '''
            result = self._values.get("channel")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]], result)

        @builtins.property
        def device_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]]:
            '''The device type criteria for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-demographic.html#cfn-pinpoint-segment-demographic-devicetype
            '''
            result = self._values.get("device_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]], result)

        @builtins.property
        def make(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]]:
            '''The device make criteria for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-demographic.html#cfn-pinpoint-segment-demographic-make
            '''
            result = self._values.get("make")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]], result)

        @builtins.property
        def model(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]]:
            '''The device model criteria for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-demographic.html#cfn-pinpoint-segment-demographic-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]], result)

        @builtins.property
        def platform(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]]:
            '''The device platform criteria for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-demographic.html#cfn-pinpoint-segment-demographic-platform
            '''
            result = self._values.get("platform")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DemographicProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.GPSPointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "coordinates": "coordinates",
            "range_in_kilometers": "rangeInKilometers",
        },
    )
    class GPSPointProperty:
        def __init__(
            self,
            *,
            coordinates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.CoordinatesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            range_in_kilometers: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the GPS coordinates of the endpoint location.

            :param coordinates: The GPS coordinates to measure distance from.
            :param range_in_kilometers: The range, in kilometers, from the GPS coordinates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-gpspoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                g_pSPoint_property = pinpoint_mixins.CfnSegmentPropsMixin.GPSPointProperty(
                    coordinates=pinpoint_mixins.CfnSegmentPropsMixin.CoordinatesProperty(
                        latitude=123,
                        longitude=123
                    ),
                    range_in_kilometers=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__008e449d9b2bb3817ff56a42d780d1c98f6e5d165e995ef26dccdfec05947a05)
                check_type(argname="argument coordinates", value=coordinates, expected_type=type_hints["coordinates"])
                check_type(argname="argument range_in_kilometers", value=range_in_kilometers, expected_type=type_hints["range_in_kilometers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if coordinates is not None:
                self._values["coordinates"] = coordinates
            if range_in_kilometers is not None:
                self._values["range_in_kilometers"] = range_in_kilometers

        @builtins.property
        def coordinates(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.CoordinatesProperty"]]:
            '''The GPS coordinates to measure distance from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-gpspoint.html#cfn-pinpoint-segment-gpspoint-coordinates
            '''
            result = self._values.get("coordinates")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.CoordinatesProperty"]], result)

        @builtins.property
        def range_in_kilometers(self) -> typing.Optional[jsii.Number]:
            '''The range, in kilometers, from the GPS coordinates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-gpspoint.html#cfn-pinpoint-segment-gpspoint-rangeinkilometers
            '''
            result = self._values.get("range_in_kilometers")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GPSPointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.GroupsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "source_segments": "sourceSegments",
            "source_type": "sourceType",
            "type": "type",
        },
    )
    class GroupsProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SegmentDimensionsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_segments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SourceSegmentsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_type: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An array that defines the set of segment criteria to evaluate when handling segment groups for the segment.

            :param dimensions: An array that defines the dimensions to include or exclude from the segment.
            :param source_segments: The base segment to build the segment on. A base segment, also called a *source segment* , defines the initial population of endpoints for a segment. When you add dimensions to the segment, Amazon Pinpoint filters the base segment by using the dimensions that you specify. You can specify more than one dimensional segment or only one imported segment. If you specify an imported segment, the segment size estimate that displays on the Amazon Pinpoint console indicates the size of the imported segment without any filters applied to it.
            :param source_type: Specifies how to handle multiple base segments for the segment. For example, if you specify three base segments for the segment, whether the resulting segment is based on all, any, or none of the base segments.
            :param type: Specifies how to handle multiple dimensions for the segment. For example, if you specify three dimensions for the segment, whether the resulting segment includes endpoints that match all, any, or none of the dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-groups.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                # attributes: Any
                # metrics: Any
                # user_attributes: Any
                
                groups_property = pinpoint_mixins.CfnSegmentPropsMixin.GroupsProperty(
                    dimensions=[pinpoint_mixins.CfnSegmentPropsMixin.SegmentDimensionsProperty(
                        attributes=attributes,
                        behavior=pinpoint_mixins.CfnSegmentPropsMixin.BehaviorProperty(
                            recency=pinpoint_mixins.CfnSegmentPropsMixin.RecencyProperty(
                                duration="duration",
                                recency_type="recencyType"
                            )
                        ),
                        demographic=pinpoint_mixins.CfnSegmentPropsMixin.DemographicProperty(
                            app_version=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            channel=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            device_type=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            make=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            model=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            platform=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        ),
                        location=pinpoint_mixins.CfnSegmentPropsMixin.LocationProperty(
                            country=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            gps_point=pinpoint_mixins.CfnSegmentPropsMixin.GPSPointProperty(
                                coordinates=pinpoint_mixins.CfnSegmentPropsMixin.CoordinatesProperty(
                                    latitude=123,
                                    longitude=123
                                ),
                                range_in_kilometers=123
                            )
                        ),
                        metrics=metrics,
                        user_attributes=user_attributes
                    )],
                    source_segments=[pinpoint_mixins.CfnSegmentPropsMixin.SourceSegmentsProperty(
                        id="id",
                        version=123
                    )],
                    source_type="sourceType",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6191be77b25456a2d2ffec50538158849c4cd2fb09df39906411e76ad818ea87)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument source_segments", value=source_segments, expected_type=type_hints["source_segments"])
                check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if source_segments is not None:
                self._values["source_segments"] = source_segments
            if source_type is not None:
                self._values["source_type"] = source_type
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SegmentDimensionsProperty"]]]]:
            '''An array that defines the dimensions to include or exclude from the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-groups.html#cfn-pinpoint-segment-groups-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SegmentDimensionsProperty"]]]], result)

        @builtins.property
        def source_segments(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SourceSegmentsProperty"]]]]:
            '''The base segment to build the segment on.

            A base segment, also called a *source segment* , defines the initial population of endpoints for a segment. When you add dimensions to the segment, Amazon Pinpoint filters the base segment by using the dimensions that you specify.

            You can specify more than one dimensional segment or only one imported segment. If you specify an imported segment, the segment size estimate that displays on the Amazon Pinpoint console indicates the size of the imported segment without any filters applied to it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-groups.html#cfn-pinpoint-segment-groups-sourcesegments
            '''
            result = self._values.get("source_segments")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SourceSegmentsProperty"]]]], result)

        @builtins.property
        def source_type(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle multiple base segments for the segment.

            For example, if you specify three base segments for the segment, whether the resulting segment is based on all, any, or none of the base segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-groups.html#cfn-pinpoint-segment-groups-sourcetype
            '''
            result = self._values.get("source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle multiple dimensions for the segment.

            For example, if you specify three dimensions for the segment, whether the resulting segment includes endpoints that match all, any, or none of the dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-groups.html#cfn-pinpoint-segment-groups-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"country": "country", "gps_point": "gpsPoint"},
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            country: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            gps_point: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.GPSPointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies location-based criteria, such as region or GPS coordinates, for the segment.

            :param country: The country or region code, in ISO 3166-1 alpha-2 format, for the segment.
            :param gps_point: The GPS point dimension for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                location_property = pinpoint_mixins.CfnSegmentPropsMixin.LocationProperty(
                    country=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    gps_point=pinpoint_mixins.CfnSegmentPropsMixin.GPSPointProperty(
                        coordinates=pinpoint_mixins.CfnSegmentPropsMixin.CoordinatesProperty(
                            latitude=123,
                            longitude=123
                        ),
                        range_in_kilometers=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0627fcc86b5738a20ed3c516bcf082bdbed1d197267a96557668f7eaa8b9ebac)
                check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                check_type(argname="argument gps_point", value=gps_point, expected_type=type_hints["gps_point"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if country is not None:
                self._values["country"] = country
            if gps_point is not None:
                self._values["gps_point"] = gps_point

        @builtins.property
        def country(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]]:
            '''The country or region code, in ISO 3166-1 alpha-2 format, for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-location.html#cfn-pinpoint-segment-location-country
            '''
            result = self._values.get("country")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.SetDimensionProperty"]], result)

        @builtins.property
        def gps_point(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.GPSPointProperty"]]:
            '''The GPS point dimension for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-location.html#cfn-pinpoint-segment-location-gpspoint
            '''
            result = self._values.get("gps_point")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.GPSPointProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.RecencyProperty",
        jsii_struct_bases=[],
        name_mapping={"duration": "duration", "recency_type": "recencyType"},
    )
    class RecencyProperty:
        def __init__(
            self,
            *,
            duration: typing.Optional[builtins.str] = None,
            recency_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies how recently segment members were active.

            :param duration: The duration to use when determining which users have been active or inactive with your app. Possible values: ``HR_24`` | ``DAY_7`` | ``DAY_14`` | ``DAY_30`` .
            :param recency_type: The type of recency dimension to use for the segment. Valid values are: ``ACTIVE`` and ``INACTIVE`` . If the value is ``ACTIVE`` , the segment includes users who have used your app within the specified duration are included in the segment. If the value is ``INACTIVE`` , the segment includes users who haven't used your app within the specified duration are included in the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-recency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                recency_property = pinpoint_mixins.CfnSegmentPropsMixin.RecencyProperty(
                    duration="duration",
                    recency_type="recencyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6dd70d15a0a1e551f5927c473aa87f6969788d7050ad1b5321ba20133a072a7)
                check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                check_type(argname="argument recency_type", value=recency_type, expected_type=type_hints["recency_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration is not None:
                self._values["duration"] = duration
            if recency_type is not None:
                self._values["recency_type"] = recency_type

        @builtins.property
        def duration(self) -> typing.Optional[builtins.str]:
            '''The duration to use when determining which users have been active or inactive with your app.

            Possible values: ``HR_24`` | ``DAY_7`` | ``DAY_14`` | ``DAY_30`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-recency.html#cfn-pinpoint-segment-recency-duration
            '''
            result = self._values.get("duration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recency_type(self) -> typing.Optional[builtins.str]:
            '''The type of recency dimension to use for the segment.

            Valid values are: ``ACTIVE`` and ``INACTIVE`` . If the value is ``ACTIVE`` , the segment includes users who have used your app within the specified duration are included in the segment. If the value is ``INACTIVE`` , the segment includes users who haven't used your app within the specified duration are included in the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-recency.html#cfn-pinpoint-segment-recency-recencytype
            '''
            result = self._values.get("recency_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.SegmentDimensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "behavior": "behavior",
            "demographic": "demographic",
            "location": "location",
            "metrics": "metrics",
            "user_attributes": "userAttributes",
        },
    )
    class SegmentDimensionsProperty:
        def __init__(
            self,
            *,
            attributes: typing.Any = None,
            behavior: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.BehaviorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            demographic: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.DemographicProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metrics: typing.Any = None,
            user_attributes: typing.Any = None,
        ) -> None:
            '''Specifies the dimension settings for a segment.

            :param attributes: One or more custom attributes to use as criteria for the segment. For more information see `AttributeDimension <https://docs.aws.amazon.com/pinpoint/latest/apireference/apps-application-id-segments.html#apps-application-id-segments-model-attributedimension>`_
            :param behavior: The behavior-based criteria, such as how recently users have used your app, for the segment.
            :param demographic: The demographic-based criteria, such as device platform, for the segment.
            :param location: The location-based criteria, such as region or GPS coordinates, for the segment.
            :param metrics: One or more custom metrics to use as criteria for the segment.
            :param user_attributes: One or more custom user attributes to use as criteria for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                # attributes: Any
                # metrics: Any
                # user_attributes: Any
                
                segment_dimensions_property = pinpoint_mixins.CfnSegmentPropsMixin.SegmentDimensionsProperty(
                    attributes=attributes,
                    behavior=pinpoint_mixins.CfnSegmentPropsMixin.BehaviorProperty(
                        recency=pinpoint_mixins.CfnSegmentPropsMixin.RecencyProperty(
                            duration="duration",
                            recency_type="recencyType"
                        )
                    ),
                    demographic=pinpoint_mixins.CfnSegmentPropsMixin.DemographicProperty(
                        app_version=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        channel=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        device_type=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        make=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        model=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        platform=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    ),
                    location=pinpoint_mixins.CfnSegmentPropsMixin.LocationProperty(
                        country=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        gps_point=pinpoint_mixins.CfnSegmentPropsMixin.GPSPointProperty(
                            coordinates=pinpoint_mixins.CfnSegmentPropsMixin.CoordinatesProperty(
                                latitude=123,
                                longitude=123
                            ),
                            range_in_kilometers=123
                        )
                    ),
                    metrics=metrics,
                    user_attributes=user_attributes
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab7cfa5c28d69d3d57393e97cbae7140c3a6cb7060e363261fe8db1d07244138)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
                check_type(argname="argument demographic", value=demographic, expected_type=type_hints["demographic"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
                check_type(argname="argument user_attributes", value=user_attributes, expected_type=type_hints["user_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if behavior is not None:
                self._values["behavior"] = behavior
            if demographic is not None:
                self._values["demographic"] = demographic
            if location is not None:
                self._values["location"] = location
            if metrics is not None:
                self._values["metrics"] = metrics
            if user_attributes is not None:
                self._values["user_attributes"] = user_attributes

        @builtins.property
        def attributes(self) -> typing.Any:
            '''One or more custom attributes to use as criteria for the segment.

            For more information see `AttributeDimension <https://docs.aws.amazon.com/pinpoint/latest/apireference/apps-application-id-segments.html#apps-application-id-segments-model-attributedimension>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Any, result)

        @builtins.property
        def behavior(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.BehaviorProperty"]]:
            '''The behavior-based criteria, such as how recently users have used your app, for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-behavior
            '''
            result = self._values.get("behavior")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.BehaviorProperty"]], result)

        @builtins.property
        def demographic(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.DemographicProperty"]]:
            '''The demographic-based criteria, such as device platform, for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-demographic
            '''
            result = self._values.get("demographic")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.DemographicProperty"]], result)

        @builtins.property
        def location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.LocationProperty"]]:
            '''The location-based criteria, such as region or GPS coordinates, for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.LocationProperty"]], result)

        @builtins.property
        def metrics(self) -> typing.Any:
            '''One or more custom metrics to use as criteria for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Any, result)

        @builtins.property
        def user_attributes(self) -> typing.Any:
            '''One or more custom user attributes to use as criteria for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-userattributes
            '''
            result = self._values.get("user_attributes")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentDimensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.SegmentGroupsProperty",
        jsii_struct_bases=[],
        name_mapping={"groups": "groups", "include": "include"},
    )
    class SegmentGroupsProperty:
        def __init__(
            self,
            *,
            groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentPropsMixin.GroupsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            include: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the set of segment criteria to evaluate when handling segment groups for the segment.

            :param groups: Specifies the set of segment criteria to evaluate when handling segment groups for the segment.
            :param include: Specifies how to handle multiple segment groups for the segment. For example, if the segment includes three segment groups, whether the resulting segment includes endpoints that match all, any, or none of the segment groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                # attributes: Any
                # metrics: Any
                # user_attributes: Any
                
                segment_groups_property = pinpoint_mixins.CfnSegmentPropsMixin.SegmentGroupsProperty(
                    groups=[pinpoint_mixins.CfnSegmentPropsMixin.GroupsProperty(
                        dimensions=[pinpoint_mixins.CfnSegmentPropsMixin.SegmentDimensionsProperty(
                            attributes=attributes,
                            behavior=pinpoint_mixins.CfnSegmentPropsMixin.BehaviorProperty(
                                recency=pinpoint_mixins.CfnSegmentPropsMixin.RecencyProperty(
                                    duration="duration",
                                    recency_type="recencyType"
                                )
                            ),
                            demographic=pinpoint_mixins.CfnSegmentPropsMixin.DemographicProperty(
                                app_version=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                channel=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                device_type=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                make=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                model=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                platform=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            location=pinpoint_mixins.CfnSegmentPropsMixin.LocationProperty(
                                country=pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                gps_point=pinpoint_mixins.CfnSegmentPropsMixin.GPSPointProperty(
                                    coordinates=pinpoint_mixins.CfnSegmentPropsMixin.CoordinatesProperty(
                                        latitude=123,
                                        longitude=123
                                    ),
                                    range_in_kilometers=123
                                )
                            ),
                            metrics=metrics,
                            user_attributes=user_attributes
                        )],
                        source_segments=[pinpoint_mixins.CfnSegmentPropsMixin.SourceSegmentsProperty(
                            id="id",
                            version=123
                        )],
                        source_type="sourceType",
                        type="type"
                    )],
                    include="include"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b59212370c3d66d06399b5f44c168689c8a1d20ceec9cb9a3232f63d7dc64a4b)
                check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if groups is not None:
                self._values["groups"] = groups
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.GroupsProperty"]]]]:
            '''Specifies the set of segment criteria to evaluate when handling segment groups for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html#cfn-pinpoint-segment-segmentgroups-groups
            '''
            result = self._values.get("groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentPropsMixin.GroupsProperty"]]]], result)

        @builtins.property
        def include(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle multiple segment groups for the segment.

            For example, if the segment includes three segment groups, whether the resulting segment includes endpoints that match all, any, or none of the segment groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html#cfn-pinpoint-segment-segmentgroups-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentGroupsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.SetDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class SetDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the dimension type and values for a segment dimension.

            :param dimension_type: The type of segment dimension to use. Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.
            :param values: The criteria values to use for the segment dimension. Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                set_dimension_property = pinpoint_mixins.CfnSegmentPropsMixin.SetDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b98b8ef9b8039e275a6249142de6ddaadf62b7f2f9c0a8bea5fb46c70fcd0c9)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The type of segment dimension to use.

            Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html#cfn-pinpoint-segment-setdimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The criteria values to use for the segment dimension.

            Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html#cfn-pinpoint-segment-setdimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSegmentPropsMixin.SourceSegmentsProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "version": "version"},
    )
    class SourceSegmentsProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the base segment to build the segment on.

            A base segment, also called a *source segment* , defines the initial population of endpoints for a segment. When you add dimensions to the segment, Amazon Pinpoint filters the base segment by using the dimensions that you specify.

            You can specify more than one dimensional segment or only one imported segment. If you specify an imported segment, the segment size estimate that displays on the Amazon Pinpoint console indicates the size of the imported segment without any filters applied to it.

            :param id: The unique identifier for the source segment.
            :param version: The version number of the source segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-sourcesegments.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
                
                source_segments_property = pinpoint_mixins.CfnSegmentPropsMixin.SourceSegmentsProperty(
                    id="id",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__20074c68c7c80e9e611b40116c221bf64fbe1ac9e2c3e6c63c0dd90b4398880a)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the source segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-sourcesegments.html#cfn-pinpoint-segment-sourcesegments-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''The version number of the source segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-sourcesegments.html#cfn-pinpoint-segment-sourcesegments-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceSegmentsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSmsTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "body": "body",
        "default_substitutions": "defaultSubstitutions",
        "tags": "tags",
        "template_description": "templateDescription",
        "template_name": "templateName",
    },
)
class CfnSmsTemplateMixinProps:
    def __init__(
        self,
        *,
        body: typing.Optional[builtins.str] = None,
        default_substitutions: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
        template_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSmsTemplatePropsMixin.

        :param body: The message body to use in text messages that are based on the message template.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        :param template_name: The name of the message template to use for the message. If specified, this value must match the name of an existing message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            # tags: Any
            
            cfn_sms_template_mixin_props = pinpoint_mixins.CfnSmsTemplateMixinProps(
                body="body",
                default_substitutions="defaultSubstitutions",
                tags=tags,
                template_description="templateDescription",
                template_name="templateName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb210b74c56bd13e227f58a9dd17bf64facaee15dadeee9710014b20a1004f2)
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument default_substitutions", value=default_substitutions, expected_type=type_hints["default_substitutions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body is not None:
            self._values["body"] = body
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description
        if template_name is not None:
            self._values["template_name"] = template_name

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''The message body to use in text messages that are based on the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-body
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-defaultsubstitutions
        '''
        result = self._values.get("default_substitutions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the message template to use for the message.

        If specified, this value must match the name of an existing message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatename
        '''
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSmsTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSmsTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnSmsTemplatePropsMixin",
):
    '''Creates a message template that you can use in messages that are sent through the SMS channel.

    A *message template* is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html
    :cloudformationResource: AWS::Pinpoint::SmsTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        # tags: Any
        
        cfn_sms_template_props_mixin = pinpoint_mixins.CfnSmsTemplatePropsMixin(pinpoint_mixins.CfnSmsTemplateMixinProps(
            body="body",
            default_substitutions="defaultSubstitutions",
            tags=tags,
            template_description="templateDescription",
            template_name="templateName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSmsTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::SmsTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__565b94255612cb3469baa415a5d7fb54292c680aefa9a3ed459de8649c458e0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b77021d7737abf774868946d532f56145800049b9d7014c1052cc610f2d261a7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81be6820c16d881a98cfe75529b821c891e274eeee5d303721669fe81d0ed6d4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSmsTemplateMixinProps:
        return typing.cast(CfnSmsTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnVoiceChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={"application_id": "applicationId", "enabled": "enabled"},
)
class CfnVoiceChannelMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnVoiceChannelPropsMixin.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the voice channel applies to.
        :param enabled: Specifies whether to enable the voice channel for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
            
            cfn_voice_channel_mixin_props = pinpoint_mixins.CfnVoiceChannelMixinProps(
                application_id="applicationId",
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375c0753539bc256f9713402b9c89a64f6432937fdc0a2744b661075872e2839)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the Amazon Pinpoint application that the voice channel applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable the voice channel for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVoiceChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVoiceChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pinpoint.mixins.CfnVoiceChannelPropsMixin",
):
    '''A *channel* is a type of platform that you can deliver messages to.

    To send a voice message, you send the message through the voice channel. Before you can use Amazon Pinpoint to send voice messages, you have to enable the voice channel for an Amazon Pinpoint application.

    The VoiceChannel resource represents the status and other information about the voice channel for an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html
    :cloudformationResource: AWS::Pinpoint::VoiceChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pinpoint import mixins as pinpoint_mixins
        
        cfn_voice_channel_props_mixin = pinpoint_mixins.CfnVoiceChannelPropsMixin(pinpoint_mixins.CfnVoiceChannelMixinProps(
            application_id="applicationId",
            enabled=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVoiceChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pinpoint::VoiceChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33a0fb39f3fa96368620e790d1dbda1264229595e0920f4b77affd807c40f3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6f610f4566fbec97f11466d806aa738a03ea719130f5215112b632280ad7d3a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5657b7586d0bc549865086bc0dd8447acf7cf7445efee8075b9056a1b9c696d9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVoiceChannelMixinProps:
        return typing.cast(CfnVoiceChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnADMChannelMixinProps",
    "CfnADMChannelPropsMixin",
    "CfnAPNSChannelMixinProps",
    "CfnAPNSChannelPropsMixin",
    "CfnAPNSSandboxChannelMixinProps",
    "CfnAPNSSandboxChannelPropsMixin",
    "CfnAPNSVoipChannelMixinProps",
    "CfnAPNSVoipChannelPropsMixin",
    "CfnAPNSVoipSandboxChannelMixinProps",
    "CfnAPNSVoipSandboxChannelPropsMixin",
    "CfnAppMixinProps",
    "CfnAppPropsMixin",
    "CfnApplicationSettingsMixinProps",
    "CfnApplicationSettingsPropsMixin",
    "CfnBaiduChannelMixinProps",
    "CfnBaiduChannelPropsMixin",
    "CfnCampaignMixinProps",
    "CfnCampaignPropsMixin",
    "CfnEmailChannelMixinProps",
    "CfnEmailChannelPropsMixin",
    "CfnEmailTemplateMixinProps",
    "CfnEmailTemplatePropsMixin",
    "CfnEventStreamMixinProps",
    "CfnEventStreamPropsMixin",
    "CfnGCMChannelMixinProps",
    "CfnGCMChannelPropsMixin",
    "CfnInAppTemplateMixinProps",
    "CfnInAppTemplatePropsMixin",
    "CfnPushTemplateMixinProps",
    "CfnPushTemplatePropsMixin",
    "CfnSMSChannelMixinProps",
    "CfnSMSChannelPropsMixin",
    "CfnSegmentMixinProps",
    "CfnSegmentPropsMixin",
    "CfnSmsTemplateMixinProps",
    "CfnSmsTemplatePropsMixin",
    "CfnVoiceChannelMixinProps",
    "CfnVoiceChannelPropsMixin",
]

publication.publish()

def _typecheckingstub__1dd9aaddc35d0385416911df2379f7ada44ebee4c28281f27a5fa4535c8fe32a(
    *,
    application_id: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8473e5cf4df9904b17c4d495fa8e09fd3aecb24eb592dd7043390d25aceb9542(
    props: typing.Union[CfnADMChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ce4ef4965fdf25cc0bc888d500e8a938be46c6fcd8777b38322dae02ecd688(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9df8762cce9bbf8b252a299a5206e1c0f9cce1e823bebc49c66a488f4424f32(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc8d7f608458c01f5acac9da9852a83ee6aebb88121347dd44bda90e40250ca(
    *,
    application_id: typing.Optional[builtins.str] = None,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0381bd02b7c3e926ca9ada83ed905dcff7c6293a19c98c715717e28f99da844(
    props: typing.Union[CfnAPNSChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc6d56dd19d32bec1bc9a7e1bc7e7a643b7780477601eead712052fd3b0f2b5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3646761d54d51fe582cefacfeca585cf3a0413fa44520265ece033426623a1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b165a667eb6248aca8784274b7960b0794cd7023a017460473d825383f1c4b(
    *,
    application_id: typing.Optional[builtins.str] = None,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad32dbf8b1268208013e4e20244952c8f6b018f2b6e43e3fdd595947a5d560e9(
    props: typing.Union[CfnAPNSSandboxChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf3031aecefa9800ff9206dfffd8b7cc09fa63443de5d448d960945ea4dd93c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5164447deca46281aa430dcf5efe8b0a13c0f78adf2090c107535994f4d7f68e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16903d719b59deb65b078d33eac5ab412c6b72ba09274f3c2c3e45e84abc1f0e(
    *,
    application_id: typing.Optional[builtins.str] = None,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d76d69e4778dec3aeac9fb5a4265a25ba4678af7422c8ebd07fb25f3100d4ec(
    props: typing.Union[CfnAPNSVoipChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef33ec8dd7ce1b34df8e7ae1c6f7c4e11089264241e8204fb450d680e882073c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60336d77c42ef655c91ba776467681f596d46ba0e0f6aee05a38a34effbd348b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a6ac24da8053f25d433b758d19468fd03e7ab643da46af34db23f3b9fbb66b6(
    *,
    application_id: typing.Optional[builtins.str] = None,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683281e55c7b65544c176020ab52ba1166b64ec53a5930aa30d844e0d9f63cbb(
    props: typing.Union[CfnAPNSVoipSandboxChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897b7ea05d6013b050f4e84a2d195e4886473b26336c895c4364f554d9d1e461(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fa32e568b247badd1c8209709d12476c4289d6e7cfb3d14bd08326778ce4b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36725735f25e88f9303233468d9af0c98a239c29a0e27de053bd0fa7c91407f(
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12906bbe11a3cc27828a64ba49fd3afae517fcde1a3d553986befb538f7e48c2(
    props: typing.Union[CfnAppMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f583d4b8d624135ee33bddec2038d5ad538ed994de8164c31fd8ef4655da457(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f643db60a88118870236b25f454d752e54044dc3aa3c79ce48c7278a10f04f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9794cb7939c5fcd57b0cc93bbe379f36bde1d1e06501e34c4eb996682646da71(
    *,
    application_id: typing.Optional[builtins.str] = None,
    campaign_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationSettingsPropsMixin.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationSettingsPropsMixin.LimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    quiet_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationSettingsPropsMixin.QuietTimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c3ddd95f0b77fcc1d23ee0d204260ad0fe88a286c02fc5dd4d50d09367b323(
    props: typing.Union[CfnApplicationSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31377c1cb8d24b8fab7c7078b99b8e9a54e3c792dde9534766f88d038d2a416(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d678a54f7350a2ad438688f4ae3631714bdeb561e49481fbdd043331a9844e17(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20ae34bca941d286265d1848de5ffef21153f3f393b6e7f120e46d0828f1472(
    *,
    lambda_function_name: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    web_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44e38170b3251fbb2c8355e2701740349d3e882e6914b6a9c94c2ad7cf7b2f7(
    *,
    daily: typing.Optional[jsii.Number] = None,
    maximum_duration: typing.Optional[jsii.Number] = None,
    messages_per_second: typing.Optional[jsii.Number] = None,
    total: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a97d0224652b8f9c5c04138bb332ff59d9e327d8a5b3bda069f61fb5e124a0(
    *,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f53a69ea383f0ee41493e7a422b38a399e6d88f08d8dbcd34fb3f611850245(
    *,
    api_key: typing.Optional[builtins.str] = None,
    application_id: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    secret_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed15c23cefc2cb368352b8cd444397da4ccd15776922cd1a225bf8522934ba6(
    props: typing.Union[CfnBaiduChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328c5ad3bb2831effd6e3dcc6ae2dba2aca150f93ef20e0667af1f5ac18fd0eb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63f2211443c5f823f7871a1bc3cc68e1aecd3932c0d22bf638f277c8b8fecfb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753429197d419217949c08eeff09e2c672620a8b71618f0742d0c22490ff1b7c(
    *,
    additional_treatments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.WriteTreatmentResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    application_id: typing.Optional[builtins.str] = None,
    campaign_hook: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    holdout_percent: typing.Optional[jsii.Number] = None,
    is_paused: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.LimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    message_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.MessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    segment_id: typing.Optional[builtins.str] = None,
    segment_version: typing.Optional[jsii.Number] = None,
    tags: typing.Any = None,
    template_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    treatment_description: typing.Optional[builtins.str] = None,
    treatment_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3df051f1faf3b00d389160d92dcc1901cddee7ad83042fc1f4e23ce3799451(
    props: typing.Union[CfnCampaignMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08edc80efc9880484c7437d1cb2b403357de4cc61a7c354bb6d7057a1f8aa68(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c1d2c9e0f5cf732828389989f982de131a7e884f5ae93710fc74d894d53309(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451d3c1cad3d4f79dd4398ce2bfae0618f30d34ba8bc7ba0553a3ec33983d21c(
    *,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f181bd2ff162055f54ff2d351caf0c44f34de894e72af167ef7476191b72bc42(
    *,
    body: typing.Optional[builtins.str] = None,
    from_address: typing.Optional[builtins.str] = None,
    html_body: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4754eba285099c12270f93e2cbc54d33e404e484902ae26c34f3f6859de0128(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.EventDimensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4eaf61e1dc240fa7fa5eba2b6a4b337dcbee83170afee17f85ab807418791b9(
    *,
    lambda_function_name: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    web_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb06c5184968a17c51382375ee6a0850f4977b0847f728699b25f5a2e7cfdc1(
    *,
    content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.InAppMessageContentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_config: typing.Any = None,
    layout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a73699746dff574d227d0cb5236d91cc266c887c1a45d9d011c94d0e87c384a(
    *,
    body: typing.Optional[builtins.str] = None,
    entity_id: typing.Optional[builtins.str] = None,
    message_type: typing.Optional[builtins.str] = None,
    origination_number: typing.Optional[builtins.str] = None,
    sender_id: typing.Optional[builtins.str] = None,
    template_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d27f04de53b58df77dd1c810188fdfa7baf64f54ecf97ca8fec381297b78938(
    *,
    delivery_uri: typing.Optional[builtins.str] = None,
    endpoint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786d362f3693db41a80db78ef8057f82b0e0f758db853c3beff045e8e5ce1ca3(
    *,
    background_color: typing.Optional[builtins.str] = None,
    border_radius: typing.Optional[jsii.Number] = None,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9de554e028d77723abd20b1c4ed56a12363dfd5ffc1bde5db6b7f8a8670257(
    *,
    attributes: typing.Any = None,
    event_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bf42c083c2798dfe493d6231b7a67cdaae0953ce6827f14e3140b5a86cb306(
    *,
    alignment: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1084d78b83d9eec8859eaf9f987080bc355cca685978cfe90c9f8f624d92a65a(
    *,
    android: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.DefaultButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ios: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    web: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f89c4425ce0b15f158a4f5ed82bd14bb8f3f5589247683deba9e1dd1f1a63a(
    *,
    background_color: typing.Optional[builtins.str] = None,
    body_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.InAppMessageBodyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    header_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.InAppMessageHeaderConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_url: typing.Optional[builtins.str] = None,
    primary_btn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.InAppMessageButtonProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secondary_btn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.InAppMessageButtonProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95c9a234aaf80f423aea511787a609cfeafbf48f307de4877f9d4f0f83b1651(
    *,
    alignment: typing.Optional[builtins.str] = None,
    header: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84fa518555528b08422b0fef703c5e4f481af0933a0d34d45dacf174616b6e4(
    *,
    daily: typing.Optional[jsii.Number] = None,
    maximum_duration: typing.Optional[jsii.Number] = None,
    messages_per_second: typing.Optional[jsii.Number] = None,
    session: typing.Optional[jsii.Number] = None,
    total: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f1d516dbb2e652d8f6b56adea664fec5d0e54cf111be27727f61e796afc355(
    *,
    adm_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    apns_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    baidu_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CampaignCustomMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    email_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CampaignEmailMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gcm_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.MessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    in_app_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CampaignInAppMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sms_message: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CampaignSmsMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744f2f6614f20bc8e8f5b252e7195b133edc97af1786280813dfbfb35a7c3869(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    image_icon_url: typing.Optional[builtins.str] = None,
    image_small_icon_url: typing.Optional[builtins.str] = None,
    image_url: typing.Optional[builtins.str] = None,
    json_body: typing.Optional[builtins.str] = None,
    media_url: typing.Optional[builtins.str] = None,
    raw_content: typing.Optional[builtins.str] = None,
    silent_push: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    time_to_live: typing.Optional[jsii.Number] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c916cab6c5be94f92e7aad54cafe1f7d4d68bdb0f094f4f33da83607a99a08f(
    *,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e57d36ee7e92356d9eb5066d9f73f18f31af04088fd7088cc67f2559de9207(
    *,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6727be0b4098b61be735b0f0e0814f072cc9815213377308b6e33dc3fb27b6(
    *,
    end_time: typing.Optional[builtins.str] = None,
    event_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CampaignEventFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    frequency: typing.Optional[builtins.str] = None,
    is_local_time: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    quiet_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.QuietTimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_time: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18acfce852144900828a5bd56dcd8232eeeac4e750382f369369f2243afd483d(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e25f02fdb6430dfad99f546b8a94f9fe423b9bd53f41eeb8ca78584d8a0d5b(
    *,
    email_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    push_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sms_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    voice_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58697bafda66b00785decd7c3977a8cb8cbd51e3afec522ee5605a172e82c2c4(
    *,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb9593bc3c501df9484d40adc1b657be47b04fbcd7c26ac0f7eb78265d81147(
    *,
    custom_delivery_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CustomDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    message_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.MessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    size_percent: typing.Optional[jsii.Number] = None,
    template_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    treatment_description: typing.Optional[builtins.str] = None,
    treatment_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bf5efe1c44f4d4822fcb29a16505db7147755d8cc3aee683ecd60f3f852a8f(
    *,
    application_id: typing.Optional[builtins.str] = None,
    configuration_set: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    from_address: typing.Optional[builtins.str] = None,
    identity: typing.Optional[builtins.str] = None,
    orchestration_sending_role_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44a38596ffe5481c92374f39b4971beef85061d58bf30618b0879071c9863b2(
    props: typing.Union[CfnEmailChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92fb222d8f183220d8c5310db44543f0357d8d849527e91b5574190b6ca3f45(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0035014b0b5199fa23130934dc0d9e7f39297cd8841cf2c62f309a9263b736(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a9b1632c75f56a79c5acaa7e9dd1ba95d19ebd367d793d1d4a1d7274ff0026(
    *,
    default_substitutions: typing.Optional[builtins.str] = None,
    html_part: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
    text_part: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16ef553798d8e177814f78a06d4ec641e4f2be2ec2a1bd60ed01e87c1b6658f(
    props: typing.Union[CfnEmailTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824c69a4bbee0b26288c2d4ba0abe55ff8d3553d2d71489694b1123a8d512a36(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05f2b7e8b832032ed0ccd8966d0ba8c8edf173830a63842f016f0bb9369cc05(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65eb52a33ff235d68fd046f0e9e557577da2bc9052492592abeac9aad4800dd4(
    *,
    application_id: typing.Optional[builtins.str] = None,
    destination_stream_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4df4e03dfc9c943f3c9faabd6792441390a7bcf9631bd1099448a4c4502b3d(
    props: typing.Union[CfnEventStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c28d66a9cceebc5a01c871572f1ceeb588202399c6fd98653cba270e7f759f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ed5e8dfc64f2d5a15095dea61705695028650eaf4c0bf75b86a70800e03b91(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7305a7546dca84aaeaf15f3cf4b301450cf88730bf181c024dcb58b7f18c609(
    *,
    api_key: typing.Optional[builtins.str] = None,
    application_id: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    service_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e60ec568e317e069d5690858611273e400278e4212ae7b4ca86852ff94430c2(
    props: typing.Union[CfnGCMChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2927a3935ef29fbcdadc0cec0eac51c404ea4cd656021dc45656a7463127605(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f930066e03b289ed967495821722491945ac9c95db5c662510a9aa90fe50df(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a34e3c907857fa18cc77baf3f122e12ac776a84dc6e5395c6506479eb2e3e63(
    *,
    content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInAppTemplatePropsMixin.InAppMessageContentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_config: typing.Any = None,
    layout: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c472843c6e49f8d8fdfadda4852087b75d5e87811dd41211aa87be5fc60e7d9(
    props: typing.Union[CfnInAppTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4f53f14277bcfdb7de73261fcdda068b2d228fa9820e26c314f1d655af4306(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563360f5dab2e59e859c7178d041ca2dbda61661c2cea5f68ccf048a6b12857d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a777e4cb215c4dcf140c11b4eb928dfeda970d6a89206209cd2c1f96af1a1b53(
    *,
    alignment: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee17eb5854db07fc6c6699b057d12536630f81681d658a5d16b69aea94ca6d5(
    *,
    android: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInAppTemplatePropsMixin.DefaultButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ios: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    web: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInAppTemplatePropsMixin.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f161f518d24bbbbed257f6afa45c1b4b029d26d159c26247f3345b61c265bdf1(
    *,
    background_color: typing.Optional[builtins.str] = None,
    border_radius: typing.Optional[jsii.Number] = None,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1940e0aa991d2797b8dc4cc7115e9aa4f5b19f6ab81d8c1b8b6a9d945ce77c(
    *,
    alignment: typing.Optional[builtins.str] = None,
    header: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6e1fc6160581b6b83297ef105009fc1651d9b6c53502b12089dfe237b1e062(
    *,
    background_color: typing.Optional[builtins.str] = None,
    body_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInAppTemplatePropsMixin.BodyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    header_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInAppTemplatePropsMixin.HeaderConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_url: typing.Optional[builtins.str] = None,
    primary_btn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInAppTemplatePropsMixin.ButtonConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secondary_btn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInAppTemplatePropsMixin.ButtonConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fccb4ffb54d9885de6de5d0730b539df768a88042e06822ae9a763f57e01e1(
    *,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc360cdbf06f07cb37910d5d6df4f2984a280abf9ee4cc47f76bcd0aba5b5db3(
    *,
    adm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    apns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPushTemplatePropsMixin.APNSPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    baidu: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPushTemplatePropsMixin.DefaultPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_substitutions: typing.Optional[builtins.str] = None,
    gcm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPushTemplatePropsMixin.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3919970457bf4a81e91ded4fe1d52d0f92a0787f9857243e58bc9349d5fec8(
    props: typing.Union[CfnPushTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cea071d1a0c5b227d96ce44e0f5088fca2743996a98ac7868a435f95ff843de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af1782419b173ca8339e9912f5a3f6bb953b50075dd6d154b8b0973ecede4da(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37687b0fded5962a8403469dc7acc3bb74275bfd84b89e65ff522f59ce30f0fb(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    media_url: typing.Optional[builtins.str] = None,
    sound: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e52bd22a04b00a9e008e659a5d0314116329626228f82df9f784f9c15089b5(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    image_icon_url: typing.Optional[builtins.str] = None,
    image_url: typing.Optional[builtins.str] = None,
    small_image_icon_url: typing.Optional[builtins.str] = None,
    sound: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad920b6450be39fb3f60e0fd89c90a0a228b3a27f4164e36b167b35b66f1c0f7(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    sound: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4cceb113c845c823629fac850a547ac7b305c81b831d6470f270e9c8148b348(
    *,
    application_id: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    sender_id: typing.Optional[builtins.str] = None,
    short_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b02daf6ca3003a33f0a0a6f1c36f2e7068f68cbfbd96de629462c0ea20e434d(
    props: typing.Union[CfnSMSChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f4fbbcee6bf031c0fdd5e93012e9931b3ac125c673f6fe656c084082414bcd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53ed908c2222289b87245ec87189cac2820869adb460301a6f15fb81592cf1a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf5bccc93e00660e1ec67c69272e8fe86b3e31c43d5092e9a57ead21b66bf04(
    *,
    application_id: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SegmentDimensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    segment_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SegmentGroupsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d859b090913775364783816130ae920a75be6e262515aa87583a39ade38fcbe(
    props: typing.Union[CfnSegmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fabfbad555b37487ef47d2657a38c565d1e2c1b305b63b571d4e65b6924692(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b4c83fc2eb2392ebe2e05776cbc93aede4924759f8afd108bafc3d76004e50(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed354882c80eaef5421f892e58153c993c7121162442369bb25b2e4d9f7ed26c(
    *,
    recency: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.RecencyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6917be5d090634f383b2c9616d783f5d6cbca0e79482cc0686056d6d3026d9fa(
    *,
    latitude: typing.Optional[jsii.Number] = None,
    longitude: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b0bba6fcf634c61b672b5ce5057056d8775279948aafc5fcd65fe6039835e4(
    *,
    app_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    channel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    device_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    make: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    model: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    platform: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008e449d9b2bb3817ff56a42d780d1c98f6e5d165e995ef26dccdfec05947a05(
    *,
    coordinates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.CoordinatesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    range_in_kilometers: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6191be77b25456a2d2ffec50538158849c4cd2fb09df39906411e76ad818ea87(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SegmentDimensionsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_segments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SourceSegmentsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0627fcc86b5738a20ed3c516bcf082bdbed1d197267a96557668f7eaa8b9ebac(
    *,
    country: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gps_point: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.GPSPointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6dd70d15a0a1e551f5927c473aa87f6969788d7050ad1b5321ba20133a072a7(
    *,
    duration: typing.Optional[builtins.str] = None,
    recency_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7cfa5c28d69d3d57393e97cbae7140c3a6cb7060e363261fe8db1d07244138(
    *,
    attributes: typing.Any = None,
    behavior: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.BehaviorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    demographic: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.DemographicProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Any = None,
    user_attributes: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59212370c3d66d06399b5f44c168689c8a1d20ceec9cb9a3232f63d7dc64a4b(
    *,
    groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentPropsMixin.GroupsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b98b8ef9b8039e275a6249142de6ddaadf62b7f2f9c0a8bea5fb46c70fcd0c9(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20074c68c7c80e9e611b40116c221bf64fbe1ac9e2c3e6c63c0dd90b4398880a(
    *,
    id: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb210b74c56bd13e227f58a9dd17bf64facaee15dadeee9710014b20a1004f2(
    *,
    body: typing.Optional[builtins.str] = None,
    default_substitutions: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565b94255612cb3469baa415a5d7fb54292c680aefa9a3ed459de8649c458e0c(
    props: typing.Union[CfnSmsTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77021d7737abf774868946d532f56145800049b9d7014c1052cc610f2d261a7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81be6820c16d881a98cfe75529b821c891e274eeee5d303721669fe81d0ed6d4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375c0753539bc256f9713402b9c89a64f6432937fdc0a2744b661075872e2839(
    *,
    application_id: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33a0fb39f3fa96368620e790d1dbda1264229595e0920f4b77affd807c40f3b(
    props: typing.Union[CfnVoiceChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f610f4566fbec97f11466d806aa738a03ea719130f5215112b632280ad7d3a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5657b7586d0bc549865086bc0dd8447acf7cf7445efee8075b9056a1b9c696d9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
