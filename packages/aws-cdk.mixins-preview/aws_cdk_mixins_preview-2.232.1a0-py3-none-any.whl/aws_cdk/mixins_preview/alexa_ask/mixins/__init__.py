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
    jsii_type="@aws-cdk/mixins-preview.alexa_ask.mixins.CfnSkillMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_configuration": "authenticationConfiguration",
        "skill_package": "skillPackage",
        "vendor_id": "vendorId",
    },
)
class CfnSkillMixinProps:
    def __init__(
        self,
        *,
        authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSkillPropsMixin.AuthenticationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        skill_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSkillPropsMixin.SkillPackageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vendor_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSkillPropsMixin.

        :param authentication_configuration: Login with Amazon (LWA) configuration used to authenticate with the Alexa service. Only Login with Amazon clients created through the are supported. The client ID, client secret, and refresh token are required.
        :param skill_package: Configuration for the skill package that contains the components of the Alexa skill. Skill packages are retrieved from an Amazon S3 bucket and key and used to create and update the skill. For more information about the skill package format, see the .
        :param vendor_id: The vendor ID associated with the Amazon developer account that will host the skill. Details for retrieving the vendor ID are in . The provided LWA credentials must be linked to the developer account associated with this vendor ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ask-skill.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.alexa_ask import mixins as alexa_ask_mixins
            
            # manifest: Any
            
            cfn_skill_mixin_props = alexa_ask_mixins.CfnSkillMixinProps(
                authentication_configuration=alexa_ask_mixins.CfnSkillPropsMixin.AuthenticationConfigurationProperty(
                    client_id="clientId",
                    client_secret="clientSecret",
                    refresh_token="refreshToken"
                ),
                skill_package=alexa_ask_mixins.CfnSkillPropsMixin.SkillPackageProperty(
                    overrides=alexa_ask_mixins.CfnSkillPropsMixin.OverridesProperty(
                        manifest=manifest
                    ),
                    s3_bucket="s3Bucket",
                    s3_bucket_role="s3BucketRole",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion"
                ),
                vendor_id="vendorId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6c58146f6b8a609a04e88edc00aca2b994edaeaf55d863684a146ea9270b54)
            check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
            check_type(argname="argument skill_package", value=skill_package, expected_type=type_hints["skill_package"])
            check_type(argname="argument vendor_id", value=vendor_id, expected_type=type_hints["vendor_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_configuration is not None:
            self._values["authentication_configuration"] = authentication_configuration
        if skill_package is not None:
            self._values["skill_package"] = skill_package
        if vendor_id is not None:
            self._values["vendor_id"] = vendor_id

    @builtins.property
    def authentication_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSkillPropsMixin.AuthenticationConfigurationProperty"]]:
        '''Login with Amazon (LWA) configuration used to authenticate with the Alexa service.

        Only Login with Amazon clients created through the  are supported. The client ID, client secret, and refresh token are required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ask-skill.html#cfn-ask-skill-authenticationconfiguration
        '''
        result = self._values.get("authentication_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSkillPropsMixin.AuthenticationConfigurationProperty"]], result)

    @builtins.property
    def skill_package(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSkillPropsMixin.SkillPackageProperty"]]:
        '''Configuration for the skill package that contains the components of the Alexa skill.

        Skill packages are retrieved from an Amazon S3 bucket and key and used to create and update the skill. For more information about the skill package format, see the  .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ask-skill.html#cfn-ask-skill-skillpackage
        '''
        result = self._values.get("skill_package")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSkillPropsMixin.SkillPackageProperty"]], result)

    @builtins.property
    def vendor_id(self) -> typing.Optional[builtins.str]:
        '''The vendor ID associated with the Amazon developer account that will host the skill.

        Details for retrieving the vendor ID are in  . The provided LWA credentials must be linked to the developer account associated with this vendor ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ask-skill.html#cfn-ask-skill-vendorid
        '''
        result = self._values.get("vendor_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSkillMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSkillPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.alexa_ask.mixins.CfnSkillPropsMixin",
):
    '''The ``Alexa::ASK::Skill`` resource creates an Alexa skill that enables customers to access new abilities.

    For more information about developing a skill, see the  .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ask-skill.html
    :cloudformationResource: Alexa::ASK::Skill
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.alexa_ask import mixins as alexa_ask_mixins
        
        # manifest: Any
        
        cfn_skill_props_mixin = alexa_ask_mixins.CfnSkillPropsMixin(alexa_ask_mixins.CfnSkillMixinProps(
            authentication_configuration=alexa_ask_mixins.CfnSkillPropsMixin.AuthenticationConfigurationProperty(
                client_id="clientId",
                client_secret="clientSecret",
                refresh_token="refreshToken"
            ),
            skill_package=alexa_ask_mixins.CfnSkillPropsMixin.SkillPackageProperty(
                overrides=alexa_ask_mixins.CfnSkillPropsMixin.OverridesProperty(
                    manifest=manifest
                ),
                s3_bucket="s3Bucket",
                s3_bucket_role="s3BucketRole",
                s3_key="s3Key",
                s3_object_version="s3ObjectVersion"
            ),
            vendor_id="vendorId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSkillMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``Alexa::ASK::Skill``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9141dc594772595c2db5b261da509eb350cf67b47ee89bd95e929e226c5ce91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d41410569b4eead7a2bab0b9a2b57957530b2381fbe7c7219c02f3d3ac882070)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e4e83d12cfd09edd362de4e7558b7770a2a3b6df067c4c1f59279fb5adb2231)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSkillMixinProps:
        return typing.cast(CfnSkillMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.alexa_ask.mixins.CfnSkillPropsMixin.AuthenticationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "refresh_token": "refreshToken",
        },
    )
    class AuthenticationConfigurationProperty:
        def __init__(
            self,
            *,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AuthenticationConfiguration`` property type specifies the Login with Amazon (LWA) configuration used to authenticate with the Alexa service.

            Only Login with Amazon security profiles created through the  are supported for authentication. A client ID, client secret, and refresh token are required. You can generate a client ID and client secret by creating a new  on the Amazon Developer Portal or you can retrieve them from an existing profile. You can then retrieve the refresh token using the Alexa Skills Kit CLI. For instructions, see  in the  .

            ``AuthenticationConfiguration`` is a property of the ``Alexa::ASK::Skill`` resource.

            :param client_id: Client ID from Login with Amazon (LWA).
            :param client_secret: Client secret from Login with Amazon (LWA).
            :param refresh_token: Refresh token from Login with Amazon (LWA). This token is secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-authenticationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.alexa_ask import mixins as alexa_ask_mixins
                
                authentication_configuration_property = alexa_ask_mixins.CfnSkillPropsMixin.AuthenticationConfigurationProperty(
                    client_id="clientId",
                    client_secret="clientSecret",
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d5b1e028553fd9524d4572682c985d0a8868edb61fd583398803d8934ee1113)
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''Client ID from Login with Amazon (LWA).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-authenticationconfiguration.html#cfn-ask-skill-authenticationconfiguration-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''Client secret from Login with Amazon (LWA).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-authenticationconfiguration.html#cfn-ask-skill-authenticationconfiguration-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''Refresh token from Login with Amazon (LWA).

            This token is secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-authenticationconfiguration.html#cfn-ask-skill-authenticationconfiguration-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.alexa_ask.mixins.CfnSkillPropsMixin.OverridesProperty",
        jsii_struct_bases=[],
        name_mapping={"manifest": "manifest"},
    )
    class OverridesProperty:
        def __init__(self, *, manifest: typing.Any = None) -> None:
            '''The ``Overrides`` property type provides overrides to the skill package to apply when creating or updating the skill.

            Values provided here do not modify the contents of the original skill package. Currently, only overriding values inside of the skill manifest component of the package is supported.

            ``Overrides`` is a property of the ``Alexa::ASK::Skill SkillPackage`` property type.

            :param manifest: Overrides to apply to the skill manifest inside of the skill package. The skill manifest contains metadata about the skill. For more information, see .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-overrides.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.alexa_ask import mixins as alexa_ask_mixins
                
                # manifest: Any
                
                overrides_property = alexa_ask_mixins.CfnSkillPropsMixin.OverridesProperty(
                    manifest=manifest
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3fa7b16a2d282f96ba55bfa3b3e16e5d33af0f47b810586054ea08d48fa2292)
                check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if manifest is not None:
                self._values["manifest"] = manifest

        @builtins.property
        def manifest(self) -> typing.Any:
            '''Overrides to apply to the skill manifest inside of the skill package.

            The skill manifest contains metadata about the skill. For more information, see  .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-overrides.html#cfn-ask-skill-overrides-manifest
            '''
            result = self._values.get("manifest")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.alexa_ask.mixins.CfnSkillPropsMixin.SkillPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "overrides": "overrides",
            "s3_bucket": "s3Bucket",
            "s3_bucket_role": "s3BucketRole",
            "s3_key": "s3Key",
            "s3_object_version": "s3ObjectVersion",
        },
    )
    class SkillPackageProperty:
        def __init__(
            self,
            *,
            overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSkillPropsMixin.OverridesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_bucket_role: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
            s3_object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``SkillPackage`` property type contains configuration details for the skill package that contains the components of the Alexa skill.

            Skill packages are retrieved from an Amazon S3 bucket and key and used to create and update the skill. More details about the skill package format are located in the  .

            ``SkillPackage`` is a property of the ``Alexa::ASK::Skill`` resource.

            :param overrides: Overrides to the skill package to apply when creating or updating the skill. Values provided here do not modify the contents of the original skill package. Currently, only overriding values inside of the skill manifest component of the package is supported.
            :param s3_bucket: The name of the Amazon S3 bucket where the .zip file that contains the skill package is stored.
            :param s3_bucket_role: ARN of the IAM role that grants the Alexa service ( ``alexa-appkit.amazon.com`` ) permission to access the bucket and retrieve the skill package. This property is optional. If you do not provide it, the bucket must be publicly accessible or configured with a policy that allows this access. Otherwise, CloudFormation cannot create the skill.
            :param s3_key: The location and name of the skill package .zip file.
            :param s3_object_version: If you have S3 versioning enabled, the version ID of the skill package.zip file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-skillpackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.alexa_ask import mixins as alexa_ask_mixins
                
                # manifest: Any
                
                skill_package_property = alexa_ask_mixins.CfnSkillPropsMixin.SkillPackageProperty(
                    overrides=alexa_ask_mixins.CfnSkillPropsMixin.OverridesProperty(
                        manifest=manifest
                    ),
                    s3_bucket="s3Bucket",
                    s3_bucket_role="s3BucketRole",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f73e5e2860d75d330431553e078c5e0b61870d10e3243a3750282b82d5f946c4)
                check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_bucket_role", value=s3_bucket_role, expected_type=type_hints["s3_bucket_role"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
                check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if overrides is not None:
                self._values["overrides"] = overrides
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_bucket_role is not None:
                self._values["s3_bucket_role"] = s3_bucket_role
            if s3_key is not None:
                self._values["s3_key"] = s3_key
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version

        @builtins.property
        def overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSkillPropsMixin.OverridesProperty"]]:
            '''Overrides to the skill package to apply when creating or updating the skill.

            Values provided here do not modify the contents of the original skill package. Currently, only overriding values inside of the skill manifest component of the package is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-skillpackage.html#cfn-ask-skill-skillpackage-overrides
            '''
            result = self._values.get("overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSkillPropsMixin.OverridesProperty"]], result)

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket where the .zip file that contains the skill package is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-skillpackage.html#cfn-ask-skill-skillpackage-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_role(self) -> typing.Optional[builtins.str]:
            '''ARN of the IAM role that grants the Alexa service ( ``alexa-appkit.amazon.com`` ) permission to access the bucket and retrieve the skill package. This property is optional. If you do not provide it, the bucket must be publicly accessible or configured with a policy that allows this access. Otherwise, CloudFormation cannot create the skill.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-skillpackage.html#cfn-ask-skill-skillpackage-s3bucketrole
            '''
            result = self._values.get("s3_bucket_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''The location and name of the skill package .zip file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-skillpackage.html#cfn-ask-skill-skillpackage-s3key
            '''
            result = self._values.get("s3_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_version(self) -> typing.Optional[builtins.str]:
            '''If you have S3 versioning enabled, the version ID of the skill package.zip file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-skillpackage.html#cfn-ask-skill-skillpackage-s3objectversion
            '''
            result = self._values.get("s3_object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SkillPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnSkillMixinProps",
    "CfnSkillPropsMixin",
]

publication.publish()

def _typecheckingstub__4d6c58146f6b8a609a04e88edc00aca2b994edaeaf55d863684a146ea9270b54(
    *,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSkillPropsMixin.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    skill_package: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSkillPropsMixin.SkillPackageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vendor_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9141dc594772595c2db5b261da509eb350cf67b47ee89bd95e929e226c5ce91(
    props: typing.Union[CfnSkillMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41410569b4eead7a2bab0b9a2b57957530b2381fbe7c7219c02f3d3ac882070(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4e83d12cfd09edd362de4e7558b7770a2a3b6df067c4c1f59279fb5adb2231(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5b1e028553fd9524d4572682c985d0a8868edb61fd583398803d8934ee1113(
    *,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fa7b16a2d282f96ba55bfa3b3e16e5d33af0f47b810586054ea08d48fa2292(
    *,
    manifest: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73e5e2860d75d330431553e078c5e0b61870d10e3243a3750282b82d5f946c4(
    *,
    overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSkillPropsMixin.OverridesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_bucket_role: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
    s3_object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
