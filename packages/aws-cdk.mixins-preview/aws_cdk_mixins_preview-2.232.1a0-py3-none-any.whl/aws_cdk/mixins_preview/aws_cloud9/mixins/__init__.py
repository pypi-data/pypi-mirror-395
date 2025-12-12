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
    jsii_type="@aws-cdk/mixins-preview.aws_cloud9.mixins.CfnEnvironmentEC2MixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "automatic_stop_time_minutes": "automaticStopTimeMinutes",
        "connection_type": "connectionType",
        "description": "description",
        "image_id": "imageId",
        "instance_type": "instanceType",
        "name": "name",
        "owner_arn": "ownerArn",
        "repositories": "repositories",
        "subnet_id": "subnetId",
        "tags": "tags",
    },
)
class CfnEnvironmentEC2MixinProps:
    def __init__(
        self,
        *,
        automatic_stop_time_minutes: typing.Optional[jsii.Number] = None,
        connection_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner_arn: typing.Optional[builtins.str] = None,
        repositories: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentEC2PropsMixin.RepositoryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEnvironmentEC2PropsMixin.

        :param automatic_stop_time_minutes: The number of minutes until the running instance is shut down after the environment was last used.
        :param connection_type: The connection type used for connecting to an Amazon EC2 environment. Valid values are ``CONNECT_SSH`` (default) and ``CONNECT_SSM`` (connected through AWS Systems Manager ).
        :param description: The description of the environment to create.
        :param image_id: The identifier for the Amazon Machine Image (AMI) that's used to create the EC2 instance. To choose an AMI for the instance, you must specify a valid AMI alias or a valid AWS Systems Manager path. From December 04, 2023, you will be required to include the ``ImageId`` parameter for the ``CreateEnvironmentEC2`` action. This change will be reflected across all direct methods of communicating with the API, such as AWS SDK, AWS CLI and AWS CloudFormation. This change will only affect direct API consumers, and not AWS Cloud9 console users. Since Ubuntu 18.04 has ended standard support as of May 31, 2023, we recommend you choose Ubuntu 22.04. *AMI aliases* - Amazon Linux 2: ``amazonlinux-2-x86_64`` - Amazon Linux 2023 (recommended): ``amazonlinux-2023-x86_64`` - Ubuntu 18.04: ``ubuntu-18.04-x86_64`` - Ubuntu 22.04: ``ubuntu-22.04-x86_64`` *SSM paths* - Amazon Linux 2: ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-2-x86_64`` - Amazon Linux 2023 (recommended): ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-2023-x86_64`` - Ubuntu 18.04: ``resolve:ssm:/aws/service/cloud9/amis/ubuntu-18.04-x86_64`` - Ubuntu 22.04: ``resolve:ssm:/aws/service/cloud9/amis/ubuntu-22.04-x86_64``
        :param instance_type: The type of instance to connect to the environment (for example, ``t2.micro`` ).
        :param name: The name of the environment.
        :param owner_arn: The Amazon Resource Name (ARN) of the environment owner. This ARN can be the ARN of any AWS Identity and Access Management principal. If this value is not specified, the ARN defaults to this environment's creator.
        :param repositories: Any AWS CodeCommit source code repositories to be cloned into the development environment.
        :param subnet_id: The ID of the subnet in Amazon Virtual Private Cloud (Amazon VPC) that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.
        :param tags: An array of key-value pairs that will be associated with the new AWS Cloud9 development environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloud9 import mixins as cloud9_mixins
            
            cfn_environment_eC2_mixin_props = cloud9_mixins.CfnEnvironmentEC2MixinProps(
                automatic_stop_time_minutes=123,
                connection_type="connectionType",
                description="description",
                image_id="imageId",
                instance_type="instanceType",
                name="name",
                owner_arn="ownerArn",
                repositories=[cloud9_mixins.CfnEnvironmentEC2PropsMixin.RepositoryProperty(
                    path_component="pathComponent",
                    repository_url="repositoryUrl"
                )],
                subnet_id="subnetId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee9c9559cebb31dba5ce8c5de43b46b91416df9cdb1c34c6d662d348d267503)
            check_type(argname="argument automatic_stop_time_minutes", value=automatic_stop_time_minutes, expected_type=type_hints["automatic_stop_time_minutes"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner_arn", value=owner_arn, expected_type=type_hints["owner_arn"])
            check_type(argname="argument repositories", value=repositories, expected_type=type_hints["repositories"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatic_stop_time_minutes is not None:
            self._values["automatic_stop_time_minutes"] = automatic_stop_time_minutes
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if description is not None:
            self._values["description"] = description
        if image_id is not None:
            self._values["image_id"] = image_id
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if name is not None:
            self._values["name"] = name
        if owner_arn is not None:
            self._values["owner_arn"] = owner_arn
        if repositories is not None:
            self._values["repositories"] = repositories
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def automatic_stop_time_minutes(self) -> typing.Optional[jsii.Number]:
        '''The number of minutes until the running instance is shut down after the environment was last used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-automaticstoptimeminutes
        '''
        result = self._values.get("automatic_stop_time_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def connection_type(self) -> typing.Optional[builtins.str]:
        '''The connection type used for connecting to an Amazon EC2 environment.

        Valid values are ``CONNECT_SSH`` (default) and ``CONNECT_SSM`` (connected through AWS Systems Manager ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-connectiontype
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the environment to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for the Amazon Machine Image (AMI) that's used to create the EC2 instance.

        To choose an AMI for the instance, you must specify a valid AMI alias or a valid AWS Systems Manager path.

        From December 04, 2023, you will be required to include the ``ImageId`` parameter for the ``CreateEnvironmentEC2`` action. This change will be reflected across all direct methods of communicating with the API, such as AWS SDK, AWS CLI and AWS CloudFormation. This change will only affect direct API consumers, and not AWS Cloud9 console users.

        Since Ubuntu 18.04 has ended standard support as of May 31, 2023, we recommend you choose Ubuntu 22.04.

        *AMI aliases*

        - Amazon Linux 2: ``amazonlinux-2-x86_64``
        - Amazon Linux 2023 (recommended): ``amazonlinux-2023-x86_64``
        - Ubuntu 18.04: ``ubuntu-18.04-x86_64``
        - Ubuntu 22.04: ``ubuntu-22.04-x86_64``

        *SSM paths*

        - Amazon Linux 2: ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-2-x86_64``
        - Amazon Linux 2023 (recommended): ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-2023-x86_64``
        - Ubuntu 18.04: ``resolve:ssm:/aws/service/cloud9/amis/ubuntu-18.04-x86_64``
        - Ubuntu 22.04: ``resolve:ssm:/aws/service/cloud9/amis/ubuntu-22.04-x86_64``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-imageid
        '''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The type of instance to connect to the environment (for example, ``t2.micro`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the environment owner.

        This ARN can be the ARN of any AWS Identity and Access Management principal. If this value is not specified, the ARN defaults to this environment's creator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-ownerarn
        '''
        result = self._values.get("owner_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repositories(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentEC2PropsMixin.RepositoryProperty"]]]]:
        '''Any AWS CodeCommit source code repositories to be cloned into the development environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-repositories
        '''
        result = self._values.get("repositories")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentEC2PropsMixin.RepositoryProperty"]]]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the subnet in Amazon Virtual Private Cloud (Amazon VPC) that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-subnetid
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs that will be associated with the new AWS Cloud9 development environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentEC2MixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentEC2PropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloud9.mixins.CfnEnvironmentEC2PropsMixin",
):
    '''The ``AWS::Cloud9::EnvironmentEC2`` resource creates an Amazon EC2 development environment in AWS Cloud9 .

    For more information, see `Creating an Environment <https://docs.aws.amazon.com/cloud9/latest/user-guide/create-environment.html>`_ in the *AWS Cloud9 User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html
    :cloudformationResource: AWS::Cloud9::EnvironmentEC2
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloud9 import mixins as cloud9_mixins
        
        cfn_environment_eC2_props_mixin = cloud9_mixins.CfnEnvironmentEC2PropsMixin(cloud9_mixins.CfnEnvironmentEC2MixinProps(
            automatic_stop_time_minutes=123,
            connection_type="connectionType",
            description="description",
            image_id="imageId",
            instance_type="instanceType",
            name="name",
            owner_arn="ownerArn",
            repositories=[cloud9_mixins.CfnEnvironmentEC2PropsMixin.RepositoryProperty(
                path_component="pathComponent",
                repository_url="repositoryUrl"
            )],
            subnet_id="subnetId",
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
        props: typing.Union[CfnEnvironmentEC2MixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cloud9::EnvironmentEC2``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78cd3c52da9fa02340ae0802cc99b6ca48f31df51627d84255662d111fe68590)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94e76bda9921b9bc097a074527d3d1b2b66bc084bf4fcc437ed3b190a1919281)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874f4981b14e14ff14a8d5b3383b32b13af4df435b33d4e682e7aeece780647b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentEC2MixinProps:
        return typing.cast(CfnEnvironmentEC2MixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloud9.mixins.CfnEnvironmentEC2PropsMixin.RepositoryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "path_component": "pathComponent",
            "repository_url": "repositoryUrl",
        },
    )
    class RepositoryProperty:
        def __init__(
            self,
            *,
            path_component: typing.Optional[builtins.str] = None,
            repository_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Repository`` property type specifies an AWS CodeCommit source code repository to be cloned into an AWS Cloud9 development environment.

            :param path_component: The path within the development environment's default file system location to clone the AWS CodeCommit repository into. For example, ``/REPOSITORY_NAME`` would clone the repository into the ``/home/USER_NAME/environment/REPOSITORY_NAME`` directory in the environment.
            :param repository_url: The clone URL of the AWS CodeCommit repository to be cloned. For example, for an AWS CodeCommit repository this might be ``https://git-codecommit.us-east-2.amazonaws.com/v1/repos/REPOSITORY_NAME`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloud9-environmentec2-repository.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloud9 import mixins as cloud9_mixins
                
                repository_property = cloud9_mixins.CfnEnvironmentEC2PropsMixin.RepositoryProperty(
                    path_component="pathComponent",
                    repository_url="repositoryUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2bc722165dae77751671664373a26876f6874a38b4c6cbf740e7c337c860672)
                check_type(argname="argument path_component", value=path_component, expected_type=type_hints["path_component"])
                check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if path_component is not None:
                self._values["path_component"] = path_component
            if repository_url is not None:
                self._values["repository_url"] = repository_url

        @builtins.property
        def path_component(self) -> typing.Optional[builtins.str]:
            '''The path within the development environment's default file system location to clone the AWS CodeCommit repository into.

            For example, ``/REPOSITORY_NAME`` would clone the repository into the ``/home/USER_NAME/environment/REPOSITORY_NAME`` directory in the environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloud9-environmentec2-repository.html#cfn-cloud9-environmentec2-repository-pathcomponent
            '''
            result = self._values.get("path_component")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def repository_url(self) -> typing.Optional[builtins.str]:
            '''The clone URL of the AWS CodeCommit repository to be cloned.

            For example, for an AWS CodeCommit repository this might be ``https://git-codecommit.us-east-2.amazonaws.com/v1/repos/REPOSITORY_NAME`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloud9-environmentec2-repository.html#cfn-cloud9-environmentec2-repository-repositoryurl
            '''
            result = self._values.get("repository_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RepositoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnEnvironmentEC2MixinProps",
    "CfnEnvironmentEC2PropsMixin",
]

publication.publish()

def _typecheckingstub__9ee9c9559cebb31dba5ce8c5de43b46b91416df9cdb1c34c6d662d348d267503(
    *,
    automatic_stop_time_minutes: typing.Optional[jsii.Number] = None,
    connection_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    owner_arn: typing.Optional[builtins.str] = None,
    repositories: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentEC2PropsMixin.RepositoryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78cd3c52da9fa02340ae0802cc99b6ca48f31df51627d84255662d111fe68590(
    props: typing.Union[CfnEnvironmentEC2MixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e76bda9921b9bc097a074527d3d1b2b66bc084bf4fcc437ed3b190a1919281(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874f4981b14e14ff14a8d5b3383b32b13af4df435b33d4e682e7aeece780647b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bc722165dae77751671664373a26876f6874a38b4c6cbf740e7c337c860672(
    *,
    path_component: typing.Optional[builtins.str] = None,
    repository_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
