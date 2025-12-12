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
    jsii_type="@aws-cdk/mixins-preview.aws_codestarconnections.mixins.CfnConnectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_name": "connectionName",
        "host_arn": "hostArn",
        "provider_type": "providerType",
        "tags": "tags",
    },
)
class CfnConnectionMixinProps:
    def __init__(
        self,
        *,
        connection_name: typing.Optional[builtins.str] = None,
        host_arn: typing.Optional[builtins.str] = None,
        provider_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConnectionPropsMixin.

        :param connection_name: The name of the connection. Connection names must be unique in an AWS account .
        :param host_arn: The Amazon Resource Name (ARN) of the host associated with the connection.
        :param provider_type: The name of the external provider where your third-party code repository is configured.
        :param tags: Specifies the tags applied to the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codestarconnections import mixins as codestarconnections_mixins
            
            cfn_connection_mixin_props = codestarconnections_mixins.CfnConnectionMixinProps(
                connection_name="connectionName",
                host_arn="hostArn",
                provider_type="providerType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5068ba6e1b2d5d68263cc37300e0dc56c5a8c8474a4d858fd71fd41a418642a0)
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument host_arn", value=host_arn, expected_type=type_hints["host_arn"])
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if host_arn is not None:
            self._values["host_arn"] = host_arn
        if provider_type is not None:
            self._values["provider_type"] = provider_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''The name of the connection.

        Connection names must be unique in an AWS account .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-connectionname
        '''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the host associated with the connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-hostarn
        '''
        result = self._values.get("host_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_type(self) -> typing.Optional[builtins.str]:
        '''The name of the external provider where your third-party code repository is configured.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-providertype
        '''
        result = self._values.get("provider_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies the tags applied to the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codestarconnections.mixins.CfnConnectionPropsMixin",
):
    '''The AWS::CodeStarConnections::Connection resource can be used to connect external source providers with services like AWS CodePipeline .

    *Note:* A connection created through CloudFormation is in ``PENDING`` status by default. You can make its status ``AVAILABLE`` by updating the connection in the console.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html
    :cloudformationResource: AWS::CodeStarConnections::Connection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codestarconnections import mixins as codestarconnections_mixins
        
        cfn_connection_props_mixin = codestarconnections_mixins.CfnConnectionPropsMixin(codestarconnections_mixins.CfnConnectionMixinProps(
            connection_name="connectionName",
            host_arn="hostArn",
            provider_type="providerType",
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
        props: typing.Union[CfnConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeStarConnections::Connection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efaa74b20242a3772693bb95825c12291b73e92e6a67f29582d67c57e2b1165e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__015dd57d1fb2da29332679c2db9e03fe92d7c15b4d704784e1aef6f2d0d1ab77)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0978591205252c8d67d217a6d860da4d651a1c21aeeb4458b6dbf81574a89b37)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectionMixinProps:
        return typing.cast(CfnConnectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_codestarconnections.mixins.CfnRepositoryLinkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_arn": "connectionArn",
        "encryption_key_arn": "encryptionKeyArn",
        "owner_id": "ownerId",
        "repository_name": "repositoryName",
        "tags": "tags",
    },
)
class CfnRepositoryLinkMixinProps:
    def __init__(
        self,
        *,
        connection_arn: typing.Optional[builtins.str] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        owner_id: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRepositoryLinkPropsMixin.

        :param connection_arn: The Amazon Resource Name (ARN) of the connection associated with the repository link.
        :param encryption_key_arn: The Amazon Resource Name (ARN) of the encryption key for the repository associated with the repository link.
        :param owner_id: The owner ID for the repository associated with the repository link, such as the owner ID in GitHub.
        :param repository_name: The name of the repository associated with the repository link.
        :param tags: The tags for the repository to be associated with the repository link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-repositorylink.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codestarconnections import mixins as codestarconnections_mixins
            
            cfn_repository_link_mixin_props = codestarconnections_mixins.CfnRepositoryLinkMixinProps(
                connection_arn="connectionArn",
                encryption_key_arn="encryptionKeyArn",
                owner_id="ownerId",
                repository_name="repositoryName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2be9aca7d32ac094489a5ab35187bd9b0a910d466353a27e0d2a6b0f9f964299)
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_arn is not None:
            self._values["connection_arn"] = connection_arn
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if owner_id is not None:
            self._values["owner_id"] = owner_id
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the connection associated with the repository link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-repositorylink.html#cfn-codestarconnections-repositorylink-connectionarn
        '''
        result = self._values.get("connection_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the encryption key for the repository associated with the repository link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-repositorylink.html#cfn-codestarconnections-repositorylink-encryptionkeyarn
        '''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_id(self) -> typing.Optional[builtins.str]:
        '''The owner ID for the repository associated with the repository link, such as the owner ID in GitHub.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-repositorylink.html#cfn-codestarconnections-repositorylink-ownerid
        '''
        result = self._values.get("owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''The name of the repository associated with the repository link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-repositorylink.html#cfn-codestarconnections-repositorylink-repositoryname
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the repository to be associated with the repository link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-repositorylink.html#cfn-codestarconnections-repositorylink-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryLinkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRepositoryLinkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codestarconnections.mixins.CfnRepositoryLinkPropsMixin",
):
    '''Information about the repository link resource, such as the repository link ARN, the associated connection ARN, encryption key ARN, and owner ID.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-repositorylink.html
    :cloudformationResource: AWS::CodeStarConnections::RepositoryLink
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codestarconnections import mixins as codestarconnections_mixins
        
        cfn_repository_link_props_mixin = codestarconnections_mixins.CfnRepositoryLinkPropsMixin(codestarconnections_mixins.CfnRepositoryLinkMixinProps(
            connection_arn="connectionArn",
            encryption_key_arn="encryptionKeyArn",
            owner_id="ownerId",
            repository_name="repositoryName",
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
        props: typing.Union[CfnRepositoryLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeStarConnections::RepositoryLink``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94052a8a197618a8fea1ecdc48c87b33c91f4559e77ee9f7173c815540a7f6e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56b966dfabda04fc14e458f62906c72c9617ec66a9e67bca8f4849482b414302)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b06179e14a210f9aeea87250276ee73ec0e316075e91a8ff3b30abe064d32de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRepositoryLinkMixinProps:
        return typing.cast(CfnRepositoryLinkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_codestarconnections.mixins.CfnSyncConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "config_file": "configFile",
        "publish_deployment_status": "publishDeploymentStatus",
        "repository_link_id": "repositoryLinkId",
        "resource_name": "resourceName",
        "role_arn": "roleArn",
        "sync_type": "syncType",
        "trigger_resource_update_on": "triggerResourceUpdateOn",
    },
)
class CfnSyncConfigurationMixinProps:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        config_file: typing.Optional[builtins.str] = None,
        publish_deployment_status: typing.Optional[builtins.str] = None,
        repository_link_id: typing.Optional[builtins.str] = None,
        resource_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        sync_type: typing.Optional[builtins.str] = None,
        trigger_resource_update_on: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSyncConfigurationPropsMixin.

        :param branch: The branch associated with a specific sync configuration.
        :param config_file: The file path to the configuration file associated with a specific sync configuration. The path should point to an actual file in the sync configurations linked repository.
        :param publish_deployment_status: Whether to enable or disable publishing of deployment status to source providers.
        :param repository_link_id: The ID of the repository link associated with a specific sync configuration.
        :param resource_name: The name of the connection resource associated with a specific sync configuration.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role associated with a specific sync configuration.
        :param sync_type: The type of sync for a specific sync configuration.
        :param trigger_resource_update_on: When to trigger Git sync to begin the stack update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-syncconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codestarconnections import mixins as codestarconnections_mixins
            
            cfn_sync_configuration_mixin_props = codestarconnections_mixins.CfnSyncConfigurationMixinProps(
                branch="branch",
                config_file="configFile",
                publish_deployment_status="publishDeploymentStatus",
                repository_link_id="repositoryLinkId",
                resource_name="resourceName",
                role_arn="roleArn",
                sync_type="syncType",
                trigger_resource_update_on="triggerResourceUpdateOn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d17edc82e87cebb87cd9d7c1b11f67db5928201683b49e75ce757693596bab)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument config_file", value=config_file, expected_type=type_hints["config_file"])
            check_type(argname="argument publish_deployment_status", value=publish_deployment_status, expected_type=type_hints["publish_deployment_status"])
            check_type(argname="argument repository_link_id", value=repository_link_id, expected_type=type_hints["repository_link_id"])
            check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument sync_type", value=sync_type, expected_type=type_hints["sync_type"])
            check_type(argname="argument trigger_resource_update_on", value=trigger_resource_update_on, expected_type=type_hints["trigger_resource_update_on"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch is not None:
            self._values["branch"] = branch
        if config_file is not None:
            self._values["config_file"] = config_file
        if publish_deployment_status is not None:
            self._values["publish_deployment_status"] = publish_deployment_status
        if repository_link_id is not None:
            self._values["repository_link_id"] = repository_link_id
        if resource_name is not None:
            self._values["resource_name"] = resource_name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if sync_type is not None:
            self._values["sync_type"] = sync_type
        if trigger_resource_update_on is not None:
            self._values["trigger_resource_update_on"] = trigger_resource_update_on

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''The branch associated with a specific sync configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-syncconfiguration.html#cfn-codestarconnections-syncconfiguration-branch
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_file(self) -> typing.Optional[builtins.str]:
        '''The file path to the configuration file associated with a specific sync configuration.

        The path should point to an actual file in the sync configurations linked repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-syncconfiguration.html#cfn-codestarconnections-syncconfiguration-configfile
        '''
        result = self._values.get("config_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_deployment_status(self) -> typing.Optional[builtins.str]:
        '''Whether to enable or disable publishing of deployment status to source providers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-syncconfiguration.html#cfn-codestarconnections-syncconfiguration-publishdeploymentstatus
        '''
        result = self._values.get("publish_deployment_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_link_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the repository link associated with a specific sync configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-syncconfiguration.html#cfn-codestarconnections-syncconfiguration-repositorylinkid
        '''
        result = self._values.get("repository_link_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_name(self) -> typing.Optional[builtins.str]:
        '''The name of the connection resource associated with a specific sync configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-syncconfiguration.html#cfn-codestarconnections-syncconfiguration-resourcename
        '''
        result = self._values.get("resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role associated with a specific sync configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-syncconfiguration.html#cfn-codestarconnections-syncconfiguration-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_type(self) -> typing.Optional[builtins.str]:
        '''The type of sync for a specific sync configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-syncconfiguration.html#cfn-codestarconnections-syncconfiguration-synctype
        '''
        result = self._values.get("sync_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_resource_update_on(self) -> typing.Optional[builtins.str]:
        '''When to trigger Git sync to begin the stack update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-syncconfiguration.html#cfn-codestarconnections-syncconfiguration-triggerresourceupdateon
        '''
        result = self._values.get("trigger_resource_update_on")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSyncConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSyncConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codestarconnections.mixins.CfnSyncConfigurationPropsMixin",
):
    '''Information, such as repository, branch, provider, and resource names for a specific sync configuration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-syncconfiguration.html
    :cloudformationResource: AWS::CodeStarConnections::SyncConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codestarconnections import mixins as codestarconnections_mixins
        
        cfn_sync_configuration_props_mixin = codestarconnections_mixins.CfnSyncConfigurationPropsMixin(codestarconnections_mixins.CfnSyncConfigurationMixinProps(
            branch="branch",
            config_file="configFile",
            publish_deployment_status="publishDeploymentStatus",
            repository_link_id="repositoryLinkId",
            resource_name="resourceName",
            role_arn="roleArn",
            sync_type="syncType",
            trigger_resource_update_on="triggerResourceUpdateOn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSyncConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeStarConnections::SyncConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18c562ff18ea336fb5765ff116718e428c1bce2f09271cef739ba8403859f95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e5cc5c0356903e41bc4304f0b662aa004661085224a55bafda95acde6023d5d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81908dc3d733b41b9b8bb8340caf32b378d2cf4d32379a5a6a418e0844f0643)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSyncConfigurationMixinProps:
        return typing.cast(CfnSyncConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnConnectionMixinProps",
    "CfnConnectionPropsMixin",
    "CfnRepositoryLinkMixinProps",
    "CfnRepositoryLinkPropsMixin",
    "CfnSyncConfigurationMixinProps",
    "CfnSyncConfigurationPropsMixin",
]

publication.publish()

def _typecheckingstub__5068ba6e1b2d5d68263cc37300e0dc56c5a8c8474a4d858fd71fd41a418642a0(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    host_arn: typing.Optional[builtins.str] = None,
    provider_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efaa74b20242a3772693bb95825c12291b73e92e6a67f29582d67c57e2b1165e(
    props: typing.Union[CfnConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015dd57d1fb2da29332679c2db9e03fe92d7c15b4d704784e1aef6f2d0d1ab77(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0978591205252c8d67d217a6d860da4d651a1c21aeeb4458b6dbf81574a89b37(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be9aca7d32ac094489a5ab35187bd9b0a910d466353a27e0d2a6b0f9f964299(
    *,
    connection_arn: typing.Optional[builtins.str] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
    owner_id: typing.Optional[builtins.str] = None,
    repository_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94052a8a197618a8fea1ecdc48c87b33c91f4559e77ee9f7173c815540a7f6e0(
    props: typing.Union[CfnRepositoryLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b966dfabda04fc14e458f62906c72c9617ec66a9e67bca8f4849482b414302(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b06179e14a210f9aeea87250276ee73ec0e316075e91a8ff3b30abe064d32de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d17edc82e87cebb87cd9d7c1b11f67db5928201683b49e75ce757693596bab(
    *,
    branch: typing.Optional[builtins.str] = None,
    config_file: typing.Optional[builtins.str] = None,
    publish_deployment_status: typing.Optional[builtins.str] = None,
    repository_link_id: typing.Optional[builtins.str] = None,
    resource_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    sync_type: typing.Optional[builtins.str] = None,
    trigger_resource_update_on: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18c562ff18ea336fb5765ff116718e428c1bce2f09271cef739ba8403859f95(
    props: typing.Union[CfnSyncConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5cc5c0356903e41bc4304f0b662aa004661085224a55bafda95acde6023d5d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81908dc3d733b41b9b8bb8340caf32b378d2cf4d32379a5a6a418e0844f0643(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
