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
    jsii_type="@aws-cdk/mixins-preview.aws_codeartifact.mixins.CfnDomainMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "encryption_key": "encryptionKey",
        "permissions_policy_document": "permissionsPolicyDocument",
        "tags": "tags",
    },
)
class CfnDomainMixinProps:
    def __init__(
        self,
        *,
        domain_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        permissions_policy_document: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDomainPropsMixin.

        :param domain_name: A string that specifies the name of the requested domain.
        :param encryption_key: The key used to encrypt the domain.
        :param permissions_policy_document: The document that defines the resource policy that is set on a domain.
        :param tags: A list of tags to be applied to the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codeartifact import mixins as codeartifact_mixins
            
            # permissions_policy_document: Any
            
            cfn_domain_mixin_props = codeartifact_mixins.CfnDomainMixinProps(
                domain_name="domainName",
                encryption_key="encryptionKey",
                permissions_policy_document=permissions_policy_document,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a10ad46ffe1f7dd909132b66a848d024303fe2d7f5cc16008610fc45fa0245)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument permissions_policy_document", value=permissions_policy_document, expected_type=type_hints["permissions_policy_document"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if permissions_policy_document is not None:
            self._values["permissions_policy_document"] = permissions_policy_document
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''A string that specifies the name of the requested domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The key used to encrypt the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-encryptionkey
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_policy_document(self) -> typing.Any:
        '''The document that defines the resource policy that is set on a domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-permissionspolicydocument
        '''
        result = self._values.get("permissions_policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to be applied to the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html#cfn-codeartifact-domain-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codeartifact.mixins.CfnDomainPropsMixin",
):
    '''The ``AWS::CodeArtifact::Domain`` resource creates an AWS CodeArtifact domain.

    CodeArtifact *domains* make it easier to manage multiple repositories across an organization. You can use a domain to apply permissions across many repositories owned by different AWS accounts. For more information about domains, see the `Domain concepts information <https://docs.aws.amazon.com/codeartifact/latest/ug/codeartifact-concepts.html#welcome-concepts-domain>`_ in the *CodeArtifact User Guide* . For more information about the ``CreateDomain`` API, see `CreateDomain <https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_CreateDomain.html>`_ in the *CodeArtifact API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-domain.html
    :cloudformationResource: AWS::CodeArtifact::Domain
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codeartifact import mixins as codeartifact_mixins
        
        # permissions_policy_document: Any
        
        cfn_domain_props_mixin = codeartifact_mixins.CfnDomainPropsMixin(codeartifact_mixins.CfnDomainMixinProps(
            domain_name="domainName",
            encryption_key="encryptionKey",
            permissions_policy_document=permissions_policy_document,
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
        props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeArtifact::Domain``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a9c8f7264c50c9fe8ede04828aedfa3b11d39f622fd3ac92d111252fd1c347)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b62f6891c30f4d2bd2ef1c7e9dddb7f5aecbf0b90bad72cdbadeab6f17e021f6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3a52360b83a85068c9964c79c7e8b9545e6309b7e768de5eb162edfbf866e3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainMixinProps:
        return typing.cast(CfnDomainMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_codeartifact.mixins.CfnPackageGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "contact_info": "contactInfo",
        "description": "description",
        "domain_name": "domainName",
        "domain_owner": "domainOwner",
        "origin_configuration": "originConfiguration",
        "pattern": "pattern",
        "tags": "tags",
    },
)
class CfnPackageGroupMixinProps:
    def __init__(
        self,
        *,
        contact_info: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_owner: typing.Optional[builtins.str] = None,
        origin_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackageGroupPropsMixin.OriginConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        pattern: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPackageGroupPropsMixin.

        :param contact_info: The contact information of the package group.
        :param description: The description of the package group.
        :param domain_name: The domain that contains the package group.
        :param domain_owner: The 12-digit account number of the AWS account that owns the domain. It does not include dashes or spaces.
        :param origin_configuration: Details about the package origin configuration of a package group.
        :param pattern: The pattern of the package group. The pattern determines which packages are associated with the package group.
        :param tags: An array of key-value pairs to apply to the package group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-packagegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codeartifact import mixins as codeartifact_mixins
            
            cfn_package_group_mixin_props = codeartifact_mixins.CfnPackageGroupMixinProps(
                contact_info="contactInfo",
                description="description",
                domain_name="domainName",
                domain_owner="domainOwner",
                origin_configuration=codeartifact_mixins.CfnPackageGroupPropsMixin.OriginConfigurationProperty(
                    restrictions=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionsProperty(
                        external_upstream=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                            repositories=["repositories"],
                            restriction_mode="restrictionMode"
                        ),
                        internal_upstream=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                            repositories=["repositories"],
                            restriction_mode="restrictionMode"
                        ),
                        publish=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                            repositories=["repositories"],
                            restriction_mode="restrictionMode"
                        )
                    )
                ),
                pattern="pattern",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c983703994b428a2fe5231cd4b76bbbe89838ba5101853629993e94d9f8cb1)
            check_type(argname="argument contact_info", value=contact_info, expected_type=type_hints["contact_info"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_owner", value=domain_owner, expected_type=type_hints["domain_owner"])
            check_type(argname="argument origin_configuration", value=origin_configuration, expected_type=type_hints["origin_configuration"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contact_info is not None:
            self._values["contact_info"] = contact_info
        if description is not None:
            self._values["description"] = description
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_owner is not None:
            self._values["domain_owner"] = domain_owner
        if origin_configuration is not None:
            self._values["origin_configuration"] = origin_configuration
        if pattern is not None:
            self._values["pattern"] = pattern
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def contact_info(self) -> typing.Optional[builtins.str]:
        '''The contact information of the package group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-packagegroup.html#cfn-codeartifact-packagegroup-contactinfo
        '''
        result = self._values.get("contact_info")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the package group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-packagegroup.html#cfn-codeartifact-packagegroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain that contains the package group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-packagegroup.html#cfn-codeartifact-packagegroup-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_owner(self) -> typing.Optional[builtins.str]:
        '''The 12-digit account number of the AWS account that owns the domain.

        It does not include dashes or spaces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-packagegroup.html#cfn-codeartifact-packagegroup-domainowner
        '''
        result = self._values.get("domain_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackageGroupPropsMixin.OriginConfigurationProperty"]]:
        '''Details about the package origin configuration of a package group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-packagegroup.html#cfn-codeartifact-packagegroup-originconfiguration
        '''
        result = self._values.get("origin_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackageGroupPropsMixin.OriginConfigurationProperty"]], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''The pattern of the package group.

        The pattern determines which packages are associated with the package group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-packagegroup.html#cfn-codeartifact-packagegroup-pattern
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to the package group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-packagegroup.html#cfn-codeartifact-packagegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPackageGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPackageGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codeartifact.mixins.CfnPackageGroupPropsMixin",
):
    '''Creates a package group.

    For more information about creating package groups, including example CLI commands, see `Create a package group <https://docs.aws.amazon.com/codeartifact/latest/ug/create-package-group.html>`_ in the *CodeArtifact User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-packagegroup.html
    :cloudformationResource: AWS::CodeArtifact::PackageGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codeartifact import mixins as codeartifact_mixins
        
        cfn_package_group_props_mixin = codeartifact_mixins.CfnPackageGroupPropsMixin(codeartifact_mixins.CfnPackageGroupMixinProps(
            contact_info="contactInfo",
            description="description",
            domain_name="domainName",
            domain_owner="domainOwner",
            origin_configuration=codeartifact_mixins.CfnPackageGroupPropsMixin.OriginConfigurationProperty(
                restrictions=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionsProperty(
                    external_upstream=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                        repositories=["repositories"],
                        restriction_mode="restrictionMode"
                    ),
                    internal_upstream=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                        repositories=["repositories"],
                        restriction_mode="restrictionMode"
                    ),
                    publish=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                        repositories=["repositories"],
                        restriction_mode="restrictionMode"
                    )
                )
            ),
            pattern="pattern",
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
        props: typing.Union[CfnPackageGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeArtifact::PackageGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac33ed178b39338c5a2583cb84848d496543601e23b9a0e0c22599ff2afd1db2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89f67c30c66eae89f80d01006acaff9ef9db7765c14ecadea926c53650b17d7c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72efa8c2a430b370d95d0bdff5de09d357935d2ae91f60d0c19e5ae5e8475550)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPackageGroupMixinProps:
        return typing.cast(CfnPackageGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codeartifact.mixins.CfnPackageGroupPropsMixin.OriginConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"restrictions": "restrictions"},
    )
    class OriginConfigurationProperty:
        def __init__(
            self,
            *,
            restrictions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackageGroupPropsMixin.RestrictionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param restrictions: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeartifact-packagegroup-originconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codeartifact import mixins as codeartifact_mixins
                
                origin_configuration_property = codeartifact_mixins.CfnPackageGroupPropsMixin.OriginConfigurationProperty(
                    restrictions=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionsProperty(
                        external_upstream=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                            repositories=["repositories"],
                            restriction_mode="restrictionMode"
                        ),
                        internal_upstream=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                            repositories=["repositories"],
                            restriction_mode="restrictionMode"
                        ),
                        publish=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                            repositories=["repositories"],
                            restriction_mode="restrictionMode"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ddc0f891d1c5b986d68307ec5610e43a28f1b6d5de2508cbfe2361e0e24903a1)
                check_type(argname="argument restrictions", value=restrictions, expected_type=type_hints["restrictions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if restrictions is not None:
                self._values["restrictions"] = restrictions

        @builtins.property
        def restrictions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackageGroupPropsMixin.RestrictionsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeartifact-packagegroup-originconfiguration.html#cfn-codeartifact-packagegroup-originconfiguration-restrictions
            '''
            result = self._values.get("restrictions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackageGroupPropsMixin.RestrictionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codeartifact.mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "repositories": "repositories",
            "restriction_mode": "restrictionMode",
        },
    )
    class RestrictionTypeProperty:
        def __init__(
            self,
            *,
            repositories: typing.Optional[typing.Sequence[builtins.str]] = None,
            restriction_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param repositories: 
            :param restriction_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeartifact-packagegroup-restrictiontype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codeartifact import mixins as codeartifact_mixins
                
                restriction_type_property = codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                    repositories=["repositories"],
                    restriction_mode="restrictionMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09f2a622bd3bcc5e60f18bc1e8c1f25cb6467f68711deae75ce9b5c9fead0e0c)
                check_type(argname="argument repositories", value=repositories, expected_type=type_hints["repositories"])
                check_type(argname="argument restriction_mode", value=restriction_mode, expected_type=type_hints["restriction_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if repositories is not None:
                self._values["repositories"] = repositories
            if restriction_mode is not None:
                self._values["restriction_mode"] = restriction_mode

        @builtins.property
        def repositories(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeartifact-packagegroup-restrictiontype.html#cfn-codeartifact-packagegroup-restrictiontype-repositories
            '''
            result = self._values.get("repositories")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def restriction_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeartifact-packagegroup-restrictiontype.html#cfn-codeartifact-packagegroup-restrictiontype-restrictionmode
            '''
            result = self._values.get("restriction_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RestrictionTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codeartifact.mixins.CfnPackageGroupPropsMixin.RestrictionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "external_upstream": "externalUpstream",
            "internal_upstream": "internalUpstream",
            "publish": "publish",
        },
    )
    class RestrictionsProperty:
        def __init__(
            self,
            *,
            external_upstream: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackageGroupPropsMixin.RestrictionTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            internal_upstream: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackageGroupPropsMixin.RestrictionTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            publish: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPackageGroupPropsMixin.RestrictionTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param external_upstream: 
            :param internal_upstream: 
            :param publish: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeartifact-packagegroup-restrictions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codeartifact import mixins as codeartifact_mixins
                
                restrictions_property = codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionsProperty(
                    external_upstream=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                        repositories=["repositories"],
                        restriction_mode="restrictionMode"
                    ),
                    internal_upstream=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                        repositories=["repositories"],
                        restriction_mode="restrictionMode"
                    ),
                    publish=codeartifact_mixins.CfnPackageGroupPropsMixin.RestrictionTypeProperty(
                        repositories=["repositories"],
                        restriction_mode="restrictionMode"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9a02008bb40ba5a546428c323627715875344c815b4cbde5878c6d31a6db58e)
                check_type(argname="argument external_upstream", value=external_upstream, expected_type=type_hints["external_upstream"])
                check_type(argname="argument internal_upstream", value=internal_upstream, expected_type=type_hints["internal_upstream"])
                check_type(argname="argument publish", value=publish, expected_type=type_hints["publish"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if external_upstream is not None:
                self._values["external_upstream"] = external_upstream
            if internal_upstream is not None:
                self._values["internal_upstream"] = internal_upstream
            if publish is not None:
                self._values["publish"] = publish

        @builtins.property
        def external_upstream(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackageGroupPropsMixin.RestrictionTypeProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeartifact-packagegroup-restrictions.html#cfn-codeartifact-packagegroup-restrictions-externalupstream
            '''
            result = self._values.get("external_upstream")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackageGroupPropsMixin.RestrictionTypeProperty"]], result)

        @builtins.property
        def internal_upstream(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackageGroupPropsMixin.RestrictionTypeProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeartifact-packagegroup-restrictions.html#cfn-codeartifact-packagegroup-restrictions-internalupstream
            '''
            result = self._values.get("internal_upstream")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackageGroupPropsMixin.RestrictionTypeProperty"]], result)

        @builtins.property
        def publish(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackageGroupPropsMixin.RestrictionTypeProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeartifact-packagegroup-restrictions.html#cfn-codeartifact-packagegroup-restrictions-publish
            '''
            result = self._values.get("publish")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPackageGroupPropsMixin.RestrictionTypeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RestrictionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_codeartifact.mixins.CfnRepositoryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "domain_name": "domainName",
        "domain_owner": "domainOwner",
        "external_connections": "externalConnections",
        "permissions_policy_document": "permissionsPolicyDocument",
        "repository_name": "repositoryName",
        "tags": "tags",
        "upstreams": "upstreams",
    },
)
class CfnRepositoryMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_owner: typing.Optional[builtins.str] = None,
        external_connections: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions_policy_document: typing.Any = None,
        repository_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        upstreams: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnRepositoryPropsMixin.

        :param description: A text description of the repository.
        :param domain_name: The name of the domain that contains the repository.
        :param domain_owner: The 12-digit account number of the AWS account that owns the domain that contains the repository. It does not include dashes or spaces.
        :param external_connections: An array of external connections associated with the repository. For more information, see `Supported external connection repositories <https://docs.aws.amazon.com/codeartifact/latest/ug/external-connection.html#supported-public-repositories>`_ in the *CodeArtifact user guide* .
        :param permissions_policy_document: The document that defines the resource policy that is set on a repository.
        :param repository_name: The name of an upstream repository.
        :param tags: A list of tags to be applied to the repository.
        :param upstreams: A list of upstream repositories to associate with the repository. The order of the upstream repositories in the list determines their priority order when AWS CodeArtifact looks for a requested package version. For more information, see `Working with upstream repositories <https://docs.aws.amazon.com/codeartifact/latest/ug/repos-upstream.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codeartifact import mixins as codeartifact_mixins
            
            # permissions_policy_document: Any
            
            cfn_repository_mixin_props = codeartifact_mixins.CfnRepositoryMixinProps(
                description="description",
                domain_name="domainName",
                domain_owner="domainOwner",
                external_connections=["externalConnections"],
                permissions_policy_document=permissions_policy_document,
                repository_name="repositoryName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                upstreams=["upstreams"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46086d1d030a5fddfcc40fd6d5dde6f7c6bb641e572b5c0d33982129a9e23ec)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_owner", value=domain_owner, expected_type=type_hints["domain_owner"])
            check_type(argname="argument external_connections", value=external_connections, expected_type=type_hints["external_connections"])
            check_type(argname="argument permissions_policy_document", value=permissions_policy_document, expected_type=type_hints["permissions_policy_document"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument upstreams", value=upstreams, expected_type=type_hints["upstreams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_owner is not None:
            self._values["domain_owner"] = domain_owner
        if external_connections is not None:
            self._values["external_connections"] = external_connections
        if permissions_policy_document is not None:
            self._values["permissions_policy_document"] = permissions_policy_document
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if tags is not None:
            self._values["tags"] = tags
        if upstreams is not None:
            self._values["upstreams"] = upstreams

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A text description of the repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain that contains the repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_owner(self) -> typing.Optional[builtins.str]:
        '''The 12-digit account number of the AWS account that owns the domain that contains the repository.

        It does not include dashes or spaces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-domainowner
        '''
        result = self._values.get("domain_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_connections(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of external connections associated with the repository.

        For more information, see `Supported external connection repositories <https://docs.aws.amazon.com/codeartifact/latest/ug/external-connection.html#supported-public-repositories>`_ in the *CodeArtifact user guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-externalconnections
        '''
        result = self._values.get("external_connections")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permissions_policy_document(self) -> typing.Any:
        '''The document that defines the resource policy that is set on a repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-permissionspolicydocument
        '''
        result = self._values.get("permissions_policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''The name of an upstream repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-repositoryname
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to be applied to the repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def upstreams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of upstream repositories to associate with the repository.

        The order of the upstream repositories in the list determines their priority order when AWS CodeArtifact looks for a requested package version. For more information, see `Working with upstream repositories <https://docs.aws.amazon.com/codeartifact/latest/ug/repos-upstream.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#cfn-codeartifact-repository-upstreams
        '''
        result = self._values.get("upstreams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRepositoryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codeartifact.mixins.CfnRepositoryPropsMixin",
):
    '''The ``AWS::CodeArtifact::Repository`` resource creates an AWS CodeArtifact repository.

    CodeArtifact *repositories* contain a set of package versions. For more information about repositories, see the `Repository concepts information <https://docs.aws.amazon.com/codeartifact/latest/ug/codeartifact-concepts.html#welcome-concepts-repository>`_ in the *CodeArtifact User Guide* . For more information about the ``CreateRepository`` API, see `CreateRepository <https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_CreateRepository.html>`_ in the *CodeArtifact API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html
    :cloudformationResource: AWS::CodeArtifact::Repository
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codeartifact import mixins as codeartifact_mixins
        
        # permissions_policy_document: Any
        
        cfn_repository_props_mixin = codeartifact_mixins.CfnRepositoryPropsMixin(codeartifact_mixins.CfnRepositoryMixinProps(
            description="description",
            domain_name="domainName",
            domain_owner="domainOwner",
            external_connections=["externalConnections"],
            permissions_policy_document=permissions_policy_document,
            repository_name="repositoryName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            upstreams=["upstreams"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRepositoryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeArtifact::Repository``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a56199be1e0b3a15348eca96c9898cf55908320cc147e742200e7dd0468ec1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58592f4b89382701ae19885f7ef9f76e38558996481b4fe8419ef48f1b7e64c6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3fb865af45b9d2b8ef45cdec6d5f8d2fed52a6604306774cbfc60f8aae33ce)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRepositoryMixinProps:
        return typing.cast(CfnRepositoryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnDomainMixinProps",
    "CfnDomainPropsMixin",
    "CfnPackageGroupMixinProps",
    "CfnPackageGroupPropsMixin",
    "CfnRepositoryMixinProps",
    "CfnRepositoryPropsMixin",
]

publication.publish()

def _typecheckingstub__f7a10ad46ffe1f7dd909132b66a848d024303fe2d7f5cc16008610fc45fa0245(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    permissions_policy_document: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a9c8f7264c50c9fe8ede04828aedfa3b11d39f622fd3ac92d111252fd1c347(
    props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62f6891c30f4d2bd2ef1c7e9dddb7f5aecbf0b90bad72cdbadeab6f17e021f6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3a52360b83a85068c9964c79c7e8b9545e6309b7e768de5eb162edfbf866e3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c983703994b428a2fe5231cd4b76bbbe89838ba5101853629993e94d9f8cb1(
    *,
    contact_info: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_owner: typing.Optional[builtins.str] = None,
    origin_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackageGroupPropsMixin.OriginConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    pattern: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac33ed178b39338c5a2583cb84848d496543601e23b9a0e0c22599ff2afd1db2(
    props: typing.Union[CfnPackageGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f67c30c66eae89f80d01006acaff9ef9db7765c14ecadea926c53650b17d7c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72efa8c2a430b370d95d0bdff5de09d357935d2ae91f60d0c19e5ae5e8475550(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc0f891d1c5b986d68307ec5610e43a28f1b6d5de2508cbfe2361e0e24903a1(
    *,
    restrictions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackageGroupPropsMixin.RestrictionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f2a622bd3bcc5e60f18bc1e8c1f25cb6467f68711deae75ce9b5c9fead0e0c(
    *,
    repositories: typing.Optional[typing.Sequence[builtins.str]] = None,
    restriction_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a02008bb40ba5a546428c323627715875344c815b4cbde5878c6d31a6db58e(
    *,
    external_upstream: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackageGroupPropsMixin.RestrictionTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    internal_upstream: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackageGroupPropsMixin.RestrictionTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPackageGroupPropsMixin.RestrictionTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46086d1d030a5fddfcc40fd6d5dde6f7c6bb641e572b5c0d33982129a9e23ec(
    *,
    description: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_owner: typing.Optional[builtins.str] = None,
    external_connections: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions_policy_document: typing.Any = None,
    repository_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    upstreams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a56199be1e0b3a15348eca96c9898cf55908320cc147e742200e7dd0468ec1(
    props: typing.Union[CfnRepositoryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58592f4b89382701ae19885f7ef9f76e38558996481b4fe8419ef48f1b7e64c6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3fb865af45b9d2b8ef45cdec6d5f8d2fed52a6604306774cbfc60f8aae33ce(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
