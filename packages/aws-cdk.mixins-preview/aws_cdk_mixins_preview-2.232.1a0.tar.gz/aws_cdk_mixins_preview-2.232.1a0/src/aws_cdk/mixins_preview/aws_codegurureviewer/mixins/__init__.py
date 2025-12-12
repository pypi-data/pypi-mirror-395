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
    jsii_type="@aws-cdk/mixins-preview.aws_codegurureviewer.mixins.CfnRepositoryAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "connection_arn": "connectionArn",
        "name": "name",
        "owner": "owner",
        "tags": "tags",
        "type": "type",
    },
)
class CfnRepositoryAssociationMixinProps:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        connection_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRepositoryAssociationPropsMixin.

        :param bucket_name: The name of the bucket. This is required for your S3Bucket repository. The name must start with the prefix ``codeguru-reviewer-*`` .
        :param connection_arn: The Amazon Resource Name (ARN) of an AWS CodeStar Connections connection. Its format is ``arn:aws:codestar-connections:region-id:aws-account_id:connection/connection-id`` . For more information, see `Connection <https://docs.aws.amazon.com/codestar-connections/latest/APIReference/API_Connection.html>`_ in the *AWS CodeStar Connections API Reference* . ``ConnectionArn`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.
        :param name: The name of the repository.
        :param owner: The owner of the repository. For a GitHub Enterprise Server or Bitbucket repository, this is the username for the account that owns the repository. ``Owner`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.
        :param tags: An array of key-value pairs used to tag an associated repository. A tag is a custom attribute label with two parts: - A *tag key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag keys are case sensitive. - An optional field known as a *tag value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag value is the same as using an empty string. Like tag keys, tag values are case sensitive.
        :param type: The type of repository that contains the source code to be reviewed. The valid values are:. - ``CodeCommit`` - ``Bitbucket`` - ``GitHubEnterpriseServer`` - ``S3Bucket``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codegurureviewer import mixins as codegurureviewer_mixins
            
            cfn_repository_association_mixin_props = codegurureviewer_mixins.CfnRepositoryAssociationMixinProps(
                bucket_name="bucketName",
                connection_arn="connectionArn",
                name="name",
                owner="owner",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a990251200528f6f6de7c6b8d8e8d0015207c207743da915fc690e53390ba89c)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if connection_arn is not None:
            self._values["connection_arn"] = connection_arn
        if name is not None:
            self._values["name"] = name
        if owner is not None:
            self._values["owner"] = owner
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the bucket.

        This is required for your S3Bucket repository. The name must start with the prefix ``codeguru-reviewer-*`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-bucketname
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an AWS CodeStar Connections connection.

        Its format is ``arn:aws:codestar-connections:region-id:aws-account_id:connection/connection-id`` . For more information, see `Connection <https://docs.aws.amazon.com/codestar-connections/latest/APIReference/API_Connection.html>`_ in the *AWS CodeStar Connections API Reference* .

        ``ConnectionArn`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-connectionarn
        '''
        result = self._values.get("connection_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''The owner of the repository.

        For a GitHub Enterprise Server or Bitbucket repository, this is the username for the account that owns the repository.

        ``Owner`` must be specified for Bitbucket and GitHub Enterprise Server repositories. It has no effect if it is specified for an AWS CodeCommit repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-owner
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs used to tag an associated repository.

        A tag is a custom attribute label with two parts:

        - A *tag key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag keys are case sensitive.
        - An optional field known as a *tag value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag value is the same as using an empty string. Like tag keys, tag values are case sensitive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of repository that contains the source code to be reviewed. The valid values are:.

        - ``CodeCommit``
        - ``Bitbucket``
        - ``GitHubEnterpriseServer``
        - ``S3Bucket``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRepositoryAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codegurureviewer.mixins.CfnRepositoryAssociationPropsMixin",
):
    '''This resource configures how Amazon CodeGuru Reviewer retrieves the source code to be reviewed.

    You can use an AWS CloudFormation template to create an association with the following repository types:

    - AWS CodeCommit - For more information, see `Create an AWS CodeCommit repository association <https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/create-codecommit-association.html>`_ in the *Amazon CodeGuru Reviewer User Guide* .
    - Bitbucket - For more information, see `Create a Bitbucket repository association <https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/create-bitbucket-association.html>`_ in the *Amazon CodeGuru Reviewer User Guide* .
    - GitHub Enterprise Server - For more information, see `Create a GitHub Enterprise Server repository association <https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/create-github-enterprise-association.html>`_ in the *Amazon CodeGuru Reviewer User Guide* .
    - S3Bucket - For more information, see `Create code reviews with GitHub Actions <https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/working-with-cicd.html>`_ in the *Amazon CodeGuru Reviewer User Guide* .

    .. epigraph::

       You cannot use a CloudFormation template to create an association with a GitHub repository.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html
    :cloudformationResource: AWS::CodeGuruReviewer::RepositoryAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codegurureviewer import mixins as codegurureviewer_mixins
        
        cfn_repository_association_props_mixin = codegurureviewer_mixins.CfnRepositoryAssociationPropsMixin(codegurureviewer_mixins.CfnRepositoryAssociationMixinProps(
            bucket_name="bucketName",
            connection_arn="connectionArn",
            name="name",
            owner="owner",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRepositoryAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeGuruReviewer::RepositoryAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c87bb1af98c38c1ed14383e459570dd84d88aa73e11ede0eaea289cb869dc68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0bcf2637fde593b305de95f910ac9111209fa9eabdbdc47dcd1ea84a79300a3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c8075acd4ee06ca02011cd7739adfb9423acfdc7dc533420cfe02f6114cd47)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRepositoryAssociationMixinProps:
        return typing.cast(CfnRepositoryAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnRepositoryAssociationMixinProps",
    "CfnRepositoryAssociationPropsMixin",
]

publication.publish()

def _typecheckingstub__a990251200528f6f6de7c6b8d8e8d0015207c207743da915fc690e53390ba89c(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    connection_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c87bb1af98c38c1ed14383e459570dd84d88aa73e11ede0eaea289cb869dc68(
    props: typing.Union[CfnRepositoryAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bcf2637fde593b305de95f910ac9111209fa9eabdbdc47dcd1ea84a79300a3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c8075acd4ee06ca02011cd7739adfb9423acfdc7dc533420cfe02f6114cd47(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
