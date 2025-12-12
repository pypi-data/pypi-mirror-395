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
    jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnConnectionAliasMixinProps",
    jsii_struct_bases=[],
    name_mapping={"connection_string": "connectionString", "tags": "tags"},
)
class CfnConnectionAliasMixinProps:
    def __init__(
        self,
        *,
        connection_string: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConnectionAliasPropsMixin.

        :param connection_string: The connection string specified for the connection alias. The connection string must be in the form of a fully qualified domain name (FQDN), such as ``www.example.com`` .
        :param tags: The tags to associate with the connection alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-connectionalias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
            
            cfn_connection_alias_mixin_props = workspaces_mixins.CfnConnectionAliasMixinProps(
                connection_string="connectionString",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07c8e43319127364f5b0c7600066c1219a00c7cf5a3b3b78c3a1c8505393b6d)
            check_type(argname="argument connection_string", value=connection_string, expected_type=type_hints["connection_string"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_string is not None:
            self._values["connection_string"] = connection_string
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connection_string(self) -> typing.Optional[builtins.str]:
        '''The connection string specified for the connection alias.

        The connection string must be in the form of a fully qualified domain name (FQDN), such as ``www.example.com`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-connectionalias.html#cfn-workspaces-connectionalias-connectionstring
        '''
        result = self._values.get("connection_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to associate with the connection alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-connectionalias.html#cfn-workspaces-connectionalias-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectionAliasMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectionAliasPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnConnectionAliasPropsMixin",
):
    '''The ``AWS::WorkSpaces::ConnectionAlias`` resource specifies a connection alias.

    Connection aliases are used for cross-Region redirection. For more information, see `Cross-Region Redirection for Amazon WorkSpaces <https://docs.aws.amazon.com/workspaces/latest/adminguide/cross-region-redirection.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-connectionalias.html
    :cloudformationResource: AWS::WorkSpaces::ConnectionAlias
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
        
        cfn_connection_alias_props_mixin = workspaces_mixins.CfnConnectionAliasPropsMixin(workspaces_mixins.CfnConnectionAliasMixinProps(
            connection_string="connectionString",
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
        props: typing.Union[CfnConnectionAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpaces::ConnectionAlias``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea35a199fe42702b693aabb98bdb788360093aa91ededc3d3ecb3f88eb6c3eaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8643f9ed53003832f22011fc0aab16bb441a0ada8970be6ed8b5e07f3a1f4c8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3536469eb40003042af9b0a9eda14d441889d164c96460d5cbc99561fbfe5b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectionAliasMixinProps:
        return typing.cast(CfnConnectionAliasMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnConnectionAliasPropsMixin.ConnectionAliasAssociationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "associated_account_id": "associatedAccountId",
            "association_status": "associationStatus",
            "connection_identifier": "connectionIdentifier",
            "resource_id": "resourceId",
        },
    )
    class ConnectionAliasAssociationProperty:
        def __init__(
            self,
            *,
            associated_account_id: typing.Optional[builtins.str] = None,
            association_status: typing.Optional[builtins.str] = None,
            connection_identifier: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a connection alias association that is used for cross-Region redirection.

            For more information, see `Cross-Region Redirection for Amazon WorkSpaces <https://docs.aws.amazon.com/workspaces/latest/adminguide/cross-region-redirection.html>`_ .

            :param associated_account_id: The identifier of the AWS account that associated the connection alias with a directory.
            :param association_status: The association status of the connection alias.
            :param connection_identifier: The identifier of the connection alias association. You use the connection identifier in the DNS TXT record when you're configuring your DNS routing policies.
            :param resource_id: The identifier of the directory associated with a connection alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-connectionalias-connectionaliasassociation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
                
                connection_alias_association_property = workspaces_mixins.CfnConnectionAliasPropsMixin.ConnectionAliasAssociationProperty(
                    associated_account_id="associatedAccountId",
                    association_status="associationStatus",
                    connection_identifier="connectionIdentifier",
                    resource_id="resourceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5080543c3ed5a3332bd598f7666d0478f7ec150fe4b17ec00adf60644a798f51)
                check_type(argname="argument associated_account_id", value=associated_account_id, expected_type=type_hints["associated_account_id"])
                check_type(argname="argument association_status", value=association_status, expected_type=type_hints["association_status"])
                check_type(argname="argument connection_identifier", value=connection_identifier, expected_type=type_hints["connection_identifier"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if associated_account_id is not None:
                self._values["associated_account_id"] = associated_account_id
            if association_status is not None:
                self._values["association_status"] = association_status
            if connection_identifier is not None:
                self._values["connection_identifier"] = connection_identifier
            if resource_id is not None:
                self._values["resource_id"] = resource_id

        @builtins.property
        def associated_account_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the AWS account that associated the connection alias with a directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-connectionalias-connectionaliasassociation.html#cfn-workspaces-connectionalias-connectionaliasassociation-associatedaccountid
            '''
            result = self._values.get("associated_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def association_status(self) -> typing.Optional[builtins.str]:
            '''The association status of the connection alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-connectionalias-connectionaliasassociation.html#cfn-workspaces-connectionalias-connectionaliasassociation-associationstatus
            '''
            result = self._values.get("association_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connection_identifier(self) -> typing.Optional[builtins.str]:
            '''The identifier of the connection alias association.

            You use the connection identifier in the DNS TXT record when you're configuring your DNS routing policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-connectionalias-connectionaliasassociation.html#cfn-workspaces-connectionalias-connectionaliasassociation-connectionidentifier
            '''
            result = self._values.get("connection_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the directory associated with a connection alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-connectionalias-connectionaliasassociation.html#cfn-workspaces-connectionalias-connectionaliasassociation-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionAliasAssociationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnWorkspaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bundle_id": "bundleId",
        "directory_id": "directoryId",
        "root_volume_encryption_enabled": "rootVolumeEncryptionEnabled",
        "tags": "tags",
        "user_name": "userName",
        "user_volume_encryption_enabled": "userVolumeEncryptionEnabled",
        "volume_encryption_key": "volumeEncryptionKey",
        "workspace_properties": "workspaceProperties",
    },
)
class CfnWorkspaceMixinProps:
    def __init__(
        self,
        *,
        bundle_id: typing.Optional[builtins.str] = None,
        directory_id: typing.Optional[builtins.str] = None,
        root_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_name: typing.Optional[builtins.str] = None,
        user_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        volume_encryption_key: typing.Optional[builtins.str] = None,
        workspace_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.WorkspacePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWorkspacePropsMixin.

        :param bundle_id: The identifier of the bundle for the WorkSpace.
        :param directory_id: The identifier of the Directory Service directory for the WorkSpace.
        :param root_volume_encryption_enabled: Indicates whether the data stored on the root volume is encrypted.
        :param tags: The tags for the WorkSpace.
        :param user_name: The user name of the user for the WorkSpace. This user name must exist in the Directory Service directory for the WorkSpace.
        :param user_volume_encryption_enabled: Indicates whether the data stored on the user volume is encrypted.
        :param volume_encryption_key: The symmetric AWS KMS key used to encrypt data stored on your WorkSpace. Amazon WorkSpaces does not support asymmetric KMS keys.
        :param workspace_properties: The WorkSpace properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
            
            cfn_workspace_mixin_props = workspaces_mixins.CfnWorkspaceMixinProps(
                bundle_id="bundleId",
                directory_id="directoryId",
                root_volume_encryption_enabled=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_name="userName",
                user_volume_encryption_enabled=False,
                volume_encryption_key="volumeEncryptionKey",
                workspace_properties=workspaces_mixins.CfnWorkspacePropsMixin.WorkspacePropertiesProperty(
                    compute_type_name="computeTypeName",
                    root_volume_size_gib=123,
                    running_mode="runningMode",
                    running_mode_auto_stop_timeout_in_minutes=123,
                    user_volume_size_gib=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed608a58c84bd30dc947b4c9c4ef47d01595375e8aba4651458548d8f2f41e7)
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument root_volume_encryption_enabled", value=root_volume_encryption_enabled, expected_type=type_hints["root_volume_encryption_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument user_volume_encryption_enabled", value=user_volume_encryption_enabled, expected_type=type_hints["user_volume_encryption_enabled"])
            check_type(argname="argument volume_encryption_key", value=volume_encryption_key, expected_type=type_hints["volume_encryption_key"])
            check_type(argname="argument workspace_properties", value=workspace_properties, expected_type=type_hints["workspace_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if directory_id is not None:
            self._values["directory_id"] = directory_id
        if root_volume_encryption_enabled is not None:
            self._values["root_volume_encryption_enabled"] = root_volume_encryption_enabled
        if tags is not None:
            self._values["tags"] = tags
        if user_name is not None:
            self._values["user_name"] = user_name
        if user_volume_encryption_enabled is not None:
            self._values["user_volume_encryption_enabled"] = user_volume_encryption_enabled
        if volume_encryption_key is not None:
            self._values["volume_encryption_key"] = volume_encryption_key
        if workspace_properties is not None:
            self._values["workspace_properties"] = workspace_properties

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the bundle for the WorkSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Directory Service directory for the WorkSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-directoryid
        '''
        result = self._values.get("directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_volume_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the data stored on the root volume is encrypted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-rootvolumeencryptionenabled
        '''
        result = self._values.get("root_volume_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the WorkSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The user name of the user for the WorkSpace.

        This user name must exist in the Directory Service directory for the WorkSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-username
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_volume_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the data stored on the user volume is encrypted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-uservolumeencryptionenabled
        '''
        result = self._values.get("user_volume_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def volume_encryption_key(self) -> typing.Optional[builtins.str]:
        '''The symmetric AWS KMS key used to encrypt data stored on your WorkSpace.

        Amazon WorkSpaces does not support asymmetric KMS keys.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-volumeencryptionkey
        '''
        result = self._values.get("volume_encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.WorkspacePropertiesProperty"]]:
        '''The WorkSpace properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-workspaceproperties
        '''
        result = self._values.get("workspace_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.WorkspacePropertiesProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkspacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnWorkspacePropsMixin",
):
    '''The ``AWS::WorkSpaces::Workspace`` resource specifies a WorkSpace.

    Updates are not supported for the ``BundleId`` , ``RootVolumeEncryptionEnabled`` , ``UserVolumeEncryptionEnabled`` , or ``VolumeEncryptionKey`` properties. To update these properties, you must also update a property that triggers a replacement, such as the ``UserName`` property.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html
    :cloudformationResource: AWS::WorkSpaces::Workspace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
        
        cfn_workspace_props_mixin = workspaces_mixins.CfnWorkspacePropsMixin(workspaces_mixins.CfnWorkspaceMixinProps(
            bundle_id="bundleId",
            directory_id="directoryId",
            root_volume_encryption_enabled=False,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_name="userName",
            user_volume_encryption_enabled=False,
            volume_encryption_key="volumeEncryptionKey",
            workspace_properties=workspaces_mixins.CfnWorkspacePropsMixin.WorkspacePropertiesProperty(
                compute_type_name="computeTypeName",
                root_volume_size_gib=123,
                running_mode="runningMode",
                running_mode_auto_stop_timeout_in_minutes=123,
                user_volume_size_gib=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWorkspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpaces::Workspace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__127819a5e0ddbab47646803e0459741156c1b547a4434efb8fc2a63cc663de10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86447719e6fc9f919cdf422557323ba5984a304dc3068ac575b244e4a1b209b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90352b517fbe1733c5ee5c9aba8fef521a8dad34fb0370a494be31030d442abe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkspaceMixinProps:
        return typing.cast(CfnWorkspaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnWorkspacePropsMixin.WorkspacePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_type_name": "computeTypeName",
            "root_volume_size_gib": "rootVolumeSizeGib",
            "running_mode": "runningMode",
            "running_mode_auto_stop_timeout_in_minutes": "runningModeAutoStopTimeoutInMinutes",
            "user_volume_size_gib": "userVolumeSizeGib",
        },
    )
    class WorkspacePropertiesProperty:
        def __init__(
            self,
            *,
            compute_type_name: typing.Optional[builtins.str] = None,
            root_volume_size_gib: typing.Optional[jsii.Number] = None,
            running_mode: typing.Optional[builtins.str] = None,
            running_mode_auto_stop_timeout_in_minutes: typing.Optional[jsii.Number] = None,
            user_volume_size_gib: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about a WorkSpace.

            :param compute_type_name: The compute type. For more information, see `Amazon WorkSpaces Bundles <https://docs.aws.amazon.com/workspaces/details/#Amazon_WorkSpaces_Bundles>`_ .
            :param root_volume_size_gib: The size of the root volume. For important information about how to modify the size of the root and user volumes, see `Modify a WorkSpace <https://docs.aws.amazon.com/workspaces/latest/adminguide/modify-workspaces.html>`_ .
            :param running_mode: The running mode. For more information, see `Manage the WorkSpace Running Mode <https://docs.aws.amazon.com/workspaces/latest/adminguide/running-mode.html>`_ .
            :param running_mode_auto_stop_timeout_in_minutes: The time after a user logs off when WorkSpaces are automatically stopped. Configured in 60-minute intervals.
            :param user_volume_size_gib: The size of the user storage. For important information about how to modify the size of the root and user volumes, see `Modify a WorkSpace <https://docs.aws.amazon.com/workspaces/latest/adminguide/modify-workspaces.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
                
                workspace_properties_property = workspaces_mixins.CfnWorkspacePropsMixin.WorkspacePropertiesProperty(
                    compute_type_name="computeTypeName",
                    root_volume_size_gib=123,
                    running_mode="runningMode",
                    running_mode_auto_stop_timeout_in_minutes=123,
                    user_volume_size_gib=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dabd5cb2b3a3a819339522bf40e131450ab7863f73ded733526efc368a524ebe)
                check_type(argname="argument compute_type_name", value=compute_type_name, expected_type=type_hints["compute_type_name"])
                check_type(argname="argument root_volume_size_gib", value=root_volume_size_gib, expected_type=type_hints["root_volume_size_gib"])
                check_type(argname="argument running_mode", value=running_mode, expected_type=type_hints["running_mode"])
                check_type(argname="argument running_mode_auto_stop_timeout_in_minutes", value=running_mode_auto_stop_timeout_in_minutes, expected_type=type_hints["running_mode_auto_stop_timeout_in_minutes"])
                check_type(argname="argument user_volume_size_gib", value=user_volume_size_gib, expected_type=type_hints["user_volume_size_gib"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_type_name is not None:
                self._values["compute_type_name"] = compute_type_name
            if root_volume_size_gib is not None:
                self._values["root_volume_size_gib"] = root_volume_size_gib
            if running_mode is not None:
                self._values["running_mode"] = running_mode
            if running_mode_auto_stop_timeout_in_minutes is not None:
                self._values["running_mode_auto_stop_timeout_in_minutes"] = running_mode_auto_stop_timeout_in_minutes
            if user_volume_size_gib is not None:
                self._values["user_volume_size_gib"] = user_volume_size_gib

        @builtins.property
        def compute_type_name(self) -> typing.Optional[builtins.str]:
            '''The compute type.

            For more information, see `Amazon WorkSpaces Bundles <https://docs.aws.amazon.com/workspaces/details/#Amazon_WorkSpaces_Bundles>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html#cfn-workspaces-workspace-workspaceproperties-computetypename
            '''
            result = self._values.get("compute_type_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def root_volume_size_gib(self) -> typing.Optional[jsii.Number]:
            '''The size of the root volume.

            For important information about how to modify the size of the root and user volumes, see `Modify a WorkSpace <https://docs.aws.amazon.com/workspaces/latest/adminguide/modify-workspaces.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html#cfn-workspaces-workspace-workspaceproperties-rootvolumesizegib
            '''
            result = self._values.get("root_volume_size_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def running_mode(self) -> typing.Optional[builtins.str]:
            '''The running mode.

            For more information, see `Manage the WorkSpace Running Mode <https://docs.aws.amazon.com/workspaces/latest/adminguide/running-mode.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html#cfn-workspaces-workspace-workspaceproperties-runningmode
            '''
            result = self._values.get("running_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def running_mode_auto_stop_timeout_in_minutes(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The time after a user logs off when WorkSpaces are automatically stopped.

            Configured in 60-minute intervals.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html#cfn-workspaces-workspace-workspaceproperties-runningmodeautostoptimeoutinminutes
            '''
            result = self._values.get("running_mode_auto_stop_timeout_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def user_volume_size_gib(self) -> typing.Optional[jsii.Number]:
            '''The size of the user storage.

            For important information about how to modify the size of the root and user volumes, see `Modify a WorkSpace <https://docs.aws.amazon.com/workspaces/latest/adminguide/modify-workspaces.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html#cfn-workspaces-workspace-workspaceproperties-uservolumesizegib
            '''
            result = self._values.get("user_volume_size_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkspacePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnWorkspacesPoolMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_settings": "applicationSettings",
        "bundle_id": "bundleId",
        "capacity": "capacity",
        "description": "description",
        "directory_id": "directoryId",
        "pool_name": "poolName",
        "running_mode": "runningMode",
        "tags": "tags",
        "timeout_settings": "timeoutSettings",
    },
)
class CfnWorkspacesPoolMixinProps:
    def __init__(
        self,
        *,
        application_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacesPoolPropsMixin.ApplicationSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        bundle_id: typing.Optional[builtins.str] = None,
        capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacesPoolPropsMixin.CapacityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        directory_id: typing.Optional[builtins.str] = None,
        pool_name: typing.Optional[builtins.str] = None,
        running_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacesPoolPropsMixin.TimeoutSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWorkspacesPoolPropsMixin.

        :param application_settings: The persistent application settings for users of the pool.
        :param bundle_id: The identifier of the bundle used by the pool.
        :param capacity: Describes the user capacity for the pool.
        :param description: The description of the pool.
        :param directory_id: The identifier of the directory used by the pool.
        :param pool_name: The name of the pool.
        :param running_mode: The running mode of the pool.
        :param tags: 
        :param timeout_settings: The amount of time that a pool session remains active after users disconnect. If they try to reconnect to the pool session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new pool instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
            
            cfn_workspaces_pool_mixin_props = workspaces_mixins.CfnWorkspacesPoolMixinProps(
                application_settings=workspaces_mixins.CfnWorkspacesPoolPropsMixin.ApplicationSettingsProperty(
                    settings_group="settingsGroup",
                    status="status"
                ),
                bundle_id="bundleId",
                capacity=workspaces_mixins.CfnWorkspacesPoolPropsMixin.CapacityProperty(
                    desired_user_sessions=123
                ),
                description="description",
                directory_id="directoryId",
                pool_name="poolName",
                running_mode="runningMode",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                timeout_settings=workspaces_mixins.CfnWorkspacesPoolPropsMixin.TimeoutSettingsProperty(
                    disconnect_timeout_in_seconds=123,
                    idle_disconnect_timeout_in_seconds=123,
                    max_user_duration_in_seconds=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecfb987918720d3425e9abc2d9b9863493abc855606b2955f090b937a66c693)
            check_type(argname="argument application_settings", value=application_settings, expected_type=type_hints["application_settings"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument pool_name", value=pool_name, expected_type=type_hints["pool_name"])
            check_type(argname="argument running_mode", value=running_mode, expected_type=type_hints["running_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout_settings", value=timeout_settings, expected_type=type_hints["timeout_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_settings is not None:
            self._values["application_settings"] = application_settings
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if capacity is not None:
            self._values["capacity"] = capacity
        if description is not None:
            self._values["description"] = description
        if directory_id is not None:
            self._values["directory_id"] = directory_id
        if pool_name is not None:
            self._values["pool_name"] = pool_name
        if running_mode is not None:
            self._values["running_mode"] = running_mode
        if tags is not None:
            self._values["tags"] = tags
        if timeout_settings is not None:
            self._values["timeout_settings"] = timeout_settings

    @builtins.property
    def application_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacesPoolPropsMixin.ApplicationSettingsProperty"]]:
        '''The persistent application settings for users of the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-applicationsettings
        '''
        result = self._values.get("application_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacesPoolPropsMixin.ApplicationSettingsProperty"]], result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the bundle used by the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacesPoolPropsMixin.CapacityProperty"]]:
        '''Describes the user capacity for the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-capacity
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacesPoolPropsMixin.CapacityProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the directory used by the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-directoryid
        '''
        result = self._values.get("directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pool_name(self) -> typing.Optional[builtins.str]:
        '''The name of the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-poolname
        '''
        result = self._values.get("pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def running_mode(self) -> typing.Optional[builtins.str]:
        '''The running mode of the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-runningmode
        '''
        result = self._values.get("running_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-tags
        :stability: deprecated
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def timeout_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacesPoolPropsMixin.TimeoutSettingsProperty"]]:
        '''The amount of time that a pool session remains active after users disconnect.

        If they try to reconnect to the pool session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new pool instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-timeoutsettings
        '''
        result = self._values.get("timeout_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacesPoolPropsMixin.TimeoutSettingsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspacesPoolMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkspacesPoolPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnWorkspacesPoolPropsMixin",
):
    '''Describes a pool of WorkSpaces.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html
    :cloudformationResource: AWS::WorkSpaces::WorkspacesPool
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
        
        cfn_workspaces_pool_props_mixin = workspaces_mixins.CfnWorkspacesPoolPropsMixin(workspaces_mixins.CfnWorkspacesPoolMixinProps(
            application_settings=workspaces_mixins.CfnWorkspacesPoolPropsMixin.ApplicationSettingsProperty(
                settings_group="settingsGroup",
                status="status"
            ),
            bundle_id="bundleId",
            capacity=workspaces_mixins.CfnWorkspacesPoolPropsMixin.CapacityProperty(
                desired_user_sessions=123
            ),
            description="description",
            directory_id="directoryId",
            pool_name="poolName",
            running_mode="runningMode",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            timeout_settings=workspaces_mixins.CfnWorkspacesPoolPropsMixin.TimeoutSettingsProperty(
                disconnect_timeout_in_seconds=123,
                idle_disconnect_timeout_in_seconds=123,
                max_user_duration_in_seconds=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWorkspacesPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpaces::WorkspacesPool``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a523fb58ad53939e1669ac47713e64c22ee37be93c2c328f9e6af89c5c707395)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4baa17ce088ddd44b957b80cc0afff6d751029b771e227365a7480df59ae17d7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9813f86b85b41299b947c00378ca7c0913afd5d0ca4b853fc3d51a35f4846993)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkspacesPoolMixinProps:
        return typing.cast(CfnWorkspacesPoolMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnWorkspacesPoolPropsMixin.ApplicationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"settings_group": "settingsGroup", "status": "status"},
    )
    class ApplicationSettingsProperty:
        def __init__(
            self,
            *,
            settings_group: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The persistent application settings for users in the pool.

            :param settings_group: The path prefix for the S3 bucket where users’ persistent application settings are stored.
            :param status: Enables or disables persistent application settings for users during their pool sessions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-applicationsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
                
                application_settings_property = workspaces_mixins.CfnWorkspacesPoolPropsMixin.ApplicationSettingsProperty(
                    settings_group="settingsGroup",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cdfcd3d673c40d0410ca642b97c4df4def0ad2dae57896c6c6154e1083c60222)
                check_type(argname="argument settings_group", value=settings_group, expected_type=type_hints["settings_group"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if settings_group is not None:
                self._values["settings_group"] = settings_group
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def settings_group(self) -> typing.Optional[builtins.str]:
            '''The path prefix for the S3 bucket where users’ persistent application settings are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-applicationsettings.html#cfn-workspaces-workspacespool-applicationsettings-settingsgroup
            '''
            result = self._values.get("settings_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Enables or disables persistent application settings for users during their pool sessions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-applicationsettings.html#cfn-workspaces-workspacespool-applicationsettings-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnWorkspacesPoolPropsMixin.CapacityProperty",
        jsii_struct_bases=[],
        name_mapping={"desired_user_sessions": "desiredUserSessions"},
    )
    class CapacityProperty:
        def __init__(
            self,
            *,
            desired_user_sessions: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the user capacity for the pool.

            :param desired_user_sessions: The desired number of user sessions for the WorkSpaces in the pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-capacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
                
                capacity_property = workspaces_mixins.CfnWorkspacesPoolPropsMixin.CapacityProperty(
                    desired_user_sessions=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b7b6a4fb939a0c3296ff453b152b90fa671a6999cd4e6f03d9f3835cc62fa10)
                check_type(argname="argument desired_user_sessions", value=desired_user_sessions, expected_type=type_hints["desired_user_sessions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if desired_user_sessions is not None:
                self._values["desired_user_sessions"] = desired_user_sessions

        @builtins.property
        def desired_user_sessions(self) -> typing.Optional[jsii.Number]:
            '''The desired number of user sessions for the WorkSpaces in the pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-capacity.html#cfn-workspaces-workspacespool-capacity-desiredusersessions
            '''
            result = self._values.get("desired_user_sessions")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspaces.mixins.CfnWorkspacesPoolPropsMixin.TimeoutSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "disconnect_timeout_in_seconds": "disconnectTimeoutInSeconds",
            "idle_disconnect_timeout_in_seconds": "idleDisconnectTimeoutInSeconds",
            "max_user_duration_in_seconds": "maxUserDurationInSeconds",
        },
    )
    class TimeoutSettingsProperty:
        def __init__(
            self,
            *,
            disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
            idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
            max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the timeout settings for the pool.

            :param disconnect_timeout_in_seconds: Specifies the amount of time, in seconds, that a streaming session remains active after users disconnect. If users try to reconnect to the streaming session after a disconnection or network interruption within the time set, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance.
            :param idle_disconnect_timeout_in_seconds: The amount of time in seconds a connection will stay active while idle.
            :param max_user_duration_in_seconds: Specifies the maximum amount of time, in seconds, that a streaming session can remain active. If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-timeoutsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspaces import mixins as workspaces_mixins
                
                timeout_settings_property = workspaces_mixins.CfnWorkspacesPoolPropsMixin.TimeoutSettingsProperty(
                    disconnect_timeout_in_seconds=123,
                    idle_disconnect_timeout_in_seconds=123,
                    max_user_duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aabcfbd369dcebff9929acc5d2306dcbde5085cc3088c9acb2dc198f239450ef)
                check_type(argname="argument disconnect_timeout_in_seconds", value=disconnect_timeout_in_seconds, expected_type=type_hints["disconnect_timeout_in_seconds"])
                check_type(argname="argument idle_disconnect_timeout_in_seconds", value=idle_disconnect_timeout_in_seconds, expected_type=type_hints["idle_disconnect_timeout_in_seconds"])
                check_type(argname="argument max_user_duration_in_seconds", value=max_user_duration_in_seconds, expected_type=type_hints["max_user_duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if disconnect_timeout_in_seconds is not None:
                self._values["disconnect_timeout_in_seconds"] = disconnect_timeout_in_seconds
            if idle_disconnect_timeout_in_seconds is not None:
                self._values["idle_disconnect_timeout_in_seconds"] = idle_disconnect_timeout_in_seconds
            if max_user_duration_in_seconds is not None:
                self._values["max_user_duration_in_seconds"] = max_user_duration_in_seconds

        @builtins.property
        def disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Specifies the amount of time, in seconds, that a streaming session remains active after users disconnect.

            If users try to reconnect to the streaming session after a disconnection or network interruption within the time set, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-timeoutsettings.html#cfn-workspaces-workspacespool-timeoutsettings-disconnecttimeoutinseconds
            '''
            result = self._values.get("disconnect_timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def idle_disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time in seconds a connection will stay active while idle.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-timeoutsettings.html#cfn-workspaces-workspacespool-timeoutsettings-idledisconnecttimeoutinseconds
            '''
            result = self._values.get("idle_disconnect_timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_user_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum amount of time, in seconds, that a streaming session can remain active.

            If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-timeoutsettings.html#cfn-workspaces-workspacespool-timeoutsettings-maxuserdurationinseconds
            '''
            result = self._values.get("max_user_duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeoutSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnConnectionAliasMixinProps",
    "CfnConnectionAliasPropsMixin",
    "CfnWorkspaceMixinProps",
    "CfnWorkspacePropsMixin",
    "CfnWorkspacesPoolMixinProps",
    "CfnWorkspacesPoolPropsMixin",
]

publication.publish()

def _typecheckingstub__a07c8e43319127364f5b0c7600066c1219a00c7cf5a3b3b78c3a1c8505393b6d(
    *,
    connection_string: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea35a199fe42702b693aabb98bdb788360093aa91ededc3d3ecb3f88eb6c3eaa(
    props: typing.Union[CfnConnectionAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8643f9ed53003832f22011fc0aab16bb441a0ada8970be6ed8b5e07f3a1f4c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3536469eb40003042af9b0a9eda14d441889d164c96460d5cbc99561fbfe5b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5080543c3ed5a3332bd598f7666d0478f7ec150fe4b17ec00adf60644a798f51(
    *,
    associated_account_id: typing.Optional[builtins.str] = None,
    association_status: typing.Optional[builtins.str] = None,
    connection_identifier: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed608a58c84bd30dc947b4c9c4ef47d01595375e8aba4651458548d8f2f41e7(
    *,
    bundle_id: typing.Optional[builtins.str] = None,
    directory_id: typing.Optional[builtins.str] = None,
    root_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_name: typing.Optional[builtins.str] = None,
    user_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    volume_encryption_key: typing.Optional[builtins.str] = None,
    workspace_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.WorkspacePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__127819a5e0ddbab47646803e0459741156c1b547a4434efb8fc2a63cc663de10(
    props: typing.Union[CfnWorkspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86447719e6fc9f919cdf422557323ba5984a304dc3068ac575b244e4a1b209b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90352b517fbe1733c5ee5c9aba8fef521a8dad34fb0370a494be31030d442abe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dabd5cb2b3a3a819339522bf40e131450ab7863f73ded733526efc368a524ebe(
    *,
    compute_type_name: typing.Optional[builtins.str] = None,
    root_volume_size_gib: typing.Optional[jsii.Number] = None,
    running_mode: typing.Optional[builtins.str] = None,
    running_mode_auto_stop_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    user_volume_size_gib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecfb987918720d3425e9abc2d9b9863493abc855606b2955f090b937a66c693(
    *,
    application_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacesPoolPropsMixin.ApplicationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bundle_id: typing.Optional[builtins.str] = None,
    capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacesPoolPropsMixin.CapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    directory_id: typing.Optional[builtins.str] = None,
    pool_name: typing.Optional[builtins.str] = None,
    running_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacesPoolPropsMixin.TimeoutSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a523fb58ad53939e1669ac47713e64c22ee37be93c2c328f9e6af89c5c707395(
    props: typing.Union[CfnWorkspacesPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4baa17ce088ddd44b957b80cc0afff6d751029b771e227365a7480df59ae17d7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9813f86b85b41299b947c00378ca7c0913afd5d0ca4b853fc3d51a35f4846993(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfcd3d673c40d0410ca642b97c4df4def0ad2dae57896c6c6154e1083c60222(
    *,
    settings_group: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7b6a4fb939a0c3296ff453b152b90fa671a6999cd4e6f03d9f3835cc62fa10(
    *,
    desired_user_sessions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabcfbd369dcebff9929acc5d2306dcbde5085cc3088c9acb2dc198f239450ef(
    *,
    disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
