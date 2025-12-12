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
    jsii_type="@aws-cdk/mixins-preview.aws_codestar.mixins.CfnGitHubRepositoryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "code": "code",
        "connection_arn": "connectionArn",
        "enable_issues": "enableIssues",
        "is_private": "isPrivate",
        "repository_access_token": "repositoryAccessToken",
        "repository_description": "repositoryDescription",
        "repository_name": "repositoryName",
        "repository_owner": "repositoryOwner",
    },
)
class CfnGitHubRepositoryMixinProps:
    def __init__(
        self,
        *,
        code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGitHubRepositoryPropsMixin.CodeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        connection_arn: typing.Optional[builtins.str] = None,
        enable_issues: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        is_private: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        repository_access_token: typing.Optional[builtins.str] = None,
        repository_description: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_owner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnGitHubRepositoryPropsMixin.

        :param code: Information about code to be committed to a repository after it is created in an CloudFormation stack.
        :param connection_arn: 
        :param enable_issues: Indicates whether to enable issues for the GitHub repository. You can use GitHub issues to track information and bugs for your repository.
        :param is_private: Indicates whether the GitHub repository is a private repository. If so, you choose who can see and commit to this repository.
        :param repository_access_token: The GitHub user's personal access token for the GitHub repository.
        :param repository_description: A comment or description about the new repository. This description is displayed in GitHub after the repository is created.
        :param repository_name: The name of the repository you want to create in GitHub with CloudFormation stack creation.
        :param repository_owner: The GitHub user name for the owner of the GitHub repository to be created. If this repository should be owned by a GitHub organization, provide its name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codestar import mixins as codestar_mixins
            
            cfn_git_hub_repository_mixin_props = codestar_mixins.CfnGitHubRepositoryMixinProps(
                code=codestar_mixins.CfnGitHubRepositoryPropsMixin.CodeProperty(
                    s3=codestar_mixins.CfnGitHubRepositoryPropsMixin.S3Property(
                        bucket="bucket",
                        key="key",
                        object_version="objectVersion"
                    )
                ),
                connection_arn="connectionArn",
                enable_issues=False,
                is_private=False,
                repository_access_token="repositoryAccessToken",
                repository_description="repositoryDescription",
                repository_name="repositoryName",
                repository_owner="repositoryOwner"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f8c3f7f6221553578a7cccbb58615e799edb70d15adf7701ea4f0ef8e1cf50)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            check_type(argname="argument enable_issues", value=enable_issues, expected_type=type_hints["enable_issues"])
            check_type(argname="argument is_private", value=is_private, expected_type=type_hints["is_private"])
            check_type(argname="argument repository_access_token", value=repository_access_token, expected_type=type_hints["repository_access_token"])
            check_type(argname="argument repository_description", value=repository_description, expected_type=type_hints["repository_description"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument repository_owner", value=repository_owner, expected_type=type_hints["repository_owner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code is not None:
            self._values["code"] = code
        if connection_arn is not None:
            self._values["connection_arn"] = connection_arn
        if enable_issues is not None:
            self._values["enable_issues"] = enable_issues
        if is_private is not None:
            self._values["is_private"] = is_private
        if repository_access_token is not None:
            self._values["repository_access_token"] = repository_access_token
        if repository_description is not None:
            self._values["repository_description"] = repository_description
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if repository_owner is not None:
            self._values["repository_owner"] = repository_owner

    @builtins.property
    def code(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGitHubRepositoryPropsMixin.CodeProperty"]]:
        '''Information about code to be committed to a repository after it is created in an CloudFormation stack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGitHubRepositoryPropsMixin.CodeProperty"]], result)

    @builtins.property
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-connectionarn
        '''
        result = self._values.get("connection_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_issues(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether to enable issues for the GitHub repository.

        You can use GitHub issues to track information and bugs for your repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-enableissues
        '''
        result = self._values.get("enable_issues")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def is_private(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the GitHub repository is a private repository.

        If so, you choose who can see and commit to this repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-isprivate
        '''
        result = self._values.get("is_private")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def repository_access_token(self) -> typing.Optional[builtins.str]:
        '''The GitHub user's personal access token for the GitHub repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryaccesstoken
        '''
        result = self._values.get("repository_access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_description(self) -> typing.Optional[builtins.str]:
        '''A comment or description about the new repository.

        This description is displayed in GitHub after the repository is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositorydescription
        '''
        result = self._values.get("repository_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''The name of the repository you want to create in GitHub with CloudFormation stack creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryname
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_owner(self) -> typing.Optional[builtins.str]:
        '''The GitHub user name for the owner of the GitHub repository to be created.

        If this repository should be owned by a GitHub organization, provide its name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryowner
        '''
        result = self._values.get("repository_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGitHubRepositoryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGitHubRepositoryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codestar.mixins.CfnGitHubRepositoryPropsMixin",
):
    '''The ``AWS::CodeStar::GitHubRepository`` resource creates a GitHub repository where users can store source code for use with AWS workflows.

    You must provide a location for the source code ZIP file in the CloudFormation template, so the code can be uploaded to the created repository. You must have created a personal access token in GitHub to provide in the CloudFormation template. AWS uses this token to connect to GitHub on your behalf.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html
    :cloudformationResource: AWS::CodeStar::GitHubRepository
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codestar import mixins as codestar_mixins
        
        cfn_git_hub_repository_props_mixin = codestar_mixins.CfnGitHubRepositoryPropsMixin(codestar_mixins.CfnGitHubRepositoryMixinProps(
            code=codestar_mixins.CfnGitHubRepositoryPropsMixin.CodeProperty(
                s3=codestar_mixins.CfnGitHubRepositoryPropsMixin.S3Property(
                    bucket="bucket",
                    key="key",
                    object_version="objectVersion"
                )
            ),
            connection_arn="connectionArn",
            enable_issues=False,
            is_private=False,
            repository_access_token="repositoryAccessToken",
            repository_description="repositoryDescription",
            repository_name="repositoryName",
            repository_owner="repositoryOwner"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGitHubRepositoryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeStar::GitHubRepository``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708a6587c74c3aab8107190407e41ad5647ebe4de3332f9c10aa99bfc9cac708)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d43fe04b4e0158444527b577862002f7e4e0b4b83bc4cd4189989a1751e479ed)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb14b2e2d4551ec58b393a746ccae4731fb110f6491c6338cd8fda508da8a29)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGitHubRepositoryMixinProps:
        return typing.cast(CfnGitHubRepositoryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codestar.mixins.CfnGitHubRepositoryPropsMixin.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGitHubRepositoryPropsMixin.S3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``Code`` property type specifies information about code to be committed.

            ``Code`` is a property of the ``AWS::CodeStar::GitHubRepository`` resource.

            :param s3: Information about the Amazon S3 bucket that contains a ZIP file of code to be committed to the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-code.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codestar import mixins as codestar_mixins
                
                code_property = codestar_mixins.CfnGitHubRepositoryPropsMixin.CodeProperty(
                    s3=codestar_mixins.CfnGitHubRepositoryPropsMixin.S3Property(
                        bucket="bucket",
                        key="key",
                        object_version="objectVersion"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f461bc40eea3c86f2b71c549e641a8bfc8e6f2b506a6e52d0f70a7bd4b7f96b1)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGitHubRepositoryPropsMixin.S3Property"]]:
            '''Information about the Amazon S3 bucket that contains a ZIP file of code to be committed to the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-code.html#cfn-codestar-githubrepository-code-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGitHubRepositoryPropsMixin.S3Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codestar.mixins.CfnGitHubRepositoryPropsMixin.S3Property",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key": "key",
            "object_version": "objectVersion",
        },
    )
    class S3Property:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``S3`` property type specifies information about the Amazon S3 bucket that contains the code to be committed to the new repository.

            ``S3`` is a property of the ``AWS::CodeStar::GitHubRepository`` resource.

            :param bucket: The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.
            :param key: The S3 object key or file name for the ZIP file.
            :param object_version: The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codestar import mixins as codestar_mixins
                
                s3_property = codestar_mixins.CfnGitHubRepositoryPropsMixin.S3Property(
                    bucket="bucket",
                    key="key",
                    object_version="objectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59da16859ce61f42ee16f03ca85b17fa9360a941ff75601c8f7fdcc6b71d9d19)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument object_version", value=object_version, expected_type=type_hints["object_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key
            if object_version is not None:
                self._values["object_version"] = object_version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html#cfn-codestar-githubrepository-s3-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The S3 object key or file name for the ZIP file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html#cfn-codestar-githubrepository-s3-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            '''The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html#cfn-codestar-githubrepository-s3-objectversion
            '''
            result = self._values.get("object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnGitHubRepositoryMixinProps",
    "CfnGitHubRepositoryPropsMixin",
]

publication.publish()

def _typecheckingstub__80f8c3f7f6221553578a7cccbb58615e799edb70d15adf7701ea4f0ef8e1cf50(
    *,
    code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGitHubRepositoryPropsMixin.CodeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connection_arn: typing.Optional[builtins.str] = None,
    enable_issues: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_private: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    repository_access_token: typing.Optional[builtins.str] = None,
    repository_description: typing.Optional[builtins.str] = None,
    repository_name: typing.Optional[builtins.str] = None,
    repository_owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708a6587c74c3aab8107190407e41ad5647ebe4de3332f9c10aa99bfc9cac708(
    props: typing.Union[CfnGitHubRepositoryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43fe04b4e0158444527b577862002f7e4e0b4b83bc4cd4189989a1751e479ed(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb14b2e2d4551ec58b393a746ccae4731fb110f6491c6338cd8fda508da8a29(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f461bc40eea3c86f2b71c549e641a8bfc8e6f2b506a6e52d0f70a7bd4b7f96b1(
    *,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGitHubRepositoryPropsMixin.S3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59da16859ce61f42ee16f03ca85b17fa9360a941ff75601c8f7fdcc6b71d9d19(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
