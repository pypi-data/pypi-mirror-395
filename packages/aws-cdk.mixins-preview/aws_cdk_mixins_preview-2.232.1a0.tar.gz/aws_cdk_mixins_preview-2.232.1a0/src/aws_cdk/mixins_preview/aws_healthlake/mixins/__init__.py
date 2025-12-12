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
    jsii_type="@aws-cdk/mixins-preview.aws_healthlake.mixins.CfnFHIRDatastoreMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "datastore_name": "datastoreName",
        "datastore_type_version": "datastoreTypeVersion",
        "identity_provider_configuration": "identityProviderConfiguration",
        "preload_data_config": "preloadDataConfig",
        "sse_configuration": "sseConfiguration",
        "tags": "tags",
    },
)
class CfnFHIRDatastoreMixinProps:
    def __init__(
        self,
        *,
        datastore_name: typing.Optional[builtins.str] = None,
        datastore_type_version: typing.Optional[builtins.str] = None,
        identity_provider_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFHIRDatastorePropsMixin.IdentityProviderConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        preload_data_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFHIRDatastorePropsMixin.PreloadDataConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sse_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFHIRDatastorePropsMixin.SseConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFHIRDatastorePropsMixin.

        :param datastore_name: The data store name (user-generated).
        :param datastore_type_version: The FHIR release version supported by the data store. Current support is for version ``R4`` .
        :param identity_provider_configuration: The identity provider configuration selected when the data store was created.
        :param preload_data_config: The preloaded Synthea data configuration for the data store.
        :param sse_configuration: The server-side encryption key configuration for a customer-provided encryption key specified for creating a data store.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthlake import mixins as healthlake_mixins
            
            cfn_fHIRDatastore_mixin_props = healthlake_mixins.CfnFHIRDatastoreMixinProps(
                datastore_name="datastoreName",
                datastore_type_version="datastoreTypeVersion",
                identity_provider_configuration=healthlake_mixins.CfnFHIRDatastorePropsMixin.IdentityProviderConfigurationProperty(
                    authorization_strategy="authorizationStrategy",
                    fine_grained_authorization_enabled=False,
                    idp_lambda_arn="idpLambdaArn",
                    metadata="metadata"
                ),
                preload_data_config=healthlake_mixins.CfnFHIRDatastorePropsMixin.PreloadDataConfigProperty(
                    preload_data_type="preloadDataType"
                ),
                sse_configuration=healthlake_mixins.CfnFHIRDatastorePropsMixin.SseConfigurationProperty(
                    kms_encryption_config=healthlake_mixins.CfnFHIRDatastorePropsMixin.KmsEncryptionConfigProperty(
                        cmk_type="cmkType",
                        kms_key_id="kmsKeyId"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d953924aff61cd0da68aad2b91d472df8ba6e7d8c054574a482ebe09185afb80)
            check_type(argname="argument datastore_name", value=datastore_name, expected_type=type_hints["datastore_name"])
            check_type(argname="argument datastore_type_version", value=datastore_type_version, expected_type=type_hints["datastore_type_version"])
            check_type(argname="argument identity_provider_configuration", value=identity_provider_configuration, expected_type=type_hints["identity_provider_configuration"])
            check_type(argname="argument preload_data_config", value=preload_data_config, expected_type=type_hints["preload_data_config"])
            check_type(argname="argument sse_configuration", value=sse_configuration, expected_type=type_hints["sse_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if datastore_name is not None:
            self._values["datastore_name"] = datastore_name
        if datastore_type_version is not None:
            self._values["datastore_type_version"] = datastore_type_version
        if identity_provider_configuration is not None:
            self._values["identity_provider_configuration"] = identity_provider_configuration
        if preload_data_config is not None:
            self._values["preload_data_config"] = preload_data_config
        if sse_configuration is not None:
            self._values["sse_configuration"] = sse_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def datastore_name(self) -> typing.Optional[builtins.str]:
        '''The data store name (user-generated).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-datastorename
        '''
        result = self._values.get("datastore_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datastore_type_version(self) -> typing.Optional[builtins.str]:
        '''The FHIR release version supported by the data store.

        Current support is for version ``R4`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-datastoretypeversion
        '''
        result = self._values.get("datastore_type_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFHIRDatastorePropsMixin.IdentityProviderConfigurationProperty"]]:
        '''The identity provider configuration selected when the data store was created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-identityproviderconfiguration
        '''
        result = self._values.get("identity_provider_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFHIRDatastorePropsMixin.IdentityProviderConfigurationProperty"]], result)

    @builtins.property
    def preload_data_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFHIRDatastorePropsMixin.PreloadDataConfigProperty"]]:
        '''The preloaded Synthea data configuration for the data store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-preloaddataconfig
        '''
        result = self._values.get("preload_data_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFHIRDatastorePropsMixin.PreloadDataConfigProperty"]], result)

    @builtins.property
    def sse_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFHIRDatastorePropsMixin.SseConfigurationProperty"]]:
        '''The server-side encryption key configuration for a customer-provided encryption key specified for creating a data store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-sseconfiguration
        '''
        result = self._values.get("sse_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFHIRDatastorePropsMixin.SseConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html#cfn-healthlake-fhirdatastore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFHIRDatastoreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFHIRDatastorePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_healthlake.mixins.CfnFHIRDatastorePropsMixin",
):
    '''Creates a Data Store that can ingest and export FHIR formatted data.

    .. epigraph::

       Please note that when a user tries to do an Update operation via CloudFormation, changes to the Data Store name, Type Version, PreloadDataConfig, or SSEConfiguration will delete their existing Data Store for the stack and create a new one. This will lead to potential loss of data.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-healthlake-fhirdatastore.html
    :cloudformationResource: AWS::HealthLake::FHIRDatastore
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_healthlake import mixins as healthlake_mixins
        
        cfn_fHIRDatastore_props_mixin = healthlake_mixins.CfnFHIRDatastorePropsMixin(healthlake_mixins.CfnFHIRDatastoreMixinProps(
            datastore_name="datastoreName",
            datastore_type_version="datastoreTypeVersion",
            identity_provider_configuration=healthlake_mixins.CfnFHIRDatastorePropsMixin.IdentityProviderConfigurationProperty(
                authorization_strategy="authorizationStrategy",
                fine_grained_authorization_enabled=False,
                idp_lambda_arn="idpLambdaArn",
                metadata="metadata"
            ),
            preload_data_config=healthlake_mixins.CfnFHIRDatastorePropsMixin.PreloadDataConfigProperty(
                preload_data_type="preloadDataType"
            ),
            sse_configuration=healthlake_mixins.CfnFHIRDatastorePropsMixin.SseConfigurationProperty(
                kms_encryption_config=healthlake_mixins.CfnFHIRDatastorePropsMixin.KmsEncryptionConfigProperty(
                    cmk_type="cmkType",
                    kms_key_id="kmsKeyId"
                )
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
        props: typing.Union[CfnFHIRDatastoreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::HealthLake::FHIRDatastore``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0cc57c563c0761f4c109dfe92d66a20584d46b8c9fa43233f4144b1f050804)
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
            type_hints = typing.get_type_hints(_typecheckingstub__395044fb97247a7ffe4b923db2eef6ef7ad956f2720667a865ee9023869f2ff2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7d25d264699d789f01478749dd84cb9bb56a72058a1780447ba89f2beb35b4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFHIRDatastoreMixinProps:
        return typing.cast(CfnFHIRDatastoreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_healthlake.mixins.CfnFHIRDatastorePropsMixin.CreatedAtProperty",
        jsii_struct_bases=[],
        name_mapping={"nanos": "nanos", "seconds": "seconds"},
    )
    class CreatedAtProperty:
        def __init__(
            self,
            *,
            nanos: typing.Optional[jsii.Number] = None,
            seconds: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The time that a Data Store was created.

            :param nanos: Nanoseconds.
            :param seconds: Seconds since epoch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-createdat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_healthlake import mixins as healthlake_mixins
                
                created_at_property = healthlake_mixins.CfnFHIRDatastorePropsMixin.CreatedAtProperty(
                    nanos=123,
                    seconds="seconds"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bed98f89122c3710b4ccba28b365159fe9b70fc1e6c9f86506d7a9357b84f956)
                check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
                check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if nanos is not None:
                self._values["nanos"] = nanos
            if seconds is not None:
                self._values["seconds"] = seconds

        @builtins.property
        def nanos(self) -> typing.Optional[jsii.Number]:
            '''Nanoseconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-createdat.html#cfn-healthlake-fhirdatastore-createdat-nanos
            '''
            result = self._values.get("nanos")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def seconds(self) -> typing.Optional[builtins.str]:
            '''Seconds since epoch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-createdat.html#cfn-healthlake-fhirdatastore-createdat-seconds
            '''
            result = self._values.get("seconds")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreatedAtProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_healthlake.mixins.CfnFHIRDatastorePropsMixin.IdentityProviderConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_strategy": "authorizationStrategy",
            "fine_grained_authorization_enabled": "fineGrainedAuthorizationEnabled",
            "idp_lambda_arn": "idpLambdaArn",
            "metadata": "metadata",
        },
    )
    class IdentityProviderConfigurationProperty:
        def __init__(
            self,
            *,
            authorization_strategy: typing.Optional[builtins.str] = None,
            fine_grained_authorization_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            idp_lambda_arn: typing.Optional[builtins.str] = None,
            metadata: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The identity provider configuration selected when the data store was created.

            :param authorization_strategy: The authorization strategy selected when the HealthLake data store is created. .. epigraph:: HealthLake provides support for both SMART on FHIR V1 and V2 as described below. - ``SMART_ON_FHIR_V1`` – Support for only SMART on FHIR V1, which includes ``read`` (read/search) and ``write`` (create/update/delete) permissions. - ``SMART_ON_FHIR`` – Support for both SMART on FHIR V1 and V2, which includes ``create`` , ``read`` , ``update`` , ``delete`` , and ``search`` permissions. - ``AWS_AUTH`` – The default HealthLake authorization strategy; not affiliated with SMART on FHIR.
            :param fine_grained_authorization_enabled: The parameter to enable SMART on FHIR fine-grained authorization for the data store.
            :param idp_lambda_arn: The Amazon Resource Name (ARN) of the Lambda function to use to decode the access token created by the authorization server.
            :param metadata: The JSON metadata elements to use in your identity provider configuration. Required elements are listed based on the launch specification of the SMART application. For more information on all possible elements, see `Metadata <https://docs.aws.amazon.com/https://build.fhir.org/ig/HL7/smart-app-launch/conformance.html#metadata>`_ in SMART's App Launch specification. ``authorization_endpoint`` : The URL to the OAuth2 authorization endpoint. ``grant_types_supported`` : An array of grant types that are supported at the token endpoint. You must provide at least one grant type option. Valid options are ``authorization_code`` and ``client_credentials`` . ``token_endpoint`` : The URL to the OAuth2 token endpoint. ``capabilities`` : An array of strings of the SMART capabilities that the authorization server supports. ``code_challenge_methods_supported`` : An array of strings of supported PKCE code challenge methods. You must include the ``S256`` method in the array of PKCE code challenge methods.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-identityproviderconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_healthlake import mixins as healthlake_mixins
                
                identity_provider_configuration_property = healthlake_mixins.CfnFHIRDatastorePropsMixin.IdentityProviderConfigurationProperty(
                    authorization_strategy="authorizationStrategy",
                    fine_grained_authorization_enabled=False,
                    idp_lambda_arn="idpLambdaArn",
                    metadata="metadata"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__344b9f6e3cac857f9d7e97c686a6246922fb96d009c67b3b95e4a9d8d688cdfc)
                check_type(argname="argument authorization_strategy", value=authorization_strategy, expected_type=type_hints["authorization_strategy"])
                check_type(argname="argument fine_grained_authorization_enabled", value=fine_grained_authorization_enabled, expected_type=type_hints["fine_grained_authorization_enabled"])
                check_type(argname="argument idp_lambda_arn", value=idp_lambda_arn, expected_type=type_hints["idp_lambda_arn"])
                check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_strategy is not None:
                self._values["authorization_strategy"] = authorization_strategy
            if fine_grained_authorization_enabled is not None:
                self._values["fine_grained_authorization_enabled"] = fine_grained_authorization_enabled
            if idp_lambda_arn is not None:
                self._values["idp_lambda_arn"] = idp_lambda_arn
            if metadata is not None:
                self._values["metadata"] = metadata

        @builtins.property
        def authorization_strategy(self) -> typing.Optional[builtins.str]:
            '''The authorization strategy selected when the HealthLake data store is created.

            .. epigraph::

               HealthLake provides support for both SMART on FHIR V1 and V2 as described below.

               - ``SMART_ON_FHIR_V1`` – Support for only SMART on FHIR V1, which includes ``read`` (read/search) and ``write`` (create/update/delete) permissions.
               - ``SMART_ON_FHIR`` – Support for both SMART on FHIR V1 and V2, which includes ``create`` , ``read`` , ``update`` , ``delete`` , and ``search`` permissions.
               - ``AWS_AUTH`` – The default HealthLake authorization strategy; not affiliated with SMART on FHIR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-identityproviderconfiguration.html#cfn-healthlake-fhirdatastore-identityproviderconfiguration-authorizationstrategy
            '''
            result = self._values.get("authorization_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fine_grained_authorization_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The parameter to enable SMART on FHIR fine-grained authorization for the data store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-identityproviderconfiguration.html#cfn-healthlake-fhirdatastore-identityproviderconfiguration-finegrainedauthorizationenabled
            '''
            result = self._values.get("fine_grained_authorization_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def idp_lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Lambda function to use to decode the access token created by the authorization server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-identityproviderconfiguration.html#cfn-healthlake-fhirdatastore-identityproviderconfiguration-idplambdaarn
            '''
            result = self._values.get("idp_lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metadata(self) -> typing.Optional[builtins.str]:
            '''The JSON metadata elements to use in your identity provider configuration.

            Required elements are listed based on the launch specification of the SMART application. For more information on all possible elements, see `Metadata <https://docs.aws.amazon.com/https://build.fhir.org/ig/HL7/smart-app-launch/conformance.html#metadata>`_ in SMART's App Launch specification.

            ``authorization_endpoint`` : The URL to the OAuth2 authorization endpoint.

            ``grant_types_supported`` : An array of grant types that are supported at the token endpoint. You must provide at least one grant type option. Valid options are ``authorization_code`` and ``client_credentials`` .

            ``token_endpoint`` : The URL to the OAuth2 token endpoint.

            ``capabilities`` : An array of strings of the SMART capabilities that the authorization server supports.

            ``code_challenge_methods_supported`` : An array of strings of supported PKCE code challenge methods. You must include the ``S256`` method in the array of PKCE code challenge methods.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-identityproviderconfiguration.html#cfn-healthlake-fhirdatastore-identityproviderconfiguration-metadata
            '''
            result = self._values.get("metadata")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentityProviderConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_healthlake.mixins.CfnFHIRDatastorePropsMixin.KmsEncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"cmk_type": "cmkType", "kms_key_id": "kmsKeyId"},
    )
    class KmsEncryptionConfigProperty:
        def __init__(
            self,
            *,
            cmk_type: typing.Optional[builtins.str] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The customer-managed-key(CMK) used when creating a Data Store.

            If a customer owned key is not specified, an Amazon owned key will be used for encryption.

            :param cmk_type: The type of customer-managed-key(CMK) used for encryption. The two types of supported CMKs are customer owned CMKs and Amazon owned CMKs. For more information on CMK types, see `KmsEncryptionConfig <https://docs.aws.amazon.com/healthlake/latest/APIReference/API_KmsEncryptionConfig.html#HealthLake-Type-KmsEncryptionConfig-CmkType>`_ .
            :param kms_key_id: The Key Management Service (KMS) encryption key id/alias used to encrypt the data store contents at rest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-kmsencryptionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_healthlake import mixins as healthlake_mixins
                
                kms_encryption_config_property = healthlake_mixins.CfnFHIRDatastorePropsMixin.KmsEncryptionConfigProperty(
                    cmk_type="cmkType",
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29ec767d6829572ca3a0a011f025a92035012ae303fee551481f2a4e4437baaf)
                check_type(argname="argument cmk_type", value=cmk_type, expected_type=type_hints["cmk_type"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cmk_type is not None:
                self._values["cmk_type"] = cmk_type
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def cmk_type(self) -> typing.Optional[builtins.str]:
            '''The type of customer-managed-key(CMK) used for encryption.

            The two types of supported CMKs are customer owned CMKs and Amazon owned CMKs. For more information on CMK types, see `KmsEncryptionConfig <https://docs.aws.amazon.com/healthlake/latest/APIReference/API_KmsEncryptionConfig.html#HealthLake-Type-KmsEncryptionConfig-CmkType>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-kmsencryptionconfig.html#cfn-healthlake-fhirdatastore-kmsencryptionconfig-cmktype
            '''
            result = self._values.get("cmk_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The Key Management Service (KMS) encryption key id/alias used to encrypt the data store contents at rest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-kmsencryptionconfig.html#cfn-healthlake-fhirdatastore-kmsencryptionconfig-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KmsEncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_healthlake.mixins.CfnFHIRDatastorePropsMixin.PreloadDataConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"preload_data_type": "preloadDataType"},
    )
    class PreloadDataConfigProperty:
        def __init__(
            self,
            *,
            preload_data_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An optional parameter to preload (import) open source Synthea FHIR data upon creation of the data store.

            :param preload_data_type: The type of preloaded data. Only Synthea preloaded data is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-preloaddataconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_healthlake import mixins as healthlake_mixins
                
                preload_data_config_property = healthlake_mixins.CfnFHIRDatastorePropsMixin.PreloadDataConfigProperty(
                    preload_data_type="preloadDataType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ab8747ee912b1d00e09f1bbdc46529fd195bc37f8551f510c0b7a3bd54bc5fe)
                check_type(argname="argument preload_data_type", value=preload_data_type, expected_type=type_hints["preload_data_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if preload_data_type is not None:
                self._values["preload_data_type"] = preload_data_type

        @builtins.property
        def preload_data_type(self) -> typing.Optional[builtins.str]:
            '''The type of preloaded data.

            Only Synthea preloaded data is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-preloaddataconfig.html#cfn-healthlake-fhirdatastore-preloaddataconfig-preloaddatatype
            '''
            result = self._values.get("preload_data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PreloadDataConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_healthlake.mixins.CfnFHIRDatastorePropsMixin.SseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_encryption_config": "kmsEncryptionConfig"},
    )
    class SseConfigurationProperty:
        def __init__(
            self,
            *,
            kms_encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFHIRDatastorePropsMixin.KmsEncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The server-side encryption key configuration for a customer-provided encryption key.

            :param kms_encryption_config: The server-side encryption key configuration for a customer provided encryption key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-sseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_healthlake import mixins as healthlake_mixins
                
                sse_configuration_property = healthlake_mixins.CfnFHIRDatastorePropsMixin.SseConfigurationProperty(
                    kms_encryption_config=healthlake_mixins.CfnFHIRDatastorePropsMixin.KmsEncryptionConfigProperty(
                        cmk_type="cmkType",
                        kms_key_id="kmsKeyId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74f2dc439e6541fa0018a3a2c5cb7f1b7c64e5147b5bb277431449a076a56488)
                check_type(argname="argument kms_encryption_config", value=kms_encryption_config, expected_type=type_hints["kms_encryption_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_encryption_config is not None:
                self._values["kms_encryption_config"] = kms_encryption_config

        @builtins.property
        def kms_encryption_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFHIRDatastorePropsMixin.KmsEncryptionConfigProperty"]]:
            '''The server-side encryption key configuration for a customer provided encryption key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-healthlake-fhirdatastore-sseconfiguration.html#cfn-healthlake-fhirdatastore-sseconfiguration-kmsencryptionconfig
            '''
            result = self._values.get("kms_encryption_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFHIRDatastorePropsMixin.KmsEncryptionConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnFHIRDatastoreMixinProps",
    "CfnFHIRDatastorePropsMixin",
]

publication.publish()

def _typecheckingstub__d953924aff61cd0da68aad2b91d472df8ba6e7d8c054574a482ebe09185afb80(
    *,
    datastore_name: typing.Optional[builtins.str] = None,
    datastore_type_version: typing.Optional[builtins.str] = None,
    identity_provider_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFHIRDatastorePropsMixin.IdentityProviderConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    preload_data_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFHIRDatastorePropsMixin.PreloadDataConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sse_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFHIRDatastorePropsMixin.SseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0cc57c563c0761f4c109dfe92d66a20584d46b8c9fa43233f4144b1f050804(
    props: typing.Union[CfnFHIRDatastoreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395044fb97247a7ffe4b923db2eef6ef7ad956f2720667a865ee9023869f2ff2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7d25d264699d789f01478749dd84cb9bb56a72058a1780447ba89f2beb35b4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed98f89122c3710b4ccba28b365159fe9b70fc1e6c9f86506d7a9357b84f956(
    *,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344b9f6e3cac857f9d7e97c686a6246922fb96d009c67b3b95e4a9d8d688cdfc(
    *,
    authorization_strategy: typing.Optional[builtins.str] = None,
    fine_grained_authorization_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    idp_lambda_arn: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ec767d6829572ca3a0a011f025a92035012ae303fee551481f2a4e4437baaf(
    *,
    cmk_type: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab8747ee912b1d00e09f1bbdc46529fd195bc37f8551f510c0b7a3bd54bc5fe(
    *,
    preload_data_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f2dc439e6541fa0018a3a2c5cb7f1b7c64e5147b5bb277431449a076a56488(
    *,
    kms_encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFHIRDatastorePropsMixin.KmsEncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
