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
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_classic_flow": "allowClassicFlow",
        "allow_unauthenticated_identities": "allowUnauthenticatedIdentities",
        "cognito_events": "cognitoEvents",
        "cognito_identity_providers": "cognitoIdentityProviders",
        "cognito_streams": "cognitoStreams",
        "developer_provider_name": "developerProviderName",
        "identity_pool_name": "identityPoolName",
        "identity_pool_tags": "identityPoolTags",
        "open_id_connect_provider_arns": "openIdConnectProviderArns",
        "push_sync": "pushSync",
        "saml_provider_arns": "samlProviderArns",
        "supported_login_providers": "supportedLoginProviders",
    },
)
class CfnIdentityPoolMixinProps:
    def __init__(
        self,
        *,
        allow_classic_flow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        allow_unauthenticated_identities: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        cognito_events: typing.Any = None,
        cognito_identity_providers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentityPoolPropsMixin.CognitoIdentityProviderProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        cognito_streams: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentityPoolPropsMixin.CognitoStreamsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        developer_provider_name: typing.Optional[builtins.str] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        identity_pool_tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        open_id_connect_provider_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        push_sync: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentityPoolPropsMixin.PushSyncProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        saml_provider_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        supported_login_providers: typing.Any = None,
    ) -> None:
        '''Properties for CfnIdentityPoolPropsMixin.

        :param allow_classic_flow: Enables the Basic (Classic) authentication flow.
        :param allow_unauthenticated_identities: Specifies whether the identity pool supports unauthenticated logins.
        :param cognito_events: The events to configure.
        :param cognito_identity_providers: The Amazon Cognito user pools and their client IDs.
        :param cognito_streams: Configuration options for configuring Amazon Cognito streams.
        :param developer_provider_name: The "domain" Amazon Cognito uses when referencing your users. This name acts as a placeholder that allows your backend and the Amazon Cognito service to communicate about the developer provider. For the ``DeveloperProviderName`` , you can use letters and periods (.), underscores (_), and dashes (-). *Minimum length* : 1 *Maximum length* : 100
        :param identity_pool_name: The name of your Amazon Cognito identity pool. *Minimum length* : 1 *Maximum length* : 128 *Pattern* : ``[\\w\\s+=,.@-]+``
        :param identity_pool_tags: Tags to assign to the identity pool. A tag is a label that you can apply to identity pools to categorize and manage them in different ways, such as by purpose, owner, environment, or other criteria.
        :param open_id_connect_provider_arns: The Amazon Resource Names (ARNs) of the OpenID connect providers.
        :param push_sync: The configuration options to be applied to the identity pool.
        :param saml_provider_arns: The Amazon Resource Names (ARNs) of the Security Assertion Markup Language (SAML) providers.
        :param supported_login_providers: Key-value pairs that map provider names to provider app IDs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            # cognito_events: Any
            # supported_login_providers: Any
            
            cfn_identity_pool_mixin_props = cognito_mixins.CfnIdentityPoolMixinProps(
                allow_classic_flow=False,
                allow_unauthenticated_identities=False,
                cognito_events=cognito_events,
                cognito_identity_providers=[cognito_mixins.CfnIdentityPoolPropsMixin.CognitoIdentityProviderProperty(
                    client_id="clientId",
                    provider_name="providerName",
                    server_side_token_check=False
                )],
                cognito_streams=cognito_mixins.CfnIdentityPoolPropsMixin.CognitoStreamsProperty(
                    role_arn="roleArn",
                    streaming_status="streamingStatus",
                    stream_name="streamName"
                ),
                developer_provider_name="developerProviderName",
                identity_pool_name="identityPoolName",
                identity_pool_tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                open_id_connect_provider_arns=["openIdConnectProviderArns"],
                push_sync=cognito_mixins.CfnIdentityPoolPropsMixin.PushSyncProperty(
                    application_arns=["applicationArns"],
                    role_arn="roleArn"
                ),
                saml_provider_arns=["samlProviderArns"],
                supported_login_providers=supported_login_providers
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67372ba211f7acfcaed8f890308ad723cafd4a8ed2cd64ae44c2a72152668c7b)
            check_type(argname="argument allow_classic_flow", value=allow_classic_flow, expected_type=type_hints["allow_classic_flow"])
            check_type(argname="argument allow_unauthenticated_identities", value=allow_unauthenticated_identities, expected_type=type_hints["allow_unauthenticated_identities"])
            check_type(argname="argument cognito_events", value=cognito_events, expected_type=type_hints["cognito_events"])
            check_type(argname="argument cognito_identity_providers", value=cognito_identity_providers, expected_type=type_hints["cognito_identity_providers"])
            check_type(argname="argument cognito_streams", value=cognito_streams, expected_type=type_hints["cognito_streams"])
            check_type(argname="argument developer_provider_name", value=developer_provider_name, expected_type=type_hints["developer_provider_name"])
            check_type(argname="argument identity_pool_name", value=identity_pool_name, expected_type=type_hints["identity_pool_name"])
            check_type(argname="argument identity_pool_tags", value=identity_pool_tags, expected_type=type_hints["identity_pool_tags"])
            check_type(argname="argument open_id_connect_provider_arns", value=open_id_connect_provider_arns, expected_type=type_hints["open_id_connect_provider_arns"])
            check_type(argname="argument push_sync", value=push_sync, expected_type=type_hints["push_sync"])
            check_type(argname="argument saml_provider_arns", value=saml_provider_arns, expected_type=type_hints["saml_provider_arns"])
            check_type(argname="argument supported_login_providers", value=supported_login_providers, expected_type=type_hints["supported_login_providers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_classic_flow is not None:
            self._values["allow_classic_flow"] = allow_classic_flow
        if allow_unauthenticated_identities is not None:
            self._values["allow_unauthenticated_identities"] = allow_unauthenticated_identities
        if cognito_events is not None:
            self._values["cognito_events"] = cognito_events
        if cognito_identity_providers is not None:
            self._values["cognito_identity_providers"] = cognito_identity_providers
        if cognito_streams is not None:
            self._values["cognito_streams"] = cognito_streams
        if developer_provider_name is not None:
            self._values["developer_provider_name"] = developer_provider_name
        if identity_pool_name is not None:
            self._values["identity_pool_name"] = identity_pool_name
        if identity_pool_tags is not None:
            self._values["identity_pool_tags"] = identity_pool_tags
        if open_id_connect_provider_arns is not None:
            self._values["open_id_connect_provider_arns"] = open_id_connect_provider_arns
        if push_sync is not None:
            self._values["push_sync"] = push_sync
        if saml_provider_arns is not None:
            self._values["saml_provider_arns"] = saml_provider_arns
        if supported_login_providers is not None:
            self._values["supported_login_providers"] = supported_login_providers

    @builtins.property
    def allow_classic_flow(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables the Basic (Classic) authentication flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-allowclassicflow
        '''
        result = self._values.get("allow_classic_flow")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def allow_unauthenticated_identities(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the identity pool supports unauthenticated logins.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-allowunauthenticatedidentities
        '''
        result = self._values.get("allow_unauthenticated_identities")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cognito_events(self) -> typing.Any:
        '''The events to configure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitoevents
        '''
        result = self._values.get("cognito_events")
        return typing.cast(typing.Any, result)

    @builtins.property
    def cognito_identity_providers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolPropsMixin.CognitoIdentityProviderProperty"]]]]:
        '''The Amazon Cognito user pools and their client IDs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitoidentityproviders
        '''
        result = self._values.get("cognito_identity_providers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolPropsMixin.CognitoIdentityProviderProperty"]]]], result)

    @builtins.property
    def cognito_streams(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolPropsMixin.CognitoStreamsProperty"]]:
        '''Configuration options for configuring Amazon Cognito streams.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitostreams
        '''
        result = self._values.get("cognito_streams")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolPropsMixin.CognitoStreamsProperty"]], result)

    @builtins.property
    def developer_provider_name(self) -> typing.Optional[builtins.str]:
        '''The "domain" Amazon Cognito uses when referencing your users.

        This name acts as a placeholder that allows your backend and the Amazon Cognito service to communicate about the developer provider. For the ``DeveloperProviderName`` , you can use letters and periods (.), underscores (_), and dashes (-).

        *Minimum length* : 1

        *Maximum length* : 100

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-developerprovidername
        '''
        result = self._values.get("developer_provider_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_pool_name(self) -> typing.Optional[builtins.str]:
        '''The name of your Amazon Cognito identity pool.

        *Minimum length* : 1

        *Maximum length* : 128

        *Pattern* : ``[\\w\\s+=,.@-]+``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-identitypoolname
        '''
        result = self._values.get("identity_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_pool_tags(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the identity pool.

        A tag is a label that you can apply to identity pools to categorize and manage them in different ways, such as by purpose, owner, environment, or other criteria.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-identitypooltags
        '''
        result = self._values.get("identity_pool_tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def open_id_connect_provider_arns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the OpenID connect providers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-openidconnectproviderarns
        '''
        result = self._values.get("open_id_connect_provider_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def push_sync(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolPropsMixin.PushSyncProperty"]]:
        '''The configuration options to be applied to the identity pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-pushsync
        '''
        result = self._values.get("push_sync")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolPropsMixin.PushSyncProperty"]], result)

    @builtins.property
    def saml_provider_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the Security Assertion Markup Language (SAML) providers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-samlproviderarns
        '''
        result = self._values.get("saml_provider_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def supported_login_providers(self) -> typing.Any:
        '''Key-value pairs that map provider names to provider app IDs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-supportedloginproviders
        '''
        result = self._values.get("supported_login_providers")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdentityPoolMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolPrincipalTagMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "identity_pool_id": "identityPoolId",
        "identity_provider_name": "identityProviderName",
        "principal_tags": "principalTags",
        "use_defaults": "useDefaults",
    },
)
class CfnIdentityPoolPrincipalTagMixinProps:
    def __init__(
        self,
        *,
        identity_pool_id: typing.Optional[builtins.str] = None,
        identity_provider_name: typing.Optional[builtins.str] = None,
        principal_tags: typing.Any = None,
        use_defaults: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnIdentityPoolPrincipalTagPropsMixin.

        :param identity_pool_id: The identity pool that you want to associate with this principal tag map.
        :param identity_provider_name: The identity pool identity provider (IdP) that you want to associate with this principal tag map.
        :param principal_tags: A JSON-formatted list of user claims and the principal tags that you want to associate with them. When Amazon Cognito requests credentials, it sets the value of the principal tag to the value of the user's claim.
        :param use_defaults: Use a default set of mappings between claims and tags for this provider, instead of a custom map.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolprincipaltag.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            # principal_tags: Any
            
            cfn_identity_pool_principal_tag_mixin_props = cognito_mixins.CfnIdentityPoolPrincipalTagMixinProps(
                identity_pool_id="identityPoolId",
                identity_provider_name="identityProviderName",
                principal_tags=principal_tags,
                use_defaults=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f91c12eafe779b4f3590afb48f6e5199e76efbcfd2937fe2b0319f96e4c1f22)
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument identity_provider_name", value=identity_provider_name, expected_type=type_hints["identity_provider_name"])
            check_type(argname="argument principal_tags", value=principal_tags, expected_type=type_hints["principal_tags"])
            check_type(argname="argument use_defaults", value=use_defaults, expected_type=type_hints["use_defaults"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_pool_id is not None:
            self._values["identity_pool_id"] = identity_pool_id
        if identity_provider_name is not None:
            self._values["identity_provider_name"] = identity_provider_name
        if principal_tags is not None:
            self._values["principal_tags"] = principal_tags
        if use_defaults is not None:
            self._values["use_defaults"] = use_defaults

    @builtins.property
    def identity_pool_id(self) -> typing.Optional[builtins.str]:
        '''The identity pool that you want to associate with this principal tag map.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolprincipaltag.html#cfn-cognito-identitypoolprincipaltag-identitypoolid
        '''
        result = self._values.get("identity_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_name(self) -> typing.Optional[builtins.str]:
        '''The identity pool identity provider (IdP) that you want to associate with this principal tag map.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolprincipaltag.html#cfn-cognito-identitypoolprincipaltag-identityprovidername
        '''
        result = self._values.get("identity_provider_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal_tags(self) -> typing.Any:
        '''A JSON-formatted list of user claims and the principal tags that you want to associate with them.

        When Amazon Cognito requests credentials, it sets the value of the principal tag to the value of the user's claim.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolprincipaltag.html#cfn-cognito-identitypoolprincipaltag-principaltags
        '''
        result = self._values.get("principal_tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_defaults(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Use a default set of mappings between claims and tags for this provider, instead of a custom map.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolprincipaltag.html#cfn-cognito-identitypoolprincipaltag-usedefaults
        '''
        result = self._values.get("use_defaults")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdentityPoolPrincipalTagMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdentityPoolPrincipalTagPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolPrincipalTagPropsMixin",
):
    '''A list of the identity pool principal tag assignments for attributes for access control.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolprincipaltag.html
    :cloudformationResource: AWS::Cognito::IdentityPoolPrincipalTag
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        # principal_tags: Any
        
        cfn_identity_pool_principal_tag_props_mixin = cognito_mixins.CfnIdentityPoolPrincipalTagPropsMixin(cognito_mixins.CfnIdentityPoolPrincipalTagMixinProps(
            identity_pool_id="identityPoolId",
            identity_provider_name="identityProviderName",
            principal_tags=principal_tags,
            use_defaults=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIdentityPoolPrincipalTagMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::IdentityPoolPrincipalTag``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d99b534551a6fc1282c0297e63fca99035093683f976192337285a5802014064)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46ac8a87771a22f5c7026fe406745e498f54b8ddb63186551f22d18a2dfbbaa0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f52cfd8be909f9f29db4e8dc8d16d48b355a1c93e3a4d8cec7a41268b4a3682)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdentityPoolPrincipalTagMixinProps:
        return typing.cast(CfnIdentityPoolPrincipalTagMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnIdentityPoolPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolPropsMixin",
):
    '''The ``AWS::Cognito::IdentityPool`` resource creates an Amazon Cognito identity pool.

    To avoid deleting the resource accidentally from CloudFormation , use `DeletionPolicy Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ and the `UpdateReplacePolicy Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ to retain the resource on deletion or replacement.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html
    :cloudformationResource: AWS::Cognito::IdentityPool
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        # cognito_events: Any
        # supported_login_providers: Any
        
        cfn_identity_pool_props_mixin = cognito_mixins.CfnIdentityPoolPropsMixin(cognito_mixins.CfnIdentityPoolMixinProps(
            allow_classic_flow=False,
            allow_unauthenticated_identities=False,
            cognito_events=cognito_events,
            cognito_identity_providers=[cognito_mixins.CfnIdentityPoolPropsMixin.CognitoIdentityProviderProperty(
                client_id="clientId",
                provider_name="providerName",
                server_side_token_check=False
            )],
            cognito_streams=cognito_mixins.CfnIdentityPoolPropsMixin.CognitoStreamsProperty(
                role_arn="roleArn",
                streaming_status="streamingStatus",
                stream_name="streamName"
            ),
            developer_provider_name="developerProviderName",
            identity_pool_name="identityPoolName",
            identity_pool_tags=[CfnTag(
                key="key",
                value="value"
            )],
            open_id_connect_provider_arns=["openIdConnectProviderArns"],
            push_sync=cognito_mixins.CfnIdentityPoolPropsMixin.PushSyncProperty(
                application_arns=["applicationArns"],
                role_arn="roleArn"
            ),
            saml_provider_arns=["samlProviderArns"],
            supported_login_providers=supported_login_providers
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIdentityPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::IdentityPool``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8dbe76c211016a6eb10b06afb75505b0d79bdc02ef51bcb9649bd8bcfab4ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1afda541c56ec87c1ee0ebf90dc305652fa5dcb99325f1522f645e58f1e81d3a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7faf4c99172c88c9a9f08ad0748491a731fa27c9e2280e1321316d563efef619)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdentityPoolMixinProps:
        return typing.cast(CfnIdentityPoolMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolPropsMixin.CognitoIdentityProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "provider_name": "providerName",
            "server_side_token_check": "serverSideTokenCheck",
        },
    )
    class CognitoIdentityProviderProperty:
        def __init__(
            self,
            *,
            client_id: typing.Optional[builtins.str] = None,
            provider_name: typing.Optional[builtins.str] = None,
            server_side_token_check: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''``CognitoIdentityProvider`` is a property of the `AWS::Cognito::IdentityPool <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html>`_ resource that represents an Amazon Cognito user pool and its client ID.

            :param client_id: The client ID for the Amazon Cognito user pool.
            :param provider_name: The provider name for an Amazon Cognito user pool. For example: ``cognito-idp.us-east-2.amazonaws.com/us-east-2_123456789`` .
            :param server_side_token_check: TRUE if server-side token validation is enabled for the identity provider’s token. After you set the ``ServerSideTokenCheck`` to TRUE for an identity pool, that identity pool checks with the integrated user pools to make sure the user has not been globally signed out or deleted before the identity pool provides an OIDC token or AWS credentials for the user. If the user is signed out or deleted, the identity pool returns a 400 Not Authorized error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                cognito_identity_provider_property = cognito_mixins.CfnIdentityPoolPropsMixin.CognitoIdentityProviderProperty(
                    client_id="clientId",
                    provider_name="providerName",
                    server_side_token_check=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__319186e502894de6c361b0b7f1c59618cf5929c4f46e821e8dc1d98d0b9ac254)
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
                check_type(argname="argument server_side_token_check", value=server_side_token_check, expected_type=type_hints["server_side_token_check"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_id is not None:
                self._values["client_id"] = client_id
            if provider_name is not None:
                self._values["provider_name"] = provider_name
            if server_side_token_check is not None:
                self._values["server_side_token_check"] = server_side_token_check

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The client ID for the Amazon Cognito user pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html#cfn-cognito-identitypool-cognitoidentityprovider-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def provider_name(self) -> typing.Optional[builtins.str]:
            '''The provider name for an Amazon Cognito user pool.

            For example: ``cognito-idp.us-east-2.amazonaws.com/us-east-2_123456789`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html#cfn-cognito-identitypool-cognitoidentityprovider-providername
            '''
            result = self._values.get("provider_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_side_token_check(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''TRUE if server-side token validation is enabled for the identity provider’s token.

            After you set the ``ServerSideTokenCheck`` to TRUE for an identity pool, that identity pool checks with the integrated user pools to make sure the user has not been globally signed out or deleted before the identity pool provides an OIDC token or AWS credentials for the user.

            If the user is signed out or deleted, the identity pool returns a 400 Not Authorized error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html#cfn-cognito-identitypool-cognitoidentityprovider-serversidetokencheck
            '''
            result = self._values.get("server_side_token_check")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoIdentityProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolPropsMixin.CognitoStreamsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "role_arn": "roleArn",
            "streaming_status": "streamingStatus",
            "stream_name": "streamName",
        },
    )
    class CognitoStreamsProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            streaming_status: typing.Optional[builtins.str] = None,
            stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``CognitoStreams`` is a property of the `AWS::Cognito::IdentityPool <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html>`_ resource that defines configuration options for Amazon Cognito streams.

            :param role_arn: The Amazon Resource Name (ARN) of the role Amazon Cognito can assume to publish to the stream. This role must grant access to Amazon Cognito (cognito-sync) to invoke ``PutRecord`` on your Amazon Cognito stream.
            :param streaming_status: Status of the Amazon Cognito streams. Valid values are: ``ENABLED`` or ``DISABLED`` .
            :param stream_name: The name of the Amazon Cognito stream to receive updates. This stream must be in the developer's account and in the same Region as the identity pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                cognito_streams_property = cognito_mixins.CfnIdentityPoolPropsMixin.CognitoStreamsProperty(
                    role_arn="roleArn",
                    streaming_status="streamingStatus",
                    stream_name="streamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d60592fbd79d0d4ed98e60335d9de499d192554f28fceb89949f59f2353cc80)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument streaming_status", value=streaming_status, expected_type=type_hints["streaming_status"])
                check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if streaming_status is not None:
                self._values["streaming_status"] = streaming_status
            if stream_name is not None:
                self._values["stream_name"] = stream_name

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the role Amazon Cognito can assume to publish to the stream.

            This role must grant access to Amazon Cognito (cognito-sync) to invoke ``PutRecord`` on your Amazon Cognito stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html#cfn-cognito-identitypool-cognitostreams-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def streaming_status(self) -> typing.Optional[builtins.str]:
            '''Status of the Amazon Cognito streams.

            Valid values are: ``ENABLED`` or ``DISABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html#cfn-cognito-identitypool-cognitostreams-streamingstatus
            '''
            result = self._values.get("streaming_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon Cognito stream to receive updates.

            This stream must be in the developer's account and in the same Region as the identity pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html#cfn-cognito-identitypool-cognitostreams-streamname
            '''
            result = self._values.get("stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoStreamsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolPropsMixin.PushSyncProperty",
        jsii_struct_bases=[],
        name_mapping={"application_arns": "applicationArns", "role_arn": "roleArn"},
    )
    class PushSyncProperty:
        def __init__(
            self,
            *,
            application_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``PushSync`` is a property of the `AWS::Cognito::IdentityPool <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html>`_ resource that defines the configuration options to be applied to an Amazon Cognito identity pool.

            :param application_arns: The ARNs of the Amazon SNS platform applications that could be used by clients.
            :param role_arn: An IAM role configured to allow Amazon Cognito to call Amazon SNS on behalf of the developer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-pushsync.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                push_sync_property = cognito_mixins.CfnIdentityPoolPropsMixin.PushSyncProperty(
                    application_arns=["applicationArns"],
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5e85e722f1cfff970f70b8bb8fefdbff91c23a333290a905009ab1c733d5845)
                check_type(argname="argument application_arns", value=application_arns, expected_type=type_hints["application_arns"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_arns is not None:
                self._values["application_arns"] = application_arns
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def application_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ARNs of the Amazon SNS platform applications that could be used by clients.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-pushsync.html#cfn-cognito-identitypool-pushsync-applicationarns
            '''
            result = self._values.get("application_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''An IAM role configured to allow Amazon Cognito to call Amazon SNS on behalf of the developer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-pushsync.html#cfn-cognito-identitypool-pushsync-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PushSyncProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolRoleAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "identity_pool_id": "identityPoolId",
        "role_mappings": "roleMappings",
        "roles": "roles",
    },
)
class CfnIdentityPoolRoleAttachmentMixinProps:
    def __init__(
        self,
        *,
        identity_pool_id: typing.Optional[builtins.str] = None,
        role_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentityPoolRoleAttachmentPropsMixin.RoleMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        roles: typing.Any = None,
    ) -> None:
        '''Properties for CfnIdentityPoolRoleAttachmentPropsMixin.

        :param identity_pool_id: An identity pool ID in the format ``REGION:GUID`` .
        :param role_mappings: How users for a specific identity provider are mapped to roles. This is a string to the ``RoleMapping`` object map. The string identifies the identity provider. For example: ``graph.facebook.com`` or ``cognito-idp.us-east-1.amazonaws.com/us-east-1_abcdefghi:app_client_id`` . If the ``IdentityProvider`` field isn't provided in this object, the string is used as the identity provider name. For more information, see the `RoleMapping property <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html>`_ .
        :param roles: The map of the roles associated with this pool. For a given role, the key is either "authenticated" or "unauthenticated". The value is the role ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            # roles: Any
            
            cfn_identity_pool_role_attachment_mixin_props = cognito_mixins.CfnIdentityPoolRoleAttachmentMixinProps(
                identity_pool_id="identityPoolId",
                role_mappings={
                    "role_mappings_key": cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.RoleMappingProperty(
                        ambiguous_role_resolution="ambiguousRoleResolution",
                        identity_provider="identityProvider",
                        rules_configuration=cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.RulesConfigurationTypeProperty(
                            rules=[cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.MappingRuleProperty(
                                claim="claim",
                                match_type="matchType",
                                role_arn="roleArn",
                                value="value"
                            )]
                        ),
                        type="type"
                    )
                },
                roles=roles
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168d215443ea4cdf0133a5b8de2ce5e76c33f46aa74b29efdb4f84ffc43b0f72)
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument role_mappings", value=role_mappings, expected_type=type_hints["role_mappings"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_pool_id is not None:
            self._values["identity_pool_id"] = identity_pool_id
        if role_mappings is not None:
            self._values["role_mappings"] = role_mappings
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def identity_pool_id(self) -> typing.Optional[builtins.str]:
        '''An identity pool ID in the format ``REGION:GUID`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-identitypoolid
        '''
        result = self._values.get("identity_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolRoleAttachmentPropsMixin.RoleMappingProperty"]]]]:
        '''How users for a specific identity provider are mapped to roles.

        This is a string to the ``RoleMapping`` object map. The string identifies the identity provider. For example: ``graph.facebook.com`` or ``cognito-idp.us-east-1.amazonaws.com/us-east-1_abcdefghi:app_client_id`` .

        If the ``IdentityProvider`` field isn't provided in this object, the string is used as the identity provider name.

        For more information, see the `RoleMapping property <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-rolemappings
        '''
        result = self._values.get("role_mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolRoleAttachmentPropsMixin.RoleMappingProperty"]]]], result)

    @builtins.property
    def roles(self) -> typing.Any:
        '''The map of the roles associated with this pool.

        For a given role, the key is either "authenticated" or "unauthenticated". The value is the role ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-roles
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdentityPoolRoleAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdentityPoolRoleAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolRoleAttachmentPropsMixin",
):
    '''The ``AWS::Cognito::IdentityPoolRoleAttachment`` resource manages the role configuration for an Amazon Cognito identity pool.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html
    :cloudformationResource: AWS::Cognito::IdentityPoolRoleAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        # roles: Any
        
        cfn_identity_pool_role_attachment_props_mixin = cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin(cognito_mixins.CfnIdentityPoolRoleAttachmentMixinProps(
            identity_pool_id="identityPoolId",
            role_mappings={
                "role_mappings_key": cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.RoleMappingProperty(
                    ambiguous_role_resolution="ambiguousRoleResolution",
                    identity_provider="identityProvider",
                    rules_configuration=cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.RulesConfigurationTypeProperty(
                        rules=[cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.MappingRuleProperty(
                            claim="claim",
                            match_type="matchType",
                            role_arn="roleArn",
                            value="value"
                        )]
                    ),
                    type="type"
                )
            },
            roles=roles
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIdentityPoolRoleAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::IdentityPoolRoleAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5773f928aed19ced0139cdcc1a3b4cf187cc01ac7a7a479fbc0a1a9ee77f4fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7784d0756a3bc97eb67c584b6a5ca7e9faaf00efa3d36b2ded5d0b0c52379d9b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16cca5ea0bb1f12d747decef5b42428f1c413d16202b2b98d41b4ccd8e7bdf88)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdentityPoolRoleAttachmentMixinProps:
        return typing.cast(CfnIdentityPoolRoleAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolRoleAttachmentPropsMixin.MappingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "claim": "claim",
            "match_type": "matchType",
            "role_arn": "roleArn",
            "value": "value",
        },
    )
    class MappingRuleProperty:
        def __init__(
            self,
            *,
            claim: typing.Optional[builtins.str] = None,
            match_type: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines how to map a claim to a role ARN.

            :param claim: The claim name that must be present in the token. For example: "isAdmin" or "paid".
            :param match_type: The match condition that specifies how closely the claim value in the IdP token must match ``Value`` . Valid values are: ``Equals`` , ``Contains`` , ``StartsWith`` , and ``NotEqual`` .
            :param role_arn: The Amazon Resource Name (ARN) of the role.
            :param value: A brief string that the claim must match. For example, "paid" or "yes".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                mapping_rule_property = cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.MappingRuleProperty(
                    claim="claim",
                    match_type="matchType",
                    role_arn="roleArn",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02291e3d9811ee3ae170ba10ed51d6872090f4f4d6cfbdd1e5b5553fd71e3bfc)
                check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
                check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if claim is not None:
                self._values["claim"] = claim
            if match_type is not None:
                self._values["match_type"] = match_type
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def claim(self) -> typing.Optional[builtins.str]:
            '''The claim name that must be present in the token.

            For example: "isAdmin" or "paid".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-claim
            '''
            result = self._values.get("claim")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def match_type(self) -> typing.Optional[builtins.str]:
            '''The match condition that specifies how closely the claim value in the IdP token must match ``Value`` .

            Valid values are: ``Equals`` , ``Contains`` , ``StartsWith`` , and ``NotEqual`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-matchtype
            '''
            result = self._values.get("match_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A brief string that the claim must match.

            For example, "paid" or "yes".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MappingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolRoleAttachmentPropsMixin.RoleMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ambiguous_role_resolution": "ambiguousRoleResolution",
            "identity_provider": "identityProvider",
            "rules_configuration": "rulesConfiguration",
            "type": "type",
        },
    )
    class RoleMappingProperty:
        def __init__(
            self,
            *,
            ambiguous_role_resolution: typing.Optional[builtins.str] = None,
            identity_provider: typing.Optional[builtins.str] = None,
            rules_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentityPoolRoleAttachmentPropsMixin.RulesConfigurationTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''One of a set of ``RoleMappings`` , a property of the `AWS::Cognito::IdentityPoolRoleAttachment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html>`_ resource that defines the role-mapping attributes of an Amazon Cognito identity pool.

            :param ambiguous_role_resolution: If you specify Token or Rules as the ``Type`` , ``AmbiguousRoleResolution`` is required. Specifies the action to be taken if either no rules match the claim value for the ``Rules`` type, or there is no ``cognito:preferred_role`` claim and there are multiple ``cognito:roles`` matches for the ``Token`` type.
            :param identity_provider: Identifier for the identity provider for which the role is mapped. For example: ``graph.facebook.com`` or ``cognito-idp.us-east-1.amazonaws.com/us-east-1_abcdefghi:app_client_id (http://cognito-idp.us-east-1.amazonaws.com/us-east-1_abcdefghi:app_client_id)`` . This is the identity provider that is used by the user for authentication. If the identity provider property isn't provided, the key of the entry in the ``RoleMappings`` map is used as the identity provider.
            :param rules_configuration: The rules to be used for mapping users to roles. If you specify "Rules" as the role-mapping type, RulesConfiguration is required.
            :param type: The role mapping type. Token will use ``cognito:roles`` and ``cognito:preferred_role`` claims from the Cognito identity provider token to map groups to roles. Rules will attempt to match claims from the token to map to a role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                role_mapping_property = cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.RoleMappingProperty(
                    ambiguous_role_resolution="ambiguousRoleResolution",
                    identity_provider="identityProvider",
                    rules_configuration=cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.RulesConfigurationTypeProperty(
                        rules=[cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.MappingRuleProperty(
                            claim="claim",
                            match_type="matchType",
                            role_arn="roleArn",
                            value="value"
                        )]
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75ee55531c8fd535053b9a99a3002aba33c53a37e5e8cc29a59278aba611b246)
                check_type(argname="argument ambiguous_role_resolution", value=ambiguous_role_resolution, expected_type=type_hints["ambiguous_role_resolution"])
                check_type(argname="argument identity_provider", value=identity_provider, expected_type=type_hints["identity_provider"])
                check_type(argname="argument rules_configuration", value=rules_configuration, expected_type=type_hints["rules_configuration"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ambiguous_role_resolution is not None:
                self._values["ambiguous_role_resolution"] = ambiguous_role_resolution
            if identity_provider is not None:
                self._values["identity_provider"] = identity_provider
            if rules_configuration is not None:
                self._values["rules_configuration"] = rules_configuration
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def ambiguous_role_resolution(self) -> typing.Optional[builtins.str]:
            '''If you specify Token or Rules as the ``Type`` , ``AmbiguousRoleResolution`` is required.

            Specifies the action to be taken if either no rules match the claim value for the ``Rules`` type, or there is no ``cognito:preferred_role`` claim and there are multiple ``cognito:roles`` matches for the ``Token`` type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-ambiguousroleresolution
            '''
            result = self._values.get("ambiguous_role_resolution")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identity_provider(self) -> typing.Optional[builtins.str]:
            '''Identifier for the identity provider for which the role is mapped.

            For example: ``graph.facebook.com`` or ``cognito-idp.us-east-1.amazonaws.com/us-east-1_abcdefghi:app_client_id (http://cognito-idp.us-east-1.amazonaws.com/us-east-1_abcdefghi:app_client_id)`` . This is the identity provider that is used by the user for authentication.

            If the identity provider property isn't provided, the key of the entry in the ``RoleMappings`` map is used as the identity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-identityprovider
            '''
            result = self._values.get("identity_provider")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rules_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolRoleAttachmentPropsMixin.RulesConfigurationTypeProperty"]]:
            '''The rules to be used for mapping users to roles.

            If you specify "Rules" as the role-mapping type, RulesConfiguration is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-rulesconfiguration
            '''
            result = self._values.get("rules_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolRoleAttachmentPropsMixin.RulesConfigurationTypeProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The role mapping type.

            Token will use ``cognito:roles`` and ``cognito:preferred_role`` claims from the Cognito identity provider token to map groups to roles. Rules will attempt to match claims from the token to map to a role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoleMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnIdentityPoolRoleAttachmentPropsMixin.RulesConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class RulesConfigurationTypeProperty:
        def __init__(
            self,
            *,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentityPoolRoleAttachmentPropsMixin.MappingRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''``RulesConfigurationType`` is a subproperty of the `RoleMapping <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html>`_ property that defines the rules to be used for mapping users to roles.

            :param rules: The rules. You can specify up to 25 rules per identity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rulesconfigurationtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                rules_configuration_type_property = cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.RulesConfigurationTypeProperty(
                    rules=[cognito_mixins.CfnIdentityPoolRoleAttachmentPropsMixin.MappingRuleProperty(
                        claim="claim",
                        match_type="matchType",
                        role_arn="roleArn",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33e77f7a0af99852e72568ca368b9516a74f44dbec61c00b6945520e65eb8c6c)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolRoleAttachmentPropsMixin.MappingRuleProperty"]]]]:
            '''The rules.

            You can specify up to 25 rules per identity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rulesconfigurationtype.html#cfn-cognito-identitypoolroleattachment-rulesconfigurationtype-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityPoolRoleAttachmentPropsMixin.MappingRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RulesConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnLogDeliveryConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_configurations": "logConfigurations",
        "user_pool_id": "userPoolId",
    },
)
class CfnLogDeliveryConfigurationMixinProps:
    def __init__(
        self,
        *,
        log_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLogDeliveryConfigurationPropsMixin.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLogDeliveryConfigurationPropsMixin.

        :param log_configurations: A logging destination of a user pool. User pools can have multiple logging destinations for message-delivery and user-activity logs.
        :param user_pool_id: The ID of the user pool where you configured logging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-logdeliveryconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            cfn_log_delivery_configuration_mixin_props = cognito_mixins.CfnLogDeliveryConfigurationMixinProps(
                log_configurations=[cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.LogConfigurationProperty(
                    cloud_watch_logs_configuration=cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.CloudWatchLogsConfigurationProperty(
                        log_group_arn="logGroupArn"
                    ),
                    event_source="eventSource",
                    firehose_configuration=cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.FirehoseConfigurationProperty(
                        stream_arn="streamArn"
                    ),
                    log_level="logLevel",
                    s3_configuration=cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.S3ConfigurationProperty(
                        bucket_arn="bucketArn"
                    )
                )],
                user_pool_id="userPoolId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7dc0fd1985ad951a09c32b0ba2125be6c457dbdd7776fdcb1c9338bfb2134c)
            check_type(argname="argument log_configurations", value=log_configurations, expected_type=type_hints["log_configurations"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_configurations is not None:
            self._values["log_configurations"] = log_configurations
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id

    @builtins.property
    def log_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLogDeliveryConfigurationPropsMixin.LogConfigurationProperty"]]]]:
        '''A logging destination of a user pool.

        User pools can have multiple logging destinations for message-delivery and user-activity logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-logdeliveryconfiguration.html#cfn-cognito-logdeliveryconfiguration-logconfigurations
        '''
        result = self._values.get("log_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLogDeliveryConfigurationPropsMixin.LogConfigurationProperty"]]]], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user pool where you configured logging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-logdeliveryconfiguration.html#cfn-cognito-logdeliveryconfiguration-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogDeliveryConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLogDeliveryConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnLogDeliveryConfigurationPropsMixin",
):
    '''Sets up or modifies the logging configuration of a user pool.

    User pools can export user notification logs and, when threat protection is active, user-activity logs. For more information, see `Exporting user pool logs <https://docs.aws.amazon.com/cognito/latest/developerguide/exporting-quotas-and-usage.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-logdeliveryconfiguration.html
    :cloudformationResource: AWS::Cognito::LogDeliveryConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_log_delivery_configuration_props_mixin = cognito_mixins.CfnLogDeliveryConfigurationPropsMixin(cognito_mixins.CfnLogDeliveryConfigurationMixinProps(
            log_configurations=[cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.LogConfigurationProperty(
                cloud_watch_logs_configuration=cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.CloudWatchLogsConfigurationProperty(
                    log_group_arn="logGroupArn"
                ),
                event_source="eventSource",
                firehose_configuration=cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.FirehoseConfigurationProperty(
                    stream_arn="streamArn"
                ),
                log_level="logLevel",
                s3_configuration=cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.S3ConfigurationProperty(
                    bucket_arn="bucketArn"
                )
            )],
            user_pool_id="userPoolId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLogDeliveryConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::LogDeliveryConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed6f05b2201a8e9047fd68640758506144467fe4b6428bb525a903cafb2c960)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5892764c73e4e82f5843e3c919356c946b9acdc6ec48ad04bb22e97472727481)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b17db6b74f8c6b7d62f91ed4bedc6dac67d4a87e0c46fd0d56c3b74ebb513ff)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLogDeliveryConfigurationMixinProps:
        return typing.cast(CfnLogDeliveryConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnLogDeliveryConfigurationPropsMixin.CloudWatchLogsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogsConfigurationProperty:
        def __init__(
            self,
            *,
            log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for the CloudWatch log group destination of user pool detailed activity logging, or of user activity log export with advanced security features.

            :param log_group_arn: The Amazon Resource Name (arn) of a CloudWatch Logs log group where your user pool sends logs. The log group must not be encrypted with AWS Key Management Service and must be in the same AWS account as your user pool. To send logs to log groups with a resource policy of a size greater than 5120 characters, configure a log group with a path that starts with ``/aws/vendedlogs`` . For more information, see `Enabling logging from certain AWS services <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AWS-logs-and-resource-policy.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-cloudwatchlogsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                cloud_watch_logs_configuration_property = cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.CloudWatchLogsConfigurationProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e262cd546721d0e261a4ddba3f87a5888b52f27f048a44df94827dac8333aa51)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (arn) of a CloudWatch Logs log group where your user pool sends logs.

            The log group must not be encrypted with AWS Key Management Service and must be in the same AWS account as your user pool.

            To send logs to log groups with a resource policy of a size greater than 5120 characters, configure a log group with a path that starts with ``/aws/vendedlogs`` . For more information, see `Enabling logging from certain AWS services <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AWS-logs-and-resource-policy.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-cloudwatchlogsconfiguration.html#cfn-cognito-logdeliveryconfiguration-cloudwatchlogsconfiguration-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnLogDeliveryConfigurationPropsMixin.FirehoseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_arn": "streamArn"},
    )
    class FirehoseConfigurationProperty:
        def __init__(self, *, stream_arn: typing.Optional[builtins.str] = None) -> None:
            '''Configuration for the Amazon Data Firehose stream destination of user activity log export with threat protection.

            :param stream_arn: The ARN of an Amazon Data Firehose stream that's the destination for threat protection log export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-firehoseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                firehose_configuration_property = cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.FirehoseConfigurationProperty(
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec235e874eafe7f5a05155fac7646add3fe391efb69ba9c172b04cd249b9ed38)
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stream_arn is not None:
                self._values["stream_arn"] = stream_arn

        @builtins.property
        def stream_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an Amazon Data Firehose stream that's the destination for threat protection log export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-firehoseconfiguration.html#cfn-cognito-logdeliveryconfiguration-firehoseconfiguration-streamarn
            '''
            result = self._values.get("stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnLogDeliveryConfigurationPropsMixin.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_configuration": "cloudWatchLogsConfiguration",
            "event_source": "eventSource",
            "firehose_configuration": "firehoseConfiguration",
            "log_level": "logLevel",
            "s3_configuration": "s3Configuration",
        },
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLogDeliveryConfigurationPropsMixin.CloudWatchLogsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            event_source: typing.Optional[builtins.str] = None,
            firehose_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLogDeliveryConfigurationPropsMixin.FirehoseConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            log_level: typing.Optional[builtins.str] = None,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLogDeliveryConfigurationPropsMixin.S3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration of user event logs to an external AWS service like Amazon Data Firehose, Amazon S3, or Amazon CloudWatch Logs.

            :param cloud_watch_logs_configuration: Configuration for the CloudWatch log group destination of user pool detailed activity logging, or of user activity log export with advanced security features.
            :param event_source: The source of events that your user pool sends for logging. To send error-level logs about user notification activity, set to ``userNotification`` . To send info-level logs about threat-protection user activity in user pools with the Plus feature plan, set to ``userAuthEvents`` .
            :param firehose_configuration: Configuration for the Amazon Data Firehose stream destination of user activity log export with threat protection.
            :param log_level: The ``errorlevel`` selection of logs that a user pool sends for detailed activity logging. To send ``userNotification`` activity with `information about message delivery <https://docs.aws.amazon.com/cognito/latest/developerguide/exporting-quotas-and-usage.html>`_ , choose ``ERROR`` with ``CloudWatchLogsConfiguration`` . To send ``userAuthEvents`` activity with user logs from threat protection with the Plus feature plan, choose ``INFO`` with one of ``CloudWatchLogsConfiguration`` , ``FirehoseConfiguration`` , or ``S3Configuration`` .
            :param s3_configuration: Configuration for the Amazon S3 bucket destination of user activity log export with threat protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                log_configuration_property = cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.LogConfigurationProperty(
                    cloud_watch_logs_configuration=cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.CloudWatchLogsConfigurationProperty(
                        log_group_arn="logGroupArn"
                    ),
                    event_source="eventSource",
                    firehose_configuration=cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.FirehoseConfigurationProperty(
                        stream_arn="streamArn"
                    ),
                    log_level="logLevel",
                    s3_configuration=cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.S3ConfigurationProperty(
                        bucket_arn="bucketArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9c88f4e4809609dd8c8eb72fceda2839eb4bd051dae401860bdc87b8eb974a9)
                check_type(argname="argument cloud_watch_logs_configuration", value=cloud_watch_logs_configuration, expected_type=type_hints["cloud_watch_logs_configuration"])
                check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                check_type(argname="argument firehose_configuration", value=firehose_configuration, expected_type=type_hints["firehose_configuration"])
                check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_configuration is not None:
                self._values["cloud_watch_logs_configuration"] = cloud_watch_logs_configuration
            if event_source is not None:
                self._values["event_source"] = event_source
            if firehose_configuration is not None:
                self._values["firehose_configuration"] = firehose_configuration
            if log_level is not None:
                self._values["log_level"] = log_level
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration

        @builtins.property
        def cloud_watch_logs_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLogDeliveryConfigurationPropsMixin.CloudWatchLogsConfigurationProperty"]]:
            '''Configuration for the CloudWatch log group destination of user pool detailed activity logging, or of user activity log export with advanced security features.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-logconfiguration.html#cfn-cognito-logdeliveryconfiguration-logconfiguration-cloudwatchlogsconfiguration
            '''
            result = self._values.get("cloud_watch_logs_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLogDeliveryConfigurationPropsMixin.CloudWatchLogsConfigurationProperty"]], result)

        @builtins.property
        def event_source(self) -> typing.Optional[builtins.str]:
            '''The source of events that your user pool sends for logging.

            To send error-level logs about user notification activity, set to ``userNotification`` . To send info-level logs about threat-protection user activity in user pools with the Plus feature plan, set to ``userAuthEvents`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-logconfiguration.html#cfn-cognito-logdeliveryconfiguration-logconfiguration-eventsource
            '''
            result = self._values.get("event_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def firehose_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLogDeliveryConfigurationPropsMixin.FirehoseConfigurationProperty"]]:
            '''Configuration for the Amazon Data Firehose stream destination of user activity log export with threat protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-logconfiguration.html#cfn-cognito-logdeliveryconfiguration-logconfiguration-firehoseconfiguration
            '''
            result = self._values.get("firehose_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLogDeliveryConfigurationPropsMixin.FirehoseConfigurationProperty"]], result)

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            '''The ``errorlevel`` selection of logs that a user pool sends for detailed activity logging.

            To send ``userNotification`` activity with `information about message delivery <https://docs.aws.amazon.com/cognito/latest/developerguide/exporting-quotas-and-usage.html>`_ , choose ``ERROR`` with ``CloudWatchLogsConfiguration`` . To send ``userAuthEvents`` activity with user logs from threat protection with the Plus feature plan, choose ``INFO`` with one of ``CloudWatchLogsConfiguration`` , ``FirehoseConfiguration`` , or ``S3Configuration`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-logconfiguration.html#cfn-cognito-logdeliveryconfiguration-logconfiguration-loglevel
            '''
            result = self._values.get("log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLogDeliveryConfigurationPropsMixin.S3ConfigurationProperty"]]:
            '''Configuration for the Amazon S3 bucket destination of user activity log export with threat protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-logconfiguration.html#cfn-cognito-logdeliveryconfiguration-logconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLogDeliveryConfigurationPropsMixin.S3ConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnLogDeliveryConfigurationPropsMixin.S3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_arn": "bucketArn"},
    )
    class S3ConfigurationProperty:
        def __init__(self, *, bucket_arn: typing.Optional[builtins.str] = None) -> None:
            '''Configuration for the Amazon S3 bucket destination of user activity log export with threat protection.

            :param bucket_arn: The ARN of an Amazon S3 bucket that's the destination for threat protection log export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-s3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                s3_configuration_property = cognito_mixins.CfnLogDeliveryConfigurationPropsMixin.S3ConfigurationProperty(
                    bucket_arn="bucketArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c46d27b5076b2ed38018d69680a95bedadfce5cbd004bb04ee6c3c8315c0b08b)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an Amazon S3 bucket that's the destination for threat protection log export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-logdeliveryconfiguration-s3configuration.html#cfn-cognito-logdeliveryconfiguration-s3configuration-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnManagedLoginBrandingMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "assets": "assets",
        "client_id": "clientId",
        "return_merged_resources": "returnMergedResources",
        "settings": "settings",
        "use_cognito_provided_values": "useCognitoProvidedValues",
        "user_pool_id": "userPoolId",
    },
)
class CfnManagedLoginBrandingMixinProps:
    def __init__(
        self,
        *,
        assets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnManagedLoginBrandingPropsMixin.AssetTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        client_id: typing.Optional[builtins.str] = None,
        return_merged_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        settings: typing.Any = None,
        use_cognito_provided_values: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnManagedLoginBrandingPropsMixin.

        :param assets: An array of image files that you want to apply to roles like backgrounds, logos, and icons. Each object must also indicate whether it is for dark mode, light mode, or browser-adaptive mode.
        :param client_id: The app client that you want to assign the branding style to. Each style is linked to an app client until you delete it.
        :param return_merged_resources: When ``true`` , returns values for branding options that are unchanged from Amazon Cognito defaults. When ``false`` or when you omit this parameter, returns only values that you customized in your branding style.
        :param settings: A JSON file, encoded as a ``Document`` type, with the the settings that you want to apply to your style. The following components are not currently implemented and reserved for future use: - ``signUp`` - ``instructions`` - ``sessionTimerDisplay`` - ``languageSelector`` (for localization, see `Managed login localization) <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html#managed-login-localization>`_
        :param use_cognito_provided_values: When true, applies the default branding style options. This option reverts to default style options that are managed by Amazon Cognito. You can modify them later in the branding editor. When you specify ``true`` for this option, you must also omit values for ``Settings`` and ``Assets`` in the request.
        :param user_pool_id: The user pool where the branding style is assigned.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-managedloginbranding.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            # settings: Any
            
            cfn_managed_login_branding_mixin_props = cognito_mixins.CfnManagedLoginBrandingMixinProps(
                assets=[cognito_mixins.CfnManagedLoginBrandingPropsMixin.AssetTypeProperty(
                    bytes="bytes",
                    category="category",
                    color_mode="colorMode",
                    extension="extension",
                    resource_id="resourceId"
                )],
                client_id="clientId",
                return_merged_resources=False,
                settings=settings,
                use_cognito_provided_values=False,
                user_pool_id="userPoolId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e330787a0be824f4f51ab86296111b41dfe8ebda32bd0c74f5c629a371f839)
            check_type(argname="argument assets", value=assets, expected_type=type_hints["assets"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument return_merged_resources", value=return_merged_resources, expected_type=type_hints["return_merged_resources"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument use_cognito_provided_values", value=use_cognito_provided_values, expected_type=type_hints["use_cognito_provided_values"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assets is not None:
            self._values["assets"] = assets
        if client_id is not None:
            self._values["client_id"] = client_id
        if return_merged_resources is not None:
            self._values["return_merged_resources"] = return_merged_resources
        if settings is not None:
            self._values["settings"] = settings
        if use_cognito_provided_values is not None:
            self._values["use_cognito_provided_values"] = use_cognito_provided_values
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id

    @builtins.property
    def assets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnManagedLoginBrandingPropsMixin.AssetTypeProperty"]]]]:
        '''An array of image files that you want to apply to roles like backgrounds, logos, and icons.

        Each object must also indicate whether it is for dark mode, light mode, or browser-adaptive mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-managedloginbranding.html#cfn-cognito-managedloginbranding-assets
        '''
        result = self._values.get("assets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnManagedLoginBrandingPropsMixin.AssetTypeProperty"]]]], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The app client that you want to assign the branding style to.

        Each style is linked to an app client until you delete it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-managedloginbranding.html#cfn-cognito-managedloginbranding-clientid
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def return_merged_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When ``true`` , returns values for branding options that are unchanged from Amazon Cognito defaults.

        When ``false`` or when you omit this parameter, returns only values that you customized in your branding style.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-managedloginbranding.html#cfn-cognito-managedloginbranding-returnmergedresources
        '''
        result = self._values.get("return_merged_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def settings(self) -> typing.Any:
        '''A JSON file, encoded as a ``Document`` type, with the the settings that you want to apply to your style.

        The following components are not currently implemented and reserved for future use:

        - ``signUp``
        - ``instructions``
        - ``sessionTimerDisplay``
        - ``languageSelector`` (for localization, see `Managed login localization) <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html#managed-login-localization>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-managedloginbranding.html#cfn-cognito-managedloginbranding-settings
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_cognito_provided_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When true, applies the default branding style options.

        This option reverts to default style options that are managed by Amazon Cognito. You can modify them later in the branding editor.

        When you specify ``true`` for this option, you must also omit values for ``Settings`` and ``Assets`` in the request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-managedloginbranding.html#cfn-cognito-managedloginbranding-usecognitoprovidedvalues
        '''
        result = self._values.get("use_cognito_provided_values")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The user pool where the branding style is assigned.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-managedloginbranding.html#cfn-cognito-managedloginbranding-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnManagedLoginBrandingMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnManagedLoginBrandingPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnManagedLoginBrandingPropsMixin",
):
    '''Creates a new set of branding settings for a user pool style and associates it with an app client.

    This operation is the programmatic option for the creation of a new style in the branding designer.

    Provides values for UI customization in a ``Settings`` JSON object and image files in an ``Assets`` array. To send the JSON object ``Document`` type parameter in ``Settings`` , you might need to update to the most recent version of your AWS SDK.

    This operation has a 2-megabyte request-size limit and include the CSS settings and image assets for your app client. Your branding settings might exceed 2MB in size. Amazon Cognito doesn't require that you pass all parameters in one request and preserves existing style settings that you don't specify. If your request is larger than 2MB, separate it into multiple requests, each with a size smaller than the limit.

    As a best practice, modify the output of `DescribeManagedLoginBrandingByClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeManagedLoginBrandingByClient.html>`_ into the request parameters for this operation. To get all settings, set ``ReturnMergedResources`` to ``true`` . For more information, see `API and SDK operations for managed login branding <https://docs.aws.amazon.com/cognito/latest/developerguide/managed-login-brandingdesigner.html#branding-designer-api>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-managedloginbranding.html
    :cloudformationResource: AWS::Cognito::ManagedLoginBranding
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        # settings: Any
        
        cfn_managed_login_branding_props_mixin = cognito_mixins.CfnManagedLoginBrandingPropsMixin(cognito_mixins.CfnManagedLoginBrandingMixinProps(
            assets=[cognito_mixins.CfnManagedLoginBrandingPropsMixin.AssetTypeProperty(
                bytes="bytes",
                category="category",
                color_mode="colorMode",
                extension="extension",
                resource_id="resourceId"
            )],
            client_id="clientId",
            return_merged_resources=False,
            settings=settings,
            use_cognito_provided_values=False,
            user_pool_id="userPoolId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnManagedLoginBrandingMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::ManagedLoginBranding``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecfe74d36dab9813eef90dc6cdaa29eb4852bdcbf1914d65617cb153fe2b836)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3906a9848a69e5e5e4a49360589157dea0ffb558e1af09c579f6020edf52814)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc97a067735caf25eeab8dbff072cf54d9edf492d8c38f5dd147435b9de4aed)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnManagedLoginBrandingMixinProps:
        return typing.cast(CfnManagedLoginBrandingMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnManagedLoginBrandingPropsMixin.AssetTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bytes": "bytes",
            "category": "category",
            "color_mode": "colorMode",
            "extension": "extension",
            "resource_id": "resourceId",
        },
    )
    class AssetTypeProperty:
        def __init__(
            self,
            *,
            bytes: typing.Optional[builtins.str] = None,
            category: typing.Optional[builtins.str] = None,
            color_mode: typing.Optional[builtins.str] = None,
            extension: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An image file from a managed login branding style in a user pool.

            :param bytes: The image file, in Base64-encoded binary.
            :param category: The category that the image corresponds to in your managed login configuration. Managed login has asset categories for different types of logos, backgrounds, and icons.
            :param color_mode: The display-mode target of the asset: light, dark, or browser-adaptive. For example, Amazon Cognito displays a dark-mode image only when the browser or application is in dark mode, but displays a browser-adaptive file in all contexts.
            :param extension: The file type of the image file.
            :param resource_id: The ID of the asset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-managedloginbranding-assettype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                asset_type_property = cognito_mixins.CfnManagedLoginBrandingPropsMixin.AssetTypeProperty(
                    bytes="bytes",
                    category="category",
                    color_mode="colorMode",
                    extension="extension",
                    resource_id="resourceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b61b5fb1f0562c023bdb570ff994a8ed6bdb641da85d627afca099f926bac8b6)
                check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                check_type(argname="argument category", value=category, expected_type=type_hints["category"])
                check_type(argname="argument color_mode", value=color_mode, expected_type=type_hints["color_mode"])
                check_type(argname="argument extension", value=extension, expected_type=type_hints["extension"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bytes is not None:
                self._values["bytes"] = bytes
            if category is not None:
                self._values["category"] = category
            if color_mode is not None:
                self._values["color_mode"] = color_mode
            if extension is not None:
                self._values["extension"] = extension
            if resource_id is not None:
                self._values["resource_id"] = resource_id

        @builtins.property
        def bytes(self) -> typing.Optional[builtins.str]:
            '''The image file, in Base64-encoded binary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-managedloginbranding-assettype.html#cfn-cognito-managedloginbranding-assettype-bytes
            '''
            result = self._values.get("bytes")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def category(self) -> typing.Optional[builtins.str]:
            '''The category that the image corresponds to in your managed login configuration.

            Managed login has asset categories for different types of logos, backgrounds, and icons.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-managedloginbranding-assettype.html#cfn-cognito-managedloginbranding-assettype-category
            '''
            result = self._values.get("category")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def color_mode(self) -> typing.Optional[builtins.str]:
            '''The display-mode target of the asset: light, dark, or browser-adaptive.

            For example, Amazon Cognito displays a dark-mode image only when the browser or application is in dark mode, but displays a browser-adaptive file in all contexts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-managedloginbranding-assettype.html#cfn-cognito-managedloginbranding-assettype-colormode
            '''
            result = self._values.get("color_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def extension(self) -> typing.Optional[builtins.str]:
            '''The file type of the image file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-managedloginbranding-assettype.html#cfn-cognito-managedloginbranding-assettype-extension
            '''
            result = self._values.get("extension")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-managedloginbranding-assettype.html#cfn-cognito-managedloginbranding-assettype-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnTermsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "enforcement": "enforcement",
        "links": "links",
        "terms_name": "termsName",
        "terms_source": "termsSource",
        "user_pool_id": "userPoolId",
    },
)
class CfnTermsMixinProps:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        enforcement: typing.Optional[builtins.str] = None,
        links: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        terms_name: typing.Optional[builtins.str] = None,
        terms_source: typing.Optional[builtins.str] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTermsPropsMixin.

        :param client_id: The ID of the app client that the terms documents are assigned to.
        :param enforcement: This parameter is reserved for future use and currently accepts one value.
        :param links: A map of URLs to languages. For each localized language that will view the requested ``TermsName`` , assign a URL. A selection of ``cognito:default`` displays for all languages that don't have a language-specific URL. For example, ``"cognito:default": "https://terms.example.com", "cognito:spanish": "https://terms.example.com/es"`` .
        :param terms_name: The type and friendly name of the terms documents.
        :param terms_source: This parameter is reserved for future use and currently accepts one value.
        :param user_pool_id: The ID of the user pool that contains the terms documents.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-terms.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            cfn_terms_mixin_props = cognito_mixins.CfnTermsMixinProps(
                client_id="clientId",
                enforcement="enforcement",
                links={
                    "links_key": "links"
                },
                terms_name="termsName",
                terms_source="termsSource",
                user_pool_id="userPoolId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50edd69682d897f64e6a8e00e18625250720173bfd2b3a93a6a57e9890d5b9ca)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument enforcement", value=enforcement, expected_type=type_hints["enforcement"])
            check_type(argname="argument links", value=links, expected_type=type_hints["links"])
            check_type(argname="argument terms_name", value=terms_name, expected_type=type_hints["terms_name"])
            check_type(argname="argument terms_source", value=terms_source, expected_type=type_hints["terms_source"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if enforcement is not None:
            self._values["enforcement"] = enforcement
        if links is not None:
            self._values["links"] = links
        if terms_name is not None:
            self._values["terms_name"] = terms_name
        if terms_source is not None:
            self._values["terms_source"] = terms_source
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the app client that the terms documents are assigned to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-terms.html#cfn-cognito-terms-clientid
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforcement(self) -> typing.Optional[builtins.str]:
        '''This parameter is reserved for future use and currently accepts one value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-terms.html#cfn-cognito-terms-enforcement
        '''
        result = self._values.get("enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def links(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''A map of URLs to languages.

        For each localized language that will view the requested ``TermsName`` , assign a URL. A selection of ``cognito:default`` displays for all languages that don't have a language-specific URL.

        For example, ``"cognito:default": "https://terms.example.com", "cognito:spanish": "https://terms.example.com/es"`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-terms.html#cfn-cognito-terms-links
        '''
        result = self._values.get("links")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def terms_name(self) -> typing.Optional[builtins.str]:
        '''The type and friendly name of the terms documents.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-terms.html#cfn-cognito-terms-termsname
        '''
        result = self._values.get("terms_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def terms_source(self) -> typing.Optional[builtins.str]:
        '''This parameter is reserved for future use and currently accepts one value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-terms.html#cfn-cognito-terms-termssource
        '''
        result = self._values.get("terms_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user pool that contains the terms documents.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-terms.html#cfn-cognito-terms-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTermsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTermsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnTermsPropsMixin",
):
    '''Creates terms documents for the requested app client.

    When Terms and conditions and Privacy policy documents are configured, the app client displays links to them in the sign-up page of managed login for the app client.

    You can provide URLs for terms documents in the languages that are supported by `managed login localization <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html#managed-login-localization>`_ . Amazon Cognito directs users to the terms documents for their current language, with fallback to ``default`` if no document exists for the language.

    Each request accepts one type of terms document and a map of language-to-link for that document type. You must provide both types of terms documents in at least one language before Amazon Cognito displays your terms documents. Supply each type in separate requests.

    For more information, see `Terms documents <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html#managed-login-terms-documents>`_ .
    .. epigraph::

       Amazon Cognito evaluates AWS Identity and Access Management (IAM) policies in requests for this API operation. For this operation, you must use IAM credentials to authorize requests, and you must grant yourself the corresponding IAM permission in a policy.

       **Learn more** - `Signing AWS API Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`_

       - `Using the Amazon Cognito user pools API and user pool endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-terms.html
    :cloudformationResource: AWS::Cognito::Terms
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_terms_props_mixin = cognito_mixins.CfnTermsPropsMixin(cognito_mixins.CfnTermsMixinProps(
            client_id="clientId",
            enforcement="enforcement",
            links={
                "links_key": "links"
            },
            terms_name="termsName",
            terms_source="termsSource",
            user_pool_id="userPoolId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTermsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::Terms``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd579d5524dde035def5068b60abb4291090b621aaaf64e0dceb3af0b5869d6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b03237ac9820180897c64f4e711a27fb1800b4803f9b6fa647a4e8e5085da24)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12bfefcccc355f52b3a3b71dffd2c558f89c4d7e2eac8d6cb2a605b118141109)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTermsMixinProps:
        return typing.cast(CfnTermsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


class CfnUserPoolApplicationLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolApplicationLogs",
):
    '''Builder for CfnUserPoolLogsMixin to generate APPLICATION_LOGS for CfnUserPool.

    :cloudformationResource: AWS::Cognito::UserPool
    :logType: APPLICATION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_user_pool_application_logs = cognito_mixins.CfnUserPoolApplicationLogs()
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
    ) -> "CfnUserPoolLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4db235510fc5eb251fa30acb177907f4382335645fc74a776d26e2b183a4de)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnUserPoolLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnUserPoolLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab0278a1a87376bbe7ef47b9b12523351081708f498ccbb854c50f112c19d8a)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnUserPoolLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnUserPoolLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26c56616c3e8cae4a801e66825c009e52b03a58064b7370625db0f3242af699)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnUserPoolLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolClientMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_token_validity": "accessTokenValidity",
        "allowed_o_auth_flows": "allowedOAuthFlows",
        "allowed_o_auth_flows_user_pool_client": "allowedOAuthFlowsUserPoolClient",
        "allowed_o_auth_scopes": "allowedOAuthScopes",
        "analytics_configuration": "analyticsConfiguration",
        "auth_session_validity": "authSessionValidity",
        "callback_ur_ls": "callbackUrLs",
        "client_name": "clientName",
        "default_redirect_uri": "defaultRedirectUri",
        "enable_propagate_additional_user_context_data": "enablePropagateAdditionalUserContextData",
        "enable_token_revocation": "enableTokenRevocation",
        "explicit_auth_flows": "explicitAuthFlows",
        "generate_secret": "generateSecret",
        "id_token_validity": "idTokenValidity",
        "logout_ur_ls": "logoutUrLs",
        "prevent_user_existence_errors": "preventUserExistenceErrors",
        "read_attributes": "readAttributes",
        "refresh_token_rotation": "refreshTokenRotation",
        "refresh_token_validity": "refreshTokenValidity",
        "supported_identity_providers": "supportedIdentityProviders",
        "token_validity_units": "tokenValidityUnits",
        "user_pool_id": "userPoolId",
        "write_attributes": "writeAttributes",
    },
)
class CfnUserPoolClientMixinProps:
    def __init__(
        self,
        *,
        access_token_validity: typing.Optional[jsii.Number] = None,
        allowed_o_auth_flows: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_o_auth_flows_user_pool_client: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        allowed_o_auth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        analytics_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolClientPropsMixin.AnalyticsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        auth_session_validity: typing.Optional[jsii.Number] = None,
        callback_ur_ls: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_name: typing.Optional[builtins.str] = None,
        default_redirect_uri: typing.Optional[builtins.str] = None,
        enable_propagate_additional_user_context_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        enable_token_revocation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        explicit_auth_flows: typing.Optional[typing.Sequence[builtins.str]] = None,
        generate_secret: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        id_token_validity: typing.Optional[jsii.Number] = None,
        logout_ur_ls: typing.Optional[typing.Sequence[builtins.str]] = None,
        prevent_user_existence_errors: typing.Optional[builtins.str] = None,
        read_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        refresh_token_rotation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolClientPropsMixin.RefreshTokenRotationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        refresh_token_validity: typing.Optional[jsii.Number] = None,
        supported_identity_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
        token_validity_units: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolClientPropsMixin.TokenValidityUnitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
        write_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnUserPoolClientPropsMixin.

        :param access_token_validity: The access token time limit. After this limit expires, your user can't use their access token. To specify the time unit for ``AccessTokenValidity`` as ``seconds`` , ``minutes`` , ``hours`` , or ``days`` , set a ``TokenValidityUnits`` value in your API request. For example, when you set ``AccessTokenValidity`` to ``10`` and ``TokenValidityUnits`` to ``hours`` , your user can authorize access with their access token for 10 hours. The default time unit for ``AccessTokenValidity`` in an API request is hours. *Valid range* is displayed below in seconds. If you don't specify otherwise in the configuration of your app client, your access tokens are valid for one hour.
        :param allowed_o_auth_flows: The OAuth grant types that you want your app client to generate for clients in managed login authentication. To create an app client that generates client credentials grants, you must add ``client_credentials`` as the only allowed OAuth flow. - **code** - Use a code grant flow, which provides an authorization code as the response. This code can be exchanged for access tokens with the ``/oauth2/token`` endpoint. - **implicit** - Issue the access token, and the ID token when scopes like ``openid`` and ``profile`` are requested, directly to your user. - **client_credentials** - Issue the access token from the ``/oauth2/token`` endpoint directly to a non-person user, authorized by a combination of the client ID and client secret.
        :param allowed_o_auth_flows_user_pool_client: Set to ``true`` to use OAuth 2.0 authorization server features in your app client. This parameter must have a value of ``true`` before you can configure the following features in your app client. - ``CallBackURLs`` : Callback URLs. - ``LogoutURLs`` : Sign-out redirect URLs. - ``AllowedOAuthScopes`` : OAuth 2.0 scopes. - ``AllowedOAuthFlows`` : Support for authorization code, implicit, and client credentials OAuth 2.0 grants. To use authorization server features, configure one of these features in the Amazon Cognito console or set ``AllowedOAuthFlowsUserPoolClient`` to ``true`` in a ``CreateUserPoolClient`` or ``UpdateUserPoolClient`` API request. If you don't set a value for ``AllowedOAuthFlowsUserPoolClient`` in a request with the AWS CLI or SDKs, it defaults to ``false`` . When ``false`` , only SDK-based API sign-in is permitted.
        :param allowed_o_auth_scopes: The OAuth, OpenID Connect (OIDC), and custom scopes that you want to permit your app client to authorize access with. Scopes govern access control to user pool self-service API operations, user data from the ``userInfo`` endpoint, and third-party APIs. Scope values include ``phone`` , ``email`` , ``openid`` , and ``profile`` . The ``aws.cognito.signin.user.admin`` scope authorizes user self-service operations. Custom scopes with resource servers authorize access to external APIs.
        :param analytics_configuration: The user pool analytics configuration for collecting metrics and sending them to your Amazon Pinpoint campaign. In AWS Regions where Amazon Pinpoint isn't available, user pools might not have access to analytics or might be configurable with campaigns in the US East (N. Virginia) Region. For more information, see `Using Amazon Pinpoint analytics <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-pinpoint-integration.html>`_ .
        :param auth_session_validity: Amazon Cognito creates a session token for each API request in an authentication flow. ``AuthSessionValidity`` is the duration, in minutes, of that session token. Your user pool native user must respond to each authentication challenge before the session expires.
        :param callback_ur_ls: A list of allowed redirect, or callback, URLs for managed login authentication. These URLs are the paths where you want to send your users' browsers after they complete authentication with managed login or a third-party IdP. Typically, callback URLs are the home of an application that uses OAuth or OIDC libraries to process authentication outcomes. A redirect URI must meet the following requirements: - Be an absolute URI. - Be registered with the authorization server. Amazon Cognito doesn't accept authorization requests with ``redirect_uri`` values that aren't in the list of ``CallbackURLs`` that you provide in this parameter. - Not include a fragment component. See `OAuth 2.0 - Redirection Endpoint <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc6749#section-3.1.2>`_ . Amazon Cognito requires HTTPS over HTTP except for callback URLs to ``http://localhost`` , ``http://127.0.0.1`` and ``http://[::1]`` . These callback URLs are for testing purposes only. You can specify custom TCP ports for your callback URLs. App callback URLs such as ``myapp://example`` are also supported.
        :param client_name: A friendly name for the app client that you want to create.
        :param default_redirect_uri: The default redirect URI. In app clients with one assigned IdP, replaces ``redirect_uri`` in authentication requests. Must be in the ``CallbackURLs`` list.
        :param enable_propagate_additional_user_context_data: When ``true`` , your application can include additional ``UserContextData`` in authentication requests. This data includes the IP address, and contributes to analysis by threat protection features. For more information about propagation of user context data, see `Adding session data to API requests <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-adaptive-authentication.html#user-pool-settings-adaptive-authentication-device-fingerprint>`_ . If you don’t include this parameter, you can't send the source IP address to Amazon Cognito threat protection features. You can only activate ``EnablePropagateAdditionalUserContextData`` in an app client that has a client secret.
        :param enable_token_revocation: Activates or deactivates token revocation. If you don't include this parameter, token revocation is automatically activated for the new user pool client.
        :param explicit_auth_flows: The `authentication flows <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow-methods.html>`_ that you want your user pool client to support. For each app client in your user pool, you can sign in your users with any combination of one or more flows, including with a user name and Secure Remote Password (SRP), a user name and password, or a custom authentication process that you define with Lambda functions. .. epigraph:: If you don't specify a value for ``ExplicitAuthFlows`` , your app client supports ``ALLOW_REFRESH_TOKEN_AUTH`` , ``ALLOW_USER_SRP_AUTH`` , and ``ALLOW_CUSTOM_AUTH`` . The values for authentication flow options include the following. - ``ALLOW_USER_AUTH`` : Enable selection-based sign-in with ``USER_AUTH`` . This setting covers username-password, secure remote password (SRP), passwordless, and passkey authentication. This authentiation flow can do username-password and SRP authentication without other ``ExplicitAuthFlows`` permitting them. For example users can complete an SRP challenge through ``USER_AUTH`` without the flow ``USER_SRP_AUTH`` being active for the app client. This flow doesn't include ``CUSTOM_AUTH`` . To activate this setting, your user pool must be in the `Essentials tier <https://docs.aws.amazon.com/cognito/latest/developerguide/feature-plans-features-essentials.html>`_ or higher. - ``ALLOW_ADMIN_USER_PASSWORD_AUTH`` : Enable admin based user password authentication flow ``ADMIN_USER_PASSWORD_AUTH`` . This setting replaces the ``ADMIN_NO_SRP_AUTH`` setting. With this authentication flow, your app passes a user name and password to Amazon Cognito in the request, instead of using the Secure Remote Password (SRP) protocol to securely transmit the password. - ``ALLOW_CUSTOM_AUTH`` : Enable Lambda trigger based authentication. - ``ALLOW_USER_PASSWORD_AUTH`` : Enable user password-based authentication. In this flow, Amazon Cognito receives the password in the request instead of using the SRP protocol to verify passwords. - ``ALLOW_USER_SRP_AUTH`` : Enable SRP-based authentication. - ``ALLOW_REFRESH_TOKEN_AUTH`` : Enable authflow to refresh tokens. In some environments, you will see the values ``ADMIN_NO_SRP_AUTH`` , ``CUSTOM_AUTH_FLOW_ONLY`` , or ``USER_PASSWORD_AUTH`` . You can't assign these legacy ``ExplicitAuthFlows`` values to user pool clients at the same time as values that begin with ``ALLOW_`` , like ``ALLOW_USER_SRP_AUTH`` .
        :param generate_secret: When ``true`` , generates a client secret for the app client. Client secrets are used with server-side and machine-to-machine applications. Client secrets are automatically generated; you can't specify a secret value. For more information, see `App client types <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html#user-pool-settings-client-app-client-types>`_ .
        :param id_token_validity: The ID token time limit. After this limit expires, your user can't use their ID token. To specify the time unit for ``IdTokenValidity`` as ``seconds`` , ``minutes`` , ``hours`` , or ``days`` , set a ``TokenValidityUnits`` value in your API request. For example, when you set ``IdTokenValidity`` as ``10`` and ``TokenValidityUnits`` as ``hours`` , your user can authenticate their session with their ID token for 10 hours. The default time unit for ``IdTokenValidity`` in an API request is hours. *Valid range* is displayed below in seconds. If you don't specify otherwise in the configuration of your app client, your ID tokens are valid for one hour.
        :param logout_ur_ls: A list of allowed logout URLs for managed login authentication. When you pass ``logout_uri`` and ``client_id`` parameters to ``/logout`` , Amazon Cognito signs out your user and redirects them to the logout URL. This parameter describes the URLs that you want to be the permitted targets of ``logout_uri`` . A typical use of these URLs is when a user selects "Sign out" and you redirect them to your public homepage. For more information, see `Logout endpoint <https://docs.aws.amazon.com/cognito/latest/developerguide/logout-endpoint.html>`_ .
        :param prevent_user_existence_errors: Errors and responses that you want Amazon Cognito APIs to return during authentication, account confirmation, and password recovery when the user doesn't exist in the user pool. When set to ``ENABLED`` and the user doesn't exist, authentication returns an error indicating either the username or password was incorrect. Account confirmation and password recovery return a response indicating a code was sent to a simulated destination. When set to ``LEGACY`` , those APIs return a ``UserNotFoundException`` exception if the user doesn't exist in the user pool. Valid values include: - ``ENABLED`` - This prevents user existence-related errors. - ``LEGACY`` - This represents the early behavior of Amazon Cognito where user existence related errors aren't prevented. Defaults to ``LEGACY`` when you don't provide a value.
        :param read_attributes: The list of user attributes that you want your app client to have read access to. After your user authenticates in your app, their access token authorizes them to read their own attribute value for any attribute in this list. An example of this kind of activity is when your user selects a link to view their profile information. When you don't specify the ``ReadAttributes`` for your app client, your app can read the values of ``email_verified`` , ``phone_number_verified`` , and the Standard attributes of your user pool. When your user pool app client has read access to these default attributes, ``ReadAttributes`` doesn't return any information. Amazon Cognito only populates ``ReadAttributes`` in the API response if you have specified your own custom set of read attributes.
        :param refresh_token_rotation: The configuration of your app client for refresh token rotation. When enabled, your app client issues new ID, access, and refresh tokens when users renew their sessions with refresh tokens. When disabled, token refresh issues only ID and access tokens.
        :param refresh_token_validity: The refresh token time limit. After this limit expires, your user can't use their refresh token. To specify the time unit for ``RefreshTokenValidity`` as ``seconds`` , ``minutes`` , ``hours`` , or ``days`` , set a ``TokenValidityUnits`` value in your API request. For example, when you set ``RefreshTokenValidity`` as ``10`` and ``TokenValidityUnits`` as ``days`` , your user can refresh their session and retrieve new access and ID tokens for 10 days. The default time unit for ``RefreshTokenValidity`` in an API request is days. You can't set ``RefreshTokenValidity`` to 0. If you do, Amazon Cognito overrides the value with the default value of 30 days. *Valid range* is displayed below in seconds. If you don't specify otherwise in the configuration of your app client, your refresh tokens are valid for 30 days.
        :param supported_identity_providers: A list of provider names for the identity providers (IdPs) that are supported on this client. The following are supported: ``COGNITO`` , ``Facebook`` , ``Google`` , ``SignInWithApple`` , and ``LoginWithAmazon`` . You can also specify the names that you configured for the SAML and OIDC IdPs in your user pool, for example ``MySAMLIdP`` or ``MyOIDCIdP`` . This parameter sets the IdPs that `managed login <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html>`_ will display on the login page for your app client. The removal of ``COGNITO`` from this list doesn't prevent authentication operations for local users with the user pools API in an AWS SDK. The only way to prevent SDK-based authentication is to block access with a `AWS WAF rule <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-waf.html>`_ .
        :param token_validity_units: The units that validity times are represented in. The default unit for refresh tokens is days, and the default for ID and access tokens are hours.
        :param user_pool_id: The ID of the user pool where you want to create an app client.
        :param write_attributes: The list of user attributes that you want your app client to have write access to. After your user authenticates in your app, their access token authorizes them to set or modify their own attribute value for any attribute in this list. When you don't specify the ``WriteAttributes`` for your app client, your app can write the values of the Standard attributes of your user pool. When your user pool has write access to these default attributes, ``WriteAttributes`` doesn't return any information. Amazon Cognito only populates ``WriteAttributes`` in the API response if you have specified your own custom set of write attributes. If your app client allows users to sign in through an IdP, this array must include all attributes that you have mapped to IdP attributes. Amazon Cognito updates mapped attributes when users sign in to your application through an IdP. If your app client does not have write access to a mapped attribute, Amazon Cognito throws an error when it tries to update the attribute. For more information, see `Specifying IdP Attribute Mappings for Your user pool <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-specifying-attribute-mapping.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            cfn_user_pool_client_mixin_props = cognito_mixins.CfnUserPoolClientMixinProps(
                access_token_validity=123,
                allowed_oAuth_flows=["allowedOAuthFlows"],
                allowed_oAuth_flows_user_pool_client=False,
                allowed_oAuth_scopes=["allowedOAuthScopes"],
                analytics_configuration=cognito_mixins.CfnUserPoolClientPropsMixin.AnalyticsConfigurationProperty(
                    application_arn="applicationArn",
                    application_id="applicationId",
                    external_id="externalId",
                    role_arn="roleArn",
                    user_data_shared=False
                ),
                auth_session_validity=123,
                callback_ur_ls=["callbackUrLs"],
                client_name="clientName",
                default_redirect_uri="defaultRedirectUri",
                enable_propagate_additional_user_context_data=False,
                enable_token_revocation=False,
                explicit_auth_flows=["explicitAuthFlows"],
                generate_secret=False,
                id_token_validity=123,
                logout_ur_ls=["logoutUrLs"],
                prevent_user_existence_errors="preventUserExistenceErrors",
                read_attributes=["readAttributes"],
                refresh_token_rotation=cognito_mixins.CfnUserPoolClientPropsMixin.RefreshTokenRotationProperty(
                    feature="feature",
                    retry_grace_period_seconds=123
                ),
                refresh_token_validity=123,
                supported_identity_providers=["supportedIdentityProviders"],
                token_validity_units=cognito_mixins.CfnUserPoolClientPropsMixin.TokenValidityUnitsProperty(
                    access_token="accessToken",
                    id_token="idToken",
                    refresh_token="refreshToken"
                ),
                user_pool_id="userPoolId",
                write_attributes=["writeAttributes"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e532d389795ac4922c47d8ce6cacb3d723d5e3f8de091a81a562936c9559ce4)
            check_type(argname="argument access_token_validity", value=access_token_validity, expected_type=type_hints["access_token_validity"])
            check_type(argname="argument allowed_o_auth_flows", value=allowed_o_auth_flows, expected_type=type_hints["allowed_o_auth_flows"])
            check_type(argname="argument allowed_o_auth_flows_user_pool_client", value=allowed_o_auth_flows_user_pool_client, expected_type=type_hints["allowed_o_auth_flows_user_pool_client"])
            check_type(argname="argument allowed_o_auth_scopes", value=allowed_o_auth_scopes, expected_type=type_hints["allowed_o_auth_scopes"])
            check_type(argname="argument analytics_configuration", value=analytics_configuration, expected_type=type_hints["analytics_configuration"])
            check_type(argname="argument auth_session_validity", value=auth_session_validity, expected_type=type_hints["auth_session_validity"])
            check_type(argname="argument callback_ur_ls", value=callback_ur_ls, expected_type=type_hints["callback_ur_ls"])
            check_type(argname="argument client_name", value=client_name, expected_type=type_hints["client_name"])
            check_type(argname="argument default_redirect_uri", value=default_redirect_uri, expected_type=type_hints["default_redirect_uri"])
            check_type(argname="argument enable_propagate_additional_user_context_data", value=enable_propagate_additional_user_context_data, expected_type=type_hints["enable_propagate_additional_user_context_data"])
            check_type(argname="argument enable_token_revocation", value=enable_token_revocation, expected_type=type_hints["enable_token_revocation"])
            check_type(argname="argument explicit_auth_flows", value=explicit_auth_flows, expected_type=type_hints["explicit_auth_flows"])
            check_type(argname="argument generate_secret", value=generate_secret, expected_type=type_hints["generate_secret"])
            check_type(argname="argument id_token_validity", value=id_token_validity, expected_type=type_hints["id_token_validity"])
            check_type(argname="argument logout_ur_ls", value=logout_ur_ls, expected_type=type_hints["logout_ur_ls"])
            check_type(argname="argument prevent_user_existence_errors", value=prevent_user_existence_errors, expected_type=type_hints["prevent_user_existence_errors"])
            check_type(argname="argument read_attributes", value=read_attributes, expected_type=type_hints["read_attributes"])
            check_type(argname="argument refresh_token_rotation", value=refresh_token_rotation, expected_type=type_hints["refresh_token_rotation"])
            check_type(argname="argument refresh_token_validity", value=refresh_token_validity, expected_type=type_hints["refresh_token_validity"])
            check_type(argname="argument supported_identity_providers", value=supported_identity_providers, expected_type=type_hints["supported_identity_providers"])
            check_type(argname="argument token_validity_units", value=token_validity_units, expected_type=type_hints["token_validity_units"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            check_type(argname="argument write_attributes", value=write_attributes, expected_type=type_hints["write_attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token_validity is not None:
            self._values["access_token_validity"] = access_token_validity
        if allowed_o_auth_flows is not None:
            self._values["allowed_o_auth_flows"] = allowed_o_auth_flows
        if allowed_o_auth_flows_user_pool_client is not None:
            self._values["allowed_o_auth_flows_user_pool_client"] = allowed_o_auth_flows_user_pool_client
        if allowed_o_auth_scopes is not None:
            self._values["allowed_o_auth_scopes"] = allowed_o_auth_scopes
        if analytics_configuration is not None:
            self._values["analytics_configuration"] = analytics_configuration
        if auth_session_validity is not None:
            self._values["auth_session_validity"] = auth_session_validity
        if callback_ur_ls is not None:
            self._values["callback_ur_ls"] = callback_ur_ls
        if client_name is not None:
            self._values["client_name"] = client_name
        if default_redirect_uri is not None:
            self._values["default_redirect_uri"] = default_redirect_uri
        if enable_propagate_additional_user_context_data is not None:
            self._values["enable_propagate_additional_user_context_data"] = enable_propagate_additional_user_context_data
        if enable_token_revocation is not None:
            self._values["enable_token_revocation"] = enable_token_revocation
        if explicit_auth_flows is not None:
            self._values["explicit_auth_flows"] = explicit_auth_flows
        if generate_secret is not None:
            self._values["generate_secret"] = generate_secret
        if id_token_validity is not None:
            self._values["id_token_validity"] = id_token_validity
        if logout_ur_ls is not None:
            self._values["logout_ur_ls"] = logout_ur_ls
        if prevent_user_existence_errors is not None:
            self._values["prevent_user_existence_errors"] = prevent_user_existence_errors
        if read_attributes is not None:
            self._values["read_attributes"] = read_attributes
        if refresh_token_rotation is not None:
            self._values["refresh_token_rotation"] = refresh_token_rotation
        if refresh_token_validity is not None:
            self._values["refresh_token_validity"] = refresh_token_validity
        if supported_identity_providers is not None:
            self._values["supported_identity_providers"] = supported_identity_providers
        if token_validity_units is not None:
            self._values["token_validity_units"] = token_validity_units
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id
        if write_attributes is not None:
            self._values["write_attributes"] = write_attributes

    @builtins.property
    def access_token_validity(self) -> typing.Optional[jsii.Number]:
        '''The access token time limit.

        After this limit expires, your user can't use their access token. To specify the time unit for ``AccessTokenValidity`` as ``seconds`` , ``minutes`` , ``hours`` , or ``days`` , set a ``TokenValidityUnits`` value in your API request.

        For example, when you set ``AccessTokenValidity`` to ``10`` and ``TokenValidityUnits`` to ``hours`` , your user can authorize access with
        their access token for 10 hours.

        The default time unit for ``AccessTokenValidity`` in an API request is hours. *Valid range* is displayed below in seconds.

        If you don't specify otherwise in the configuration of your app client, your access
        tokens are valid for one hour.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-accesstokenvalidity
        '''
        result = self._values.get("access_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def allowed_o_auth_flows(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The OAuth grant types that you want your app client to generate for clients in managed login authentication.

        To create an app client that generates client credentials grants, you must add ``client_credentials`` as the only allowed OAuth flow.

        - **code** - Use a code grant flow, which provides an authorization code as the response. This code can be exchanged for access tokens with the ``/oauth2/token`` endpoint.
        - **implicit** - Issue the access token, and the ID token when scopes like ``openid`` and ``profile`` are requested, directly to your user.
        - **client_credentials** - Issue the access token from the ``/oauth2/token`` endpoint directly to a non-person user, authorized by a combination of the client ID and client secret.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthflows
        '''
        result = self._values.get("allowed_o_auth_flows")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_o_auth_flows_user_pool_client(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Set to ``true`` to use OAuth 2.0 authorization server features in your app client.

        This parameter must have a value of ``true`` before you can configure the following features in your app client.

        - ``CallBackURLs`` : Callback URLs.
        - ``LogoutURLs`` : Sign-out redirect URLs.
        - ``AllowedOAuthScopes`` : OAuth 2.0 scopes.
        - ``AllowedOAuthFlows`` : Support for authorization code, implicit, and client credentials OAuth 2.0 grants.

        To use authorization server features, configure one of these features in the Amazon Cognito console or set ``AllowedOAuthFlowsUserPoolClient`` to ``true`` in a ``CreateUserPoolClient`` or ``UpdateUserPoolClient`` API request. If you don't set a value for ``AllowedOAuthFlowsUserPoolClient`` in a request with the AWS CLI or SDKs, it defaults to ``false`` . When ``false`` , only SDK-based API sign-in is permitted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthflowsuserpoolclient
        '''
        result = self._values.get("allowed_o_auth_flows_user_pool_client")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def allowed_o_auth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The OAuth, OpenID Connect (OIDC), and custom scopes that you want to permit your app client to authorize access with.

        Scopes govern access control to user pool self-service API operations, user data from the ``userInfo`` endpoint, and third-party APIs. Scope values include ``phone`` , ``email`` , ``openid`` , and ``profile`` . The ``aws.cognito.signin.user.admin`` scope authorizes user self-service operations. Custom scopes with resource servers authorize access to external APIs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthscopes
        '''
        result = self._values.get("allowed_o_auth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def analytics_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolClientPropsMixin.AnalyticsConfigurationProperty"]]:
        '''The user pool analytics configuration for collecting metrics and sending them to your Amazon Pinpoint campaign.

        In AWS Regions where Amazon Pinpoint isn't available, user pools might not have access to analytics or might be configurable with campaigns in the US East (N. Virginia) Region. For more information, see `Using Amazon Pinpoint analytics <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-pinpoint-integration.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-analyticsconfiguration
        '''
        result = self._values.get("analytics_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolClientPropsMixin.AnalyticsConfigurationProperty"]], result)

    @builtins.property
    def auth_session_validity(self) -> typing.Optional[jsii.Number]:
        '''Amazon Cognito creates a session token for each API request in an authentication flow.

        ``AuthSessionValidity`` is the duration, in minutes, of that session token. Your user pool native user must respond to each authentication challenge before the session expires.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-authsessionvalidity
        '''
        result = self._values.get("auth_session_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def callback_ur_ls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of allowed redirect, or callback, URLs for managed login authentication.

        These URLs are the paths where you want to send your users' browsers after they complete authentication with managed login or a third-party IdP. Typically, callback URLs are the home of an application that uses OAuth or OIDC libraries to process authentication outcomes.

        A redirect URI must meet the following requirements:

        - Be an absolute URI.
        - Be registered with the authorization server. Amazon Cognito doesn't accept authorization requests with ``redirect_uri`` values that aren't in the list of ``CallbackURLs`` that you provide in this parameter.
        - Not include a fragment component.

        See `OAuth 2.0 - Redirection Endpoint <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc6749#section-3.1.2>`_ .

        Amazon Cognito requires HTTPS over HTTP except for callback URLs to ``http://localhost`` , ``http://127.0.0.1`` and ``http://[::1]`` . These callback URLs are for testing purposes only. You can specify custom TCP ports for your callback URLs.

        App callback URLs such as ``myapp://example`` are also supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-callbackurls
        '''
        result = self._values.get("callback_ur_ls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_name(self) -> typing.Optional[builtins.str]:
        '''A friendly name for the app client that you want to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-clientname
        '''
        result = self._values.get("client_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_redirect_uri(self) -> typing.Optional[builtins.str]:
        '''The default redirect URI.

        In app clients with one assigned IdP, replaces ``redirect_uri`` in authentication requests. Must be in the ``CallbackURLs`` list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-defaultredirecturi
        '''
        result = self._values.get("default_redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_propagate_additional_user_context_data(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When ``true`` , your application can include additional ``UserContextData`` in authentication requests.

        This data includes the IP address, and contributes to analysis by threat protection features. For more information about propagation of user context data, see `Adding session data to API requests <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-adaptive-authentication.html#user-pool-settings-adaptive-authentication-device-fingerprint>`_ . If you don’t include this parameter, you can't send the source IP address to Amazon Cognito threat protection features. You can only activate ``EnablePropagateAdditionalUserContextData`` in an app client that has a client secret.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-enablepropagateadditionalusercontextdata
        '''
        result = self._values.get("enable_propagate_additional_user_context_data")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def enable_token_revocation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Activates or deactivates token revocation.

        If you don't include this parameter, token revocation is automatically activated for the new user pool client.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-enabletokenrevocation
        '''
        result = self._values.get("enable_token_revocation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def explicit_auth_flows(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The `authentication flows <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow-methods.html>`_ that you want your user pool client to support. For each app client in your user pool, you can sign in your users with any combination of one or more flows, including with a user name and Secure Remote Password (SRP), a user name and password, or a custom authentication process that you define with Lambda functions.

        .. epigraph::

           If you don't specify a value for ``ExplicitAuthFlows`` , your app client supports ``ALLOW_REFRESH_TOKEN_AUTH`` , ``ALLOW_USER_SRP_AUTH`` , and ``ALLOW_CUSTOM_AUTH`` .

        The values for authentication flow options include the following.

        - ``ALLOW_USER_AUTH`` : Enable selection-based sign-in with ``USER_AUTH`` . This setting covers username-password, secure remote password (SRP), passwordless, and passkey authentication. This authentiation flow can do username-password and SRP authentication without other ``ExplicitAuthFlows`` permitting them. For example users can complete an SRP challenge through ``USER_AUTH`` without the flow ``USER_SRP_AUTH`` being active for the app client. This flow doesn't include ``CUSTOM_AUTH`` .

        To activate this setting, your user pool must be in the `Essentials tier <https://docs.aws.amazon.com/cognito/latest/developerguide/feature-plans-features-essentials.html>`_ or higher.

        - ``ALLOW_ADMIN_USER_PASSWORD_AUTH`` : Enable admin based user password authentication flow ``ADMIN_USER_PASSWORD_AUTH`` . This setting replaces the ``ADMIN_NO_SRP_AUTH`` setting. With this authentication flow, your app passes a user name and password to Amazon Cognito in the request, instead of using the Secure Remote Password (SRP) protocol to securely transmit the password.
        - ``ALLOW_CUSTOM_AUTH`` : Enable Lambda trigger based authentication.
        - ``ALLOW_USER_PASSWORD_AUTH`` : Enable user password-based authentication. In this flow, Amazon Cognito receives the password in the request instead of using the SRP protocol to verify passwords.
        - ``ALLOW_USER_SRP_AUTH`` : Enable SRP-based authentication.
        - ``ALLOW_REFRESH_TOKEN_AUTH`` : Enable authflow to refresh tokens.

        In some environments, you will see the values ``ADMIN_NO_SRP_AUTH`` , ``CUSTOM_AUTH_FLOW_ONLY`` , or ``USER_PASSWORD_AUTH`` . You can't assign these legacy ``ExplicitAuthFlows`` values to user pool clients at the same time as values that begin with ``ALLOW_`` ,
        like ``ALLOW_USER_SRP_AUTH`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-explicitauthflows
        '''
        result = self._values.get("explicit_auth_flows")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def generate_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When ``true`` , generates a client secret for the app client.

        Client secrets are used with server-side and machine-to-machine applications. Client secrets are automatically generated; you can't specify a secret value. For more information, see `App client types <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html#user-pool-settings-client-app-client-types>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-generatesecret
        '''
        result = self._values.get("generate_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def id_token_validity(self) -> typing.Optional[jsii.Number]:
        '''The ID token time limit.

        After this limit expires, your user can't use their ID token. To specify the time unit for ``IdTokenValidity`` as ``seconds`` , ``minutes`` , ``hours`` , or ``days`` , set a ``TokenValidityUnits`` value in your API request.

        For example, when you set ``IdTokenValidity`` as ``10`` and ``TokenValidityUnits`` as ``hours`` , your user can authenticate their session with their ID token for 10 hours.

        The default time unit for ``IdTokenValidity`` in an API request is hours. *Valid range* is displayed below in seconds.

        If you don't specify otherwise in the configuration of your app client, your ID
        tokens are valid for one hour.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-idtokenvalidity
        '''
        result = self._values.get("id_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def logout_ur_ls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of allowed logout URLs for managed login authentication.

        When you pass ``logout_uri`` and ``client_id`` parameters to ``/logout`` , Amazon Cognito signs out your user and redirects them to the logout URL. This parameter describes the URLs that you want to be the permitted targets of ``logout_uri`` . A typical use of these URLs is when a user selects "Sign out" and you redirect them to your public homepage. For more information, see `Logout endpoint <https://docs.aws.amazon.com/cognito/latest/developerguide/logout-endpoint.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-logouturls
        '''
        result = self._values.get("logout_ur_ls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prevent_user_existence_errors(self) -> typing.Optional[builtins.str]:
        '''Errors and responses that you want Amazon Cognito APIs to return during authentication, account confirmation, and password recovery when the user doesn't exist in the user pool.

        When set to ``ENABLED`` and the user doesn't exist, authentication returns an error indicating either the username or password was incorrect. Account confirmation and password recovery return a response indicating a code was sent to a simulated destination. When set to ``LEGACY`` , those APIs return a ``UserNotFoundException`` exception if the user doesn't exist in the user pool.

        Valid values include:

        - ``ENABLED`` - This prevents user existence-related errors.
        - ``LEGACY`` - This represents the early behavior of Amazon Cognito where user existence related errors aren't prevented.

        Defaults to ``LEGACY`` when you don't provide a value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-preventuserexistenceerrors
        '''
        result = self._values.get("prevent_user_existence_errors")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of user attributes that you want your app client to have read access to.

        After your user authenticates in your app, their access token authorizes them to read their own attribute value for any attribute in this list. An example of this kind of activity is when your user selects a link to view their profile information.

        When you don't specify the ``ReadAttributes`` for your app client, your app can read the values of ``email_verified`` , ``phone_number_verified`` , and the Standard attributes of your user pool. When your user pool app client has read access to these default attributes, ``ReadAttributes`` doesn't return any information. Amazon Cognito only populates ``ReadAttributes`` in the API response if you have specified your own custom set of read attributes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-readattributes
        '''
        result = self._values.get("read_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def refresh_token_rotation(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolClientPropsMixin.RefreshTokenRotationProperty"]]:
        '''The configuration of your app client for refresh token rotation.

        When enabled, your app client issues new ID, access, and refresh tokens when users renew their sessions with refresh tokens. When disabled, token refresh issues only ID and access tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-refreshtokenrotation
        '''
        result = self._values.get("refresh_token_rotation")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolClientPropsMixin.RefreshTokenRotationProperty"]], result)

    @builtins.property
    def refresh_token_validity(self) -> typing.Optional[jsii.Number]:
        '''The refresh token time limit.

        After this limit expires, your user can't use their refresh token. To specify the time unit for ``RefreshTokenValidity`` as ``seconds`` , ``minutes`` , ``hours`` , or ``days`` , set a ``TokenValidityUnits`` value in your API request.

        For example, when you set ``RefreshTokenValidity`` as ``10`` and ``TokenValidityUnits`` as ``days`` , your user can refresh their session
        and retrieve new access and ID tokens for 10 days.

        The default time unit for ``RefreshTokenValidity`` in an API request is days. You can't set ``RefreshTokenValidity`` to 0. If you do, Amazon Cognito overrides the value with the default value of 30 days. *Valid range* is displayed below in seconds.

        If you don't specify otherwise in the configuration of your app client, your refresh
        tokens are valid for 30 days.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-refreshtokenvalidity
        '''
        result = self._values.get("refresh_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def supported_identity_providers(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of provider names for the identity providers (IdPs) that are supported on this client.

        The following are supported: ``COGNITO`` , ``Facebook`` , ``Google`` , ``SignInWithApple`` , and ``LoginWithAmazon`` . You can also specify the names that you configured for the SAML and OIDC IdPs in your user pool, for example ``MySAMLIdP`` or ``MyOIDCIdP`` .

        This parameter sets the IdPs that `managed login <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html>`_ will display on the login page for your app client. The removal of ``COGNITO`` from this list doesn't prevent authentication operations for local users with the user pools API in an AWS SDK. The only way to prevent SDK-based authentication is to block access with a `AWS WAF rule <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-waf.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-supportedidentityproviders
        '''
        result = self._values.get("supported_identity_providers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def token_validity_units(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolClientPropsMixin.TokenValidityUnitsProperty"]]:
        '''The units that validity times are represented in.

        The default unit for refresh tokens is days, and the default for ID and access tokens are hours.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-tokenvalidityunits
        '''
        result = self._values.get("token_validity_units")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolClientPropsMixin.TokenValidityUnitsProperty"]], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user pool where you want to create an app client.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def write_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of user attributes that you want your app client to have write access to.

        After your user authenticates in your app, their access token authorizes them to set or modify their own attribute value for any attribute in this list.

        When you don't specify the ``WriteAttributes`` for your app client, your app can write the values of the Standard attributes of your user pool. When your user pool has write access to these default attributes, ``WriteAttributes`` doesn't return any information. Amazon Cognito only populates ``WriteAttributes`` in the API response if you have specified your own custom set of write attributes.

        If your app client allows users to sign in through an IdP, this array must include all attributes that you have mapped to IdP attributes. Amazon Cognito updates mapped attributes when users sign in to your application through an IdP. If your app client does not have write access to a mapped attribute, Amazon Cognito throws an error when it tries to update the attribute. For more information, see `Specifying IdP Attribute Mappings for Your user pool <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-specifying-attribute-mapping.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-writeattributes
        '''
        result = self._values.get("write_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolClientMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolClientPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolClientPropsMixin",
):
    '''The ``AWS::Cognito::UserPoolClient`` resource specifies an Amazon Cognito user pool client.

    .. epigraph::

       If you don't specify a value for a parameter, Amazon Cognito sets it to a default value.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html
    :cloudformationResource: AWS::Cognito::UserPoolClient
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_user_pool_client_props_mixin = cognito_mixins.CfnUserPoolClientPropsMixin(cognito_mixins.CfnUserPoolClientMixinProps(
            access_token_validity=123,
            allowed_oAuth_flows=["allowedOAuthFlows"],
            allowed_oAuth_flows_user_pool_client=False,
            allowed_oAuth_scopes=["allowedOAuthScopes"],
            analytics_configuration=cognito_mixins.CfnUserPoolClientPropsMixin.AnalyticsConfigurationProperty(
                application_arn="applicationArn",
                application_id="applicationId",
                external_id="externalId",
                role_arn="roleArn",
                user_data_shared=False
            ),
            auth_session_validity=123,
            callback_ur_ls=["callbackUrLs"],
            client_name="clientName",
            default_redirect_uri="defaultRedirectUri",
            enable_propagate_additional_user_context_data=False,
            enable_token_revocation=False,
            explicit_auth_flows=["explicitAuthFlows"],
            generate_secret=False,
            id_token_validity=123,
            logout_ur_ls=["logoutUrLs"],
            prevent_user_existence_errors="preventUserExistenceErrors",
            read_attributes=["readAttributes"],
            refresh_token_rotation=cognito_mixins.CfnUserPoolClientPropsMixin.RefreshTokenRotationProperty(
                feature="feature",
                retry_grace_period_seconds=123
            ),
            refresh_token_validity=123,
            supported_identity_providers=["supportedIdentityProviders"],
            token_validity_units=cognito_mixins.CfnUserPoolClientPropsMixin.TokenValidityUnitsProperty(
                access_token="accessToken",
                id_token="idToken",
                refresh_token="refreshToken"
            ),
            user_pool_id="userPoolId",
            write_attributes=["writeAttributes"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPoolClientMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::UserPoolClient``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b63a49343b23ab25d840335f4463698504a034a39338fdda7c875103036248)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4623a022f2c8c9b26f180bba43525e5ac3b20f34c0081a5ab8bdf9112b0c775a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb4011ec7b79d05bcbe288b3736f4b905388ff454842ecd2fd84f90e8ad4346)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPoolClientMixinProps:
        return typing.cast(CfnUserPoolClientMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolClientPropsMixin.AnalyticsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_arn": "applicationArn",
            "application_id": "applicationId",
            "external_id": "externalId",
            "role_arn": "roleArn",
            "user_data_shared": "userDataShared",
        },
    )
    class AnalyticsConfigurationProperty:
        def __init__(
            self,
            *,
            application_arn: typing.Optional[builtins.str] = None,
            application_id: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            user_data_shared: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The settings for Amazon Pinpoint analytics configuration.

            With an analytics configuration, your application can collect user-activity metrics for user notifications with a Amazon Pinpoint campaign.

            Amazon Pinpoint isn't available in all AWS Regions. For a list of available Regions, see `Amazon Cognito and Amazon Pinpoint Region availability <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-pinpoint-integration.html#cognito-user-pools-find-region-mappings>`_ .

            :param application_arn: The Amazon Resource Name (ARN) of an Amazon Pinpoint project that you want to connect to your user pool app client. Amazon Cognito publishes events to the Amazon Pinpoint project that ``ApplicationArn`` declares. You can also configure your application to pass an endpoint ID in the ``AnalyticsMetadata`` parameter of sign-in operations. The endpoint ID is information about the destination for push notifications
            :param application_id: Your Amazon Pinpoint project ID.
            :param external_id: The `external ID <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html>`_ of the role that Amazon Cognito assumes to send analytics data to Amazon Pinpoint.
            :param role_arn: The ARN of an AWS Identity and Access Management role that has the permissions required for Amazon Cognito to publish events to Amazon Pinpoint analytics.
            :param user_data_shared: If ``UserDataShared`` is ``true`` , Amazon Cognito includes user data in the events that it publishes to Amazon Pinpoint analytics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                analytics_configuration_property = cognito_mixins.CfnUserPoolClientPropsMixin.AnalyticsConfigurationProperty(
                    application_arn="applicationArn",
                    application_id="applicationId",
                    external_id="externalId",
                    role_arn="roleArn",
                    user_data_shared=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e332caa52c3ae7ca3bde041e68ce083c5fa259abda034e66762e877a679ce44f)
                check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
                check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument user_data_shared", value=user_data_shared, expected_type=type_hints["user_data_shared"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_arn is not None:
                self._values["application_arn"] = application_arn
            if application_id is not None:
                self._values["application_id"] = application_id
            if external_id is not None:
                self._values["external_id"] = external_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if user_data_shared is not None:
                self._values["user_data_shared"] = user_data_shared

        @builtins.property
        def application_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an Amazon Pinpoint project that you want to connect to your user pool app client.

            Amazon Cognito publishes events to the Amazon Pinpoint project that ``ApplicationArn`` declares. You can also configure your application to pass an endpoint ID in the ``AnalyticsMetadata`` parameter of sign-in operations. The endpoint ID is information about the destination for push notifications

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-applicationarn
            '''
            result = self._values.get("application_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def application_id(self) -> typing.Optional[builtins.str]:
            '''Your Amazon Pinpoint project ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-applicationid
            '''
            result = self._values.get("application_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The `external ID <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html>`_ of the role that Amazon Cognito assumes to send analytics data to Amazon Pinpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an AWS Identity and Access Management role that has the permissions required for Amazon Cognito to publish events to Amazon Pinpoint analytics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_data_shared(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If ``UserDataShared`` is ``true`` , Amazon Cognito includes user data in the events that it publishes to Amazon Pinpoint analytics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-userdatashared
            '''
            result = self._values.get("user_data_shared")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalyticsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolClientPropsMixin.RefreshTokenRotationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "feature": "feature",
            "retry_grace_period_seconds": "retryGracePeriodSeconds",
        },
    )
    class RefreshTokenRotationProperty:
        def __init__(
            self,
            *,
            feature: typing.Optional[builtins.str] = None,
            retry_grace_period_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration of your app client for refresh token rotation.

            When enabled, your app client issues new ID, access, and refresh tokens when users renew their sessions with refresh tokens. When disabled, token refresh issues only ID and access tokens.

            :param feature: The state of refresh token rotation for the current app client.
            :param retry_grace_period_seconds: When you request a token refresh with ``GetTokensFromRefreshToken`` , the original refresh token that you're rotating out can remain valid for a period of time of up to 60 seconds. This allows for client-side retries. When ``RetryGracePeriodSeconds`` is ``0`` , the grace period is disabled and a successful request immediately invalidates the submitted refresh token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-refreshtokenrotation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                refresh_token_rotation_property = cognito_mixins.CfnUserPoolClientPropsMixin.RefreshTokenRotationProperty(
                    feature="feature",
                    retry_grace_period_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__613c8c20af6e35d6859a7cfb9597b5eae4f28578e550ca3b6685280877fe131a)
                check_type(argname="argument feature", value=feature, expected_type=type_hints["feature"])
                check_type(argname="argument retry_grace_period_seconds", value=retry_grace_period_seconds, expected_type=type_hints["retry_grace_period_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if feature is not None:
                self._values["feature"] = feature
            if retry_grace_period_seconds is not None:
                self._values["retry_grace_period_seconds"] = retry_grace_period_seconds

        @builtins.property
        def feature(self) -> typing.Optional[builtins.str]:
            '''The state of refresh token rotation for the current app client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-refreshtokenrotation.html#cfn-cognito-userpoolclient-refreshtokenrotation-feature
            '''
            result = self._values.get("feature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retry_grace_period_seconds(self) -> typing.Optional[jsii.Number]:
            '''When you request a token refresh with ``GetTokensFromRefreshToken`` , the original refresh token that you're rotating out can remain valid for a period of time of up to 60 seconds.

            This allows for client-side retries. When ``RetryGracePeriodSeconds`` is ``0`` , the grace period is disabled and a successful request immediately invalidates the submitted refresh token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-refreshtokenrotation.html#cfn-cognito-userpoolclient-refreshtokenrotation-retrygraceperiodseconds
            '''
            result = self._values.get("retry_grace_period_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RefreshTokenRotationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolClientPropsMixin.TokenValidityUnitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "id_token": "idToken",
            "refresh_token": "refreshToken",
        },
    )
    class TokenValidityUnitsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            id_token: typing.Optional[builtins.str] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The units that validity times are represented in.

            The default unit for refresh tokens is days, and the default for ID and access tokens are hours.

            :param access_token: A time unit for the value that you set in the ``AccessTokenValidity`` parameter. The default ``AccessTokenValidity`` time unit is ``hours`` . ``AccessTokenValidity`` duration can range from five minutes to one day.
            :param id_token: A time unit for the value that you set in the ``IdTokenValidity`` parameter. The default ``IdTokenValidity`` time unit is ``hours`` . ``IdTokenValidity`` duration can range from five minutes to one day.
            :param refresh_token: A time unit for the value that you set in the ``RefreshTokenValidity`` parameter. The default ``RefreshTokenValidity`` time unit is ``days`` . ``RefreshTokenValidity`` duration can range from 60 minutes to 10 years.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-tokenvalidityunits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                token_validity_units_property = cognito_mixins.CfnUserPoolClientPropsMixin.TokenValidityUnitsProperty(
                    access_token="accessToken",
                    id_token="idToken",
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__30f9e8cbfdc24a7b3fee76419a3cb061a0e1d19a3d9df14651f951cf5308ae0c)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument id_token", value=id_token, expected_type=type_hints["id_token"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if id_token is not None:
                self._values["id_token"] = id_token
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''A time unit for the value that you set in the ``AccessTokenValidity`` parameter.

            The default ``AccessTokenValidity`` time unit is ``hours`` . ``AccessTokenValidity`` duration can range from five minutes to one day.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-tokenvalidityunits.html#cfn-cognito-userpoolclient-tokenvalidityunits-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id_token(self) -> typing.Optional[builtins.str]:
            '''A time unit for the value that you set in the ``IdTokenValidity`` parameter.

            The default ``IdTokenValidity`` time unit is ``hours`` . ``IdTokenValidity`` duration can range from five minutes to one day.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-tokenvalidityunits.html#cfn-cognito-userpoolclient-tokenvalidityunits-idtoken
            '''
            result = self._values.get("id_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''A time unit for the value that you set in the ``RefreshTokenValidity`` parameter.

            The default ``RefreshTokenValidity`` time unit is ``days`` . ``RefreshTokenValidity`` duration can range from 60 minutes to 10 years.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-tokenvalidityunits.html#cfn-cognito-userpoolclient-tokenvalidityunits-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TokenValidityUnitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolDomainMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "custom_domain_config": "customDomainConfig",
        "domain": "domain",
        "managed_login_version": "managedLoginVersion",
        "user_pool_id": "userPoolId",
    },
)
class CfnUserPoolDomainMixinProps:
    def __init__(
        self,
        *,
        custom_domain_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolDomainPropsMixin.CustomDomainConfigTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        domain: typing.Optional[builtins.str] = None,
        managed_login_version: typing.Optional[jsii.Number] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPoolDomainPropsMixin.

        :param custom_domain_config: The configuration for a custom domain that hosts the sign-up and sign-in pages for your application. Use this object to specify an SSL certificate that is managed by ACM. When you create a custom domain, the passkey RP ID defaults to the custom domain. If you had a prefix domain active, this will cause passkey integration for your prefix domain to stop working due to a mismatch in RP ID. To keep the prefix domain passkey integration working, you can explicitly set RP ID to the prefix domain.
        :param domain: The name of the domain that you want to update. For custom domains, this is the fully-qualified domain name, for example ``auth.example.com`` . For prefix domains, this is the prefix alone, such as ``myprefix`` .
        :param managed_login_version: A version number that indicates the state of managed login for your domain. Version ``1`` is hosted UI (classic). Version ``2`` is the newer managed login with the branding editor. For more information, see `Managed login <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html>`_ .
        :param user_pool_id: The ID of the user pool that is associated with the domain you're updating.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            cfn_user_pool_domain_mixin_props = cognito_mixins.CfnUserPoolDomainMixinProps(
                custom_domain_config=cognito_mixins.CfnUserPoolDomainPropsMixin.CustomDomainConfigTypeProperty(
                    certificate_arn="certificateArn"
                ),
                domain="domain",
                managed_login_version=123,
                user_pool_id="userPoolId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e66606d15225fd4d37f6f40ef6a7ae86addd65389adadcac33c7941641856e)
            check_type(argname="argument custom_domain_config", value=custom_domain_config, expected_type=type_hints["custom_domain_config"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument managed_login_version", value=managed_login_version, expected_type=type_hints["managed_login_version"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_domain_config is not None:
            self._values["custom_domain_config"] = custom_domain_config
        if domain is not None:
            self._values["domain"] = domain
        if managed_login_version is not None:
            self._values["managed_login_version"] = managed_login_version
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id

    @builtins.property
    def custom_domain_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolDomainPropsMixin.CustomDomainConfigTypeProperty"]]:
        '''The configuration for a custom domain that hosts the sign-up and sign-in pages for your application.

        Use this object to specify an SSL certificate that is managed by ACM.

        When you create a custom domain, the passkey RP ID defaults to the custom domain. If you had a prefix domain active, this will cause passkey integration for your prefix domain to stop working due to a mismatch in RP ID. To keep the prefix domain passkey integration working, you can explicitly set RP ID to the prefix domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-customdomainconfig
        '''
        result = self._values.get("custom_domain_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolDomainPropsMixin.CustomDomainConfigTypeProperty"]], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The name of the domain that you want to update.

        For custom domains, this is the fully-qualified domain name, for example ``auth.example.com`` . For prefix domains, this is the prefix alone, such as ``myprefix`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_login_version(self) -> typing.Optional[jsii.Number]:
        '''A version number that indicates the state of managed login for your domain.

        Version ``1`` is hosted UI (classic). Version ``2`` is the newer managed login with the branding editor. For more information, see `Managed login <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-managedloginversion
        '''
        result = self._values.get("managed_login_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user pool that is associated with the domain you're updating.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolDomainMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolDomainPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolDomainPropsMixin",
):
    '''The AWS::Cognito::UserPoolDomain resource creates a new domain for a user pool.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html
    :cloudformationResource: AWS::Cognito::UserPoolDomain
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_user_pool_domain_props_mixin = cognito_mixins.CfnUserPoolDomainPropsMixin(cognito_mixins.CfnUserPoolDomainMixinProps(
            custom_domain_config=cognito_mixins.CfnUserPoolDomainPropsMixin.CustomDomainConfigTypeProperty(
                certificate_arn="certificateArn"
            ),
            domain="domain",
            managed_login_version=123,
            user_pool_id="userPoolId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPoolDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::UserPoolDomain``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358f34659721db949b690457fcdd4f91bace3b0a360abdbe9fbeef71153097a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2e22b6171f38af8b33ceb1119a0e59768dc766baa9511f6799d456ebb7d9730)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68be555aa86942219471838a71fa05968a43e212ff693c6c8a07df542b200a4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPoolDomainMixinProps:
        return typing.cast(CfnUserPoolDomainMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolDomainPropsMixin.CustomDomainConfigTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class CustomDomainConfigTypeProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for a hosted UI custom domain.

            :param certificate_arn: The Amazon Resource Name (ARN) of an Certificate Manager SSL certificate. You use this certificate for the subdomain of your custom domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooldomain-customdomainconfigtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                custom_domain_config_type_property = cognito_mixins.CfnUserPoolDomainPropsMixin.CustomDomainConfigTypeProperty(
                    certificate_arn="certificateArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b64ddacc1502f003abdad85c8c1c2007177671b73ee3b1f2cd2cd6ea2a3a9076)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an Certificate Manager SSL certificate.

            You use this certificate for the subdomain of your custom domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooldomain-customdomainconfigtype.html#cfn-cognito-userpooldomain-customdomainconfigtype-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomDomainConfigTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "group_name": "groupName",
        "precedence": "precedence",
        "role_arn": "roleArn",
        "user_pool_id": "userPoolId",
    },
)
class CfnUserPoolGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        group_name: typing.Optional[builtins.str] = None,
        precedence: typing.Optional[jsii.Number] = None,
        role_arn: typing.Optional[builtins.str] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPoolGroupPropsMixin.

        :param description: A description of the group that you're creating.
        :param group_name: A name for the group. This name must be unique in your user pool.
        :param precedence: A non-negative integer value that specifies the precedence of this group relative to the other groups that a user can belong to in the user pool. Zero is the highest precedence value. Groups with lower ``Precedence`` values take precedence over groups with higher or null ``Precedence`` values. If a user belongs to two or more groups, it is the group with the lowest precedence value whose role ARN is given in the user's tokens for the ``cognito:roles`` and ``cognito:preferred_role`` claims. Two groups can have the same ``Precedence`` value. If this happens, neither group takes precedence over the other. If two groups with the same ``Precedence`` have the same role ARN, that role is used in the ``cognito:preferred_role`` claim in tokens for users in each group. If the two groups have different role ARNs, the ``cognito:preferred_role`` claim isn't set in users' tokens. The default ``Precedence`` value is null. The maximum ``Precedence`` value is ``2^31-1`` .
        :param role_arn: The Amazon Resource Name (ARN) for the IAM role that you want to associate with the group. A group role primarily declares a preferred role for the credentials that you get from an identity pool. Amazon Cognito ID tokens have a ``cognito:preferred_role`` claim that presents the highest-precedence group that a user belongs to. Both ID and access tokens also contain a ``cognito:groups`` claim that list all the groups that a user is a member of.
        :param user_pool_id: The ID of the user pool where you want to create a user group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            cfn_user_pool_group_mixin_props = cognito_mixins.CfnUserPoolGroupMixinProps(
                description="description",
                group_name="groupName",
                precedence=123,
                role_arn="roleArn",
                user_pool_id="userPoolId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df84da68a329c74e004f6e48b071c91c4ba6b3147e626ea71f52a50db1558c90)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument precedence", value=precedence, expected_type=type_hints["precedence"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if group_name is not None:
            self._values["group_name"] = group_name
        if precedence is not None:
            self._values["precedence"] = precedence
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the group that you're creating.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''A name for the group.

        This name must be unique in your user pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def precedence(self) -> typing.Optional[jsii.Number]:
        '''A non-negative integer value that specifies the precedence of this group relative to the other groups that a user can belong to in the user pool.

        Zero is the highest precedence value. Groups with lower ``Precedence`` values take precedence over groups with higher or null ``Precedence`` values. If a user belongs to two or more groups, it is the group with the lowest precedence value whose role ARN is given in the user's tokens for the ``cognito:roles`` and ``cognito:preferred_role`` claims.

        Two groups can have the same ``Precedence`` value. If this happens, neither group takes precedence over the other. If two groups with the same ``Precedence`` have the same role ARN, that role is used in the ``cognito:preferred_role`` claim in tokens for users in each group. If the two groups have different role ARNs, the ``cognito:preferred_role`` claim isn't set in users' tokens.

        The default ``Precedence`` value is null. The maximum ``Precedence`` value is ``2^31-1`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-precedence
        '''
        result = self._values.get("precedence")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the IAM role that you want to associate with the group.

        A group role primarily declares a preferred role for the credentials that you get from an identity pool. Amazon Cognito ID tokens have a ``cognito:preferred_role`` claim that presents the highest-precedence group that a user belongs to. Both ID and access tokens also contain a ``cognito:groups`` claim that list all the groups that a user is a member of.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user pool where you want to create a user group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolGroupPropsMixin",
):
    '''A user pool group.

    Contains details about the group and the way that it contributes to IAM role decisions with identity pools. Identity pools can make decisions about the IAM role to assign based on groups: users get credentials for the role associated with their highest-priority group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html
    :cloudformationResource: AWS::Cognito::UserPoolGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_user_pool_group_props_mixin = cognito_mixins.CfnUserPoolGroupPropsMixin(cognito_mixins.CfnUserPoolGroupMixinProps(
            description="description",
            group_name="groupName",
            precedence=123,
            role_arn="roleArn",
            user_pool_id="userPoolId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPoolGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::UserPoolGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b54f7d09a2ab1419a594e60ffc241db1b7a4025cd7d4db53bcf498b89f6c0c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdec3efe2e32098d40027daa512a05c00f59e2d11d01062dff34e479706e2ea9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c987314f58dc906b6e86ee12863fd1b779702be2f1d78d1f4205a9135d734b5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPoolGroupMixinProps:
        return typing.cast(CfnUserPoolGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolIdentityProviderMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_mapping": "attributeMapping",
        "idp_identifiers": "idpIdentifiers",
        "provider_details": "providerDetails",
        "provider_name": "providerName",
        "provider_type": "providerType",
        "user_pool_id": "userPoolId",
    },
)
class CfnUserPoolIdentityProviderMixinProps:
    def __init__(
        self,
        *,
        attribute_mapping: typing.Any = None,
        idp_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        provider_details: typing.Any = None,
        provider_name: typing.Optional[builtins.str] = None,
        provider_type: typing.Optional[builtins.str] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPoolIdentityProviderPropsMixin.

        :param attribute_mapping: A mapping of IdP attributes to standard and custom user pool attributes. Specify a user pool attribute as the key of the key-value pair, and the IdP attribute claim name as the value.
        :param idp_identifiers: An array of IdP identifiers, for example ``"IdPIdentifiers": [ "MyIdP", "MyIdP2" ]`` . Identifiers are friendly names that you can pass in the ``idp_identifier`` query parameter of requests to the `Authorize endpoint <https://docs.aws.amazon.com/cognito/latest/developerguide/authorization-endpoint.html>`_ to silently redirect to sign-in with the associated IdP. Identifiers in a domain format also enable the use of `email-address matching with SAML providers <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managing-saml-idp-naming.html>`_ .
        :param provider_details: The scopes, URLs, and identifiers for your external identity provider. The following examples describe the provider detail keys for each IdP type. These values and their schema are subject to change. Social IdP ``authorize_scopes`` values must match the values listed here. - **OpenID Connect (OIDC)** - Amazon Cognito accepts the following elements when it can't discover endpoint URLs from ``oidc_issuer`` : ``attributes_url`` , ``authorize_url`` , ``jwks_uri`` , ``token_url`` . Create or update request: ``"ProviderDetails": { "attributes_request_method": "GET", "attributes_url": "https://auth.example.com/userInfo", "authorize_scopes": "openid profile email", "authorize_url": "https://auth.example.com/authorize", "client_id": "1example23456789", "client_secret": "provider-app-client-secret", "jwks_uri": "https://auth.example.com/.well-known/jwks.json", "oidc_issuer": "https://auth.example.com", "token_url": "https://example.com/token" }`` Describe response: ``"ProviderDetails": { "attributes_request_method": "GET", "attributes_url": "https://auth.example.com/userInfo", "attributes_url_add_attributes": "false", "authorize_scopes": "openid profile email", "authorize_url": "https://auth.example.com/authorize", "client_id": "1example23456789", "client_secret": "provider-app-client-secret", "jwks_uri": "https://auth.example.com/.well-known/jwks.json", "oidc_issuer": "https://auth.example.com", "token_url": "https://example.com/token" }`` - **SAML** - Create or update request with Metadata URL: ``"ProviderDetails": { "IDPInit": "true", "IDPSignout": "true", "EncryptedResponses" : "true", "MetadataURL": "https://auth.example.com/sso/saml/metadata", "RequestSigningAlgorithm": "rsa-sha256" }`` Create or update request with Metadata file: ``"ProviderDetails": { "IDPInit": "true", "IDPSignout": "true", "EncryptedResponses" : "true", "MetadataFile": "[metadata XML]", "RequestSigningAlgorithm": "rsa-sha256" }`` The value of ``MetadataFile`` must be the plaintext metadata document with all quote (") characters escaped by backslashes. Describe response: ``"ProviderDetails": { "IDPInit": "true", "IDPSignout": "true", "EncryptedResponses" : "true", "ActiveEncryptionCertificate": "[certificate]", "MetadataURL": "https://auth.example.com/sso/saml/metadata", "RequestSigningAlgorithm": "rsa-sha256", "SLORedirectBindingURI": "https://auth.example.com/slo/saml", "SSORedirectBindingURI": "https://auth.example.com/sso/saml" }`` - **LoginWithAmazon** - Create or update request: ``"ProviderDetails": { "authorize_scopes": "profile postal_code", "client_id": "amzn1.application-oa2-client.1example23456789", "client_secret": "provider-app-client-secret"`` Describe response: ``"ProviderDetails": { "attributes_url": "https://api.amazon.com/user/profile", "attributes_url_add_attributes": "false", "authorize_scopes": "profile postal_code", "authorize_url": "https://www.amazon.com/ap/oa", "client_id": "amzn1.application-oa2-client.1example23456789", "client_secret": "provider-app-client-secret", "token_request_method": "POST", "token_url": "https://api.amazon.com/auth/o2/token" }`` - **Google** - Create or update request: ``"ProviderDetails": { "authorize_scopes": "email profile openid", "client_id": "1example23456789.apps.googleusercontent.com", "client_secret": "provider-app-client-secret" }`` Describe response: ``"ProviderDetails": { "attributes_url": "https://people.googleapis.com/v1/people/me?personFields=", "attributes_url_add_attributes": "true", "authorize_scopes": "email profile openid", "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth", "client_id": "1example23456789.apps.googleusercontent.com", "client_secret": "provider-app-client-secret", "oidc_issuer": "https://accounts.google.com", "token_request_method": "POST", "token_url": "https://www.googleapis.com/oauth2/v4/token" }`` - **SignInWithApple** - Create or update request: ``"ProviderDetails": { "authorize_scopes": "email name", "client_id": "com.example.cognito", "private_key": "1EXAMPLE", "key_id": "2EXAMPLE", "team_id": "3EXAMPLE" }`` Describe response: ``"ProviderDetails": { "attributes_url_add_attributes": "false", "authorize_scopes": "email name", "authorize_url": "https://appleid.apple.com/auth/authorize", "client_id": "com.example.cognito", "key_id": "1EXAMPLE", "oidc_issuer": "https://appleid.apple.com", "team_id": "2EXAMPLE", "token_request_method": "POST", "token_url": "https://appleid.apple.com/auth/token" }`` - **Facebook** - Create or update request: ``"ProviderDetails": { "api_version": "v17.0", "authorize_scopes": "public_profile, email", "client_id": "1example23456789", "client_secret": "provider-app-client-secret" }`` Describe response: ``"ProviderDetails": { "api_version": "v17.0", "attributes_url": "https://graph.facebook.com/v17.0/me?fields=", "attributes_url_add_attributes": "true", "authorize_scopes": "public_profile, email", "authorize_url": "https://www.facebook.com/v17.0/dialog/oauth", "client_id": "1example23456789", "client_secret": "provider-app-client-secret", "token_request_method": "GET", "token_url": "https://graph.facebook.com/v17.0/oauth/access_token" }``
        :param provider_name: The name that you want to assign to the IdP. You can pass the identity provider name in the ``identity_provider`` query parameter of requests to the `Authorize endpoint <https://docs.aws.amazon.com/cognito/latest/developerguide/authorization-endpoint.html>`_ to silently redirect to sign-in with the associated IdP.
        :param provider_type: The type of IdP that you want to add. Amazon Cognito supports OIDC, SAML 2.0, Login With Amazon, Sign In With Apple, Google, and Facebook IdPs.
        :param user_pool_id: The Id of the user pool where you want to create an IdP.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            # attribute_mapping: Any
            # provider_details: Any
            
            cfn_user_pool_identity_provider_mixin_props = cognito_mixins.CfnUserPoolIdentityProviderMixinProps(
                attribute_mapping=attribute_mapping,
                idp_identifiers=["idpIdentifiers"],
                provider_details=provider_details,
                provider_name="providerName",
                provider_type="providerType",
                user_pool_id="userPoolId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad95163e1e5fe169b249166175ef3afbd380dbb9c879b749aab9243d262d69e)
            check_type(argname="argument attribute_mapping", value=attribute_mapping, expected_type=type_hints["attribute_mapping"])
            check_type(argname="argument idp_identifiers", value=idp_identifiers, expected_type=type_hints["idp_identifiers"])
            check_type(argname="argument provider_details", value=provider_details, expected_type=type_hints["provider_details"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_mapping is not None:
            self._values["attribute_mapping"] = attribute_mapping
        if idp_identifiers is not None:
            self._values["idp_identifiers"] = idp_identifiers
        if provider_details is not None:
            self._values["provider_details"] = provider_details
        if provider_name is not None:
            self._values["provider_name"] = provider_name
        if provider_type is not None:
            self._values["provider_type"] = provider_type
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id

    @builtins.property
    def attribute_mapping(self) -> typing.Any:
        '''A mapping of IdP attributes to standard and custom user pool attributes.

        Specify a user pool attribute as the key of the key-value pair, and the IdP attribute claim name as the value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-attributemapping
        '''
        result = self._values.get("attribute_mapping")
        return typing.cast(typing.Any, result)

    @builtins.property
    def idp_identifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of IdP identifiers, for example ``"IdPIdentifiers": [ "MyIdP", "MyIdP2" ]`` .

        Identifiers are friendly names that you can pass in the ``idp_identifier`` query parameter of requests to the `Authorize endpoint <https://docs.aws.amazon.com/cognito/latest/developerguide/authorization-endpoint.html>`_ to silently redirect to sign-in with the associated IdP. Identifiers in a domain format also enable the use of `email-address matching with SAML providers <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managing-saml-idp-naming.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-idpidentifiers
        '''
        result = self._values.get("idp_identifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def provider_details(self) -> typing.Any:
        '''The scopes, URLs, and identifiers for your external identity provider.

        The following
        examples describe the provider detail keys for each IdP type. These values and their
        schema are subject to change. Social IdP ``authorize_scopes`` values must match
        the values listed here.

        - **OpenID Connect (OIDC)** - Amazon Cognito accepts the following elements when it can't discover endpoint URLs from ``oidc_issuer`` : ``attributes_url`` , ``authorize_url`` , ``jwks_uri`` , ``token_url`` .

        Create or update request: ``"ProviderDetails": { "attributes_request_method": "GET", "attributes_url": "https://auth.example.com/userInfo", "authorize_scopes": "openid profile email", "authorize_url": "https://auth.example.com/authorize", "client_id": "1example23456789", "client_secret": "provider-app-client-secret", "jwks_uri": "https://auth.example.com/.well-known/jwks.json", "oidc_issuer": "https://auth.example.com", "token_url": "https://example.com/token" }``

        Describe response: ``"ProviderDetails": { "attributes_request_method": "GET", "attributes_url": "https://auth.example.com/userInfo", "attributes_url_add_attributes": "false", "authorize_scopes": "openid profile email", "authorize_url": "https://auth.example.com/authorize", "client_id": "1example23456789", "client_secret": "provider-app-client-secret", "jwks_uri": "https://auth.example.com/.well-known/jwks.json", "oidc_issuer": "https://auth.example.com", "token_url": "https://example.com/token" }``

        - **SAML** - Create or update request with Metadata URL: ``"ProviderDetails": { "IDPInit": "true", "IDPSignout": "true", "EncryptedResponses" : "true", "MetadataURL": "https://auth.example.com/sso/saml/metadata", "RequestSigningAlgorithm": "rsa-sha256" }``

        Create or update request with Metadata file: ``"ProviderDetails": { "IDPInit": "true", "IDPSignout": "true", "EncryptedResponses" : "true", "MetadataFile": "[metadata XML]", "RequestSigningAlgorithm": "rsa-sha256" }``

        The value of ``MetadataFile`` must be the plaintext metadata document with all quote (") characters escaped by backslashes.

        Describe response: ``"ProviderDetails": { "IDPInit": "true", "IDPSignout": "true", "EncryptedResponses" : "true", "ActiveEncryptionCertificate": "[certificate]", "MetadataURL": "https://auth.example.com/sso/saml/metadata", "RequestSigningAlgorithm": "rsa-sha256", "SLORedirectBindingURI": "https://auth.example.com/slo/saml", "SSORedirectBindingURI": "https://auth.example.com/sso/saml" }``

        - **LoginWithAmazon** - Create or update request: ``"ProviderDetails": { "authorize_scopes": "profile postal_code", "client_id": "amzn1.application-oa2-client.1example23456789", "client_secret": "provider-app-client-secret"``

        Describe response: ``"ProviderDetails": { "attributes_url": "https://api.amazon.com/user/profile", "attributes_url_add_attributes": "false", "authorize_scopes": "profile postal_code", "authorize_url": "https://www.amazon.com/ap/oa", "client_id": "amzn1.application-oa2-client.1example23456789", "client_secret": "provider-app-client-secret", "token_request_method": "POST", "token_url": "https://api.amazon.com/auth/o2/token" }``

        - **Google** - Create or update request: ``"ProviderDetails": { "authorize_scopes": "email profile openid", "client_id": "1example23456789.apps.googleusercontent.com", "client_secret": "provider-app-client-secret" }``

        Describe response: ``"ProviderDetails": { "attributes_url": "https://people.googleapis.com/v1/people/me?personFields=", "attributes_url_add_attributes": "true", "authorize_scopes": "email profile openid", "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth", "client_id": "1example23456789.apps.googleusercontent.com", "client_secret": "provider-app-client-secret", "oidc_issuer": "https://accounts.google.com", "token_request_method": "POST", "token_url": "https://www.googleapis.com/oauth2/v4/token" }``

        - **SignInWithApple** - Create or update request: ``"ProviderDetails": { "authorize_scopes": "email name", "client_id": "com.example.cognito", "private_key": "1EXAMPLE", "key_id": "2EXAMPLE", "team_id": "3EXAMPLE" }``

        Describe response: ``"ProviderDetails": { "attributes_url_add_attributes": "false", "authorize_scopes": "email name", "authorize_url": "https://appleid.apple.com/auth/authorize", "client_id": "com.example.cognito", "key_id": "1EXAMPLE", "oidc_issuer": "https://appleid.apple.com", "team_id": "2EXAMPLE", "token_request_method": "POST", "token_url": "https://appleid.apple.com/auth/token" }``

        - **Facebook** - Create or update request: ``"ProviderDetails": { "api_version": "v17.0", "authorize_scopes": "public_profile, email", "client_id": "1example23456789", "client_secret": "provider-app-client-secret" }``

        Describe response: ``"ProviderDetails": { "api_version": "v17.0", "attributes_url": "https://graph.facebook.com/v17.0/me?fields=", "attributes_url_add_attributes": "true", "authorize_scopes": "public_profile, email", "authorize_url": "https://www.facebook.com/v17.0/dialog/oauth", "client_id": "1example23456789", "client_secret": "provider-app-client-secret", "token_request_method": "GET", "token_url": "https://graph.facebook.com/v17.0/oauth/access_token" }``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providerdetails
        '''
        result = self._values.get("provider_details")
        return typing.cast(typing.Any, result)

    @builtins.property
    def provider_name(self) -> typing.Optional[builtins.str]:
        '''The name that you want to assign to the IdP.

        You can pass the identity provider name in the ``identity_provider`` query parameter of requests to the `Authorize endpoint <https://docs.aws.amazon.com/cognito/latest/developerguide/authorization-endpoint.html>`_ to silently redirect to sign-in with the associated IdP.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providername
        '''
        result = self._values.get("provider_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_type(self) -> typing.Optional[builtins.str]:
        '''The type of IdP that you want to add.

        Amazon Cognito supports OIDC, SAML 2.0, Login With Amazon, Sign In With Apple, Google, and Facebook IdPs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providertype
        '''
        result = self._values.get("provider_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The Id of the user pool where you want to create an IdP.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolIdentityProviderMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolIdentityProviderPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolIdentityProviderPropsMixin",
):
    '''The ``AWS::Cognito::UserPoolIdentityProvider`` resource creates an identity provider for a user pool.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html
    :cloudformationResource: AWS::Cognito::UserPoolIdentityProvider
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        # attribute_mapping: Any
        # provider_details: Any
        
        cfn_user_pool_identity_provider_props_mixin = cognito_mixins.CfnUserPoolIdentityProviderPropsMixin(cognito_mixins.CfnUserPoolIdentityProviderMixinProps(
            attribute_mapping=attribute_mapping,
            idp_identifiers=["idpIdentifiers"],
            provider_details=provider_details,
            provider_name="providerName",
            provider_type="providerType",
            user_pool_id="userPoolId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPoolIdentityProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::UserPoolIdentityProvider``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee8f564c09c0f730f44abae0eb4b415ffc4129ab4dbb0b5cd455edffd408b02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f288797fd7e05b3471c17a0de30dd3ffa1dcc891fcfbf02cf574e8fb9f46dc3a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e35daa5ca12236e2cd7bf12d369f5b4692f04eedfa1d6e7f2329bc094a5503c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPoolIdentityProviderMixinProps:
        return typing.cast(CfnUserPoolIdentityProviderMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolLogsMixin",
):
    '''The ``AWS::Cognito::UserPool`` resource creates an Amazon Cognito user pool.

    For more information on working with Amazon Cognito user pools, see `Amazon Cognito User Pools <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html>`_ and `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`_ .
    .. epigraph::

       If you don't specify a value for a parameter, Amazon Cognito sets it to a default value.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html
    :cloudformationResource: AWS::Cognito::UserPool
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_user_pool_logs_mixin = cognito_mixins.CfnUserPoolLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::Cognito::UserPool``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1fb4dc936c2a21510ac01fd7735b0c69e8eee810ebf0ac9f27186cc0b9cfed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82ae5f776c379223f34a1e1c04661d4c79c53a2167b542fd232aeea78662a380)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71756f1b68c5e7898a7f60f96d7b0875296ce17a423aa9053941555354131f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPLICATION_LOGS")
    def APPLICATION_LOGS(cls) -> CfnUserPoolApplicationLogs:
        return typing.cast(CfnUserPoolApplicationLogs, jsii.sget(cls, "APPLICATION_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_recovery_setting": "accountRecoverySetting",
        "admin_create_user_config": "adminCreateUserConfig",
        "alias_attributes": "aliasAttributes",
        "auto_verified_attributes": "autoVerifiedAttributes",
        "deletion_protection": "deletionProtection",
        "device_configuration": "deviceConfiguration",
        "email_authentication_message": "emailAuthenticationMessage",
        "email_authentication_subject": "emailAuthenticationSubject",
        "email_configuration": "emailConfiguration",
        "email_verification_message": "emailVerificationMessage",
        "email_verification_subject": "emailVerificationSubject",
        "enabled_mfas": "enabledMfas",
        "lambda_config": "lambdaConfig",
        "mfa_configuration": "mfaConfiguration",
        "policies": "policies",
        "schema": "schema",
        "sms_authentication_message": "smsAuthenticationMessage",
        "sms_configuration": "smsConfiguration",
        "sms_verification_message": "smsVerificationMessage",
        "user_attribute_update_settings": "userAttributeUpdateSettings",
        "username_attributes": "usernameAttributes",
        "username_configuration": "usernameConfiguration",
        "user_pool_add_ons": "userPoolAddOns",
        "user_pool_name": "userPoolName",
        "user_pool_tags": "userPoolTags",
        "user_pool_tier": "userPoolTier",
        "verification_message_template": "verificationMessageTemplate",
        "web_authn_relying_party_id": "webAuthnRelyingPartyId",
        "web_authn_user_verification": "webAuthnUserVerification",
    },
)
class CfnUserPoolMixinProps:
    def __init__(
        self,
        *,
        account_recovery_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.AccountRecoverySettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        admin_create_user_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.AdminCreateUserConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        alias_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_verified_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[builtins.str] = None,
        device_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.DeviceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        email_authentication_message: typing.Optional[builtins.str] = None,
        email_authentication_subject: typing.Optional[builtins.str] = None,
        email_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.EmailConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        email_verification_message: typing.Optional[builtins.str] = None,
        email_verification_subject: typing.Optional[builtins.str] = None,
        enabled_mfas: typing.Optional[typing.Sequence[builtins.str]] = None,
        lambda_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.LambdaConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        mfa_configuration: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.PoliciesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.SchemaAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        sms_authentication_message: typing.Optional[builtins.str] = None,
        sms_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.SmsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sms_verification_message: typing.Optional[builtins.str] = None,
        user_attribute_update_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.UserAttributeUpdateSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        username_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        username_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.UsernameConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        user_pool_add_ons: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.UserPoolAddOnsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        user_pool_name: typing.Optional[builtins.str] = None,
        user_pool_tags: typing.Any = None,
        user_pool_tier: typing.Optional[builtins.str] = None,
        verification_message_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.VerificationMessageTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        web_authn_relying_party_id: typing.Optional[builtins.str] = None,
        web_authn_user_verification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPoolPropsMixin.

        :param account_recovery_setting: The available verified method a user can use to recover their password when they call ``ForgotPassword`` . You can use this setting to define a preferred method when a user has more than one method available. With this setting, SMS doesn't qualify for a valid password recovery mechanism if the user also has SMS multi-factor authentication (MFA) activated. In the absence of this setting, Amazon Cognito uses the legacy behavior to determine the recovery method where SMS is preferred through email.
        :param admin_create_user_config: The settings for administrator creation of users in a user pool. Contains settings for allowing user sign-up, customizing invitation messages to new users, and the amount of time before temporary passwords expire.
        :param alias_attributes: Attributes supported as an alias for this user pool. For more information about alias attributes, see `Customizing sign-in attributes <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases>`_ .
        :param auto_verified_attributes: The attributes that you want your user pool to automatically verify. For more information, see `Verifying contact information at sign-up <https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html#allowing-users-to-sign-up-and-confirm-themselves>`_ .
        :param deletion_protection: When active, ``DeletionProtection`` prevents accidental deletion of your user pool. Before you can delete a user pool that you have protected against deletion, you must deactivate this feature. When you try to delete a protected user pool in a ``DeleteUserPool`` API request, Amazon Cognito returns an ``InvalidParameterException`` error. To delete a protected user pool, send a new ``DeleteUserPool`` request after you deactivate deletion protection in an ``UpdateUserPool`` API request.
        :param device_configuration: The device-remembering configuration for a user pool. Device remembering or device tracking is a "Remember me on this device" option for user pools that perform authentication with the device key of a trusted device in the back end, instead of a user-provided MFA code. For more information about device authentication, see `Working with user devices in your user pool <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`_ . A null value indicates that you have deactivated device remembering in your user pool. .. epigraph:: When you provide a value for any ``DeviceConfiguration`` field, you activate the Amazon Cognito device-remembering feature. For more information, see `Working with devices <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`_ .
        :param email_authentication_message: 
        :param email_authentication_subject: 
        :param email_configuration: The email configuration of your user pool. The email configuration type sets your preferred sending method, AWS Region, and sender for messages from your user pool.
        :param email_verification_message: This parameter is no longer used. See `VerificationMessageTemplateType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html>`_ .
        :param email_verification_subject: This parameter is no longer used. See `VerificationMessageTemplateType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html>`_ .
        :param enabled_mfas: Set enabled MFA options on a specified user pool. To disable all MFAs after it has been enabled, set ``MfaConfiguration`` to ``OFF`` and remove EnabledMfas. MFAs can only be all disabled if ``MfaConfiguration`` is ``OFF`` . After you enable ``SMS_MFA`` , you can only disable it by setting ``MfaConfiguration`` to ``OFF`` . Can be one of the following values: - ``SMS_MFA`` - Enables MFA with SMS for the user pool. To select this option, you must also provide values for ``SmsConfiguration`` . - ``SOFTWARE_TOKEN_MFA`` - Enables software token MFA for the user pool. - ``EMAIL_OTP`` - Enables MFA with email for the user pool. To select this option, you must provide values for ``EmailConfiguration`` and within those, set ``EmailSendingAccount`` to ``DEVELOPER`` . Allowed values: ``SMS_MFA`` | ``SOFTWARE_TOKEN_MFA`` | ``EMAIL_OTP``
        :param lambda_config: A collection of user pool Lambda triggers. Amazon Cognito invokes triggers at several possible stages of authentication operations. Triggers can modify the outcome of the operations that invoked them.
        :param mfa_configuration: Displays the state of multi-factor authentication (MFA) as on, off, or optional. When ``ON`` , all users must set up MFA before they can sign in. When ``OPTIONAL`` , your application must make a client-side determination of whether a user wants to register an MFA device. For user pools with adaptive authentication with threat protection, choose ``OPTIONAL`` . When ``MfaConfiguration`` is ``OPTIONAL`` , managed login doesn't automatically prompt users to set up MFA. Amazon Cognito generates MFA prompts in API responses and in managed login for users who have chosen and configured a preferred MFA factor.
        :param policies: A list of user pool policies. Contains the policy that sets password-complexity requirements.
        :param schema: An array of attributes for the new user pool. You can add custom attributes and modify the properties of default attributes. The specifications in this parameter set the required attributes in your user pool. For more information, see `Working with user attributes <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html>`_ .
        :param sms_authentication_message: The contents of the SMS authentication message.
        :param sms_configuration: The settings for your Amazon Cognito user pool to send SMS messages with Amazon Simple Notification Service. To send SMS messages with Amazon SNS in the AWS Region that you want, the Amazon Cognito user pool uses an AWS Identity and Access Management (IAM) role in your AWS account . For more information see `SMS message settings <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`_ .
        :param sms_verification_message: This parameter is no longer used. See `VerificationMessageTemplateType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html>`_ .
        :param user_attribute_update_settings: The settings for updates to user attributes. These settings include the property ``AttributesRequireVerificationBeforeUpdate`` , a user-pool setting that tells Amazon Cognito how to handle changes to the value of your users' email address and phone number attributes. For more information, see `Verifying updates to email addresses and phone numbers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-email-phone-verification.html#user-pool-settings-verifications-verify-attribute-updates>`_ .
        :param username_attributes: Specifies whether a user can use an email address or phone number as a username when they sign up.
        :param username_configuration: Sets the case sensitivity option for sign-in usernames. When ``CaseSensitive`` is ``false`` (case insensitive), users can sign in with any combination of capital and lowercase letters. For example, ``username`` , ``USERNAME`` , or ``UserName`` , or for email, ``email@example.com`` or ``EMaiL@eXamplE.Com`` . For most use cases, set case sensitivity to ``false`` as a best practice. When usernames and email addresses are case insensitive, Amazon Cognito treats any variation in case as the same user, and prevents a case variation from being assigned to the same attribute for a different user. When ``CaseSensitive`` is ``true`` (case sensitive), Amazon Cognito interprets ``USERNAME`` and ``UserName`` as distinct users. This configuration is immutable after you set it.
        :param user_pool_add_ons: Contains settings for activation of threat protection, including the operating mode and additional authentication types. To log user security information but take no action, set to ``AUDIT`` . To configure automatic security responses to potentially unwanted traffic to your user pool, set to ``ENFORCED`` . For more information, see `Adding advanced security to a user pool <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-advanced-security.html>`_ . To activate this setting, your user pool must be on the `Plus tier <https://docs.aws.amazon.com/cognito/latest/developerguide/feature-plans-features-plus.html>`_ .
        :param user_pool_name: A friendly name for your user pool.
        :param user_pool_tags: The tag keys and values to assign to the user pool. A tag is a label that you can use to categorize and manage user pools in different ways, such as by purpose, owner, environment, or other criteria.
        :param user_pool_tier: The user pool `feature plan <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sign-in-feature-plans.html>`_ , or tier. This parameter determines the eligibility of the user pool for features like managed login, access-token customization, and threat protection. Defaults to ``ESSENTIALS`` .
        :param verification_message_template: The template for the verification message that your user pool delivers to users who set an email address or phone number attribute. Set the email message type that corresponds to your ``DefaultEmailOption`` selection. For ``CONFIRM_WITH_LINK`` , specify an ``EmailMessageByLink`` and leave ``EmailMessage`` blank. For ``CONFIRM_WITH_CODE`` , specify an ``EmailMessage`` and leave ``EmailMessageByLink`` blank. When you supply both parameters with either choice, Amazon Cognito returns an error.
        :param web_authn_relying_party_id: Sets or displays the authentication domain, typically your user pool domain, that passkey providers must use as a relying party (RP) in their configuration. Under the following conditions, the passkey relying party ID must be the fully-qualified domain name of your custom domain: - The user pool is configured for passkey authentication. - The user pool has a custom domain, whether or not it also has a prefix domain. - Your application performs authentication with managed login or the classic hosted UI.
        :param web_authn_user_verification: When ``required`` , users can only register and sign in users with passkeys that are capable of `user verification <https://docs.aws.amazon.com/https://www.w3.org/TR/webauthn-2/#enum-userVerificationRequirement>`_ . When ``preferred`` , your user pool doesn't require the use of authenticators with user verification but encourages it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            # user_pool_tags: Any
            
            cfn_user_pool_mixin_props = cognito_mixins.CfnUserPoolMixinProps(
                account_recovery_setting=cognito_mixins.CfnUserPoolPropsMixin.AccountRecoverySettingProperty(
                    recovery_mechanisms=[cognito_mixins.CfnUserPoolPropsMixin.RecoveryOptionProperty(
                        name="name",
                        priority=123
                    )]
                ),
                admin_create_user_config=cognito_mixins.CfnUserPoolPropsMixin.AdminCreateUserConfigProperty(
                    allow_admin_create_user_only=False,
                    invite_message_template=cognito_mixins.CfnUserPoolPropsMixin.InviteMessageTemplateProperty(
                        email_message="emailMessage",
                        email_subject="emailSubject",
                        sms_message="smsMessage"
                    ),
                    unused_account_validity_days=123
                ),
                alias_attributes=["aliasAttributes"],
                auto_verified_attributes=["autoVerifiedAttributes"],
                deletion_protection="deletionProtection",
                device_configuration=cognito_mixins.CfnUserPoolPropsMixin.DeviceConfigurationProperty(
                    challenge_required_on_new_device=False,
                    device_only_remembered_on_user_prompt=False
                ),
                email_authentication_message="emailAuthenticationMessage",
                email_authentication_subject="emailAuthenticationSubject",
                email_configuration=cognito_mixins.CfnUserPoolPropsMixin.EmailConfigurationProperty(
                    configuration_set="configurationSet",
                    email_sending_account="emailSendingAccount",
                    from="from",
                    reply_to_email_address="replyToEmailAddress",
                    source_arn="sourceArn"
                ),
                email_verification_message="emailVerificationMessage",
                email_verification_subject="emailVerificationSubject",
                enabled_mfas=["enabledMfas"],
                lambda_config=cognito_mixins.CfnUserPoolPropsMixin.LambdaConfigProperty(
                    create_auth_challenge="createAuthChallenge",
                    custom_email_sender=cognito_mixins.CfnUserPoolPropsMixin.CustomEmailSenderProperty(
                        lambda_arn="lambdaArn",
                        lambda_version="lambdaVersion"
                    ),
                    custom_message="customMessage",
                    custom_sms_sender=cognito_mixins.CfnUserPoolPropsMixin.CustomSMSSenderProperty(
                        lambda_arn="lambdaArn",
                        lambda_version="lambdaVersion"
                    ),
                    define_auth_challenge="defineAuthChallenge",
                    kms_key_id="kmsKeyId",
                    post_authentication="postAuthentication",
                    post_confirmation="postConfirmation",
                    pre_authentication="preAuthentication",
                    pre_sign_up="preSignUp",
                    pre_token_generation="preTokenGeneration",
                    pre_token_generation_config=cognito_mixins.CfnUserPoolPropsMixin.PreTokenGenerationConfigProperty(
                        lambda_arn="lambdaArn",
                        lambda_version="lambdaVersion"
                    ),
                    user_migration="userMigration",
                    verify_auth_challenge_response="verifyAuthChallengeResponse"
                ),
                mfa_configuration="mfaConfiguration",
                policies=cognito_mixins.CfnUserPoolPropsMixin.PoliciesProperty(
                    password_policy=cognito_mixins.CfnUserPoolPropsMixin.PasswordPolicyProperty(
                        minimum_length=123,
                        password_history_size=123,
                        require_lowercase=False,
                        require_numbers=False,
                        require_symbols=False,
                        require_uppercase=False,
                        temporary_password_validity_days=123
                    ),
                    sign_in_policy=cognito_mixins.CfnUserPoolPropsMixin.SignInPolicyProperty(
                        allowed_first_auth_factors=["allowedFirstAuthFactors"]
                    )
                ),
                schema=[cognito_mixins.CfnUserPoolPropsMixin.SchemaAttributeProperty(
                    attribute_data_type="attributeDataType",
                    developer_only_attribute=False,
                    mutable=False,
                    name="name",
                    number_attribute_constraints=cognito_mixins.CfnUserPoolPropsMixin.NumberAttributeConstraintsProperty(
                        max_value="maxValue",
                        min_value="minValue"
                    ),
                    required=False,
                    string_attribute_constraints=cognito_mixins.CfnUserPoolPropsMixin.StringAttributeConstraintsProperty(
                        max_length="maxLength",
                        min_length="minLength"
                    )
                )],
                sms_authentication_message="smsAuthenticationMessage",
                sms_configuration=cognito_mixins.CfnUserPoolPropsMixin.SmsConfigurationProperty(
                    external_id="externalId",
                    sns_caller_arn="snsCallerArn",
                    sns_region="snsRegion"
                ),
                sms_verification_message="smsVerificationMessage",
                user_attribute_update_settings=cognito_mixins.CfnUserPoolPropsMixin.UserAttributeUpdateSettingsProperty(
                    attributes_require_verification_before_update=["attributesRequireVerificationBeforeUpdate"]
                ),
                username_attributes=["usernameAttributes"],
                username_configuration=cognito_mixins.CfnUserPoolPropsMixin.UsernameConfigurationProperty(
                    case_sensitive=False
                ),
                user_pool_add_ons=cognito_mixins.CfnUserPoolPropsMixin.UserPoolAddOnsProperty(
                    advanced_security_additional_flows=cognito_mixins.CfnUserPoolPropsMixin.AdvancedSecurityAdditionalFlowsProperty(
                        custom_auth_mode="customAuthMode"
                    ),
                    advanced_security_mode="advancedSecurityMode"
                ),
                user_pool_name="userPoolName",
                user_pool_tags=user_pool_tags,
                user_pool_tier="userPoolTier",
                verification_message_template=cognito_mixins.CfnUserPoolPropsMixin.VerificationMessageTemplateProperty(
                    default_email_option="defaultEmailOption",
                    email_message="emailMessage",
                    email_message_by_link="emailMessageByLink",
                    email_subject="emailSubject",
                    email_subject_by_link="emailSubjectByLink",
                    sms_message="smsMessage"
                ),
                web_authn_relying_party_id="webAuthnRelyingPartyId",
                web_authn_user_verification="webAuthnUserVerification"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b4eb0e7220a005c8b0ba6bd6da0c1c84e2acc270ad0946b545ce105d321867)
            check_type(argname="argument account_recovery_setting", value=account_recovery_setting, expected_type=type_hints["account_recovery_setting"])
            check_type(argname="argument admin_create_user_config", value=admin_create_user_config, expected_type=type_hints["admin_create_user_config"])
            check_type(argname="argument alias_attributes", value=alias_attributes, expected_type=type_hints["alias_attributes"])
            check_type(argname="argument auto_verified_attributes", value=auto_verified_attributes, expected_type=type_hints["auto_verified_attributes"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument device_configuration", value=device_configuration, expected_type=type_hints["device_configuration"])
            check_type(argname="argument email_authentication_message", value=email_authentication_message, expected_type=type_hints["email_authentication_message"])
            check_type(argname="argument email_authentication_subject", value=email_authentication_subject, expected_type=type_hints["email_authentication_subject"])
            check_type(argname="argument email_configuration", value=email_configuration, expected_type=type_hints["email_configuration"])
            check_type(argname="argument email_verification_message", value=email_verification_message, expected_type=type_hints["email_verification_message"])
            check_type(argname="argument email_verification_subject", value=email_verification_subject, expected_type=type_hints["email_verification_subject"])
            check_type(argname="argument enabled_mfas", value=enabled_mfas, expected_type=type_hints["enabled_mfas"])
            check_type(argname="argument lambda_config", value=lambda_config, expected_type=type_hints["lambda_config"])
            check_type(argname="argument mfa_configuration", value=mfa_configuration, expected_type=type_hints["mfa_configuration"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument sms_authentication_message", value=sms_authentication_message, expected_type=type_hints["sms_authentication_message"])
            check_type(argname="argument sms_configuration", value=sms_configuration, expected_type=type_hints["sms_configuration"])
            check_type(argname="argument sms_verification_message", value=sms_verification_message, expected_type=type_hints["sms_verification_message"])
            check_type(argname="argument user_attribute_update_settings", value=user_attribute_update_settings, expected_type=type_hints["user_attribute_update_settings"])
            check_type(argname="argument username_attributes", value=username_attributes, expected_type=type_hints["username_attributes"])
            check_type(argname="argument username_configuration", value=username_configuration, expected_type=type_hints["username_configuration"])
            check_type(argname="argument user_pool_add_ons", value=user_pool_add_ons, expected_type=type_hints["user_pool_add_ons"])
            check_type(argname="argument user_pool_name", value=user_pool_name, expected_type=type_hints["user_pool_name"])
            check_type(argname="argument user_pool_tags", value=user_pool_tags, expected_type=type_hints["user_pool_tags"])
            check_type(argname="argument user_pool_tier", value=user_pool_tier, expected_type=type_hints["user_pool_tier"])
            check_type(argname="argument verification_message_template", value=verification_message_template, expected_type=type_hints["verification_message_template"])
            check_type(argname="argument web_authn_relying_party_id", value=web_authn_relying_party_id, expected_type=type_hints["web_authn_relying_party_id"])
            check_type(argname="argument web_authn_user_verification", value=web_authn_user_verification, expected_type=type_hints["web_authn_user_verification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_recovery_setting is not None:
            self._values["account_recovery_setting"] = account_recovery_setting
        if admin_create_user_config is not None:
            self._values["admin_create_user_config"] = admin_create_user_config
        if alias_attributes is not None:
            self._values["alias_attributes"] = alias_attributes
        if auto_verified_attributes is not None:
            self._values["auto_verified_attributes"] = auto_verified_attributes
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if device_configuration is not None:
            self._values["device_configuration"] = device_configuration
        if email_authentication_message is not None:
            self._values["email_authentication_message"] = email_authentication_message
        if email_authentication_subject is not None:
            self._values["email_authentication_subject"] = email_authentication_subject
        if email_configuration is not None:
            self._values["email_configuration"] = email_configuration
        if email_verification_message is not None:
            self._values["email_verification_message"] = email_verification_message
        if email_verification_subject is not None:
            self._values["email_verification_subject"] = email_verification_subject
        if enabled_mfas is not None:
            self._values["enabled_mfas"] = enabled_mfas
        if lambda_config is not None:
            self._values["lambda_config"] = lambda_config
        if mfa_configuration is not None:
            self._values["mfa_configuration"] = mfa_configuration
        if policies is not None:
            self._values["policies"] = policies
        if schema is not None:
            self._values["schema"] = schema
        if sms_authentication_message is not None:
            self._values["sms_authentication_message"] = sms_authentication_message
        if sms_configuration is not None:
            self._values["sms_configuration"] = sms_configuration
        if sms_verification_message is not None:
            self._values["sms_verification_message"] = sms_verification_message
        if user_attribute_update_settings is not None:
            self._values["user_attribute_update_settings"] = user_attribute_update_settings
        if username_attributes is not None:
            self._values["username_attributes"] = username_attributes
        if username_configuration is not None:
            self._values["username_configuration"] = username_configuration
        if user_pool_add_ons is not None:
            self._values["user_pool_add_ons"] = user_pool_add_ons
        if user_pool_name is not None:
            self._values["user_pool_name"] = user_pool_name
        if user_pool_tags is not None:
            self._values["user_pool_tags"] = user_pool_tags
        if user_pool_tier is not None:
            self._values["user_pool_tier"] = user_pool_tier
        if verification_message_template is not None:
            self._values["verification_message_template"] = verification_message_template
        if web_authn_relying_party_id is not None:
            self._values["web_authn_relying_party_id"] = web_authn_relying_party_id
        if web_authn_user_verification is not None:
            self._values["web_authn_user_verification"] = web_authn_user_verification

    @builtins.property
    def account_recovery_setting(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.AccountRecoverySettingProperty"]]:
        '''The available verified method a user can use to recover their password when they call ``ForgotPassword`` .

        You can use this setting to define a preferred method when a user has more than one method available. With this setting, SMS doesn't qualify for a valid password recovery mechanism if the user also has SMS multi-factor authentication (MFA) activated. In the absence of this setting, Amazon Cognito uses the legacy behavior to determine the recovery method where SMS is preferred through email.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-accountrecoverysetting
        '''
        result = self._values.get("account_recovery_setting")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.AccountRecoverySettingProperty"]], result)

    @builtins.property
    def admin_create_user_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.AdminCreateUserConfigProperty"]]:
        '''The settings for administrator creation of users in a user pool.

        Contains settings for allowing user sign-up, customizing invitation messages to new users, and the amount of time before temporary passwords expire.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-admincreateuserconfig
        '''
        result = self._values.get("admin_create_user_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.AdminCreateUserConfigProperty"]], result)

    @builtins.property
    def alias_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Attributes supported as an alias for this user pool.

        For more information about alias attributes, see `Customizing sign-in attributes <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-aliasattributes
        '''
        result = self._values.get("alias_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auto_verified_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The attributes that you want your user pool to automatically verify.

        For more information, see `Verifying contact information at sign-up <https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html#allowing-users-to-sign-up-and-confirm-themselves>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-autoverifiedattributes
        '''
        result = self._values.get("auto_verified_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.str]:
        '''When active, ``DeletionProtection`` prevents accidental deletion of your user pool.

        Before you can delete a user pool that you have protected against deletion, you
        must deactivate this feature.

        When you try to delete a protected user pool in a ``DeleteUserPool`` API request, Amazon Cognito returns an ``InvalidParameterException`` error. To delete a protected user pool, send a new ``DeleteUserPool`` request after you deactivate deletion protection in an ``UpdateUserPool`` API request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.DeviceConfigurationProperty"]]:
        '''The device-remembering configuration for a user pool.

        Device remembering or device tracking is a "Remember me on this device" option for user pools that perform authentication with the device key of a trusted device in the back end, instead of a user-provided MFA code. For more information about device authentication, see `Working with user devices in your user pool <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`_ . A null value indicates that you have deactivated device remembering in your user pool.
        .. epigraph::

           When you provide a value for any ``DeviceConfiguration`` field, you activate the Amazon Cognito device-remembering feature. For more information, see `Working with devices <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-deviceconfiguration
        '''
        result = self._values.get("device_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.DeviceConfigurationProperty"]], result)

    @builtins.property
    def email_authentication_message(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailauthenticationmessage
        '''
        result = self._values.get("email_authentication_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_authentication_subject(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailauthenticationsubject
        '''
        result = self._values.get("email_authentication_subject")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.EmailConfigurationProperty"]]:
        '''The email configuration of your user pool.

        The email configuration type sets your preferred sending method, AWS Region, and sender for messages from your user pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailconfiguration
        '''
        result = self._values.get("email_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.EmailConfigurationProperty"]], result)

    @builtins.property
    def email_verification_message(self) -> typing.Optional[builtins.str]:
        '''This parameter is no longer used.

        See `VerificationMessageTemplateType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailverificationmessage
        '''
        result = self._values.get("email_verification_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_verification_subject(self) -> typing.Optional[builtins.str]:
        '''This parameter is no longer used.

        See `VerificationMessageTemplateType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailverificationsubject
        '''
        result = self._values.get("email_verification_subject")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled_mfas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set enabled MFA options on a specified user pool.

        To disable all MFAs after it has been enabled, set ``MfaConfiguration`` to ``OFF`` and remove EnabledMfas. MFAs can only be all disabled if ``MfaConfiguration`` is ``OFF`` . After you enable ``SMS_MFA`` , you can only disable it by setting ``MfaConfiguration`` to ``OFF`` . Can be one of the following values:

        - ``SMS_MFA`` - Enables MFA with SMS for the user pool. To select this option, you must also provide values for ``SmsConfiguration`` .
        - ``SOFTWARE_TOKEN_MFA`` - Enables software token MFA for the user pool.
        - ``EMAIL_OTP`` - Enables MFA with email for the user pool. To select this option, you must provide values for ``EmailConfiguration`` and within those, set ``EmailSendingAccount`` to ``DEVELOPER`` .

        Allowed values: ``SMS_MFA`` | ``SOFTWARE_TOKEN_MFA`` | ``EMAIL_OTP``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-enabledmfas
        '''
        result = self._values.get("enabled_mfas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lambda_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.LambdaConfigProperty"]]:
        '''A collection of user pool Lambda triggers.

        Amazon Cognito invokes triggers at several possible stages of authentication operations. Triggers can modify the outcome of the operations that invoked them.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-lambdaconfig
        '''
        result = self._values.get("lambda_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.LambdaConfigProperty"]], result)

    @builtins.property
    def mfa_configuration(self) -> typing.Optional[builtins.str]:
        '''Displays the state of multi-factor authentication (MFA) as on, off, or optional.

        When ``ON`` , all users must set up MFA before they can sign in. When ``OPTIONAL`` , your application must make a client-side determination of whether a user wants to register an MFA device. For user pools with adaptive authentication with threat protection, choose ``OPTIONAL`` .

        When ``MfaConfiguration`` is ``OPTIONAL`` , managed login doesn't automatically prompt users to set up MFA. Amazon Cognito generates MFA prompts in API responses and in managed login for users who have chosen and configured a preferred MFA factor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-mfaconfiguration
        '''
        result = self._values.get("mfa_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.PoliciesProperty"]]:
        '''A list of user pool policies.

        Contains the policy that sets password-complexity requirements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.PoliciesProperty"]], result)

    @builtins.property
    def schema(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.SchemaAttributeProperty"]]]]:
        '''An array of attributes for the new user pool.

        You can add custom attributes and modify the properties of default attributes. The specifications in this parameter set the required attributes in your user pool. For more information, see `Working with user attributes <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-schema
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.SchemaAttributeProperty"]]]], result)

    @builtins.property
    def sms_authentication_message(self) -> typing.Optional[builtins.str]:
        '''The contents of the SMS authentication message.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsauthenticationmessage
        '''
        result = self._values.get("sms_authentication_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sms_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.SmsConfigurationProperty"]]:
        '''The settings for your Amazon Cognito user pool to send SMS messages with Amazon Simple Notification Service.

        To send SMS messages with Amazon SNS in the AWS Region that you want, the Amazon Cognito user pool uses an AWS Identity and Access Management (IAM) role in your AWS account . For more information see `SMS message settings <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsconfiguration
        '''
        result = self._values.get("sms_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.SmsConfigurationProperty"]], result)

    @builtins.property
    def sms_verification_message(self) -> typing.Optional[builtins.str]:
        '''This parameter is no longer used.

        See `VerificationMessageTemplateType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsverificationmessage
        '''
        result = self._values.get("sms_verification_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_attribute_update_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.UserAttributeUpdateSettingsProperty"]]:
        '''The settings for updates to user attributes.

        These settings include the property ``AttributesRequireVerificationBeforeUpdate`` ,
        a user-pool setting that tells Amazon Cognito how to handle changes to the value of your users' email address and phone number attributes. For
        more information, see `Verifying updates to email addresses and phone numbers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-email-phone-verification.html#user-pool-settings-verifications-verify-attribute-updates>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userattributeupdatesettings
        '''
        result = self._values.get("user_attribute_update_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.UserAttributeUpdateSettingsProperty"]], result)

    @builtins.property
    def username_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies whether a user can use an email address or phone number as a username when they sign up.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-usernameattributes
        '''
        result = self._values.get("username_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.UsernameConfigurationProperty"]]:
        '''Sets the case sensitivity option for sign-in usernames.

        When ``CaseSensitive`` is ``false`` (case insensitive), users can sign in with any combination of capital and lowercase letters. For example, ``username`` , ``USERNAME`` , or ``UserName`` , or for email, ``email@example.com`` or ``EMaiL@eXamplE.Com`` . For most use cases, set case sensitivity to ``false`` as a best practice. When usernames and email addresses are case insensitive, Amazon Cognito treats any variation in case as the same user, and prevents a case variation from being assigned to the same attribute for a different user.

        When ``CaseSensitive`` is ``true`` (case sensitive), Amazon Cognito interprets ``USERNAME`` and ``UserName`` as distinct users.

        This configuration is immutable after you set it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-usernameconfiguration
        '''
        result = self._values.get("username_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.UsernameConfigurationProperty"]], result)

    @builtins.property
    def user_pool_add_ons(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.UserPoolAddOnsProperty"]]:
        '''Contains settings for activation of threat protection, including the operating mode and additional authentication types.

        To log user security information but take no action, set to ``AUDIT`` . To configure automatic security responses to potentially unwanted traffic to your user pool, set to ``ENFORCED`` .

        For more information, see `Adding advanced security to a user pool <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-advanced-security.html>`_ . To activate this setting, your user pool must be on the `Plus tier <https://docs.aws.amazon.com/cognito/latest/developerguide/feature-plans-features-plus.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooladdons
        '''
        result = self._values.get("user_pool_add_ons")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.UserPoolAddOnsProperty"]], result)

    @builtins.property
    def user_pool_name(self) -> typing.Optional[builtins.str]:
        '''A friendly name for your user pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpoolname
        '''
        result = self._values.get("user_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_pool_tags(self) -> typing.Any:
        '''The tag keys and values to assign to the user pool.

        A tag is a label that you can use to categorize and manage user pools in different ways, such as by purpose, owner, environment, or other criteria.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooltags
        '''
        result = self._values.get("user_pool_tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def user_pool_tier(self) -> typing.Optional[builtins.str]:
        '''The user pool `feature plan <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sign-in-feature-plans.html>`_ , or tier. This parameter determines the eligibility of the user pool for features like managed login, access-token customization, and threat protection. Defaults to ``ESSENTIALS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooltier
        '''
        result = self._values.get("user_pool_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verification_message_template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.VerificationMessageTemplateProperty"]]:
        '''The template for the verification message that your user pool delivers to users who set an email address or phone number attribute.

        Set the email message type that corresponds to your ``DefaultEmailOption`` selection. For ``CONFIRM_WITH_LINK`` , specify an ``EmailMessageByLink`` and leave ``EmailMessage`` blank. For ``CONFIRM_WITH_CODE`` , specify an ``EmailMessage`` and leave ``EmailMessageByLink`` blank. When you supply both parameters with either choice, Amazon Cognito returns an error.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-verificationmessagetemplate
        '''
        result = self._values.get("verification_message_template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.VerificationMessageTemplateProperty"]], result)

    @builtins.property
    def web_authn_relying_party_id(self) -> typing.Optional[builtins.str]:
        '''Sets or displays the authentication domain, typically your user pool domain, that passkey providers must use as a relying party (RP) in their configuration.

        Under the following conditions, the passkey relying party ID must be the fully-qualified domain name of your custom domain:

        - The user pool is configured for passkey authentication.
        - The user pool has a custom domain, whether or not it also has a prefix domain.
        - Your application performs authentication with managed login or the classic hosted UI.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-webauthnrelyingpartyid
        '''
        result = self._values.get("web_authn_relying_party_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_authn_user_verification(self) -> typing.Optional[builtins.str]:
        '''When ``required`` , users can only register and sign in users with passkeys that are capable of `user verification <https://docs.aws.amazon.com/https://www.w3.org/TR/webauthn-2/#enum-userVerificationRequirement>`_ . When ``preferred`` , your user pool doesn't require the use of authenticators with user verification but encourages it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-webauthnuserverification
        '''
        result = self._values.get("web_authn_user_verification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin",
):
    '''The ``AWS::Cognito::UserPool`` resource creates an Amazon Cognito user pool.

    For more information on working with Amazon Cognito user pools, see `Amazon Cognito User Pools <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html>`_ and `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`_ .
    .. epigraph::

       If you don't specify a value for a parameter, Amazon Cognito sets it to a default value.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html
    :cloudformationResource: AWS::Cognito::UserPool
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        # user_pool_tags: Any
        
        cfn_user_pool_props_mixin = cognito_mixins.CfnUserPoolPropsMixin(cognito_mixins.CfnUserPoolMixinProps(
            account_recovery_setting=cognito_mixins.CfnUserPoolPropsMixin.AccountRecoverySettingProperty(
                recovery_mechanisms=[cognito_mixins.CfnUserPoolPropsMixin.RecoveryOptionProperty(
                    name="name",
                    priority=123
                )]
            ),
            admin_create_user_config=cognito_mixins.CfnUserPoolPropsMixin.AdminCreateUserConfigProperty(
                allow_admin_create_user_only=False,
                invite_message_template=cognito_mixins.CfnUserPoolPropsMixin.InviteMessageTemplateProperty(
                    email_message="emailMessage",
                    email_subject="emailSubject",
                    sms_message="smsMessage"
                ),
                unused_account_validity_days=123
            ),
            alias_attributes=["aliasAttributes"],
            auto_verified_attributes=["autoVerifiedAttributes"],
            deletion_protection="deletionProtection",
            device_configuration=cognito_mixins.CfnUserPoolPropsMixin.DeviceConfigurationProperty(
                challenge_required_on_new_device=False,
                device_only_remembered_on_user_prompt=False
            ),
            email_authentication_message="emailAuthenticationMessage",
            email_authentication_subject="emailAuthenticationSubject",
            email_configuration=cognito_mixins.CfnUserPoolPropsMixin.EmailConfigurationProperty(
                configuration_set="configurationSet",
                email_sending_account="emailSendingAccount",
                from="from",
                reply_to_email_address="replyToEmailAddress",
                source_arn="sourceArn"
            ),
            email_verification_message="emailVerificationMessage",
            email_verification_subject="emailVerificationSubject",
            enabled_mfas=["enabledMfas"],
            lambda_config=cognito_mixins.CfnUserPoolPropsMixin.LambdaConfigProperty(
                create_auth_challenge="createAuthChallenge",
                custom_email_sender=cognito_mixins.CfnUserPoolPropsMixin.CustomEmailSenderProperty(
                    lambda_arn="lambdaArn",
                    lambda_version="lambdaVersion"
                ),
                custom_message="customMessage",
                custom_sms_sender=cognito_mixins.CfnUserPoolPropsMixin.CustomSMSSenderProperty(
                    lambda_arn="lambdaArn",
                    lambda_version="lambdaVersion"
                ),
                define_auth_challenge="defineAuthChallenge",
                kms_key_id="kmsKeyId",
                post_authentication="postAuthentication",
                post_confirmation="postConfirmation",
                pre_authentication="preAuthentication",
                pre_sign_up="preSignUp",
                pre_token_generation="preTokenGeneration",
                pre_token_generation_config=cognito_mixins.CfnUserPoolPropsMixin.PreTokenGenerationConfigProperty(
                    lambda_arn="lambdaArn",
                    lambda_version="lambdaVersion"
                ),
                user_migration="userMigration",
                verify_auth_challenge_response="verifyAuthChallengeResponse"
            ),
            mfa_configuration="mfaConfiguration",
            policies=cognito_mixins.CfnUserPoolPropsMixin.PoliciesProperty(
                password_policy=cognito_mixins.CfnUserPoolPropsMixin.PasswordPolicyProperty(
                    minimum_length=123,
                    password_history_size=123,
                    require_lowercase=False,
                    require_numbers=False,
                    require_symbols=False,
                    require_uppercase=False,
                    temporary_password_validity_days=123
                ),
                sign_in_policy=cognito_mixins.CfnUserPoolPropsMixin.SignInPolicyProperty(
                    allowed_first_auth_factors=["allowedFirstAuthFactors"]
                )
            ),
            schema=[cognito_mixins.CfnUserPoolPropsMixin.SchemaAttributeProperty(
                attribute_data_type="attributeDataType",
                developer_only_attribute=False,
                mutable=False,
                name="name",
                number_attribute_constraints=cognito_mixins.CfnUserPoolPropsMixin.NumberAttributeConstraintsProperty(
                    max_value="maxValue",
                    min_value="minValue"
                ),
                required=False,
                string_attribute_constraints=cognito_mixins.CfnUserPoolPropsMixin.StringAttributeConstraintsProperty(
                    max_length="maxLength",
                    min_length="minLength"
                )
            )],
            sms_authentication_message="smsAuthenticationMessage",
            sms_configuration=cognito_mixins.CfnUserPoolPropsMixin.SmsConfigurationProperty(
                external_id="externalId",
                sns_caller_arn="snsCallerArn",
                sns_region="snsRegion"
            ),
            sms_verification_message="smsVerificationMessage",
            user_attribute_update_settings=cognito_mixins.CfnUserPoolPropsMixin.UserAttributeUpdateSettingsProperty(
                attributes_require_verification_before_update=["attributesRequireVerificationBeforeUpdate"]
            ),
            username_attributes=["usernameAttributes"],
            username_configuration=cognito_mixins.CfnUserPoolPropsMixin.UsernameConfigurationProperty(
                case_sensitive=False
            ),
            user_pool_add_ons=cognito_mixins.CfnUserPoolPropsMixin.UserPoolAddOnsProperty(
                advanced_security_additional_flows=cognito_mixins.CfnUserPoolPropsMixin.AdvancedSecurityAdditionalFlowsProperty(
                    custom_auth_mode="customAuthMode"
                ),
                advanced_security_mode="advancedSecurityMode"
            ),
            user_pool_name="userPoolName",
            user_pool_tags=user_pool_tags,
            user_pool_tier="userPoolTier",
            verification_message_template=cognito_mixins.CfnUserPoolPropsMixin.VerificationMessageTemplateProperty(
                default_email_option="defaultEmailOption",
                email_message="emailMessage",
                email_message_by_link="emailMessageByLink",
                email_subject="emailSubject",
                email_subject_by_link="emailSubjectByLink",
                sms_message="smsMessage"
            ),
            web_authn_relying_party_id="webAuthnRelyingPartyId",
            web_authn_user_verification="webAuthnUserVerification"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::UserPool``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d554208e2da41ddcef3ae18f20026408f2e78fdf626a88e252dd98aff0d82e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a6db27c3b3965403f5875859a06d7836b47192e5ae073bc7ba2b015e84faebd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea9c45d0f50699a5d6887a5b3f0331e264e18dbced3e5b69cf53bd1a25a5d7f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPoolMixinProps:
        return typing.cast(CfnUserPoolMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.AccountRecoverySettingProperty",
        jsii_struct_bases=[],
        name_mapping={"recovery_mechanisms": "recoveryMechanisms"},
    )
    class AccountRecoverySettingProperty:
        def __init__(
            self,
            *,
            recovery_mechanisms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.RecoveryOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The available verified method a user can use to recover their password when they call ``ForgotPassword`` .

            You can use this setting to define a preferred method when a user has more than one method available. With this setting, SMS doesn't qualify for a valid password recovery mechanism if the user also has SMS multi-factor authentication (MFA) activated. In the absence of this setting, Amazon Cognito uses the legacy behavior to determine the recovery method where SMS is preferred through email.

            :param recovery_mechanisms: The list of options and priorities for user message delivery in forgot-password operations. Sets or displays user pool preferences for email or SMS message priority, whether users should fall back to a second delivery method, and whether passwords should only be reset by administrators.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-accountrecoverysetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                account_recovery_setting_property = cognito_mixins.CfnUserPoolPropsMixin.AccountRecoverySettingProperty(
                    recovery_mechanisms=[cognito_mixins.CfnUserPoolPropsMixin.RecoveryOptionProperty(
                        name="name",
                        priority=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e37deb353af10c224b4a2543dde1921c0c6742397a53b41b2a4bbc501a284a58)
                check_type(argname="argument recovery_mechanisms", value=recovery_mechanisms, expected_type=type_hints["recovery_mechanisms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if recovery_mechanisms is not None:
                self._values["recovery_mechanisms"] = recovery_mechanisms

        @builtins.property
        def recovery_mechanisms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.RecoveryOptionProperty"]]]]:
            '''The list of options and priorities for user message delivery in forgot-password operations.

            Sets or displays user pool preferences for email or SMS message priority, whether users should fall back to a second delivery method, and whether passwords should only be reset by administrators.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-accountrecoverysetting.html#cfn-cognito-userpool-accountrecoverysetting-recoverymechanisms
            '''
            result = self._values.get("recovery_mechanisms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.RecoveryOptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountRecoverySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.AdminCreateUserConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_admin_create_user_only": "allowAdminCreateUserOnly",
            "invite_message_template": "inviteMessageTemplate",
            "unused_account_validity_days": "unusedAccountValidityDays",
        },
    )
    class AdminCreateUserConfigProperty:
        def __init__(
            self,
            *,
            allow_admin_create_user_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            invite_message_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.InviteMessageTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            unused_account_validity_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The settings for administrator creation of users in a user pool.

            Contains settings for allowing user sign-up, customizing invitation messages to new users, and the amount of time before temporary passwords expire.

            :param allow_admin_create_user_only: The setting for allowing self-service sign-up. When ``true`` , only administrators can create new user profiles. When ``false`` , users can register themselves and create a new user profile with the ``SignUp`` operation.
            :param invite_message_template: The template for the welcome message to new users. This template must include the ``{####}`` temporary password placeholder if you are creating users with passwords. If your users don't have passwords, you can omit the placeholder. See also `Customizing User Invitation Messages <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-customizations.html#cognito-user-pool-settings-user-invitation-message-customization>`_ .
            :param unused_account_validity_days: This parameter is no longer in use. The password expiration limit in days for administrator-created users. When this time expires, the user can't sign in with their temporary password. To reset the account after that time limit, you must call ``AdminCreateUser`` again, specifying ``RESEND`` for the ``MessageAction`` parameter. The default value for this parameter is 7.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                admin_create_user_config_property = cognito_mixins.CfnUserPoolPropsMixin.AdminCreateUserConfigProperty(
                    allow_admin_create_user_only=False,
                    invite_message_template=cognito_mixins.CfnUserPoolPropsMixin.InviteMessageTemplateProperty(
                        email_message="emailMessage",
                        email_subject="emailSubject",
                        sms_message="smsMessage"
                    ),
                    unused_account_validity_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4cd99587e534d381f9835a3824aaf31173bcb4b8124748e662ca5bc0ce2bf25)
                check_type(argname="argument allow_admin_create_user_only", value=allow_admin_create_user_only, expected_type=type_hints["allow_admin_create_user_only"])
                check_type(argname="argument invite_message_template", value=invite_message_template, expected_type=type_hints["invite_message_template"])
                check_type(argname="argument unused_account_validity_days", value=unused_account_validity_days, expected_type=type_hints["unused_account_validity_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_admin_create_user_only is not None:
                self._values["allow_admin_create_user_only"] = allow_admin_create_user_only
            if invite_message_template is not None:
                self._values["invite_message_template"] = invite_message_template
            if unused_account_validity_days is not None:
                self._values["unused_account_validity_days"] = unused_account_validity_days

        @builtins.property
        def allow_admin_create_user_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The setting for allowing self-service sign-up.

            When ``true`` , only administrators can create new user profiles. When ``false`` , users can register themselves and create a new user profile with the ``SignUp`` operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html#cfn-cognito-userpool-admincreateuserconfig-allowadmincreateuseronly
            '''
            result = self._values.get("allow_admin_create_user_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def invite_message_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.InviteMessageTemplateProperty"]]:
            '''The template for the welcome message to new users.

            This template must include the ``{####}`` temporary password placeholder if you are creating users with passwords. If your users don't have passwords, you can omit the placeholder.

            See also `Customizing User Invitation Messages <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-customizations.html#cognito-user-pool-settings-user-invitation-message-customization>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html#cfn-cognito-userpool-admincreateuserconfig-invitemessagetemplate
            '''
            result = self._values.get("invite_message_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.InviteMessageTemplateProperty"]], result)

        @builtins.property
        def unused_account_validity_days(self) -> typing.Optional[jsii.Number]:
            '''This parameter is no longer in use.

            The password expiration limit in days for administrator-created users. When this time expires, the user can't sign in with their temporary password. To reset the account after that time limit, you must call ``AdminCreateUser`` again, specifying ``RESEND`` for the ``MessageAction`` parameter.

            The default value for this parameter is 7.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html#cfn-cognito-userpool-admincreateuserconfig-unusedaccountvaliditydays
            '''
            result = self._values.get("unused_account_validity_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdminCreateUserConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.AdvancedSecurityAdditionalFlowsProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_auth_mode": "customAuthMode"},
    )
    class AdvancedSecurityAdditionalFlowsProperty:
        def __init__(
            self,
            *,
            custom_auth_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Threat protection configuration options for additional authentication types in your user pool, including custom authentication.

            :param custom_auth_mode: The operating mode of threat protection in custom authentication with `Custom authentication challenge Lambda triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-advancedsecurityadditionalflows.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                advanced_security_additional_flows_property = cognito_mixins.CfnUserPoolPropsMixin.AdvancedSecurityAdditionalFlowsProperty(
                    custom_auth_mode="customAuthMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a4bbba40f607275e69bf26e843a8c67bd6535e93bd7c1eeb7c4a20a62ae903d)
                check_type(argname="argument custom_auth_mode", value=custom_auth_mode, expected_type=type_hints["custom_auth_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_auth_mode is not None:
                self._values["custom_auth_mode"] = custom_auth_mode

        @builtins.property
        def custom_auth_mode(self) -> typing.Optional[builtins.str]:
            '''The operating mode of threat protection in custom authentication with `Custom authentication challenge Lambda triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-advancedsecurityadditionalflows.html#cfn-cognito-userpool-advancedsecurityadditionalflows-customauthmode
            '''
            result = self._values.get("custom_auth_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedSecurityAdditionalFlowsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.CustomEmailSenderProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_arn": "lambdaArn", "lambda_version": "lambdaVersion"},
    )
    class CustomEmailSenderProperty:
        def __init__(
            self,
            *,
            lambda_arn: typing.Optional[builtins.str] = None,
            lambda_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of a custom email sender Lambda trigger.

            This trigger routes all email notifications from a user pool to a Lambda function that delivers the message using custom logic.

            :param lambda_arn: The Amazon Resource Name (ARN) of the function that you want to assign to your Lambda trigger.
            :param lambda_version: The user pool trigger version of the request that Amazon Cognito sends to your Lambda function. Higher-numbered versions add fields that support new features. You must use a ``LambdaVersion`` of ``V1_0`` with a custom sender function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-customemailsender.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                custom_email_sender_property = cognito_mixins.CfnUserPoolPropsMixin.CustomEmailSenderProperty(
                    lambda_arn="lambdaArn",
                    lambda_version="lambdaVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e73af3177e974a2e869fa9e007f41ce3f8032787bd8581b976997db9c7e8ba64)
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
                check_type(argname="argument lambda_version", value=lambda_version, expected_type=type_hints["lambda_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn
            if lambda_version is not None:
                self._values["lambda_version"] = lambda_version

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the function that you want to assign to your Lambda trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-customemailsender.html#cfn-cognito-userpool-customemailsender-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_version(self) -> typing.Optional[builtins.str]:
            '''The user pool trigger version of the request that Amazon Cognito sends to your Lambda function.

            Higher-numbered versions add fields that support new features.

            You must use a ``LambdaVersion`` of ``V1_0`` with a custom sender function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-customemailsender.html#cfn-cognito-userpool-customemailsender-lambdaversion
            '''
            result = self._values.get("lambda_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomEmailSenderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.CustomSMSSenderProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_arn": "lambdaArn", "lambda_version": "lambdaVersion"},
    )
    class CustomSMSSenderProperty:
        def __init__(
            self,
            *,
            lambda_arn: typing.Optional[builtins.str] = None,
            lambda_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of a custom SMS sender Lambda trigger.

            This trigger routes all SMS notifications from a user pool to a Lambda function that delivers the message using custom logic.

            :param lambda_arn: The Amazon Resource Name (ARN) of the function that you want to assign to your Lambda trigger.
            :param lambda_version: The user pool trigger version of the request that Amazon Cognito sends to your Lambda function. Higher-numbered versions add fields that support new features. You must use a ``LambdaVersion`` of ``V1_0`` with a custom sender function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-customsmssender.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                custom_sMSSender_property = cognito_mixins.CfnUserPoolPropsMixin.CustomSMSSenderProperty(
                    lambda_arn="lambdaArn",
                    lambda_version="lambdaVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__674bca0bca940515ceefc699729b8d1545a40ee53bba87da7c4f686da3e3c8b6)
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
                check_type(argname="argument lambda_version", value=lambda_version, expected_type=type_hints["lambda_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn
            if lambda_version is not None:
                self._values["lambda_version"] = lambda_version

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the function that you want to assign to your Lambda trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-customsmssender.html#cfn-cognito-userpool-customsmssender-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_version(self) -> typing.Optional[builtins.str]:
            '''The user pool trigger version of the request that Amazon Cognito sends to your Lambda function.

            Higher-numbered versions add fields that support new features.

            You must use a ``LambdaVersion`` of ``V1_0`` with a custom sender function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-customsmssender.html#cfn-cognito-userpool-customsmssender-lambdaversion
            '''
            result = self._values.get("lambda_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomSMSSenderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.DeviceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "challenge_required_on_new_device": "challengeRequiredOnNewDevice",
            "device_only_remembered_on_user_prompt": "deviceOnlyRememberedOnUserPrompt",
        },
    )
    class DeviceConfigurationProperty:
        def __init__(
            self,
            *,
            challenge_required_on_new_device: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            device_only_remembered_on_user_prompt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The device-remembering configuration for a user pool.

            :param challenge_required_on_new_device: When true, a remembered device can sign in with device authentication instead of SMS and time-based one-time password (TOTP) factors for multi-factor authentication (MFA). .. epigraph:: Whether or not ``ChallengeRequiredOnNewDevice`` is true, users who sign in with devices that have not been confirmed or remembered must still provide a second factor in a user pool that requires MFA.
            :param device_only_remembered_on_user_prompt: When true, Amazon Cognito doesn't automatically remember a user's device when your app sends a ``ConfirmDevice`` API request. In your app, create a prompt for your user to choose whether they want to remember their device. Return the user's choice in an ``UpdateDeviceStatus`` API request. When ``DeviceOnlyRememberedOnUserPrompt`` is ``false`` , Amazon Cognito immediately remembers devices that you register in a ``ConfirmDevice`` API request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-deviceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                device_configuration_property = cognito_mixins.CfnUserPoolPropsMixin.DeviceConfigurationProperty(
                    challenge_required_on_new_device=False,
                    device_only_remembered_on_user_prompt=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2aef09c6b425659a4aaa710804d63183ce7cb73e3b5ee0800fa78020987d4d1)
                check_type(argname="argument challenge_required_on_new_device", value=challenge_required_on_new_device, expected_type=type_hints["challenge_required_on_new_device"])
                check_type(argname="argument device_only_remembered_on_user_prompt", value=device_only_remembered_on_user_prompt, expected_type=type_hints["device_only_remembered_on_user_prompt"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if challenge_required_on_new_device is not None:
                self._values["challenge_required_on_new_device"] = challenge_required_on_new_device
            if device_only_remembered_on_user_prompt is not None:
                self._values["device_only_remembered_on_user_prompt"] = device_only_remembered_on_user_prompt

        @builtins.property
        def challenge_required_on_new_device(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true, a remembered device can sign in with device authentication instead of SMS and time-based one-time password (TOTP) factors for multi-factor authentication (MFA).

            .. epigraph::

               Whether or not ``ChallengeRequiredOnNewDevice`` is true, users who sign in with devices that have not been confirmed or remembered must still provide a second factor in a user pool that requires MFA.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-deviceconfiguration.html#cfn-cognito-userpool-deviceconfiguration-challengerequiredonnewdevice
            '''
            result = self._values.get("challenge_required_on_new_device")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def device_only_remembered_on_user_prompt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true, Amazon Cognito doesn't automatically remember a user's device when your app sends a ``ConfirmDevice`` API request.

            In your app, create a prompt for your user to choose whether they want to remember their device. Return the user's choice in an ``UpdateDeviceStatus`` API request.

            When ``DeviceOnlyRememberedOnUserPrompt`` is ``false`` , Amazon Cognito immediately remembers devices that you register in a ``ConfirmDevice`` API request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-deviceconfiguration.html#cfn-cognito-userpool-deviceconfiguration-deviceonlyrememberedonuserprompt
            '''
            result = self._values.get("device_only_remembered_on_user_prompt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.EmailConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration_set": "configurationSet",
            "email_sending_account": "emailSendingAccount",
            "from_": "from",
            "reply_to_email_address": "replyToEmailAddress",
            "source_arn": "sourceArn",
        },
    )
    class EmailConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_set: typing.Optional[builtins.str] = None,
            email_sending_account: typing.Optional[builtins.str] = None,
            from_: typing.Optional[builtins.str] = None,
            reply_to_email_address: typing.Optional[builtins.str] = None,
            source_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The email configuration of your user pool.

            The email configuration type sets your preferred sending method, AWS Region, and sender for messages from your user pool.

            :param configuration_set: The set of configuration rules that can be applied to emails sent using Amazon Simple Email Service. A configuration set is applied to an email by including a reference to the configuration set in the headers of the email. Once applied, all of the rules in that configuration set are applied to the email. Configuration sets can be used to apply the following types of rules to emails: - **Event publishing** - Amazon Simple Email Service can track the number of send, delivery, open, click, bounce, and complaint events for each email sent. Use event publishing to send information about these events to other AWS services such as and Amazon CloudWatch - **IP pool management** - When leasing dedicated IP addresses with Amazon Simple Email Service, you can create groups of IP addresses, called dedicated IP pools. You can then associate the dedicated IP pools with configuration sets.
            :param email_sending_account: Specifies whether Amazon Cognito uses its built-in functionality to send your users email messages, or uses your Amazon Simple Email Service email configuration. Specify one of the following values: - **COGNITO_DEFAULT** - When Amazon Cognito emails your users, it uses its built-in email functionality. When you use the default option, Amazon Cognito allows only a limited number of emails each day for your user pool. For typical production environments, the default email limit is less than the required delivery volume. To achieve a higher delivery volume, specify DEVELOPER to use your Amazon SES email configuration. To look up the email delivery limit for the default option, see `Limits <https://docs.aws.amazon.com/cognito/latest/developerguide/limits.html>`_ in the *Amazon Cognito Developer Guide* . The default FROM address is ``no-reply@verificationemail.com`` . To customize the FROM address, provide the Amazon Resource Name (ARN) of an Amazon SES verified email address for the ``SourceArn`` parameter. - **DEVELOPER** - When Amazon Cognito emails your users, it uses your Amazon SES configuration. Amazon Cognito calls Amazon SES on your behalf to send email from your verified email address. When you use this option, the email delivery limits are the same limits that apply to your Amazon SES verified email address in your AWS account . If you use this option, provide the ARN of an Amazon SES verified email address for the ``SourceArn`` parameter. Before Amazon Cognito can email your users, it requires additional permissions to call Amazon SES on your behalf. When you update your user pool with this option, Amazon Cognito creates a *service-linked role* , which is a type of role in your AWS account . This role contains the permissions that allow you to access Amazon SES and send email messages from your email address. For more information about the service-linked role that Amazon Cognito creates, see `Using Service-Linked Roles for Amazon Cognito <https://docs.aws.amazon.com/cognito/latest/developerguide/using-service-linked-roles.html>`_ in the *Amazon Cognito Developer Guide* .
            :param from_: Either the sender’s email address or the sender’s name with their email address. For example, ``testuser@example.com`` or ``Test User <testuser@example.com>`` . This address appears before the body of the email.
            :param reply_to_email_address: The destination to which the receiver of the email should reply.
            :param source_arn: The ARN of a verified email address or an address from a verified domain in Amazon SES. You can set a ``SourceArn`` email from a verified domain only with an API request. You can set a verified email address, but not an address in a verified domain, in the Amazon Cognito console. Amazon Cognito uses the email address that you provide in one of the following ways, depending on the value that you specify for the ``EmailSendingAccount`` parameter: - If you specify ``COGNITO_DEFAULT`` , Amazon Cognito uses this address as the custom FROM address when it emails your users using its built-in email account. - If you specify ``DEVELOPER`` , Amazon Cognito emails your users with this address by calling Amazon SES on your behalf. The Region value of the ``SourceArn`` parameter must indicate a supported AWS Region of your user pool. Typically, the Region in the ``SourceArn`` and the user pool Region are the same. For more information, see `Amazon SES email configuration regions <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-email.html#user-pool-email-developer-region-mapping>`_ in the `Amazon Cognito Developer Guide <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                email_configuration_property = cognito_mixins.CfnUserPoolPropsMixin.EmailConfigurationProperty(
                    configuration_set="configurationSet",
                    email_sending_account="emailSendingAccount",
                    from="from",
                    reply_to_email_address="replyToEmailAddress",
                    source_arn="sourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__32ab99ce231b12bfb027f5f68af56cebfb3d524a5e2ac8b1c13be4dbf287e5f3)
                check_type(argname="argument configuration_set", value=configuration_set, expected_type=type_hints["configuration_set"])
                check_type(argname="argument email_sending_account", value=email_sending_account, expected_type=type_hints["email_sending_account"])
                check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
                check_type(argname="argument reply_to_email_address", value=reply_to_email_address, expected_type=type_hints["reply_to_email_address"])
                check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration_set is not None:
                self._values["configuration_set"] = configuration_set
            if email_sending_account is not None:
                self._values["email_sending_account"] = email_sending_account
            if from_ is not None:
                self._values["from_"] = from_
            if reply_to_email_address is not None:
                self._values["reply_to_email_address"] = reply_to_email_address
            if source_arn is not None:
                self._values["source_arn"] = source_arn

        @builtins.property
        def configuration_set(self) -> typing.Optional[builtins.str]:
            '''The set of configuration rules that can be applied to emails sent using Amazon Simple Email Service.

            A configuration set is applied to an email by including a reference to the configuration set in the headers of the email. Once applied, all of the rules in that configuration set are applied to the email. Configuration sets can be used to apply the following types of rules to emails:

            - **Event publishing** - Amazon Simple Email Service can track the number of send, delivery, open, click, bounce, and complaint events for each email sent. Use event publishing to send information about these events to other AWS services such as and Amazon CloudWatch
            - **IP pool management** - When leasing dedicated IP addresses with Amazon Simple Email Service, you can create groups of IP addresses, called dedicated IP pools. You can then associate the dedicated IP pools with configuration sets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-configurationset
            '''
            result = self._values.get("configuration_set")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def email_sending_account(self) -> typing.Optional[builtins.str]:
            '''Specifies whether Amazon Cognito uses its built-in functionality to send your users email messages, or uses your Amazon Simple Email Service email configuration.

            Specify one of the following values:

            - **COGNITO_DEFAULT** - When Amazon Cognito emails your users, it uses its built-in email functionality. When you use the default option, Amazon Cognito allows only a limited number of emails each day for your user pool. For typical production environments, the default email limit is less than the required delivery volume. To achieve a higher delivery volume, specify DEVELOPER to use your Amazon SES email configuration.

            To look up the email delivery limit for the default option, see `Limits <https://docs.aws.amazon.com/cognito/latest/developerguide/limits.html>`_ in the *Amazon Cognito Developer Guide* .

            The default FROM address is ``no-reply@verificationemail.com`` . To customize the FROM address, provide the Amazon Resource Name (ARN) of an Amazon SES verified email address for the ``SourceArn`` parameter.

            - **DEVELOPER** - When Amazon Cognito emails your users, it uses your Amazon SES configuration. Amazon Cognito calls Amazon SES on your behalf to send email from your verified email address. When you use this option, the email delivery limits are the same limits that apply to your Amazon SES verified email address in your AWS account .

            If you use this option, provide the ARN of an Amazon SES verified email address for the ``SourceArn`` parameter.

            Before Amazon Cognito can email your users, it requires additional permissions to call Amazon SES on your behalf. When you update your user pool with this option, Amazon Cognito creates a *service-linked role* , which is a type of role in your AWS account . This role contains the permissions that allow you to access Amazon SES and send email messages from your email address. For more information about the service-linked role that Amazon Cognito creates, see `Using Service-Linked Roles for Amazon Cognito <https://docs.aws.amazon.com/cognito/latest/developerguide/using-service-linked-roles.html>`_ in the *Amazon Cognito Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-emailsendingaccount
            '''
            result = self._values.get("email_sending_account")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def from_(self) -> typing.Optional[builtins.str]:
            '''Either the sender’s email address or the sender’s name with their email address.

            For example, ``testuser@example.com`` or ``Test User <testuser@example.com>`` . This address appears before the body of the email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-from
            '''
            result = self._values.get("from_")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reply_to_email_address(self) -> typing.Optional[builtins.str]:
            '''The destination to which the receiver of the email should reply.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-replytoemailaddress
            '''
            result = self._values.get("reply_to_email_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of a verified email address or an address from a verified domain in Amazon SES.

            You can set a ``SourceArn`` email from a verified domain only with an API request. You can set a verified email address, but not an address in a verified domain, in the Amazon Cognito console. Amazon Cognito uses the email address that you provide in one of the following ways, depending on the value that you specify for the ``EmailSendingAccount`` parameter:

            - If you specify ``COGNITO_DEFAULT`` , Amazon Cognito uses this address as the custom FROM address when it emails your users using its built-in email account.
            - If you specify ``DEVELOPER`` , Amazon Cognito emails your users with this address by calling Amazon SES on your behalf.

            The Region value of the ``SourceArn`` parameter must indicate a supported AWS Region of your user pool. Typically, the Region in the ``SourceArn`` and the user pool Region are the same. For more information, see `Amazon SES email configuration regions <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-email.html#user-pool-email-developer-region-mapping>`_ in the `Amazon Cognito Developer Guide <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-sourcearn
            '''
            result = self._values.get("source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.InviteMessageTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email_message": "emailMessage",
            "email_subject": "emailSubject",
            "sms_message": "smsMessage",
        },
    )
    class InviteMessageTemplateProperty:
        def __init__(
            self,
            *,
            email_message: typing.Optional[builtins.str] = None,
            email_subject: typing.Optional[builtins.str] = None,
            sms_message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The template for the welcome message to new users.

            This template must include the ``{####}`` temporary password placeholder if you are creating users with passwords. If your users don't have passwords, you can omit the placeholder.

            See also `Customizing User Invitation Messages <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-customizations.html#cognito-user-pool-settings-user-invitation-message-customization>`_ .

            :param email_message: The message template for email messages. EmailMessage is allowed only if `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is DEVELOPER.
            :param email_subject: The subject line for email messages. EmailSubject is allowed only if `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is DEVELOPER.
            :param sms_message: The message template for SMS messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                invite_message_template_property = cognito_mixins.CfnUserPoolPropsMixin.InviteMessageTemplateProperty(
                    email_message="emailMessage",
                    email_subject="emailSubject",
                    sms_message="smsMessage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4d187426586a42084d4a1511ffc21221e7220be7964c86f7cbdd071471447b7)
                check_type(argname="argument email_message", value=email_message, expected_type=type_hints["email_message"])
                check_type(argname="argument email_subject", value=email_subject, expected_type=type_hints["email_subject"])
                check_type(argname="argument sms_message", value=sms_message, expected_type=type_hints["sms_message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email_message is not None:
                self._values["email_message"] = email_message
            if email_subject is not None:
                self._values["email_subject"] = email_subject
            if sms_message is not None:
                self._values["sms_message"] = sms_message

        @builtins.property
        def email_message(self) -> typing.Optional[builtins.str]:
            '''The message template for email messages.

            EmailMessage is allowed only if `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is DEVELOPER.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html#cfn-cognito-userpool-invitemessagetemplate-emailmessage
            '''
            result = self._values.get("email_message")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def email_subject(self) -> typing.Optional[builtins.str]:
            '''The subject line for email messages.

            EmailSubject is allowed only if `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is DEVELOPER.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html#cfn-cognito-userpool-invitemessagetemplate-emailsubject
            '''
            result = self._values.get("email_subject")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sms_message(self) -> typing.Optional[builtins.str]:
            '''The message template for SMS messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html#cfn-cognito-userpool-invitemessagetemplate-smsmessage
            '''
            result = self._values.get("sms_message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InviteMessageTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.LambdaConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "create_auth_challenge": "createAuthChallenge",
            "custom_email_sender": "customEmailSender",
            "custom_message": "customMessage",
            "custom_sms_sender": "customSmsSender",
            "define_auth_challenge": "defineAuthChallenge",
            "kms_key_id": "kmsKeyId",
            "post_authentication": "postAuthentication",
            "post_confirmation": "postConfirmation",
            "pre_authentication": "preAuthentication",
            "pre_sign_up": "preSignUp",
            "pre_token_generation": "preTokenGeneration",
            "pre_token_generation_config": "preTokenGenerationConfig",
            "user_migration": "userMigration",
            "verify_auth_challenge_response": "verifyAuthChallengeResponse",
        },
    )
    class LambdaConfigProperty:
        def __init__(
            self,
            *,
            create_auth_challenge: typing.Optional[builtins.str] = None,
            custom_email_sender: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.CustomEmailSenderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_message: typing.Optional[builtins.str] = None,
            custom_sms_sender: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.CustomSMSSenderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            define_auth_challenge: typing.Optional[builtins.str] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
            post_authentication: typing.Optional[builtins.str] = None,
            post_confirmation: typing.Optional[builtins.str] = None,
            pre_authentication: typing.Optional[builtins.str] = None,
            pre_sign_up: typing.Optional[builtins.str] = None,
            pre_token_generation: typing.Optional[builtins.str] = None,
            pre_token_generation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.PreTokenGenerationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            user_migration: typing.Optional[builtins.str] = None,
            verify_auth_challenge_response: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A collection of user pool Lambda triggers.

            Amazon Cognito invokes triggers at several possible stages of user pool operations. Triggers can modify the outcome of the operations that invoked them.

            :param create_auth_challenge: The configuration of a create auth challenge Lambda trigger, one of three triggers in the sequence of the `custom authentication challenge triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html>`_ .
            :param custom_email_sender: The configuration of a custom email sender Lambda trigger. This trigger routes all email notifications from a user pool to a Lambda function that delivers the message using custom logic.
            :param custom_message: A custom message Lambda trigger. This trigger is an opportunity to customize all SMS and email messages from your user pool. When a custom message trigger is active, your user pool routes all messages to a Lambda function that returns a runtime-customized message subject and body for your user pool to deliver to a user.
            :param custom_sms_sender: The configuration of a custom SMS sender Lambda trigger. This trigger routes all SMS notifications from a user pool to a Lambda function that delivers the message using custom logic.
            :param define_auth_challenge: The configuration of a define auth challenge Lambda trigger, one of three triggers in the sequence of the `custom authentication challenge triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html>`_ .
            :param kms_key_id: The ARN of an `KMS key <https://docs.aws.amazon.com//kms/latest/developerguide/concepts.html#master_keys>`_ . Amazon Cognito uses the key to encrypt codes and temporary passwords sent to custom sender Lambda triggers.
            :param post_authentication: The configuration of a `post authentication Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-authentication.html>`_ in a user pool. This trigger can take custom actions after a user signs in.
            :param post_confirmation: The configuration of a `post confirmation Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-confirmation.html>`_ in a user pool. This trigger can take custom actions after a user confirms their user account and their email address or phone number.
            :param pre_authentication: The configuration of a `pre authentication trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-authentication.html>`_ in a user pool. This trigger can evaluate and modify user sign-in events.
            :param pre_sign_up: The configuration of a `pre sign-up Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html>`_ in a user pool. This trigger evaluates new users and can bypass confirmation, `link a federated user profile <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-identity-federation-consolidate-users.html>`_ , or block sign-up requests.
            :param pre_token_generation: The legacy configuration of a `pre token generation Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html>`_ in a user pool. Set this parameter for legacy purposes. If you also set an ARN in ``PreTokenGenerationConfig`` , its value must be identical to ``PreTokenGeneration`` . For new instances of pre token generation triggers, set the ``LambdaArn`` of ``PreTokenGenerationConfig`` .
            :param pre_token_generation_config: The detailed configuration of a `pre token generation Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html>`_ in a user pool. If you also set an ARN in ``PreTokenGeneration`` , its value must be identical to ``PreTokenGenerationConfig`` .
            :param user_migration: The configuration of a `migrate user Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-migrate-user.html>`_ in a user pool. This trigger can create user profiles when users sign in or attempt to reset their password with credentials that don't exist yet.
            :param verify_auth_challenge_response: The configuration of a verify auth challenge Lambda trigger, one of three triggers in the sequence of the `custom authentication challenge triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                lambda_config_property = cognito_mixins.CfnUserPoolPropsMixin.LambdaConfigProperty(
                    create_auth_challenge="createAuthChallenge",
                    custom_email_sender=cognito_mixins.CfnUserPoolPropsMixin.CustomEmailSenderProperty(
                        lambda_arn="lambdaArn",
                        lambda_version="lambdaVersion"
                    ),
                    custom_message="customMessage",
                    custom_sms_sender=cognito_mixins.CfnUserPoolPropsMixin.CustomSMSSenderProperty(
                        lambda_arn="lambdaArn",
                        lambda_version="lambdaVersion"
                    ),
                    define_auth_challenge="defineAuthChallenge",
                    kms_key_id="kmsKeyId",
                    post_authentication="postAuthentication",
                    post_confirmation="postConfirmation",
                    pre_authentication="preAuthentication",
                    pre_sign_up="preSignUp",
                    pre_token_generation="preTokenGeneration",
                    pre_token_generation_config=cognito_mixins.CfnUserPoolPropsMixin.PreTokenGenerationConfigProperty(
                        lambda_arn="lambdaArn",
                        lambda_version="lambdaVersion"
                    ),
                    user_migration="userMigration",
                    verify_auth_challenge_response="verifyAuthChallengeResponse"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65103e5cf2c7380c0ecd07f02f4a4c1ea091a78147746bd7a57a2fd49a6fc886)
                check_type(argname="argument create_auth_challenge", value=create_auth_challenge, expected_type=type_hints["create_auth_challenge"])
                check_type(argname="argument custom_email_sender", value=custom_email_sender, expected_type=type_hints["custom_email_sender"])
                check_type(argname="argument custom_message", value=custom_message, expected_type=type_hints["custom_message"])
                check_type(argname="argument custom_sms_sender", value=custom_sms_sender, expected_type=type_hints["custom_sms_sender"])
                check_type(argname="argument define_auth_challenge", value=define_auth_challenge, expected_type=type_hints["define_auth_challenge"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument post_authentication", value=post_authentication, expected_type=type_hints["post_authentication"])
                check_type(argname="argument post_confirmation", value=post_confirmation, expected_type=type_hints["post_confirmation"])
                check_type(argname="argument pre_authentication", value=pre_authentication, expected_type=type_hints["pre_authentication"])
                check_type(argname="argument pre_sign_up", value=pre_sign_up, expected_type=type_hints["pre_sign_up"])
                check_type(argname="argument pre_token_generation", value=pre_token_generation, expected_type=type_hints["pre_token_generation"])
                check_type(argname="argument pre_token_generation_config", value=pre_token_generation_config, expected_type=type_hints["pre_token_generation_config"])
                check_type(argname="argument user_migration", value=user_migration, expected_type=type_hints["user_migration"])
                check_type(argname="argument verify_auth_challenge_response", value=verify_auth_challenge_response, expected_type=type_hints["verify_auth_challenge_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if create_auth_challenge is not None:
                self._values["create_auth_challenge"] = create_auth_challenge
            if custom_email_sender is not None:
                self._values["custom_email_sender"] = custom_email_sender
            if custom_message is not None:
                self._values["custom_message"] = custom_message
            if custom_sms_sender is not None:
                self._values["custom_sms_sender"] = custom_sms_sender
            if define_auth_challenge is not None:
                self._values["define_auth_challenge"] = define_auth_challenge
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if post_authentication is not None:
                self._values["post_authentication"] = post_authentication
            if post_confirmation is not None:
                self._values["post_confirmation"] = post_confirmation
            if pre_authentication is not None:
                self._values["pre_authentication"] = pre_authentication
            if pre_sign_up is not None:
                self._values["pre_sign_up"] = pre_sign_up
            if pre_token_generation is not None:
                self._values["pre_token_generation"] = pre_token_generation
            if pre_token_generation_config is not None:
                self._values["pre_token_generation_config"] = pre_token_generation_config
            if user_migration is not None:
                self._values["user_migration"] = user_migration
            if verify_auth_challenge_response is not None:
                self._values["verify_auth_challenge_response"] = verify_auth_challenge_response

        @builtins.property
        def create_auth_challenge(self) -> typing.Optional[builtins.str]:
            '''The configuration of a create auth challenge Lambda trigger, one of three triggers in the sequence of the `custom authentication challenge triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-createauthchallenge
            '''
            result = self._values.get("create_auth_challenge")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_email_sender(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.CustomEmailSenderProperty"]]:
            '''The configuration of a custom email sender Lambda trigger.

            This trigger routes all email notifications from a user pool to a Lambda function that delivers the message using custom logic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-customemailsender
            '''
            result = self._values.get("custom_email_sender")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.CustomEmailSenderProperty"]], result)

        @builtins.property
        def custom_message(self) -> typing.Optional[builtins.str]:
            '''A custom message Lambda trigger.

            This trigger is an opportunity to customize all SMS and email messages from your user pool. When a custom message trigger is active, your user pool routes all messages to a Lambda function that returns a runtime-customized message subject and body for your user pool to deliver to a user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-custommessage
            '''
            result = self._values.get("custom_message")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_sms_sender(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.CustomSMSSenderProperty"]]:
            '''The configuration of a custom SMS sender Lambda trigger.

            This trigger routes all SMS notifications from a user pool to a Lambda function that delivers the message using custom logic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-customsmssender
            '''
            result = self._values.get("custom_sms_sender")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.CustomSMSSenderProperty"]], result)

        @builtins.property
        def define_auth_challenge(self) -> typing.Optional[builtins.str]:
            '''The configuration of a define auth challenge Lambda trigger, one of three triggers in the sequence of the `custom authentication challenge triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-defineauthchallenge
            '''
            result = self._values.get("define_auth_challenge")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ARN of an `KMS key <https://docs.aws.amazon.com//kms/latest/developerguide/concepts.html#master_keys>`_ . Amazon Cognito uses the key to encrypt codes and temporary passwords sent to custom sender Lambda triggers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def post_authentication(self) -> typing.Optional[builtins.str]:
            '''The configuration of a `post authentication Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-authentication.html>`_ in a user pool. This trigger can take custom actions after a user signs in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-postauthentication
            '''
            result = self._values.get("post_authentication")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def post_confirmation(self) -> typing.Optional[builtins.str]:
            '''The configuration of a `post confirmation Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-confirmation.html>`_ in a user pool. This trigger can take custom actions after a user confirms their user account and their email address or phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-postconfirmation
            '''
            result = self._values.get("post_confirmation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pre_authentication(self) -> typing.Optional[builtins.str]:
            '''The configuration of a `pre authentication trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-authentication.html>`_ in a user pool. This trigger can evaluate and modify user sign-in events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-preauthentication
            '''
            result = self._values.get("pre_authentication")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pre_sign_up(self) -> typing.Optional[builtins.str]:
            '''The configuration of a `pre sign-up Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html>`_ in a user pool. This trigger evaluates new users and can bypass confirmation, `link a federated user profile <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-identity-federation-consolidate-users.html>`_ , or block sign-up requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-presignup
            '''
            result = self._values.get("pre_sign_up")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pre_token_generation(self) -> typing.Optional[builtins.str]:
            '''The legacy configuration of a `pre token generation Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html>`_ in a user pool.

            Set this parameter for legacy purposes. If you also set an ARN in ``PreTokenGenerationConfig`` , its value must be identical to ``PreTokenGeneration`` . For new instances of pre token generation triggers, set the ``LambdaArn`` of ``PreTokenGenerationConfig`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-pretokengeneration
            '''
            result = self._values.get("pre_token_generation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pre_token_generation_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.PreTokenGenerationConfigProperty"]]:
            '''The detailed configuration of a `pre token generation Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html>`_ in a user pool. If you also set an ARN in ``PreTokenGeneration`` , its value must be identical to ``PreTokenGenerationConfig`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-pretokengenerationconfig
            '''
            result = self._values.get("pre_token_generation_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.PreTokenGenerationConfigProperty"]], result)

        @builtins.property
        def user_migration(self) -> typing.Optional[builtins.str]:
            '''The configuration of a `migrate user Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-migrate-user.html>`_ in a user pool. This trigger can create user profiles when users sign in or attempt to reset their password with credentials that don't exist yet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-usermigration
            '''
            result = self._values.get("user_migration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def verify_auth_challenge_response(self) -> typing.Optional[builtins.str]:
            '''The configuration of a verify auth challenge Lambda trigger, one of three triggers in the sequence of the `custom authentication challenge triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-verifyauthchallengeresponse
            '''
            result = self._values.get("verify_auth_challenge_response")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.NumberAttributeConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"max_value": "maxValue", "min_value": "minValue"},
    )
    class NumberAttributeConstraintsProperty:
        def __init__(
            self,
            *,
            max_value: typing.Optional[builtins.str] = None,
            min_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The minimum and maximum values of an attribute that is of the number type, for example ``custom:age`` .

            :param max_value: The maximum length of a number attribute value. Must be a number less than or equal to ``2^1023`` , represented as a string with a length of 131072 characters or fewer.
            :param min_value: The minimum value of an attribute that is of the number data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-numberattributeconstraints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                number_attribute_constraints_property = cognito_mixins.CfnUserPoolPropsMixin.NumberAttributeConstraintsProperty(
                    max_value="maxValue",
                    min_value="minValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89988d61e2f0a35f24155e7f199b54a505941559e2a182b2636f18cb32474a4a)
                check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
                check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_value is not None:
                self._values["max_value"] = max_value
            if min_value is not None:
                self._values["min_value"] = min_value

        @builtins.property
        def max_value(self) -> typing.Optional[builtins.str]:
            '''The maximum length of a number attribute value.

            Must be a number less than or equal to ``2^1023`` , represented as a string with a length of 131072 characters or fewer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-numberattributeconstraints.html#cfn-cognito-userpool-numberattributeconstraints-maxvalue
            '''
            result = self._values.get("max_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def min_value(self) -> typing.Optional[builtins.str]:
            '''The minimum value of an attribute that is of the number data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-numberattributeconstraints.html#cfn-cognito-userpool-numberattributeconstraints-minvalue
            '''
            result = self._values.get("min_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NumberAttributeConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.PasswordPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "minimum_length": "minimumLength",
            "password_history_size": "passwordHistorySize",
            "require_lowercase": "requireLowercase",
            "require_numbers": "requireNumbers",
            "require_symbols": "requireSymbols",
            "require_uppercase": "requireUppercase",
            "temporary_password_validity_days": "temporaryPasswordValidityDays",
        },
    )
    class PasswordPolicyProperty:
        def __init__(
            self,
            *,
            minimum_length: typing.Optional[jsii.Number] = None,
            password_history_size: typing.Optional[jsii.Number] = None,
            require_lowercase: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_numbers: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_symbols: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_uppercase: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            temporary_password_validity_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The password policy settings for a user pool, including complexity, history, and length requirements.

            :param minimum_length: The minimum length of the password in the policy that you have set. This value can't be less than 6.
            :param password_history_size: The number of previous passwords that you want Amazon Cognito to restrict each user from reusing. Users can't set a password that matches any of ``n`` previous passwords, where ``n`` is the value of ``PasswordHistorySize`` .
            :param require_lowercase: The requirement in a password policy that users must include at least one lowercase letter in their password.
            :param require_numbers: The requirement in a password policy that users must include at least one number in their password.
            :param require_symbols: The requirement in a password policy that users must include at least one symbol in their password.
            :param require_uppercase: The requirement in a password policy that users must include at least one uppercase letter in their password.
            :param temporary_password_validity_days: The number of days a temporary password is valid in the password policy. If the user doesn't sign in during this time, an administrator must reset their password. Defaults to ``7`` . If you submit a value of ``0`` , Amazon Cognito treats it as a null value and sets ``TemporaryPasswordValidityDays`` to its default value. .. epigraph:: When you set ``TemporaryPasswordValidityDays`` for a user pool, you can no longer set a value for the legacy ``UnusedAccountValidityDays`` parameter in that user pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                password_policy_property = cognito_mixins.CfnUserPoolPropsMixin.PasswordPolicyProperty(
                    minimum_length=123,
                    password_history_size=123,
                    require_lowercase=False,
                    require_numbers=False,
                    require_symbols=False,
                    require_uppercase=False,
                    temporary_password_validity_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae3196a187243e4fad17f7d8bbb0b72212dfcd771265ecce6669519d4aef2e1b)
                check_type(argname="argument minimum_length", value=minimum_length, expected_type=type_hints["minimum_length"])
                check_type(argname="argument password_history_size", value=password_history_size, expected_type=type_hints["password_history_size"])
                check_type(argname="argument require_lowercase", value=require_lowercase, expected_type=type_hints["require_lowercase"])
                check_type(argname="argument require_numbers", value=require_numbers, expected_type=type_hints["require_numbers"])
                check_type(argname="argument require_symbols", value=require_symbols, expected_type=type_hints["require_symbols"])
                check_type(argname="argument require_uppercase", value=require_uppercase, expected_type=type_hints["require_uppercase"])
                check_type(argname="argument temporary_password_validity_days", value=temporary_password_validity_days, expected_type=type_hints["temporary_password_validity_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if minimum_length is not None:
                self._values["minimum_length"] = minimum_length
            if password_history_size is not None:
                self._values["password_history_size"] = password_history_size
            if require_lowercase is not None:
                self._values["require_lowercase"] = require_lowercase
            if require_numbers is not None:
                self._values["require_numbers"] = require_numbers
            if require_symbols is not None:
                self._values["require_symbols"] = require_symbols
            if require_uppercase is not None:
                self._values["require_uppercase"] = require_uppercase
            if temporary_password_validity_days is not None:
                self._values["temporary_password_validity_days"] = temporary_password_validity_days

        @builtins.property
        def minimum_length(self) -> typing.Optional[jsii.Number]:
            '''The minimum length of the password in the policy that you have set.

            This value can't be less than 6.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-minimumlength
            '''
            result = self._values.get("minimum_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def password_history_size(self) -> typing.Optional[jsii.Number]:
            '''The number of previous passwords that you want Amazon Cognito to restrict each user from reusing.

            Users can't set a password that matches any of ``n`` previous passwords, where ``n`` is the value of ``PasswordHistorySize`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-passwordhistorysize
            '''
            result = self._values.get("password_history_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def require_lowercase(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The requirement in a password policy that users must include at least one lowercase letter in their password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requirelowercase
            '''
            result = self._values.get("require_lowercase")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_numbers(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The requirement in a password policy that users must include at least one number in their password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requirenumbers
            '''
            result = self._values.get("require_numbers")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_symbols(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The requirement in a password policy that users must include at least one symbol in their password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requiresymbols
            '''
            result = self._values.get("require_symbols")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_uppercase(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The requirement in a password policy that users must include at least one uppercase letter in their password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requireuppercase
            '''
            result = self._values.get("require_uppercase")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def temporary_password_validity_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days a temporary password is valid in the password policy.

            If the user doesn't sign in during this time, an administrator must reset their password. Defaults to ``7`` . If you submit a value of ``0`` , Amazon Cognito treats it as a null value and sets ``TemporaryPasswordValidityDays`` to its default value.
            .. epigraph::

               When you set ``TemporaryPasswordValidityDays`` for a user pool, you can no longer set a value for the legacy ``UnusedAccountValidityDays`` parameter in that user pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-temporarypasswordvaliditydays
            '''
            result = self._values.get("temporary_password_validity_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PasswordPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.PoliciesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password_policy": "passwordPolicy",
            "sign_in_policy": "signInPolicy",
        },
    )
    class PoliciesProperty:
        def __init__(
            self,
            *,
            password_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.PasswordPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sign_in_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.SignInPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A list of user pool policies.

            Contains the policy that sets password-complexity requirements.

            :param password_policy: The password policy settings for a user pool, including complexity, history, and length requirements.
            :param sign_in_policy: The policy for allowed types of authentication in a user pool. To activate this setting, your user pool must be in the `Essentials tier <https://docs.aws.amazon.com/cognito/latest/developerguide/feature-plans-features-essentials.html>`_ or higher.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-policies.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                policies_property = cognito_mixins.CfnUserPoolPropsMixin.PoliciesProperty(
                    password_policy=cognito_mixins.CfnUserPoolPropsMixin.PasswordPolicyProperty(
                        minimum_length=123,
                        password_history_size=123,
                        require_lowercase=False,
                        require_numbers=False,
                        require_symbols=False,
                        require_uppercase=False,
                        temporary_password_validity_days=123
                    ),
                    sign_in_policy=cognito_mixins.CfnUserPoolPropsMixin.SignInPolicyProperty(
                        allowed_first_auth_factors=["allowedFirstAuthFactors"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f3ae7f7d28fac3a4c70fe4ce669b7df7f18177b066f44ebfa9563dee7a54d41)
                check_type(argname="argument password_policy", value=password_policy, expected_type=type_hints["password_policy"])
                check_type(argname="argument sign_in_policy", value=sign_in_policy, expected_type=type_hints["sign_in_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password_policy is not None:
                self._values["password_policy"] = password_policy
            if sign_in_policy is not None:
                self._values["sign_in_policy"] = sign_in_policy

        @builtins.property
        def password_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.PasswordPolicyProperty"]]:
            '''The password policy settings for a user pool, including complexity, history, and length requirements.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-policies.html#cfn-cognito-userpool-policies-passwordpolicy
            '''
            result = self._values.get("password_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.PasswordPolicyProperty"]], result)

        @builtins.property
        def sign_in_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.SignInPolicyProperty"]]:
            '''The policy for allowed types of authentication in a user pool.

            To activate this setting, your user pool must be in the `Essentials tier <https://docs.aws.amazon.com/cognito/latest/developerguide/feature-plans-features-essentials.html>`_ or higher.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-policies.html#cfn-cognito-userpool-policies-signinpolicy
            '''
            result = self._values.get("sign_in_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.SignInPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PoliciesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.PreTokenGenerationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_arn": "lambdaArn", "lambda_version": "lambdaVersion"},
    )
    class PreTokenGenerationConfigProperty:
        def __init__(
            self,
            *,
            lambda_arn: typing.Optional[builtins.str] = None,
            lambda_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties of a pre token generation Lambda trigger.

            :param lambda_arn: The Amazon Resource Name (ARN) of the function that you want to assign to your Lambda trigger. This parameter and the ``PreTokenGeneration`` property of ``LambdaConfig`` have the same value. For new instances of pre token generation triggers, set ``LambdaArn`` .
            :param lambda_version: The user pool trigger version of the request that Amazon Cognito sends to your Lambda function. Higher-numbered versions add fields that support new features.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-pretokengenerationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                pre_token_generation_config_property = cognito_mixins.CfnUserPoolPropsMixin.PreTokenGenerationConfigProperty(
                    lambda_arn="lambdaArn",
                    lambda_version="lambdaVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f85ba6f0c51363de6ace5233467621d3bdfbda2a6e1a72957682753d3733956)
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
                check_type(argname="argument lambda_version", value=lambda_version, expected_type=type_hints["lambda_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn
            if lambda_version is not None:
                self._values["lambda_version"] = lambda_version

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the function that you want to assign to your Lambda trigger.

            This parameter and the ``PreTokenGeneration`` property of ``LambdaConfig`` have the same value. For new instances of pre token generation triggers, set ``LambdaArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-pretokengenerationconfig.html#cfn-cognito-userpool-pretokengenerationconfig-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_version(self) -> typing.Optional[builtins.str]:
            '''The user pool trigger version of the request that Amazon Cognito sends to your Lambda function.

            Higher-numbered versions add fields that support new features.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-pretokengenerationconfig.html#cfn-cognito-userpool-pretokengenerationconfig-lambdaversion
            '''
            result = self._values.get("lambda_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PreTokenGenerationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.RecoveryOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "priority": "priority"},
    )
    class RecoveryOptionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A recovery option for a user.

            The ``AccountRecoverySettingType`` data type is an array of this object. Each ``RecoveryOptionType`` has a priority property that determines whether it is a primary or secondary option.

            For example, if ``verified_email`` has a priority of ``1`` and ``verified_phone_number`` has a priority of ``2`` , your user pool sends account-recovery messages to a verified email address but falls back to an SMS message if the user has a verified phone number. The ``admin_only`` option prevents self-service account recovery.

            :param name: The recovery method that this object sets a recovery option for.
            :param priority: Your priority preference for using the specified attribute in account recovery. The highest priority is ``1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-recoveryoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                recovery_option_property = cognito_mixins.CfnUserPoolPropsMixin.RecoveryOptionProperty(
                    name="name",
                    priority=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a0922a3d3f95cada5344420464005a99f31eeb5f2d43801f6bb21432f9fd0baf)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if priority is not None:
                self._values["priority"] = priority

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The recovery method that this object sets a recovery option for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-recoveryoption.html#cfn-cognito-userpool-recoveryoption-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''Your priority preference for using the specified attribute in account recovery.

            The highest priority is ``1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-recoveryoption.html#cfn-cognito-userpool-recoveryoption-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecoveryOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.SchemaAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_data_type": "attributeDataType",
            "developer_only_attribute": "developerOnlyAttribute",
            "mutable": "mutable",
            "name": "name",
            "number_attribute_constraints": "numberAttributeConstraints",
            "required": "required",
            "string_attribute_constraints": "stringAttributeConstraints",
        },
    )
    class SchemaAttributeProperty:
        def __init__(
            self,
            *,
            attribute_data_type: typing.Optional[builtins.str] = None,
            developer_only_attribute: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            mutable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
            number_attribute_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.NumberAttributeConstraintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            string_attribute_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.StringAttributeConstraintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A list of the user attributes and their properties in your user pool.

            The attribute schema contains standard attributes, custom attributes with a ``custom:`` prefix, and developer attributes with a ``dev:`` prefix. For more information, see `User pool attributes <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html>`_ .

            Developer-only ``dev:`` attributes are a legacy feature of user pools, and are read-only to all app clients. You can create and update developer-only attributes only with IAM-authenticated API operations. Use app client read/write permissions instead.

            :param attribute_data_type: The data format of the values for your attribute. When you choose an ``AttributeDataType`` , Amazon Cognito validates the input against the data type. A custom attribute value in your user's ID token is always a string, for example ``"custom:isMember" : "true"`` or ``"custom:YearsAsMember" : "12"`` .
            :param developer_only_attribute: .. epigraph:: You should use `WriteAttributes <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UserPoolClientType.html#CognitoUserPools-Type-UserPoolClientType-WriteAttributes>`_ in the user pool client to control how attributes can be mutated for new use cases instead of using ``DeveloperOnlyAttribute`` . Specifies whether the attribute type is developer only. This attribute can only be modified by an administrator. Users won't be able to modify this attribute using their access token. For example, ``DeveloperOnlyAttribute`` can be modified using AdminUpdateUserAttributes but can't be updated using UpdateUserAttributes.
            :param mutable: Specifies whether the value of the attribute can be changed. Any user pool attribute whose value you map from an IdP attribute must be mutable, with a parameter value of ``true`` . Amazon Cognito updates mapped attributes when users sign in to your application through an IdP. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. For more information, see `Specifying Identity Provider Attribute Mappings for Your User Pool <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-specifying-attribute-mapping.html>`_ .
            :param name: The name of your user pool attribute. When you create or update a user pool, adding a schema attribute creates a custom or developer-only attribute. When you add an attribute with a ``Name`` value of ``MyAttribute`` , Amazon Cognito creates the custom attribute ``custom:MyAttribute`` . When ``DeveloperOnlyAttribute`` is ``true`` , Amazon Cognito creates your attribute as ``dev:MyAttribute`` . In an operation that describes a user pool, Amazon Cognito returns this value as ``value`` for standard attributes, ``custom:value`` for custom attributes, and ``dev:value`` for developer-only attributes..
            :param number_attribute_constraints: Specifies the constraints for an attribute of the number type.
            :param required: Specifies whether a user pool attribute is required. If the attribute is required and the user doesn't provide a value, registration or sign-in will fail.
            :param string_attribute_constraints: Specifies the constraints for an attribute of the string type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                schema_attribute_property = cognito_mixins.CfnUserPoolPropsMixin.SchemaAttributeProperty(
                    attribute_data_type="attributeDataType",
                    developer_only_attribute=False,
                    mutable=False,
                    name="name",
                    number_attribute_constraints=cognito_mixins.CfnUserPoolPropsMixin.NumberAttributeConstraintsProperty(
                        max_value="maxValue",
                        min_value="minValue"
                    ),
                    required=False,
                    string_attribute_constraints=cognito_mixins.CfnUserPoolPropsMixin.StringAttributeConstraintsProperty(
                        max_length="maxLength",
                        min_length="minLength"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f193ffa1c73e08598e11778b2fa6daf2e97ecb8d5dba9faaa8663b157e3e5b62)
                check_type(argname="argument attribute_data_type", value=attribute_data_type, expected_type=type_hints["attribute_data_type"])
                check_type(argname="argument developer_only_attribute", value=developer_only_attribute, expected_type=type_hints["developer_only_attribute"])
                check_type(argname="argument mutable", value=mutable, expected_type=type_hints["mutable"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument number_attribute_constraints", value=number_attribute_constraints, expected_type=type_hints["number_attribute_constraints"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
                check_type(argname="argument string_attribute_constraints", value=string_attribute_constraints, expected_type=type_hints["string_attribute_constraints"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_data_type is not None:
                self._values["attribute_data_type"] = attribute_data_type
            if developer_only_attribute is not None:
                self._values["developer_only_attribute"] = developer_only_attribute
            if mutable is not None:
                self._values["mutable"] = mutable
            if name is not None:
                self._values["name"] = name
            if number_attribute_constraints is not None:
                self._values["number_attribute_constraints"] = number_attribute_constraints
            if required is not None:
                self._values["required"] = required
            if string_attribute_constraints is not None:
                self._values["string_attribute_constraints"] = string_attribute_constraints

        @builtins.property
        def attribute_data_type(self) -> typing.Optional[builtins.str]:
            '''The data format of the values for your attribute.

            When you choose an ``AttributeDataType`` , Amazon Cognito validates the input against the data type. A custom attribute value in your user's ID token is always a string, for example ``"custom:isMember" : "true"`` or ``"custom:YearsAsMember" : "12"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-attributedatatype
            '''
            result = self._values.get("attribute_data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def developer_only_attribute(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''.. epigraph::

   You should use `WriteAttributes <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UserPoolClientType.html#CognitoUserPools-Type-UserPoolClientType-WriteAttributes>`_ in the user pool client to control how attributes can be mutated for new use cases instead of using ``DeveloperOnlyAttribute`` .

            Specifies whether the attribute type is developer only. This attribute can only be modified by an administrator. Users won't be able to modify this attribute using their access token. For example, ``DeveloperOnlyAttribute`` can be modified using AdminUpdateUserAttributes but can't be updated using UpdateUserAttributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-developeronlyattribute
            '''
            result = self._values.get("developer_only_attribute")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def mutable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the value of the attribute can be changed.

            Any user pool attribute whose value you map from an IdP attribute must be mutable, with a parameter value of ``true`` . Amazon Cognito updates mapped attributes when users sign in to your application through an IdP. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. For more information, see `Specifying Identity Provider Attribute Mappings for Your User Pool <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-specifying-attribute-mapping.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-mutable
            '''
            result = self._values.get("mutable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of your user pool attribute.

            When you create or update a user pool, adding a schema attribute creates a custom or developer-only attribute. When you add an attribute with a ``Name`` value of ``MyAttribute`` , Amazon Cognito creates the custom attribute ``custom:MyAttribute`` . When ``DeveloperOnlyAttribute`` is ``true`` , Amazon Cognito creates your attribute as ``dev:MyAttribute`` . In an operation that describes a user pool, Amazon Cognito returns this value as ``value`` for standard attributes, ``custom:value`` for custom attributes, and ``dev:value`` for developer-only attributes..

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def number_attribute_constraints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.NumberAttributeConstraintsProperty"]]:
            '''Specifies the constraints for an attribute of the number type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-numberattributeconstraints
            '''
            result = self._values.get("number_attribute_constraints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.NumberAttributeConstraintsProperty"]], result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a user pool attribute is required.

            If the attribute is required and the user doesn't provide a value, registration or sign-in will fail.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def string_attribute_constraints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.StringAttributeConstraintsProperty"]]:
            '''Specifies the constraints for an attribute of the string type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-stringattributeconstraints
            '''
            result = self._values.get("string_attribute_constraints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.StringAttributeConstraintsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.SignInPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"allowed_first_auth_factors": "allowedFirstAuthFactors"},
    )
    class SignInPolicyProperty:
        def __init__(
            self,
            *,
            allowed_first_auth_factors: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The policy for allowed types of authentication in a user pool.

            To activate this setting, your user pool must be in the `Essentials tier <https://docs.aws.amazon.com/cognito/latest/developerguide/feature-plans-features-essentials.html>`_ or higher.

            :param allowed_first_auth_factors: The sign-in methods that a user pool supports as the first factor. You can permit users to start authentication with a standard username and password, or with other one-time password and hardware factors. Supports values of ``EMAIL_OTP`` , ``SMS_OTP`` , ``WEB_AUTHN`` and ``PASSWORD`` ,

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-signinpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                sign_in_policy_property = cognito_mixins.CfnUserPoolPropsMixin.SignInPolicyProperty(
                    allowed_first_auth_factors=["allowedFirstAuthFactors"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d315d482fe59a2097c8690f5629d1a758b692bfd959c9e4c5d739226a57d0754)
                check_type(argname="argument allowed_first_auth_factors", value=allowed_first_auth_factors, expected_type=type_hints["allowed_first_auth_factors"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_first_auth_factors is not None:
                self._values["allowed_first_auth_factors"] = allowed_first_auth_factors

        @builtins.property
        def allowed_first_auth_factors(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The sign-in methods that a user pool supports as the first factor.

            You can permit users to start authentication with a standard username and password, or with other one-time password and hardware factors.

            Supports values of ``EMAIL_OTP`` , ``SMS_OTP`` , ``WEB_AUTHN`` and ``PASSWORD`` ,

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-signinpolicy.html#cfn-cognito-userpool-signinpolicy-allowedfirstauthfactors
            '''
            result = self._values.get("allowed_first_auth_factors")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignInPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.SmsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "external_id": "externalId",
            "sns_caller_arn": "snsCallerArn",
            "sns_region": "snsRegion",
        },
    )
    class SmsConfigurationProperty:
        def __init__(
            self,
            *,
            external_id: typing.Optional[builtins.str] = None,
            sns_caller_arn: typing.Optional[builtins.str] = None,
            sns_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''User pool configuration for delivery of SMS messages with Amazon Simple Notification Service.

            To send SMS messages with Amazon SNS in the AWS Region that you want, the Amazon Cognito user pool uses an AWS Identity and Access Management (IAM) role in your AWS account .

            :param external_id: The external ID provides additional security for your IAM role. You can use an ``ExternalId`` with the IAM role that you use with Amazon SNS to send SMS messages for your user pool. If you provide an ``ExternalId`` , your Amazon Cognito user pool includes it in the request to assume your IAM role. You can configure the role trust policy to require that Amazon Cognito, and any principal, provide the ``ExternalID`` . If you use the Amazon Cognito Management Console to create a role for SMS multi-factor authentication (MFA), Amazon Cognito creates a role with the required permissions and a trust policy that demonstrates use of the ``ExternalId`` . For more information about the ``ExternalId`` of a role, see `How to use an external ID when granting access to your AWS resources to a third party <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html>`_ .
            :param sns_caller_arn: The Amazon Resource Name (ARN) of the Amazon SNS caller. This is the ARN of the IAM role in your AWS account that Amazon Cognito will use to send SMS messages. SMS messages are subject to a `spending limit <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-email-phone-verification.html>`_ .
            :param sns_region: The AWS Region to use with Amazon SNS integration. You can choose the same Region as your user pool, or a supported *Legacy Amazon SNS alternate Region* . Amazon Cognito resources in the Asia Pacific (Seoul) AWS Region must use your Amazon SNS configuration in the Asia Pacific (Tokyo) Region. For more information, see `SMS message settings for Amazon Cognito user pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-smsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                sms_configuration_property = cognito_mixins.CfnUserPoolPropsMixin.SmsConfigurationProperty(
                    external_id="externalId",
                    sns_caller_arn="snsCallerArn",
                    sns_region="snsRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1aa14a5e3ca16a6ba478ce6806526d77db9c4300d404a57126ec544c2f0621c0)
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument sns_caller_arn", value=sns_caller_arn, expected_type=type_hints["sns_caller_arn"])
                check_type(argname="argument sns_region", value=sns_region, expected_type=type_hints["sns_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if external_id is not None:
                self._values["external_id"] = external_id
            if sns_caller_arn is not None:
                self._values["sns_caller_arn"] = sns_caller_arn
            if sns_region is not None:
                self._values["sns_region"] = sns_region

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID provides additional security for your IAM role.

            You can use an ``ExternalId`` with the IAM role that you use with Amazon SNS to send SMS messages for your user pool. If you provide an ``ExternalId`` , your Amazon Cognito user pool includes it in the request to assume your IAM role. You can configure the role trust policy to require that Amazon Cognito, and any principal, provide the ``ExternalID`` . If you use the Amazon Cognito Management Console to create a role for SMS multi-factor authentication (MFA), Amazon Cognito creates a role with the required permissions and a trust policy that demonstrates use of the ``ExternalId`` .

            For more information about the ``ExternalId`` of a role, see `How to use an external ID when granting access to your AWS resources to a third party <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-smsconfiguration.html#cfn-cognito-userpool-smsconfiguration-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sns_caller_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS caller.

            This is the ARN of the IAM role in your AWS account that Amazon Cognito will use to send SMS messages. SMS messages are subject to a `spending limit <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-email-phone-verification.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-smsconfiguration.html#cfn-cognito-userpool-smsconfiguration-snscallerarn
            '''
            result = self._values.get("sns_caller_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sns_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region to use with Amazon SNS integration.

            You can choose the same Region as your user pool, or a supported *Legacy Amazon SNS alternate Region* .

            Amazon Cognito resources in the Asia Pacific (Seoul) AWS Region must use your Amazon SNS configuration in the Asia Pacific (Tokyo) Region. For more information, see `SMS message settings for Amazon Cognito user pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-smsconfiguration.html#cfn-cognito-userpool-smsconfiguration-snsregion
            '''
            result = self._values.get("sns_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SmsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.StringAttributeConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"max_length": "maxLength", "min_length": "minLength"},
    )
    class StringAttributeConstraintsProperty:
        def __init__(
            self,
            *,
            max_length: typing.Optional[builtins.str] = None,
            min_length: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The minimum and maximum length values of an attribute that is of the string type, for example ``custom:department`` .

            :param max_length: The maximum length of a string attribute value. Must be a number less than or equal to ``2^1023`` , represented as a string with a length of 131072 characters or fewer.
            :param min_length: The minimum length of a string attribute value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-stringattributeconstraints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                string_attribute_constraints_property = cognito_mixins.CfnUserPoolPropsMixin.StringAttributeConstraintsProperty(
                    max_length="maxLength",
                    min_length="minLength"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__839792d52dc06409222f843bcf48e7733ed636508fa5cd1d8d128874214a3f84)
                check_type(argname="argument max_length", value=max_length, expected_type=type_hints["max_length"])
                check_type(argname="argument min_length", value=min_length, expected_type=type_hints["min_length"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_length is not None:
                self._values["max_length"] = max_length
            if min_length is not None:
                self._values["min_length"] = min_length

        @builtins.property
        def max_length(self) -> typing.Optional[builtins.str]:
            '''The maximum length of a string attribute value.

            Must be a number less than or equal to ``2^1023`` , represented as a string with a length of 131072 characters or fewer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-stringattributeconstraints.html#cfn-cognito-userpool-stringattributeconstraints-maxlength
            '''
            result = self._values.get("max_length")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def min_length(self) -> typing.Optional[builtins.str]:
            '''The minimum length of a string attribute value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-stringattributeconstraints.html#cfn-cognito-userpool-stringattributeconstraints-minlength
            '''
            result = self._values.get("min_length")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StringAttributeConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.UserAttributeUpdateSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes_require_verification_before_update": "attributesRequireVerificationBeforeUpdate",
        },
    )
    class UserAttributeUpdateSettingsProperty:
        def __init__(
            self,
            *,
            attributes_require_verification_before_update: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The settings for updates to user attributes.

            These settings include the property ``AttributesRequireVerificationBeforeUpdate`` ,
            a user-pool setting that tells Amazon Cognito how to handle changes to the value of your users' email address and phone number attributes. For
            more information, see `Verifying updates to email addresses and phone numbers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-email-phone-verification.html#user-pool-settings-verifications-verify-attribute-updates>`_ .

            :param attributes_require_verification_before_update: Requires that your user verifies their email address, phone number, or both before Amazon Cognito updates the value of that attribute. When you update a user attribute that has this option activated, Amazon Cognito sends a verification message to the new phone number or email address. Amazon Cognito doesn’t change the value of the attribute until your user responds to the verification message and confirms the new value. When ``AttributesRequireVerificationBeforeUpdate`` is false, your user pool doesn't require that your users verify attribute changes before Amazon Cognito updates them. In a user pool where ``AttributesRequireVerificationBeforeUpdate`` is false, API operations that change attribute values can immediately update a user’s ``email`` or ``phone_number`` attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-userattributeupdatesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                user_attribute_update_settings_property = cognito_mixins.CfnUserPoolPropsMixin.UserAttributeUpdateSettingsProperty(
                    attributes_require_verification_before_update=["attributesRequireVerificationBeforeUpdate"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4a904a94de7bbe7bc3c476ff8d4f61a27e9dc49fde101198f9e13c21272864a)
                check_type(argname="argument attributes_require_verification_before_update", value=attributes_require_verification_before_update, expected_type=type_hints["attributes_require_verification_before_update"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes_require_verification_before_update is not None:
                self._values["attributes_require_verification_before_update"] = attributes_require_verification_before_update

        @builtins.property
        def attributes_require_verification_before_update(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Requires that your user verifies their email address, phone number, or both before Amazon Cognito updates the value of that attribute.

            When you update a user attribute that has this option activated, Amazon Cognito sends a verification message to the new phone number or email address. Amazon Cognito doesn’t change the value of the attribute until your user responds to the verification message and confirms the new value.

            When ``AttributesRequireVerificationBeforeUpdate`` is false, your user pool doesn't require that your users verify attribute changes before Amazon Cognito updates them. In a user pool where ``AttributesRequireVerificationBeforeUpdate`` is false, API operations that change attribute values can immediately update a user’s ``email`` or ``phone_number`` attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-userattributeupdatesettings.html#cfn-cognito-userpool-userattributeupdatesettings-attributesrequireverificationbeforeupdate
            '''
            result = self._values.get("attributes_require_verification_before_update")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserAttributeUpdateSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.UserPoolAddOnsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "advanced_security_additional_flows": "advancedSecurityAdditionalFlows",
            "advanced_security_mode": "advancedSecurityMode",
        },
    )
    class UserPoolAddOnsProperty:
        def __init__(
            self,
            *,
            advanced_security_additional_flows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolPropsMixin.AdvancedSecurityAdditionalFlowsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            advanced_security_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''User pool add-ons.

            Contains settings for activation of threat protection. To log user security information but take no action, set to ``AUDIT`` . To configure automatic security responses to risky traffic to your user pool, set to ``ENFORCED`` .

            For more information, see `Adding advanced security to a user pool <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-advanced-security.html>`_ . To activate this setting, your user pool must be on the `Plus tier <https://docs.aws.amazon.com/cognito/latest/developerguide/feature-plans-features-plus.html>`_ .

            :param advanced_security_additional_flows: Threat protection configuration options for additional authentication types in your user pool, including custom authentication.
            :param advanced_security_mode: The operating mode of threat protection for standard authentication types in your user pool, including username-password and secure remote password (SRP) authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-userpooladdons.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                user_pool_add_ons_property = cognito_mixins.CfnUserPoolPropsMixin.UserPoolAddOnsProperty(
                    advanced_security_additional_flows=cognito_mixins.CfnUserPoolPropsMixin.AdvancedSecurityAdditionalFlowsProperty(
                        custom_auth_mode="customAuthMode"
                    ),
                    advanced_security_mode="advancedSecurityMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33bee5b6675cddb872158b231f7ad1d372edb7db236f886e9076fe9103227395)
                check_type(argname="argument advanced_security_additional_flows", value=advanced_security_additional_flows, expected_type=type_hints["advanced_security_additional_flows"])
                check_type(argname="argument advanced_security_mode", value=advanced_security_mode, expected_type=type_hints["advanced_security_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if advanced_security_additional_flows is not None:
                self._values["advanced_security_additional_flows"] = advanced_security_additional_flows
            if advanced_security_mode is not None:
                self._values["advanced_security_mode"] = advanced_security_mode

        @builtins.property
        def advanced_security_additional_flows(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.AdvancedSecurityAdditionalFlowsProperty"]]:
            '''Threat protection configuration options for additional authentication types in your user pool, including custom authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-userpooladdons.html#cfn-cognito-userpool-userpooladdons-advancedsecurityadditionalflows
            '''
            result = self._values.get("advanced_security_additional_flows")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolPropsMixin.AdvancedSecurityAdditionalFlowsProperty"]], result)

        @builtins.property
        def advanced_security_mode(self) -> typing.Optional[builtins.str]:
            '''The operating mode of threat protection for standard authentication types in your user pool, including username-password and secure remote password (SRP) authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-userpooladdons.html#cfn-cognito-userpool-userpooladdons-advancedsecuritymode
            '''
            result = self._values.get("advanced_security_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPoolAddOnsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.UsernameConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"case_sensitive": "caseSensitive"},
    )
    class UsernameConfigurationProperty:
        def __init__(
            self,
            *,
            case_sensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Case sensitivity of the username input for the selected sign-in option.

            When case sensitivity is set to ``False`` (case insensitive), users can sign in with any combination of capital and lowercase letters. For example, ``username`` , ``USERNAME`` , or ``UserName`` , or for email, ``email@example.com`` or ``EMaiL@eXamplE.Com`` . For most use cases, set case sensitivity to ``False`` (case insensitive) as a best practice. When usernames and email addresses are case insensitive, Amazon Cognito treats any variation in case as the same user, and prevents a case variation from being assigned to the same attribute for a different user.

            :param case_sensitive: Specifies whether user name case sensitivity will be applied for all users in the user pool through Amazon Cognito APIs. For most use cases, set case sensitivity to ``False`` (case insensitive) as a best practice. When usernames and email addresses are case insensitive, users can sign in as the same user when they enter a different capitalization of their user name. Valid values include: - **true** - Enables case sensitivity for all username input. When this option is set to ``true`` , users must sign in using the exact capitalization of their given username, such as “UserName”. This is the default value. - **false** - Enables case insensitivity for all username input. For example, when this option is set to ``false`` , users can sign in using ``username`` , ``USERNAME`` , or ``UserName`` . This option also enables both ``preferred_username`` and ``email`` alias to be case insensitive, in addition to the ``username`` attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-usernameconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                username_configuration_property = cognito_mixins.CfnUserPoolPropsMixin.UsernameConfigurationProperty(
                    case_sensitive=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6bf733e1fe322d182e7f5339a664e78eabf0b6ebfcaf4eb05d3f381eb3e14bce)
                check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if case_sensitive is not None:
                self._values["case_sensitive"] = case_sensitive

        @builtins.property
        def case_sensitive(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether user name case sensitivity will be applied for all users in the user pool through Amazon Cognito APIs.

            For most use cases, set case sensitivity to ``False`` (case insensitive) as a best practice. When usernames and email addresses are case insensitive, users can sign in as the same user when they enter a different capitalization of their user name.

            Valid values include:

            - **true** - Enables case sensitivity for all username input. When this option is set to ``true`` , users must sign in using the exact capitalization of their given username, such as “UserName”. This is the default value.
            - **false** - Enables case insensitivity for all username input. For example, when this option is set to ``false`` , users can sign in using ``username`` , ``USERNAME`` , or ``UserName`` . This option also enables both ``preferred_username`` and ``email`` alias to be case insensitive, in addition to the ``username`` attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-usernameconfiguration.html#cfn-cognito-userpool-usernameconfiguration-casesensitive
            '''
            result = self._values.get("case_sensitive")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UsernameConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolPropsMixin.VerificationMessageTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_email_option": "defaultEmailOption",
            "email_message": "emailMessage",
            "email_message_by_link": "emailMessageByLink",
            "email_subject": "emailSubject",
            "email_subject_by_link": "emailSubjectByLink",
            "sms_message": "smsMessage",
        },
    )
    class VerificationMessageTemplateProperty:
        def __init__(
            self,
            *,
            default_email_option: typing.Optional[builtins.str] = None,
            email_message: typing.Optional[builtins.str] = None,
            email_message_by_link: typing.Optional[builtins.str] = None,
            email_subject: typing.Optional[builtins.str] = None,
            email_subject_by_link: typing.Optional[builtins.str] = None,
            sms_message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The template for the verification message that your user pool delivers to users who set an email address or phone number attribute.

            :param default_email_option: The configuration of verification emails to contain a clickable link or a verification code. For link, your template body must contain link text in the format ``{##Click here##}`` . "Click here" in the example is a customizable string. For code, your template body must contain a code placeholder in the format ``{####}`` .
            :param email_message: The template for email messages that Amazon Cognito sends to your users. You can set an ``EmailMessage`` template only if the value of `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` . When your `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` , your user pool sends email messages with your own Amazon SES configuration.
            :param email_message_by_link: The email message template for sending a confirmation link to the user. You can set an ``EmailMessageByLink`` template only if the value of `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` . When your `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` , your user pool sends email messages with your own Amazon SES configuration.
            :param email_subject: The subject line for the email message template. You can set an ``EmailSubject`` template only if the value of `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` . When your `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` , your user pool sends email messages with your own Amazon SES configuration.
            :param email_subject_by_link: The subject line for the email message template for sending a confirmation link to the user. You can set an ``EmailSubjectByLink`` template only if the value of `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` . When your `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` , your user pool sends email messages with your own Amazon SES configuration.
            :param sms_message: The template for SMS messages that Amazon Cognito sends to your users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                verification_message_template_property = cognito_mixins.CfnUserPoolPropsMixin.VerificationMessageTemplateProperty(
                    default_email_option="defaultEmailOption",
                    email_message="emailMessage",
                    email_message_by_link="emailMessageByLink",
                    email_subject="emailSubject",
                    email_subject_by_link="emailSubjectByLink",
                    sms_message="smsMessage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9135c349e152da1db72c849369a0ba11f4e87df06249ba29adf2e8a6ba50602d)
                check_type(argname="argument default_email_option", value=default_email_option, expected_type=type_hints["default_email_option"])
                check_type(argname="argument email_message", value=email_message, expected_type=type_hints["email_message"])
                check_type(argname="argument email_message_by_link", value=email_message_by_link, expected_type=type_hints["email_message_by_link"])
                check_type(argname="argument email_subject", value=email_subject, expected_type=type_hints["email_subject"])
                check_type(argname="argument email_subject_by_link", value=email_subject_by_link, expected_type=type_hints["email_subject_by_link"])
                check_type(argname="argument sms_message", value=sms_message, expected_type=type_hints["sms_message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_email_option is not None:
                self._values["default_email_option"] = default_email_option
            if email_message is not None:
                self._values["email_message"] = email_message
            if email_message_by_link is not None:
                self._values["email_message_by_link"] = email_message_by_link
            if email_subject is not None:
                self._values["email_subject"] = email_subject
            if email_subject_by_link is not None:
                self._values["email_subject_by_link"] = email_subject_by_link
            if sms_message is not None:
                self._values["sms_message"] = sms_message

        @builtins.property
        def default_email_option(self) -> typing.Optional[builtins.str]:
            '''The configuration of verification emails to contain a clickable link or a verification code.

            For link, your template body must contain link text in the format ``{##Click here##}`` . "Click here" in the example is a customizable string. For code, your template body must contain a code placeholder in the format ``{####}`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-defaultemailoption
            '''
            result = self._values.get("default_email_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def email_message(self) -> typing.Optional[builtins.str]:
            '''The template for email messages that Amazon Cognito sends to your users.

            You can set an ``EmailMessage`` template only if the value of `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` . When your `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` , your user pool sends email messages with your own Amazon SES configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailmessage
            '''
            result = self._values.get("email_message")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def email_message_by_link(self) -> typing.Optional[builtins.str]:
            '''The email message template for sending a confirmation link to the user.

            You can set an ``EmailMessageByLink`` template only if the value of `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` . When your `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` , your user pool sends email messages with your own Amazon SES configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailmessagebylink
            '''
            result = self._values.get("email_message_by_link")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def email_subject(self) -> typing.Optional[builtins.str]:
            '''The subject line for the email message template.

            You can set an ``EmailSubject`` template only if the value of `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` . When your `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` , your user pool sends email messages with your own Amazon SES configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailsubject
            '''
            result = self._values.get("email_subject")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def email_subject_by_link(self) -> typing.Optional[builtins.str]:
            '''The subject line for the email message template for sending a confirmation link to the user.

            You can set an ``EmailSubjectByLink`` template only if the value of `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` . When your `EmailSendingAccount <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_EmailConfigurationType.html#CognitoUserPools-Type-EmailConfigurationType-EmailSendingAccount>`_ is ``DEVELOPER`` , your user pool sends email messages with your own Amazon SES configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailsubjectbylink
            '''
            result = self._values.get("email_subject_by_link")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sms_message(self) -> typing.Optional[builtins.str]:
            '''The template for SMS messages that Amazon Cognito sends to your users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-smsmessage
            '''
            result = self._values.get("sms_message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VerificationMessageTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolResourceServerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "identifier": "identifier",
        "name": "name",
        "scopes": "scopes",
        "user_pool_id": "userPoolId",
    },
)
class CfnUserPoolResourceServerMixinProps:
    def __init__(
        self,
        *,
        identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolResourceServerPropsMixin.ResourceServerScopeTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPoolResourceServerPropsMixin.

        :param identifier: A unique resource server identifier for the resource server. The identifier can be an API friendly name like ``solar-system-data`` . You can also set an API URL like ``https://solar-system-data-api.example.com`` as your identifier. Amazon Cognito represents scopes in the access token in the format ``$resource-server-identifier/$scope`` . Longer scope-identifier strings increase the size of your access tokens.
        :param name: A friendly name for the resource server.
        :param scopes: A list of scopes. Each scope is a map with keys ``ScopeName`` and ``ScopeDescription`` .
        :param user_pool_id: The ID of the user pool where you want to create a resource server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            cfn_user_pool_resource_server_mixin_props = cognito_mixins.CfnUserPoolResourceServerMixinProps(
                identifier="identifier",
                name="name",
                scopes=[cognito_mixins.CfnUserPoolResourceServerPropsMixin.ResourceServerScopeTypeProperty(
                    scope_description="scopeDescription",
                    scope_name="scopeName"
                )],
                user_pool_id="userPoolId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f22de66f81ae3a647fd8406b34be954145013bd316552668da42482a69789a4)
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identifier is not None:
            self._values["identifier"] = identifier
        if name is not None:
            self._values["name"] = name
        if scopes is not None:
            self._values["scopes"] = scopes
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        '''A unique resource server identifier for the resource server.

        The identifier can be an API friendly name like ``solar-system-data`` . You can also set an API URL like ``https://solar-system-data-api.example.com`` as your identifier.

        Amazon Cognito represents scopes in the access token in the format ``$resource-server-identifier/$scope`` . Longer scope-identifier strings increase the size of your access tokens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-identifier
        '''
        result = self._values.get("identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A friendly name for the resource server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolResourceServerPropsMixin.ResourceServerScopeTypeProperty"]]]]:
        '''A list of scopes.

        Each scope is a map with keys ``ScopeName`` and ``ScopeDescription`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-scopes
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolResourceServerPropsMixin.ResourceServerScopeTypeProperty"]]]], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user pool where you want to create a resource server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolResourceServerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolResourceServerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolResourceServerPropsMixin",
):
    '''The ``AWS::Cognito::UserPoolResourceServer`` resource creates a new OAuth2.0 resource server and defines custom scopes in it.

    .. epigraph::

       If you don't specify a value for a parameter, Amazon Cognito sets it to a default value.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html
    :cloudformationResource: AWS::Cognito::UserPoolResourceServer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_user_pool_resource_server_props_mixin = cognito_mixins.CfnUserPoolResourceServerPropsMixin(cognito_mixins.CfnUserPoolResourceServerMixinProps(
            identifier="identifier",
            name="name",
            scopes=[cognito_mixins.CfnUserPoolResourceServerPropsMixin.ResourceServerScopeTypeProperty(
                scope_description="scopeDescription",
                scope_name="scopeName"
            )],
            user_pool_id="userPoolId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPoolResourceServerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::UserPoolResourceServer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0770b40e72391a6c945a4ed8ca6914479c6e02713d6c3f8c73a8994bc011586b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a22928a86e5ba8adca1c7a422836b471d63104f95f4c5a01f4b9bea1cca683b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d592c676ee26f852399d3f880bc90920ae7a657f8a462664a9da626db4541025)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPoolResourceServerMixinProps:
        return typing.cast(CfnUserPoolResourceServerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolResourceServerPropsMixin.ResourceServerScopeTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "scope_description": "scopeDescription",
            "scope_name": "scopeName",
        },
    )
    class ResourceServerScopeTypeProperty:
        def __init__(
            self,
            *,
            scope_description: typing.Optional[builtins.str] = None,
            scope_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''One custom scope associated with a user pool resource server.

            This data type is a member of ``ResourceServerScopeType`` . For more information, see `Scopes, M2M, and API authorization with resource servers <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-define-resource-servers.html>`_ .

            :param scope_description: A friendly description of a custom scope.
            :param scope_name: The name of the scope. Amazon Cognito renders custom scopes in the format ``resourceServerIdentifier/ScopeName`` . For example, if this parameter is ``exampleScope`` in the resource server with the identifier ``exampleResourceServer`` , you request and receive the scope ``exampleResourceServer/exampleScope`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolresourceserver-resourceserverscopetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                resource_server_scope_type_property = cognito_mixins.CfnUserPoolResourceServerPropsMixin.ResourceServerScopeTypeProperty(
                    scope_description="scopeDescription",
                    scope_name="scopeName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fb6433e17ce7bfaaca2e01b8464c2c5bad4b5326ec0b8606692db302e34843bf)
                check_type(argname="argument scope_description", value=scope_description, expected_type=type_hints["scope_description"])
                check_type(argname="argument scope_name", value=scope_name, expected_type=type_hints["scope_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if scope_description is not None:
                self._values["scope_description"] = scope_description
            if scope_name is not None:
                self._values["scope_name"] = scope_name

        @builtins.property
        def scope_description(self) -> typing.Optional[builtins.str]:
            '''A friendly description of a custom scope.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolresourceserver-resourceserverscopetype.html#cfn-cognito-userpoolresourceserver-resourceserverscopetype-scopedescription
            '''
            result = self._values.get("scope_description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope_name(self) -> typing.Optional[builtins.str]:
            '''The name of the scope.

            Amazon Cognito renders custom scopes in the format ``resourceServerIdentifier/ScopeName`` . For example, if this parameter is ``exampleScope`` in the resource server with the identifier ``exampleResourceServer`` , you request and receive the scope ``exampleResourceServer/exampleScope`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolresourceserver-resourceserverscopetype.html#cfn-cognito-userpoolresourceserver-resourceserverscopetype-scopename
            '''
            result = self._values.get("scope_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceServerScopeTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolRiskConfigurationAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_takeover_risk_configuration": "accountTakeoverRiskConfiguration",
        "client_id": "clientId",
        "compromised_credentials_risk_configuration": "compromisedCredentialsRiskConfiguration",
        "risk_exception_configuration": "riskExceptionConfiguration",
        "user_pool_id": "userPoolId",
    },
)
class CfnUserPoolRiskConfigurationAttachmentMixinProps:
    def __init__(
        self,
        *,
        account_takeover_risk_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverRiskConfigurationTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        client_id: typing.Optional[builtins.str] = None,
        compromised_credentials_risk_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsRiskConfigurationTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        risk_exception_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.RiskExceptionConfigurationTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPoolRiskConfigurationAttachmentPropsMixin.

        :param account_takeover_risk_configuration: The settings for automated responses and notification templates for adaptive authentication with threat protection.
        :param client_id: The app client where this configuration is applied. When this parameter isn't present, the risk configuration applies to all user pool app clients that don't have client-level settings.
        :param compromised_credentials_risk_configuration: Settings for compromised-credentials actions and authentication types with threat protection in full-function ``ENFORCED`` mode.
        :param risk_exception_configuration: Exceptions to the risk evaluation configuration, including always-allow and always-block IP address ranges.
        :param user_pool_id: The ID of the user pool that has the risk configuration applied.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            cfn_user_pool_risk_configuration_attachment_mixin_props = cognito_mixins.CfnUserPoolRiskConfigurationAttachmentMixinProps(
                account_takeover_risk_configuration=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverRiskConfigurationTypeProperty(
                    actions=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionsTypeProperty(
                        high_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                            event_action="eventAction",
                            notify=False
                        ),
                        low_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                            event_action="eventAction",
                            notify=False
                        ),
                        medium_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                            event_action="eventAction",
                            notify=False
                        )
                    ),
                    notify_configuration=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyConfigurationTypeProperty(
                        block_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                            html_body="htmlBody",
                            subject="subject",
                            text_body="textBody"
                        ),
                        from="from",
                        mfa_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                            html_body="htmlBody",
                            subject="subject",
                            text_body="textBody"
                        ),
                        no_action_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                            html_body="htmlBody",
                            subject="subject",
                            text_body="textBody"
                        ),
                        reply_to="replyTo",
                        source_arn="sourceArn"
                    )
                ),
                client_id="clientId",
                compromised_credentials_risk_configuration=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsRiskConfigurationTypeProperty(
                    actions=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsActionsTypeProperty(
                        event_action="eventAction"
                    ),
                    event_filter=["eventFilter"]
                ),
                risk_exception_configuration=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.RiskExceptionConfigurationTypeProperty(
                    blocked_ip_range_list=["blockedIpRangeList"],
                    skipped_ip_range_list=["skippedIpRangeList"]
                ),
                user_pool_id="userPoolId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beba5baf1167c4ec99de20b2008c3bf527fb8a56065f80566e497e3c730a6ba2)
            check_type(argname="argument account_takeover_risk_configuration", value=account_takeover_risk_configuration, expected_type=type_hints["account_takeover_risk_configuration"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument compromised_credentials_risk_configuration", value=compromised_credentials_risk_configuration, expected_type=type_hints["compromised_credentials_risk_configuration"])
            check_type(argname="argument risk_exception_configuration", value=risk_exception_configuration, expected_type=type_hints["risk_exception_configuration"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_takeover_risk_configuration is not None:
            self._values["account_takeover_risk_configuration"] = account_takeover_risk_configuration
        if client_id is not None:
            self._values["client_id"] = client_id
        if compromised_credentials_risk_configuration is not None:
            self._values["compromised_credentials_risk_configuration"] = compromised_credentials_risk_configuration
        if risk_exception_configuration is not None:
            self._values["risk_exception_configuration"] = risk_exception_configuration
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id

    @builtins.property
    def account_takeover_risk_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverRiskConfigurationTypeProperty"]]:
        '''The settings for automated responses and notification templates for adaptive authentication with threat protection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfiguration
        '''
        result = self._values.get("account_takeover_risk_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverRiskConfigurationTypeProperty"]], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The app client where this configuration is applied.

        When this parameter isn't present, the risk configuration applies to all user pool app clients that don't have client-level settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-clientid
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compromised_credentials_risk_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsRiskConfigurationTypeProperty"]]:
        '''Settings for compromised-credentials actions and authentication types with threat protection in full-function ``ENFORCED`` mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfiguration
        '''
        result = self._values.get("compromised_credentials_risk_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsRiskConfigurationTypeProperty"]], result)

    @builtins.property
    def risk_exception_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.RiskExceptionConfigurationTypeProperty"]]:
        '''Exceptions to the risk evaluation configuration, including always-allow and always-block IP address ranges.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfiguration
        '''
        result = self._values.get("risk_exception_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.RiskExceptionConfigurationTypeProperty"]], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user pool that has the risk configuration applied.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolRiskConfigurationAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolRiskConfigurationAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin",
):
    '''The ``AWS::Cognito::UserPoolRiskConfigurationAttachment`` resource sets the risk configuration that is used for Amazon Cognito advanced security features.

    You can specify risk configuration for a single client (with a specific ``clientId`` ) or for all clients (by setting the ``clientId`` to ``ALL`` ). If you specify ``ALL`` , the default configuration is used for every client that has had no risk configuration set previously. If you specify risk configuration for a particular client, it no longer falls back to the ``ALL`` configuration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html
    :cloudformationResource: AWS::Cognito::UserPoolRiskConfigurationAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_user_pool_risk_configuration_attachment_props_mixin = cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin(cognito_mixins.CfnUserPoolRiskConfigurationAttachmentMixinProps(
            account_takeover_risk_configuration=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverRiskConfigurationTypeProperty(
                actions=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionsTypeProperty(
                    high_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                        event_action="eventAction",
                        notify=False
                    ),
                    low_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                        event_action="eventAction",
                        notify=False
                    ),
                    medium_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                        event_action="eventAction",
                        notify=False
                    )
                ),
                notify_configuration=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyConfigurationTypeProperty(
                    block_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                        html_body="htmlBody",
                        subject="subject",
                        text_body="textBody"
                    ),
                    from="from",
                    mfa_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                        html_body="htmlBody",
                        subject="subject",
                        text_body="textBody"
                    ),
                    no_action_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                        html_body="htmlBody",
                        subject="subject",
                        text_body="textBody"
                    ),
                    reply_to="replyTo",
                    source_arn="sourceArn"
                )
            ),
            client_id="clientId",
            compromised_credentials_risk_configuration=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsRiskConfigurationTypeProperty(
                actions=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsActionsTypeProperty(
                    event_action="eventAction"
                ),
                event_filter=["eventFilter"]
            ),
            risk_exception_configuration=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.RiskExceptionConfigurationTypeProperty(
                blocked_ip_range_list=["blockedIpRangeList"],
                skipped_ip_range_list=["skippedIpRangeList"]
            ),
            user_pool_id="userPoolId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPoolRiskConfigurationAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::UserPoolRiskConfigurationAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93192f2e1fc7c5049ccecdcae4bde64696ae11d62c284ab385196cab219b65ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ea5ae5a393a4302402218860870b4c34efcdc4e40f50b2689341d40c11cb7cc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258bd0a3de4fec6e4c36e1523db36e13f4cba089509259a662a768a4921c953d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPoolRiskConfigurationAttachmentMixinProps:
        return typing.cast(CfnUserPoolRiskConfigurationAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"event_action": "eventAction", "notify": "notify"},
    )
    class AccountTakeoverActionTypeProperty:
        def __init__(
            self,
            *,
            event_action: typing.Optional[builtins.str] = None,
            notify: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The automated response to a risk level for adaptive authentication in full-function, or ``ENFORCED`` , mode.

            You can assign an action to each risk level that advanced security features evaluates.

            :param event_action: The action to take for the attempted account takeover action for the associated risk level. Valid values are as follows: - ``BLOCK`` : Block the request. - ``MFA_IF_CONFIGURED`` : Present an MFA challenge if possible. MFA is possible if the user pool has active MFA methods that the user can set up. For example, if the user pool only supports SMS message MFA but the user doesn't have a phone number attribute, MFA setup isn't possible. If MFA setup isn't possible, allow the request. - ``MFA_REQUIRED`` : Present an MFA challenge if possible. Block the request if a user hasn't set up MFA. To sign in with required MFA, users must have an email address or phone number attribute, or a registered TOTP factor. - ``NO_ACTION`` : Take no action. Permit sign-in.
            :param notify: Determines whether Amazon Cognito sends a user a notification message when your user pools assesses a user's session at the associated risk level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                account_takeover_action_type_property = cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                    event_action="eventAction",
                    notify=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f167401bf0c4da9beff9ad04b852943b30f0c79f2d60b9ac1344bb0f23ee7982)
                check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
                check_type(argname="argument notify", value=notify, expected_type=type_hints["notify"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_action is not None:
                self._values["event_action"] = event_action
            if notify is not None:
                self._values["notify"] = notify

        @builtins.property
        def event_action(self) -> typing.Optional[builtins.str]:
            '''The action to take for the attempted account takeover action for the associated risk level.

            Valid values are as follows:

            - ``BLOCK`` : Block the request.
            - ``MFA_IF_CONFIGURED`` : Present an MFA challenge if possible. MFA is possible if the user pool has active MFA methods that the user can set up. For example, if the user pool only supports SMS message MFA but the user doesn't have a phone number attribute, MFA setup isn't possible. If MFA setup isn't possible, allow the request.
            - ``MFA_REQUIRED`` : Present an MFA challenge if possible. Block the request if a user hasn't set up MFA. To sign in with required MFA, users must have an email address or phone number attribute, or a registered TOTP factor.
            - ``NO_ACTION`` : Take no action. Permit sign-in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype-eventaction
            '''
            result = self._values.get("event_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notify(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether Amazon Cognito sends a user a notification message when your user pools assesses a user's session at the associated risk level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype-notify
            '''
            result = self._values.get("notify")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountTakeoverActionTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionsTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "high_action": "highAction",
            "low_action": "lowAction",
            "medium_action": "mediumAction",
        },
    )
    class AccountTakeoverActionsTypeProperty:
        def __init__(
            self,
            *,
            high_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            low_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            medium_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A list of account-takeover actions for each level of risk that Amazon Cognito might assess with advanced security features.

            :param high_action: The action that you assign to a high-risk assessment by threat protection.
            :param low_action: The action that you assign to a low-risk assessment by threat protection.
            :param medium_action: The action that you assign to a medium-risk assessment by threat protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                account_takeover_actions_type_property = cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionsTypeProperty(
                    high_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                        event_action="eventAction",
                        notify=False
                    ),
                    low_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                        event_action="eventAction",
                        notify=False
                    ),
                    medium_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                        event_action="eventAction",
                        notify=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59dade50c619211325532c6884779119cf1f77848617803ffe7474e1a19668d9)
                check_type(argname="argument high_action", value=high_action, expected_type=type_hints["high_action"])
                check_type(argname="argument low_action", value=low_action, expected_type=type_hints["low_action"])
                check_type(argname="argument medium_action", value=medium_action, expected_type=type_hints["medium_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if high_action is not None:
                self._values["high_action"] = high_action
            if low_action is not None:
                self._values["low_action"] = low_action
            if medium_action is not None:
                self._values["medium_action"] = medium_action

        @builtins.property
        def high_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty"]]:
            '''The action that you assign to a high-risk assessment by threat protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype-highaction
            '''
            result = self._values.get("high_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty"]], result)

        @builtins.property
        def low_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty"]]:
            '''The action that you assign to a low-risk assessment by threat protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype-lowaction
            '''
            result = self._values.get("low_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty"]], result)

        @builtins.property
        def medium_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty"]]:
            '''The action that you assign to a medium-risk assessment by threat protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype-mediumaction
            '''
            result = self._values.get("medium_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountTakeoverActionsTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverRiskConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "notify_configuration": "notifyConfiguration",
        },
    )
    class AccountTakeoverRiskConfigurationTypeProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionsTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            notify_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyConfigurationTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The settings for automated responses and notification templates for adaptive authentication with advanced security features.

            :param actions: A list of account-takeover actions for each level of risk that Amazon Cognito might assess with threat protection.
            :param notify_configuration: The settings for composing and sending an email message when threat protection assesses a risk level with adaptive authentication. When you choose to notify users in ``AccountTakeoverRiskConfiguration`` , Amazon Cognito sends an email message using the method and template that you set with this data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                account_takeover_risk_configuration_type_property = cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverRiskConfigurationTypeProperty(
                    actions=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionsTypeProperty(
                        high_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                            event_action="eventAction",
                            notify=False
                        ),
                        low_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                            event_action="eventAction",
                            notify=False
                        ),
                        medium_action=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty(
                            event_action="eventAction",
                            notify=False
                        )
                    ),
                    notify_configuration=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyConfigurationTypeProperty(
                        block_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                            html_body="htmlBody",
                            subject="subject",
                            text_body="textBody"
                        ),
                        from="from",
                        mfa_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                            html_body="htmlBody",
                            subject="subject",
                            text_body="textBody"
                        ),
                        no_action_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                            html_body="htmlBody",
                            subject="subject",
                            text_body="textBody"
                        ),
                        reply_to="replyTo",
                        source_arn="sourceArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0298b663676a52d42fee0a69572d01b3d15f2fe971b8465216f979bff0dd8c45)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument notify_configuration", value=notify_configuration, expected_type=type_hints["notify_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if notify_configuration is not None:
                self._values["notify_configuration"] = notify_configuration

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionsTypeProperty"]]:
            '''A list of account-takeover actions for each level of risk that Amazon Cognito might assess with threat protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionsTypeProperty"]], result)

        @builtins.property
        def notify_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyConfigurationTypeProperty"]]:
            '''The settings for composing and sending an email message when threat protection assesses a risk level with adaptive authentication.

            When you choose to notify users in ``AccountTakeoverRiskConfiguration`` , Amazon Cognito sends an email message using the method and template that you set with this data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype-notifyconfiguration
            '''
            result = self._values.get("notify_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyConfigurationTypeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountTakeoverRiskConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsActionsTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"event_action": "eventAction"},
    )
    class CompromisedCredentialsActionsTypeProperty:
        def __init__(
            self,
            *,
            event_action: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for user pool actions when Amazon Cognito detects compromised credentials with advanced security features in full-function ``ENFORCED`` mode.

            :param event_action: The action that Amazon Cognito takes when it detects compromised credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsactionstype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                compromised_credentials_actions_type_property = cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsActionsTypeProperty(
                    event_action="eventAction"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb33fef7634374502d211b06833dba2bdad6ed768c610515c50659069b024258)
                check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_action is not None:
                self._values["event_action"] = event_action

        @builtins.property
        def event_action(self) -> typing.Optional[builtins.str]:
            '''The action that Amazon Cognito takes when it detects compromised credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsactionstype.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsactionstype-eventaction
            '''
            result = self._values.get("event_action")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CompromisedCredentialsActionsTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsRiskConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"actions": "actions", "event_filter": "eventFilter"},
    )
    class CompromisedCredentialsRiskConfigurationTypeProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsActionsTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            event_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Settings for compromised-credentials actions and authentication-event sources with advanced security features in full-function ``ENFORCED`` mode.

            :param actions: Settings for the actions that you want your user pool to take when Amazon Cognito detects compromised credentials.
            :param event_filter: Settings for the sign-in activity where you want to configure compromised-credentials actions. Defaults to all events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                compromised_credentials_risk_configuration_type_property = cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsRiskConfigurationTypeProperty(
                    actions=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsActionsTypeProperty(
                        event_action="eventAction"
                    ),
                    event_filter=["eventFilter"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc58a9ae23c713c2f62956ce8db972888aa755af33a2a9477d89cd5b5f401d27)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument event_filter", value=event_filter, expected_type=type_hints["event_filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if event_filter is not None:
                self._values["event_filter"] = event_filter

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsActionsTypeProperty"]]:
            '''Settings for the actions that you want your user pool to take when Amazon Cognito detects compromised credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsActionsTypeProperty"]], result)

        @builtins.property
        def event_filter(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Settings for the sign-in activity where you want to configure compromised-credentials actions.

            Defaults to all events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype-eventfilter
            '''
            result = self._values.get("event_filter")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CompromisedCredentialsRiskConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_email": "blockEmail",
            "from_": "from",
            "mfa_email": "mfaEmail",
            "no_action_email": "noActionEmail",
            "reply_to": "replyTo",
            "source_arn": "sourceArn",
        },
    )
    class NotifyConfigurationTypeProperty:
        def __init__(
            self,
            *,
            block_email: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            from_: typing.Optional[builtins.str] = None,
            mfa_email: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            no_action_email: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            reply_to: typing.Optional[builtins.str] = None,
            source_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for Amazon SES email messages that advanced security features sends to a user when your adaptive authentication automated response has a *Notify* action.

            :param block_email: The template for the email message that your user pool sends when a detected risk event is blocked.
            :param from_: The email address that sends the email message. The address must be either individually verified with Amazon Simple Email Service, or from a domain that has been verified with Amazon SES.
            :param mfa_email: The template for the email message that your user pool sends when MFA is challenged in response to a detected risk.
            :param no_action_email: The template for the email message that your user pool sends when no action is taken in response to a detected risk.
            :param reply_to: The reply-to email address of an email template. Can be an email address in the format ``admin@example.com`` or ``Administrator <admin@example.com>`` .
            :param source_arn: The Amazon Resource Name (ARN) of the identity that is associated with the sending authorization policy. This identity permits Amazon Cognito to send for the email address specified in the ``From`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                notify_configuration_type_property = cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyConfigurationTypeProperty(
                    block_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                        html_body="htmlBody",
                        subject="subject",
                        text_body="textBody"
                    ),
                    from="from",
                    mfa_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                        html_body="htmlBody",
                        subject="subject",
                        text_body="textBody"
                    ),
                    no_action_email=cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                        html_body="htmlBody",
                        subject="subject",
                        text_body="textBody"
                    ),
                    reply_to="replyTo",
                    source_arn="sourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5631343483d8904bb763c1c6138811195e6f62fdba49c358fb5ee1a89433123c)
                check_type(argname="argument block_email", value=block_email, expected_type=type_hints["block_email"])
                check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
                check_type(argname="argument mfa_email", value=mfa_email, expected_type=type_hints["mfa_email"])
                check_type(argname="argument no_action_email", value=no_action_email, expected_type=type_hints["no_action_email"])
                check_type(argname="argument reply_to", value=reply_to, expected_type=type_hints["reply_to"])
                check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block_email is not None:
                self._values["block_email"] = block_email
            if from_ is not None:
                self._values["from_"] = from_
            if mfa_email is not None:
                self._values["mfa_email"] = mfa_email
            if no_action_email is not None:
                self._values["no_action_email"] = no_action_email
            if reply_to is not None:
                self._values["reply_to"] = reply_to
            if source_arn is not None:
                self._values["source_arn"] = source_arn

        @builtins.property
        def block_email(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty"]]:
            '''The template for the email message that your user pool sends when a detected risk event is blocked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-blockemail
            '''
            result = self._values.get("block_email")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty"]], result)

        @builtins.property
        def from_(self) -> typing.Optional[builtins.str]:
            '''The email address that sends the email message.

            The address must be either individually verified with Amazon Simple Email Service, or from a domain that has been verified with Amazon SES.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-from
            '''
            result = self._values.get("from_")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mfa_email(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty"]]:
            '''The template for the email message that your user pool sends when MFA is challenged in response to a detected risk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-mfaemail
            '''
            result = self._values.get("mfa_email")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty"]], result)

        @builtins.property
        def no_action_email(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty"]]:
            '''The template for the email message that your user pool sends when no action is taken in response to a detected risk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-noactionemail
            '''
            result = self._values.get("no_action_email")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty"]], result)

        @builtins.property
        def reply_to(self) -> typing.Optional[builtins.str]:
            '''The reply-to email address of an email template.

            Can be an email address in the format ``admin@example.com`` or ``Administrator <admin@example.com>`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-replyto
            '''
            result = self._values.get("reply_to")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the identity that is associated with the sending authorization policy.

            This identity permits Amazon Cognito to send for the email address specified in the ``From`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-sourcearn
            '''
            result = self._values.get("source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotifyConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "html_body": "htmlBody",
            "subject": "subject",
            "text_body": "textBody",
        },
    )
    class NotifyEmailTypeProperty:
        def __init__(
            self,
            *,
            html_body: typing.Optional[builtins.str] = None,
            subject: typing.Optional[builtins.str] = None,
            text_body: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The template for email messages that advanced security features sends to a user when your threat protection automated response has a *Notify* action.

            :param html_body: The body of an email notification formatted in HTML. Choose an ``HtmlBody`` or a ``TextBody`` to send an HTML-formatted or plaintext message, respectively.
            :param subject: The subject of the threat protection email notification.
            :param text_body: The body of an email notification formatted in plaintext. Choose an ``HtmlBody`` or a ``TextBody`` to send an HTML-formatted or plaintext message, respectively.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                notify_email_type_property = cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty(
                    html_body="htmlBody",
                    subject="subject",
                    text_body="textBody"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59300f032446f124979ba74a7276aee9ad24860c364eb27738e26a115571b9d4)
                check_type(argname="argument html_body", value=html_body, expected_type=type_hints["html_body"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
                check_type(argname="argument text_body", value=text_body, expected_type=type_hints["text_body"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if html_body is not None:
                self._values["html_body"] = html_body
            if subject is not None:
                self._values["subject"] = subject
            if text_body is not None:
                self._values["text_body"] = text_body

        @builtins.property
        def html_body(self) -> typing.Optional[builtins.str]:
            '''The body of an email notification formatted in HTML.

            Choose an ``HtmlBody`` or a ``TextBody`` to send an HTML-formatted or plaintext message, respectively.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyemailtype-htmlbody
            '''
            result = self._values.get("html_body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subject(self) -> typing.Optional[builtins.str]:
            '''The subject of the threat protection email notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyemailtype-subject
            '''
            result = self._values.get("subject")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_body(self) -> typing.Optional[builtins.str]:
            '''The body of an email notification formatted in plaintext.

            Choose an ``HtmlBody`` or a ``TextBody`` to send an HTML-formatted or plaintext message, respectively.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyemailtype-textbody
            '''
            result = self._values.get("text_body")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotifyEmailTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.RiskExceptionConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "blocked_ip_range_list": "blockedIpRangeList",
            "skipped_ip_range_list": "skippedIpRangeList",
        },
    )
    class RiskExceptionConfigurationTypeProperty:
        def __init__(
            self,
            *,
            blocked_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            skipped_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Exceptions to the risk evaluation configuration, including always-allow and always-block IP address ranges.

            :param blocked_ip_range_list: An always-block IP address list. Overrides the risk decision and always blocks authentication requests. This parameter is displayed and set in CIDR notation.
            :param skipped_ip_range_list: An always-allow IP address list. Risk detection isn't performed on the IP addresses in this range list. This parameter is displayed and set in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                risk_exception_configuration_type_property = cognito_mixins.CfnUserPoolRiskConfigurationAttachmentPropsMixin.RiskExceptionConfigurationTypeProperty(
                    blocked_ip_range_list=["blockedIpRangeList"],
                    skipped_ip_range_list=["skippedIpRangeList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ad09d4794a4c4794a1305dea288466c07d30fe7a5d0e64df1ff67b44ff0ecd6)
                check_type(argname="argument blocked_ip_range_list", value=blocked_ip_range_list, expected_type=type_hints["blocked_ip_range_list"])
                check_type(argname="argument skipped_ip_range_list", value=skipped_ip_range_list, expected_type=type_hints["skipped_ip_range_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if blocked_ip_range_list is not None:
                self._values["blocked_ip_range_list"] = blocked_ip_range_list
            if skipped_ip_range_list is not None:
                self._values["skipped_ip_range_list"] = skipped_ip_range_list

        @builtins.property
        def blocked_ip_range_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An always-block IP address list.

            Overrides the risk decision and always blocks authentication requests. This parameter is displayed and set in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype-blockediprangelist
            '''
            result = self._values.get("blocked_ip_range_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def skipped_ip_range_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An always-allow IP address list.

            Risk detection isn't performed on the IP addresses in this range list. This parameter is displayed and set in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype-skippediprangelist
            '''
            result = self._values.get("skipped_ip_range_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RiskExceptionConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolUICustomizationAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "css": "css", "user_pool_id": "userPoolId"},
)
class CfnUserPoolUICustomizationAttachmentMixinProps:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        css: typing.Optional[builtins.str] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPoolUICustomizationAttachmentPropsMixin.

        :param client_id: The app client ID for your UI customization. When this value isn't present, the customization applies to all user pool app clients that don't have client-level settings..
        :param css: A plaintext CSS file that contains the custom fields that you want to apply to your user pool or app client. To download a template, go to the Amazon Cognito console. Navigate to your user pool *App clients* tab, select *Login pages* , edit *Hosted UI (classic) style* , and select the link to ``CSS template.css`` .
        :param user_pool_id: The ID of the user pool where you want to apply branding to the classic hosted UI.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            cfn_user_pool_uICustomization_attachment_mixin_props = cognito_mixins.CfnUserPoolUICustomizationAttachmentMixinProps(
                client_id="clientId",
                css="css",
                user_pool_id="userPoolId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c14acb1204af4805e1423f497b62f5a51515a8b3b55332e2d046ad32d3ab90)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument css", value=css, expected_type=type_hints["css"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if css is not None:
            self._values["css"] = css
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The app client ID for your UI customization.

        When this value isn't present, the customization applies to all user pool app clients that don't have client-level settings..

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-clientid
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def css(self) -> typing.Optional[builtins.str]:
        '''A plaintext CSS file that contains the custom fields that you want to apply to your user pool or app client.

        To download a template, go to the Amazon Cognito console. Navigate to your user pool *App clients* tab, select *Login pages* , edit *Hosted UI (classic) style* , and select the link to ``CSS template.css`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-css
        '''
        result = self._values.get("css")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user pool where you want to apply branding to the classic hosted UI.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolUICustomizationAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolUICustomizationAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolUICustomizationAttachmentPropsMixin",
):
    '''A container for the UI customization information for the hosted UI in a user pool.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html
    :cloudformationResource: AWS::Cognito::UserPoolUICustomizationAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_user_pool_uICustomization_attachment_props_mixin = cognito_mixins.CfnUserPoolUICustomizationAttachmentPropsMixin(cognito_mixins.CfnUserPoolUICustomizationAttachmentMixinProps(
            client_id="clientId",
            css="css",
            user_pool_id="userPoolId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPoolUICustomizationAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::UserPoolUICustomizationAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc519a0f1b05cf69d3ce974e4106fe5d0c0ffa26e642770d72390311f2fe81e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96120b5d71319f26da24a98deb19000042602b0764169f76aa8107e52b004196)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d68447a947f163c28096a4cd044c2b3b3ed4cf881b1eb06bc75b6ddf7ed2c6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPoolUICustomizationAttachmentMixinProps:
        return typing.cast(CfnUserPoolUICustomizationAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolUserMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_metadata": "clientMetadata",
        "desired_delivery_mediums": "desiredDeliveryMediums",
        "force_alias_creation": "forceAliasCreation",
        "message_action": "messageAction",
        "user_attributes": "userAttributes",
        "username": "username",
        "user_pool_id": "userPoolId",
        "validation_data": "validationData",
    },
)
class CfnUserPoolUserMixinProps:
    def __init__(
        self,
        *,
        client_metadata: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        desired_delivery_mediums: typing.Optional[typing.Sequence[builtins.str]] = None,
        force_alias_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        message_action: typing.Optional[builtins.str] = None,
        user_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolUserPropsMixin.AttributeTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        username: typing.Optional[builtins.str] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
        validation_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPoolUserPropsMixin.AttributeTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnUserPoolUserPropsMixin.

        :param client_metadata: A map of custom key-value pairs that you can provide as input for any custom workflows that this action triggers. You create custom workflows by assigning AWS Lambda functions to user pool triggers. When Amazon Cognito invokes any of these functions, it passes a JSON payload, which the function receives as input. This payload contains a ``clientMetadata`` attribute that provides the data that you assigned to the ClientMetadata parameter in your request. In your function code, you can process the ``clientMetadata`` value to enhance your workflow for your specific needs. To review the Lambda trigger types that Amazon Cognito invokes at runtime with API requests, see `Connecting API actions to Lambda triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-working-with-lambda-triggers.html#lambda-triggers-by-event>`_ in the *Amazon Cognito Developer Guide* . .. epigraph:: When you use the ``ClientMetadata`` parameter, note that Amazon Cognito won't do the following: - Store the ``ClientMetadata`` value. This data is available only to AWS Lambda triggers that are assigned to a user pool to support custom workflows. If your user pool configuration doesn't include triggers, the ``ClientMetadata`` parameter serves no purpose. - Validate the ``ClientMetadata`` value. - Encrypt the ``ClientMetadata`` value. Don't send sensitive information in this parameter.
        :param desired_delivery_mediums: Specify ``EMAIL`` if email will be used to send the welcome message. Specify ``SMS`` if the phone number will be used. The default value is ``SMS`` . You can specify more than one value.
        :param force_alias_creation: This parameter is used only if the ``phone_number_verified`` or ``email_verified`` attribute is set to ``True`` . Otherwise, it is ignored. If this parameter is set to ``True`` and the phone number or email address specified in the ``UserAttributes`` parameter already exists as an alias with a different user, this request migrates the alias from the previous user to the newly-created user. The previous user will no longer be able to log in using that alias. If this parameter is set to ``False`` , the API throws an ``AliasExistsException`` error if the alias already exists. The default value is ``False`` .
        :param message_action: Set to ``RESEND`` to resend the invitation message to a user that already exists, and to reset the temporary-password duration with a new temporary password. Set to ``SUPPRESS`` to suppress sending the message. You can specify only one value.
        :param user_attributes: An array of name-value pairs that contain user attributes and attribute values to be set for the user to be created. You can create a user without specifying any attributes other than ``Username`` . However, any attributes that you specify as required (when creating a user pool or in the *Attributes* tab of the console) either you should supply (in your call to ``AdminCreateUser`` ) or the user should supply (when they sign up in response to your welcome message). For custom attributes, you must prepend the ``custom:`` prefix to the attribute name. To send a message inviting the user to sign up, you must specify the user's email address or phone number. You can do this in your call to AdminCreateUser or in the *Users* tab of the Amazon Cognito console for managing your user pools. You must also provide an email address or phone number when you expect the user to do passwordless sign-in with an email or SMS OTP. These attributes must be provided when passwordless options are the only available, or when you don't submit a ``TemporaryPassword`` . In your call to ``AdminCreateUser`` , you can set the ``email_verified`` attribute to ``True`` , and you can set the ``phone_number_verified`` attribute to ``True`` . - *email* : The email address of the user to whom the message that contains the code and username will be sent. Required if the ``email_verified`` attribute is set to ``True`` , or if ``"EMAIL"`` is specified in the ``DesiredDeliveryMediums`` parameter. - *phone_number* : The phone number of the user to whom the message that contains the code and username will be sent. Required if the ``phone_number_verified`` attribute is set to ``True`` , or if ``"SMS"`` is specified in the ``DesiredDeliveryMediums`` parameter.
        :param username: The value that you want to set as the username sign-in attribute. The following conditions apply to the username parameter. - The username can't be a duplicate of another username in the same user pool. - You can't change the value of a username after you create it. - You can only provide a value if usernames are a valid sign-in attribute for your user pool. If your user pool only supports phone numbers or email addresses as sign-in attributes, Amazon Cognito automatically generates a username value. For more information, see `Customizing sign-in attributes <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases>`_ .
        :param user_pool_id: The ID of the user pool where you want to create a user.
        :param validation_data: Temporary user attributes that contribute to the outcomes of your pre sign-up Lambda trigger. This set of key-value pairs are for custom validation of information that you collect from your users but don't need to retain. Your Lambda function can analyze this additional data and act on it. Your function can automatically confirm and verify select users or perform external API operations like logging user attributes and validation data to Amazon CloudWatch Logs. For more information about the pre sign-up Lambda trigger, see `Pre sign-up Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            cfn_user_pool_user_mixin_props = cognito_mixins.CfnUserPoolUserMixinProps(
                client_metadata={
                    "client_metadata_key": "clientMetadata"
                },
                desired_delivery_mediums=["desiredDeliveryMediums"],
                force_alias_creation=False,
                message_action="messageAction",
                user_attributes=[cognito_mixins.CfnUserPoolUserPropsMixin.AttributeTypeProperty(
                    name="name",
                    value="value"
                )],
                username="username",
                user_pool_id="userPoolId",
                validation_data=[cognito_mixins.CfnUserPoolUserPropsMixin.AttributeTypeProperty(
                    name="name",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f299bb36816a063080972c8f8b6135ae6c362760c3044f1e00e5e19b8fa26b2a)
            check_type(argname="argument client_metadata", value=client_metadata, expected_type=type_hints["client_metadata"])
            check_type(argname="argument desired_delivery_mediums", value=desired_delivery_mediums, expected_type=type_hints["desired_delivery_mediums"])
            check_type(argname="argument force_alias_creation", value=force_alias_creation, expected_type=type_hints["force_alias_creation"])
            check_type(argname="argument message_action", value=message_action, expected_type=type_hints["message_action"])
            check_type(argname="argument user_attributes", value=user_attributes, expected_type=type_hints["user_attributes"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            check_type(argname="argument validation_data", value=validation_data, expected_type=type_hints["validation_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_metadata is not None:
            self._values["client_metadata"] = client_metadata
        if desired_delivery_mediums is not None:
            self._values["desired_delivery_mediums"] = desired_delivery_mediums
        if force_alias_creation is not None:
            self._values["force_alias_creation"] = force_alias_creation
        if message_action is not None:
            self._values["message_action"] = message_action
        if user_attributes is not None:
            self._values["user_attributes"] = user_attributes
        if username is not None:
            self._values["username"] = username
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id
        if validation_data is not None:
            self._values["validation_data"] = validation_data

    @builtins.property
    def client_metadata(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''A map of custom key-value pairs that you can provide as input for any custom workflows that this action triggers.

        You create custom workflows by assigning AWS Lambda functions to user pool triggers.

        When Amazon Cognito invokes any of these functions, it passes a JSON payload, which the function receives as input. This payload contains a ``clientMetadata`` attribute that provides the data that you assigned to the ClientMetadata parameter in your request. In your function code, you can process the ``clientMetadata`` value to enhance your workflow for your specific needs.

        To review the Lambda trigger types that Amazon Cognito invokes at runtime with API requests, see `Connecting API actions to Lambda triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-working-with-lambda-triggers.html#lambda-triggers-by-event>`_ in the *Amazon Cognito Developer Guide* .
        .. epigraph::

           When you use the ``ClientMetadata`` parameter, note that Amazon Cognito won't do the following:

           - Store the ``ClientMetadata`` value. This data is available only to AWS Lambda triggers that are assigned to a user pool to support custom workflows. If your user pool configuration doesn't include triggers, the ``ClientMetadata`` parameter serves no purpose.
           - Validate the ``ClientMetadata`` value.
           - Encrypt the ``ClientMetadata`` value. Don't send sensitive information in this parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-clientmetadata
        '''
        result = self._values.get("client_metadata")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def desired_delivery_mediums(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify ``EMAIL`` if email will be used to send the welcome message.

        Specify ``SMS`` if the phone number will be used. The default value is ``SMS`` . You can specify more than one value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-desireddeliverymediums
        '''
        result = self._values.get("desired_delivery_mediums")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def force_alias_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''This parameter is used only if the ``phone_number_verified`` or ``email_verified`` attribute is set to ``True`` .

        Otherwise, it is ignored.

        If this parameter is set to ``True`` and the phone number or email address specified in the ``UserAttributes`` parameter already exists as an alias with a different user, this request migrates the alias from the previous user to the newly-created user. The previous user will no longer be able to log in using that alias.

        If this parameter is set to ``False`` , the API throws an ``AliasExistsException`` error if the alias already exists. The default value is ``False`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-forcealiascreation
        '''
        result = self._values.get("force_alias_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def message_action(self) -> typing.Optional[builtins.str]:
        '''Set to ``RESEND`` to resend the invitation message to a user that already exists, and to reset the temporary-password duration with a new temporary password.

        Set to ``SUPPRESS`` to suppress sending the message. You can specify only one value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-messageaction
        '''
        result = self._values.get("message_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolUserPropsMixin.AttributeTypeProperty"]]]]:
        '''An array of name-value pairs that contain user attributes and attribute values to be set for the user to be created.

        You can create a user without specifying any attributes other than ``Username`` . However, any attributes that you specify as required (when creating a user pool or in the *Attributes* tab of the console) either you should supply (in your call to ``AdminCreateUser`` ) or the user should supply (when they sign up in response to your welcome message).

        For custom attributes, you must prepend the ``custom:`` prefix to the attribute name.

        To send a message inviting the user to sign up, you must specify the user's email address or phone number. You can do this in your call to AdminCreateUser or in the *Users* tab of the Amazon Cognito console for managing your user pools.

        You must also provide an email address or phone number when you expect the user to do passwordless sign-in with an email or SMS OTP. These attributes must be provided when passwordless options are the only available, or when you don't submit a ``TemporaryPassword`` .

        In your call to ``AdminCreateUser`` , you can set the ``email_verified`` attribute to ``True`` , and you can set the ``phone_number_verified`` attribute to ``True`` .

        - *email* : The email address of the user to whom the message that contains the code and username will be sent. Required if the ``email_verified`` attribute is set to ``True`` , or if ``"EMAIL"`` is specified in the ``DesiredDeliveryMediums`` parameter.
        - *phone_number* : The phone number of the user to whom the message that contains the code and username will be sent. Required if the ``phone_number_verified`` attribute is set to ``True`` , or if ``"SMS"`` is specified in the ``DesiredDeliveryMediums`` parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-userattributes
        '''
        result = self._values.get("user_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolUserPropsMixin.AttributeTypeProperty"]]]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The value that you want to set as the username sign-in attribute.

        The following conditions apply to the username parameter.

        - The username can't be a duplicate of another username in the same user pool.
        - You can't change the value of a username after you create it.
        - You can only provide a value if usernames are a valid sign-in attribute for your user pool. If your user pool only supports phone numbers or email addresses as sign-in attributes, Amazon Cognito automatically generates a username value. For more information, see `Customizing sign-in attributes <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user pool where you want to create a user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validation_data(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolUserPropsMixin.AttributeTypeProperty"]]]]:
        '''Temporary user attributes that contribute to the outcomes of your pre sign-up Lambda trigger.

        This set of key-value pairs are for custom validation of information that you collect from your users but don't need to retain.

        Your Lambda function can analyze this additional data and act on it. Your function can automatically confirm and verify select users or perform external API operations like logging user attributes and validation data to Amazon CloudWatch Logs.

        For more information about the pre sign-up Lambda trigger, see `Pre sign-up Lambda trigger <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-validationdata
        '''
        result = self._values.get("validation_data")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPoolUserPropsMixin.AttributeTypeProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolUserMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolUserPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolUserPropsMixin",
):
    '''The ``AWS::Cognito::UserPoolUser`` resource creates an Amazon Cognito user pool user.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html
    :cloudformationResource: AWS::Cognito::UserPoolUser
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_user_pool_user_props_mixin = cognito_mixins.CfnUserPoolUserPropsMixin(cognito_mixins.CfnUserPoolUserMixinProps(
            client_metadata={
                "client_metadata_key": "clientMetadata"
            },
            desired_delivery_mediums=["desiredDeliveryMediums"],
            force_alias_creation=False,
            message_action="messageAction",
            user_attributes=[cognito_mixins.CfnUserPoolUserPropsMixin.AttributeTypeProperty(
                name="name",
                value="value"
            )],
            username="username",
            user_pool_id="userPoolId",
            validation_data=[cognito_mixins.CfnUserPoolUserPropsMixin.AttributeTypeProperty(
                name="name",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPoolUserMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::UserPoolUser``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d296cc9d1d383068e6d10ba36615b95c0827d9ac427124a96e7af565decd87e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f42433ae8cdd1d649731e207c78f87822766ad03baa5d12a39382cde1a59fd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad49972e65e7bc4709616563ae9de5bdf450f74db5d78beb116811f7f718d5ee)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPoolUserMixinProps:
        return typing.cast(CfnUserPoolUserMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolUserPropsMixin.AttributeTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class AttributeTypeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name and value of a user attribute.

            :param name: The name of the attribute.
            :param value: The value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooluser-attributetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
                
                attribute_type_property = cognito_mixins.CfnUserPoolUserPropsMixin.AttributeTypeProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5af9f1b5e19b28052eb6597fdfb7e4c23031e57e63af83cb1c45fd149520988b)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooluser-attributetype.html#cfn-cognito-userpooluser-attributetype-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooluser-attributetype.html#cfn-cognito-userpooluser-attributetype-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolUserToGroupAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "username": "username",
        "user_pool_id": "userPoolId",
    },
)
class CfnUserPoolUserToGroupAttachmentMixinProps:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
        user_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPoolUserToGroupAttachmentPropsMixin.

        :param group_name: The name of the group that you want to add your user to.
        :param username: The user's username.
        :param user_pool_id: The ID of the user pool that contains the group that you want to add the user to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
            
            cfn_user_pool_user_to_group_attachment_mixin_props = cognito_mixins.CfnUserPoolUserToGroupAttachmentMixinProps(
                group_name="groupName",
                username="username",
                user_pool_id="userPoolId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee93abc2bb82b8b72c9bcda38096d761cd417b91a7e1fc31c24471eb32f809a2)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if username is not None:
            self._values["username"] = username
        if user_pool_id is not None:
            self._values["user_pool_id"] = user_pool_id

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the group that you want to add your user to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The user's username.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user pool that contains the group that you want to add the user to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-userpoolid
        '''
        result = self._values.get("user_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolUserToGroupAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPoolUserToGroupAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cognito.mixins.CfnUserPoolUserToGroupAttachmentPropsMixin",
):
    '''Adds a user to a group.

    A user who is in a group can present a preferred-role claim to an identity pool, and populates a ``cognito:groups`` claim to their access and identity tokens.
    .. epigraph::

       Amazon Cognito evaluates AWS Identity and Access Management (IAM) policies in requests for this API operation. For this operation, you must use IAM credentials to authorize requests, and you must grant yourself the corresponding IAM permission in a policy.

       **Learn more** - `Signing AWS API Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`_

       - `Using the Amazon Cognito user pools API and user pool endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html
    :cloudformationResource: AWS::Cognito::UserPoolUserToGroupAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cognito import mixins as cognito_mixins
        
        cfn_user_pool_user_to_group_attachment_props_mixin = cognito_mixins.CfnUserPoolUserToGroupAttachmentPropsMixin(cognito_mixins.CfnUserPoolUserToGroupAttachmentMixinProps(
            group_name="groupName",
            username="username",
            user_pool_id="userPoolId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPoolUserToGroupAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cognito::UserPoolUserToGroupAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8ebfa91f39004c1a522367c28cf35d9ff8c2f19b88ecdd67daf94a7196478f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bf67189ee01e05ad7323e686c809ff4882163a8fc4ea8545d00f2aa797d1f3a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c0259d725c9a9acae560c6398df369893a8eb8b73370e2a633da0aeee9ca0b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPoolUserToGroupAttachmentMixinProps:
        return typing.cast(CfnUserPoolUserToGroupAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnIdentityPoolMixinProps",
    "CfnIdentityPoolPrincipalTagMixinProps",
    "CfnIdentityPoolPrincipalTagPropsMixin",
    "CfnIdentityPoolPropsMixin",
    "CfnIdentityPoolRoleAttachmentMixinProps",
    "CfnIdentityPoolRoleAttachmentPropsMixin",
    "CfnLogDeliveryConfigurationMixinProps",
    "CfnLogDeliveryConfigurationPropsMixin",
    "CfnManagedLoginBrandingMixinProps",
    "CfnManagedLoginBrandingPropsMixin",
    "CfnTermsMixinProps",
    "CfnTermsPropsMixin",
    "CfnUserPoolApplicationLogs",
    "CfnUserPoolClientMixinProps",
    "CfnUserPoolClientPropsMixin",
    "CfnUserPoolDomainMixinProps",
    "CfnUserPoolDomainPropsMixin",
    "CfnUserPoolGroupMixinProps",
    "CfnUserPoolGroupPropsMixin",
    "CfnUserPoolIdentityProviderMixinProps",
    "CfnUserPoolIdentityProviderPropsMixin",
    "CfnUserPoolLogsMixin",
    "CfnUserPoolMixinProps",
    "CfnUserPoolPropsMixin",
    "CfnUserPoolResourceServerMixinProps",
    "CfnUserPoolResourceServerPropsMixin",
    "CfnUserPoolRiskConfigurationAttachmentMixinProps",
    "CfnUserPoolRiskConfigurationAttachmentPropsMixin",
    "CfnUserPoolUICustomizationAttachmentMixinProps",
    "CfnUserPoolUICustomizationAttachmentPropsMixin",
    "CfnUserPoolUserMixinProps",
    "CfnUserPoolUserPropsMixin",
    "CfnUserPoolUserToGroupAttachmentMixinProps",
    "CfnUserPoolUserToGroupAttachmentPropsMixin",
]

publication.publish()

def _typecheckingstub__67372ba211f7acfcaed8f890308ad723cafd4a8ed2cd64ae44c2a72152668c7b(
    *,
    allow_classic_flow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    allow_unauthenticated_identities: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cognito_events: typing.Any = None,
    cognito_identity_providers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentityPoolPropsMixin.CognitoIdentityProviderProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    cognito_streams: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentityPoolPropsMixin.CognitoStreamsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    developer_provider_name: typing.Optional[builtins.str] = None,
    identity_pool_name: typing.Optional[builtins.str] = None,
    identity_pool_tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    open_id_connect_provider_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    push_sync: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentityPoolPropsMixin.PushSyncProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    saml_provider_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    supported_login_providers: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f91c12eafe779b4f3590afb48f6e5199e76efbcfd2937fe2b0319f96e4c1f22(
    *,
    identity_pool_id: typing.Optional[builtins.str] = None,
    identity_provider_name: typing.Optional[builtins.str] = None,
    principal_tags: typing.Any = None,
    use_defaults: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99b534551a6fc1282c0297e63fca99035093683f976192337285a5802014064(
    props: typing.Union[CfnIdentityPoolPrincipalTagMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ac8a87771a22f5c7026fe406745e498f54b8ddb63186551f22d18a2dfbbaa0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f52cfd8be909f9f29db4e8dc8d16d48b355a1c93e3a4d8cec7a41268b4a3682(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8dbe76c211016a6eb10b06afb75505b0d79bdc02ef51bcb9649bd8bcfab4ec(
    props: typing.Union[CfnIdentityPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afda541c56ec87c1ee0ebf90dc305652fa5dcb99325f1522f645e58f1e81d3a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7faf4c99172c88c9a9f08ad0748491a731fa27c9e2280e1321316d563efef619(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319186e502894de6c361b0b7f1c59618cf5929c4f46e821e8dc1d98d0b9ac254(
    *,
    client_id: typing.Optional[builtins.str] = None,
    provider_name: typing.Optional[builtins.str] = None,
    server_side_token_check: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d60592fbd79d0d4ed98e60335d9de499d192554f28fceb89949f59f2353cc80(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    streaming_status: typing.Optional[builtins.str] = None,
    stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e85e722f1cfff970f70b8bb8fefdbff91c23a333290a905009ab1c733d5845(
    *,
    application_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168d215443ea4cdf0133a5b8de2ce5e76c33f46aa74b29efdb4f84ffc43b0f72(
    *,
    identity_pool_id: typing.Optional[builtins.str] = None,
    role_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentityPoolRoleAttachmentPropsMixin.RoleMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    roles: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5773f928aed19ced0139cdcc1a3b4cf187cc01ac7a7a479fbc0a1a9ee77f4fc(
    props: typing.Union[CfnIdentityPoolRoleAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7784d0756a3bc97eb67c584b6a5ca7e9faaf00efa3d36b2ded5d0b0c52379d9b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16cca5ea0bb1f12d747decef5b42428f1c413d16202b2b98d41b4ccd8e7bdf88(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02291e3d9811ee3ae170ba10ed51d6872090f4f4d6cfbdd1e5b5553fd71e3bfc(
    *,
    claim: typing.Optional[builtins.str] = None,
    match_type: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ee55531c8fd535053b9a99a3002aba33c53a37e5e8cc29a59278aba611b246(
    *,
    ambiguous_role_resolution: typing.Optional[builtins.str] = None,
    identity_provider: typing.Optional[builtins.str] = None,
    rules_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentityPoolRoleAttachmentPropsMixin.RulesConfigurationTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e77f7a0af99852e72568ca368b9516a74f44dbec61c00b6945520e65eb8c6c(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentityPoolRoleAttachmentPropsMixin.MappingRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7dc0fd1985ad951a09c32b0ba2125be6c457dbdd7776fdcb1c9338bfb2134c(
    *,
    log_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLogDeliveryConfigurationPropsMixin.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed6f05b2201a8e9047fd68640758506144467fe4b6428bb525a903cafb2c960(
    props: typing.Union[CfnLogDeliveryConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5892764c73e4e82f5843e3c919356c946b9acdc6ec48ad04bb22e97472727481(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b17db6b74f8c6b7d62f91ed4bedc6dac67d4a87e0c46fd0d56c3b74ebb513ff(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e262cd546721d0e261a4ddba3f87a5888b52f27f048a44df94827dac8333aa51(
    *,
    log_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec235e874eafe7f5a05155fac7646add3fe391efb69ba9c172b04cd249b9ed38(
    *,
    stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c88f4e4809609dd8c8eb72fceda2839eb4bd051dae401860bdc87b8eb974a9(
    *,
    cloud_watch_logs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLogDeliveryConfigurationPropsMixin.CloudWatchLogsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_source: typing.Optional[builtins.str] = None,
    firehose_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLogDeliveryConfigurationPropsMixin.FirehoseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_level: typing.Optional[builtins.str] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLogDeliveryConfigurationPropsMixin.S3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46d27b5076b2ed38018d69680a95bedadfce5cbd004bb04ee6c3c8315c0b08b(
    *,
    bucket_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e330787a0be824f4f51ab86296111b41dfe8ebda32bd0c74f5c629a371f839(
    *,
    assets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnManagedLoginBrandingPropsMixin.AssetTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    client_id: typing.Optional[builtins.str] = None,
    return_merged_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    settings: typing.Any = None,
    use_cognito_provided_values: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecfe74d36dab9813eef90dc6cdaa29eb4852bdcbf1914d65617cb153fe2b836(
    props: typing.Union[CfnManagedLoginBrandingMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3906a9848a69e5e5e4a49360589157dea0ffb558e1af09c579f6020edf52814(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc97a067735caf25eeab8dbff072cf54d9edf492d8c38f5dd147435b9de4aed(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61b5fb1f0562c023bdb570ff994a8ed6bdb641da85d627afca099f926bac8b6(
    *,
    bytes: typing.Optional[builtins.str] = None,
    category: typing.Optional[builtins.str] = None,
    color_mode: typing.Optional[builtins.str] = None,
    extension: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50edd69682d897f64e6a8e00e18625250720173bfd2b3a93a6a57e9890d5b9ca(
    *,
    client_id: typing.Optional[builtins.str] = None,
    enforcement: typing.Optional[builtins.str] = None,
    links: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    terms_name: typing.Optional[builtins.str] = None,
    terms_source: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd579d5524dde035def5068b60abb4291090b621aaaf64e0dceb3af0b5869d6c(
    props: typing.Union[CfnTermsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b03237ac9820180897c64f4e711a27fb1800b4803f9b6fa647a4e8e5085da24(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12bfefcccc355f52b3a3b71dffd2c558f89c4d7e2eac8d6cb2a605b118141109(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4db235510fc5eb251fa30acb177907f4382335645fc74a776d26e2b183a4de(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab0278a1a87376bbe7ef47b9b12523351081708f498ccbb854c50f112c19d8a(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26c56616c3e8cae4a801e66825c009e52b03a58064b7370625db0f3242af699(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e532d389795ac4922c47d8ce6cacb3d723d5e3f8de091a81a562936c9559ce4(
    *,
    access_token_validity: typing.Optional[jsii.Number] = None,
    allowed_o_auth_flows: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_o_auth_flows_user_pool_client: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    allowed_o_auth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    analytics_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolClientPropsMixin.AnalyticsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auth_session_validity: typing.Optional[jsii.Number] = None,
    callback_ur_ls: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_name: typing.Optional[builtins.str] = None,
    default_redirect_uri: typing.Optional[builtins.str] = None,
    enable_propagate_additional_user_context_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_token_revocation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    explicit_auth_flows: typing.Optional[typing.Sequence[builtins.str]] = None,
    generate_secret: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    id_token_validity: typing.Optional[jsii.Number] = None,
    logout_ur_ls: typing.Optional[typing.Sequence[builtins.str]] = None,
    prevent_user_existence_errors: typing.Optional[builtins.str] = None,
    read_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    refresh_token_rotation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolClientPropsMixin.RefreshTokenRotationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    refresh_token_validity: typing.Optional[jsii.Number] = None,
    supported_identity_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    token_validity_units: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolClientPropsMixin.TokenValidityUnitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
    write_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b63a49343b23ab25d840335f4463698504a034a39338fdda7c875103036248(
    props: typing.Union[CfnUserPoolClientMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4623a022f2c8c9b26f180bba43525e5ac3b20f34c0081a5ab8bdf9112b0c775a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb4011ec7b79d05bcbe288b3736f4b905388ff454842ecd2fd84f90e8ad4346(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e332caa52c3ae7ca3bde041e68ce083c5fa259abda034e66762e877a679ce44f(
    *,
    application_arn: typing.Optional[builtins.str] = None,
    application_id: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    user_data_shared: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613c8c20af6e35d6859a7cfb9597b5eae4f28578e550ca3b6685280877fe131a(
    *,
    feature: typing.Optional[builtins.str] = None,
    retry_grace_period_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f9e8cbfdc24a7b3fee76419a3cb061a0e1d19a3d9df14651f951cf5308ae0c(
    *,
    access_token: typing.Optional[builtins.str] = None,
    id_token: typing.Optional[builtins.str] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e66606d15225fd4d37f6f40ef6a7ae86addd65389adadcac33c7941641856e(
    *,
    custom_domain_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolDomainPropsMixin.CustomDomainConfigTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain: typing.Optional[builtins.str] = None,
    managed_login_version: typing.Optional[jsii.Number] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358f34659721db949b690457fcdd4f91bace3b0a360abdbe9fbeef71153097a4(
    props: typing.Union[CfnUserPoolDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e22b6171f38af8b33ceb1119a0e59768dc766baa9511f6799d456ebb7d9730(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68be555aa86942219471838a71fa05968a43e212ff693c6c8a07df542b200a4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64ddacc1502f003abdad85c8c1c2007177671b73ee3b1f2cd2cd6ea2a3a9076(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df84da68a329c74e004f6e48b071c91c4ba6b3147e626ea71f52a50db1558c90(
    *,
    description: typing.Optional[builtins.str] = None,
    group_name: typing.Optional[builtins.str] = None,
    precedence: typing.Optional[jsii.Number] = None,
    role_arn: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b54f7d09a2ab1419a594e60ffc241db1b7a4025cd7d4db53bcf498b89f6c0c5(
    props: typing.Union[CfnUserPoolGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdec3efe2e32098d40027daa512a05c00f59e2d11d01062dff34e479706e2ea9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c987314f58dc906b6e86ee12863fd1b779702be2f1d78d1f4205a9135d734b5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad95163e1e5fe169b249166175ef3afbd380dbb9c879b749aab9243d262d69e(
    *,
    attribute_mapping: typing.Any = None,
    idp_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    provider_details: typing.Any = None,
    provider_name: typing.Optional[builtins.str] = None,
    provider_type: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee8f564c09c0f730f44abae0eb4b415ffc4129ab4dbb0b5cd455edffd408b02(
    props: typing.Union[CfnUserPoolIdentityProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f288797fd7e05b3471c17a0de30dd3ffa1dcc891fcfbf02cf574e8fb9f46dc3a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e35daa5ca12236e2cd7bf12d369f5b4692f04eedfa1d6e7f2329bc094a5503c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1fb4dc936c2a21510ac01fd7735b0c69e8eee810ebf0ac9f27186cc0b9cfed(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ae5f776c379223f34a1e1c04661d4c79c53a2167b542fd232aeea78662a380(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71756f1b68c5e7898a7f60f96d7b0875296ce17a423aa9053941555354131f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b4eb0e7220a005c8b0ba6bd6da0c1c84e2acc270ad0946b545ce105d321867(
    *,
    account_recovery_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.AccountRecoverySettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    admin_create_user_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.AdminCreateUserConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    alias_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_verified_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[builtins.str] = None,
    device_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.DeviceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    email_authentication_message: typing.Optional[builtins.str] = None,
    email_authentication_subject: typing.Optional[builtins.str] = None,
    email_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.EmailConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    email_verification_message: typing.Optional[builtins.str] = None,
    email_verification_subject: typing.Optional[builtins.str] = None,
    enabled_mfas: typing.Optional[typing.Sequence[builtins.str]] = None,
    lambda_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mfa_configuration: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.PoliciesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.SchemaAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    sms_authentication_message: typing.Optional[builtins.str] = None,
    sms_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.SmsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sms_verification_message: typing.Optional[builtins.str] = None,
    user_attribute_update_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.UserAttributeUpdateSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    username_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    username_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.UsernameConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_pool_add_ons: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.UserPoolAddOnsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_pool_name: typing.Optional[builtins.str] = None,
    user_pool_tags: typing.Any = None,
    user_pool_tier: typing.Optional[builtins.str] = None,
    verification_message_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.VerificationMessageTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    web_authn_relying_party_id: typing.Optional[builtins.str] = None,
    web_authn_user_verification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d554208e2da41ddcef3ae18f20026408f2e78fdf626a88e252dd98aff0d82e(
    props: typing.Union[CfnUserPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6db27c3b3965403f5875859a06d7836b47192e5ae073bc7ba2b015e84faebd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea9c45d0f50699a5d6887a5b3f0331e264e18dbced3e5b69cf53bd1a25a5d7f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37deb353af10c224b4a2543dde1921c0c6742397a53b41b2a4bbc501a284a58(
    *,
    recovery_mechanisms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.RecoveryOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4cd99587e534d381f9835a3824aaf31173bcb4b8124748e662ca5bc0ce2bf25(
    *,
    allow_admin_create_user_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    invite_message_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.InviteMessageTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    unused_account_validity_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4bbba40f607275e69bf26e843a8c67bd6535e93bd7c1eeb7c4a20a62ae903d(
    *,
    custom_auth_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73af3177e974a2e869fa9e007f41ce3f8032787bd8581b976997db9c7e8ba64(
    *,
    lambda_arn: typing.Optional[builtins.str] = None,
    lambda_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674bca0bca940515ceefc699729b8d1545a40ee53bba87da7c4f686da3e3c8b6(
    *,
    lambda_arn: typing.Optional[builtins.str] = None,
    lambda_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2aef09c6b425659a4aaa710804d63183ce7cb73e3b5ee0800fa78020987d4d1(
    *,
    challenge_required_on_new_device: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    device_only_remembered_on_user_prompt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ab99ce231b12bfb027f5f68af56cebfb3d524a5e2ac8b1c13be4dbf287e5f3(
    *,
    configuration_set: typing.Optional[builtins.str] = None,
    email_sending_account: typing.Optional[builtins.str] = None,
    from_: typing.Optional[builtins.str] = None,
    reply_to_email_address: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d187426586a42084d4a1511ffc21221e7220be7964c86f7cbdd071471447b7(
    *,
    email_message: typing.Optional[builtins.str] = None,
    email_subject: typing.Optional[builtins.str] = None,
    sms_message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65103e5cf2c7380c0ecd07f02f4a4c1ea091a78147746bd7a57a2fd49a6fc886(
    *,
    create_auth_challenge: typing.Optional[builtins.str] = None,
    custom_email_sender: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.CustomEmailSenderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_message: typing.Optional[builtins.str] = None,
    custom_sms_sender: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.CustomSMSSenderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    define_auth_challenge: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    post_authentication: typing.Optional[builtins.str] = None,
    post_confirmation: typing.Optional[builtins.str] = None,
    pre_authentication: typing.Optional[builtins.str] = None,
    pre_sign_up: typing.Optional[builtins.str] = None,
    pre_token_generation: typing.Optional[builtins.str] = None,
    pre_token_generation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.PreTokenGenerationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_migration: typing.Optional[builtins.str] = None,
    verify_auth_challenge_response: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89988d61e2f0a35f24155e7f199b54a505941559e2a182b2636f18cb32474a4a(
    *,
    max_value: typing.Optional[builtins.str] = None,
    min_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3196a187243e4fad17f7d8bbb0b72212dfcd771265ecce6669519d4aef2e1b(
    *,
    minimum_length: typing.Optional[jsii.Number] = None,
    password_history_size: typing.Optional[jsii.Number] = None,
    require_lowercase: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_numbers: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_symbols: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_uppercase: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    temporary_password_validity_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3ae7f7d28fac3a4c70fe4ce669b7df7f18177b066f44ebfa9563dee7a54d41(
    *,
    password_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.PasswordPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sign_in_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.SignInPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f85ba6f0c51363de6ace5233467621d3bdfbda2a6e1a72957682753d3733956(
    *,
    lambda_arn: typing.Optional[builtins.str] = None,
    lambda_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0922a3d3f95cada5344420464005a99f31eeb5f2d43801f6bb21432f9fd0baf(
    *,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f193ffa1c73e08598e11778b2fa6daf2e97ecb8d5dba9faaa8663b157e3e5b62(
    *,
    attribute_data_type: typing.Optional[builtins.str] = None,
    developer_only_attribute: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    mutable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    number_attribute_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.NumberAttributeConstraintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    string_attribute_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.StringAttributeConstraintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d315d482fe59a2097c8690f5629d1a758b692bfd959c9e4c5d739226a57d0754(
    *,
    allowed_first_auth_factors: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa14a5e3ca16a6ba478ce6806526d77db9c4300d404a57126ec544c2f0621c0(
    *,
    external_id: typing.Optional[builtins.str] = None,
    sns_caller_arn: typing.Optional[builtins.str] = None,
    sns_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839792d52dc06409222f843bcf48e7733ed636508fa5cd1d8d128874214a3f84(
    *,
    max_length: typing.Optional[builtins.str] = None,
    min_length: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a904a94de7bbe7bc3c476ff8d4f61a27e9dc49fde101198f9e13c21272864a(
    *,
    attributes_require_verification_before_update: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bee5b6675cddb872158b231f7ad1d372edb7db236f886e9076fe9103227395(
    *,
    advanced_security_additional_flows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolPropsMixin.AdvancedSecurityAdditionalFlowsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    advanced_security_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf733e1fe322d182e7f5339a664e78eabf0b6ebfcaf4eb05d3f381eb3e14bce(
    *,
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9135c349e152da1db72c849369a0ba11f4e87df06249ba29adf2e8a6ba50602d(
    *,
    default_email_option: typing.Optional[builtins.str] = None,
    email_message: typing.Optional[builtins.str] = None,
    email_message_by_link: typing.Optional[builtins.str] = None,
    email_subject: typing.Optional[builtins.str] = None,
    email_subject_by_link: typing.Optional[builtins.str] = None,
    sms_message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f22de66f81ae3a647fd8406b34be954145013bd316552668da42482a69789a4(
    *,
    identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolResourceServerPropsMixin.ResourceServerScopeTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0770b40e72391a6c945a4ed8ca6914479c6e02713d6c3f8c73a8994bc011586b(
    props: typing.Union[CfnUserPoolResourceServerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a22928a86e5ba8adca1c7a422836b471d63104f95f4c5a01f4b9bea1cca683b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d592c676ee26f852399d3f880bc90920ae7a657f8a462664a9da626db4541025(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6433e17ce7bfaaca2e01b8464c2c5bad4b5326ec0b8606692db302e34843bf(
    *,
    scope_description: typing.Optional[builtins.str] = None,
    scope_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beba5baf1167c4ec99de20b2008c3bf527fb8a56065f80566e497e3c730a6ba2(
    *,
    account_takeover_risk_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverRiskConfigurationTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    client_id: typing.Optional[builtins.str] = None,
    compromised_credentials_risk_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsRiskConfigurationTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    risk_exception_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.RiskExceptionConfigurationTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93192f2e1fc7c5049ccecdcae4bde64696ae11d62c284ab385196cab219b65ec(
    props: typing.Union[CfnUserPoolRiskConfigurationAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea5ae5a393a4302402218860870b4c34efcdc4e40f50b2689341d40c11cb7cc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258bd0a3de4fec6e4c36e1523db36e13f4cba089509259a662a768a4921c953d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f167401bf0c4da9beff9ad04b852943b30f0c79f2d60b9ac1344bb0f23ee7982(
    *,
    event_action: typing.Optional[builtins.str] = None,
    notify: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59dade50c619211325532c6884779119cf1f77848617803ffe7474e1a19668d9(
    *,
    high_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    low_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    medium_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0298b663676a52d42fee0a69572d01b3d15f2fe971b8465216f979bff0dd8c45(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.AccountTakeoverActionsTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    notify_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyConfigurationTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb33fef7634374502d211b06833dba2bdad6ed768c610515c50659069b024258(
    *,
    event_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc58a9ae23c713c2f62956ce8db972888aa755af33a2a9477d89cd5b5f401d27(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.CompromisedCredentialsActionsTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5631343483d8904bb763c1c6138811195e6f62fdba49c358fb5ee1a89433123c(
    *,
    block_email: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    from_: typing.Optional[builtins.str] = None,
    mfa_email: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    no_action_email: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolRiskConfigurationAttachmentPropsMixin.NotifyEmailTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    reply_to: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59300f032446f124979ba74a7276aee9ad24860c364eb27738e26a115571b9d4(
    *,
    html_body: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
    text_body: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad09d4794a4c4794a1305dea288466c07d30fe7a5d0e64df1ff67b44ff0ecd6(
    *,
    blocked_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    skipped_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c14acb1204af4805e1423f497b62f5a51515a8b3b55332e2d046ad32d3ab90(
    *,
    client_id: typing.Optional[builtins.str] = None,
    css: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc519a0f1b05cf69d3ce974e4106fe5d0c0ffa26e642770d72390311f2fe81e5(
    props: typing.Union[CfnUserPoolUICustomizationAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96120b5d71319f26da24a98deb19000042602b0764169f76aa8107e52b004196(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d68447a947f163c28096a4cd044c2b3b3ed4cf881b1eb06bc75b6ddf7ed2c6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f299bb36816a063080972c8f8b6135ae6c362760c3044f1e00e5e19b8fa26b2a(
    *,
    client_metadata: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    desired_delivery_mediums: typing.Optional[typing.Sequence[builtins.str]] = None,
    force_alias_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    message_action: typing.Optional[builtins.str] = None,
    user_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolUserPropsMixin.AttributeTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    username: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
    validation_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPoolUserPropsMixin.AttributeTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d296cc9d1d383068e6d10ba36615b95c0827d9ac427124a96e7af565decd87e(
    props: typing.Union[CfnUserPoolUserMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f42433ae8cdd1d649731e207c78f87822766ad03baa5d12a39382cde1a59fd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad49972e65e7bc4709616563ae9de5bdf450f74db5d78beb116811f7f718d5ee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af9f1b5e19b28052eb6597fdfb7e4c23031e57e63af83cb1c45fd149520988b(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee93abc2bb82b8b72c9bcda38096d761cd417b91a7e1fc31c24471eb32f809a2(
    *,
    group_name: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8ebfa91f39004c1a522367c28cf35d9ff8c2f19b88ecdd67daf94a7196478f(
    props: typing.Union[CfnUserPoolUserToGroupAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf67189ee01e05ad7323e686c809ff4882163a8fc4ea8545d00f2aa797d1f3a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c0259d725c9a9acae560c6398df369893a8eb8b73370e2a633da0aeee9ca0b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
