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
    jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnCRLMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "crl_data": "crlData",
        "enabled": "enabled",
        "name": "name",
        "tags": "tags",
        "trust_anchor_arn": "trustAnchorArn",
    },
)
class CfnCRLMixinProps:
    def __init__(
        self,
        *,
        crl_data: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trust_anchor_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCRLPropsMixin.

        :param crl_data: The x509 v3 specified certificate revocation list (CRL).
        :param enabled: Specifies whether the certificate revocation list (CRL) is enabled.
        :param name: The name of the certificate revocation list (CRL).
        :param tags: A list of tags to attach to the certificate revocation list (CRL).
        :param trust_anchor_arn: The ARN of the TrustAnchor the certificate revocation list (CRL) will provide revocation for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
            
            cfn_cRLMixin_props = rolesanywhere_mixins.CfnCRLMixinProps(
                crl_data="crlData",
                enabled=False,
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trust_anchor_arn="trustAnchorArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d51681b60e94e6c96ed8753e6b6ef65d98cc5730e34a8b2f5a16daa07dd8e1ba)
            check_type(argname="argument crl_data", value=crl_data, expected_type=type_hints["crl_data"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trust_anchor_arn", value=trust_anchor_arn, expected_type=type_hints["trust_anchor_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if crl_data is not None:
            self._values["crl_data"] = crl_data
        if enabled is not None:
            self._values["enabled"] = enabled
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if trust_anchor_arn is not None:
            self._values["trust_anchor_arn"] = trust_anchor_arn

    @builtins.property
    def crl_data(self) -> typing.Optional[builtins.str]:
        '''The x509 v3 specified certificate revocation list (CRL).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-crldata
        '''
        result = self._values.get("crl_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the certificate revocation list (CRL) is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the certificate revocation list (CRL).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to attach to the certificate revocation list (CRL).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def trust_anchor_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the TrustAnchor the certificate revocation list (CRL) will provide revocation for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html#cfn-rolesanywhere-crl-trustanchorarn
        '''
        result = self._values.get("trust_anchor_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCRLMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCRLPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnCRLPropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-crl.html
    :cloudformationResource: AWS::RolesAnywhere::CRL
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
        
        cfn_cRLProps_mixin = rolesanywhere_mixins.CfnCRLPropsMixin(rolesanywhere_mixins.CfnCRLMixinProps(
            crl_data="crlData",
            enabled=False,
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trust_anchor_arn="trustAnchorArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCRLMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RolesAnywhere::CRL``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__100210b43f8d7cbad7271156c6728f8592de69eacfc4fea27f53a4e4ee1896fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36c0d622f5a29658c156bae772a46cb97fd9d2c3105918596e392a92fe570096)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d27711e0020d8ac047031ce0038d0c18fe400b61e6054761876200c1c18afc7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCRLMixinProps:
        return typing.cast(CfnCRLMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_role_session_name": "acceptRoleSessionName",
        "attribute_mappings": "attributeMappings",
        "duration_seconds": "durationSeconds",
        "enabled": "enabled",
        "managed_policy_arns": "managedPolicyArns",
        "name": "name",
        "require_instance_properties": "requireInstanceProperties",
        "role_arns": "roleArns",
        "session_policy": "sessionPolicy",
        "tags": "tags",
    },
)
class CfnProfileMixinProps:
    def __init__(
        self,
        *,
        accept_role_session_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        attribute_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProfilePropsMixin.AttributeMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        duration_seconds: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        require_instance_properties: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProfilePropsMixin.

        :param accept_role_session_name: Used to determine if a custom role session name will be accepted in a temporary credential request.
        :param attribute_mappings: A mapping applied to the authenticating end-entity certificate.
        :param duration_seconds: The number of seconds vended session credentials will be valid for.
        :param enabled: The enabled status of the resource.
        :param managed_policy_arns: A list of managed policy ARNs. Managed policies identified by this list will be applied to the vended session credentials.
        :param name: The customer specified name of the resource.
        :param require_instance_properties: Specifies whether instance properties are required in CreateSession requests with this profile.
        :param role_arns: A list of IAM role ARNs that can be assumed when this profile is specified in a CreateSession request.
        :param session_policy: A session policy that will applied to the trust boundary of the vended session credentials.
        :param tags: A list of Tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
            
            cfn_profile_mixin_props = rolesanywhere_mixins.CfnProfileMixinProps(
                accept_role_session_name=False,
                attribute_mappings=[rolesanywhere_mixins.CfnProfilePropsMixin.AttributeMappingProperty(
                    certificate_field="certificateField",
                    mapping_rules=[rolesanywhere_mixins.CfnProfilePropsMixin.MappingRuleProperty(
                        specifier="specifier"
                    )]
                )],
                duration_seconds=123,
                enabled=False,
                managed_policy_arns=["managedPolicyArns"],
                name="name",
                require_instance_properties=False,
                role_arns=["roleArns"],
                session_policy="sessionPolicy",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ebebcd76260ad0d0ddc085951f689fa5f51eef9008771e19efc5d1e839205d)
            check_type(argname="argument accept_role_session_name", value=accept_role_session_name, expected_type=type_hints["accept_role_session_name"])
            check_type(argname="argument attribute_mappings", value=attribute_mappings, expected_type=type_hints["attribute_mappings"])
            check_type(argname="argument duration_seconds", value=duration_seconds, expected_type=type_hints["duration_seconds"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument require_instance_properties", value=require_instance_properties, expected_type=type_hints["require_instance_properties"])
            check_type(argname="argument role_arns", value=role_arns, expected_type=type_hints["role_arns"])
            check_type(argname="argument session_policy", value=session_policy, expected_type=type_hints["session_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_role_session_name is not None:
            self._values["accept_role_session_name"] = accept_role_session_name
        if attribute_mappings is not None:
            self._values["attribute_mappings"] = attribute_mappings
        if duration_seconds is not None:
            self._values["duration_seconds"] = duration_seconds
        if enabled is not None:
            self._values["enabled"] = enabled
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if name is not None:
            self._values["name"] = name
        if require_instance_properties is not None:
            self._values["require_instance_properties"] = require_instance_properties
        if role_arns is not None:
            self._values["role_arns"] = role_arns
        if session_policy is not None:
            self._values["session_policy"] = session_policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def accept_role_session_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Used to determine if a custom role session name will be accepted in a temporary credential request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-acceptrolesessionname
        '''
        result = self._values.get("accept_role_session_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def attribute_mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProfilePropsMixin.AttributeMappingProperty"]]]]:
        '''A mapping applied to the authenticating end-entity certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-attributemappings
        '''
        result = self._values.get("attribute_mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProfilePropsMixin.AttributeMappingProperty"]]]], result)

    @builtins.property
    def duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds vended session credentials will be valid for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-durationseconds
        '''
        result = self._values.get("duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The enabled status of the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of managed policy ARNs.

        Managed policies identified by this list will be applied to the vended session credentials.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-managedpolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The customer specified name of the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_instance_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether instance properties are required in CreateSession requests with this profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-requireinstanceproperties
        '''
        result = self._values.get("require_instance_properties")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def role_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM role ARNs that can be assumed when this profile is specified in a CreateSession request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-rolearns
        '''
        result = self._values.get("role_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_policy(self) -> typing.Optional[builtins.str]:
        '''A session policy that will applied to the trust boundary of the vended session credentials.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-sessionpolicy
        '''
        result = self._values.get("session_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of Tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html#cfn-rolesanywhere-profile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnProfilePropsMixin",
):
    '''Creates a Profile.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-profile.html
    :cloudformationResource: AWS::RolesAnywhere::Profile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
        
        cfn_profile_props_mixin = rolesanywhere_mixins.CfnProfilePropsMixin(rolesanywhere_mixins.CfnProfileMixinProps(
            accept_role_session_name=False,
            attribute_mappings=[rolesanywhere_mixins.CfnProfilePropsMixin.AttributeMappingProperty(
                certificate_field="certificateField",
                mapping_rules=[rolesanywhere_mixins.CfnProfilePropsMixin.MappingRuleProperty(
                    specifier="specifier"
                )]
            )],
            duration_seconds=123,
            enabled=False,
            managed_policy_arns=["managedPolicyArns"],
            name="name",
            require_instance_properties=False,
            role_arns=["roleArns"],
            session_policy="sessionPolicy",
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
        props: typing.Union[CfnProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RolesAnywhere::Profile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7bcc0257681415b73b9e8ede195e10d418e89249e374409bbcc24cf7c7369b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f5571332cefbe916ad40746921aa5ba1d55ec625111f03d14abefece027f388)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415eb989f43b75eb9d997da8a1005c31ce111d446e043f43798e1308eac452ad)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProfileMixinProps:
        return typing.cast(CfnProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnProfilePropsMixin.AttributeMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_field": "certificateField",
            "mapping_rules": "mappingRules",
        },
    )
    class AttributeMappingProperty:
        def __init__(
            self,
            *,
            certificate_field: typing.Optional[builtins.str] = None,
            mapping_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProfilePropsMixin.MappingRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A mapping applied to the authenticating end-entity certificate.

            :param certificate_field: Fields (x509Subject, x509Issuer and x509SAN) within X.509 certificates.
            :param mapping_rules: A list of mapping entries for every supported specifier or sub-field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-profile-attributemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
                
                attribute_mapping_property = rolesanywhere_mixins.CfnProfilePropsMixin.AttributeMappingProperty(
                    certificate_field="certificateField",
                    mapping_rules=[rolesanywhere_mixins.CfnProfilePropsMixin.MappingRuleProperty(
                        specifier="specifier"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7ae494c894f78d6e553bfa1271d4cca464ac0bdbd60646d7c89c4b78ec831229)
                check_type(argname="argument certificate_field", value=certificate_field, expected_type=type_hints["certificate_field"])
                check_type(argname="argument mapping_rules", value=mapping_rules, expected_type=type_hints["mapping_rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_field is not None:
                self._values["certificate_field"] = certificate_field
            if mapping_rules is not None:
                self._values["mapping_rules"] = mapping_rules

        @builtins.property
        def certificate_field(self) -> typing.Optional[builtins.str]:
            '''Fields (x509Subject, x509Issuer and x509SAN) within X.509 certificates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-profile-attributemapping.html#cfn-rolesanywhere-profile-attributemapping-certificatefield
            '''
            result = self._values.get("certificate_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mapping_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProfilePropsMixin.MappingRuleProperty"]]]]:
            '''A list of mapping entries for every supported specifier or sub-field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-profile-attributemapping.html#cfn-rolesanywhere-profile-attributemapping-mappingrules
            '''
            result = self._values.get("mapping_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProfilePropsMixin.MappingRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnProfilePropsMixin.MappingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"specifier": "specifier"},
    )
    class MappingRuleProperty:
        def __init__(self, *, specifier: typing.Optional[builtins.str] = None) -> None:
            '''A single mapping entry for each supported specifier or sub-field.

            :param specifier: Specifier within a certificate field, such as CN, OU, or UID from the Subject field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-profile-mappingrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
                
                mapping_rule_property = rolesanywhere_mixins.CfnProfilePropsMixin.MappingRuleProperty(
                    specifier="specifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbff0bbe32b8af3c3f72ca1e13ff6b8b589b717757e41eb7bd06f1abdc332f15)
                check_type(argname="argument specifier", value=specifier, expected_type=type_hints["specifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if specifier is not None:
                self._values["specifier"] = specifier

        @builtins.property
        def specifier(self) -> typing.Optional[builtins.str]:
            '''Specifier within a certificate field, such as CN, OU, or UID from the Subject field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-profile-mappingrule.html#cfn-rolesanywhere-profile-mappingrule-specifier
            '''
            result = self._values.get("specifier")
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
    jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnTrustAnchorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "name": "name",
        "notification_settings": "notificationSettings",
        "source": "source",
        "tags": "tags",
    },
)
class CfnTrustAnchorMixinProps:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        notification_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrustAnchorPropsMixin.NotificationSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrustAnchorPropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTrustAnchorPropsMixin.

        :param enabled: Indicates whether the trust anchor is enabled.
        :param name: The name of the trust anchor.
        :param notification_settings: A list of notification settings to be associated to the trust anchor.
        :param source: The trust anchor type and its related certificate data.
        :param tags: The tags to attach to the trust anchor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
            
            cfn_trust_anchor_mixin_props = rolesanywhere_mixins.CfnTrustAnchorMixinProps(
                enabled=False,
                name="name",
                notification_settings=[rolesanywhere_mixins.CfnTrustAnchorPropsMixin.NotificationSettingProperty(
                    channel="channel",
                    enabled=False,
                    event="event",
                    threshold=123
                )],
                source=rolesanywhere_mixins.CfnTrustAnchorPropsMixin.SourceProperty(
                    source_data=rolesanywhere_mixins.CfnTrustAnchorPropsMixin.SourceDataProperty(
                        acm_pca_arn="acmPcaArn",
                        x509_certificate_data="x509CertificateData"
                    ),
                    source_type="sourceType"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27f725fbeed84ec7b7d53a0e3093b4378a0a8188c7088919478b108fad39a5d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notification_settings", value=notification_settings, expected_type=type_hints["notification_settings"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if name is not None:
            self._values["name"] = name
        if notification_settings is not None:
            self._values["notification_settings"] = notification_settings
        if source is not None:
            self._values["source"] = source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the trust anchor is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the trust anchor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrustAnchorPropsMixin.NotificationSettingProperty"]]]]:
        '''A list of notification settings to be associated to the trust anchor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-notificationsettings
        '''
        result = self._values.get("notification_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrustAnchorPropsMixin.NotificationSettingProperty"]]]], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrustAnchorPropsMixin.SourceProperty"]]:
        '''The trust anchor type and its related certificate data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrustAnchorPropsMixin.SourceProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to attach to the trust anchor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html#cfn-rolesanywhere-trustanchor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrustAnchorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTrustAnchorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnTrustAnchorPropsMixin",
):
    '''Creates a TrustAnchor.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rolesanywhere-trustanchor.html
    :cloudformationResource: AWS::RolesAnywhere::TrustAnchor
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
        
        cfn_trust_anchor_props_mixin = rolesanywhere_mixins.CfnTrustAnchorPropsMixin(rolesanywhere_mixins.CfnTrustAnchorMixinProps(
            enabled=False,
            name="name",
            notification_settings=[rolesanywhere_mixins.CfnTrustAnchorPropsMixin.NotificationSettingProperty(
                channel="channel",
                enabled=False,
                event="event",
                threshold=123
            )],
            source=rolesanywhere_mixins.CfnTrustAnchorPropsMixin.SourceProperty(
                source_data=rolesanywhere_mixins.CfnTrustAnchorPropsMixin.SourceDataProperty(
                    acm_pca_arn="acmPcaArn",
                    x509_certificate_data="x509CertificateData"
                ),
                source_type="sourceType"
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
        props: typing.Union[CfnTrustAnchorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RolesAnywhere::TrustAnchor``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d583a4cc5ca849d272acdfa774f0459918d08d4162b6efd86c210699c9b75813)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30487468c144471e0bb7ed5301a264bbd7b96241d1bc38da318ff30a00a61143)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6cac847d507435e3e6f701f72c5c4341d820eb334bc7c885ccb4ce22e1ef78e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTrustAnchorMixinProps:
        return typing.cast(CfnTrustAnchorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnTrustAnchorPropsMixin.NotificationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel": "channel",
            "enabled": "enabled",
            "event": "event",
            "threshold": "threshold",
        },
    )
    class NotificationSettingProperty:
        def __init__(
            self,
            *,
            channel: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            event: typing.Optional[builtins.str] = None,
            threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Customizable notification settings that will be applied to notification events.

            IAM Roles Anywhere consumes these settings while notifying across multiple channels - CloudWatch metrics, EventBridge, and AWS Health Dashboard .

            :param channel: The specified channel of notification. IAM Roles Anywhere uses CloudWatch metrics, EventBridge, and AWS Health Dashboard to notify for an event. .. epigraph:: In the absence of a specific channel, IAM Roles Anywhere applies this setting to 'ALL' channels.
            :param enabled: Indicates whether the notification setting is enabled.
            :param event: The event to which this notification setting is applied.
            :param threshold: The number of days before a notification event. This value is required for a notification setting that is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-notificationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
                
                notification_setting_property = rolesanywhere_mixins.CfnTrustAnchorPropsMixin.NotificationSettingProperty(
                    channel="channel",
                    enabled=False,
                    event="event",
                    threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b4cb2c61b60d9534b2dd39168a9df5759015bd6de1b3c70bb23224149de52e1)
                check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument event", value=event, expected_type=type_hints["event"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel is not None:
                self._values["channel"] = channel
            if enabled is not None:
                self._values["enabled"] = enabled
            if event is not None:
                self._values["event"] = event
            if threshold is not None:
                self._values["threshold"] = threshold

        @builtins.property
        def channel(self) -> typing.Optional[builtins.str]:
            '''The specified channel of notification.

            IAM Roles Anywhere uses CloudWatch metrics, EventBridge, and AWS Health Dashboard to notify for an event.
            .. epigraph::

               In the absence of a specific channel, IAM Roles Anywhere applies this setting to 'ALL' channels.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-notificationsetting.html#cfn-rolesanywhere-trustanchor-notificationsetting-channel
            '''
            result = self._values.get("channel")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the notification setting is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-notificationsetting.html#cfn-rolesanywhere-trustanchor-notificationsetting-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def event(self) -> typing.Optional[builtins.str]:
            '''The event to which this notification setting is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-notificationsetting.html#cfn-rolesanywhere-trustanchor-notificationsetting-event
            '''
            result = self._values.get("event")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of days before a notification event.

            This value is required for a notification setting that is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-notificationsetting.html#cfn-rolesanywhere-trustanchor-notificationsetting-threshold
            '''
            result = self._values.get("threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnTrustAnchorPropsMixin.SourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "acm_pca_arn": "acmPcaArn",
            "x509_certificate_data": "x509CertificateData",
        },
    )
    class SourceDataProperty:
        def __init__(
            self,
            *,
            acm_pca_arn: typing.Optional[builtins.str] = None,
            x509_certificate_data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A union object representing the data field of the TrustAnchor depending on its type.

            :param acm_pca_arn: The root certificate of the Private Certificate Authority specified by this ARN is used in trust validation for temporary credential requests. Included for trust anchors of type ``AWS_ACM_PCA`` . .. epigraph:: This field is not supported in your region.
            :param x509_certificate_data: The PEM-encoded data for the certificate anchor. Included for trust anchors of type ``CERTIFICATE_BUNDLE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-sourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
                
                source_data_property = rolesanywhere_mixins.CfnTrustAnchorPropsMixin.SourceDataProperty(
                    acm_pca_arn="acmPcaArn",
                    x509_certificate_data="x509CertificateData"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__836c54848f94b86a92323a149fde8163f8ab0de66a219215503850fd0d7abb20)
                check_type(argname="argument acm_pca_arn", value=acm_pca_arn, expected_type=type_hints["acm_pca_arn"])
                check_type(argname="argument x509_certificate_data", value=x509_certificate_data, expected_type=type_hints["x509_certificate_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acm_pca_arn is not None:
                self._values["acm_pca_arn"] = acm_pca_arn
            if x509_certificate_data is not None:
                self._values["x509_certificate_data"] = x509_certificate_data

        @builtins.property
        def acm_pca_arn(self) -> typing.Optional[builtins.str]:
            '''The root certificate of the Private Certificate Authority specified by this ARN is used in trust validation for temporary credential requests.

            Included for trust anchors of type ``AWS_ACM_PCA`` .
            .. epigraph::

               This field is not supported in your region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-sourcedata.html#cfn-rolesanywhere-trustanchor-sourcedata-acmpcaarn
            '''
            result = self._values.get("acm_pca_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def x509_certificate_data(self) -> typing.Optional[builtins.str]:
            '''The PEM-encoded data for the certificate anchor.

            Included for trust anchors of type ``CERTIFICATE_BUNDLE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-sourcedata.html#cfn-rolesanywhere-trustanchor-sourcedata-x509certificatedata
            '''
            result = self._values.get("x509_certificate_data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rolesanywhere.mixins.CfnTrustAnchorPropsMixin.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={"source_data": "sourceData", "source_type": "sourceType"},
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            source_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrustAnchorPropsMixin.SourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Object representing the TrustAnchor type and its related certificate data.

            :param source_data: A union object representing the data field of the TrustAnchor depending on its type.
            :param source_type: The type of the TrustAnchor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rolesanywhere import mixins as rolesanywhere_mixins
                
                source_property = rolesanywhere_mixins.CfnTrustAnchorPropsMixin.SourceProperty(
                    source_data=rolesanywhere_mixins.CfnTrustAnchorPropsMixin.SourceDataProperty(
                        acm_pca_arn="acmPcaArn",
                        x509_certificate_data="x509CertificateData"
                    ),
                    source_type="sourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8116195624dc12882d2b4db481c62ac8b0ee216f493faaf80e5d5ef90abd09ef)
                check_type(argname="argument source_data", value=source_data, expected_type=type_hints["source_data"])
                check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_data is not None:
                self._values["source_data"] = source_data
            if source_type is not None:
                self._values["source_type"] = source_type

        @builtins.property
        def source_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrustAnchorPropsMixin.SourceDataProperty"]]:
            '''A union object representing the data field of the TrustAnchor depending on its type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-source.html#cfn-rolesanywhere-trustanchor-source-sourcedata
            '''
            result = self._values.get("source_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrustAnchorPropsMixin.SourceDataProperty"]], result)

        @builtins.property
        def source_type(self) -> typing.Optional[builtins.str]:
            '''The type of the TrustAnchor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rolesanywhere-trustanchor-source.html#cfn-rolesanywhere-trustanchor-source-sourcetype
            '''
            result = self._values.get("source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCRLMixinProps",
    "CfnCRLPropsMixin",
    "CfnProfileMixinProps",
    "CfnProfilePropsMixin",
    "CfnTrustAnchorMixinProps",
    "CfnTrustAnchorPropsMixin",
]

publication.publish()

def _typecheckingstub__d51681b60e94e6c96ed8753e6b6ef65d98cc5730e34a8b2f5a16daa07dd8e1ba(
    *,
    crl_data: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust_anchor_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100210b43f8d7cbad7271156c6728f8592de69eacfc4fea27f53a4e4ee1896fe(
    props: typing.Union[CfnCRLMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c0d622f5a29658c156bae772a46cb97fd9d2c3105918596e392a92fe570096(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d27711e0020d8ac047031ce0038d0c18fe400b61e6054761876200c1c18afc7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ebebcd76260ad0d0ddc085951f689fa5f51eef9008771e19efc5d1e839205d(
    *,
    accept_role_session_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    attribute_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProfilePropsMixin.AttributeMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    duration_seconds: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    require_instance_properties: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7bcc0257681415b73b9e8ede195e10d418e89249e374409bbcc24cf7c7369b(
    props: typing.Union[CfnProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5571332cefbe916ad40746921aa5ba1d55ec625111f03d14abefece027f388(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415eb989f43b75eb9d997da8a1005c31ce111d446e043f43798e1308eac452ad(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae494c894f78d6e553bfa1271d4cca464ac0bdbd60646d7c89c4b78ec831229(
    *,
    certificate_field: typing.Optional[builtins.str] = None,
    mapping_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProfilePropsMixin.MappingRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbff0bbe32b8af3c3f72ca1e13ff6b8b589b717757e41eb7bd06f1abdc332f15(
    *,
    specifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27f725fbeed84ec7b7d53a0e3093b4378a0a8188c7088919478b108fad39a5d(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    notification_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrustAnchorPropsMixin.NotificationSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrustAnchorPropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d583a4cc5ca849d272acdfa774f0459918d08d4162b6efd86c210699c9b75813(
    props: typing.Union[CfnTrustAnchorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30487468c144471e0bb7ed5301a264bbd7b96241d1bc38da318ff30a00a61143(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6cac847d507435e3e6f701f72c5c4341d820eb334bc7c885ccb4ce22e1ef78e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4cb2c61b60d9534b2dd39168a9df5759015bd6de1b3c70bb23224149de52e1(
    *,
    channel: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    event: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836c54848f94b86a92323a149fde8163f8ab0de66a219215503850fd0d7abb20(
    *,
    acm_pca_arn: typing.Optional[builtins.str] = None,
    x509_certificate_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8116195624dc12882d2b4db481c62ac8b0ee216f493faaf80e5d5ef90abd09ef(
    *,
    source_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrustAnchorPropsMixin.SourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
