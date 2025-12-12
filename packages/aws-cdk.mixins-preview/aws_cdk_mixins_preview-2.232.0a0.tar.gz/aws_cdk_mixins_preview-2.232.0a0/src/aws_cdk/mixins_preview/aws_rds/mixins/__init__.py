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
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnCustomDBEngineVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_installation_files_s3_bucket_name": "databaseInstallationFilesS3BucketName",
        "database_installation_files_s3_prefix": "databaseInstallationFilesS3Prefix",
        "description": "description",
        "engine": "engine",
        "engine_version": "engineVersion",
        "image_id": "imageId",
        "kms_key_id": "kmsKeyId",
        "manifest": "manifest",
        "source_custom_db_engine_version_identifier": "sourceCustomDbEngineVersionIdentifier",
        "status": "status",
        "tags": "tags",
        "use_aws_provided_latest_image": "useAwsProvidedLatestImage",
    },
)
class CfnCustomDBEngineVersionMixinProps:
    def __init__(
        self,
        *,
        database_installation_files_s3_bucket_name: typing.Optional[builtins.str] = None,
        database_installation_files_s3_prefix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        manifest: typing.Optional[builtins.str] = None,
        source_custom_db_engine_version_identifier: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        use_aws_provided_latest_image: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnCustomDBEngineVersionPropsMixin.

        :param database_installation_files_s3_bucket_name: The name of an Amazon S3 bucket that contains database installation files for your CEV. For example, a valid bucket name is ``my-custom-installation-files`` .
        :param database_installation_files_s3_prefix: The Amazon S3 directory that contains the database installation files for your CEV. For example, a valid bucket name is ``123456789012/cev1`` . If this setting isn't specified, no prefix is assumed.
        :param description: An optional description of your CEV.
        :param engine: The database engine to use for your custom engine version (CEV). Valid values: - ``custom-oracle-ee`` - ``custom-oracle-ee-cdb``
        :param engine_version: The name of your CEV. The name format is ``major version.customized_string`` . For example, a valid CEV name is ``19.my_cev1`` . This setting is required for RDS Custom for Oracle, but optional for Amazon RDS. The combination of ``Engine`` and ``EngineVersion`` is unique per customer per Region. *Constraints:* Minimum length is 1. Maximum length is 60. *Pattern:* ``^[a-z0-9_.-]{1,60$`` }
        :param image_id: A value that indicates the ID of the AMI.
        :param kms_key_id: The AWS KMS key identifier for an encrypted CEV. A symmetric encryption KMS key is required for RDS Custom, but optional for Amazon RDS. If you have an existing symmetric encryption KMS key in your account, you can use it with RDS Custom. No further action is necessary. If you don't already have a symmetric encryption KMS key in your account, follow the instructions in `Creating a symmetric encryption KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk>`_ in the *AWS Key Management Service Developer Guide* . You can choose the same symmetric encryption key when you create a CEV and a DB instance, or choose different keys.
        :param manifest: The CEV manifest, which is a JSON document that describes the installation .zip files stored in Amazon S3. Specify the name/value pairs in a file or a quoted string. RDS Custom applies the patches in the order in which they are listed. The following JSON fields are valid: - **MediaImportTemplateVersion** - Version of the CEV manifest. The date is in the format ``YYYY-MM-DD`` . - **databaseInstallationFileNames** - Ordered list of installation files for the CEV. - **opatchFileNames** - Ordered list of OPatch installers used for the Oracle DB engine. - **psuRuPatchFileNames** - The PSU and RU patches for this CEV. - **OtherPatchFileNames** - The patches that are not in the list of PSU and RU patches. Amazon RDS applies these patches after applying the PSU and RU patches. For more information, see `Creating the CEV manifest <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-cev.html#custom-cev.preparing.manifest>`_ in the *Amazon RDS User Guide* .
        :param source_custom_db_engine_version_identifier: The ARN of a CEV to use as a source for creating a new CEV. You can specify a different Amazon Machine Imagine (AMI) by using either ``Source`` or ``UseAwsProvidedLatestImage`` . You can't specify a different JSON manifest when you specify ``SourceCustomDbEngineVersionIdentifier`` .
        :param status: A value that indicates the status of a custom engine version (CEV). Default: - "available"
        :param tags: A list of tags. For more information, see `Tagging Amazon RDS Resources <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html>`_ in the *Amazon RDS User Guide.*
        :param use_aws_provided_latest_image: Specifies whether to use the latest service-provided Amazon Machine Image (AMI) for the CEV. If you specify ``UseAwsProvidedLatestImage`` , you can't also specify ``ImageId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_custom_dBEngine_version_mixin_props = rds_mixins.CfnCustomDBEngineVersionMixinProps(
                database_installation_files_s3_bucket_name="databaseInstallationFilesS3BucketName",
                database_installation_files_s3_prefix="databaseInstallationFilesS3Prefix",
                description="description",
                engine="engine",
                engine_version="engineVersion",
                image_id="imageId",
                kms_key_id="kmsKeyId",
                manifest="manifest",
                source_custom_db_engine_version_identifier="sourceCustomDbEngineVersionIdentifier",
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                use_aws_provided_latest_image=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6488da1eaa721a066c7a3dfb2e60c84e891fa17a4cce0642a271277c13505e)
            check_type(argname="argument database_installation_files_s3_bucket_name", value=database_installation_files_s3_bucket_name, expected_type=type_hints["database_installation_files_s3_bucket_name"])
            check_type(argname="argument database_installation_files_s3_prefix", value=database_installation_files_s3_prefix, expected_type=type_hints["database_installation_files_s3_prefix"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
            check_type(argname="argument source_custom_db_engine_version_identifier", value=source_custom_db_engine_version_identifier, expected_type=type_hints["source_custom_db_engine_version_identifier"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument use_aws_provided_latest_image", value=use_aws_provided_latest_image, expected_type=type_hints["use_aws_provided_latest_image"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database_installation_files_s3_bucket_name is not None:
            self._values["database_installation_files_s3_bucket_name"] = database_installation_files_s3_bucket_name
        if database_installation_files_s3_prefix is not None:
            self._values["database_installation_files_s3_prefix"] = database_installation_files_s3_prefix
        if description is not None:
            self._values["description"] = description
        if engine is not None:
            self._values["engine"] = engine
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if image_id is not None:
            self._values["image_id"] = image_id
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if manifest is not None:
            self._values["manifest"] = manifest
        if source_custom_db_engine_version_identifier is not None:
            self._values["source_custom_db_engine_version_identifier"] = source_custom_db_engine_version_identifier
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if use_aws_provided_latest_image is not None:
            self._values["use_aws_provided_latest_image"] = use_aws_provided_latest_image

    @builtins.property
    def database_installation_files_s3_bucket_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The name of an Amazon S3 bucket that contains database installation files for your CEV.

        For example, a valid bucket name is ``my-custom-installation-files`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-databaseinstallationfiless3bucketname
        '''
        result = self._values.get("database_installation_files_s3_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_installation_files_s3_prefix(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 directory that contains the database installation files for your CEV.

        For example, a valid bucket name is ``123456789012/cev1`` . If this setting isn't specified, no prefix is assumed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-databaseinstallationfiless3prefix
        '''
        result = self._values.get("database_installation_files_s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of your CEV.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The database engine to use for your custom engine version (CEV).

        Valid values:

        - ``custom-oracle-ee``
        - ``custom-oracle-ee-cdb``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The name of your CEV.

        The name format is ``major version.customized_string`` . For example, a valid CEV name is ``19.my_cev1`` . This setting is required for RDS Custom for Oracle, but optional for Amazon RDS. The combination of ``Engine`` and ``EngineVersion`` is unique per customer per Region.

        *Constraints:* Minimum length is 1. Maximum length is 60.

        *Pattern:* ``^[a-z0-9_.-]{1,60$`` }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''A value that indicates the ID of the AMI.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-imageid
        '''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS KMS key identifier for an encrypted CEV.

        A symmetric encryption KMS key is required for RDS Custom, but optional for Amazon RDS.

        If you have an existing symmetric encryption KMS key in your account, you can use it with RDS Custom. No further action is necessary. If you don't already have a symmetric encryption KMS key in your account, follow the instructions in `Creating a symmetric encryption KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk>`_ in the *AWS Key Management Service Developer Guide* .

        You can choose the same symmetric encryption key when you create a CEV and a DB instance, or choose different keys.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manifest(self) -> typing.Optional[builtins.str]:
        '''The CEV manifest, which is a JSON document that describes the installation .zip files stored in Amazon S3. Specify the name/value pairs in a file or a quoted string. RDS Custom applies the patches in the order in which they are listed.

        The following JSON fields are valid:

        - **MediaImportTemplateVersion** - Version of the CEV manifest. The date is in the format ``YYYY-MM-DD`` .
        - **databaseInstallationFileNames** - Ordered list of installation files for the CEV.
        - **opatchFileNames** - Ordered list of OPatch installers used for the Oracle DB engine.
        - **psuRuPatchFileNames** - The PSU and RU patches for this CEV.
        - **OtherPatchFileNames** - The patches that are not in the list of PSU and RU patches. Amazon RDS applies these patches after applying the PSU and RU patches.

        For more information, see `Creating the CEV manifest <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-cev.html#custom-cev.preparing.manifest>`_ in the *Amazon RDS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-manifest
        '''
        result = self._values.get("manifest")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_custom_db_engine_version_identifier(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The ARN of a CEV to use as a source for creating a new CEV.

        You can specify a different Amazon Machine Imagine (AMI) by using either ``Source`` or ``UseAwsProvidedLatestImage`` . You can't specify a different JSON manifest when you specify ``SourceCustomDbEngineVersionIdentifier`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-sourcecustomdbengineversionidentifier
        '''
        result = self._values.get("source_custom_db_engine_version_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''A value that indicates the status of a custom engine version (CEV).

        :default: - "available"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags.

        For more information, see `Tagging Amazon RDS Resources <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html>`_ in the *Amazon RDS User Guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def use_aws_provided_latest_image(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to use the latest service-provided Amazon Machine Image (AMI) for the CEV.

        If you specify ``UseAwsProvidedLatestImage`` , you can't also specify ``ImageId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html#cfn-rds-customdbengineversion-useawsprovidedlatestimage
        '''
        result = self._values.get("use_aws_provided_latest_image")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomDBEngineVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCustomDBEngineVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnCustomDBEngineVersionPropsMixin",
):
    '''Creates a custom DB engine version (CEV).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-customdbengineversion.html
    :cloudformationResource: AWS::RDS::CustomDBEngineVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_custom_dBEngine_version_props_mixin = rds_mixins.CfnCustomDBEngineVersionPropsMixin(rds_mixins.CfnCustomDBEngineVersionMixinProps(
            database_installation_files_s3_bucket_name="databaseInstallationFilesS3BucketName",
            database_installation_files_s3_prefix="databaseInstallationFilesS3Prefix",
            description="description",
            engine="engine",
            engine_version="engineVersion",
            image_id="imageId",
            kms_key_id="kmsKeyId",
            manifest="manifest",
            source_custom_db_engine_version_identifier="sourceCustomDbEngineVersionIdentifier",
            status="status",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            use_aws_provided_latest_image=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCustomDBEngineVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::CustomDBEngineVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfe1e329c96032655418fdef14c9fb8593688d3e520138e05bb430c07c7ee47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1725cf4521bc20c8363c44661d11b34ebb0e815c3ec646163d18c81375d21c80)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e9fa4212139e8a339a6454e5877672906e92ee8d3dd76dd92ec057135f8d5a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCustomDBEngineVersionMixinProps:
        return typing.cast(CfnCustomDBEngineVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_storage": "allocatedStorage",
        "associated_roles": "associatedRoles",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zones": "availabilityZones",
        "backtrack_window": "backtrackWindow",
        "backup_retention_period": "backupRetentionPeriod",
        "cluster_scalability_type": "clusterScalabilityType",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "database_insights_mode": "databaseInsightsMode",
        "database_name": "databaseName",
        "db_cluster_identifier": "dbClusterIdentifier",
        "db_cluster_instance_class": "dbClusterInstanceClass",
        "db_cluster_parameter_group_name": "dbClusterParameterGroupName",
        "db_instance_parameter_group_name": "dbInstanceParameterGroupName",
        "db_subnet_group_name": "dbSubnetGroupName",
        "db_system_id": "dbSystemId",
        "delete_automated_backups": "deleteAutomatedBackups",
        "deletion_protection": "deletionProtection",
        "domain": "domain",
        "domain_iam_role_name": "domainIamRoleName",
        "enable_cloudwatch_logs_exports": "enableCloudwatchLogsExports",
        "enable_global_write_forwarding": "enableGlobalWriteForwarding",
        "enable_http_endpoint": "enableHttpEndpoint",
        "enable_iam_database_authentication": "enableIamDatabaseAuthentication",
        "enable_local_write_forwarding": "enableLocalWriteForwarding",
        "engine": "engine",
        "engine_lifecycle_support": "engineLifecycleSupport",
        "engine_mode": "engineMode",
        "engine_version": "engineVersion",
        "global_cluster_identifier": "globalClusterIdentifier",
        "iops": "iops",
        "kms_key_id": "kmsKeyId",
        "manage_master_user_password": "manageMasterUserPassword",
        "master_user_authentication_type": "masterUserAuthenticationType",
        "master_username": "masterUsername",
        "master_user_password": "masterUserPassword",
        "master_user_secret": "masterUserSecret",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role_arn": "monitoringRoleArn",
        "network_type": "networkType",
        "performance_insights_enabled": "performanceInsightsEnabled",
        "performance_insights_kms_key_id": "performanceInsightsKmsKeyId",
        "performance_insights_retention_period": "performanceInsightsRetentionPeriod",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "publicly_accessible": "publiclyAccessible",
        "replication_source_identifier": "replicationSourceIdentifier",
        "restore_to_time": "restoreToTime",
        "restore_type": "restoreType",
        "scaling_configuration": "scalingConfiguration",
        "serverless_v2_scaling_configuration": "serverlessV2ScalingConfiguration",
        "snapshot_identifier": "snapshotIdentifier",
        "source_db_cluster_identifier": "sourceDbClusterIdentifier",
        "source_db_cluster_resource_id": "sourceDbClusterResourceId",
        "source_region": "sourceRegion",
        "storage_encrypted": "storageEncrypted",
        "storage_type": "storageType",
        "tags": "tags",
        "use_latest_restorable_time": "useLatestRestorableTime",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnDBClusterMixinProps:
    def __init__(
        self,
        *,
        allocated_storage: typing.Optional[jsii.Number] = None,
        associated_roles: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDBClusterPropsMixin.DBClusterRoleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        backtrack_window: typing.Optional[jsii.Number] = None,
        backup_retention_period: typing.Optional[jsii.Number] = None,
        cluster_scalability_type: typing.Optional[builtins.str] = None,
        copy_tags_to_snapshot: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        database_insights_mode: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        db_cluster_identifier: typing.Optional[builtins.str] = None,
        db_cluster_instance_class: typing.Optional[builtins.str] = None,
        db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        db_instance_parameter_group_name: typing.Optional[builtins.str] = None,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        db_system_id: typing.Optional[builtins.str] = None,
        delete_automated_backups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_iam_role_name: typing.Optional[builtins.str] = None,
        enable_cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_global_write_forwarding: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        enable_http_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        enable_iam_database_authentication: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        enable_local_write_forwarding: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_lifecycle_support: typing.Optional[builtins.str] = None,
        engine_mode: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        global_cluster_identifier: typing.Optional[builtins.str] = None,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        manage_master_user_password: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        master_user_authentication_type: typing.Optional[builtins.str] = None,
        master_username: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[builtins.str] = None,
        master_user_secret: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDBClusterPropsMixin.MasterUserSecretProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        monitoring_interval: typing.Optional[jsii.Number] = None,
        monitoring_role_arn: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        performance_insights_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        performance_insights_kms_key_id: typing.Optional[builtins.str] = None,
        performance_insights_retention_period: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        replication_source_identifier: typing.Optional[builtins.str] = None,
        restore_to_time: typing.Optional[builtins.str] = None,
        restore_type: typing.Optional[builtins.str] = None,
        scaling_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDBClusterPropsMixin.ScalingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        serverless_v2_scaling_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDBClusterPropsMixin.ServerlessV2ScalingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        snapshot_identifier: typing.Optional[builtins.str] = None,
        source_db_cluster_identifier: typing.Optional[builtins.str] = None,
        source_db_cluster_resource_id: typing.Optional[builtins.str] = None,
        source_region: typing.Optional[builtins.str] = None,
        storage_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        use_latest_restorable_time: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnDBClusterPropsMixin.

        :param allocated_storage: The amount of storage in gibibytes (GiB) to allocate to each DB instance in the Multi-AZ DB cluster. Valid for Cluster Type: Multi-AZ DB clusters only This setting is required to create a Multi-AZ DB cluster.
        :param associated_roles: Provides a list of the AWS Identity and Access Management (IAM) roles that are associated with the DB cluster. IAM roles that are associated with a DB cluster grant permission for the DB cluster to access other Amazon Web Services on your behalf. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param auto_minor_version_upgrade: Specifies whether minor engine upgrades are applied automatically to the DB cluster during the maintenance window. By default, minor engine upgrades are applied automatically. Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB cluster. For more information about automatic minor version upgrades, see `Automatically upgrading the minor engine version <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Upgrading.html#USER_UpgradeDBInstance.Upgrading.AutoMinorVersionUpgrades>`_ .
        :param availability_zones: A list of Availability Zones (AZs) where instances in the DB cluster can be created. For information on AWS Regions and Availability Zones, see `Choosing the Regions and Availability Zones <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.RegionsAndAvailabilityZones.html>`_ in the *Amazon Aurora User Guide* . Valid for: Aurora DB clusters only
        :param backtrack_window: The target backtrack window, in seconds. To disable backtracking, set this value to ``0`` . Valid for Cluster Type: Aurora MySQL DB clusters only Default: ``0`` Constraints: - If specified, this value must be set to a number from 0 to 259,200 (72 hours).
        :param backup_retention_period: The number of days for which automated backups are retained. Default: 1 Constraints: - Must be a value from 1 to 35 Valid for: Aurora DB clusters and Multi-AZ DB clusters Default: - 1
        :param cluster_scalability_type: Specifies the scalability mode of the Aurora DB cluster. When set to ``limitless`` , the cluster operates as an Aurora Limitless Database, allowing you to create a DB shard group for horizontal scaling (sharding) capabilities. When set to ``standard`` (the default), the cluster uses normal DB instance creation. *Important:* Automated backup retention isn't supported with Aurora Limitless Database clusters. If you set this property to ``limitless`` , you cannot set ``DeleteAutomatedBackups`` to ``false`` . To create a backup, use manual snapshots instead.
        :param copy_tags_to_snapshot: A value that indicates whether to copy all tags from the DB cluster to snapshots of the DB cluster. The default is not to copy them. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param database_insights_mode: The mode of Database Insights to enable for the DB cluster. If you set this value to ``advanced`` , you must also set the ``PerformanceInsightsEnabled`` parameter to ``true`` and the ``PerformanceInsightsRetentionPeriod`` parameter to 465. Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters
        :param database_name: The name of your database. If you don't provide a name, then Amazon RDS won't create a database in this DB cluster. For naming constraints, see `Naming Constraints <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_Limits.html#RDS_Limits.Constraints>`_ in the *Amazon Aurora User Guide* . Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param db_cluster_identifier: The DB cluster identifier. This parameter is stored as a lowercase string. Constraints: - Must contain from 1 to 63 letters, numbers, or hyphens. - First character must be a letter. - Can't end with a hyphen or contain two consecutive hyphens. Example: ``my-cluster1`` Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param db_cluster_instance_class: The compute and memory capacity of each DB instance in the Multi-AZ DB cluster, for example ``db.m6gd.xlarge`` . Not all DB instance classes are available in all AWS Regions , or for all database engines. For the full list of DB instance classes and availability for your engine, see `DB instance class <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html>`_ in the *Amazon RDS User Guide* . This setting is required to create a Multi-AZ DB cluster. Valid for Cluster Type: Multi-AZ DB clusters only
        :param db_cluster_parameter_group_name: The name of the DB cluster parameter group to associate with this DB cluster. .. epigraph:: If you apply a parameter group to an existing DB cluster, then its DB instances might need to reboot. This can result in an outage while the DB instances are rebooting. If you apply a change to parameter group associated with a stopped DB cluster, then the update stack waits until the DB cluster is started. To list all of the available DB cluster parameter group names, use the following command: ``aws rds describe-db-cluster-parameter-groups --query "DBClusterParameterGroups[].DBClusterParameterGroupName" --output text`` Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param db_instance_parameter_group_name: The name of the DB parameter group to apply to all instances of the DB cluster. .. epigraph:: When you apply a parameter group using the ``DBInstanceParameterGroupName`` parameter, the DB cluster isn't rebooted automatically. Also, parameter changes are applied immediately rather than during the next maintenance window. Valid for Cluster Type: Aurora DB clusters only Default: The existing name setting Constraints: - The DB parameter group must be in the same DB parameter group family as this DB cluster. - The ``DBInstanceParameterGroupName`` parameter is valid in combination with the ``AllowMajorVersionUpgrade`` parameter for a major version upgrade only.
        :param db_subnet_group_name: A DB subnet group that you want to associate with this DB cluster. If you are restoring a DB cluster to a point in time with ``RestoreType`` set to ``copy-on-write`` , and don't specify a DB subnet group name, then the DB cluster is restored with a default DB subnet group. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param db_system_id: Reserved for future use.
        :param delete_automated_backups: Specifies whether to remove automated backups immediately after the DB cluster is deleted. This parameter isn't case-sensitive. The default is to remove automated backups immediately after the DB cluster is deleted, unless the AWS Backup policy specifies a point-in-time restore rule.
        :param deletion_protection: A value that indicates whether the DB cluster has deletion protection enabled. The database can't be deleted when deletion protection is enabled. By default, deletion protection is disabled. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param domain: Indicates the directory ID of the Active Directory to create the DB cluster. For Amazon Aurora DB clusters, Amazon RDS can use Kerberos authentication to authenticate users that connect to the DB cluster. For more information, see `Kerberos authentication <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/kerberos-authentication.html>`_ in the *Amazon Aurora User Guide* . Valid for: Aurora DB clusters only
        :param domain_iam_role_name: Specifies the name of the IAM role to use when making API calls to the Directory Service. Valid for: Aurora DB clusters only
        :param enable_cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. The values in the list depend on the DB engine being used. For more information, see `Publishing Database Logs to Amazon CloudWatch Logs <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_LogAccess.html#USER_LogAccess.Procedural.UploadtoCloudWatch>`_ in the *Amazon Aurora User Guide* . *Aurora MySQL* Valid values: ``audit`` , ``error`` , ``general`` , ``slowquery`` *Aurora PostgreSQL* Valid values: ``postgresql`` Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param enable_global_write_forwarding: Specifies whether to enable this DB cluster to forward write operations to the primary cluster of a global cluster (Aurora global database). By default, write operations are not allowed on Aurora DB clusters that are secondary clusters in an Aurora global database. You can set this value only on Aurora DB clusters that are members of an Aurora global database. With this parameter enabled, a secondary cluster can forward writes to the current primary cluster, and the resulting changes are replicated back to this cluster. For the primary DB cluster of an Aurora global database, this value is used immediately if the primary is demoted by a global cluster API operation, but it does nothing until then. Valid for Cluster Type: Aurora DB clusters only
        :param enable_http_endpoint: Specifies whether to enable the HTTP endpoint for the DB cluster. By default, the HTTP endpoint isn't enabled. When enabled, the HTTP endpoint provides a connectionless web service API (RDS Data API) for running SQL queries on the DB cluster. You can also query your database from inside the RDS console with the RDS query editor. For more information, see `Using RDS Data API <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/data-api.html>`_ in the *Amazon Aurora User Guide* . Valid for Cluster Type: Aurora DB clusters only
        :param enable_iam_database_authentication: A value that indicates whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. By default, mapping is disabled. For more information, see `IAM Database Authentication <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.IAMDBAuth.html>`_ in the *Amazon Aurora User Guide.* Valid for: Aurora DB clusters only
        :param enable_local_write_forwarding: Specifies whether read replicas can forward write operations to the writer DB instance in the DB cluster. By default, write operations aren't allowed on reader DB instances. Valid for: Aurora DB clusters only
        :param engine: The name of the database engine to be used for this DB cluster. Valid Values: - ``aurora-mysql`` - ``aurora-postgresql`` - ``mysql`` - ``postgres`` Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param engine_lifecycle_support: The life cycle type for this DB cluster. .. epigraph:: By default, this value is set to ``open-source-rds-extended-support`` , which enrolls your DB cluster into Amazon RDS Extended Support. At the end of standard support, you can avoid charges for Extended Support by setting the value to ``open-source-rds-extended-support-disabled`` . In this case, creating the DB cluster will fail if the DB major version is past its end of standard support date. You can use this setting to enroll your DB cluster into Amazon RDS Extended Support. With RDS Extended Support, you can run the selected major engine version on your DB cluster past the end of standard support for that engine version. For more information, see the following sections: - Amazon Aurora - `Amazon RDS Extended Support with Amazon Aurora <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/extended-support.html>`_ in the *Amazon Aurora User Guide* - Amazon RDS - `Amazon RDS Extended Support with Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support.html>`_ in the *Amazon RDS User Guide* Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters Valid Values: ``open-source-rds-extended-support | open-source-rds-extended-support-disabled`` Default: ``open-source-rds-extended-support``
        :param engine_mode: The DB engine mode of the DB cluster, either ``provisioned`` or ``serverless`` . The ``serverless`` engine mode only applies for Aurora Serverless v1 DB clusters. Aurora Serverless v2 DB clusters use the ``provisioned`` engine mode. For information about limitations and requirements for Serverless DB clusters, see the following sections in the *Amazon Aurora User Guide* : - `Limitations of Aurora Serverless v1 <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.html#aurora-serverless.limitations>`_ - `Requirements for Aurora Serverless v2 <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.requirements.html>`_ Valid for Cluster Type: Aurora DB clusters only
        :param engine_version: The version number of the database engine to use. To list all of the available engine versions for Aurora MySQL version 2 (5.7-compatible) and version 3 (8.0-compatible), use the following command: ``aws rds describe-db-engine-versions --engine aurora-mysql --query "DBEngineVersions[].EngineVersion"`` You can supply either ``5.7`` or ``8.0`` to use the default engine version for Aurora MySQL version 2 or version 3, respectively. To list all of the available engine versions for Aurora PostgreSQL, use the following command: ``aws rds describe-db-engine-versions --engine aurora-postgresql --query "DBEngineVersions[].EngineVersion"`` To list all of the available engine versions for RDS for MySQL, use the following command: ``aws rds describe-db-engine-versions --engine mysql --query "DBEngineVersions[].EngineVersion"`` To list all of the available engine versions for RDS for PostgreSQL, use the following command: ``aws rds describe-db-engine-versions --engine postgres --query "DBEngineVersions[].EngineVersion"`` *Aurora MySQL* For information, see `Database engine updates for Amazon Aurora MySQL <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Updates.html>`_ in the *Amazon Aurora User Guide* . *Aurora PostgreSQL* For information, see `Amazon Aurora PostgreSQL releases and engine versions <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Updates.20180305.html>`_ in the *Amazon Aurora User Guide* . *MySQL* For information, see `Amazon RDS for MySQL <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html#MySQL.Concepts.VersionMgmt>`_ in the *Amazon RDS User Guide* . *PostgreSQL* For information, see `Amazon RDS for PostgreSQL <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts>`_ in the *Amazon RDS User Guide* . Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param global_cluster_identifier: If you are configuring an Aurora global database cluster and want your Aurora DB cluster to be a secondary member in the global database cluster, specify the global cluster ID of the global database cluster. To define the primary database cluster of the global cluster, use the `AWS::RDS::GlobalCluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html>`_ resource. If you aren't configuring a global database cluster, don't specify this property. .. epigraph:: To remove the DB cluster from a global database cluster, specify an empty value for the ``GlobalClusterIdentifier`` property. For information about Aurora global databases, see `Working with Amazon Aurora Global Databases <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html>`_ in the *Amazon Aurora User Guide* . Valid for: Aurora DB clusters only
        :param iops: The amount of Provisioned IOPS (input/output operations per second) to be initially allocated for each DB instance in the Multi-AZ DB cluster. For information about valid IOPS values, see `Provisioned IOPS storage <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html#USER_PIOPS>`_ in the *Amazon RDS User Guide* . This setting is required to create a Multi-AZ DB cluster. Valid for Cluster Type: Multi-AZ DB clusters only Constraints: - Must be a multiple between .5 and 50 of the storage amount for the DB cluster.
        :param kms_key_id: The Amazon Resource Name (ARN) of the AWS KMS key that is used to encrypt the database instances in the DB cluster, such as ``arn:aws:kms:us-east-1:012345678910:key/abcd1234-a123-456a-a12b-a123b4cd56ef`` . If you enable the ``StorageEncrypted`` property but don't specify this property, the default KMS key is used. If you specify this property, you must set the ``StorageEncrypted`` property to ``true`` . If you specify the ``SnapshotIdentifier`` property, the ``StorageEncrypted`` property value is inherited from the snapshot, and if the DB cluster is encrypted, the specified ``KmsKeyId`` property is used. If you create a read replica of an encrypted DB cluster in another AWS Region, make sure to set ``KmsKeyId`` to a KMS key identifier that is valid in the destination AWS Region. This KMS key is used to encrypt the read replica in that AWS Region. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param manage_master_user_password: Specifies whether to manage the master user password with AWS Secrets Manager. For more information, see `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html>`_ in the *Amazon RDS User Guide* and `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-secrets-manager.html>`_ in the *Amazon Aurora User Guide.* Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters Constraints: - Can't manage the master user password with AWS Secrets Manager if ``MasterUserPassword`` is specified.
        :param master_user_authentication_type: Specifies the authentication type for the master user. With IAM master user authentication, you can configure the master DB user with IAM database authentication when you create a DB cluster. You can specify one of the following values: - ``password`` - Use standard database authentication with a password. - ``iam-db-auth`` - Use IAM database authentication for the master user. Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters This option is only valid for RDS for MySQL, RDS for MariaDB, RDS for PostgreSQL, Aurora MySQL, and Aurora PostgreSQL engines.
        :param master_username: The name of the master user for the DB cluster. .. epigraph:: If you specify the ``SourceDBClusterIdentifier`` , ``SnapshotIdentifier`` , or ``GlobalClusterIdentifier`` property, don't specify this property. The value is inherited from the source DB cluster, the snapshot, or the primary DB cluster for the global database cluster, respectively. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param master_user_password: The master password for the DB instance. .. epigraph:: If you specify the ``SourceDBClusterIdentifier`` , ``SnapshotIdentifier`` , or ``GlobalClusterIdentifier`` property, don't specify this property. The value is inherited from the source DB cluster, the snapshot, or the primary DB cluster for the global database cluster, respectively. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param master_user_secret: The secret managed by RDS in AWS Secrets Manager for the master user password. .. epigraph:: When you restore a DB cluster from a snapshot, Amazon RDS generates a new secret instead of reusing the secret specified in the ``SecretArn`` property. This ensures that the restored DB cluster is securely managed with a dedicated secret. To maintain consistent integration with your application, you might need to update resource configurations to reference the newly created secret. For more information, see `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html>`_ in the *Amazon RDS User Guide* and `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-secrets-manager.html>`_ in the *Amazon Aurora User Guide.*
        :param monitoring_interval: The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB cluster. To turn off collecting Enhanced Monitoring metrics, specify ``0`` . If ``MonitoringRoleArn`` is specified, also set ``MonitoringInterval`` to a value other than ``0`` . Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters Valid Values: ``0 | 1 | 5 | 10 | 15 | 30 | 60`` Default: ``0``
        :param monitoring_role_arn: The Amazon Resource Name (ARN) for the IAM role that permits RDS to send Enhanced Monitoring metrics to Amazon CloudWatch Logs. An example is ``arn:aws:iam:123456789012:role/emaccess`` . For information on creating a monitoring role, see `Setting up and enabling Enhanced Monitoring <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html#USER_Monitoring.OS.Enabling>`_ in the *Amazon RDS User Guide* . If ``MonitoringInterval`` is set to a value other than ``0`` , supply a ``MonitoringRoleArn`` value. Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters
        :param network_type: The network type of the DB cluster. Valid values: - ``IPV4`` - ``DUAL`` The network type is determined by the ``DBSubnetGroup`` specified for the DB cluster. A ``DBSubnetGroup`` can support only the IPv4 protocol or the IPv4 and IPv6 protocols ( ``DUAL`` ). For more information, see `Working with a DB instance in a VPC <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html>`_ in the *Amazon Aurora User Guide.* Valid for: Aurora DB clusters only
        :param performance_insights_enabled: Specifies whether to turn on Performance Insights for the DB cluster. For more information, see `Using Amazon Performance Insights <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html>`_ in the *Amazon RDS User Guide* . Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters
        :param performance_insights_kms_key_id: The AWS KMS key identifier for encryption of Performance Insights data. The AWS KMS key identifier is the key ARN, key ID, alias ARN, or alias name for the KMS key. If you don't specify a value for ``PerformanceInsightsKMSKeyId`` , then Amazon RDS uses your default KMS key. There is a default KMS key for your AWS account . Your AWS account has a different default KMS key for each AWS Region . Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters
        :param performance_insights_retention_period: The number of days to retain Performance Insights data. When creating a DB cluster without enabling Performance Insights, you can't specify the parameter ``PerformanceInsightsRetentionPeriod`` . Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters Valid Values: - ``7`` - *month* * 31, where *month* is a number of months from 1-23. Examples: ``93`` (3 months * 31), ``341`` (11 months * 31), ``589`` (19 months * 31) - ``731`` Default: ``7`` days If you specify a retention period that isn't valid, such as ``94`` , Amazon RDS issues an error.
        :param port: The port number on which the DB instances in the DB cluster accept connections. Default: - When ``EngineMode`` is ``provisioned`` , ``3306`` (for both Aurora MySQL and Aurora PostgreSQL) - When ``EngineMode`` is ``serverless`` : - ``3306`` when ``Engine`` is ``aurora`` or ``aurora-mysql`` - ``5432`` when ``Engine`` is ``aurora-postgresql`` .. epigraph:: The ``No interruption`` on update behavior only applies to DB clusters. If you are updating a DB instance, see `Port <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-port>`_ for the AWS::RDS::DBInstance resource. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param preferred_backup_window: The daily time range during which automated backups are created. For more information, see `Backup Window <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html#Aurora.Managing.Backups.BackupWindow>`_ in the *Amazon Aurora User Guide.* Constraints: - Must be in the format ``hh24:mi-hh24:mi`` . - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param preferred_maintenance_window: The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC). Format: ``ddd:hh24:mi-ddd:hh24:mi`` The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see `Maintaining an Amazon Aurora DB cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#AdjustingTheMaintenanceWindow.Aurora>`_ in the *Amazon Aurora User Guide.* Valid Days: Mon, Tue, Wed, Thu, Fri, Sat, Sun. Constraints: Minimum 30-minute window. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param publicly_accessible: Specifies whether the DB cluster is publicly accessible. Valid for Cluster Type: Multi-AZ DB clusters only When the DB cluster is publicly accessible and you connect from outside of the DB cluster's virtual private cloud (VPC), its domain name system (DNS) endpoint resolves to the public IP address. When you connect from within the same VPC as the DB cluster, the endpoint resolves to the private IP address. Access to the DB cluster is controlled by its security group settings. When the DB cluster isn't publicly accessible, it is an internal DB cluster with a DNS name that resolves to a private IP address. The default behavior when ``PubliclyAccessible`` is not specified depends on whether a ``DBSubnetGroup`` is specified. If ``DBSubnetGroup`` isn't specified, ``PubliclyAccessible`` defaults to ``true`` . If ``DBSubnetGroup`` is specified, ``PubliclyAccessible`` defaults to ``false`` unless the value of ``DBSubnetGroup`` is ``default`` , in which case ``PubliclyAccessible`` defaults to ``true`` . If ``PubliclyAccessible`` is true and the VPC that the ``DBSubnetGroup`` is in doesn't have an internet gateway attached to it, Amazon RDS returns an error.
        :param replication_source_identifier: The Amazon Resource Name (ARN) of the source DB instance or DB cluster if this DB cluster is created as a read replica. Valid for: Aurora DB clusters only
        :param restore_to_time: The date and time to restore the DB cluster to. Valid Values: Value must be a time in Universal Coordinated Time (UTC) format Constraints: - Must be before the latest restorable time for the DB instance - Must be specified if ``UseLatestRestorableTime`` parameter isn't provided - Can't be specified if the ``UseLatestRestorableTime`` parameter is enabled - Can't be specified if the ``RestoreType`` parameter is ``copy-on-write`` This property must be used with ``SourceDBClusterIdentifier`` property. The resulting cluster will have the identifier that matches the value of the ``DBclusterIdentifier`` property. Example: ``2015-03-07T23:45:00Z`` Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param restore_type: The type of restore to be performed. You can specify one of the following values:. - ``full-copy`` - The new DB cluster is restored as a full copy of the source DB cluster. - ``copy-on-write`` - The new DB cluster is restored as a clone of the source DB cluster. If you don't specify a ``RestoreType`` value, then the new DB cluster is restored as a full copy of the source DB cluster. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param scaling_configuration: The scaling configuration of an Aurora Serverless v1 DB cluster. This property is only supported for Aurora Serverless v1. For Aurora Serverless v2, Use the ``ServerlessV2ScalingConfiguration`` property. Valid for: Aurora Serverless v1 DB clusters only
        :param serverless_v2_scaling_configuration: The scaling configuration of an Aurora Serverless V2 DB cluster. This property is only supported for Aurora Serverless v2. For Aurora Serverless v1, Use the ``ScalingConfiguration`` property. Valid for: Aurora Serverless v2 DB clusters only
        :param snapshot_identifier: The identifier for the DB snapshot or DB cluster snapshot to restore from. You can use either the name or the Amazon Resource Name (ARN) to specify a DB cluster snapshot. However, you can use only the ARN to specify a DB snapshot. After you restore a DB cluster with a ``SnapshotIdentifier`` property, you must specify the same ``SnapshotIdentifier`` property for any future updates to the DB cluster. When you specify this property for an update, the DB cluster is not restored from the snapshot again, and the data in the database is not changed. However, if you don't specify the ``SnapshotIdentifier`` property, an empty DB cluster is created, and the original DB cluster is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB cluster is restored from the specified ``SnapshotIdentifier`` property, and the original DB cluster is deleted. If you specify the ``SnapshotIdentifier`` property to restore a DB cluster (as opposed to specifying it for DB cluster updates), then don't specify the following properties: - ``GlobalClusterIdentifier`` - ``MasterUsername`` - ``MasterUserPassword`` - ``ReplicationSourceIdentifier`` - ``RestoreType`` - ``SourceDBClusterIdentifier`` - ``SourceRegion`` - ``StorageEncrypted`` (for an encrypted snapshot) - ``UseLatestRestorableTime`` Constraints: - Must match the identifier of an existing Snapshot. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param source_db_cluster_identifier: When restoring a DB cluster to a point in time, the identifier of the source DB cluster from which to restore. Constraints: - Must match the identifier of an existing DBCluster. - Cannot be specified if ``SourceDbClusterResourceId`` is specified. You must specify either ``SourceDBClusterIdentifier`` or ``SourceDbClusterResourceId`` , but not both. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param source_db_cluster_resource_id: The resource ID of the source DB cluster from which to restore.
        :param source_region: The AWS Region which contains the source DB cluster when replicating a DB cluster. For example, ``us-east-1`` . Valid for: Aurora DB clusters only
        :param storage_encrypted: Indicates whether the DB cluster is encrypted. If you specify the ``KmsKeyId`` property, then you must enable encryption. If you specify the ``SourceDBClusterIdentifier`` property, don't specify this property. The value is inherited from the source DB cluster, and if the DB cluster is encrypted, the specified ``KmsKeyId`` property is used. If you specify the ``SnapshotIdentifier`` and the specified snapshot is encrypted, don't specify this property. The value is inherited from the snapshot, and the specified ``KmsKeyId`` property is used. If you specify the ``SnapshotIdentifier`` and the specified snapshot isn't encrypted, you can use this property to specify that the restored DB cluster is encrypted. Specify the ``KmsKeyId`` property for the KMS key to use for encryption. If you don't want the restored DB cluster to be encrypted, then don't set this property or set it to ``false`` . .. epigraph:: If you specify both the ``StorageEncrypted`` and ``SnapshotIdentifier`` properties without specifying the ``KmsKeyId`` property, then the restored DB cluster inherits the encryption settings from the DB snapshot that provide. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param storage_type: The storage type to associate with the DB cluster. For information on storage types for Aurora DB clusters, see `Storage configurations for Amazon Aurora DB clusters <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html#aurora-storage-type>`_ . For information on storage types for Multi-AZ DB clusters, see `Settings for creating Multi-AZ DB clusters <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/create-multi-az-db-cluster.html#create-multi-az-db-cluster-settings>`_ . This setting is required to create a Multi-AZ DB cluster. When specified for a Multi-AZ DB cluster, a value for the ``Iops`` parameter is required. Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters Valid Values: - Aurora DB clusters - ``aurora | aurora-iopt1`` - Multi-AZ DB clusters - ``io1 | io2 | gp3`` Default: - Aurora DB clusters - ``aurora`` - Multi-AZ DB clusters - ``io1`` .. epigraph:: When you create an Aurora DB cluster with the storage type set to ``aurora-iopt1`` , the storage type is returned in the response. The storage type isn't returned when you set it to ``aurora`` .
        :param tags: Tags to assign to the DB cluster. Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters
        :param use_latest_restorable_time: A value that indicates whether to restore the DB cluster to the latest restorable backup time. By default, the DB cluster is not restored to the latest restorable backup time. Valid for: Aurora DB clusters and Multi-AZ DB clusters
        :param vpc_security_group_ids: A list of EC2 VPC security groups to associate with this DB cluster. If you plan to update the resource, don't specify VPC security groups in a shared VPC. Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_dBCluster_mixin_props = rds_mixins.CfnDBClusterMixinProps(
                allocated_storage=123,
                associated_roles=[rds_mixins.CfnDBClusterPropsMixin.DBClusterRoleProperty(
                    feature_name="featureName",
                    role_arn="roleArn"
                )],
                auto_minor_version_upgrade=False,
                availability_zones=["availabilityZones"],
                backtrack_window=123,
                backup_retention_period=123,
                cluster_scalability_type="clusterScalabilityType",
                copy_tags_to_snapshot=False,
                database_insights_mode="databaseInsightsMode",
                database_name="databaseName",
                db_cluster_identifier="dbClusterIdentifier",
                db_cluster_instance_class="dbClusterInstanceClass",
                db_cluster_parameter_group_name="dbClusterParameterGroupName",
                db_instance_parameter_group_name="dbInstanceParameterGroupName",
                db_subnet_group_name="dbSubnetGroupName",
                db_system_id="dbSystemId",
                delete_automated_backups=False,
                deletion_protection=False,
                domain="domain",
                domain_iam_role_name="domainIamRoleName",
                enable_cloudwatch_logs_exports=["enableCloudwatchLogsExports"],
                enable_global_write_forwarding=False,
                enable_http_endpoint=False,
                enable_iam_database_authentication=False,
                enable_local_write_forwarding=False,
                engine="engine",
                engine_lifecycle_support="engineLifecycleSupport",
                engine_mode="engineMode",
                engine_version="engineVersion",
                global_cluster_identifier="globalClusterIdentifier",
                iops=123,
                kms_key_id="kmsKeyId",
                manage_master_user_password=False,
                master_user_authentication_type="masterUserAuthenticationType",
                master_username="masterUsername",
                master_user_password="masterUserPassword",
                master_user_secret=rds_mixins.CfnDBClusterPropsMixin.MasterUserSecretProperty(
                    kms_key_id="kmsKeyId",
                    secret_arn="secretArn"
                ),
                monitoring_interval=123,
                monitoring_role_arn="monitoringRoleArn",
                network_type="networkType",
                performance_insights_enabled=False,
                performance_insights_kms_key_id="performanceInsightsKmsKeyId",
                performance_insights_retention_period=123,
                port=123,
                preferred_backup_window="preferredBackupWindow",
                preferred_maintenance_window="preferredMaintenanceWindow",
                publicly_accessible=False,
                replication_source_identifier="replicationSourceIdentifier",
                restore_to_time="restoreToTime",
                restore_type="restoreType",
                scaling_configuration=rds_mixins.CfnDBClusterPropsMixin.ScalingConfigurationProperty(
                    auto_pause=False,
                    max_capacity=123,
                    min_capacity=123,
                    seconds_before_timeout=123,
                    seconds_until_auto_pause=123,
                    timeout_action="timeoutAction"
                ),
                serverless_v2_scaling_configuration=rds_mixins.CfnDBClusterPropsMixin.ServerlessV2ScalingConfigurationProperty(
                    max_capacity=123,
                    min_capacity=123,
                    seconds_until_auto_pause=123
                ),
                snapshot_identifier="snapshotIdentifier",
                source_db_cluster_identifier="sourceDbClusterIdentifier",
                source_db_cluster_resource_id="sourceDbClusterResourceId",
                source_region="sourceRegion",
                storage_encrypted=False,
                storage_type="storageType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                use_latest_restorable_time=False,
                vpc_security_group_ids=["vpcSecurityGroupIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43eff098b77d78d495a02edad613bba9e83d951ea3a6fdabca7197611100a1b)
            check_type(argname="argument allocated_storage", value=allocated_storage, expected_type=type_hints["allocated_storage"])
            check_type(argname="argument associated_roles", value=associated_roles, expected_type=type_hints["associated_roles"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument backtrack_window", value=backtrack_window, expected_type=type_hints["backtrack_window"])
            check_type(argname="argument backup_retention_period", value=backup_retention_period, expected_type=type_hints["backup_retention_period"])
            check_type(argname="argument cluster_scalability_type", value=cluster_scalability_type, expected_type=type_hints["cluster_scalability_type"])
            check_type(argname="argument copy_tags_to_snapshot", value=copy_tags_to_snapshot, expected_type=type_hints["copy_tags_to_snapshot"])
            check_type(argname="argument database_insights_mode", value=database_insights_mode, expected_type=type_hints["database_insights_mode"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument db_cluster_identifier", value=db_cluster_identifier, expected_type=type_hints["db_cluster_identifier"])
            check_type(argname="argument db_cluster_instance_class", value=db_cluster_instance_class, expected_type=type_hints["db_cluster_instance_class"])
            check_type(argname="argument db_cluster_parameter_group_name", value=db_cluster_parameter_group_name, expected_type=type_hints["db_cluster_parameter_group_name"])
            check_type(argname="argument db_instance_parameter_group_name", value=db_instance_parameter_group_name, expected_type=type_hints["db_instance_parameter_group_name"])
            check_type(argname="argument db_subnet_group_name", value=db_subnet_group_name, expected_type=type_hints["db_subnet_group_name"])
            check_type(argname="argument db_system_id", value=db_system_id, expected_type=type_hints["db_system_id"])
            check_type(argname="argument delete_automated_backups", value=delete_automated_backups, expected_type=type_hints["delete_automated_backups"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument domain_iam_role_name", value=domain_iam_role_name, expected_type=type_hints["domain_iam_role_name"])
            check_type(argname="argument enable_cloudwatch_logs_exports", value=enable_cloudwatch_logs_exports, expected_type=type_hints["enable_cloudwatch_logs_exports"])
            check_type(argname="argument enable_global_write_forwarding", value=enable_global_write_forwarding, expected_type=type_hints["enable_global_write_forwarding"])
            check_type(argname="argument enable_http_endpoint", value=enable_http_endpoint, expected_type=type_hints["enable_http_endpoint"])
            check_type(argname="argument enable_iam_database_authentication", value=enable_iam_database_authentication, expected_type=type_hints["enable_iam_database_authentication"])
            check_type(argname="argument enable_local_write_forwarding", value=enable_local_write_forwarding, expected_type=type_hints["enable_local_write_forwarding"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_lifecycle_support", value=engine_lifecycle_support, expected_type=type_hints["engine_lifecycle_support"])
            check_type(argname="argument engine_mode", value=engine_mode, expected_type=type_hints["engine_mode"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument global_cluster_identifier", value=global_cluster_identifier, expected_type=type_hints["global_cluster_identifier"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument manage_master_user_password", value=manage_master_user_password, expected_type=type_hints["manage_master_user_password"])
            check_type(argname="argument master_user_authentication_type", value=master_user_authentication_type, expected_type=type_hints["master_user_authentication_type"])
            check_type(argname="argument master_username", value=master_username, expected_type=type_hints["master_username"])
            check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
            check_type(argname="argument master_user_secret", value=master_user_secret, expected_type=type_hints["master_user_secret"])
            check_type(argname="argument monitoring_interval", value=monitoring_interval, expected_type=type_hints["monitoring_interval"])
            check_type(argname="argument monitoring_role_arn", value=monitoring_role_arn, expected_type=type_hints["monitoring_role_arn"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument performance_insights_enabled", value=performance_insights_enabled, expected_type=type_hints["performance_insights_enabled"])
            check_type(argname="argument performance_insights_kms_key_id", value=performance_insights_kms_key_id, expected_type=type_hints["performance_insights_kms_key_id"])
            check_type(argname="argument performance_insights_retention_period", value=performance_insights_retention_period, expected_type=type_hints["performance_insights_retention_period"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_backup_window", value=preferred_backup_window, expected_type=type_hints["preferred_backup_window"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument replication_source_identifier", value=replication_source_identifier, expected_type=type_hints["replication_source_identifier"])
            check_type(argname="argument restore_to_time", value=restore_to_time, expected_type=type_hints["restore_to_time"])
            check_type(argname="argument restore_type", value=restore_type, expected_type=type_hints["restore_type"])
            check_type(argname="argument scaling_configuration", value=scaling_configuration, expected_type=type_hints["scaling_configuration"])
            check_type(argname="argument serverless_v2_scaling_configuration", value=serverless_v2_scaling_configuration, expected_type=type_hints["serverless_v2_scaling_configuration"])
            check_type(argname="argument snapshot_identifier", value=snapshot_identifier, expected_type=type_hints["snapshot_identifier"])
            check_type(argname="argument source_db_cluster_identifier", value=source_db_cluster_identifier, expected_type=type_hints["source_db_cluster_identifier"])
            check_type(argname="argument source_db_cluster_resource_id", value=source_db_cluster_resource_id, expected_type=type_hints["source_db_cluster_resource_id"])
            check_type(argname="argument source_region", value=source_region, expected_type=type_hints["source_region"])
            check_type(argname="argument storage_encrypted", value=storage_encrypted, expected_type=type_hints["storage_encrypted"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument use_latest_restorable_time", value=use_latest_restorable_time, expected_type=type_hints["use_latest_restorable_time"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if associated_roles is not None:
            self._values["associated_roles"] = associated_roles
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if backtrack_window is not None:
            self._values["backtrack_window"] = backtrack_window
        if backup_retention_period is not None:
            self._values["backup_retention_period"] = backup_retention_period
        if cluster_scalability_type is not None:
            self._values["cluster_scalability_type"] = cluster_scalability_type
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if database_insights_mode is not None:
            self._values["database_insights_mode"] = database_insights_mode
        if database_name is not None:
            self._values["database_name"] = database_name
        if db_cluster_identifier is not None:
            self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_cluster_instance_class is not None:
            self._values["db_cluster_instance_class"] = db_cluster_instance_class
        if db_cluster_parameter_group_name is not None:
            self._values["db_cluster_parameter_group_name"] = db_cluster_parameter_group_name
        if db_instance_parameter_group_name is not None:
            self._values["db_instance_parameter_group_name"] = db_instance_parameter_group_name
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if db_system_id is not None:
            self._values["db_system_id"] = db_system_id
        if delete_automated_backups is not None:
            self._values["delete_automated_backups"] = delete_automated_backups
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if domain is not None:
            self._values["domain"] = domain
        if domain_iam_role_name is not None:
            self._values["domain_iam_role_name"] = domain_iam_role_name
        if enable_cloudwatch_logs_exports is not None:
            self._values["enable_cloudwatch_logs_exports"] = enable_cloudwatch_logs_exports
        if enable_global_write_forwarding is not None:
            self._values["enable_global_write_forwarding"] = enable_global_write_forwarding
        if enable_http_endpoint is not None:
            self._values["enable_http_endpoint"] = enable_http_endpoint
        if enable_iam_database_authentication is not None:
            self._values["enable_iam_database_authentication"] = enable_iam_database_authentication
        if enable_local_write_forwarding is not None:
            self._values["enable_local_write_forwarding"] = enable_local_write_forwarding
        if engine is not None:
            self._values["engine"] = engine
        if engine_lifecycle_support is not None:
            self._values["engine_lifecycle_support"] = engine_lifecycle_support
        if engine_mode is not None:
            self._values["engine_mode"] = engine_mode
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if global_cluster_identifier is not None:
            self._values["global_cluster_identifier"] = global_cluster_identifier
        if iops is not None:
            self._values["iops"] = iops
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if manage_master_user_password is not None:
            self._values["manage_master_user_password"] = manage_master_user_password
        if master_user_authentication_type is not None:
            self._values["master_user_authentication_type"] = master_user_authentication_type
        if master_username is not None:
            self._values["master_username"] = master_username
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password
        if master_user_secret is not None:
            self._values["master_user_secret"] = master_user_secret
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role_arn is not None:
            self._values["monitoring_role_arn"] = monitoring_role_arn
        if network_type is not None:
            self._values["network_type"] = network_type
        if performance_insights_enabled is not None:
            self._values["performance_insights_enabled"] = performance_insights_enabled
        if performance_insights_kms_key_id is not None:
            self._values["performance_insights_kms_key_id"] = performance_insights_kms_key_id
        if performance_insights_retention_period is not None:
            self._values["performance_insights_retention_period"] = performance_insights_retention_period
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if replication_source_identifier is not None:
            self._values["replication_source_identifier"] = replication_source_identifier
        if restore_to_time is not None:
            self._values["restore_to_time"] = restore_to_time
        if restore_type is not None:
            self._values["restore_type"] = restore_type
        if scaling_configuration is not None:
            self._values["scaling_configuration"] = scaling_configuration
        if serverless_v2_scaling_configuration is not None:
            self._values["serverless_v2_scaling_configuration"] = serverless_v2_scaling_configuration
        if snapshot_identifier is not None:
            self._values["snapshot_identifier"] = snapshot_identifier
        if source_db_cluster_identifier is not None:
            self._values["source_db_cluster_identifier"] = source_db_cluster_identifier
        if source_db_cluster_resource_id is not None:
            self._values["source_db_cluster_resource_id"] = source_db_cluster_resource_id
        if source_region is not None:
            self._values["source_region"] = source_region
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if tags is not None:
            self._values["tags"] = tags
        if use_latest_restorable_time is not None:
            self._values["use_latest_restorable_time"] = use_latest_restorable_time
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        '''The amount of storage in gibibytes (GiB) to allocate to each DB instance in the Multi-AZ DB cluster.

        Valid for Cluster Type: Multi-AZ DB clusters only

        This setting is required to create a Multi-AZ DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-allocatedstorage
        '''
        result = self._values.get("allocated_storage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def associated_roles(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBClusterPropsMixin.DBClusterRoleProperty"]]]]:
        '''Provides a list of the AWS Identity and Access Management (IAM) roles that are associated with the DB cluster.

        IAM roles that are associated with a DB cluster grant permission for the DB cluster to access other Amazon Web Services on your behalf.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-associatedroles
        '''
        result = self._values.get("associated_roles")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBClusterPropsMixin.DBClusterRoleProperty"]]]], result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether minor engine upgrades are applied automatically to the DB cluster during the maintenance window.

        By default, minor engine upgrades are applied automatically.

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB cluster.

        For more information about automatic minor version upgrades, see `Automatically upgrading the minor engine version <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Upgrading.html#USER_UpgradeDBInstance.Upgrading.AutoMinorVersionUpgrades>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Availability Zones (AZs) where instances in the DB cluster can be created.

        For information on AWS Regions and Availability Zones, see `Choosing the Regions and Availability Zones <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.RegionsAndAvailabilityZones.html>`_ in the *Amazon Aurora User Guide* .

        Valid for: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-availabilityzones
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def backtrack_window(self) -> typing.Optional[jsii.Number]:
        '''The target backtrack window, in seconds. To disable backtracking, set this value to ``0`` .

        Valid for Cluster Type: Aurora MySQL DB clusters only

        Default: ``0``

        Constraints:

        - If specified, this value must be set to a number from 0 to 259,200 (72 hours).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-backtrackwindow
        '''
        result = self._values.get("backtrack_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which automated backups are retained.

        Default: 1

        Constraints:

        - Must be a value from 1 to 35

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :default: - 1

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-backupretentionperiod
        '''
        result = self._values.get("backup_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cluster_scalability_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the scalability mode of the Aurora DB cluster.

        When set to ``limitless`` , the cluster operates as an Aurora Limitless Database, allowing you to create a DB shard group for horizontal scaling (sharding) capabilities. When set to ``standard`` (the default), the cluster uses normal DB instance creation.

        *Important:* Automated backup retention isn't supported with Aurora Limitless Database clusters. If you set this property to ``limitless`` , you cannot set ``DeleteAutomatedBackups`` to ``false`` . To create a backup, use manual snapshots instead.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-clusterscalabilitytype
        '''
        result = self._values.get("cluster_scalability_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_tags_to_snapshot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether to copy all tags from the DB cluster to snapshots of the DB cluster.

        The default is not to copy them.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-copytagstosnapshot
        '''
        result = self._values.get("copy_tags_to_snapshot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def database_insights_mode(self) -> typing.Optional[builtins.str]:
        '''The mode of Database Insights to enable for the DB cluster.

        If you set this value to ``advanced`` , you must also set the ``PerformanceInsightsEnabled`` parameter to ``true`` and the ``PerformanceInsightsRetentionPeriod`` parameter to 465.

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-databaseinsightsmode
        '''
        result = self._values.get("database_insights_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of your database.

        If you don't provide a name, then Amazon RDS won't create a database in this DB cluster. For naming constraints, see `Naming Constraints <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_Limits.html#RDS_Limits.Constraints>`_ in the *Amazon Aurora User Guide* .

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The DB cluster identifier. This parameter is stored as a lowercase string.

        Constraints:

        - Must contain from 1 to 63 letters, numbers, or hyphens.
        - First character must be a letter.
        - Can't end with a hyphen or contain two consecutive hyphens.

        Example: ``my-cluster1``

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbclusteridentifier
        '''
        result = self._values.get("db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_cluster_instance_class(self) -> typing.Optional[builtins.str]:
        '''The compute and memory capacity of each DB instance in the Multi-AZ DB cluster, for example ``db.m6gd.xlarge`` . Not all DB instance classes are available in all AWS Regions , or for all database engines.

        For the full list of DB instance classes and availability for your engine, see `DB instance class <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html>`_ in the *Amazon RDS User Guide* .

        This setting is required to create a Multi-AZ DB cluster.

        Valid for Cluster Type: Multi-AZ DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbclusterinstanceclass
        '''
        result = self._values.get("db_cluster_instance_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the DB cluster parameter group to associate with this DB cluster.

        .. epigraph::

           If you apply a parameter group to an existing DB cluster, then its DB instances might need to reboot. This can result in an outage while the DB instances are rebooting.

           If you apply a change to parameter group associated with a stopped DB cluster, then the update stack waits until the DB cluster is started.

        To list all of the available DB cluster parameter group names, use the following command:

        ``aws rds describe-db-cluster-parameter-groups --query "DBClusterParameterGroups[].DBClusterParameterGroupName" --output text``

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbclusterparametergroupname
        '''
        result = self._values.get("db_cluster_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_instance_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the DB parameter group to apply to all instances of the DB cluster.

        .. epigraph::

           When you apply a parameter group using the ``DBInstanceParameterGroupName`` parameter, the DB cluster isn't rebooted automatically. Also, parameter changes are applied immediately rather than during the next maintenance window.

        Valid for Cluster Type: Aurora DB clusters only

        Default: The existing name setting

        Constraints:

        - The DB parameter group must be in the same DB parameter group family as this DB cluster.
        - The ``DBInstanceParameterGroupName`` parameter is valid in combination with the ``AllowMajorVersionUpgrade`` parameter for a major version upgrade only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbinstanceparametergroupname
        '''
        result = self._values.get("db_instance_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''A DB subnet group that you want to associate with this DB cluster.

        If you are restoring a DB cluster to a point in time with ``RestoreType`` set to ``copy-on-write`` , and don't specify a DB subnet group name, then the DB cluster is restored with a default DB subnet group.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbsubnetgroupname
        '''
        result = self._values.get("db_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_system_id(self) -> typing.Optional[builtins.str]:
        '''Reserved for future use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbsystemid
        '''
        result = self._values.get("db_system_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_automated_backups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to remove automated backups immediately after the DB cluster is deleted.

        This parameter isn't case-sensitive. The default is to remove automated backups immediately after the DB cluster is deleted, unless the AWS Backup policy specifies a point-in-time restore rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-deleteautomatedbackups
        '''
        result = self._values.get("delete_automated_backups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether the DB cluster has deletion protection enabled.

        The database can't be deleted when deletion protection is enabled. By default, deletion protection is disabled.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Indicates the directory ID of the Active Directory to create the DB cluster.

        For Amazon Aurora DB clusters, Amazon RDS can use Kerberos authentication to authenticate users that connect to the DB cluster.

        For more information, see `Kerberos authentication <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/kerberos-authentication.html>`_ in the *Amazon Aurora User Guide* .

        Valid for: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_iam_role_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the IAM role to use when making API calls to the Directory Service.

        Valid for: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-domainiamrolename
        '''
        result = self._values.get("domain_iam_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_cloudwatch_logs_exports(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of log types that need to be enabled for exporting to CloudWatch Logs.

        The values in the list depend on the DB engine being used. For more information, see `Publishing Database Logs to Amazon CloudWatch Logs <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_LogAccess.html#USER_LogAccess.Procedural.UploadtoCloudWatch>`_ in the *Amazon Aurora User Guide* .

        *Aurora MySQL*

        Valid values: ``audit`` , ``error`` , ``general`` , ``slowquery``

        *Aurora PostgreSQL*

        Valid values: ``postgresql``

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enablecloudwatchlogsexports
        '''
        result = self._values.get("enable_cloudwatch_logs_exports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_global_write_forwarding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable this DB cluster to forward write operations to the primary cluster of a global cluster (Aurora global database).

        By default, write operations are not allowed on Aurora DB clusters that are secondary clusters in an Aurora global database.

        You can set this value only on Aurora DB clusters that are members of an Aurora global database. With this parameter enabled, a secondary cluster can forward writes to the current primary cluster, and the resulting changes are replicated back to this cluster. For the primary DB cluster of an Aurora global database, this value is used immediately if the primary is demoted by a global cluster API operation, but it does nothing until then.

        Valid for Cluster Type: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enableglobalwriteforwarding
        '''
        result = self._values.get("enable_global_write_forwarding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def enable_http_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable the HTTP endpoint for the DB cluster. By default, the HTTP endpoint isn't enabled.

        When enabled, the HTTP endpoint provides a connectionless web service API (RDS Data API) for running SQL queries on the DB cluster. You can also query your database from inside the RDS console with the RDS query editor.

        For more information, see `Using RDS Data API <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/data-api.html>`_ in the *Amazon Aurora User Guide* .

        Valid for Cluster Type: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enablehttpendpoint
        '''
        result = self._values.get("enable_http_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def enable_iam_database_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts.

        By default, mapping is disabled.

        For more information, see `IAM Database Authentication <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.IAMDBAuth.html>`_ in the *Amazon Aurora User Guide.*

        Valid for: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enableiamdatabaseauthentication
        '''
        result = self._values.get("enable_iam_database_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def enable_local_write_forwarding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether read replicas can forward write operations to the writer DB instance in the DB cluster.

        By default, write operations aren't allowed on reader DB instances.

        Valid for: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enablelocalwriteforwarding
        '''
        result = self._values.get("enable_local_write_forwarding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The name of the database engine to be used for this DB cluster.

        Valid Values:

        - ``aurora-mysql``
        - ``aurora-postgresql``
        - ``mysql``
        - ``postgres``

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_lifecycle_support(self) -> typing.Optional[builtins.str]:
        '''The life cycle type for this DB cluster.

        .. epigraph::

           By default, this value is set to ``open-source-rds-extended-support`` , which enrolls your DB cluster into Amazon RDS Extended Support. At the end of standard support, you can avoid charges for Extended Support by setting the value to ``open-source-rds-extended-support-disabled`` . In this case, creating the DB cluster will fail if the DB major version is past its end of standard support date.

        You can use this setting to enroll your DB cluster into Amazon RDS Extended Support. With RDS Extended Support, you can run the selected major engine version on your DB cluster past the end of standard support for that engine version. For more information, see the following sections:

        - Amazon Aurora - `Amazon RDS Extended Support with Amazon Aurora <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/extended-support.html>`_ in the *Amazon Aurora User Guide*
        - Amazon RDS - `Amazon RDS Extended Support with Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support.html>`_ in the *Amazon RDS User Guide*

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        Valid Values: ``open-source-rds-extended-support | open-source-rds-extended-support-disabled``

        Default: ``open-source-rds-extended-support``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enginelifecyclesupport
        '''
        result = self._values.get("engine_lifecycle_support")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_mode(self) -> typing.Optional[builtins.str]:
        '''The DB engine mode of the DB cluster, either ``provisioned`` or ``serverless`` .

        The ``serverless`` engine mode only applies for Aurora Serverless v1 DB clusters. Aurora Serverless v2 DB clusters use the ``provisioned`` engine mode.

        For information about limitations and requirements for Serverless DB clusters, see the following sections in the *Amazon Aurora User Guide* :

        - `Limitations of Aurora Serverless v1 <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.html#aurora-serverless.limitations>`_
        - `Requirements for Aurora Serverless v2 <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.requirements.html>`_

        Valid for Cluster Type: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enginemode
        '''
        result = self._values.get("engine_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the database engine to use.

        To list all of the available engine versions for Aurora MySQL version 2 (5.7-compatible) and version 3 (8.0-compatible), use the following command:

        ``aws rds describe-db-engine-versions --engine aurora-mysql --query "DBEngineVersions[].EngineVersion"``

        You can supply either ``5.7`` or ``8.0`` to use the default engine version for Aurora MySQL version 2 or version 3, respectively.

        To list all of the available engine versions for Aurora PostgreSQL, use the following command:

        ``aws rds describe-db-engine-versions --engine aurora-postgresql --query "DBEngineVersions[].EngineVersion"``

        To list all of the available engine versions for RDS for MySQL, use the following command:

        ``aws rds describe-db-engine-versions --engine mysql --query "DBEngineVersions[].EngineVersion"``

        To list all of the available engine versions for RDS for PostgreSQL, use the following command:

        ``aws rds describe-db-engine-versions --engine postgres --query "DBEngineVersions[].EngineVersion"``

        *Aurora MySQL*

        For information, see `Database engine updates for Amazon Aurora MySQL <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Updates.html>`_ in the *Amazon Aurora User Guide* .

        *Aurora PostgreSQL*

        For information, see `Amazon Aurora PostgreSQL releases and engine versions <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Updates.20180305.html>`_ in the *Amazon Aurora User Guide* .

        *MySQL*

        For information, see `Amazon RDS for MySQL <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html#MySQL.Concepts.VersionMgmt>`_ in the *Amazon RDS User Guide* .

        *PostgreSQL*

        For information, see `Amazon RDS for PostgreSQL <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts>`_ in the *Amazon RDS User Guide* .

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''If you are configuring an Aurora global database cluster and want your Aurora DB cluster to be a secondary member in the global database cluster, specify the global cluster ID of the global database cluster.

        To define the primary database cluster of the global cluster, use the `AWS::RDS::GlobalCluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html>`_ resource.

        If you aren't configuring a global database cluster, don't specify this property.
        .. epigraph::

           To remove the DB cluster from a global database cluster, specify an empty value for the ``GlobalClusterIdentifier`` property.

        For information about Aurora global databases, see `Working with Amazon Aurora Global Databases <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html>`_ in the *Amazon Aurora User Guide* .

        Valid for: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-globalclusteridentifier
        '''
        result = self._values.get("global_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''The amount of Provisioned IOPS (input/output operations per second) to be initially allocated for each DB instance in the Multi-AZ DB cluster.

        For information about valid IOPS values, see `Provisioned IOPS storage <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html#USER_PIOPS>`_ in the *Amazon RDS User Guide* .

        This setting is required to create a Multi-AZ DB cluster.

        Valid for Cluster Type: Multi-AZ DB clusters only

        Constraints:

        - Must be a multiple between .5 and 50 of the storage amount for the DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-iops
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS KMS key that is used to encrypt the database instances in the DB cluster, such as ``arn:aws:kms:us-east-1:012345678910:key/abcd1234-a123-456a-a12b-a123b4cd56ef`` .

        If you enable the ``StorageEncrypted`` property but don't specify this property, the default KMS key is used. If you specify this property, you must set the ``StorageEncrypted`` property to ``true`` .

        If you specify the ``SnapshotIdentifier`` property, the ``StorageEncrypted`` property value is inherited from the snapshot, and if the DB cluster is encrypted, the specified ``KmsKeyId`` property is used.

        If you create a read replica of an encrypted DB cluster in another AWS Region, make sure to set ``KmsKeyId`` to a KMS key identifier that is valid in the destination AWS Region. This KMS key is used to encrypt the read replica in that AWS Region.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manage_master_user_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to manage the master user password with AWS Secrets Manager.

        For more information, see `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html>`_ in the *Amazon RDS User Guide* and `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-secrets-manager.html>`_ in the *Amazon Aurora User Guide.*

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        Constraints:

        - Can't manage the master user password with AWS Secrets Manager if ``MasterUserPassword`` is specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-managemasteruserpassword
        '''
        result = self._values.get("manage_master_user_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def master_user_authentication_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the authentication type for the master user.

        With IAM master user authentication, you can configure the master DB user with IAM database authentication when you create a DB cluster.

        You can specify one of the following values:

        - ``password`` - Use standard database authentication with a password.
        - ``iam-db-auth`` - Use IAM database authentication for the master user.

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        This option is only valid for RDS for MySQL, RDS for MariaDB, RDS for PostgreSQL, Aurora MySQL, and Aurora PostgreSQL engines.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masteruserauthenticationtype
        '''
        result = self._values.get("master_user_authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_username(self) -> typing.Optional[builtins.str]:
        '''The name of the master user for the DB cluster.

        .. epigraph::

           If you specify the ``SourceDBClusterIdentifier`` , ``SnapshotIdentifier`` , or ``GlobalClusterIdentifier`` property, don't specify this property. The value is inherited from the source DB cluster, the snapshot, or the primary DB cluster for the global database cluster, respectively.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masterusername
        '''
        result = self._values.get("master_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_password(self) -> typing.Optional[builtins.str]:
        '''The master password for the DB instance.

        .. epigraph::

           If you specify the ``SourceDBClusterIdentifier`` , ``SnapshotIdentifier`` , or ``GlobalClusterIdentifier`` property, don't specify this property. The value is inherited from the source DB cluster, the snapshot, or the primary DB cluster for the global database cluster, respectively.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masteruserpassword
        '''
        result = self._values.get("master_user_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_secret(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBClusterPropsMixin.MasterUserSecretProperty"]]:
        '''The secret managed by RDS in AWS Secrets Manager for the master user password.

        .. epigraph::

           When you restore a DB cluster from a snapshot, Amazon RDS generates a new secret instead of reusing the secret specified in the ``SecretArn`` property. This ensures that the restored DB cluster is securely managed with a dedicated secret. To maintain consistent integration with your application, you might need to update resource configurations to reference the newly created secret.

        For more information, see `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html>`_ in the *Amazon RDS User Guide* and `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-secrets-manager.html>`_ in the *Amazon Aurora User Guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masterusersecret
        '''
        result = self._values.get("master_user_secret")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBClusterPropsMixin.MasterUserSecretProperty"]], result)

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[jsii.Number]:
        '''The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB cluster.

        To turn off collecting Enhanced Monitoring metrics, specify ``0`` .

        If ``MonitoringRoleArn`` is specified, also set ``MonitoringInterval`` to a value other than ``0`` .

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        Valid Values: ``0 | 1 | 5 | 10 | 15 | 30 | 60``

        Default: ``0``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-monitoringinterval
        '''
        result = self._values.get("monitoring_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitoring_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the IAM role that permits RDS to send Enhanced Monitoring metrics to Amazon CloudWatch Logs.

        An example is ``arn:aws:iam:123456789012:role/emaccess`` . For information on creating a monitoring role, see `Setting up and enabling Enhanced Monitoring <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html#USER_Monitoring.OS.Enabling>`_ in the *Amazon RDS User Guide* .

        If ``MonitoringInterval`` is set to a value other than ``0`` , supply a ``MonitoringRoleArn`` value.

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-monitoringrolearn
        '''
        result = self._values.get("monitoring_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''The network type of the DB cluster.

        Valid values:

        - ``IPV4``
        - ``DUAL``

        The network type is determined by the ``DBSubnetGroup`` specified for the DB cluster. A ``DBSubnetGroup`` can support only the IPv4 protocol or the IPv4 and IPv6 protocols ( ``DUAL`` ).

        For more information, see `Working with a DB instance in a VPC <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html>`_ in the *Amazon Aurora User Guide.*

        Valid for: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def performance_insights_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to turn on Performance Insights for the DB cluster.

        For more information, see `Using Amazon Performance Insights <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html>`_ in the *Amazon RDS User Guide* .

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-performanceinsightsenabled
        '''
        result = self._values.get("performance_insights_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def performance_insights_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS KMS key identifier for encryption of Performance Insights data.

        The AWS KMS key identifier is the key ARN, key ID, alias ARN, or alias name for the KMS key.

        If you don't specify a value for ``PerformanceInsightsKMSKeyId`` , then Amazon RDS uses your default KMS key. There is a default KMS key for your AWS account . Your AWS account has a different default KMS key for each AWS Region .

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-performanceinsightskmskeyid
        '''
        result = self._values.get("performance_insights_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def performance_insights_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain Performance Insights data.

        When creating a DB cluster without enabling Performance Insights, you can't specify the parameter ``PerformanceInsightsRetentionPeriod`` .

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        Valid Values:

        - ``7``
        - *month* * 31, where *month* is a number of months from 1-23. Examples: ``93`` (3 months * 31), ``341`` (11 months * 31), ``589`` (19 months * 31)
        - ``731``

        Default: ``7`` days

        If you specify a retention period that isn't valid, such as ``94`` , Amazon RDS issues an error.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-performanceinsightsretentionperiod
        '''
        result = self._values.get("performance_insights_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number on which the DB instances in the DB cluster accept connections.

        Default:

        - When ``EngineMode`` is ``provisioned`` , ``3306`` (for both Aurora MySQL and Aurora PostgreSQL)
        - When ``EngineMode`` is ``serverless`` :
        - ``3306`` when ``Engine`` is ``aurora`` or ``aurora-mysql``
        - ``5432`` when ``Engine`` is ``aurora-postgresql``

        .. epigraph::

           The ``No interruption`` on update behavior only applies to DB clusters. If you are updating a DB instance, see `Port <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-port>`_ for the AWS::RDS::DBInstance resource.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range during which automated backups are created.

        For more information, see `Backup Window <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html#Aurora.Managing.Backups.BackupWindow>`_ in the *Amazon Aurora User Guide.*

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi`` .
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-preferredbackupwindow
        '''
        result = self._values.get("preferred_backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC).

        Format: ``ddd:hh24:mi-ddd:hh24:mi``

        The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see `Maintaining an Amazon Aurora DB cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#AdjustingTheMaintenanceWindow.Aurora>`_ in the *Amazon Aurora User Guide.*

        Valid Days: Mon, Tue, Wed, Thu, Fri, Sat, Sun.

        Constraints: Minimum 30-minute window.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the DB cluster is publicly accessible.

        Valid for Cluster Type: Multi-AZ DB clusters only

        When the DB cluster is publicly accessible and you connect from outside of the DB cluster's virtual private cloud (VPC), its domain name system (DNS) endpoint resolves to the public IP address. When you connect from within the same VPC as the DB cluster, the endpoint resolves to the private IP address. Access to the DB cluster is controlled by its security group settings.

        When the DB cluster isn't publicly accessible, it is an internal DB cluster with a DNS name that resolves to a private IP address.

        The default behavior when ``PubliclyAccessible`` is not specified depends on whether a ``DBSubnetGroup`` is specified.

        If ``DBSubnetGroup`` isn't specified, ``PubliclyAccessible`` defaults to ``true`` .

        If ``DBSubnetGroup`` is specified, ``PubliclyAccessible`` defaults to ``false`` unless the value of ``DBSubnetGroup`` is ``default`` , in which case ``PubliclyAccessible`` defaults to ``true`` .

        If ``PubliclyAccessible`` is true and the VPC that the ``DBSubnetGroup`` is in doesn't have an internet gateway attached to it, Amazon RDS returns an error.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def replication_source_identifier(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the source DB instance or DB cluster if this DB cluster is created as a read replica.

        Valid for: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-replicationsourceidentifier
        '''
        result = self._values.get("replication_source_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_to_time(self) -> typing.Optional[builtins.str]:
        '''The date and time to restore the DB cluster to.

        Valid Values: Value must be a time in Universal Coordinated Time (UTC) format

        Constraints:

        - Must be before the latest restorable time for the DB instance
        - Must be specified if ``UseLatestRestorableTime`` parameter isn't provided
        - Can't be specified if the ``UseLatestRestorableTime`` parameter is enabled
        - Can't be specified if the ``RestoreType`` parameter is ``copy-on-write``

        This property must be used with ``SourceDBClusterIdentifier`` property. The resulting cluster will have the identifier that matches the value of the ``DBclusterIdentifier`` property.

        Example: ``2015-03-07T23:45:00Z``

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-restoretotime
        '''
        result = self._values.get("restore_to_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_type(self) -> typing.Optional[builtins.str]:
        '''The type of restore to be performed. You can specify one of the following values:.

        - ``full-copy`` - The new DB cluster is restored as a full copy of the source DB cluster.
        - ``copy-on-write`` - The new DB cluster is restored as a clone of the source DB cluster.

        If you don't specify a ``RestoreType`` value, then the new DB cluster is restored as a full copy of the source DB cluster.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-restoretype
        '''
        result = self._values.get("restore_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBClusterPropsMixin.ScalingConfigurationProperty"]]:
        '''The scaling configuration of an Aurora Serverless v1 DB cluster.

        This property is only supported for Aurora Serverless v1. For Aurora Serverless v2, Use the ``ServerlessV2ScalingConfiguration`` property.

        Valid for: Aurora Serverless v1 DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-scalingconfiguration
        '''
        result = self._values.get("scaling_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBClusterPropsMixin.ScalingConfigurationProperty"]], result)

    @builtins.property
    def serverless_v2_scaling_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBClusterPropsMixin.ServerlessV2ScalingConfigurationProperty"]]:
        '''The scaling configuration of an Aurora Serverless V2 DB cluster.

        This property is only supported for Aurora Serverless v2. For Aurora Serverless v1, Use the ``ScalingConfiguration`` property.

        Valid for: Aurora Serverless v2 DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-serverlessv2scalingconfiguration
        '''
        result = self._values.get("serverless_v2_scaling_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBClusterPropsMixin.ServerlessV2ScalingConfigurationProperty"]], result)

    @builtins.property
    def snapshot_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier for the DB snapshot or DB cluster snapshot to restore from.

        You can use either the name or the Amazon Resource Name (ARN) to specify a DB cluster snapshot. However, you can use only the ARN to specify a DB snapshot.

        After you restore a DB cluster with a ``SnapshotIdentifier`` property, you must specify the same ``SnapshotIdentifier`` property for any future updates to the DB cluster. When you specify this property for an update, the DB cluster is not restored from the snapshot again, and the data in the database is not changed. However, if you don't specify the ``SnapshotIdentifier`` property, an empty DB cluster is created, and the original DB cluster is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB cluster is restored from the specified ``SnapshotIdentifier`` property, and the original DB cluster is deleted.

        If you specify the ``SnapshotIdentifier`` property to restore a DB cluster (as opposed to specifying it for DB cluster updates), then don't specify the following properties:

        - ``GlobalClusterIdentifier``
        - ``MasterUsername``
        - ``MasterUserPassword``
        - ``ReplicationSourceIdentifier``
        - ``RestoreType``
        - ``SourceDBClusterIdentifier``
        - ``SourceRegion``
        - ``StorageEncrypted`` (for an encrypted snapshot)
        - ``UseLatestRestorableTime``

        Constraints:

        - Must match the identifier of an existing Snapshot.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-snapshotidentifier
        '''
        result = self._values.get("snapshot_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''When restoring a DB cluster to a point in time, the identifier of the source DB cluster from which to restore.

        Constraints:

        - Must match the identifier of an existing DBCluster.
        - Cannot be specified if ``SourceDbClusterResourceId`` is specified. You must specify either ``SourceDBClusterIdentifier`` or ``SourceDbClusterResourceId`` , but not both.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-sourcedbclusteridentifier
        '''
        result = self._values.get("source_db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_db_cluster_resource_id(self) -> typing.Optional[builtins.str]:
        '''The resource ID of the source DB cluster from which to restore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-sourcedbclusterresourceid
        '''
        result = self._values.get("source_db_cluster_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_region(self) -> typing.Optional[builtins.str]:
        '''The AWS Region which contains the source DB cluster when replicating a DB cluster. For example, ``us-east-1`` .

        Valid for: Aurora DB clusters only

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-sourceregion
        '''
        result = self._values.get("source_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the DB cluster is encrypted.

        If you specify the ``KmsKeyId`` property, then you must enable encryption.

        If you specify the ``SourceDBClusterIdentifier`` property, don't specify this property. The value is inherited from the source DB cluster, and if the DB cluster is encrypted, the specified ``KmsKeyId`` property is used.

        If you specify the ``SnapshotIdentifier`` and the specified snapshot is encrypted, don't specify this property. The value is inherited from the snapshot, and the specified ``KmsKeyId`` property is used.

        If you specify the ``SnapshotIdentifier`` and the specified snapshot isn't encrypted, you can use this property to specify that the restored DB cluster is encrypted. Specify the ``KmsKeyId`` property for the KMS key to use for encryption. If you don't want the restored DB cluster to be encrypted, then don't set this property or set it to ``false`` .
        .. epigraph::

           If you specify both the ``StorageEncrypted`` and ``SnapshotIdentifier`` properties without specifying the ``KmsKeyId`` property, then the restored DB cluster inherits the encryption settings from the DB snapshot that provide.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-storageencrypted
        '''
        result = self._values.get("storage_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''The storage type to associate with the DB cluster.

        For information on storage types for Aurora DB clusters, see `Storage configurations for Amazon Aurora DB clusters <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html#aurora-storage-type>`_ . For information on storage types for Multi-AZ DB clusters, see `Settings for creating Multi-AZ DB clusters <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/create-multi-az-db-cluster.html#create-multi-az-db-cluster-settings>`_ .

        This setting is required to create a Multi-AZ DB cluster.

        When specified for a Multi-AZ DB cluster, a value for the ``Iops`` parameter is required.

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        Valid Values:

        - Aurora DB clusters - ``aurora | aurora-iopt1``
        - Multi-AZ DB clusters - ``io1 | io2 | gp3``

        Default:

        - Aurora DB clusters - ``aurora``
        - Multi-AZ DB clusters - ``io1``

        .. epigraph::

           When you create an Aurora DB cluster with the storage type set to ``aurora-iopt1`` , the storage type is returned in the response. The storage type isn't returned when you set it to ``aurora`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-storagetype
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the DB cluster.

        Valid for Cluster Type: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def use_latest_restorable_time(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether to restore the DB cluster to the latest restorable backup time.

        By default, the DB cluster is not restored to the latest restorable backup time.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-uselatestrestorabletime
        '''
        result = self._values.get("use_latest_restorable_time")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of EC2 VPC security groups to associate with this DB cluster.

        If you plan to update the resource, don't specify VPC security groups in a shared VPC.

        Valid for: Aurora DB clusters and Multi-AZ DB clusters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBClusterParameterGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_cluster_parameter_group_name": "dbClusterParameterGroupName",
        "description": "description",
        "family": "family",
        "parameters": "parameters",
        "tags": "tags",
    },
)
class CfnDBClusterParameterGroupMixinProps:
    def __init__(
        self,
        *,
        db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        family: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDBClusterParameterGroupPropsMixin.

        :param db_cluster_parameter_group_name: The name of the DB cluster parameter group. Constraints: - Must not match the name of an existing DB cluster parameter group. .. epigraph:: This value is stored as a lowercase string.
        :param description: The description for the DB cluster parameter group.
        :param family: The DB cluster parameter group family name. A DB cluster parameter group can be associated with one and only one DB cluster parameter group family, and can be applied only to a DB cluster running a database engine and engine version compatible with that DB cluster parameter group family. *Aurora MySQL* Example: ``aurora-mysql5.7`` , ``aurora-mysql8.0`` *Aurora PostgreSQL* Example: ``aurora-postgresql14`` *RDS for MySQL* Example: ``mysql8.0`` *RDS for PostgreSQL* Example: ``postgres13`` To list all of the available parameter group families for a DB engine, use the following command: ``aws rds describe-db-engine-versions --query "DBEngineVersions[].DBParameterGroupFamily" --engine <engine>`` For example, to list all of the available parameter group families for the Aurora PostgreSQL DB engine, use the following command: ``aws rds describe-db-engine-versions --query "DBEngineVersions[].DBParameterGroupFamily" --engine aurora-postgresql`` .. epigraph:: The output contains duplicates. The following are the valid DB engine values: - ``aurora-mysql`` - ``aurora-postgresql`` - ``mysql`` - ``postgres``
        :param parameters: Provides a list of parameters for the DB cluster parameter group.
        :param tags: Tags to assign to the DB cluster parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            # parameters: Any
            
            cfn_dBCluster_parameter_group_mixin_props = rds_mixins.CfnDBClusterParameterGroupMixinProps(
                db_cluster_parameter_group_name="dbClusterParameterGroupName",
                description="description",
                family="family",
                parameters=parameters,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeda1b2281cd8734564a372d702be4527700d8e9453c0941cdafaf95c01a1298)
            check_type(argname="argument db_cluster_parameter_group_name", value=db_cluster_parameter_group_name, expected_type=type_hints["db_cluster_parameter_group_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if db_cluster_parameter_group_name is not None:
            self._values["db_cluster_parameter_group_name"] = db_cluster_parameter_group_name
        if description is not None:
            self._values["description"] = description
        if family is not None:
            self._values["family"] = family
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def db_cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the DB cluster parameter group.

        Constraints:

        - Must not match the name of an existing DB cluster parameter group.

        .. epigraph::

           This value is stored as a lowercase string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-dbclusterparametergroupname
        '''
        result = self._values.get("db_cluster_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the DB cluster parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The DB cluster parameter group family name.

        A DB cluster parameter group can be associated with one and only one DB cluster parameter group family, and can be applied only to a DB cluster running a database engine and engine version compatible with that DB cluster parameter group family.

        *Aurora MySQL*

        Example: ``aurora-mysql5.7`` , ``aurora-mysql8.0``

        *Aurora PostgreSQL*

        Example: ``aurora-postgresql14``

        *RDS for MySQL*

        Example: ``mysql8.0``

        *RDS for PostgreSQL*

        Example: ``postgres13``

        To list all of the available parameter group families for a DB engine, use the following command:

        ``aws rds describe-db-engine-versions --query "DBEngineVersions[].DBParameterGroupFamily" --engine <engine>``

        For example, to list all of the available parameter group families for the Aurora PostgreSQL DB engine, use the following command:

        ``aws rds describe-db-engine-versions --query "DBEngineVersions[].DBParameterGroupFamily" --engine aurora-postgresql``
        .. epigraph::

           The output contains duplicates.

        The following are the valid DB engine values:

        - ``aurora-mysql``
        - ``aurora-postgresql``
        - ``mysql``
        - ``postgres``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-family
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''Provides a list of parameters for the DB cluster parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the DB cluster parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBClusterParameterGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDBClusterParameterGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBClusterParameterGroupPropsMixin",
):
    '''The ``AWS::RDS::DBClusterParameterGroup`` resource creates a new Amazon RDS DB cluster parameter group.

    For information about configuring parameters for Amazon Aurora DB clusters, see `Working with parameter groups <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_WorkingWithParamGroups.html>`_ in the *Amazon Aurora User Guide* .
    .. epigraph::

       If you apply a parameter group to a DB cluster, then its DB instances might need to reboot. This can result in an outage while the DB instances are rebooting.

       If you apply a change to parameter group associated with a stopped DB cluster, then the updated stack waits until the DB cluster is started.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html
    :cloudformationResource: AWS::RDS::DBClusterParameterGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        # parameters: Any
        
        cfn_dBCluster_parameter_group_props_mixin = rds_mixins.CfnDBClusterParameterGroupPropsMixin(rds_mixins.CfnDBClusterParameterGroupMixinProps(
            db_cluster_parameter_group_name="dbClusterParameterGroupName",
            description="description",
            family="family",
            parameters=parameters,
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
        props: typing.Union[CfnDBClusterParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBClusterParameterGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209db834d31713852f9cadcf73edf258847750626d5c278851b3be9d47539b37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95839d07f33e9d12c55687d1ad3cd1fe37e540e7b37866f8d807d037189d75fb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ee113678308303e85ee68f8faedbe7715ffbec183c1e4198186640b29e3bfe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBClusterParameterGroupMixinProps:
        return typing.cast(CfnDBClusterParameterGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnDBClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBClusterPropsMixin",
):
    '''The ``AWS::RDS::DBCluster`` resource creates an Amazon Aurora DB cluster or Multi-AZ DB cluster.

    For more information about creating an Aurora DB cluster, see `Creating an Amazon Aurora DB cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.CreateInstance.html>`_ in the *Amazon Aurora User Guide* .

    For more information about creating a Multi-AZ DB cluster, see `Creating a Multi-AZ DB cluster <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/create-multi-az-db-cluster.html>`_ in the *Amazon RDS User Guide* .
    .. epigraph::

       You can only create this resource in AWS Regions where Amazon Aurora or Multi-AZ DB clusters are supported.

    *Updating DB clusters*

    When properties labeled " *Update requires:* `Replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ " are updated, AWS CloudFormation first creates a replacement DB cluster, then changes references from other dependent resources to point to the replacement DB cluster, and finally deletes the old DB cluster.
    .. epigraph::

       We highly recommend that you take a snapshot of the database before updating the stack. If you don't, you lose the data when AWS CloudFormation replaces your DB cluster. To preserve your data, perform the following procedure:

       - Deactivate any applications that are using the DB cluster so that there's no activity on the DB instance.
       - Create a snapshot of the DB cluster. For more information, see `Creating a DB cluster snapshot <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_CreateSnapshotCluster.html>`_ .
       - If you want to restore your DB cluster using a DB cluster snapshot, modify the updated template with your DB cluster changes and add the ``SnapshotIdentifier`` property with the ID of the DB cluster snapshot that you want to use.

       After you restore a DB cluster with a ``SnapshotIdentifier`` property, you must specify the same ``SnapshotIdentifier`` property for any future updates to the DB cluster. When you specify this property for an update, the DB cluster is not restored from the DB cluster snapshot again, and the data in the database is not changed. However, if you don't specify the ``SnapshotIdentifier`` property, an empty DB cluster is created, and the original DB cluster is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB cluster is restored from the specified ``SnapshotIdentifier`` property, and the original DB cluster is deleted.

       - Update the stack.

    Currently, when you are updating the stack for an Aurora Serverless DB cluster, you can't include changes to any other properties when you specify one of the following properties: ``PreferredBackupWindow`` , ``PreferredMaintenanceWindow`` , and ``Port`` . This limitation doesn't apply to provisioned DB clusters.

    For more information about updating other properties of this resource, see ``[ModifyDBCluster](https://docs.aws.amazon.com//AmazonRDS/latest/APIReference/API_ModifyDBCluster.html)`` . For more information about updating stacks, see `AWS CloudFormation Stacks Updates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks.html>`_ .

    *Deleting DB clusters*

    The default ``DeletionPolicy`` for ``AWS::RDS::DBCluster`` resources is ``Snapshot`` . For more information about how AWS CloudFormation deletes resources, see `DeletionPolicy Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html
    :cloudformationResource: AWS::RDS::DBCluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_dBCluster_props_mixin = rds_mixins.CfnDBClusterPropsMixin(rds_mixins.CfnDBClusterMixinProps(
            allocated_storage=123,
            associated_roles=[rds_mixins.CfnDBClusterPropsMixin.DBClusterRoleProperty(
                feature_name="featureName",
                role_arn="roleArn"
            )],
            auto_minor_version_upgrade=False,
            availability_zones=["availabilityZones"],
            backtrack_window=123,
            backup_retention_period=123,
            cluster_scalability_type="clusterScalabilityType",
            copy_tags_to_snapshot=False,
            database_insights_mode="databaseInsightsMode",
            database_name="databaseName",
            db_cluster_identifier="dbClusterIdentifier",
            db_cluster_instance_class="dbClusterInstanceClass",
            db_cluster_parameter_group_name="dbClusterParameterGroupName",
            db_instance_parameter_group_name="dbInstanceParameterGroupName",
            db_subnet_group_name="dbSubnetGroupName",
            db_system_id="dbSystemId",
            delete_automated_backups=False,
            deletion_protection=False,
            domain="domain",
            domain_iam_role_name="domainIamRoleName",
            enable_cloudwatch_logs_exports=["enableCloudwatchLogsExports"],
            enable_global_write_forwarding=False,
            enable_http_endpoint=False,
            enable_iam_database_authentication=False,
            enable_local_write_forwarding=False,
            engine="engine",
            engine_lifecycle_support="engineLifecycleSupport",
            engine_mode="engineMode",
            engine_version="engineVersion",
            global_cluster_identifier="globalClusterIdentifier",
            iops=123,
            kms_key_id="kmsKeyId",
            manage_master_user_password=False,
            master_user_authentication_type="masterUserAuthenticationType",
            master_username="masterUsername",
            master_user_password="masterUserPassword",
            master_user_secret=rds_mixins.CfnDBClusterPropsMixin.MasterUserSecretProperty(
                kms_key_id="kmsKeyId",
                secret_arn="secretArn"
            ),
            monitoring_interval=123,
            monitoring_role_arn="monitoringRoleArn",
            network_type="networkType",
            performance_insights_enabled=False,
            performance_insights_kms_key_id="performanceInsightsKmsKeyId",
            performance_insights_retention_period=123,
            port=123,
            preferred_backup_window="preferredBackupWindow",
            preferred_maintenance_window="preferredMaintenanceWindow",
            publicly_accessible=False,
            replication_source_identifier="replicationSourceIdentifier",
            restore_to_time="restoreToTime",
            restore_type="restoreType",
            scaling_configuration=rds_mixins.CfnDBClusterPropsMixin.ScalingConfigurationProperty(
                auto_pause=False,
                max_capacity=123,
                min_capacity=123,
                seconds_before_timeout=123,
                seconds_until_auto_pause=123,
                timeout_action="timeoutAction"
            ),
            serverless_v2_scaling_configuration=rds_mixins.CfnDBClusterPropsMixin.ServerlessV2ScalingConfigurationProperty(
                max_capacity=123,
                min_capacity=123,
                seconds_until_auto_pause=123
            ),
            snapshot_identifier="snapshotIdentifier",
            source_db_cluster_identifier="sourceDbClusterIdentifier",
            source_db_cluster_resource_id="sourceDbClusterResourceId",
            source_region="sourceRegion",
            storage_encrypted=False,
            storage_type="storageType",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            use_latest_restorable_time=False,
            vpc_security_group_ids=["vpcSecurityGroupIds"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDBClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBCluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0426765f8b906b0936fed08cc80c7784e3f62780f4a7589ad8ffae8d0b7aaef3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73903f3a7f50b357f79e8f8f01ca186d30e4bb3895f068d7ce071becf934372a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4fe7a534466db1dd4ddd7dea08d880ebcc82b90dfded5662fbefa509ec251f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBClusterMixinProps:
        return typing.cast(CfnDBClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBClusterPropsMixin.DBClusterRoleProperty",
        jsii_struct_bases=[],
        name_mapping={"feature_name": "featureName", "role_arn": "roleArn"},
    )
    class DBClusterRoleProperty:
        def __init__(
            self,
            *,
            feature_name: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an AWS Identity and Access Management (IAM) role that is associated with a DB cluster.

            :param feature_name: The name of the feature associated with the AWS Identity and Access Management (IAM) role. IAM roles that are associated with a DB cluster grant permission for the DB cluster to access other AWS services on your behalf. For the list of supported feature names, see the ``SupportedFeatureNames`` description in `DBEngineVersion <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DBEngineVersion.html>`_ in the *Amazon RDS API Reference* .
            :param role_arn: The Amazon Resource Name (ARN) of the IAM role that is associated with the DB cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-dbclusterrole.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                d_bCluster_role_property = rds_mixins.CfnDBClusterPropsMixin.DBClusterRoleProperty(
                    feature_name="featureName",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16cc24520a196a07064430096317906f87562602a7119850549bc07a907ba382)
                check_type(argname="argument feature_name", value=feature_name, expected_type=type_hints["feature_name"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if feature_name is not None:
                self._values["feature_name"] = feature_name
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def feature_name(self) -> typing.Optional[builtins.str]:
            '''The name of the feature associated with the AWS Identity and Access Management (IAM) role.

            IAM roles that are associated with a DB cluster grant permission for the DB cluster to access other AWS services on your behalf. For the list of supported feature names, see the ``SupportedFeatureNames`` description in `DBEngineVersion <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DBEngineVersion.html>`_ in the *Amazon RDS API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-dbclusterrole.html#cfn-rds-dbcluster-dbclusterrole-featurename
            '''
            result = self._values.get("feature_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role that is associated with the DB cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-dbclusterrole.html#cfn-rds-dbcluster-dbclusterrole-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DBClusterRoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBClusterPropsMixin.EndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address", "port": "port"},
    )
    class EndpointProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Endpoint`` return value specifies the connection endpoint for the primary instance of the DB cluster.

            :param address: Specifies the connection endpoint for the primary instance of the DB cluster.
            :param port: Specifies the port that the database engine is listening on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-endpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                endpoint_property = rds_mixins.CfnDBClusterPropsMixin.EndpointProperty(
                    address="address",
                    port="port"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fbe76a5c8d6cbd2e7bdc61c95378fa201e5650240c5686f0e6b5b5a7c135c63)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''Specifies the connection endpoint for the primary instance of the DB cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-endpoint.html#cfn-rds-dbcluster-endpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''Specifies the port that the database engine is listening on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-endpoint.html#cfn-rds-dbcluster-endpoint-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBClusterPropsMixin.MasterUserSecretProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId", "secret_arn": "secretArn"},
    )
    class MasterUserSecretProperty:
        def __init__(
            self,
            *,
            kms_key_id: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``MasterUserSecret`` return value specifies the secret managed by RDS in AWS Secrets Manager for the master user password.

            For more information, see `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html>`_ in the *Amazon RDS User Guide* and `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-secrets-manager.html>`_ in the *Amazon Aurora User Guide.*

            :param kms_key_id: The AWS KMS key identifier that is used to encrypt the secret.
            :param secret_arn: The Amazon Resource Name (ARN) of the secret. This parameter is a return value that you can retrieve using the ``Fn::GetAtt`` intrinsic function. For more information, see `Return values <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#aws-resource-rds-dbcluster-return-values>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                master_user_secret_property = rds_mixins.CfnDBClusterPropsMixin.MasterUserSecretProperty(
                    kms_key_id="kmsKeyId",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60095e872106c8429daafe37f171afcd2fe5aa0eb62d010ab82fbd8a2df5073a)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The AWS KMS key identifier that is used to encrypt the secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html#cfn-rds-dbcluster-masterusersecret-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the secret.

            This parameter is a return value that you can retrieve using the ``Fn::GetAtt`` intrinsic function. For more information, see `Return values <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#aws-resource-rds-dbcluster-return-values>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html#cfn-rds-dbcluster-masterusersecret-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MasterUserSecretProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBClusterPropsMixin.ReadEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address"},
    )
    class ReadEndpointProperty:
        def __init__(self, *, address: typing.Optional[builtins.str] = None) -> None:
            '''The ``ReadEndpoint`` return value specifies the reader endpoint for the DB cluster.

            The reader endpoint for a DB cluster load-balances connections across the Aurora Replicas that are available in a DB cluster. As clients request new connections to the reader endpoint, Aurora distributes the connection requests among the Aurora Replicas in the DB cluster. This functionality can help balance your read workload across multiple Aurora Replicas in your DB cluster.

            If a failover occurs, and the Aurora Replica that you are connected to is promoted to be the primary instance, your connection is dropped. To continue sending your read workload to other Aurora Replicas in the cluster, you can then reconnect to the reader endpoint.

            For more information about Aurora endpoints, see `Amazon Aurora connection management <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.Endpoints.html>`_ in the *Amazon Aurora User Guide* .

            :param address: The host address of the reader endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-readendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                read_endpoint_property = rds_mixins.CfnDBClusterPropsMixin.ReadEndpointProperty(
                    address="address"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92ff6889ac0d278daadaa99e0e9460705cc484405ac9e2f2e9c65fcdd5ed9fc4)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The host address of the reader endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-readendpoint.html#cfn-rds-dbcluster-readendpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBClusterPropsMixin.ScalingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_pause": "autoPause",
            "max_capacity": "maxCapacity",
            "min_capacity": "minCapacity",
            "seconds_before_timeout": "secondsBeforeTimeout",
            "seconds_until_auto_pause": "secondsUntilAutoPause",
            "timeout_action": "timeoutAction",
        },
    )
    class ScalingConfigurationProperty:
        def __init__(
            self,
            *,
            auto_pause: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_capacity: typing.Optional[jsii.Number] = None,
            min_capacity: typing.Optional[jsii.Number] = None,
            seconds_before_timeout: typing.Optional[jsii.Number] = None,
            seconds_until_auto_pause: typing.Optional[jsii.Number] = None,
            timeout_action: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ScalingConfiguration`` property type specifies the scaling configuration of an Aurora Serverless v1 DB cluster.

            For more information, see `Using Amazon Aurora Serverless <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.html>`_ in the *Amazon Aurora User Guide* .

            This property is only supported for Aurora Serverless v1. For Aurora Serverless v2, Use the ``ServerlessV2ScalingConfiguration`` property.

            Valid for: Aurora Serverless v1 DB clusters only

            :param auto_pause: Indicates whether to allow or disallow automatic pause for an Aurora DB cluster in ``serverless`` DB engine mode. A DB cluster can be paused only when it's idle (it has no connections). .. epigraph:: If a DB cluster is paused for more than seven days, the DB cluster might be backed up with a snapshot. In this case, the DB cluster is restored when there is a request to connect to it.
            :param max_capacity: The maximum capacity for an Aurora DB cluster in ``serverless`` DB engine mode. For Aurora MySQL, valid capacity values are ``1`` , ``2`` , ``4`` , ``8`` , ``16`` , ``32`` , ``64`` , ``128`` , and ``256`` . For Aurora PostgreSQL, valid capacity values are ``2`` , ``4`` , ``8`` , ``16`` , ``32`` , ``64`` , ``192`` , and ``384`` . The maximum capacity must be greater than or equal to the minimum capacity.
            :param min_capacity: The minimum capacity for an Aurora DB cluster in ``serverless`` DB engine mode. For Aurora MySQL, valid capacity values are ``1`` , ``2`` , ``4`` , ``8`` , ``16`` , ``32`` , ``64`` , ``128`` , and ``256`` . For Aurora PostgreSQL, valid capacity values are ``2`` , ``4`` , ``8`` , ``16`` , ``32`` , ``64`` , ``192`` , and ``384`` . The minimum capacity must be less than or equal to the maximum capacity.
            :param seconds_before_timeout: The amount of time, in seconds, that Aurora Serverless v1 tries to find a scaling point to perform seamless scaling before enforcing the timeout action. The default is 300. Specify a value between 60 and 600 seconds.
            :param seconds_until_auto_pause: The time, in seconds, before an Aurora DB cluster in ``serverless`` mode is paused. Specify a value between 300 and 86,400 seconds.
            :param timeout_action: The action to take when the timeout is reached, either ``ForceApplyCapacityChange`` or ``RollbackCapacityChange`` . ``ForceApplyCapacityChange`` sets the capacity to the specified value as soon as possible. ``RollbackCapacityChange`` , the default, ignores the capacity change if a scaling point isn't found in the timeout period. .. epigraph:: If you specify ``ForceApplyCapacityChange`` , connections that prevent Aurora Serverless v1 from finding a scaling point might be dropped. For more information, see `Autoscaling for Aurora Serverless v1 <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.how-it-works.html#aurora-serverless.how-it-works.auto-scaling>`_ in the *Amazon Aurora User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                scaling_configuration_property = rds_mixins.CfnDBClusterPropsMixin.ScalingConfigurationProperty(
                    auto_pause=False,
                    max_capacity=123,
                    min_capacity=123,
                    seconds_before_timeout=123,
                    seconds_until_auto_pause=123,
                    timeout_action="timeoutAction"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e11a9e386c17fd99becae1d93b08711eba50ac7dcb2268cb4ed7e2f23a5792dc)
                check_type(argname="argument auto_pause", value=auto_pause, expected_type=type_hints["auto_pause"])
                check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
                check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
                check_type(argname="argument seconds_before_timeout", value=seconds_before_timeout, expected_type=type_hints["seconds_before_timeout"])
                check_type(argname="argument seconds_until_auto_pause", value=seconds_until_auto_pause, expected_type=type_hints["seconds_until_auto_pause"])
                check_type(argname="argument timeout_action", value=timeout_action, expected_type=type_hints["timeout_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_pause is not None:
                self._values["auto_pause"] = auto_pause
            if max_capacity is not None:
                self._values["max_capacity"] = max_capacity
            if min_capacity is not None:
                self._values["min_capacity"] = min_capacity
            if seconds_before_timeout is not None:
                self._values["seconds_before_timeout"] = seconds_before_timeout
            if seconds_until_auto_pause is not None:
                self._values["seconds_until_auto_pause"] = seconds_until_auto_pause
            if timeout_action is not None:
                self._values["timeout_action"] = timeout_action

        @builtins.property
        def auto_pause(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to allow or disallow automatic pause for an Aurora DB cluster in ``serverless`` DB engine mode.

            A DB cluster can be paused only when it's idle (it has no connections).
            .. epigraph::

               If a DB cluster is paused for more than seven days, the DB cluster might be backed up with a snapshot. In this case, the DB cluster is restored when there is a request to connect to it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-autopause
            '''
            result = self._values.get("auto_pause")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            '''The maximum capacity for an Aurora DB cluster in ``serverless`` DB engine mode.

            For Aurora MySQL, valid capacity values are ``1`` , ``2`` , ``4`` , ``8`` , ``16`` , ``32`` , ``64`` , ``128`` , and ``256`` .

            For Aurora PostgreSQL, valid capacity values are ``2`` , ``4`` , ``8`` , ``16`` , ``32`` , ``64`` , ``192`` , and ``384`` .

            The maximum capacity must be greater than or equal to the minimum capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-maxcapacity
            '''
            result = self._values.get("max_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_capacity(self) -> typing.Optional[jsii.Number]:
            '''The minimum capacity for an Aurora DB cluster in ``serverless`` DB engine mode.

            For Aurora MySQL, valid capacity values are ``1`` , ``2`` , ``4`` , ``8`` , ``16`` , ``32`` , ``64`` , ``128`` , and ``256`` .

            For Aurora PostgreSQL, valid capacity values are ``2`` , ``4`` , ``8`` , ``16`` , ``32`` , ``64`` , ``192`` , and ``384`` .

            The minimum capacity must be less than or equal to the maximum capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-mincapacity
            '''
            result = self._values.get("min_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def seconds_before_timeout(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, that Aurora Serverless v1 tries to find a scaling point to perform seamless scaling before enforcing the timeout action.

            The default is 300.

            Specify a value between 60 and 600 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-secondsbeforetimeout
            '''
            result = self._values.get("seconds_before_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def seconds_until_auto_pause(self) -> typing.Optional[jsii.Number]:
            '''The time, in seconds, before an Aurora DB cluster in ``serverless`` mode is paused.

            Specify a value between 300 and 86,400 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-secondsuntilautopause
            '''
            result = self._values.get("seconds_until_auto_pause")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_action(self) -> typing.Optional[builtins.str]:
            '''The action to take when the timeout is reached, either ``ForceApplyCapacityChange`` or ``RollbackCapacityChange`` .

            ``ForceApplyCapacityChange`` sets the capacity to the specified value as soon as possible.

            ``RollbackCapacityChange`` , the default, ignores the capacity change if a scaling point isn't found in the timeout period.
            .. epigraph::

               If you specify ``ForceApplyCapacityChange`` , connections that prevent Aurora Serverless v1 from finding a scaling point might be dropped.

            For more information, see `Autoscaling for Aurora Serverless v1 <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.how-it-works.html#aurora-serverless.how-it-works.auto-scaling>`_ in the *Amazon Aurora User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-timeoutaction
            '''
            result = self._values.get("timeout_action")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBClusterPropsMixin.ServerlessV2ScalingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_capacity": "maxCapacity",
            "min_capacity": "minCapacity",
            "seconds_until_auto_pause": "secondsUntilAutoPause",
        },
    )
    class ServerlessV2ScalingConfigurationProperty:
        def __init__(
            self,
            *,
            max_capacity: typing.Optional[jsii.Number] = None,
            min_capacity: typing.Optional[jsii.Number] = None,
            seconds_until_auto_pause: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``ServerlessV2ScalingConfiguration`` property type specifies the scaling configuration of an Aurora Serverless V2 DB cluster.

            For more information, see `Using Amazon Aurora Serverless v2 <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html>`_ in the *Amazon Aurora User Guide* .

            If you have an Aurora cluster, you must set this attribute before you add a DB instance that uses the ``db.serverless`` DB instance class. For more information, see `Clusters that use Aurora Serverless v2 must have a capacity range specified <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.requirements.html#aurora-serverless-v2.requirements.capacity-range>`_ in the *Amazon Aurora User Guide* .

            This property is only supported for Aurora Serverless v2. For Aurora Serverless v1, use the ``ScalingConfiguration`` property.

            Valid for: Aurora Serverless v2 DB clusters

            :param max_capacity: The maximum number of Aurora capacity units (ACUs) for a DB instance in an Aurora Serverless v2 cluster. You can specify ACU values in half-step increments, such as 40, 40.5, 41, and so on. The largest value that you can use is 128. The maximum capacity must be higher than 0.5 ACUs. For more information, see `Choosing the maximum Aurora Serverless v2 capacity setting for a cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.setting-capacity.html#aurora-serverless-v2.max_capacity_considerations>`_ in the *Amazon Aurora User Guide* . Aurora automatically sets certain parameters for Aurora Serverless V2 DB instances to values that depend on the maximum ACU value in the capacity range. When you update the maximum capacity value, the ``ParameterApplyStatus`` value for the DB instance changes to ``pending-reboot`` . You can update the parameter values by rebooting the DB instance after changing the capacity range.
            :param min_capacity: The minimum number of Aurora capacity units (ACUs) for a DB instance in an Aurora Serverless v2 cluster. You can specify ACU values in half-step increments, such as 8, 8.5, 9, and so on. For Aurora versions that support the Aurora Serverless v2 auto-pause feature, the smallest value that you can use is 0. For versions that don't support Aurora Serverless v2 auto-pause, the smallest value that you can use is 0.5.
            :param seconds_until_auto_pause: Specifies the number of seconds an Aurora Serverless v2 DB instance must be idle before Aurora attempts to automatically pause it. Specify a value between 300 seconds (five minutes) and 86,400 seconds (one day). The default is 300 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-serverlessv2scalingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                serverless_v2_scaling_configuration_property = rds_mixins.CfnDBClusterPropsMixin.ServerlessV2ScalingConfigurationProperty(
                    max_capacity=123,
                    min_capacity=123,
                    seconds_until_auto_pause=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07fbb348251d57a869a276a01ebafe297ad9843da66d815e44c84bb65d814568)
                check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
                check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
                check_type(argname="argument seconds_until_auto_pause", value=seconds_until_auto_pause, expected_type=type_hints["seconds_until_auto_pause"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_capacity is not None:
                self._values["max_capacity"] = max_capacity
            if min_capacity is not None:
                self._values["min_capacity"] = min_capacity
            if seconds_until_auto_pause is not None:
                self._values["seconds_until_auto_pause"] = seconds_until_auto_pause

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of Aurora capacity units (ACUs) for a DB instance in an Aurora Serverless v2 cluster.

            You can specify ACU values in half-step increments, such as 40, 40.5, 41, and so on. The largest value that you can use is 128.

            The maximum capacity must be higher than 0.5 ACUs. For more information, see `Choosing the maximum Aurora Serverless v2 capacity setting for a cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.setting-capacity.html#aurora-serverless-v2.max_capacity_considerations>`_ in the *Amazon Aurora User Guide* .

            Aurora automatically sets certain parameters for Aurora Serverless V2 DB instances to values that depend on the maximum ACU value in the capacity range. When you update the maximum capacity value, the ``ParameterApplyStatus`` value for the DB instance changes to ``pending-reboot`` . You can update the parameter values by rebooting the DB instance after changing the capacity range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-serverlessv2scalingconfiguration.html#cfn-rds-dbcluster-serverlessv2scalingconfiguration-maxcapacity
            '''
            result = self._values.get("max_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_capacity(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of Aurora capacity units (ACUs) for a DB instance in an Aurora Serverless v2 cluster.

            You can specify ACU values in half-step increments, such as 8, 8.5, 9, and so on. For Aurora versions that support the Aurora Serverless v2 auto-pause feature, the smallest value that you can use is 0. For versions that don't support Aurora Serverless v2 auto-pause, the smallest value that you can use is 0.5.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-serverlessv2scalingconfiguration.html#cfn-rds-dbcluster-serverlessv2scalingconfiguration-mincapacity
            '''
            result = self._values.get("min_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def seconds_until_auto_pause(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of seconds an Aurora Serverless v2 DB instance must be idle before Aurora attempts to automatically pause it.

            Specify a value between 300 seconds (five minutes) and 86,400 seconds (one day). The default is 300 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-serverlessv2scalingconfiguration.html#cfn-rds-dbcluster-serverlessv2scalingconfiguration-secondsuntilautopause
            '''
            result = self._values.get("seconds_until_auto_pause")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerlessV2ScalingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_storage": "allocatedStorage",
        "allow_major_version_upgrade": "allowMajorVersionUpgrade",
        "apply_immediately": "applyImmediately",
        "associated_roles": "associatedRoles",
        "automatic_backup_replication_kms_key_id": "automaticBackupReplicationKmsKeyId",
        "automatic_backup_replication_region": "automaticBackupReplicationRegion",
        "automatic_backup_replication_retention_period": "automaticBackupReplicationRetentionPeriod",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "backup_retention_period": "backupRetentionPeriod",
        "backup_target": "backupTarget",
        "ca_certificate_identifier": "caCertificateIdentifier",
        "certificate_rotation_restart": "certificateRotationRestart",
        "character_set_name": "characterSetName",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "custom_iam_instance_profile": "customIamInstanceProfile",
        "database_insights_mode": "databaseInsightsMode",
        "db_cluster_identifier": "dbClusterIdentifier",
        "db_cluster_snapshot_identifier": "dbClusterSnapshotIdentifier",
        "db_instance_class": "dbInstanceClass",
        "db_instance_identifier": "dbInstanceIdentifier",
        "db_name": "dbName",
        "db_parameter_group_name": "dbParameterGroupName",
        "db_security_groups": "dbSecurityGroups",
        "db_snapshot_identifier": "dbSnapshotIdentifier",
        "db_subnet_group_name": "dbSubnetGroupName",
        "db_system_id": "dbSystemId",
        "dedicated_log_volume": "dedicatedLogVolume",
        "delete_automated_backups": "deleteAutomatedBackups",
        "deletion_protection": "deletionProtection",
        "domain": "domain",
        "domain_auth_secret_arn": "domainAuthSecretArn",
        "domain_dns_ips": "domainDnsIps",
        "domain_fqdn": "domainFqdn",
        "domain_iam_role_name": "domainIamRoleName",
        "domain_ou": "domainOu",
        "enable_cloudwatch_logs_exports": "enableCloudwatchLogsExports",
        "enable_iam_database_authentication": "enableIamDatabaseAuthentication",
        "enable_performance_insights": "enablePerformanceInsights",
        "engine": "engine",
        "engine_lifecycle_support": "engineLifecycleSupport",
        "engine_version": "engineVersion",
        "iops": "iops",
        "kms_key_id": "kmsKeyId",
        "license_model": "licenseModel",
        "manage_master_user_password": "manageMasterUserPassword",
        "master_user_authentication_type": "masterUserAuthenticationType",
        "master_username": "masterUsername",
        "master_user_password": "masterUserPassword",
        "master_user_secret": "masterUserSecret",
        "max_allocated_storage": "maxAllocatedStorage",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role_arn": "monitoringRoleArn",
        "multi_az": "multiAz",
        "nchar_character_set_name": "ncharCharacterSetName",
        "network_type": "networkType",
        "option_group_name": "optionGroupName",
        "performance_insights_kms_key_id": "performanceInsightsKmsKeyId",
        "performance_insights_retention_period": "performanceInsightsRetentionPeriod",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "processor_features": "processorFeatures",
        "promotion_tier": "promotionTier",
        "publicly_accessible": "publiclyAccessible",
        "replica_mode": "replicaMode",
        "restore_time": "restoreTime",
        "source_db_cluster_identifier": "sourceDbClusterIdentifier",
        "source_db_instance_automated_backups_arn": "sourceDbInstanceAutomatedBackupsArn",
        "source_db_instance_identifier": "sourceDbInstanceIdentifier",
        "source_dbi_resource_id": "sourceDbiResourceId",
        "source_region": "sourceRegion",
        "storage_encrypted": "storageEncrypted",
        "storage_throughput": "storageThroughput",
        "storage_type": "storageType",
        "tags": "tags",
        "tde_credential_arn": "tdeCredentialArn",
        "tde_credential_password": "tdeCredentialPassword",
        "timezone": "timezone",
        "use_default_processor_features": "useDefaultProcessorFeatures",
        "use_latest_restorable_time": "useLatestRestorableTime",
        "vpc_security_groups": "vpcSecurityGroups",
    },
)
class CfnDBInstanceMixinProps:
    def __init__(
        self,
        *,
        allocated_storage: typing.Optional[builtins.str] = None,
        allow_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        apply_immediately: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        associated_roles: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDBInstancePropsMixin.DBInstanceRoleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        automatic_backup_replication_kms_key_id: typing.Optional[builtins.str] = None,
        automatic_backup_replication_region: typing.Optional[builtins.str] = None,
        automatic_backup_replication_retention_period: typing.Optional[jsii.Number] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        backup_retention_period: typing.Optional[jsii.Number] = None,
        backup_target: typing.Optional[builtins.str] = None,
        ca_certificate_identifier: typing.Optional[builtins.str] = None,
        certificate_rotation_restart: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        character_set_name: typing.Optional[builtins.str] = None,
        copy_tags_to_snapshot: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        custom_iam_instance_profile: typing.Optional[builtins.str] = None,
        database_insights_mode: typing.Optional[builtins.str] = None,
        db_cluster_identifier: typing.Optional[builtins.str] = None,
        db_cluster_snapshot_identifier: typing.Optional[builtins.str] = None,
        db_instance_class: typing.Optional[builtins.str] = None,
        db_instance_identifier: typing.Optional[builtins.str] = None,
        db_name: typing.Optional[builtins.str] = None,
        db_parameter_group_name: typing.Optional[builtins.str] = None,
        db_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        db_snapshot_identifier: typing.Optional[builtins.str] = None,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        db_system_id: typing.Optional[builtins.str] = None,
        dedicated_log_volume: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        delete_automated_backups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_auth_secret_arn: typing.Optional[builtins.str] = None,
        domain_dns_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_fqdn: typing.Optional[builtins.str] = None,
        domain_iam_role_name: typing.Optional[builtins.str] = None,
        domain_ou: typing.Optional[builtins.str] = None,
        enable_cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_iam_database_authentication: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        enable_performance_insights: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_lifecycle_support: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        license_model: typing.Optional[builtins.str] = None,
        manage_master_user_password: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        master_user_authentication_type: typing.Optional[builtins.str] = None,
        master_username: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[builtins.str] = None,
        master_user_secret: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDBInstancePropsMixin.MasterUserSecretProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[jsii.Number] = None,
        monitoring_role_arn: typing.Optional[builtins.str] = None,
        multi_az: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        nchar_character_set_name: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        option_group_name: typing.Optional[builtins.str] = None,
        performance_insights_kms_key_id: typing.Optional[builtins.str] = None,
        performance_insights_retention_period: typing.Optional[jsii.Number] = None,
        port: typing.Optional[builtins.str] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        processor_features: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDBInstancePropsMixin.ProcessorFeatureProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        promotion_tier: typing.Optional[jsii.Number] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        replica_mode: typing.Optional[builtins.str] = None,
        restore_time: typing.Optional[builtins.str] = None,
        source_db_cluster_identifier: typing.Optional[builtins.str] = None,
        source_db_instance_automated_backups_arn: typing.Optional[builtins.str] = None,
        source_db_instance_identifier: typing.Optional[builtins.str] = None,
        source_dbi_resource_id: typing.Optional[builtins.str] = None,
        source_region: typing.Optional[builtins.str] = None,
        storage_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        storage_throughput: typing.Optional[jsii.Number] = None,
        storage_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tde_credential_arn: typing.Optional[builtins.str] = None,
        tde_credential_password: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
        use_default_processor_features: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        use_latest_restorable_time: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        vpc_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnDBInstancePropsMixin.

        :param allocated_storage: The amount of storage in gibibytes (GiB) to be initially allocated for the database instance. .. epigraph:: If any value is set in the ``Iops`` parameter, ``AllocatedStorage`` must be at least 100 GiB, which corresponds to the minimum Iops value of 1,000. If you increase the ``Iops`` value (in 1,000 IOPS increments), then you must also increase the ``AllocatedStorage`` value (in 100-GiB increments). *Amazon Aurora* Not applicable. Aurora cluster volumes automatically grow as the amount of data in your database increases, though you are only charged for the space that you use in an Aurora cluster volume. *Db2* Constraints to the amount of storage for each storage type are the following: - General Purpose (SSD) storage (gp3): Must be an integer from 20 to 64000. - Provisioned IOPS storage (io1): Must be an integer from 100 to 64000. *MySQL* Constraints to the amount of storage for each storage type are the following: - General Purpose (SSD) storage (gp2): Must be an integer from 20 to 65536. - Provisioned IOPS storage (io1): Must be an integer from 100 to 65536. - Magnetic storage (standard): Must be an integer from 5 to 3072. *MariaDB* Constraints to the amount of storage for each storage type are the following: - General Purpose (SSD) storage (gp2): Must be an integer from 20 to 65536. - Provisioned IOPS storage (io1): Must be an integer from 100 to 65536. - Magnetic storage (standard): Must be an integer from 5 to 3072. *PostgreSQL* Constraints to the amount of storage for each storage type are the following: - General Purpose (SSD) storage (gp2): Must be an integer from 20 to 65536. - Provisioned IOPS storage (io1): Must be an integer from 100 to 65536. - Magnetic storage (standard): Must be an integer from 5 to 3072. *Oracle* Constraints to the amount of storage for each storage type are the following: - General Purpose (SSD) storage (gp2): Must be an integer from 20 to 65536. - Provisioned IOPS storage (io1): Must be an integer from 100 to 65536. - Magnetic storage (standard): Must be an integer from 10 to 3072. *SQL Server* Constraints to the amount of storage for each storage type are the following: - General Purpose (SSD) storage (gp2): - Enterprise and Standard editions: Must be an integer from 20 to 16384. - Web and Express editions: Must be an integer from 20 to 16384. - Provisioned IOPS storage (io1): - Enterprise and Standard editions: Must be an integer from 20 to 16384. - Web and Express editions: Must be an integer from 20 to 16384. - Magnetic storage (standard): - Enterprise and Standard editions: Must be an integer from 20 to 1024. - Web and Express editions: Must be an integer from 20 to 1024.
        :param allow_major_version_upgrade: A value that indicates whether major version upgrades are allowed. Changing this parameter doesn't result in an outage and the change is asynchronously applied as soon as possible. Constraints: Major version upgrades must be allowed when specifying a value for the ``EngineVersion`` parameter that is a different major version than the DB instance's current version.
        :param apply_immediately: Specifies whether changes to the DB instance and any pending modifications are applied immediately, regardless of the ``PreferredMaintenanceWindow`` setting. If set to ``false`` , changes are applied during the next maintenance window. Until RDS applies the changes, the DB instance remains in a drift state. As a result, the configuration doesn't fully reflect the requested modifications and temporarily diverges from the intended state. In addition to the settings described in `Modifying a DB instance <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.DBInstance.Modifying.html>`_ , this property also determines whether the DB instance reboots when a static parameter is modified in the associated DB parameter group. Default: ``true``
        :param associated_roles: The AWS Identity and Access Management (IAM) roles associated with the DB instance. *Amazon Aurora* Not applicable. The associated roles are managed by the DB cluster.
        :param automatic_backup_replication_kms_key_id: The AWS KMS key identifier for encryption of the replicated automated backups. The KMS key ID is the Amazon Resource Name (ARN) for the KMS encryption key in the destination AWS Region , for example, ``arn:aws:kms:us-east-1:123456789012:key/AKIAIOSFODNN7EXAMPLE`` .
        :param automatic_backup_replication_region: The AWS Region associated with the automated backup.
        :param automatic_backup_replication_retention_period: The retention period for automated backups in a different AWS Region. Use this parameter to set a unique retention period that only applies to cross-Region automated backups. To enable automated backups in a different Region, specify a positive value for the ``AutomaticBackupReplicationRegion`` parameter. If not specified, this parameter defaults to the value of the ``BackupRetentionPeriod`` parameter. The maximum allowed value is 35.
        :param auto_minor_version_upgrade: A value that indicates whether minor engine upgrades are applied automatically to the DB instance during the maintenance window. By default, minor engine upgrades are applied automatically.
        :param availability_zone: The Availability Zone (AZ) where the database will be created. For information on AWS Regions and Availability Zones, see `Regions and Availability Zones <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html>`_ . For Amazon Aurora, each Aurora DB cluster hosts copies of its storage in three separate Availability Zones. Specify one of these Availability Zones. Aurora automatically chooses an appropriate Availability Zone if you don't specify one. Default: A random, system-chosen Availability Zone in the endpoint's AWS Region . Constraints: - The ``AvailabilityZone`` parameter can't be specified if the DB instance is a Multi-AZ deployment. - The specified Availability Zone must be in the same AWS Region as the current endpoint. Example: ``us-east-1d``
        :param backup_retention_period: The number of days for which automated backups are retained. Setting this parameter to a positive number enables backups. Setting this parameter to 0 disables automated backups. *Amazon Aurora* Not applicable. The retention period for automated backups is managed by the DB cluster. Default: 1 Constraints: - Must be a value from 0 to 35 - Can't be set to 0 if the DB instance is a source to read replicas
        :param backup_target: The location for storing automated backups and manual snapshots. Valid Values: - ``local`` (Dedicated Local Zone) - ``outposts`` ( AWS Outposts) - ``region`` ( AWS Region ) Default: ``region`` For more information, see `Working with Amazon RDS on AWS Outposts <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-on-outposts.html>`_ in the *Amazon RDS User Guide* .
        :param ca_certificate_identifier: The identifier of the CA certificate for this DB instance. For more information, see `Using SSL/TLS to encrypt a connection to a DB instance <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html>`_ in the *Amazon RDS User Guide* and `Using SSL/TLS to encrypt a connection to a DB cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL.html>`_ in the *Amazon Aurora User Guide* .
        :param certificate_rotation_restart: Specifies whether the DB instance is restarted when you rotate your SSL/TLS certificate. By default, the DB instance is restarted when you rotate your SSL/TLS certificate. The certificate is not updated until the DB instance is restarted. .. epigraph:: Set this parameter only if you are *not* using SSL/TLS to connect to the DB instance. If you are using SSL/TLS to connect to the DB instance, follow the appropriate instructions for your DB engine to rotate your SSL/TLS certificate: - For more information about rotating your SSL/TLS certificate for RDS DB engines, see `Rotating Your SSL/TLS Certificate. <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL-certificate-rotation.html>`_ in the *Amazon RDS User Guide.* - For more information about rotating your SSL/TLS certificate for Aurora DB engines, see `Rotating Your SSL/TLS Certificate <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL-certificate-rotation.html>`_ in the *Amazon Aurora User Guide* . This setting doesn't apply to RDS Custom DB instances.
        :param character_set_name: For supported engines, indicates that the DB instance should be associated with the specified character set. *Amazon Aurora* Not applicable. The character set is managed by the DB cluster. For more information, see `AWS::RDS::DBCluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html>`_ .
        :param copy_tags_to_snapshot: Specifies whether to copy tags from the DB instance to snapshots of the DB instance. By default, tags are not copied. This setting doesn't apply to Amazon Aurora DB instances. Copying tags to snapshots is managed by the DB cluster. Setting this value for an Aurora DB instance has no effect on the DB cluster setting.
        :param custom_iam_instance_profile: The instance profile associated with the underlying Amazon EC2 instance of an RDS Custom DB instance. This setting is required for RDS Custom. Constraints: - The profile must exist in your account. - The profile must have an IAM role that Amazon EC2 has permissions to assume. - The instance profile name and the associated IAM role name must start with the prefix ``AWSRDSCustom`` . For the list of permissions required for the IAM role, see `Configure IAM and your VPC <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-setup-orcl.html#custom-setup-orcl.iam-vpc>`_ in the *Amazon RDS User Guide* .
        :param database_insights_mode: The mode of Database Insights to enable for the DB instance. .. epigraph:: Aurora DB instances inherit this value from the DB cluster, so you can't change this value.
        :param db_cluster_identifier: The identifier of the DB cluster that this DB instance will belong to. This setting doesn't apply to RDS Custom DB instances.
        :param db_cluster_snapshot_identifier: The identifier for the Multi-AZ DB cluster snapshot to restore from. For more information on Multi-AZ DB clusters, see `Multi-AZ DB cluster deployments <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts.html>`_ in the *Amazon RDS User Guide* . Constraints: - Must match the identifier of an existing Multi-AZ DB cluster snapshot. - Can't be specified when ``DBSnapshotIdentifier`` is specified. - Must be specified when ``DBSnapshotIdentifier`` isn't specified. - If you are restoring from a shared manual Multi-AZ DB cluster snapshot, the ``DBClusterSnapshotIdentifier`` must be the ARN of the shared snapshot. - Can't be the identifier of an Aurora DB cluster snapshot.
        :param db_instance_class: The compute and memory capacity of the DB instance, for example ``db.m5.large`` . Not all DB instance classes are available in all AWS Regions , or for all database engines. For the full list of DB instance classes, and availability for your engine, see `DB instance classes <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html>`_ in the *Amazon RDS User Guide* or `Aurora DB instance classes <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.DBInstanceClass.html>`_ in the *Amazon Aurora User Guide* .
        :param db_instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the DB instance. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . For information about constraints that apply to DB instance identifiers, see `Naming constraints in Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html#RDS_Limits.Constraints>`_ in the *Amazon RDS User Guide* . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param db_name: The meaning of this parameter differs according to the database engine you use. .. epigraph:: If you specify the ``[DBSnapshotIdentifier](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsnapshotidentifier)`` property, this property only applies to RDS for Oracle. *Amazon Aurora* Not applicable. The database name is managed by the DB cluster. *Db2* The name of the database to create when the DB instance is created. If this parameter isn't specified, no database is created in the DB instance. Constraints: - Must contain 1 to 64 letters or numbers. - Must begin with a letter. Subsequent characters can be letters, underscores, or digits (0-9). - Can't be a word reserved by the specified database engine. *MySQL* The name of the database to create when the DB instance is created. If this parameter is not specified, no database is created in the DB instance. Constraints: - Must contain 1 to 64 letters or numbers. - Can't be a word reserved by the specified database engine *MariaDB* The name of the database to create when the DB instance is created. If this parameter is not specified, no database is created in the DB instance. Constraints: - Must contain 1 to 64 letters or numbers. - Can't be a word reserved by the specified database engine *PostgreSQL* The name of the database to create when the DB instance is created. If this parameter is not specified, the default ``postgres`` database is created in the DB instance. Constraints: - Must begin with a letter. Subsequent characters can be letters, underscores, or digits (0-9). - Must contain 1 to 63 characters. - Can't be a word reserved by the specified database engine *Oracle* The Oracle System ID (SID) of the created DB instance. If you specify ``null`` , the default value ``ORCL`` is used. You can't specify the string NULL, or any other reserved word, for ``DBName`` . Default: ``ORCL`` Constraints: - Can't be longer than 8 characters *SQL Server* Not applicable. Must be null.
        :param db_parameter_group_name: The name of an existing DB parameter group or a reference to an `AWS::RDS::DBParameterGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html>`_ resource created in the template. To list all of the available DB parameter group names, use the following command: ``aws rds describe-db-parameter-groups --query "DBParameterGroups[].DBParameterGroupName" --output text`` .. epigraph:: If any of the data members of the referenced parameter group are changed during an update, the DB instance might need to be restarted, which causes some interruption. If the parameter group contains static parameters, whether they were changed or not, an update triggers a reboot. If you don't specify a value for ``DBParameterGroupName`` property, the default DB parameter group for the specified engine and engine version is used.
        :param db_security_groups: A list of the DB security groups to assign to the DB instance. The list can include both the name of existing DB security groups or references to AWS::RDS::DBSecurityGroup resources created in the template. If you set DBSecurityGroups, you must not set VPCSecurityGroups, and vice versa. Also, note that the DBSecurityGroups property exists only for backwards compatibility with older regions and is no longer recommended for providing security information to an RDS DB instance. Instead, use VPCSecurityGroups. .. epigraph:: If you specify this property, AWS CloudFormation sends only the following properties (if specified) to Amazon RDS during create operations: - ``AllocatedStorage`` - ``AutoMinorVersionUpgrade`` - ``AvailabilityZone`` - ``BackupRetentionPeriod`` - ``CharacterSetName`` - ``DBInstanceClass`` - ``DBName`` - ``DBParameterGroupName`` - ``DBSecurityGroups`` - ``DBSubnetGroupName`` - ``Engine`` - ``EngineVersion`` - ``Iops`` - ``LicenseModel`` - ``MasterUsername`` - ``MasterUserPassword`` - ``MultiAZ`` - ``OptionGroupName`` - ``PreferredBackupWindow`` - ``PreferredMaintenanceWindow`` All other properties are ignored. Specify a virtual private cloud (VPC) security group if you want to submit other properties, such as ``StorageType`` , ``StorageEncrypted`` , or ``KmsKeyId`` . If you're already using the ``DBSecurityGroups`` property, you can't use these other properties by updating your DB instance to use a VPC security group. You must recreate the DB instance.
        :param db_snapshot_identifier: The name or Amazon Resource Name (ARN) of the DB snapshot that's used to restore the DB instance. If you're restoring from a shared manual DB snapshot, you must specify the ARN of the snapshot. By specifying this property, you can create a DB instance from the specified DB snapshot. If the ``DBSnapshotIdentifier`` property is an empty string or the ``AWS::RDS::DBInstance`` declaration has no ``DBSnapshotIdentifier`` property, AWS CloudFormation creates a new database. If the property contains a value (other than an empty string), AWS CloudFormation creates a database from the specified snapshot. If a snapshot with the specified name doesn't exist, AWS CloudFormation can't create the database and it rolls back the stack. Some DB instance properties aren't valid when you restore from a snapshot, such as the ``MasterUsername`` and ``MasterUserPassword`` properties, and the point-in-time recovery properties ``RestoreTime`` and ``UseLatestRestorableTime`` . For information about the properties that you can specify, see the ```RestoreDBInstanceFromDBSnapshot`` <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_RestoreDBInstanceFromDBSnapshot.html>`_ action in the *Amazon RDS API Reference* . After you restore a DB instance with a ``DBSnapshotIdentifier`` property, you must specify the same ``DBSnapshotIdentifier`` property for any future updates to the DB instance. When you specify this property for an update, the DB instance is not restored from the DB snapshot again, and the data in the database is not changed. However, if you don't specify the ``DBSnapshotIdentifier`` property, an empty DB instance is created, and the original DB instance is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB instance is restored from the specified ``DBSnapshotIdentifier`` property, and the original DB instance is deleted. If you specify the ``DBSnapshotIdentifier`` property to restore a DB instance (as opposed to specifying it for DB instance updates), then don't specify the following properties: - ``CharacterSetName`` - ``DBClusterIdentifier`` - ``DBName`` - ``KmsKeyId`` - ``MasterUsername`` - ``MasterUserPassword`` - ``PromotionTier`` - ``SourceDBInstanceIdentifier`` - ``SourceRegion`` - ``StorageEncrypted`` (for an unencrypted snapshot) - ``Timezone`` *Amazon Aurora* Not applicable. Snapshot restore is managed by the DB cluster.
        :param db_subnet_group_name: A DB subnet group to associate with the DB instance. If you update this value, the new subnet group must be a subnet group in a new VPC. If you don't specify a DB subnet group, RDS uses the default DB subnet group if one exists. If a default DB subnet group does not exist, and you don't specify a ``DBSubnetGroupName`` , the DB instance fails to launch. For more information about using Amazon RDS in a VPC, see `Amazon VPC and Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.html>`_ in the *Amazon RDS User Guide* . This setting doesn't apply to Amazon Aurora DB instances. The DB subnet group is managed by the DB cluster. If specified, the setting must match the DB cluster setting.
        :param db_system_id: The Oracle system identifier (SID), which is the name of the Oracle database instance that manages your database files. In this context, the term "Oracle database instance" refers exclusively to the system global area (SGA) and Oracle background processes. If you don't specify a SID, the value defaults to ``RDSCDB`` . The Oracle SID is also the name of your CDB.
        :param dedicated_log_volume: Indicates whether the DB instance has a dedicated log volume (DLV) enabled.
        :param delete_automated_backups: A value that indicates whether to remove automated backups immediately after the DB instance is deleted. This parameter isn't case-sensitive. The default is to remove automated backups immediately after the DB instance is deleted. *Amazon Aurora* Not applicable. When you delete a DB cluster, all automated backups for that DB cluster are deleted and can't be recovered. Manual DB cluster snapshots of the DB cluster are not deleted.
        :param deletion_protection: Specifies whether the DB instance has deletion protection enabled. The database can't be deleted when deletion protection is enabled. By default, deletion protection isn't enabled. For more information, see `Deleting a DB Instance <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_DeleteInstance.html>`_ . This setting doesn't apply to Amazon Aurora DB instances. You can enable or disable deletion protection for the DB cluster. For more information, see ``CreateDBCluster`` . DB instances in a DB cluster can be deleted even when deletion protection is enabled for the DB cluster.
        :param domain: The Active Directory directory ID to create the DB instance in. Currently, only Db2, MySQL, Microsoft SQL Server, Oracle, and PostgreSQL DB instances can be created in an Active Directory Domain. For more information, see `Kerberos Authentication <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/kerberos-authentication.html>`_ in the *Amazon RDS User Guide* .
        :param domain_auth_secret_arn: The ARN for the Secrets Manager secret with the credentials for the user joining the domain. Example: ``arn:aws:secretsmanager:region:account-number:secret:myselfmanagedADtestsecret-123456``
        :param domain_dns_ips: The IPv4 DNS IP addresses of your primary and secondary Active Directory domain controllers. Constraints: - Two IP addresses must be provided. If there isn't a secondary domain controller, use the IP address of the primary domain controller for both entries in the list. Example: ``123.124.125.126,234.235.236.237``
        :param domain_fqdn: The fully qualified domain name (FQDN) of an Active Directory domain. Constraints: - Can't be longer than 64 characters. Example: ``mymanagedADtest.mymanagedAD.mydomain``
        :param domain_iam_role_name: The name of the IAM role to use when making API calls to the Directory Service. This setting doesn't apply to the following DB instances: - Amazon Aurora (The domain is managed by the DB cluster.) - RDS Custom
        :param domain_ou: The Active Directory organizational unit for your DB instance to join. Constraints: - Must be in the distinguished name format. - Can't be longer than 64 characters. Example: ``OU=mymanagedADtestOU,DC=mymanagedADtest,DC=mymanagedAD,DC=mydomain``
        :param enable_cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. The values in the list depend on the DB engine being used. For more information, see `Publishing Database Logs to Amazon CloudWatch Logs <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.html#USER_LogAccess.Procedural.UploadtoCloudWatch>`_ in the *Amazon Relational Database Service User Guide* . *Amazon Aurora* Not applicable. CloudWatch Logs exports are managed by the DB cluster. *Db2* Valid values: ``diag.log`` , ``notify.log`` *MariaDB* Valid values: ``audit`` , ``error`` , ``general`` , ``slowquery`` *Microsoft SQL Server* Valid values: ``agent`` , ``error`` *MySQL* Valid values: ``audit`` , ``error`` , ``general`` , ``slowquery`` *Oracle* Valid values: ``alert`` , ``audit`` , ``listener`` , ``trace`` , ``oemagent`` *PostgreSQL* Valid values: ``postgresql`` , ``upgrade``
        :param enable_iam_database_authentication: A value that indicates whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. By default, mapping is disabled. This property is supported for RDS for MariaDB, RDS for MySQL, and RDS for PostgreSQL. For more information, see `IAM Database Authentication for MariaDB, MySQL, and PostgreSQL <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html>`_ in the *Amazon RDS User Guide.* *Amazon Aurora* Not applicable. Mapping AWS IAM accounts to database accounts is managed by the DB cluster.
        :param enable_performance_insights: Specifies whether to enable Performance Insights for the DB instance. For more information, see `Using Amazon Performance Insights <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html>`_ in the *Amazon RDS User Guide* . This setting doesn't apply to RDS Custom DB instances.
        :param engine: The name of the database engine to use for this DB instance. Not every database engine is available in every AWS Region. This property is required when creating a DB instance. .. epigraph:: You can convert an Oracle database from the non-CDB architecture to the container database (CDB) architecture by updating the ``Engine`` value in your templates from ``oracle-ee`` to ``oracle-ee-cdb`` or from ``oracle-se2`` to ``oracle-se2-cdb`` . Converting to the CDB architecture requires an interruption. Valid Values: - ``aurora-mysql`` (for Aurora MySQL DB instances) - ``aurora-postgresql`` (for Aurora PostgreSQL DB instances) - ``custom-oracle-ee`` (for RDS Custom for Oracle DB instances) - ``custom-oracle-ee-cdb`` (for RDS Custom for Oracle DB instances) - ``custom-sqlserver-ee`` (for RDS Custom for SQL Server DB instances) - ``custom-sqlserver-se`` (for RDS Custom for SQL Server DB instances) - ``custom-sqlserver-web`` (for RDS Custom for SQL Server DB instances) - ``db2-ae`` - ``db2-se`` - ``mariadb`` - ``mysql`` - ``oracle-ee`` - ``oracle-ee-cdb`` - ``oracle-se2`` - ``oracle-se2-cdb`` - ``postgres`` - ``sqlserver-ee`` - ``sqlserver-se`` - ``sqlserver-ex`` - ``sqlserver-web``
        :param engine_lifecycle_support: The life cycle type for this DB instance. .. epigraph:: By default, this value is set to ``open-source-rds-extended-support`` , which enrolls your DB instance into Amazon RDS Extended Support. At the end of standard support, you can avoid charges for Extended Support by setting the value to ``open-source-rds-extended-support-disabled`` . In this case, creating the DB instance will fail if the DB major version is past its end of standard support date. This setting applies only to RDS for MySQL and RDS for PostgreSQL. For Amazon Aurora DB instances, the life cycle type is managed by the DB cluster. You can use this setting to enroll your DB instance into Amazon RDS Extended Support. With RDS Extended Support, you can run the selected major engine version on your DB instance past the end of standard support for that engine version. For more information, see `Amazon RDS Extended Support with Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support.html>`_ in the *Amazon RDS User Guide* . Valid Values: ``open-source-rds-extended-support | open-source-rds-extended-support-disabled`` Default: ``open-source-rds-extended-support``
        :param engine_version: The version number of the database engine to use. For a list of valid engine versions, use the ``DescribeDBEngineVersions`` action. The following are the database engines and links to information about the major and minor versions that are available with Amazon RDS. Not every database engine is available for every AWS Region. *Amazon Aurora* Not applicable. The version number of the database engine to be used by the DB instance is managed by the DB cluster. *Db2* See `Amazon RDS for Db2 <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Db2.html#Db2.Concepts.VersionMgmt>`_ in the *Amazon RDS User Guide.* *MariaDB* See `MariaDB on Amazon RDS Versions <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MariaDB.html#MariaDB.Concepts.VersionMgmt>`_ in the *Amazon RDS User Guide.* *Microsoft SQL Server* See `Microsoft SQL Server Versions on Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_SQLServer.html#SQLServer.Concepts.General.VersionSupport>`_ in the *Amazon RDS User Guide.* *MySQL* See `MySQL on Amazon RDS Versions <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html#MySQL.Concepts.VersionMgmt>`_ in the *Amazon RDS User Guide.* *Oracle* See `Oracle Database Engine Release Notes <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.Oracle.PatchComposition.html>`_ in the *Amazon RDS User Guide.* *PostgreSQL* See `Supported PostgreSQL Database Versions <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts.General.DBVersions>`_ in the *Amazon RDS User Guide.*
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. If you specify this property, you must follow the range of allowed ratios of your requested IOPS rate to the amount of storage that you allocate (IOPS to allocated storage). For example, you can provision an Oracle database instance with 1000 IOPS and 200 GiB of storage (a ratio of 5:1), or specify 2000 IOPS with 200 GiB of storage (a ratio of 10:1). For more information, see `Amazon RDS Provisioned IOPS Storage to Improve Performance <https://docs.aws.amazon.com/AmazonRDS/latest/DeveloperGuide/CHAP_Storage.html#USER_PIOPS>`_ in the *Amazon RDS User Guide* . .. epigraph:: If you specify ``io1`` for the ``StorageType`` property, then you must also specify the ``Iops`` property. Constraints: - For RDS for Db2, MariaDB, MySQL, Oracle, and PostgreSQL - Must be a multiple between .5 and 50 of the storage amount for the DB instance. - For RDS for SQL Server - Must be a multiple between 1 and 50 of the storage amount for the DB instance.
        :param kms_key_id: The ARN of the AWS KMS key that's used to encrypt the DB instance, such as ``arn:aws:kms:us-east-1:012345678910:key/abcd1234-a123-456a-a12b-a123b4cd56ef`` . If you enable the StorageEncrypted property but don't specify this property, AWS CloudFormation uses the default KMS key. If you specify this property, you must set the StorageEncrypted property to true. If you specify the ``SourceDBInstanceIdentifier`` or ``SourceDbiResourceId`` property, don't specify this property. The value is inherited from the source DB instance, and if the DB instance is encrypted, the specified ``KmsKeyId`` property is used. However, if the source DB instance is in a different AWS Region, you must specify a KMS key ID. If you specify the ``SourceDBInstanceAutomatedBackupsArn`` property, don't specify this property. The value is inherited from the source DB instance automated backup, and if the automated backup is encrypted, the specified ``KmsKeyId`` property is used. If you create an encrypted read replica in a different AWS Region, then you must specify a KMS key for the destination AWS Region. KMS encryption keys are specific to the region that they're created in, and you can't use encryption keys from one region in another region. If you specify the ``DBSnapshotIdentifier`` property, don't specify this property. The ``StorageEncrypted`` property value is inherited from the snapshot. If the DB instance is encrypted, the specified ``KmsKeyId`` property is also inherited from the snapshot. If you specify ``DBSecurityGroups`` , AWS CloudFormation ignores this property. To specify both a security group and this property, you must use a VPC security group. For more information about Amazon RDS and VPC, see `Using Amazon RDS with Amazon VPC <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.html>`_ in the *Amazon RDS User Guide* . *Amazon Aurora* Not applicable. The KMS key identifier is managed by the DB cluster.
        :param license_model: License model information for this DB instance. Valid Values: - Aurora MySQL - ``general-public-license`` - Aurora PostgreSQL - ``postgresql-license`` - RDS for Db2 - ``bring-your-own-license`` . For more information about RDS for Db2 licensing, see ` <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/db2-licensing.html>`_ in the *Amazon RDS User Guide.* - RDS for MariaDB - ``general-public-license`` - RDS for Microsoft SQL Server - ``license-included`` - RDS for MySQL - ``general-public-license`` - RDS for Oracle - ``bring-your-own-license`` or ``license-included`` - RDS for PostgreSQL - ``postgresql-license`` .. epigraph:: If you've specified ``DBSecurityGroups`` and then you update the license model, AWS CloudFormation replaces the underlying DB instance. This will incur some interruptions to database availability.
        :param manage_master_user_password: Specifies whether to manage the master user password with AWS Secrets Manager. For more information, see `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html>`_ in the *Amazon RDS User Guide.* Constraints: - Can't manage the master user password with AWS Secrets Manager if ``MasterUserPassword`` is specified.
        :param master_user_authentication_type: Specifies the authentication type for the master user. With IAM master user authentication, you can configure the master DB user with IAM database authentication when you create a DB instance. You can specify one of the following values: - ``password`` - Use standard database authentication with a password. - ``iam-db-auth`` - Use IAM database authentication for the master user. This option is only valid for RDS for MySQL, RDS for MariaDB, RDS for PostgreSQL, Aurora MySQL, and Aurora PostgreSQL engines.
        :param master_username: The master user name for the DB instance. .. epigraph:: If you specify the ``SourceDBInstanceIdentifier`` or ``DBSnapshotIdentifier`` property, don't specify this property. The value is inherited from the source DB instance or snapshot. When migrating a self-managed Db2 database, we recommend that you use the same master username as your self-managed Db2 instance name. *Amazon Aurora* Not applicable. The name for the master user is managed by the DB cluster. *RDS for Db2* Constraints: - Must be 1 to 16 letters or numbers. - First character must be a letter. - Can't be a reserved word for the chosen database engine. *RDS for MariaDB* Constraints: - Must be 1 to 16 letters or numbers. - Can't be a reserved word for the chosen database engine. *RDS for Microsoft SQL Server* Constraints: - Must be 1 to 128 letters or numbers. - First character must be a letter. - Can't be a reserved word for the chosen database engine. *RDS for MySQL* Constraints: - Must be 1 to 16 letters or numbers. - First character must be a letter. - Can't be a reserved word for the chosen database engine. *RDS for Oracle* Constraints: - Must be 1 to 30 letters or numbers. - First character must be a letter. - Can't be a reserved word for the chosen database engine. *RDS for PostgreSQL* Constraints: - Must be 1 to 63 letters or numbers. - First character must be a letter. - Can't be a reserved word for the chosen database engine.
        :param master_user_password: The password for the master user. The password can include any printable ASCII character except "/", """, or "@". *Amazon Aurora* Not applicable. The password for the master user is managed by the DB cluster. *RDS for Db2* Must contain from 8 to 255 characters. *RDS for MariaDB* Constraints: Must contain from 8 to 41 characters. *RDS for Microsoft SQL Server* Constraints: Must contain from 8 to 128 characters. *RDS for MySQL* Constraints: Must contain from 8 to 41 characters. *RDS for Oracle* Constraints: Must contain from 8 to 30 characters. *RDS for PostgreSQL* Constraints: Must contain from 8 to 128 characters.
        :param master_user_secret: The secret managed by RDS in AWS Secrets Manager for the master user password. For more information, see `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html>`_ in the *Amazon RDS User Guide.*
        :param max_allocated_storage: The upper limit in gibibytes (GiB) to which Amazon RDS can automatically scale the storage of the DB instance. For more information about this setting, including limitations that apply to it, see `Managing capacity automatically with Amazon RDS storage autoscaling <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling>`_ in the *Amazon RDS User Guide* . This setting doesn't apply to the following DB instances: - Amazon Aurora (Storage is managed by the DB cluster.) - RDS Custom
        :param monitoring_interval: The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB instance. To disable collection of Enhanced Monitoring metrics, specify ``0`` . If ``MonitoringRoleArn`` is specified, then you must set ``MonitoringInterval`` to a value other than ``0`` . This setting doesn't apply to RDS Custom DB instances. Valid Values: ``0 | 1 | 5 | 10 | 15 | 30 | 60`` Default: ``0``
        :param monitoring_role_arn: The ARN for the IAM role that permits RDS to send enhanced monitoring metrics to Amazon CloudWatch Logs. For example, ``arn:aws:iam:123456789012:role/emaccess`` . For information on creating a monitoring role, see `Setting Up and Enabling Enhanced Monitoring <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html#USER_Monitoring.OS.Enabling>`_ in the *Amazon RDS User Guide* . If ``MonitoringInterval`` is set to a value other than ``0`` , then you must supply a ``MonitoringRoleArn`` value. This setting doesn't apply to RDS Custom DB instances.
        :param multi_az: Specifies whether the DB instance is a Multi-AZ deployment. You can't set the ``AvailabilityZone`` parameter if the DB instance is a Multi-AZ deployment. This setting doesn't apply to Amazon Aurora because the DB instance Availability Zones (AZs) are managed by the DB cluster.
        :param nchar_character_set_name: The name of the NCHAR character set for the Oracle DB instance. This setting doesn't apply to RDS Custom DB instances.
        :param network_type: The network type of the DB instance. Valid values: - ``IPV4`` - ``DUAL`` The network type is determined by the ``DBSubnetGroup`` specified for the DB instance. A ``DBSubnetGroup`` can support only the IPv4 protocol or the IPv4 and IPv6 protocols ( ``DUAL`` ). For more information, see `Working with a DB instance in a VPC <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html>`_ in the *Amazon RDS User Guide.*
        :param option_group_name: Indicates that the DB instance should be associated with the specified option group. Permanent options, such as the TDE option for Oracle Advanced Security TDE, can't be removed from an option group. Also, that option group can't be removed from a DB instance once it is associated with a DB instance.
        :param performance_insights_kms_key_id: The AWS KMS key identifier for encryption of Performance Insights data. The KMS key identifier is the key ARN, key ID, alias ARN, or alias name for the KMS key. If you do not specify a value for ``PerformanceInsightsKMSKeyId`` , then Amazon RDS uses your default KMS key. There is a default KMS key for your AWS account. Your AWS account has a different default KMS key for each AWS Region. For information about enabling Performance Insights, see `EnablePerformanceInsights <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enableperformanceinsights>`_ .
        :param performance_insights_retention_period: The number of days to retain Performance Insights data. When creating a DB instance without enabling Performance Insights, you can't specify the parameter ``PerformanceInsightsRetentionPeriod`` . This setting doesn't apply to RDS Custom DB instances. Valid Values: - ``7`` - *month* * 31, where *month* is a number of months from 1-23. Examples: ``93`` (3 months * 31), ``341`` (11 months * 31), ``589`` (19 months * 31) - ``731`` Default: ``7`` days If you specify a retention period that isn't valid, such as ``94`` , Amazon RDS returns an error.
        :param port: The port number on which the database accepts connections. This setting doesn't apply to Aurora DB instances. The port number is managed by the cluster. Valid Values: ``1150-65535`` Default: - RDS for Db2 - ``50000`` - RDS for MariaDB - ``3306`` - RDS for Microsoft SQL Server - ``1433`` - RDS for MySQL - ``3306`` - RDS for Oracle - ``1521`` - RDS for PostgreSQL - ``5432`` Constraints: - For RDS for Microsoft SQL Server, the value can't be ``1234`` , ``1434`` , ``3260`` , ``3343`` , ``3389`` , ``47001`` , or ``49152-49156`` .
        :param preferred_backup_window: The daily time range during which automated backups are created if automated backups are enabled, using the ``BackupRetentionPeriod`` parameter. For more information, see `Backup Window <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow>`_ in the *Amazon RDS User Guide.* Constraints: - Must be in the format ``hh24:mi-hh24:mi`` . - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. *Amazon Aurora* Not applicable. The daily time range for creating automated backups is managed by the DB cluster.
        :param preferred_maintenance_window: The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC). Format: ``ddd:hh24:mi-ddd:hh24:mi`` The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see `Maintaining a DB instance <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#AdjustingTheMaintenanceWindow>`_ in the *Amazon RDS User Guide.* .. epigraph:: This property applies when AWS CloudFormation initially creates the DB instance. If you use AWS CloudFormation to update the DB instance, those updates are applied immediately. Constraints: Minimum 30-minute window.
        :param processor_features: The number of CPU cores and the number of threads per core for the DB instance class of the DB instance. This setting doesn't apply to Amazon Aurora or RDS Custom DB instances.
        :param promotion_tier: The order of priority in which an Aurora Replica is promoted to the primary instance after a failure of the existing primary instance. For more information, see `Fault Tolerance for an Aurora DB Cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraHighAvailability.html#Aurora.Managing.FaultTolerance>`_ in the *Amazon Aurora User Guide* . This setting doesn't apply to RDS Custom DB instances. Default: ``1`` Valid Values: ``0 - 15``
        :param publicly_accessible: Indicates whether the DB instance is an internet-facing instance. If you specify true, AWS CloudFormation creates an instance with a publicly resolvable DNS name, which resolves to a public IP address. If you specify false, AWS CloudFormation creates an internal instance with a DNS name that resolves to a private IP address. The default behavior value depends on your VPC setup and the database subnet group. For more information, see the ``PubliclyAccessible`` parameter in the `CreateDBInstance <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_CreateDBInstance.html>`_ in the *Amazon RDS API Reference* .
        :param replica_mode: The open mode of an Oracle read replica. For more information, see `Working with Oracle Read Replicas for Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/oracle-read-replicas.html>`_ in the *Amazon RDS User Guide* . This setting is only supported in RDS for Oracle. Default: ``open-read-only`` Valid Values: ``open-read-only`` or ``mounted``
        :param restore_time: The date and time to restore from. This parameter applies to point-in-time recovery. For more information, see `Restoring a DB instance to a specified time <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html>`_ in the in the *Amazon RDS User Guide* . Constraints: - Must be a time in Universal Coordinated Time (UTC) format. - Must be before the latest restorable time for the DB instance. - Can't be specified if the ``UseLatestRestorableTime`` parameter is enabled. Example: ``2009-09-07T23:45:00Z``
        :param source_db_cluster_identifier: The identifier of the Multi-AZ DB cluster that will act as the source for the read replica. Each DB cluster can have up to 15 read replicas. Constraints: - Must be the identifier of an existing Multi-AZ DB cluster. - Can't be specified if the ``SourceDBInstanceIdentifier`` parameter is also specified. - The specified DB cluster must have automatic backups enabled, that is, its backup retention period must be greater than 0. - The source DB cluster must be in the same AWS Region as the read replica. Cross-Region replication isn't supported.
        :param source_db_instance_automated_backups_arn: The Amazon Resource Name (ARN) of the replicated automated backups from which to restore, for example, ``arn:aws:rds:us-east-1:123456789012:auto-backup:ab-L2IJCEXJP7XQ7HOJ4SIEXAMPLE`` . This setting doesn't apply to RDS Custom.
        :param source_db_instance_identifier: If you want to create a read replica DB instance, specify the ID of the source DB instance. Each DB instance can have a limited number of read replicas. For more information, see `Working with Read Replicas <https://docs.aws.amazon.com/AmazonRDS/latest/DeveloperGuide/USER_ReadRepl.html>`_ in the *Amazon RDS User Guide* . For information about constraints that apply to DB instance identifiers, see `Naming constraints in Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html#RDS_Limits.Constraints>`_ in the *Amazon RDS User Guide* . The ``SourceDBInstanceIdentifier`` property determines whether a DB instance is a read replica. If you remove the ``SourceDBInstanceIdentifier`` property from your template and then update your stack, AWS CloudFormation promotes the read replica to a standalone DB instance. If you specify the ``UseLatestRestorableTime`` or ``RestoreTime`` properties in conjunction with the ``SourceDBInstanceIdentifier`` property, RDS restores the DB instance to the requested point in time, thereby creating a new DB instance. .. epigraph:: - If you specify a source DB instance that uses VPC security groups, we recommend that you specify the ``VPCSecurityGroups`` property. If you don't specify the property, the read replica inherits the value of the ``VPCSecurityGroups`` property from the source DB when you create the replica. However, if you update the stack, AWS CloudFormation reverts the replica's ``VPCSecurityGroups`` property to the default value because it's not defined in the stack's template. This change might cause unexpected issues. - Read replicas don't support deletion policies. AWS CloudFormation ignores any deletion policy that's associated with a read replica. - If you specify ``SourceDBInstanceIdentifier`` , don't specify the ``DBSnapshotIdentifier`` property. You can't create a read replica from a snapshot. - Don't set the ``BackupRetentionPeriod`` , ``DBName`` , ``MasterUsername`` , ``MasterUserPassword`` , and ``PreferredBackupWindow`` properties. The database attributes are inherited from the source DB instance, and backups are disabled for read replicas. - If the source DB instance is in a different region than the read replica, specify the source region in ``SourceRegion`` , and specify an ARN for a valid DB instance in ``SourceDBInstanceIdentifier`` . For more information, see `Constructing a Amazon RDS Amazon Resource Name (ARN) <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html#USER_Tagging.ARN>`_ in the *Amazon RDS User Guide* . - For DB instances in Amazon Aurora clusters, don't specify this property. Amazon RDS automatically assigns writer and reader DB instances.
        :param source_dbi_resource_id: The resource ID of the source DB instance from which to restore.
        :param source_region: The ID of the region that contains the source DB instance for the read replica.
        :param storage_encrypted: A value that indicates whether the DB instance is encrypted. By default, it isn't encrypted. If you specify the ``KmsKeyId`` property, then you must enable encryption. If you specify the ``SourceDBInstanceIdentifier`` or ``SourceDbiResourceId`` property, don't specify this property. The value is inherited from the source DB instance, and if the DB instance is encrypted, the specified ``KmsKeyId`` property is used. If you specify the ``SourceDBInstanceAutomatedBackupsArn`` property, don't specify this property. The value is inherited from the source DB instance automated backup. If you specify ``DBSnapshotIdentifier`` property, don't specify this property. The value is inherited from the snapshot. *Amazon Aurora* Not applicable. The encryption for DB instances is managed by the DB cluster.
        :param storage_throughput: Specifies the storage throughput value, in mebibyte per second (MiBps), for the DB instance. This setting applies only to the ``gp3`` storage type. This setting doesn't apply to RDS Custom or Amazon Aurora.
        :param storage_type: The storage type to associate with the DB instance. If you specify ``io1`` , ``io2`` , or ``gp3`` , you must also include a value for the ``Iops`` parameter. This setting doesn't apply to Amazon Aurora DB instances. Storage is managed by the DB cluster. Valid Values: ``gp2 | gp3 | io1 | io2 | standard`` Default: ``io1`` , if the ``Iops`` parameter is specified. Otherwise, ``gp3`` .
        :param tags: Tags to assign to the DB instance.
        :param tde_credential_arn: 
        :param tde_credential_password: 
        :param timezone: The time zone of the DB instance. The time zone parameter is currently supported only by `RDS for Db2 <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/db2-time-zone>`_ and `RDS for SQL Server <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_SQLServer.html#SQLServer.Concepts.General.TimeZone>`_ .
        :param use_default_processor_features: Specifies whether the DB instance class of the DB instance uses its default processor features. This setting doesn't apply to RDS Custom DB instances.
        :param use_latest_restorable_time: Specifies whether the DB instance is restored from the latest backup time. By default, the DB instance isn't restored from the latest backup time. This parameter applies to point-in-time recovery. For more information, see `Restoring a DB instance to a specified time <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html>`_ in the in the *Amazon RDS User Guide* . Constraints: - Can't be specified if the ``RestoreTime`` parameter is provided.
        :param vpc_security_groups: A list of the VPC security group IDs to assign to the DB instance. The list can include both the physical IDs of existing VPC security groups and references to `AWS::EC2::SecurityGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html>`_ resources created in the template. If you plan to update the resource, don't specify VPC security groups in a shared VPC. If you set ``VPCSecurityGroups`` , you must not set ```DBSecurityGroups`` <https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsecuritygroups>`_ , and vice versa. .. epigraph:: You can migrate a DB instance in your stack from an RDS DB security group to a VPC security group, but keep the following in mind: - You can't revert to using an RDS security group after you establish a VPC security group membership. - When you migrate your DB instance to VPC security groups, if your stack update rolls back because the DB instance update fails or because an update fails in another AWS CloudFormation resource, the rollback fails because it can't revert to an RDS security group. - To use the properties that are available when you use a VPC security group, you must recreate the DB instance. If you don't, AWS CloudFormation submits only the property values that are listed in the ```DBSecurityGroups`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsecuritygroups>`_ property. To avoid this situation, migrate your DB instance to using VPC security groups only when that is the only change in your stack template. *Amazon Aurora* Not applicable. The associated list of EC2 VPC security groups is managed by the DB cluster. If specified, the setting must match the DB cluster setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_dBInstance_mixin_props = rds_mixins.CfnDBInstanceMixinProps(
                allocated_storage="allocatedStorage",
                allow_major_version_upgrade=False,
                apply_immediately=False,
                associated_roles=[rds_mixins.CfnDBInstancePropsMixin.DBInstanceRoleProperty(
                    feature_name="featureName",
                    role_arn="roleArn"
                )],
                automatic_backup_replication_kms_key_id="automaticBackupReplicationKmsKeyId",
                automatic_backup_replication_region="automaticBackupReplicationRegion",
                automatic_backup_replication_retention_period=123,
                auto_minor_version_upgrade=False,
                availability_zone="availabilityZone",
                backup_retention_period=123,
                backup_target="backupTarget",
                ca_certificate_identifier="caCertificateIdentifier",
                certificate_rotation_restart=False,
                character_set_name="characterSetName",
                copy_tags_to_snapshot=False,
                custom_iam_instance_profile="customIamInstanceProfile",
                database_insights_mode="databaseInsightsMode",
                db_cluster_identifier="dbClusterIdentifier",
                db_cluster_snapshot_identifier="dbClusterSnapshotIdentifier",
                db_instance_class="dbInstanceClass",
                db_instance_identifier="dbInstanceIdentifier",
                db_name="dbName",
                db_parameter_group_name="dbParameterGroupName",
                db_security_groups=["dbSecurityGroups"],
                db_snapshot_identifier="dbSnapshotIdentifier",
                db_subnet_group_name="dbSubnetGroupName",
                db_system_id="dbSystemId",
                dedicated_log_volume=False,
                delete_automated_backups=False,
                deletion_protection=False,
                domain="domain",
                domain_auth_secret_arn="domainAuthSecretArn",
                domain_dns_ips=["domainDnsIps"],
                domain_fqdn="domainFqdn",
                domain_iam_role_name="domainIamRoleName",
                domain_ou="domainOu",
                enable_cloudwatch_logs_exports=["enableCloudwatchLogsExports"],
                enable_iam_database_authentication=False,
                enable_performance_insights=False,
                engine="engine",
                engine_lifecycle_support="engineLifecycleSupport",
                engine_version="engineVersion",
                iops=123,
                kms_key_id="kmsKeyId",
                license_model="licenseModel",
                manage_master_user_password=False,
                master_user_authentication_type="masterUserAuthenticationType",
                master_username="masterUsername",
                master_user_password="masterUserPassword",
                master_user_secret=rds_mixins.CfnDBInstancePropsMixin.MasterUserSecretProperty(
                    kms_key_id="kmsKeyId",
                    secret_arn="secretArn"
                ),
                max_allocated_storage=123,
                monitoring_interval=123,
                monitoring_role_arn="monitoringRoleArn",
                multi_az=False,
                nchar_character_set_name="ncharCharacterSetName",
                network_type="networkType",
                option_group_name="optionGroupName",
                performance_insights_kms_key_id="performanceInsightsKmsKeyId",
                performance_insights_retention_period=123,
                port="port",
                preferred_backup_window="preferredBackupWindow",
                preferred_maintenance_window="preferredMaintenanceWindow",
                processor_features=[rds_mixins.CfnDBInstancePropsMixin.ProcessorFeatureProperty(
                    name="name",
                    value="value"
                )],
                promotion_tier=123,
                publicly_accessible=False,
                replica_mode="replicaMode",
                restore_time="restoreTime",
                source_db_cluster_identifier="sourceDbClusterIdentifier",
                source_db_instance_automated_backups_arn="sourceDbInstanceAutomatedBackupsArn",
                source_db_instance_identifier="sourceDbInstanceIdentifier",
                source_dbi_resource_id="sourceDbiResourceId",
                source_region="sourceRegion",
                storage_encrypted=False,
                storage_throughput=123,
                storage_type="storageType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tde_credential_arn="tdeCredentialArn",
                tde_credential_password="tdeCredentialPassword",
                timezone="timezone",
                use_default_processor_features=False,
                use_latest_restorable_time=False,
                vpc_security_groups=["vpcSecurityGroups"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6f1c64298fe52c0293ad649a7a349d80ad2a01120798ffc49e70d693e422db)
            check_type(argname="argument allocated_storage", value=allocated_storage, expected_type=type_hints["allocated_storage"])
            check_type(argname="argument allow_major_version_upgrade", value=allow_major_version_upgrade, expected_type=type_hints["allow_major_version_upgrade"])
            check_type(argname="argument apply_immediately", value=apply_immediately, expected_type=type_hints["apply_immediately"])
            check_type(argname="argument associated_roles", value=associated_roles, expected_type=type_hints["associated_roles"])
            check_type(argname="argument automatic_backup_replication_kms_key_id", value=automatic_backup_replication_kms_key_id, expected_type=type_hints["automatic_backup_replication_kms_key_id"])
            check_type(argname="argument automatic_backup_replication_region", value=automatic_backup_replication_region, expected_type=type_hints["automatic_backup_replication_region"])
            check_type(argname="argument automatic_backup_replication_retention_period", value=automatic_backup_replication_retention_period, expected_type=type_hints["automatic_backup_replication_retention_period"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument backup_retention_period", value=backup_retention_period, expected_type=type_hints["backup_retention_period"])
            check_type(argname="argument backup_target", value=backup_target, expected_type=type_hints["backup_target"])
            check_type(argname="argument ca_certificate_identifier", value=ca_certificate_identifier, expected_type=type_hints["ca_certificate_identifier"])
            check_type(argname="argument certificate_rotation_restart", value=certificate_rotation_restart, expected_type=type_hints["certificate_rotation_restart"])
            check_type(argname="argument character_set_name", value=character_set_name, expected_type=type_hints["character_set_name"])
            check_type(argname="argument copy_tags_to_snapshot", value=copy_tags_to_snapshot, expected_type=type_hints["copy_tags_to_snapshot"])
            check_type(argname="argument custom_iam_instance_profile", value=custom_iam_instance_profile, expected_type=type_hints["custom_iam_instance_profile"])
            check_type(argname="argument database_insights_mode", value=database_insights_mode, expected_type=type_hints["database_insights_mode"])
            check_type(argname="argument db_cluster_identifier", value=db_cluster_identifier, expected_type=type_hints["db_cluster_identifier"])
            check_type(argname="argument db_cluster_snapshot_identifier", value=db_cluster_snapshot_identifier, expected_type=type_hints["db_cluster_snapshot_identifier"])
            check_type(argname="argument db_instance_class", value=db_instance_class, expected_type=type_hints["db_instance_class"])
            check_type(argname="argument db_instance_identifier", value=db_instance_identifier, expected_type=type_hints["db_instance_identifier"])
            check_type(argname="argument db_name", value=db_name, expected_type=type_hints["db_name"])
            check_type(argname="argument db_parameter_group_name", value=db_parameter_group_name, expected_type=type_hints["db_parameter_group_name"])
            check_type(argname="argument db_security_groups", value=db_security_groups, expected_type=type_hints["db_security_groups"])
            check_type(argname="argument db_snapshot_identifier", value=db_snapshot_identifier, expected_type=type_hints["db_snapshot_identifier"])
            check_type(argname="argument db_subnet_group_name", value=db_subnet_group_name, expected_type=type_hints["db_subnet_group_name"])
            check_type(argname="argument db_system_id", value=db_system_id, expected_type=type_hints["db_system_id"])
            check_type(argname="argument dedicated_log_volume", value=dedicated_log_volume, expected_type=type_hints["dedicated_log_volume"])
            check_type(argname="argument delete_automated_backups", value=delete_automated_backups, expected_type=type_hints["delete_automated_backups"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument domain_auth_secret_arn", value=domain_auth_secret_arn, expected_type=type_hints["domain_auth_secret_arn"])
            check_type(argname="argument domain_dns_ips", value=domain_dns_ips, expected_type=type_hints["domain_dns_ips"])
            check_type(argname="argument domain_fqdn", value=domain_fqdn, expected_type=type_hints["domain_fqdn"])
            check_type(argname="argument domain_iam_role_name", value=domain_iam_role_name, expected_type=type_hints["domain_iam_role_name"])
            check_type(argname="argument domain_ou", value=domain_ou, expected_type=type_hints["domain_ou"])
            check_type(argname="argument enable_cloudwatch_logs_exports", value=enable_cloudwatch_logs_exports, expected_type=type_hints["enable_cloudwatch_logs_exports"])
            check_type(argname="argument enable_iam_database_authentication", value=enable_iam_database_authentication, expected_type=type_hints["enable_iam_database_authentication"])
            check_type(argname="argument enable_performance_insights", value=enable_performance_insights, expected_type=type_hints["enable_performance_insights"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_lifecycle_support", value=engine_lifecycle_support, expected_type=type_hints["engine_lifecycle_support"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument manage_master_user_password", value=manage_master_user_password, expected_type=type_hints["manage_master_user_password"])
            check_type(argname="argument master_user_authentication_type", value=master_user_authentication_type, expected_type=type_hints["master_user_authentication_type"])
            check_type(argname="argument master_username", value=master_username, expected_type=type_hints["master_username"])
            check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
            check_type(argname="argument master_user_secret", value=master_user_secret, expected_type=type_hints["master_user_secret"])
            check_type(argname="argument max_allocated_storage", value=max_allocated_storage, expected_type=type_hints["max_allocated_storage"])
            check_type(argname="argument monitoring_interval", value=monitoring_interval, expected_type=type_hints["monitoring_interval"])
            check_type(argname="argument monitoring_role_arn", value=monitoring_role_arn, expected_type=type_hints["monitoring_role_arn"])
            check_type(argname="argument multi_az", value=multi_az, expected_type=type_hints["multi_az"])
            check_type(argname="argument nchar_character_set_name", value=nchar_character_set_name, expected_type=type_hints["nchar_character_set_name"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument option_group_name", value=option_group_name, expected_type=type_hints["option_group_name"])
            check_type(argname="argument performance_insights_kms_key_id", value=performance_insights_kms_key_id, expected_type=type_hints["performance_insights_kms_key_id"])
            check_type(argname="argument performance_insights_retention_period", value=performance_insights_retention_period, expected_type=type_hints["performance_insights_retention_period"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_backup_window", value=preferred_backup_window, expected_type=type_hints["preferred_backup_window"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument processor_features", value=processor_features, expected_type=type_hints["processor_features"])
            check_type(argname="argument promotion_tier", value=promotion_tier, expected_type=type_hints["promotion_tier"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument replica_mode", value=replica_mode, expected_type=type_hints["replica_mode"])
            check_type(argname="argument restore_time", value=restore_time, expected_type=type_hints["restore_time"])
            check_type(argname="argument source_db_cluster_identifier", value=source_db_cluster_identifier, expected_type=type_hints["source_db_cluster_identifier"])
            check_type(argname="argument source_db_instance_automated_backups_arn", value=source_db_instance_automated_backups_arn, expected_type=type_hints["source_db_instance_automated_backups_arn"])
            check_type(argname="argument source_db_instance_identifier", value=source_db_instance_identifier, expected_type=type_hints["source_db_instance_identifier"])
            check_type(argname="argument source_dbi_resource_id", value=source_dbi_resource_id, expected_type=type_hints["source_dbi_resource_id"])
            check_type(argname="argument source_region", value=source_region, expected_type=type_hints["source_region"])
            check_type(argname="argument storage_encrypted", value=storage_encrypted, expected_type=type_hints["storage_encrypted"])
            check_type(argname="argument storage_throughput", value=storage_throughput, expected_type=type_hints["storage_throughput"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tde_credential_arn", value=tde_credential_arn, expected_type=type_hints["tde_credential_arn"])
            check_type(argname="argument tde_credential_password", value=tde_credential_password, expected_type=type_hints["tde_credential_password"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument use_default_processor_features", value=use_default_processor_features, expected_type=type_hints["use_default_processor_features"])
            check_type(argname="argument use_latest_restorable_time", value=use_latest_restorable_time, expected_type=type_hints["use_latest_restorable_time"])
            check_type(argname="argument vpc_security_groups", value=vpc_security_groups, expected_type=type_hints["vpc_security_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if allow_major_version_upgrade is not None:
            self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if apply_immediately is not None:
            self._values["apply_immediately"] = apply_immediately
        if associated_roles is not None:
            self._values["associated_roles"] = associated_roles
        if automatic_backup_replication_kms_key_id is not None:
            self._values["automatic_backup_replication_kms_key_id"] = automatic_backup_replication_kms_key_id
        if automatic_backup_replication_region is not None:
            self._values["automatic_backup_replication_region"] = automatic_backup_replication_region
        if automatic_backup_replication_retention_period is not None:
            self._values["automatic_backup_replication_retention_period"] = automatic_backup_replication_retention_period
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_retention_period is not None:
            self._values["backup_retention_period"] = backup_retention_period
        if backup_target is not None:
            self._values["backup_target"] = backup_target
        if ca_certificate_identifier is not None:
            self._values["ca_certificate_identifier"] = ca_certificate_identifier
        if certificate_rotation_restart is not None:
            self._values["certificate_rotation_restart"] = certificate_rotation_restart
        if character_set_name is not None:
            self._values["character_set_name"] = character_set_name
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if custom_iam_instance_profile is not None:
            self._values["custom_iam_instance_profile"] = custom_iam_instance_profile
        if database_insights_mode is not None:
            self._values["database_insights_mode"] = database_insights_mode
        if db_cluster_identifier is not None:
            self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_cluster_snapshot_identifier is not None:
            self._values["db_cluster_snapshot_identifier"] = db_cluster_snapshot_identifier
        if db_instance_class is not None:
            self._values["db_instance_class"] = db_instance_class
        if db_instance_identifier is not None:
            self._values["db_instance_identifier"] = db_instance_identifier
        if db_name is not None:
            self._values["db_name"] = db_name
        if db_parameter_group_name is not None:
            self._values["db_parameter_group_name"] = db_parameter_group_name
        if db_security_groups is not None:
            self._values["db_security_groups"] = db_security_groups
        if db_snapshot_identifier is not None:
            self._values["db_snapshot_identifier"] = db_snapshot_identifier
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if db_system_id is not None:
            self._values["db_system_id"] = db_system_id
        if dedicated_log_volume is not None:
            self._values["dedicated_log_volume"] = dedicated_log_volume
        if delete_automated_backups is not None:
            self._values["delete_automated_backups"] = delete_automated_backups
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if domain is not None:
            self._values["domain"] = domain
        if domain_auth_secret_arn is not None:
            self._values["domain_auth_secret_arn"] = domain_auth_secret_arn
        if domain_dns_ips is not None:
            self._values["domain_dns_ips"] = domain_dns_ips
        if domain_fqdn is not None:
            self._values["domain_fqdn"] = domain_fqdn
        if domain_iam_role_name is not None:
            self._values["domain_iam_role_name"] = domain_iam_role_name
        if domain_ou is not None:
            self._values["domain_ou"] = domain_ou
        if enable_cloudwatch_logs_exports is not None:
            self._values["enable_cloudwatch_logs_exports"] = enable_cloudwatch_logs_exports
        if enable_iam_database_authentication is not None:
            self._values["enable_iam_database_authentication"] = enable_iam_database_authentication
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if engine is not None:
            self._values["engine"] = engine
        if engine_lifecycle_support is not None:
            self._values["engine_lifecycle_support"] = engine_lifecycle_support
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if iops is not None:
            self._values["iops"] = iops
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if license_model is not None:
            self._values["license_model"] = license_model
        if manage_master_user_password is not None:
            self._values["manage_master_user_password"] = manage_master_user_password
        if master_user_authentication_type is not None:
            self._values["master_user_authentication_type"] = master_user_authentication_type
        if master_username is not None:
            self._values["master_username"] = master_username
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password
        if master_user_secret is not None:
            self._values["master_user_secret"] = master_user_secret
        if max_allocated_storage is not None:
            self._values["max_allocated_storage"] = max_allocated_storage
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role_arn is not None:
            self._values["monitoring_role_arn"] = monitoring_role_arn
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if nchar_character_set_name is not None:
            self._values["nchar_character_set_name"] = nchar_character_set_name
        if network_type is not None:
            self._values["network_type"] = network_type
        if option_group_name is not None:
            self._values["option_group_name"] = option_group_name
        if performance_insights_kms_key_id is not None:
            self._values["performance_insights_kms_key_id"] = performance_insights_kms_key_id
        if performance_insights_retention_period is not None:
            self._values["performance_insights_retention_period"] = performance_insights_retention_period
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if processor_features is not None:
            self._values["processor_features"] = processor_features
        if promotion_tier is not None:
            self._values["promotion_tier"] = promotion_tier
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if replica_mode is not None:
            self._values["replica_mode"] = replica_mode
        if restore_time is not None:
            self._values["restore_time"] = restore_time
        if source_db_cluster_identifier is not None:
            self._values["source_db_cluster_identifier"] = source_db_cluster_identifier
        if source_db_instance_automated_backups_arn is not None:
            self._values["source_db_instance_automated_backups_arn"] = source_db_instance_automated_backups_arn
        if source_db_instance_identifier is not None:
            self._values["source_db_instance_identifier"] = source_db_instance_identifier
        if source_dbi_resource_id is not None:
            self._values["source_dbi_resource_id"] = source_dbi_resource_id
        if source_region is not None:
            self._values["source_region"] = source_region
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if storage_throughput is not None:
            self._values["storage_throughput"] = storage_throughput
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if tags is not None:
            self._values["tags"] = tags
        if tde_credential_arn is not None:
            self._values["tde_credential_arn"] = tde_credential_arn
        if tde_credential_password is not None:
            self._values["tde_credential_password"] = tde_credential_password
        if timezone is not None:
            self._values["timezone"] = timezone
        if use_default_processor_features is not None:
            self._values["use_default_processor_features"] = use_default_processor_features
        if use_latest_restorable_time is not None:
            self._values["use_latest_restorable_time"] = use_latest_restorable_time
        if vpc_security_groups is not None:
            self._values["vpc_security_groups"] = vpc_security_groups

    @builtins.property
    def allocated_storage(self) -> typing.Optional[builtins.str]:
        '''The amount of storage in gibibytes (GiB) to be initially allocated for the database instance.

        .. epigraph::

           If any value is set in the ``Iops`` parameter, ``AllocatedStorage`` must be at least 100 GiB, which corresponds to the minimum Iops value of 1,000. If you increase the ``Iops`` value (in 1,000 IOPS increments), then you must also increase the ``AllocatedStorage`` value (in 100-GiB increments).

        *Amazon Aurora*

        Not applicable. Aurora cluster volumes automatically grow as the amount of data in your database increases, though you are only charged for the space that you use in an Aurora cluster volume.

        *Db2*

        Constraints to the amount of storage for each storage type are the following:

        - General Purpose (SSD) storage (gp3): Must be an integer from 20 to 64000.
        - Provisioned IOPS storage (io1): Must be an integer from 100 to 64000.

        *MySQL*

        Constraints to the amount of storage for each storage type are the following:

        - General Purpose (SSD) storage (gp2): Must be an integer from 20 to 65536.
        - Provisioned IOPS storage (io1): Must be an integer from 100 to 65536.
        - Magnetic storage (standard): Must be an integer from 5 to 3072.

        *MariaDB*

        Constraints to the amount of storage for each storage type are the following:

        - General Purpose (SSD) storage (gp2): Must be an integer from 20 to 65536.
        - Provisioned IOPS storage (io1): Must be an integer from 100 to 65536.
        - Magnetic storage (standard): Must be an integer from 5 to 3072.

        *PostgreSQL*

        Constraints to the amount of storage for each storage type are the following:

        - General Purpose (SSD) storage (gp2): Must be an integer from 20 to 65536.
        - Provisioned IOPS storage (io1): Must be an integer from 100 to 65536.
        - Magnetic storage (standard): Must be an integer from 5 to 3072.

        *Oracle*

        Constraints to the amount of storage for each storage type are the following:

        - General Purpose (SSD) storage (gp2): Must be an integer from 20 to 65536.
        - Provisioned IOPS storage (io1): Must be an integer from 100 to 65536.
        - Magnetic storage (standard): Must be an integer from 10 to 3072.

        *SQL Server*

        Constraints to the amount of storage for each storage type are the following:

        - General Purpose (SSD) storage (gp2):
        - Enterprise and Standard editions: Must be an integer from 20 to 16384.
        - Web and Express editions: Must be an integer from 20 to 16384.
        - Provisioned IOPS storage (io1):
        - Enterprise and Standard editions: Must be an integer from 20 to 16384.
        - Web and Express editions: Must be an integer from 20 to 16384.
        - Magnetic storage (standard):
        - Enterprise and Standard editions: Must be an integer from 20 to 1024.
        - Web and Express editions: Must be an integer from 20 to 1024.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-allocatedstorage
        '''
        result = self._values.get("allocated_storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_major_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether major version upgrades are allowed.

        Changing this parameter doesn't result in an outage and the change is asynchronously applied as soon as possible.

        Constraints: Major version upgrades must be allowed when specifying a value for the ``EngineVersion`` parameter that is a different major version than the DB instance's current version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-allowmajorversionupgrade
        '''
        result = self._values.get("allow_major_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def apply_immediately(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether changes to the DB instance and any pending modifications are applied immediately, regardless of the ``PreferredMaintenanceWindow`` setting.

        If set to ``false`` , changes are applied during the next maintenance window. Until RDS applies the changes, the DB instance remains in a drift state. As a result, the configuration doesn't fully reflect the requested modifications and temporarily diverges from the intended state.

        In addition to the settings described in `Modifying a DB instance <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.DBInstance.Modifying.html>`_ , this property also determines whether the DB instance reboots when a static parameter is modified in the associated DB parameter group.

        Default: ``true``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-applyimmediately
        '''
        result = self._values.get("apply_immediately")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def associated_roles(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBInstancePropsMixin.DBInstanceRoleProperty"]]]]:
        '''The AWS Identity and Access Management (IAM) roles associated with the DB instance.

        *Amazon Aurora*

        Not applicable. The associated roles are managed by the DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-associatedroles
        '''
        result = self._values.get("associated_roles")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBInstancePropsMixin.DBInstanceRoleProperty"]]]], result)

    @builtins.property
    def automatic_backup_replication_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS KMS key identifier for encryption of the replicated automated backups.

        The KMS key ID is the Amazon Resource Name (ARN) for the KMS encryption key in the destination AWS Region , for example, ``arn:aws:kms:us-east-1:123456789012:key/AKIAIOSFODNN7EXAMPLE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-automaticbackupreplicationkmskeyid
        '''
        result = self._values.get("automatic_backup_replication_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automatic_backup_replication_region(self) -> typing.Optional[builtins.str]:
        '''The AWS Region associated with the automated backup.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-automaticbackupreplicationregion
        '''
        result = self._values.get("automatic_backup_replication_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automatic_backup_replication_retention_period(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''The retention period for automated backups in a different AWS Region.

        Use this parameter to set a unique retention period that only applies to cross-Region automated backups. To enable automated backups in a different Region, specify a positive value for the ``AutomaticBackupReplicationRegion`` parameter.

        If not specified, this parameter defaults to the value of the ``BackupRetentionPeriod`` parameter. The maximum allowed value is 35.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-automaticbackupreplicationretentionperiod
        '''
        result = self._values.get("automatic_backup_replication_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether minor engine upgrades are applied automatically to the DB instance during the maintenance window.

        By default, minor engine upgrades are applied automatically.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone (AZ) where the database will be created.

        For information on AWS Regions and Availability Zones, see `Regions and Availability Zones <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html>`_ .

        For Amazon Aurora, each Aurora DB cluster hosts copies of its storage in three separate Availability Zones. Specify one of these Availability Zones. Aurora automatically chooses an appropriate Availability Zone if you don't specify one.

        Default: A random, system-chosen Availability Zone in the endpoint's AWS Region .

        Constraints:

        - The ``AvailabilityZone`` parameter can't be specified if the DB instance is a Multi-AZ deployment.
        - The specified Availability Zone must be in the same AWS Region as the current endpoint.

        Example: ``us-east-1d``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which automated backups are retained.

        Setting this parameter to a positive number enables backups. Setting this parameter to 0 disables automated backups.

        *Amazon Aurora*

        Not applicable. The retention period for automated backups is managed by the DB cluster.

        Default: 1

        Constraints:

        - Must be a value from 0 to 35
        - Can't be set to 0 if the DB instance is a source to read replicas

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-backupretentionperiod
        '''
        result = self._values.get("backup_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backup_target(self) -> typing.Optional[builtins.str]:
        '''The location for storing automated backups and manual snapshots.

        Valid Values:

        - ``local`` (Dedicated Local Zone)
        - ``outposts`` ( AWS Outposts)
        - ``region`` ( AWS Region )

        Default: ``region``

        For more information, see `Working with Amazon RDS on AWS Outposts <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-on-outposts.html>`_ in the *Amazon RDS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-backuptarget
        '''
        result = self._values.get("backup_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_certificate_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the CA certificate for this DB instance.

        For more information, see `Using SSL/TLS to encrypt a connection to a DB instance <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html>`_ in the *Amazon RDS User Guide* and `Using SSL/TLS to encrypt a connection to a DB cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL.html>`_ in the *Amazon Aurora User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-cacertificateidentifier
        '''
        result = self._values.get("ca_certificate_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_rotation_restart(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the DB instance is restarted when you rotate your SSL/TLS certificate.

        By default, the DB instance is restarted when you rotate your SSL/TLS certificate. The certificate is not updated until the DB instance is restarted.
        .. epigraph::

           Set this parameter only if you are *not* using SSL/TLS to connect to the DB instance.

        If you are using SSL/TLS to connect to the DB instance, follow the appropriate instructions for your DB engine to rotate your SSL/TLS certificate:

        - For more information about rotating your SSL/TLS certificate for RDS DB engines, see `Rotating Your SSL/TLS Certificate. <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL-certificate-rotation.html>`_ in the *Amazon RDS User Guide.*
        - For more information about rotating your SSL/TLS certificate for Aurora DB engines, see `Rotating Your SSL/TLS Certificate <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL-certificate-rotation.html>`_ in the *Amazon Aurora User Guide* .

        This setting doesn't apply to RDS Custom DB instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-certificaterotationrestart
        '''
        result = self._values.get("certificate_rotation_restart")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def character_set_name(self) -> typing.Optional[builtins.str]:
        '''For supported engines, indicates that the DB instance should be associated with the specified character set.

        *Amazon Aurora*

        Not applicable. The character set is managed by the DB cluster. For more information, see `AWS::RDS::DBCluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-charactersetname
        '''
        result = self._values.get("character_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_tags_to_snapshot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to copy tags from the DB instance to snapshots of the DB instance.

        By default, tags are not copied.

        This setting doesn't apply to Amazon Aurora DB instances. Copying tags to snapshots is managed by the DB cluster. Setting this value for an Aurora DB instance has no effect on the DB cluster setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-copytagstosnapshot
        '''
        result = self._values.get("copy_tags_to_snapshot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def custom_iam_instance_profile(self) -> typing.Optional[builtins.str]:
        '''The instance profile associated with the underlying Amazon EC2 instance of an RDS Custom DB instance.

        This setting is required for RDS Custom.

        Constraints:

        - The profile must exist in your account.
        - The profile must have an IAM role that Amazon EC2 has permissions to assume.
        - The instance profile name and the associated IAM role name must start with the prefix ``AWSRDSCustom`` .

        For the list of permissions required for the IAM role, see `Configure IAM and your VPC <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-setup-orcl.html#custom-setup-orcl.iam-vpc>`_ in the *Amazon RDS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-customiaminstanceprofile
        '''
        result = self._values.get("custom_iam_instance_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_insights_mode(self) -> typing.Optional[builtins.str]:
        '''The mode of Database Insights to enable for the DB instance.

        .. epigraph::

           Aurora DB instances inherit this value from the DB cluster, so you can't change this value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-databaseinsightsmode
        '''
        result = self._values.get("database_insights_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the DB cluster that this DB instance will belong to.

        This setting doesn't apply to RDS Custom DB instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dbclusteridentifier
        '''
        result = self._values.get("db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_cluster_snapshot_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier for the Multi-AZ DB cluster snapshot to restore from.

        For more information on Multi-AZ DB clusters, see `Multi-AZ DB cluster deployments <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts.html>`_ in the *Amazon RDS User Guide* .

        Constraints:

        - Must match the identifier of an existing Multi-AZ DB cluster snapshot.
        - Can't be specified when ``DBSnapshotIdentifier`` is specified.
        - Must be specified when ``DBSnapshotIdentifier`` isn't specified.
        - If you are restoring from a shared manual Multi-AZ DB cluster snapshot, the ``DBClusterSnapshotIdentifier`` must be the ARN of the shared snapshot.
        - Can't be the identifier of an Aurora DB cluster snapshot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dbclustersnapshotidentifier
        '''
        result = self._values.get("db_cluster_snapshot_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_instance_class(self) -> typing.Optional[builtins.str]:
        '''The compute and memory capacity of the DB instance, for example ``db.m5.large`` . Not all DB instance classes are available in all AWS Regions , or for all database engines. For the full list of DB instance classes, and availability for your engine, see `DB instance classes <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html>`_ in the *Amazon RDS User Guide* or `Aurora DB instance classes <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.DBInstanceClass.html>`_ in the *Amazon Aurora User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dbinstanceclass
        '''
        result = self._values.get("db_instance_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_instance_identifier(self) -> typing.Optional[builtins.str]:
        '''A name for the DB instance.

        If you specify a name, AWS CloudFormation converts it to lowercase. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the DB instance. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        For information about constraints that apply to DB instance identifiers, see `Naming constraints in Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html#RDS_Limits.Constraints>`_ in the *Amazon RDS User Guide* .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dbinstanceidentifier
        '''
        result = self._values.get("db_instance_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_name(self) -> typing.Optional[builtins.str]:
        '''The meaning of this parameter differs according to the database engine you use.

        .. epigraph::

           If you specify the ``[DBSnapshotIdentifier](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsnapshotidentifier)`` property, this property only applies to RDS for Oracle.

        *Amazon Aurora*

        Not applicable. The database name is managed by the DB cluster.

        *Db2*

        The name of the database to create when the DB instance is created. If this parameter isn't specified, no database is created in the DB instance.

        Constraints:

        - Must contain 1 to 64 letters or numbers.
        - Must begin with a letter. Subsequent characters can be letters, underscores, or digits (0-9).
        - Can't be a word reserved by the specified database engine.

        *MySQL*

        The name of the database to create when the DB instance is created. If this parameter is not specified, no database is created in the DB instance.

        Constraints:

        - Must contain 1 to 64 letters or numbers.
        - Can't be a word reserved by the specified database engine

        *MariaDB*

        The name of the database to create when the DB instance is created. If this parameter is not specified, no database is created in the DB instance.

        Constraints:

        - Must contain 1 to 64 letters or numbers.
        - Can't be a word reserved by the specified database engine

        *PostgreSQL*

        The name of the database to create when the DB instance is created. If this parameter is not specified, the default ``postgres`` database is created in the DB instance.

        Constraints:

        - Must begin with a letter. Subsequent characters can be letters, underscores, or digits (0-9).
        - Must contain 1 to 63 characters.
        - Can't be a word reserved by the specified database engine

        *Oracle*

        The Oracle System ID (SID) of the created DB instance. If you specify ``null`` , the default value ``ORCL`` is used. You can't specify the string NULL, or any other reserved word, for ``DBName`` .

        Default: ``ORCL``

        Constraints:

        - Can't be longer than 8 characters

        *SQL Server*

        Not applicable. Must be null.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dbname
        '''
        result = self._values.get("db_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of an existing DB parameter group or a reference to an `AWS::RDS::DBParameterGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html>`_ resource created in the template.

        To list all of the available DB parameter group names, use the following command:

        ``aws rds describe-db-parameter-groups --query "DBParameterGroups[].DBParameterGroupName" --output text``
        .. epigraph::

           If any of the data members of the referenced parameter group are changed during an update, the DB instance might need to be restarted, which causes some interruption. If the parameter group contains static parameters, whether they were changed or not, an update triggers a reboot.

        If you don't specify a value for ``DBParameterGroupName`` property, the default DB parameter group for the specified engine and engine version is used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dbparametergroupname
        '''
        result = self._values.get("db_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the DB security groups to assign to the DB instance.

        The list can include both the name of existing DB security groups or references to AWS::RDS::DBSecurityGroup resources created in the template.

        If you set DBSecurityGroups, you must not set VPCSecurityGroups, and vice versa. Also, note that the DBSecurityGroups property exists only for backwards compatibility with older regions and is no longer recommended for providing security information to an RDS DB instance. Instead, use VPCSecurityGroups.
        .. epigraph::

           If you specify this property, AWS CloudFormation sends only the following properties (if specified) to Amazon RDS during create operations:

           - ``AllocatedStorage``
           - ``AutoMinorVersionUpgrade``
           - ``AvailabilityZone``
           - ``BackupRetentionPeriod``
           - ``CharacterSetName``
           - ``DBInstanceClass``
           - ``DBName``
           - ``DBParameterGroupName``
           - ``DBSecurityGroups``
           - ``DBSubnetGroupName``
           - ``Engine``
           - ``EngineVersion``
           - ``Iops``
           - ``LicenseModel``
           - ``MasterUsername``
           - ``MasterUserPassword``
           - ``MultiAZ``
           - ``OptionGroupName``
           - ``PreferredBackupWindow``
           - ``PreferredMaintenanceWindow``

           All other properties are ignored. Specify a virtual private cloud (VPC) security group if you want to submit other properties, such as ``StorageType`` , ``StorageEncrypted`` , or ``KmsKeyId`` . If you're already using the ``DBSecurityGroups`` property, you can't use these other properties by updating your DB instance to use a VPC security group. You must recreate the DB instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dbsecuritygroups
        '''
        result = self._values.get("db_security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def db_snapshot_identifier(self) -> typing.Optional[builtins.str]:
        '''The name or Amazon Resource Name (ARN) of the DB snapshot that's used to restore the DB instance.

        If you're restoring from a shared manual DB snapshot, you must specify the ARN of the snapshot.

        By specifying this property, you can create a DB instance from the specified DB snapshot. If the ``DBSnapshotIdentifier`` property is an empty string or the ``AWS::RDS::DBInstance`` declaration has no ``DBSnapshotIdentifier`` property, AWS CloudFormation creates a new database. If the property contains a value (other than an empty string), AWS CloudFormation creates a database from the specified snapshot. If a snapshot with the specified name doesn't exist, AWS CloudFormation can't create the database and it rolls back the stack.

        Some DB instance properties aren't valid when you restore from a snapshot, such as the ``MasterUsername`` and ``MasterUserPassword`` properties, and the point-in-time recovery properties ``RestoreTime`` and ``UseLatestRestorableTime`` . For information about the properties that you can specify, see the ```RestoreDBInstanceFromDBSnapshot`` <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_RestoreDBInstanceFromDBSnapshot.html>`_ action in the *Amazon RDS API Reference* .

        After you restore a DB instance with a ``DBSnapshotIdentifier`` property, you must specify the same ``DBSnapshotIdentifier`` property for any future updates to the DB instance. When you specify this property for an update, the DB instance is not restored from the DB snapshot again, and the data in the database is not changed. However, if you don't specify the ``DBSnapshotIdentifier`` property, an empty DB instance is created, and the original DB instance is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB instance is restored from the specified ``DBSnapshotIdentifier`` property, and the original DB instance is deleted.

        If you specify the ``DBSnapshotIdentifier`` property to restore a DB instance (as opposed to specifying it for DB instance updates), then don't specify the following properties:

        - ``CharacterSetName``
        - ``DBClusterIdentifier``
        - ``DBName``
        - ``KmsKeyId``
        - ``MasterUsername``
        - ``MasterUserPassword``
        - ``PromotionTier``
        - ``SourceDBInstanceIdentifier``
        - ``SourceRegion``
        - ``StorageEncrypted`` (for an unencrypted snapshot)
        - ``Timezone``

        *Amazon Aurora*

        Not applicable. Snapshot restore is managed by the DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dbsnapshotidentifier
        '''
        result = self._values.get("db_snapshot_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''A DB subnet group to associate with the DB instance.

        If you update this value, the new subnet group must be a subnet group in a new VPC.

        If you don't specify a DB subnet group, RDS uses the default DB subnet group if one exists. If a default DB subnet group does not exist, and you don't specify a ``DBSubnetGroupName`` , the DB instance fails to launch.

        For more information about using Amazon RDS in a VPC, see `Amazon VPC and Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.html>`_ in the *Amazon RDS User Guide* .

        This setting doesn't apply to Amazon Aurora DB instances. The DB subnet group is managed by the DB cluster. If specified, the setting must match the DB cluster setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dbsubnetgroupname
        '''
        result = self._values.get("db_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_system_id(self) -> typing.Optional[builtins.str]:
        '''The Oracle system identifier (SID), which is the name of the Oracle database instance that manages your database files.

        In this context, the term "Oracle database instance" refers exclusively to the system global area (SGA) and Oracle background processes. If you don't specify a SID, the value defaults to ``RDSCDB`` . The Oracle SID is also the name of your CDB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dbsystemid
        '''
        result = self._values.get("db_system_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dedicated_log_volume(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the DB instance has a dedicated log volume (DLV) enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-dedicatedlogvolume
        '''
        result = self._values.get("dedicated_log_volume")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def delete_automated_backups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether to remove automated backups immediately after the DB instance is deleted.

        This parameter isn't case-sensitive. The default is to remove automated backups immediately after the DB instance is deleted.

        *Amazon Aurora*

        Not applicable. When you delete a DB cluster, all automated backups for that DB cluster are deleted and can't be recovered. Manual DB cluster snapshots of the DB cluster are not deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-deleteautomatedbackups
        '''
        result = self._values.get("delete_automated_backups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the DB instance has deletion protection enabled.

        The database can't be deleted when deletion protection is enabled. By default, deletion protection isn't enabled. For more information, see `Deleting a DB Instance <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_DeleteInstance.html>`_ .

        This setting doesn't apply to Amazon Aurora DB instances. You can enable or disable deletion protection for the DB cluster. For more information, see ``CreateDBCluster`` . DB instances in a DB cluster can be deleted even when deletion protection is enabled for the DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The Active Directory directory ID to create the DB instance in.

        Currently, only Db2, MySQL, Microsoft SQL Server, Oracle, and PostgreSQL DB instances can be created in an Active Directory Domain.

        For more information, see `Kerberos Authentication <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/kerberos-authentication.html>`_ in the *Amazon RDS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_auth_secret_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN for the Secrets Manager secret with the credentials for the user joining the domain.

        Example: ``arn:aws:secretsmanager:region:account-number:secret:myselfmanagedADtestsecret-123456``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-domainauthsecretarn
        '''
        result = self._values.get("domain_auth_secret_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_dns_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IPv4 DNS IP addresses of your primary and secondary Active Directory domain controllers.

        Constraints:

        - Two IP addresses must be provided. If there isn't a secondary domain controller, use the IP address of the primary domain controller for both entries in the list.

        Example: ``123.124.125.126,234.235.236.237``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-domaindnsips
        '''
        result = self._values.get("domain_dns_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domain_fqdn(self) -> typing.Optional[builtins.str]:
        '''The fully qualified domain name (FQDN) of an Active Directory domain.

        Constraints:

        - Can't be longer than 64 characters.

        Example: ``mymanagedADtest.mymanagedAD.mydomain``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-domainfqdn
        '''
        result = self._values.get("domain_fqdn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_iam_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role to use when making API calls to the Directory Service.

        This setting doesn't apply to the following DB instances:

        - Amazon Aurora (The domain is managed by the DB cluster.)
        - RDS Custom

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-domainiamrolename
        '''
        result = self._values.get("domain_iam_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_ou(self) -> typing.Optional[builtins.str]:
        '''The Active Directory organizational unit for your DB instance to join.

        Constraints:

        - Must be in the distinguished name format.
        - Can't be longer than 64 characters.

        Example: ``OU=mymanagedADtestOU,DC=mymanagedADtest,DC=mymanagedAD,DC=mydomain``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-domainou
        '''
        result = self._values.get("domain_ou")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_cloudwatch_logs_exports(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of log types that need to be enabled for exporting to CloudWatch Logs.

        The values in the list depend on the DB engine being used. For more information, see `Publishing Database Logs to Amazon CloudWatch Logs <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.html#USER_LogAccess.Procedural.UploadtoCloudWatch>`_ in the *Amazon Relational Database Service User Guide* .

        *Amazon Aurora*

        Not applicable. CloudWatch Logs exports are managed by the DB cluster.

        *Db2*

        Valid values: ``diag.log`` , ``notify.log``

        *MariaDB*

        Valid values: ``audit`` , ``error`` , ``general`` , ``slowquery``

        *Microsoft SQL Server*

        Valid values: ``agent`` , ``error``

        *MySQL*

        Valid values: ``audit`` , ``error`` , ``general`` , ``slowquery``

        *Oracle*

        Valid values: ``alert`` , ``audit`` , ``listener`` , ``trace`` , ``oemagent``

        *PostgreSQL*

        Valid values: ``postgresql`` , ``upgrade``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-enablecloudwatchlogsexports
        '''
        result = self._values.get("enable_cloudwatch_logs_exports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_iam_database_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts.

        By default, mapping is disabled.

        This property is supported for RDS for MariaDB, RDS for MySQL, and RDS for PostgreSQL. For more information, see `IAM Database Authentication for MariaDB, MySQL, and PostgreSQL <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html>`_ in the *Amazon RDS User Guide.*

        *Amazon Aurora*

        Not applicable. Mapping AWS IAM accounts to database accounts is managed by the DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-enableiamdatabaseauthentication
        '''
        result = self._values.get("enable_iam_database_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def enable_performance_insights(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable Performance Insights for the DB instance.

        For more information, see `Using Amazon Performance Insights <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html>`_ in the *Amazon RDS User Guide* .

        This setting doesn't apply to RDS Custom DB instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-enableperformanceinsights
        '''
        result = self._values.get("enable_performance_insights")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The name of the database engine to use for this DB instance.

        Not every database engine is available in every AWS Region.

        This property is required when creating a DB instance.
        .. epigraph::

           You can convert an Oracle database from the non-CDB architecture to the container database (CDB) architecture by updating the ``Engine`` value in your templates from ``oracle-ee`` to ``oracle-ee-cdb`` or from ``oracle-se2`` to ``oracle-se2-cdb`` . Converting to the CDB architecture requires an interruption.

        Valid Values:

        - ``aurora-mysql`` (for Aurora MySQL DB instances)
        - ``aurora-postgresql`` (for Aurora PostgreSQL DB instances)
        - ``custom-oracle-ee`` (for RDS Custom for Oracle DB instances)
        - ``custom-oracle-ee-cdb`` (for RDS Custom for Oracle DB instances)
        - ``custom-sqlserver-ee`` (for RDS Custom for SQL Server DB instances)
        - ``custom-sqlserver-se`` (for RDS Custom for SQL Server DB instances)
        - ``custom-sqlserver-web`` (for RDS Custom for SQL Server DB instances)
        - ``db2-ae``
        - ``db2-se``
        - ``mariadb``
        - ``mysql``
        - ``oracle-ee``
        - ``oracle-ee-cdb``
        - ``oracle-se2``
        - ``oracle-se2-cdb``
        - ``postgres``
        - ``sqlserver-ee``
        - ``sqlserver-se``
        - ``sqlserver-ex``
        - ``sqlserver-web``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_lifecycle_support(self) -> typing.Optional[builtins.str]:
        '''The life cycle type for this DB instance.

        .. epigraph::

           By default, this value is set to ``open-source-rds-extended-support`` , which enrolls your DB instance into Amazon RDS Extended Support. At the end of standard support, you can avoid charges for Extended Support by setting the value to ``open-source-rds-extended-support-disabled`` . In this case, creating the DB instance will fail if the DB major version is past its end of standard support date.

        This setting applies only to RDS for MySQL and RDS for PostgreSQL. For Amazon Aurora DB instances, the life cycle type is managed by the DB cluster.

        You can use this setting to enroll your DB instance into Amazon RDS Extended Support. With RDS Extended Support, you can run the selected major engine version on your DB instance past the end of standard support for that engine version. For more information, see `Amazon RDS Extended Support with Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support.html>`_ in the *Amazon RDS User Guide* .

        Valid Values: ``open-source-rds-extended-support | open-source-rds-extended-support-disabled``

        Default: ``open-source-rds-extended-support``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-enginelifecyclesupport
        '''
        result = self._values.get("engine_lifecycle_support")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the database engine to use.

        For a list of valid engine versions, use the ``DescribeDBEngineVersions`` action.

        The following are the database engines and links to information about the major and minor versions that are available with Amazon RDS. Not every database engine is available for every AWS Region.

        *Amazon Aurora*

        Not applicable. The version number of the database engine to be used by the DB instance is managed by the DB cluster.

        *Db2*

        See `Amazon RDS for Db2 <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Db2.html#Db2.Concepts.VersionMgmt>`_ in the *Amazon RDS User Guide.*

        *MariaDB*

        See `MariaDB on Amazon RDS Versions <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MariaDB.html#MariaDB.Concepts.VersionMgmt>`_ in the *Amazon RDS User Guide.*

        *Microsoft SQL Server*

        See `Microsoft SQL Server Versions on Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_SQLServer.html#SQLServer.Concepts.General.VersionSupport>`_ in the *Amazon RDS User Guide.*

        *MySQL*

        See `MySQL on Amazon RDS Versions <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html#MySQL.Concepts.VersionMgmt>`_ in the *Amazon RDS User Guide.*

        *Oracle*

        See `Oracle Database Engine Release Notes <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.Oracle.PatchComposition.html>`_ in the *Amazon RDS User Guide.*

        *PostgreSQL*

        See `Supported PostgreSQL Database Versions <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts.General.DBVersions>`_ in the *Amazon RDS User Guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''The number of I/O operations per second (IOPS) that the database provisions.

        The value must be equal to or greater than 1000.

        If you specify this property, you must follow the range of allowed ratios of your requested IOPS rate to the amount of storage that you allocate (IOPS to allocated storage). For example, you can provision an Oracle database instance with 1000 IOPS and 200 GiB of storage (a ratio of 5:1), or specify 2000 IOPS with 200 GiB of storage (a ratio of 10:1). For more information, see `Amazon RDS Provisioned IOPS Storage to Improve Performance <https://docs.aws.amazon.com/AmazonRDS/latest/DeveloperGuide/CHAP_Storage.html#USER_PIOPS>`_ in the *Amazon RDS User Guide* .
        .. epigraph::

           If you specify ``io1`` for the ``StorageType`` property, then you must also specify the ``Iops`` property.

        Constraints:

        - For RDS for Db2, MariaDB, MySQL, Oracle, and PostgreSQL - Must be a multiple between .5 and 50 of the storage amount for the DB instance.
        - For RDS for SQL Server - Must be a multiple between 1 and 50 of the storage amount for the DB instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-iops
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS KMS key that's used to encrypt the DB instance, such as ``arn:aws:kms:us-east-1:012345678910:key/abcd1234-a123-456a-a12b-a123b4cd56ef`` .

        If you enable the StorageEncrypted property but don't specify this property, AWS CloudFormation uses the default KMS key. If you specify this property, you must set the StorageEncrypted property to true.

        If you specify the ``SourceDBInstanceIdentifier`` or ``SourceDbiResourceId`` property, don't specify this property. The value is inherited from the source DB instance, and if the DB instance is encrypted, the specified ``KmsKeyId`` property is used. However, if the source DB instance is in a different AWS Region, you must specify a KMS key ID.

        If you specify the ``SourceDBInstanceAutomatedBackupsArn`` property, don't specify this property. The value is inherited from the source DB instance automated backup, and if the automated backup is encrypted, the specified ``KmsKeyId`` property is used.

        If you create an encrypted read replica in a different AWS Region, then you must specify a KMS key for the destination AWS Region. KMS encryption keys are specific to the region that they're created in, and you can't use encryption keys from one region in another region.

        If you specify the ``DBSnapshotIdentifier`` property, don't specify this property. The ``StorageEncrypted`` property value is inherited from the snapshot. If the DB instance is encrypted, the specified ``KmsKeyId`` property is also inherited from the snapshot.

        If you specify ``DBSecurityGroups`` , AWS CloudFormation ignores this property. To specify both a security group and this property, you must use a VPC security group. For more information about Amazon RDS and VPC, see `Using Amazon RDS with Amazon VPC <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.html>`_ in the *Amazon RDS User Guide* .

        *Amazon Aurora*

        Not applicable. The KMS key identifier is managed by the DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_model(self) -> typing.Optional[builtins.str]:
        '''License model information for this DB instance.

        Valid Values:

        - Aurora MySQL - ``general-public-license``
        - Aurora PostgreSQL - ``postgresql-license``
        - RDS for Db2 - ``bring-your-own-license`` . For more information about RDS for Db2 licensing, see ` <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/db2-licensing.html>`_ in the *Amazon RDS User Guide.*
        - RDS for MariaDB - ``general-public-license``
        - RDS for Microsoft SQL Server - ``license-included``
        - RDS for MySQL - ``general-public-license``
        - RDS for Oracle - ``bring-your-own-license`` or ``license-included``
        - RDS for PostgreSQL - ``postgresql-license``

        .. epigraph::

           If you've specified ``DBSecurityGroups`` and then you update the license model, AWS CloudFormation replaces the underlying DB instance. This will incur some interruptions to database availability.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-licensemodel
        '''
        result = self._values.get("license_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manage_master_user_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to manage the master user password with AWS Secrets Manager.

        For more information, see `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html>`_ in the *Amazon RDS User Guide.*

        Constraints:

        - Can't manage the master user password with AWS Secrets Manager if ``MasterUserPassword`` is specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-managemasteruserpassword
        '''
        result = self._values.get("manage_master_user_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def master_user_authentication_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the authentication type for the master user.

        With IAM master user authentication, you can configure the master DB user with IAM database authentication when you create a DB instance.

        You can specify one of the following values:

        - ``password`` - Use standard database authentication with a password.
        - ``iam-db-auth`` - Use IAM database authentication for the master user.

        This option is only valid for RDS for MySQL, RDS for MariaDB, RDS for PostgreSQL, Aurora MySQL, and Aurora PostgreSQL engines.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-masteruserauthenticationtype
        '''
        result = self._values.get("master_user_authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_username(self) -> typing.Optional[builtins.str]:
        '''The master user name for the DB instance.

        .. epigraph::

           If you specify the ``SourceDBInstanceIdentifier`` or ``DBSnapshotIdentifier`` property, don't specify this property. The value is inherited from the source DB instance or snapshot.

           When migrating a self-managed Db2 database, we recommend that you use the same master username as your self-managed Db2 instance name.

        *Amazon Aurora*

        Not applicable. The name for the master user is managed by the DB cluster.

        *RDS for Db2*

        Constraints:

        - Must be 1 to 16 letters or numbers.
        - First character must be a letter.
        - Can't be a reserved word for the chosen database engine.

        *RDS for MariaDB*

        Constraints:

        - Must be 1 to 16 letters or numbers.
        - Can't be a reserved word for the chosen database engine.

        *RDS for Microsoft SQL Server*

        Constraints:

        - Must be 1 to 128 letters or numbers.
        - First character must be a letter.
        - Can't be a reserved word for the chosen database engine.

        *RDS for MySQL*

        Constraints:

        - Must be 1 to 16 letters or numbers.
        - First character must be a letter.
        - Can't be a reserved word for the chosen database engine.

        *RDS for Oracle*

        Constraints:

        - Must be 1 to 30 letters or numbers.
        - First character must be a letter.
        - Can't be a reserved word for the chosen database engine.

        *RDS for PostgreSQL*

        Constraints:

        - Must be 1 to 63 letters or numbers.
        - First character must be a letter.
        - Can't be a reserved word for the chosen database engine.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-masterusername
        '''
        result = self._values.get("master_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_password(self) -> typing.Optional[builtins.str]:
        '''The password for the master user. The password can include any printable ASCII character except "/", """, or "@".

        *Amazon Aurora*

        Not applicable. The password for the master user is managed by the DB cluster.

        *RDS for Db2*

        Must contain from 8 to 255 characters.

        *RDS for MariaDB*

        Constraints: Must contain from 8 to 41 characters.

        *RDS for Microsoft SQL Server*

        Constraints: Must contain from 8 to 128 characters.

        *RDS for MySQL*

        Constraints: Must contain from 8 to 41 characters.

        *RDS for Oracle*

        Constraints: Must contain from 8 to 30 characters.

        *RDS for PostgreSQL*

        Constraints: Must contain from 8 to 128 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-masteruserpassword
        '''
        result = self._values.get("master_user_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_secret(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBInstancePropsMixin.MasterUserSecretProperty"]]:
        '''The secret managed by RDS in AWS Secrets Manager for the master user password.

        For more information, see `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html>`_ in the *Amazon RDS User Guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-masterusersecret
        '''
        result = self._values.get("master_user_secret")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBInstancePropsMixin.MasterUserSecretProperty"]], result)

    @builtins.property
    def max_allocated_storage(self) -> typing.Optional[jsii.Number]:
        '''The upper limit in gibibytes (GiB) to which Amazon RDS can automatically scale the storage of the DB instance.

        For more information about this setting, including limitations that apply to it, see `Managing capacity automatically with Amazon RDS storage autoscaling <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling>`_ in the *Amazon RDS User Guide* .

        This setting doesn't apply to the following DB instances:

        - Amazon Aurora (Storage is managed by the DB cluster.)
        - RDS Custom

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-maxallocatedstorage
        '''
        result = self._values.get("max_allocated_storage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[jsii.Number]:
        '''The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB instance.

        To disable collection of Enhanced Monitoring metrics, specify ``0`` .

        If ``MonitoringRoleArn`` is specified, then you must set ``MonitoringInterval`` to a value other than ``0`` .

        This setting doesn't apply to RDS Custom DB instances.

        Valid Values: ``0 | 1 | 5 | 10 | 15 | 30 | 60``

        Default: ``0``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-monitoringinterval
        '''
        result = self._values.get("monitoring_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitoring_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN for the IAM role that permits RDS to send enhanced monitoring metrics to Amazon CloudWatch Logs.

        For example, ``arn:aws:iam:123456789012:role/emaccess`` . For information on creating a monitoring role, see `Setting Up and Enabling Enhanced Monitoring <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html#USER_Monitoring.OS.Enabling>`_ in the *Amazon RDS User Guide* .

        If ``MonitoringInterval`` is set to a value other than ``0`` , then you must supply a ``MonitoringRoleArn`` value.

        This setting doesn't apply to RDS Custom DB instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-monitoringrolearn
        '''
        result = self._values.get("monitoring_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_az(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the DB instance is a Multi-AZ deployment.

        You can't set the ``AvailabilityZone`` parameter if the DB instance is a Multi-AZ deployment.

        This setting doesn't apply to Amazon Aurora because the DB instance Availability Zones (AZs) are managed by the DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-multiaz
        '''
        result = self._values.get("multi_az")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def nchar_character_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the NCHAR character set for the Oracle DB instance.

        This setting doesn't apply to RDS Custom DB instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-ncharcharactersetname
        '''
        result = self._values.get("nchar_character_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''The network type of the DB instance.

        Valid values:

        - ``IPV4``
        - ``DUAL``

        The network type is determined by the ``DBSubnetGroup`` specified for the DB instance. A ``DBSubnetGroup`` can support only the IPv4 protocol or the IPv4 and IPv6 protocols ( ``DUAL`` ).

        For more information, see `Working with a DB instance in a VPC <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html>`_ in the *Amazon RDS User Guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def option_group_name(self) -> typing.Optional[builtins.str]:
        '''Indicates that the DB instance should be associated with the specified option group.

        Permanent options, such as the TDE option for Oracle Advanced Security TDE, can't be removed from an option group. Also, that option group can't be removed from a DB instance once it is associated with a DB instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-optiongroupname
        '''
        result = self._values.get("option_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def performance_insights_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS KMS key identifier for encryption of Performance Insights data.

        The KMS key identifier is the key ARN, key ID, alias ARN, or alias name for the KMS key.

        If you do not specify a value for ``PerformanceInsightsKMSKeyId`` , then Amazon RDS uses your default KMS key. There is a default KMS key for your AWS account. Your AWS account has a different default KMS key for each AWS Region.

        For information about enabling Performance Insights, see `EnablePerformanceInsights <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enableperformanceinsights>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-performanceinsightskmskeyid
        '''
        result = self._values.get("performance_insights_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def performance_insights_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain Performance Insights data.

        When creating a DB instance without enabling Performance Insights, you can't specify the parameter ``PerformanceInsightsRetentionPeriod`` .

        This setting doesn't apply to RDS Custom DB instances.

        Valid Values:

        - ``7``
        - *month* * 31, where *month* is a number of months from 1-23. Examples: ``93`` (3 months * 31), ``341`` (11 months * 31), ``589`` (19 months * 31)
        - ``731``

        Default: ``7`` days

        If you specify a retention period that isn't valid, such as ``94`` , Amazon RDS returns an error.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-performanceinsightsretentionperiod
        '''
        result = self._values.get("performance_insights_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''The port number on which the database accepts connections.

        This setting doesn't apply to Aurora DB instances. The port number is managed by the cluster.

        Valid Values: ``1150-65535``

        Default:

        - RDS for Db2 - ``50000``
        - RDS for MariaDB - ``3306``
        - RDS for Microsoft SQL Server - ``1433``
        - RDS for MySQL - ``3306``
        - RDS for Oracle - ``1521``
        - RDS for PostgreSQL - ``5432``

        Constraints:

        - For RDS for Microsoft SQL Server, the value can't be ``1234`` , ``1434`` , ``3260`` , ``3343`` , ``3389`` , ``47001`` , or ``49152-49156`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range during which automated backups are created if automated backups are enabled, using the ``BackupRetentionPeriod`` parameter.

        For more information, see `Backup Window <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow>`_ in the *Amazon RDS User Guide.*

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi`` .
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        *Amazon Aurora*

        Not applicable. The daily time range for creating automated backups is managed by the DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-preferredbackupwindow
        '''
        result = self._values.get("preferred_backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC).

        Format: ``ddd:hh24:mi-ddd:hh24:mi``

        The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see `Maintaining a DB instance <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#AdjustingTheMaintenanceWindow>`_ in the *Amazon RDS User Guide.*
        .. epigraph::

           This property applies when AWS CloudFormation initially creates the DB instance. If you use AWS CloudFormation to update the DB instance, those updates are applied immediately.

        Constraints: Minimum 30-minute window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processor_features(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBInstancePropsMixin.ProcessorFeatureProperty"]]]]:
        '''The number of CPU cores and the number of threads per core for the DB instance class of the DB instance.

        This setting doesn't apply to Amazon Aurora or RDS Custom DB instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-processorfeatures
        '''
        result = self._values.get("processor_features")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBInstancePropsMixin.ProcessorFeatureProperty"]]]], result)

    @builtins.property
    def promotion_tier(self) -> typing.Optional[jsii.Number]:
        '''The order of priority in which an Aurora Replica is promoted to the primary instance after a failure of the existing primary instance.

        For more information, see `Fault Tolerance for an Aurora DB Cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraHighAvailability.html#Aurora.Managing.FaultTolerance>`_ in the *Amazon Aurora User Guide* .

        This setting doesn't apply to RDS Custom DB instances.

        Default: ``1``

        Valid Values: ``0 - 15``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-promotiontier
        '''
        result = self._values.get("promotion_tier")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the DB instance is an internet-facing instance.

        If you specify true, AWS CloudFormation creates an instance with a publicly resolvable DNS name, which resolves to a public IP address. If you specify false, AWS CloudFormation creates an internal instance with a DNS name that resolves to a private IP address.

        The default behavior value depends on your VPC setup and the database subnet group. For more information, see the ``PubliclyAccessible`` parameter in the `CreateDBInstance <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_CreateDBInstance.html>`_ in the *Amazon RDS API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def replica_mode(self) -> typing.Optional[builtins.str]:
        '''The open mode of an Oracle read replica.

        For more information, see `Working with Oracle Read Replicas for Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/oracle-read-replicas.html>`_ in the *Amazon RDS User Guide* .

        This setting is only supported in RDS for Oracle.

        Default: ``open-read-only``

        Valid Values: ``open-read-only`` or ``mounted``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-replicamode
        '''
        result = self._values.get("replica_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_time(self) -> typing.Optional[builtins.str]:
        '''The date and time to restore from.

        This parameter applies to point-in-time recovery. For more information, see `Restoring a DB instance to a specified time <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html>`_ in the in the *Amazon RDS User Guide* .

        Constraints:

        - Must be a time in Universal Coordinated Time (UTC) format.
        - Must be before the latest restorable time for the DB instance.
        - Can't be specified if the ``UseLatestRestorableTime`` parameter is enabled.

        Example: ``2009-09-07T23:45:00Z``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-restoretime
        '''
        result = self._values.get("restore_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Multi-AZ DB cluster that will act as the source for the read replica.

        Each DB cluster can have up to 15 read replicas.

        Constraints:

        - Must be the identifier of an existing Multi-AZ DB cluster.
        - Can't be specified if the ``SourceDBInstanceIdentifier`` parameter is also specified.
        - The specified DB cluster must have automatic backups enabled, that is, its backup retention period must be greater than 0.
        - The source DB cluster must be in the same AWS Region as the read replica. Cross-Region replication isn't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-sourcedbclusteridentifier
        '''
        result = self._values.get("source_db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_db_instance_automated_backups_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the replicated automated backups from which to restore, for example, ``arn:aws:rds:us-east-1:123456789012:auto-backup:ab-L2IJCEXJP7XQ7HOJ4SIEXAMPLE`` .

        This setting doesn't apply to RDS Custom.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-sourcedbinstanceautomatedbackupsarn
        '''
        result = self._values.get("source_db_instance_automated_backups_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_db_instance_identifier(self) -> typing.Optional[builtins.str]:
        '''If you want to create a read replica DB instance, specify the ID of the source DB instance.

        Each DB instance can have a limited number of read replicas. For more information, see `Working with Read Replicas <https://docs.aws.amazon.com/AmazonRDS/latest/DeveloperGuide/USER_ReadRepl.html>`_ in the *Amazon RDS User Guide* .

        For information about constraints that apply to DB instance identifiers, see `Naming constraints in Amazon RDS <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html#RDS_Limits.Constraints>`_ in the *Amazon RDS User Guide* .

        The ``SourceDBInstanceIdentifier`` property determines whether a DB instance is a read replica. If you remove the ``SourceDBInstanceIdentifier`` property from your template and then update your stack, AWS CloudFormation promotes the read replica to a standalone DB instance.

        If you specify the ``UseLatestRestorableTime`` or ``RestoreTime`` properties in conjunction with the ``SourceDBInstanceIdentifier`` property, RDS restores the DB instance to the requested point in time, thereby creating a new DB instance.
        .. epigraph::

           - If you specify a source DB instance that uses VPC security groups, we recommend that you specify the ``VPCSecurityGroups`` property. If you don't specify the property, the read replica inherits the value of the ``VPCSecurityGroups`` property from the source DB when you create the replica. However, if you update the stack, AWS CloudFormation reverts the replica's ``VPCSecurityGroups`` property to the default value because it's not defined in the stack's template. This change might cause unexpected issues.
           - Read replicas don't support deletion policies. AWS CloudFormation ignores any deletion policy that's associated with a read replica.
           - If you specify ``SourceDBInstanceIdentifier`` , don't specify the ``DBSnapshotIdentifier`` property. You can't create a read replica from a snapshot.
           - Don't set the ``BackupRetentionPeriod`` , ``DBName`` , ``MasterUsername`` , ``MasterUserPassword`` , and ``PreferredBackupWindow`` properties. The database attributes are inherited from the source DB instance, and backups are disabled for read replicas.
           - If the source DB instance is in a different region than the read replica, specify the source region in ``SourceRegion`` , and specify an ARN for a valid DB instance in ``SourceDBInstanceIdentifier`` . For more information, see `Constructing a Amazon RDS Amazon Resource Name (ARN) <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html#USER_Tagging.ARN>`_ in the *Amazon RDS User Guide* .
           - For DB instances in Amazon Aurora clusters, don't specify this property. Amazon RDS automatically assigns writer and reader DB instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-sourcedbinstanceidentifier
        '''
        result = self._values.get("source_db_instance_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_dbi_resource_id(self) -> typing.Optional[builtins.str]:
        '''The resource ID of the source DB instance from which to restore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-sourcedbiresourceid
        '''
        result = self._values.get("source_dbi_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_region(self) -> typing.Optional[builtins.str]:
        '''The ID of the region that contains the source DB instance for the read replica.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-sourceregion
        '''
        result = self._values.get("source_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether the DB instance is encrypted. By default, it isn't encrypted.

        If you specify the ``KmsKeyId`` property, then you must enable encryption.

        If you specify the ``SourceDBInstanceIdentifier`` or ``SourceDbiResourceId`` property, don't specify this property. The value is inherited from the source DB instance, and if the DB instance is encrypted, the specified ``KmsKeyId`` property is used.

        If you specify the ``SourceDBInstanceAutomatedBackupsArn`` property, don't specify this property. The value is inherited from the source DB instance automated backup.

        If you specify ``DBSnapshotIdentifier`` property, don't specify this property. The value is inherited from the snapshot.

        *Amazon Aurora*

        Not applicable. The encryption for DB instances is managed by the DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-storageencrypted
        '''
        result = self._values.get("storage_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def storage_throughput(self) -> typing.Optional[jsii.Number]:
        '''Specifies the storage throughput value, in mebibyte per second (MiBps), for the DB instance.

        This setting applies only to the ``gp3`` storage type.

        This setting doesn't apply to RDS Custom or Amazon Aurora.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-storagethroughput
        '''
        result = self._values.get("storage_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''The storage type to associate with the DB instance.

        If you specify ``io1`` , ``io2`` , or ``gp3`` , you must also include a value for the ``Iops`` parameter.

        This setting doesn't apply to Amazon Aurora DB instances. Storage is managed by the DB cluster.

        Valid Values: ``gp2 | gp3 | io1 | io2 | standard``

        Default: ``io1`` , if the ``Iops`` parameter is specified. Otherwise, ``gp3`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-storagetype
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the DB instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tde_credential_arn(self) -> typing.Optional[builtins.str]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-tdecredentialarn
        :stability: deprecated
        '''
        result = self._values.get("tde_credential_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tde_credential_password(self) -> typing.Optional[builtins.str]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-tdecredentialpassword
        :stability: deprecated
        '''
        result = self._values.get("tde_credential_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''The time zone of the DB instance.

        The time zone parameter is currently supported only by `RDS for Db2 <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/db2-time-zone>`_ and `RDS for SQL Server <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_SQLServer.html#SQLServer.Concepts.General.TimeZone>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-timezone
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_default_processor_features(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the DB instance class of the DB instance uses its default processor features.

        This setting doesn't apply to RDS Custom DB instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-usedefaultprocessorfeatures
        '''
        result = self._values.get("use_default_processor_features")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def use_latest_restorable_time(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the DB instance is restored from the latest backup time.

        By default, the DB instance isn't restored from the latest backup time. This parameter applies to point-in-time recovery. For more information, see `Restoring a DB instance to a specified time <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html>`_ in the in the *Amazon RDS User Guide* .

        Constraints:

        - Can't be specified if the ``RestoreTime`` parameter is provided.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-uselatestrestorabletime
        '''
        result = self._values.get("use_latest_restorable_time")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def vpc_security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the VPC security group IDs to assign to the DB instance.

        The list can include both the physical IDs of existing VPC security groups and references to `AWS::EC2::SecurityGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html>`_ resources created in the template.

        If you plan to update the resource, don't specify VPC security groups in a shared VPC.

        If you set ``VPCSecurityGroups`` , you must not set ```DBSecurityGroups`` <https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsecuritygroups>`_ , and vice versa.
        .. epigraph::

           You can migrate a DB instance in your stack from an RDS DB security group to a VPC security group, but keep the following in mind:

           - You can't revert to using an RDS security group after you establish a VPC security group membership.
           - When you migrate your DB instance to VPC security groups, if your stack update rolls back because the DB instance update fails or because an update fails in another AWS CloudFormation resource, the rollback fails because it can't revert to an RDS security group.
           - To use the properties that are available when you use a VPC security group, you must recreate the DB instance. If you don't, AWS CloudFormation submits only the property values that are listed in the ```DBSecurityGroups`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsecuritygroups>`_ property.

        To avoid this situation, migrate your DB instance to using VPC security groups only when that is the only change in your stack template.

        *Amazon Aurora*

        Not applicable. The associated list of EC2 VPC security groups is managed by the DB cluster. If specified, the setting must match the DB cluster setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#cfn-rds-dbinstance-vpcsecuritygroups
        '''
        result = self._values.get("vpc_security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDBInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBInstancePropsMixin",
):
    '''The ``AWS::RDS::DBInstance`` resource creates an Amazon DB instance.

    The new DB instance can be an RDS DB instance, or it can be a DB instance in an Aurora DB cluster.

    For more information about creating an RDS DB instance, see `Creating an Amazon RDS DB instance <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html>`_ in the *Amazon RDS User Guide* .

    For more information about creating a DB instance in an Aurora DB cluster, see `Creating an Amazon Aurora DB cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.CreateInstance.html>`_ in the *Amazon Aurora User Guide* .

    If you import an existing DB instance, and the template configuration doesn't match the actual configuration of the DB instance, AWS CloudFormation applies the changes in the template during the import operation.
    .. epigraph::

       If a DB instance is deleted or replaced during an update, AWS CloudFormation deletes all automated snapshots. However, it retains manual DB snapshots. During an update that requires replacement, you can apply a stack policy to prevent DB instances from being replaced. For more information, see `Prevent Updates to Stack Resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html>`_ .

    *Updating DB instances*

    When properties labeled " *Update requires:* `Replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ " are updated, AWS CloudFormation first creates a replacement DB instance, then changes references from other dependent resources to point to the replacement DB instance, and finally deletes the old DB instance.
    .. epigraph::

       We highly recommend that you take a snapshot of the database before updating the stack. If you don't, you lose the data when AWS CloudFormation replaces your DB instance. To preserve your data, perform the following procedure:

       - Deactivate any applications that are using the DB instance so that there's no activity on the DB instance.
       - Create a snapshot of the DB instance. For more information, see `Creating a DB Snapshot <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateSnapshot.html>`_ .
       - If you want to restore your instance using a DB snapshot, modify the updated template with your DB instance changes and add the ``DBSnapshotIdentifier`` property with the ID of the DB snapshot that you want to use.

       After you restore a DB instance with a ``DBSnapshotIdentifier`` property, you can delete the ``DBSnapshotIdentifier`` property. When you specify this property for an update, the DB instance is not restored from the DB snapshot again, and the data in the database is not changed. However, if you don't specify the ``DBSnapshotIdentifier`` property, an empty DB instance is created, and the original DB instance is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB instance is restored from the specified ``DBSnapshotIdentifier`` property, and the original DB instance is deleted.

       - Update the stack.

    For more information about updating other properties of this resource, see ``[ModifyDBInstance](https://docs.aws.amazon.com//AmazonRDS/latest/APIReference/API_ModifyDBInstance.html)`` . For more information about updating stacks, see `AWS CloudFormation Stacks Updates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks.html>`_ .

    *Deleting DB instances*

    For DB instances that are part of an Aurora DB cluster, you can set a deletion policy for your DB instance to control how AWS CloudFormation handles the DB instance when the stack is deleted. For Amazon RDS DB instances, you can choose to *retain* the DB instance, to *delete* the DB instance, or to *create a snapshot* of the DB instance. The default AWS CloudFormation behavior depends on the ``DBClusterIdentifier`` property:

    - For ``AWS::RDS::DBInstance`` resources that don't specify the ``DBClusterIdentifier`` property, AWS CloudFormation saves a snapshot of the DB instance.
    - For ``AWS::RDS::DBInstance`` resources that do specify the ``DBClusterIdentifier`` property, AWS CloudFormation deletes the DB instance.

    For more information, see `DeletionPolicy Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html
    :cloudformationResource: AWS::RDS::DBInstance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_dBInstance_props_mixin = rds_mixins.CfnDBInstancePropsMixin(rds_mixins.CfnDBInstanceMixinProps(
            allocated_storage="allocatedStorage",
            allow_major_version_upgrade=False,
            apply_immediately=False,
            associated_roles=[rds_mixins.CfnDBInstancePropsMixin.DBInstanceRoleProperty(
                feature_name="featureName",
                role_arn="roleArn"
            )],
            automatic_backup_replication_kms_key_id="automaticBackupReplicationKmsKeyId",
            automatic_backup_replication_region="automaticBackupReplicationRegion",
            automatic_backup_replication_retention_period=123,
            auto_minor_version_upgrade=False,
            availability_zone="availabilityZone",
            backup_retention_period=123,
            backup_target="backupTarget",
            ca_certificate_identifier="caCertificateIdentifier",
            certificate_rotation_restart=False,
            character_set_name="characterSetName",
            copy_tags_to_snapshot=False,
            custom_iam_instance_profile="customIamInstanceProfile",
            database_insights_mode="databaseInsightsMode",
            db_cluster_identifier="dbClusterIdentifier",
            db_cluster_snapshot_identifier="dbClusterSnapshotIdentifier",
            db_instance_class="dbInstanceClass",
            db_instance_identifier="dbInstanceIdentifier",
            db_name="dbName",
            db_parameter_group_name="dbParameterGroupName",
            db_security_groups=["dbSecurityGroups"],
            db_snapshot_identifier="dbSnapshotIdentifier",
            db_subnet_group_name="dbSubnetGroupName",
            db_system_id="dbSystemId",
            dedicated_log_volume=False,
            delete_automated_backups=False,
            deletion_protection=False,
            domain="domain",
            domain_auth_secret_arn="domainAuthSecretArn",
            domain_dns_ips=["domainDnsIps"],
            domain_fqdn="domainFqdn",
            domain_iam_role_name="domainIamRoleName",
            domain_ou="domainOu",
            enable_cloudwatch_logs_exports=["enableCloudwatchLogsExports"],
            enable_iam_database_authentication=False,
            enable_performance_insights=False,
            engine="engine",
            engine_lifecycle_support="engineLifecycleSupport",
            engine_version="engineVersion",
            iops=123,
            kms_key_id="kmsKeyId",
            license_model="licenseModel",
            manage_master_user_password=False,
            master_user_authentication_type="masterUserAuthenticationType",
            master_username="masterUsername",
            master_user_password="masterUserPassword",
            master_user_secret=rds_mixins.CfnDBInstancePropsMixin.MasterUserSecretProperty(
                kms_key_id="kmsKeyId",
                secret_arn="secretArn"
            ),
            max_allocated_storage=123,
            monitoring_interval=123,
            monitoring_role_arn="monitoringRoleArn",
            multi_az=False,
            nchar_character_set_name="ncharCharacterSetName",
            network_type="networkType",
            option_group_name="optionGroupName",
            performance_insights_kms_key_id="performanceInsightsKmsKeyId",
            performance_insights_retention_period=123,
            port="port",
            preferred_backup_window="preferredBackupWindow",
            preferred_maintenance_window="preferredMaintenanceWindow",
            processor_features=[rds_mixins.CfnDBInstancePropsMixin.ProcessorFeatureProperty(
                name="name",
                value="value"
            )],
            promotion_tier=123,
            publicly_accessible=False,
            replica_mode="replicaMode",
            restore_time="restoreTime",
            source_db_cluster_identifier="sourceDbClusterIdentifier",
            source_db_instance_automated_backups_arn="sourceDbInstanceAutomatedBackupsArn",
            source_db_instance_identifier="sourceDbInstanceIdentifier",
            source_dbi_resource_id="sourceDbiResourceId",
            source_region="sourceRegion",
            storage_encrypted=False,
            storage_throughput=123,
            storage_type="storageType",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tde_credential_arn="tdeCredentialArn",
            tde_credential_password="tdeCredentialPassword",
            timezone="timezone",
            use_default_processor_features=False,
            use_latest_restorable_time=False,
            vpc_security_groups=["vpcSecurityGroups"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDBInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBInstance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28f3e3d8e6c1bb9a4a2e15f25bbd620022e59a17140df4dcab5f82dfe56852e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b091d3fff3f9c022b8169f68c548710a9887382d3d614074c4e3b04d30cd949)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6da180346468151d65ab251d989f3808890ce5ceeea96db4386368240e2e92)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBInstanceMixinProps:
        return typing.cast(CfnDBInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBInstancePropsMixin.CertificateDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"ca_identifier": "caIdentifier", "valid_till": "validTill"},
    )
    class CertificateDetailsProperty:
        def __init__(
            self,
            *,
            ca_identifier: typing.Optional[builtins.str] = None,
            valid_till: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the DB instance’s server certificate.

            For more information, see `Using SSL/TLS to encrypt a connection to a DB instance <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html>`_ in the *Amazon RDS User Guide* and `Using SSL/TLS to encrypt a connection to a DB cluster <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL.html>`_ in the *Amazon Aurora User Guide* .

            :param ca_identifier: The CA identifier of the CA certificate used for the DB instance's server certificate.
            :param valid_till: The expiration date of the DB instance’s server certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-certificatedetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                certificate_details_property = rds_mixins.CfnDBInstancePropsMixin.CertificateDetailsProperty(
                    ca_identifier="caIdentifier",
                    valid_till="validTill"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50edfa60e98c0ff64d156e4b4b9f84747fc7345375289857eb262781f3673999)
                check_type(argname="argument ca_identifier", value=ca_identifier, expected_type=type_hints["ca_identifier"])
                check_type(argname="argument valid_till", value=valid_till, expected_type=type_hints["valid_till"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ca_identifier is not None:
                self._values["ca_identifier"] = ca_identifier
            if valid_till is not None:
                self._values["valid_till"] = valid_till

        @builtins.property
        def ca_identifier(self) -> typing.Optional[builtins.str]:
            '''The CA identifier of the CA certificate used for the DB instance's server certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-certificatedetails.html#cfn-rds-dbinstance-certificatedetails-caidentifier
            '''
            result = self._values.get("ca_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def valid_till(self) -> typing.Optional[builtins.str]:
            '''The expiration date of the DB instance’s server certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-certificatedetails.html#cfn-rds-dbinstance-certificatedetails-validtill
            '''
            result = self._values.get("valid_till")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBInstancePropsMixin.DBInstanceRoleProperty",
        jsii_struct_bases=[],
        name_mapping={"feature_name": "featureName", "role_arn": "roleArn"},
    )
    class DBInstanceRoleProperty:
        def __init__(
            self,
            *,
            feature_name: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about an AWS Identity and Access Management (IAM) role that is associated with a DB instance.

            :param feature_name: The name of the feature associated with the AWS Identity and Access Management (IAM) role. IAM roles that are associated with a DB instance grant permission for the DB instance to access other AWS services on your behalf. For the list of supported feature names, see the ``SupportedFeatureNames`` description in `DBEngineVersion <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DBEngineVersion.html>`_ in the *Amazon RDS API Reference* .
            :param role_arn: The Amazon Resource Name (ARN) of the IAM role that is associated with the DB instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancerole.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                d_bInstance_role_property = rds_mixins.CfnDBInstancePropsMixin.DBInstanceRoleProperty(
                    feature_name="featureName",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d50286575a28f98261e5d8f798b3f18970a43f7558b9449f2108afcc6d2de46)
                check_type(argname="argument feature_name", value=feature_name, expected_type=type_hints["feature_name"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if feature_name is not None:
                self._values["feature_name"] = feature_name
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def feature_name(self) -> typing.Optional[builtins.str]:
            '''The name of the feature associated with the AWS Identity and Access Management (IAM) role.

            IAM roles that are associated with a DB instance grant permission for the DB instance to access other AWS services on your behalf. For the list of supported feature names, see the ``SupportedFeatureNames`` description in `DBEngineVersion <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DBEngineVersion.html>`_ in the *Amazon RDS API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancerole.html#cfn-rds-dbinstance-dbinstancerole-featurename
            '''
            result = self._values.get("feature_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role that is associated with the DB instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancerole.html#cfn-rds-dbinstance-dbinstancerole-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DBInstanceRoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBInstancePropsMixin.DBInstanceStatusInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "message": "message",
            "normal": "normal",
            "status": "status",
            "status_type": "statusType",
        },
    )
    class DBInstanceStatusInfoProperty:
        def __init__(
            self,
            *,
            message: typing.Optional[builtins.str] = None,
            normal: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            status: typing.Optional[builtins.str] = None,
            status_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides a list of status information for a DB instance.

            :param message: Details of the error if there is an error for the instance. If the instance isn't in an error state, this value is blank.
            :param normal: Indicates whether the instance is operating normally (TRUE) or is in an error state (FALSE).
            :param status: The status of the DB instance. For a StatusType of read replica, the values can be replicating, replication stop point set, replication stop point reached, error, stopped, or terminated.
            :param status_type: This value is currently "read replication.".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancestatusinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                d_bInstance_status_info_property = rds_mixins.CfnDBInstancePropsMixin.DBInstanceStatusInfoProperty(
                    message="message",
                    normal=False,
                    status="status",
                    status_type="statusType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6dac2c818dcc4db1355921d8d11a019cd96034f421c80abe867d125d4cb74880)
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                check_type(argname="argument normal", value=normal, expected_type=type_hints["normal"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument status_type", value=status_type, expected_type=type_hints["status_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message is not None:
                self._values["message"] = message
            if normal is not None:
                self._values["normal"] = normal
            if status is not None:
                self._values["status"] = status
            if status_type is not None:
                self._values["status_type"] = status_type

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''Details of the error if there is an error for the instance.

            If the instance isn't in an error state, this value is blank.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancestatusinfo.html#cfn-rds-dbinstance-dbinstancestatusinfo-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def normal(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the instance is operating normally (TRUE) or is in an error state (FALSE).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancestatusinfo.html#cfn-rds-dbinstance-dbinstancestatusinfo-normal
            '''
            result = self._values.get("normal")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the DB instance.

            For a StatusType of read replica, the values can be replicating, replication stop point set, replication stop point reached, error, stopped, or terminated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancestatusinfo.html#cfn-rds-dbinstance-dbinstancestatusinfo-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_type(self) -> typing.Optional[builtins.str]:
            '''This value is currently "read replication.".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancestatusinfo.html#cfn-rds-dbinstance-dbinstancestatusinfo-statustype
            '''
            result = self._values.get("status_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DBInstanceStatusInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBInstancePropsMixin.EndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address": "address",
            "hosted_zone_id": "hostedZoneId",
            "port": "port",
        },
    )
    class EndpointProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This data type represents the information you need to connect to an Amazon RDS DB instance.

            This data type is used as a response element in the following actions:

            - ``CreateDBInstance``
            - ``DescribeDBInstances``
            - ``DeleteDBInstance``

            For the data structure that represents Amazon Aurora DB cluster endpoints, see ``DBClusterEndpoint`` .

            :param address: Specifies the DNS address of the DB instance.
            :param hosted_zone_id: Specifies the ID that Amazon Route 53 assigns when you create a hosted zone.
            :param port: Specifies the port that the database engine is listening on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-endpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                endpoint_property = rds_mixins.CfnDBInstancePropsMixin.EndpointProperty(
                    address="address",
                    hosted_zone_id="hostedZoneId",
                    port="port"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df440e91d1ed15f679bfb7b3e4fc93294fe3f0e0b96e71ce0b662a730d3dcf2e)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''Specifies the DNS address of the DB instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-endpoint.html#cfn-rds-dbinstance-endpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the ID that Amazon Route 53 assigns when you create a hosted zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-endpoint.html#cfn-rds-dbinstance-endpoint-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''Specifies the port that the database engine is listening on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-endpoint.html#cfn-rds-dbinstance-endpoint-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBInstancePropsMixin.MasterUserSecretProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId", "secret_arn": "secretArn"},
    )
    class MasterUserSecretProperty:
        def __init__(
            self,
            *,
            kms_key_id: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``MasterUserSecret`` return value specifies the secret managed by RDS in AWS Secrets Manager for the master user password.

            For more information, see `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html>`_ in the *Amazon RDS User Guide* and `Password management with AWS Secrets Manager <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-secrets-manager.html>`_ in the *Amazon Aurora User Guide.*

            :param kms_key_id: The AWS KMS key identifier that is used to encrypt the secret.
            :param secret_arn: The Amazon Resource Name (ARN) of the secret. This parameter is a return value that you can retrieve using the ``Fn::GetAtt`` intrinsic function. For more information, see `Return values <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#aws-resource-rds-dbinstance-return-values>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-masterusersecret.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                master_user_secret_property = rds_mixins.CfnDBInstancePropsMixin.MasterUserSecretProperty(
                    kms_key_id="kmsKeyId",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3e1c30363d091ced94a32371f235eacaf7e4cece819b64bec90a14209e523ea)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The AWS KMS key identifier that is used to encrypt the secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-masterusersecret.html#cfn-rds-dbinstance-masterusersecret-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the secret.

            This parameter is a return value that you can retrieve using the ``Fn::GetAtt`` intrinsic function. For more information, see `Return values <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html#aws-resource-rds-dbinstance-return-values>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-masterusersecret.html#cfn-rds-dbinstance-masterusersecret-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MasterUserSecretProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBInstancePropsMixin.ProcessorFeatureProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class ProcessorFeatureProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ProcessorFeature`` property type specifies the processor features of a DB instance class.

            :param name: The name of the processor feature. Valid names are ``coreCount`` and ``threadsPerCore`` .
            :param value: The value of a processor feature.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-processorfeature.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                processor_feature_property = rds_mixins.CfnDBInstancePropsMixin.ProcessorFeatureProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e191daff57d83d50eb1e45a22334e5120c6cb6f4fc21039ca5d97d4a9626d85)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the processor feature.

            Valid names are ``coreCount`` and ``threadsPerCore`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-processorfeature.html#cfn-rds-dbinstance-processorfeature-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of a processor feature.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-processorfeature.html#cfn-rds-dbinstance-processorfeature-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessorFeatureProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBParameterGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_parameter_group_name": "dbParameterGroupName",
        "description": "description",
        "family": "family",
        "parameters": "parameters",
        "tags": "tags",
    },
)
class CfnDBParameterGroupMixinProps:
    def __init__(
        self,
        *,
        db_parameter_group_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        family: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDBParameterGroupPropsMixin.

        :param db_parameter_group_name: The name of the DB parameter group. Constraints: - Must be 1 to 255 letters, numbers, or hyphens. - First character must be a letter - Can't end with a hyphen or contain two consecutive hyphens If you don't specify a value for ``DBParameterGroupName`` property, a name is automatically created for the DB parameter group. .. epigraph:: This value is stored as a lowercase string.
        :param description: Provides the customer-specified description for this DB parameter group.
        :param family: The DB parameter group family name. A DB parameter group can be associated with one and only one DB parameter group family, and can be applied only to a DB instance running a database engine and engine version compatible with that DB parameter group family. To list all of the available parameter group families for a DB engine, use the following command: ``aws rds describe-db-engine-versions --query "DBEngineVersions[].DBParameterGroupFamily" --engine <engine>`` For example, to list all of the available parameter group families for the MySQL DB engine, use the following command: ``aws rds describe-db-engine-versions --query "DBEngineVersions[].DBParameterGroupFamily" --engine mysql`` .. epigraph:: The output contains duplicates. The following are the valid DB engine values: - ``aurora-mysql`` - ``aurora-postgresql`` - ``db2-ae`` - ``db2-se`` - ``mysql`` - ``oracle-ee`` - ``oracle-ee-cdb`` - ``oracle-se2`` - ``oracle-se2-cdb`` - ``postgres`` - ``sqlserver-ee`` - ``sqlserver-se`` - ``sqlserver-ex`` - ``sqlserver-web``
        :param parameters: A mapping of parameter names and values for the parameter update. You must specify at least one parameter name and value. For more information about parameter groups, see `Working with parameter groups <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html>`_ in the *Amazon RDS User Guide* , or `Working with parameter groups <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_WorkingWithParamGroups.html>`_ in the *Amazon Aurora User Guide* . .. epigraph:: AWS CloudFormation doesn't support specifying an apply method for each individual parameter. The default apply method for each parameter is used.
        :param tags: Tags to assign to the DB parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbparametergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            # parameters: Any
            
            cfn_dBParameter_group_mixin_props = rds_mixins.CfnDBParameterGroupMixinProps(
                db_parameter_group_name="dbParameterGroupName",
                description="description",
                family="family",
                parameters=parameters,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26a6de74bb445a96302eba76f71fa3ae3da32030ea5b852d71178605ab585ee)
            check_type(argname="argument db_parameter_group_name", value=db_parameter_group_name, expected_type=type_hints["db_parameter_group_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if db_parameter_group_name is not None:
            self._values["db_parameter_group_name"] = db_parameter_group_name
        if description is not None:
            self._values["description"] = description
        if family is not None:
            self._values["family"] = family
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def db_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the DB parameter group.

        Constraints:

        - Must be 1 to 255 letters, numbers, or hyphens.
        - First character must be a letter
        - Can't end with a hyphen or contain two consecutive hyphens

        If you don't specify a value for ``DBParameterGroupName`` property, a name is automatically created for the DB parameter group.
        .. epigraph::

           This value is stored as a lowercase string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbparametergroup.html#cfn-rds-dbparametergroup-dbparametergroupname
        '''
        result = self._values.get("db_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Provides the customer-specified description for this DB parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbparametergroup.html#cfn-rds-dbparametergroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The DB parameter group family name.

        A DB parameter group can be associated with one and only one DB parameter group family, and can be applied only to a DB instance running a database engine and engine version compatible with that DB parameter group family.

        To list all of the available parameter group families for a DB engine, use the following command:

        ``aws rds describe-db-engine-versions --query "DBEngineVersions[].DBParameterGroupFamily" --engine <engine>``

        For example, to list all of the available parameter group families for the MySQL DB engine, use the following command:

        ``aws rds describe-db-engine-versions --query "DBEngineVersions[].DBParameterGroupFamily" --engine mysql``
        .. epigraph::

           The output contains duplicates.

        The following are the valid DB engine values:

        - ``aurora-mysql``
        - ``aurora-postgresql``
        - ``db2-ae``
        - ``db2-se``
        - ``mysql``
        - ``oracle-ee``
        - ``oracle-ee-cdb``
        - ``oracle-se2``
        - ``oracle-se2-cdb``
        - ``postgres``
        - ``sqlserver-ee``
        - ``sqlserver-se``
        - ``sqlserver-ex``
        - ``sqlserver-web``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbparametergroup.html#cfn-rds-dbparametergroup-family
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''A mapping of parameter names and values for the parameter update.

        You must specify at least one parameter name and value.

        For more information about parameter groups, see `Working with parameter groups <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html>`_ in the *Amazon RDS User Guide* , or `Working with parameter groups <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_WorkingWithParamGroups.html>`_ in the *Amazon Aurora User Guide* .
        .. epigraph::

           AWS CloudFormation doesn't support specifying an apply method for each individual parameter. The default apply method for each parameter is used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbparametergroup.html#cfn-rds-dbparametergroup-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the DB parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbparametergroup.html#cfn-rds-dbparametergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBParameterGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDBParameterGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBParameterGroupPropsMixin",
):
    '''The ``AWS::RDS::DBParameterGroup`` resource creates a custom parameter group for an RDS database family.

    This type can be declared in a template and referenced in the ``DBParameterGroupName`` property of an ``[AWS::RDS::DBInstance](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html)`` resource.

    For information about configuring parameters for Amazon RDS DB instances, see `Working with parameter groups <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html>`_ in the *Amazon RDS User Guide* .

    For information about configuring parameters for Amazon Aurora DB instances, see `Working with parameter groups <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_WorkingWithParamGroups.html>`_ in the *Amazon Aurora User Guide* .
    .. epigraph::

       Applying a parameter group to a DB instance may require the DB instance to reboot, resulting in a database outage for the duration of the reboot.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbparametergroup.html
    :cloudformationResource: AWS::RDS::DBParameterGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        # parameters: Any
        
        cfn_dBParameter_group_props_mixin = rds_mixins.CfnDBParameterGroupPropsMixin(rds_mixins.CfnDBParameterGroupMixinProps(
            db_parameter_group_name="dbParameterGroupName",
            description="description",
            family="family",
            parameters=parameters,
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
        props: typing.Union[CfnDBParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBParameterGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a041592f57685a029a39714da665b6c15082377316f005590626ddad3c711b80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d0da7fd8ddfc9e68a912aa700079b5f0b3a223b77c212ddccb57627f8fb99c6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860345a33d1d146ca8017e7640b74af9114561ee657fbf9ed5732366b9726189)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBParameterGroupMixinProps:
        return typing.cast(CfnDBParameterGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBProxyEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_proxy_endpoint_name": "dbProxyEndpointName",
        "db_proxy_name": "dbProxyName",
        "endpoint_network_type": "endpointNetworkType",
        "tags": "tags",
        "target_role": "targetRole",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
        "vpc_subnet_ids": "vpcSubnetIds",
    },
)
class CfnDBProxyEndpointMixinProps:
    def __init__(
        self,
        *,
        db_proxy_endpoint_name: typing.Optional[builtins.str] = None,
        db_proxy_name: typing.Optional[builtins.str] = None,
        endpoint_network_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnDBProxyEndpointPropsMixin.TagFormatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_role: typing.Optional[builtins.str] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnDBProxyEndpointPropsMixin.

        :param db_proxy_endpoint_name: The name of the DB proxy endpoint to create.
        :param db_proxy_name: The name of the DB proxy associated with the DB proxy endpoint that you create.
        :param endpoint_network_type: The network type of the DB proxy endpoint. The network type determines the IP version that the proxy endpoint supports. Valid values: - ``IPV4`` - The proxy endpoint supports IPv4 only. - ``IPV6`` - The proxy endpoint supports IPv6 only. - ``DUAL`` - The proxy endpoint supports both IPv4 and IPv6.
        :param tags: An optional set of key-value pairs to associate arbitrary data of your choosing with the proxy.
        :param target_role: A value that indicates whether the DB proxy endpoint can be used for read/write or read-only operations.
        :param vpc_security_group_ids: The VPC security group IDs for the DB proxy endpoint that you create. You can specify a different set of security group IDs than for the original DB proxy. The default is the default security group for the VPC.
        :param vpc_subnet_ids: The VPC subnet IDs for the DB proxy endpoint that you create. You can specify a different set of subnet IDs than for the original DB proxy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxyendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_dBProxy_endpoint_mixin_props = rds_mixins.CfnDBProxyEndpointMixinProps(
                db_proxy_endpoint_name="dbProxyEndpointName",
                db_proxy_name="dbProxyName",
                endpoint_network_type="endpointNetworkType",
                tags=[rds_mixins.CfnDBProxyEndpointPropsMixin.TagFormatProperty(
                    key="key",
                    value="value"
                )],
                target_role="targetRole",
                vpc_security_group_ids=["vpcSecurityGroupIds"],
                vpc_subnet_ids=["vpcSubnetIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b658b9d41c7bec4e42eab20c6d8e3937cfb5e9b37d871a4dcd3d920a8906cc)
            check_type(argname="argument db_proxy_endpoint_name", value=db_proxy_endpoint_name, expected_type=type_hints["db_proxy_endpoint_name"])
            check_type(argname="argument db_proxy_name", value=db_proxy_name, expected_type=type_hints["db_proxy_name"])
            check_type(argname="argument endpoint_network_type", value=endpoint_network_type, expected_type=type_hints["endpoint_network_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_role", value=target_role, expected_type=type_hints["target_role"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
            check_type(argname="argument vpc_subnet_ids", value=vpc_subnet_ids, expected_type=type_hints["vpc_subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if db_proxy_endpoint_name is not None:
            self._values["db_proxy_endpoint_name"] = db_proxy_endpoint_name
        if db_proxy_name is not None:
            self._values["db_proxy_name"] = db_proxy_name
        if endpoint_network_type is not None:
            self._values["endpoint_network_type"] = endpoint_network_type
        if tags is not None:
            self._values["tags"] = tags
        if target_role is not None:
            self._values["target_role"] = target_role
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids
        if vpc_subnet_ids is not None:
            self._values["vpc_subnet_ids"] = vpc_subnet_ids

    @builtins.property
    def db_proxy_endpoint_name(self) -> typing.Optional[builtins.str]:
        '''The name of the DB proxy endpoint to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxyendpoint.html#cfn-rds-dbproxyendpoint-dbproxyendpointname
        '''
        result = self._values.get("db_proxy_endpoint_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_proxy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the DB proxy associated with the DB proxy endpoint that you create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxyendpoint.html#cfn-rds-dbproxyendpoint-dbproxyname
        '''
        result = self._values.get("db_proxy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_network_type(self) -> typing.Optional[builtins.str]:
        '''The network type of the DB proxy endpoint.

        The network type determines the IP version that the proxy endpoint supports.

        Valid values:

        - ``IPV4`` - The proxy endpoint supports IPv4 only.
        - ``IPV6`` - The proxy endpoint supports IPv6 only.
        - ``DUAL`` - The proxy endpoint supports both IPv4 and IPv6.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxyendpoint.html#cfn-rds-dbproxyendpoint-endpointnetworktype
        '''
        result = self._values.get("endpoint_network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnDBProxyEndpointPropsMixin.TagFormatProperty"]]:
        '''An optional set of key-value pairs to associate arbitrary data of your choosing with the proxy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxyendpoint.html#cfn-rds-dbproxyendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnDBProxyEndpointPropsMixin.TagFormatProperty"]], result)

    @builtins.property
    def target_role(self) -> typing.Optional[builtins.str]:
        '''A value that indicates whether the DB proxy endpoint can be used for read/write or read-only operations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxyendpoint.html#cfn-rds-dbproxyendpoint-targetrole
        '''
        result = self._values.get("target_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The VPC security group IDs for the DB proxy endpoint that you create.

        You can specify a different set of security group IDs than for the original DB proxy. The default is the default security group for the VPC.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxyendpoint.html#cfn-rds-dbproxyendpoint-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The VPC subnet IDs for the DB proxy endpoint that you create.

        You can specify a different set of subnet IDs than for the original DB proxy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxyendpoint.html#cfn-rds-dbproxyendpoint-vpcsubnetids
        '''
        result = self._values.get("vpc_subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBProxyEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDBProxyEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBProxyEndpointPropsMixin",
):
    '''The ``AWS::RDS::DBProxyEndpoint`` resource creates or updates a DB proxy endpoint.

    You can use custom proxy endpoints to access a proxy through a different VPC than the proxy's default VPC.

    For more information about RDS Proxy, see `AWS::RDS::DBProxy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxyendpoint.html
    :cloudformationResource: AWS::RDS::DBProxyEndpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_dBProxy_endpoint_props_mixin = rds_mixins.CfnDBProxyEndpointPropsMixin(rds_mixins.CfnDBProxyEndpointMixinProps(
            db_proxy_endpoint_name="dbProxyEndpointName",
            db_proxy_name="dbProxyName",
            endpoint_network_type="endpointNetworkType",
            tags=[rds_mixins.CfnDBProxyEndpointPropsMixin.TagFormatProperty(
                key="key",
                value="value"
            )],
            target_role="targetRole",
            vpc_security_group_ids=["vpcSecurityGroupIds"],
            vpc_subnet_ids=["vpcSubnetIds"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDBProxyEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBProxyEndpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8fbf534ff2c1f140a704c7f6b6747f1712a0c0711d952ac7e8a13179d8d3c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53c568cf824ffc9ad457d27b9598edb1c64005c0480c1443848f2535b7f421c7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab9120e7e2a071f6de82d62788f61c0e7a7037f2fb05697035d55f7d4486961)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBProxyEndpointMixinProps:
        return typing.cast(CfnDBProxyEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBProxyEndpointPropsMixin.TagFormatProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagFormatProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Metadata assigned to an Amazon RDS resource consisting of a key-value pair.

            For more information, see `Tagging Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html>`_ in the *Amazon RDS User Guide* or `Tagging Amazon Aurora and Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_Tagging.html>`_ in the *Amazon Aurora User Guide* .

            :param key: A key is the required name of the tag. The string value can be from 1 to 128 Unicode characters in length and can't be prefixed with ``aws:`` or ``rds:`` . The string can only contain only the set of Unicode letters, digits, white-space, '*', '.', ':', '/', '=', '+', '-', '@' (Java regex: "^([\\p{L}\\p{Z}\\p{N}*.:/=+\\-@]*)$").
            :param value: A value is the optional value of the tag. The string value can be from 1 to 256 Unicode characters in length and can't be prefixed with ``aws:`` or ``rds:`` . The string can only contain only the set of Unicode letters, digits, white-space, '*', '.', ':', '/', '=', '+', '-', '@' (Java regex: "^([\\p{L}\\p{Z}\\p{N}*.:/=+\\-@]*)$").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxyendpoint-tagformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                tag_format_property = rds_mixins.CfnDBProxyEndpointPropsMixin.TagFormatProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6966bd8d446f46df408c030c920ba5d7947cad36d026fa940a1ef95a02315677)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''A key is the required name of the tag.

            The string value can be from 1 to 128 Unicode characters in length and can't be prefixed with ``aws:`` or ``rds:`` . The string can only contain only the set of Unicode letters, digits, white-space, '*', '.', ':', '/', '=', '+', '-', '@' (Java regex: "^([\\p{L}\\p{Z}\\p{N}*.:/=+-@]*)$").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxyendpoint-tagformat.html#cfn-rds-dbproxyendpoint-tagformat-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A value is the optional value of the tag.

            The string value can be from 1 to 256 Unicode characters in length and can't be prefixed with ``aws:`` or ``rds:`` . The string can only contain only the set of Unicode letters, digits, white-space, '*', '.', ':', '/', '=', '+', '-', '@' (Java regex: "^([\\p{L}\\p{Z}\\p{N}*.:/=+-@]*)$").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxyendpoint-tagformat.html#cfn-rds-dbproxyendpoint-tagformat-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBProxyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth": "auth",
        "db_proxy_name": "dbProxyName",
        "debug_logging": "debugLogging",
        "default_auth_scheme": "defaultAuthScheme",
        "endpoint_network_type": "endpointNetworkType",
        "engine_family": "engineFamily",
        "idle_client_timeout": "idleClientTimeout",
        "require_tls": "requireTls",
        "role_arn": "roleArn",
        "tags": "tags",
        "target_connection_network_type": "targetConnectionNetworkType",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
        "vpc_subnet_ids": "vpcSubnetIds",
    },
)
class CfnDBProxyMixinProps:
    def __init__(
        self,
        *,
        auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDBProxyPropsMixin.AuthFormatProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        db_proxy_name: typing.Optional[builtins.str] = None,
        debug_logging: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        default_auth_scheme: typing.Optional[builtins.str] = None,
        endpoint_network_type: typing.Optional[builtins.str] = None,
        engine_family: typing.Optional[builtins.str] = None,
        idle_client_timeout: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnDBProxyPropsMixin.TagFormatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_connection_network_type: typing.Optional[builtins.str] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnDBProxyPropsMixin.

        :param auth: The authorization mechanism that the proxy uses.
        :param db_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region . An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens.
        :param debug_logging: Specifies whether the proxy logs detailed connection and query information. When you enable ``DebugLogging`` , the proxy captures connection details and connection pool behavior from your queries. Debug logging increases CloudWatch costs and can impact proxy performance. Enable this option only when you need to troubleshoot connection or performance issues.
        :param default_auth_scheme: The default authentication scheme that the proxy uses for client connections to the proxy and connections from the proxy to the underlying database. Valid values are ``NONE`` and ``IAM_AUTH`` . When set to ``IAM_AUTH`` , the proxy uses end-to-end IAM authentication to connect to the database.
        :param endpoint_network_type: The network type of the DB proxy endpoint. The network type determines the IP version that the proxy endpoint supports. Valid values: - ``IPV4`` - The proxy endpoint supports IPv4 only. - ``IPV6`` - The proxy endpoint supports IPv6 only. - ``DUAL`` - The proxy endpoint supports both IPv4 and IPv6.
        :param engine_family: The kinds of databases that the proxy can connect to. This value determines which database network protocol the proxy recognizes when it interprets network traffic to and from the database. For Aurora MySQL, RDS for MariaDB, and RDS for MySQL databases, specify ``MYSQL`` . For Aurora PostgreSQL and RDS for PostgreSQL databases, specify ``POSTGRESQL`` . For RDS for Microsoft SQL Server, specify ``SQLSERVER`` .
        :param idle_client_timeout: The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it. You can set this value higher or lower than the connection timeout limit for the associated database.
        :param require_tls: Specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By enabling this setting, you can enforce encrypted TLS connections to the proxy.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role that the proxy uses to access secrets in AWS Secrets Manager.
        :param tags: An optional set of key-value pairs to associate arbitrary data of your choosing with the proxy.
        :param target_connection_network_type: The network type that the proxy uses to connect to the target database. The network type determines the IP version that the proxy uses for connections to the database. Valid values: - ``IPV4`` - The proxy connects to the database using IPv4 only. - ``IPV6`` - The proxy connects to the database using IPv6 only.
        :param vpc_security_group_ids: One or more VPC security group IDs to associate with the new proxy. If you plan to update the resource, don't specify VPC security groups in a shared VPC.
        :param vpc_subnet_ids: One or more VPC subnet IDs to associate with the new proxy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_dBProxy_mixin_props = rds_mixins.CfnDBProxyMixinProps(
                auth=[rds_mixins.CfnDBProxyPropsMixin.AuthFormatProperty(
                    auth_scheme="authScheme",
                    client_password_auth_type="clientPasswordAuthType",
                    description="description",
                    iam_auth="iamAuth",
                    secret_arn="secretArn"
                )],
                db_proxy_name="dbProxyName",
                debug_logging=False,
                default_auth_scheme="defaultAuthScheme",
                endpoint_network_type="endpointNetworkType",
                engine_family="engineFamily",
                idle_client_timeout=123,
                require_tls=False,
                role_arn="roleArn",
                tags=[rds_mixins.CfnDBProxyPropsMixin.TagFormatProperty(
                    key="key",
                    value="value"
                )],
                target_connection_network_type="targetConnectionNetworkType",
                vpc_security_group_ids=["vpcSecurityGroupIds"],
                vpc_subnet_ids=["vpcSubnetIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121eff4dd724752490f92e20e7f92b129b2d3d89ffd1fb866a19891cadc77624)
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument db_proxy_name", value=db_proxy_name, expected_type=type_hints["db_proxy_name"])
            check_type(argname="argument debug_logging", value=debug_logging, expected_type=type_hints["debug_logging"])
            check_type(argname="argument default_auth_scheme", value=default_auth_scheme, expected_type=type_hints["default_auth_scheme"])
            check_type(argname="argument endpoint_network_type", value=endpoint_network_type, expected_type=type_hints["endpoint_network_type"])
            check_type(argname="argument engine_family", value=engine_family, expected_type=type_hints["engine_family"])
            check_type(argname="argument idle_client_timeout", value=idle_client_timeout, expected_type=type_hints["idle_client_timeout"])
            check_type(argname="argument require_tls", value=require_tls, expected_type=type_hints["require_tls"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_connection_network_type", value=target_connection_network_type, expected_type=type_hints["target_connection_network_type"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
            check_type(argname="argument vpc_subnet_ids", value=vpc_subnet_ids, expected_type=type_hints["vpc_subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth is not None:
            self._values["auth"] = auth
        if db_proxy_name is not None:
            self._values["db_proxy_name"] = db_proxy_name
        if debug_logging is not None:
            self._values["debug_logging"] = debug_logging
        if default_auth_scheme is not None:
            self._values["default_auth_scheme"] = default_auth_scheme
        if endpoint_network_type is not None:
            self._values["endpoint_network_type"] = endpoint_network_type
        if engine_family is not None:
            self._values["engine_family"] = engine_family
        if idle_client_timeout is not None:
            self._values["idle_client_timeout"] = idle_client_timeout
        if require_tls is not None:
            self._values["require_tls"] = require_tls
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if target_connection_network_type is not None:
            self._values["target_connection_network_type"] = target_connection_network_type
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids
        if vpc_subnet_ids is not None:
            self._values["vpc_subnet_ids"] = vpc_subnet_ids

    @builtins.property
    def auth(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBProxyPropsMixin.AuthFormatProperty"]]]]:
        '''The authorization mechanism that the proxy uses.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-auth
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBProxyPropsMixin.AuthFormatProperty"]]]], result)

    @builtins.property
    def db_proxy_name(self) -> typing.Optional[builtins.str]:
        '''The identifier for the proxy.

        This name must be unique for all proxies owned by your AWS account in the specified AWS Region . An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-dbproxyname
        '''
        result = self._values.get("db_proxy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def debug_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the proxy logs detailed connection and query information.

        When you enable ``DebugLogging`` , the proxy captures connection details and connection pool behavior from your queries. Debug logging increases CloudWatch costs and can impact proxy performance. Enable this option only when you need to troubleshoot connection or performance issues.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-debuglogging
        '''
        result = self._values.get("debug_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def default_auth_scheme(self) -> typing.Optional[builtins.str]:
        '''The default authentication scheme that the proxy uses for client connections to the proxy and connections from the proxy to the underlying database.

        Valid values are ``NONE`` and ``IAM_AUTH`` . When set to ``IAM_AUTH`` , the proxy uses end-to-end IAM authentication to connect to the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-defaultauthscheme
        '''
        result = self._values.get("default_auth_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_network_type(self) -> typing.Optional[builtins.str]:
        '''The network type of the DB proxy endpoint.

        The network type determines the IP version that the proxy endpoint supports.

        Valid values:

        - ``IPV4`` - The proxy endpoint supports IPv4 only.
        - ``IPV6`` - The proxy endpoint supports IPv6 only.
        - ``DUAL`` - The proxy endpoint supports both IPv4 and IPv6.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-endpointnetworktype
        '''
        result = self._values.get("endpoint_network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_family(self) -> typing.Optional[builtins.str]:
        '''The kinds of databases that the proxy can connect to.

        This value determines which database network protocol the proxy recognizes when it interprets network traffic to and from the database. For Aurora MySQL, RDS for MariaDB, and RDS for MySQL databases, specify ``MYSQL`` . For Aurora PostgreSQL and RDS for PostgreSQL databases, specify ``POSTGRESQL`` . For RDS for Microsoft SQL Server, specify ``SQLSERVER`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-enginefamily
        '''
        result = self._values.get("engine_family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_client_timeout(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it.

        You can set this value higher or lower than the connection timeout limit for the associated database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-idleclienttimeout
        '''
        result = self._values.get("idle_client_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy.

        By enabling this setting, you can enforce encrypted TLS connections to the proxy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-requiretls
        '''
        result = self._values.get("require_tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that the proxy uses to access secrets in AWS Secrets Manager.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnDBProxyPropsMixin.TagFormatProperty"]]:
        '''An optional set of key-value pairs to associate arbitrary data of your choosing with the proxy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnDBProxyPropsMixin.TagFormatProperty"]], result)

    @builtins.property
    def target_connection_network_type(self) -> typing.Optional[builtins.str]:
        '''The network type that the proxy uses to connect to the target database.

        The network type determines the IP version that the proxy uses for connections to the database.

        Valid values:

        - ``IPV4`` - The proxy connects to the database using IPv4 only.
        - ``IPV6`` - The proxy connects to the database using IPv6 only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-targetconnectionnetworktype
        '''
        result = self._values.get("target_connection_network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more VPC security group IDs to associate with the new proxy.

        If you plan to update the resource, don't specify VPC security groups in a shared VPC.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more VPC subnet IDs to associate with the new proxy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-vpcsubnetids
        '''
        result = self._values.get("vpc_subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBProxyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDBProxyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBProxyPropsMixin",
):
    '''The ``AWS::RDS::DBProxy`` resource creates or updates a DB proxy.

    For information about RDS Proxy for Amazon RDS, see `Managing Connections with Amazon RDS Proxy <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html>`_ in the *Amazon RDS User Guide* .

    For information about RDS Proxy for Amazon Aurora, see `Managing Connections with Amazon RDS Proxy <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-proxy.html>`_ in the *Amazon Aurora User Guide* .
    .. epigraph::

       Limitations apply to RDS Proxy, including DB engine version limitations and AWS Region limitations.

       For information about limitations that apply to RDS Proxy for Amazon RDS, see `Limitations for RDS Proxy <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html#rds-proxy.limitations>`_ in the *Amazon RDS User Guide* .

       For information about that apply to RDS Proxy for Amazon Aurora, see `Limitations for RDS Proxy <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-proxy.html#rds-proxy.limitations>`_ in the *Amazon Aurora User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html
    :cloudformationResource: AWS::RDS::DBProxy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_dBProxy_props_mixin = rds_mixins.CfnDBProxyPropsMixin(rds_mixins.CfnDBProxyMixinProps(
            auth=[rds_mixins.CfnDBProxyPropsMixin.AuthFormatProperty(
                auth_scheme="authScheme",
                client_password_auth_type="clientPasswordAuthType",
                description="description",
                iam_auth="iamAuth",
                secret_arn="secretArn"
            )],
            db_proxy_name="dbProxyName",
            debug_logging=False,
            default_auth_scheme="defaultAuthScheme",
            endpoint_network_type="endpointNetworkType",
            engine_family="engineFamily",
            idle_client_timeout=123,
            require_tls=False,
            role_arn="roleArn",
            tags=[rds_mixins.CfnDBProxyPropsMixin.TagFormatProperty(
                key="key",
                value="value"
            )],
            target_connection_network_type="targetConnectionNetworkType",
            vpc_security_group_ids=["vpcSecurityGroupIds"],
            vpc_subnet_ids=["vpcSubnetIds"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDBProxyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBProxy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__613a2811c20bca87220368fdd015c3be7ba4e2f4e929bc6845a326567c50ff47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eace7e687dca7dc9236511abd59f5769756e97fe8a4430b95f3b0b920c532d62)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c6ca829b771e10130f8258bf9b74a7646942616cff804ee7aaa7bd51b2ef563)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBProxyMixinProps:
        return typing.cast(CfnDBProxyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBProxyPropsMixin.AuthFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_scheme": "authScheme",
            "client_password_auth_type": "clientPasswordAuthType",
            "description": "description",
            "iam_auth": "iamAuth",
            "secret_arn": "secretArn",
        },
    )
    class AuthFormatProperty:
        def __init__(
            self,
            *,
            auth_scheme: typing.Optional[builtins.str] = None,
            client_password_auth_type: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            iam_auth: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the details of authentication used by a proxy to log in as a specific database user.

            :param auth_scheme: The type of authentication that the proxy uses for connections from the proxy to the underlying database.
            :param client_password_auth_type: Specifies the details of authentication used by a proxy to log in as a specific database user.
            :param description: A user-specified description about the authentication used by a proxy to log in as a specific database user.
            :param iam_auth: A value that indicates whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy. The ``ENABLED`` value is valid only for proxies with RDS for Microsoft SQL Server.
            :param secret_arn: The Amazon Resource Name (ARN) representing the secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                auth_format_property = rds_mixins.CfnDBProxyPropsMixin.AuthFormatProperty(
                    auth_scheme="authScheme",
                    client_password_auth_type="clientPasswordAuthType",
                    description="description",
                    iam_auth="iamAuth",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72d0427f22698fff24a4cc5a00fd9ccb47733fbbd4dbaedd1ab5c8bf1aeae7c2)
                check_type(argname="argument auth_scheme", value=auth_scheme, expected_type=type_hints["auth_scheme"])
                check_type(argname="argument client_password_auth_type", value=client_password_auth_type, expected_type=type_hints["client_password_auth_type"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument iam_auth", value=iam_auth, expected_type=type_hints["iam_auth"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_scheme is not None:
                self._values["auth_scheme"] = auth_scheme
            if client_password_auth_type is not None:
                self._values["client_password_auth_type"] = client_password_auth_type
            if description is not None:
                self._values["description"] = description
            if iam_auth is not None:
                self._values["iam_auth"] = iam_auth
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def auth_scheme(self) -> typing.Optional[builtins.str]:
            '''The type of authentication that the proxy uses for connections from the proxy to the underlying database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html#cfn-rds-dbproxy-authformat-authscheme
            '''
            result = self._values.get("auth_scheme")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_password_auth_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the details of authentication used by a proxy to log in as a specific database user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html#cfn-rds-dbproxy-authformat-clientpasswordauthtype
            '''
            result = self._values.get("client_password_auth_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A user-specified description about the authentication used by a proxy to log in as a specific database user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html#cfn-rds-dbproxy-authformat-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iam_auth(self) -> typing.Optional[builtins.str]:
            '''A value that indicates whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy.

            The ``ENABLED`` value is valid only for proxies with RDS for Microsoft SQL Server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html#cfn-rds-dbproxy-authformat-iamauth
            '''
            result = self._values.get("iam_auth")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) representing the secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster.

            These secrets are stored within Amazon Secrets Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html#cfn-rds-dbproxy-authformat-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBProxyPropsMixin.TagFormatProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagFormatProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Metadata assigned to an Amazon RDS resource consisting of a key-value pair.

            For more information, see `Tagging Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html>`_ in the *Amazon RDS User Guide* or `Tagging Amazon Aurora and Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_Tagging.html>`_ in the *Amazon Aurora User Guide* .

            :param key: A key is the required name of the tag. The string value can be from 1 to 128 Unicode characters in length and can't be prefixed with ``aws:`` or ``rds:`` . The string can only contain only the set of Unicode letters, digits, white-space, '*', '.', ':', '/', '=', '+', '-', '@' (Java regex: "^([\\p{L}\\p{Z}\\p{N}*.:/=+\\-@]*)$").
            :param value: A value is the optional value of the tag. The string value can be from 1 to 256 Unicode characters in length and can't be prefixed with ``aws:`` or ``rds:`` . The string can only contain only the set of Unicode letters, digits, white-space, '*', '.', ':', '/', '=', '+', '-', '@' (Java regex: "^([\\p{L}\\p{Z}\\p{N}*.:/=+\\-@]*)$").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-tagformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                tag_format_property = rds_mixins.CfnDBProxyPropsMixin.TagFormatProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5270d326f93d5e2bfc34b7f0c8cf3e8ae1f8411e6b011e53cbb9dda10d8368d5)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''A key is the required name of the tag.

            The string value can be from 1 to 128 Unicode characters in length and can't be prefixed with ``aws:`` or ``rds:`` . The string can only contain only the set of Unicode letters, digits, white-space, '*', '.', ':', '/', '=', '+', '-', '@' (Java regex: "^([\\p{L}\\p{Z}\\p{N}*.:/=+-@]*)$").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-tagformat.html#cfn-rds-dbproxy-tagformat-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A value is the optional value of the tag.

            The string value can be from 1 to 256 Unicode characters in length and can't be prefixed with ``aws:`` or ``rds:`` . The string can only contain only the set of Unicode letters, digits, white-space, '*', '.', ':', '/', '=', '+', '-', '@' (Java regex: "^([\\p{L}\\p{Z}\\p{N}*.:/=+-@]*)$").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-tagformat.html#cfn-rds-dbproxy-tagformat-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBProxyTargetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_pool_configuration_info": "connectionPoolConfigurationInfo",
        "db_cluster_identifiers": "dbClusterIdentifiers",
        "db_instance_identifiers": "dbInstanceIdentifiers",
        "db_proxy_name": "dbProxyName",
        "target_group_name": "targetGroupName",
    },
)
class CfnDBProxyTargetGroupMixinProps:
    def __init__(
        self,
        *,
        connection_pool_configuration_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDBProxyTargetGroupPropsMixin.ConnectionPoolConfigurationInfoFormatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        db_cluster_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        db_instance_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        db_proxy_name: typing.Optional[builtins.str] = None,
        target_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDBProxyTargetGroupPropsMixin.

        :param connection_pool_configuration_info: Displays the settings that control the size and behavior of the connection pool associated with a ``DBProxyTarget`` .
        :param db_cluster_identifiers: One or more DB cluster identifiers.
        :param db_instance_identifiers: One or more DB instance identifiers.
        :param db_proxy_name: The identifier of the ``DBProxy`` that is associated with the ``DBProxyTargetGroup`` .
        :param target_group_name: The identifier for the target group. .. epigraph:: Currently, this property must be set to ``default`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_dBProxy_target_group_mixin_props = rds_mixins.CfnDBProxyTargetGroupMixinProps(
                connection_pool_configuration_info=rds_mixins.CfnDBProxyTargetGroupPropsMixin.ConnectionPoolConfigurationInfoFormatProperty(
                    connection_borrow_timeout=123,
                    init_query="initQuery",
                    max_connections_percent=123,
                    max_idle_connections_percent=123,
                    session_pinning_filters=["sessionPinningFilters"]
                ),
                db_cluster_identifiers=["dbClusterIdentifiers"],
                db_instance_identifiers=["dbInstanceIdentifiers"],
                db_proxy_name="dbProxyName",
                target_group_name="targetGroupName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581fda2d223fe0b8c4816c0caa6dd03bbe8e532a9882e891a1fec9b6fe61cc9e)
            check_type(argname="argument connection_pool_configuration_info", value=connection_pool_configuration_info, expected_type=type_hints["connection_pool_configuration_info"])
            check_type(argname="argument db_cluster_identifiers", value=db_cluster_identifiers, expected_type=type_hints["db_cluster_identifiers"])
            check_type(argname="argument db_instance_identifiers", value=db_instance_identifiers, expected_type=type_hints["db_instance_identifiers"])
            check_type(argname="argument db_proxy_name", value=db_proxy_name, expected_type=type_hints["db_proxy_name"])
            check_type(argname="argument target_group_name", value=target_group_name, expected_type=type_hints["target_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_pool_configuration_info is not None:
            self._values["connection_pool_configuration_info"] = connection_pool_configuration_info
        if db_cluster_identifiers is not None:
            self._values["db_cluster_identifiers"] = db_cluster_identifiers
        if db_instance_identifiers is not None:
            self._values["db_instance_identifiers"] = db_instance_identifiers
        if db_proxy_name is not None:
            self._values["db_proxy_name"] = db_proxy_name
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name

    @builtins.property
    def connection_pool_configuration_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBProxyTargetGroupPropsMixin.ConnectionPoolConfigurationInfoFormatProperty"]]:
        '''Displays the settings that control the size and behavior of the connection pool associated with a ``DBProxyTarget`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfo
        '''
        result = self._values.get("connection_pool_configuration_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBProxyTargetGroupPropsMixin.ConnectionPoolConfigurationInfoFormatProperty"]], result)

    @builtins.property
    def db_cluster_identifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more DB cluster identifiers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-dbclusteridentifiers
        '''
        result = self._values.get("db_cluster_identifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def db_instance_identifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more DB instance identifiers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-dbinstanceidentifiers
        '''
        result = self._values.get("db_instance_identifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def db_proxy_name(self) -> typing.Optional[builtins.str]:
        '''The identifier of the ``DBProxy`` that is associated with the ``DBProxyTargetGroup`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-dbproxyname
        '''
        result = self._values.get("db_proxy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        '''The identifier for the target group.

        .. epigraph::

           Currently, this property must be set to ``default`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-targetgroupname
        '''
        result = self._values.get("target_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBProxyTargetGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDBProxyTargetGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBProxyTargetGroupPropsMixin",
):
    '''The ``AWS::RDS::DBProxyTargetGroup`` resource represents a set of RDS DB instances, Aurora DB clusters, or both that a proxy can connect to.

    Currently, each target group is associated with exactly one RDS DB instance or Aurora DB cluster.

    This data type is used as a response element in the ``DescribeDBProxyTargetGroups`` action.

    For information about RDS Proxy for Amazon RDS, see `Managing Connections with Amazon RDS Proxy <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html>`_ in the *Amazon RDS User Guide* .

    For information about RDS Proxy for Amazon Aurora, see `Managing Connections with Amazon RDS Proxy <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-proxy.html>`_ in the *Amazon Aurora User Guide* .

    For a sample template that creates a DB proxy and registers a DB instance, see `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#aws-resource-rds-dbproxy--examples>`_ in AWS::RDS::DBProxy.
    .. epigraph::

       Limitations apply to RDS Proxy, including DB engine version limitations and AWS Region limitations.

       For information about limitations that apply to RDS Proxy for Amazon RDS, see `Limitations for RDS Proxy <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html#rds-proxy.limitations>`_ in the *Amazon RDS User Guide* .

       For information about that apply to RDS Proxy for Amazon Aurora, see `Limitations for RDS Proxy <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-proxy.html#rds-proxy.limitations>`_ in the *Amazon Aurora User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html
    :cloudformationResource: AWS::RDS::DBProxyTargetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_dBProxy_target_group_props_mixin = rds_mixins.CfnDBProxyTargetGroupPropsMixin(rds_mixins.CfnDBProxyTargetGroupMixinProps(
            connection_pool_configuration_info=rds_mixins.CfnDBProxyTargetGroupPropsMixin.ConnectionPoolConfigurationInfoFormatProperty(
                connection_borrow_timeout=123,
                init_query="initQuery",
                max_connections_percent=123,
                max_idle_connections_percent=123,
                session_pinning_filters=["sessionPinningFilters"]
            ),
            db_cluster_identifiers=["dbClusterIdentifiers"],
            db_instance_identifiers=["dbInstanceIdentifiers"],
            db_proxy_name="dbProxyName",
            target_group_name="targetGroupName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDBProxyTargetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBProxyTargetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddfef73b5aad68fc1c307d4d7eda635e4b9d4fb007dbdc733679f1433bbec821)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76b132a2d3c195d33d4a0baf0c30249a2032bd60d1300c6e19041bbe202771a7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e245cd671d061c36b5bb2d19236bb16f92e9fe6833c29e4dd11f313825ec9fea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBProxyTargetGroupMixinProps:
        return typing.cast(CfnDBProxyTargetGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBProxyTargetGroupPropsMixin.ConnectionPoolConfigurationInfoFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_borrow_timeout": "connectionBorrowTimeout",
            "init_query": "initQuery",
            "max_connections_percent": "maxConnectionsPercent",
            "max_idle_connections_percent": "maxIdleConnectionsPercent",
            "session_pinning_filters": "sessionPinningFilters",
        },
    )
    class ConnectionPoolConfigurationInfoFormatProperty:
        def __init__(
            self,
            *,
            connection_borrow_timeout: typing.Optional[jsii.Number] = None,
            init_query: typing.Optional[builtins.str] = None,
            max_connections_percent: typing.Optional[jsii.Number] = None,
            max_idle_connections_percent: typing.Optional[jsii.Number] = None,
            session_pinning_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the settings that control the size and behavior of the connection pool associated with a ``DBProxyTargetGroup`` .

            :param connection_borrow_timeout: The number of seconds for a proxy to wait for a connection to become available in the connection pool. This setting only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions. Default: ``120`` Constraints: - Must be between 0 and 300.
            :param init_query: Add an initialization query, or modify the current one. You can specify one or more SQL statements for the proxy to run when opening each new database connection. The setting is typically used with ``SET`` statements to make sure that each connection has identical settings. Make sure the query added here is valid. This is an optional field, so you can choose to leave it empty. For including multiple variables in a single SET statement, use a comma separator. For example: ``SET variable1=value1, variable2=value2`` Default: no initialization query .. epigraph:: Since you can access initialization query as part of target group configuration, it is not protected by authentication or cryptographic methods. Anyone with access to view or manage your proxy target group configuration can view the initialization query. You should not add sensitive data, such as passwords or long-lived encryption keys, to this option.
            :param max_connections_percent: The maximum size of the connection pool for each target in a target group. The value is expressed as a percentage of the ``max_connections`` setting for the RDS DB instance or Aurora DB cluster used by the target group. If you specify ``MaxIdleConnectionsPercent`` , then you must also include a value for this parameter. Default: ``10`` for RDS for Microsoft SQL Server, and ``100`` for all other engines Constraints: - Must be between 1 and 100.
            :param max_idle_connections_percent: A value that controls how actively the proxy closes idle database connections in the connection pool. The value is expressed as a percentage of the ``max_connections`` setting for the RDS DB instance or Aurora DB cluster used by the target group. With a high value, the proxy leaves a high percentage of idle database connections open. A low value causes the proxy to close more idle connections and return them to the database. If you specify this parameter, then you must also include a value for ``MaxConnectionsPercent`` . Default: The default value is half of the value of ``MaxConnectionsPercent`` . For example, if ``MaxConnectionsPercent`` is 80, then the default value of ``MaxIdleConnectionsPercent`` is 40. If the value of ``MaxConnectionsPercent`` isn't specified, then for SQL Server, ``MaxIdleConnectionsPercent`` is ``5`` , and for all other engines, the default is ``50`` . Constraints: - Must be between 0 and the value of ``MaxConnectionsPercent`` .
            :param session_pinning_filters: Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection. Including an item in the list exempts that class of SQL operations from the pinning behavior. Default: no session pinning filters

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                connection_pool_configuration_info_format_property = rds_mixins.CfnDBProxyTargetGroupPropsMixin.ConnectionPoolConfigurationInfoFormatProperty(
                    connection_borrow_timeout=123,
                    init_query="initQuery",
                    max_connections_percent=123,
                    max_idle_connections_percent=123,
                    session_pinning_filters=["sessionPinningFilters"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cc3f853ce587302f2b5ccfd26075da37ddd375056532c79dd32e62cc31d8ade)
                check_type(argname="argument connection_borrow_timeout", value=connection_borrow_timeout, expected_type=type_hints["connection_borrow_timeout"])
                check_type(argname="argument init_query", value=init_query, expected_type=type_hints["init_query"])
                check_type(argname="argument max_connections_percent", value=max_connections_percent, expected_type=type_hints["max_connections_percent"])
                check_type(argname="argument max_idle_connections_percent", value=max_idle_connections_percent, expected_type=type_hints["max_idle_connections_percent"])
                check_type(argname="argument session_pinning_filters", value=session_pinning_filters, expected_type=type_hints["session_pinning_filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_borrow_timeout is not None:
                self._values["connection_borrow_timeout"] = connection_borrow_timeout
            if init_query is not None:
                self._values["init_query"] = init_query
            if max_connections_percent is not None:
                self._values["max_connections_percent"] = max_connections_percent
            if max_idle_connections_percent is not None:
                self._values["max_idle_connections_percent"] = max_idle_connections_percent
            if session_pinning_filters is not None:
                self._values["session_pinning_filters"] = session_pinning_filters

        @builtins.property
        def connection_borrow_timeout(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds for a proxy to wait for a connection to become available in the connection pool.

            This setting only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions.

            Default: ``120``

            Constraints:

            - Must be between 0 and 300.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat-connectionborrowtimeout
            '''
            result = self._values.get("connection_borrow_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def init_query(self) -> typing.Optional[builtins.str]:
            '''Add an initialization query, or modify the current one.

            You can specify one or more SQL statements for the proxy to run when opening each new database connection. The setting is typically used with ``SET`` statements to make sure that each connection has identical settings. Make sure the query added here is valid. This is an optional field, so you can choose to leave it empty. For including multiple variables in a single SET statement, use a comma separator.

            For example: ``SET variable1=value1, variable2=value2``

            Default: no initialization query
            .. epigraph::

               Since you can access initialization query as part of target group configuration, it is not protected by authentication or cryptographic methods. Anyone with access to view or manage your proxy target group configuration can view the initialization query. You should not add sensitive data, such as passwords or long-lived encryption keys, to this option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat-initquery
            '''
            result = self._values.get("init_query")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_connections_percent(self) -> typing.Optional[jsii.Number]:
            '''The maximum size of the connection pool for each target in a target group.

            The value is expressed as a percentage of the ``max_connections`` setting for the RDS DB instance or Aurora DB cluster used by the target group.

            If you specify ``MaxIdleConnectionsPercent`` , then you must also include a value for this parameter.

            Default: ``10`` for RDS for Microsoft SQL Server, and ``100`` for all other engines

            Constraints:

            - Must be between 1 and 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat-maxconnectionspercent
            '''
            result = self._values.get("max_connections_percent")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_idle_connections_percent(self) -> typing.Optional[jsii.Number]:
            '''A value that controls how actively the proxy closes idle database connections in the connection pool.

            The value is expressed as a percentage of the ``max_connections`` setting for the RDS DB instance or Aurora DB cluster used by the target group. With a high value, the proxy leaves a high percentage of idle database connections open. A low value causes the proxy to close more idle connections and return them to the database.

            If you specify this parameter, then you must also include a value for ``MaxConnectionsPercent`` .

            Default: The default value is half of the value of ``MaxConnectionsPercent`` . For example, if ``MaxConnectionsPercent`` is 80, then the default value of ``MaxIdleConnectionsPercent`` is 40. If the value of ``MaxConnectionsPercent`` isn't specified, then for SQL Server, ``MaxIdleConnectionsPercent`` is ``5`` , and for all other engines, the default is ``50`` .

            Constraints:

            - Must be between 0 and the value of ``MaxConnectionsPercent`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat-maxidleconnectionspercent
            '''
            result = self._values.get("max_idle_connections_percent")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def session_pinning_filters(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection.

            Including an item in the list exempts that class of SQL operations from the pinning behavior.

            Default: no session pinning filters

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat-sessionpinningfilters
            '''
            result = self._values.get("session_pinning_filters")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionPoolConfigurationInfoFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBSecurityGroupIngressMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidrip": "cidrip",
        "db_security_group_name": "dbSecurityGroupName",
        "ec2_security_group_id": "ec2SecurityGroupId",
        "ec2_security_group_name": "ec2SecurityGroupName",
        "ec2_security_group_owner_id": "ec2SecurityGroupOwnerId",
    },
)
class CfnDBSecurityGroupIngressMixinProps:
    def __init__(
        self,
        *,
        cidrip: typing.Optional[builtins.str] = None,
        db_security_group_name: typing.Optional[builtins.str] = None,
        ec2_security_group_id: typing.Optional[builtins.str] = None,
        ec2_security_group_name: typing.Optional[builtins.str] = None,
        ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDBSecurityGroupIngressPropsMixin.

        :param cidrip: The IP range to authorize.
        :param db_security_group_name: The name of the DB security group to add authorization to.
        :param ec2_security_group_id: Id of the EC2 security group to authorize. For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.
        :param ec2_security_group_name: Name of the EC2 security group to authorize. For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.
        :param ec2_security_group_owner_id: AWS account number of the owner of the EC2 security group specified in the ``EC2SecurityGroupName`` parameter. The AWS access key ID isn't an acceptable value. For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroupingress.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_dBSecurity_group_ingress_mixin_props = rds_mixins.CfnDBSecurityGroupIngressMixinProps(
                cidrip="cidrip",
                db_security_group_name="dbSecurityGroupName",
                ec2_security_group_id="ec2SecurityGroupId",
                ec2_security_group_name="ec2SecurityGroupName",
                ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67ddd8f877f9e5fe6e2f02e4fc73413ea77a40dc85bd09540b96233435d6e10)
            check_type(argname="argument cidrip", value=cidrip, expected_type=type_hints["cidrip"])
            check_type(argname="argument db_security_group_name", value=db_security_group_name, expected_type=type_hints["db_security_group_name"])
            check_type(argname="argument ec2_security_group_id", value=ec2_security_group_id, expected_type=type_hints["ec2_security_group_id"])
            check_type(argname="argument ec2_security_group_name", value=ec2_security_group_name, expected_type=type_hints["ec2_security_group_name"])
            check_type(argname="argument ec2_security_group_owner_id", value=ec2_security_group_owner_id, expected_type=type_hints["ec2_security_group_owner_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidrip is not None:
            self._values["cidrip"] = cidrip
        if db_security_group_name is not None:
            self._values["db_security_group_name"] = db_security_group_name
        if ec2_security_group_id is not None:
            self._values["ec2_security_group_id"] = ec2_security_group_id
        if ec2_security_group_name is not None:
            self._values["ec2_security_group_name"] = ec2_security_group_name
        if ec2_security_group_owner_id is not None:
            self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

    @builtins.property
    def cidrip(self) -> typing.Optional[builtins.str]:
        '''The IP range to authorize.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroupingress.html#cfn-rds-dbsecuritygroupingress-cidrip
        '''
        result = self._values.get("cidrip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_security_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the DB security group to add authorization to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroupingress.html#cfn-rds-dbsecuritygroupingress-dbsecuritygroupname
        '''
        result = self._values.get("db_security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_security_group_id(self) -> typing.Optional[builtins.str]:
        '''Id of the EC2 security group to authorize.

        For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroupingress.html#cfn-rds-dbsecuritygroupingress-ec2securitygroupid
        '''
        result = self._values.get("ec2_security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_security_group_name(self) -> typing.Optional[builtins.str]:
        '''Name of the EC2 security group to authorize.

        For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroupingress.html#cfn-rds-dbsecuritygroupingress-ec2securitygroupname
        '''
        result = self._values.get("ec2_security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_security_group_owner_id(self) -> typing.Optional[builtins.str]:
        '''AWS account number of the owner of the EC2 security group specified in the ``EC2SecurityGroupName`` parameter.

        The AWS access key ID isn't an acceptable value. For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroupingress.html#cfn-rds-dbsecuritygroupingress-ec2securitygroupownerid
        '''
        result = self._values.get("ec2_security_group_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBSecurityGroupIngressMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDBSecurityGroupIngressPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBSecurityGroupIngressPropsMixin",
):
    '''The ``AWS::RDS::DBSecurityGroupIngress`` resource enables ingress to a DB security group using one of two forms of authorization.

    First, you can add EC2 or VPC security groups to the DB security group if the application using the database is running on EC2 or VPC instances. Second, IP ranges are available if the application accessing your database is running on the Internet.

    This type supports updates. For more information about updating stacks, see `AWS CloudFormation Stacks Updates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks.html>`_ .

    For details about the settings for DB security group ingress, see `AuthorizeDBSecurityGroupIngress <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_AuthorizeDBSecurityGroupIngress.html>`_ .
    .. epigraph::

       EC2-Classic was retired on August 15, 2022. If you haven't migrated from EC2-Classic to a VPC, we recommend that you migrate as soon as possible. For more information, see `Migrate from EC2-Classic to a VPC <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/vpc-migrate.html>`_ in the *Amazon EC2 User Guide* , the blog `EC2-Classic Networking is Retiring – Here’s How to Prepare <https://docs.aws.amazon.com/aws/ec2-classic-is-retiring-heres-how-to-prepare/>`_ , and `Moving a DB instance not in a VPC into a VPC <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.Non-VPC2VPC.html>`_ in the *Amazon RDS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroupingress.html
    :cloudformationResource: AWS::RDS::DBSecurityGroupIngress
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_dBSecurity_group_ingress_props_mixin = rds_mixins.CfnDBSecurityGroupIngressPropsMixin(rds_mixins.CfnDBSecurityGroupIngressMixinProps(
            cidrip="cidrip",
            db_security_group_name="dbSecurityGroupName",
            ec2_security_group_id="ec2SecurityGroupId",
            ec2_security_group_name="ec2SecurityGroupName",
            ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDBSecurityGroupIngressMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBSecurityGroupIngress``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ca657d061512f1f1199dc2c645a8479ef2f58dae01bd78779483ee66d7472e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76d64303477785df92102d08061cff5275bf474184612b8632ff3fab96539867)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40602c6356a6747a819d095043c2b91ab4fc7b4838b2481f041307462b7a8289)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBSecurityGroupIngressMixinProps:
        return typing.cast(CfnDBSecurityGroupIngressMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBSecurityGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_security_group_ingress": "dbSecurityGroupIngress",
        "ec2_vpc_id": "ec2VpcId",
        "group_description": "groupDescription",
        "tags": "tags",
    },
)
class CfnDBSecurityGroupMixinProps:
    def __init__(
        self,
        *,
        db_security_group_ingress: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDBSecurityGroupPropsMixin.IngressProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ec2_vpc_id: typing.Optional[builtins.str] = None,
        group_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDBSecurityGroupPropsMixin.

        :param db_security_group_ingress: Ingress rules to be applied to the DB security group.
        :param ec2_vpc_id: The identifier of an Amazon virtual private cloud (VPC). This property indicates the VPC that this DB security group belongs to. .. epigraph:: This property is included for backwards compatibility and is no longer recommended for providing security information to an RDS DB instance.
        :param group_description: Provides the description of the DB security group.
        :param tags: Metadata assigned to an Amazon RDS resource consisting of a key-value pair. For more information, see `Tagging Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html>`_ in the *Amazon RDS User Guide* or `Tagging Amazon Aurora and Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_Tagging.html>`_ in the *Amazon Aurora User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_dBSecurity_group_mixin_props = rds_mixins.CfnDBSecurityGroupMixinProps(
                db_security_group_ingress=[rds_mixins.CfnDBSecurityGroupPropsMixin.IngressProperty(
                    cidrip="cidrip",
                    ec2_security_group_id="ec2SecurityGroupId",
                    ec2_security_group_name="ec2SecurityGroupName",
                    ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
                )],
                ec2_vpc_id="ec2VpcId",
                group_description="groupDescription",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c6ede1f8723fb4f4b340bd0591ada4f3e3de17908b32c22217203dd392baa3f)
            check_type(argname="argument db_security_group_ingress", value=db_security_group_ingress, expected_type=type_hints["db_security_group_ingress"])
            check_type(argname="argument ec2_vpc_id", value=ec2_vpc_id, expected_type=type_hints["ec2_vpc_id"])
            check_type(argname="argument group_description", value=group_description, expected_type=type_hints["group_description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if db_security_group_ingress is not None:
            self._values["db_security_group_ingress"] = db_security_group_ingress
        if ec2_vpc_id is not None:
            self._values["ec2_vpc_id"] = ec2_vpc_id
        if group_description is not None:
            self._values["group_description"] = group_description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def db_security_group_ingress(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBSecurityGroupPropsMixin.IngressProperty"]]]]:
        '''Ingress rules to be applied to the DB security group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroup.html#cfn-rds-dbsecuritygroup-dbsecuritygroupingress
        '''
        result = self._values.get("db_security_group_ingress")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDBSecurityGroupPropsMixin.IngressProperty"]]]], result)

    @builtins.property
    def ec2_vpc_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of an Amazon virtual private cloud (VPC).

        This property indicates the VPC that this DB security group belongs to.
        .. epigraph::

           This property is included for backwards compatibility and is no longer recommended for providing security information to an RDS DB instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroup.html#cfn-rds-dbsecuritygroup-ec2vpcid
        '''
        result = self._values.get("ec2_vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_description(self) -> typing.Optional[builtins.str]:
        '''Provides the description of the DB security group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroup.html#cfn-rds-dbsecuritygroup-groupdescription
        '''
        result = self._values.get("group_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata assigned to an Amazon RDS resource consisting of a key-value pair.

        For more information, see `Tagging Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html>`_ in the *Amazon RDS User Guide* or `Tagging Amazon Aurora and Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_Tagging.html>`_ in the *Amazon Aurora User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroup.html#cfn-rds-dbsecuritygroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBSecurityGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDBSecurityGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBSecurityGroupPropsMixin",
):
    '''The ``AWS::RDS::DBSecurityGroup`` resource creates or updates an Amazon RDS DB security group.

    .. epigraph::

       EC2-Classic was retired on August 15, 2022. If you haven't migrated from EC2-Classic to a VPC, we recommend that you migrate as soon as possible. For more information, see `Migrate from EC2-Classic to a VPC <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/vpc-migrate.html>`_ in the *Amazon EC2 User Guide* , the blog `EC2-Classic Networking is Retiring – Here’s How to Prepare <https://docs.aws.amazon.com/aws/ec2-classic-is-retiring-heres-how-to-prepare/>`_ , and `Moving a DB instance not in a VPC into a VPC <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.Non-VPC2VPC.html>`_ in the *Amazon RDS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsecuritygroup.html
    :cloudformationResource: AWS::RDS::DBSecurityGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_dBSecurity_group_props_mixin = rds_mixins.CfnDBSecurityGroupPropsMixin(rds_mixins.CfnDBSecurityGroupMixinProps(
            db_security_group_ingress=[rds_mixins.CfnDBSecurityGroupPropsMixin.IngressProperty(
                cidrip="cidrip",
                ec2_security_group_id="ec2SecurityGroupId",
                ec2_security_group_name="ec2SecurityGroupName",
                ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
            )],
            ec2_vpc_id="ec2VpcId",
            group_description="groupDescription",
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
        props: typing.Union[CfnDBSecurityGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBSecurityGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13553d76ce4b9c462e125e9b91784d2e519f304cfb3c4371e8dd00d324abad33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceca4698b8e7a98a5d4397bed06858d17f2f4f07ed339e5ff4b048f19a2dc800)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415b1c1c9b28ab9b0b3259971bfc5f5b12b4d1c82bd2e0c74819ab3ce9041022)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBSecurityGroupMixinProps:
        return typing.cast(CfnDBSecurityGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBSecurityGroupPropsMixin.IngressProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cidrip": "cidrip",
            "ec2_security_group_id": "ec2SecurityGroupId",
            "ec2_security_group_name": "ec2SecurityGroupName",
            "ec2_security_group_owner_id": "ec2SecurityGroupOwnerId",
        },
    )
    class IngressProperty:
        def __init__(
            self,
            *,
            cidrip: typing.Optional[builtins.str] = None,
            ec2_security_group_id: typing.Optional[builtins.str] = None,
            ec2_security_group_name: typing.Optional[builtins.str] = None,
            ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Ingress`` property type specifies an individual ingress rule within an ``AWS::RDS::DBSecurityGroup`` resource.

            .. epigraph::

               EC2-Classic was retired on August 15, 2022. If you haven't migrated from EC2-Classic to a VPC, we recommend that you migrate as soon as possible. For more information, see `Migrate from EC2-Classic to a VPC <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/vpc-migrate.html>`_ in the *Amazon EC2 User Guide* , the blog `EC2-Classic Networking is Retiring – Here’s How to Prepare <https://docs.aws.amazon.com/aws/ec2-classic-is-retiring-heres-how-to-prepare/>`_ , and `Moving a DB instance not in a VPC into a VPC <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.Non-VPC2VPC.html>`_ in the *Amazon RDS User Guide* .

            :param cidrip: The IP range to authorize.
            :param ec2_security_group_id: Id of the EC2 security group to authorize. For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.
            :param ec2_security_group_name: Name of the EC2 security group to authorize. For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.
            :param ec2_security_group_owner_id: AWS account number of the owner of the EC2 security group specified in the ``EC2SecurityGroupName`` parameter. The AWS access key ID isn't an acceptable value. For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbsecuritygroup-ingress.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                ingress_property = rds_mixins.CfnDBSecurityGroupPropsMixin.IngressProperty(
                    cidrip="cidrip",
                    ec2_security_group_id="ec2SecurityGroupId",
                    ec2_security_group_name="ec2SecurityGroupName",
                    ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b254b017ba7906cc32a81703e906afdcae801104f6b58e9a6f3907398512db10)
                check_type(argname="argument cidrip", value=cidrip, expected_type=type_hints["cidrip"])
                check_type(argname="argument ec2_security_group_id", value=ec2_security_group_id, expected_type=type_hints["ec2_security_group_id"])
                check_type(argname="argument ec2_security_group_name", value=ec2_security_group_name, expected_type=type_hints["ec2_security_group_name"])
                check_type(argname="argument ec2_security_group_owner_id", value=ec2_security_group_owner_id, expected_type=type_hints["ec2_security_group_owner_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidrip is not None:
                self._values["cidrip"] = cidrip
            if ec2_security_group_id is not None:
                self._values["ec2_security_group_id"] = ec2_security_group_id
            if ec2_security_group_name is not None:
                self._values["ec2_security_group_name"] = ec2_security_group_name
            if ec2_security_group_owner_id is not None:
                self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

        @builtins.property
        def cidrip(self) -> typing.Optional[builtins.str]:
            '''The IP range to authorize.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbsecuritygroup-ingress.html#cfn-rds-dbsecuritygroup-ingress-cidrip
            '''
            result = self._values.get("cidrip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ec2_security_group_id(self) -> typing.Optional[builtins.str]:
            '''Id of the EC2 security group to authorize.

            For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbsecuritygroup-ingress.html#cfn-rds-dbsecuritygroup-ingress-ec2securitygroupid
            '''
            result = self._values.get("ec2_security_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ec2_security_group_name(self) -> typing.Optional[builtins.str]:
            '''Name of the EC2 security group to authorize.

            For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbsecuritygroup-ingress.html#cfn-rds-dbsecuritygroup-ingress-ec2securitygroupname
            '''
            result = self._values.get("ec2_security_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ec2_security_group_owner_id(self) -> typing.Optional[builtins.str]:
            '''AWS account number of the owner of the EC2 security group specified in the ``EC2SecurityGroupName`` parameter.

            The AWS access key ID isn't an acceptable value. For VPC DB security groups, ``EC2SecurityGroupId`` must be provided. Otherwise, ``EC2SecurityGroupOwnerId`` and either ``EC2SecurityGroupName`` or ``EC2SecurityGroupId`` must be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbsecuritygroup-ingress.html#cfn-rds-dbsecuritygroup-ingress-ec2securitygroupownerid
            '''
            result = self._values.get("ec2_security_group_owner_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBShardGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_redundancy": "computeRedundancy",
        "db_cluster_identifier": "dbClusterIdentifier",
        "db_shard_group_identifier": "dbShardGroupIdentifier",
        "max_acu": "maxAcu",
        "min_acu": "minAcu",
        "publicly_accessible": "publiclyAccessible",
        "tags": "tags",
    },
)
class CfnDBShardGroupMixinProps:
    def __init__(
        self,
        *,
        compute_redundancy: typing.Optional[jsii.Number] = None,
        db_cluster_identifier: typing.Optional[builtins.str] = None,
        db_shard_group_identifier: typing.Optional[builtins.str] = None,
        max_acu: typing.Optional[jsii.Number] = None,
        min_acu: typing.Optional[jsii.Number] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDBShardGroupPropsMixin.

        :param compute_redundancy: Specifies whether to create standby standby DB data access shard for the DB shard group. Valid values are the following: - 0 - Creates a DB shard group without a standby DB data access shard. This is the default value. - 1 - Creates a DB shard group with a standby DB data access shard in a different Availability Zone (AZ). - 2 - Creates a DB shard group with two standby DB data access shard in two different AZs.
        :param db_cluster_identifier: The name of the primary DB cluster for the DB shard group.
        :param db_shard_group_identifier: The name of the DB shard group.
        :param max_acu: The maximum capacity of the DB shard group in Aurora capacity units (ACUs).
        :param min_acu: The minimum capacity of the DB shard group in Aurora capacity units (ACUs).
        :param publicly_accessible: Specifies whether the DB shard group is publicly accessible. When the DB shard group is publicly accessible, its Domain Name System (DNS) endpoint resolves to the private IP address from within the DB shard group's virtual private cloud (VPC). It resolves to the public IP address from outside of the DB shard group's VPC. Access to the DB shard group is ultimately controlled by the security group it uses. That public access is not permitted if the security group assigned to the DB shard group doesn't permit it. When the DB shard group isn't publicly accessible, it is an internal DB shard group with a DNS name that resolves to a private IP address. Default: The default behavior varies depending on whether ``DBSubnetGroupName`` is specified. If ``DBSubnetGroupName`` isn't specified, and ``PubliclyAccessible`` isn't specified, the following applies: - If the default VPC in the target Region doesn’t have an internet gateway attached to it, the DB shard group is private. - If the default VPC in the target Region has an internet gateway attached to it, the DB shard group is public. If ``DBSubnetGroupName`` is specified, and ``PubliclyAccessible`` isn't specified, the following applies: - If the subnets are part of a VPC that doesn’t have an internet gateway attached to it, the DB shard group is private. - If the subnets are part of a VPC that has an internet gateway attached to it, the DB shard group is public.
        :param tags: An optional set of key-value pairs to associate arbitrary data of your choosing with the DB shard group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbshardgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_dBShard_group_mixin_props = rds_mixins.CfnDBShardGroupMixinProps(
                compute_redundancy=123,
                db_cluster_identifier="dbClusterIdentifier",
                db_shard_group_identifier="dbShardGroupIdentifier",
                max_acu=123,
                min_acu=123,
                publicly_accessible=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e457d12ecf98905e4ca91e749ffec080dda50fc6d2d3d65a7a7dd1fc3a48a06)
            check_type(argname="argument compute_redundancy", value=compute_redundancy, expected_type=type_hints["compute_redundancy"])
            check_type(argname="argument db_cluster_identifier", value=db_cluster_identifier, expected_type=type_hints["db_cluster_identifier"])
            check_type(argname="argument db_shard_group_identifier", value=db_shard_group_identifier, expected_type=type_hints["db_shard_group_identifier"])
            check_type(argname="argument max_acu", value=max_acu, expected_type=type_hints["max_acu"])
            check_type(argname="argument min_acu", value=min_acu, expected_type=type_hints["min_acu"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_redundancy is not None:
            self._values["compute_redundancy"] = compute_redundancy
        if db_cluster_identifier is not None:
            self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_shard_group_identifier is not None:
            self._values["db_shard_group_identifier"] = db_shard_group_identifier
        if max_acu is not None:
            self._values["max_acu"] = max_acu
        if min_acu is not None:
            self._values["min_acu"] = min_acu
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def compute_redundancy(self) -> typing.Optional[jsii.Number]:
        '''Specifies whether to create standby standby DB data access shard for the DB shard group.

        Valid values are the following:

        - 0 - Creates a DB shard group without a standby DB data access shard. This is the default value.
        - 1 - Creates a DB shard group with a standby DB data access shard in a different Availability Zone (AZ).
        - 2 - Creates a DB shard group with two standby DB data access shard in two different AZs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbshardgroup.html#cfn-rds-dbshardgroup-computeredundancy
        '''
        result = self._values.get("compute_redundancy")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The name of the primary DB cluster for the DB shard group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbshardgroup.html#cfn-rds-dbshardgroup-dbclusteridentifier
        '''
        result = self._values.get("db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_shard_group_identifier(self) -> typing.Optional[builtins.str]:
        '''The name of the DB shard group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbshardgroup.html#cfn-rds-dbshardgroup-dbshardgroupidentifier
        '''
        result = self._values.get("db_shard_group_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_acu(self) -> typing.Optional[jsii.Number]:
        '''The maximum capacity of the DB shard group in Aurora capacity units (ACUs).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbshardgroup.html#cfn-rds-dbshardgroup-maxacu
        '''
        result = self._values.get("max_acu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_acu(self) -> typing.Optional[jsii.Number]:
        '''The minimum capacity of the DB shard group in Aurora capacity units (ACUs).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbshardgroup.html#cfn-rds-dbshardgroup-minacu
        '''
        result = self._values.get("min_acu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the DB shard group is publicly accessible.

        When the DB shard group is publicly accessible, its Domain Name System (DNS) endpoint resolves to the private IP address from within the DB shard group's virtual private cloud (VPC). It resolves to the public IP address from outside of the DB shard group's VPC. Access to the DB shard group is ultimately controlled by the security group it uses. That public access is not permitted if the security group assigned to the DB shard group doesn't permit it.

        When the DB shard group isn't publicly accessible, it is an internal DB shard group with a DNS name that resolves to a private IP address.

        Default: The default behavior varies depending on whether ``DBSubnetGroupName`` is specified.

        If ``DBSubnetGroupName`` isn't specified, and ``PubliclyAccessible`` isn't specified, the following applies:

        - If the default VPC in the target Region doesn’t have an internet gateway attached to it, the DB shard group is private.
        - If the default VPC in the target Region has an internet gateway attached to it, the DB shard group is public.

        If ``DBSubnetGroupName`` is specified, and ``PubliclyAccessible`` isn't specified, the following applies:

        - If the subnets are part of a VPC that doesn’t have an internet gateway attached to it, the DB shard group is private.
        - If the subnets are part of a VPC that has an internet gateway attached to it, the DB shard group is public.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbshardgroup.html#cfn-rds-dbshardgroup-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional set of key-value pairs to associate arbitrary data of your choosing with the DB shard group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbshardgroup.html#cfn-rds-dbshardgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBShardGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDBShardGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBShardGroupPropsMixin",
):
    '''Creates a new DB shard group for Aurora Limitless Database.

    You must enable Aurora Limitless Database to create a DB shard group.

    Valid for: Aurora DB clusters only

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbshardgroup.html
    :cloudformationResource: AWS::RDS::DBShardGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_dBShard_group_props_mixin = rds_mixins.CfnDBShardGroupPropsMixin(rds_mixins.CfnDBShardGroupMixinProps(
            compute_redundancy=123,
            db_cluster_identifier="dbClusterIdentifier",
            db_shard_group_identifier="dbShardGroupIdentifier",
            max_acu=123,
            min_acu=123,
            publicly_accessible=False,
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
        props: typing.Union[CfnDBShardGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBShardGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7cc015a896c281ee277dde4bf45ed8d866881cba4fb3b1a9d3ed1f02bfa8c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee2301fcafc0b4fd7245b79e442ee1eb04ce53a047aea0052c35ae6ac15b8a8d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d05cefe685a97678f5cee490d57c2228d0e57d0c97bc7fa6296f0c0bd06ea5b1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBShardGroupMixinProps:
        return typing.cast(CfnDBShardGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBSubnetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_subnet_group_description": "dbSubnetGroupDescription",
        "db_subnet_group_name": "dbSubnetGroupName",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnDBSubnetGroupMixinProps:
    def __init__(
        self,
        *,
        db_subnet_group_description: typing.Optional[builtins.str] = None,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDBSubnetGroupPropsMixin.

        :param db_subnet_group_description: The description for the DB subnet group.
        :param db_subnet_group_name: The name for the DB subnet group. This value is stored as a lowercase string. Constraints: - Must contain no more than 255 letters, numbers, periods, underscores, spaces, or hyphens. - Must not be default. - First character must be a letter. Example: ``mydbsubnetgroup``
        :param subnet_ids: The EC2 Subnet IDs for the DB subnet group.
        :param tags: Tags to assign to the DB subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_dBSubnet_group_mixin_props = rds_mixins.CfnDBSubnetGroupMixinProps(
                db_subnet_group_description="dbSubnetGroupDescription",
                db_subnet_group_name="dbSubnetGroupName",
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9db1a7ad1ac5a1d268713a5f661f3a5b7b9e6174b4483511086010f4e0d8b59)
            check_type(argname="argument db_subnet_group_description", value=db_subnet_group_description, expected_type=type_hints["db_subnet_group_description"])
            check_type(argname="argument db_subnet_group_name", value=db_subnet_group_name, expected_type=type_hints["db_subnet_group_name"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if db_subnet_group_description is not None:
            self._values["db_subnet_group_description"] = db_subnet_group_description
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def db_subnet_group_description(self) -> typing.Optional[builtins.str]:
        '''The description for the DB subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnetgroup.html#cfn-rds-dbsubnetgroup-dbsubnetgroupdescription
        '''
        result = self._values.get("db_subnet_group_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name for the DB subnet group. This value is stored as a lowercase string.

        Constraints:

        - Must contain no more than 255 letters, numbers, periods, underscores, spaces, or hyphens.
        - Must not be default.
        - First character must be a letter.

        Example: ``mydbsubnetgroup``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnetgroup.html#cfn-rds-dbsubnetgroup-dbsubnetgroupname
        '''
        result = self._values.get("db_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The EC2 Subnet IDs for the DB subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnetgroup.html#cfn-rds-dbsubnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the DB subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnetgroup.html#cfn-rds-dbsubnetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBSubnetGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDBSubnetGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnDBSubnetGroupPropsMixin",
):
    '''The ``AWS::RDS::DBSubnetGroup`` resource creates a database subnet group.

    Subnet groups must contain at least two subnets in two different Availability Zones in the same region.

    For more information, see `Working with DB subnet groups <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html#USER_VPC.Subnets>`_ in the *Amazon RDS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnetgroup.html
    :cloudformationResource: AWS::RDS::DBSubnetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_dBSubnet_group_props_mixin = rds_mixins.CfnDBSubnetGroupPropsMixin(rds_mixins.CfnDBSubnetGroupMixinProps(
            db_subnet_group_description="dbSubnetGroupDescription",
            db_subnet_group_name="dbSubnetGroupName",
            subnet_ids=["subnetIds"],
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
        props: typing.Union[CfnDBSubnetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::DBSubnetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd4ae444dbe4514bda7bf4afe26c4e3075bc0910d535e8e64940c3d67a30a4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06f13ea82ee1f1a6aa2b07081012bdd0fe95f070c2f8a57d573b29e0dd695802)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c0337614ee85c975bee5f06a809142803d4601119fe51e15a00787ddce95de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDBSubnetGroupMixinProps:
        return typing.cast(CfnDBSubnetGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnEventSubscriptionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "event_categories": "eventCategories",
        "sns_topic_arn": "snsTopicArn",
        "source_ids": "sourceIds",
        "source_type": "sourceType",
        "subscription_name": "subscriptionName",
        "tags": "tags",
    },
)
class CfnEventSubscriptionMixinProps:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        event_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        sns_topic_arn: typing.Optional[builtins.str] = None,
        source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_type: typing.Optional[builtins.str] = None,
        subscription_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEventSubscriptionPropsMixin.

        :param enabled: Specifies whether to activate the subscription. If the event notification subscription isn't activated, the subscription is created but not active. Default: - true
        :param event_categories: A list of event categories for a particular source type ( ``SourceType`` ) that you want to subscribe to. You can see a list of the categories for a given source type in the "Amazon RDS event categories and event messages" section of the `*Amazon RDS User Guide* <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.Messages.html>`_ or the `*Amazon Aurora User Guide* <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_Events.Messages.html>`_ . You can also see this list by using the ``DescribeEventCategories`` operation.
        :param sns_topic_arn: The Amazon Resource Name (ARN) of the SNS topic created for event notification. SNS automatically creates the ARN when you create a topic and subscribe to it. .. epigraph:: RDS doesn't support FIFO (first in, first out) topics. For more information, see `Message ordering and deduplication (FIFO topics) <https://docs.aws.amazon.com/sns/latest/dg/sns-fifo-topics.html>`_ in the *Amazon Simple Notification Service Developer Guide* .
        :param source_ids: The list of identifiers of the event sources for which events are returned. If not specified, then all sources are included in the response. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens. It can't end with a hyphen or contain two consecutive hyphens. Constraints: - If ``SourceIds`` are supplied, ``SourceType`` must also be provided. - If the source type is a DB instance, a ``DBInstanceIdentifier`` value must be supplied. - If the source type is a DB cluster, a ``DBClusterIdentifier`` value must be supplied. - If the source type is a DB parameter group, a ``DBParameterGroupName`` value must be supplied. - If the source type is a DB security group, a ``DBSecurityGroupName`` value must be supplied. - If the source type is a DB snapshot, a ``DBSnapshotIdentifier`` value must be supplied. - If the source type is a DB cluster snapshot, a ``DBClusterSnapshotIdentifier`` value must be supplied. - If the source type is an RDS Proxy, a ``DBProxyName`` value must be supplied.
        :param source_type: The type of source that is generating the events. For example, if you want to be notified of events generated by a DB instance, you set this parameter to ``db-instance`` . For RDS Proxy events, specify ``db-proxy`` . If this value isn't specified, all events are returned. Valid Values: ``db-instance | db-cluster | db-parameter-group | db-security-group | db-snapshot | db-cluster-snapshot | db-proxy | zero-etl | custom-engine-version | blue-green-deployment``
        :param subscription_name: The name of the subscription. Constraints: The name must be less than 255 characters.
        :param tags: An optional array of key-value pairs to apply to this subscription.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_event_subscription_mixin_props = rds_mixins.CfnEventSubscriptionMixinProps(
                enabled=False,
                event_categories=["eventCategories"],
                sns_topic_arn="snsTopicArn",
                source_ids=["sourceIds"],
                source_type="sourceType",
                subscription_name="subscriptionName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185b22033f2e5422c0967451d8ec44a669b7ab4f4bb44182c03f2d23613ff385)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_categories", value=event_categories, expected_type=type_hints["event_categories"])
            check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
            check_type(argname="argument source_ids", value=source_ids, expected_type=type_hints["source_ids"])
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument subscription_name", value=subscription_name, expected_type=type_hints["subscription_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_categories is not None:
            self._values["event_categories"] = event_categories
        if sns_topic_arn is not None:
            self._values["sns_topic_arn"] = sns_topic_arn
        if source_ids is not None:
            self._values["source_ids"] = source_ids
        if source_type is not None:
            self._values["source_type"] = source_type
        if subscription_name is not None:
            self._values["subscription_name"] = subscription_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to activate the subscription.

        If the event notification subscription isn't activated, the subscription is created but not active.

        :default: - true

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def event_categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of event categories for a particular source type ( ``SourceType`` ) that you want to subscribe to.

        You can see a list of the categories for a given source type in the "Amazon RDS event categories and event messages" section of the `*Amazon RDS User Guide* <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.Messages.html>`_ or the `*Amazon Aurora User Guide* <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_Events.Messages.html>`_ . You can also see this list by using the ``DescribeEventCategories`` operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-eventcategories
        '''
        result = self._values.get("event_categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the SNS topic created for event notification.

        SNS automatically creates the ARN when you create a topic and subscribe to it.
        .. epigraph::

           RDS doesn't support FIFO (first in, first out) topics. For more information, see `Message ordering and deduplication (FIFO topics) <https://docs.aws.amazon.com/sns/latest/dg/sns-fifo-topics.html>`_ in the *Amazon Simple Notification Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-snstopicarn
        '''
        result = self._values.get("sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of identifiers of the event sources for which events are returned.

        If not specified, then all sources are included in the response. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens. It can't end with a hyphen or contain two consecutive hyphens.

        Constraints:

        - If ``SourceIds`` are supplied, ``SourceType`` must also be provided.
        - If the source type is a DB instance, a ``DBInstanceIdentifier`` value must be supplied.
        - If the source type is a DB cluster, a ``DBClusterIdentifier`` value must be supplied.
        - If the source type is a DB parameter group, a ``DBParameterGroupName`` value must be supplied.
        - If the source type is a DB security group, a ``DBSecurityGroupName`` value must be supplied.
        - If the source type is a DB snapshot, a ``DBSnapshotIdentifier`` value must be supplied.
        - If the source type is a DB cluster snapshot, a ``DBClusterSnapshotIdentifier`` value must be supplied.
        - If the source type is an RDS Proxy, a ``DBProxyName`` value must be supplied.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-sourceids
        '''
        result = self._values.get("source_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_type(self) -> typing.Optional[builtins.str]:
        '''The type of source that is generating the events.

        For example, if you want to be notified of events generated by a DB instance, you set this parameter to ``db-instance`` . For RDS Proxy events, specify ``db-proxy`` . If this value isn't specified, all events are returned.

        Valid Values: ``db-instance | db-cluster | db-parameter-group | db-security-group | db-snapshot | db-cluster-snapshot | db-proxy | zero-etl | custom-engine-version | blue-green-deployment``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-sourcetype
        '''
        result = self._values.get("source_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subscription.

        Constraints: The name must be less than 255 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-subscriptionname
        '''
        result = self._values.get("subscription_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional array of key-value pairs to apply to this subscription.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventSubscriptionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEventSubscriptionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnEventSubscriptionPropsMixin",
):
    '''The ``AWS::RDS::EventSubscription`` resource allows you to receive notifications for Amazon Relational Database Service events through the Amazon Simple Notification Service (Amazon SNS).

    For more information, see `Using Amazon RDS Event Notification <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.html>`_ in the *Amazon RDS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html
    :cloudformationResource: AWS::RDS::EventSubscription
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_event_subscription_props_mixin = rds_mixins.CfnEventSubscriptionPropsMixin(rds_mixins.CfnEventSubscriptionMixinProps(
            enabled=False,
            event_categories=["eventCategories"],
            sns_topic_arn="snsTopicArn",
            source_ids=["sourceIds"],
            source_type="sourceType",
            subscription_name="subscriptionName",
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
        props: typing.Union[CfnEventSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::EventSubscription``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934744984e63142f6b4505a8542d51703ffc3a358d4983d62007c87f0010da5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b09b7a6e3066181936b133b7ca9e8b28f28ed20f94b40513cd6195fdd5cfd7e5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567d7adfb774f5407205bee6d4e264b7dfac42136f97d55007ddd8c200c645e7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEventSubscriptionMixinProps:
        return typing.cast(CfnEventSubscriptionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnGlobalClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deletion_protection": "deletionProtection",
        "engine": "engine",
        "engine_lifecycle_support": "engineLifecycleSupport",
        "engine_version": "engineVersion",
        "global_cluster_identifier": "globalClusterIdentifier",
        "source_db_cluster_identifier": "sourceDbClusterIdentifier",
        "storage_encrypted": "storageEncrypted",
        "tags": "tags",
    },
)
class CfnGlobalClusterMixinProps:
    def __init__(
        self,
        *,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_lifecycle_support: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        global_cluster_identifier: typing.Optional[builtins.str] = None,
        source_db_cluster_identifier: typing.Optional[builtins.str] = None,
        storage_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGlobalClusterPropsMixin.

        :param deletion_protection: Specifies whether to enable deletion protection for the new global database cluster. The global database can't be deleted when deletion protection is enabled.
        :param engine: The database engine to use for this global database cluster. Valid Values: ``aurora-mysql | aurora-postgresql`` Constraints: - Can't be specified if ``SourceDBClusterIdentifier`` is specified. In this case, Amazon Aurora uses the engine of the source DB cluster.
        :param engine_lifecycle_support: The life cycle type for this global database cluster. .. epigraph:: By default, this value is set to ``open-source-rds-extended-support`` , which enrolls your global cluster into Amazon RDS Extended Support. At the end of standard support, you can avoid charges for Extended Support by setting the value to ``open-source-rds-extended-support-disabled`` . In this case, creating the global cluster will fail if the DB major version is past its end of standard support date. This setting only applies to Aurora PostgreSQL-based global databases. You can use this setting to enroll your global cluster into Amazon RDS Extended Support. With RDS Extended Support, you can run the selected major engine version on your global cluster past the end of standard support for that engine version. For more information, see `Amazon RDS Extended Support with Amazon Aurora <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/extended-support.html>`_ in the *Amazon Aurora User Guide* . Valid Values: ``open-source-rds-extended-support | open-source-rds-extended-support-disabled`` Default: ``open-source-rds-extended-support``
        :param engine_version: The engine version to use for this global database cluster. Constraints: - Can't be specified if ``SourceDBClusterIdentifier`` is specified. In this case, Amazon Aurora uses the engine version of the source DB cluster.
        :param global_cluster_identifier: The cluster identifier for this global database cluster. This parameter is stored as a lowercase string.
        :param source_db_cluster_identifier: The Amazon Resource Name (ARN) to use as the primary cluster of the global database. If you provide a value for this parameter, don't specify values for the following settings because Amazon Aurora uses the values from the specified source DB cluster: - ``DatabaseName`` - ``Engine`` - ``EngineVersion`` - ``StorageEncrypted``
        :param storage_encrypted: Specifies whether to enable storage encryption for the new global database cluster. Constraints: - Can't be specified if ``SourceDBClusterIdentifier`` is specified. In this case, Amazon Aurora uses the setting from the source DB cluster.
        :param tags: Metadata assigned to an Amazon RDS resource consisting of a key-value pair. For more information, see `Tagging Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html>`_ in the *Amazon RDS User Guide* or `Tagging Amazon Aurora and Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_Tagging.html>`_ in the *Amazon Aurora User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_global_cluster_mixin_props = rds_mixins.CfnGlobalClusterMixinProps(
                deletion_protection=False,
                engine="engine",
                engine_lifecycle_support="engineLifecycleSupport",
                engine_version="engineVersion",
                global_cluster_identifier="globalClusterIdentifier",
                source_db_cluster_identifier="sourceDbClusterIdentifier",
                storage_encrypted=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e12cf738de37d57c7c007c82a838ecaefc8adee5dffafe16ffa1a26ec820b1)
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_lifecycle_support", value=engine_lifecycle_support, expected_type=type_hints["engine_lifecycle_support"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument global_cluster_identifier", value=global_cluster_identifier, expected_type=type_hints["global_cluster_identifier"])
            check_type(argname="argument source_db_cluster_identifier", value=source_db_cluster_identifier, expected_type=type_hints["source_db_cluster_identifier"])
            check_type(argname="argument storage_encrypted", value=storage_encrypted, expected_type=type_hints["storage_encrypted"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if engine is not None:
            self._values["engine"] = engine
        if engine_lifecycle_support is not None:
            self._values["engine_lifecycle_support"] = engine_lifecycle_support
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if global_cluster_identifier is not None:
            self._values["global_cluster_identifier"] = global_cluster_identifier
        if source_db_cluster_identifier is not None:
            self._values["source_db_cluster_identifier"] = source_db_cluster_identifier
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable deletion protection for the new global database cluster.

        The global database can't be deleted when deletion protection is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html#cfn-rds-globalcluster-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The database engine to use for this global database cluster.

        Valid Values: ``aurora-mysql | aurora-postgresql``

        Constraints:

        - Can't be specified if ``SourceDBClusterIdentifier`` is specified. In this case, Amazon Aurora uses the engine of the source DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html#cfn-rds-globalcluster-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_lifecycle_support(self) -> typing.Optional[builtins.str]:
        '''The life cycle type for this global database cluster.

        .. epigraph::

           By default, this value is set to ``open-source-rds-extended-support`` , which enrolls your global cluster into Amazon RDS Extended Support. At the end of standard support, you can avoid charges for Extended Support by setting the value to ``open-source-rds-extended-support-disabled`` . In this case, creating the global cluster will fail if the DB major version is past its end of standard support date.

        This setting only applies to Aurora PostgreSQL-based global databases.

        You can use this setting to enroll your global cluster into Amazon RDS Extended Support. With RDS Extended Support, you can run the selected major engine version on your global cluster past the end of standard support for that engine version. For more information, see `Amazon RDS Extended Support with Amazon Aurora <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/extended-support.html>`_ in the *Amazon Aurora User Guide* .

        Valid Values: ``open-source-rds-extended-support | open-source-rds-extended-support-disabled``

        Default: ``open-source-rds-extended-support``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html#cfn-rds-globalcluster-enginelifecyclesupport
        '''
        result = self._values.get("engine_lifecycle_support")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The engine version to use for this global database cluster.

        Constraints:

        - Can't be specified if ``SourceDBClusterIdentifier`` is specified. In this case, Amazon Aurora uses the engine version of the source DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html#cfn-rds-globalcluster-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The cluster identifier for this global database cluster.

        This parameter is stored as a lowercase string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html#cfn-rds-globalcluster-globalclusteridentifier
        '''
        result = self._values.get("global_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) to use as the primary cluster of the global database.

        If you provide a value for this parameter, don't specify values for the following settings because Amazon Aurora uses the values from the specified source DB cluster:

        - ``DatabaseName``
        - ``Engine``
        - ``EngineVersion``
        - ``StorageEncrypted``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html#cfn-rds-globalcluster-sourcedbclusteridentifier
        '''
        result = self._values.get("source_db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to enable storage encryption for the new global database cluster.

        Constraints:

        - Can't be specified if ``SourceDBClusterIdentifier`` is specified. In this case, Amazon Aurora uses the setting from the source DB cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html#cfn-rds-globalcluster-storageencrypted
        '''
        result = self._values.get("storage_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata assigned to an Amazon RDS resource consisting of a key-value pair.

        For more information, see `Tagging Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html>`_ in the *Amazon RDS User Guide* or `Tagging Amazon Aurora and Amazon RDS resources <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_Tagging.html>`_ in the *Amazon Aurora User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html#cfn-rds-globalcluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGlobalClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGlobalClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnGlobalClusterPropsMixin",
):
    '''The ``AWS::RDS::GlobalCluster`` resource creates or updates an Amazon Aurora global database spread across multiple AWS Regions.

    The global database contains a single primary cluster with read-write capability, and a read-only secondary cluster that receives data from the primary cluster through high-speed replication performed by the Aurora storage subsystem.

    You can create a global database that is initially empty, and then add a primary cluster and a secondary cluster to it.

    For information about Aurora global databases, see `Working with Amazon Aurora Global Databases <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html>`_ in the *Amazon Aurora User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-globalcluster.html
    :cloudformationResource: AWS::RDS::GlobalCluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_global_cluster_props_mixin = rds_mixins.CfnGlobalClusterPropsMixin(rds_mixins.CfnGlobalClusterMixinProps(
            deletion_protection=False,
            engine="engine",
            engine_lifecycle_support="engineLifecycleSupport",
            engine_version="engineVersion",
            global_cluster_identifier="globalClusterIdentifier",
            source_db_cluster_identifier="sourceDbClusterIdentifier",
            storage_encrypted=False,
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
        props: typing.Union[CfnGlobalClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::GlobalCluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12046e3c4a90a2e675e17eb1e57411d1a3aec88d476e5bb07dfe1d0bd3e39b6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bef7af265da11034876438d29f49dc44083eb6eb9985d4783cf2d736903ff6a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ebd365c9ff5aa90534e1f37815d2586ef857128a462ad0134b852bd87d7563f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGlobalClusterMixinProps:
        return typing.cast(CfnGlobalClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnGlobalClusterPropsMixin.GlobalEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address"},
    )
    class GlobalEndpointProperty:
        def __init__(self, *, address: typing.Optional[builtins.str] = None) -> None:
            '''The writer endpoint for the new global database cluster.

            This endpoint always points to the writer DB instance in the current primary cluster.

            :param address: The writer endpoint for the new global database cluster. This endpoint always points to the writer DB instance in the current primary cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-globalcluster-globalendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                global_endpoint_property = rds_mixins.CfnGlobalClusterPropsMixin.GlobalEndpointProperty(
                    address="address"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b59b7586ecff95abfe8bfd2876307c2854434992133b5b2032db870fb9e7c8b8)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The writer endpoint for the new global database cluster.

            This endpoint always points to the writer DB instance in the current primary cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-globalcluster-globalendpoint.html#cfn-rds-globalcluster-globalendpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnIntegrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_encryption_context": "additionalEncryptionContext",
        "data_filter": "dataFilter",
        "description": "description",
        "integration_name": "integrationName",
        "kms_key_id": "kmsKeyId",
        "source_arn": "sourceArn",
        "tags": "tags",
        "target_arn": "targetArn",
    },
)
class CfnIntegrationMixinProps:
    def __init__(
        self,
        *,
        additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        data_filter: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        integration_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        source_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIntegrationPropsMixin.

        :param additional_encryption_context: An optional set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see `Encryption context <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context>`_ in the *AWS Key Management Service Developer Guide* . You can only include this parameter if you specify the ``KMSKeyId`` parameter.
        :param data_filter: Data filters for the integration. These filters determine which tables from the source database are sent to the target Amazon Redshift data warehouse.
        :param description: A description of the integration.
        :param integration_name: The name of the integration.
        :param kms_key_id: The AWS Key Management System ( AWS KMS) key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key.
        :param source_arn: The Amazon Resource Name (ARN) of the database to use as the source for replication.
        :param tags: An optional array of key-value pairs to apply to this integration.
        :param target_arn: The ARN of the Redshift data warehouse to use as the target for replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_integration_mixin_props = rds_mixins.CfnIntegrationMixinProps(
                additional_encryption_context={
                    "additional_encryption_context_key": "additionalEncryptionContext"
                },
                data_filter="dataFilter",
                description="description",
                integration_name="integrationName",
                kms_key_id="kmsKeyId",
                source_arn="sourceArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_arn="targetArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c642c7656cff1f9958ffd59c3867475ccfcaef94bb83ba65d53d2ad2cf5b1f)
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument data_filter", value=data_filter, expected_type=type_hints["data_filter"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument integration_name", value=integration_name, expected_type=type_hints["integration_name"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
        if data_filter is not None:
            self._values["data_filter"] = data_filter
        if description is not None:
            self._values["description"] = description
        if integration_name is not None:
            self._values["integration_name"] = integration_name
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if source_arn is not None:
            self._values["source_arn"] = source_arn
        if tags is not None:
            self._values["tags"] = tags
        if target_arn is not None:
            self._values["target_arn"] = target_arn

    @builtins.property
    def additional_encryption_context(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''An optional set of non-secret key–value pairs that contains additional contextual information about the data.

        For more information, see `Encryption context <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context>`_ in the *AWS Key Management Service Developer Guide* .

        You can only include this parameter if you specify the ``KMSKeyId`` parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html#cfn-rds-integration-additionalencryptioncontext
        '''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def data_filter(self) -> typing.Optional[builtins.str]:
        '''Data filters for the integration.

        These filters determine which tables from the source database are sent to the target Amazon Redshift data warehouse.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html#cfn-rds-integration-datafilter
        '''
        result = self._values.get("data_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html#cfn-rds-integration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_name(self) -> typing.Optional[builtins.str]:
        '''The name of the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html#cfn-rds-integration-integrationname
        '''
        result = self._values.get("integration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS Key Management System ( AWS KMS) key identifier for the key to use to encrypt the integration.

        If you don't specify an encryption key, RDS uses a default AWS owned key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html#cfn-rds-integration-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the database to use as the source for replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html#cfn-rds-integration-sourcearn
        '''
        result = self._values.get("source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional array of key-value pairs to apply to this integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html#cfn-rds-integration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the Redshift data warehouse to use as the target for replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html#cfn-rds-integration-targetarn
        '''
        result = self._values.get("target_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIntegrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnIntegrationPropsMixin",
):
    '''A zero-ETL integration with Amazon Redshift.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html
    :cloudformationResource: AWS::RDS::Integration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_integration_props_mixin = rds_mixins.CfnIntegrationPropsMixin(rds_mixins.CfnIntegrationMixinProps(
            additional_encryption_context={
                "additional_encryption_context_key": "additionalEncryptionContext"
            },
            data_filter="dataFilter",
            description="description",
            integration_name="integrationName",
            kms_key_id="kmsKeyId",
            source_arn="sourceArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_arn="targetArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::Integration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f7e0f4498dcbf6754fa66429c139b8ad503ce784458fd198472b7cd7e40a54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9956489aa458243367307482724ad7ec8db74aed3efc5ee7fd180afd8ce2fd21)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2d4e8606bb2b689b1b46ad9f4788a244c7c728b3fd3280272a84531009da02)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIntegrationMixinProps:
        return typing.cast(CfnIntegrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnOptionGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "engine_name": "engineName",
        "major_engine_version": "majorEngineVersion",
        "option_configurations": "optionConfigurations",
        "option_group_description": "optionGroupDescription",
        "option_group_name": "optionGroupName",
        "tags": "tags",
    },
)
class CfnOptionGroupMixinProps:
    def __init__(
        self,
        *,
        engine_name: typing.Optional[builtins.str] = None,
        major_engine_version: typing.Optional[builtins.str] = None,
        option_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOptionGroupPropsMixin.OptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        option_group_description: typing.Optional[builtins.str] = None,
        option_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOptionGroupPropsMixin.

        :param engine_name: Specifies the name of the engine that this option group should be associated with. Valid Values: - ``mariadb`` - ``mysql`` - ``oracle-ee`` - ``oracle-ee-cdb`` - ``oracle-se2`` - ``oracle-se2-cdb`` - ``postgres`` - ``sqlserver-ee`` - ``sqlserver-se`` - ``sqlserver-ex`` - ``sqlserver-web``
        :param major_engine_version: Specifies the major version of the engine that this option group should be associated with.
        :param option_configurations: A list of all available options for an option group.
        :param option_group_description: The description of the option group.
        :param option_group_name: The name of the option group to be created. Constraints: - Must be 1 to 255 letters, numbers, or hyphens - First character must be a letter - Can't end with a hyphen or contain two consecutive hyphens Example: ``myoptiongroup`` If you don't specify a value for ``OptionGroupName`` property, a name is automatically created for the option group. .. epigraph:: This value is stored as a lowercase string.
        :param tags: Tags to assign to the option group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
            
            cfn_option_group_mixin_props = rds_mixins.CfnOptionGroupMixinProps(
                engine_name="engineName",
                major_engine_version="majorEngineVersion",
                option_configurations=[rds_mixins.CfnOptionGroupPropsMixin.OptionConfigurationProperty(
                    db_security_group_memberships=["dbSecurityGroupMemberships"],
                    option_name="optionName",
                    option_settings=[rds_mixins.CfnOptionGroupPropsMixin.OptionSettingProperty(
                        name="name",
                        value="value"
                    )],
                    option_version="optionVersion",
                    port=123,
                    vpc_security_group_memberships=["vpcSecurityGroupMemberships"]
                )],
                option_group_description="optionGroupDescription",
                option_group_name="optionGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcce897aedb62a3dedd686338f69d2fdcd132f181acef5de7eda4826444784f4)
            check_type(argname="argument engine_name", value=engine_name, expected_type=type_hints["engine_name"])
            check_type(argname="argument major_engine_version", value=major_engine_version, expected_type=type_hints["major_engine_version"])
            check_type(argname="argument option_configurations", value=option_configurations, expected_type=type_hints["option_configurations"])
            check_type(argname="argument option_group_description", value=option_group_description, expected_type=type_hints["option_group_description"])
            check_type(argname="argument option_group_name", value=option_group_name, expected_type=type_hints["option_group_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if engine_name is not None:
            self._values["engine_name"] = engine_name
        if major_engine_version is not None:
            self._values["major_engine_version"] = major_engine_version
        if option_configurations is not None:
            self._values["option_configurations"] = option_configurations
        if option_group_description is not None:
            self._values["option_group_description"] = option_group_description
        if option_group_name is not None:
            self._values["option_group_name"] = option_group_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def engine_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the engine that this option group should be associated with.

        Valid Values:

        - ``mariadb``
        - ``mysql``
        - ``oracle-ee``
        - ``oracle-ee-cdb``
        - ``oracle-se2``
        - ``oracle-se2-cdb``
        - ``postgres``
        - ``sqlserver-ee``
        - ``sqlserver-se``
        - ``sqlserver-ex``
        - ``sqlserver-web``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-enginename
        '''
        result = self._values.get("engine_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def major_engine_version(self) -> typing.Optional[builtins.str]:
        '''Specifies the major version of the engine that this option group should be associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-majorengineversion
        '''
        result = self._values.get("major_engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def option_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOptionGroupPropsMixin.OptionConfigurationProperty"]]]]:
        '''A list of all available options for an option group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-optionconfigurations
        '''
        result = self._values.get("option_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOptionGroupPropsMixin.OptionConfigurationProperty"]]]], result)

    @builtins.property
    def option_group_description(self) -> typing.Optional[builtins.str]:
        '''The description of the option group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-optiongroupdescription
        '''
        result = self._values.get("option_group_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def option_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the option group to be created.

        Constraints:

        - Must be 1 to 255 letters, numbers, or hyphens
        - First character must be a letter
        - Can't end with a hyphen or contain two consecutive hyphens

        Example: ``myoptiongroup``

        If you don't specify a value for ``OptionGroupName`` property, a name is automatically created for the option group.
        .. epigraph::

           This value is stored as a lowercase string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-optiongroupname
        '''
        result = self._values.get("option_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the option group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOptionGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOptionGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnOptionGroupPropsMixin",
):
    '''The ``AWS::RDS::OptionGroup`` resource creates or updates an option group, to enable and configure features that are specific to a particular DB engine.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html
    :cloudformationResource: AWS::RDS::OptionGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
        
        cfn_option_group_props_mixin = rds_mixins.CfnOptionGroupPropsMixin(rds_mixins.CfnOptionGroupMixinProps(
            engine_name="engineName",
            major_engine_version="majorEngineVersion",
            option_configurations=[rds_mixins.CfnOptionGroupPropsMixin.OptionConfigurationProperty(
                db_security_group_memberships=["dbSecurityGroupMemberships"],
                option_name="optionName",
                option_settings=[rds_mixins.CfnOptionGroupPropsMixin.OptionSettingProperty(
                    name="name",
                    value="value"
                )],
                option_version="optionVersion",
                port=123,
                vpc_security_group_memberships=["vpcSecurityGroupMemberships"]
            )],
            option_group_description="optionGroupDescription",
            option_group_name="optionGroupName",
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
        props: typing.Union[CfnOptionGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RDS::OptionGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbca3e89f8a4275c314a4adf8ddd6402ce71787662d3baea276ce77d3bb0e3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bab1f17e634cb378394eb155c345d523d60db467cdcd29b6c5caf74ebfdff26b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__451d0abb5b771757ebbfa7e9e09e0fa59e46246e547fd248e3102475c583ec4e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOptionGroupMixinProps:
        return typing.cast(CfnOptionGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnOptionGroupPropsMixin.OptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "db_security_group_memberships": "dbSecurityGroupMemberships",
            "option_name": "optionName",
            "option_settings": "optionSettings",
            "option_version": "optionVersion",
            "port": "port",
            "vpc_security_group_memberships": "vpcSecurityGroupMemberships",
        },
    )
    class OptionConfigurationProperty:
        def __init__(
            self,
            *,
            db_security_group_memberships: typing.Optional[typing.Sequence[builtins.str]] = None,
            option_name: typing.Optional[builtins.str] = None,
            option_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOptionGroupPropsMixin.OptionSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            option_version: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            vpc_security_group_memberships: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``OptionConfiguration`` property type specifies an individual option, and its settings, within an ``AWS::RDS::OptionGroup`` resource.

            :param db_security_group_memberships: A list of DB security groups used for this option.
            :param option_name: The configuration of options to include in a group.
            :param option_settings: The option settings to include in an option group.
            :param option_version: The version for the option.
            :param port: The optional port for the option.
            :param vpc_security_group_memberships: A list of VPC security group names used for this option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                option_configuration_property = rds_mixins.CfnOptionGroupPropsMixin.OptionConfigurationProperty(
                    db_security_group_memberships=["dbSecurityGroupMemberships"],
                    option_name="optionName",
                    option_settings=[rds_mixins.CfnOptionGroupPropsMixin.OptionSettingProperty(
                        name="name",
                        value="value"
                    )],
                    option_version="optionVersion",
                    port=123,
                    vpc_security_group_memberships=["vpcSecurityGroupMemberships"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2735ce1a9dc50d8b323dab4303e0f2ac545847966863d4ef176d3be56ab3255a)
                check_type(argname="argument db_security_group_memberships", value=db_security_group_memberships, expected_type=type_hints["db_security_group_memberships"])
                check_type(argname="argument option_name", value=option_name, expected_type=type_hints["option_name"])
                check_type(argname="argument option_settings", value=option_settings, expected_type=type_hints["option_settings"])
                check_type(argname="argument option_version", value=option_version, expected_type=type_hints["option_version"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument vpc_security_group_memberships", value=vpc_security_group_memberships, expected_type=type_hints["vpc_security_group_memberships"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if db_security_group_memberships is not None:
                self._values["db_security_group_memberships"] = db_security_group_memberships
            if option_name is not None:
                self._values["option_name"] = option_name
            if option_settings is not None:
                self._values["option_settings"] = option_settings
            if option_version is not None:
                self._values["option_version"] = option_version
            if port is not None:
                self._values["port"] = port
            if vpc_security_group_memberships is not None:
                self._values["vpc_security_group_memberships"] = vpc_security_group_memberships

        @builtins.property
        def db_security_group_memberships(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of DB security groups used for this option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfiguration.html#cfn-rds-optiongroup-optionconfiguration-dbsecuritygroupmemberships
            '''
            result = self._values.get("db_security_group_memberships")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def option_name(self) -> typing.Optional[builtins.str]:
            '''The configuration of options to include in a group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfiguration.html#cfn-rds-optiongroup-optionconfiguration-optionname
            '''
            result = self._values.get("option_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def option_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOptionGroupPropsMixin.OptionSettingProperty"]]]]:
            '''The option settings to include in an option group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfiguration.html#cfn-rds-optiongroup-optionconfiguration-optionsettings
            '''
            result = self._values.get("option_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOptionGroupPropsMixin.OptionSettingProperty"]]]], result)

        @builtins.property
        def option_version(self) -> typing.Optional[builtins.str]:
            '''The version for the option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfiguration.html#cfn-rds-optiongroup-optionconfiguration-optionversion
            '''
            result = self._values.get("option_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The optional port for the option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfiguration.html#cfn-rds-optiongroup-optionconfiguration-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def vpc_security_group_memberships(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of VPC security group names used for this option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfiguration.html#cfn-rds-optiongroup-optionconfiguration-vpcsecuritygroupmemberships
            '''
            result = self._values.get("vpc_security_group_memberships")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rds.mixins.CfnOptionGroupPropsMixin.OptionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class OptionSettingProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``OptionSetting`` property type specifies the value for an option within an ``OptionSetting`` property.

            :param name: The name of the option that has settings that you can set.
            :param value: The current value of the option setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rds import mixins as rds_mixins
                
                option_setting_property = rds_mixins.CfnOptionGroupPropsMixin.OptionSettingProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4674fac63ccbe21405d738a10ac96c29899ac73e9c4187e7bd8bb89783471ae9)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the option that has settings that you can set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionsetting.html#cfn-rds-optiongroup-optionsetting-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The current value of the option setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionsetting.html#cfn-rds-optiongroup-optionsetting-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCustomDBEngineVersionMixinProps",
    "CfnCustomDBEngineVersionPropsMixin",
    "CfnDBClusterMixinProps",
    "CfnDBClusterParameterGroupMixinProps",
    "CfnDBClusterParameterGroupPropsMixin",
    "CfnDBClusterPropsMixin",
    "CfnDBInstanceMixinProps",
    "CfnDBInstancePropsMixin",
    "CfnDBParameterGroupMixinProps",
    "CfnDBParameterGroupPropsMixin",
    "CfnDBProxyEndpointMixinProps",
    "CfnDBProxyEndpointPropsMixin",
    "CfnDBProxyMixinProps",
    "CfnDBProxyPropsMixin",
    "CfnDBProxyTargetGroupMixinProps",
    "CfnDBProxyTargetGroupPropsMixin",
    "CfnDBSecurityGroupIngressMixinProps",
    "CfnDBSecurityGroupIngressPropsMixin",
    "CfnDBSecurityGroupMixinProps",
    "CfnDBSecurityGroupPropsMixin",
    "CfnDBShardGroupMixinProps",
    "CfnDBShardGroupPropsMixin",
    "CfnDBSubnetGroupMixinProps",
    "CfnDBSubnetGroupPropsMixin",
    "CfnEventSubscriptionMixinProps",
    "CfnEventSubscriptionPropsMixin",
    "CfnGlobalClusterMixinProps",
    "CfnGlobalClusterPropsMixin",
    "CfnIntegrationMixinProps",
    "CfnIntegrationPropsMixin",
    "CfnOptionGroupMixinProps",
    "CfnOptionGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__ed6488da1eaa721a066c7a3dfb2e60c84e891fa17a4cce0642a271277c13505e(
    *,
    database_installation_files_s3_bucket_name: typing.Optional[builtins.str] = None,
    database_installation_files_s3_prefix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    manifest: typing.Optional[builtins.str] = None,
    source_custom_db_engine_version_identifier: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_aws_provided_latest_image: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfe1e329c96032655418fdef14c9fb8593688d3e520138e05bb430c07c7ee47(
    props: typing.Union[CfnCustomDBEngineVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1725cf4521bc20c8363c44661d11b34ebb0e815c3ec646163d18c81375d21c80(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e9fa4212139e8a339a6454e5877672906e92ee8d3dd76dd92ec057135f8d5a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43eff098b77d78d495a02edad613bba9e83d951ea3a6fdabca7197611100a1b(
    *,
    allocated_storage: typing.Optional[jsii.Number] = None,
    associated_roles: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDBClusterPropsMixin.DBClusterRoleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    backtrack_window: typing.Optional[jsii.Number] = None,
    backup_retention_period: typing.Optional[jsii.Number] = None,
    cluster_scalability_type: typing.Optional[builtins.str] = None,
    copy_tags_to_snapshot: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    database_insights_mode: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    db_cluster_identifier: typing.Optional[builtins.str] = None,
    db_cluster_instance_class: typing.Optional[builtins.str] = None,
    db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
    db_instance_parameter_group_name: typing.Optional[builtins.str] = None,
    db_subnet_group_name: typing.Optional[builtins.str] = None,
    db_system_id: typing.Optional[builtins.str] = None,
    delete_automated_backups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    domain: typing.Optional[builtins.str] = None,
    domain_iam_role_name: typing.Optional[builtins.str] = None,
    enable_cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_global_write_forwarding: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_http_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_iam_database_authentication: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_local_write_forwarding: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_lifecycle_support: typing.Optional[builtins.str] = None,
    engine_mode: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    global_cluster_identifier: typing.Optional[builtins.str] = None,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    manage_master_user_password: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    master_user_authentication_type: typing.Optional[builtins.str] = None,
    master_username: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[builtins.str] = None,
    master_user_secret: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDBClusterPropsMixin.MasterUserSecretProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    monitoring_interval: typing.Optional[jsii.Number] = None,
    monitoring_role_arn: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    performance_insights_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    performance_insights_kms_key_id: typing.Optional[builtins.str] = None,
    performance_insights_retention_period: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_backup_window: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    replication_source_identifier: typing.Optional[builtins.str] = None,
    restore_to_time: typing.Optional[builtins.str] = None,
    restore_type: typing.Optional[builtins.str] = None,
    scaling_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDBClusterPropsMixin.ScalingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    serverless_v2_scaling_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDBClusterPropsMixin.ServerlessV2ScalingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snapshot_identifier: typing.Optional[builtins.str] = None,
    source_db_cluster_identifier: typing.Optional[builtins.str] = None,
    source_db_cluster_resource_id: typing.Optional[builtins.str] = None,
    source_region: typing.Optional[builtins.str] = None,
    storage_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    storage_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_latest_restorable_time: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeda1b2281cd8734564a372d702be4527700d8e9453c0941cdafaf95c01a1298(
    *,
    db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    family: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209db834d31713852f9cadcf73edf258847750626d5c278851b3be9d47539b37(
    props: typing.Union[CfnDBClusterParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95839d07f33e9d12c55687d1ad3cd1fe37e540e7b37866f8d807d037189d75fb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ee113678308303e85ee68f8faedbe7715ffbec183c1e4198186640b29e3bfe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0426765f8b906b0936fed08cc80c7784e3f62780f4a7589ad8ffae8d0b7aaef3(
    props: typing.Union[CfnDBClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73903f3a7f50b357f79e8f8f01ca186d30e4bb3895f068d7ce071becf934372a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4fe7a534466db1dd4ddd7dea08d880ebcc82b90dfded5662fbefa509ec251f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16cc24520a196a07064430096317906f87562602a7119850549bc07a907ba382(
    *,
    feature_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbe76a5c8d6cbd2e7bdc61c95378fa201e5650240c5686f0e6b5b5a7c135c63(
    *,
    address: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60095e872106c8429daafe37f171afcd2fe5aa0eb62d010ab82fbd8a2df5073a(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ff6889ac0d278daadaa99e0e9460705cc484405ac9e2f2e9c65fcdd5ed9fc4(
    *,
    address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11a9e386c17fd99becae1d93b08711eba50ac7dcb2268cb4ed7e2f23a5792dc(
    *,
    auto_pause: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    seconds_before_timeout: typing.Optional[jsii.Number] = None,
    seconds_until_auto_pause: typing.Optional[jsii.Number] = None,
    timeout_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07fbb348251d57a869a276a01ebafe297ad9843da66d815e44c84bb65d814568(
    *,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    seconds_until_auto_pause: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6f1c64298fe52c0293ad649a7a349d80ad2a01120798ffc49e70d693e422db(
    *,
    allocated_storage: typing.Optional[builtins.str] = None,
    allow_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    apply_immediately: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    associated_roles: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDBInstancePropsMixin.DBInstanceRoleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    automatic_backup_replication_kms_key_id: typing.Optional[builtins.str] = None,
    automatic_backup_replication_region: typing.Optional[builtins.str] = None,
    automatic_backup_replication_retention_period: typing.Optional[jsii.Number] = None,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    backup_retention_period: typing.Optional[jsii.Number] = None,
    backup_target: typing.Optional[builtins.str] = None,
    ca_certificate_identifier: typing.Optional[builtins.str] = None,
    certificate_rotation_restart: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    character_set_name: typing.Optional[builtins.str] = None,
    copy_tags_to_snapshot: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    custom_iam_instance_profile: typing.Optional[builtins.str] = None,
    database_insights_mode: typing.Optional[builtins.str] = None,
    db_cluster_identifier: typing.Optional[builtins.str] = None,
    db_cluster_snapshot_identifier: typing.Optional[builtins.str] = None,
    db_instance_class: typing.Optional[builtins.str] = None,
    db_instance_identifier: typing.Optional[builtins.str] = None,
    db_name: typing.Optional[builtins.str] = None,
    db_parameter_group_name: typing.Optional[builtins.str] = None,
    db_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    db_snapshot_identifier: typing.Optional[builtins.str] = None,
    db_subnet_group_name: typing.Optional[builtins.str] = None,
    db_system_id: typing.Optional[builtins.str] = None,
    dedicated_log_volume: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    delete_automated_backups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    domain: typing.Optional[builtins.str] = None,
    domain_auth_secret_arn: typing.Optional[builtins.str] = None,
    domain_dns_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_fqdn: typing.Optional[builtins.str] = None,
    domain_iam_role_name: typing.Optional[builtins.str] = None,
    domain_ou: typing.Optional[builtins.str] = None,
    enable_cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_iam_database_authentication: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_performance_insights: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_lifecycle_support: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    license_model: typing.Optional[builtins.str] = None,
    manage_master_user_password: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    master_user_authentication_type: typing.Optional[builtins.str] = None,
    master_username: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[builtins.str] = None,
    master_user_secret: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDBInstancePropsMixin.MasterUserSecretProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_allocated_storage: typing.Optional[jsii.Number] = None,
    monitoring_interval: typing.Optional[jsii.Number] = None,
    monitoring_role_arn: typing.Optional[builtins.str] = None,
    multi_az: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    nchar_character_set_name: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    option_group_name: typing.Optional[builtins.str] = None,
    performance_insights_kms_key_id: typing.Optional[builtins.str] = None,
    performance_insights_retention_period: typing.Optional[jsii.Number] = None,
    port: typing.Optional[builtins.str] = None,
    preferred_backup_window: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    processor_features: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDBInstancePropsMixin.ProcessorFeatureProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    promotion_tier: typing.Optional[jsii.Number] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    replica_mode: typing.Optional[builtins.str] = None,
    restore_time: typing.Optional[builtins.str] = None,
    source_db_cluster_identifier: typing.Optional[builtins.str] = None,
    source_db_instance_automated_backups_arn: typing.Optional[builtins.str] = None,
    source_db_instance_identifier: typing.Optional[builtins.str] = None,
    source_dbi_resource_id: typing.Optional[builtins.str] = None,
    source_region: typing.Optional[builtins.str] = None,
    storage_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    storage_throughput: typing.Optional[jsii.Number] = None,
    storage_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tde_credential_arn: typing.Optional[builtins.str] = None,
    tde_credential_password: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
    use_default_processor_features: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_latest_restorable_time: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    vpc_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f3e3d8e6c1bb9a4a2e15f25bbd620022e59a17140df4dcab5f82dfe56852e7(
    props: typing.Union[CfnDBInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b091d3fff3f9c022b8169f68c548710a9887382d3d614074c4e3b04d30cd949(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6da180346468151d65ab251d989f3808890ce5ceeea96db4386368240e2e92(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50edfa60e98c0ff64d156e4b4b9f84747fc7345375289857eb262781f3673999(
    *,
    ca_identifier: typing.Optional[builtins.str] = None,
    valid_till: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d50286575a28f98261e5d8f798b3f18970a43f7558b9449f2108afcc6d2de46(
    *,
    feature_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dac2c818dcc4db1355921d8d11a019cd96034f421c80abe867d125d4cb74880(
    *,
    message: typing.Optional[builtins.str] = None,
    normal: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    status_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df440e91d1ed15f679bfb7b3e4fc93294fe3f0e0b96e71ce0b662a730d3dcf2e(
    *,
    address: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e1c30363d091ced94a32371f235eacaf7e4cece819b64bec90a14209e523ea(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e191daff57d83d50eb1e45a22334e5120c6cb6f4fc21039ca5d97d4a9626d85(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26a6de74bb445a96302eba76f71fa3ae3da32030ea5b852d71178605ab585ee(
    *,
    db_parameter_group_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    family: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a041592f57685a029a39714da665b6c15082377316f005590626ddad3c711b80(
    props: typing.Union[CfnDBParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0da7fd8ddfc9e68a912aa700079b5f0b3a223b77c212ddccb57627f8fb99c6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860345a33d1d146ca8017e7640b74af9114561ee657fbf9ed5732366b9726189(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b658b9d41c7bec4e42eab20c6d8e3937cfb5e9b37d871a4dcd3d920a8906cc(
    *,
    db_proxy_endpoint_name: typing.Optional[builtins.str] = None,
    db_proxy_name: typing.Optional[builtins.str] = None,
    endpoint_network_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDBProxyEndpointPropsMixin.TagFormatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_role: typing.Optional[builtins.str] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8fbf534ff2c1f140a704c7f6b6747f1712a0c0711d952ac7e8a13179d8d3c2(
    props: typing.Union[CfnDBProxyEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c568cf824ffc9ad457d27b9598edb1c64005c0480c1443848f2535b7f421c7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab9120e7e2a071f6de82d62788f61c0e7a7037f2fb05697035d55f7d4486961(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6966bd8d446f46df408c030c920ba5d7947cad36d026fa940a1ef95a02315677(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121eff4dd724752490f92e20e7f92b129b2d3d89ffd1fb866a19891cadc77624(
    *,
    auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDBProxyPropsMixin.AuthFormatProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    db_proxy_name: typing.Optional[builtins.str] = None,
    debug_logging: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    default_auth_scheme: typing.Optional[builtins.str] = None,
    endpoint_network_type: typing.Optional[builtins.str] = None,
    engine_family: typing.Optional[builtins.str] = None,
    idle_client_timeout: typing.Optional[jsii.Number] = None,
    require_tls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDBProxyPropsMixin.TagFormatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_connection_network_type: typing.Optional[builtins.str] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613a2811c20bca87220368fdd015c3be7ba4e2f4e929bc6845a326567c50ff47(
    props: typing.Union[CfnDBProxyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eace7e687dca7dc9236511abd59f5769756e97fe8a4430b95f3b0b920c532d62(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6ca829b771e10130f8258bf9b74a7646942616cff804ee7aaa7bd51b2ef563(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d0427f22698fff24a4cc5a00fd9ccb47733fbbd4dbaedd1ab5c8bf1aeae7c2(
    *,
    auth_scheme: typing.Optional[builtins.str] = None,
    client_password_auth_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    iam_auth: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5270d326f93d5e2bfc34b7f0c8cf3e8ae1f8411e6b011e53cbb9dda10d8368d5(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581fda2d223fe0b8c4816c0caa6dd03bbe8e532a9882e891a1fec9b6fe61cc9e(
    *,
    connection_pool_configuration_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDBProxyTargetGroupPropsMixin.ConnectionPoolConfigurationInfoFormatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    db_cluster_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    db_instance_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    db_proxy_name: typing.Optional[builtins.str] = None,
    target_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfef73b5aad68fc1c307d4d7eda635e4b9d4fb007dbdc733679f1433bbec821(
    props: typing.Union[CfnDBProxyTargetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b132a2d3c195d33d4a0baf0c30249a2032bd60d1300c6e19041bbe202771a7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e245cd671d061c36b5bb2d19236bb16f92e9fe6833c29e4dd11f313825ec9fea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc3f853ce587302f2b5ccfd26075da37ddd375056532c79dd32e62cc31d8ade(
    *,
    connection_borrow_timeout: typing.Optional[jsii.Number] = None,
    init_query: typing.Optional[builtins.str] = None,
    max_connections_percent: typing.Optional[jsii.Number] = None,
    max_idle_connections_percent: typing.Optional[jsii.Number] = None,
    session_pinning_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67ddd8f877f9e5fe6e2f02e4fc73413ea77a40dc85bd09540b96233435d6e10(
    *,
    cidrip: typing.Optional[builtins.str] = None,
    db_security_group_name: typing.Optional[builtins.str] = None,
    ec2_security_group_id: typing.Optional[builtins.str] = None,
    ec2_security_group_name: typing.Optional[builtins.str] = None,
    ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ca657d061512f1f1199dc2c645a8479ef2f58dae01bd78779483ee66d7472e(
    props: typing.Union[CfnDBSecurityGroupIngressMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d64303477785df92102d08061cff5275bf474184612b8632ff3fab96539867(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40602c6356a6747a819d095043c2b91ab4fc7b4838b2481f041307462b7a8289(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6ede1f8723fb4f4b340bd0591ada4f3e3de17908b32c22217203dd392baa3f(
    *,
    db_security_group_ingress: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDBSecurityGroupPropsMixin.IngressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ec2_vpc_id: typing.Optional[builtins.str] = None,
    group_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13553d76ce4b9c462e125e9b91784d2e519f304cfb3c4371e8dd00d324abad33(
    props: typing.Union[CfnDBSecurityGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceca4698b8e7a98a5d4397bed06858d17f2f4f07ed339e5ff4b048f19a2dc800(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415b1c1c9b28ab9b0b3259971bfc5f5b12b4d1c82bd2e0c74819ab3ce9041022(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b254b017ba7906cc32a81703e906afdcae801104f6b58e9a6f3907398512db10(
    *,
    cidrip: typing.Optional[builtins.str] = None,
    ec2_security_group_id: typing.Optional[builtins.str] = None,
    ec2_security_group_name: typing.Optional[builtins.str] = None,
    ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e457d12ecf98905e4ca91e749ffec080dda50fc6d2d3d65a7a7dd1fc3a48a06(
    *,
    compute_redundancy: typing.Optional[jsii.Number] = None,
    db_cluster_identifier: typing.Optional[builtins.str] = None,
    db_shard_group_identifier: typing.Optional[builtins.str] = None,
    max_acu: typing.Optional[jsii.Number] = None,
    min_acu: typing.Optional[jsii.Number] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7cc015a896c281ee277dde4bf45ed8d866881cba4fb3b1a9d3ed1f02bfa8c3(
    props: typing.Union[CfnDBShardGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2301fcafc0b4fd7245b79e442ee1eb04ce53a047aea0052c35ae6ac15b8a8d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05cefe685a97678f5cee490d57c2228d0e57d0c97bc7fa6296f0c0bd06ea5b1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9db1a7ad1ac5a1d268713a5f661f3a5b7b9e6174b4483511086010f4e0d8b59(
    *,
    db_subnet_group_description: typing.Optional[builtins.str] = None,
    db_subnet_group_name: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd4ae444dbe4514bda7bf4afe26c4e3075bc0910d535e8e64940c3d67a30a4b(
    props: typing.Union[CfnDBSubnetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f13ea82ee1f1a6aa2b07081012bdd0fe95f070c2f8a57d573b29e0dd695802(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c0337614ee85c975bee5f06a809142803d4601119fe51e15a00787ddce95de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185b22033f2e5422c0967451d8ec44a669b7ab4f4bb44182c03f2d23613ff385(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    event_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
    source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_type: typing.Optional[builtins.str] = None,
    subscription_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934744984e63142f6b4505a8542d51703ffc3a358d4983d62007c87f0010da5d(
    props: typing.Union[CfnEventSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09b7a6e3066181936b133b7ca9e8b28f28ed20f94b40513cd6195fdd5cfd7e5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567d7adfb774f5407205bee6d4e264b7dfac42136f97d55007ddd8c200c645e7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e12cf738de37d57c7c007c82a838ecaefc8adee5dffafe16ffa1a26ec820b1(
    *,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_lifecycle_support: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    global_cluster_identifier: typing.Optional[builtins.str] = None,
    source_db_cluster_identifier: typing.Optional[builtins.str] = None,
    storage_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12046e3c4a90a2e675e17eb1e57411d1a3aec88d476e5bb07dfe1d0bd3e39b6b(
    props: typing.Union[CfnGlobalClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bef7af265da11034876438d29f49dc44083eb6eb9985d4783cf2d736903ff6a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ebd365c9ff5aa90534e1f37815d2586ef857128a462ad0134b852bd87d7563f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59b7586ecff95abfe8bfd2876307c2854434992133b5b2032db870fb9e7c8b8(
    *,
    address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c642c7656cff1f9958ffd59c3867475ccfcaef94bb83ba65d53d2ad2cf5b1f(
    *,
    additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    data_filter: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    integration_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f7e0f4498dcbf6754fa66429c139b8ad503ce784458fd198472b7cd7e40a54(
    props: typing.Union[CfnIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9956489aa458243367307482724ad7ec8db74aed3efc5ee7fd180afd8ce2fd21(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2d4e8606bb2b689b1b46ad9f4788a244c7c728b3fd3280272a84531009da02(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcce897aedb62a3dedd686338f69d2fdcd132f181acef5de7eda4826444784f4(
    *,
    engine_name: typing.Optional[builtins.str] = None,
    major_engine_version: typing.Optional[builtins.str] = None,
    option_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOptionGroupPropsMixin.OptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    option_group_description: typing.Optional[builtins.str] = None,
    option_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbca3e89f8a4275c314a4adf8ddd6402ce71787662d3baea276ce77d3bb0e3a(
    props: typing.Union[CfnOptionGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab1f17e634cb378394eb155c345d523d60db467cdcd29b6c5caf74ebfdff26b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451d0abb5b771757ebbfa7e9e09e0fa59e46246e547fd248e3102475c583ec4e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2735ce1a9dc50d8b323dab4303e0f2ac545847966863d4ef176d3be56ab3255a(
    *,
    db_security_group_memberships: typing.Optional[typing.Sequence[builtins.str]] = None,
    option_name: typing.Optional[builtins.str] = None,
    option_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOptionGroupPropsMixin.OptionSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    option_version: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    vpc_security_group_memberships: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4674fac63ccbe21405d738a10ac96c29899ac73e9c4187e7bd8bb89783471ae9(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
