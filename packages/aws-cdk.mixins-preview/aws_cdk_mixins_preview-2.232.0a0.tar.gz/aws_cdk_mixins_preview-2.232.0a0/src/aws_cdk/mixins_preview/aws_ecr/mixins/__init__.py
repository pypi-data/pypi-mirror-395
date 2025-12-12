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
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnPublicRepositoryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository_catalog_data": "repositoryCatalogData",
        "repository_name": "repositoryName",
        "repository_policy_text": "repositoryPolicyText",
        "tags": "tags",
    },
)
class CfnPublicRepositoryMixinProps:
    def __init__(
        self,
        *,
        repository_catalog_data: typing.Any = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPublicRepositoryPropsMixin.

        :param repository_catalog_data: The details about the repository that are publicly visible in the Amazon ECR Public Gallery. For more information, see `Amazon ECR Public repository catalog data <https://docs.aws.amazon.com/AmazonECR/latest/public/public-repository-catalog-data.html>`_ in the *Amazon ECR Public User Guide* .
        :param repository_name: The name to use for the public repository. The repository name may be specified on its own (such as ``nginx-web-app`` ) or it can be prepended with a namespace to group the repository into a category (such as ``project-a/nginx-web-app`` ). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the repository name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param repository_policy_text: The JSON repository policy text to apply to the public repository. For more information, see `Amazon ECR Public repository policies <https://docs.aws.amazon.com/AmazonECR/latest/public/public-repository-policies.html>`_ in the *Amazon ECR Public User Guide* .
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
            
            # repository_catalog_data: Any
            # repository_policy_text: Any
            
            cfn_public_repository_mixin_props = ecr_mixins.CfnPublicRepositoryMixinProps(
                repository_catalog_data=repository_catalog_data,
                repository_name="repositoryName",
                repository_policy_text=repository_policy_text,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffacb83d0acda1bba29391c93bd0646e1eba3a6185f8f5e1d50f8384342b09a3)
            check_type(argname="argument repository_catalog_data", value=repository_catalog_data, expected_type=type_hints["repository_catalog_data"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument repository_policy_text", value=repository_policy_text, expected_type=type_hints["repository_policy_text"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if repository_catalog_data is not None:
            self._values["repository_catalog_data"] = repository_catalog_data
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if repository_policy_text is not None:
            self._values["repository_policy_text"] = repository_policy_text
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def repository_catalog_data(self) -> typing.Any:
        '''The details about the repository that are publicly visible in the Amazon ECR Public Gallery.

        For more information, see `Amazon ECR Public repository catalog data <https://docs.aws.amazon.com/AmazonECR/latest/public/public-repository-catalog-data.html>`_ in the *Amazon ECR Public User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositorycatalogdata
        '''
        result = self._values.get("repository_catalog_data")
        return typing.cast(typing.Any, result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''The name to use for the public repository.

        The repository name may be specified on its own (such as ``nginx-web-app`` ) or it can be prepended with a namespace to group the repository into a category (such as ``project-a/nginx-web-app`` ). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the repository name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositoryname
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_policy_text(self) -> typing.Any:
        '''The JSON repository policy text to apply to the public repository.

        For more information, see `Amazon ECR Public repository policies <https://docs.aws.amazon.com/AmazonECR/latest/public/public-repository-policies.html>`_ in the *Amazon ECR Public User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositorypolicytext
        '''
        result = self._values.get("repository_policy_text")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublicRepositoryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPublicRepositoryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnPublicRepositoryPropsMixin",
):
    '''The ``AWS::ECR::PublicRepository`` resource specifies an Amazon Elastic Container Registry Public (Amazon ECR Public) repository, where users can push and pull Docker images, Open Container Initiative (OCI) images, and OCI compatible artifacts.

    For more information, see `Amazon ECR public repositories <https://docs.aws.amazon.com/AmazonECR/latest/public/public-repositories.html>`_ in the *Amazon ECR Public User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html
    :cloudformationResource: AWS::ECR::PublicRepository
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
        
        # repository_catalog_data: Any
        # repository_policy_text: Any
        
        cfn_public_repository_props_mixin = ecr_mixins.CfnPublicRepositoryPropsMixin(ecr_mixins.CfnPublicRepositoryMixinProps(
            repository_catalog_data=repository_catalog_data,
            repository_name="repositoryName",
            repository_policy_text=repository_policy_text,
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
        props: typing.Union[CfnPublicRepositoryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ECR::PublicRepository``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2b00f2d112387c0918d1863fd585ec57aba79fde04ccc20841714e2afdcfde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8de6f94ca247329d2c728174664632b43b700f0839d7ca908d764ba8b89ef14c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe509bb853d5a6b35679c3815b0be4a609716237d6a1192871abd1ffcb75a028)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPublicRepositoryMixinProps:
        return typing.cast(CfnPublicRepositoryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnPublicRepositoryPropsMixin.RepositoryCatalogDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "about_text": "aboutText",
            "architectures": "architectures",
            "operating_systems": "operatingSystems",
            "repository_description": "repositoryDescription",
            "usage_text": "usageText",
        },
    )
    class RepositoryCatalogDataProperty:
        def __init__(
            self,
            *,
            about_text: typing.Optional[builtins.str] = None,
            architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
            operating_systems: typing.Optional[typing.Sequence[builtins.str]] = None,
            repository_description: typing.Optional[builtins.str] = None,
            usage_text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details about the repository that are publicly visible in the Amazon ECR Public Gallery.

            For more information, see `Amazon ECR Public repository catalog data <https://docs.aws.amazon.com/AmazonECR/latest/public/public-repository-catalog-data.html>`_ in the *Amazon ECR Public User Guide* .

            :param about_text: The longform description of the contents of the repository. This text appears in the repository details on the Amazon ECR Public Gallery.
            :param architectures: The architecture tags that are associated with the repository.
            :param operating_systems: The operating system tags that are associated with the repository.
            :param repository_description: The short description of the repository.
            :param usage_text: The longform usage details of the contents of the repository. The usage text provides context for users of the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-publicrepository-repositorycatalogdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                repository_catalog_data_property = ecr_mixins.CfnPublicRepositoryPropsMixin.RepositoryCatalogDataProperty(
                    about_text="aboutText",
                    architectures=["architectures"],
                    operating_systems=["operatingSystems"],
                    repository_description="repositoryDescription",
                    usage_text="usageText"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ca1f909e33540543c9dfb8f13d2d5ef17251134ef9cfcae97c427e48cc18667)
                check_type(argname="argument about_text", value=about_text, expected_type=type_hints["about_text"])
                check_type(argname="argument architectures", value=architectures, expected_type=type_hints["architectures"])
                check_type(argname="argument operating_systems", value=operating_systems, expected_type=type_hints["operating_systems"])
                check_type(argname="argument repository_description", value=repository_description, expected_type=type_hints["repository_description"])
                check_type(argname="argument usage_text", value=usage_text, expected_type=type_hints["usage_text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if about_text is not None:
                self._values["about_text"] = about_text
            if architectures is not None:
                self._values["architectures"] = architectures
            if operating_systems is not None:
                self._values["operating_systems"] = operating_systems
            if repository_description is not None:
                self._values["repository_description"] = repository_description
            if usage_text is not None:
                self._values["usage_text"] = usage_text

        @builtins.property
        def about_text(self) -> typing.Optional[builtins.str]:
            '''The longform description of the contents of the repository.

            This text appears in the repository details on the Amazon ECR Public Gallery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-publicrepository-repositorycatalogdata.html#cfn-ecr-publicrepository-repositorycatalogdata-abouttext
            '''
            result = self._values.get("about_text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def architectures(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The architecture tags that are associated with the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-publicrepository-repositorycatalogdata.html#cfn-ecr-publicrepository-repositorycatalogdata-architectures
            '''
            result = self._values.get("architectures")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def operating_systems(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The operating system tags that are associated with the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-publicrepository-repositorycatalogdata.html#cfn-ecr-publicrepository-repositorycatalogdata-operatingsystems
            '''
            result = self._values.get("operating_systems")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def repository_description(self) -> typing.Optional[builtins.str]:
            '''The short description of the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-publicrepository-repositorycatalogdata.html#cfn-ecr-publicrepository-repositorycatalogdata-repositorydescription
            '''
            result = self._values.get("repository_description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def usage_text(self) -> typing.Optional[builtins.str]:
            '''The longform usage details of the contents of the repository.

            The usage text provides context for users of the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-publicrepository-repositorycatalogdata.html#cfn-ecr-publicrepository-repositorycatalogdata-usagetext
            '''
            result = self._values.get("usage_text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RepositoryCatalogDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnPullThroughCacheRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "credential_arn": "credentialArn",
        "custom_role_arn": "customRoleArn",
        "ecr_repository_prefix": "ecrRepositoryPrefix",
        "upstream_registry": "upstreamRegistry",
        "upstream_registry_url": "upstreamRegistryUrl",
        "upstream_repository_prefix": "upstreamRepositoryPrefix",
    },
)
class CfnPullThroughCacheRuleMixinProps:
    def __init__(
        self,
        *,
        credential_arn: typing.Optional[builtins.str] = None,
        custom_role_arn: typing.Optional[builtins.str] = None,
        ecr_repository_prefix: typing.Optional[builtins.str] = None,
        upstream_registry: typing.Optional[builtins.str] = None,
        upstream_registry_url: typing.Optional[builtins.str] = None,
        upstream_repository_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPullThroughCacheRulePropsMixin.

        :param credential_arn: The ARN of the Secrets Manager secret associated with the pull through cache rule.
        :param custom_role_arn: The ARN of the IAM role associated with the pull through cache rule.
        :param ecr_repository_prefix: The Amazon ECR repository prefix associated with the pull through cache rule.
        :param upstream_registry: The name of the upstream source registry associated with the pull through cache rule.
        :param upstream_registry_url: The upstream registry URL associated with the pull through cache rule.
        :param upstream_repository_prefix: The upstream repository prefix associated with the pull through cache rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pullthroughcacherule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
            
            cfn_pull_through_cache_rule_mixin_props = ecr_mixins.CfnPullThroughCacheRuleMixinProps(
                credential_arn="credentialArn",
                custom_role_arn="customRoleArn",
                ecr_repository_prefix="ecrRepositoryPrefix",
                upstream_registry="upstreamRegistry",
                upstream_registry_url="upstreamRegistryUrl",
                upstream_repository_prefix="upstreamRepositoryPrefix"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c464cee78a158e4b16f37f9f163b51a2b0be23800ad26b5a07ba1848de4a09)
            check_type(argname="argument credential_arn", value=credential_arn, expected_type=type_hints["credential_arn"])
            check_type(argname="argument custom_role_arn", value=custom_role_arn, expected_type=type_hints["custom_role_arn"])
            check_type(argname="argument ecr_repository_prefix", value=ecr_repository_prefix, expected_type=type_hints["ecr_repository_prefix"])
            check_type(argname="argument upstream_registry", value=upstream_registry, expected_type=type_hints["upstream_registry"])
            check_type(argname="argument upstream_registry_url", value=upstream_registry_url, expected_type=type_hints["upstream_registry_url"])
            check_type(argname="argument upstream_repository_prefix", value=upstream_repository_prefix, expected_type=type_hints["upstream_repository_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if credential_arn is not None:
            self._values["credential_arn"] = credential_arn
        if custom_role_arn is not None:
            self._values["custom_role_arn"] = custom_role_arn
        if ecr_repository_prefix is not None:
            self._values["ecr_repository_prefix"] = ecr_repository_prefix
        if upstream_registry is not None:
            self._values["upstream_registry"] = upstream_registry
        if upstream_registry_url is not None:
            self._values["upstream_registry_url"] = upstream_registry_url
        if upstream_repository_prefix is not None:
            self._values["upstream_repository_prefix"] = upstream_repository_prefix

    @builtins.property
    def credential_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the Secrets Manager secret associated with the pull through cache rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pullthroughcacherule.html#cfn-ecr-pullthroughcacherule-credentialarn
        '''
        result = self._values.get("credential_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role associated with the pull through cache rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pullthroughcacherule.html#cfn-ecr-pullthroughcacherule-customrolearn
        '''
        result = self._values.get("custom_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecr_repository_prefix(self) -> typing.Optional[builtins.str]:
        '''The Amazon ECR repository prefix associated with the pull through cache rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pullthroughcacherule.html#cfn-ecr-pullthroughcacherule-ecrrepositoryprefix
        '''
        result = self._values.get("ecr_repository_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upstream_registry(self) -> typing.Optional[builtins.str]:
        '''The name of the upstream source registry associated with the pull through cache rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pullthroughcacherule.html#cfn-ecr-pullthroughcacherule-upstreamregistry
        '''
        result = self._values.get("upstream_registry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upstream_registry_url(self) -> typing.Optional[builtins.str]:
        '''The upstream registry URL associated with the pull through cache rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pullthroughcacherule.html#cfn-ecr-pullthroughcacherule-upstreamregistryurl
        '''
        result = self._values.get("upstream_registry_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upstream_repository_prefix(self) -> typing.Optional[builtins.str]:
        '''The upstream repository prefix associated with the pull through cache rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pullthroughcacherule.html#cfn-ecr-pullthroughcacherule-upstreamrepositoryprefix
        '''
        result = self._values.get("upstream_repository_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPullThroughCacheRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPullThroughCacheRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnPullThroughCacheRulePropsMixin",
):
    '''The ``AWS::ECR::PullThroughCacheRule`` resource creates or updates a pull through cache rule.

    A pull through cache rule provides a way to cache images from an upstream registry in your Amazon ECR private registry.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pullthroughcacherule.html
    :cloudformationResource: AWS::ECR::PullThroughCacheRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
        
        cfn_pull_through_cache_rule_props_mixin = ecr_mixins.CfnPullThroughCacheRulePropsMixin(ecr_mixins.CfnPullThroughCacheRuleMixinProps(
            credential_arn="credentialArn",
            custom_role_arn="customRoleArn",
            ecr_repository_prefix="ecrRepositoryPrefix",
            upstream_registry="upstreamRegistry",
            upstream_registry_url="upstreamRegistryUrl",
            upstream_repository_prefix="upstreamRepositoryPrefix"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPullThroughCacheRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ECR::PullThroughCacheRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa4c0acd628f2eddc585f005888cc30b0c33b0e3951f44995a59586ba19dee6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58b1f3b5927d430b77a441e8e6e19d82cac3bfa6c3f42bacc9b04f1840c83979)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861de03a47b669f508a869e054c1e18c02196c4a0cccd07157c49c5058f32a36)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPullThroughCacheRuleMixinProps:
        return typing.cast(CfnPullThroughCacheRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnPullTimeUpdateExclusionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"principal_arn": "principalArn"},
)
class CfnPullTimeUpdateExclusionMixinProps:
    def __init__(self, *, principal_arn: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnPullTimeUpdateExclusionPropsMixin.

        :param principal_arn: The ARN of the IAM principal to remove from the pull time update exclusion list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pulltimeupdateexclusion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
            
            cfn_pull_time_update_exclusion_mixin_props = ecr_mixins.CfnPullTimeUpdateExclusionMixinProps(
                principal_arn="principalArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11ec6c3387fe7dd96b43777ed1c68bcc96a3284e7020c79bb89546275763fac)
            check_type(argname="argument principal_arn", value=principal_arn, expected_type=type_hints["principal_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if principal_arn is not None:
            self._values["principal_arn"] = principal_arn

    @builtins.property
    def principal_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM principal to remove from the pull time update exclusion list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pulltimeupdateexclusion.html#cfn-ecr-pulltimeupdateexclusion-principalarn
        '''
        result = self._values.get("principal_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPullTimeUpdateExclusionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPullTimeUpdateExclusionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnPullTimeUpdateExclusionPropsMixin",
):
    '''Resource Type definition for AWS::ECR::PullTimeUpdateExclusion controls the exclusion configuration for ecr image pull time update.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-pulltimeupdateexclusion.html
    :cloudformationResource: AWS::ECR::PullTimeUpdateExclusion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
        
        cfn_pull_time_update_exclusion_props_mixin = ecr_mixins.CfnPullTimeUpdateExclusionPropsMixin(ecr_mixins.CfnPullTimeUpdateExclusionMixinProps(
            principal_arn="principalArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPullTimeUpdateExclusionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ECR::PullTimeUpdateExclusion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab20b42b899b6090c8259aa3b141595c1bac402c80a8218e4653edc63ba05971)
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
            type_hints = typing.get_type_hints(_typecheckingstub__058c997b8d2da73a8508a33d022e52513ad81783cf5b2876f5da16c1aa997019)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8604572b7b95331adc3f02536dd5243d019ed69b9a82184c4a0f20cd78cfd5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPullTimeUpdateExclusionMixinProps:
        return typing.cast(CfnPullTimeUpdateExclusionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRegistryPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy_text": "policyText"},
)
class CfnRegistryPolicyMixinProps:
    def __init__(self, *, policy_text: typing.Any = None) -> None:
        '''Properties for CfnRegistryPolicyPropsMixin.

        :param policy_text: The JSON policy text for your registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registrypolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
            
            # policy_text: Any
            
            cfn_registry_policy_mixin_props = ecr_mixins.CfnRegistryPolicyMixinProps(
                policy_text=policy_text
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4344da9628ff4dcab8738ebe732f0589bd7d5f7b590b186f2d7820ca888bcb)
            check_type(argname="argument policy_text", value=policy_text, expected_type=type_hints["policy_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_text is not None:
            self._values["policy_text"] = policy_text

    @builtins.property
    def policy_text(self) -> typing.Any:
        '''The JSON policy text for your registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registrypolicy.html#cfn-ecr-registrypolicy-policytext
        '''
        result = self._values.get("policy_text")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegistryPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRegistryPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRegistryPolicyPropsMixin",
):
    '''The ``AWS::ECR::RegistryPolicy`` resource creates or updates the permissions policy for a private registry.

    A private registry policy is used to specify permissions for another AWS account and is used when configuring cross-account replication. For more information, see `Registry permissions <https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry-permissions.html>`_ in the *Amazon Elastic Container Registry User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registrypolicy.html
    :cloudformationResource: AWS::ECR::RegistryPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
        
        # policy_text: Any
        
        cfn_registry_policy_props_mixin = ecr_mixins.CfnRegistryPolicyPropsMixin(ecr_mixins.CfnRegistryPolicyMixinProps(
            policy_text=policy_text
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRegistryPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ECR::RegistryPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0bed870fd5e7e5f5b1e0d40749e47166fcd11037a6df1daa2b9fd3c655f8f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__824dd89b74c5b8372bfd7ab292a93d51ff9a0760f6f8fbb82ecf03670d6a7d9f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e6aa763d6920932be8882a98405c610bb81ddcd60b12a4487c910f6bc00494)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRegistryPolicyMixinProps:
        return typing.cast(CfnRegistryPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRegistryScanningConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules", "scan_type": "scanType"},
)
class CfnRegistryScanningConfigurationMixinProps:
    def __init__(
        self,
        *,
        rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRegistryScanningConfigurationPropsMixin.ScanningRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        scan_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRegistryScanningConfigurationPropsMixin.

        :param rules: The scanning rules associated with the registry.
        :param scan_type: The type of scanning configured for the registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registryscanningconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
            
            cfn_registry_scanning_configuration_mixin_props = ecr_mixins.CfnRegistryScanningConfigurationMixinProps(
                rules=[ecr_mixins.CfnRegistryScanningConfigurationPropsMixin.ScanningRuleProperty(
                    repository_filters=[ecr_mixins.CfnRegistryScanningConfigurationPropsMixin.RepositoryFilterProperty(
                        filter="filter",
                        filter_type="filterType"
                    )],
                    scan_frequency="scanFrequency"
                )],
                scan_type="scanType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22e4f481bd52b97375688aca48ceebee2b4d5b403074e4510b066c559744a55)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument scan_type", value=scan_type, expected_type=type_hints["scan_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rules is not None:
            self._values["rules"] = rules
        if scan_type is not None:
            self._values["scan_type"] = scan_type

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRegistryScanningConfigurationPropsMixin.ScanningRuleProperty"]]]]:
        '''The scanning rules associated with the registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registryscanningconfiguration.html#cfn-ecr-registryscanningconfiguration-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRegistryScanningConfigurationPropsMixin.ScanningRuleProperty"]]]], result)

    @builtins.property
    def scan_type(self) -> typing.Optional[builtins.str]:
        '''The type of scanning configured for the registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registryscanningconfiguration.html#cfn-ecr-registryscanningconfiguration-scantype
        '''
        result = self._values.get("scan_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegistryScanningConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRegistryScanningConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRegistryScanningConfigurationPropsMixin",
):
    '''The scanning configuration for a private registry.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registryscanningconfiguration.html
    :cloudformationResource: AWS::ECR::RegistryScanningConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
        
        cfn_registry_scanning_configuration_props_mixin = ecr_mixins.CfnRegistryScanningConfigurationPropsMixin(ecr_mixins.CfnRegistryScanningConfigurationMixinProps(
            rules=[ecr_mixins.CfnRegistryScanningConfigurationPropsMixin.ScanningRuleProperty(
                repository_filters=[ecr_mixins.CfnRegistryScanningConfigurationPropsMixin.RepositoryFilterProperty(
                    filter="filter",
                    filter_type="filterType"
                )],
                scan_frequency="scanFrequency"
            )],
            scan_type="scanType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRegistryScanningConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ECR::RegistryScanningConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247ad09029000475a9a342247388ded4311bbb748c1f7e8144b7aed8860bf072)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad2cc609bf29b1adbbb0e8246b3d8a709849d8fc9be4b61f7a0060aa96bdca1d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf4f7f120c19a1b114a61a9099f0f6dfdeec9d6119cf328b62f0c16df0cef71)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRegistryScanningConfigurationMixinProps:
        return typing.cast(CfnRegistryScanningConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRegistryScanningConfigurationPropsMixin.RepositoryFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"filter": "filter", "filter_type": "filterType"},
    )
    class RepositoryFilterProperty:
        def __init__(
            self,
            *,
            filter: typing.Optional[builtins.str] = None,
            filter_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The filter settings used with image replication.

            Specifying a repository filter to a replication rule provides a method for controlling which repositories in a private registry are replicated. If no filters are added, the contents of all repositories are replicated.

            :param filter: The filter to use when scanning.
            :param filter_type: The type associated with the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-registryscanningconfiguration-repositoryfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                repository_filter_property = ecr_mixins.CfnRegistryScanningConfigurationPropsMixin.RepositoryFilterProperty(
                    filter="filter",
                    filter_type="filterType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c214f0bed1a5abb359c8d8c51ca5eb96239cc2546b4780c073fe2dbf3545786)
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter is not None:
                self._values["filter"] = filter
            if filter_type is not None:
                self._values["filter_type"] = filter_type

        @builtins.property
        def filter(self) -> typing.Optional[builtins.str]:
            '''The filter to use when scanning.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-registryscanningconfiguration-repositoryfilter.html#cfn-ecr-registryscanningconfiguration-repositoryfilter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            '''The type associated with the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-registryscanningconfiguration-repositoryfilter.html#cfn-ecr-registryscanningconfiguration-repositoryfilter-filtertype
            '''
            result = self._values.get("filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RepositoryFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRegistryScanningConfigurationPropsMixin.ScanningRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "repository_filters": "repositoryFilters",
            "scan_frequency": "scanFrequency",
        },
    )
    class ScanningRuleProperty:
        def __init__(
            self,
            *,
            repository_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRegistryScanningConfigurationPropsMixin.RepositoryFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            scan_frequency: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The scanning rules associated with the registry.

            :param repository_filters: The details of a scanning repository filter. For more information on how to use filters, see `Using filters <https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html#image-scanning-filters>`_ in the *Amazon Elastic Container Registry User Guide* .
            :param scan_frequency: The frequency that scans are performed at for a private registry. When the ``ENHANCED`` scan type is specified, the supported scan frequencies are ``CONTINUOUS_SCAN`` and ``SCAN_ON_PUSH`` . When the ``BASIC`` scan type is specified, the ``SCAN_ON_PUSH`` scan frequency is supported. If scan on push is not specified, then the ``MANUAL`` scan frequency is set by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-registryscanningconfiguration-scanningrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                scanning_rule_property = ecr_mixins.CfnRegistryScanningConfigurationPropsMixin.ScanningRuleProperty(
                    repository_filters=[ecr_mixins.CfnRegistryScanningConfigurationPropsMixin.RepositoryFilterProperty(
                        filter="filter",
                        filter_type="filterType"
                    )],
                    scan_frequency="scanFrequency"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4bd4e276c2eb6ac2ac6ca100623f518e4fcc0240a49b797ffb977236f71aa792)
                check_type(argname="argument repository_filters", value=repository_filters, expected_type=type_hints["repository_filters"])
                check_type(argname="argument scan_frequency", value=scan_frequency, expected_type=type_hints["scan_frequency"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if repository_filters is not None:
                self._values["repository_filters"] = repository_filters
            if scan_frequency is not None:
                self._values["scan_frequency"] = scan_frequency

        @builtins.property
        def repository_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRegistryScanningConfigurationPropsMixin.RepositoryFilterProperty"]]]]:
            '''The details of a scanning repository filter.

            For more information on how to use filters, see `Using filters <https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html#image-scanning-filters>`_ in the *Amazon Elastic Container Registry User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-registryscanningconfiguration-scanningrule.html#cfn-ecr-registryscanningconfiguration-scanningrule-repositoryfilters
            '''
            result = self._values.get("repository_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRegistryScanningConfigurationPropsMixin.RepositoryFilterProperty"]]]], result)

        @builtins.property
        def scan_frequency(self) -> typing.Optional[builtins.str]:
            '''The frequency that scans are performed at for a private registry.

            When the ``ENHANCED`` scan type is specified, the supported scan frequencies are ``CONTINUOUS_SCAN`` and ``SCAN_ON_PUSH`` . When the ``BASIC`` scan type is specified, the ``SCAN_ON_PUSH`` scan frequency is supported. If scan on push is not specified, then the ``MANUAL`` scan frequency is set by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-registryscanningconfiguration-scanningrule.html#cfn-ecr-registryscanningconfiguration-scanningrule-scanfrequency
            '''
            result = self._values.get("scan_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScanningRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnReplicationConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"replication_configuration": "replicationConfiguration"},
)
class CfnReplicationConfigurationMixinProps:
    def __init__(
        self,
        *,
        replication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationConfigurationPropsMixin.ReplicationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnReplicationConfigurationPropsMixin.

        :param replication_configuration: The replication configuration for a registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-replicationconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
            
            cfn_replication_configuration_mixin_props = ecr_mixins.CfnReplicationConfigurationMixinProps(
                replication_configuration=ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationConfigurationProperty(
                    rules=[ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationRuleProperty(
                        destinations=[ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationDestinationProperty(
                            region="region",
                            registry_id="registryId"
                        )],
                        repository_filters=[ecr_mixins.CfnReplicationConfigurationPropsMixin.RepositoryFilterProperty(
                            filter="filter",
                            filter_type="filterType"
                        )]
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c1ebb5487536ce9b51661e19d1577be2c54672ae3ee6f7f9fd2d9ed5979e1e)
            check_type(argname="argument replication_configuration", value=replication_configuration, expected_type=type_hints["replication_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if replication_configuration is not None:
            self._values["replication_configuration"] = replication_configuration

    @builtins.property
    def replication_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationConfigurationPropsMixin.ReplicationConfigurationProperty"]]:
        '''The replication configuration for a registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-replicationconfiguration.html#cfn-ecr-replicationconfiguration-replicationconfiguration
        '''
        result = self._values.get("replication_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationConfigurationPropsMixin.ReplicationConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReplicationConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnReplicationConfigurationPropsMixin",
):
    '''The ``AWS::ECR::ReplicationConfiguration`` resource creates or updates the replication configuration for a private registry.

    The first time a replication configuration is applied to a private registry, a service-linked IAM role is created in your account for the replication process. For more information, see `Using Service-Linked Roles for Amazon ECR <https://docs.aws.amazon.com/AmazonECR/latest/userguide/using-service-linked-roles.html>`_ in the *Amazon Elastic Container Registry User Guide* .
    .. epigraph::

       When configuring cross-account replication, the destination account must grant the source account permission to replicate. This permission is controlled using a private registry permissions policy. For more information, see ``AWS::ECR::RegistryPolicy`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-replicationconfiguration.html
    :cloudformationResource: AWS::ECR::ReplicationConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
        
        cfn_replication_configuration_props_mixin = ecr_mixins.CfnReplicationConfigurationPropsMixin(ecr_mixins.CfnReplicationConfigurationMixinProps(
            replication_configuration=ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationConfigurationProperty(
                rules=[ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationRuleProperty(
                    destinations=[ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationDestinationProperty(
                        region="region",
                        registry_id="registryId"
                    )],
                    repository_filters=[ecr_mixins.CfnReplicationConfigurationPropsMixin.RepositoryFilterProperty(
                        filter="filter",
                        filter_type="filterType"
                    )]
                )]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReplicationConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ECR::ReplicationConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd716eb0f9c76f9a8c3a444813be386c2839c957bb7c8874ada7263d7e817add)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ef33c290e021978da25f07172b798002d52dcd0c1f9c57e9ebbb8c7fac5338d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648de56b1c799d329ac779d4aef0bc2b74a3536f571b2fea23715a1418028143)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReplicationConfigurationMixinProps:
        return typing.cast(CfnReplicationConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnReplicationConfigurationPropsMixin.ReplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class ReplicationConfigurationProperty:
        def __init__(
            self,
            *,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationConfigurationPropsMixin.ReplicationRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The replication configuration for a registry.

            :param rules: An array of objects representing the replication destinations and repository filters for a replication configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                replication_configuration_property = ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationConfigurationProperty(
                    rules=[ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationRuleProperty(
                        destinations=[ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationDestinationProperty(
                            region="region",
                            registry_id="registryId"
                        )],
                        repository_filters=[ecr_mixins.CfnReplicationConfigurationPropsMixin.RepositoryFilterProperty(
                            filter="filter",
                            filter_type="filterType"
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7abd43cdef6dc5071e545f87ba0f44d8036f11d4ebf387c760bb09347bc68fc7)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationConfigurationPropsMixin.ReplicationRuleProperty"]]]]:
            '''An array of objects representing the replication destinations and repository filters for a replication configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationconfiguration.html#cfn-ecr-replicationconfiguration-replicationconfiguration-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationConfigurationPropsMixin.ReplicationRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnReplicationConfigurationPropsMixin.ReplicationDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"region": "region", "registry_id": "registryId"},
    )
    class ReplicationDestinationProperty:
        def __init__(
            self,
            *,
            region: typing.Optional[builtins.str] = None,
            registry_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An array of objects representing the destination for a replication rule.

            :param region: The Region to replicate to.
            :param registry_id: The AWS account ID of the Amazon ECR private registry to replicate to. When configuring cross-Region replication within your own registry, specify your own account ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                replication_destination_property = ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationDestinationProperty(
                    region="region",
                    registry_id="registryId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7be4d0b94d38dc90de26d581c0f60fd996f6dfeddf3f9e213745d4efe9560ffc)
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument registry_id", value=registry_id, expected_type=type_hints["registry_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if region is not None:
                self._values["region"] = region
            if registry_id is not None:
                self._values["registry_id"] = registry_id

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The Region to replicate to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationdestination.html#cfn-ecr-replicationconfiguration-replicationdestination-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def registry_id(self) -> typing.Optional[builtins.str]:
            '''The AWS account ID of the Amazon ECR private registry to replicate to.

            When configuring cross-Region replication within your own registry, specify your own account ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationdestination.html#cfn-ecr-replicationconfiguration-replicationdestination-registryid
            '''
            result = self._values.get("registry_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnReplicationConfigurationPropsMixin.ReplicationRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destinations": "destinations",
            "repository_filters": "repositoryFilters",
        },
    )
    class ReplicationRuleProperty:
        def __init__(
            self,
            *,
            destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationConfigurationPropsMixin.ReplicationDestinationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            repository_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationConfigurationPropsMixin.RepositoryFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An array of objects representing the replication destinations and repository filters for a replication configuration.

            :param destinations: An array of objects representing the destination for a replication rule.
            :param repository_filters: An array of objects representing the filters for a replication rule. Specifying a repository filter for a replication rule provides a method for controlling which repositories in a private registry are replicated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                replication_rule_property = ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationRuleProperty(
                    destinations=[ecr_mixins.CfnReplicationConfigurationPropsMixin.ReplicationDestinationProperty(
                        region="region",
                        registry_id="registryId"
                    )],
                    repository_filters=[ecr_mixins.CfnReplicationConfigurationPropsMixin.RepositoryFilterProperty(
                        filter="filter",
                        filter_type="filterType"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18255465bbe2f32bcc905097ed1027a4f95b608e099ac3627105cae802ee0f54)
                check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
                check_type(argname="argument repository_filters", value=repository_filters, expected_type=type_hints["repository_filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destinations is not None:
                self._values["destinations"] = destinations
            if repository_filters is not None:
                self._values["repository_filters"] = repository_filters

        @builtins.property
        def destinations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationConfigurationPropsMixin.ReplicationDestinationProperty"]]]]:
            '''An array of objects representing the destination for a replication rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationrule.html#cfn-ecr-replicationconfiguration-replicationrule-destinations
            '''
            result = self._values.get("destinations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationConfigurationPropsMixin.ReplicationDestinationProperty"]]]], result)

        @builtins.property
        def repository_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationConfigurationPropsMixin.RepositoryFilterProperty"]]]]:
            '''An array of objects representing the filters for a replication rule.

            Specifying a repository filter for a replication rule provides a method for controlling which repositories in a private registry are replicated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationrule.html#cfn-ecr-replicationconfiguration-replicationrule-repositoryfilters
            '''
            result = self._values.get("repository_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationConfigurationPropsMixin.RepositoryFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnReplicationConfigurationPropsMixin.RepositoryFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"filter": "filter", "filter_type": "filterType"},
    )
    class RepositoryFilterProperty:
        def __init__(
            self,
            *,
            filter: typing.Optional[builtins.str] = None,
            filter_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The filter settings used with image replication.

            Specifying a repository filter to a replication rule provides a method for controlling which repositories in a private registry are replicated. If no filters are added, the contents of all repositories are replicated.

            :param filter: The repository filter details. When the ``PREFIX_MATCH`` filter type is specified, this value is required and should be the repository name prefix to configure replication for.
            :param filter_type: The repository filter type. The only supported value is ``PREFIX_MATCH`` , which is a repository name prefix specified with the ``filter`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-repositoryfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                repository_filter_property = ecr_mixins.CfnReplicationConfigurationPropsMixin.RepositoryFilterProperty(
                    filter="filter",
                    filter_type="filterType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbc9e1d9cb1c97c2a81b8cc1efc39146d5bcbc2864ba409276b218554729e47b)
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter is not None:
                self._values["filter"] = filter
            if filter_type is not None:
                self._values["filter_type"] = filter_type

        @builtins.property
        def filter(self) -> typing.Optional[builtins.str]:
            '''The repository filter details.

            When the ``PREFIX_MATCH`` filter type is specified, this value is required and should be the repository name prefix to configure replication for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-repositoryfilter.html#cfn-ecr-replicationconfiguration-repositoryfilter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            '''The repository filter type.

            The only supported value is ``PREFIX_MATCH`` , which is a repository name prefix specified with the ``filter`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-repositoryfilter.html#cfn-ecr-replicationconfiguration-repositoryfilter-filtertype
            '''
            result = self._values.get("filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RepositoryFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRepositoryCreationTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "applied_for": "appliedFor",
        "custom_role_arn": "customRoleArn",
        "description": "description",
        "encryption_configuration": "encryptionConfiguration",
        "image_tag_mutability": "imageTagMutability",
        "image_tag_mutability_exclusion_filters": "imageTagMutabilityExclusionFilters",
        "lifecycle_policy": "lifecyclePolicy",
        "prefix": "prefix",
        "repository_policy": "repositoryPolicy",
        "resource_tags": "resourceTags",
    },
)
class CfnRepositoryCreationTemplateMixinProps:
    def __init__(
        self,
        *,
        applied_for: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_role_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRepositoryCreationTemplatePropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        image_tag_mutability: typing.Optional[builtins.str] = None,
        image_tag_mutability_exclusion_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRepositoryCreationTemplatePropsMixin.ImageTagMutabilityExclusionFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        lifecycle_policy: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        repository_policy: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnRepositoryCreationTemplatePropsMixin.

        :param applied_for: A list of enumerable Strings representing the repository creation scenarios that this template will apply towards. The two supported scenarios are PULL_THROUGH_CACHE and REPLICATION
        :param custom_role_arn: The ARN of the role to be assumed by Amazon ECR. Amazon ECR will assume your supplied role when the customRoleArn is specified. When this field isn't specified, Amazon ECR will use the service-linked role for the repository creation template.
        :param description: The description associated with the repository creation template.
        :param encryption_configuration: The encryption configuration associated with the repository creation template.
        :param image_tag_mutability: The tag mutability setting for the repository. If this parameter is omitted, the default setting of ``MUTABLE`` will be used which will allow image tags to be overwritten. If ``IMMUTABLE`` is specified, all image tags within the repository will be immutable which will prevent them from being overwritten.
        :param image_tag_mutability_exclusion_filters: A list of filters that specify which image tags are excluded from the repository creation template's image tag mutability setting.
        :param lifecycle_policy: The lifecycle policy to use for repositories created using the template.
        :param prefix: The repository namespace prefix associated with the repository creation template.
        :param repository_policy: The repository policy to apply to repositories created using the template. A repository policy is a permissions policy associated with a repository to control access permissions.
        :param resource_tags: The metadata to apply to the repository to help you categorize and organize. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
            
            cfn_repository_creation_template_mixin_props = ecr_mixins.CfnRepositoryCreationTemplateMixinProps(
                applied_for=["appliedFor"],
                custom_role_arn="customRoleArn",
                description="description",
                encryption_configuration=ecr_mixins.CfnRepositoryCreationTemplatePropsMixin.EncryptionConfigurationProperty(
                    encryption_type="encryptionType",
                    kms_key="kmsKey"
                ),
                image_tag_mutability="imageTagMutability",
                image_tag_mutability_exclusion_filters=[ecr_mixins.CfnRepositoryCreationTemplatePropsMixin.ImageTagMutabilityExclusionFilterProperty(
                    image_tag_mutability_exclusion_filter_type="imageTagMutabilityExclusionFilterType",
                    image_tag_mutability_exclusion_filter_value="imageTagMutabilityExclusionFilterValue"
                )],
                lifecycle_policy="lifecyclePolicy",
                prefix="prefix",
                repository_policy="repositoryPolicy",
                resource_tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca89f92d3b4ec27098a54f4c2ed6943de2a363d24f2e926d58e26ef9fdeed761)
            check_type(argname="argument applied_for", value=applied_for, expected_type=type_hints["applied_for"])
            check_type(argname="argument custom_role_arn", value=custom_role_arn, expected_type=type_hints["custom_role_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument image_tag_mutability", value=image_tag_mutability, expected_type=type_hints["image_tag_mutability"])
            check_type(argname="argument image_tag_mutability_exclusion_filters", value=image_tag_mutability_exclusion_filters, expected_type=type_hints["image_tag_mutability_exclusion_filters"])
            check_type(argname="argument lifecycle_policy", value=lifecycle_policy, expected_type=type_hints["lifecycle_policy"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument repository_policy", value=repository_policy, expected_type=type_hints["repository_policy"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if applied_for is not None:
            self._values["applied_for"] = applied_for
        if custom_role_arn is not None:
            self._values["custom_role_arn"] = custom_role_arn
        if description is not None:
            self._values["description"] = description
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if image_tag_mutability is not None:
            self._values["image_tag_mutability"] = image_tag_mutability
        if image_tag_mutability_exclusion_filters is not None:
            self._values["image_tag_mutability_exclusion_filters"] = image_tag_mutability_exclusion_filters
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if prefix is not None:
            self._values["prefix"] = prefix
        if repository_policy is not None:
            self._values["repository_policy"] = repository_policy
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags

    @builtins.property
    def applied_for(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of enumerable Strings representing the repository creation scenarios that this template will apply towards.

        The two supported scenarios are PULL_THROUGH_CACHE and REPLICATION

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html#cfn-ecr-repositorycreationtemplate-appliedfor
        '''
        result = self._values.get("applied_for")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the role to be assumed by Amazon ECR.

        Amazon ECR will assume your supplied role when the customRoleArn is specified. When this field isn't specified, Amazon ECR will use the service-linked role for the repository creation template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html#cfn-ecr-repositorycreationtemplate-customrolearn
        '''
        result = self._values.get("custom_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description associated with the repository creation template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html#cfn-ecr-repositorycreationtemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryCreationTemplatePropsMixin.EncryptionConfigurationProperty"]]:
        '''The encryption configuration associated with the repository creation template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html#cfn-ecr-repositorycreationtemplate-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryCreationTemplatePropsMixin.EncryptionConfigurationProperty"]], result)

    @builtins.property
    def image_tag_mutability(self) -> typing.Optional[builtins.str]:
        '''The tag mutability setting for the repository.

        If this parameter is omitted, the default setting of ``MUTABLE`` will be used which will allow image tags to be overwritten. If ``IMMUTABLE`` is specified, all image tags within the repository will be immutable which will prevent them from being overwritten.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html#cfn-ecr-repositorycreationtemplate-imagetagmutability
        '''
        result = self._values.get("image_tag_mutability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag_mutability_exclusion_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryCreationTemplatePropsMixin.ImageTagMutabilityExclusionFilterProperty"]]]]:
        '''A list of filters that specify which image tags are excluded from the repository creation template's image tag mutability setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html#cfn-ecr-repositorycreationtemplate-imagetagmutabilityexclusionfilters
        '''
        result = self._values.get("image_tag_mutability_exclusion_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryCreationTemplatePropsMixin.ImageTagMutabilityExclusionFilterProperty"]]]], result)

    @builtins.property
    def lifecycle_policy(self) -> typing.Optional[builtins.str]:
        '''The lifecycle policy to use for repositories created using the template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html#cfn-ecr-repositorycreationtemplate-lifecyclepolicy
        '''
        result = self._values.get("lifecycle_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The repository namespace prefix associated with the repository creation template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html#cfn-ecr-repositorycreationtemplate-prefix
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_policy(self) -> typing.Optional[builtins.str]:
        '''The repository policy to apply to repositories created using the template.

        A repository policy is a permissions policy associated with a repository to control access permissions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html#cfn-ecr-repositorycreationtemplate-repositorypolicy
        '''
        result = self._values.get("repository_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
        '''The metadata to apply to the repository to help you categorize and organize.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html#cfn-ecr-repositorycreationtemplate-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryCreationTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRepositoryCreationTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRepositoryCreationTemplatePropsMixin",
):
    '''The details of the repository creation template associated with the request.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repositorycreationtemplate.html
    :cloudformationResource: AWS::ECR::RepositoryCreationTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
        
        cfn_repository_creation_template_props_mixin = ecr_mixins.CfnRepositoryCreationTemplatePropsMixin(ecr_mixins.CfnRepositoryCreationTemplateMixinProps(
            applied_for=["appliedFor"],
            custom_role_arn="customRoleArn",
            description="description",
            encryption_configuration=ecr_mixins.CfnRepositoryCreationTemplatePropsMixin.EncryptionConfigurationProperty(
                encryption_type="encryptionType",
                kms_key="kmsKey"
            ),
            image_tag_mutability="imageTagMutability",
            image_tag_mutability_exclusion_filters=[ecr_mixins.CfnRepositoryCreationTemplatePropsMixin.ImageTagMutabilityExclusionFilterProperty(
                image_tag_mutability_exclusion_filter_type="imageTagMutabilityExclusionFilterType",
                image_tag_mutability_exclusion_filter_value="imageTagMutabilityExclusionFilterValue"
            )],
            lifecycle_policy="lifecyclePolicy",
            prefix="prefix",
            repository_policy="repositoryPolicy",
            resource_tags=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRepositoryCreationTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ECR::RepositoryCreationTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89ad1be22a51856d5c55c99dd07330235d78cb06b62df90ed8ef9d275421fd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__822ad0c07fb20d6654810a073a2305b7ace09a0b41501fb71645d850d6667de3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5241c8704826a664ad3caaa884e0bfcb332132400a884709d94a79bc81d8e2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRepositoryCreationTemplateMixinProps:
        return typing.cast(CfnRepositoryCreationTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRepositoryCreationTemplatePropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType", "kms_key": "kmsKey"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_type: typing.Optional[builtins.str] = None,
            kms_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The encryption configuration for the repository. This determines how the contents of your repository are encrypted at rest.

            By default, when no encryption configuration is set or the ``AES256`` encryption type is used, Amazon ECR uses server-side encryption with Amazon S3-managed encryption keys which encrypts your data at rest using an AES256 encryption algorithm. This does not require any action on your part.

            For more control over the encryption of the contents of your repository, you can use server-side encryption with AWS Key Management Service key stored in AWS Key Management Service ( AWS  ) to encrypt your images. For more information, see `Amazon ECR encryption at rest <https://docs.aws.amazon.com/AmazonECR/latest/userguide/encryption-at-rest.html>`_ in the *Amazon Elastic Container Registry User Guide* .

            :param encryption_type: The encryption type to use. If you use the ``KMS`` encryption type, the contents of the repository will be encrypted using server-side encryption with AWS Key Management Service key stored in AWS . When you use AWS to encrypt your data, you can either use the default AWS managed AWS key for Amazon ECR, or specify your own AWS key, which you already created. If you use the ``KMS_DSSE`` encryption type, the contents of the repository will be encrypted with two layers of encryption using server-side encryption with the AWS Management Service key stored in AWS . Similar to the ``KMS`` encryption type, you can either use the default AWS managed AWS key for Amazon ECR, or specify your own AWS key, which you've already created. If you use the ``AES256`` encryption type, Amazon ECR uses server-side encryption with Amazon S3-managed encryption keys which encrypts the images in the repository using an AES256 encryption algorithm. For more information, see `Amazon ECR encryption at rest <https://docs.aws.amazon.com/AmazonECR/latest/userguide/encryption-at-rest.html>`_ in the *Amazon Elastic Container Registry User Guide* .
            :param kms_key: If you use the ``KMS`` encryption type, specify the AWS key to use for encryption. The alias, key ID, or full ARN of the AWS key can be specified. The key must exist in the same Region as the repository. If no key is specified, the default AWS managed AWS key for Amazon ECR will be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repositorycreationtemplate-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                encryption_configuration_property = ecr_mixins.CfnRepositoryCreationTemplatePropsMixin.EncryptionConfigurationProperty(
                    encryption_type="encryptionType",
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29f8297441ff9afc38699f6711ed34286059e92f12769cf44efeb4de008039a0)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_type is not None:
                self._values["encryption_type"] = encryption_type
            if kms_key is not None:
                self._values["kms_key"] = kms_key

        @builtins.property
        def encryption_type(self) -> typing.Optional[builtins.str]:
            '''The encryption type to use.

            If you use the ``KMS`` encryption type, the contents of the repository will be encrypted using server-side encryption with AWS Key Management Service key stored in AWS  . When you use AWS  to encrypt your data, you can either use the default AWS managed AWS  key for Amazon ECR, or specify your own AWS  key, which you already created.

            If you use the ``KMS_DSSE`` encryption type, the contents of the repository will be encrypted with two layers of encryption using server-side encryption with the AWS  Management Service key stored in AWS  . Similar to the ``KMS`` encryption type, you can either use the default AWS managed AWS  key for Amazon ECR, or specify your own AWS  key, which you've already created.

            If you use the ``AES256`` encryption type, Amazon ECR uses server-side encryption with Amazon S3-managed encryption keys which encrypts the images in the repository using an AES256 encryption algorithm.

            For more information, see `Amazon ECR encryption at rest <https://docs.aws.amazon.com/AmazonECR/latest/userguide/encryption-at-rest.html>`_ in the *Amazon Elastic Container Registry User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repositorycreationtemplate-encryptionconfiguration.html#cfn-ecr-repositorycreationtemplate-encryptionconfiguration-encryptiontype
            '''
            result = self._values.get("encryption_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''If you use the ``KMS`` encryption type, specify the AWS  key to use for encryption.

            The alias, key ID, or full ARN of the AWS  key can be specified. The key must exist in the same Region as the repository. If no key is specified, the default AWS managed AWS  key for Amazon ECR will be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repositorycreationtemplate-encryptionconfiguration.html#cfn-ecr-repositorycreationtemplate-encryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRepositoryCreationTemplatePropsMixin.ImageTagMutabilityExclusionFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_tag_mutability_exclusion_filter_type": "imageTagMutabilityExclusionFilterType",
            "image_tag_mutability_exclusion_filter_value": "imageTagMutabilityExclusionFilterValue",
        },
    )
    class ImageTagMutabilityExclusionFilterProperty:
        def __init__(
            self,
            *,
            image_tag_mutability_exclusion_filter_type: typing.Optional[builtins.str] = None,
            image_tag_mutability_exclusion_filter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A filter that specifies which image tags should be excluded from the repository's image tag mutability setting.

            :param image_tag_mutability_exclusion_filter_type: 
            :param image_tag_mutability_exclusion_filter_value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repositorycreationtemplate-imagetagmutabilityexclusionfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                image_tag_mutability_exclusion_filter_property = ecr_mixins.CfnRepositoryCreationTemplatePropsMixin.ImageTagMutabilityExclusionFilterProperty(
                    image_tag_mutability_exclusion_filter_type="imageTagMutabilityExclusionFilterType",
                    image_tag_mutability_exclusion_filter_value="imageTagMutabilityExclusionFilterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ecf814d53b6daa61be2f2fe9be26a24a94093d738629ade447d64e72577b25e1)
                check_type(argname="argument image_tag_mutability_exclusion_filter_type", value=image_tag_mutability_exclusion_filter_type, expected_type=type_hints["image_tag_mutability_exclusion_filter_type"])
                check_type(argname="argument image_tag_mutability_exclusion_filter_value", value=image_tag_mutability_exclusion_filter_value, expected_type=type_hints["image_tag_mutability_exclusion_filter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_tag_mutability_exclusion_filter_type is not None:
                self._values["image_tag_mutability_exclusion_filter_type"] = image_tag_mutability_exclusion_filter_type
            if image_tag_mutability_exclusion_filter_value is not None:
                self._values["image_tag_mutability_exclusion_filter_value"] = image_tag_mutability_exclusion_filter_value

        @builtins.property
        def image_tag_mutability_exclusion_filter_type(
            self,
        ) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repositorycreationtemplate-imagetagmutabilityexclusionfilter.html#cfn-ecr-repositorycreationtemplate-imagetagmutabilityexclusionfilter-imagetagmutabilityexclusionfiltertype
            '''
            result = self._values.get("image_tag_mutability_exclusion_filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_tag_mutability_exclusion_filter_value(
            self,
        ) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repositorycreationtemplate-imagetagmutabilityexclusionfilter.html#cfn-ecr-repositorycreationtemplate-imagetagmutabilityexclusionfilter-imagetagmutabilityexclusionfiltervalue
            '''
            result = self._values.get("image_tag_mutability_exclusion_filter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageTagMutabilityExclusionFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRepositoryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "empty_on_delete": "emptyOnDelete",
        "encryption_configuration": "encryptionConfiguration",
        "image_scanning_configuration": "imageScanningConfiguration",
        "image_tag_mutability": "imageTagMutability",
        "image_tag_mutability_exclusion_filters": "imageTagMutabilityExclusionFilters",
        "lifecycle_policy": "lifecyclePolicy",
        "repository_name": "repositoryName",
        "repository_policy_text": "repositoryPolicyText",
        "tags": "tags",
    },
)
class CfnRepositoryMixinProps:
    def __init__(
        self,
        *,
        empty_on_delete: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRepositoryPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        image_scanning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRepositoryPropsMixin.ImageScanningConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        image_tag_mutability: typing.Optional[builtins.str] = None,
        image_tag_mutability_exclusion_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRepositoryPropsMixin.ImageTagMutabilityExclusionFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        lifecycle_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRepositoryPropsMixin.LifecyclePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRepositoryPropsMixin.

        :param empty_on_delete: If true, deleting the repository force deletes the contents of the repository. If false, the repository must be empty before attempting to delete it.
        :param encryption_configuration: The encryption configuration for the repository. This determines how the contents of your repository are encrypted at rest.
        :param image_scanning_configuration: .. epigraph:: The ``imageScanningConfiguration`` parameter is being deprecated, in favor of specifying the image scanning configuration at the registry level. For more information, see ``PutRegistryScanningConfiguration`` . The image scanning configuration for the repository. This determines whether images are scanned for known vulnerabilities after being pushed to the repository.
        :param image_tag_mutability: The tag mutability setting for the repository. If this parameter is omitted, the default setting of ``MUTABLE`` will be used which will allow image tags to be overwritten. If ``IMMUTABLE`` is specified, all image tags within the repository will be immutable which will prevent them from being overwritten.
        :param image_tag_mutability_exclusion_filters: A list of filters that specify which image tags are excluded from the repository's image tag mutability setting.
        :param lifecycle_policy: Creates or updates a lifecycle policy. For information about lifecycle policy syntax, see `Lifecycle policy template <https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html>`_ .
        :param repository_name: The name to use for the repository. The repository name may be specified on its own (such as ``nginx-web-app`` ) or it can be prepended with a namespace to group the repository into a category (such as ``project-a/nginx-web-app`` ). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the repository name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . The repository name must start with a letter and can only contain lowercase letters, numbers, hyphens, underscores, and forward slashes. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param repository_policy_text: The JSON repository policy text to apply to the repository. For more information, see `Amazon ECR repository policies <https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policy-examples.html>`_ in the *Amazon Elastic Container Registry User Guide* .
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
            
            # repository_policy_text: Any
            
            cfn_repository_mixin_props = ecr_mixins.CfnRepositoryMixinProps(
                empty_on_delete=False,
                encryption_configuration=ecr_mixins.CfnRepositoryPropsMixin.EncryptionConfigurationProperty(
                    encryption_type="encryptionType",
                    kms_key="kmsKey"
                ),
                image_scanning_configuration=ecr_mixins.CfnRepositoryPropsMixin.ImageScanningConfigurationProperty(
                    scan_on_push=False
                ),
                image_tag_mutability="imageTagMutability",
                image_tag_mutability_exclusion_filters=[ecr_mixins.CfnRepositoryPropsMixin.ImageTagMutabilityExclusionFilterProperty(
                    image_tag_mutability_exclusion_filter_type="imageTagMutabilityExclusionFilterType",
                    image_tag_mutability_exclusion_filter_value="imageTagMutabilityExclusionFilterValue"
                )],
                lifecycle_policy=ecr_mixins.CfnRepositoryPropsMixin.LifecyclePolicyProperty(
                    lifecycle_policy_text="lifecyclePolicyText",
                    registry_id="registryId"
                ),
                repository_name="repositoryName",
                repository_policy_text=repository_policy_text,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67c4c29795c0ffe55c7b34cd838ff9f3f7a3af421e0e1ed1bad81403ec83be1)
            check_type(argname="argument empty_on_delete", value=empty_on_delete, expected_type=type_hints["empty_on_delete"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument image_scanning_configuration", value=image_scanning_configuration, expected_type=type_hints["image_scanning_configuration"])
            check_type(argname="argument image_tag_mutability", value=image_tag_mutability, expected_type=type_hints["image_tag_mutability"])
            check_type(argname="argument image_tag_mutability_exclusion_filters", value=image_tag_mutability_exclusion_filters, expected_type=type_hints["image_tag_mutability_exclusion_filters"])
            check_type(argname="argument lifecycle_policy", value=lifecycle_policy, expected_type=type_hints["lifecycle_policy"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument repository_policy_text", value=repository_policy_text, expected_type=type_hints["repository_policy_text"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if empty_on_delete is not None:
            self._values["empty_on_delete"] = empty_on_delete
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if image_scanning_configuration is not None:
            self._values["image_scanning_configuration"] = image_scanning_configuration
        if image_tag_mutability is not None:
            self._values["image_tag_mutability"] = image_tag_mutability
        if image_tag_mutability_exclusion_filters is not None:
            self._values["image_tag_mutability_exclusion_filters"] = image_tag_mutability_exclusion_filters
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if repository_policy_text is not None:
            self._values["repository_policy_text"] = repository_policy_text
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def empty_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If true, deleting the repository force deletes the contents of the repository.

        If false, the repository must be empty before attempting to delete it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-emptyondelete
        '''
        result = self._values.get("empty_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.EncryptionConfigurationProperty"]]:
        '''The encryption configuration for the repository.

        This determines how the contents of your repository are encrypted at rest.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.EncryptionConfigurationProperty"]], result)

    @builtins.property
    def image_scanning_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.ImageScanningConfigurationProperty"]]:
        '''.. epigraph::

   The ``imageScanningConfiguration`` parameter is being deprecated, in favor of specifying the image scanning configuration at the registry level.

        For more information, see ``PutRegistryScanningConfiguration`` .

        The image scanning configuration for the repository. This determines whether images are scanned for known vulnerabilities after being pushed to the repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagescanningconfiguration
        '''
        result = self._values.get("image_scanning_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.ImageScanningConfigurationProperty"]], result)

    @builtins.property
    def image_tag_mutability(self) -> typing.Optional[builtins.str]:
        '''The tag mutability setting for the repository.

        If this parameter is omitted, the default setting of ``MUTABLE`` will be used which will allow image tags to be overwritten. If ``IMMUTABLE`` is specified, all image tags within the repository will be immutable which will prevent them from being overwritten.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagetagmutability
        '''
        result = self._values.get("image_tag_mutability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag_mutability_exclusion_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.ImageTagMutabilityExclusionFilterProperty"]]]]:
        '''A list of filters that specify which image tags are excluded from the repository's image tag mutability setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagetagmutabilityexclusionfilters
        '''
        result = self._values.get("image_tag_mutability_exclusion_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.ImageTagMutabilityExclusionFilterProperty"]]]], result)

    @builtins.property
    def lifecycle_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.LifecyclePolicyProperty"]]:
        '''Creates or updates a lifecycle policy.

        For information about lifecycle policy syntax, see `Lifecycle policy template <https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-lifecyclepolicy
        '''
        result = self._values.get("lifecycle_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.LifecyclePolicyProperty"]], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''The name to use for the repository.

        The repository name may be specified on its own (such as ``nginx-web-app`` ) or it can be prepended with a namespace to group the repository into a category (such as ``project-a/nginx-web-app`` ). If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the repository name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        The repository name must start with a letter and can only contain lowercase letters, numbers, hyphens, underscores, and forward slashes.
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositoryname
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_policy_text(self) -> typing.Any:
        '''The JSON repository policy text to apply to the repository.

        For more information, see `Amazon ECR repository policies <https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policy-examples.html>`_ in the *Amazon Elastic Container Registry User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositorypolicytext
        '''
        result = self._values.get("repository_policy_text")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRepositoryPropsMixin",
):
    '''The ``AWS::ECR::Repository`` resource specifies an Amazon Elastic Container Registry (Amazon ECR) repository, where users can push and pull Docker images, Open Container Initiative (OCI) images, and OCI compatible artifacts.

    For more information, see `Amazon ECR private repositories <https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html>`_ in the *Amazon ECR User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
    :cloudformationResource: AWS::ECR::Repository
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
        
        # repository_policy_text: Any
        
        cfn_repository_props_mixin = ecr_mixins.CfnRepositoryPropsMixin(ecr_mixins.CfnRepositoryMixinProps(
            empty_on_delete=False,
            encryption_configuration=ecr_mixins.CfnRepositoryPropsMixin.EncryptionConfigurationProperty(
                encryption_type="encryptionType",
                kms_key="kmsKey"
            ),
            image_scanning_configuration=ecr_mixins.CfnRepositoryPropsMixin.ImageScanningConfigurationProperty(
                scan_on_push=False
            ),
            image_tag_mutability="imageTagMutability",
            image_tag_mutability_exclusion_filters=[ecr_mixins.CfnRepositoryPropsMixin.ImageTagMutabilityExclusionFilterProperty(
                image_tag_mutability_exclusion_filter_type="imageTagMutabilityExclusionFilterType",
                image_tag_mutability_exclusion_filter_value="imageTagMutabilityExclusionFilterValue"
            )],
            lifecycle_policy=ecr_mixins.CfnRepositoryPropsMixin.LifecyclePolicyProperty(
                lifecycle_policy_text="lifecyclePolicyText",
                registry_id="registryId"
            ),
            repository_name="repositoryName",
            repository_policy_text=repository_policy_text,
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
        props: typing.Union[CfnRepositoryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ECR::Repository``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ec8854c9c6a8281c41efba365048f9e5ac923836e17590048c5865191496f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33c5d9d37ae1894a53972de8fd3fe713608152756beb9d1e3274a5d82755a573)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ab9d0d69d0a5c54d39c090d791dcf84bbeff36f399ccb92a211aa800c5ba1a)
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

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRepositoryPropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType", "kms_key": "kmsKey"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_type: typing.Optional[builtins.str] = None,
            kms_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The encryption configuration for the repository. This determines how the contents of your repository are encrypted at rest.

            By default, when no encryption configuration is set or the ``AES256`` encryption type is used, Amazon ECR uses server-side encryption with Amazon S3-managed encryption keys which encrypts your data at rest using an AES256 encryption algorithm. This does not require any action on your part.

            For more control over the encryption of the contents of your repository, you can use server-side encryption with AWS Key Management Service key stored in AWS Key Management Service ( AWS  ) to encrypt your images. For more information, see `Amazon ECR encryption at rest <https://docs.aws.amazon.com/AmazonECR/latest/userguide/encryption-at-rest.html>`_ in the *Amazon Elastic Container Registry User Guide* .

            :param encryption_type: The encryption type to use. If you use the ``KMS`` encryption type, the contents of the repository will be encrypted using server-side encryption with AWS Key Management Service key stored in AWS . When you use AWS to encrypt your data, you can either use the default AWS managed AWS key for Amazon ECR, or specify your own AWS key, which you already created. If you use the ``KMS_DSSE`` encryption type, the contents of the repository will be encrypted with two layers of encryption using server-side encryption with the AWS Management Service key stored in AWS . Similar to the ``KMS`` encryption type, you can either use the default AWS managed AWS key for Amazon ECR, or specify your own AWS key, which you've already created. If you use the ``AES256`` encryption type, Amazon ECR uses server-side encryption with Amazon S3-managed encryption keys which encrypts the images in the repository using an AES256 encryption algorithm. For more information, see `Amazon ECR encryption at rest <https://docs.aws.amazon.com/AmazonECR/latest/userguide/encryption-at-rest.html>`_ in the *Amazon Elastic Container Registry User Guide* .
            :param kms_key: If you use the ``KMS`` encryption type, specify the AWS key to use for encryption. The alias, key ID, or full ARN of the AWS key can be specified. The key must exist in the same Region as the repository. If no key is specified, the default AWS managed AWS key for Amazon ECR will be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                encryption_configuration_property = ecr_mixins.CfnRepositoryPropsMixin.EncryptionConfigurationProperty(
                    encryption_type="encryptionType",
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__838173b8462d4ca6891178375a20d7acd405067fdfcd2f7be9835bd7b7ff46df)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_type is not None:
                self._values["encryption_type"] = encryption_type
            if kms_key is not None:
                self._values["kms_key"] = kms_key

        @builtins.property
        def encryption_type(self) -> typing.Optional[builtins.str]:
            '''The encryption type to use.

            If you use the ``KMS`` encryption type, the contents of the repository will be encrypted using server-side encryption with AWS Key Management Service key stored in AWS  . When you use AWS  to encrypt your data, you can either use the default AWS managed AWS  key for Amazon ECR, or specify your own AWS  key, which you already created.

            If you use the ``KMS_DSSE`` encryption type, the contents of the repository will be encrypted with two layers of encryption using server-side encryption with the AWS  Management Service key stored in AWS  . Similar to the ``KMS`` encryption type, you can either use the default AWS managed AWS  key for Amazon ECR, or specify your own AWS  key, which you've already created.

            If you use the ``AES256`` encryption type, Amazon ECR uses server-side encryption with Amazon S3-managed encryption keys which encrypts the images in the repository using an AES256 encryption algorithm.

            For more information, see `Amazon ECR encryption at rest <https://docs.aws.amazon.com/AmazonECR/latest/userguide/encryption-at-rest.html>`_ in the *Amazon Elastic Container Registry User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-encryptionconfiguration.html#cfn-ecr-repository-encryptionconfiguration-encryptiontype
            '''
            result = self._values.get("encryption_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''If you use the ``KMS`` encryption type, specify the AWS  key to use for encryption.

            The alias, key ID, or full ARN of the AWS  key can be specified. The key must exist in the same Region as the repository. If no key is specified, the default AWS managed AWS  key for Amazon ECR will be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-encryptionconfiguration.html#cfn-ecr-repository-encryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRepositoryPropsMixin.ImageScanningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"scan_on_push": "scanOnPush"},
    )
    class ImageScanningConfigurationProperty:
        def __init__(
            self,
            *,
            scan_on_push: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The image scanning configuration for a repository.

            :param scan_on_push: The setting that determines whether images are scanned after being pushed to a repository. If set to ``true`` , images will be scanned after being pushed. If this parameter is not specified, it will default to ``false`` and images will not be scanned unless a scan is manually started.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-imagescanningconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                image_scanning_configuration_property = ecr_mixins.CfnRepositoryPropsMixin.ImageScanningConfigurationProperty(
                    scan_on_push=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__170e6aa86245f93a568940350b0050193844fa6c815d956f56ed8ed19c52e9ce)
                check_type(argname="argument scan_on_push", value=scan_on_push, expected_type=type_hints["scan_on_push"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if scan_on_push is not None:
                self._values["scan_on_push"] = scan_on_push

        @builtins.property
        def scan_on_push(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The setting that determines whether images are scanned after being pushed to a repository.

            If set to ``true`` , images will be scanned after being pushed. If this parameter is not specified, it will default to ``false`` and images will not be scanned unless a scan is manually started.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-imagescanningconfiguration.html#cfn-ecr-repository-imagescanningconfiguration-scanonpush
            '''
            result = self._values.get("scan_on_push")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageScanningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRepositoryPropsMixin.ImageTagMutabilityExclusionFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_tag_mutability_exclusion_filter_type": "imageTagMutabilityExclusionFilterType",
            "image_tag_mutability_exclusion_filter_value": "imageTagMutabilityExclusionFilterValue",
        },
    )
    class ImageTagMutabilityExclusionFilterProperty:
        def __init__(
            self,
            *,
            image_tag_mutability_exclusion_filter_type: typing.Optional[builtins.str] = None,
            image_tag_mutability_exclusion_filter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A filter that specifies which image tags should be excluded from the repository's image tag mutability setting.

            :param image_tag_mutability_exclusion_filter_type: Specifies the type of filter to use for excluding image tags from the repository's mutability setting.
            :param image_tag_mutability_exclusion_filter_value: The value to use when filtering image tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-imagetagmutabilityexclusionfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                image_tag_mutability_exclusion_filter_property = ecr_mixins.CfnRepositoryPropsMixin.ImageTagMutabilityExclusionFilterProperty(
                    image_tag_mutability_exclusion_filter_type="imageTagMutabilityExclusionFilterType",
                    image_tag_mutability_exclusion_filter_value="imageTagMutabilityExclusionFilterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50ad7009962959cb0992da0f52158243dd8fe6a994d7097797eda585eef1617c)
                check_type(argname="argument image_tag_mutability_exclusion_filter_type", value=image_tag_mutability_exclusion_filter_type, expected_type=type_hints["image_tag_mutability_exclusion_filter_type"])
                check_type(argname="argument image_tag_mutability_exclusion_filter_value", value=image_tag_mutability_exclusion_filter_value, expected_type=type_hints["image_tag_mutability_exclusion_filter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_tag_mutability_exclusion_filter_type is not None:
                self._values["image_tag_mutability_exclusion_filter_type"] = image_tag_mutability_exclusion_filter_type
            if image_tag_mutability_exclusion_filter_value is not None:
                self._values["image_tag_mutability_exclusion_filter_value"] = image_tag_mutability_exclusion_filter_value

        @builtins.property
        def image_tag_mutability_exclusion_filter_type(
            self,
        ) -> typing.Optional[builtins.str]:
            '''Specifies the type of filter to use for excluding image tags from the repository's mutability setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-imagetagmutabilityexclusionfilter.html#cfn-ecr-repository-imagetagmutabilityexclusionfilter-imagetagmutabilityexclusionfiltertype
            '''
            result = self._values.get("image_tag_mutability_exclusion_filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_tag_mutability_exclusion_filter_value(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The value to use when filtering image tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-imagetagmutabilityexclusionfilter.html#cfn-ecr-repository-imagetagmutabilityexclusionfilter-imagetagmutabilityexclusionfiltervalue
            '''
            result = self._values.get("image_tag_mutability_exclusion_filter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageTagMutabilityExclusionFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnRepositoryPropsMixin.LifecyclePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lifecycle_policy_text": "lifecyclePolicyText",
            "registry_id": "registryId",
        },
    )
    class LifecyclePolicyProperty:
        def __init__(
            self,
            *,
            lifecycle_policy_text: typing.Optional[builtins.str] = None,
            registry_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LifecyclePolicy`` property type specifies a lifecycle policy.

            For information about lifecycle policy syntax, see `Lifecycle policy template <https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html>`_ in the *Amazon ECR User Guide* .

            :param lifecycle_policy_text: The JSON repository policy text to apply to the repository.
            :param registry_id: The AWS account ID associated with the registry that contains the repository. If you do not specify a registry, the default registry is assumed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                lifecycle_policy_property = ecr_mixins.CfnRepositoryPropsMixin.LifecyclePolicyProperty(
                    lifecycle_policy_text="lifecyclePolicyText",
                    registry_id="registryId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9505a5381605ed7ee09c0c272dcd284128c67bd4e6153b2cff6719b310ad533a)
                check_type(argname="argument lifecycle_policy_text", value=lifecycle_policy_text, expected_type=type_hints["lifecycle_policy_text"])
                check_type(argname="argument registry_id", value=registry_id, expected_type=type_hints["registry_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lifecycle_policy_text is not None:
                self._values["lifecycle_policy_text"] = lifecycle_policy_text
            if registry_id is not None:
                self._values["registry_id"] = registry_id

        @builtins.property
        def lifecycle_policy_text(self) -> typing.Optional[builtins.str]:
            '''The JSON repository policy text to apply to the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-lifecyclepolicytext
            '''
            result = self._values.get("lifecycle_policy_text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def registry_id(self) -> typing.Optional[builtins.str]:
            '''The AWS account ID associated with the registry that contains the repository.

            If you do not specify a registry, the default registry is assumed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-registryid
            '''
            result = self._values.get("registry_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecyclePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnSigningConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules"},
)
class CfnSigningConfigurationMixinProps:
    def __init__(
        self,
        *,
        rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSigningConfigurationPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnSigningConfigurationPropsMixin.

        :param rules: A list of signing rules. Each rule defines a signing profile and optional repository filters that determine which images are automatically signed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-signingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
            
            cfn_signing_configuration_mixin_props = ecr_mixins.CfnSigningConfigurationMixinProps(
                rules=[ecr_mixins.CfnSigningConfigurationPropsMixin.RuleProperty(
                    repository_filters=[ecr_mixins.CfnSigningConfigurationPropsMixin.RepositoryFilterProperty(
                        filter="filter",
                        filter_type="filterType"
                    )],
                    signing_profile_arn="signingProfileArn"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966f1bfc1abc3f80c08d6d48b7f9f833af9a6da00798ef6e3cf9198e28722df3)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSigningConfigurationPropsMixin.RuleProperty"]]]]:
        '''A list of signing rules.

        Each rule defines a signing profile and optional repository filters that determine which images are automatically signed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-signingconfiguration.html#cfn-ecr-signingconfiguration-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSigningConfigurationPropsMixin.RuleProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSigningConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSigningConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnSigningConfigurationPropsMixin",
):
    '''The signing configuration for a registry, which specifies rules for automatically signing images when pushed.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-signingconfiguration.html
    :cloudformationResource: AWS::ECR::SigningConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
        
        cfn_signing_configuration_props_mixin = ecr_mixins.CfnSigningConfigurationPropsMixin(ecr_mixins.CfnSigningConfigurationMixinProps(
            rules=[ecr_mixins.CfnSigningConfigurationPropsMixin.RuleProperty(
                repository_filters=[ecr_mixins.CfnSigningConfigurationPropsMixin.RepositoryFilterProperty(
                    filter="filter",
                    filter_type="filterType"
                )],
                signing_profile_arn="signingProfileArn"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSigningConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ECR::SigningConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9efbb5ec6237e006eed283649ff659237e19ba1e604128fb672a59f2e8628e21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__636d9bf70295c0a716552fc4b063aae4cff83f112ce078cdea3a8c282e237416)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__badc136b8d3e2c9895a6fc7ea0c7442c01e313041747f91ab5c3e59a288a5b7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSigningConfigurationMixinProps:
        return typing.cast(CfnSigningConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnSigningConfigurationPropsMixin.RepositoryFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"filter": "filter", "filter_type": "filterType"},
    )
    class RepositoryFilterProperty:
        def __init__(
            self,
            *,
            filter: typing.Optional[builtins.str] = None,
            filter_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A repository filter used to determine which repositories have their images automatically signed on push.

            Each filter consists of a filter type and filter value.

            :param filter: The filter value used to match repository names. When using ``WILDCARD_MATCH`` , the ``*`` character matches any sequence of characters. Examples: - ``myapp/*`` - Matches all repositories starting with ``myapp/`` - ``* /production`` - Matches all repositories ending with ``/production`` - ``*prod*`` - Matches all repositories containing ``prod``
            :param filter_type: The type of filter to apply. Currently, only ``WILDCARD_MATCH`` is supported, which uses wildcard patterns to match repository names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-signingconfiguration-repositoryfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                repository_filter_property = ecr_mixins.CfnSigningConfigurationPropsMixin.RepositoryFilterProperty(
                    filter="filter",
                    filter_type="filterType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19ecc832f9f2b6e316a2b5ed7507394abc977986757f2e4c33ac2118743deb2e)
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter is not None:
                self._values["filter"] = filter
            if filter_type is not None:
                self._values["filter_type"] = filter_type

        @builtins.property
        def filter(self) -> typing.Optional[builtins.str]:
            '''The filter value used to match repository names.

            When using ``WILDCARD_MATCH`` , the ``*`` character matches any sequence of characters.

            Examples:

            - ``myapp/*`` - Matches all repositories starting with ``myapp/``
            - ``* /production`` - Matches all repositories ending with ``/production``
            - ``*prod*`` - Matches all repositories containing ``prod``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-signingconfiguration-repositoryfilter.html#cfn-ecr-signingconfiguration-repositoryfilter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            '''The type of filter to apply.

            Currently, only ``WILDCARD_MATCH`` is supported, which uses wildcard patterns to match repository names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-signingconfiguration-repositoryfilter.html#cfn-ecr-signingconfiguration-repositoryfilter-filtertype
            '''
            result = self._values.get("filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RepositoryFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.mixins.CfnSigningConfigurationPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "repository_filters": "repositoryFilters",
            "signing_profile_arn": "signingProfileArn",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            repository_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSigningConfigurationPropsMixin.RepositoryFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            signing_profile_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A signing rule that specifies a signing profile and optional repository filters.

            When an image is pushed to a matching repository, a signing job is created using the specified profile.

            :param repository_filters: A list of repository filters that determine which repositories have their images signed on push. If no filters are specified, all images pushed to the registry are signed using the rule's signing profile. Maximum of 100 filters per rule.
            :param signing_profile_arn: The ARN of the AWS Signer signing profile to use for signing images that match this rule. For more information about signing profiles, see `Signing profiles <https://docs.aws.amazon.com/signer/latest/developerguide/signing-profiles.html>`_ in the *AWS Signer Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-signingconfiguration-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ecr import mixins as ecr_mixins
                
                rule_property = ecr_mixins.CfnSigningConfigurationPropsMixin.RuleProperty(
                    repository_filters=[ecr_mixins.CfnSigningConfigurationPropsMixin.RepositoryFilterProperty(
                        filter="filter",
                        filter_type="filterType"
                    )],
                    signing_profile_arn="signingProfileArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ac913911f131d626d04e1a6c4d91867881ac275f1b050fd30c9a94715127fbc)
                check_type(argname="argument repository_filters", value=repository_filters, expected_type=type_hints["repository_filters"])
                check_type(argname="argument signing_profile_arn", value=signing_profile_arn, expected_type=type_hints["signing_profile_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if repository_filters is not None:
                self._values["repository_filters"] = repository_filters
            if signing_profile_arn is not None:
                self._values["signing_profile_arn"] = signing_profile_arn

        @builtins.property
        def repository_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSigningConfigurationPropsMixin.RepositoryFilterProperty"]]]]:
            '''A list of repository filters that determine which repositories have their images signed on push.

            If no filters are specified, all images pushed to the registry are signed using the rule's signing profile. Maximum of 100 filters per rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-signingconfiguration-rule.html#cfn-ecr-signingconfiguration-rule-repositoryfilters
            '''
            result = self._values.get("repository_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSigningConfigurationPropsMixin.RepositoryFilterProperty"]]]], result)

        @builtins.property
        def signing_profile_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the AWS Signer signing profile to use for signing images that match this rule.

            For more information about signing profiles, see `Signing profiles <https://docs.aws.amazon.com/signer/latest/developerguide/signing-profiles.html>`_ in the *AWS Signer Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-signingconfiguration-rule.html#cfn-ecr-signingconfiguration-rule-signingprofilearn
            '''
            result = self._values.get("signing_profile_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnPublicRepositoryMixinProps",
    "CfnPublicRepositoryPropsMixin",
    "CfnPullThroughCacheRuleMixinProps",
    "CfnPullThroughCacheRulePropsMixin",
    "CfnPullTimeUpdateExclusionMixinProps",
    "CfnPullTimeUpdateExclusionPropsMixin",
    "CfnRegistryPolicyMixinProps",
    "CfnRegistryPolicyPropsMixin",
    "CfnRegistryScanningConfigurationMixinProps",
    "CfnRegistryScanningConfigurationPropsMixin",
    "CfnReplicationConfigurationMixinProps",
    "CfnReplicationConfigurationPropsMixin",
    "CfnRepositoryCreationTemplateMixinProps",
    "CfnRepositoryCreationTemplatePropsMixin",
    "CfnRepositoryMixinProps",
    "CfnRepositoryPropsMixin",
    "CfnSigningConfigurationMixinProps",
    "CfnSigningConfigurationPropsMixin",
]

publication.publish()

def _typecheckingstub__ffacb83d0acda1bba29391c93bd0646e1eba3a6185f8f5e1d50f8384342b09a3(
    *,
    repository_catalog_data: typing.Any = None,
    repository_name: typing.Optional[builtins.str] = None,
    repository_policy_text: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2b00f2d112387c0918d1863fd585ec57aba79fde04ccc20841714e2afdcfde(
    props: typing.Union[CfnPublicRepositoryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de6f94ca247329d2c728174664632b43b700f0839d7ca908d764ba8b89ef14c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe509bb853d5a6b35679c3815b0be4a609716237d6a1192871abd1ffcb75a028(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca1f909e33540543c9dfb8f13d2d5ef17251134ef9cfcae97c427e48cc18667(
    *,
    about_text: typing.Optional[builtins.str] = None,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    operating_systems: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_description: typing.Optional[builtins.str] = None,
    usage_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c464cee78a158e4b16f37f9f163b51a2b0be23800ad26b5a07ba1848de4a09(
    *,
    credential_arn: typing.Optional[builtins.str] = None,
    custom_role_arn: typing.Optional[builtins.str] = None,
    ecr_repository_prefix: typing.Optional[builtins.str] = None,
    upstream_registry: typing.Optional[builtins.str] = None,
    upstream_registry_url: typing.Optional[builtins.str] = None,
    upstream_repository_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa4c0acd628f2eddc585f005888cc30b0c33b0e3951f44995a59586ba19dee6(
    props: typing.Union[CfnPullThroughCacheRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b1f3b5927d430b77a441e8e6e19d82cac3bfa6c3f42bacc9b04f1840c83979(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861de03a47b669f508a869e054c1e18c02196c4a0cccd07157c49c5058f32a36(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11ec6c3387fe7dd96b43777ed1c68bcc96a3284e7020c79bb89546275763fac(
    *,
    principal_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab20b42b899b6090c8259aa3b141595c1bac402c80a8218e4653edc63ba05971(
    props: typing.Union[CfnPullTimeUpdateExclusionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058c997b8d2da73a8508a33d022e52513ad81783cf5b2876f5da16c1aa997019(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8604572b7b95331adc3f02536dd5243d019ed69b9a82184c4a0f20cd78cfd5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4344da9628ff4dcab8738ebe732f0589bd7d5f7b590b186f2d7820ca888bcb(
    *,
    policy_text: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0bed870fd5e7e5f5b1e0d40749e47166fcd11037a6df1daa2b9fd3c655f8f0(
    props: typing.Union[CfnRegistryPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824dd89b74c5b8372bfd7ab292a93d51ff9a0760f6f8fbb82ecf03670d6a7d9f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e6aa763d6920932be8882a98405c610bb81ddcd60b12a4487c910f6bc00494(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22e4f481bd52b97375688aca48ceebee2b4d5b403074e4510b066c559744a55(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRegistryScanningConfigurationPropsMixin.ScanningRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    scan_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247ad09029000475a9a342247388ded4311bbb748c1f7e8144b7aed8860bf072(
    props: typing.Union[CfnRegistryScanningConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2cc609bf29b1adbbb0e8246b3d8a709849d8fc9be4b61f7a0060aa96bdca1d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf4f7f120c19a1b114a61a9099f0f6dfdeec9d6119cf328b62f0c16df0cef71(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c214f0bed1a5abb359c8d8c51ca5eb96239cc2546b4780c073fe2dbf3545786(
    *,
    filter: typing.Optional[builtins.str] = None,
    filter_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd4e276c2eb6ac2ac6ca100623f518e4fcc0240a49b797ffb977236f71aa792(
    *,
    repository_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRegistryScanningConfigurationPropsMixin.RepositoryFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    scan_frequency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c1ebb5487536ce9b51661e19d1577be2c54672ae3ee6f7f9fd2d9ed5979e1e(
    *,
    replication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationConfigurationPropsMixin.ReplicationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd716eb0f9c76f9a8c3a444813be386c2839c957bb7c8874ada7263d7e817add(
    props: typing.Union[CfnReplicationConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef33c290e021978da25f07172b798002d52dcd0c1f9c57e9ebbb8c7fac5338d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648de56b1c799d329ac779d4aef0bc2b74a3536f571b2fea23715a1418028143(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abd43cdef6dc5071e545f87ba0f44d8036f11d4ebf387c760bb09347bc68fc7(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationConfigurationPropsMixin.ReplicationRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be4d0b94d38dc90de26d581c0f60fd996f6dfeddf3f9e213745d4efe9560ffc(
    *,
    region: typing.Optional[builtins.str] = None,
    registry_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18255465bbe2f32bcc905097ed1027a4f95b608e099ac3627105cae802ee0f54(
    *,
    destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationConfigurationPropsMixin.ReplicationDestinationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    repository_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationConfigurationPropsMixin.RepositoryFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc9e1d9cb1c97c2a81b8cc1efc39146d5bcbc2864ba409276b218554729e47b(
    *,
    filter: typing.Optional[builtins.str] = None,
    filter_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca89f92d3b4ec27098a54f4c2ed6943de2a363d24f2e926d58e26ef9fdeed761(
    *,
    applied_for: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_role_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRepositoryCreationTemplatePropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_tag_mutability: typing.Optional[builtins.str] = None,
    image_tag_mutability_exclusion_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRepositoryCreationTemplatePropsMixin.ImageTagMutabilityExclusionFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lifecycle_policy: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    repository_policy: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89ad1be22a51856d5c55c99dd07330235d78cb06b62df90ed8ef9d275421fd2(
    props: typing.Union[CfnRepositoryCreationTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822ad0c07fb20d6654810a073a2305b7ace09a0b41501fb71645d850d6667de3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5241c8704826a664ad3caaa884e0bfcb332132400a884709d94a79bc81d8e2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f8297441ff9afc38699f6711ed34286059e92f12769cf44efeb4de008039a0(
    *,
    encryption_type: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf814d53b6daa61be2f2fe9be26a24a94093d738629ade447d64e72577b25e1(
    *,
    image_tag_mutability_exclusion_filter_type: typing.Optional[builtins.str] = None,
    image_tag_mutability_exclusion_filter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67c4c29795c0ffe55c7b34cd838ff9f3f7a3af421e0e1ed1bad81403ec83be1(
    *,
    empty_on_delete: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRepositoryPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_scanning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRepositoryPropsMixin.ImageScanningConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_tag_mutability: typing.Optional[builtins.str] = None,
    image_tag_mutability_exclusion_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRepositoryPropsMixin.ImageTagMutabilityExclusionFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lifecycle_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRepositoryPropsMixin.LifecyclePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    repository_name: typing.Optional[builtins.str] = None,
    repository_policy_text: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ec8854c9c6a8281c41efba365048f9e5ac923836e17590048c5865191496f5(
    props: typing.Union[CfnRepositoryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c5d9d37ae1894a53972de8fd3fe713608152756beb9d1e3274a5d82755a573(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ab9d0d69d0a5c54d39c090d791dcf84bbeff36f399ccb92a211aa800c5ba1a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838173b8462d4ca6891178375a20d7acd405067fdfcd2f7be9835bd7b7ff46df(
    *,
    encryption_type: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170e6aa86245f93a568940350b0050193844fa6c815d956f56ed8ed19c52e9ce(
    *,
    scan_on_push: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ad7009962959cb0992da0f52158243dd8fe6a994d7097797eda585eef1617c(
    *,
    image_tag_mutability_exclusion_filter_type: typing.Optional[builtins.str] = None,
    image_tag_mutability_exclusion_filter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9505a5381605ed7ee09c0c272dcd284128c67bd4e6153b2cff6719b310ad533a(
    *,
    lifecycle_policy_text: typing.Optional[builtins.str] = None,
    registry_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966f1bfc1abc3f80c08d6d48b7f9f833af9a6da00798ef6e3cf9198e28722df3(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSigningConfigurationPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efbb5ec6237e006eed283649ff659237e19ba1e604128fb672a59f2e8628e21(
    props: typing.Union[CfnSigningConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636d9bf70295c0a716552fc4b063aae4cff83f112ce078cdea3a8c282e237416(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__badc136b8d3e2c9895a6fc7ea0c7442c01e313041747f91ab5c3e59a288a5b7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ecc832f9f2b6e316a2b5ed7507394abc977986757f2e4c33ac2118743deb2e(
    *,
    filter: typing.Optional[builtins.str] = None,
    filter_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac913911f131d626d04e1a6c4d91867881ac275f1b050fd30c9a94715127fbc(
    *,
    repository_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSigningConfigurationPropsMixin.RepositoryFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    signing_profile_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
