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
    jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnNamespaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_password_secret_kms_key_id": "adminPasswordSecretKmsKeyId",
        "admin_username": "adminUsername",
        "admin_user_password": "adminUserPassword",
        "db_name": "dbName",
        "default_iam_role_arn": "defaultIamRoleArn",
        "final_snapshot_name": "finalSnapshotName",
        "final_snapshot_retention_period": "finalSnapshotRetentionPeriod",
        "iam_roles": "iamRoles",
        "kms_key_id": "kmsKeyId",
        "log_exports": "logExports",
        "manage_admin_password": "manageAdminPassword",
        "namespace_name": "namespaceName",
        "namespace_resource_policy": "namespaceResourcePolicy",
        "redshift_idc_application_arn": "redshiftIdcApplicationArn",
        "snapshot_copy_configurations": "snapshotCopyConfigurations",
        "tags": "tags",
    },
)
class CfnNamespaceMixinProps:
    def __init__(
        self,
        *,
        admin_password_secret_kms_key_id: typing.Optional[builtins.str] = None,
        admin_username: typing.Optional[builtins.str] = None,
        admin_user_password: typing.Optional[builtins.str] = None,
        db_name: typing.Optional[builtins.str] = None,
        default_iam_role_arn: typing.Optional[builtins.str] = None,
        final_snapshot_name: typing.Optional[builtins.str] = None,
        final_snapshot_retention_period: typing.Optional[jsii.Number] = None,
        iam_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        manage_admin_password: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        namespace_name: typing.Optional[builtins.str] = None,
        namespace_resource_policy: typing.Any = None,
        redshift_idc_application_arn: typing.Optional[builtins.str] = None,
        snapshot_copy_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNamespacePropsMixin.SnapshotCopyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnNamespacePropsMixin.

        :param admin_password_secret_kms_key_id: The ID of the AWS Key Management Service (KMS) key used to encrypt and store the namespace's admin credentials secret. You can only use this parameter if ``ManageAdminPassword`` is ``true`` .
        :param admin_username: The username of the administrator for the primary database created in the namespace.
        :param admin_user_password: The password of the administrator for the primary database created in the namespace.
        :param db_name: The name of the primary database created in the namespace.
        :param default_iam_role_arn: The Amazon Resource Name (ARN) of the IAM role to set as a default in the namespace.
        :param final_snapshot_name: The name of the snapshot to be created before the namespace is deleted.
        :param final_snapshot_retention_period: How long to retain the final snapshot.
        :param iam_roles: A list of IAM roles to associate with the namespace.
        :param kms_key_id: The ID of the AWS Key Management Service key used to encrypt your data.
        :param log_exports: The types of logs the namespace can export. Available export types are ``userlog`` , ``connectionlog`` , and ``useractivitylog`` .
        :param manage_admin_password: If true, Amazon Redshift uses AWS Secrets Manager to manage the namespace's admin credentials. You can't use ``AdminUserPassword`` if ``ManageAdminPassword`` is true. If ``ManageAdminPassword`` is ``false`` or not set, Amazon Redshift uses ``AdminUserPassword`` for the admin user account's password.
        :param namespace_name: The name of the namespace. Must be between 3-64 alphanumeric characters in lowercase, and it cannot be a reserved word. A list of reserved words can be found in `Reserved Words <https://docs.aws.amazon.com//redshift/latest/dg/r_pg_keywords.html>`_ in the Amazon Redshift Database Developer Guide.
        :param namespace_resource_policy: The resource policy that will be attached to the namespace.
        :param redshift_idc_application_arn: The ARN for the Redshift application that integrates with IAM Identity Center.
        :param snapshot_copy_configurations: The snapshot copy configurations for the namespace.
        :param tags: The map of the key-value pairs used to tag the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
            
            # namespace_resource_policy: Any
            
            cfn_namespace_mixin_props = redshiftserverless_mixins.CfnNamespaceMixinProps(
                admin_password_secret_kms_key_id="adminPasswordSecretKmsKeyId",
                admin_username="adminUsername",
                admin_user_password="adminUserPassword",
                db_name="dbName",
                default_iam_role_arn="defaultIamRoleArn",
                final_snapshot_name="finalSnapshotName",
                final_snapshot_retention_period=123,
                iam_roles=["iamRoles"],
                kms_key_id="kmsKeyId",
                log_exports=["logExports"],
                manage_admin_password=False,
                namespace_name="namespaceName",
                namespace_resource_policy=namespace_resource_policy,
                redshift_idc_application_arn="redshiftIdcApplicationArn",
                snapshot_copy_configurations=[redshiftserverless_mixins.CfnNamespacePropsMixin.SnapshotCopyConfigurationProperty(
                    destination_kms_key_id="destinationKmsKeyId",
                    destination_region="destinationRegion",
                    snapshot_retention_period=123
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12caf34ce16a040b23c6f0cbae0fea444374587464aa8e977ee3f3a3f36d884c)
            check_type(argname="argument admin_password_secret_kms_key_id", value=admin_password_secret_kms_key_id, expected_type=type_hints["admin_password_secret_kms_key_id"])
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument admin_user_password", value=admin_user_password, expected_type=type_hints["admin_user_password"])
            check_type(argname="argument db_name", value=db_name, expected_type=type_hints["db_name"])
            check_type(argname="argument default_iam_role_arn", value=default_iam_role_arn, expected_type=type_hints["default_iam_role_arn"])
            check_type(argname="argument final_snapshot_name", value=final_snapshot_name, expected_type=type_hints["final_snapshot_name"])
            check_type(argname="argument final_snapshot_retention_period", value=final_snapshot_retention_period, expected_type=type_hints["final_snapshot_retention_period"])
            check_type(argname="argument iam_roles", value=iam_roles, expected_type=type_hints["iam_roles"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument log_exports", value=log_exports, expected_type=type_hints["log_exports"])
            check_type(argname="argument manage_admin_password", value=manage_admin_password, expected_type=type_hints["manage_admin_password"])
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
            check_type(argname="argument namespace_resource_policy", value=namespace_resource_policy, expected_type=type_hints["namespace_resource_policy"])
            check_type(argname="argument redshift_idc_application_arn", value=redshift_idc_application_arn, expected_type=type_hints["redshift_idc_application_arn"])
            check_type(argname="argument snapshot_copy_configurations", value=snapshot_copy_configurations, expected_type=type_hints["snapshot_copy_configurations"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_password_secret_kms_key_id is not None:
            self._values["admin_password_secret_kms_key_id"] = admin_password_secret_kms_key_id
        if admin_username is not None:
            self._values["admin_username"] = admin_username
        if admin_user_password is not None:
            self._values["admin_user_password"] = admin_user_password
        if db_name is not None:
            self._values["db_name"] = db_name
        if default_iam_role_arn is not None:
            self._values["default_iam_role_arn"] = default_iam_role_arn
        if final_snapshot_name is not None:
            self._values["final_snapshot_name"] = final_snapshot_name
        if final_snapshot_retention_period is not None:
            self._values["final_snapshot_retention_period"] = final_snapshot_retention_period
        if iam_roles is not None:
            self._values["iam_roles"] = iam_roles
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if log_exports is not None:
            self._values["log_exports"] = log_exports
        if manage_admin_password is not None:
            self._values["manage_admin_password"] = manage_admin_password
        if namespace_name is not None:
            self._values["namespace_name"] = namespace_name
        if namespace_resource_policy is not None:
            self._values["namespace_resource_policy"] = namespace_resource_policy
        if redshift_idc_application_arn is not None:
            self._values["redshift_idc_application_arn"] = redshift_idc_application_arn
        if snapshot_copy_configurations is not None:
            self._values["snapshot_copy_configurations"] = snapshot_copy_configurations
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def admin_password_secret_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS Key Management Service (KMS) key used to encrypt and store the namespace's admin credentials secret.

        You can only use this parameter if ``ManageAdminPassword`` is ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-adminpasswordsecretkmskeyid
        '''
        result = self._values.get("admin_password_secret_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_username(self) -> typing.Optional[builtins.str]:
        '''The username of the administrator for the primary database created in the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-adminusername
        '''
        result = self._values.get("admin_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_user_password(self) -> typing.Optional[builtins.str]:
        '''The password of the administrator for the primary database created in the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-adminuserpassword
        '''
        result = self._values.get("admin_user_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_name(self) -> typing.Optional[builtins.str]:
        '''The name of the primary database created in the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-dbname
        '''
        result = self._values.get("db_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role to set as a default in the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-defaultiamrolearn
        '''
        result = self._values.get("default_iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def final_snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of the snapshot to be created before the namespace is deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-finalsnapshotname
        '''
        result = self._values.get("final_snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def final_snapshot_retention_period(self) -> typing.Optional[jsii.Number]:
        '''How long to retain the final snapshot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-finalsnapshotretentionperiod
        '''
        result = self._values.get("final_snapshot_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def iam_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles to associate with the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-iamroles
        '''
        result = self._values.get("iam_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS Key Management Service key used to encrypt your data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_exports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The types of logs the namespace can export.

        Available export types are ``userlog`` , ``connectionlog`` , and ``useractivitylog`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-logexports
        '''
        result = self._values.get("log_exports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def manage_admin_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If true, Amazon Redshift uses AWS Secrets Manager to manage the namespace's admin credentials.

        You can't use ``AdminUserPassword`` if ``ManageAdminPassword`` is true. If ``ManageAdminPassword`` is ``false`` or not set, Amazon Redshift uses ``AdminUserPassword`` for the admin user account's password.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-manageadminpassword
        '''
        result = self._values.get("manage_admin_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def namespace_name(self) -> typing.Optional[builtins.str]:
        '''The name of the namespace.

        Must be between 3-64 alphanumeric characters in lowercase, and it cannot be a reserved word. A list of reserved words can be found in `Reserved Words <https://docs.aws.amazon.com//redshift/latest/dg/r_pg_keywords.html>`_ in the Amazon Redshift Database Developer Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-namespacename
        '''
        result = self._values.get("namespace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace_resource_policy(self) -> typing.Any:
        '''The resource policy that will be attached to the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-namespaceresourcepolicy
        '''
        result = self._values.get("namespace_resource_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def redshift_idc_application_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN for the Redshift application that integrates with IAM Identity Center.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-redshiftidcapplicationarn
        '''
        result = self._values.get("redshift_idc_application_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_copy_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNamespacePropsMixin.SnapshotCopyConfigurationProperty"]]]]:
        '''The snapshot copy configurations for the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-snapshotcopyconfigurations
        '''
        result = self._values.get("snapshot_copy_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNamespacePropsMixin.SnapshotCopyConfigurationProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The map of the key-value pairs used to tag the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html#cfn-redshiftserverless-namespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNamespaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNamespacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnNamespacePropsMixin",
):
    '''A collection of database objects and users.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-namespace.html
    :cloudformationResource: AWS::RedshiftServerless::Namespace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
        
        # namespace_resource_policy: Any
        
        cfn_namespace_props_mixin = redshiftserverless_mixins.CfnNamespacePropsMixin(redshiftserverless_mixins.CfnNamespaceMixinProps(
            admin_password_secret_kms_key_id="adminPasswordSecretKmsKeyId",
            admin_username="adminUsername",
            admin_user_password="adminUserPassword",
            db_name="dbName",
            default_iam_role_arn="defaultIamRoleArn",
            final_snapshot_name="finalSnapshotName",
            final_snapshot_retention_period=123,
            iam_roles=["iamRoles"],
            kms_key_id="kmsKeyId",
            log_exports=["logExports"],
            manage_admin_password=False,
            namespace_name="namespaceName",
            namespace_resource_policy=namespace_resource_policy,
            redshift_idc_application_arn="redshiftIdcApplicationArn",
            snapshot_copy_configurations=[redshiftserverless_mixins.CfnNamespacePropsMixin.SnapshotCopyConfigurationProperty(
                destination_kms_key_id="destinationKmsKeyId",
                destination_region="destinationRegion",
                snapshot_retention_period=123
            )],
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
        props: typing.Union[CfnNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RedshiftServerless::Namespace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87396856dcdb3e1d25836c558050697de375a9723dbf3f5f679a9f83272f7fd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5a9c22c041d9849335cc9285f679635d11f4ef15a20ef5774ceae8f866c4311)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5426aa0e69dd2d0ecd54a7cdfb92ddc5b7bc7430fc03dd7902df5fd3f115e40)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNamespaceMixinProps:
        return typing.cast(CfnNamespaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnNamespacePropsMixin.NamespaceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "admin_password_secret_arn": "adminPasswordSecretArn",
            "admin_password_secret_kms_key_id": "adminPasswordSecretKmsKeyId",
            "admin_username": "adminUsername",
            "creation_date": "creationDate",
            "db_name": "dbName",
            "default_iam_role_arn": "defaultIamRoleArn",
            "iam_roles": "iamRoles",
            "kms_key_id": "kmsKeyId",
            "log_exports": "logExports",
            "namespace_arn": "namespaceArn",
            "namespace_id": "namespaceId",
            "namespace_name": "namespaceName",
            "status": "status",
        },
    )
    class NamespaceProperty:
        def __init__(
            self,
            *,
            admin_password_secret_arn: typing.Optional[builtins.str] = None,
            admin_password_secret_kms_key_id: typing.Optional[builtins.str] = None,
            admin_username: typing.Optional[builtins.str] = None,
            creation_date: typing.Optional[builtins.str] = None,
            db_name: typing.Optional[builtins.str] = None,
            default_iam_role_arn: typing.Optional[builtins.str] = None,
            iam_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
            log_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
            namespace_arn: typing.Optional[builtins.str] = None,
            namespace_id: typing.Optional[builtins.str] = None,
            namespace_name: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A collection of database objects and users.

            :param admin_password_secret_arn: The Amazon Resource Name (ARN) for the namespace's admin user credentials secret.
            :param admin_password_secret_kms_key_id: The ID of the AWS Key Management Service (KMS) key used to encrypt and store the namespace's admin credentials secret.
            :param admin_username: The username of the administrator for the first database created in the namespace.
            :param creation_date: The date of when the namespace was created.
            :param db_name: The name of the first database created in the namespace.
            :param default_iam_role_arn: The Amazon Resource Name (ARN) of the IAM role to set as a default in the namespace.
            :param iam_roles: A list of IAM roles to associate with the namespace.
            :param kms_key_id: The ID of the AWS Key Management Service key used to encrypt your data.
            :param log_exports: The types of logs the namespace can export. Available export types are User log, Connection log, and User activity log.
            :param namespace_arn: The Amazon Resource Name (ARN) associated with a namespace.
            :param namespace_id: The unique identifier of a namespace.
            :param namespace_name: The name of the namespace. Must be between 3-64 alphanumeric characters in lowercase, and it cannot be a reserved word. A list of reserved words can be found in `Reserved Words <https://docs.aws.amazon.com//redshift/latest/dg/r_pg_keywords.html>`_ in the Amazon Redshift Database Developer Guide.
            :param status: The status of the namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
                
                namespace_property = redshiftserverless_mixins.CfnNamespacePropsMixin.NamespaceProperty(
                    admin_password_secret_arn="adminPasswordSecretArn",
                    admin_password_secret_kms_key_id="adminPasswordSecretKmsKeyId",
                    admin_username="adminUsername",
                    creation_date="creationDate",
                    db_name="dbName",
                    default_iam_role_arn="defaultIamRoleArn",
                    iam_roles=["iamRoles"],
                    kms_key_id="kmsKeyId",
                    log_exports=["logExports"],
                    namespace_arn="namespaceArn",
                    namespace_id="namespaceId",
                    namespace_name="namespaceName",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff413b13be8348e48568d9263969a1a822550303933983a3fa8a1fdfb21ddd6d)
                check_type(argname="argument admin_password_secret_arn", value=admin_password_secret_arn, expected_type=type_hints["admin_password_secret_arn"])
                check_type(argname="argument admin_password_secret_kms_key_id", value=admin_password_secret_kms_key_id, expected_type=type_hints["admin_password_secret_kms_key_id"])
                check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
                check_type(argname="argument creation_date", value=creation_date, expected_type=type_hints["creation_date"])
                check_type(argname="argument db_name", value=db_name, expected_type=type_hints["db_name"])
                check_type(argname="argument default_iam_role_arn", value=default_iam_role_arn, expected_type=type_hints["default_iam_role_arn"])
                check_type(argname="argument iam_roles", value=iam_roles, expected_type=type_hints["iam_roles"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument log_exports", value=log_exports, expected_type=type_hints["log_exports"])
                check_type(argname="argument namespace_arn", value=namespace_arn, expected_type=type_hints["namespace_arn"])
                check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
                check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if admin_password_secret_arn is not None:
                self._values["admin_password_secret_arn"] = admin_password_secret_arn
            if admin_password_secret_kms_key_id is not None:
                self._values["admin_password_secret_kms_key_id"] = admin_password_secret_kms_key_id
            if admin_username is not None:
                self._values["admin_username"] = admin_username
            if creation_date is not None:
                self._values["creation_date"] = creation_date
            if db_name is not None:
                self._values["db_name"] = db_name
            if default_iam_role_arn is not None:
                self._values["default_iam_role_arn"] = default_iam_role_arn
            if iam_roles is not None:
                self._values["iam_roles"] = iam_roles
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if log_exports is not None:
                self._values["log_exports"] = log_exports
            if namespace_arn is not None:
                self._values["namespace_arn"] = namespace_arn
            if namespace_id is not None:
                self._values["namespace_id"] = namespace_id
            if namespace_name is not None:
                self._values["namespace_name"] = namespace_name
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def admin_password_secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the namespace's admin user credentials secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-adminpasswordsecretarn
            '''
            result = self._values.get("admin_password_secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def admin_password_secret_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the AWS Key Management Service (KMS) key used to encrypt and store the namespace's admin credentials secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-adminpasswordsecretkmskeyid
            '''
            result = self._values.get("admin_password_secret_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def admin_username(self) -> typing.Optional[builtins.str]:
            '''The username of the administrator for the first database created in the namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-adminusername
            '''
            result = self._values.get("admin_username")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def creation_date(self) -> typing.Optional[builtins.str]:
            '''The date of when the namespace was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-creationdate
            '''
            result = self._values.get("creation_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def db_name(self) -> typing.Optional[builtins.str]:
            '''The name of the first database created in the namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-dbname
            '''
            result = self._values.get("db_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_iam_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role to set as a default in the namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-defaultiamrolearn
            '''
            result = self._values.get("default_iam_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iam_roles(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of IAM roles to associate with the namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-iamroles
            '''
            result = self._values.get("iam_roles")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the AWS Key Management Service key used to encrypt your data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_exports(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The types of logs the namespace can export.

            Available export types are User log, Connection log, and User activity log.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-logexports
            '''
            result = self._values.get("log_exports")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def namespace_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) associated with a namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-namespacearn
            '''
            result = self._values.get("namespace_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of a namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-namespaceid
            '''
            result = self._values.get("namespace_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace_name(self) -> typing.Optional[builtins.str]:
            '''The name of the namespace.

            Must be between 3-64 alphanumeric characters in lowercase, and it cannot be a reserved word. A list of reserved words can be found in `Reserved Words <https://docs.aws.amazon.com//redshift/latest/dg/r_pg_keywords.html>`_ in the Amazon Redshift Database Developer Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-namespacename
            '''
            result = self._values.get("namespace_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-namespace.html#cfn-redshiftserverless-namespace-namespace-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NamespaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnNamespacePropsMixin.SnapshotCopyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_kms_key_id": "destinationKmsKeyId",
            "destination_region": "destinationRegion",
            "snapshot_retention_period": "snapshotRetentionPeriod",
        },
    )
    class SnapshotCopyConfigurationProperty:
        def __init__(
            self,
            *,
            destination_kms_key_id: typing.Optional[builtins.str] = None,
            destination_region: typing.Optional[builtins.str] = None,
            snapshot_retention_period: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The object that you configure to copy snapshots from one namespace to a namespace in another AWS Region .

            :param destination_kms_key_id: The ID of the KMS key to use to encrypt your snapshots in the destination AWS Region .
            :param destination_region: The destination AWS Region to copy snapshots to.
            :param snapshot_retention_period: The retention period of snapshots that are copied to the destination AWS Region .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-snapshotcopyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
                
                snapshot_copy_configuration_property = redshiftserverless_mixins.CfnNamespacePropsMixin.SnapshotCopyConfigurationProperty(
                    destination_kms_key_id="destinationKmsKeyId",
                    destination_region="destinationRegion",
                    snapshot_retention_period=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3006635c687b31a3b74db41e5b3754f904274e573e1200753fbd2e40dbba5578)
                check_type(argname="argument destination_kms_key_id", value=destination_kms_key_id, expected_type=type_hints["destination_kms_key_id"])
                check_type(argname="argument destination_region", value=destination_region, expected_type=type_hints["destination_region"])
                check_type(argname="argument snapshot_retention_period", value=snapshot_retention_period, expected_type=type_hints["snapshot_retention_period"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_kms_key_id is not None:
                self._values["destination_kms_key_id"] = destination_kms_key_id
            if destination_region is not None:
                self._values["destination_region"] = destination_region
            if snapshot_retention_period is not None:
                self._values["snapshot_retention_period"] = snapshot_retention_period

        @builtins.property
        def destination_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the KMS key to use to encrypt your snapshots in the destination AWS Region .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-snapshotcopyconfiguration.html#cfn-redshiftserverless-namespace-snapshotcopyconfiguration-destinationkmskeyid
            '''
            result = self._values.get("destination_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_region(self) -> typing.Optional[builtins.str]:
            '''The destination AWS Region to copy snapshots to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-snapshotcopyconfiguration.html#cfn-redshiftserverless-namespace-snapshotcopyconfiguration-destinationregion
            '''
            result = self._values.get("destination_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def snapshot_retention_period(self) -> typing.Optional[jsii.Number]:
            '''The retention period of snapshots that are copied to the destination AWS Region .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-namespace-snapshotcopyconfiguration.html#cfn-redshiftserverless-namespace-snapshotcopyconfiguration-snapshotretentionperiod
            '''
            result = self._values.get("snapshot_retention_period")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnapshotCopyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnSnapshotMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "namespace_name": "namespaceName",
        "retention_period": "retentionPeriod",
        "snapshot_name": "snapshotName",
        "tags": "tags",
    },
)
class CfnSnapshotMixinProps:
    def __init__(
        self,
        *,
        namespace_name: typing.Optional[builtins.str] = None,
        retention_period: typing.Optional[jsii.Number] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSnapshotPropsMixin.

        :param namespace_name: The name of the namepsace.
        :param retention_period: The retention period of the snapshot created by the scheduled action.
        :param snapshot_name: The name of the snapshot.
        :param tags: An array of `Tag objects <https://docs.aws.amazon.com/redshift-serverless/latest/APIReference/API_Tag.html>`_ to associate with the snapshot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-snapshot.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
            
            cfn_snapshot_mixin_props = redshiftserverless_mixins.CfnSnapshotMixinProps(
                namespace_name="namespaceName",
                retention_period=123,
                snapshot_name="snapshotName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e36a99770b839a69eca7a652bedb2a8bb5ac34265cb5b51fbeec4e3ae4763f)
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument snapshot_name", value=snapshot_name, expected_type=type_hints["snapshot_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if namespace_name is not None:
            self._values["namespace_name"] = namespace_name
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def namespace_name(self) -> typing.Optional[builtins.str]:
        '''The name of the namepsace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-snapshot.html#cfn-redshiftserverless-snapshot-namespacename
        '''
        result = self._values.get("namespace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_period(self) -> typing.Optional[jsii.Number]:
        '''The retention period of the snapshot created by the scheduled action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-snapshot.html#cfn-redshiftserverless-snapshot-retentionperiod
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of the snapshot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-snapshot.html#cfn-redshiftserverless-snapshot-snapshotname
        '''
        result = self._values.get("snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of `Tag objects <https://docs.aws.amazon.com/redshift-serverless/latest/APIReference/API_Tag.html>`_ to associate with the snapshot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-snapshot.html#cfn-redshiftserverless-snapshot-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSnapshotMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSnapshotPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnSnapshotPropsMixin",
):
    '''A snapshot object that contains databases.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-snapshot.html
    :cloudformationResource: AWS::RedshiftServerless::Snapshot
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
        
        cfn_snapshot_props_mixin = redshiftserverless_mixins.CfnSnapshotPropsMixin(redshiftserverless_mixins.CfnSnapshotMixinProps(
            namespace_name="namespaceName",
            retention_period=123,
            snapshot_name="snapshotName",
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
        props: typing.Union[CfnSnapshotMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RedshiftServerless::Snapshot``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f711b2102a6237fb561dc29ee147bf3bb018a9019dd4d4e2405803d8c6e7c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30d522c66e6a0a0aa0180c10359d4f1dbdcaed318cf844b958d46113683f6cc7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91158730fdf307eb12bc605b69755ec2faa0f010b7a847ccfb94e408efb7ec0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSnapshotMixinProps:
        return typing.cast(CfnSnapshotMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnSnapshotPropsMixin.SnapshotProperty",
        jsii_struct_bases=[],
        name_mapping={
            "admin_username": "adminUsername",
            "kms_key_id": "kmsKeyId",
            "namespace_arn": "namespaceArn",
            "namespace_name": "namespaceName",
            "owner_account": "ownerAccount",
            "retention_period": "retentionPeriod",
            "snapshot_arn": "snapshotArn",
            "snapshot_create_time": "snapshotCreateTime",
            "snapshot_name": "snapshotName",
            "status": "status",
        },
    )
    class SnapshotProperty:
        def __init__(
            self,
            *,
            admin_username: typing.Optional[builtins.str] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
            namespace_arn: typing.Optional[builtins.str] = None,
            namespace_name: typing.Optional[builtins.str] = None,
            owner_account: typing.Optional[builtins.str] = None,
            retention_period: typing.Optional[jsii.Number] = None,
            snapshot_arn: typing.Optional[builtins.str] = None,
            snapshot_create_time: typing.Optional[builtins.str] = None,
            snapshot_name: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A snapshot object that contains databases.

            :param admin_username: The username of the database within a snapshot.
            :param kms_key_id: The unique identifier of the KMS key used to encrypt the snapshot.
            :param namespace_arn: The Amazon Resource Name (ARN) of the namespace the snapshot was created from.
            :param namespace_name: The name of the namepsace.
            :param owner_account: The owner AWS ; account of the snapshot.
            :param retention_period: The retention period of the snapshot created by the scheduled action.
            :param snapshot_arn: The Amazon Resource Name (ARN) of the snapshot.
            :param snapshot_create_time: The timestamp of when the snapshot was created.
            :param snapshot_name: The name of the snapshot.
            :param status: The status of the snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
                
                snapshot_property = redshiftserverless_mixins.CfnSnapshotPropsMixin.SnapshotProperty(
                    admin_username="adminUsername",
                    kms_key_id="kmsKeyId",
                    namespace_arn="namespaceArn",
                    namespace_name="namespaceName",
                    owner_account="ownerAccount",
                    retention_period=123,
                    snapshot_arn="snapshotArn",
                    snapshot_create_time="snapshotCreateTime",
                    snapshot_name="snapshotName",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__35ee4b525ed89078e5affbb02c24443fbaff82aa04ced2e08ccc049b49b5df20)
                check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument namespace_arn", value=namespace_arn, expected_type=type_hints["namespace_arn"])
                check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
                check_type(argname="argument owner_account", value=owner_account, expected_type=type_hints["owner_account"])
                check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
                check_type(argname="argument snapshot_arn", value=snapshot_arn, expected_type=type_hints["snapshot_arn"])
                check_type(argname="argument snapshot_create_time", value=snapshot_create_time, expected_type=type_hints["snapshot_create_time"])
                check_type(argname="argument snapshot_name", value=snapshot_name, expected_type=type_hints["snapshot_name"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if admin_username is not None:
                self._values["admin_username"] = admin_username
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if namespace_arn is not None:
                self._values["namespace_arn"] = namespace_arn
            if namespace_name is not None:
                self._values["namespace_name"] = namespace_name
            if owner_account is not None:
                self._values["owner_account"] = owner_account
            if retention_period is not None:
                self._values["retention_period"] = retention_period
            if snapshot_arn is not None:
                self._values["snapshot_arn"] = snapshot_arn
            if snapshot_create_time is not None:
                self._values["snapshot_create_time"] = snapshot_create_time
            if snapshot_name is not None:
                self._values["snapshot_name"] = snapshot_name
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def admin_username(self) -> typing.Optional[builtins.str]:
            '''The username of the database within a snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html#cfn-redshiftserverless-snapshot-snapshot-adminusername
            '''
            result = self._values.get("admin_username")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the KMS key used to encrypt the snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html#cfn-redshiftserverless-snapshot-snapshot-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the namespace the snapshot was created from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html#cfn-redshiftserverless-snapshot-snapshot-namespacearn
            '''
            result = self._values.get("namespace_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace_name(self) -> typing.Optional[builtins.str]:
            '''The name of the namepsace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html#cfn-redshiftserverless-snapshot-snapshot-namespacename
            '''
            result = self._values.get("namespace_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def owner_account(self) -> typing.Optional[builtins.str]:
            '''The owner AWS ;

            account of the snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html#cfn-redshiftserverless-snapshot-snapshot-owneraccount
            '''
            result = self._values.get("owner_account")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retention_period(self) -> typing.Optional[jsii.Number]:
            '''The retention period of the snapshot created by the scheduled action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html#cfn-redshiftserverless-snapshot-snapshot-retentionperiod
            '''
            result = self._values.get("retention_period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def snapshot_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html#cfn-redshiftserverless-snapshot-snapshot-snapshotarn
            '''
            result = self._values.get("snapshot_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def snapshot_create_time(self) -> typing.Optional[builtins.str]:
            '''The timestamp of when the snapshot was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html#cfn-redshiftserverless-snapshot-snapshot-snapshotcreatetime
            '''
            result = self._values.get("snapshot_create_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def snapshot_name(self) -> typing.Optional[builtins.str]:
            '''The name of the snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html#cfn-redshiftserverless-snapshot-snapshot-snapshotname
            '''
            result = self._values.get("snapshot_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-snapshot-snapshot.html#cfn-redshiftserverless-snapshot-snapshot-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnapshotProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnWorkgroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "base_capacity": "baseCapacity",
        "config_parameters": "configParameters",
        "enhanced_vpc_routing": "enhancedVpcRouting",
        "max_capacity": "maxCapacity",
        "namespace_name": "namespaceName",
        "port": "port",
        "price_performance_target": "pricePerformanceTarget",
        "publicly_accessible": "publiclyAccessible",
        "recovery_point_id": "recoveryPointId",
        "security_group_ids": "securityGroupIds",
        "snapshot_arn": "snapshotArn",
        "snapshot_name": "snapshotName",
        "snapshot_owner_account": "snapshotOwnerAccount",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "track_name": "trackName",
        "workgroup": "workgroup",
        "workgroup_name": "workgroupName",
    },
)
class CfnWorkgroupMixinProps:
    def __init__(
        self,
        *,
        base_capacity: typing.Optional[jsii.Number] = None,
        config_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkgroupPropsMixin.ConfigParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        enhanced_vpc_routing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        namespace_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        price_performance_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkgroupPropsMixin.PerformanceTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        recovery_point_id: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_arn: typing.Optional[builtins.str] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_owner_account: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        track_name: typing.Optional[builtins.str] = None,
        workgroup: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkgroupPropsMixin.WorkgroupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        workgroup_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWorkgroupPropsMixin.

        :param base_capacity: The base compute capacity of the workgroup in Redshift Processing Units (RPUs).
        :param config_parameters: The key of the parameter. The options are ``auto_mv`` , ``datestyle`` , ``enable_case_sensitive_identifier`` , ``enable_user_activity_logging`` , ``query_group`` , ``search_path`` , ``require_ssl`` , ``use_fips_ssl`` , and query monitoring metrics that let you define performance boundaries. For more information about query monitoring rules and available metrics, see `Query monitoring metrics for Amazon Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/dg/cm-c-wlm-query-monitoring-rules.html#cm-c-wlm-query-monitoring-metrics-serverless>`_ .
        :param enhanced_vpc_routing: The value that specifies whether to enable enhanced virtual private cloud (VPC) routing, which forces Amazon Redshift Serverless to route traffic through your VPC. Default: - false
        :param max_capacity: The maximum data-warehouse capacity Amazon Redshift Serverless uses to serve queries. The max capacity is specified in RPUs.
        :param namespace_name: The namespace the workgroup is associated with.
        :param port: The custom port to use when connecting to a workgroup. Valid port ranges are 5431-5455 and 8191-8215. The default is 5439.
        :param price_performance_target: An object that represents the price performance target settings for the workgroup.
        :param publicly_accessible: A value that specifies whether the workgroup can be accessible from a public network. Default: - false
        :param recovery_point_id: The recovery point id to restore from.
        :param security_group_ids: A list of security group IDs to associate with the workgroup.
        :param snapshot_arn: The Amazon Resource Name (ARN) of the snapshot to restore from.
        :param snapshot_name: The snapshot name to restore from.
        :param snapshot_owner_account: The Amazon Web Services account that owns the snapshot.
        :param subnet_ids: A list of subnet IDs the workgroup is associated with.
        :param tags: The map of the key-value pairs used to tag the workgroup.
        :param track_name: An optional parameter for the name of the track for the workgroup. If you don't provide a track name, the workgroup is assigned to the current track.
        :param workgroup: The collection of computing resources from which an endpoint is created.
        :param workgroup_name: The name of the workgroup.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
            
            cfn_workgroup_mixin_props = redshiftserverless_mixins.CfnWorkgroupMixinProps(
                base_capacity=123,
                config_parameters=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.ConfigParameterProperty(
                    parameter_key="parameterKey",
                    parameter_value="parameterValue"
                )],
                enhanced_vpc_routing=False,
                max_capacity=123,
                namespace_name="namespaceName",
                port=123,
                price_performance_target=redshiftserverless_mixins.CfnWorkgroupPropsMixin.PerformanceTargetProperty(
                    level=123,
                    status="status"
                ),
                publicly_accessible=False,
                recovery_point_id="recoveryPointId",
                security_group_ids=["securityGroupIds"],
                snapshot_arn="snapshotArn",
                snapshot_name="snapshotName",
                snapshot_owner_account="snapshotOwnerAccount",
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                track_name="trackName",
                workgroup=redshiftserverless_mixins.CfnWorkgroupPropsMixin.WorkgroupProperty(
                    base_capacity=123,
                    config_parameters=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.ConfigParameterProperty(
                        parameter_key="parameterKey",
                        parameter_value="parameterValue"
                    )],
                    creation_date="creationDate",
                    endpoint=redshiftserverless_mixins.CfnWorkgroupPropsMixin.EndpointProperty(
                        address="address",
                        port=123,
                        vpc_endpoints=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.VpcEndpointProperty(
                            network_interfaces=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.NetworkInterfaceProperty(
                                availability_zone="availabilityZone",
                                network_interface_id="networkInterfaceId",
                                private_ip_address="privateIpAddress",
                                subnet_id="subnetId"
                            )],
                            vpc_endpoint_id="vpcEndpointId",
                            vpc_id="vpcId"
                        )]
                    ),
                    enhanced_vpc_routing=False,
                    max_capacity=123,
                    namespace_name="namespaceName",
                    price_performance_target=redshiftserverless_mixins.CfnWorkgroupPropsMixin.PerformanceTargetProperty(
                        level=123,
                        status="status"
                    ),
                    publicly_accessible=False,
                    security_group_ids=["securityGroupIds"],
                    status="status",
                    subnet_ids=["subnetIds"],
                    track_name="trackName",
                    workgroup_arn="workgroupArn",
                    workgroup_id="workgroupId",
                    workgroup_name="workgroupName"
                ),
                workgroup_name="workgroupName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25dcf158a7219c7a3eeef48297c2ae320502f75d819b76a687026c2ef6c0cb5)
            check_type(argname="argument base_capacity", value=base_capacity, expected_type=type_hints["base_capacity"])
            check_type(argname="argument config_parameters", value=config_parameters, expected_type=type_hints["config_parameters"])
            check_type(argname="argument enhanced_vpc_routing", value=enhanced_vpc_routing, expected_type=type_hints["enhanced_vpc_routing"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument price_performance_target", value=price_performance_target, expected_type=type_hints["price_performance_target"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument recovery_point_id", value=recovery_point_id, expected_type=type_hints["recovery_point_id"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument snapshot_arn", value=snapshot_arn, expected_type=type_hints["snapshot_arn"])
            check_type(argname="argument snapshot_name", value=snapshot_name, expected_type=type_hints["snapshot_name"])
            check_type(argname="argument snapshot_owner_account", value=snapshot_owner_account, expected_type=type_hints["snapshot_owner_account"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument track_name", value=track_name, expected_type=type_hints["track_name"])
            check_type(argname="argument workgroup", value=workgroup, expected_type=type_hints["workgroup"])
            check_type(argname="argument workgroup_name", value=workgroup_name, expected_type=type_hints["workgroup_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_capacity is not None:
            self._values["base_capacity"] = base_capacity
        if config_parameters is not None:
            self._values["config_parameters"] = config_parameters
        if enhanced_vpc_routing is not None:
            self._values["enhanced_vpc_routing"] = enhanced_vpc_routing
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if namespace_name is not None:
            self._values["namespace_name"] = namespace_name
        if port is not None:
            self._values["port"] = port
        if price_performance_target is not None:
            self._values["price_performance_target"] = price_performance_target
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if recovery_point_id is not None:
            self._values["recovery_point_id"] = recovery_point_id
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if snapshot_arn is not None:
            self._values["snapshot_arn"] = snapshot_arn
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_owner_account is not None:
            self._values["snapshot_owner_account"] = snapshot_owner_account
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if track_name is not None:
            self._values["track_name"] = track_name
        if workgroup is not None:
            self._values["workgroup"] = workgroup
        if workgroup_name is not None:
            self._values["workgroup_name"] = workgroup_name

    @builtins.property
    def base_capacity(self) -> typing.Optional[jsii.Number]:
        '''The base compute capacity of the workgroup in Redshift Processing Units (RPUs).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-basecapacity
        '''
        result = self._values.get("base_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def config_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.ConfigParameterProperty"]]]]:
        '''The key of the parameter.

        The options are ``auto_mv`` , ``datestyle`` , ``enable_case_sensitive_identifier`` , ``enable_user_activity_logging`` , ``query_group`` , ``search_path`` , ``require_ssl`` , ``use_fips_ssl`` , and query monitoring metrics that let you define performance boundaries. For more information about query monitoring rules and available metrics, see `Query monitoring metrics for Amazon Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/dg/cm-c-wlm-query-monitoring-rules.html#cm-c-wlm-query-monitoring-metrics-serverless>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-configparameters
        '''
        result = self._values.get("config_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.ConfigParameterProperty"]]]], result)

    @builtins.property
    def enhanced_vpc_routing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The value that specifies whether to enable enhanced virtual private cloud (VPC) routing, which forces Amazon Redshift Serverless to route traffic through your VPC.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-enhancedvpcrouting
        '''
        result = self._values.get("enhanced_vpc_routing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''The maximum data-warehouse capacity Amazon Redshift Serverless uses to serve queries.

        The max capacity is specified in RPUs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-maxcapacity
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def namespace_name(self) -> typing.Optional[builtins.str]:
        '''The namespace the workgroup is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-namespacename
        '''
        result = self._values.get("namespace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The custom port to use when connecting to a workgroup.

        Valid port ranges are 5431-5455 and 8191-8215. The default is 5439.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def price_performance_target(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.PerformanceTargetProperty"]]:
        '''An object that represents the price performance target settings for the workgroup.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-priceperformancetarget
        '''
        result = self._values.get("price_performance_target")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.PerformanceTargetProperty"]], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that specifies whether the workgroup can be accessible from a public network.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def recovery_point_id(self) -> typing.Optional[builtins.str]:
        '''The recovery point id to restore from.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-recoverypointid
        '''
        result = self._values.get("recovery_point_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group IDs to associate with the workgroup.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the snapshot to restore from.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-snapshotarn
        '''
        result = self._values.get("snapshot_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The snapshot name to restore from.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-snapshotname
        '''
        result = self._values.get("snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_owner_account(self) -> typing.Optional[builtins.str]:
        '''The Amazon Web Services account that owns the snapshot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-snapshotowneraccount
        '''
        result = self._values.get("snapshot_owner_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of subnet IDs the workgroup is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The map of the key-value pairs used to tag the workgroup.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def track_name(self) -> typing.Optional[builtins.str]:
        '''An optional parameter for the name of the track for the workgroup.

        If you don't provide a track name, the workgroup is assigned to the current track.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-trackname
        '''
        result = self._values.get("track_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workgroup(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.WorkgroupProperty"]]:
        '''The collection of computing resources from which an endpoint is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-workgroup
        '''
        result = self._values.get("workgroup")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.WorkgroupProperty"]], result)

    @builtins.property
    def workgroup_name(self) -> typing.Optional[builtins.str]:
        '''The name of the workgroup.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html#cfn-redshiftserverless-workgroup-workgroupname
        '''
        result = self._values.get("workgroup_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkgroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkgroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnWorkgroupPropsMixin",
):
    '''The collection of compute resources in Amazon Redshift Serverless.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshiftserverless-workgroup.html
    :cloudformationResource: AWS::RedshiftServerless::Workgroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
        
        cfn_workgroup_props_mixin = redshiftserverless_mixins.CfnWorkgroupPropsMixin(redshiftserverless_mixins.CfnWorkgroupMixinProps(
            base_capacity=123,
            config_parameters=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.ConfigParameterProperty(
                parameter_key="parameterKey",
                parameter_value="parameterValue"
            )],
            enhanced_vpc_routing=False,
            max_capacity=123,
            namespace_name="namespaceName",
            port=123,
            price_performance_target=redshiftserverless_mixins.CfnWorkgroupPropsMixin.PerformanceTargetProperty(
                level=123,
                status="status"
            ),
            publicly_accessible=False,
            recovery_point_id="recoveryPointId",
            security_group_ids=["securityGroupIds"],
            snapshot_arn="snapshotArn",
            snapshot_name="snapshotName",
            snapshot_owner_account="snapshotOwnerAccount",
            subnet_ids=["subnetIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            track_name="trackName",
            workgroup=redshiftserverless_mixins.CfnWorkgroupPropsMixin.WorkgroupProperty(
                base_capacity=123,
                config_parameters=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.ConfigParameterProperty(
                    parameter_key="parameterKey",
                    parameter_value="parameterValue"
                )],
                creation_date="creationDate",
                endpoint=redshiftserverless_mixins.CfnWorkgroupPropsMixin.EndpointProperty(
                    address="address",
                    port=123,
                    vpc_endpoints=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.VpcEndpointProperty(
                        network_interfaces=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.NetworkInterfaceProperty(
                            availability_zone="availabilityZone",
                            network_interface_id="networkInterfaceId",
                            private_ip_address="privateIpAddress",
                            subnet_id="subnetId"
                        )],
                        vpc_endpoint_id="vpcEndpointId",
                        vpc_id="vpcId"
                    )]
                ),
                enhanced_vpc_routing=False,
                max_capacity=123,
                namespace_name="namespaceName",
                price_performance_target=redshiftserverless_mixins.CfnWorkgroupPropsMixin.PerformanceTargetProperty(
                    level=123,
                    status="status"
                ),
                publicly_accessible=False,
                security_group_ids=["securityGroupIds"],
                status="status",
                subnet_ids=["subnetIds"],
                track_name="trackName",
                workgroup_arn="workgroupArn",
                workgroup_id="workgroupId",
                workgroup_name="workgroupName"
            ),
            workgroup_name="workgroupName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWorkgroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RedshiftServerless::Workgroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e331c38730f6d920616af20a7b86db8d214a917292fa64360f628718200140f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6cc225a97f7a0dc9c62966e9567db712a738649190ca70c351144231a295520)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349024edf6e9aab051b8e52d214774f23f049cbeb6b1babbacb6ec84478358b8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkgroupMixinProps:
        return typing.cast(CfnWorkgroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnWorkgroupPropsMixin.ConfigParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_key": "parameterKey",
            "parameter_value": "parameterValue",
        },
    )
    class ConfigParameterProperty:
        def __init__(
            self,
            *,
            parameter_key: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A array of parameters to set for more control over a serverless database.

            :param parameter_key: The key of the parameter. The options are ``auto_mv`` , ``datestyle`` , ``enable_case_sensitive_identifier`` , ``enable_user_activity_logging`` , ``query_group`` , ``search_path`` , ``require_ssl`` , ``use_fips_ssl`` , and query monitoring metrics that let you define performance boundaries. For more information about query monitoring rules and available metrics, see `Query monitoring metrics for Amazon Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/dg/cm-c-wlm-query-monitoring-rules.html#cm-c-wlm-query-monitoring-metrics-serverless>`_ .
            :param parameter_value: The value of the parameter to set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-configparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
                
                config_parameter_property = redshiftserverless_mixins.CfnWorkgroupPropsMixin.ConfigParameterProperty(
                    parameter_key="parameterKey",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a63bbb8b34a24dc07e5d8d0d9a5ed941ecd05f305cc93de99384875989d7286f)
                check_type(argname="argument parameter_key", value=parameter_key, expected_type=type_hints["parameter_key"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_key is not None:
                self._values["parameter_key"] = parameter_key
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def parameter_key(self) -> typing.Optional[builtins.str]:
            '''The key of the parameter.

            The options are ``auto_mv`` , ``datestyle`` , ``enable_case_sensitive_identifier`` , ``enable_user_activity_logging`` , ``query_group`` , ``search_path`` , ``require_ssl`` , ``use_fips_ssl`` , and query monitoring metrics that let you define performance boundaries. For more information about query monitoring rules and available metrics, see `Query monitoring metrics for Amazon Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/dg/cm-c-wlm-query-monitoring-rules.html#cm-c-wlm-query-monitoring-metrics-serverless>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-configparameter.html#cfn-redshiftserverless-workgroup-configparameter-parameterkey
            '''
            result = self._values.get("parameter_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''The value of the parameter to set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-configparameter.html#cfn-redshiftserverless-workgroup-configparameter-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnWorkgroupPropsMixin.EndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address": "address",
            "port": "port",
            "vpc_endpoints": "vpcEndpoints",
        },
    )
    class EndpointProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            vpc_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkgroupPropsMixin.VpcEndpointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The VPC endpoint object.

            :param address: The DNS address of the VPC endpoint.
            :param port: The port that Amazon Redshift Serverless listens on.
            :param vpc_endpoints: An array of ``VpcEndpoint`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-endpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
                
                endpoint_property = redshiftserverless_mixins.CfnWorkgroupPropsMixin.EndpointProperty(
                    address="address",
                    port=123,
                    vpc_endpoints=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.VpcEndpointProperty(
                        network_interfaces=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.NetworkInterfaceProperty(
                            availability_zone="availabilityZone",
                            network_interface_id="networkInterfaceId",
                            private_ip_address="privateIpAddress",
                            subnet_id="subnetId"
                        )],
                        vpc_endpoint_id="vpcEndpointId",
                        vpc_id="vpcId"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__428041ace492183ac61fda1a7aa985b0cf3138532f7965016755a44d55486ea0)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument vpc_endpoints", value=vpc_endpoints, expected_type=type_hints["vpc_endpoints"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if port is not None:
                self._values["port"] = port
            if vpc_endpoints is not None:
                self._values["vpc_endpoints"] = vpc_endpoints

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The DNS address of the VPC endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-endpoint.html#cfn-redshiftserverless-workgroup-endpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port that Amazon Redshift Serverless listens on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-endpoint.html#cfn-redshiftserverless-workgroup-endpoint-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def vpc_endpoints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.VpcEndpointProperty"]]]]:
            '''An array of ``VpcEndpoint`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-endpoint.html#cfn-redshiftserverless-workgroup-endpoint-vpcendpoints
            '''
            result = self._values.get("vpc_endpoints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.VpcEndpointProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnWorkgroupPropsMixin.NetworkInterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "network_interface_id": "networkInterfaceId",
            "private_ip_address": "privateIpAddress",
            "subnet_id": "subnetId",
        },
    )
    class NetworkInterfaceProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            network_interface_id: typing.Optional[builtins.str] = None,
            private_ip_address: typing.Optional[builtins.str] = None,
            subnet_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a network interface in an Amazon Redshift Serverless managed VPC endpoint.

            :param availability_zone: The availability Zone.
            :param network_interface_id: The unique identifier of the network interface.
            :param private_ip_address: The IPv4 address of the network interface within the subnet.
            :param subnet_id: The unique identifier of the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-networkinterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
                
                network_interface_property = redshiftserverless_mixins.CfnWorkgroupPropsMixin.NetworkInterfaceProperty(
                    availability_zone="availabilityZone",
                    network_interface_id="networkInterfaceId",
                    private_ip_address="privateIpAddress",
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b71ffe6cfdb14ae068840462f17742b44b7674cc6a8c9f473516fe81a3444bfc)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
                check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if network_interface_id is not None:
                self._values["network_interface_id"] = network_interface_id
            if private_ip_address is not None:
                self._values["private_ip_address"] = private_ip_address
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The availability Zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-networkinterface.html#cfn-redshiftserverless-workgroup-networkinterface-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_interface_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the network interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-networkinterface.html#cfn-redshiftserverless-workgroup-networkinterface-networkinterfaceid
            '''
            result = self._values.get("network_interface_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_ip_address(self) -> typing.Optional[builtins.str]:
            '''The IPv4 address of the network interface within the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-networkinterface.html#cfn-redshiftserverless-workgroup-networkinterface-privateipaddress
            '''
            result = self._values.get("private_ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-networkinterface.html#cfn-redshiftserverless-workgroup-networkinterface-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkInterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnWorkgroupPropsMixin.PerformanceTargetProperty",
        jsii_struct_bases=[],
        name_mapping={"level": "level", "status": "status"},
    )
    class PerformanceTargetProperty:
        def __init__(
            self,
            *,
            level: typing.Optional[jsii.Number] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the price performance target settings for the workgroup.

            :param level: The target price performance level for the workgroup. Valid values include 1, 25, 50, 75, and 100. These correspond to the price performance levels LOW_COST, ECONOMICAL, BALANCED, RESOURCEFUL, and HIGH_PERFORMANCE.
            :param status: Whether the price performance target is enabled for the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-performancetarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
                
                performance_target_property = redshiftserverless_mixins.CfnWorkgroupPropsMixin.PerformanceTargetProperty(
                    level=123,
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9db1732385af334c5ff64a441df8544b611e20723c0b224e741534025b4060a9)
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if level is not None:
                self._values["level"] = level
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def level(self) -> typing.Optional[jsii.Number]:
            '''The target price performance level for the workgroup.

            Valid values include 1, 25, 50, 75, and 100. These correspond to the price performance levels LOW_COST, ECONOMICAL, BALANCED, RESOURCEFUL, and HIGH_PERFORMANCE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-performancetarget.html#cfn-redshiftserverless-workgroup-performancetarget-level
            '''
            result = self._values.get("level")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Whether the price performance target is enabled for the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-performancetarget.html#cfn-redshiftserverless-workgroup-performancetarget-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PerformanceTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnWorkgroupPropsMixin.VpcEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "network_interfaces": "networkInterfaces",
            "vpc_endpoint_id": "vpcEndpointId",
            "vpc_id": "vpcId",
        },
    )
    class VpcEndpointProperty:
        def __init__(
            self,
            *,
            network_interfaces: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkgroupPropsMixin.NetworkInterfaceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            vpc_endpoint_id: typing.Optional[builtins.str] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connection endpoint for connecting to Amazon Redshift Serverless through the proxy.

            :param network_interfaces: One or more network interfaces of the endpoint. Also known as an interface endpoint.
            :param vpc_endpoint_id: The connection endpoint ID for connecting to Amazon Redshift Serverless.
            :param vpc_id: The VPC identifier that the endpoint is associated with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-vpcendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
                
                vpc_endpoint_property = redshiftserverless_mixins.CfnWorkgroupPropsMixin.VpcEndpointProperty(
                    network_interfaces=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.NetworkInterfaceProperty(
                        availability_zone="availabilityZone",
                        network_interface_id="networkInterfaceId",
                        private_ip_address="privateIpAddress",
                        subnet_id="subnetId"
                    )],
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7727cd6197013e4670800f880a0d6d6d2a4b55ca1bc37be123a18ed983d2b43)
                check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
                check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_interfaces is not None:
                self._values["network_interfaces"] = network_interfaces
            if vpc_endpoint_id is not None:
                self._values["vpc_endpoint_id"] = vpc_endpoint_id
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def network_interfaces(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.NetworkInterfaceProperty"]]]]:
            '''One or more network interfaces of the endpoint.

            Also known as an interface endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-vpcendpoint.html#cfn-redshiftserverless-workgroup-vpcendpoint-networkinterfaces
            '''
            result = self._values.get("network_interfaces")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.NetworkInterfaceProperty"]]]], result)

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
            '''The connection endpoint ID for connecting to Amazon Redshift Serverless.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-vpcendpoint.html#cfn-redshiftserverless-workgroup-vpcendpoint-vpcendpointid
            '''
            result = self._values.get("vpc_endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The VPC identifier that the endpoint is associated with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-vpcendpoint.html#cfn-redshiftserverless-workgroup-vpcendpoint-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshiftserverless.mixins.CfnWorkgroupPropsMixin.WorkgroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_capacity": "baseCapacity",
            "config_parameters": "configParameters",
            "creation_date": "creationDate",
            "endpoint": "endpoint",
            "enhanced_vpc_routing": "enhancedVpcRouting",
            "max_capacity": "maxCapacity",
            "namespace_name": "namespaceName",
            "price_performance_target": "pricePerformanceTarget",
            "publicly_accessible": "publiclyAccessible",
            "security_group_ids": "securityGroupIds",
            "status": "status",
            "subnet_ids": "subnetIds",
            "track_name": "trackName",
            "workgroup_arn": "workgroupArn",
            "workgroup_id": "workgroupId",
            "workgroup_name": "workgroupName",
        },
    )
    class WorkgroupProperty:
        def __init__(
            self,
            *,
            base_capacity: typing.Optional[jsii.Number] = None,
            config_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkgroupPropsMixin.ConfigParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            creation_date: typing.Optional[builtins.str] = None,
            endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkgroupPropsMixin.EndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enhanced_vpc_routing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_capacity: typing.Optional[jsii.Number] = None,
            namespace_name: typing.Optional[builtins.str] = None,
            price_performance_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkgroupPropsMixin.PerformanceTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            status: typing.Optional[builtins.str] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            track_name: typing.Optional[builtins.str] = None,
            workgroup_arn: typing.Optional[builtins.str] = None,
            workgroup_id: typing.Optional[builtins.str] = None,
            workgroup_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The collection of computing resources from which an endpoint is created.

            :param base_capacity: The base data warehouse capacity of the workgroup in Redshift Processing Units (RPUs).
            :param config_parameters: An array of parameters to set for advanced control over a database. The options are ``auto_mv`` , ``datestyle`` , ``enable_case_sensitive_identifier`` , ``enable_user_activity_logging`` , ``query_group`` , ``search_path`` , ``require_ssl`` , ``use_fips_ssl`` , and query monitoring metrics that let you define performance boundaries. For more information about query monitoring rules and available metrics, see `Query monitoring metrics for Amazon Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/dg/cm-c-wlm-query-monitoring-rules.html#cm-c-wlm-query-monitoring-metrics-serverless>`_ .
            :param creation_date: The creation date of the workgroup.
            :param endpoint: The endpoint that is created from the workgroup.
            :param enhanced_vpc_routing: The value that specifies whether to enable enhanced virtual private cloud (VPC) routing, which forces Amazon Redshift Serverless to route traffic through your VPC.
            :param max_capacity: The maximum data-warehouse capacity Amazon Redshift Serverless uses to serve queries. The max capacity is specified in RPUs.
            :param namespace_name: The namespace the workgroup is associated with.
            :param price_performance_target: An object that represents the price performance target settings for the workgroup.
            :param publicly_accessible: A value that specifies whether the workgroup can be accessible from a public network.
            :param security_group_ids: An array of security group IDs to associate with the workgroup.
            :param status: The status of the workgroup.
            :param subnet_ids: An array of subnet IDs the workgroup is associated with.
            :param track_name: The name of the track for the workgroup.
            :param workgroup_arn: The Amazon Resource Name (ARN) that links to the workgroup.
            :param workgroup_id: The unique identifier of the workgroup.
            :param workgroup_name: The name of the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshiftserverless import mixins as redshiftserverless_mixins
                
                workgroup_property = redshiftserverless_mixins.CfnWorkgroupPropsMixin.WorkgroupProperty(
                    base_capacity=123,
                    config_parameters=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.ConfigParameterProperty(
                        parameter_key="parameterKey",
                        parameter_value="parameterValue"
                    )],
                    creation_date="creationDate",
                    endpoint=redshiftserverless_mixins.CfnWorkgroupPropsMixin.EndpointProperty(
                        address="address",
                        port=123,
                        vpc_endpoints=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.VpcEndpointProperty(
                            network_interfaces=[redshiftserverless_mixins.CfnWorkgroupPropsMixin.NetworkInterfaceProperty(
                                availability_zone="availabilityZone",
                                network_interface_id="networkInterfaceId",
                                private_ip_address="privateIpAddress",
                                subnet_id="subnetId"
                            )],
                            vpc_endpoint_id="vpcEndpointId",
                            vpc_id="vpcId"
                        )]
                    ),
                    enhanced_vpc_routing=False,
                    max_capacity=123,
                    namespace_name="namespaceName",
                    price_performance_target=redshiftserverless_mixins.CfnWorkgroupPropsMixin.PerformanceTargetProperty(
                        level=123,
                        status="status"
                    ),
                    publicly_accessible=False,
                    security_group_ids=["securityGroupIds"],
                    status="status",
                    subnet_ids=["subnetIds"],
                    track_name="trackName",
                    workgroup_arn="workgroupArn",
                    workgroup_id="workgroupId",
                    workgroup_name="workgroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__995378f34fa6c065c0452047e4cbd224ac21a0469da88dfd7215ec90cfc4363b)
                check_type(argname="argument base_capacity", value=base_capacity, expected_type=type_hints["base_capacity"])
                check_type(argname="argument config_parameters", value=config_parameters, expected_type=type_hints["config_parameters"])
                check_type(argname="argument creation_date", value=creation_date, expected_type=type_hints["creation_date"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument enhanced_vpc_routing", value=enhanced_vpc_routing, expected_type=type_hints["enhanced_vpc_routing"])
                check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
                check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
                check_type(argname="argument price_performance_target", value=price_performance_target, expected_type=type_hints["price_performance_target"])
                check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
                check_type(argname="argument track_name", value=track_name, expected_type=type_hints["track_name"])
                check_type(argname="argument workgroup_arn", value=workgroup_arn, expected_type=type_hints["workgroup_arn"])
                check_type(argname="argument workgroup_id", value=workgroup_id, expected_type=type_hints["workgroup_id"])
                check_type(argname="argument workgroup_name", value=workgroup_name, expected_type=type_hints["workgroup_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_capacity is not None:
                self._values["base_capacity"] = base_capacity
            if config_parameters is not None:
                self._values["config_parameters"] = config_parameters
            if creation_date is not None:
                self._values["creation_date"] = creation_date
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if enhanced_vpc_routing is not None:
                self._values["enhanced_vpc_routing"] = enhanced_vpc_routing
            if max_capacity is not None:
                self._values["max_capacity"] = max_capacity
            if namespace_name is not None:
                self._values["namespace_name"] = namespace_name
            if price_performance_target is not None:
                self._values["price_performance_target"] = price_performance_target
            if publicly_accessible is not None:
                self._values["publicly_accessible"] = publicly_accessible
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if status is not None:
                self._values["status"] = status
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids
            if track_name is not None:
                self._values["track_name"] = track_name
            if workgroup_arn is not None:
                self._values["workgroup_arn"] = workgroup_arn
            if workgroup_id is not None:
                self._values["workgroup_id"] = workgroup_id
            if workgroup_name is not None:
                self._values["workgroup_name"] = workgroup_name

        @builtins.property
        def base_capacity(self) -> typing.Optional[jsii.Number]:
            '''The base data warehouse capacity of the workgroup in Redshift Processing Units (RPUs).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-basecapacity
            '''
            result = self._values.get("base_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def config_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.ConfigParameterProperty"]]]]:
            '''An array of parameters to set for advanced control over a database.

            The options are ``auto_mv`` , ``datestyle`` , ``enable_case_sensitive_identifier`` , ``enable_user_activity_logging`` , ``query_group`` , ``search_path`` , ``require_ssl`` , ``use_fips_ssl`` , and query monitoring metrics that let you define performance boundaries. For more information about query monitoring rules and available metrics, see `Query monitoring metrics for Amazon Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/dg/cm-c-wlm-query-monitoring-rules.html#cm-c-wlm-query-monitoring-metrics-serverless>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-configparameters
            '''
            result = self._values.get("config_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.ConfigParameterProperty"]]]], result)

        @builtins.property
        def creation_date(self) -> typing.Optional[builtins.str]:
            '''The creation date of the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-creationdate
            '''
            result = self._values.get("creation_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.EndpointProperty"]]:
            '''The endpoint that is created from the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.EndpointProperty"]], result)

        @builtins.property
        def enhanced_vpc_routing(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The value that specifies whether to enable enhanced virtual private cloud (VPC) routing, which forces Amazon Redshift Serverless to route traffic through your VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-enhancedvpcrouting
            '''
            result = self._values.get("enhanced_vpc_routing")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            '''The maximum data-warehouse capacity Amazon Redshift Serverless uses to serve queries.

            The max capacity is specified in RPUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-maxcapacity
            '''
            result = self._values.get("max_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def namespace_name(self) -> typing.Optional[builtins.str]:
            '''The namespace the workgroup is associated with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-namespacename
            '''
            result = self._values.get("namespace_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def price_performance_target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.PerformanceTargetProperty"]]:
            '''An object that represents the price performance target settings for the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-priceperformancetarget
            '''
            result = self._values.get("price_performance_target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkgroupPropsMixin.PerformanceTargetProperty"]], result)

        @builtins.property
        def publicly_accessible(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that specifies whether the workgroup can be accessible from a public network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-publiclyaccessible
            '''
            result = self._values.get("publicly_accessible")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of security group IDs to associate with the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of subnet IDs the workgroup is associated with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def track_name(self) -> typing.Optional[builtins.str]:
            '''The name of the track for the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-trackname
            '''
            result = self._values.get("track_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workgroup_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) that links to the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-workgrouparn
            '''
            result = self._values.get("workgroup_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workgroup_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-workgroupid
            '''
            result = self._values.get("workgroup_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workgroup_name(self) -> typing.Optional[builtins.str]:
            '''The name of the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshiftserverless-workgroup-workgroup.html#cfn-redshiftserverless-workgroup-workgroup-workgroupname
            '''
            result = self._values.get("workgroup_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkgroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnNamespaceMixinProps",
    "CfnNamespacePropsMixin",
    "CfnSnapshotMixinProps",
    "CfnSnapshotPropsMixin",
    "CfnWorkgroupMixinProps",
    "CfnWorkgroupPropsMixin",
]

publication.publish()

def _typecheckingstub__12caf34ce16a040b23c6f0cbae0fea444374587464aa8e977ee3f3a3f36d884c(
    *,
    admin_password_secret_kms_key_id: typing.Optional[builtins.str] = None,
    admin_username: typing.Optional[builtins.str] = None,
    admin_user_password: typing.Optional[builtins.str] = None,
    db_name: typing.Optional[builtins.str] = None,
    default_iam_role_arn: typing.Optional[builtins.str] = None,
    final_snapshot_name: typing.Optional[builtins.str] = None,
    final_snapshot_retention_period: typing.Optional[jsii.Number] = None,
    iam_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
    manage_admin_password: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    namespace_name: typing.Optional[builtins.str] = None,
    namespace_resource_policy: typing.Any = None,
    redshift_idc_application_arn: typing.Optional[builtins.str] = None,
    snapshot_copy_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNamespacePropsMixin.SnapshotCopyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87396856dcdb3e1d25836c558050697de375a9723dbf3f5f679a9f83272f7fd4(
    props: typing.Union[CfnNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a9c22c041d9849335cc9285f679635d11f4ef15a20ef5774ceae8f866c4311(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5426aa0e69dd2d0ecd54a7cdfb92ddc5b7bc7430fc03dd7902df5fd3f115e40(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff413b13be8348e48568d9263969a1a822550303933983a3fa8a1fdfb21ddd6d(
    *,
    admin_password_secret_arn: typing.Optional[builtins.str] = None,
    admin_password_secret_kms_key_id: typing.Optional[builtins.str] = None,
    admin_username: typing.Optional[builtins.str] = None,
    creation_date: typing.Optional[builtins.str] = None,
    db_name: typing.Optional[builtins.str] = None,
    default_iam_role_arn: typing.Optional[builtins.str] = None,
    iam_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace_arn: typing.Optional[builtins.str] = None,
    namespace_id: typing.Optional[builtins.str] = None,
    namespace_name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3006635c687b31a3b74db41e5b3754f904274e573e1200753fbd2e40dbba5578(
    *,
    destination_kms_key_id: typing.Optional[builtins.str] = None,
    destination_region: typing.Optional[builtins.str] = None,
    snapshot_retention_period: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e36a99770b839a69eca7a652bedb2a8bb5ac34265cb5b51fbeec4e3ae4763f(
    *,
    namespace_name: typing.Optional[builtins.str] = None,
    retention_period: typing.Optional[jsii.Number] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f711b2102a6237fb561dc29ee147bf3bb018a9019dd4d4e2405803d8c6e7c1(
    props: typing.Union[CfnSnapshotMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d522c66e6a0a0aa0180c10359d4f1dbdcaed318cf844b958d46113683f6cc7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91158730fdf307eb12bc605b69755ec2faa0f010b7a847ccfb94e408efb7ec0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ee4b525ed89078e5affbb02c24443fbaff82aa04ced2e08ccc049b49b5df20(
    *,
    admin_username: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    namespace_arn: typing.Optional[builtins.str] = None,
    namespace_name: typing.Optional[builtins.str] = None,
    owner_account: typing.Optional[builtins.str] = None,
    retention_period: typing.Optional[jsii.Number] = None,
    snapshot_arn: typing.Optional[builtins.str] = None,
    snapshot_create_time: typing.Optional[builtins.str] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25dcf158a7219c7a3eeef48297c2ae320502f75d819b76a687026c2ef6c0cb5(
    *,
    base_capacity: typing.Optional[jsii.Number] = None,
    config_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkgroupPropsMixin.ConfigParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    enhanced_vpc_routing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    namespace_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    price_performance_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkgroupPropsMixin.PerformanceTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    recovery_point_id: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_arn: typing.Optional[builtins.str] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    snapshot_owner_account: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    track_name: typing.Optional[builtins.str] = None,
    workgroup: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkgroupPropsMixin.WorkgroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    workgroup_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e331c38730f6d920616af20a7b86db8d214a917292fa64360f628718200140f0(
    props: typing.Union[CfnWorkgroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cc225a97f7a0dc9c62966e9567db712a738649190ca70c351144231a295520(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349024edf6e9aab051b8e52d214774f23f049cbeb6b1babbacb6ec84478358b8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63bbb8b34a24dc07e5d8d0d9a5ed941ecd05f305cc93de99384875989d7286f(
    *,
    parameter_key: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428041ace492183ac61fda1a7aa985b0cf3138532f7965016755a44d55486ea0(
    *,
    address: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    vpc_endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkgroupPropsMixin.VpcEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71ffe6cfdb14ae068840462f17742b44b7674cc6a8c9f473516fe81a3444bfc(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    network_interface_id: typing.Optional[builtins.str] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db1732385af334c5ff64a441df8544b611e20723c0b224e741534025b4060a9(
    *,
    level: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7727cd6197013e4670800f880a0d6d6d2a4b55ca1bc37be123a18ed983d2b43(
    *,
    network_interfaces: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkgroupPropsMixin.NetworkInterfaceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995378f34fa6c065c0452047e4cbd224ac21a0469da88dfd7215ec90cfc4363b(
    *,
    base_capacity: typing.Optional[jsii.Number] = None,
    config_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkgroupPropsMixin.ConfigParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    creation_date: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkgroupPropsMixin.EndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enhanced_vpc_routing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    namespace_name: typing.Optional[builtins.str] = None,
    price_performance_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkgroupPropsMixin.PerformanceTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    track_name: typing.Optional[builtins.str] = None,
    workgroup_arn: typing.Optional[builtins.str] = None,
    workgroup_id: typing.Optional[builtins.str] = None,
    workgroup_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
