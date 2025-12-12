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
    jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "policy_store_id": "policyStoreId",
        "principal_entity_type": "principalEntityType",
    },
)
class CfnIdentitySourceMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentitySourcePropsMixin.IdentitySourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        policy_store_id: typing.Optional[builtins.str] = None,
        principal_entity_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIdentitySourcePropsMixin.

        :param configuration: Contains configuration information used when creating a new identity source.
        :param policy_store_id: Specifies the ID of the policy store in which you want to store this identity source. Only policies and requests made using this policy store can reference identities from the identity provider configured in the new identity source.
        :param principal_entity_type: Specifies the namespace and data type of the principals generated for identities authenticated by the new identity source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-identitysource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
            
            cfn_identity_source_mixin_props = verifiedpermissions_mixins.CfnIdentitySourceMixinProps(
                configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.IdentitySourceConfigurationProperty(
                    cognito_user_pool_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.CognitoUserPoolConfigurationProperty(
                        client_ids=["clientIds"],
                        group_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.CognitoGroupConfigurationProperty(
                            group_entity_type="groupEntityType"
                        ),
                        user_pool_arn="userPoolArn"
                    ),
                    open_id_connect_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectConfigurationProperty(
                        entity_id_prefix="entityIdPrefix",
                        group_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectGroupConfigurationProperty(
                            group_claim="groupClaim",
                            group_entity_type="groupEntityType"
                        ),
                        issuer="issuer",
                        token_selection=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectTokenSelectionProperty(
                            access_token_only=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty(
                                audiences=["audiences"],
                                principal_id_claim="principalIdClaim"
                            ),
                            identity_token_only=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty(
                                client_ids=["clientIds"],
                                principal_id_claim="principalIdClaim"
                            )
                        )
                    )
                ),
                policy_store_id="policyStoreId",
                principal_entity_type="principalEntityType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda88177405e83bed311910442c1eb0bce5802fcaec2f5aaf5b09d3580f093f4)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument policy_store_id", value=policy_store_id, expected_type=type_hints["policy_store_id"])
            check_type(argname="argument principal_entity_type", value=principal_entity_type, expected_type=type_hints["principal_entity_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if policy_store_id is not None:
            self._values["policy_store_id"] = policy_store_id
        if principal_entity_type is not None:
            self._values["principal_entity_type"] = principal_entity_type

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.IdentitySourceConfigurationProperty"]]:
        '''Contains configuration information used when creating a new identity source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-identitysource.html#cfn-verifiedpermissions-identitysource-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.IdentitySourceConfigurationProperty"]], result)

    @builtins.property
    def policy_store_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the ID of the policy store in which you want to store this identity source.

        Only policies and requests made using this policy store can reference identities from the identity provider configured in the new identity source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-identitysource.html#cfn-verifiedpermissions-identitysource-policystoreid
        '''
        result = self._values.get("policy_store_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal_entity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the namespace and data type of the principals generated for identities authenticated by the new identity source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-identitysource.html#cfn-verifiedpermissions-identitysource-principalentitytype
        '''
        result = self._values.get("principal_entity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdentitySourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdentitySourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourcePropsMixin",
):
    '''Creates or updates a reference to Amazon Cognito as an external identity provider.

    If you are creating a new identity source, then you must specify a ``Configuration`` . If you are updating an existing identity source, then you must specify an ``UpdateConfiguration`` .

    After you create an identity source, you can use the identities provided by the IdP as proxies for the principal in authorization queries that use the `IsAuthorizedWithToken <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_IsAuthorizedWithToken.html>`_ operation. These identities take the form of tokens that contain claims about the user, such as IDs, attributes and group memberships. Amazon Cognito provides both identity tokens and access tokens, and Verified Permissions can use either or both. Any combination of identity and access tokens results in the same Cedar principal. Verified Permissions automatically translates the information about the identities into the standard Cedar attributes that can be evaluated by your policies. Because the Amazon Cognito identity and access tokens can contain different information, the tokens you choose to use determine the attributes that are available to access in the Cedar principal from your policies.

    Amazon Cognito Identity is not available in all of the same AWS Regions as  . Because of this, the ``AWS::VerifiedPermissions::IdentitySource`` type is not available to create from CloudFormation in Regions where Amazon Cognito Identity is not currently available. Users can still create ``AWS::VerifiedPermissions::IdentitySource`` in those Regions, but only from the AWS CLI ,  SDK, or from the AWS console.
    .. epigraph::

       To reference a user from this identity source in your Cedar policies, use the following syntax.

       *IdentityType::"|*

       Where ``IdentityType`` is the string that you provide to the ``PrincipalEntityType`` parameter for this operation. The ``CognitoUserPoolId`` and ``CognitoClientId`` are defined by the Amazon Cognito user pool.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-identitysource.html
    :cloudformationResource: AWS::VerifiedPermissions::IdentitySource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
        
        cfn_identity_source_props_mixin = verifiedpermissions_mixins.CfnIdentitySourcePropsMixin(verifiedpermissions_mixins.CfnIdentitySourceMixinProps(
            configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.IdentitySourceConfigurationProperty(
                cognito_user_pool_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.CognitoUserPoolConfigurationProperty(
                    client_ids=["clientIds"],
                    group_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.CognitoGroupConfigurationProperty(
                        group_entity_type="groupEntityType"
                    ),
                    user_pool_arn="userPoolArn"
                ),
                open_id_connect_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectConfigurationProperty(
                    entity_id_prefix="entityIdPrefix",
                    group_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectGroupConfigurationProperty(
                        group_claim="groupClaim",
                        group_entity_type="groupEntityType"
                    ),
                    issuer="issuer",
                    token_selection=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectTokenSelectionProperty(
                        access_token_only=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty(
                            audiences=["audiences"],
                            principal_id_claim="principalIdClaim"
                        ),
                        identity_token_only=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty(
                            client_ids=["clientIds"],
                            principal_id_claim="principalIdClaim"
                        )
                    )
                )
            ),
            policy_store_id="policyStoreId",
            principal_entity_type="principalEntityType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIdentitySourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VerifiedPermissions::IdentitySource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab854a58acf88c9972606bf46fdb9fed434d9450061c65b20d64725c686f4f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3721cbd400042512733e75c2e1a25eed446d200c73891bac96080e295c1f40e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01651ac556dd449cd3590281be4fa0803cbb78f28dec23c9a8ccb3d5c61dcd33)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdentitySourceMixinProps:
        return typing.cast(CfnIdentitySourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourcePropsMixin.CognitoGroupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"group_entity_type": "groupEntityType"},
    )
    class CognitoGroupConfigurationProperty:
        def __init__(
            self,
            *,
            group_entity_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The type of entity that a policy store maps to groups from an Amazon Cognito user pool identity source.

            :param group_entity_type: The name of the schema entity type that's mapped to the user pool group. Defaults to ``AWS::CognitoGroup`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-cognitogroupconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                cognito_group_configuration_property = verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.CognitoGroupConfigurationProperty(
                    group_entity_type="groupEntityType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c1ef244582538b174ef25ef522890d4d07d417df9543fb9b4c5a6fed9b06f39b)
                check_type(argname="argument group_entity_type", value=group_entity_type, expected_type=type_hints["group_entity_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_entity_type is not None:
                self._values["group_entity_type"] = group_entity_type

        @builtins.property
        def group_entity_type(self) -> typing.Optional[builtins.str]:
            '''The name of the schema entity type that's mapped to the user pool group.

            Defaults to ``AWS::CognitoGroup`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-cognitogroupconfiguration.html#cfn-verifiedpermissions-identitysource-cognitogroupconfiguration-groupentitytype
            '''
            result = self._values.get("group_entity_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoGroupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourcePropsMixin.CognitoUserPoolConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_ids": "clientIds",
            "group_configuration": "groupConfiguration",
            "user_pool_arn": "userPoolArn",
        },
    )
    class CognitoUserPoolConfigurationProperty:
        def __init__(
            self,
            *,
            client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            group_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentitySourcePropsMixin.CognitoGroupConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            user_pool_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains configuration information used when creating or updating an identity source that represents a connection to an Amazon Cognito user pool used as an identity provider for Verified Permissions .

            :param client_ids: The unique application client IDs that are associated with the specified Amazon Cognito user pool. Example: ``"ClientIds": ["&ExampleCogClientId;"]``
            :param group_configuration: The type of entity that a policy store maps to groups from an Amazon Cognito user pool identity source.
            :param user_pool_arn: The `Amazon Resource Name (ARN) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the Amazon Cognito user pool that contains the identities to be authorized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-cognitouserpoolconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                cognito_user_pool_configuration_property = verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.CognitoUserPoolConfigurationProperty(
                    client_ids=["clientIds"],
                    group_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.CognitoGroupConfigurationProperty(
                        group_entity_type="groupEntityType"
                    ),
                    user_pool_arn="userPoolArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8b768ea020da52f15fc3c7b7e92de35b04a245b0f11aaa7af80b7f5d3b4b1cf)
                check_type(argname="argument client_ids", value=client_ids, expected_type=type_hints["client_ids"])
                check_type(argname="argument group_configuration", value=group_configuration, expected_type=type_hints["group_configuration"])
                check_type(argname="argument user_pool_arn", value=user_pool_arn, expected_type=type_hints["user_pool_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_ids is not None:
                self._values["client_ids"] = client_ids
            if group_configuration is not None:
                self._values["group_configuration"] = group_configuration
            if user_pool_arn is not None:
                self._values["user_pool_arn"] = user_pool_arn

        @builtins.property
        def client_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The unique application client IDs that are associated with the specified Amazon Cognito user pool.

            Example: ``"ClientIds": ["&ExampleCogClientId;"]``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-cognitouserpoolconfiguration.html#cfn-verifiedpermissions-identitysource-cognitouserpoolconfiguration-clientids
            '''
            result = self._values.get("client_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def group_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.CognitoGroupConfigurationProperty"]]:
            '''The type of entity that a policy store maps to groups from an Amazon Cognito user pool identity source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-cognitouserpoolconfiguration.html#cfn-verifiedpermissions-identitysource-cognitouserpoolconfiguration-groupconfiguration
            '''
            result = self._values.get("group_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.CognitoGroupConfigurationProperty"]], result)

        @builtins.property
        def user_pool_arn(self) -> typing.Optional[builtins.str]:
            '''The `Amazon Resource Name (ARN) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the Amazon Cognito user pool that contains the identities to be authorized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-cognitouserpoolconfiguration.html#cfn-verifiedpermissions-identitysource-cognitouserpoolconfiguration-userpoolarn
            '''
            result = self._values.get("user_pool_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoUserPoolConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourcePropsMixin.IdentitySourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cognito_user_pool_configuration": "cognitoUserPoolConfiguration",
            "open_id_connect_configuration": "openIdConnectConfiguration",
        },
    )
    class IdentitySourceConfigurationProperty:
        def __init__(
            self,
            *,
            cognito_user_pool_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentitySourcePropsMixin.CognitoUserPoolConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            open_id_connect_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentitySourcePropsMixin.OpenIdConnectConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains configuration information used when creating or updating a new identity source.

            .. epigraph::

               At this time, the only valid member of this structure is a Amazon Cognito user pool configuration.

               You must specify a ``userPoolArn`` , and optionally, a ``ClientId`` .

            :param cognito_user_pool_configuration: A structure that contains configuration information used when creating or updating an identity source that represents a connection to an Amazon Cognito user pool used as an identity provider for Verified Permissions .
            :param open_id_connect_configuration: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-identitysourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                identity_source_configuration_property = verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.IdentitySourceConfigurationProperty(
                    cognito_user_pool_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.CognitoUserPoolConfigurationProperty(
                        client_ids=["clientIds"],
                        group_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.CognitoGroupConfigurationProperty(
                            group_entity_type="groupEntityType"
                        ),
                        user_pool_arn="userPoolArn"
                    ),
                    open_id_connect_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectConfigurationProperty(
                        entity_id_prefix="entityIdPrefix",
                        group_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectGroupConfigurationProperty(
                            group_claim="groupClaim",
                            group_entity_type="groupEntityType"
                        ),
                        issuer="issuer",
                        token_selection=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectTokenSelectionProperty(
                            access_token_only=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty(
                                audiences=["audiences"],
                                principal_id_claim="principalIdClaim"
                            ),
                            identity_token_only=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty(
                                client_ids=["clientIds"],
                                principal_id_claim="principalIdClaim"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a54e4299e5bb8133648bb8a1d2e134121b107356b076f5edbd9d8ef044756e0b)
                check_type(argname="argument cognito_user_pool_configuration", value=cognito_user_pool_configuration, expected_type=type_hints["cognito_user_pool_configuration"])
                check_type(argname="argument open_id_connect_configuration", value=open_id_connect_configuration, expected_type=type_hints["open_id_connect_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cognito_user_pool_configuration is not None:
                self._values["cognito_user_pool_configuration"] = cognito_user_pool_configuration
            if open_id_connect_configuration is not None:
                self._values["open_id_connect_configuration"] = open_id_connect_configuration

        @builtins.property
        def cognito_user_pool_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.CognitoUserPoolConfigurationProperty"]]:
            '''A structure that contains configuration information used when creating or updating an identity source that represents a connection to an Amazon Cognito user pool used as an identity provider for Verified Permissions .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-identitysourceconfiguration.html#cfn-verifiedpermissions-identitysource-identitysourceconfiguration-cognitouserpoolconfiguration
            '''
            result = self._values.get("cognito_user_pool_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.CognitoUserPoolConfigurationProperty"]], result)

        @builtins.property
        def open_id_connect_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.OpenIdConnectConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-identitysourceconfiguration.html#cfn-verifiedpermissions-identitysource-identitysourceconfiguration-openidconnectconfiguration
            '''
            result = self._values.get("open_id_connect_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.OpenIdConnectConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentitySourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourcePropsMixin.IdentitySourceDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_ids": "clientIds",
            "discovery_url": "discoveryUrl",
            "open_id_issuer": "openIdIssuer",
            "user_pool_arn": "userPoolArn",
        },
    )
    class IdentitySourceDetailsProperty:
        def __init__(
            self,
            *,
            client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            discovery_url: typing.Optional[builtins.str] = None,
            open_id_issuer: typing.Optional[builtins.str] = None,
            user_pool_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param client_ids: 
            :param discovery_url: 
            :param open_id_issuer: 
            :param user_pool_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-identitysourcedetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                identity_source_details_property = verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.IdentitySourceDetailsProperty(
                    client_ids=["clientIds"],
                    discovery_url="discoveryUrl",
                    open_id_issuer="openIdIssuer",
                    user_pool_arn="userPoolArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4d6aaf6c1d9dd5e1cdce6013aab00e1825d608cd69613539958a42b1b91ff4a)
                check_type(argname="argument client_ids", value=client_ids, expected_type=type_hints["client_ids"])
                check_type(argname="argument discovery_url", value=discovery_url, expected_type=type_hints["discovery_url"])
                check_type(argname="argument open_id_issuer", value=open_id_issuer, expected_type=type_hints["open_id_issuer"])
                check_type(argname="argument user_pool_arn", value=user_pool_arn, expected_type=type_hints["user_pool_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_ids is not None:
                self._values["client_ids"] = client_ids
            if discovery_url is not None:
                self._values["discovery_url"] = discovery_url
            if open_id_issuer is not None:
                self._values["open_id_issuer"] = open_id_issuer
            if user_pool_arn is not None:
                self._values["user_pool_arn"] = user_pool_arn

        @builtins.property
        def client_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-identitysourcedetails.html#cfn-verifiedpermissions-identitysource-identitysourcedetails-clientids
            '''
            result = self._values.get("client_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def discovery_url(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-identitysourcedetails.html#cfn-verifiedpermissions-identitysource-identitysourcedetails-discoveryurl
            '''
            result = self._values.get("discovery_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def open_id_issuer(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-identitysourcedetails.html#cfn-verifiedpermissions-identitysource-identitysourcedetails-openidissuer
            '''
            result = self._values.get("open_id_issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-identitysourcedetails.html#cfn-verifiedpermissions-identitysource-identitysourcedetails-userpoolarn
            '''
            result = self._values.get("user_pool_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentitySourceDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audiences": "audiences",
            "principal_id_claim": "principalIdClaim",
        },
    )
    class OpenIdConnectAccessTokenConfigurationProperty:
        def __init__(
            self,
            *,
            audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
            principal_id_claim: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of an OpenID Connect (OIDC) identity source for handling access token claims.

            Contains the claim that you want to identify as the principal in an authorization request, and the values of the ``aud`` claim, or audiences, that you want to accept.

            This data type is part of a `OpenIdConnectTokenSelection <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_OpenIdConnectTokenSelection.html>`_ structure, which is a parameter of `CreateIdentitySource <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_CreateIdentitySource.html>`_ .

            :param audiences: The access token ``aud`` claim values that you want to accept in your policy store. For example, ``https://myapp.example.com, https://myapp2.example.com`` .
            :param principal_id_claim: The claim that determines the principal in OIDC access tokens. For example, ``sub`` . Default: - "sub"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectaccesstokenconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                open_id_connect_access_token_configuration_property = verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty(
                    audiences=["audiences"],
                    principal_id_claim="principalIdClaim"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad7a656707903564568235f1d6e418c3d79e82a99cb19d196eb1697232932893)
                check_type(argname="argument audiences", value=audiences, expected_type=type_hints["audiences"])
                check_type(argname="argument principal_id_claim", value=principal_id_claim, expected_type=type_hints["principal_id_claim"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audiences is not None:
                self._values["audiences"] = audiences
            if principal_id_claim is not None:
                self._values["principal_id_claim"] = principal_id_claim

        @builtins.property
        def audiences(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The access token ``aud`` claim values that you want to accept in your policy store.

            For example, ``https://myapp.example.com, https://myapp2.example.com`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectaccesstokenconfiguration.html#cfn-verifiedpermissions-identitysource-openidconnectaccesstokenconfiguration-audiences
            '''
            result = self._values.get("audiences")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def principal_id_claim(self) -> typing.Optional[builtins.str]:
            '''The claim that determines the principal in OIDC access tokens.

            For example, ``sub`` .

            :default: - "sub"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectaccesstokenconfiguration.html#cfn-verifiedpermissions-identitysource-openidconnectaccesstokenconfiguration-principalidclaim
            '''
            result = self._values.get("principal_id_claim")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenIdConnectAccessTokenConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourcePropsMixin.OpenIdConnectConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "entity_id_prefix": "entityIdPrefix",
            "group_configuration": "groupConfiguration",
            "issuer": "issuer",
            "token_selection": "tokenSelection",
        },
    )
    class OpenIdConnectConfigurationProperty:
        def __init__(
            self,
            *,
            entity_id_prefix: typing.Optional[builtins.str] = None,
            group_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentitySourcePropsMixin.OpenIdConnectGroupConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            issuer: typing.Optional[builtins.str] = None,
            token_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentitySourcePropsMixin.OpenIdConnectTokenSelectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains configuration details of an OpenID Connect (OIDC) identity provider, or identity source, that Verified Permissions can use to generate entities from authenticated identities.

            It specifies the issuer URL, token type that you want to use, and policy store entity details.

            This data type is part of a `Configuration <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_Configuration.html>`_ structure, which is a parameter to `CreateIdentitySource <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_CreateIdentitySource.html>`_ .

            :param entity_id_prefix: A descriptive string that you want to prefix to user entities from your OIDC identity provider. For example, if you set an ``entityIdPrefix`` of ``MyOIDCProvider`` , you can reference principals in your policies in the format ``MyCorp::User::MyOIDCProvider|Carlos`` .
            :param group_configuration: The claim in OIDC identity provider tokens that indicates a user's group membership, and the entity type that you want to map it to. For example, this object can map the contents of a ``groups`` claim to ``MyCorp::UserGroup`` .
            :param issuer: The issuer URL of an OIDC identity provider. This URL must have an OIDC discovery endpoint at the path ``.well-known/openid-configuration`` .
            :param token_selection: The token type that you want to process from your OIDC identity provider. Your policy store can process either identity (ID) or access tokens from a given OIDC identity source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                open_id_connect_configuration_property = verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectConfigurationProperty(
                    entity_id_prefix="entityIdPrefix",
                    group_configuration=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectGroupConfigurationProperty(
                        group_claim="groupClaim",
                        group_entity_type="groupEntityType"
                    ),
                    issuer="issuer",
                    token_selection=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectTokenSelectionProperty(
                        access_token_only=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty(
                            audiences=["audiences"],
                            principal_id_claim="principalIdClaim"
                        ),
                        identity_token_only=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty(
                            client_ids=["clientIds"],
                            principal_id_claim="principalIdClaim"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f90bfb08d86e5798b075868b865d067974adfe954f38732f5ba1343f2f8241e2)
                check_type(argname="argument entity_id_prefix", value=entity_id_prefix, expected_type=type_hints["entity_id_prefix"])
                check_type(argname="argument group_configuration", value=group_configuration, expected_type=type_hints["group_configuration"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
                check_type(argname="argument token_selection", value=token_selection, expected_type=type_hints["token_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entity_id_prefix is not None:
                self._values["entity_id_prefix"] = entity_id_prefix
            if group_configuration is not None:
                self._values["group_configuration"] = group_configuration
            if issuer is not None:
                self._values["issuer"] = issuer
            if token_selection is not None:
                self._values["token_selection"] = token_selection

        @builtins.property
        def entity_id_prefix(self) -> typing.Optional[builtins.str]:
            '''A descriptive string that you want to prefix to user entities from your OIDC identity provider.

            For example, if you set an ``entityIdPrefix`` of ``MyOIDCProvider`` , you can reference principals in your policies in the format ``MyCorp::User::MyOIDCProvider|Carlos`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectconfiguration.html#cfn-verifiedpermissions-identitysource-openidconnectconfiguration-entityidprefix
            '''
            result = self._values.get("entity_id_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.OpenIdConnectGroupConfigurationProperty"]]:
            '''The claim in OIDC identity provider tokens that indicates a user's group membership, and the entity type that you want to map it to.

            For example, this object can map the contents of a ``groups`` claim to ``MyCorp::UserGroup`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectconfiguration.html#cfn-verifiedpermissions-identitysource-openidconnectconfiguration-groupconfiguration
            '''
            result = self._values.get("group_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.OpenIdConnectGroupConfigurationProperty"]], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''The issuer URL of an OIDC identity provider.

            This URL must have an OIDC discovery endpoint at the path ``.well-known/openid-configuration`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectconfiguration.html#cfn-verifiedpermissions-identitysource-openidconnectconfiguration-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_selection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.OpenIdConnectTokenSelectionProperty"]]:
            '''The token type that you want to process from your OIDC identity provider.

            Your policy store can process either identity (ID) or access tokens from a given OIDC identity source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectconfiguration.html#cfn-verifiedpermissions-identitysource-openidconnectconfiguration-tokenselection
            '''
            result = self._values.get("token_selection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.OpenIdConnectTokenSelectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenIdConnectConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourcePropsMixin.OpenIdConnectGroupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_claim": "groupClaim",
            "group_entity_type": "groupEntityType",
        },
    )
    class OpenIdConnectGroupConfigurationProperty:
        def __init__(
            self,
            *,
            group_claim: typing.Optional[builtins.str] = None,
            group_entity_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The claim in OIDC identity provider tokens that indicates a user's group membership, and the entity type that you want to map it to.

            For example, this object can map the contents of a ``groups`` claim to ``MyCorp::UserGroup`` .

            This data type is part of a `OpenIdConnectConfiguration <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_OpenIdConnectConfiguration.html>`_ structure, which is a parameter of `CreateIdentitySource <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_CreateIdentitySource.html>`_ .

            :param group_claim: The token claim that you want Verified Permissions to interpret as group membership. For example, ``groups`` .
            :param group_entity_type: The policy store entity type that you want to map your users' group claim to. For example, ``MyCorp::UserGroup`` . A group entity type is an entity that can have a user entity type as a member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectgroupconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                open_id_connect_group_configuration_property = verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectGroupConfigurationProperty(
                    group_claim="groupClaim",
                    group_entity_type="groupEntityType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__122ba2af56f53817730cc1a9e28464de91a3ddd2995d56756ec507f70fa8686a)
                check_type(argname="argument group_claim", value=group_claim, expected_type=type_hints["group_claim"])
                check_type(argname="argument group_entity_type", value=group_entity_type, expected_type=type_hints["group_entity_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_claim is not None:
                self._values["group_claim"] = group_claim
            if group_entity_type is not None:
                self._values["group_entity_type"] = group_entity_type

        @builtins.property
        def group_claim(self) -> typing.Optional[builtins.str]:
            '''The token claim that you want Verified Permissions to interpret as group membership.

            For example, ``groups`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectgroupconfiguration.html#cfn-verifiedpermissions-identitysource-openidconnectgroupconfiguration-groupclaim
            '''
            result = self._values.get("group_claim")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_entity_type(self) -> typing.Optional[builtins.str]:
            '''The policy store entity type that you want to map your users' group claim to.

            For example, ``MyCorp::UserGroup`` . A group entity type is an entity that can have a user entity type as a member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectgroupconfiguration.html#cfn-verifiedpermissions-identitysource-openidconnectgroupconfiguration-groupentitytype
            '''
            result = self._values.get("group_entity_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenIdConnectGroupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_ids": "clientIds",
            "principal_id_claim": "principalIdClaim",
        },
    )
    class OpenIdConnectIdentityTokenConfigurationProperty:
        def __init__(
            self,
            *,
            client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            principal_id_claim: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of an OpenID Connect (OIDC) identity source for handling identity (ID) token claims.

            Contains the claim that you want to identify as the principal in an authorization request, and the values of the ``aud`` claim, or audiences, that you want to accept.

            This data type is part of a `OpenIdConnectTokenSelection <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_OpenIdConnectTokenSelection.html>`_ structure, which is a parameter of `CreateIdentitySource <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_CreateIdentitySource.html>`_ .

            :param client_ids: The ID token audience, or client ID, claim values that you want to accept in your policy store from an OIDC identity provider. For example, ``1example23456789, 2example10111213`` .
            :param principal_id_claim: The claim that determines the principal in OIDC access tokens. For example, ``sub`` . Default: - "sub"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectidentitytokenconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                open_id_connect_identity_token_configuration_property = verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty(
                    client_ids=["clientIds"],
                    principal_id_claim="principalIdClaim"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3939bbe475c548db0dd957591ac8b7243acb685cdad207be0217ed6766324a8)
                check_type(argname="argument client_ids", value=client_ids, expected_type=type_hints["client_ids"])
                check_type(argname="argument principal_id_claim", value=principal_id_claim, expected_type=type_hints["principal_id_claim"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_ids is not None:
                self._values["client_ids"] = client_ids
            if principal_id_claim is not None:
                self._values["principal_id_claim"] = principal_id_claim

        @builtins.property
        def client_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ID token audience, or client ID, claim values that you want to accept in your policy store from an OIDC identity provider.

            For example, ``1example23456789, 2example10111213`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectidentitytokenconfiguration.html#cfn-verifiedpermissions-identitysource-openidconnectidentitytokenconfiguration-clientids
            '''
            result = self._values.get("client_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def principal_id_claim(self) -> typing.Optional[builtins.str]:
            '''The claim that determines the principal in OIDC access tokens.

            For example, ``sub`` .

            :default: - "sub"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnectidentitytokenconfiguration.html#cfn-verifiedpermissions-identitysource-openidconnectidentitytokenconfiguration-principalidclaim
            '''
            result = self._values.get("principal_id_claim")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenIdConnectIdentityTokenConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnIdentitySourcePropsMixin.OpenIdConnectTokenSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token_only": "accessTokenOnly",
            "identity_token_only": "identityTokenOnly",
        },
    )
    class OpenIdConnectTokenSelectionProperty:
        def __init__(
            self,
            *,
            access_token_only: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            identity_token_only: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The token type that you want to process from your OIDC identity provider.

            Your policy store can process either identity (ID) or access tokens from a given OIDC identity source.

            This data type is part of a `OpenIdConnectConfiguration <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_OpenIdConnectConfiguration.html>`_ structure, which is a parameter of `CreateIdentitySource <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_CreateIdentitySource.html>`_ .

            :param access_token_only: The OIDC configuration for processing access tokens. Contains allowed audience claims, for example ``https://auth.example.com`` , and the claim that you want to map to the principal, for example ``sub`` .
            :param identity_token_only: The OIDC configuration for processing identity (ID) tokens. Contains allowed client ID claims, for example ``1example23456789`` , and the claim that you want to map to the principal, for example ``sub`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnecttokenselection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                open_id_connect_token_selection_property = verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectTokenSelectionProperty(
                    access_token_only=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty(
                        audiences=["audiences"],
                        principal_id_claim="principalIdClaim"
                    ),
                    identity_token_only=verifiedpermissions_mixins.CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty(
                        client_ids=["clientIds"],
                        principal_id_claim="principalIdClaim"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c722935bc38a3e6a6b248dca506d0ac943c5f652ea40fbafe4081f66b9a9a97)
                check_type(argname="argument access_token_only", value=access_token_only, expected_type=type_hints["access_token_only"])
                check_type(argname="argument identity_token_only", value=identity_token_only, expected_type=type_hints["identity_token_only"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token_only is not None:
                self._values["access_token_only"] = access_token_only
            if identity_token_only is not None:
                self._values["identity_token_only"] = identity_token_only

        @builtins.property
        def access_token_only(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty"]]:
            '''The OIDC configuration for processing access tokens.

            Contains allowed audience claims, for example ``https://auth.example.com`` , and the claim that you want to map to the principal, for example ``sub`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnecttokenselection.html#cfn-verifiedpermissions-identitysource-openidconnecttokenselection-accesstokenonly
            '''
            result = self._values.get("access_token_only")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty"]], result)

        @builtins.property
        def identity_token_only(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty"]]:
            '''The OIDC configuration for processing identity (ID) tokens.

            Contains allowed client ID claims, for example ``1example23456789`` , and the claim that you want to map to the principal, for example ``sub`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-identitysource-openidconnecttokenselection.html#cfn-verifiedpermissions-identitysource-openidconnecttokenselection-identitytokenonly
            '''
            result = self._values.get("identity_token_only")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenIdConnectTokenSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition", "policy_store_id": "policyStoreId"},
)
class CfnPolicyMixinProps:
    def __init__(
        self,
        *,
        definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.PolicyDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        policy_store_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPolicyPropsMixin.

        :param definition: Specifies the policy type and content to use for the new or updated policy. The definition structure must include either a ``Static`` or a ``TemplateLinked`` element.
        :param policy_store_id: Specifies the ``PolicyStoreId`` of the policy store you want to store the policy in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
            
            cfn_policy_mixin_props = verifiedpermissions_mixins.CfnPolicyMixinProps(
                definition=verifiedpermissions_mixins.CfnPolicyPropsMixin.PolicyDefinitionProperty(
                    static=verifiedpermissions_mixins.CfnPolicyPropsMixin.StaticPolicyDefinitionProperty(
                        description="description",
                        statement="statement"
                    ),
                    template_linked=verifiedpermissions_mixins.CfnPolicyPropsMixin.TemplateLinkedPolicyDefinitionProperty(
                        policy_template_id="policyTemplateId",
                        principal=verifiedpermissions_mixins.CfnPolicyPropsMixin.EntityIdentifierProperty(
                            entity_id="entityId",
                            entity_type="entityType"
                        ),
                        resource=verifiedpermissions_mixins.CfnPolicyPropsMixin.EntityIdentifierProperty(
                            entity_id="entityId",
                            entity_type="entityType"
                        )
                    )
                ),
                policy_store_id="policyStoreId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae7ca6168e1b90b6ec490dd73d93a9ca77740a0d5996a034cd84ba73ca248e54)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument policy_store_id", value=policy_store_id, expected_type=type_hints["policy_store_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if definition is not None:
            self._values["definition"] = definition
        if policy_store_id is not None:
            self._values["policy_store_id"] = policy_store_id

    @builtins.property
    def definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.PolicyDefinitionProperty"]]:
        '''Specifies the policy type and content to use for the new or updated policy.

        The definition structure must include either a ``Static`` or a ``TemplateLinked`` element.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policy.html#cfn-verifiedpermissions-policy-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.PolicyDefinitionProperty"]], result)

    @builtins.property
    def policy_store_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the ``PolicyStoreId`` of the policy store you want to store the policy in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policy.html#cfn-verifiedpermissions-policy-policystoreid
        '''
        result = self._values.get("policy_store_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyPropsMixin",
):
    '''Creates or updates a Cedar policy and saves it in the specified policy store.

    You can create either a static policy or a policy linked to a policy template.

    You can directly update only static policies. To update a template-linked policy, you must update its linked policy template instead.

    - To create a static policy, in the ``Definition`` include a ``Static`` element that includes the Cedar policy text in the ``Statement`` element.
    - To create a policy that is dynamically linked to a policy template, in the ``Definition`` include a ``Templatelinked`` element that specifies the policy template ID and the principal and resource to associate with this policy. If the policy template is ever updated, any policies linked to the policy template automatically use the updated template.

    .. epigraph::

       - If policy validation is enabled in the policy store, then updating a static policy causes Verified Permissions to validate the policy against the schema in the policy store. If the updated static policy doesn't pass validation, the operation fails and the update isn't stored.
       - When you edit a static policy, You can change only certain elements of a static policy:
       - The action referenced by the policy.
       - A condition clause, such as when and unless.

       You can't change these elements of a static policy:

       - Changing a policy from a static policy to a template-linked policy.
       - Changing the effect of a static policy from permit or forbid.
       - The principal referenced by a static policy.
       - The resource referenced by a static policy.
       - To update a template-linked policy, you must update the template instead.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policy.html
    :cloudformationResource: AWS::VerifiedPermissions::Policy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
        
        cfn_policy_props_mixin = verifiedpermissions_mixins.CfnPolicyPropsMixin(verifiedpermissions_mixins.CfnPolicyMixinProps(
            definition=verifiedpermissions_mixins.CfnPolicyPropsMixin.PolicyDefinitionProperty(
                static=verifiedpermissions_mixins.CfnPolicyPropsMixin.StaticPolicyDefinitionProperty(
                    description="description",
                    statement="statement"
                ),
                template_linked=verifiedpermissions_mixins.CfnPolicyPropsMixin.TemplateLinkedPolicyDefinitionProperty(
                    policy_template_id="policyTemplateId",
                    principal=verifiedpermissions_mixins.CfnPolicyPropsMixin.EntityIdentifierProperty(
                        entity_id="entityId",
                        entity_type="entityType"
                    ),
                    resource=verifiedpermissions_mixins.CfnPolicyPropsMixin.EntityIdentifierProperty(
                        entity_id="entityId",
                        entity_type="entityType"
                    )
                )
            ),
            policy_store_id="policyStoreId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VerifiedPermissions::Policy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee449372df8845112a302d564c98fd3d2897c30850b55ee2ff80b4605b6192ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08c60b30013bd24d7217c79575cfbd6e20e2c1159c0bad67f9efd6ddc8fcaa4c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a80b5829e7df5cc01ef6e123f6d39022c30caccbb2652db5e023239d2d596d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPolicyMixinProps:
        return typing.cast(CfnPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyPropsMixin.EntityIdentifierProperty",
        jsii_struct_bases=[],
        name_mapping={"entity_id": "entityId", "entity_type": "entityType"},
    )
    class EntityIdentifierProperty:
        def __init__(
            self,
            *,
            entity_id: typing.Optional[builtins.str] = None,
            entity_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the identifier of an entity in a policy, including its ID and type.

            :param entity_id: The identifier of an entity. ``"entityId":" *identifier* "``
            :param entity_type: The type of an entity. Example: ``"entityType":" *typeName* "``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-entityidentifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                entity_identifier_property = verifiedpermissions_mixins.CfnPolicyPropsMixin.EntityIdentifierProperty(
                    entity_id="entityId",
                    entity_type="entityType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fed3b057a6bd4b34309eff7c88c19b232a4afbc1728d246e27ab9e89b31370c2)
                check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
                check_type(argname="argument entity_type", value=entity_type, expected_type=type_hints["entity_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entity_id is not None:
                self._values["entity_id"] = entity_id
            if entity_type is not None:
                self._values["entity_type"] = entity_type

        @builtins.property
        def entity_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of an entity.

            ``"entityId":" *identifier* "``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-entityidentifier.html#cfn-verifiedpermissions-policy-entityidentifier-entityid
            '''
            result = self._values.get("entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entity_type(self) -> typing.Optional[builtins.str]:
            '''The type of an entity.

            Example: ``"entityType":" *typeName* "``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-entityidentifier.html#cfn-verifiedpermissions-policy-entityidentifier-entitytype
            '''
            result = self._values.get("entity_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntityIdentifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyPropsMixin.PolicyDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"static": "static", "template_linked": "templateLinked"},
    )
    class PolicyDefinitionProperty:
        def __init__(
            self,
            *,
            static: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.StaticPolicyDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            template_linked: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.TemplateLinkedPolicyDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that defines a Cedar policy.

            It includes the policy type, a description, and a policy body. This is a top level data type used to create a policy.

            This data type is used as a request parameter for the `CreatePolicy <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_CreatePolicy.html>`_ operation. This structure must always have either an ``Static`` or a ``TemplateLinked`` element.

            :param static: A structure that describes a static policy. An static policy doesn't use a template or allow placeholders for entities.
            :param template_linked: A structure that describes a policy that was instantiated from a template. The template can specify placeholders for ``principal`` and ``resource`` . When you use `CreatePolicy <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_CreatePolicy.html>`_ to create a policy from a template, you specify the exact principal and resource to use for the instantiated policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-policydefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                policy_definition_property = verifiedpermissions_mixins.CfnPolicyPropsMixin.PolicyDefinitionProperty(
                    static=verifiedpermissions_mixins.CfnPolicyPropsMixin.StaticPolicyDefinitionProperty(
                        description="description",
                        statement="statement"
                    ),
                    template_linked=verifiedpermissions_mixins.CfnPolicyPropsMixin.TemplateLinkedPolicyDefinitionProperty(
                        policy_template_id="policyTemplateId",
                        principal=verifiedpermissions_mixins.CfnPolicyPropsMixin.EntityIdentifierProperty(
                            entity_id="entityId",
                            entity_type="entityType"
                        ),
                        resource=verifiedpermissions_mixins.CfnPolicyPropsMixin.EntityIdentifierProperty(
                            entity_id="entityId",
                            entity_type="entityType"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d80ea24719b5a25f0156d5489d18ec692a986b7a86487dddcfad7b42734ff38)
                check_type(argname="argument static", value=static, expected_type=type_hints["static"])
                check_type(argname="argument template_linked", value=template_linked, expected_type=type_hints["template_linked"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if static is not None:
                self._values["static"] = static
            if template_linked is not None:
                self._values["template_linked"] = template_linked

        @builtins.property
        def static(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.StaticPolicyDefinitionProperty"]]:
            '''A structure that describes a static policy.

            An static policy doesn't use a template or allow placeholders for entities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-policydefinition.html#cfn-verifiedpermissions-policy-policydefinition-static
            '''
            result = self._values.get("static")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.StaticPolicyDefinitionProperty"]], result)

        @builtins.property
        def template_linked(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.TemplateLinkedPolicyDefinitionProperty"]]:
            '''A structure that describes a policy that was instantiated from a template.

            The template can specify placeholders for ``principal`` and ``resource`` . When you use `CreatePolicy <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_CreatePolicy.html>`_ to create a policy from a template, you specify the exact principal and resource to use for the instantiated policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-policydefinition.html#cfn-verifiedpermissions-policy-policydefinition-templatelinked
            '''
            result = self._values.get("template_linked")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.TemplateLinkedPolicyDefinitionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyPropsMixin.StaticPolicyDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"description": "description", "statement": "statement"},
    )
    class StaticPolicyDefinitionProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            statement: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that defines a static policy.

            :param description: The description of the static policy.
            :param statement: The policy content of the static policy, written in the Cedar policy language.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-staticpolicydefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                static_policy_definition_property = verifiedpermissions_mixins.CfnPolicyPropsMixin.StaticPolicyDefinitionProperty(
                    description="description",
                    statement="statement"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ffc3939cbfc196a758261c79aeef2107be588f8e1c1585fe75bde9954fbc82a7)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if statement is not None:
                self._values["statement"] = statement

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the static policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-staticpolicydefinition.html#cfn-verifiedpermissions-policy-staticpolicydefinition-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def statement(self) -> typing.Optional[builtins.str]:
            '''The policy content of the static policy, written in the Cedar policy language.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-staticpolicydefinition.html#cfn-verifiedpermissions-policy-staticpolicydefinition-statement
            '''
            result = self._values.get("statement")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StaticPolicyDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyPropsMixin.TemplateLinkedPolicyDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_template_id": "policyTemplateId",
            "principal": "principal",
            "resource": "resource",
        },
    )
    class TemplateLinkedPolicyDefinitionProperty:
        def __init__(
            self,
            *,
            policy_template_id: typing.Optional[builtins.str] = None,
            principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.EntityIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyPropsMixin.EntityIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that describes a policy created by instantiating a policy template.

            .. epigraph::

               You can't directly update a template-linked policy. You must update the associated policy template instead.

            :param policy_template_id: The unique identifier of the policy template used to create this policy.
            :param principal: The principal associated with this template-linked policy. Verified Permissions substitutes this principal for the ``?principal`` placeholder in the policy template when it evaluates an authorization request.
            :param resource: The resource associated with this template-linked policy. Verified Permissions substitutes this resource for the ``?resource`` placeholder in the policy template when it evaluates an authorization request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-templatelinkedpolicydefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                template_linked_policy_definition_property = verifiedpermissions_mixins.CfnPolicyPropsMixin.TemplateLinkedPolicyDefinitionProperty(
                    policy_template_id="policyTemplateId",
                    principal=verifiedpermissions_mixins.CfnPolicyPropsMixin.EntityIdentifierProperty(
                        entity_id="entityId",
                        entity_type="entityType"
                    ),
                    resource=verifiedpermissions_mixins.CfnPolicyPropsMixin.EntityIdentifierProperty(
                        entity_id="entityId",
                        entity_type="entityType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__235d586e68bbe2f0c8dfec74700a2fbe01763913def236254f0b52b93105815c)
                check_type(argname="argument policy_template_id", value=policy_template_id, expected_type=type_hints["policy_template_id"])
                check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
                check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_template_id is not None:
                self._values["policy_template_id"] = policy_template_id
            if principal is not None:
                self._values["principal"] = principal
            if resource is not None:
                self._values["resource"] = resource

        @builtins.property
        def policy_template_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the policy template used to create this policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-templatelinkedpolicydefinition.html#cfn-verifiedpermissions-policy-templatelinkedpolicydefinition-policytemplateid
            '''
            result = self._values.get("policy_template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def principal(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.EntityIdentifierProperty"]]:
            '''The principal associated with this template-linked policy.

            Verified Permissions substitutes this principal for the ``?principal`` placeholder in the policy template when it evaluates an authorization request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-templatelinkedpolicydefinition.html#cfn-verifiedpermissions-policy-templatelinkedpolicydefinition-principal
            '''
            result = self._values.get("principal")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.EntityIdentifierProperty"]], result)

        @builtins.property
        def resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.EntityIdentifierProperty"]]:
            '''The resource associated with this template-linked policy.

            Verified Permissions substitutes this resource for the ``?resource`` placeholder in the policy template when it evaluates an authorization request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policy-templatelinkedpolicydefinition.html#cfn-verifiedpermissions-policy-templatelinkedpolicydefinition-resource
            '''
            result = self._values.get("resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyPropsMixin.EntityIdentifierProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateLinkedPolicyDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyStoreMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deletion_protection": "deletionProtection",
        "description": "description",
        "schema": "schema",
        "tags": "tags",
        "validation_settings": "validationSettings",
    },
)
class CfnPolicyStoreMixinProps:
    def __init__(
        self,
        *,
        deletion_protection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyStorePropsMixin.DeletionProtectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyStorePropsMixin.SchemaDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        validation_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPolicyStorePropsMixin.ValidationSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPolicyStorePropsMixin.

        :param deletion_protection: Specifies whether the policy store can be deleted. If enabled, the policy store can't be deleted. The default state is ``DISABLED`` .
        :param description: Descriptive text that you can provide to help with identification of the current policy store.
        :param schema: Creates or updates the policy schema in a policy store. Cedar can use the schema to validate any Cedar policies and policy templates submitted to the policy store. Any changes to the schema validate only policies and templates submitted after the schema change. Existing policies and templates are not re-evaluated against the changed schema. If you later update a policy, then it is evaluated against the new schema at that time.
        :param tags: The list of key-value pairs to associate with the policy store.
        :param validation_settings: Specifies the validation setting for this policy store. Currently, the only valid and required value is ``Mode`` . .. epigraph:: We recommend that you turn on ``STRICT`` mode only after you define a schema. If a schema doesn't exist, then ``STRICT`` mode causes any policy to fail validation, and Verified Permissions rejects the policy. You can turn off validation by using the `UpdatePolicyStore <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_UpdatePolicyStore>`_ . Then, when you have a schema defined, use `UpdatePolicyStore <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_UpdatePolicyStore>`_ again to turn validation back on.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policystore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
            
            cfn_policy_store_mixin_props = verifiedpermissions_mixins.CfnPolicyStoreMixinProps(
                deletion_protection=verifiedpermissions_mixins.CfnPolicyStorePropsMixin.DeletionProtectionProperty(
                    mode="mode"
                ),
                description="description",
                schema=verifiedpermissions_mixins.CfnPolicyStorePropsMixin.SchemaDefinitionProperty(
                    cedar_format="cedarFormat",
                    cedar_json="cedarJson"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                validation_settings=verifiedpermissions_mixins.CfnPolicyStorePropsMixin.ValidationSettingsProperty(
                    mode="mode"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c279880c1c71e9afdf3fbe3a4ee3be9a014efaa5b164a500714d71ac568840)
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument validation_settings", value=validation_settings, expected_type=type_hints["validation_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if description is not None:
            self._values["description"] = description
        if schema is not None:
            self._values["schema"] = schema
        if tags is not None:
            self._values["tags"] = tags
        if validation_settings is not None:
            self._values["validation_settings"] = validation_settings

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyStorePropsMixin.DeletionProtectionProperty"]]:
        '''Specifies whether the policy store can be deleted. If enabled, the policy store can't be deleted.

        The default state is ``DISABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policystore.html#cfn-verifiedpermissions-policystore-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyStorePropsMixin.DeletionProtectionProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Descriptive text that you can provide to help with identification of the current policy store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policystore.html#cfn-verifiedpermissions-policystore-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyStorePropsMixin.SchemaDefinitionProperty"]]:
        '''Creates or updates the policy schema in a policy store.

        Cedar can use the schema to validate any Cedar policies and policy templates submitted to the policy store. Any changes to the schema validate only policies and templates submitted after the schema change. Existing policies and templates are not re-evaluated against the changed schema. If you later update a policy, then it is evaluated against the new schema at that time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policystore.html#cfn-verifiedpermissions-policystore-schema
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyStorePropsMixin.SchemaDefinitionProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of key-value pairs to associate with the policy store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policystore.html#cfn-verifiedpermissions-policystore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def validation_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyStorePropsMixin.ValidationSettingsProperty"]]:
        '''Specifies the validation setting for this policy store.

        Currently, the only valid and required value is ``Mode`` .
        .. epigraph::

           We recommend that you turn on ``STRICT`` mode only after you define a schema. If a schema doesn't exist, then ``STRICT`` mode causes any policy to fail validation, and Verified Permissions rejects the policy. You can turn off validation by using the `UpdatePolicyStore <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_UpdatePolicyStore>`_ . Then, when you have a schema defined, use `UpdatePolicyStore <https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_UpdatePolicyStore>`_ again to turn validation back on.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policystore.html#cfn-verifiedpermissions-policystore-validationsettings
        '''
        result = self._values.get("validation_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPolicyStorePropsMixin.ValidationSettingsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyStoreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPolicyStorePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyStorePropsMixin",
):
    '''Creates a policy store.

    A policy store is a container for policy resources. You can create a separate policy store for each of your applications.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policystore.html
    :cloudformationResource: AWS::VerifiedPermissions::PolicyStore
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
        
        cfn_policy_store_props_mixin = verifiedpermissions_mixins.CfnPolicyStorePropsMixin(verifiedpermissions_mixins.CfnPolicyStoreMixinProps(
            deletion_protection=verifiedpermissions_mixins.CfnPolicyStorePropsMixin.DeletionProtectionProperty(
                mode="mode"
            ),
            description="description",
            schema=verifiedpermissions_mixins.CfnPolicyStorePropsMixin.SchemaDefinitionProperty(
                cedar_format="cedarFormat",
                cedar_json="cedarJson"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            validation_settings=verifiedpermissions_mixins.CfnPolicyStorePropsMixin.ValidationSettingsProperty(
                mode="mode"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPolicyStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VerifiedPermissions::PolicyStore``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ff4a4d8f94ee1c2fc238a7b5598cf458d24f27e2ff40c73163e8c7ea119b63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2edc574e30b1efb921cb22aad0f9cc799fefdb7363804fd67afce93ed0d008aa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93af044e6cd81573c6f383bbefff3c073872442a5abf662456b1ebb0e7165c86)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPolicyStoreMixinProps:
        return typing.cast(CfnPolicyStoreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyStorePropsMixin.DeletionProtectionProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode"},
    )
    class DeletionProtectionProperty:
        def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
            '''Specifies whether the policy store can be deleted.

            :param mode: Specifies whether the policy store can be deleted. If enabled, the policy store can't be deleted. The default state is ``DISABLED`` . Default: - "DISABLED"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policystore-deletionprotection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                deletion_protection_property = verifiedpermissions_mixins.CfnPolicyStorePropsMixin.DeletionProtectionProperty(
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__107f1b6c82d485fc7ee9e866a1bad76f677dd9c4941d4cdd01354f5e7c3d85e8)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the policy store can be deleted. If enabled, the policy store can't be deleted.

            The default state is ``DISABLED`` .

            :default: - "DISABLED"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policystore-deletionprotection.html#cfn-verifiedpermissions-policystore-deletionprotection-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeletionProtectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyStorePropsMixin.SchemaDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"cedar_format": "cedarFormat", "cedar_json": "cedarJson"},
    )
    class SchemaDefinitionProperty:
        def __init__(
            self,
            *,
            cedar_format: typing.Optional[builtins.str] = None,
            cedar_json: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains a list of principal types, resource types, and actions that can be specified in policies stored in the same policy store.

            If the validation mode for the policy store is set to ``STRICT`` , then policies that can't be validated by this schema are rejected by Verified Permissions and can't be stored in the policy store.

            :param cedar_format: 
            :param cedar_json: A JSON string representation of the schema supported by applications that use this policy store. For more information, see `Policy store schema <https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/schema.html>`_ in the AVP User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policystore-schemadefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                schema_definition_property = verifiedpermissions_mixins.CfnPolicyStorePropsMixin.SchemaDefinitionProperty(
                    cedar_format="cedarFormat",
                    cedar_json="cedarJson"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50e1cd92d5b39d9b6903cb2b30521a8aa31fbed7303755fd6077cb43bd2ea3e2)
                check_type(argname="argument cedar_format", value=cedar_format, expected_type=type_hints["cedar_format"])
                check_type(argname="argument cedar_json", value=cedar_json, expected_type=type_hints["cedar_json"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cedar_format is not None:
                self._values["cedar_format"] = cedar_format
            if cedar_json is not None:
                self._values["cedar_json"] = cedar_json

        @builtins.property
        def cedar_format(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policystore-schemadefinition.html#cfn-verifiedpermissions-policystore-schemadefinition-cedarformat
            '''
            result = self._values.get("cedar_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cedar_json(self) -> typing.Optional[builtins.str]:
            '''A JSON string representation of the schema supported by applications that use this policy store.

            For more information, see `Policy store schema <https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/schema.html>`_ in the AVP User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policystore-schemadefinition.html#cfn-verifiedpermissions-policystore-schemadefinition-cedarjson
            '''
            result = self._values.get("cedar_json")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyStorePropsMixin.ValidationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode"},
    )
    class ValidationSettingsProperty:
        def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
            '''A structure that contains Cedar policy validation settings for the policy store.

            The validation mode determines which validation failures that Cedar considers serious enough to block acceptance of a new or edited static policy or policy template.

            :param mode: The validation mode currently configured for this policy store. The valid values are:. - *OFF* – Neither Verified Permissions nor Cedar perform any validation on policies. No validation errors are reported by either service. - *STRICT* – Requires a schema to be present in the policy store. Cedar performs validation on all submitted new or updated static policies and policy templates. Any that fail validation are rejected and Cedar doesn't store them in the policy store. .. epigraph:: If ``Mode=STRICT`` and the policy store doesn't contain a schema, Verified Permissions rejects all static policies and policy templates because there is no schema to validate against. To submit a static policy or policy template without a schema, you must turn off validation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policystore-validationsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
                
                validation_settings_property = verifiedpermissions_mixins.CfnPolicyStorePropsMixin.ValidationSettingsProperty(
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34c923274299cf5d5851594492ffbf4131de7a63fda25a3f4dfea418b495bfb8)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The validation mode currently configured for this policy store. The valid values are:.

            - *OFF* – Neither Verified Permissions nor Cedar perform any validation on policies. No validation errors are reported by either service.
            - *STRICT* – Requires a schema to be present in the policy store. Cedar performs validation on all submitted new or updated static policies and policy templates. Any that fail validation are rejected and Cedar doesn't store them in the policy store.

            .. epigraph::

               If ``Mode=STRICT`` and the policy store doesn't contain a schema, Verified Permissions rejects all static policies and policy templates because there is no schema to validate against.

               To submit a static policy or policy template without a schema, you must turn off validation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-verifiedpermissions-policystore-validationsettings.html#cfn-verifiedpermissions-policystore-validationsettings-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "policy_store_id": "policyStoreId",
        "statement": "statement",
    },
)
class CfnPolicyTemplateMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        policy_store_id: typing.Optional[builtins.str] = None,
        statement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPolicyTemplatePropsMixin.

        :param description: The description to attach to the new or updated policy template.
        :param policy_store_id: The unique identifier of the policy store that contains the template.
        :param statement: Specifies the content that you want to use for the new policy template, written in the Cedar policy language.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policytemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
            
            cfn_policy_template_mixin_props = verifiedpermissions_mixins.CfnPolicyTemplateMixinProps(
                description="description",
                policy_store_id="policyStoreId",
                statement="statement"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979624b967c56a8a8d02b2618371c9084dc35edbde2402f63b40c22da42bae45)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument policy_store_id", value=policy_store_id, expected_type=type_hints["policy_store_id"])
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if policy_store_id is not None:
            self._values["policy_store_id"] = policy_store_id
        if statement is not None:
            self._values["statement"] = statement

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description to attach to the new or updated policy template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policytemplate.html#cfn-verifiedpermissions-policytemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_store_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the policy store that contains the template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policytemplate.html#cfn-verifiedpermissions-policytemplate-policystoreid
        '''
        result = self._values.get("policy_store_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement(self) -> typing.Optional[builtins.str]:
        '''Specifies the content that you want to use for the new policy template, written in the Cedar policy language.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policytemplate.html#cfn-verifiedpermissions-policytemplate-statement
        '''
        result = self._values.get("statement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPolicyTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_verifiedpermissions.mixins.CfnPolicyTemplatePropsMixin",
):
    '''Creates a policy template.

    A template can use placeholders for the principal and resource. A template must be instantiated into a policy by associating it with specific principals and resources to use for the placeholders. That instantiated policy can then be considered in authorization decisions. The instantiated policy works identically to any other policy, except that it is dynamically linked to the template. If the template changes, then any policies that are linked to that template are immediately updated as well.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-verifiedpermissions-policytemplate.html
    :cloudformationResource: AWS::VerifiedPermissions::PolicyTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_verifiedpermissions import mixins as verifiedpermissions_mixins
        
        cfn_policy_template_props_mixin = verifiedpermissions_mixins.CfnPolicyTemplatePropsMixin(verifiedpermissions_mixins.CfnPolicyTemplateMixinProps(
            description="description",
            policy_store_id="policyStoreId",
            statement="statement"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPolicyTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VerifiedPermissions::PolicyTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805b0ff423efcd78688608400cf5708c2bb01d2b5c45f63bd54d44d85fe6670d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea4cb4c45dfa874401a4d60d0c2490336ba5f33870e266d969fb68b34d899196)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcac39cca881bbc38c72efa317da504f9546afa813460bc33eec128873329161)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPolicyTemplateMixinProps:
        return typing.cast(CfnPolicyTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnIdentitySourceMixinProps",
    "CfnIdentitySourcePropsMixin",
    "CfnPolicyMixinProps",
    "CfnPolicyPropsMixin",
    "CfnPolicyStoreMixinProps",
    "CfnPolicyStorePropsMixin",
    "CfnPolicyTemplateMixinProps",
    "CfnPolicyTemplatePropsMixin",
]

publication.publish()

def _typecheckingstub__dda88177405e83bed311910442c1eb0bce5802fcaec2f5aaf5b09d3580f093f4(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentitySourcePropsMixin.IdentitySourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy_store_id: typing.Optional[builtins.str] = None,
    principal_entity_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab854a58acf88c9972606bf46fdb9fed434d9450061c65b20d64725c686f4f3(
    props: typing.Union[CfnIdentitySourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3721cbd400042512733e75c2e1a25eed446d200c73891bac96080e295c1f40e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01651ac556dd449cd3590281be4fa0803cbb78f28dec23c9a8ccb3d5c61dcd33(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ef244582538b174ef25ef522890d4d07d417df9543fb9b4c5a6fed9b06f39b(
    *,
    group_entity_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b768ea020da52f15fc3c7b7e92de35b04a245b0f11aaa7af80b7f5d3b4b1cf(
    *,
    client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentitySourcePropsMixin.CognitoGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_pool_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54e4299e5bb8133648bb8a1d2e134121b107356b076f5edbd9d8ef044756e0b(
    *,
    cognito_user_pool_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentitySourcePropsMixin.CognitoUserPoolConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    open_id_connect_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentitySourcePropsMixin.OpenIdConnectConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d6aaf6c1d9dd5e1cdce6013aab00e1825d608cd69613539958a42b1b91ff4a(
    *,
    client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    discovery_url: typing.Optional[builtins.str] = None,
    open_id_issuer: typing.Optional[builtins.str] = None,
    user_pool_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7a656707903564568235f1d6e418c3d79e82a99cb19d196eb1697232932893(
    *,
    audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id_claim: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90bfb08d86e5798b075868b865d067974adfe954f38732f5ba1343f2f8241e2(
    *,
    entity_id_prefix: typing.Optional[builtins.str] = None,
    group_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentitySourcePropsMixin.OpenIdConnectGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    issuer: typing.Optional[builtins.str] = None,
    token_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentitySourcePropsMixin.OpenIdConnectTokenSelectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122ba2af56f53817730cc1a9e28464de91a3ddd2995d56756ec507f70fa8686a(
    *,
    group_claim: typing.Optional[builtins.str] = None,
    group_entity_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3939bbe475c548db0dd957591ac8b7243acb685cdad207be0217ed6766324a8(
    *,
    client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id_claim: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c722935bc38a3e6a6b248dca506d0ac943c5f652ea40fbafe4081f66b9a9a97(
    *,
    access_token_only: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentitySourcePropsMixin.OpenIdConnectAccessTokenConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    identity_token_only: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentitySourcePropsMixin.OpenIdConnectIdentityTokenConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7ca6168e1b90b6ec490dd73d93a9ca77740a0d5996a034cd84ba73ca248e54(
    *,
    definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.PolicyDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy_store_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee449372df8845112a302d564c98fd3d2897c30850b55ee2ff80b4605b6192ab(
    props: typing.Union[CfnPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c60b30013bd24d7217c79575cfbd6e20e2c1159c0bad67f9efd6ddc8fcaa4c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a80b5829e7df5cc01ef6e123f6d39022c30caccbb2652db5e023239d2d596d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed3b057a6bd4b34309eff7c88c19b232a4afbc1728d246e27ab9e89b31370c2(
    *,
    entity_id: typing.Optional[builtins.str] = None,
    entity_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d80ea24719b5a25f0156d5489d18ec692a986b7a86487dddcfad7b42734ff38(
    *,
    static: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.StaticPolicyDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_linked: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.TemplateLinkedPolicyDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc3939cbfc196a758261c79aeef2107be588f8e1c1585fe75bde9954fbc82a7(
    *,
    description: typing.Optional[builtins.str] = None,
    statement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235d586e68bbe2f0c8dfec74700a2fbe01763913def236254f0b52b93105815c(
    *,
    policy_template_id: typing.Optional[builtins.str] = None,
    principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.EntityIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyPropsMixin.EntityIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c279880c1c71e9afdf3fbe3a4ee3be9a014efaa5b164a500714d71ac568840(
    *,
    deletion_protection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyStorePropsMixin.DeletionProtectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyStorePropsMixin.SchemaDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    validation_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPolicyStorePropsMixin.ValidationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ff4a4d8f94ee1c2fc238a7b5598cf458d24f27e2ff40c73163e8c7ea119b63(
    props: typing.Union[CfnPolicyStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edc574e30b1efb921cb22aad0f9cc799fefdb7363804fd67afce93ed0d008aa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93af044e6cd81573c6f383bbefff3c073872442a5abf662456b1ebb0e7165c86(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107f1b6c82d485fc7ee9e866a1bad76f677dd9c4941d4cdd01354f5e7c3d85e8(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e1cd92d5b39d9b6903cb2b30521a8aa31fbed7303755fd6077cb43bd2ea3e2(
    *,
    cedar_format: typing.Optional[builtins.str] = None,
    cedar_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c923274299cf5d5851594492ffbf4131de7a63fda25a3f4dfea418b495bfb8(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979624b967c56a8a8d02b2618371c9084dc35edbde2402f63b40c22da42bae45(
    *,
    description: typing.Optional[builtins.str] = None,
    policy_store_id: typing.Optional[builtins.str] = None,
    statement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805b0ff423efcd78688608400cf5708c2bb01d2b5c45f63bd54d44d85fe6670d(
    props: typing.Union[CfnPolicyTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4cb4c45dfa874401a4d60d0c2490336ba5f33870e266d969fb68b34d899196(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcac39cca881bbc38c72efa317da504f9546afa813460bc33eec128873329161(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
