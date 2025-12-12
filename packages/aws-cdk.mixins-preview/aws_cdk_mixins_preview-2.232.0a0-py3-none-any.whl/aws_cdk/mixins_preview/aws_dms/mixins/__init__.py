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
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnCertificateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_identifier": "certificateIdentifier",
        "certificate_pem": "certificatePem",
        "certificate_wallet": "certificateWallet",
    },
)
class CfnCertificateMixinProps:
    def __init__(
        self,
        *,
        certificate_identifier: typing.Optional[builtins.str] = None,
        certificate_pem: typing.Optional[builtins.str] = None,
        certificate_wallet: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCertificatePropsMixin.

        :param certificate_identifier: A customer-assigned name for the certificate. Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen or contain two consecutive hyphens.
        :param certificate_pem: The contents of a ``.pem`` file, which contains an X.509 certificate.
        :param certificate_wallet: The location of an imported Oracle Wallet certificate for use with SSL. An example is: ``filebase64("${path.root}/rds-ca-2019-root.sso")``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            cfn_certificate_mixin_props = dms_mixins.CfnCertificateMixinProps(
                certificate_identifier="certificateIdentifier",
                certificate_pem="certificatePem",
                certificate_wallet="certificateWallet"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70a6c0f54de3d4c48820cbd980d20a53cad4178170227a894a9b4fd08c99a1f)
            check_type(argname="argument certificate_identifier", value=certificate_identifier, expected_type=type_hints["certificate_identifier"])
            check_type(argname="argument certificate_pem", value=certificate_pem, expected_type=type_hints["certificate_pem"])
            check_type(argname="argument certificate_wallet", value=certificate_wallet, expected_type=type_hints["certificate_wallet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_identifier is not None:
            self._values["certificate_identifier"] = certificate_identifier
        if certificate_pem is not None:
            self._values["certificate_pem"] = certificate_pem
        if certificate_wallet is not None:
            self._values["certificate_wallet"] = certificate_wallet

    @builtins.property
    def certificate_identifier(self) -> typing.Optional[builtins.str]:
        '''A customer-assigned name for the certificate.

        Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html#cfn-dms-certificate-certificateidentifier
        '''
        result = self._values.get("certificate_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_pem(self) -> typing.Optional[builtins.str]:
        '''The contents of a ``.pem`` file, which contains an X.509 certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html#cfn-dms-certificate-certificatepem
        '''
        result = self._values.get("certificate_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_wallet(self) -> typing.Optional[builtins.str]:
        '''The location of an imported Oracle Wallet certificate for use with SSL.

        An example is: ``filebase64("${path.root}/rds-ca-2019-root.sso")``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html#cfn-dms-certificate-certificatewallet
        '''
        result = self._values.get("certificate_wallet")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCertificatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnCertificatePropsMixin",
):
    '''The ``AWS::DMS::Certificate`` resource creates an Secure Sockets Layer (SSL) certificate that encrypts connections between AWS DMS endpoints and the replication instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html
    :cloudformationResource: AWS::DMS::Certificate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        cfn_certificate_props_mixin = dms_mixins.CfnCertificatePropsMixin(dms_mixins.CfnCertificateMixinProps(
            certificate_identifier="certificateIdentifier",
            certificate_pem="certificatePem",
            certificate_wallet="certificateWallet"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DMS::Certificate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7234037361d91287084bf54e83c54395892261316d0e6364a0a3030e7a8617)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ee082a82efe34d44c3ecb9110a6bc379b7622b2ac0300abcfa8f59439c12b2c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d30bd0c6b668b86d7da50ebdd19c3cf59e1e3579c0bd1c4c698a78ef1f0dfc3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCertificateMixinProps:
        return typing.cast(CfnCertificateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataMigrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_migration_identifier": "dataMigrationIdentifier",
        "data_migration_name": "dataMigrationName",
        "data_migration_settings": "dataMigrationSettings",
        "data_migration_type": "dataMigrationType",
        "migration_project_identifier": "migrationProjectIdentifier",
        "service_access_role_arn": "serviceAccessRoleArn",
        "source_data_settings": "sourceDataSettings",
        "tags": "tags",
    },
)
class CfnDataMigrationMixinProps:
    def __init__(
        self,
        *,
        data_migration_identifier: typing.Optional[builtins.str] = None,
        data_migration_name: typing.Optional[builtins.str] = None,
        data_migration_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataMigrationPropsMixin.DataMigrationSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_migration_type: typing.Optional[builtins.str] = None,
        migration_project_identifier: typing.Optional[builtins.str] = None,
        service_access_role_arn: typing.Optional[builtins.str] = None,
        source_data_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataMigrationPropsMixin.SourceDataSettingsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataMigrationPropsMixin.

        :param data_migration_identifier: The property describes an ARN of the data migration.
        :param data_migration_name: The user-friendly name for the data migration.
        :param data_migration_settings: Specifies CloudWatch settings and selection rules for the data migration.
        :param data_migration_type: Specifies whether the data migration is full-load only, change data capture (CDC) only, or full-load and CDC.
        :param migration_project_identifier: The property describes an identifier for the migration project. It is used for describing/deleting/modifying can be name/arn
        :param service_access_role_arn: The IAM role that the data migration uses to access AWS resources.
        :param source_data_settings: Specifies information about the data migration's source data provider.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-datamigration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            cfn_data_migration_mixin_props = dms_mixins.CfnDataMigrationMixinProps(
                data_migration_identifier="dataMigrationIdentifier",
                data_migration_name="dataMigrationName",
                data_migration_settings=dms_mixins.CfnDataMigrationPropsMixin.DataMigrationSettingsProperty(
                    cloudwatch_logs_enabled=False,
                    number_of_jobs=123,
                    selection_rules="selectionRules"
                ),
                data_migration_type="dataMigrationType",
                migration_project_identifier="migrationProjectIdentifier",
                service_access_role_arn="serviceAccessRoleArn",
                source_data_settings=[dms_mixins.CfnDataMigrationPropsMixin.SourceDataSettingsProperty(
                    cdc_start_position="cdcStartPosition",
                    cdc_start_time="cdcStartTime",
                    cdc_stop_time="cdcStopTime",
                    slot_name="slotName"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90dbc13e13a47cb11be71c7aa9312933ec33169a36fb281927aa87cc8ee36bf9)
            check_type(argname="argument data_migration_identifier", value=data_migration_identifier, expected_type=type_hints["data_migration_identifier"])
            check_type(argname="argument data_migration_name", value=data_migration_name, expected_type=type_hints["data_migration_name"])
            check_type(argname="argument data_migration_settings", value=data_migration_settings, expected_type=type_hints["data_migration_settings"])
            check_type(argname="argument data_migration_type", value=data_migration_type, expected_type=type_hints["data_migration_type"])
            check_type(argname="argument migration_project_identifier", value=migration_project_identifier, expected_type=type_hints["migration_project_identifier"])
            check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
            check_type(argname="argument source_data_settings", value=source_data_settings, expected_type=type_hints["source_data_settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_migration_identifier is not None:
            self._values["data_migration_identifier"] = data_migration_identifier
        if data_migration_name is not None:
            self._values["data_migration_name"] = data_migration_name
        if data_migration_settings is not None:
            self._values["data_migration_settings"] = data_migration_settings
        if data_migration_type is not None:
            self._values["data_migration_type"] = data_migration_type
        if migration_project_identifier is not None:
            self._values["migration_project_identifier"] = migration_project_identifier
        if service_access_role_arn is not None:
            self._values["service_access_role_arn"] = service_access_role_arn
        if source_data_settings is not None:
            self._values["source_data_settings"] = source_data_settings
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_migration_identifier(self) -> typing.Optional[builtins.str]:
        '''The property describes an ARN of the data migration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-datamigration.html#cfn-dms-datamigration-datamigrationidentifier
        '''
        result = self._values.get("data_migration_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_migration_name(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name for the data migration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-datamigration.html#cfn-dms-datamigration-datamigrationname
        '''
        result = self._values.get("data_migration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_migration_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataMigrationPropsMixin.DataMigrationSettingsProperty"]]:
        '''Specifies CloudWatch settings and selection rules for the data migration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-datamigration.html#cfn-dms-datamigration-datamigrationsettings
        '''
        result = self._values.get("data_migration_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataMigrationPropsMixin.DataMigrationSettingsProperty"]], result)

    @builtins.property
    def data_migration_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the data migration is full-load only, change data capture (CDC) only, or full-load and CDC.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-datamigration.html#cfn-dms-datamigration-datamigrationtype
        '''
        result = self._values.get("data_migration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def migration_project_identifier(self) -> typing.Optional[builtins.str]:
        '''The property describes an identifier for the migration project.

        It is used for describing/deleting/modifying can be name/arn

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-datamigration.html#cfn-dms-datamigration-migrationprojectidentifier
        '''
        result = self._values.get("migration_project_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''The IAM role that the data migration uses to access AWS resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-datamigration.html#cfn-dms-datamigration-serviceaccessrolearn
        '''
        result = self._values.get("service_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_data_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataMigrationPropsMixin.SourceDataSettingsProperty"]]]]:
        '''Specifies information about the data migration's source data provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-datamigration.html#cfn-dms-datamigration-sourcedatasettings
        '''
        result = self._values.get("source_data_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataMigrationPropsMixin.SourceDataSettingsProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-datamigration.html#cfn-dms-datamigration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataMigrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataMigrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataMigrationPropsMixin",
):
    '''This object provides information about a AWS DMS data migration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-datamigration.html
    :cloudformationResource: AWS::DMS::DataMigration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        cfn_data_migration_props_mixin = dms_mixins.CfnDataMigrationPropsMixin(dms_mixins.CfnDataMigrationMixinProps(
            data_migration_identifier="dataMigrationIdentifier",
            data_migration_name="dataMigrationName",
            data_migration_settings=dms_mixins.CfnDataMigrationPropsMixin.DataMigrationSettingsProperty(
                cloudwatch_logs_enabled=False,
                number_of_jobs=123,
                selection_rules="selectionRules"
            ),
            data_migration_type="dataMigrationType",
            migration_project_identifier="migrationProjectIdentifier",
            service_access_role_arn="serviceAccessRoleArn",
            source_data_settings=[dms_mixins.CfnDataMigrationPropsMixin.SourceDataSettingsProperty(
                cdc_start_position="cdcStartPosition",
                cdc_start_time="cdcStartTime",
                cdc_stop_time="cdcStopTime",
                slot_name="slotName"
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
        props: typing.Union[CfnDataMigrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DMS::DataMigration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ad56f45c9791531457418b84e1fc66b862e627878a26c524896a179f28778d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__932ba2abd6cfdd4a3c6fb01f7f486b6f4d684bf1fd9b7d1c77a0ff6e5e5ad6e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e47108af63e3a3196fa86c9628fafb0a2dc0c64749e6841826cd2ffb988af9d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataMigrationMixinProps:
        return typing.cast(CfnDataMigrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataMigrationPropsMixin.DataMigrationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloudwatch_logs_enabled": "cloudwatchLogsEnabled",
            "number_of_jobs": "numberOfJobs",
            "selection_rules": "selectionRules",
        },
    )
    class DataMigrationSettingsProperty:
        def __init__(
            self,
            *,
            cloudwatch_logs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            number_of_jobs: typing.Optional[jsii.Number] = None,
            selection_rules: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Options for configuring a data migration, including whether to enable CloudWatch logs, and the selection rules to use to include or exclude database objects from the migration.

            :param cloudwatch_logs_enabled: Whether to enable CloudWatch logging for the data migration.
            :param number_of_jobs: The number of parallel jobs that trigger parallel threads to unload the tables from the source, and then load them to the target.
            :param selection_rules: A JSON-formatted string that defines what objects to include and exclude from the migration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-datamigration-datamigrationsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                data_migration_settings_property = dms_mixins.CfnDataMigrationPropsMixin.DataMigrationSettingsProperty(
                    cloudwatch_logs_enabled=False,
                    number_of_jobs=123,
                    selection_rules="selectionRules"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b074a29c4603c3766a09f83c0bb600c7e7fb34a4061744b090a5b8e1f1e1802)
                check_type(argname="argument cloudwatch_logs_enabled", value=cloudwatch_logs_enabled, expected_type=type_hints["cloudwatch_logs_enabled"])
                check_type(argname="argument number_of_jobs", value=number_of_jobs, expected_type=type_hints["number_of_jobs"])
                check_type(argname="argument selection_rules", value=selection_rules, expected_type=type_hints["selection_rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloudwatch_logs_enabled is not None:
                self._values["cloudwatch_logs_enabled"] = cloudwatch_logs_enabled
            if number_of_jobs is not None:
                self._values["number_of_jobs"] = number_of_jobs
            if selection_rules is not None:
                self._values["selection_rules"] = selection_rules

        @builtins.property
        def cloudwatch_logs_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to enable CloudWatch logging for the data migration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-datamigration-datamigrationsettings.html#cfn-dms-datamigration-datamigrationsettings-cloudwatchlogsenabled
            '''
            result = self._values.get("cloudwatch_logs_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def number_of_jobs(self) -> typing.Optional[jsii.Number]:
            '''The number of parallel jobs that trigger parallel threads to unload the tables from the source, and then load them to the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-datamigration-datamigrationsettings.html#cfn-dms-datamigration-datamigrationsettings-numberofjobs
            '''
            result = self._values.get("number_of_jobs")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def selection_rules(self) -> typing.Optional[builtins.str]:
            '''A JSON-formatted string that defines what objects to include and exclude from the migration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-datamigration-datamigrationsettings.html#cfn-dms-datamigration-datamigrationsettings-selectionrules
            '''
            result = self._values.get("selection_rules")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataMigrationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataMigrationPropsMixin.SourceDataSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cdc_start_position": "cdcStartPosition",
            "cdc_start_time": "cdcStartTime",
            "cdc_stop_time": "cdcStopTime",
            "slot_name": "slotName",
        },
    )
    class SourceDataSettingsProperty:
        def __init__(
            self,
            *,
            cdc_start_position: typing.Optional[builtins.str] = None,
            cdc_start_time: typing.Optional[builtins.str] = None,
            cdc_stop_time: typing.Optional[builtins.str] = None,
            slot_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param cdc_start_position: The property is a point in the database engine's log that defines a time where you can begin CDC.
            :param cdc_start_time: The property indicates the start time for a change data capture (CDC) operation. The value is server time in UTC format.
            :param cdc_stop_time: The property indicates the stop time for a change data capture (CDC) operation. The value is server time in UTC format.
            :param slot_name: The property sets the name of a previously created logical replication slot for a change data capture (CDC) load of the source instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-datamigration-sourcedatasettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                source_data_settings_property = dms_mixins.CfnDataMigrationPropsMixin.SourceDataSettingsProperty(
                    cdc_start_position="cdcStartPosition",
                    cdc_start_time="cdcStartTime",
                    cdc_stop_time="cdcStopTime",
                    slot_name="slotName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__febf5ad16f4d461915c788bf018174e0184025fdd4dd8990859552e3a67b5765)
                check_type(argname="argument cdc_start_position", value=cdc_start_position, expected_type=type_hints["cdc_start_position"])
                check_type(argname="argument cdc_start_time", value=cdc_start_time, expected_type=type_hints["cdc_start_time"])
                check_type(argname="argument cdc_stop_time", value=cdc_stop_time, expected_type=type_hints["cdc_stop_time"])
                check_type(argname="argument slot_name", value=slot_name, expected_type=type_hints["slot_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cdc_start_position is not None:
                self._values["cdc_start_position"] = cdc_start_position
            if cdc_start_time is not None:
                self._values["cdc_start_time"] = cdc_start_time
            if cdc_stop_time is not None:
                self._values["cdc_stop_time"] = cdc_stop_time
            if slot_name is not None:
                self._values["slot_name"] = slot_name

        @builtins.property
        def cdc_start_position(self) -> typing.Optional[builtins.str]:
            '''The property is a point in the database engine's log that defines a time where you can begin CDC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-datamigration-sourcedatasettings.html#cfn-dms-datamigration-sourcedatasettings-cdcstartposition
            '''
            result = self._values.get("cdc_start_position")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cdc_start_time(self) -> typing.Optional[builtins.str]:
            '''The property indicates the start time for a change data capture (CDC) operation.

            The value is server time in UTC format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-datamigration-sourcedatasettings.html#cfn-dms-datamigration-sourcedatasettings-cdcstarttime
            '''
            result = self._values.get("cdc_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cdc_stop_time(self) -> typing.Optional[builtins.str]:
            '''The property indicates the stop time for a change data capture (CDC) operation.

            The value is server time in UTC format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-datamigration-sourcedatasettings.html#cfn-dms-datamigration-sourcedatasettings-cdcstoptime
            '''
            result = self._values.get("cdc_stop_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slot_name(self) -> typing.Optional[builtins.str]:
            '''The property sets the name of a previously created logical replication slot for a change data capture (CDC) load of the source instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-datamigration-sourcedatasettings.html#cfn-dms-datamigration-sourcedatasettings-slotname
            '''
            result = self._values.get("slot_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceDataSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_provider_identifier": "dataProviderIdentifier",
        "data_provider_name": "dataProviderName",
        "description": "description",
        "engine": "engine",
        "exact_settings": "exactSettings",
        "settings": "settings",
        "tags": "tags",
    },
)
class CfnDataProviderMixinProps:
    def __init__(
        self,
        *,
        data_provider_identifier: typing.Optional[builtins.str] = None,
        data_provider_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        exact_settings: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.SettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataProviderPropsMixin.

        :param data_provider_identifier: The identifier of the data provider. Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.
        :param data_provider_name: The name of the data provider.
        :param description: A description of the data provider. Descriptions can have up to 31 characters. A description can contain only ASCII letters, digits, and hyphens ('-'). Also, it can't end with a hyphen or contain two consecutive hyphens, and can only begin with a letter.
        :param engine: The type of database engine for the data provider. Valid values include ``"aurora"`` , ``"aurora-postgresql"`` , ``"mysql"`` , ``"oracle"`` , ``"postgres"`` , ``"sqlserver"`` , ``redshift`` , ``mariadb`` , ``mongodb`` , ``db2`` , ``db2-zos`` , ``docdb`` , and ``sybase`` . A value of ``"aurora"`` represents Amazon Aurora MySQL-Compatible Edition.
        :param exact_settings: The property describes the exact settings which can be modified. Default: - false
        :param settings: The settings in JSON format for a data provider.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-dataprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            cfn_data_provider_mixin_props = dms_mixins.CfnDataProviderMixinProps(
                data_provider_identifier="dataProviderIdentifier",
                data_provider_name="dataProviderName",
                description="description",
                engine="engine",
                exact_settings=False,
                settings=dms_mixins.CfnDataProviderPropsMixin.SettingsProperty(
                    doc_db_settings=dms_mixins.CfnDataProviderPropsMixin.DocDbSettingsProperty(
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    ibm_db2_luw_settings=dms_mixins.CfnDataProviderPropsMixin.IbmDb2LuwSettingsProperty(
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    ibm_db2_zOs_settings=dms_mixins.CfnDataProviderPropsMixin.IbmDb2zOsSettingsProperty(
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    maria_db_settings=dms_mixins.CfnDataProviderPropsMixin.MariaDbSettingsProperty(
                        certificate_arn="certificateArn",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    microsoft_sql_server_settings=dms_mixins.CfnDataProviderPropsMixin.MicrosoftSqlServerSettingsProperty(
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    mongo_db_settings=dms_mixins.CfnDataProviderPropsMixin.MongoDbSettingsProperty(
                        auth_mechanism="authMechanism",
                        auth_source="authSource",
                        auth_type="authType",
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    my_sql_settings=dms_mixins.CfnDataProviderPropsMixin.MySqlSettingsProperty(
                        certificate_arn="certificateArn",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    oracle_settings=dms_mixins.CfnDataProviderPropsMixin.OracleSettingsProperty(
                        asm_server="asmServer",
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        secrets_manager_oracle_asm_access_role_arn="secretsManagerOracleAsmAccessRoleArn",
                        secrets_manager_oracle_asm_secret_id="secretsManagerOracleAsmSecretId",
                        secrets_manager_security_db_encryption_access_role_arn="secretsManagerSecurityDbEncryptionAccessRoleArn",
                        secrets_manager_security_db_encryption_secret_id="secretsManagerSecurityDbEncryptionSecretId",
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    postgre_sql_settings=dms_mixins.CfnDataProviderPropsMixin.PostgreSqlSettingsProperty(
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    redshift_settings=dms_mixins.CfnDataProviderPropsMixin.RedshiftSettingsProperty(
                        database_name="databaseName",
                        port=123,
                        server_name="serverName"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d4927345d0666d9a9001178c1330a615d5ce98258a5e1f39321ec0aea15380)
            check_type(argname="argument data_provider_identifier", value=data_provider_identifier, expected_type=type_hints["data_provider_identifier"])
            check_type(argname="argument data_provider_name", value=data_provider_name, expected_type=type_hints["data_provider_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument exact_settings", value=exact_settings, expected_type=type_hints["exact_settings"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_provider_identifier is not None:
            self._values["data_provider_identifier"] = data_provider_identifier
        if data_provider_name is not None:
            self._values["data_provider_name"] = data_provider_name
        if description is not None:
            self._values["description"] = description
        if engine is not None:
            self._values["engine"] = engine
        if exact_settings is not None:
            self._values["exact_settings"] = exact_settings
        if settings is not None:
            self._values["settings"] = settings
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_provider_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the data provider.

        Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-dataprovider.html#cfn-dms-dataprovider-dataprovideridentifier
        '''
        result = self._values.get("data_provider_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_provider_name(self) -> typing.Optional[builtins.str]:
        '''The name of the data provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-dataprovider.html#cfn-dms-dataprovider-dataprovidername
        '''
        result = self._values.get("data_provider_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the data provider.

        Descriptions can have up to 31 characters. A description can contain only ASCII letters, digits, and hyphens ('-'). Also, it can't end with a hyphen or contain two consecutive hyphens, and can only begin with a letter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-dataprovider.html#cfn-dms-dataprovider-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The type of database engine for the data provider.

        Valid values include ``"aurora"`` , ``"aurora-postgresql"`` , ``"mysql"`` , ``"oracle"`` , ``"postgres"`` , ``"sqlserver"`` , ``redshift`` , ``mariadb`` , ``mongodb`` , ``db2`` , ``db2-zos`` , ``docdb`` , and ``sybase`` . A value of ``"aurora"`` represents Amazon Aurora MySQL-Compatible Edition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-dataprovider.html#cfn-dms-dataprovider-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact_settings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The property describes the exact settings which can be modified.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-dataprovider.html#cfn-dms-dataprovider-exactsettings
        '''
        result = self._values.get("exact_settings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.SettingsProperty"]]:
        '''The settings in JSON format for a data provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-dataprovider.html#cfn-dms-dataprovider-settings
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.SettingsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-dataprovider.html#cfn-dms-dataprovider-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataProviderMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataProviderPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin",
):
    '''Provides information that defines a data provider.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-dataprovider.html
    :cloudformationResource: AWS::DMS::DataProvider
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        cfn_data_provider_props_mixin = dms_mixins.CfnDataProviderPropsMixin(dms_mixins.CfnDataProviderMixinProps(
            data_provider_identifier="dataProviderIdentifier",
            data_provider_name="dataProviderName",
            description="description",
            engine="engine",
            exact_settings=False,
            settings=dms_mixins.CfnDataProviderPropsMixin.SettingsProperty(
                doc_db_settings=dms_mixins.CfnDataProviderPropsMixin.DocDbSettingsProperty(
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                ),
                ibm_db2_luw_settings=dms_mixins.CfnDataProviderPropsMixin.IbmDb2LuwSettingsProperty(
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                ),
                ibm_db2_zOs_settings=dms_mixins.CfnDataProviderPropsMixin.IbmDb2zOsSettingsProperty(
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                ),
                maria_db_settings=dms_mixins.CfnDataProviderPropsMixin.MariaDbSettingsProperty(
                    certificate_arn="certificateArn",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                ),
                microsoft_sql_server_settings=dms_mixins.CfnDataProviderPropsMixin.MicrosoftSqlServerSettingsProperty(
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                ),
                mongo_db_settings=dms_mixins.CfnDataProviderPropsMixin.MongoDbSettingsProperty(
                    auth_mechanism="authMechanism",
                    auth_source="authSource",
                    auth_type="authType",
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                ),
                my_sql_settings=dms_mixins.CfnDataProviderPropsMixin.MySqlSettingsProperty(
                    certificate_arn="certificateArn",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                ),
                oracle_settings=dms_mixins.CfnDataProviderPropsMixin.OracleSettingsProperty(
                    asm_server="asmServer",
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    secrets_manager_oracle_asm_access_role_arn="secretsManagerOracleAsmAccessRoleArn",
                    secrets_manager_oracle_asm_secret_id="secretsManagerOracleAsmSecretId",
                    secrets_manager_security_db_encryption_access_role_arn="secretsManagerSecurityDbEncryptionAccessRoleArn",
                    secrets_manager_security_db_encryption_secret_id="secretsManagerSecurityDbEncryptionSecretId",
                    server_name="serverName",
                    ssl_mode="sslMode"
                ),
                postgre_sql_settings=dms_mixins.CfnDataProviderPropsMixin.PostgreSqlSettingsProperty(
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                ),
                redshift_settings=dms_mixins.CfnDataProviderPropsMixin.RedshiftSettingsProperty(
                    database_name="databaseName",
                    port=123,
                    server_name="serverName"
                )
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
        props: typing.Union[CfnDataProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DMS::DataProvider``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047b83c76ce3b76269f0f183b99fde0cef0ecc938f18a86ee9d7902a465bf9d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da92fc69cc8009cd6305c62d73c6690e0070a1994f9e478d46c4786306331d4d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f965c2bef3550e030b2ab082e4680594767f1bb89f2ab0cb3a57c5c28b828815)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataProviderMixinProps:
        return typing.cast(CfnDataProviderMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.DocDbSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "database_name": "databaseName",
            "port": "port",
            "server_name": "serverName",
            "ssl_mode": "sslMode",
        },
    )
    class DocDbSettingsProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
            ssl_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a DocumentDB endpoint.

            :param certificate_arn: 
            :param database_name: The database name on the DocumentDB source endpoint.
            :param port: The port value for the DocumentDB source endpoint.
            :param server_name: The name of the server on the DocumentDB source endpoint.
            :param ssl_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-docdbsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                doc_db_settings_property = dms_mixins.CfnDataProviderPropsMixin.DocDbSettingsProperty(
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f7b63b32f64134a49cab5cc53172f2d392a191f418ccb5a2e0374675b026e7d)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name
            if ssl_mode is not None:
                self._values["ssl_mode"] = ssl_mode

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-docdbsettings.html#cfn-dms-dataprovider-docdbsettings-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The database name on the DocumentDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-docdbsettings.html#cfn-dms-dataprovider-docdbsettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port value for the DocumentDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-docdbsettings.html#cfn-dms-dataprovider-docdbsettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''The name of the server on the DocumentDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-docdbsettings.html#cfn-dms-dataprovider-docdbsettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-docdbsettings.html#cfn-dms-dataprovider-docdbsettings-sslmode
            '''
            result = self._values.get("ssl_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocDbSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.IbmDb2LuwSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "database_name": "databaseName",
            "port": "port",
            "server_name": "serverName",
            "ssl_mode": "sslMode",
        },
    )
    class IbmDb2LuwSettingsProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
            ssl_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''IbmDb2LuwSettings property identifier.

            :param certificate_arn: 
            :param database_name: 
            :param port: 
            :param server_name: 
            :param ssl_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2luwsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                ibm_db2_luw_settings_property = dms_mixins.CfnDataProviderPropsMixin.IbmDb2LuwSettingsProperty(
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8aae24464632da8194c4c0edff59fea61c395c83ae1e11721de742929d33537)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name
            if ssl_mode is not None:
                self._values["ssl_mode"] = ssl_mode

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2luwsettings.html#cfn-dms-dataprovider-ibmdb2luwsettings-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2luwsettings.html#cfn-dms-dataprovider-ibmdb2luwsettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2luwsettings.html#cfn-dms-dataprovider-ibmdb2luwsettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2luwsettings.html#cfn-dms-dataprovider-ibmdb2luwsettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2luwsettings.html#cfn-dms-dataprovider-ibmdb2luwsettings-sslmode
            '''
            result = self._values.get("ssl_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IbmDb2LuwSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.IbmDb2zOsSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "database_name": "databaseName",
            "port": "port",
            "server_name": "serverName",
            "ssl_mode": "sslMode",
        },
    )
    class IbmDb2zOsSettingsProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
            ssl_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''IbmDb2zOsSettings property identifier.

            :param certificate_arn: 
            :param database_name: 
            :param port: 
            :param server_name: 
            :param ssl_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2zossettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                ibm_db2z_os_settings_property = dms_mixins.CfnDataProviderPropsMixin.IbmDb2zOsSettingsProperty(
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8391960543eeecd5e6487fbc965cbbb5300ac881b612c520fd962d994b990045)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name
            if ssl_mode is not None:
                self._values["ssl_mode"] = ssl_mode

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2zossettings.html#cfn-dms-dataprovider-ibmdb2zossettings-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2zossettings.html#cfn-dms-dataprovider-ibmdb2zossettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2zossettings.html#cfn-dms-dataprovider-ibmdb2zossettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2zossettings.html#cfn-dms-dataprovider-ibmdb2zossettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-ibmdb2zossettings.html#cfn-dms-dataprovider-ibmdb2zossettings-sslmode
            '''
            result = self._values.get("ssl_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IbmDb2zOsSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.MariaDbSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "port": "port",
            "server_name": "serverName",
            "ssl_mode": "sslMode",
        },
    )
    class MariaDbSettingsProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
            ssl_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''MariaDbSettings property identifier.

            :param certificate_arn: 
            :param port: 
            :param server_name: 
            :param ssl_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mariadbsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                maria_db_settings_property = dms_mixins.CfnDataProviderPropsMixin.MariaDbSettingsProperty(
                    certificate_arn="certificateArn",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ae35873fd5ba7f5015eb9392070fe20b3ce0bb42120d9ce43173bbcddd93899)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name
            if ssl_mode is not None:
                self._values["ssl_mode"] = ssl_mode

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mariadbsettings.html#cfn-dms-dataprovider-mariadbsettings-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mariadbsettings.html#cfn-dms-dataprovider-mariadbsettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mariadbsettings.html#cfn-dms-dataprovider-mariadbsettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mariadbsettings.html#cfn-dms-dataprovider-mariadbsettings-sslmode
            '''
            result = self._values.get("ssl_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MariaDbSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.MicrosoftSqlServerSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "database_name": "databaseName",
            "port": "port",
            "server_name": "serverName",
            "ssl_mode": "sslMode",
        },
    )
    class MicrosoftSqlServerSettingsProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
            ssl_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a Microsoft SQL Server endpoint.

            :param certificate_arn: 
            :param database_name: Database name for the endpoint.
            :param port: Endpoint TCP port.
            :param server_name: Fully qualified domain name of the endpoint. For an Amazon RDS SQL Server instance, this is the output of `DescribeDBInstances <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>`_ , in the ``[Endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_Endpoint.html) .Address`` field.
            :param ssl_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-microsoftsqlserversettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                microsoft_sql_server_settings_property = dms_mixins.CfnDataProviderPropsMixin.MicrosoftSqlServerSettingsProperty(
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf0d9578d1246fe7d44409d8b7340727750f5da95d920958cb5a7f891f1c0603)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name
            if ssl_mode is not None:
                self._values["ssl_mode"] = ssl_mode

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-microsoftsqlserversettings.html#cfn-dms-dataprovider-microsoftsqlserversettings-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''Database name for the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-microsoftsqlserversettings.html#cfn-dms-dataprovider-microsoftsqlserversettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''Endpoint TCP port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-microsoftsqlserversettings.html#cfn-dms-dataprovider-microsoftsqlserversettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''Fully qualified domain name of the endpoint.

            For an Amazon RDS SQL Server instance, this is the output of `DescribeDBInstances <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>`_ , in the ``[Endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_Endpoint.html) .Address`` field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-microsoftsqlserversettings.html#cfn-dms-dataprovider-microsoftsqlserversettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-microsoftsqlserversettings.html#cfn-dms-dataprovider-microsoftsqlserversettings-sslmode
            '''
            result = self._values.get("ssl_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MicrosoftSqlServerSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.MongoDbSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_mechanism": "authMechanism",
            "auth_source": "authSource",
            "auth_type": "authType",
            "certificate_arn": "certificateArn",
            "database_name": "databaseName",
            "port": "port",
            "server_name": "serverName",
            "ssl_mode": "sslMode",
        },
    )
    class MongoDbSettingsProperty:
        def __init__(
            self,
            *,
            auth_mechanism: typing.Optional[builtins.str] = None,
            auth_source: typing.Optional[builtins.str] = None,
            auth_type: typing.Optional[builtins.str] = None,
            certificate_arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
            ssl_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a MongoDB endpoint.

            :param auth_mechanism: The authentication mechanism you use to access the MongoDB source endpoint. For the default value, in MongoDB version 2.x, ``"default"`` is ``"mongodb_cr"`` . For MongoDB version 3.x or later, ``"default"`` is ``"scram_sha_1"`` . This setting isn't used when ``AuthType`` is set to ``"no"`` .
            :param auth_source: The MongoDB database name. This setting isn't used when ``AuthType`` is set to ``"no"`` . The default is ``"admin"`` .
            :param auth_type: The authentication type you use to access the MongoDB source endpoint. When when set to ``"no"`` , user name and password parameters are not used and can be empty.
            :param certificate_arn: 
            :param database_name: The database name on the MongoDB source endpoint.
            :param port: The port value for the MongoDB source endpoint.
            :param server_name: The name of the server on the MongoDB source endpoint. For MongoDB Atlas, provide the server name for any of the servers in the replication set.
            :param ssl_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mongodbsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                mongo_db_settings_property = dms_mixins.CfnDataProviderPropsMixin.MongoDbSettingsProperty(
                    auth_mechanism="authMechanism",
                    auth_source="authSource",
                    auth_type="authType",
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4dafb406842c97c219ec3faa01b1f05c37df1713fadf16e04589be98d87cb9e3)
                check_type(argname="argument auth_mechanism", value=auth_mechanism, expected_type=type_hints["auth_mechanism"])
                check_type(argname="argument auth_source", value=auth_source, expected_type=type_hints["auth_source"])
                check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_mechanism is not None:
                self._values["auth_mechanism"] = auth_mechanism
            if auth_source is not None:
                self._values["auth_source"] = auth_source
            if auth_type is not None:
                self._values["auth_type"] = auth_type
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name
            if ssl_mode is not None:
                self._values["ssl_mode"] = ssl_mode

        @builtins.property
        def auth_mechanism(self) -> typing.Optional[builtins.str]:
            '''The authentication mechanism you use to access the MongoDB source endpoint.

            For the default value, in MongoDB version 2.x, ``"default"`` is ``"mongodb_cr"`` . For MongoDB version 3.x or later, ``"default"`` is ``"scram_sha_1"`` . This setting isn't used when ``AuthType`` is set to ``"no"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mongodbsettings.html#cfn-dms-dataprovider-mongodbsettings-authmechanism
            '''
            result = self._values.get("auth_mechanism")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auth_source(self) -> typing.Optional[builtins.str]:
            '''The MongoDB database name. This setting isn't used when ``AuthType`` is set to ``"no"`` .

            The default is ``"admin"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mongodbsettings.html#cfn-dms-dataprovider-mongodbsettings-authsource
            '''
            result = self._values.get("auth_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auth_type(self) -> typing.Optional[builtins.str]:
            '''The authentication type you use to access the MongoDB source endpoint.

            When when set to ``"no"`` , user name and password parameters are not used and can be empty.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mongodbsettings.html#cfn-dms-dataprovider-mongodbsettings-authtype
            '''
            result = self._values.get("auth_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mongodbsettings.html#cfn-dms-dataprovider-mongodbsettings-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The database name on the MongoDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mongodbsettings.html#cfn-dms-dataprovider-mongodbsettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port value for the MongoDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mongodbsettings.html#cfn-dms-dataprovider-mongodbsettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''The name of the server on the MongoDB source endpoint.

            For MongoDB Atlas, provide the server name for any of the servers in the replication set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mongodbsettings.html#cfn-dms-dataprovider-mongodbsettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mongodbsettings.html#cfn-dms-dataprovider-mongodbsettings-sslmode
            '''
            result = self._values.get("ssl_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MongoDbSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.MySqlSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "port": "port",
            "server_name": "serverName",
            "ssl_mode": "sslMode",
        },
    )
    class MySqlSettingsProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
            ssl_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a MySQL endpoint.

            :param certificate_arn: 
            :param port: Endpoint TCP port.
            :param server_name: The host name of the endpoint database. For an Amazon RDS MySQL instance, this is the output of `DescribeDBInstances <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>`_ , in the ``[Endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_Endpoint.html) .Address`` field. For an Aurora MySQL instance, this is the output of `DescribeDBClusters <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBClusters.html>`_ , in the ``Endpoint`` field.
            :param ssl_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mysqlsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                my_sql_settings_property = dms_mixins.CfnDataProviderPropsMixin.MySqlSettingsProperty(
                    certificate_arn="certificateArn",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65c3869ac264ec65ed20d092b3d84b8e2087218efad19450b8b12d301951b857)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name
            if ssl_mode is not None:
                self._values["ssl_mode"] = ssl_mode

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mysqlsettings.html#cfn-dms-dataprovider-mysqlsettings-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''Endpoint TCP port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mysqlsettings.html#cfn-dms-dataprovider-mysqlsettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''The host name of the endpoint database.

            For an Amazon RDS MySQL instance, this is the output of `DescribeDBInstances <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>`_ , in the ``[Endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_Endpoint.html) .Address`` field.

            For an Aurora MySQL instance, this is the output of `DescribeDBClusters <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBClusters.html>`_ , in the ``Endpoint`` field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mysqlsettings.html#cfn-dms-dataprovider-mysqlsettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-mysqlsettings.html#cfn-dms-dataprovider-mysqlsettings-sslmode
            '''
            result = self._values.get("ssl_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MySqlSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.OracleSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "asm_server": "asmServer",
            "certificate_arn": "certificateArn",
            "database_name": "databaseName",
            "port": "port",
            "secrets_manager_oracle_asm_access_role_arn": "secretsManagerOracleAsmAccessRoleArn",
            "secrets_manager_oracle_asm_secret_id": "secretsManagerOracleAsmSecretId",
            "secrets_manager_security_db_encryption_access_role_arn": "secretsManagerSecurityDbEncryptionAccessRoleArn",
            "secrets_manager_security_db_encryption_secret_id": "secretsManagerSecurityDbEncryptionSecretId",
            "server_name": "serverName",
            "ssl_mode": "sslMode",
        },
    )
    class OracleSettingsProperty:
        def __init__(
            self,
            *,
            asm_server: typing.Optional[builtins.str] = None,
            certificate_arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            secrets_manager_oracle_asm_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_oracle_asm_secret_id: typing.Optional[builtins.str] = None,
            secrets_manager_security_db_encryption_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_security_db_encryption_secret_id: typing.Optional[builtins.str] = None,
            server_name: typing.Optional[builtins.str] = None,
            ssl_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines an Oracle endpoint.

            :param asm_server: For an Oracle source endpoint, your ASM server address. You can set this value from the ``asm_server`` value. You set ``asm_server`` as part of the extra connection attribute string to access an Oracle server with Binary Reader that uses ASM. For more information, see `Configuration for change data capture (CDC) on an Oracle source database <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC.Configuration>`_ .
            :param certificate_arn: 
            :param database_name: Database name for the endpoint.
            :param port: Endpoint TCP port.
            :param secrets_manager_oracle_asm_access_role_arn: Required only if your Oracle endpoint uses Automatic Storage Management (ASM). The full ARN of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the ``SecretsManagerOracleAsmSecret`` . This ``SecretsManagerOracleAsmSecret`` has the secret value that allows access to the Oracle ASM of the endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerOracleAsmSecretId`` . Or you can specify clear-text values for ``AsmUser`` , ``AsmPassword`` , and ``AsmServerName`` . You can't specify both. For more information on creating this ``SecretsManagerOracleAsmSecret`` and the ``SecretsManagerOracleAsmAccessRoleArn`` and ``SecretsManagerOracleAsmSecretId`` required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_oracle_asm_secret_id: Required only if your Oracle endpoint uses Automatic Storage Management (ASM). The full ARN, partial ARN, or friendly name of the ``SecretsManagerOracleAsmSecret`` that contains the Oracle ASM connection details for the Oracle endpoint.
            :param secrets_manager_security_db_encryption_access_role_arn: 
            :param secrets_manager_security_db_encryption_secret_id: 
            :param server_name: Fully qualified domain name of the endpoint. For an Amazon RDS Oracle instance, this is the output of `DescribeDBInstances <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>`_ , in the ``[Endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_Endpoint.html) .Address`` field.
            :param ssl_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                oracle_settings_property = dms_mixins.CfnDataProviderPropsMixin.OracleSettingsProperty(
                    asm_server="asmServer",
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    secrets_manager_oracle_asm_access_role_arn="secretsManagerOracleAsmAccessRoleArn",
                    secrets_manager_oracle_asm_secret_id="secretsManagerOracleAsmSecretId",
                    secrets_manager_security_db_encryption_access_role_arn="secretsManagerSecurityDbEncryptionAccessRoleArn",
                    secrets_manager_security_db_encryption_secret_id="secretsManagerSecurityDbEncryptionSecretId",
                    server_name="serverName",
                    ssl_mode="sslMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31292ce834981b09d01ff3ec1420b2d85c6c6590e771777fda90f28c6885cd40)
                check_type(argname="argument asm_server", value=asm_server, expected_type=type_hints["asm_server"])
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument secrets_manager_oracle_asm_access_role_arn", value=secrets_manager_oracle_asm_access_role_arn, expected_type=type_hints["secrets_manager_oracle_asm_access_role_arn"])
                check_type(argname="argument secrets_manager_oracle_asm_secret_id", value=secrets_manager_oracle_asm_secret_id, expected_type=type_hints["secrets_manager_oracle_asm_secret_id"])
                check_type(argname="argument secrets_manager_security_db_encryption_access_role_arn", value=secrets_manager_security_db_encryption_access_role_arn, expected_type=type_hints["secrets_manager_security_db_encryption_access_role_arn"])
                check_type(argname="argument secrets_manager_security_db_encryption_secret_id", value=secrets_manager_security_db_encryption_secret_id, expected_type=type_hints["secrets_manager_security_db_encryption_secret_id"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asm_server is not None:
                self._values["asm_server"] = asm_server
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if port is not None:
                self._values["port"] = port
            if secrets_manager_oracle_asm_access_role_arn is not None:
                self._values["secrets_manager_oracle_asm_access_role_arn"] = secrets_manager_oracle_asm_access_role_arn
            if secrets_manager_oracle_asm_secret_id is not None:
                self._values["secrets_manager_oracle_asm_secret_id"] = secrets_manager_oracle_asm_secret_id
            if secrets_manager_security_db_encryption_access_role_arn is not None:
                self._values["secrets_manager_security_db_encryption_access_role_arn"] = secrets_manager_security_db_encryption_access_role_arn
            if secrets_manager_security_db_encryption_secret_id is not None:
                self._values["secrets_manager_security_db_encryption_secret_id"] = secrets_manager_security_db_encryption_secret_id
            if server_name is not None:
                self._values["server_name"] = server_name
            if ssl_mode is not None:
                self._values["ssl_mode"] = ssl_mode

        @builtins.property
        def asm_server(self) -> typing.Optional[builtins.str]:
            '''For an Oracle source endpoint, your ASM server address.

            You can set this value from the ``asm_server`` value. You set ``asm_server`` as part of the extra connection attribute string to access an Oracle server with Binary Reader that uses ASM. For more information, see `Configuration for change data capture (CDC) on an Oracle source database <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC.Configuration>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html#cfn-dms-dataprovider-oraclesettings-asmserver
            '''
            result = self._values.get("asm_server")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html#cfn-dms-dataprovider-oraclesettings-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''Database name for the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html#cfn-dms-dataprovider-oraclesettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''Endpoint TCP port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html#cfn-dms-dataprovider-oraclesettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def secrets_manager_oracle_asm_access_role_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''Required only if your Oracle endpoint uses Automatic Storage Management (ASM).

            The full ARN of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the ``SecretsManagerOracleAsmSecret`` . This ``SecretsManagerOracleAsmSecret`` has the secret value that allows access to the Oracle ASM of the endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerOracleAsmSecretId`` . Or you can specify clear-text values for ``AsmUser`` , ``AsmPassword`` , and ``AsmServerName`` . You can't specify both. For more information on creating this ``SecretsManagerOracleAsmSecret`` and the ``SecretsManagerOracleAsmAccessRoleArn`` and ``SecretsManagerOracleAsmSecretId`` required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html#cfn-dms-dataprovider-oraclesettings-secretsmanageroracleasmaccessrolearn
            '''
            result = self._values.get("secrets_manager_oracle_asm_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_oracle_asm_secret_id(self) -> typing.Optional[builtins.str]:
            '''Required only if your Oracle endpoint uses Automatic Storage Management (ASM).

            The full ARN, partial ARN, or friendly name of the ``SecretsManagerOracleAsmSecret`` that contains the Oracle ASM connection details for the Oracle endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html#cfn-dms-dataprovider-oraclesettings-secretsmanageroracleasmsecretid
            '''
            result = self._values.get("secrets_manager_oracle_asm_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_security_db_encryption_access_role_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html#cfn-dms-dataprovider-oraclesettings-secretsmanagersecuritydbencryptionaccessrolearn
            '''
            result = self._values.get("secrets_manager_security_db_encryption_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_security_db_encryption_secret_id(
            self,
        ) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html#cfn-dms-dataprovider-oraclesettings-secretsmanagersecuritydbencryptionsecretid
            '''
            result = self._values.get("secrets_manager_security_db_encryption_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''Fully qualified domain name of the endpoint.

            For an Amazon RDS Oracle instance, this is the output of `DescribeDBInstances <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>`_ , in the ``[Endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_Endpoint.html) .Address`` field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html#cfn-dms-dataprovider-oraclesettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-oraclesettings.html#cfn-dms-dataprovider-oraclesettings-sslmode
            '''
            result = self._values.get("ssl_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OracleSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.PostgreSqlSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "database_name": "databaseName",
            "port": "port",
            "server_name": "serverName",
            "ssl_mode": "sslMode",
        },
    )
    class PostgreSqlSettingsProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
            ssl_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a PostgreSQL endpoint.

            :param certificate_arn: 
            :param database_name: Database name for the endpoint.
            :param port: Endpoint TCP port. The default is 5432.
            :param server_name: The host name of the endpoint database. For an Amazon RDS PostgreSQL instance, this is the output of `DescribeDBInstances <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>`_ , in the ``[Endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_Endpoint.html) .Address`` field. For an Aurora PostgreSQL instance, this is the output of `DescribeDBClusters <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBClusters.html>`_ , in the ``Endpoint`` field.
            :param ssl_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-postgresqlsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                postgre_sql_settings_property = dms_mixins.CfnDataProviderPropsMixin.PostgreSqlSettingsProperty(
                    certificate_arn="certificateArn",
                    database_name="databaseName",
                    port=123,
                    server_name="serverName",
                    ssl_mode="sslMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__629201e112f0fc80806495c56e327fe4ef59d962a6b3906d65fb3708e4b58907)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name
            if ssl_mode is not None:
                self._values["ssl_mode"] = ssl_mode

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-postgresqlsettings.html#cfn-dms-dataprovider-postgresqlsettings-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''Database name for the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-postgresqlsettings.html#cfn-dms-dataprovider-postgresqlsettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''Endpoint TCP port.

            The default is 5432.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-postgresqlsettings.html#cfn-dms-dataprovider-postgresqlsettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''The host name of the endpoint database.

            For an Amazon RDS PostgreSQL instance, this is the output of `DescribeDBInstances <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>`_ , in the ``[Endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_Endpoint.html) .Address`` field.

            For an Aurora PostgreSQL instance, this is the output of `DescribeDBClusters <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBClusters.html>`_ , in the ``Endpoint`` field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-postgresqlsettings.html#cfn-dms-dataprovider-postgresqlsettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-postgresqlsettings.html#cfn-dms-dataprovider-postgresqlsettings-sslmode
            '''
            result = self._values.get("ssl_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PostgreSqlSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.RedshiftSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_name": "databaseName",
            "port": "port",
            "server_name": "serverName",
        },
    )
    class RedshiftSettingsProperty:
        def __init__(
            self,
            *,
            database_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines an Amazon Redshift endpoint.

            :param database_name: The name of the Amazon Redshift data warehouse (service) that you are working with.
            :param port: The port number for Amazon Redshift. The default value is 5439.
            :param server_name: The name of the Amazon Redshift cluster you are using.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-redshiftsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                redshift_settings_property = dms_mixins.CfnDataProviderPropsMixin.RedshiftSettingsProperty(
                    database_name="databaseName",
                    port=123,
                    server_name="serverName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__388bbdca2c2dad947685fce9cb7bb6a11bc24d43bdc597823bb2246c68715199)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_name is not None:
                self._values["database_name"] = database_name
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon Redshift data warehouse (service) that you are working with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-redshiftsettings.html#cfn-dms-dataprovider-redshiftsettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number for Amazon Redshift.

            The default value is 5439.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-redshiftsettings.html#cfn-dms-dataprovider-redshiftsettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon Redshift cluster you are using.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-redshiftsettings.html#cfn-dms-dataprovider-redshiftsettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnDataProviderPropsMixin.SettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "doc_db_settings": "docDbSettings",
            "ibm_db2_luw_settings": "ibmDb2LuwSettings",
            "ibm_db2_z_os_settings": "ibmDb2ZOsSettings",
            "maria_db_settings": "mariaDbSettings",
            "microsoft_sql_server_settings": "microsoftSqlServerSettings",
            "mongo_db_settings": "mongoDbSettings",
            "my_sql_settings": "mySqlSettings",
            "oracle_settings": "oracleSettings",
            "postgre_sql_settings": "postgreSqlSettings",
            "redshift_settings": "redshiftSettings",
        },
    )
    class SettingsProperty:
        def __init__(
            self,
            *,
            doc_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.DocDbSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ibm_db2_luw_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.IbmDb2LuwSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ibm_db2_z_os_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.IbmDb2zOsSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maria_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.MariaDbSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            microsoft_sql_server_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.MicrosoftSqlServerSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mongo_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.MongoDbSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            my_sql_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.MySqlSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            oracle_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.OracleSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            postgre_sql_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.PostgreSqlSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            redshift_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProviderPropsMixin.RedshiftSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The property identifies the exact type of settings for the data provider.

            :param doc_db_settings: DocDbSettings property identifier.
            :param ibm_db2_luw_settings: IbmDb2LuwSettings property identifier.
            :param ibm_db2_z_os_settings: IbmDb2zOsSettings property identifier.
            :param maria_db_settings: MariaDbSettings property identifier.
            :param microsoft_sql_server_settings: MicrosoftSqlServerSettings property identifier.
            :param mongo_db_settings: MongoDbSettings property identifier.
            :param my_sql_settings: MySqlSettings property identifier.
            :param oracle_settings: OracleSettings property identifier.
            :param postgre_sql_settings: PostgreSqlSettings property identifier.
            :param redshift_settings: RedshiftSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                settings_property = dms_mixins.CfnDataProviderPropsMixin.SettingsProperty(
                    doc_db_settings=dms_mixins.CfnDataProviderPropsMixin.DocDbSettingsProperty(
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    ibm_db2_luw_settings=dms_mixins.CfnDataProviderPropsMixin.IbmDb2LuwSettingsProperty(
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    ibm_db2_zOs_settings=dms_mixins.CfnDataProviderPropsMixin.IbmDb2zOsSettingsProperty(
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    maria_db_settings=dms_mixins.CfnDataProviderPropsMixin.MariaDbSettingsProperty(
                        certificate_arn="certificateArn",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    microsoft_sql_server_settings=dms_mixins.CfnDataProviderPropsMixin.MicrosoftSqlServerSettingsProperty(
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    mongo_db_settings=dms_mixins.CfnDataProviderPropsMixin.MongoDbSettingsProperty(
                        auth_mechanism="authMechanism",
                        auth_source="authSource",
                        auth_type="authType",
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    my_sql_settings=dms_mixins.CfnDataProviderPropsMixin.MySqlSettingsProperty(
                        certificate_arn="certificateArn",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    oracle_settings=dms_mixins.CfnDataProviderPropsMixin.OracleSettingsProperty(
                        asm_server="asmServer",
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        secrets_manager_oracle_asm_access_role_arn="secretsManagerOracleAsmAccessRoleArn",
                        secrets_manager_oracle_asm_secret_id="secretsManagerOracleAsmSecretId",
                        secrets_manager_security_db_encryption_access_role_arn="secretsManagerSecurityDbEncryptionAccessRoleArn",
                        secrets_manager_security_db_encryption_secret_id="secretsManagerSecurityDbEncryptionSecretId",
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    postgre_sql_settings=dms_mixins.CfnDataProviderPropsMixin.PostgreSqlSettingsProperty(
                        certificate_arn="certificateArn",
                        database_name="databaseName",
                        port=123,
                        server_name="serverName",
                        ssl_mode="sslMode"
                    ),
                    redshift_settings=dms_mixins.CfnDataProviderPropsMixin.RedshiftSettingsProperty(
                        database_name="databaseName",
                        port=123,
                        server_name="serverName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a72b6f2dc1862be6d2d8a14bf262d927d9bb9b11e954f246093e50e8fadcd4c7)
                check_type(argname="argument doc_db_settings", value=doc_db_settings, expected_type=type_hints["doc_db_settings"])
                check_type(argname="argument ibm_db2_luw_settings", value=ibm_db2_luw_settings, expected_type=type_hints["ibm_db2_luw_settings"])
                check_type(argname="argument ibm_db2_z_os_settings", value=ibm_db2_z_os_settings, expected_type=type_hints["ibm_db2_z_os_settings"])
                check_type(argname="argument maria_db_settings", value=maria_db_settings, expected_type=type_hints["maria_db_settings"])
                check_type(argname="argument microsoft_sql_server_settings", value=microsoft_sql_server_settings, expected_type=type_hints["microsoft_sql_server_settings"])
                check_type(argname="argument mongo_db_settings", value=mongo_db_settings, expected_type=type_hints["mongo_db_settings"])
                check_type(argname="argument my_sql_settings", value=my_sql_settings, expected_type=type_hints["my_sql_settings"])
                check_type(argname="argument oracle_settings", value=oracle_settings, expected_type=type_hints["oracle_settings"])
                check_type(argname="argument postgre_sql_settings", value=postgre_sql_settings, expected_type=type_hints["postgre_sql_settings"])
                check_type(argname="argument redshift_settings", value=redshift_settings, expected_type=type_hints["redshift_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if doc_db_settings is not None:
                self._values["doc_db_settings"] = doc_db_settings
            if ibm_db2_luw_settings is not None:
                self._values["ibm_db2_luw_settings"] = ibm_db2_luw_settings
            if ibm_db2_z_os_settings is not None:
                self._values["ibm_db2_z_os_settings"] = ibm_db2_z_os_settings
            if maria_db_settings is not None:
                self._values["maria_db_settings"] = maria_db_settings
            if microsoft_sql_server_settings is not None:
                self._values["microsoft_sql_server_settings"] = microsoft_sql_server_settings
            if mongo_db_settings is not None:
                self._values["mongo_db_settings"] = mongo_db_settings
            if my_sql_settings is not None:
                self._values["my_sql_settings"] = my_sql_settings
            if oracle_settings is not None:
                self._values["oracle_settings"] = oracle_settings
            if postgre_sql_settings is not None:
                self._values["postgre_sql_settings"] = postgre_sql_settings
            if redshift_settings is not None:
                self._values["redshift_settings"] = redshift_settings

        @builtins.property
        def doc_db_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.DocDbSettingsProperty"]]:
            '''DocDbSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html#cfn-dms-dataprovider-settings-docdbsettings
            '''
            result = self._values.get("doc_db_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.DocDbSettingsProperty"]], result)

        @builtins.property
        def ibm_db2_luw_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.IbmDb2LuwSettingsProperty"]]:
            '''IbmDb2LuwSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html#cfn-dms-dataprovider-settings-ibmdb2luwsettings
            '''
            result = self._values.get("ibm_db2_luw_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.IbmDb2LuwSettingsProperty"]], result)

        @builtins.property
        def ibm_db2_z_os_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.IbmDb2zOsSettingsProperty"]]:
            '''IbmDb2zOsSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html#cfn-dms-dataprovider-settings-ibmdb2zossettings
            '''
            result = self._values.get("ibm_db2_z_os_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.IbmDb2zOsSettingsProperty"]], result)

        @builtins.property
        def maria_db_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.MariaDbSettingsProperty"]]:
            '''MariaDbSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html#cfn-dms-dataprovider-settings-mariadbsettings
            '''
            result = self._values.get("maria_db_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.MariaDbSettingsProperty"]], result)

        @builtins.property
        def microsoft_sql_server_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.MicrosoftSqlServerSettingsProperty"]]:
            '''MicrosoftSqlServerSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html#cfn-dms-dataprovider-settings-microsoftsqlserversettings
            '''
            result = self._values.get("microsoft_sql_server_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.MicrosoftSqlServerSettingsProperty"]], result)

        @builtins.property
        def mongo_db_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.MongoDbSettingsProperty"]]:
            '''MongoDbSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html#cfn-dms-dataprovider-settings-mongodbsettings
            '''
            result = self._values.get("mongo_db_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.MongoDbSettingsProperty"]], result)

        @builtins.property
        def my_sql_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.MySqlSettingsProperty"]]:
            '''MySqlSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html#cfn-dms-dataprovider-settings-mysqlsettings
            '''
            result = self._values.get("my_sql_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.MySqlSettingsProperty"]], result)

        @builtins.property
        def oracle_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.OracleSettingsProperty"]]:
            '''OracleSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html#cfn-dms-dataprovider-settings-oraclesettings
            '''
            result = self._values.get("oracle_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.OracleSettingsProperty"]], result)

        @builtins.property
        def postgre_sql_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.PostgreSqlSettingsProperty"]]:
            '''PostgreSqlSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html#cfn-dms-dataprovider-settings-postgresqlsettings
            '''
            result = self._values.get("postgre_sql_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.PostgreSqlSettingsProperty"]], result)

        @builtins.property
        def redshift_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.RedshiftSettingsProperty"]]:
            '''RedshiftSettings property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-dataprovider-settings.html#cfn-dms-dataprovider-settings-redshiftsettings
            '''
            result = self._values.get("redshift_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProviderPropsMixin.RedshiftSettingsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_arn": "certificateArn",
        "database_name": "databaseName",
        "doc_db_settings": "docDbSettings",
        "dynamo_db_settings": "dynamoDbSettings",
        "elasticsearch_settings": "elasticsearchSettings",
        "endpoint_identifier": "endpointIdentifier",
        "endpoint_type": "endpointType",
        "engine_name": "engineName",
        "extra_connection_attributes": "extraConnectionAttributes",
        "gcp_my_sql_settings": "gcpMySqlSettings",
        "ibm_db2_settings": "ibmDb2Settings",
        "kafka_settings": "kafkaSettings",
        "kinesis_settings": "kinesisSettings",
        "kms_key_id": "kmsKeyId",
        "microsoft_sql_server_settings": "microsoftSqlServerSettings",
        "mongo_db_settings": "mongoDbSettings",
        "my_sql_settings": "mySqlSettings",
        "neptune_settings": "neptuneSettings",
        "oracle_settings": "oracleSettings",
        "password": "password",
        "port": "port",
        "postgre_sql_settings": "postgreSqlSettings",
        "redis_settings": "redisSettings",
        "redshift_settings": "redshiftSettings",
        "resource_identifier": "resourceIdentifier",
        "s3_settings": "s3Settings",
        "server_name": "serverName",
        "ssl_mode": "sslMode",
        "sybase_settings": "sybaseSettings",
        "tags": "tags",
        "username": "username",
    },
)
class CfnEndpointMixinProps:
    def __init__(
        self,
        *,
        certificate_arn: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        doc_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.DocDbSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dynamo_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.DynamoDbSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        elasticsearch_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.ElasticsearchSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        endpoint_identifier: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        engine_name: typing.Optional[builtins.str] = None,
        extra_connection_attributes: typing.Optional[builtins.str] = None,
        gcp_my_sql_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.GcpMySQLSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ibm_db2_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.IbmDb2SettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kafka_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.KafkaSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kinesis_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.KinesisSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        microsoft_sql_server_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.MicrosoftSqlServerSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        mongo_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.MongoDbSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        my_sql_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.MySqlSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        neptune_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.NeptuneSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        oracle_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.OracleSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        postgre_sql_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.PostgreSqlSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        redis_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.RedisSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        redshift_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.RedshiftSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_identifier: typing.Optional[builtins.str] = None,
        s3_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.S3SettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        server_name: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
        sybase_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointPropsMixin.SybaseSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEndpointPropsMixin.

        :param certificate_arn: The Amazon Resource Name (ARN) for the certificate.
        :param database_name: The name of the endpoint database. For a MySQL source or target endpoint, don't specify ``DatabaseName`` . To migrate to a specific database, use this setting and ``targetDbType`` .
        :param doc_db_settings: Settings in JSON format for the source and target DocumentDB endpoint. For more information about other available settings, see `Using extra connections attributes with Amazon DocumentDB as a source <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.DocumentDB.html#CHAP_Source.DocumentDB.ECAs>`_ and `Using Amazon DocumentDB as a target for AWS Database Migration Service <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.DocumentDB.html>`_ in the *AWS Database Migration Service User Guide* .
        :param dynamo_db_settings: Settings in JSON format for the target Amazon DynamoDB endpoint. For information about other available settings, see `Using object mapping to migrate data to DynamoDB <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.DynamoDB.html#CHAP_Target.DynamoDB.ObjectMapping>`_ in the *AWS Database Migration Service User Guide* .
        :param elasticsearch_settings: Settings in JSON format for the target OpenSearch endpoint. For more information about the available settings, see `Extra connection attributes when using OpenSearch as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Elasticsearch.html#CHAP_Target.Elasticsearch.Configuration>`_ in the *AWS Database Migration Service User Guide* .
        :param endpoint_identifier: The database endpoint identifier. Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.
        :param endpoint_type: The type of endpoint. Valid values are ``source`` and ``target`` .
        :param engine_name: The type of engine for the endpoint, depending on the ``EndpointType`` value. *Valid values* : ``mysql`` | ``oracle`` | ``postgres`` | ``mariadb`` | ``aurora`` | ``aurora-postgresql`` | ``opensearch`` | ``redshift`` | ``redshift-serverless`` | ``s3`` | ``db2`` | ``azuredb`` | ``sybase`` | ``dynamodb`` | ``mongodb`` | ``kinesis`` | ``kafka`` | ``elasticsearch`` | ``docdb`` | ``sqlserver`` | ``neptune``
        :param extra_connection_attributes: Additional attributes associated with the connection. Each attribute is specified as a name-value pair associated by an equal sign (=). Multiple attributes are separated by a semicolon (;) with no additional white space. For information on the attributes available for connecting your source or target endpoint, see `Working with AWS DMS Endpoints <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Endpoints.html>`_ in the *AWS Database Migration Service User Guide* .
        :param gcp_my_sql_settings: Settings in JSON format for the source GCP MySQL endpoint. These settings are much the same as the settings for any MySQL-compatible endpoint. For more information, see `Extra connection attributes when using MySQL as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html#CHAP_Source.MySQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .
        :param ibm_db2_settings: Settings in JSON format for the source IBM Db2 LUW endpoint. For information about other available settings, see `Extra connection attributes when using Db2 LUW as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.DB2.html#CHAP_Source.DB2.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .
        :param kafka_settings: Settings in JSON format for the target Apache Kafka endpoint. For more information about other available settings, see `Using object mapping to migrate data to a Kafka topic <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Kafka.html#CHAP_Target.Kafka.ObjectMapping>`_ in the *AWS Database Migration Service User Guide* .
        :param kinesis_settings: Settings in JSON format for the target endpoint for Amazon Kinesis Data Streams. For more information about other available settings, see `Using object mapping to migrate data to a Kinesis data stream <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Kinesis.html#CHAP_Target.Kinesis.ObjectMapping>`_ in the *AWS Database Migration Service User Guide* .
        :param kms_key_id: An AWS key identifier that is used to encrypt the connection parameters for the endpoint. If you don't specify a value for the ``KmsKeyId`` parameter, AWS DMS uses your default encryption key. AWS creates the default encryption key for your AWS account . Your AWS account has a different default encryption key for each AWS Region .
        :param microsoft_sql_server_settings: Settings in JSON format for the source and target Microsoft SQL Server endpoint. For information about other available settings, see `Extra connection attributes when using SQL Server as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.SQLServer.html#CHAP_Source.SQLServer.ConnectionAttrib>`_ and `Extra connection attributes when using SQL Server as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.SQLServer.html#CHAP_Target.SQLServer.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .
        :param mongo_db_settings: Settings in JSON format for the source MongoDB endpoint. For more information about the available settings, see `Using MongoDB as a target for AWS Database Migration Service <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MongoDB.html#CHAP_Source.MongoDB.Configuration>`_ in the *AWS Database Migration Service User Guide* .
        :param my_sql_settings: Settings in JSON format for the source and target MySQL endpoint. For information about other available settings, see `Extra connection attributes when using MySQL as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html#CHAP_Source.MySQL.ConnectionAttrib>`_ and `Extra connection attributes when using a MySQL-compatible database as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.MySQL.html#CHAP_Target.MySQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .
        :param neptune_settings: Settings in JSON format for the target Amazon Neptune endpoint. For more information about the available settings, see `Specifying endpoint settings for Amazon Neptune as a target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Neptune.html#CHAP_Target.Neptune.EndpointSettings>`_ in the *AWS Database Migration Service User Guide* .
        :param oracle_settings: Settings in JSON format for the source and target Oracle endpoint. For information about other available settings, see `Extra connection attributes when using Oracle as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.ConnectionAttrib>`_ and `Extra connection attributes when using Oracle as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Oracle.html#CHAP_Target.Oracle.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .
        :param password: The password to be used to log in to the endpoint database.
        :param port: The port used by the endpoint database.
        :param postgre_sql_settings: Settings in JSON format for the source and target PostgreSQL endpoint. For information about other available settings, see `Extra connection attributes when using PostgreSQL as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.PostgreSQL.html#CHAP_Source.PostgreSQL.ConnectionAttrib>`_ and `Extra connection attributes when using PostgreSQL as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.PostgreSQL.html#CHAP_Target.PostgreSQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .
        :param redis_settings: Settings in JSON format for the target Redis endpoint. For information about other available settings, see `Specifying endpoint settings for Redis as a target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Redis.html#CHAP_Target.Redis.EndpointSettings>`_ in the *AWS Database Migration Service User Guide* .
        :param redshift_settings: Settings in JSON format for the Amazon Redshift endpoint. For more information about other available settings, see `Extra connection attributes when using Amazon Redshift as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Redshift.html#CHAP_Target.Redshift.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .
        :param resource_identifier: A display name for the resource identifier at the end of the ``EndpointArn`` response parameter that is returned in the created ``Endpoint`` object. The value for this parameter can have up to 31 characters. It can contain only ASCII letters, digits, and hyphen ('-'). Also, it can't end with a hyphen or contain two consecutive hyphens, and can only begin with a letter, such as ``Example-App-ARN1`` . For example, this value might result in the ``EndpointArn`` value ``arn:aws:dms:eu-west-1:012345678901:rep:Example-App-ARN1`` . If you don't specify a ``ResourceIdentifier`` value, AWS DMS generates a default identifier value for the end of ``EndpointArn`` .
        :param s3_settings: Settings in JSON format for the source and target Amazon S3 endpoint. For more information about other available settings, see `Extra connection attributes when using Amazon S3 as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.S3.html#CHAP_Source.S3.Configuring>`_ and `Extra connection attributes when using Amazon S3 as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring>`_ in the *AWS Database Migration Service User Guide* .
        :param server_name: The name of the server where the endpoint database resides.
        :param ssl_mode: The Secure Sockets Layer (SSL) mode to use for the SSL connection. The default is ``none`` . .. epigraph:: When ``engine_name`` is set to S3, the only allowed value is ``none`` .
        :param sybase_settings: Settings in JSON format for the source and target SAP ASE endpoint. For information about other available settings, see `Extra connection attributes when using SAP ASE as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.SAP.html#CHAP_Source.SAP.ConnectionAttrib>`_ and `Extra connection attributes when using SAP ASE as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.SAP.html#CHAP_Target.SAP.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .
        :param tags: One or more tags to be assigned to the endpoint.
        :param username: The user name to be used to log in to the endpoint database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            cfn_endpoint_mixin_props = dms_mixins.CfnEndpointMixinProps(
                certificate_arn="certificateArn",
                database_name="databaseName",
                doc_db_settings=dms_mixins.CfnEndpointPropsMixin.DocDbSettingsProperty(
                    docs_to_investigate=123,
                    extract_doc_id=False,
                    nesting_level="nestingLevel",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId"
                ),
                dynamo_db_settings=dms_mixins.CfnEndpointPropsMixin.DynamoDbSettingsProperty(
                    service_access_role_arn="serviceAccessRoleArn"
                ),
                elasticsearch_settings=dms_mixins.CfnEndpointPropsMixin.ElasticsearchSettingsProperty(
                    endpoint_uri="endpointUri",
                    error_retry_duration=123,
                    full_load_error_percentage=123,
                    service_access_role_arn="serviceAccessRoleArn"
                ),
                endpoint_identifier="endpointIdentifier",
                endpoint_type="endpointType",
                engine_name="engineName",
                extra_connection_attributes="extraConnectionAttributes",
                gcp_my_sql_settings=dms_mixins.CfnEndpointPropsMixin.GcpMySQLSettingsProperty(
                    after_connect_script="afterConnectScript",
                    clean_source_metadata_on_mismatch=False,
                    database_name="databaseName",
                    events_poll_interval=123,
                    max_file_size=123,
                    parallel_load_threads=123,
                    password="password",
                    port=123,
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    server_name="serverName",
                    server_timezone="serverTimezone",
                    username="username"
                ),
                ibm_db2_settings=dms_mixins.CfnEndpointPropsMixin.IbmDb2SettingsProperty(
                    current_lsn="currentLsn",
                    keep_csv_files=False,
                    load_timeout=123,
                    max_file_size=123,
                    max_kBytes_per_read=123,
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    set_data_capture_changes=False,
                    write_buffer_size=123
                ),
                kafka_settings=dms_mixins.CfnEndpointPropsMixin.KafkaSettingsProperty(
                    broker="broker",
                    include_control_details=False,
                    include_null_and_empty=False,
                    include_partition_value=False,
                    include_table_alter_operations=False,
                    include_transaction_details=False,
                    message_format="messageFormat",
                    message_max_bytes=123,
                    no_hex_prefix=False,
                    partition_include_schema_table=False,
                    sasl_password="saslPassword",
                    sasl_user_name="saslUserName",
                    security_protocol="securityProtocol",
                    ssl_ca_certificate_arn="sslCaCertificateArn",
                    ssl_client_certificate_arn="sslClientCertificateArn",
                    ssl_client_key_arn="sslClientKeyArn",
                    ssl_client_key_password="sslClientKeyPassword",
                    topic="topic"
                ),
                kinesis_settings=dms_mixins.CfnEndpointPropsMixin.KinesisSettingsProperty(
                    include_control_details=False,
                    include_null_and_empty=False,
                    include_partition_value=False,
                    include_table_alter_operations=False,
                    include_transaction_details=False,
                    message_format="messageFormat",
                    no_hex_prefix=False,
                    partition_include_schema_table=False,
                    service_access_role_arn="serviceAccessRoleArn",
                    stream_arn="streamArn"
                ),
                kms_key_id="kmsKeyId",
                microsoft_sql_server_settings=dms_mixins.CfnEndpointPropsMixin.MicrosoftSqlServerSettingsProperty(
                    bcp_packet_size=123,
                    control_tables_file_group="controlTablesFileGroup",
                    database_name="databaseName",
                    force_lob_lookup=False,
                    password="password",
                    port=123,
                    query_single_always_on_node=False,
                    read_backup_only=False,
                    safeguard_policy="safeguardPolicy",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    server_name="serverName",
                    tlog_access_mode="tlogAccessMode",
                    trim_space_in_char=False,
                    use_bcp_full_load=False,
                    username="username",
                    use_third_party_backup_device=False
                ),
                mongo_db_settings=dms_mixins.CfnEndpointPropsMixin.MongoDbSettingsProperty(
                    auth_mechanism="authMechanism",
                    auth_source="authSource",
                    auth_type="authType",
                    database_name="databaseName",
                    docs_to_investigate="docsToInvestigate",
                    extract_doc_id="extractDocId",
                    nesting_level="nestingLevel",
                    password="password",
                    port=123,
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    server_name="serverName",
                    username="username"
                ),
                my_sql_settings=dms_mixins.CfnEndpointPropsMixin.MySqlSettingsProperty(
                    after_connect_script="afterConnectScript",
                    clean_source_metadata_on_mismatch=False,
                    events_poll_interval=123,
                    max_file_size=123,
                    parallel_load_threads=123,
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    server_timezone="serverTimezone",
                    target_db_type="targetDbType"
                ),
                neptune_settings=dms_mixins.CfnEndpointPropsMixin.NeptuneSettingsProperty(
                    error_retry_duration=123,
                    iam_auth_enabled=False,
                    max_file_size=123,
                    max_retry_count=123,
                    s3_bucket_folder="s3BucketFolder",
                    s3_bucket_name="s3BucketName",
                    service_access_role_arn="serviceAccessRoleArn"
                ),
                oracle_settings=dms_mixins.CfnEndpointPropsMixin.OracleSettingsProperty(
                    access_alternate_directly=False,
                    additional_archived_log_dest_id=123,
                    add_supplemental_logging=False,
                    allow_select_nested_tables=False,
                    archived_log_dest_id=123,
                    archived_logs_only=False,
                    asm_password="asmPassword",
                    asm_server="asmServer",
                    asm_user="asmUser",
                    char_length_semantics="charLengthSemantics",
                    direct_path_no_log=False,
                    direct_path_parallel_load=False,
                    enable_homogenous_tablespace=False,
                    extra_archived_log_dest_ids=[123],
                    fail_tasks_on_lob_truncation=False,
                    number_datatype_scale=123,
                    oracle_path_prefix="oraclePathPrefix",
                    parallel_asm_read_threads=123,
                    read_ahead_blocks=123,
                    read_table_space_name=False,
                    replace_path_prefix=False,
                    retry_interval=123,
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_oracle_asm_access_role_arn="secretsManagerOracleAsmAccessRoleArn",
                    secrets_manager_oracle_asm_secret_id="secretsManagerOracleAsmSecretId",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    security_db_encryption="securityDbEncryption",
                    security_db_encryption_name="securityDbEncryptionName",
                    spatial_data_option_to_geo_json_function_name="spatialDataOptionToGeoJsonFunctionName",
                    standby_delay_time=123,
                    use_alternate_folder_for_online=False,
                    use_bFile=False,
                    use_direct_path_full_load=False,
                    use_logminer_reader=False,
                    use_path_prefix="usePathPrefix"
                ),
                password="password",
                port=123,
                postgre_sql_settings=dms_mixins.CfnEndpointPropsMixin.PostgreSqlSettingsProperty(
                    after_connect_script="afterConnectScript",
                    babelfish_database_name="babelfishDatabaseName",
                    capture_ddls=False,
                    database_mode="databaseMode",
                    ddl_artifacts_schema="ddlArtifactsSchema",
                    execute_timeout=123,
                    fail_tasks_on_lob_truncation=False,
                    heartbeat_enable=False,
                    heartbeat_frequency=123,
                    heartbeat_schema="heartbeatSchema",
                    map_boolean_as_boolean=False,
                    max_file_size=123,
                    plugin_name="pluginName",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    slot_name="slotName"
                ),
                redis_settings=dms_mixins.CfnEndpointPropsMixin.RedisSettingsProperty(
                    auth_password="authPassword",
                    auth_type="authType",
                    auth_user_name="authUserName",
                    port=123,
                    server_name="serverName",
                    ssl_ca_certificate_arn="sslCaCertificateArn",
                    ssl_security_protocol="sslSecurityProtocol"
                ),
                redshift_settings=dms_mixins.CfnEndpointPropsMixin.RedshiftSettingsProperty(
                    accept_any_date=False,
                    after_connect_script="afterConnectScript",
                    bucket_folder="bucketFolder",
                    bucket_name="bucketName",
                    case_sensitive_names=False,
                    comp_update=False,
                    connection_timeout=123,
                    date_format="dateFormat",
                    empty_as_null=False,
                    encryption_mode="encryptionMode",
                    explicit_ids=False,
                    file_transfer_upload_streams=123,
                    load_timeout=123,
                    map_boolean_as_boolean=False,
                    max_file_size=123,
                    remove_quotes=False,
                    replace_chars="replaceChars",
                    replace_invalid_chars="replaceInvalidChars",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    server_side_encryption_kms_key_id="serverSideEncryptionKmsKeyId",
                    service_access_role_arn="serviceAccessRoleArn",
                    time_format="timeFormat",
                    trim_blanks=False,
                    truncate_columns=False,
                    write_buffer_size=123
                ),
                resource_identifier="resourceIdentifier",
                s3_settings=dms_mixins.CfnEndpointPropsMixin.S3SettingsProperty(
                    add_column_name=False,
                    add_trailing_padding_character=False,
                    bucket_folder="bucketFolder",
                    bucket_name="bucketName",
                    canned_acl_for_objects="cannedAclForObjects",
                    cdc_inserts_and_updates=False,
                    cdc_inserts_only=False,
                    cdc_max_batch_interval=123,
                    cdc_min_file_size=123,
                    cdc_path="cdcPath",
                    compression_type="compressionType",
                    csv_delimiter="csvDelimiter",
                    csv_no_sup_value="csvNoSupValue",
                    csv_null_value="csvNullValue",
                    csv_row_delimiter="csvRowDelimiter",
                    data_format="dataFormat",
                    data_page_size=123,
                    date_partition_delimiter="datePartitionDelimiter",
                    date_partition_enabled=False,
                    date_partition_sequence="datePartitionSequence",
                    date_partition_timezone="datePartitionTimezone",
                    dict_page_size_limit=123,
                    enable_statistics=False,
                    encoding_type="encodingType",
                    encryption_mode="encryptionMode",
                    expected_bucket_owner="expectedBucketOwner",
                    external_table_definition="externalTableDefinition",
                    glue_catalog_generation=False,
                    ignore_header_rows=123,
                    include_op_for_full_load=False,
                    max_file_size=123,
                    parquet_timestamp_in_millisecond=False,
                    parquet_version="parquetVersion",
                    preserve_transactions=False,
                    rfc4180=False,
                    row_group_length=123,
                    server_side_encryption_kms_key_id="serverSideEncryptionKmsKeyId",
                    service_access_role_arn="serviceAccessRoleArn",
                    timestamp_column_name="timestampColumnName",
                    use_csv_no_sup_value=False,
                    use_task_start_time_for_full_load_timestamp=False
                ),
                server_name="serverName",
                ssl_mode="sslMode",
                sybase_settings=dms_mixins.CfnEndpointPropsMixin.SybaseSettingsProperty(
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                username="username"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2684e4a60971e37b026b9a8ed0390af9df88907d73b8be26de417479dbcea603)
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument doc_db_settings", value=doc_db_settings, expected_type=type_hints["doc_db_settings"])
            check_type(argname="argument dynamo_db_settings", value=dynamo_db_settings, expected_type=type_hints["dynamo_db_settings"])
            check_type(argname="argument elasticsearch_settings", value=elasticsearch_settings, expected_type=type_hints["elasticsearch_settings"])
            check_type(argname="argument endpoint_identifier", value=endpoint_identifier, expected_type=type_hints["endpoint_identifier"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument engine_name", value=engine_name, expected_type=type_hints["engine_name"])
            check_type(argname="argument extra_connection_attributes", value=extra_connection_attributes, expected_type=type_hints["extra_connection_attributes"])
            check_type(argname="argument gcp_my_sql_settings", value=gcp_my_sql_settings, expected_type=type_hints["gcp_my_sql_settings"])
            check_type(argname="argument ibm_db2_settings", value=ibm_db2_settings, expected_type=type_hints["ibm_db2_settings"])
            check_type(argname="argument kafka_settings", value=kafka_settings, expected_type=type_hints["kafka_settings"])
            check_type(argname="argument kinesis_settings", value=kinesis_settings, expected_type=type_hints["kinesis_settings"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument microsoft_sql_server_settings", value=microsoft_sql_server_settings, expected_type=type_hints["microsoft_sql_server_settings"])
            check_type(argname="argument mongo_db_settings", value=mongo_db_settings, expected_type=type_hints["mongo_db_settings"])
            check_type(argname="argument my_sql_settings", value=my_sql_settings, expected_type=type_hints["my_sql_settings"])
            check_type(argname="argument neptune_settings", value=neptune_settings, expected_type=type_hints["neptune_settings"])
            check_type(argname="argument oracle_settings", value=oracle_settings, expected_type=type_hints["oracle_settings"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument postgre_sql_settings", value=postgre_sql_settings, expected_type=type_hints["postgre_sql_settings"])
            check_type(argname="argument redis_settings", value=redis_settings, expected_type=type_hints["redis_settings"])
            check_type(argname="argument redshift_settings", value=redshift_settings, expected_type=type_hints["redshift_settings"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            check_type(argname="argument s3_settings", value=s3_settings, expected_type=type_hints["s3_settings"])
            check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
            check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            check_type(argname="argument sybase_settings", value=sybase_settings, expected_type=type_hints["sybase_settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if database_name is not None:
            self._values["database_name"] = database_name
        if doc_db_settings is not None:
            self._values["doc_db_settings"] = doc_db_settings
        if dynamo_db_settings is not None:
            self._values["dynamo_db_settings"] = dynamo_db_settings
        if elasticsearch_settings is not None:
            self._values["elasticsearch_settings"] = elasticsearch_settings
        if endpoint_identifier is not None:
            self._values["endpoint_identifier"] = endpoint_identifier
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if engine_name is not None:
            self._values["engine_name"] = engine_name
        if extra_connection_attributes is not None:
            self._values["extra_connection_attributes"] = extra_connection_attributes
        if gcp_my_sql_settings is not None:
            self._values["gcp_my_sql_settings"] = gcp_my_sql_settings
        if ibm_db2_settings is not None:
            self._values["ibm_db2_settings"] = ibm_db2_settings
        if kafka_settings is not None:
            self._values["kafka_settings"] = kafka_settings
        if kinesis_settings is not None:
            self._values["kinesis_settings"] = kinesis_settings
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if microsoft_sql_server_settings is not None:
            self._values["microsoft_sql_server_settings"] = microsoft_sql_server_settings
        if mongo_db_settings is not None:
            self._values["mongo_db_settings"] = mongo_db_settings
        if my_sql_settings is not None:
            self._values["my_sql_settings"] = my_sql_settings
        if neptune_settings is not None:
            self._values["neptune_settings"] = neptune_settings
        if oracle_settings is not None:
            self._values["oracle_settings"] = oracle_settings
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if postgre_sql_settings is not None:
            self._values["postgre_sql_settings"] = postgre_sql_settings
        if redis_settings is not None:
            self._values["redis_settings"] = redis_settings
        if redshift_settings is not None:
            self._values["redshift_settings"] = redshift_settings
        if resource_identifier is not None:
            self._values["resource_identifier"] = resource_identifier
        if s3_settings is not None:
            self._values["s3_settings"] = s3_settings
        if server_name is not None:
            self._values["server_name"] = server_name
        if ssl_mode is not None:
            self._values["ssl_mode"] = ssl_mode
        if sybase_settings is not None:
            self._values["sybase_settings"] = sybase_settings
        if tags is not None:
            self._values["tags"] = tags
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-certificatearn
        '''
        result = self._values.get("certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the endpoint database.

        For a MySQL source or target endpoint, don't specify ``DatabaseName`` . To migrate to a specific database, use this setting and ``targetDbType`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def doc_db_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.DocDbSettingsProperty"]]:
        '''Settings in JSON format for the source and target DocumentDB endpoint.

        For more information about other available settings, see `Using extra connections attributes with Amazon DocumentDB as a source <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.DocumentDB.html#CHAP_Source.DocumentDB.ECAs>`_ and `Using Amazon DocumentDB as a target for AWS Database Migration Service <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.DocumentDB.html>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-docdbsettings
        '''
        result = self._values.get("doc_db_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.DocDbSettingsProperty"]], result)

    @builtins.property
    def dynamo_db_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.DynamoDbSettingsProperty"]]:
        '''Settings in JSON format for the target Amazon DynamoDB endpoint.

        For information about other available settings, see `Using object mapping to migrate data to DynamoDB <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.DynamoDB.html#CHAP_Target.DynamoDB.ObjectMapping>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-dynamodbsettings
        '''
        result = self._values.get("dynamo_db_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.DynamoDbSettingsProperty"]], result)

    @builtins.property
    def elasticsearch_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.ElasticsearchSettingsProperty"]]:
        '''Settings in JSON format for the target OpenSearch endpoint.

        For more information about the available settings, see `Extra connection attributes when using OpenSearch as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Elasticsearch.html#CHAP_Target.Elasticsearch.Configuration>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-elasticsearchsettings
        '''
        result = self._values.get("elasticsearch_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.ElasticsearchSettingsProperty"]], result)

    @builtins.property
    def endpoint_identifier(self) -> typing.Optional[builtins.str]:
        '''The database endpoint identifier.

        Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-endpointidentifier
        '''
        result = self._values.get("endpoint_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''The type of endpoint.

        Valid values are ``source`` and ``target`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-endpointtype
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_name(self) -> typing.Optional[builtins.str]:
        '''The type of engine for the endpoint, depending on the ``EndpointType`` value.

        *Valid values* : ``mysql`` | ``oracle`` | ``postgres`` | ``mariadb`` | ``aurora`` | ``aurora-postgresql`` | ``opensearch`` | ``redshift`` | ``redshift-serverless`` | ``s3`` | ``db2`` | ``azuredb`` | ``sybase`` | ``dynamodb`` | ``mongodb`` | ``kinesis`` | ``kafka`` | ``elasticsearch`` | ``docdb`` | ``sqlserver`` | ``neptune``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-enginename
        '''
        result = self._values.get("engine_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_connection_attributes(self) -> typing.Optional[builtins.str]:
        '''Additional attributes associated with the connection.

        Each attribute is specified as a name-value pair associated by an equal sign (=). Multiple attributes are separated by a semicolon (;) with no additional white space. For information on the attributes available for connecting your source or target endpoint, see `Working with AWS DMS Endpoints <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Endpoints.html>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-extraconnectionattributes
        '''
        result = self._values.get("extra_connection_attributes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcp_my_sql_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.GcpMySQLSettingsProperty"]]:
        '''Settings in JSON format for the source GCP MySQL endpoint.

        These settings are much the same as the settings for any MySQL-compatible endpoint. For more information, see `Extra connection attributes when using MySQL as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html#CHAP_Source.MySQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-gcpmysqlsettings
        '''
        result = self._values.get("gcp_my_sql_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.GcpMySQLSettingsProperty"]], result)

    @builtins.property
    def ibm_db2_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.IbmDb2SettingsProperty"]]:
        '''Settings in JSON format for the source IBM Db2 LUW endpoint.

        For information about other available settings, see `Extra connection attributes when using Db2 LUW as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.DB2.html#CHAP_Source.DB2.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-ibmdb2settings
        '''
        result = self._values.get("ibm_db2_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.IbmDb2SettingsProperty"]], result)

    @builtins.property
    def kafka_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.KafkaSettingsProperty"]]:
        '''Settings in JSON format for the target Apache Kafka endpoint.

        For more information about other available settings, see `Using object mapping to migrate data to a Kafka topic <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Kafka.html#CHAP_Target.Kafka.ObjectMapping>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-kafkasettings
        '''
        result = self._values.get("kafka_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.KafkaSettingsProperty"]], result)

    @builtins.property
    def kinesis_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.KinesisSettingsProperty"]]:
        '''Settings in JSON format for the target endpoint for Amazon Kinesis Data Streams.

        For more information about other available settings, see `Using object mapping to migrate data to a Kinesis data stream <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Kinesis.html#CHAP_Target.Kinesis.ObjectMapping>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-kinesissettings
        '''
        result = self._values.get("kinesis_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.KinesisSettingsProperty"]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''An AWS  key identifier that is used to encrypt the connection parameters for the endpoint.

        If you don't specify a value for the ``KmsKeyId`` parameter, AWS DMS uses your default encryption key.

        AWS  creates the default encryption key for your AWS account . Your AWS account has a different default encryption key for each AWS Region .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microsoft_sql_server_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.MicrosoftSqlServerSettingsProperty"]]:
        '''Settings in JSON format for the source and target Microsoft SQL Server endpoint.

        For information about other available settings, see `Extra connection attributes when using SQL Server as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.SQLServer.html#CHAP_Source.SQLServer.ConnectionAttrib>`_ and `Extra connection attributes when using SQL Server as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.SQLServer.html#CHAP_Target.SQLServer.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-microsoftsqlserversettings
        '''
        result = self._values.get("microsoft_sql_server_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.MicrosoftSqlServerSettingsProperty"]], result)

    @builtins.property
    def mongo_db_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.MongoDbSettingsProperty"]]:
        '''Settings in JSON format for the source MongoDB endpoint.

        For more information about the available settings, see `Using MongoDB as a target for AWS Database Migration Service <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MongoDB.html#CHAP_Source.MongoDB.Configuration>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-mongodbsettings
        '''
        result = self._values.get("mongo_db_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.MongoDbSettingsProperty"]], result)

    @builtins.property
    def my_sql_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.MySqlSettingsProperty"]]:
        '''Settings in JSON format for the source and target MySQL endpoint.

        For information about other available settings, see `Extra connection attributes when using MySQL as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html#CHAP_Source.MySQL.ConnectionAttrib>`_ and `Extra connection attributes when using a MySQL-compatible database as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.MySQL.html#CHAP_Target.MySQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-mysqlsettings
        '''
        result = self._values.get("my_sql_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.MySqlSettingsProperty"]], result)

    @builtins.property
    def neptune_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.NeptuneSettingsProperty"]]:
        '''Settings in JSON format for the target Amazon Neptune endpoint.

        For more information about the available settings, see `Specifying endpoint settings for Amazon Neptune as a target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Neptune.html#CHAP_Target.Neptune.EndpointSettings>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-neptunesettings
        '''
        result = self._values.get("neptune_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.NeptuneSettingsProperty"]], result)

    @builtins.property
    def oracle_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.OracleSettingsProperty"]]:
        '''Settings in JSON format for the source and target Oracle endpoint.

        For information about other available settings, see `Extra connection attributes when using Oracle as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.ConnectionAttrib>`_ and `Extra connection attributes when using Oracle as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Oracle.html#CHAP_Target.Oracle.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-oraclesettings
        '''
        result = self._values.get("oracle_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.OracleSettingsProperty"]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password to be used to log in to the endpoint database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port used by the endpoint database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def postgre_sql_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.PostgreSqlSettingsProperty"]]:
        '''Settings in JSON format for the source and target PostgreSQL endpoint.

        For information about other available settings, see `Extra connection attributes when using PostgreSQL as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.PostgreSQL.html#CHAP_Source.PostgreSQL.ConnectionAttrib>`_ and `Extra connection attributes when using PostgreSQL as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.PostgreSQL.html#CHAP_Target.PostgreSQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-postgresqlsettings
        '''
        result = self._values.get("postgre_sql_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.PostgreSqlSettingsProperty"]], result)

    @builtins.property
    def redis_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.RedisSettingsProperty"]]:
        '''Settings in JSON format for the target Redis endpoint.

        For information about other available settings, see `Specifying endpoint settings for Redis as a target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Redis.html#CHAP_Target.Redis.EndpointSettings>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-redissettings
        '''
        result = self._values.get("redis_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.RedisSettingsProperty"]], result)

    @builtins.property
    def redshift_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.RedshiftSettingsProperty"]]:
        '''Settings in JSON format for the Amazon Redshift endpoint.

        For more information about other available settings, see `Extra connection attributes when using Amazon Redshift as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Redshift.html#CHAP_Target.Redshift.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-redshiftsettings
        '''
        result = self._values.get("redshift_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.RedshiftSettingsProperty"]], result)

    @builtins.property
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''A display name for the resource identifier at the end of the ``EndpointArn`` response parameter that is returned in the created ``Endpoint`` object.

        The value for this parameter can have up to 31 characters. It can contain only ASCII letters, digits, and hyphen ('-'). Also, it can't end with a hyphen or contain two consecutive hyphens, and can only begin with a letter, such as ``Example-App-ARN1`` .

        For example, this value might result in the ``EndpointArn`` value ``arn:aws:dms:eu-west-1:012345678901:rep:Example-App-ARN1`` . If you don't specify a ``ResourceIdentifier`` value, AWS DMS generates a default identifier value for the end of ``EndpointArn`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.S3SettingsProperty"]]:
        '''Settings in JSON format for the source and target Amazon S3 endpoint.

        For more information about other available settings, see `Extra connection attributes when using Amazon S3 as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.S3.html#CHAP_Source.S3.Configuring>`_ and `Extra connection attributes when using Amazon S3 as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-s3settings
        '''
        result = self._values.get("s3_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.S3SettingsProperty"]], result)

    @builtins.property
    def server_name(self) -> typing.Optional[builtins.str]:
        '''The name of the server where the endpoint database resides.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-servername
        '''
        result = self._values.get("server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        '''The Secure Sockets Layer (SSL) mode to use for the SSL connection. The default is ``none`` .

        .. epigraph::

           When ``engine_name`` is set to S3, the only allowed value is ``none`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-sslmode
        '''
        result = self._values.get("ssl_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sybase_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.SybaseSettingsProperty"]]:
        '''Settings in JSON format for the source and target SAP ASE endpoint.

        For information about other available settings, see `Extra connection attributes when using SAP ASE as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.SAP.html#CHAP_Source.SAP.ConnectionAttrib>`_ and `Extra connection attributes when using SAP ASE as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.SAP.html#CHAP_Target.SAP.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-sybasesettings
        '''
        result = self._values.get("sybase_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointPropsMixin.SybaseSettingsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more tags to be assigned to the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The user name to be used to log in to the endpoint database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin",
):
    '''The ``AWS::DMS::Endpoint`` resource specifies an AWS DMS endpoint.

    Currently, AWS CloudFormation supports all AWS DMS endpoint types.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html
    :cloudformationResource: AWS::DMS::Endpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        cfn_endpoint_props_mixin = dms_mixins.CfnEndpointPropsMixin(dms_mixins.CfnEndpointMixinProps(
            certificate_arn="certificateArn",
            database_name="databaseName",
            doc_db_settings=dms_mixins.CfnEndpointPropsMixin.DocDbSettingsProperty(
                docs_to_investigate=123,
                extract_doc_id=False,
                nesting_level="nestingLevel",
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId"
            ),
            dynamo_db_settings=dms_mixins.CfnEndpointPropsMixin.DynamoDbSettingsProperty(
                service_access_role_arn="serviceAccessRoleArn"
            ),
            elasticsearch_settings=dms_mixins.CfnEndpointPropsMixin.ElasticsearchSettingsProperty(
                endpoint_uri="endpointUri",
                error_retry_duration=123,
                full_load_error_percentage=123,
                service_access_role_arn="serviceAccessRoleArn"
            ),
            endpoint_identifier="endpointIdentifier",
            endpoint_type="endpointType",
            engine_name="engineName",
            extra_connection_attributes="extraConnectionAttributes",
            gcp_my_sql_settings=dms_mixins.CfnEndpointPropsMixin.GcpMySQLSettingsProperty(
                after_connect_script="afterConnectScript",
                clean_source_metadata_on_mismatch=False,
                database_name="databaseName",
                events_poll_interval=123,
                max_file_size=123,
                parallel_load_threads=123,
                password="password",
                port=123,
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId",
                server_name="serverName",
                server_timezone="serverTimezone",
                username="username"
            ),
            ibm_db2_settings=dms_mixins.CfnEndpointPropsMixin.IbmDb2SettingsProperty(
                current_lsn="currentLsn",
                keep_csv_files=False,
                load_timeout=123,
                max_file_size=123,
                max_kBytes_per_read=123,
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId",
                set_data_capture_changes=False,
                write_buffer_size=123
            ),
            kafka_settings=dms_mixins.CfnEndpointPropsMixin.KafkaSettingsProperty(
                broker="broker",
                include_control_details=False,
                include_null_and_empty=False,
                include_partition_value=False,
                include_table_alter_operations=False,
                include_transaction_details=False,
                message_format="messageFormat",
                message_max_bytes=123,
                no_hex_prefix=False,
                partition_include_schema_table=False,
                sasl_password="saslPassword",
                sasl_user_name="saslUserName",
                security_protocol="securityProtocol",
                ssl_ca_certificate_arn="sslCaCertificateArn",
                ssl_client_certificate_arn="sslClientCertificateArn",
                ssl_client_key_arn="sslClientKeyArn",
                ssl_client_key_password="sslClientKeyPassword",
                topic="topic"
            ),
            kinesis_settings=dms_mixins.CfnEndpointPropsMixin.KinesisSettingsProperty(
                include_control_details=False,
                include_null_and_empty=False,
                include_partition_value=False,
                include_table_alter_operations=False,
                include_transaction_details=False,
                message_format="messageFormat",
                no_hex_prefix=False,
                partition_include_schema_table=False,
                service_access_role_arn="serviceAccessRoleArn",
                stream_arn="streamArn"
            ),
            kms_key_id="kmsKeyId",
            microsoft_sql_server_settings=dms_mixins.CfnEndpointPropsMixin.MicrosoftSqlServerSettingsProperty(
                bcp_packet_size=123,
                control_tables_file_group="controlTablesFileGroup",
                database_name="databaseName",
                force_lob_lookup=False,
                password="password",
                port=123,
                query_single_always_on_node=False,
                read_backup_only=False,
                safeguard_policy="safeguardPolicy",
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId",
                server_name="serverName",
                tlog_access_mode="tlogAccessMode",
                trim_space_in_char=False,
                use_bcp_full_load=False,
                username="username",
                use_third_party_backup_device=False
            ),
            mongo_db_settings=dms_mixins.CfnEndpointPropsMixin.MongoDbSettingsProperty(
                auth_mechanism="authMechanism",
                auth_source="authSource",
                auth_type="authType",
                database_name="databaseName",
                docs_to_investigate="docsToInvestigate",
                extract_doc_id="extractDocId",
                nesting_level="nestingLevel",
                password="password",
                port=123,
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId",
                server_name="serverName",
                username="username"
            ),
            my_sql_settings=dms_mixins.CfnEndpointPropsMixin.MySqlSettingsProperty(
                after_connect_script="afterConnectScript",
                clean_source_metadata_on_mismatch=False,
                events_poll_interval=123,
                max_file_size=123,
                parallel_load_threads=123,
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId",
                server_timezone="serverTimezone",
                target_db_type="targetDbType"
            ),
            neptune_settings=dms_mixins.CfnEndpointPropsMixin.NeptuneSettingsProperty(
                error_retry_duration=123,
                iam_auth_enabled=False,
                max_file_size=123,
                max_retry_count=123,
                s3_bucket_folder="s3BucketFolder",
                s3_bucket_name="s3BucketName",
                service_access_role_arn="serviceAccessRoleArn"
            ),
            oracle_settings=dms_mixins.CfnEndpointPropsMixin.OracleSettingsProperty(
                access_alternate_directly=False,
                additional_archived_log_dest_id=123,
                add_supplemental_logging=False,
                allow_select_nested_tables=False,
                archived_log_dest_id=123,
                archived_logs_only=False,
                asm_password="asmPassword",
                asm_server="asmServer",
                asm_user="asmUser",
                char_length_semantics="charLengthSemantics",
                direct_path_no_log=False,
                direct_path_parallel_load=False,
                enable_homogenous_tablespace=False,
                extra_archived_log_dest_ids=[123],
                fail_tasks_on_lob_truncation=False,
                number_datatype_scale=123,
                oracle_path_prefix="oraclePathPrefix",
                parallel_asm_read_threads=123,
                read_ahead_blocks=123,
                read_table_space_name=False,
                replace_path_prefix=False,
                retry_interval=123,
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_oracle_asm_access_role_arn="secretsManagerOracleAsmAccessRoleArn",
                secrets_manager_oracle_asm_secret_id="secretsManagerOracleAsmSecretId",
                secrets_manager_secret_id="secretsManagerSecretId",
                security_db_encryption="securityDbEncryption",
                security_db_encryption_name="securityDbEncryptionName",
                spatial_data_option_to_geo_json_function_name="spatialDataOptionToGeoJsonFunctionName",
                standby_delay_time=123,
                use_alternate_folder_for_online=False,
                use_bFile=False,
                use_direct_path_full_load=False,
                use_logminer_reader=False,
                use_path_prefix="usePathPrefix"
            ),
            password="password",
            port=123,
            postgre_sql_settings=dms_mixins.CfnEndpointPropsMixin.PostgreSqlSettingsProperty(
                after_connect_script="afterConnectScript",
                babelfish_database_name="babelfishDatabaseName",
                capture_ddls=False,
                database_mode="databaseMode",
                ddl_artifacts_schema="ddlArtifactsSchema",
                execute_timeout=123,
                fail_tasks_on_lob_truncation=False,
                heartbeat_enable=False,
                heartbeat_frequency=123,
                heartbeat_schema="heartbeatSchema",
                map_boolean_as_boolean=False,
                max_file_size=123,
                plugin_name="pluginName",
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId",
                slot_name="slotName"
            ),
            redis_settings=dms_mixins.CfnEndpointPropsMixin.RedisSettingsProperty(
                auth_password="authPassword",
                auth_type="authType",
                auth_user_name="authUserName",
                port=123,
                server_name="serverName",
                ssl_ca_certificate_arn="sslCaCertificateArn",
                ssl_security_protocol="sslSecurityProtocol"
            ),
            redshift_settings=dms_mixins.CfnEndpointPropsMixin.RedshiftSettingsProperty(
                accept_any_date=False,
                after_connect_script="afterConnectScript",
                bucket_folder="bucketFolder",
                bucket_name="bucketName",
                case_sensitive_names=False,
                comp_update=False,
                connection_timeout=123,
                date_format="dateFormat",
                empty_as_null=False,
                encryption_mode="encryptionMode",
                explicit_ids=False,
                file_transfer_upload_streams=123,
                load_timeout=123,
                map_boolean_as_boolean=False,
                max_file_size=123,
                remove_quotes=False,
                replace_chars="replaceChars",
                replace_invalid_chars="replaceInvalidChars",
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId",
                server_side_encryption_kms_key_id="serverSideEncryptionKmsKeyId",
                service_access_role_arn="serviceAccessRoleArn",
                time_format="timeFormat",
                trim_blanks=False,
                truncate_columns=False,
                write_buffer_size=123
            ),
            resource_identifier="resourceIdentifier",
            s3_settings=dms_mixins.CfnEndpointPropsMixin.S3SettingsProperty(
                add_column_name=False,
                add_trailing_padding_character=False,
                bucket_folder="bucketFolder",
                bucket_name="bucketName",
                canned_acl_for_objects="cannedAclForObjects",
                cdc_inserts_and_updates=False,
                cdc_inserts_only=False,
                cdc_max_batch_interval=123,
                cdc_min_file_size=123,
                cdc_path="cdcPath",
                compression_type="compressionType",
                csv_delimiter="csvDelimiter",
                csv_no_sup_value="csvNoSupValue",
                csv_null_value="csvNullValue",
                csv_row_delimiter="csvRowDelimiter",
                data_format="dataFormat",
                data_page_size=123,
                date_partition_delimiter="datePartitionDelimiter",
                date_partition_enabled=False,
                date_partition_sequence="datePartitionSequence",
                date_partition_timezone="datePartitionTimezone",
                dict_page_size_limit=123,
                enable_statistics=False,
                encoding_type="encodingType",
                encryption_mode="encryptionMode",
                expected_bucket_owner="expectedBucketOwner",
                external_table_definition="externalTableDefinition",
                glue_catalog_generation=False,
                ignore_header_rows=123,
                include_op_for_full_load=False,
                max_file_size=123,
                parquet_timestamp_in_millisecond=False,
                parquet_version="parquetVersion",
                preserve_transactions=False,
                rfc4180=False,
                row_group_length=123,
                server_side_encryption_kms_key_id="serverSideEncryptionKmsKeyId",
                service_access_role_arn="serviceAccessRoleArn",
                timestamp_column_name="timestampColumnName",
                use_csv_no_sup_value=False,
                use_task_start_time_for_full_load_timestamp=False
            ),
            server_name="serverName",
            ssl_mode="sslMode",
            sybase_settings=dms_mixins.CfnEndpointPropsMixin.SybaseSettingsProperty(
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            username="username"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DMS::Endpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1455e7231f232d36be063d1bf3d562140a77f7291aa34b4a7763c7bbab0c9de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c50dd22fc91a7546d628d3b5fdef50a18ed4396fa38cabf613f101bdd7d139d4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f14cdb3afc1bb521ca37a1d2fdd76cf4d8c78c17d453421cd07c6cbee4e3e6ed)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEndpointMixinProps:
        return typing.cast(CfnEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.DocDbSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "docs_to_investigate": "docsToInvestigate",
            "extract_doc_id": "extractDocId",
            "nesting_level": "nestingLevel",
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_secret_id": "secretsManagerSecretId",
        },
    )
    class DocDbSettingsProperty:
        def __init__(
            self,
            *,
            docs_to_investigate: typing.Optional[jsii.Number] = None,
            extract_doc_id: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            nesting_level: typing.Optional[builtins.str] = None,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a DocumentDB endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For more information about other available settings, see `Using extra connections attributes with Amazon DocumentDB as a source <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.DocumentDB.html#CHAP_Source.DocumentDB.ECAs>`_ and `Using Amazon DocumentDB as a target for AWS Database Migration Service <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.DocumentDB.html>`_ in the *AWS Database Migration Service User Guide* .

            :param docs_to_investigate: Indicates the number of documents to preview to determine the document organization. Use this setting when ``NestingLevel`` is set to ``"one"`` . Must be a positive value greater than ``0`` . Default value is ``1000`` .
            :param extract_doc_id: Specifies the document ID. Use this setting when ``NestingLevel`` is set to ``"none"`` . Default value is ``"false"`` .
            :param nesting_level: Specifies either document or table mode. Default value is ``"none"`` . Specify ``"none"`` to use document mode. Specify ``"one"`` to use table mode.
            :param secrets_manager_access_role_arn: The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` . The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the DocumentDB endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both. For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the DocumentDB endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-docdbsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                doc_db_settings_property = dms_mixins.CfnEndpointPropsMixin.DocDbSettingsProperty(
                    docs_to_investigate=123,
                    extract_doc_id=False,
                    nesting_level="nestingLevel",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cef9213ce344055e1ac9a7c373ce9013bc07647250bfbdc93eec4382d646da33)
                check_type(argname="argument docs_to_investigate", value=docs_to_investigate, expected_type=type_hints["docs_to_investigate"])
                check_type(argname="argument extract_doc_id", value=extract_doc_id, expected_type=type_hints["extract_doc_id"])
                check_type(argname="argument nesting_level", value=nesting_level, expected_type=type_hints["nesting_level"])
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if docs_to_investigate is not None:
                self._values["docs_to_investigate"] = docs_to_investigate
            if extract_doc_id is not None:
                self._values["extract_doc_id"] = extract_doc_id
            if nesting_level is not None:
                self._values["nesting_level"] = nesting_level
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id

        @builtins.property
        def docs_to_investigate(self) -> typing.Optional[jsii.Number]:
            '''Indicates the number of documents to preview to determine the document organization.

            Use this setting when ``NestingLevel`` is set to ``"one"`` .

            Must be a positive value greater than ``0`` . Default value is ``1000`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-docdbsettings.html#cfn-dms-endpoint-docdbsettings-docstoinvestigate
            '''
            result = self._values.get("docs_to_investigate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def extract_doc_id(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies the document ID. Use this setting when ``NestingLevel`` is set to ``"none"`` .

            Default value is ``"false"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-docdbsettings.html#cfn-dms-endpoint-docdbsettings-extractdocid
            '''
            result = self._values.get("extract_doc_id")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def nesting_level(self) -> typing.Optional[builtins.str]:
            '''Specifies either document or table mode.

            Default value is ``"none"`` . Specify ``"none"`` to use document mode. Specify ``"one"`` to use table mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-docdbsettings.html#cfn-dms-endpoint-docdbsettings-nestinglevel
            '''
            result = self._values.get("nesting_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` .

            The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the DocumentDB endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both.

               For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-docdbsettings.html#cfn-dms-endpoint-docdbsettings-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the DocumentDB endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-docdbsettings.html#cfn-dms-endpoint-docdbsettings-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocDbSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.DynamoDbSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"service_access_role_arn": "serviceAccessRoleArn"},
    )
    class DynamoDbSettingsProperty:
        def __init__(
            self,
            *,
            service_access_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information, including the Amazon Resource Name (ARN) of the IAM role used to define an Amazon DynamoDB target endpoint.

            This information also includes the output format of records applied to the endpoint and details of transaction and control table data information. For information about other available settings, see `Using object mapping to migrate data to DynamoDB <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.DynamoDB.html#CHAP_Target.DynamoDB.ObjectMapping>`_ in the *AWS Database Migration Service User Guide* .

            :param service_access_role_arn: The Amazon Resource Name (ARN) used by the service to access the IAM role. The role must allow the ``iam:PassRole`` action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-dynamodbsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                dynamo_db_settings_property = dms_mixins.CfnEndpointPropsMixin.DynamoDbSettingsProperty(
                    service_access_role_arn="serviceAccessRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9578a84443d8d08353ae2a5c12fe559666b72cfb92d8b91595bf9d2913af50c)
                check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) used by the service to access the IAM role.

            The role must allow the ``iam:PassRole`` action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-dynamodbsettings.html#cfn-dms-endpoint-dynamodbsettings-serviceaccessrolearn
            '''
            result = self._values.get("service_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDbSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.ElasticsearchSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint_uri": "endpointUri",
            "error_retry_duration": "errorRetryDuration",
            "full_load_error_percentage": "fullLoadErrorPercentage",
            "service_access_role_arn": "serviceAccessRoleArn",
        },
    )
    class ElasticsearchSettingsProperty:
        def __init__(
            self,
            *,
            endpoint_uri: typing.Optional[builtins.str] = None,
            error_retry_duration: typing.Optional[jsii.Number] = None,
            full_load_error_percentage: typing.Optional[jsii.Number] = None,
            service_access_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines an OpenSearch endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For more information about the available settings, see `Extra connection attributes when using OpenSearch as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Elasticsearch.html#CHAP_Target.Elasticsearch.Configuration>`_ in the *AWS Database Migration Service User Guide* .

            :param endpoint_uri: The endpoint for the OpenSearch cluster. AWS DMS uses HTTPS if a transport protocol (either HTTP or HTTPS) isn't specified.
            :param error_retry_duration: The maximum number of seconds for which DMS retries failed API requests to the OpenSearch cluster.
            :param full_load_error_percentage: The maximum percentage of records that can fail to be written before a full load operation stops. To avoid early failure, this counter is only effective after 1,000 records are transferred. OpenSearch also has the concept of error monitoring during the last 10 minutes of an Observation Window. If transfer of all records fail in the last 10 minutes, the full load operation stops.
            :param service_access_role_arn: The Amazon Resource Name (ARN) used by the service to access the IAM role. The role must allow the ``iam:PassRole`` action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-elasticsearchsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                elasticsearch_settings_property = dms_mixins.CfnEndpointPropsMixin.ElasticsearchSettingsProperty(
                    endpoint_uri="endpointUri",
                    error_retry_duration=123,
                    full_load_error_percentage=123,
                    service_access_role_arn="serviceAccessRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4fc14f1ae62f889f201dee6d174bf78afc5acce1e8454670ded2598abd736361)
                check_type(argname="argument endpoint_uri", value=endpoint_uri, expected_type=type_hints["endpoint_uri"])
                check_type(argname="argument error_retry_duration", value=error_retry_duration, expected_type=type_hints["error_retry_duration"])
                check_type(argname="argument full_load_error_percentage", value=full_load_error_percentage, expected_type=type_hints["full_load_error_percentage"])
                check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint_uri is not None:
                self._values["endpoint_uri"] = endpoint_uri
            if error_retry_duration is not None:
                self._values["error_retry_duration"] = error_retry_duration
            if full_load_error_percentage is not None:
                self._values["full_load_error_percentage"] = full_load_error_percentage
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn

        @builtins.property
        def endpoint_uri(self) -> typing.Optional[builtins.str]:
            '''The endpoint for the OpenSearch cluster.

            AWS DMS uses HTTPS if a transport protocol (either HTTP or HTTPS) isn't specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-elasticsearchsettings.html#cfn-dms-endpoint-elasticsearchsettings-endpointuri
            '''
            result = self._values.get("endpoint_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def error_retry_duration(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of seconds for which DMS retries failed API requests to the OpenSearch cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-elasticsearchsettings.html#cfn-dms-endpoint-elasticsearchsettings-errorretryduration
            '''
            result = self._values.get("error_retry_duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def full_load_error_percentage(self) -> typing.Optional[jsii.Number]:
            '''The maximum percentage of records that can fail to be written before a full load operation stops.

            To avoid early failure, this counter is only effective after 1,000 records are transferred. OpenSearch also has the concept of error monitoring during the last 10 minutes of an Observation Window. If transfer of all records fail in the last 10 minutes, the full load operation stops.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-elasticsearchsettings.html#cfn-dms-endpoint-elasticsearchsettings-fullloaderrorpercentage
            '''
            result = self._values.get("full_load_error_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) used by the service to access the IAM role.

            The role must allow the ``iam:PassRole`` action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-elasticsearchsettings.html#cfn-dms-endpoint-elasticsearchsettings-serviceaccessrolearn
            '''
            result = self._values.get("service_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.GcpMySQLSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "after_connect_script": "afterConnectScript",
            "clean_source_metadata_on_mismatch": "cleanSourceMetadataOnMismatch",
            "database_name": "databaseName",
            "events_poll_interval": "eventsPollInterval",
            "max_file_size": "maxFileSize",
            "parallel_load_threads": "parallelLoadThreads",
            "password": "password",
            "port": "port",
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_secret_id": "secretsManagerSecretId",
            "server_name": "serverName",
            "server_timezone": "serverTimezone",
            "username": "username",
        },
    )
    class GcpMySQLSettingsProperty:
        def __init__(
            self,
            *,
            after_connect_script: typing.Optional[builtins.str] = None,
            clean_source_metadata_on_mismatch: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            database_name: typing.Optional[builtins.str] = None,
            events_poll_interval: typing.Optional[jsii.Number] = None,
            max_file_size: typing.Optional[jsii.Number] = None,
            parallel_load_threads: typing.Optional[jsii.Number] = None,
            password: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
            server_name: typing.Optional[builtins.str] = None,
            server_timezone: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a GCP MySQL endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. These settings are much the same as the settings for any MySQL-compatible endpoint. For more information, see `Extra connection attributes when using MySQL as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html#CHAP_Source.MySQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

            :param after_connect_script: Specifies a script to run immediately after AWS DMS connects to the endpoint. The migration task continues running regardless if the SQL statement succeeds or fails. For this parameter, provide the code of the script itself, not the name of a file containing the script.
            :param clean_source_metadata_on_mismatch: Adjusts the behavior of AWS DMS when migrating from an SQL Server source database that is hosted as part of an Always On availability group cluster. If you need AWS DMS to poll all the nodes in the Always On cluster for transaction backups, set this attribute to ``false`` .
            :param database_name: Database name for the endpoint. For a MySQL source or target endpoint, don't explicitly specify the database using the ``DatabaseName`` request parameter on either the ``CreateEndpoint`` or ``ModifyEndpoint`` API call. Specifying ``DatabaseName`` when you create or modify a MySQL endpoint replicates all the task tables to this single database. For MySQL endpoints, you specify the database only when you specify the schema in the table-mapping rules of the AWS DMS task.
            :param events_poll_interval: Specifies how often to check the binary log for new changes/events when the database is idle. The default is five seconds. Example: ``eventsPollInterval=5;`` In the example, AWS DMS checks for changes in the binary logs every five seconds.
            :param max_file_size: Specifies the maximum size (in KB) of any .csv file used to transfer data to a MySQL-compatible database. Example: ``maxFileSize=512``
            :param parallel_load_threads: Improves performance when loading data into the MySQL-compatible target database. Specifies how many threads to use to load the data into the MySQL-compatible target database. Setting a large number of threads can have an adverse effect on database performance, because a separate connection is required for each thread. The default is one. Example: ``parallelLoadThreads=1``
            :param password: Endpoint connection password.
            :param port: The port used by the endpoint database.
            :param secrets_manager_access_role_arn: The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret.`` The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the MySQL endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both. For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the MySQL endpoint connection details.
            :param server_name: The MySQL host name.
            :param server_timezone: Specifies the time zone for the source MySQL database. Don't enclose time zones in single quotation marks. Example: ``serverTimezone=US/Pacific;``
            :param username: Endpoint connection user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                gcp_my_sQLSettings_property = dms_mixins.CfnEndpointPropsMixin.GcpMySQLSettingsProperty(
                    after_connect_script="afterConnectScript",
                    clean_source_metadata_on_mismatch=False,
                    database_name="databaseName",
                    events_poll_interval=123,
                    max_file_size=123,
                    parallel_load_threads=123,
                    password="password",
                    port=123,
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    server_name="serverName",
                    server_timezone="serverTimezone",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4aee00af5d13ce1e056e7fd111978f44e543ce60de717f370b7ac376dad83a1d)
                check_type(argname="argument after_connect_script", value=after_connect_script, expected_type=type_hints["after_connect_script"])
                check_type(argname="argument clean_source_metadata_on_mismatch", value=clean_source_metadata_on_mismatch, expected_type=type_hints["clean_source_metadata_on_mismatch"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument events_poll_interval", value=events_poll_interval, expected_type=type_hints["events_poll_interval"])
                check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
                check_type(argname="argument parallel_load_threads", value=parallel_load_threads, expected_type=type_hints["parallel_load_threads"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument server_timezone", value=server_timezone, expected_type=type_hints["server_timezone"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if after_connect_script is not None:
                self._values["after_connect_script"] = after_connect_script
            if clean_source_metadata_on_mismatch is not None:
                self._values["clean_source_metadata_on_mismatch"] = clean_source_metadata_on_mismatch
            if database_name is not None:
                self._values["database_name"] = database_name
            if events_poll_interval is not None:
                self._values["events_poll_interval"] = events_poll_interval
            if max_file_size is not None:
                self._values["max_file_size"] = max_file_size
            if parallel_load_threads is not None:
                self._values["parallel_load_threads"] = parallel_load_threads
            if password is not None:
                self._values["password"] = password
            if port is not None:
                self._values["port"] = port
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id
            if server_name is not None:
                self._values["server_name"] = server_name
            if server_timezone is not None:
                self._values["server_timezone"] = server_timezone
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def after_connect_script(self) -> typing.Optional[builtins.str]:
            '''Specifies a script to run immediately after AWS DMS connects to the endpoint.

            The migration task continues running regardless if the SQL statement succeeds or fails.

            For this parameter, provide the code of the script itself, not the name of a file containing the script.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-afterconnectscript
            '''
            result = self._values.get("after_connect_script")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def clean_source_metadata_on_mismatch(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Adjusts the behavior of AWS DMS when migrating from an SQL Server source database that is hosted as part of an Always On availability group cluster.

            If you need AWS DMS to poll all the nodes in the Always On cluster for transaction backups, set this attribute to ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-cleansourcemetadataonmismatch
            '''
            result = self._values.get("clean_source_metadata_on_mismatch")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''Database name for the endpoint.

            For a MySQL source or target endpoint, don't explicitly specify the database using the ``DatabaseName`` request parameter on either the ``CreateEndpoint`` or ``ModifyEndpoint`` API call. Specifying ``DatabaseName`` when you create or modify a MySQL endpoint replicates all the task tables to this single database. For MySQL endpoints, you specify the database only when you specify the schema in the table-mapping rules of the AWS DMS task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def events_poll_interval(self) -> typing.Optional[jsii.Number]:
            '''Specifies how often to check the binary log for new changes/events when the database is idle.

            The default is five seconds.

            Example: ``eventsPollInterval=5;``

            In the example, AWS DMS checks for changes in the binary logs every five seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-eventspollinterval
            '''
            result = self._values.get("events_poll_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_file_size(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum size (in KB) of any .csv file used to transfer data to a MySQL-compatible database.

            Example: ``maxFileSize=512``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-maxfilesize
            '''
            result = self._values.get("max_file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def parallel_load_threads(self) -> typing.Optional[jsii.Number]:
            '''Improves performance when loading data into the MySQL-compatible target database.

            Specifies how many threads to use to load the data into the MySQL-compatible target database. Setting a large number of threads can have an adverse effect on database performance, because a separate connection is required for each thread. The default is one.

            Example: ``parallelLoadThreads=1``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-parallelloadthreads
            '''
            result = self._values.get("parallel_load_threads")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''Endpoint connection password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port used by the endpoint database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret.`` The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the MySQL endpoint.

            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both.

               For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the MySQL endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''The MySQL host name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_timezone(self) -> typing.Optional[builtins.str]:
            '''Specifies the time zone for the source MySQL database. Don't enclose time zones in single quotation marks.

            Example: ``serverTimezone=US/Pacific;``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-servertimezone
            '''
            result = self._values.get("server_timezone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''Endpoint connection user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GcpMySQLSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.IbmDb2SettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "current_lsn": "currentLsn",
            "keep_csv_files": "keepCsvFiles",
            "load_timeout": "loadTimeout",
            "max_file_size": "maxFileSize",
            "max_k_bytes_per_read": "maxKBytesPerRead",
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_secret_id": "secretsManagerSecretId",
            "set_data_capture_changes": "setDataCaptureChanges",
            "write_buffer_size": "writeBufferSize",
        },
    )
    class IbmDb2SettingsProperty:
        def __init__(
            self,
            *,
            current_lsn: typing.Optional[builtins.str] = None,
            keep_csv_files: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            load_timeout: typing.Optional[jsii.Number] = None,
            max_file_size: typing.Optional[jsii.Number] = None,
            max_k_bytes_per_read: typing.Optional[jsii.Number] = None,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
            set_data_capture_changes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            write_buffer_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Provides information that defines an IBMDB2 endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For more information about other available settings, see `Extra connection attributes when using Db2 LUW as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.DB2.html#CHAP_Source.DB2.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

            :param current_lsn: For ongoing replication (CDC), use CurrentLSN to specify a log sequence number (LSN) where you want the replication to start.
            :param keep_csv_files: If true, AWS DMS saves any .csv files to the Db2 LUW target that were used to replicate data. DMS uses these files for analysis and troubleshooting. The default value is false.
            :param load_timeout: The amount of time (in milliseconds) before AWS DMS times out operations performed by DMS on the Db2 target. The default value is 1200 (20 minutes).
            :param max_file_size: Specifies the maximum size (in KB) of .csv files used to transfer data to Db2 LUW.
            :param max_k_bytes_per_read: Maximum number of bytes per read, as a NUMBER value. The default is 64 KB.
            :param secrets_manager_access_role_arn: The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` . The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value ofthe AWS Secrets Manager secret that allows access to the Db2 LUW endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both. For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the IBMDB2 endpoint connection details.
            :param set_data_capture_changes: Enables ongoing replication (CDC) as a BOOLEAN value. The default is true.
            :param write_buffer_size: The size (in KB) of the in-memory file write buffer used when generating .csv files on the local disk on the DMS replication instance. The default value is 1024 (1 MB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-ibmdb2settings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                ibm_db2_settings_property = dms_mixins.CfnEndpointPropsMixin.IbmDb2SettingsProperty(
                    current_lsn="currentLsn",
                    keep_csv_files=False,
                    load_timeout=123,
                    max_file_size=123,
                    max_kBytes_per_read=123,
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    set_data_capture_changes=False,
                    write_buffer_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fe3d1b2d109630d26637e093f5a7e1f3365c0fb37bfe415428427d9542e323c)
                check_type(argname="argument current_lsn", value=current_lsn, expected_type=type_hints["current_lsn"])
                check_type(argname="argument keep_csv_files", value=keep_csv_files, expected_type=type_hints["keep_csv_files"])
                check_type(argname="argument load_timeout", value=load_timeout, expected_type=type_hints["load_timeout"])
                check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
                check_type(argname="argument max_k_bytes_per_read", value=max_k_bytes_per_read, expected_type=type_hints["max_k_bytes_per_read"])
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
                check_type(argname="argument set_data_capture_changes", value=set_data_capture_changes, expected_type=type_hints["set_data_capture_changes"])
                check_type(argname="argument write_buffer_size", value=write_buffer_size, expected_type=type_hints["write_buffer_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if current_lsn is not None:
                self._values["current_lsn"] = current_lsn
            if keep_csv_files is not None:
                self._values["keep_csv_files"] = keep_csv_files
            if load_timeout is not None:
                self._values["load_timeout"] = load_timeout
            if max_file_size is not None:
                self._values["max_file_size"] = max_file_size
            if max_k_bytes_per_read is not None:
                self._values["max_k_bytes_per_read"] = max_k_bytes_per_read
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id
            if set_data_capture_changes is not None:
                self._values["set_data_capture_changes"] = set_data_capture_changes
            if write_buffer_size is not None:
                self._values["write_buffer_size"] = write_buffer_size

        @builtins.property
        def current_lsn(self) -> typing.Optional[builtins.str]:
            '''For ongoing replication (CDC), use CurrentLSN to specify a log sequence number (LSN) where you want the replication to start.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-ibmdb2settings.html#cfn-dms-endpoint-ibmdb2settings-currentlsn
            '''
            result = self._values.get("current_lsn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def keep_csv_files(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If true, AWS DMS saves any .csv files to the Db2 LUW target that were used to replicate data. DMS uses these files for analysis and troubleshooting.

            The default value is false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-ibmdb2settings.html#cfn-dms-endpoint-ibmdb2settings-keepcsvfiles
            '''
            result = self._values.get("keep_csv_files")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def load_timeout(self) -> typing.Optional[jsii.Number]:
            '''The amount of time (in milliseconds) before AWS DMS times out operations performed by DMS on the Db2 target.

            The default value is 1200 (20 minutes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-ibmdb2settings.html#cfn-dms-endpoint-ibmdb2settings-loadtimeout
            '''
            result = self._values.get("load_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_file_size(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum size (in KB) of .csv files used to transfer data to Db2 LUW.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-ibmdb2settings.html#cfn-dms-endpoint-ibmdb2settings-maxfilesize
            '''
            result = self._values.get("max_file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_k_bytes_per_read(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of bytes per read, as a NUMBER value.

            The default is 64 KB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-ibmdb2settings.html#cfn-dms-endpoint-ibmdb2settings-maxkbytesperread
            '''
            result = self._values.get("max_k_bytes_per_read")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` .

            The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value ofthe AWS Secrets Manager secret that allows access to the Db2 LUW endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both.

               For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-ibmdb2settings.html#cfn-dms-endpoint-ibmdb2settings-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the IBMDB2 endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-ibmdb2settings.html#cfn-dms-endpoint-ibmdb2settings-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def set_data_capture_changes(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables ongoing replication (CDC) as a BOOLEAN value.

            The default is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-ibmdb2settings.html#cfn-dms-endpoint-ibmdb2settings-setdatacapturechanges
            '''
            result = self._values.get("set_data_capture_changes")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def write_buffer_size(self) -> typing.Optional[jsii.Number]:
            '''The size (in KB) of the in-memory file write buffer used when generating .csv files on the local disk on the DMS replication instance. The default value is 1024 (1 MB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-ibmdb2settings.html#cfn-dms-endpoint-ibmdb2settings-writebuffersize
            '''
            result = self._values.get("write_buffer_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IbmDb2SettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.KafkaSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "broker": "broker",
            "include_control_details": "includeControlDetails",
            "include_null_and_empty": "includeNullAndEmpty",
            "include_partition_value": "includePartitionValue",
            "include_table_alter_operations": "includeTableAlterOperations",
            "include_transaction_details": "includeTransactionDetails",
            "message_format": "messageFormat",
            "message_max_bytes": "messageMaxBytes",
            "no_hex_prefix": "noHexPrefix",
            "partition_include_schema_table": "partitionIncludeSchemaTable",
            "sasl_password": "saslPassword",
            "sasl_user_name": "saslUserName",
            "security_protocol": "securityProtocol",
            "ssl_ca_certificate_arn": "sslCaCertificateArn",
            "ssl_client_certificate_arn": "sslClientCertificateArn",
            "ssl_client_key_arn": "sslClientKeyArn",
            "ssl_client_key_password": "sslClientKeyPassword",
            "topic": "topic",
        },
    )
    class KafkaSettingsProperty:
        def __init__(
            self,
            *,
            broker: typing.Optional[builtins.str] = None,
            include_control_details: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_null_and_empty: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_partition_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_table_alter_operations: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_transaction_details: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            message_format: typing.Optional[builtins.str] = None,
            message_max_bytes: typing.Optional[jsii.Number] = None,
            no_hex_prefix: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            partition_include_schema_table: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            sasl_password: typing.Optional[builtins.str] = None,
            sasl_user_name: typing.Optional[builtins.str] = None,
            security_protocol: typing.Optional[builtins.str] = None,
            ssl_ca_certificate_arn: typing.Optional[builtins.str] = None,
            ssl_client_certificate_arn: typing.Optional[builtins.str] = None,
            ssl_client_key_arn: typing.Optional[builtins.str] = None,
            ssl_client_key_password: typing.Optional[builtins.str] = None,
            topic: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that describes an Apache Kafka endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For more information about other available settings, see `Using object mapping to migrate data to a Kafka topic <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Kafka.html#CHAP_Target.Kafka.ObjectMapping>`_ in the *AWS Database Migration Service User Guide* .

            :param broker: A comma-separated list of one or more broker locations in your Kafka cluster that host your Kafka instance. Specify each broker location in the form ``*broker-hostname-or-ip* : *port*`` . For example, ``"ec2-12-345-678-901.compute-1.amazonaws.com:2345"`` . For more information and examples of specifying a list of broker locations, see `Using Apache Kafka as a target for AWS Database Migration Service <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Kafka.html>`_ in the *AWS Database Migration Service User Guide* .
            :param include_control_details: Shows detailed control information for table definition, column definition, and table and column changes in the Kafka message output. The default is ``false`` .
            :param include_null_and_empty: Include NULL and empty columns for records migrated to the endpoint. The default is ``false`` .
            :param include_partition_value: Shows the partition value within the Kafka message output unless the partition type is ``schema-table-type`` . The default is ``false`` .
            :param include_table_alter_operations: Includes any data definition language (DDL) operations that change the table in the control data, such as ``rename-table`` , ``drop-table`` , ``add-column`` , ``drop-column`` , and ``rename-column`` . The default is ``false`` .
            :param include_transaction_details: Provides detailed transaction information from the source database. This information includes a commit timestamp, a log position, and values for ``transaction_id`` , previous ``transaction_id`` , and ``transaction_record_id`` (the record offset within a transaction). The default is ``false`` .
            :param message_format: The output format for the records created on the endpoint. The message format is ``JSON`` (default) or ``JSON_UNFORMATTED`` (a single line with no tab).
            :param message_max_bytes: The maximum size in bytes for records created on the endpoint The default is 1,000,000.
            :param no_hex_prefix: Set this optional parameter to ``true`` to avoid adding a '0x' prefix to raw data in hexadecimal format. For example, by default, AWS DMS adds a '0x' prefix to the LOB column type in hexadecimal format moving from an Oracle source to a Kafka target. Use the ``NoHexPrefix`` endpoint setting to enable migration of RAW data type columns without adding the '0x' prefix.
            :param partition_include_schema_table: Prefixes schema and table names to partition values, when the partition type is ``primary-key-type`` . Doing this increases data distribution among Kafka partitions. For example, suppose that a SysBench schema has thousands of tables and each table has only limited range for a primary key. In this case, the same primary key is sent from thousands of tables to the same partition, which causes throttling. The default is ``false`` .
            :param sasl_password: The secure password that you created when you first set up your Amazon MSK cluster to validate a client identity and make an encrypted connection between server and client using SASL-SSL authentication.
            :param sasl_user_name: The secure user name you created when you first set up your Amazon MSK cluster to validate a client identity and make an encrypted connection between server and client using SASL-SSL authentication.
            :param security_protocol: Set secure connection to a Kafka target endpoint using Transport Layer Security (TLS). Options include ``ssl-encryption`` , ``ssl-authentication`` , and ``sasl-ssl`` . ``sasl-ssl`` requires ``SaslUsername`` and ``SaslPassword`` .
            :param ssl_ca_certificate_arn: The Amazon Resource Name (ARN) for the private certificate authority (CA) cert that AWS DMS uses to securely connect to your Kafka target endpoint.
            :param ssl_client_certificate_arn: The Amazon Resource Name (ARN) of the client certificate used to securely connect to a Kafka target endpoint.
            :param ssl_client_key_arn: The Amazon Resource Name (ARN) for the client private key used to securely connect to a Kafka target endpoint.
            :param ssl_client_key_password: The password for the client private key used to securely connect to a Kafka target endpoint.
            :param topic: The topic to which you migrate the data. If you don't specify a topic, AWS DMS specifies ``"kafka-default-topic"`` as the migration topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                kafka_settings_property = dms_mixins.CfnEndpointPropsMixin.KafkaSettingsProperty(
                    broker="broker",
                    include_control_details=False,
                    include_null_and_empty=False,
                    include_partition_value=False,
                    include_table_alter_operations=False,
                    include_transaction_details=False,
                    message_format="messageFormat",
                    message_max_bytes=123,
                    no_hex_prefix=False,
                    partition_include_schema_table=False,
                    sasl_password="saslPassword",
                    sasl_user_name="saslUserName",
                    security_protocol="securityProtocol",
                    ssl_ca_certificate_arn="sslCaCertificateArn",
                    ssl_client_certificate_arn="sslClientCertificateArn",
                    ssl_client_key_arn="sslClientKeyArn",
                    ssl_client_key_password="sslClientKeyPassword",
                    topic="topic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4eb2225cd664740e3203879c5c84201ba5dc2243ac35aa43b37657b1674a705a)
                check_type(argname="argument broker", value=broker, expected_type=type_hints["broker"])
                check_type(argname="argument include_control_details", value=include_control_details, expected_type=type_hints["include_control_details"])
                check_type(argname="argument include_null_and_empty", value=include_null_and_empty, expected_type=type_hints["include_null_and_empty"])
                check_type(argname="argument include_partition_value", value=include_partition_value, expected_type=type_hints["include_partition_value"])
                check_type(argname="argument include_table_alter_operations", value=include_table_alter_operations, expected_type=type_hints["include_table_alter_operations"])
                check_type(argname="argument include_transaction_details", value=include_transaction_details, expected_type=type_hints["include_transaction_details"])
                check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
                check_type(argname="argument message_max_bytes", value=message_max_bytes, expected_type=type_hints["message_max_bytes"])
                check_type(argname="argument no_hex_prefix", value=no_hex_prefix, expected_type=type_hints["no_hex_prefix"])
                check_type(argname="argument partition_include_schema_table", value=partition_include_schema_table, expected_type=type_hints["partition_include_schema_table"])
                check_type(argname="argument sasl_password", value=sasl_password, expected_type=type_hints["sasl_password"])
                check_type(argname="argument sasl_user_name", value=sasl_user_name, expected_type=type_hints["sasl_user_name"])
                check_type(argname="argument security_protocol", value=security_protocol, expected_type=type_hints["security_protocol"])
                check_type(argname="argument ssl_ca_certificate_arn", value=ssl_ca_certificate_arn, expected_type=type_hints["ssl_ca_certificate_arn"])
                check_type(argname="argument ssl_client_certificate_arn", value=ssl_client_certificate_arn, expected_type=type_hints["ssl_client_certificate_arn"])
                check_type(argname="argument ssl_client_key_arn", value=ssl_client_key_arn, expected_type=type_hints["ssl_client_key_arn"])
                check_type(argname="argument ssl_client_key_password", value=ssl_client_key_password, expected_type=type_hints["ssl_client_key_password"])
                check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if broker is not None:
                self._values["broker"] = broker
            if include_control_details is not None:
                self._values["include_control_details"] = include_control_details
            if include_null_and_empty is not None:
                self._values["include_null_and_empty"] = include_null_and_empty
            if include_partition_value is not None:
                self._values["include_partition_value"] = include_partition_value
            if include_table_alter_operations is not None:
                self._values["include_table_alter_operations"] = include_table_alter_operations
            if include_transaction_details is not None:
                self._values["include_transaction_details"] = include_transaction_details
            if message_format is not None:
                self._values["message_format"] = message_format
            if message_max_bytes is not None:
                self._values["message_max_bytes"] = message_max_bytes
            if no_hex_prefix is not None:
                self._values["no_hex_prefix"] = no_hex_prefix
            if partition_include_schema_table is not None:
                self._values["partition_include_schema_table"] = partition_include_schema_table
            if sasl_password is not None:
                self._values["sasl_password"] = sasl_password
            if sasl_user_name is not None:
                self._values["sasl_user_name"] = sasl_user_name
            if security_protocol is not None:
                self._values["security_protocol"] = security_protocol
            if ssl_ca_certificate_arn is not None:
                self._values["ssl_ca_certificate_arn"] = ssl_ca_certificate_arn
            if ssl_client_certificate_arn is not None:
                self._values["ssl_client_certificate_arn"] = ssl_client_certificate_arn
            if ssl_client_key_arn is not None:
                self._values["ssl_client_key_arn"] = ssl_client_key_arn
            if ssl_client_key_password is not None:
                self._values["ssl_client_key_password"] = ssl_client_key_password
            if topic is not None:
                self._values["topic"] = topic

        @builtins.property
        def broker(self) -> typing.Optional[builtins.str]:
            '''A comma-separated list of one or more broker locations in your Kafka cluster that host your Kafka instance.

            Specify each broker location in the form ``*broker-hostname-or-ip* : *port*`` . For example, ``"ec2-12-345-678-901.compute-1.amazonaws.com:2345"`` . For more information and examples of specifying a list of broker locations, see `Using Apache Kafka as a target for AWS Database Migration Service <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Kafka.html>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-broker
            '''
            result = self._values.get("broker")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_control_details(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Shows detailed control information for table definition, column definition, and table and column changes in the Kafka message output.

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-includecontroldetails
            '''
            result = self._values.get("include_control_details")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_null_and_empty(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include NULL and empty columns for records migrated to the endpoint.

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-includenullandempty
            '''
            result = self._values.get("include_null_and_empty")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_partition_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Shows the partition value within the Kafka message output unless the partition type is ``schema-table-type`` .

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-includepartitionvalue
            '''
            result = self._values.get("include_partition_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_table_alter_operations(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Includes any data definition language (DDL) operations that change the table in the control data, such as ``rename-table`` , ``drop-table`` , ``add-column`` , ``drop-column`` , and ``rename-column`` .

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-includetablealteroperations
            '''
            result = self._values.get("include_table_alter_operations")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_transaction_details(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Provides detailed transaction information from the source database.

            This information includes a commit timestamp, a log position, and values for ``transaction_id`` , previous ``transaction_id`` , and ``transaction_record_id`` (the record offset within a transaction). The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-includetransactiondetails
            '''
            result = self._values.get("include_transaction_details")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def message_format(self) -> typing.Optional[builtins.str]:
            '''The output format for the records created on the endpoint.

            The message format is ``JSON`` (default) or ``JSON_UNFORMATTED`` (a single line with no tab).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-messageformat
            '''
            result = self._values.get("message_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_max_bytes(self) -> typing.Optional[jsii.Number]:
            '''The maximum size in bytes for records created on the endpoint The default is 1,000,000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-messagemaxbytes
            '''
            result = self._values.get("message_max_bytes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def no_hex_prefix(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this optional parameter to ``true`` to avoid adding a '0x' prefix to raw data in hexadecimal format.

            For example, by default, AWS DMS adds a '0x' prefix to the LOB column type in hexadecimal format moving from an Oracle source to a Kafka target. Use the ``NoHexPrefix`` endpoint setting to enable migration of RAW data type columns without adding the '0x' prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-nohexprefix
            '''
            result = self._values.get("no_hex_prefix")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def partition_include_schema_table(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Prefixes schema and table names to partition values, when the partition type is ``primary-key-type`` .

            Doing this increases data distribution among Kafka partitions. For example, suppose that a SysBench schema has thousands of tables and each table has only limited range for a primary key. In this case, the same primary key is sent from thousands of tables to the same partition, which causes throttling. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-partitionincludeschematable
            '''
            result = self._values.get("partition_include_schema_table")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def sasl_password(self) -> typing.Optional[builtins.str]:
            '''The secure password that you created when you first set up your Amazon MSK cluster to validate a client identity and make an encrypted connection between server and client using SASL-SSL authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-saslpassword
            '''
            result = self._values.get("sasl_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sasl_user_name(self) -> typing.Optional[builtins.str]:
            '''The secure user name you created when you first set up your Amazon MSK cluster to validate a client identity and make an encrypted connection between server and client using SASL-SSL authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-saslusername
            '''
            result = self._values.get("sasl_user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_protocol(self) -> typing.Optional[builtins.str]:
            '''Set secure connection to a Kafka target endpoint using Transport Layer Security (TLS).

            Options include ``ssl-encryption`` , ``ssl-authentication`` , and ``sasl-ssl`` . ``sasl-ssl`` requires ``SaslUsername`` and ``SaslPassword`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-securityprotocol
            '''
            result = self._values.get("security_protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_ca_certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the private certificate authority (CA) cert that AWS DMS uses to securely connect to your Kafka target endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-sslcacertificatearn
            '''
            result = self._values.get("ssl_ca_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_client_certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the client certificate used to securely connect to a Kafka target endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-sslclientcertificatearn
            '''
            result = self._values.get("ssl_client_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_client_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the client private key used to securely connect to a Kafka target endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-sslclientkeyarn
            '''
            result = self._values.get("ssl_client_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_client_key_password(self) -> typing.Optional[builtins.str]:
            '''The password for the client private key used to securely connect to a Kafka target endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-sslclientkeypassword
            '''
            result = self._values.get("ssl_client_key_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic(self) -> typing.Optional[builtins.str]:
            '''The topic to which you migrate the data.

            If you don't specify a topic, AWS DMS specifies ``"kafka-default-topic"`` as the migration topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-topic
            '''
            result = self._values.get("topic")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.KinesisSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "include_control_details": "includeControlDetails",
            "include_null_and_empty": "includeNullAndEmpty",
            "include_partition_value": "includePartitionValue",
            "include_table_alter_operations": "includeTableAlterOperations",
            "include_transaction_details": "includeTransactionDetails",
            "message_format": "messageFormat",
            "no_hex_prefix": "noHexPrefix",
            "partition_include_schema_table": "partitionIncludeSchemaTable",
            "service_access_role_arn": "serviceAccessRoleArn",
            "stream_arn": "streamArn",
        },
    )
    class KinesisSettingsProperty:
        def __init__(
            self,
            *,
            include_control_details: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_null_and_empty: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_partition_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_table_alter_operations: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_transaction_details: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            message_format: typing.Optional[builtins.str] = None,
            no_hex_prefix: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            partition_include_schema_table: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            service_access_role_arn: typing.Optional[builtins.str] = None,
            stream_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that describes an Amazon Kinesis Data Stream endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For more information about other available settings, see `Using object mapping to migrate data to a Kinesis data stream <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Kinesis.html#CHAP_Target.Kinesis.ObjectMapping>`_ in the *AWS Database Migration Service User Guide* .

            :param include_control_details: Shows detailed control information for table definition, column definition, and table and column changes in the Kinesis message output. The default is ``false`` .
            :param include_null_and_empty: Include NULL and empty columns for records migrated to the endpoint. The default is ``false`` .
            :param include_partition_value: Shows the partition value within the Kinesis message output, unless the partition type is ``schema-table-type`` . The default is ``false`` .
            :param include_table_alter_operations: Includes any data definition language (DDL) operations that change the table in the control data, such as ``rename-table`` , ``drop-table`` , ``add-column`` , ``drop-column`` , and ``rename-column`` . The default is ``false`` .
            :param include_transaction_details: Provides detailed transaction information from the source database. This information includes a commit timestamp, a log position, and values for ``transaction_id`` , previous ``transaction_id`` , and ``transaction_record_id`` (the record offset within a transaction). The default is ``false`` .
            :param message_format: The output format for the records created on the endpoint. The message format is ``JSON`` (default) or ``JSON_UNFORMATTED`` (a single line with no tab).
            :param no_hex_prefix: Set this optional parameter to ``true`` to avoid adding a '0x' prefix to raw data in hexadecimal format. For example, by default, AWS DMS adds a '0x' prefix to the LOB column type in hexadecimal format moving from an Oracle source to an Amazon Kinesis target. Use the ``NoHexPrefix`` endpoint setting to enable migration of RAW data type columns without adding the '0x' prefix.
            :param partition_include_schema_table: Prefixes schema and table names to partition values, when the partition type is ``primary-key-type`` . Doing this increases data distribution among Kinesis shards. For example, suppose that a SysBench schema has thousands of tables and each table has only limited range for a primary key. In this case, the same primary key is sent from thousands of tables to the same shard, which causes throttling. The default is ``false`` .
            :param service_access_role_arn: The Amazon Resource Name (ARN) for the IAM role that AWS DMS uses to write to the Kinesis data stream. The role must allow the ``iam:PassRole`` action.
            :param stream_arn: The Amazon Resource Name (ARN) for the Amazon Kinesis Data Streams endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                kinesis_settings_property = dms_mixins.CfnEndpointPropsMixin.KinesisSettingsProperty(
                    include_control_details=False,
                    include_null_and_empty=False,
                    include_partition_value=False,
                    include_table_alter_operations=False,
                    include_transaction_details=False,
                    message_format="messageFormat",
                    no_hex_prefix=False,
                    partition_include_schema_table=False,
                    service_access_role_arn="serviceAccessRoleArn",
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed12e1830ccb059c4627e6b3c51b4b3c2d26f32b5dabf6ba7ee3e9270cb018a0)
                check_type(argname="argument include_control_details", value=include_control_details, expected_type=type_hints["include_control_details"])
                check_type(argname="argument include_null_and_empty", value=include_null_and_empty, expected_type=type_hints["include_null_and_empty"])
                check_type(argname="argument include_partition_value", value=include_partition_value, expected_type=type_hints["include_partition_value"])
                check_type(argname="argument include_table_alter_operations", value=include_table_alter_operations, expected_type=type_hints["include_table_alter_operations"])
                check_type(argname="argument include_transaction_details", value=include_transaction_details, expected_type=type_hints["include_transaction_details"])
                check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
                check_type(argname="argument no_hex_prefix", value=no_hex_prefix, expected_type=type_hints["no_hex_prefix"])
                check_type(argname="argument partition_include_schema_table", value=partition_include_schema_table, expected_type=type_hints["partition_include_schema_table"])
                check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_control_details is not None:
                self._values["include_control_details"] = include_control_details
            if include_null_and_empty is not None:
                self._values["include_null_and_empty"] = include_null_and_empty
            if include_partition_value is not None:
                self._values["include_partition_value"] = include_partition_value
            if include_table_alter_operations is not None:
                self._values["include_table_alter_operations"] = include_table_alter_operations
            if include_transaction_details is not None:
                self._values["include_transaction_details"] = include_transaction_details
            if message_format is not None:
                self._values["message_format"] = message_format
            if no_hex_prefix is not None:
                self._values["no_hex_prefix"] = no_hex_prefix
            if partition_include_schema_table is not None:
                self._values["partition_include_schema_table"] = partition_include_schema_table
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn
            if stream_arn is not None:
                self._values["stream_arn"] = stream_arn

        @builtins.property
        def include_control_details(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Shows detailed control information for table definition, column definition, and table and column changes in the Kinesis message output.

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-includecontroldetails
            '''
            result = self._values.get("include_control_details")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_null_and_empty(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include NULL and empty columns for records migrated to the endpoint.

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-includenullandempty
            '''
            result = self._values.get("include_null_and_empty")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_partition_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Shows the partition value within the Kinesis message output, unless the partition type is ``schema-table-type`` .

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-includepartitionvalue
            '''
            result = self._values.get("include_partition_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_table_alter_operations(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Includes any data definition language (DDL) operations that change the table in the control data, such as ``rename-table`` , ``drop-table`` , ``add-column`` , ``drop-column`` , and ``rename-column`` .

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-includetablealteroperations
            '''
            result = self._values.get("include_table_alter_operations")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_transaction_details(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Provides detailed transaction information from the source database.

            This information includes a commit timestamp, a log position, and values for ``transaction_id`` , previous ``transaction_id`` , and ``transaction_record_id`` (the record offset within a transaction). The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-includetransactiondetails
            '''
            result = self._values.get("include_transaction_details")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def message_format(self) -> typing.Optional[builtins.str]:
            '''The output format for the records created on the endpoint.

            The message format is ``JSON`` (default) or ``JSON_UNFORMATTED`` (a single line with no tab).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-messageformat
            '''
            result = self._values.get("message_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def no_hex_prefix(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this optional parameter to ``true`` to avoid adding a '0x' prefix to raw data in hexadecimal format.

            For example, by default, AWS DMS adds a '0x' prefix to the LOB column type in hexadecimal format moving from an Oracle source to an Amazon Kinesis target. Use the ``NoHexPrefix`` endpoint setting to enable migration of RAW data type columns without adding the '0x' prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-nohexprefix
            '''
            result = self._values.get("no_hex_prefix")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def partition_include_schema_table(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Prefixes schema and table names to partition values, when the partition type is ``primary-key-type`` .

            Doing this increases data distribution among Kinesis shards. For example, suppose that a SysBench schema has thousands of tables and each table has only limited range for a primary key. In this case, the same primary key is sent from thousands of tables to the same shard, which causes throttling. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-partitionincludeschematable
            '''
            result = self._values.get("partition_include_schema_table")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the IAM role that AWS DMS uses to write to the Kinesis data stream.

            The role must allow the ``iam:PassRole`` action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-serviceaccessrolearn
            '''
            result = self._values.get("service_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the Amazon Kinesis Data Streams endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-streamarn
            '''
            result = self._values.get("stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.MicrosoftSqlServerSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bcp_packet_size": "bcpPacketSize",
            "control_tables_file_group": "controlTablesFileGroup",
            "database_name": "databaseName",
            "force_lob_lookup": "forceLobLookup",
            "password": "password",
            "port": "port",
            "query_single_always_on_node": "querySingleAlwaysOnNode",
            "read_backup_only": "readBackupOnly",
            "safeguard_policy": "safeguardPolicy",
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_secret_id": "secretsManagerSecretId",
            "server_name": "serverName",
            "tlog_access_mode": "tlogAccessMode",
            "trim_space_in_char": "trimSpaceInChar",
            "use_bcp_full_load": "useBcpFullLoad",
            "username": "username",
            "use_third_party_backup_device": "useThirdPartyBackupDevice",
        },
    )
    class MicrosoftSqlServerSettingsProperty:
        def __init__(
            self,
            *,
            bcp_packet_size: typing.Optional[jsii.Number] = None,
            control_tables_file_group: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            force_lob_lookup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            password: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            query_single_always_on_node: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            read_backup_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            safeguard_policy: typing.Optional[builtins.str] = None,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
            server_name: typing.Optional[builtins.str] = None,
            tlog_access_mode: typing.Optional[builtins.str] = None,
            trim_space_in_char: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_bcp_full_load: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            username: typing.Optional[builtins.str] = None,
            use_third_party_backup_device: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Provides information that defines a Microsoft SQL Server endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For information about other available settings, see `Extra connection attributes when using SQL Server as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.SQLServer.html#CHAP_Source.SQLServer.ConnectionAttrib>`_ and `Extra connection attributes when using SQL Server as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.SQLServer.html#CHAP_Target.SQLServer.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

            :param bcp_packet_size: The maximum size of the packets (in bytes) used to transfer data using BCP.
            :param control_tables_file_group: Specifies a file group for the AWS DMS internal tables. When the replication task starts, all the internal AWS DMS control tables (awsdms_ apply_exception, awsdms_apply, awsdms_changes) are created for the specified file group.
            :param database_name: Database name for the endpoint.
            :param force_lob_lookup: Forces LOB lookup on inline LOB.
            :param password: Endpoint connection password.
            :param port: Endpoint TCP port.
            :param query_single_always_on_node: Cleans and recreates table metadata information on the replication instance when a mismatch occurs. An example is a situation where running an alter DDL statement on a table might result in different information about the table cached in the replication instance.
            :param read_backup_only: When this attribute is set to ``Y`` , AWS DMS only reads changes from transaction log backups and doesn't read from the active transaction log file during ongoing replication. Setting this parameter to ``Y`` enables you to control active transaction log file growth during full load and ongoing replication tasks. However, it can add some source latency to ongoing replication.
            :param safeguard_policy: Use this attribute to minimize the need to access the backup log and enable AWS DMS to prevent truncation using one of the following two methods. *Start transactions in the database:* This is the default method. When this method is used, AWS DMS prevents TLOG truncation by mimicking a transaction in the database. As long as such a transaction is open, changes that appear after the transaction started aren't truncated. If you need Microsoft Replication to be enabled in your database, then you must choose this method. *Exclusively use sp_repldone within a single task* : When this method is used, AWS DMS reads the changes and then uses sp_repldone to mark the TLOG transactions as ready for truncation. Although this method doesn't involve any transactional activities, it can only be used when Microsoft Replication isn't running. Also, when using this method, only one AWS DMS task can access the database at any given time. Therefore, if you need to run parallel AWS DMS tasks against the same database, use the default method.
            :param secrets_manager_access_role_arn: The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` . The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the SQL Server endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both. For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the MicrosoftSQLServer endpoint connection details.
            :param server_name: Fully qualified domain name of the endpoint. For an Amazon RDS SQL Server instance, this is the output of `DescribeDBInstances <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>`_ , in the ``[Endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_Endpoint.html) .Address`` field.
            :param tlog_access_mode: Indicates the mode used to fetch CDC data.
            :param trim_space_in_char: Use the ``TrimSpaceInChar`` source endpoint setting to right-trim data on CHAR and NCHAR data types during migration. Setting ``TrimSpaceInChar`` does not left-trim data. The default value is ``true`` .
            :param use_bcp_full_load: Use this to attribute to transfer data for full-load operations using BCP. When the target table contains an identity column that does not exist in the source table, you must disable the use BCP for loading table option.
            :param username: Endpoint connection user name.
            :param use_third_party_backup_device: When this attribute is set to ``Y`` , DMS processes third-party transaction log backups if they are created in native format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                microsoft_sql_server_settings_property = dms_mixins.CfnEndpointPropsMixin.MicrosoftSqlServerSettingsProperty(
                    bcp_packet_size=123,
                    control_tables_file_group="controlTablesFileGroup",
                    database_name="databaseName",
                    force_lob_lookup=False,
                    password="password",
                    port=123,
                    query_single_always_on_node=False,
                    read_backup_only=False,
                    safeguard_policy="safeguardPolicy",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    server_name="serverName",
                    tlog_access_mode="tlogAccessMode",
                    trim_space_in_char=False,
                    use_bcp_full_load=False,
                    username="username",
                    use_third_party_backup_device=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77c51f445e82a3d0b49f8b49b958649e47308bebb43eb574e5213fe8a2331b5c)
                check_type(argname="argument bcp_packet_size", value=bcp_packet_size, expected_type=type_hints["bcp_packet_size"])
                check_type(argname="argument control_tables_file_group", value=control_tables_file_group, expected_type=type_hints["control_tables_file_group"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument force_lob_lookup", value=force_lob_lookup, expected_type=type_hints["force_lob_lookup"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument query_single_always_on_node", value=query_single_always_on_node, expected_type=type_hints["query_single_always_on_node"])
                check_type(argname="argument read_backup_only", value=read_backup_only, expected_type=type_hints["read_backup_only"])
                check_type(argname="argument safeguard_policy", value=safeguard_policy, expected_type=type_hints["safeguard_policy"])
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument tlog_access_mode", value=tlog_access_mode, expected_type=type_hints["tlog_access_mode"])
                check_type(argname="argument trim_space_in_char", value=trim_space_in_char, expected_type=type_hints["trim_space_in_char"])
                check_type(argname="argument use_bcp_full_load", value=use_bcp_full_load, expected_type=type_hints["use_bcp_full_load"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
                check_type(argname="argument use_third_party_backup_device", value=use_third_party_backup_device, expected_type=type_hints["use_third_party_backup_device"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bcp_packet_size is not None:
                self._values["bcp_packet_size"] = bcp_packet_size
            if control_tables_file_group is not None:
                self._values["control_tables_file_group"] = control_tables_file_group
            if database_name is not None:
                self._values["database_name"] = database_name
            if force_lob_lookup is not None:
                self._values["force_lob_lookup"] = force_lob_lookup
            if password is not None:
                self._values["password"] = password
            if port is not None:
                self._values["port"] = port
            if query_single_always_on_node is not None:
                self._values["query_single_always_on_node"] = query_single_always_on_node
            if read_backup_only is not None:
                self._values["read_backup_only"] = read_backup_only
            if safeguard_policy is not None:
                self._values["safeguard_policy"] = safeguard_policy
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id
            if server_name is not None:
                self._values["server_name"] = server_name
            if tlog_access_mode is not None:
                self._values["tlog_access_mode"] = tlog_access_mode
            if trim_space_in_char is not None:
                self._values["trim_space_in_char"] = trim_space_in_char
            if use_bcp_full_load is not None:
                self._values["use_bcp_full_load"] = use_bcp_full_load
            if username is not None:
                self._values["username"] = username
            if use_third_party_backup_device is not None:
                self._values["use_third_party_backup_device"] = use_third_party_backup_device

        @builtins.property
        def bcp_packet_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum size of the packets (in bytes) used to transfer data using BCP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-bcppacketsize
            '''
            result = self._values.get("bcp_packet_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def control_tables_file_group(self) -> typing.Optional[builtins.str]:
            '''Specifies a file group for the AWS DMS internal tables.

            When the replication task starts, all the internal AWS DMS control tables (awsdms_ apply_exception, awsdms_apply, awsdms_changes) are created for the specified file group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-controltablesfilegroup
            '''
            result = self._values.get("control_tables_file_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''Database name for the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def force_lob_lookup(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Forces LOB lookup on inline LOB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-forceloblookup
            '''
            result = self._values.get("force_lob_lookup")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''Endpoint connection password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''Endpoint TCP port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def query_single_always_on_node(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Cleans and recreates table metadata information on the replication instance when a mismatch occurs.

            An example is a situation where running an alter DDL statement on a table might result in different information about the table cached in the replication instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-querysinglealwaysonnode
            '''
            result = self._values.get("query_single_always_on_node")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def read_backup_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When this attribute is set to ``Y`` , AWS DMS only reads changes from transaction log backups and doesn't read from the active transaction log file during ongoing replication.

            Setting this parameter to ``Y`` enables you to control active transaction log file growth during full load and ongoing replication tasks. However, it can add some source latency to ongoing replication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-readbackuponly
            '''
            result = self._values.get("read_backup_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def safeguard_policy(self) -> typing.Optional[builtins.str]:
            '''Use this attribute to minimize the need to access the backup log and enable AWS DMS to prevent truncation using one of the following two methods.

            *Start transactions in the database:* This is the default method. When this method is used, AWS DMS prevents TLOG truncation by mimicking a transaction in the database. As long as such a transaction is open, changes that appear after the transaction started aren't truncated. If you need Microsoft Replication to be enabled in your database, then you must choose this method.

            *Exclusively use sp_repldone within a single task* : When this method is used, AWS DMS reads the changes and then uses sp_repldone to mark the TLOG transactions as ready for truncation. Although this method doesn't involve any transactional activities, it can only be used when Microsoft Replication isn't running. Also, when using this method, only one AWS DMS task can access the database at any given time. Therefore, if you need to run parallel AWS DMS tasks against the same database, use the default method.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-safeguardpolicy
            '''
            result = self._values.get("safeguard_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` .

            The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the SQL Server endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both.

               For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the MicrosoftSQLServer endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''Fully qualified domain name of the endpoint.

            For an Amazon RDS SQL Server instance, this is the output of `DescribeDBInstances <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>`_ , in the ``[Endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_Endpoint.html) .Address`` field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tlog_access_mode(self) -> typing.Optional[builtins.str]:
            '''Indicates the mode used to fetch CDC data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-tlogaccessmode
            '''
            result = self._values.get("tlog_access_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trim_space_in_char(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Use the ``TrimSpaceInChar`` source endpoint setting to right-trim data on CHAR and NCHAR data types during migration.

            Setting ``TrimSpaceInChar`` does not left-trim data. The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-trimspaceinchar
            '''
            result = self._values.get("trim_space_in_char")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_bcp_full_load(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Use this to attribute to transfer data for full-load operations using BCP.

            When the target table contains an identity column that does not exist in the source table, you must disable the use BCP for loading table option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-usebcpfullload
            '''
            result = self._values.get("use_bcp_full_load")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''Endpoint connection user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_third_party_backup_device(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When this attribute is set to ``Y`` , DMS processes third-party transaction log backups if they are created in native format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-microsoftsqlserversettings.html#cfn-dms-endpoint-microsoftsqlserversettings-usethirdpartybackupdevice
            '''
            result = self._values.get("use_third_party_backup_device")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MicrosoftSqlServerSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.MongoDbSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_mechanism": "authMechanism",
            "auth_source": "authSource",
            "auth_type": "authType",
            "database_name": "databaseName",
            "docs_to_investigate": "docsToInvestigate",
            "extract_doc_id": "extractDocId",
            "nesting_level": "nestingLevel",
            "password": "password",
            "port": "port",
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_secret_id": "secretsManagerSecretId",
            "server_name": "serverName",
            "username": "username",
        },
    )
    class MongoDbSettingsProperty:
        def __init__(
            self,
            *,
            auth_mechanism: typing.Optional[builtins.str] = None,
            auth_source: typing.Optional[builtins.str] = None,
            auth_type: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            docs_to_investigate: typing.Optional[builtins.str] = None,
            extract_doc_id: typing.Optional[builtins.str] = None,
            nesting_level: typing.Optional[builtins.str] = None,
            password: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
            server_name: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a MongoDB endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For more information about other available settings, see `Endpoint configuration settings when using MongoDB as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MongoDB.html#CHAP_Source.MongoDB.Configuration>`_ in the *AWS Database Migration Service User Guide* .

            :param auth_mechanism: The authentication mechanism you use to access the MongoDB source endpoint. For the default value, in MongoDB version 2.x, ``"default"`` is ``"mongodb_cr"`` . For MongoDB version 3.x or later, ``"default"`` is ``"scram_sha_1"`` . This setting isn't used when ``AuthType`` is set to ``"no"`` .
            :param auth_source: The MongoDB database name. This setting isn't used when ``AuthType`` is set to ``"no"`` . The default is ``"admin"`` .
            :param auth_type: The authentication type you use to access the MongoDB source endpoint. When set to ``"no"`` , user name and password parameters are not used and can be empty.
            :param database_name: The database name on the MongoDB source endpoint.
            :param docs_to_investigate: Indicates the number of documents to preview to determine the document organization. Use this setting when ``NestingLevel`` is set to ``"one"`` . Must be a positive value greater than ``0`` . Default value is ``1000`` .
            :param extract_doc_id: Specifies the document ID. Use this setting when ``NestingLevel`` is set to ``"none"`` . Default value is ``"false"`` .
            :param nesting_level: Specifies either document or table mode. Default value is ``"none"`` . Specify ``"none"`` to use document mode. Specify ``"one"`` to use table mode.
            :param password: The password for the user account you use to access the MongoDB source endpoint.
            :param port: The port value for the MongoDB source endpoint.
            :param secrets_manager_access_role_arn: The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` . The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the MongoDB endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both. For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the MongoDB endpoint connection details.
            :param server_name: The name of the server on the MongoDB source endpoint.
            :param username: The user name you use to access the MongoDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                mongo_db_settings_property = dms_mixins.CfnEndpointPropsMixin.MongoDbSettingsProperty(
                    auth_mechanism="authMechanism",
                    auth_source="authSource",
                    auth_type="authType",
                    database_name="databaseName",
                    docs_to_investigate="docsToInvestigate",
                    extract_doc_id="extractDocId",
                    nesting_level="nestingLevel",
                    password="password",
                    port=123,
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    server_name="serverName",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b68bffcca7c8aefbf679c9b7df010ec968c5c47bc2ea3b44d6ea6c12cb3d3224)
                check_type(argname="argument auth_mechanism", value=auth_mechanism, expected_type=type_hints["auth_mechanism"])
                check_type(argname="argument auth_source", value=auth_source, expected_type=type_hints["auth_source"])
                check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument docs_to_investigate", value=docs_to_investigate, expected_type=type_hints["docs_to_investigate"])
                check_type(argname="argument extract_doc_id", value=extract_doc_id, expected_type=type_hints["extract_doc_id"])
                check_type(argname="argument nesting_level", value=nesting_level, expected_type=type_hints["nesting_level"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_mechanism is not None:
                self._values["auth_mechanism"] = auth_mechanism
            if auth_source is not None:
                self._values["auth_source"] = auth_source
            if auth_type is not None:
                self._values["auth_type"] = auth_type
            if database_name is not None:
                self._values["database_name"] = database_name
            if docs_to_investigate is not None:
                self._values["docs_to_investigate"] = docs_to_investigate
            if extract_doc_id is not None:
                self._values["extract_doc_id"] = extract_doc_id
            if nesting_level is not None:
                self._values["nesting_level"] = nesting_level
            if password is not None:
                self._values["password"] = password
            if port is not None:
                self._values["port"] = port
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id
            if server_name is not None:
                self._values["server_name"] = server_name
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def auth_mechanism(self) -> typing.Optional[builtins.str]:
            '''The authentication mechanism you use to access the MongoDB source endpoint.

            For the default value, in MongoDB version 2.x, ``"default"`` is ``"mongodb_cr"`` . For MongoDB version 3.x or later, ``"default"`` is ``"scram_sha_1"`` . This setting isn't used when ``AuthType`` is set to ``"no"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-authmechanism
            '''
            result = self._values.get("auth_mechanism")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auth_source(self) -> typing.Optional[builtins.str]:
            '''The MongoDB database name. This setting isn't used when ``AuthType`` is set to ``"no"`` .

            The default is ``"admin"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-authsource
            '''
            result = self._values.get("auth_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auth_type(self) -> typing.Optional[builtins.str]:
            '''The authentication type you use to access the MongoDB source endpoint.

            When set to ``"no"`` , user name and password parameters are not used and can be empty.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-authtype
            '''
            result = self._values.get("auth_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The database name on the MongoDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def docs_to_investigate(self) -> typing.Optional[builtins.str]:
            '''Indicates the number of documents to preview to determine the document organization.

            Use this setting when ``NestingLevel`` is set to ``"one"`` .

            Must be a positive value greater than ``0`` . Default value is ``1000`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-docstoinvestigate
            '''
            result = self._values.get("docs_to_investigate")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def extract_doc_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the document ID. Use this setting when ``NestingLevel`` is set to ``"none"`` .

            Default value is ``"false"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-extractdocid
            '''
            result = self._values.get("extract_doc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nesting_level(self) -> typing.Optional[builtins.str]:
            '''Specifies either document or table mode.

            Default value is ``"none"`` . Specify ``"none"`` to use document mode. Specify ``"one"`` to use table mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-nestinglevel
            '''
            result = self._values.get("nesting_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password for the user account you use to access the MongoDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port value for the MongoDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` .

            The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the MongoDB endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both.

               For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the MongoDB endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''The name of the server on the MongoDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The user name you use to access the MongoDB source endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MongoDbSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.MySqlSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "after_connect_script": "afterConnectScript",
            "clean_source_metadata_on_mismatch": "cleanSourceMetadataOnMismatch",
            "events_poll_interval": "eventsPollInterval",
            "max_file_size": "maxFileSize",
            "parallel_load_threads": "parallelLoadThreads",
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_secret_id": "secretsManagerSecretId",
            "server_timezone": "serverTimezone",
            "target_db_type": "targetDbType",
        },
    )
    class MySqlSettingsProperty:
        def __init__(
            self,
            *,
            after_connect_script: typing.Optional[builtins.str] = None,
            clean_source_metadata_on_mismatch: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            events_poll_interval: typing.Optional[jsii.Number] = None,
            max_file_size: typing.Optional[jsii.Number] = None,
            parallel_load_threads: typing.Optional[jsii.Number] = None,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
            server_timezone: typing.Optional[builtins.str] = None,
            target_db_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a MySQL endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For information about other available settings, see `Extra connection attributes when using MySQL as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html#CHAP_Source.MySQL.ConnectionAttrib>`_ and `Extra connection attributes when using a MySQL-compatible database as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.MySQL.html#CHAP_Target.MySQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

            :param after_connect_script: Specifies a script to run immediately after AWS DMS connects to the endpoint. The migration task continues running regardless if the SQL statement succeeds or fails. For this parameter, provide the code of the script itself, not the name of a file containing the script.
            :param clean_source_metadata_on_mismatch: Cleans and recreates table metadata information on the replication instance when a mismatch occurs. For example, in a situation where running an alter DDL on the table could result in different information about the table cached in the replication instance.
            :param events_poll_interval: Specifies how often to check the binary log for new changes/events when the database is idle. The default is five seconds. Example: ``eventsPollInterval=5;`` In the example, AWS DMS checks for changes in the binary logs every five seconds.
            :param max_file_size: Specifies the maximum size (in KB) of any .csv file used to transfer data to a MySQL-compatible database. Example: ``maxFileSize=512``
            :param parallel_load_threads: Improves performance when loading data into the MySQL-compatible target database. Specifies how many threads to use to load the data into the MySQL-compatible target database. Setting a large number of threads can have an adverse effect on database performance, because a separate connection is required for each thread. The default is one. Example: ``parallelLoadThreads=1``
            :param secrets_manager_access_role_arn: The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` . The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the MySQL endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both. For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the MySQL endpoint connection details.
            :param server_timezone: Specifies the time zone for the source MySQL database. Example: ``serverTimezone=US/Pacific;`` Note: Do not enclose time zones in single quotes.
            :param target_db_type: Specifies where to migrate source tables on the target, either to a single database or multiple databases. If you specify ``SPECIFIC_DATABASE`` , specify the database name using the ``DatabaseName`` parameter of the ``Endpoint`` object. Example: ``targetDbType=MULTIPLE_DATABASES``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                my_sql_settings_property = dms_mixins.CfnEndpointPropsMixin.MySqlSettingsProperty(
                    after_connect_script="afterConnectScript",
                    clean_source_metadata_on_mismatch=False,
                    events_poll_interval=123,
                    max_file_size=123,
                    parallel_load_threads=123,
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    server_timezone="serverTimezone",
                    target_db_type="targetDbType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ae6efca6204480a1c37476798996ae31016343a2af917e34b2b9e1d677af2b2)
                check_type(argname="argument after_connect_script", value=after_connect_script, expected_type=type_hints["after_connect_script"])
                check_type(argname="argument clean_source_metadata_on_mismatch", value=clean_source_metadata_on_mismatch, expected_type=type_hints["clean_source_metadata_on_mismatch"])
                check_type(argname="argument events_poll_interval", value=events_poll_interval, expected_type=type_hints["events_poll_interval"])
                check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
                check_type(argname="argument parallel_load_threads", value=parallel_load_threads, expected_type=type_hints["parallel_load_threads"])
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
                check_type(argname="argument server_timezone", value=server_timezone, expected_type=type_hints["server_timezone"])
                check_type(argname="argument target_db_type", value=target_db_type, expected_type=type_hints["target_db_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if after_connect_script is not None:
                self._values["after_connect_script"] = after_connect_script
            if clean_source_metadata_on_mismatch is not None:
                self._values["clean_source_metadata_on_mismatch"] = clean_source_metadata_on_mismatch
            if events_poll_interval is not None:
                self._values["events_poll_interval"] = events_poll_interval
            if max_file_size is not None:
                self._values["max_file_size"] = max_file_size
            if parallel_load_threads is not None:
                self._values["parallel_load_threads"] = parallel_load_threads
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id
            if server_timezone is not None:
                self._values["server_timezone"] = server_timezone
            if target_db_type is not None:
                self._values["target_db_type"] = target_db_type

        @builtins.property
        def after_connect_script(self) -> typing.Optional[builtins.str]:
            '''Specifies a script to run immediately after AWS DMS connects to the endpoint.

            The migration task continues running regardless if the SQL statement succeeds or fails.

            For this parameter, provide the code of the script itself, not the name of a file containing the script.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-afterconnectscript
            '''
            result = self._values.get("after_connect_script")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def clean_source_metadata_on_mismatch(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Cleans and recreates table metadata information on the replication instance when a mismatch occurs.

            For example, in a situation where running an alter DDL on the table could result in different information about the table cached in the replication instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-cleansourcemetadataonmismatch
            '''
            result = self._values.get("clean_source_metadata_on_mismatch")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def events_poll_interval(self) -> typing.Optional[jsii.Number]:
            '''Specifies how often to check the binary log for new changes/events when the database is idle.

            The default is five seconds.

            Example: ``eventsPollInterval=5;``

            In the example, AWS DMS checks for changes in the binary logs every five seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-eventspollinterval
            '''
            result = self._values.get("events_poll_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_file_size(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum size (in KB) of any .csv file used to transfer data to a MySQL-compatible database.

            Example: ``maxFileSize=512``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-maxfilesize
            '''
            result = self._values.get("max_file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def parallel_load_threads(self) -> typing.Optional[jsii.Number]:
            '''Improves performance when loading data into the MySQL-compatible target database.

            Specifies how many threads to use to load the data into the MySQL-compatible target database. Setting a large number of threads can have an adverse effect on database performance, because a separate connection is required for each thread. The default is one.

            Example: ``parallelLoadThreads=1``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-parallelloadthreads
            '''
            result = self._values.get("parallel_load_threads")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` .

            The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the MySQL endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both.

               For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the MySQL endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_timezone(self) -> typing.Optional[builtins.str]:
            '''Specifies the time zone for the source MySQL database.

            Example: ``serverTimezone=US/Pacific;``

            Note: Do not enclose time zones in single quotes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-servertimezone
            '''
            result = self._values.get("server_timezone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_db_type(self) -> typing.Optional[builtins.str]:
            '''Specifies where to migrate source tables on the target, either to a single database or multiple databases.

            If you specify ``SPECIFIC_DATABASE`` , specify the database name using the ``DatabaseName`` parameter of the ``Endpoint`` object.

            Example: ``targetDbType=MULTIPLE_DATABASES``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-targetdbtype
            '''
            result = self._values.get("target_db_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MySqlSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.NeptuneSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "error_retry_duration": "errorRetryDuration",
            "iam_auth_enabled": "iamAuthEnabled",
            "max_file_size": "maxFileSize",
            "max_retry_count": "maxRetryCount",
            "s3_bucket_folder": "s3BucketFolder",
            "s3_bucket_name": "s3BucketName",
            "service_access_role_arn": "serviceAccessRoleArn",
        },
    )
    class NeptuneSettingsProperty:
        def __init__(
            self,
            *,
            error_retry_duration: typing.Optional[jsii.Number] = None,
            iam_auth_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_file_size: typing.Optional[jsii.Number] = None,
            max_retry_count: typing.Optional[jsii.Number] = None,
            s3_bucket_folder: typing.Optional[builtins.str] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
            service_access_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines an Amazon Neptune endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For more information about the available settings, see `Specifying endpoint settings for Amazon Neptune as a target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Neptune.html#CHAP_Target.Neptune.EndpointSettings>`_ in the *AWS Database Migration Service User Guide* .

            :param error_retry_duration: The number of milliseconds for AWS DMS to wait to retry a bulk-load of migrated graph data to the Neptune target database before raising an error. The default is 250.
            :param iam_auth_enabled: If you want IAM authorization enabled for this endpoint, set this parameter to ``true`` . Then attach the appropriate IAM policy document to your service role specified by ``ServiceAccessRoleArn`` . The default is ``false`` .
            :param max_file_size: The maximum size in kilobytes of migrated graph data stored in a .csv file before AWS DMS bulk-loads the data to the Neptune target database. The default is 1,048,576 KB. If the bulk load is successful, AWS DMS clears the bucket, ready to store the next batch of migrated graph data.
            :param max_retry_count: The number of times for AWS DMS to retry a bulk load of migrated graph data to the Neptune target database before raising an error. The default is 5.
            :param s3_bucket_folder: A folder path where you want AWS DMS to store migrated graph data in the S3 bucket specified by ``S3BucketName``.
            :param s3_bucket_name: The name of the Amazon S3 bucket where AWS DMS can temporarily store migrated graph data in .csv files before bulk-loading it to the Neptune target database. AWS DMS maps the SQL source data to graph data before storing it in these .csv files.
            :param service_access_role_arn: The Amazon Resource Name (ARN) of the service role that you created for the Neptune target endpoint. The role must allow the ``iam:PassRole`` action. For more information, see `Creating an IAM Service Role for Accessing Amazon Neptune as a Target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Neptune.html#CHAP_Target.Neptune.ServiceRole>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                neptune_settings_property = dms_mixins.CfnEndpointPropsMixin.NeptuneSettingsProperty(
                    error_retry_duration=123,
                    iam_auth_enabled=False,
                    max_file_size=123,
                    max_retry_count=123,
                    s3_bucket_folder="s3BucketFolder",
                    s3_bucket_name="s3BucketName",
                    service_access_role_arn="serviceAccessRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f5c0754c1d032f6e7f9a6fc7f4a62b88fd0cd938aaadd2ca1ff0f413af1c644e)
                check_type(argname="argument error_retry_duration", value=error_retry_duration, expected_type=type_hints["error_retry_duration"])
                check_type(argname="argument iam_auth_enabled", value=iam_auth_enabled, expected_type=type_hints["iam_auth_enabled"])
                check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
                check_type(argname="argument max_retry_count", value=max_retry_count, expected_type=type_hints["max_retry_count"])
                check_type(argname="argument s3_bucket_folder", value=s3_bucket_folder, expected_type=type_hints["s3_bucket_folder"])
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_retry_duration is not None:
                self._values["error_retry_duration"] = error_retry_duration
            if iam_auth_enabled is not None:
                self._values["iam_auth_enabled"] = iam_auth_enabled
            if max_file_size is not None:
                self._values["max_file_size"] = max_file_size
            if max_retry_count is not None:
                self._values["max_retry_count"] = max_retry_count
            if s3_bucket_folder is not None:
                self._values["s3_bucket_folder"] = s3_bucket_folder
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn

        @builtins.property
        def error_retry_duration(self) -> typing.Optional[jsii.Number]:
            '''The number of milliseconds for AWS DMS to wait to retry a bulk-load of migrated graph data to the Neptune target database before raising an error.

            The default is 250.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-errorretryduration
            '''
            result = self._values.get("error_retry_duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def iam_auth_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If you want IAM authorization enabled for this endpoint, set this parameter to ``true`` .

            Then attach the appropriate IAM policy document to your service role specified by ``ServiceAccessRoleArn`` . The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-iamauthenabled
            '''
            result = self._values.get("iam_auth_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_file_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum size in kilobytes of migrated graph data stored in a .csv file before AWS DMS bulk-loads the data to the Neptune target database. The default is 1,048,576 KB. If the bulk load is successful, AWS DMS clears the bucket, ready to store the next batch of migrated graph data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-maxfilesize
            '''
            result = self._values.get("max_file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_retry_count(self) -> typing.Optional[jsii.Number]:
            '''The number of times for AWS DMS to retry a bulk load of migrated graph data to the Neptune target database before raising an error.

            The default is 5.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-maxretrycount
            '''
            result = self._values.get("max_retry_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def s3_bucket_folder(self) -> typing.Optional[builtins.str]:
            '''A folder path where you want AWS DMS to store migrated graph data in the S3 bucket specified by ``S3BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-s3bucketfolder
            '''
            result = self._values.get("s3_bucket_folder")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket where AWS DMS can temporarily store migrated graph data in .csv files before bulk-loading it to the Neptune target database. AWS DMS maps the SQL source data to graph data before storing it in these .csv files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the service role that you created for the Neptune target endpoint.

            The role must allow the ``iam:PassRole`` action.

            For more information, see `Creating an IAM Service Role for Accessing Amazon Neptune as a Target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Neptune.html#CHAP_Target.Neptune.ServiceRole>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-serviceaccessrolearn
            '''
            result = self._values.get("service_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NeptuneSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.OracleSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_alternate_directly": "accessAlternateDirectly",
            "additional_archived_log_dest_id": "additionalArchivedLogDestId",
            "add_supplemental_logging": "addSupplementalLogging",
            "allow_select_nested_tables": "allowSelectNestedTables",
            "archived_log_dest_id": "archivedLogDestId",
            "archived_logs_only": "archivedLogsOnly",
            "asm_password": "asmPassword",
            "asm_server": "asmServer",
            "asm_user": "asmUser",
            "char_length_semantics": "charLengthSemantics",
            "direct_path_no_log": "directPathNoLog",
            "direct_path_parallel_load": "directPathParallelLoad",
            "enable_homogenous_tablespace": "enableHomogenousTablespace",
            "extra_archived_log_dest_ids": "extraArchivedLogDestIds",
            "fail_tasks_on_lob_truncation": "failTasksOnLobTruncation",
            "number_datatype_scale": "numberDatatypeScale",
            "oracle_path_prefix": "oraclePathPrefix",
            "parallel_asm_read_threads": "parallelAsmReadThreads",
            "read_ahead_blocks": "readAheadBlocks",
            "read_table_space_name": "readTableSpaceName",
            "replace_path_prefix": "replacePathPrefix",
            "retry_interval": "retryInterval",
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_oracle_asm_access_role_arn": "secretsManagerOracleAsmAccessRoleArn",
            "secrets_manager_oracle_asm_secret_id": "secretsManagerOracleAsmSecretId",
            "secrets_manager_secret_id": "secretsManagerSecretId",
            "security_db_encryption": "securityDbEncryption",
            "security_db_encryption_name": "securityDbEncryptionName",
            "spatial_data_option_to_geo_json_function_name": "spatialDataOptionToGeoJsonFunctionName",
            "standby_delay_time": "standbyDelayTime",
            "use_alternate_folder_for_online": "useAlternateFolderForOnline",
            "use_b_file": "useBFile",
            "use_direct_path_full_load": "useDirectPathFullLoad",
            "use_logminer_reader": "useLogminerReader",
            "use_path_prefix": "usePathPrefix",
        },
    )
    class OracleSettingsProperty:
        def __init__(
            self,
            *,
            access_alternate_directly: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            additional_archived_log_dest_id: typing.Optional[jsii.Number] = None,
            add_supplemental_logging: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            allow_select_nested_tables: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            archived_log_dest_id: typing.Optional[jsii.Number] = None,
            archived_logs_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            asm_password: typing.Optional[builtins.str] = None,
            asm_server: typing.Optional[builtins.str] = None,
            asm_user: typing.Optional[builtins.str] = None,
            char_length_semantics: typing.Optional[builtins.str] = None,
            direct_path_no_log: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            direct_path_parallel_load: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enable_homogenous_tablespace: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            extra_archived_log_dest_ids: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            fail_tasks_on_lob_truncation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            number_datatype_scale: typing.Optional[jsii.Number] = None,
            oracle_path_prefix: typing.Optional[builtins.str] = None,
            parallel_asm_read_threads: typing.Optional[jsii.Number] = None,
            read_ahead_blocks: typing.Optional[jsii.Number] = None,
            read_table_space_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            replace_path_prefix: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            retry_interval: typing.Optional[jsii.Number] = None,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_oracle_asm_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_oracle_asm_secret_id: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
            security_db_encryption: typing.Optional[builtins.str] = None,
            security_db_encryption_name: typing.Optional[builtins.str] = None,
            spatial_data_option_to_geo_json_function_name: typing.Optional[builtins.str] = None,
            standby_delay_time: typing.Optional[jsii.Number] = None,
            use_alternate_folder_for_online: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_b_file: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_direct_path_full_load: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_logminer_reader: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_path_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines an Oracle endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For information about other available settings, see `Extra connection attributes when using Oracle as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.ConnectionAttrib>`_ and `Extra connection attributes when using Oracle as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Oracle.html#CHAP_Target.Oracle.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

            :param access_alternate_directly: Set this attribute to ``false`` in order to use the Binary Reader to capture change data for an Amazon RDS for Oracle as the source. This tells the DMS instance to not access redo logs through any specified path prefix replacement using direct file access.
            :param additional_archived_log_dest_id: Set this attribute with ``ArchivedLogDestId`` in a primary/ standby setup. This attribute is useful in the case of a switchover. In this case, AWS DMS needs to know which destination to get archive redo logs from to read changes. This need arises because the previous primary instance is now a standby instance after switchover. Although AWS DMS supports the use of the Oracle ``RESETLOGS`` option to open the database, never use ``RESETLOGS`` unless necessary. For additional information about ``RESETLOGS`` , see `RMAN Data Repair Concepts <https://docs.aws.amazon.com/https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-data-repair-concepts.html#GUID-1805CCF7-4AF2-482D-B65A-998192F89C2B>`_ in the *Oracle Database Backup and Recovery User's Guide* .
            :param add_supplemental_logging: Set this attribute to set up table-level supplemental logging for the Oracle database. This attribute enables PRIMARY KEY supplemental logging on all tables selected for a migration task. If you use this option, you still need to enable database-level supplemental logging.
            :param allow_select_nested_tables: Set this attribute to ``true`` to enable replication of Oracle tables containing columns that are nested tables or defined types.
            :param archived_log_dest_id: Specifies the ID of the destination for the archived redo logs. This value should be the same as a number in the dest_id column of the v$archived_log view. If you work with an additional redo log destination, use the ``AdditionalArchivedLogDestId`` option to specify the additional destination ID. Doing this improves performance by ensuring that the correct logs are accessed from the outset.
            :param archived_logs_only: When this field is set to ``True`` , AWS DMS only accesses the archived redo logs. If the archived redo logs are stored on Automatic Storage Management (ASM) only, the AWS DMS user account needs to be granted ASM privileges.
            :param asm_password: For an Oracle source endpoint, your Oracle Automatic Storage Management (ASM) password. You can set this value from the ``*asm_user_password*`` value. You set this value as part of the comma-separated value that you set to the ``Password`` request parameter when you create the endpoint to access transaction logs using Binary Reader. For more information, see `Configuration for change data capture (CDC) on an Oracle source database <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC.Configuration>`_ .
            :param asm_server: For an Oracle source endpoint, your ASM server address. You can set this value from the ``asm_server`` value. You set ``asm_server`` as part of the extra connection attribute string to access an Oracle server with Binary Reader that uses ASM. For more information, see `Configuration for change data capture (CDC) on an Oracle source database <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC.Configuration>`_ .
            :param asm_user: For an Oracle source endpoint, your ASM user name. You can set this value from the ``asm_user`` value. You set ``asm_user`` as part of the extra connection attribute string to access an Oracle server with Binary Reader that uses ASM. For more information, see `Configuration for change data capture (CDC) on an Oracle source database <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC.Configuration>`_ .
            :param char_length_semantics: Specifies whether the length of a character column is in bytes or in characters. To indicate that the character column length is in characters, set this attribute to ``CHAR`` . Otherwise, the character column length is in bytes. Example: ``charLengthSemantics=CHAR;``
            :param direct_path_no_log: When set to ``true`` , this attribute helps to increase the commit rate on the Oracle target database by writing directly to tables and not writing a trail to database logs.
            :param direct_path_parallel_load: When set to ``true`` , this attribute specifies a parallel load when ``useDirectPathFullLoad`` is set to ``Y`` . This attribute also only applies when you use the AWS DMS parallel load feature. Note that the target table cannot have any constraints or indexes.
            :param enable_homogenous_tablespace: Set this attribute to enable homogenous tablespace replication and create existing tables or indexes under the same tablespace on the target.
            :param extra_archived_log_dest_ids: Specifies the IDs of one more destinations for one or more archived redo logs. These IDs are the values of the ``dest_id`` column in the ``v$archived_log`` view. Use this setting with the ``archivedLogDestId`` extra connection attribute in a primary-to-single setup or a primary-to-multiple-standby setup. This setting is useful in a switchover when you use an Oracle Data Guard database as a source. In this case, AWS DMS needs information about what destination to get archive redo logs from to read changes. AWS DMS needs this because after the switchover the previous primary is a standby instance. For example, in a primary-to-single standby setup you might apply the following settings. ``archivedLogDestId=1; ExtraArchivedLogDestIds=[2]`` In a primary-to-multiple-standby setup, you might apply the following settings. ``archivedLogDestId=1; ExtraArchivedLogDestIds=[2,3,4]`` Although AWS DMS supports the use of the Oracle ``RESETLOGS`` option to open the database, never use ``RESETLOGS`` unless it's necessary. For more information about ``RESETLOGS`` , see `RMAN Data Repair Concepts <https://docs.aws.amazon.com/https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-data-repair-concepts.html#GUID-1805CCF7-4AF2-482D-B65A-998192F89C2B>`_ in the *Oracle Database Backup and Recovery User's Guide* .
            :param fail_tasks_on_lob_truncation: When set to ``true`` , this attribute causes a task to fail if the actual size of an LOB column is greater than the specified ``LobMaxSize`` . If a task is set to limited LOB mode and this option is set to ``true`` , the task fails instead of truncating the LOB data.
            :param number_datatype_scale: Specifies the number scale. You can select a scale up to 38, or you can select FLOAT. By default, the NUMBER data type is converted to precision 38, scale 10. Example: ``numberDataTypeScale=12``
            :param oracle_path_prefix: Set this string attribute to the required value in order to use the Binary Reader to capture change data for an Amazon RDS for Oracle as the source. This value specifies the default Oracle root used to access the redo logs.
            :param parallel_asm_read_threads: Set this attribute to change the number of threads that DMS configures to perform a change data capture (CDC) load using Oracle Automatic Storage Management (ASM). You can specify an integer value between 2 (the default) and 8 (the maximum). Use this attribute together with the ``readAheadBlocks`` attribute.
            :param read_ahead_blocks: Set this attribute to change the number of read-ahead blocks that DMS configures to perform a change data capture (CDC) load using Oracle Automatic Storage Management (ASM). You can specify an integer value between 1000 (the default) and 200,000 (the maximum).
            :param read_table_space_name: When set to ``true`` , this attribute supports tablespace replication.
            :param replace_path_prefix: Set this attribute to true in order to use the Binary Reader to capture change data for an Amazon RDS for Oracle as the source. This setting tells DMS instance to replace the default Oracle root with the specified ``usePathPrefix`` setting to access the redo logs.
            :param retry_interval: Specifies the number of seconds that the system waits before resending a query. Example: ``retryInterval=6;``
            :param secrets_manager_access_role_arn: The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` . The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the Oracle endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both. For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_oracle_asm_access_role_arn: Required only if your Oracle endpoint uses Advanced Storage Manager (ASM). The full ARN of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the ``SecretsManagerOracleAsmSecret`` . This ``SecretsManagerOracleAsmSecret`` has the secret value that allows access to the Oracle ASM of the endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerOracleAsmSecretId`` . Or you can specify clear-text values for ``AsmUser`` , ``AsmPassword`` , and ``AsmServerName`` . You can't specify both. For more information on creating this ``SecretsManagerOracleAsmSecret`` , the corresponding ``SecretsManagerOracleAsmAccessRoleArn`` , and the ``SecretsManagerOracleAsmSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_oracle_asm_secret_id: Required only if your Oracle endpoint uses Advanced Storage Manager (ASM). The full ARN, partial ARN, or display name of the ``SecretsManagerOracleAsmSecret`` that contains the Oracle ASM connection details for the Oracle endpoint.
            :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the Oracle endpoint connection details.
            :param security_db_encryption: For an Oracle source endpoint, the transparent data encryption (TDE) password required by AWM DMS to access Oracle redo logs encrypted by TDE using Binary Reader. It is also the ``*TDE_Password*`` part of the comma-separated value you set to the ``Password`` request parameter when you create the endpoint. The ``SecurityDbEncryptian`` setting is related to this ``SecurityDbEncryptionName`` setting. For more information, see `Supported encryption methods for using Oracle as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.Encryption>`_ in the *AWS Database Migration Service User Guide* .
            :param security_db_encryption_name: For an Oracle source endpoint, the name of a key used for the transparent data encryption (TDE) of the columns and tablespaces in an Oracle source database that is encrypted using TDE. The key value is the value of the ``SecurityDbEncryption`` setting. For more information on setting the key name value of ``SecurityDbEncryptionName`` , see the information and example for setting the ``securityDbEncryptionName`` extra connection attribute in `Supported encryption methods for using Oracle as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.Encryption>`_ in the *AWS Database Migration Service User Guide* .
            :param spatial_data_option_to_geo_json_function_name: Use this attribute to convert ``SDO_GEOMETRY`` to ``GEOJSON`` format. By default, DMS calls the ``SDO2GEOJSON`` custom function if present and accessible. Or you can create your own custom function that mimics the operation of ``SDOGEOJSON`` and set ``SpatialDataOptionToGeoJsonFunctionName`` to call it instead.
            :param standby_delay_time: Use this attribute to specify a time in minutes for the delay in standby sync. If the source is an Oracle Active Data Guard standby database, use this attribute to specify the time lag between primary and standby databases. In AWS DMS , you can create an Oracle CDC task that uses an Active Data Guard standby instance as a source for replicating ongoing changes. Doing this eliminates the need to connect to an active database that might be in production.
            :param use_alternate_folder_for_online: Set this attribute to ``true`` in order to use the Binary Reader to capture change data for an Amazon RDS for Oracle as the source. This tells the DMS instance to use any specified prefix replacement to access all online redo logs.
            :param use_b_file: Set this attribute to True to capture change data using the Binary Reader utility. Set ``UseLogminerReader`` to False to set this attribute to True. To use Binary Reader with Amazon RDS for Oracle as the source, you set additional attributes. For more information about using this setting with Oracle Automatic Storage Management (ASM), see `Using Oracle LogMiner or AWS DMS Binary Reader for CDC <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC>`_ .
            :param use_direct_path_full_load: Set this attribute to True to have AWS DMS use a direct path full load. Specify this value to use the direct path protocol in the Oracle Call Interface (OCI). By using this OCI protocol, you can bulk-load Oracle target tables during a full load.
            :param use_logminer_reader: Set this attribute to True to capture change data using the Oracle LogMiner utility (the default). Set this attribute to False if you want to access the redo logs as a binary file. When you set ``UseLogminerReader`` to False, also set ``UseBfile`` to True. For more information on this setting and using Oracle ASM, see `Using Oracle LogMiner or AWS DMS Binary Reader for CDC <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC>`_ in the *AWS DMS User Guide* .
            :param use_path_prefix: Set this string attribute to the required value in order to use the Binary Reader to capture change data for an Amazon RDS for Oracle as the source. This value specifies the path prefix used to replace the default Oracle root to access the redo logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                oracle_settings_property = dms_mixins.CfnEndpointPropsMixin.OracleSettingsProperty(
                    access_alternate_directly=False,
                    additional_archived_log_dest_id=123,
                    add_supplemental_logging=False,
                    allow_select_nested_tables=False,
                    archived_log_dest_id=123,
                    archived_logs_only=False,
                    asm_password="asmPassword",
                    asm_server="asmServer",
                    asm_user="asmUser",
                    char_length_semantics="charLengthSemantics",
                    direct_path_no_log=False,
                    direct_path_parallel_load=False,
                    enable_homogenous_tablespace=False,
                    extra_archived_log_dest_ids=[123],
                    fail_tasks_on_lob_truncation=False,
                    number_datatype_scale=123,
                    oracle_path_prefix="oraclePathPrefix",
                    parallel_asm_read_threads=123,
                    read_ahead_blocks=123,
                    read_table_space_name=False,
                    replace_path_prefix=False,
                    retry_interval=123,
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_oracle_asm_access_role_arn="secretsManagerOracleAsmAccessRoleArn",
                    secrets_manager_oracle_asm_secret_id="secretsManagerOracleAsmSecretId",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    security_db_encryption="securityDbEncryption",
                    security_db_encryption_name="securityDbEncryptionName",
                    spatial_data_option_to_geo_json_function_name="spatialDataOptionToGeoJsonFunctionName",
                    standby_delay_time=123,
                    use_alternate_folder_for_online=False,
                    use_bFile=False,
                    use_direct_path_full_load=False,
                    use_logminer_reader=False,
                    use_path_prefix="usePathPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9ee298982a0f55d01a527bed6c28274b895389a6215139ead3e02c07cc98c18)
                check_type(argname="argument access_alternate_directly", value=access_alternate_directly, expected_type=type_hints["access_alternate_directly"])
                check_type(argname="argument additional_archived_log_dest_id", value=additional_archived_log_dest_id, expected_type=type_hints["additional_archived_log_dest_id"])
                check_type(argname="argument add_supplemental_logging", value=add_supplemental_logging, expected_type=type_hints["add_supplemental_logging"])
                check_type(argname="argument allow_select_nested_tables", value=allow_select_nested_tables, expected_type=type_hints["allow_select_nested_tables"])
                check_type(argname="argument archived_log_dest_id", value=archived_log_dest_id, expected_type=type_hints["archived_log_dest_id"])
                check_type(argname="argument archived_logs_only", value=archived_logs_only, expected_type=type_hints["archived_logs_only"])
                check_type(argname="argument asm_password", value=asm_password, expected_type=type_hints["asm_password"])
                check_type(argname="argument asm_server", value=asm_server, expected_type=type_hints["asm_server"])
                check_type(argname="argument asm_user", value=asm_user, expected_type=type_hints["asm_user"])
                check_type(argname="argument char_length_semantics", value=char_length_semantics, expected_type=type_hints["char_length_semantics"])
                check_type(argname="argument direct_path_no_log", value=direct_path_no_log, expected_type=type_hints["direct_path_no_log"])
                check_type(argname="argument direct_path_parallel_load", value=direct_path_parallel_load, expected_type=type_hints["direct_path_parallel_load"])
                check_type(argname="argument enable_homogenous_tablespace", value=enable_homogenous_tablespace, expected_type=type_hints["enable_homogenous_tablespace"])
                check_type(argname="argument extra_archived_log_dest_ids", value=extra_archived_log_dest_ids, expected_type=type_hints["extra_archived_log_dest_ids"])
                check_type(argname="argument fail_tasks_on_lob_truncation", value=fail_tasks_on_lob_truncation, expected_type=type_hints["fail_tasks_on_lob_truncation"])
                check_type(argname="argument number_datatype_scale", value=number_datatype_scale, expected_type=type_hints["number_datatype_scale"])
                check_type(argname="argument oracle_path_prefix", value=oracle_path_prefix, expected_type=type_hints["oracle_path_prefix"])
                check_type(argname="argument parallel_asm_read_threads", value=parallel_asm_read_threads, expected_type=type_hints["parallel_asm_read_threads"])
                check_type(argname="argument read_ahead_blocks", value=read_ahead_blocks, expected_type=type_hints["read_ahead_blocks"])
                check_type(argname="argument read_table_space_name", value=read_table_space_name, expected_type=type_hints["read_table_space_name"])
                check_type(argname="argument replace_path_prefix", value=replace_path_prefix, expected_type=type_hints["replace_path_prefix"])
                check_type(argname="argument retry_interval", value=retry_interval, expected_type=type_hints["retry_interval"])
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_oracle_asm_access_role_arn", value=secrets_manager_oracle_asm_access_role_arn, expected_type=type_hints["secrets_manager_oracle_asm_access_role_arn"])
                check_type(argname="argument secrets_manager_oracle_asm_secret_id", value=secrets_manager_oracle_asm_secret_id, expected_type=type_hints["secrets_manager_oracle_asm_secret_id"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
                check_type(argname="argument security_db_encryption", value=security_db_encryption, expected_type=type_hints["security_db_encryption"])
                check_type(argname="argument security_db_encryption_name", value=security_db_encryption_name, expected_type=type_hints["security_db_encryption_name"])
                check_type(argname="argument spatial_data_option_to_geo_json_function_name", value=spatial_data_option_to_geo_json_function_name, expected_type=type_hints["spatial_data_option_to_geo_json_function_name"])
                check_type(argname="argument standby_delay_time", value=standby_delay_time, expected_type=type_hints["standby_delay_time"])
                check_type(argname="argument use_alternate_folder_for_online", value=use_alternate_folder_for_online, expected_type=type_hints["use_alternate_folder_for_online"])
                check_type(argname="argument use_b_file", value=use_b_file, expected_type=type_hints["use_b_file"])
                check_type(argname="argument use_direct_path_full_load", value=use_direct_path_full_load, expected_type=type_hints["use_direct_path_full_load"])
                check_type(argname="argument use_logminer_reader", value=use_logminer_reader, expected_type=type_hints["use_logminer_reader"])
                check_type(argname="argument use_path_prefix", value=use_path_prefix, expected_type=type_hints["use_path_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_alternate_directly is not None:
                self._values["access_alternate_directly"] = access_alternate_directly
            if additional_archived_log_dest_id is not None:
                self._values["additional_archived_log_dest_id"] = additional_archived_log_dest_id
            if add_supplemental_logging is not None:
                self._values["add_supplemental_logging"] = add_supplemental_logging
            if allow_select_nested_tables is not None:
                self._values["allow_select_nested_tables"] = allow_select_nested_tables
            if archived_log_dest_id is not None:
                self._values["archived_log_dest_id"] = archived_log_dest_id
            if archived_logs_only is not None:
                self._values["archived_logs_only"] = archived_logs_only
            if asm_password is not None:
                self._values["asm_password"] = asm_password
            if asm_server is not None:
                self._values["asm_server"] = asm_server
            if asm_user is not None:
                self._values["asm_user"] = asm_user
            if char_length_semantics is not None:
                self._values["char_length_semantics"] = char_length_semantics
            if direct_path_no_log is not None:
                self._values["direct_path_no_log"] = direct_path_no_log
            if direct_path_parallel_load is not None:
                self._values["direct_path_parallel_load"] = direct_path_parallel_load
            if enable_homogenous_tablespace is not None:
                self._values["enable_homogenous_tablespace"] = enable_homogenous_tablespace
            if extra_archived_log_dest_ids is not None:
                self._values["extra_archived_log_dest_ids"] = extra_archived_log_dest_ids
            if fail_tasks_on_lob_truncation is not None:
                self._values["fail_tasks_on_lob_truncation"] = fail_tasks_on_lob_truncation
            if number_datatype_scale is not None:
                self._values["number_datatype_scale"] = number_datatype_scale
            if oracle_path_prefix is not None:
                self._values["oracle_path_prefix"] = oracle_path_prefix
            if parallel_asm_read_threads is not None:
                self._values["parallel_asm_read_threads"] = parallel_asm_read_threads
            if read_ahead_blocks is not None:
                self._values["read_ahead_blocks"] = read_ahead_blocks
            if read_table_space_name is not None:
                self._values["read_table_space_name"] = read_table_space_name
            if replace_path_prefix is not None:
                self._values["replace_path_prefix"] = replace_path_prefix
            if retry_interval is not None:
                self._values["retry_interval"] = retry_interval
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_oracle_asm_access_role_arn is not None:
                self._values["secrets_manager_oracle_asm_access_role_arn"] = secrets_manager_oracle_asm_access_role_arn
            if secrets_manager_oracle_asm_secret_id is not None:
                self._values["secrets_manager_oracle_asm_secret_id"] = secrets_manager_oracle_asm_secret_id
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id
            if security_db_encryption is not None:
                self._values["security_db_encryption"] = security_db_encryption
            if security_db_encryption_name is not None:
                self._values["security_db_encryption_name"] = security_db_encryption_name
            if spatial_data_option_to_geo_json_function_name is not None:
                self._values["spatial_data_option_to_geo_json_function_name"] = spatial_data_option_to_geo_json_function_name
            if standby_delay_time is not None:
                self._values["standby_delay_time"] = standby_delay_time
            if use_alternate_folder_for_online is not None:
                self._values["use_alternate_folder_for_online"] = use_alternate_folder_for_online
            if use_b_file is not None:
                self._values["use_b_file"] = use_b_file
            if use_direct_path_full_load is not None:
                self._values["use_direct_path_full_load"] = use_direct_path_full_load
            if use_logminer_reader is not None:
                self._values["use_logminer_reader"] = use_logminer_reader
            if use_path_prefix is not None:
                self._values["use_path_prefix"] = use_path_prefix

        @builtins.property
        def access_alternate_directly(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this attribute to ``false`` in order to use the Binary Reader to capture change data for an Amazon RDS for Oracle as the source.

            This tells the DMS instance to not access redo logs through any specified path prefix replacement using direct file access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-accessalternatedirectly
            '''
            result = self._values.get("access_alternate_directly")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def additional_archived_log_dest_id(self) -> typing.Optional[jsii.Number]:
            '''Set this attribute with ``ArchivedLogDestId`` in a primary/ standby setup.

            This attribute is useful in the case of a switchover. In this case, AWS DMS needs to know which destination to get archive redo logs from to read changes. This need arises because the previous primary instance is now a standby instance after switchover.

            Although AWS DMS supports the use of the Oracle ``RESETLOGS`` option to open the database, never use ``RESETLOGS`` unless necessary. For additional information about ``RESETLOGS`` , see `RMAN Data Repair Concepts <https://docs.aws.amazon.com/https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-data-repair-concepts.html#GUID-1805CCF7-4AF2-482D-B65A-998192F89C2B>`_ in the *Oracle Database Backup and Recovery User's Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-additionalarchivedlogdestid
            '''
            result = self._values.get("additional_archived_log_dest_id")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def add_supplemental_logging(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this attribute to set up table-level supplemental logging for the Oracle database.

            This attribute enables PRIMARY KEY supplemental logging on all tables selected for a migration task.

            If you use this option, you still need to enable database-level supplemental logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-addsupplementallogging
            '''
            result = self._values.get("add_supplemental_logging")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def allow_select_nested_tables(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this attribute to ``true`` to enable replication of Oracle tables containing columns that are nested tables or defined types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-allowselectnestedtables
            '''
            result = self._values.get("allow_select_nested_tables")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def archived_log_dest_id(self) -> typing.Optional[jsii.Number]:
            '''Specifies the ID of the destination for the archived redo logs.

            This value should be the same as a number in the dest_id column of the v$archived_log view. If you work with an additional redo log destination, use the ``AdditionalArchivedLogDestId`` option to specify the additional destination ID. Doing this improves performance by ensuring that the correct logs are accessed from the outset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-archivedlogdestid
            '''
            result = self._values.get("archived_log_dest_id")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def archived_logs_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When this field is set to ``True`` , AWS DMS only accesses the archived redo logs.

            If the archived redo logs are stored on Automatic Storage Management (ASM) only, the AWS DMS user account needs to be granted ASM privileges.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-archivedlogsonly
            '''
            result = self._values.get("archived_logs_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def asm_password(self) -> typing.Optional[builtins.str]:
            '''For an Oracle source endpoint, your Oracle Automatic Storage Management (ASM) password.

            You can set this value from the ``*asm_user_password*`` value. You set this value as part of the comma-separated value that you set to the ``Password`` request parameter when you create the endpoint to access transaction logs using Binary Reader. For more information, see `Configuration for change data capture (CDC) on an Oracle source database <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC.Configuration>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-asmpassword
            '''
            result = self._values.get("asm_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def asm_server(self) -> typing.Optional[builtins.str]:
            '''For an Oracle source endpoint, your ASM server address.

            You can set this value from the ``asm_server`` value. You set ``asm_server`` as part of the extra connection attribute string to access an Oracle server with Binary Reader that uses ASM. For more information, see `Configuration for change data capture (CDC) on an Oracle source database <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC.Configuration>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-asmserver
            '''
            result = self._values.get("asm_server")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def asm_user(self) -> typing.Optional[builtins.str]:
            '''For an Oracle source endpoint, your ASM user name.

            You can set this value from the ``asm_user`` value. You set ``asm_user`` as part of the extra connection attribute string to access an Oracle server with Binary Reader that uses ASM. For more information, see `Configuration for change data capture (CDC) on an Oracle source database <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC.Configuration>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-asmuser
            '''
            result = self._values.get("asm_user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def char_length_semantics(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the length of a character column is in bytes or in characters.

            To indicate that the character column length is in characters, set this attribute to ``CHAR`` . Otherwise, the character column length is in bytes.

            Example: ``charLengthSemantics=CHAR;``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-charlengthsemantics
            '''
            result = self._values.get("char_length_semantics")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def direct_path_no_log(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to ``true`` , this attribute helps to increase the commit rate on the Oracle target database by writing directly to tables and not writing a trail to database logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-directpathnolog
            '''
            result = self._values.get("direct_path_no_log")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def direct_path_parallel_load(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to ``true`` , this attribute specifies a parallel load when ``useDirectPathFullLoad`` is set to ``Y`` .

            This attribute also only applies when you use the AWS DMS parallel load feature. Note that the target table cannot have any constraints or indexes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-directpathparallelload
            '''
            result = self._values.get("direct_path_parallel_load")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_homogenous_tablespace(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this attribute to enable homogenous tablespace replication and create existing tables or indexes under the same tablespace on the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-enablehomogenoustablespace
            '''
            result = self._values.get("enable_homogenous_tablespace")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def extra_archived_log_dest_ids(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies the IDs of one more destinations for one or more archived redo logs.

            These IDs are the values of the ``dest_id`` column in the ``v$archived_log`` view. Use this setting with the ``archivedLogDestId`` extra connection attribute in a primary-to-single setup or a primary-to-multiple-standby setup.

            This setting is useful in a switchover when you use an Oracle Data Guard database as a source. In this case, AWS DMS needs information about what destination to get archive redo logs from to read changes. AWS DMS needs this because after the switchover the previous primary is a standby instance. For example, in a primary-to-single standby setup you might apply the following settings.

            ``archivedLogDestId=1; ExtraArchivedLogDestIds=[2]``

            In a primary-to-multiple-standby setup, you might apply the following settings.

            ``archivedLogDestId=1; ExtraArchivedLogDestIds=[2,3,4]``

            Although AWS DMS supports the use of the Oracle ``RESETLOGS`` option to open the database, never use ``RESETLOGS`` unless it's necessary. For more information about ``RESETLOGS`` , see `RMAN Data Repair Concepts <https://docs.aws.amazon.com/https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-data-repair-concepts.html#GUID-1805CCF7-4AF2-482D-B65A-998192F89C2B>`_ in the *Oracle Database Backup and Recovery User's Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-extraarchivedlogdestids
            '''
            result = self._values.get("extra_archived_log_dest_ids")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def fail_tasks_on_lob_truncation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to ``true`` , this attribute causes a task to fail if the actual size of an LOB column is greater than the specified ``LobMaxSize`` .

            If a task is set to limited LOB mode and this option is set to ``true`` , the task fails instead of truncating the LOB data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-failtasksonlobtruncation
            '''
            result = self._values.get("fail_tasks_on_lob_truncation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def number_datatype_scale(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number scale.

            You can select a scale up to 38, or you can select FLOAT. By default, the NUMBER data type is converted to precision 38, scale 10.

            Example: ``numberDataTypeScale=12``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-numberdatatypescale
            '''
            result = self._values.get("number_datatype_scale")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def oracle_path_prefix(self) -> typing.Optional[builtins.str]:
            '''Set this string attribute to the required value in order to use the Binary Reader to capture change data for an Amazon RDS for Oracle as the source.

            This value specifies the default Oracle root used to access the redo logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-oraclepathprefix
            '''
            result = self._values.get("oracle_path_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parallel_asm_read_threads(self) -> typing.Optional[jsii.Number]:
            '''Set this attribute to change the number of threads that DMS configures to perform a change data capture (CDC) load using Oracle Automatic Storage Management (ASM).

            You can specify an integer value between 2 (the default) and 8 (the maximum). Use this attribute together with the ``readAheadBlocks`` attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-parallelasmreadthreads
            '''
            result = self._values.get("parallel_asm_read_threads")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def read_ahead_blocks(self) -> typing.Optional[jsii.Number]:
            '''Set this attribute to change the number of read-ahead blocks that DMS configures to perform a change data capture (CDC) load using Oracle Automatic Storage Management (ASM).

            You can specify an integer value between 1000 (the default) and 200,000 (the maximum).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-readaheadblocks
            '''
            result = self._values.get("read_ahead_blocks")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def read_table_space_name(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to ``true`` , this attribute supports tablespace replication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-readtablespacename
            '''
            result = self._values.get("read_table_space_name")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def replace_path_prefix(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this attribute to true in order to use the Binary Reader to capture change data for an Amazon RDS for Oracle as the source.

            This setting tells DMS instance to replace the default Oracle root with the specified ``usePathPrefix`` setting to access the redo logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-replacepathprefix
            '''
            result = self._values.get("replace_path_prefix")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def retry_interval(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of seconds that the system waits before resending a query.

            Example: ``retryInterval=6;``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-retryinterval
            '''
            result = self._values.get("retry_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` .

            The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the Oracle endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both.

               For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_oracle_asm_access_role_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''Required only if your Oracle endpoint uses Advanced Storage Manager (ASM).

            The full ARN of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the ``SecretsManagerOracleAsmSecret`` . This ``SecretsManagerOracleAsmSecret`` has the secret value that allows access to the Oracle ASM of the endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerOracleAsmSecretId`` . Or you can specify clear-text values for ``AsmUser`` , ``AsmPassword`` , and ``AsmServerName`` . You can't specify both.

               For more information on creating this ``SecretsManagerOracleAsmSecret`` , the corresponding ``SecretsManagerOracleAsmAccessRoleArn`` , and the ``SecretsManagerOracleAsmSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-secretsmanageroracleasmaccessrolearn
            '''
            result = self._values.get("secrets_manager_oracle_asm_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_oracle_asm_secret_id(self) -> typing.Optional[builtins.str]:
            '''Required only if your Oracle endpoint uses Advanced Storage Manager (ASM).

            The full ARN, partial ARN, or display name of the ``SecretsManagerOracleAsmSecret`` that contains the Oracle ASM connection details for the Oracle endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-secretsmanageroracleasmsecretid
            '''
            result = self._values.get("secrets_manager_oracle_asm_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the Oracle endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_db_encryption(self) -> typing.Optional[builtins.str]:
            '''For an Oracle source endpoint, the transparent data encryption (TDE) password required by AWM DMS to access Oracle redo logs encrypted by TDE using Binary Reader.

            It is also the ``*TDE_Password*`` part of the comma-separated value you set to the ``Password`` request parameter when you create the endpoint. The ``SecurityDbEncryptian`` setting is related to this ``SecurityDbEncryptionName`` setting. For more information, see `Supported encryption methods for using Oracle as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.Encryption>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-securitydbencryption
            '''
            result = self._values.get("security_db_encryption")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_db_encryption_name(self) -> typing.Optional[builtins.str]:
            '''For an Oracle source endpoint, the name of a key used for the transparent data encryption (TDE) of the columns and tablespaces in an Oracle source database that is encrypted using TDE.

            The key value is the value of the ``SecurityDbEncryption`` setting. For more information on setting the key name value of ``SecurityDbEncryptionName`` , see the information and example for setting the ``securityDbEncryptionName`` extra connection attribute in `Supported encryption methods for using Oracle as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.Encryption>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-securitydbencryptionname
            '''
            result = self._values.get("security_db_encryption_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def spatial_data_option_to_geo_json_function_name(
            self,
        ) -> typing.Optional[builtins.str]:
            '''Use this attribute to convert ``SDO_GEOMETRY`` to ``GEOJSON`` format.

            By default, DMS calls the ``SDO2GEOJSON`` custom function if present and accessible. Or you can create your own custom function that mimics the operation of ``SDOGEOJSON`` and set ``SpatialDataOptionToGeoJsonFunctionName`` to call it instead.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-spatialdataoptiontogeojsonfunctionname
            '''
            result = self._values.get("spatial_data_option_to_geo_json_function_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def standby_delay_time(self) -> typing.Optional[jsii.Number]:
            '''Use this attribute to specify a time in minutes for the delay in standby sync.

            If the source is an Oracle Active Data Guard standby database, use this attribute to specify the time lag between primary and standby databases.

            In AWS DMS , you can create an Oracle CDC task that uses an Active Data Guard standby instance as a source for replicating ongoing changes. Doing this eliminates the need to connect to an active database that might be in production.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-standbydelaytime
            '''
            result = self._values.get("standby_delay_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def use_alternate_folder_for_online(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this attribute to ``true`` in order to use the Binary Reader to capture change data for an Amazon RDS for Oracle as the source.

            This tells the DMS instance to use any specified prefix replacement to access all online redo logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-usealternatefolderforonline
            '''
            result = self._values.get("use_alternate_folder_for_online")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_b_file(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this attribute to True to capture change data using the Binary Reader utility.

            Set ``UseLogminerReader`` to False to set this attribute to True. To use Binary Reader with Amazon RDS for Oracle as the source, you set additional attributes. For more information about using this setting with Oracle Automatic Storage Management (ASM), see `Using Oracle LogMiner or AWS DMS Binary Reader for CDC <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-usebfile
            '''
            result = self._values.get("use_b_file")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_direct_path_full_load(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this attribute to True to have AWS DMS use a direct path full load.

            Specify this value to use the direct path protocol in the Oracle Call Interface (OCI). By using this OCI protocol, you can bulk-load Oracle target tables during a full load.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-usedirectpathfullload
            '''
            result = self._values.get("use_direct_path_full_load")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_logminer_reader(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this attribute to True to capture change data using the Oracle LogMiner utility (the default).

            Set this attribute to False if you want to access the redo logs as a binary file. When you set ``UseLogminerReader`` to False, also set ``UseBfile`` to True. For more information on this setting and using Oracle ASM, see `Using Oracle LogMiner or AWS DMS Binary Reader for CDC <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.Oracle.html#CHAP_Source.Oracle.CDC>`_ in the *AWS DMS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-uselogminerreader
            '''
            result = self._values.get("use_logminer_reader")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_path_prefix(self) -> typing.Optional[builtins.str]:
            '''Set this string attribute to the required value in order to use the Binary Reader to capture change data for an Amazon RDS for Oracle as the source.

            This value specifies the path prefix used to replace the default Oracle root to access the redo logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-oraclesettings.html#cfn-dms-endpoint-oraclesettings-usepathprefix
            '''
            result = self._values.get("use_path_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OracleSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.PostgreSqlSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "after_connect_script": "afterConnectScript",
            "babelfish_database_name": "babelfishDatabaseName",
            "capture_ddls": "captureDdls",
            "database_mode": "databaseMode",
            "ddl_artifacts_schema": "ddlArtifactsSchema",
            "execute_timeout": "executeTimeout",
            "fail_tasks_on_lob_truncation": "failTasksOnLobTruncation",
            "heartbeat_enable": "heartbeatEnable",
            "heartbeat_frequency": "heartbeatFrequency",
            "heartbeat_schema": "heartbeatSchema",
            "map_boolean_as_boolean": "mapBooleanAsBoolean",
            "max_file_size": "maxFileSize",
            "plugin_name": "pluginName",
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_secret_id": "secretsManagerSecretId",
            "slot_name": "slotName",
        },
    )
    class PostgreSqlSettingsProperty:
        def __init__(
            self,
            *,
            after_connect_script: typing.Optional[builtins.str] = None,
            babelfish_database_name: typing.Optional[builtins.str] = None,
            capture_ddls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            database_mode: typing.Optional[builtins.str] = None,
            ddl_artifacts_schema: typing.Optional[builtins.str] = None,
            execute_timeout: typing.Optional[jsii.Number] = None,
            fail_tasks_on_lob_truncation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            heartbeat_enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            heartbeat_frequency: typing.Optional[jsii.Number] = None,
            heartbeat_schema: typing.Optional[builtins.str] = None,
            map_boolean_as_boolean: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_file_size: typing.Optional[jsii.Number] = None,
            plugin_name: typing.Optional[builtins.str] = None,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
            slot_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a PostgreSQL endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For information about other available settings, see `Extra connection attributes when using PostgreSQL as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.PostgreSQL.html#CHAP_Source.PostgreSQL.ConnectionAttrib>`_ and `Extra connection attributes when using PostgreSQL as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.PostgreSQL.html#CHAP_Target.PostgreSQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

            :param after_connect_script: For use with change data capture (CDC) only, this attribute has AWS DMS bypass foreign keys and user triggers to reduce the time it takes to bulk load data. Example: ``afterConnectScript=SET session_replication_role='replica'``
            :param babelfish_database_name: The Babelfish for Aurora PostgreSQL database name for the endpoint.
            :param capture_ddls: To capture DDL events, AWS DMS creates various artifacts in the PostgreSQL database when the task starts. You can later remove these artifacts. If this value is set to ``True`` , you don't have to create tables or triggers on the source database.
            :param database_mode: Specifies the default behavior of the replication's handling of PostgreSQL- compatible endpoints that require some additional configuration, such as Babelfish endpoints.
            :param ddl_artifacts_schema: The schema in which the operational DDL database artifacts are created. The default value is ``public`` . Example: ``ddlArtifactsSchema=xyzddlschema;``
            :param execute_timeout: Sets the client statement timeout for the PostgreSQL instance, in seconds. The default value is 60 seconds. Example: ``executeTimeout=100;``
            :param fail_tasks_on_lob_truncation: When set to ``true`` , this value causes a task to fail if the actual size of a LOB column is greater than the specified ``LobMaxSize`` . The default value is ``false`` . If task is set to Limited LOB mode and this option is set to true, the task fails instead of truncating the LOB data.
            :param heartbeat_enable: The write-ahead log (WAL) heartbeat feature mimics a dummy transaction. By doing this, it prevents idle logical replication slots from holding onto old WAL logs, which can result in storage full situations on the source. This heartbeat keeps ``restart_lsn`` moving and prevents storage full scenarios. The default value is ``false`` .
            :param heartbeat_frequency: Sets the WAL heartbeat frequency (in minutes). The default value is 5 minutes.
            :param heartbeat_schema: Sets the schema in which the heartbeat artifacts are created. The default value is ``public`` .
            :param map_boolean_as_boolean: When true, lets PostgreSQL migrate the boolean type as boolean. By default, PostgreSQL migrates booleans as ``varchar(5)`` . You must set this setting on both the source and target endpoints for it to take effect. The default value is ``false`` .
            :param max_file_size: Specifies the maximum size (in KB) of any .csv file used to transfer data to PostgreSQL. The default value is 32,768 KB (32 MB). Example: ``maxFileSize=512``
            :param plugin_name: Specifies the plugin to use to create a replication slot. The default value is ``pglogical`` .
            :param secrets_manager_access_role_arn: The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` . The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the PostgreSQL endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both. For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the PostgreSQL endpoint connection details.
            :param slot_name: Sets the name of a previously created logical replication slot for a change data capture (CDC) load of the PostgreSQL source instance. When used with the ``CdcStartPosition`` request parameter for the AWS DMS API , this attribute also makes it possible to use native CDC start points. DMS verifies that the specified logical replication slot exists before starting the CDC load task. It also verifies that the task was created with a valid setting of ``CdcStartPosition`` . If the specified slot doesn't exist or the task doesn't have a valid ``CdcStartPosition`` setting, DMS raises an error. For more information about setting the ``CdcStartPosition`` request parameter, see `Determining a CDC native start point <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html#CHAP_Task.CDC.StartPoint.Native>`_ in the *AWS Database Migration Service User Guide* . For more information about using ``CdcStartPosition`` , see `CreateReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_CreateReplicationTask.html>`_ , `StartReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_StartReplicationTask.html>`_ , and `ModifyReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_ModifyReplicationTask.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                postgre_sql_settings_property = dms_mixins.CfnEndpointPropsMixin.PostgreSqlSettingsProperty(
                    after_connect_script="afterConnectScript",
                    babelfish_database_name="babelfishDatabaseName",
                    capture_ddls=False,
                    database_mode="databaseMode",
                    ddl_artifacts_schema="ddlArtifactsSchema",
                    execute_timeout=123,
                    fail_tasks_on_lob_truncation=False,
                    heartbeat_enable=False,
                    heartbeat_frequency=123,
                    heartbeat_schema="heartbeatSchema",
                    map_boolean_as_boolean=False,
                    max_file_size=123,
                    plugin_name="pluginName",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    slot_name="slotName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db0af8162afce6a0df408d4194bc26145faa2ea14b9a2339c425b1e2ddd859bc)
                check_type(argname="argument after_connect_script", value=after_connect_script, expected_type=type_hints["after_connect_script"])
                check_type(argname="argument babelfish_database_name", value=babelfish_database_name, expected_type=type_hints["babelfish_database_name"])
                check_type(argname="argument capture_ddls", value=capture_ddls, expected_type=type_hints["capture_ddls"])
                check_type(argname="argument database_mode", value=database_mode, expected_type=type_hints["database_mode"])
                check_type(argname="argument ddl_artifacts_schema", value=ddl_artifacts_schema, expected_type=type_hints["ddl_artifacts_schema"])
                check_type(argname="argument execute_timeout", value=execute_timeout, expected_type=type_hints["execute_timeout"])
                check_type(argname="argument fail_tasks_on_lob_truncation", value=fail_tasks_on_lob_truncation, expected_type=type_hints["fail_tasks_on_lob_truncation"])
                check_type(argname="argument heartbeat_enable", value=heartbeat_enable, expected_type=type_hints["heartbeat_enable"])
                check_type(argname="argument heartbeat_frequency", value=heartbeat_frequency, expected_type=type_hints["heartbeat_frequency"])
                check_type(argname="argument heartbeat_schema", value=heartbeat_schema, expected_type=type_hints["heartbeat_schema"])
                check_type(argname="argument map_boolean_as_boolean", value=map_boolean_as_boolean, expected_type=type_hints["map_boolean_as_boolean"])
                check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
                check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
                check_type(argname="argument slot_name", value=slot_name, expected_type=type_hints["slot_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if after_connect_script is not None:
                self._values["after_connect_script"] = after_connect_script
            if babelfish_database_name is not None:
                self._values["babelfish_database_name"] = babelfish_database_name
            if capture_ddls is not None:
                self._values["capture_ddls"] = capture_ddls
            if database_mode is not None:
                self._values["database_mode"] = database_mode
            if ddl_artifacts_schema is not None:
                self._values["ddl_artifacts_schema"] = ddl_artifacts_schema
            if execute_timeout is not None:
                self._values["execute_timeout"] = execute_timeout
            if fail_tasks_on_lob_truncation is not None:
                self._values["fail_tasks_on_lob_truncation"] = fail_tasks_on_lob_truncation
            if heartbeat_enable is not None:
                self._values["heartbeat_enable"] = heartbeat_enable
            if heartbeat_frequency is not None:
                self._values["heartbeat_frequency"] = heartbeat_frequency
            if heartbeat_schema is not None:
                self._values["heartbeat_schema"] = heartbeat_schema
            if map_boolean_as_boolean is not None:
                self._values["map_boolean_as_boolean"] = map_boolean_as_boolean
            if max_file_size is not None:
                self._values["max_file_size"] = max_file_size
            if plugin_name is not None:
                self._values["plugin_name"] = plugin_name
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id
            if slot_name is not None:
                self._values["slot_name"] = slot_name

        @builtins.property
        def after_connect_script(self) -> typing.Optional[builtins.str]:
            '''For use with change data capture (CDC) only, this attribute has AWS DMS bypass foreign keys and user triggers to reduce the time it takes to bulk load data.

            Example: ``afterConnectScript=SET session_replication_role='replica'``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-afterconnectscript
            '''
            result = self._values.get("after_connect_script")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def babelfish_database_name(self) -> typing.Optional[builtins.str]:
            '''The Babelfish for Aurora PostgreSQL database name for the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-babelfishdatabasename
            '''
            result = self._values.get("babelfish_database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capture_ddls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''To capture DDL events, AWS DMS creates various artifacts in the PostgreSQL database when the task starts.

            You can later remove these artifacts.

            If this value is set to ``True`` , you don't have to create tables or triggers on the source database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-captureddls
            '''
            result = self._values.get("capture_ddls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def database_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies the default behavior of the replication's handling of PostgreSQL- compatible endpoints that require some additional configuration, such as Babelfish endpoints.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-databasemode
            '''
            result = self._values.get("database_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ddl_artifacts_schema(self) -> typing.Optional[builtins.str]:
            '''The schema in which the operational DDL database artifacts are created.

            The default value is ``public`` .

            Example: ``ddlArtifactsSchema=xyzddlschema;``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-ddlartifactsschema
            '''
            result = self._values.get("ddl_artifacts_schema")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def execute_timeout(self) -> typing.Optional[jsii.Number]:
            '''Sets the client statement timeout for the PostgreSQL instance, in seconds. The default value is 60 seconds.

            Example: ``executeTimeout=100;``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-executetimeout
            '''
            result = self._values.get("execute_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def fail_tasks_on_lob_truncation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to ``true`` , this value causes a task to fail if the actual size of a LOB column is greater than the specified ``LobMaxSize`` .

            The default value is ``false`` .

            If task is set to Limited LOB mode and this option is set to true, the task fails instead of truncating the LOB data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-failtasksonlobtruncation
            '''
            result = self._values.get("fail_tasks_on_lob_truncation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def heartbeat_enable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The write-ahead log (WAL) heartbeat feature mimics a dummy transaction.

            By doing this, it prevents idle logical replication slots from holding onto old WAL logs, which can result in storage full situations on the source. This heartbeat keeps ``restart_lsn`` moving and prevents storage full scenarios.

            The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-heartbeatenable
            '''
            result = self._values.get("heartbeat_enable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def heartbeat_frequency(self) -> typing.Optional[jsii.Number]:
            '''Sets the WAL heartbeat frequency (in minutes).

            The default value is 5 minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-heartbeatfrequency
            '''
            result = self._values.get("heartbeat_frequency")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def heartbeat_schema(self) -> typing.Optional[builtins.str]:
            '''Sets the schema in which the heartbeat artifacts are created.

            The default value is ``public`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-heartbeatschema
            '''
            result = self._values.get("heartbeat_schema")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def map_boolean_as_boolean(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true, lets PostgreSQL migrate the boolean type as boolean.

            By default, PostgreSQL migrates booleans as ``varchar(5)`` . You must set this setting on both the source and target endpoints for it to take effect.

            The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-mapbooleanasboolean
            '''
            result = self._values.get("map_boolean_as_boolean")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_file_size(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum size (in KB) of any .csv file used to transfer data to PostgreSQL.

            The default value is 32,768 KB (32 MB).

            Example: ``maxFileSize=512``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-maxfilesize
            '''
            result = self._values.get("max_file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def plugin_name(self) -> typing.Optional[builtins.str]:
            '''Specifies the plugin to use to create a replication slot.

            The default value is ``pglogical`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-pluginname
            '''
            result = self._values.get("plugin_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` .

            The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the PostgreSQL endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both.

               For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the PostgreSQL endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slot_name(self) -> typing.Optional[builtins.str]:
            '''Sets the name of a previously created logical replication slot for a change data capture (CDC) load of the PostgreSQL source instance.

            When used with the ``CdcStartPosition`` request parameter for the AWS DMS API , this attribute also makes it possible to use native CDC start points. DMS verifies that the specified logical replication slot exists before starting the CDC load task. It also verifies that the task was created with a valid setting of ``CdcStartPosition`` . If the specified slot doesn't exist or the task doesn't have a valid ``CdcStartPosition`` setting, DMS raises an error.

            For more information about setting the ``CdcStartPosition`` request parameter, see `Determining a CDC native start point <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html#CHAP_Task.CDC.StartPoint.Native>`_ in the *AWS Database Migration Service User Guide* . For more information about using ``CdcStartPosition`` , see `CreateReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_CreateReplicationTask.html>`_ , `StartReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_StartReplicationTask.html>`_ , and `ModifyReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_ModifyReplicationTask.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-slotname
            '''
            result = self._values.get("slot_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PostgreSqlSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.RedisSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_password": "authPassword",
            "auth_type": "authType",
            "auth_user_name": "authUserName",
            "port": "port",
            "server_name": "serverName",
            "ssl_ca_certificate_arn": "sslCaCertificateArn",
            "ssl_security_protocol": "sslSecurityProtocol",
        },
    )
    class RedisSettingsProperty:
        def __init__(
            self,
            *,
            auth_password: typing.Optional[builtins.str] = None,
            auth_type: typing.Optional[builtins.str] = None,
            auth_user_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
            ssl_ca_certificate_arn: typing.Optional[builtins.str] = None,
            ssl_security_protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a Redis target endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For information about other available settings, see `Specifying endpoint settings for Redis as a target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Redis.html#CHAP_Target.Redis.EndpointSettings>`_ in the *AWS Database Migration Service User Guide* .

            :param auth_password: The password provided with the ``auth-role`` and ``auth-token`` options of the ``AuthType`` setting for a Redis target endpoint.
            :param auth_type: The type of authentication to perform when connecting to a Redis target. Options include ``none`` , ``auth-token`` , and ``auth-role`` . The ``auth-token`` option requires an ``AuthPassword`` value to be provided. The ``auth-role`` option requires ``AuthUserName`` and ``AuthPassword`` values to be provided.
            :param auth_user_name: The user name provided with the ``auth-role`` option of the ``AuthType`` setting for a Redis target endpoint.
            :param port: Transmission Control Protocol (TCP) port for the endpoint.
            :param server_name: Fully qualified domain name of the endpoint.
            :param ssl_ca_certificate_arn: The Amazon Resource Name (ARN) for the certificate authority (CA) that DMS uses to connect to your Redis target endpoint.
            :param ssl_security_protocol: The connection to a Redis target endpoint using Transport Layer Security (TLS). Valid values include ``plaintext`` and ``ssl-encryption`` . The default is ``ssl-encryption`` . The ``ssl-encryption`` option makes an encrypted connection. Optionally, you can identify an Amazon Resource Name (ARN) for an SSL certificate authority (CA) using the ``SslCaCertificateArn`` setting. If an ARN isn't given for a CA, DMS uses the Amazon root CA. The ``plaintext`` option doesn't provide Transport Layer Security (TLS) encryption for traffic between endpoint and database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redissettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                redis_settings_property = dms_mixins.CfnEndpointPropsMixin.RedisSettingsProperty(
                    auth_password="authPassword",
                    auth_type="authType",
                    auth_user_name="authUserName",
                    port=123,
                    server_name="serverName",
                    ssl_ca_certificate_arn="sslCaCertificateArn",
                    ssl_security_protocol="sslSecurityProtocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a38b261c2578534b7a4157f2c20ddccdc463b805e639406be3961938c38d28d4)
                check_type(argname="argument auth_password", value=auth_password, expected_type=type_hints["auth_password"])
                check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
                check_type(argname="argument auth_user_name", value=auth_user_name, expected_type=type_hints["auth_user_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
                check_type(argname="argument ssl_ca_certificate_arn", value=ssl_ca_certificate_arn, expected_type=type_hints["ssl_ca_certificate_arn"])
                check_type(argname="argument ssl_security_protocol", value=ssl_security_protocol, expected_type=type_hints["ssl_security_protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_password is not None:
                self._values["auth_password"] = auth_password
            if auth_type is not None:
                self._values["auth_type"] = auth_type
            if auth_user_name is not None:
                self._values["auth_user_name"] = auth_user_name
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name
            if ssl_ca_certificate_arn is not None:
                self._values["ssl_ca_certificate_arn"] = ssl_ca_certificate_arn
            if ssl_security_protocol is not None:
                self._values["ssl_security_protocol"] = ssl_security_protocol

        @builtins.property
        def auth_password(self) -> typing.Optional[builtins.str]:
            '''The password provided with the ``auth-role`` and ``auth-token`` options of the ``AuthType`` setting for a Redis target endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redissettings.html#cfn-dms-endpoint-redissettings-authpassword
            '''
            result = self._values.get("auth_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auth_type(self) -> typing.Optional[builtins.str]:
            '''The type of authentication to perform when connecting to a Redis target.

            Options include ``none`` , ``auth-token`` , and ``auth-role`` . The ``auth-token`` option requires an ``AuthPassword`` value to be provided. The ``auth-role`` option requires ``AuthUserName`` and ``AuthPassword`` values to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redissettings.html#cfn-dms-endpoint-redissettings-authtype
            '''
            result = self._values.get("auth_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auth_user_name(self) -> typing.Optional[builtins.str]:
            '''The user name provided with the ``auth-role`` option of the ``AuthType`` setting for a Redis target endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redissettings.html#cfn-dms-endpoint-redissettings-authusername
            '''
            result = self._values.get("auth_user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''Transmission Control Protocol (TCP) port for the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redissettings.html#cfn-dms-endpoint-redissettings-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            '''Fully qualified domain name of the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redissettings.html#cfn-dms-endpoint-redissettings-servername
            '''
            result = self._values.get("server_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_ca_certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the certificate authority (CA) that DMS uses to connect to your Redis target endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redissettings.html#cfn-dms-endpoint-redissettings-sslcacertificatearn
            '''
            result = self._values.get("ssl_ca_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_security_protocol(self) -> typing.Optional[builtins.str]:
            '''The connection to a Redis target endpoint using Transport Layer Security (TLS).

            Valid values include ``plaintext`` and ``ssl-encryption`` . The default is ``ssl-encryption`` . The ``ssl-encryption`` option makes an encrypted connection. Optionally, you can identify an Amazon Resource Name (ARN) for an SSL certificate authority (CA) using the ``SslCaCertificateArn`` setting. If an ARN isn't given for a CA, DMS uses the Amazon root CA.

            The ``plaintext`` option doesn't provide Transport Layer Security (TLS) encryption for traffic between endpoint and database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redissettings.html#cfn-dms-endpoint-redissettings-sslsecurityprotocol
            '''
            result = self._values.get("ssl_security_protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedisSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.RedshiftSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accept_any_date": "acceptAnyDate",
            "after_connect_script": "afterConnectScript",
            "bucket_folder": "bucketFolder",
            "bucket_name": "bucketName",
            "case_sensitive_names": "caseSensitiveNames",
            "comp_update": "compUpdate",
            "connection_timeout": "connectionTimeout",
            "date_format": "dateFormat",
            "empty_as_null": "emptyAsNull",
            "encryption_mode": "encryptionMode",
            "explicit_ids": "explicitIds",
            "file_transfer_upload_streams": "fileTransferUploadStreams",
            "load_timeout": "loadTimeout",
            "map_boolean_as_boolean": "mapBooleanAsBoolean",
            "max_file_size": "maxFileSize",
            "remove_quotes": "removeQuotes",
            "replace_chars": "replaceChars",
            "replace_invalid_chars": "replaceInvalidChars",
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_secret_id": "secretsManagerSecretId",
            "server_side_encryption_kms_key_id": "serverSideEncryptionKmsKeyId",
            "service_access_role_arn": "serviceAccessRoleArn",
            "time_format": "timeFormat",
            "trim_blanks": "trimBlanks",
            "truncate_columns": "truncateColumns",
            "write_buffer_size": "writeBufferSize",
        },
    )
    class RedshiftSettingsProperty:
        def __init__(
            self,
            *,
            accept_any_date: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            after_connect_script: typing.Optional[builtins.str] = None,
            bucket_folder: typing.Optional[builtins.str] = None,
            bucket_name: typing.Optional[builtins.str] = None,
            case_sensitive_names: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            comp_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            connection_timeout: typing.Optional[jsii.Number] = None,
            date_format: typing.Optional[builtins.str] = None,
            empty_as_null: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encryption_mode: typing.Optional[builtins.str] = None,
            explicit_ids: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            file_transfer_upload_streams: typing.Optional[jsii.Number] = None,
            load_timeout: typing.Optional[jsii.Number] = None,
            map_boolean_as_boolean: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_file_size: typing.Optional[jsii.Number] = None,
            remove_quotes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            replace_chars: typing.Optional[builtins.str] = None,
            replace_invalid_chars: typing.Optional[builtins.str] = None,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
            server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
            service_access_role_arn: typing.Optional[builtins.str] = None,
            time_format: typing.Optional[builtins.str] = None,
            trim_blanks: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            truncate_columns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            write_buffer_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Provides information that defines an Amazon Redshift endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For more information about other available settings, see `Extra connection attributes when using Amazon Redshift as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Redshift.html#CHAP_Target.Redshift.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

            :param accept_any_date: A value that indicates to allow any date format, including invalid formats such as 00/00/00 00:00:00, to be loaded without generating an error. You can choose ``true`` or ``false`` (the default). This parameter applies only to TIMESTAMP and DATE columns. Always use ACCEPTANYDATE with the DATEFORMAT parameter. If the date format for the data doesn't match the DATEFORMAT specification, Amazon Redshift inserts a NULL value into that field.
            :param after_connect_script: Code to run after connecting. This parameter should contain the code itself, not the name of a file containing the code.
            :param bucket_folder: An S3 folder where the comma-separated-value (.csv) files are stored before being uploaded to the target Redshift cluster. For full load mode, AWS DMS converts source records into .csv files and loads them to the *BucketFolder/TableID* path. AWS DMS uses the Redshift ``COPY`` command to upload the .csv files to the target table. The files are deleted once the ``COPY`` operation has finished. For more information, see `COPY <https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html>`_ in the *Amazon Redshift Database Developer Guide* . For change-data-capture (CDC) mode, AWS DMS creates a *NetChanges* table, and loads the .csv files to this *BucketFolder/NetChangesTableID* path.
            :param bucket_name: The name of the intermediate S3 bucket used to store .csv files before uploading data to Redshift.
            :param case_sensitive_names: If Amazon Redshift is configured to support case sensitive schema names, set ``CaseSensitiveNames`` to ``true`` . The default is ``false`` .
            :param comp_update: If you set ``CompUpdate`` to ``true`` Amazon Redshift applies automatic compression if the table is empty. This applies even if the table columns already have encodings other than ``RAW`` . If you set ``CompUpdate`` to ``false`` , automatic compression is disabled and existing column encodings aren't changed. The default is ``true`` .
            :param connection_timeout: A value that sets the amount of time to wait (in milliseconds) before timing out, beginning from when you initially establish a connection.
            :param date_format: The date format that you are using. Valid values are ``auto`` (case-sensitive), your date format string enclosed in quotes, or NULL. If this parameter is left unset (NULL), it defaults to a format of 'YYYY-MM-DD'. Using ``auto`` recognizes most strings, even some that aren't supported when you use a date format string. If your date and time values use formats different from each other, set this to ``auto`` .
            :param empty_as_null: A value that specifies whether AWS DMS should migrate empty CHAR and VARCHAR fields as NULL. A value of ``true`` sets empty CHAR and VARCHAR fields to null. The default is ``false`` .
            :param encryption_mode: The type of server-side encryption that you want to use for your data. This encryption type is part of the endpoint settings or the extra connections attributes for Amazon S3. You can choose either ``SSE_S3`` (the default) or ``SSE_KMS`` . .. epigraph:: For the ``ModifyEndpoint`` operation, you can change the existing value of the ``EncryptionMode`` parameter from ``SSE_KMS`` to ``SSE_S3`` . But you can’t change the existing value from ``SSE_S3`` to ``SSE_KMS`` . To use ``SSE_S3`` , create an AWS Identity and Access Management (IAM) role with a policy that allows ``"arn:aws:s3:::*"`` to use the following actions: ``"s3:PutObject", "s3:ListBucket"``
            :param explicit_ids: This setting is only valid for a full-load migration task. Set ``ExplicitIds`` to ``true`` to have tables with ``IDENTITY`` columns override their auto-generated values with explicit values loaded from the source data files used to populate the tables. The default is ``false`` .
            :param file_transfer_upload_streams: The number of threads used to upload a single file. This parameter accepts a value from 1 through 64. It defaults to 10. The number of parallel streams used to upload a single .csv file to an S3 bucket using S3 Multipart Upload. For more information, see `Multipart upload overview <https://docs.aws.amazon.com/AmazonS3/latest/dev/mpuoverview.html>`_ . ``FileTransferUploadStreams`` accepts a value from 1 through 64. It defaults to 10.
            :param load_timeout: The amount of time to wait (in milliseconds) before timing out of operations performed by AWS DMS on a Redshift cluster, such as Redshift COPY, INSERT, DELETE, and UPDATE.
            :param map_boolean_as_boolean: When true, lets Redshift migrate the boolean type as boolean. By default, Redshift migrates booleans as ``varchar(1)`` . You must set this setting on both the source and target endpoints for it to take effect.
            :param max_file_size: The maximum size (in KB) of any .csv file used to load data on an S3 bucket and transfer data to Amazon Redshift. It defaults to 1048576KB (1 GB).
            :param remove_quotes: A value that specifies to remove surrounding quotation marks from strings in the incoming data. All characters within the quotation marks, including delimiters, are retained. Choose ``true`` to remove quotation marks. The default is ``false`` .
            :param replace_chars: A value that specifies to replaces the invalid characters specified in ``ReplaceInvalidChars`` , substituting the specified characters instead. The default is ``"?"`` .
            :param replace_invalid_chars: A list of characters that you want to replace. Use with ``ReplaceChars`` .
            :param secrets_manager_access_role_arn: The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` . The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the Amazon Redshift endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both. For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the Amazon Redshift endpoint connection details.
            :param server_side_encryption_kms_key_id: The AWS key ID. If you are using ``SSE_KMS`` for the ``EncryptionMode`` , provide this key ID. The key that you use needs an attached policy that enables IAM user permissions and allows use of the key.
            :param service_access_role_arn: The Amazon Resource Name (ARN) of the IAM role that has access to the Amazon Redshift service. The role must allow the ``iam:PassRole`` action.
            :param time_format: The time format that you want to use. Valid values are ``auto`` (case-sensitive), ``'timeformat_string'`` , ``'epochsecs'`` , or ``'epochmillisecs'`` . It defaults to 10. Using ``auto`` recognizes most strings, even some that aren't supported when you use a time format string. If your date and time values use formats different from each other, set this parameter to ``auto`` .
            :param trim_blanks: A value that specifies to remove the trailing white space characters from a VARCHAR string. This parameter applies only to columns with a VARCHAR data type. Choose ``true`` to remove unneeded white space. The default is ``false`` .
            :param truncate_columns: A value that specifies to truncate data in columns to the appropriate number of characters, so that the data fits in the column. This parameter applies only to columns with a VARCHAR or CHAR data type, and rows with a size of 4 MB or less. Choose ``true`` to truncate data. The default is ``false`` .
            :param write_buffer_size: The size (in KB) of the in-memory file write buffer used when generating .csv files on the local disk at the DMS replication instance. The default value is 1000 (buffer size is 1000KB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                redshift_settings_property = dms_mixins.CfnEndpointPropsMixin.RedshiftSettingsProperty(
                    accept_any_date=False,
                    after_connect_script="afterConnectScript",
                    bucket_folder="bucketFolder",
                    bucket_name="bucketName",
                    case_sensitive_names=False,
                    comp_update=False,
                    connection_timeout=123,
                    date_format="dateFormat",
                    empty_as_null=False,
                    encryption_mode="encryptionMode",
                    explicit_ids=False,
                    file_transfer_upload_streams=123,
                    load_timeout=123,
                    map_boolean_as_boolean=False,
                    max_file_size=123,
                    remove_quotes=False,
                    replace_chars="replaceChars",
                    replace_invalid_chars="replaceInvalidChars",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId",
                    server_side_encryption_kms_key_id="serverSideEncryptionKmsKeyId",
                    service_access_role_arn="serviceAccessRoleArn",
                    time_format="timeFormat",
                    trim_blanks=False,
                    truncate_columns=False,
                    write_buffer_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3a5501c1d4f0cafb2dc67530f742b208a8a0822803d82053627c7384e7b75a3)
                check_type(argname="argument accept_any_date", value=accept_any_date, expected_type=type_hints["accept_any_date"])
                check_type(argname="argument after_connect_script", value=after_connect_script, expected_type=type_hints["after_connect_script"])
                check_type(argname="argument bucket_folder", value=bucket_folder, expected_type=type_hints["bucket_folder"])
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument case_sensitive_names", value=case_sensitive_names, expected_type=type_hints["case_sensitive_names"])
                check_type(argname="argument comp_update", value=comp_update, expected_type=type_hints["comp_update"])
                check_type(argname="argument connection_timeout", value=connection_timeout, expected_type=type_hints["connection_timeout"])
                check_type(argname="argument date_format", value=date_format, expected_type=type_hints["date_format"])
                check_type(argname="argument empty_as_null", value=empty_as_null, expected_type=type_hints["empty_as_null"])
                check_type(argname="argument encryption_mode", value=encryption_mode, expected_type=type_hints["encryption_mode"])
                check_type(argname="argument explicit_ids", value=explicit_ids, expected_type=type_hints["explicit_ids"])
                check_type(argname="argument file_transfer_upload_streams", value=file_transfer_upload_streams, expected_type=type_hints["file_transfer_upload_streams"])
                check_type(argname="argument load_timeout", value=load_timeout, expected_type=type_hints["load_timeout"])
                check_type(argname="argument map_boolean_as_boolean", value=map_boolean_as_boolean, expected_type=type_hints["map_boolean_as_boolean"])
                check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
                check_type(argname="argument remove_quotes", value=remove_quotes, expected_type=type_hints["remove_quotes"])
                check_type(argname="argument replace_chars", value=replace_chars, expected_type=type_hints["replace_chars"])
                check_type(argname="argument replace_invalid_chars", value=replace_invalid_chars, expected_type=type_hints["replace_invalid_chars"])
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
                check_type(argname="argument server_side_encryption_kms_key_id", value=server_side_encryption_kms_key_id, expected_type=type_hints["server_side_encryption_kms_key_id"])
                check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
                check_type(argname="argument time_format", value=time_format, expected_type=type_hints["time_format"])
                check_type(argname="argument trim_blanks", value=trim_blanks, expected_type=type_hints["trim_blanks"])
                check_type(argname="argument truncate_columns", value=truncate_columns, expected_type=type_hints["truncate_columns"])
                check_type(argname="argument write_buffer_size", value=write_buffer_size, expected_type=type_hints["write_buffer_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if accept_any_date is not None:
                self._values["accept_any_date"] = accept_any_date
            if after_connect_script is not None:
                self._values["after_connect_script"] = after_connect_script
            if bucket_folder is not None:
                self._values["bucket_folder"] = bucket_folder
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if case_sensitive_names is not None:
                self._values["case_sensitive_names"] = case_sensitive_names
            if comp_update is not None:
                self._values["comp_update"] = comp_update
            if connection_timeout is not None:
                self._values["connection_timeout"] = connection_timeout
            if date_format is not None:
                self._values["date_format"] = date_format
            if empty_as_null is not None:
                self._values["empty_as_null"] = empty_as_null
            if encryption_mode is not None:
                self._values["encryption_mode"] = encryption_mode
            if explicit_ids is not None:
                self._values["explicit_ids"] = explicit_ids
            if file_transfer_upload_streams is not None:
                self._values["file_transfer_upload_streams"] = file_transfer_upload_streams
            if load_timeout is not None:
                self._values["load_timeout"] = load_timeout
            if map_boolean_as_boolean is not None:
                self._values["map_boolean_as_boolean"] = map_boolean_as_boolean
            if max_file_size is not None:
                self._values["max_file_size"] = max_file_size
            if remove_quotes is not None:
                self._values["remove_quotes"] = remove_quotes
            if replace_chars is not None:
                self._values["replace_chars"] = replace_chars
            if replace_invalid_chars is not None:
                self._values["replace_invalid_chars"] = replace_invalid_chars
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id
            if server_side_encryption_kms_key_id is not None:
                self._values["server_side_encryption_kms_key_id"] = server_side_encryption_kms_key_id
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn
            if time_format is not None:
                self._values["time_format"] = time_format
            if trim_blanks is not None:
                self._values["trim_blanks"] = trim_blanks
            if truncate_columns is not None:
                self._values["truncate_columns"] = truncate_columns
            if write_buffer_size is not None:
                self._values["write_buffer_size"] = write_buffer_size

        @builtins.property
        def accept_any_date(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that indicates to allow any date format, including invalid formats such as 00/00/00 00:00:00, to be loaded without generating an error.

            You can choose ``true`` or ``false`` (the default).

            This parameter applies only to TIMESTAMP and DATE columns. Always use ACCEPTANYDATE with the DATEFORMAT parameter. If the date format for the data doesn't match the DATEFORMAT specification, Amazon Redshift inserts a NULL value into that field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-acceptanydate
            '''
            result = self._values.get("accept_any_date")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def after_connect_script(self) -> typing.Optional[builtins.str]:
            '''Code to run after connecting.

            This parameter should contain the code itself, not the name of a file containing the code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-afterconnectscript
            '''
            result = self._values.get("after_connect_script")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_folder(self) -> typing.Optional[builtins.str]:
            '''An S3 folder where the comma-separated-value (.csv) files are stored before being uploaded to the target Redshift cluster.

            For full load mode, AWS DMS converts source records into .csv files and loads them to the *BucketFolder/TableID* path. AWS DMS uses the Redshift ``COPY`` command to upload the .csv files to the target table. The files are deleted once the ``COPY`` operation has finished. For more information, see `COPY <https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html>`_ in the *Amazon Redshift Database Developer Guide* .

            For change-data-capture (CDC) mode, AWS DMS creates a *NetChanges* table, and loads the .csv files to this *BucketFolder/NetChangesTableID* path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-bucketfolder
            '''
            result = self._values.get("bucket_folder")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the intermediate S3 bucket used to store .csv files before uploading data to Redshift.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def case_sensitive_names(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If Amazon Redshift is configured to support case sensitive schema names, set ``CaseSensitiveNames`` to ``true`` .

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-casesensitivenames
            '''
            result = self._values.get("case_sensitive_names")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def comp_update(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If you set ``CompUpdate`` to ``true`` Amazon Redshift applies automatic compression if the table is empty.

            This applies even if the table columns already have encodings other than ``RAW`` . If you set ``CompUpdate`` to ``false`` , automatic compression is disabled and existing column encodings aren't changed. The default is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-compupdate
            '''
            result = self._values.get("comp_update")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def connection_timeout(self) -> typing.Optional[jsii.Number]:
            '''A value that sets the amount of time to wait (in milliseconds) before timing out, beginning from when you initially establish a connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-connectiontimeout
            '''
            result = self._values.get("connection_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def date_format(self) -> typing.Optional[builtins.str]:
            '''The date format that you are using.

            Valid values are ``auto`` (case-sensitive), your date format string enclosed in quotes, or NULL. If this parameter is left unset (NULL), it defaults to a format of 'YYYY-MM-DD'. Using ``auto`` recognizes most strings, even some that aren't supported when you use a date format string.

            If your date and time values use formats different from each other, set this to ``auto`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-dateformat
            '''
            result = self._values.get("date_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def empty_as_null(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that specifies whether AWS DMS should migrate empty CHAR and VARCHAR fields as NULL.

            A value of ``true`` sets empty CHAR and VARCHAR fields to null. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-emptyasnull
            '''
            result = self._values.get("empty_as_null")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encryption_mode(self) -> typing.Optional[builtins.str]:
            '''The type of server-side encryption that you want to use for your data.

            This encryption type is part of the endpoint settings or the extra connections attributes for Amazon S3. You can choose either ``SSE_S3`` (the default) or ``SSE_KMS`` .
            .. epigraph::

               For the ``ModifyEndpoint`` operation, you can change the existing value of the ``EncryptionMode`` parameter from ``SSE_KMS`` to ``SSE_S3`` . But you can’t change the existing value from ``SSE_S3`` to ``SSE_KMS`` .

            To use ``SSE_S3`` , create an AWS Identity and Access Management (IAM) role with a policy that allows ``"arn:aws:s3:::*"`` to use the following actions: ``"s3:PutObject", "s3:ListBucket"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-encryptionmode
            '''
            result = self._values.get("encryption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def explicit_ids(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This setting is only valid for a full-load migration task.

            Set ``ExplicitIds`` to ``true`` to have tables with ``IDENTITY`` columns override their auto-generated values with explicit values loaded from the source data files used to populate the tables. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-explicitids
            '''
            result = self._values.get("explicit_ids")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def file_transfer_upload_streams(self) -> typing.Optional[jsii.Number]:
            '''The number of threads used to upload a single file.

            This parameter accepts a value from 1 through 64. It defaults to 10.

            The number of parallel streams used to upload a single .csv file to an S3 bucket using S3 Multipart Upload. For more information, see `Multipart upload overview <https://docs.aws.amazon.com/AmazonS3/latest/dev/mpuoverview.html>`_ .

            ``FileTransferUploadStreams`` accepts a value from 1 through 64. It defaults to 10.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-filetransferuploadstreams
            '''
            result = self._values.get("file_transfer_upload_streams")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def load_timeout(self) -> typing.Optional[jsii.Number]:
            '''The amount of time to wait (in milliseconds) before timing out of operations performed by AWS DMS on a Redshift cluster, such as Redshift COPY, INSERT, DELETE, and UPDATE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-loadtimeout
            '''
            result = self._values.get("load_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def map_boolean_as_boolean(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true, lets Redshift migrate the boolean type as boolean.

            By default, Redshift migrates booleans as ``varchar(1)`` . You must set this setting on both the source and target endpoints for it to take effect.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-mapbooleanasboolean
            '''
            result = self._values.get("map_boolean_as_boolean")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_file_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum size (in KB) of any .csv file used to load data on an S3 bucket and transfer data to Amazon Redshift. It defaults to 1048576KB (1 GB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-maxfilesize
            '''
            result = self._values.get("max_file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def remove_quotes(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that specifies to remove surrounding quotation marks from strings in the incoming data.

            All characters within the quotation marks, including delimiters, are retained. Choose ``true`` to remove quotation marks. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-removequotes
            '''
            result = self._values.get("remove_quotes")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def replace_chars(self) -> typing.Optional[builtins.str]:
            '''A value that specifies to replaces the invalid characters specified in ``ReplaceInvalidChars`` , substituting the specified characters instead.

            The default is ``"?"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-replacechars
            '''
            result = self._values.get("replace_chars")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replace_invalid_chars(self) -> typing.Optional[builtins.str]:
            '''A list of characters that you want to replace.

            Use with ``ReplaceChars`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-replaceinvalidchars
            '''
            result = self._values.get("replace_invalid_chars")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` .

            The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the Amazon Redshift endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both.

               For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the Amazon Redshift endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_side_encryption_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The AWS  key ID.

            If you are using ``SSE_KMS`` for the ``EncryptionMode`` , provide this key ID. The key that you use needs an attached policy that enables IAM user permissions and allows use of the key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-serversideencryptionkmskeyid
            '''
            result = self._values.get("server_side_encryption_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role that has access to the Amazon Redshift service.

            The role must allow the ``iam:PassRole`` action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-serviceaccessrolearn
            '''
            result = self._values.get("service_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_format(self) -> typing.Optional[builtins.str]:
            '''The time format that you want to use.

            Valid values are ``auto`` (case-sensitive), ``'timeformat_string'`` , ``'epochsecs'`` , or ``'epochmillisecs'`` . It defaults to 10. Using ``auto`` recognizes most strings, even some that aren't supported when you use a time format string.

            If your date and time values use formats different from each other, set this parameter to ``auto`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-timeformat
            '''
            result = self._values.get("time_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trim_blanks(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that specifies to remove the trailing white space characters from a VARCHAR string.

            This parameter applies only to columns with a VARCHAR data type. Choose ``true`` to remove unneeded white space. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-trimblanks
            '''
            result = self._values.get("trim_blanks")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def truncate_columns(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that specifies to truncate data in columns to the appropriate number of characters, so that the data fits in the column.

            This parameter applies only to columns with a VARCHAR or CHAR data type, and rows with a size of 4 MB or less. Choose ``true`` to truncate data. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-truncatecolumns
            '''
            result = self._values.get("truncate_columns")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def write_buffer_size(self) -> typing.Optional[jsii.Number]:
            '''The size (in KB) of the in-memory file write buffer used when generating .csv files on the local disk at the DMS replication instance. The default value is 1000 (buffer size is 1000KB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-writebuffersize
            '''
            result = self._values.get("write_buffer_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.S3SettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_column_name": "addColumnName",
            "add_trailing_padding_character": "addTrailingPaddingCharacter",
            "bucket_folder": "bucketFolder",
            "bucket_name": "bucketName",
            "canned_acl_for_objects": "cannedAclForObjects",
            "cdc_inserts_and_updates": "cdcInsertsAndUpdates",
            "cdc_inserts_only": "cdcInsertsOnly",
            "cdc_max_batch_interval": "cdcMaxBatchInterval",
            "cdc_min_file_size": "cdcMinFileSize",
            "cdc_path": "cdcPath",
            "compression_type": "compressionType",
            "csv_delimiter": "csvDelimiter",
            "csv_no_sup_value": "csvNoSupValue",
            "csv_null_value": "csvNullValue",
            "csv_row_delimiter": "csvRowDelimiter",
            "data_format": "dataFormat",
            "data_page_size": "dataPageSize",
            "date_partition_delimiter": "datePartitionDelimiter",
            "date_partition_enabled": "datePartitionEnabled",
            "date_partition_sequence": "datePartitionSequence",
            "date_partition_timezone": "datePartitionTimezone",
            "dict_page_size_limit": "dictPageSizeLimit",
            "enable_statistics": "enableStatistics",
            "encoding_type": "encodingType",
            "encryption_mode": "encryptionMode",
            "expected_bucket_owner": "expectedBucketOwner",
            "external_table_definition": "externalTableDefinition",
            "glue_catalog_generation": "glueCatalogGeneration",
            "ignore_header_rows": "ignoreHeaderRows",
            "include_op_for_full_load": "includeOpForFullLoad",
            "max_file_size": "maxFileSize",
            "parquet_timestamp_in_millisecond": "parquetTimestampInMillisecond",
            "parquet_version": "parquetVersion",
            "preserve_transactions": "preserveTransactions",
            "rfc4180": "rfc4180",
            "row_group_length": "rowGroupLength",
            "server_side_encryption_kms_key_id": "serverSideEncryptionKmsKeyId",
            "service_access_role_arn": "serviceAccessRoleArn",
            "timestamp_column_name": "timestampColumnName",
            "use_csv_no_sup_value": "useCsvNoSupValue",
            "use_task_start_time_for_full_load_timestamp": "useTaskStartTimeForFullLoadTimestamp",
        },
    )
    class S3SettingsProperty:
        def __init__(
            self,
            *,
            add_column_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            add_trailing_padding_character: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            bucket_folder: typing.Optional[builtins.str] = None,
            bucket_name: typing.Optional[builtins.str] = None,
            canned_acl_for_objects: typing.Optional[builtins.str] = None,
            cdc_inserts_and_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            cdc_inserts_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            cdc_max_batch_interval: typing.Optional[jsii.Number] = None,
            cdc_min_file_size: typing.Optional[jsii.Number] = None,
            cdc_path: typing.Optional[builtins.str] = None,
            compression_type: typing.Optional[builtins.str] = None,
            csv_delimiter: typing.Optional[builtins.str] = None,
            csv_no_sup_value: typing.Optional[builtins.str] = None,
            csv_null_value: typing.Optional[builtins.str] = None,
            csv_row_delimiter: typing.Optional[builtins.str] = None,
            data_format: typing.Optional[builtins.str] = None,
            data_page_size: typing.Optional[jsii.Number] = None,
            date_partition_delimiter: typing.Optional[builtins.str] = None,
            date_partition_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            date_partition_sequence: typing.Optional[builtins.str] = None,
            date_partition_timezone: typing.Optional[builtins.str] = None,
            dict_page_size_limit: typing.Optional[jsii.Number] = None,
            enable_statistics: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encoding_type: typing.Optional[builtins.str] = None,
            encryption_mode: typing.Optional[builtins.str] = None,
            expected_bucket_owner: typing.Optional[builtins.str] = None,
            external_table_definition: typing.Optional[builtins.str] = None,
            glue_catalog_generation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ignore_header_rows: typing.Optional[jsii.Number] = None,
            include_op_for_full_load: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_file_size: typing.Optional[jsii.Number] = None,
            parquet_timestamp_in_millisecond: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            parquet_version: typing.Optional[builtins.str] = None,
            preserve_transactions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            rfc4180: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            row_group_length: typing.Optional[jsii.Number] = None,
            server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
            service_access_role_arn: typing.Optional[builtins.str] = None,
            timestamp_column_name: typing.Optional[builtins.str] = None,
            use_csv_no_sup_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_task_start_time_for_full_load_timestamp: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Provides information that defines an Amazon S3 endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For more information about the available settings, see `Extra connection attributes when using Amazon S3 as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.S3.html#CHAP_Source.S3.Configuring>`_ and `Extra connection attributes when using Amazon S3 as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring>`_ in the *AWS Database Migration Service User Guide* .

            :param add_column_name: An optional parameter that, when set to ``true`` or ``y`` , you can use to add column name information to the .csv output file. The default value is ``false`` . Valid values are ``true`` , ``false`` , ``y`` , and ``n`` .
            :param add_trailing_padding_character: Use the S3 target endpoint setting ``AddTrailingPaddingCharacter`` to add padding on string data. The default value is ``false`` .
            :param bucket_folder: An optional parameter to set a folder name in the S3 bucket. If provided, tables are created in the path ``*bucketFolder* / *schema_name* / *table_name* /`` . If this parameter isn't specified, the path used is ``*schema_name* / *table_name* /`` .
            :param bucket_name: The name of the S3 bucket.
            :param canned_acl_for_objects: A value that enables AWS DMS to specify a predefined (canned) access control list (ACL) for objects created in an Amazon S3 bucket as .csv or .parquet files. For more information about Amazon S3 canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ in the *Amazon S3 Developer Guide* . The default value is NONE. Valid values include NONE, PRIVATE, PUBLIC_READ, PUBLIC_READ_WRITE, AUTHENTICATED_READ, AWS_EXEC_READ, BUCKET_OWNER_READ, and BUCKET_OWNER_FULL_CONTROL.
            :param cdc_inserts_and_updates: A value that enables a change data capture (CDC) load to write INSERT and UPDATE operations to .csv or .parquet (columnar storage) output files. The default setting is ``false`` , but when ``CdcInsertsAndUpdates`` is set to ``true`` or ``y`` , only INSERTs and UPDATEs from the source database are migrated to the .csv or .parquet file. For .csv file format only, how these INSERTs and UPDATEs are recorded depends on the value of the ``IncludeOpForFullLoad`` parameter. If ``IncludeOpForFullLoad`` is set to ``true`` , the first field of every CDC record is set to either ``I`` or ``U`` to indicate INSERT and UPDATE operations at the source. But if ``IncludeOpForFullLoad`` is set to ``false`` , CDC records are written without an indication of INSERT or UPDATE operations at the source. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* . .. epigraph:: AWS DMS supports the use of the ``CdcInsertsAndUpdates`` parameter in versions 3.3.1 and later. ``CdcInsertsOnly`` and ``CdcInsertsAndUpdates`` can't both be set to ``true`` for the same endpoint. Set either ``CdcInsertsOnly`` or ``CdcInsertsAndUpdates`` to ``true`` for the same endpoint, but not both.
            :param cdc_inserts_only: A value that enables a change data capture (CDC) load to write only INSERT operations to .csv or columnar storage (.parquet) output files. By default (the ``false`` setting), the first field in a .csv or .parquet record contains the letter I (INSERT), U (UPDATE), or D (DELETE). These values indicate whether the row was inserted, updated, or deleted at the source database for a CDC load to the target. If ``CdcInsertsOnly`` is set to ``true`` or ``y`` , only INSERTs from the source database are migrated to the .csv or .parquet file. For .csv format only, how these INSERTs are recorded depends on the value of ``IncludeOpForFullLoad`` . If ``IncludeOpForFullLoad`` is set to ``true`` , the first field of every CDC record is set to I to indicate the INSERT operation at the source. If ``IncludeOpForFullLoad`` is set to ``false`` , every CDC record is written without a first field to indicate the INSERT operation at the source. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* . .. epigraph:: AWS DMS supports the interaction described preceding between the ``CdcInsertsOnly`` and ``IncludeOpForFullLoad`` parameters in versions 3.1.4 and later. ``CdcInsertsOnly`` and ``CdcInsertsAndUpdates`` can't both be set to ``true`` for the same endpoint. Set either ``CdcInsertsOnly`` or ``CdcInsertsAndUpdates`` to ``true`` for the same endpoint, but not both.
            :param cdc_max_batch_interval: Maximum length of the interval, defined in seconds, after which to output a file to Amazon S3. When ``CdcMaxBatchInterval`` and ``CdcMinFileSize`` are both specified, the file write is triggered by whichever parameter condition is met first within an AWS DMS CloudFormation template. The default value is 60 seconds.
            :param cdc_min_file_size: Minimum file size, defined in kilobytes, to reach for a file output to Amazon S3. When ``CdcMinFileSize`` and ``CdcMaxBatchInterval`` are both specified, the file write is triggered by whichever parameter condition is met first within an AWS DMS CloudFormation template. The default value is 32 MB.
            :param cdc_path: Specifies the folder path of CDC files. For an S3 source, this setting is required if a task captures change data; otherwise, it's optional. If ``CdcPath`` is set, AWS DMS reads CDC files from this path and replicates the data changes to the target endpoint. For an S3 target if you set ```PreserveTransactions`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-PreserveTransactions>`_ to ``true`` , AWS DMS verifies that you have set this parameter to a folder path on your S3 target where AWS DMS can save the transaction order for the CDC load. AWS DMS creates this CDC folder path in either your S3 target working directory or the S3 target location specified by ```BucketFolder`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketFolder>`_ and ```BucketName`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketName>`_ . For example, if you specify ``CdcPath`` as ``MyChangedData`` , and you specify ``BucketName`` as ``MyTargetBucket`` but do not specify ``BucketFolder`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyChangedData`` . If you specify the same ``CdcPath`` , and you specify ``BucketName`` as ``MyTargetBucket`` and ``BucketFolder`` as ``MyTargetData`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyTargetData/MyChangedData`` . For more information on CDC including transaction order on an S3 target, see `Capturing data changes (CDC) including transaction order on the S3 target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.EndpointSettings.CdcPath>`_ . .. epigraph:: This setting is supported in AWS DMS versions 3.4.2 and later.
            :param compression_type: An optional parameter. When set to GZIP it enables the service to compress the target files. To allow the service to write the target files uncompressed, either set this parameter to NONE (the default) or don't specify the parameter at all. This parameter applies to both .csv and .parquet file formats.
            :param csv_delimiter: The delimiter used to separate columns in the .csv file for both source and target. The default is a comma.
            :param csv_no_sup_value: This setting only applies if your Amazon S3 output files during a change data capture (CDC) load are written in .csv format. If ```UseCsvNoSupValue`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-UseCsvNoSupValue>`_ is set to true, specify a string value that you want AWS DMS to use for all columns not included in the supplemental log. If you do not specify a string value, AWS DMS uses the null value for these columns regardless of the ``UseCsvNoSupValue`` setting. .. epigraph:: This setting is supported in AWS DMS versions 3.4.1 and later.
            :param csv_null_value: An optional parameter that specifies how AWS DMS treats null values. While handling the null value, you can use this parameter to pass a user-defined string as null when writing to the target. For example, when target columns are not nullable, you can use this option to differentiate between the empty string value and the null value. So, if you set this parameter value to the empty string ("" or ''), AWS DMS treats the empty string as the null value instead of ``NULL`` . The default value is ``NULL`` . Valid values include any valid string.
            :param csv_row_delimiter: The delimiter used to separate rows in the .csv file for both source and target. The default is a carriage return ( ``\\n`` ).
            :param data_format: The format of the data that you want to use for output. You can choose one of the following:. - ``csv`` : This is a row-based file format with comma-separated values (.csv). - ``parquet`` : Apache Parquet (.parquet) is a columnar storage file format that features efficient compression and provides faster query response.
            :param data_page_size: The size of one data page in bytes. This parameter defaults to 1024 * 1024 bytes (1 MiB). This number is used for .parquet file format only.
            :param date_partition_delimiter: Specifies a date separating delimiter to use during folder partitioning. The default value is ``SLASH`` . Use this parameter when ``DatePartitionedEnabled`` is set to ``true`` .
            :param date_partition_enabled: When set to ``true`` , this parameter partitions S3 bucket folders based on transaction commit dates. The default value is ``false`` . For more information about date-based folder partitioning, see `Using date-based folder partitioning <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.DatePartitioning>`_ .
            :param date_partition_sequence: Identifies the sequence of the date format to use during folder partitioning. The default value is ``YYYYMMDD`` . Use this parameter when ``DatePartitionedEnabled`` is set to ``true`` .
            :param date_partition_timezone: When creating an S3 target endpoint, set ``DatePartitionTimezone`` to convert the current UTC time into a specified time zone. The conversion occurs when a date partition folder is created and a change data capture (CDC) file name is generated. The time zone format is Area/Location. Use this parameter when ``DatePartitionedEnabled`` is set to ``true`` , as shown in the following example. ``s3-settings='{"DatePartitionEnabled": true, "DatePartitionSequence": "YYYYMMDDHH", "DatePartitionDelimiter": "SLASH", "DatePartitionTimezone":" *Asia/Seoul* ", "BucketName": "dms-nattarat-test"}'``
            :param dict_page_size_limit: The maximum size of an encoded dictionary page of a column. If the dictionary page exceeds this, this column is stored using an encoding type of ``PLAIN`` . This parameter defaults to 1024 * 1024 bytes (1 MiB), the maximum size of a dictionary page before it reverts to ``PLAIN`` encoding. This size is used for .parquet file format only.
            :param enable_statistics: A value that enables statistics for Parquet pages and row groups. Choose ``true`` to enable statistics, ``false`` to disable. Statistics include ``NULL`` , ``DISTINCT`` , ``MAX`` , and ``MIN`` values. This parameter defaults to ``true`` . This value is used for .parquet file format only.
            :param encoding_type: The type of encoding that you're using:. - ``RLE_DICTIONARY`` uses a combination of bit-packing and run-length encoding to store repeated values more efficiently. This is the default. - ``PLAIN`` doesn't use encoding at all. Values are stored as they are. - ``PLAIN_DICTIONARY`` builds a dictionary of the values encountered in a given column. The dictionary is stored in a dictionary page for each column chunk.
            :param encryption_mode: The type of server-side encryption that you want to use for your data. This encryption type is part of the endpoint settings or the extra connections attributes for Amazon S3. You can choose either ``SSE_S3`` (the default) or ``SSE_KMS`` . .. epigraph:: For the ``ModifyEndpoint`` operation, you can change the existing value of the ``EncryptionMode`` parameter from ``SSE_KMS`` to ``SSE_S3`` . But you can’t change the existing value from ``SSE_S3`` to ``SSE_KMS`` . To use ``SSE_S3`` , you need an IAM role with permission to allow ``"arn:aws:s3:::dms-*"`` to use the following actions: - ``s3:CreateBucket`` - ``s3:ListBucket`` - ``s3:DeleteBucket`` - ``s3:GetBucketLocation`` - ``s3:GetObject`` - ``s3:PutObject`` - ``s3:DeleteObject`` - ``s3:GetObjectVersion`` - ``s3:GetBucketPolicy`` - ``s3:PutBucketPolicy`` - ``s3:DeleteBucketPolicy``
            :param expected_bucket_owner: To specify a bucket owner and prevent sniping, you can use the ``ExpectedBucketOwner`` endpoint setting. Example: ``--s3-settings='{"ExpectedBucketOwner": " *AWS_Account_ID* "}'`` When you make a request to test a connection or perform a migration, S3 checks the account ID of the bucket owner against the specified parameter.
            :param external_table_definition: The external table definition. Conditional: If ``S3`` is used as a source then ``ExternalTableDefinition`` is required.
            :param glue_catalog_generation: When true, allows AWS Glue to catalog your S3 bucket. Creating an AWS Glue catalog lets you use Athena to query your data.
            :param ignore_header_rows: When this value is set to 1, AWS DMS ignores the first row header in a .csv file. A value of 1 turns on the feature; a value of 0 turns off the feature. The default is 0.
            :param include_op_for_full_load: A value that enables a full load to write INSERT operations to the comma-separated value (.csv) output files only to indicate how the rows were added to the source database. .. epigraph:: AWS DMS supports the ``IncludeOpForFullLoad`` parameter in versions 3.1.4 and later. For full load, records can only be inserted. By default (the ``false`` setting), no information is recorded in these output files for a full load to indicate that the rows were inserted at the source database. If ``IncludeOpForFullLoad`` is set to ``true`` or ``y`` , the INSERT is recorded as an I annotation in the first field of the .csv file. This allows the format of your target records from a full load to be consistent with the target records from a CDC load. .. epigraph:: This setting works together with the ``CdcInsertsOnly`` and the ``CdcInsertsAndUpdates`` parameters for output to .csv files only. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* .
            :param max_file_size: A value that specifies the maximum size (in KB) of any .csv file to be created while migrating to an S3 target during full load. The default value is 1,048,576 KB (1 GB). Valid values include 1 to 1,048,576.
            :param parquet_timestamp_in_millisecond: A value that specifies the precision of any ``TIMESTAMP`` column values that are written to an Amazon S3 object file in .parquet format. .. epigraph:: AWS DMS supports the ``ParquetTimestampInMillisecond`` parameter in versions 3.1.4 and later. When ``ParquetTimestampInMillisecond`` is set to ``true`` or ``y`` , AWS DMS writes all ``TIMESTAMP`` columns in a .parquet formatted file with millisecond precision. Otherwise, DMS writes them with microsecond precision. Currently, Amazon Athena and AWS Glue can handle only millisecond precision for ``TIMESTAMP`` values. Set this parameter to ``true`` for S3 endpoint object files that are .parquet formatted only if you plan to query or process the data with Athena or AWS Glue . .. epigraph:: AWS DMS writes any ``TIMESTAMP`` column values written to an S3 file in .csv format with microsecond precision. Setting ``ParquetTimestampInMillisecond`` has no effect on the string format of the timestamp column value that is inserted by setting the ``TimestampColumnName`` parameter.
            :param parquet_version: The version of the Apache Parquet format that you want to use: ``parquet_1_0`` (the default) or ``parquet_2_0`` .
            :param preserve_transactions: If this setting is set to ``true`` , AWS DMS saves the transaction order for a change data capture (CDC) load on the Amazon S3 target specified by ```CdcPath`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-CdcPath>`_ . For more information, see `Capturing data changes (CDC) including transaction order on the S3 target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.EndpointSettings.CdcPath>`_ . .. epigraph:: This setting is supported in AWS DMS versions 3.4.2 and later.
            :param rfc4180: For an S3 source, when this value is set to ``true`` or ``y`` , each leading double quotation mark has to be followed by an ending double quotation mark. This formatting complies with RFC 4180. When this value is set to ``false`` or ``n`` , string literals are copied to the target as is. In this case, a delimiter (row or column) signals the end of the field. Thus, you can't use a delimiter as part of the string, because it signals the end of the value. For an S3 target, an optional parameter used to set behavior to comply with RFC 4180 for data migrated to Amazon S3 using .csv file format only. When this value is set to ``true`` or ``y`` using Amazon S3 as a target, if the data has quotation marks or newline characters in it, AWS DMS encloses the entire column with an additional pair of double quotation marks ("). Every quotation mark within the data is repeated twice. The default value is ``true`` . Valid values include ``true`` , ``false`` , ``y`` , and ``n`` .
            :param row_group_length: The number of rows in a row group. A smaller row group size provides faster reads. But as the number of row groups grows, the slower writes become. This parameter defaults to 10,000 rows. This number is used for .parquet file format only. If you choose a value larger than the maximum, ``RowGroupLength`` is set to the max row group length in bytes (64 * 1024 * 1024).
            :param server_side_encryption_kms_key_id: If you are using ``SSE_KMS`` for the ``EncryptionMode`` , provide the AWS key ID. The key that you use needs an attached policy that enables IAM user permissions and allows use of the key. Here is a CLI example: ``aws dms create-endpoint --endpoint-identifier *value* --endpoint-type target --engine-name s3 --s3-settings ServiceAccessRoleArn= *value* ,BucketFolder= *value* ,BucketName= *value* ,EncryptionMode=SSE_KMS,ServerSideEncryptionKmsKeyId= *value*``
            :param service_access_role_arn: A required parameter that specifies the Amazon Resource Name (ARN) used by the service to access the IAM role. The role must allow the ``iam:PassRole`` action. It enables AWS DMS to read and write objects from an S3 bucket.
            :param timestamp_column_name: A value that when nonblank causes AWS DMS to add a column with timestamp information to the endpoint data for an Amazon S3 target. .. epigraph:: AWS DMS supports the ``TimestampColumnName`` parameter in versions 3.1.4 and later. AWS DMS includes an additional ``STRING`` column in the .csv or .parquet object files of your migrated data when you set ``TimestampColumnName`` to a nonblank value. For a full load, each row of this timestamp column contains a timestamp for when the data was transferred from the source to the target by DMS. For a change data capture (CDC) load, each row of the timestamp column contains the timestamp for the commit of that row in the source database. The string format for this timestamp column value is ``yyyy-MM-dd HH:mm:ss.SSSSSS`` . By default, the precision of this value is in microseconds. For a CDC load, the rounding of the precision depends on the commit timestamp supported by DMS for the source database. When the ``AddColumnName`` parameter is set to ``true`` , DMS also includes a name for the timestamp column that you set with ``TimestampColumnName`` .
            :param use_csv_no_sup_value: This setting applies if the S3 output files during a change data capture (CDC) load are written in .csv format. If this setting is set to ``true`` for columns not included in the supplemental log, AWS DMS uses the value specified by ```CsvNoSupValue`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-CsvNoSupValue>`_ . If this setting isn't set or is set to ``false`` , AWS DMS uses the null value for these columns. .. epigraph:: This setting is supported in AWS DMS versions 3.4.1 and later.
            :param use_task_start_time_for_full_load_timestamp: When set to true, this parameter uses the task start time as the timestamp column value instead of the time data is written to target. For full load, when ``useTaskStartTimeForFullLoadTimestamp`` is set to ``true`` , each row of the timestamp column contains the task start time. For CDC loads, each row of the timestamp column contains the transaction commit time. When ``useTaskStartTimeForFullLoadTimestamp`` is set to ``false`` , the full load timestamp in the timestamp column increments with the time data arrives at the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                s3_settings_property = dms_mixins.CfnEndpointPropsMixin.S3SettingsProperty(
                    add_column_name=False,
                    add_trailing_padding_character=False,
                    bucket_folder="bucketFolder",
                    bucket_name="bucketName",
                    canned_acl_for_objects="cannedAclForObjects",
                    cdc_inserts_and_updates=False,
                    cdc_inserts_only=False,
                    cdc_max_batch_interval=123,
                    cdc_min_file_size=123,
                    cdc_path="cdcPath",
                    compression_type="compressionType",
                    csv_delimiter="csvDelimiter",
                    csv_no_sup_value="csvNoSupValue",
                    csv_null_value="csvNullValue",
                    csv_row_delimiter="csvRowDelimiter",
                    data_format="dataFormat",
                    data_page_size=123,
                    date_partition_delimiter="datePartitionDelimiter",
                    date_partition_enabled=False,
                    date_partition_sequence="datePartitionSequence",
                    date_partition_timezone="datePartitionTimezone",
                    dict_page_size_limit=123,
                    enable_statistics=False,
                    encoding_type="encodingType",
                    encryption_mode="encryptionMode",
                    expected_bucket_owner="expectedBucketOwner",
                    external_table_definition="externalTableDefinition",
                    glue_catalog_generation=False,
                    ignore_header_rows=123,
                    include_op_for_full_load=False,
                    max_file_size=123,
                    parquet_timestamp_in_millisecond=False,
                    parquet_version="parquetVersion",
                    preserve_transactions=False,
                    rfc4180=False,
                    row_group_length=123,
                    server_side_encryption_kms_key_id="serverSideEncryptionKmsKeyId",
                    service_access_role_arn="serviceAccessRoleArn",
                    timestamp_column_name="timestampColumnName",
                    use_csv_no_sup_value=False,
                    use_task_start_time_for_full_load_timestamp=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41721b1b55355680c2cb8be27878390b4b6b069f0060d78a3637586ece2c3ff1)
                check_type(argname="argument add_column_name", value=add_column_name, expected_type=type_hints["add_column_name"])
                check_type(argname="argument add_trailing_padding_character", value=add_trailing_padding_character, expected_type=type_hints["add_trailing_padding_character"])
                check_type(argname="argument bucket_folder", value=bucket_folder, expected_type=type_hints["bucket_folder"])
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument canned_acl_for_objects", value=canned_acl_for_objects, expected_type=type_hints["canned_acl_for_objects"])
                check_type(argname="argument cdc_inserts_and_updates", value=cdc_inserts_and_updates, expected_type=type_hints["cdc_inserts_and_updates"])
                check_type(argname="argument cdc_inserts_only", value=cdc_inserts_only, expected_type=type_hints["cdc_inserts_only"])
                check_type(argname="argument cdc_max_batch_interval", value=cdc_max_batch_interval, expected_type=type_hints["cdc_max_batch_interval"])
                check_type(argname="argument cdc_min_file_size", value=cdc_min_file_size, expected_type=type_hints["cdc_min_file_size"])
                check_type(argname="argument cdc_path", value=cdc_path, expected_type=type_hints["cdc_path"])
                check_type(argname="argument compression_type", value=compression_type, expected_type=type_hints["compression_type"])
                check_type(argname="argument csv_delimiter", value=csv_delimiter, expected_type=type_hints["csv_delimiter"])
                check_type(argname="argument csv_no_sup_value", value=csv_no_sup_value, expected_type=type_hints["csv_no_sup_value"])
                check_type(argname="argument csv_null_value", value=csv_null_value, expected_type=type_hints["csv_null_value"])
                check_type(argname="argument csv_row_delimiter", value=csv_row_delimiter, expected_type=type_hints["csv_row_delimiter"])
                check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
                check_type(argname="argument data_page_size", value=data_page_size, expected_type=type_hints["data_page_size"])
                check_type(argname="argument date_partition_delimiter", value=date_partition_delimiter, expected_type=type_hints["date_partition_delimiter"])
                check_type(argname="argument date_partition_enabled", value=date_partition_enabled, expected_type=type_hints["date_partition_enabled"])
                check_type(argname="argument date_partition_sequence", value=date_partition_sequence, expected_type=type_hints["date_partition_sequence"])
                check_type(argname="argument date_partition_timezone", value=date_partition_timezone, expected_type=type_hints["date_partition_timezone"])
                check_type(argname="argument dict_page_size_limit", value=dict_page_size_limit, expected_type=type_hints["dict_page_size_limit"])
                check_type(argname="argument enable_statistics", value=enable_statistics, expected_type=type_hints["enable_statistics"])
                check_type(argname="argument encoding_type", value=encoding_type, expected_type=type_hints["encoding_type"])
                check_type(argname="argument encryption_mode", value=encryption_mode, expected_type=type_hints["encryption_mode"])
                check_type(argname="argument expected_bucket_owner", value=expected_bucket_owner, expected_type=type_hints["expected_bucket_owner"])
                check_type(argname="argument external_table_definition", value=external_table_definition, expected_type=type_hints["external_table_definition"])
                check_type(argname="argument glue_catalog_generation", value=glue_catalog_generation, expected_type=type_hints["glue_catalog_generation"])
                check_type(argname="argument ignore_header_rows", value=ignore_header_rows, expected_type=type_hints["ignore_header_rows"])
                check_type(argname="argument include_op_for_full_load", value=include_op_for_full_load, expected_type=type_hints["include_op_for_full_load"])
                check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
                check_type(argname="argument parquet_timestamp_in_millisecond", value=parquet_timestamp_in_millisecond, expected_type=type_hints["parquet_timestamp_in_millisecond"])
                check_type(argname="argument parquet_version", value=parquet_version, expected_type=type_hints["parquet_version"])
                check_type(argname="argument preserve_transactions", value=preserve_transactions, expected_type=type_hints["preserve_transactions"])
                check_type(argname="argument rfc4180", value=rfc4180, expected_type=type_hints["rfc4180"])
                check_type(argname="argument row_group_length", value=row_group_length, expected_type=type_hints["row_group_length"])
                check_type(argname="argument server_side_encryption_kms_key_id", value=server_side_encryption_kms_key_id, expected_type=type_hints["server_side_encryption_kms_key_id"])
                check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
                check_type(argname="argument timestamp_column_name", value=timestamp_column_name, expected_type=type_hints["timestamp_column_name"])
                check_type(argname="argument use_csv_no_sup_value", value=use_csv_no_sup_value, expected_type=type_hints["use_csv_no_sup_value"])
                check_type(argname="argument use_task_start_time_for_full_load_timestamp", value=use_task_start_time_for_full_load_timestamp, expected_type=type_hints["use_task_start_time_for_full_load_timestamp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_column_name is not None:
                self._values["add_column_name"] = add_column_name
            if add_trailing_padding_character is not None:
                self._values["add_trailing_padding_character"] = add_trailing_padding_character
            if bucket_folder is not None:
                self._values["bucket_folder"] = bucket_folder
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if canned_acl_for_objects is not None:
                self._values["canned_acl_for_objects"] = canned_acl_for_objects
            if cdc_inserts_and_updates is not None:
                self._values["cdc_inserts_and_updates"] = cdc_inserts_and_updates
            if cdc_inserts_only is not None:
                self._values["cdc_inserts_only"] = cdc_inserts_only
            if cdc_max_batch_interval is not None:
                self._values["cdc_max_batch_interval"] = cdc_max_batch_interval
            if cdc_min_file_size is not None:
                self._values["cdc_min_file_size"] = cdc_min_file_size
            if cdc_path is not None:
                self._values["cdc_path"] = cdc_path
            if compression_type is not None:
                self._values["compression_type"] = compression_type
            if csv_delimiter is not None:
                self._values["csv_delimiter"] = csv_delimiter
            if csv_no_sup_value is not None:
                self._values["csv_no_sup_value"] = csv_no_sup_value
            if csv_null_value is not None:
                self._values["csv_null_value"] = csv_null_value
            if csv_row_delimiter is not None:
                self._values["csv_row_delimiter"] = csv_row_delimiter
            if data_format is not None:
                self._values["data_format"] = data_format
            if data_page_size is not None:
                self._values["data_page_size"] = data_page_size
            if date_partition_delimiter is not None:
                self._values["date_partition_delimiter"] = date_partition_delimiter
            if date_partition_enabled is not None:
                self._values["date_partition_enabled"] = date_partition_enabled
            if date_partition_sequence is not None:
                self._values["date_partition_sequence"] = date_partition_sequence
            if date_partition_timezone is not None:
                self._values["date_partition_timezone"] = date_partition_timezone
            if dict_page_size_limit is not None:
                self._values["dict_page_size_limit"] = dict_page_size_limit
            if enable_statistics is not None:
                self._values["enable_statistics"] = enable_statistics
            if encoding_type is not None:
                self._values["encoding_type"] = encoding_type
            if encryption_mode is not None:
                self._values["encryption_mode"] = encryption_mode
            if expected_bucket_owner is not None:
                self._values["expected_bucket_owner"] = expected_bucket_owner
            if external_table_definition is not None:
                self._values["external_table_definition"] = external_table_definition
            if glue_catalog_generation is not None:
                self._values["glue_catalog_generation"] = glue_catalog_generation
            if ignore_header_rows is not None:
                self._values["ignore_header_rows"] = ignore_header_rows
            if include_op_for_full_load is not None:
                self._values["include_op_for_full_load"] = include_op_for_full_load
            if max_file_size is not None:
                self._values["max_file_size"] = max_file_size
            if parquet_timestamp_in_millisecond is not None:
                self._values["parquet_timestamp_in_millisecond"] = parquet_timestamp_in_millisecond
            if parquet_version is not None:
                self._values["parquet_version"] = parquet_version
            if preserve_transactions is not None:
                self._values["preserve_transactions"] = preserve_transactions
            if rfc4180 is not None:
                self._values["rfc4180"] = rfc4180
            if row_group_length is not None:
                self._values["row_group_length"] = row_group_length
            if server_side_encryption_kms_key_id is not None:
                self._values["server_side_encryption_kms_key_id"] = server_side_encryption_kms_key_id
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn
            if timestamp_column_name is not None:
                self._values["timestamp_column_name"] = timestamp_column_name
            if use_csv_no_sup_value is not None:
                self._values["use_csv_no_sup_value"] = use_csv_no_sup_value
            if use_task_start_time_for_full_load_timestamp is not None:
                self._values["use_task_start_time_for_full_load_timestamp"] = use_task_start_time_for_full_load_timestamp

        @builtins.property
        def add_column_name(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''An optional parameter that, when set to ``true`` or ``y`` , you can use to add column name information to the .csv output file.

            The default value is ``false`` . Valid values are ``true`` , ``false`` , ``y`` , and ``n`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-addcolumnname
            '''
            result = self._values.get("add_column_name")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def add_trailing_padding_character(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Use the S3 target endpoint setting ``AddTrailingPaddingCharacter`` to add padding on string data.

            The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-addtrailingpaddingcharacter
            '''
            result = self._values.get("add_trailing_padding_character")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def bucket_folder(self) -> typing.Optional[builtins.str]:
            '''An optional parameter to set a folder name in the S3 bucket.

            If provided, tables are created in the path ``*bucketFolder* / *schema_name* / *table_name* /`` . If this parameter isn't specified, the path used is ``*schema_name* / *table_name* /`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-bucketfolder
            '''
            result = self._values.get("bucket_folder")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def canned_acl_for_objects(self) -> typing.Optional[builtins.str]:
            '''A value that enables AWS DMS to specify a predefined (canned) access control list (ACL) for objects created in an Amazon S3 bucket as .csv or .parquet files. For more information about Amazon S3 canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ in the *Amazon S3 Developer Guide* .

            The default value is NONE. Valid values include NONE, PRIVATE, PUBLIC_READ, PUBLIC_READ_WRITE, AUTHENTICATED_READ, AWS_EXEC_READ, BUCKET_OWNER_READ, and BUCKET_OWNER_FULL_CONTROL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cannedaclforobjects
            '''
            result = self._values.get("canned_acl_for_objects")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cdc_inserts_and_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that enables a change data capture (CDC) load to write INSERT and UPDATE operations to .csv or .parquet (columnar storage) output files. The default setting is ``false`` , but when ``CdcInsertsAndUpdates`` is set to ``true`` or ``y`` , only INSERTs and UPDATEs from the source database are migrated to the .csv or .parquet file.

            For .csv file format only, how these INSERTs and UPDATEs are recorded depends on the value of the ``IncludeOpForFullLoad`` parameter. If ``IncludeOpForFullLoad`` is set to ``true`` , the first field of every CDC record is set to either ``I`` or ``U`` to indicate INSERT and UPDATE operations at the source. But if ``IncludeOpForFullLoad`` is set to ``false`` , CDC records are written without an indication of INSERT or UPDATE operations at the source. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* .
            .. epigraph::

               AWS DMS supports the use of the ``CdcInsertsAndUpdates`` parameter in versions 3.3.1 and later.

               ``CdcInsertsOnly`` and ``CdcInsertsAndUpdates`` can't both be set to ``true`` for the same endpoint. Set either ``CdcInsertsOnly`` or ``CdcInsertsAndUpdates`` to ``true`` for the same endpoint, but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcinsertsandupdates
            '''
            result = self._values.get("cdc_inserts_and_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def cdc_inserts_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that enables a change data capture (CDC) load to write only INSERT operations to .csv or columnar storage (.parquet) output files. By default (the ``false`` setting), the first field in a .csv or .parquet record contains the letter I (INSERT), U (UPDATE), or D (DELETE). These values indicate whether the row was inserted, updated, or deleted at the source database for a CDC load to the target.

            If ``CdcInsertsOnly`` is set to ``true`` or ``y`` , only INSERTs from the source database are migrated to the .csv or .parquet file. For .csv format only, how these INSERTs are recorded depends on the value of ``IncludeOpForFullLoad`` . If ``IncludeOpForFullLoad`` is set to ``true`` , the first field of every CDC record is set to I to indicate the INSERT operation at the source. If ``IncludeOpForFullLoad`` is set to ``false`` , every CDC record is written without a first field to indicate the INSERT operation at the source. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* .
            .. epigraph::

               AWS DMS supports the interaction described preceding between the ``CdcInsertsOnly`` and ``IncludeOpForFullLoad`` parameters in versions 3.1.4 and later.

               ``CdcInsertsOnly`` and ``CdcInsertsAndUpdates`` can't both be set to ``true`` for the same endpoint. Set either ``CdcInsertsOnly`` or ``CdcInsertsAndUpdates`` to ``true`` for the same endpoint, but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcinsertsonly
            '''
            result = self._values.get("cdc_inserts_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def cdc_max_batch_interval(self) -> typing.Optional[jsii.Number]:
            '''Maximum length of the interval, defined in seconds, after which to output a file to Amazon S3.

            When ``CdcMaxBatchInterval`` and ``CdcMinFileSize`` are both specified, the file write is triggered by whichever parameter condition is met first within an AWS DMS CloudFormation template.

            The default value is 60 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcmaxbatchinterval
            '''
            result = self._values.get("cdc_max_batch_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def cdc_min_file_size(self) -> typing.Optional[jsii.Number]:
            '''Minimum file size, defined in kilobytes, to reach for a file output to Amazon S3.

            When ``CdcMinFileSize`` and ``CdcMaxBatchInterval`` are both specified, the file write is triggered by whichever parameter condition is met first within an AWS DMS CloudFormation template.

            The default value is 32 MB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcminfilesize
            '''
            result = self._values.get("cdc_min_file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def cdc_path(self) -> typing.Optional[builtins.str]:
            '''Specifies the folder path of CDC files.

            For an S3 source, this setting is required if a task captures change data; otherwise, it's optional. If ``CdcPath`` is set, AWS DMS reads CDC files from this path and replicates the data changes to the target endpoint. For an S3 target if you set ```PreserveTransactions`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-PreserveTransactions>`_ to ``true`` , AWS DMS verifies that you have set this parameter to a folder path on your S3 target where AWS DMS can save the transaction order for the CDC load. AWS DMS creates this CDC folder path in either your S3 target working directory or the S3 target location specified by ```BucketFolder`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketFolder>`_ and ```BucketName`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketName>`_ .

            For example, if you specify ``CdcPath`` as ``MyChangedData`` , and you specify ``BucketName`` as ``MyTargetBucket`` but do not specify ``BucketFolder`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyChangedData`` .

            If you specify the same ``CdcPath`` , and you specify ``BucketName`` as ``MyTargetBucket`` and ``BucketFolder`` as ``MyTargetData`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyTargetData/MyChangedData`` .

            For more information on CDC including transaction order on an S3 target, see `Capturing data changes (CDC) including transaction order on the S3 target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.EndpointSettings.CdcPath>`_ .
            .. epigraph::

               This setting is supported in AWS DMS versions 3.4.2 and later.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcpath
            '''
            result = self._values.get("cdc_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def compression_type(self) -> typing.Optional[builtins.str]:
            '''An optional parameter.

            When set to GZIP it enables the service to compress the target files. To allow the service to write the target files uncompressed, either set this parameter to NONE (the default) or don't specify the parameter at all. This parameter applies to both .csv and .parquet file formats.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-compressiontype
            '''
            result = self._values.get("compression_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def csv_delimiter(self) -> typing.Optional[builtins.str]:
            '''The delimiter used to separate columns in the .csv file for both source and target. The default is a comma.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvdelimiter
            '''
            result = self._values.get("csv_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def csv_no_sup_value(self) -> typing.Optional[builtins.str]:
            '''This setting only applies if your Amazon S3 output files during a change data capture (CDC) load are written in .csv format. If ```UseCsvNoSupValue`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-UseCsvNoSupValue>`_ is set to true, specify a string value that you want AWS DMS to use for all columns not included in the supplemental log. If you do not specify a string value, AWS DMS uses the null value for these columns regardless of the ``UseCsvNoSupValue`` setting.

            .. epigraph::

               This setting is supported in AWS DMS versions 3.4.1 and later.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvnosupvalue
            '''
            result = self._values.get("csv_no_sup_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def csv_null_value(self) -> typing.Optional[builtins.str]:
            '''An optional parameter that specifies how AWS DMS treats null values.

            While handling the null value, you can use this parameter to pass a user-defined string as null when writing to the target. For example, when target columns are not nullable, you can use this option to differentiate between the empty string value and the null value. So, if you set this parameter value to the empty string ("" or ''), AWS DMS treats the empty string as the null value instead of ``NULL`` .

            The default value is ``NULL`` . Valid values include any valid string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvnullvalue
            '''
            result = self._values.get("csv_null_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def csv_row_delimiter(self) -> typing.Optional[builtins.str]:
            '''The delimiter used to separate rows in the .csv file for both source and target.

            The default is a carriage return ( ``\\n`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvrowdelimiter
            '''
            result = self._values.get("csv_row_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_format(self) -> typing.Optional[builtins.str]:
            '''The format of the data that you want to use for output. You can choose one of the following:.

            - ``csv`` : This is a row-based file format with comma-separated values (.csv).
            - ``parquet`` : Apache Parquet (.parquet) is a columnar storage file format that features efficient compression and provides faster query response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-dataformat
            '''
            result = self._values.get("data_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_page_size(self) -> typing.Optional[jsii.Number]:
            '''The size of one data page in bytes.

            This parameter defaults to 1024 * 1024 bytes (1 MiB). This number is used for .parquet file format only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-datapagesize
            '''
            result = self._values.get("data_page_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def date_partition_delimiter(self) -> typing.Optional[builtins.str]:
            '''Specifies a date separating delimiter to use during folder partitioning.

            The default value is ``SLASH`` . Use this parameter when ``DatePartitionedEnabled`` is set to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-datepartitiondelimiter
            '''
            result = self._values.get("date_partition_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def date_partition_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to ``true`` , this parameter partitions S3 bucket folders based on transaction commit dates.

            The default value is ``false`` . For more information about date-based folder partitioning, see `Using date-based folder partitioning <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.DatePartitioning>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-datepartitionenabled
            '''
            result = self._values.get("date_partition_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def date_partition_sequence(self) -> typing.Optional[builtins.str]:
            '''Identifies the sequence of the date format to use during folder partitioning.

            The default value is ``YYYYMMDD`` . Use this parameter when ``DatePartitionedEnabled`` is set to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-datepartitionsequence
            '''
            result = self._values.get("date_partition_sequence")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def date_partition_timezone(self) -> typing.Optional[builtins.str]:
            '''When creating an S3 target endpoint, set ``DatePartitionTimezone`` to convert the current UTC time into a specified time zone.

            The conversion occurs when a date partition folder is created and a change data capture (CDC) file name is generated. The time zone format is Area/Location. Use this parameter when ``DatePartitionedEnabled`` is set to ``true`` , as shown in the following example.

            ``s3-settings='{"DatePartitionEnabled": true, "DatePartitionSequence": "YYYYMMDDHH", "DatePartitionDelimiter": "SLASH", "DatePartitionTimezone":" *Asia/Seoul* ", "BucketName": "dms-nattarat-test"}'``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-datepartitiontimezone
            '''
            result = self._values.get("date_partition_timezone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dict_page_size_limit(self) -> typing.Optional[jsii.Number]:
            '''The maximum size of an encoded dictionary page of a column.

            If the dictionary page exceeds this, this column is stored using an encoding type of ``PLAIN`` . This parameter defaults to 1024 * 1024 bytes (1 MiB), the maximum size of a dictionary page before it reverts to ``PLAIN`` encoding. This size is used for .parquet file format only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-dictpagesizelimit
            '''
            result = self._values.get("dict_page_size_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enable_statistics(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that enables statistics for Parquet pages and row groups.

            Choose ``true`` to enable statistics, ``false`` to disable. Statistics include ``NULL`` , ``DISTINCT`` , ``MAX`` , and ``MIN`` values. This parameter defaults to ``true`` . This value is used for .parquet file format only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-enablestatistics
            '''
            result = self._values.get("enable_statistics")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encoding_type(self) -> typing.Optional[builtins.str]:
            '''The type of encoding that you're using:.

            - ``RLE_DICTIONARY`` uses a combination of bit-packing and run-length encoding to store repeated values more efficiently. This is the default.
            - ``PLAIN`` doesn't use encoding at all. Values are stored as they are.
            - ``PLAIN_DICTIONARY`` builds a dictionary of the values encountered in a given column. The dictionary is stored in a dictionary page for each column chunk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-encodingtype
            '''
            result = self._values.get("encoding_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_mode(self) -> typing.Optional[builtins.str]:
            '''The type of server-side encryption that you want to use for your data.

            This encryption type is part of the endpoint settings or the extra connections attributes for Amazon S3. You can choose either ``SSE_S3`` (the default) or ``SSE_KMS`` .
            .. epigraph::

               For the ``ModifyEndpoint`` operation, you can change the existing value of the ``EncryptionMode`` parameter from ``SSE_KMS`` to ``SSE_S3`` . But you can’t change the existing value from ``SSE_S3`` to ``SSE_KMS`` .

            To use ``SSE_S3`` , you need an IAM role with permission to allow ``"arn:aws:s3:::dms-*"`` to use the following actions:

            - ``s3:CreateBucket``
            - ``s3:ListBucket``
            - ``s3:DeleteBucket``
            - ``s3:GetBucketLocation``
            - ``s3:GetObject``
            - ``s3:PutObject``
            - ``s3:DeleteObject``
            - ``s3:GetObjectVersion``
            - ``s3:GetBucketPolicy``
            - ``s3:PutBucketPolicy``
            - ``s3:DeleteBucketPolicy``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-encryptionmode
            '''
            result = self._values.get("encryption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expected_bucket_owner(self) -> typing.Optional[builtins.str]:
            '''To specify a bucket owner and prevent sniping, you can use the ``ExpectedBucketOwner`` endpoint setting.

            Example: ``--s3-settings='{"ExpectedBucketOwner": " *AWS_Account_ID* "}'``

            When you make a request to test a connection or perform a migration, S3 checks the account ID of the bucket owner against the specified parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-expectedbucketowner
            '''
            result = self._values.get("expected_bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_table_definition(self) -> typing.Optional[builtins.str]:
            '''The external table definition.

            Conditional: If ``S3`` is used as a source then ``ExternalTableDefinition`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-externaltabledefinition
            '''
            result = self._values.get("external_table_definition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def glue_catalog_generation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true, allows AWS Glue to catalog your S3 bucket.

            Creating an AWS Glue catalog lets you use Athena to query your data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-gluecataloggeneration
            '''
            result = self._values.get("glue_catalog_generation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ignore_header_rows(self) -> typing.Optional[jsii.Number]:
            '''When this value is set to 1, AWS DMS ignores the first row header in a .csv file. A value of 1 turns on the feature; a value of 0 turns off the feature.

            The default is 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-ignoreheaderrows
            '''
            result = self._values.get("ignore_header_rows")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def include_op_for_full_load(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that enables a full load to write INSERT operations to the comma-separated value (.csv) output files only to indicate how the rows were added to the source database.

            .. epigraph::

               AWS DMS supports the ``IncludeOpForFullLoad`` parameter in versions 3.1.4 and later.

            For full load, records can only be inserted. By default (the ``false`` setting), no information is recorded in these output files for a full load to indicate that the rows were inserted at the source database. If ``IncludeOpForFullLoad`` is set to ``true`` or ``y`` , the INSERT is recorded as an I annotation in the first field of the .csv file. This allows the format of your target records from a full load to be consistent with the target records from a CDC load.
            .. epigraph::

               This setting works together with the ``CdcInsertsOnly`` and the ``CdcInsertsAndUpdates`` parameters for output to .csv files only. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-includeopforfullload
            '''
            result = self._values.get("include_op_for_full_load")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_file_size(self) -> typing.Optional[jsii.Number]:
            '''A value that specifies the maximum size (in KB) of any .csv file to be created while migrating to an S3 target during full load.

            The default value is 1,048,576 KB (1 GB). Valid values include 1 to 1,048,576.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-maxfilesize
            '''
            result = self._values.get("max_file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def parquet_timestamp_in_millisecond(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that specifies the precision of any ``TIMESTAMP`` column values that are written to an Amazon S3 object file in .parquet format.

            .. epigraph::

               AWS DMS supports the ``ParquetTimestampInMillisecond`` parameter in versions 3.1.4 and later.

            When ``ParquetTimestampInMillisecond`` is set to ``true`` or ``y`` , AWS DMS writes all ``TIMESTAMP`` columns in a .parquet formatted file with millisecond precision. Otherwise, DMS writes them with microsecond precision.

            Currently, Amazon Athena and AWS Glue can handle only millisecond precision for ``TIMESTAMP`` values. Set this parameter to ``true`` for S3 endpoint object files that are .parquet formatted only if you plan to query or process the data with Athena or AWS Glue .
            .. epigraph::

               AWS DMS writes any ``TIMESTAMP`` column values written to an S3 file in .csv format with microsecond precision.

               Setting ``ParquetTimestampInMillisecond`` has no effect on the string format of the timestamp column value that is inserted by setting the ``TimestampColumnName`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-parquettimestampinmillisecond
            '''
            result = self._values.get("parquet_timestamp_in_millisecond")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def parquet_version(self) -> typing.Optional[builtins.str]:
            '''The version of the Apache Parquet format that you want to use: ``parquet_1_0`` (the default) or ``parquet_2_0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-parquetversion
            '''
            result = self._values.get("parquet_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preserve_transactions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If this setting is set to ``true`` , AWS DMS saves the transaction order for a change data capture (CDC) load on the Amazon S3 target specified by ```CdcPath`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-CdcPath>`_ . For more information, see `Capturing data changes (CDC) including transaction order on the S3 target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.EndpointSettings.CdcPath>`_ .

            .. epigraph::

               This setting is supported in AWS DMS versions 3.4.2 and later.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-preservetransactions
            '''
            result = self._values.get("preserve_transactions")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def rfc4180(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''For an S3 source, when this value is set to ``true`` or ``y`` , each leading double quotation mark has to be followed by an ending double quotation mark.

            This formatting complies with RFC 4180. When this value is set to ``false`` or ``n`` , string literals are copied to the target as is. In this case, a delimiter (row or column) signals the end of the field. Thus, you can't use a delimiter as part of the string, because it signals the end of the value.

            For an S3 target, an optional parameter used to set behavior to comply with RFC 4180 for data migrated to Amazon S3 using .csv file format only. When this value is set to ``true`` or ``y`` using Amazon S3 as a target, if the data has quotation marks or newline characters in it, AWS DMS encloses the entire column with an additional pair of double quotation marks ("). Every quotation mark within the data is repeated twice.

            The default value is ``true`` . Valid values include ``true`` , ``false`` , ``y`` , and ``n`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-rfc4180
            '''
            result = self._values.get("rfc4180")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def row_group_length(self) -> typing.Optional[jsii.Number]:
            '''The number of rows in a row group.

            A smaller row group size provides faster reads. But as the number of row groups grows, the slower writes become. This parameter defaults to 10,000 rows. This number is used for .parquet file format only.

            If you choose a value larger than the maximum, ``RowGroupLength`` is set to the max row group length in bytes (64 * 1024 * 1024).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-rowgrouplength
            '''
            result = self._values.get("row_group_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_side_encryption_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''If you are using ``SSE_KMS`` for the ``EncryptionMode`` , provide the AWS  key ID.

            The key that you use needs an attached policy that enables IAM user permissions and allows use of the key.

            Here is a CLI example: ``aws dms create-endpoint --endpoint-identifier *value* --endpoint-type target --engine-name s3 --s3-settings ServiceAccessRoleArn= *value* ,BucketFolder= *value* ,BucketName= *value* ,EncryptionMode=SSE_KMS,ServerSideEncryptionKmsKeyId= *value*``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-serversideencryptionkmskeyid
            '''
            result = self._values.get("server_side_encryption_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''A required parameter that specifies the Amazon Resource Name (ARN) used by the service to access the IAM role.

            The role must allow the ``iam:PassRole`` action. It enables AWS DMS to read and write objects from an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-serviceaccessrolearn
            '''
            result = self._values.get("service_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp_column_name(self) -> typing.Optional[builtins.str]:
            '''A value that when nonblank causes AWS DMS to add a column with timestamp information to the endpoint data for an Amazon S3 target.

            .. epigraph::

               AWS DMS supports the ``TimestampColumnName`` parameter in versions 3.1.4 and later.

            AWS DMS includes an additional ``STRING`` column in the .csv or .parquet object files of your migrated data when you set ``TimestampColumnName`` to a nonblank value.

            For a full load, each row of this timestamp column contains a timestamp for when the data was transferred from the source to the target by DMS.

            For a change data capture (CDC) load, each row of the timestamp column contains the timestamp for the commit of that row in the source database.

            The string format for this timestamp column value is ``yyyy-MM-dd HH:mm:ss.SSSSSS`` . By default, the precision of this value is in microseconds. For a CDC load, the rounding of the precision depends on the commit timestamp supported by DMS for the source database.

            When the ``AddColumnName`` parameter is set to ``true`` , DMS also includes a name for the timestamp column that you set with ``TimestampColumnName`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-timestampcolumnname
            '''
            result = self._values.get("timestamp_column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_csv_no_sup_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This setting applies if the S3 output files during a change data capture (CDC) load are written in .csv format. If this setting is set to ``true`` for columns not included in the supplemental log, AWS DMS uses the value specified by ```CsvNoSupValue`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-CsvNoSupValue>`_ . If this setting isn't set or is set to ``false`` , AWS DMS uses the null value for these columns.

            .. epigraph::

               This setting is supported in AWS DMS versions 3.4.1 and later.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-usecsvnosupvalue
            '''
            result = self._values.get("use_csv_no_sup_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_task_start_time_for_full_load_timestamp(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to true, this parameter uses the task start time as the timestamp column value instead of the time data is written to target.

            For full load, when ``useTaskStartTimeForFullLoadTimestamp`` is set to ``true`` , each row of the timestamp column contains the task start time. For CDC loads, each row of the timestamp column contains the transaction commit time.

            When ``useTaskStartTimeForFullLoadTimestamp`` is set to ``false`` , the full load timestamp in the timestamp column increments with the time data arrives at the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-usetaskstarttimeforfullloadtimestamp
            '''
            result = self._values.get("use_task_start_time_for_full_load_timestamp")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3SettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEndpointPropsMixin.SybaseSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_secret_id": "secretsManagerSecretId",
        },
    )
    class SybaseSettingsProperty:
        def __init__(
            self,
            *,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that defines a SAP ASE endpoint.

            This information includes the output format of records applied to the endpoint and details of transaction and control table data information. For information about other available settings, see `Extra connection attributes when using SAP ASE as a source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.SAP.html#CHAP_Source.SAP.ConnectionAttrib>`_ and `Extra connection attributes when using SAP ASE as a target for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.SAP.html#CHAP_Target.SAP.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

            :param secrets_manager_access_role_arn: The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` . The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the SAP ASE endpoint. .. epigraph:: You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both. For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .
            :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the SAP SAE endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-sybasesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                sybase_settings_property = dms_mixins.CfnEndpointPropsMixin.SybaseSettingsProperty(
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__62c24e5b733f7f0d1e946e1431ee5c7492eafa9ab9dcaf7be77890862ce56029)
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The full Amazon Resource Name (ARN) of the IAM role that specifies AWS DMS as the trusted entity and grants the required permissions to access the value in ``SecretsManagerSecret`` .

            The role must allow the ``iam:PassRole`` action. ``SecretsManagerSecret`` has the value of the AWS Secrets Manager secret that allows access to the SAP ASE endpoint.
            .. epigraph::

               You can specify one of two sets of values for these permissions. You can specify the values for this setting and ``SecretsManagerSecretId`` . Or you can specify clear-text values for ``UserName`` , ``Password`` , ``ServerName`` , and ``Port`` . You can't specify both.

               For more information on creating this ``SecretsManagerSecret`` , the corresponding ``SecretsManagerAccessRoleArn`` , and the ``SecretsManagerSecretId`` that is required to access it, see `Using secrets to access AWS Database Migration Service resources <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#security-iam-secretsmanager>`_ in the *AWS Database Migration Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-sybasesettings.html#cfn-dms-endpoint-sybasesettings-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the SAP SAE endpoint connection details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-sybasesettings.html#cfn-dms-endpoint-sybasesettings-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SybaseSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEventSubscriptionMixinProps",
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

        :param enabled: Indicates whether to activate the subscription. If you don't specify this property, CloudFormation activates the subscription.
        :param event_categories: A list of event categories for a source type that you want to subscribe to. If you don't specify this property, you are notified about all event categories. For more information, see `Working with Events and Notifications <https://docs.aws.amazon.com//dms/latest/userguide/CHAP_Events.html>`_ in the *AWS DMS User Guide* .
        :param sns_topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic created for event notification. The ARN is created by Amazon SNS when you create a topic and subscribe to it.
        :param source_ids: A list of identifiers for which AWS DMS provides notification events. If you don't specify a value, notifications are provided for all sources. If you specify multiple values, they must be of the same type. For example, if you specify a database instance ID, then all of the other values must be database instance IDs.
        :param source_type: The type of AWS DMS resource that generates the events. For example, if you want to be notified of events generated by a replication instance, you set this parameter to ``replication-instance`` . If this value isn't specified, all events are returned. *Valid values* : ``replication-instance`` | ``replication-task``
        :param subscription_name: The name of the AWS DMS event notification subscription. This name must be less than 255 characters.
        :param tags: One or more tags to be assigned to the event subscription.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            cfn_event_subscription_mixin_props = dms_mixins.CfnEventSubscriptionMixinProps(
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac00da3548a0afa219f29ba69252956da60483eb5cda8543b983a29e2b637329)
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
        '''Indicates whether to activate the subscription.

        If you don't specify this property, CloudFormation activates the subscription.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def event_categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of event categories for a source type that you want to subscribe to.

        If you don't specify this property, you are notified about all event categories. For more information, see `Working with Events and Notifications <https://docs.aws.amazon.com//dms/latest/userguide/CHAP_Events.html>`_ in the *AWS DMS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-eventcategories
        '''
        result = self._values.get("event_categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic created for event notification.

        The ARN is created by Amazon SNS when you create a topic and subscribe to it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-snstopicarn
        '''
        result = self._values.get("sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of identifiers for which AWS DMS provides notification events.

        If you don't specify a value, notifications are provided for all sources.

        If you specify multiple values, they must be of the same type. For example, if you specify a database instance ID, then all of the other values must be database instance IDs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-sourceids
        '''
        result = self._values.get("source_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_type(self) -> typing.Optional[builtins.str]:
        '''The type of AWS DMS resource that generates the events.

        For example, if you want to be notified of events generated by a replication instance, you set this parameter to ``replication-instance`` . If this value isn't specified, all events are returned.

        *Valid values* : ``replication-instance`` | ``replication-task``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-sourcetype
        '''
        result = self._values.get("source_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_name(self) -> typing.Optional[builtins.str]:
        '''The name of the AWS DMS event notification subscription.

        This name must be less than 255 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-subscriptionname
        '''
        result = self._values.get("subscription_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more tags to be assigned to the event subscription.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnEventSubscriptionPropsMixin",
):
    '''Use the ``AWS::DMS::EventSubscription`` resource to get notifications for AWS Database Migration Service events through the Amazon Simple Notification Service .

    For more information, see `Working with events and notifications in AWS Database Migration Service <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Events.html>`_ in the *AWS Database Migration Service User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html
    :cloudformationResource: AWS::DMS::EventSubscription
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        cfn_event_subscription_props_mixin = dms_mixins.CfnEventSubscriptionPropsMixin(dms_mixins.CfnEventSubscriptionMixinProps(
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
        '''Create a mixin to apply properties to ``AWS::DMS::EventSubscription``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a013588cfd17d4e203568f869048f3975534ed0d277dd3f16872c4b60b05784a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0647b49d8cc5318e90498c0d1c3e4182c78a4ecb975ae0d3425d3c771c1918de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a231fc1a057af8e51d08e588cb945e8c0d63d5128f2260a859ab34f9663fbf)
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
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnInstanceProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "description": "description",
        "instance_profile_identifier": "instanceProfileIdentifier",
        "instance_profile_name": "instanceProfileName",
        "kms_key_arn": "kmsKeyArn",
        "network_type": "networkType",
        "publicly_accessible": "publiclyAccessible",
        "subnet_group_identifier": "subnetGroupIdentifier",
        "tags": "tags",
        "vpc_security_groups": "vpcSecurityGroups",
    },
)
class CfnInstanceProfileMixinProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        instance_profile_identifier: typing.Optional[builtins.str] = None,
        instance_profile_name: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        subnet_group_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnInstanceProfilePropsMixin.

        :param availability_zone: The Availability Zone where the instance profile runs.
        :param description: A description of the instance profile. Descriptions can have up to 31 characters. A description can contain only ASCII letters, digits, and hyphens ('-'). Also, it can't end with a hyphen or contain two consecutive hyphens, and can only begin with a letter.
        :param instance_profile_identifier: The identifier of the instance profile. Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.
        :param instance_profile_name: The user-friendly name for the instance profile.
        :param kms_key_arn: The Amazon Resource Name (ARN) of the AWS key that is used to encrypt the connection parameters for the instance profile. If you don't specify a value for the ``KmsKeyArn`` parameter, then AWS DMS uses an AWS owned encryption key to encrypt your resources.
        :param network_type: Specifies the network type for the instance profile. A value of ``IPV4`` represents an instance profile with IPv4 network type and only supports IPv4 addressing. A value of ``IPV6`` represents an instance profile with IPv6 network type and only supports IPv6 addressing. A value of ``DUAL`` represents an instance profile with dual network type that supports IPv4 and IPv6 addressing.
        :param publicly_accessible: Specifies the accessibility options for the instance profile. A value of ``true`` represents an instance profile with a public IP address. A value of ``false`` represents an instance profile with a private IP address. The default value is ``true`` . Default: - false
        :param subnet_group_identifier: The identifier of the subnet group that is associated with the instance profile.
        :param tags: An array of key-value pairs to apply to this resource.
        :param vpc_security_groups: The VPC security groups that are used with the instance profile. The VPC security group must work with the VPC containing the instance profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            cfn_instance_profile_mixin_props = dms_mixins.CfnInstanceProfileMixinProps(
                availability_zone="availabilityZone",
                description="description",
                instance_profile_identifier="instanceProfileIdentifier",
                instance_profile_name="instanceProfileName",
                kms_key_arn="kmsKeyArn",
                network_type="networkType",
                publicly_accessible=False,
                subnet_group_identifier="subnetGroupIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_security_groups=["vpcSecurityGroups"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3ef36481270e451e68307a84256acf375ed5e99c929040304cbe5f3def2d73)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_profile_identifier", value=instance_profile_identifier, expected_type=type_hints["instance_profile_identifier"])
            check_type(argname="argument instance_profile_name", value=instance_profile_name, expected_type=type_hints["instance_profile_name"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument subnet_group_identifier", value=subnet_group_identifier, expected_type=type_hints["subnet_group_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_security_groups", value=vpc_security_groups, expected_type=type_hints["vpc_security_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if description is not None:
            self._values["description"] = description
        if instance_profile_identifier is not None:
            self._values["instance_profile_identifier"] = instance_profile_identifier
        if instance_profile_name is not None:
            self._values["instance_profile_name"] = instance_profile_name
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if network_type is not None:
            self._values["network_type"] = network_type
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if subnet_group_identifier is not None:
            self._values["subnet_group_identifier"] = subnet_group_identifier
        if tags is not None:
            self._values["tags"] = tags
        if vpc_security_groups is not None:
            self._values["vpc_security_groups"] = vpc_security_groups

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone where the instance profile runs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html#cfn-dms-instanceprofile-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the instance profile.

        Descriptions can have up to 31 characters. A description can contain only ASCII letters, digits, and hyphens ('-'). Also, it can't end with a hyphen or contain two consecutive hyphens, and can only begin with a letter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html#cfn-dms-instanceprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_profile_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the instance profile.

        Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html#cfn-dms-instanceprofile-instanceprofileidentifier
        '''
        result = self._values.get("instance_profile_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_profile_name(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name for the instance profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html#cfn-dms-instanceprofile-instanceprofilename
        '''
        result = self._values.get("instance_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS  key that is used to encrypt the connection parameters for the instance profile.

        If you don't specify a value for the ``KmsKeyArn`` parameter, then AWS DMS uses an AWS owned encryption key to encrypt your resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html#cfn-dms-instanceprofile-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the network type for the instance profile.

        A value of ``IPV4`` represents an instance profile with IPv4 network type and only supports IPv4 addressing. A value of ``IPV6`` represents an instance profile with IPv6 network type and only supports IPv6 addressing. A value of ``DUAL`` represents an instance profile with dual network type that supports IPv4 and IPv6 addressing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html#cfn-dms-instanceprofile-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies the accessibility options for the instance profile.

        A value of ``true`` represents an instance profile with a public IP address. A value of ``false`` represents an instance profile with a private IP address. The default value is ``true`` .

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html#cfn-dms-instanceprofile-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def subnet_group_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the subnet group that is associated with the instance profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html#cfn-dms-instanceprofile-subnetgroupidentifier
        '''
        result = self._values.get("subnet_group_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html#cfn-dms-instanceprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The VPC security groups that are used with the instance profile.

        The VPC security group must work with the VPC containing the instance profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html#cfn-dms-instanceprofile-vpcsecuritygroups
        '''
        result = self._values.get("vpc_security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstanceProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnInstanceProfilePropsMixin",
):
    '''Provides information that defines an instance profile.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-instanceprofile.html
    :cloudformationResource: AWS::DMS::InstanceProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        cfn_instance_profile_props_mixin = dms_mixins.CfnInstanceProfilePropsMixin(dms_mixins.CfnInstanceProfileMixinProps(
            availability_zone="availabilityZone",
            description="description",
            instance_profile_identifier="instanceProfileIdentifier",
            instance_profile_name="instanceProfileName",
            kms_key_arn="kmsKeyArn",
            network_type="networkType",
            publicly_accessible=False,
            subnet_group_identifier="subnetGroupIdentifier",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_security_groups=["vpcSecurityGroups"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInstanceProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DMS::InstanceProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c22fd11d61f0b6c03bafe36f7fd87b98fbe6551f9b88c369de096f7585f9cd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__def172694a05f4fbe454d4ba91fd398339500e03310cb259f4152950eb87f7e8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87de77a2832e8bafcc05a3611c6f254e5c71a451d98e4b8295e76904ba5e04c3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceProfileMixinProps:
        return typing.cast(CfnInstanceProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnMigrationProjectMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "instance_profile_arn": "instanceProfileArn",
        "instance_profile_identifier": "instanceProfileIdentifier",
        "instance_profile_name": "instanceProfileName",
        "migration_project_creation_time": "migrationProjectCreationTime",
        "migration_project_identifier": "migrationProjectIdentifier",
        "migration_project_name": "migrationProjectName",
        "schema_conversion_application_attributes": "schemaConversionApplicationAttributes",
        "source_data_provider_descriptors": "sourceDataProviderDescriptors",
        "tags": "tags",
        "target_data_provider_descriptors": "targetDataProviderDescriptors",
        "transformation_rules": "transformationRules",
    },
)
class CfnMigrationProjectMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        instance_profile_arn: typing.Optional[builtins.str] = None,
        instance_profile_identifier: typing.Optional[builtins.str] = None,
        instance_profile_name: typing.Optional[builtins.str] = None,
        migration_project_creation_time: typing.Optional[builtins.str] = None,
        migration_project_identifier: typing.Optional[builtins.str] = None,
        migration_project_name: typing.Optional[builtins.str] = None,
        schema_conversion_application_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMigrationProjectPropsMixin.SchemaConversionApplicationAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_data_provider_descriptors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_data_provider_descriptors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        transformation_rules: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMigrationProjectPropsMixin.

        :param description: A user-friendly description of the migration project.
        :param instance_profile_arn: The Amazon Resource Name (ARN) of the instance profile for your migration project.
        :param instance_profile_identifier: The identifier of the instance profile for your migration project.
        :param instance_profile_name: The name of the associated instance profile.
        :param migration_project_creation_time: (deprecated) The property describes a creating time of the migration project.
        :param migration_project_identifier: The identifier of the migration project. Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.
        :param migration_project_name: The name of the migration project.
        :param schema_conversion_application_attributes: The schema conversion application attributes, including the Amazon S3 bucket name and Amazon S3 role ARN.
        :param source_data_provider_descriptors: Information about the source data provider, including the name or ARN, and AWS Secrets Manager parameters.
        :param tags: An array of key-value pairs to apply to this resource.
        :param target_data_provider_descriptors: Information about the target data provider, including the name or ARN, and AWS Secrets Manager parameters.
        :param transformation_rules: The settings in JSON format for migration rules. Migration rules make it possible for you to change the object names according to the rules that you specify. For example, you can change an object name to lowercase or uppercase, add or remove a prefix or suffix, or rename objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            cfn_migration_project_mixin_props = dms_mixins.CfnMigrationProjectMixinProps(
                description="description",
                instance_profile_arn="instanceProfileArn",
                instance_profile_identifier="instanceProfileIdentifier",
                instance_profile_name="instanceProfileName",
                migration_project_creation_time="migrationProjectCreationTime",
                migration_project_identifier="migrationProjectIdentifier",
                migration_project_name="migrationProjectName",
                schema_conversion_application_attributes=dms_mixins.CfnMigrationProjectPropsMixin.SchemaConversionApplicationAttributesProperty(
                    s3_bucket_path="s3BucketPath",
                    s3_bucket_role_arn="s3BucketRoleArn"
                ),
                source_data_provider_descriptors=[dms_mixins.CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty(
                    data_provider_arn="dataProviderArn",
                    data_provider_identifier="dataProviderIdentifier",
                    data_provider_name="dataProviderName",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_data_provider_descriptors=[dms_mixins.CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty(
                    data_provider_arn="dataProviderArn",
                    data_provider_identifier="dataProviderIdentifier",
                    data_provider_name="dataProviderName",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId"
                )],
                transformation_rules="transformationRules"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf8990bdecb2213bb0145bd4157e6eaa6f46612b78973639baa937d8d007071)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_profile_arn", value=instance_profile_arn, expected_type=type_hints["instance_profile_arn"])
            check_type(argname="argument instance_profile_identifier", value=instance_profile_identifier, expected_type=type_hints["instance_profile_identifier"])
            check_type(argname="argument instance_profile_name", value=instance_profile_name, expected_type=type_hints["instance_profile_name"])
            check_type(argname="argument migration_project_creation_time", value=migration_project_creation_time, expected_type=type_hints["migration_project_creation_time"])
            check_type(argname="argument migration_project_identifier", value=migration_project_identifier, expected_type=type_hints["migration_project_identifier"])
            check_type(argname="argument migration_project_name", value=migration_project_name, expected_type=type_hints["migration_project_name"])
            check_type(argname="argument schema_conversion_application_attributes", value=schema_conversion_application_attributes, expected_type=type_hints["schema_conversion_application_attributes"])
            check_type(argname="argument source_data_provider_descriptors", value=source_data_provider_descriptors, expected_type=type_hints["source_data_provider_descriptors"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_data_provider_descriptors", value=target_data_provider_descriptors, expected_type=type_hints["target_data_provider_descriptors"])
            check_type(argname="argument transformation_rules", value=transformation_rules, expected_type=type_hints["transformation_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if instance_profile_arn is not None:
            self._values["instance_profile_arn"] = instance_profile_arn
        if instance_profile_identifier is not None:
            self._values["instance_profile_identifier"] = instance_profile_identifier
        if instance_profile_name is not None:
            self._values["instance_profile_name"] = instance_profile_name
        if migration_project_creation_time is not None:
            self._values["migration_project_creation_time"] = migration_project_creation_time
        if migration_project_identifier is not None:
            self._values["migration_project_identifier"] = migration_project_identifier
        if migration_project_name is not None:
            self._values["migration_project_name"] = migration_project_name
        if schema_conversion_application_attributes is not None:
            self._values["schema_conversion_application_attributes"] = schema_conversion_application_attributes
        if source_data_provider_descriptors is not None:
            self._values["source_data_provider_descriptors"] = source_data_provider_descriptors
        if tags is not None:
            self._values["tags"] = tags
        if target_data_provider_descriptors is not None:
            self._values["target_data_provider_descriptors"] = target_data_provider_descriptors
        if transformation_rules is not None:
            self._values["transformation_rules"] = transformation_rules

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A user-friendly description of the migration project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_profile_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance profile for your migration project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-instanceprofilearn
        '''
        result = self._values.get("instance_profile_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_profile_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the instance profile for your migration project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-instanceprofileidentifier
        '''
        result = self._values.get("instance_profile_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_profile_name(self) -> typing.Optional[builtins.str]:
        '''The name of the associated instance profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-instanceprofilename
        '''
        result = self._values.get("instance_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def migration_project_creation_time(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The property describes a creating time of the migration project.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-migrationprojectcreationtime
        :stability: deprecated
        '''
        result = self._values.get("migration_project_creation_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def migration_project_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the migration project.

        Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-migrationprojectidentifier
        '''
        result = self._values.get("migration_project_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def migration_project_name(self) -> typing.Optional[builtins.str]:
        '''The name of the migration project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-migrationprojectname
        '''
        result = self._values.get("migration_project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_conversion_application_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMigrationProjectPropsMixin.SchemaConversionApplicationAttributesProperty"]]:
        '''The schema conversion application attributes, including the Amazon S3 bucket name and Amazon S3 role ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-schemaconversionapplicationattributes
        '''
        result = self._values.get("schema_conversion_application_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMigrationProjectPropsMixin.SchemaConversionApplicationAttributesProperty"]], result)

    @builtins.property
    def source_data_provider_descriptors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty"]]]]:
        '''Information about the source data provider, including the name or ARN, and AWS Secrets Manager parameters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-sourcedataproviderdescriptors
        '''
        result = self._values.get("source_data_provider_descriptors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_data_provider_descriptors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty"]]]]:
        '''Information about the target data provider, including the name or ARN, and AWS Secrets Manager parameters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-targetdataproviderdescriptors
        '''
        result = self._values.get("target_data_provider_descriptors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty"]]]], result)

    @builtins.property
    def transformation_rules(self) -> typing.Optional[builtins.str]:
        '''The settings in JSON format for migration rules.

        Migration rules make it possible for you to change the object names according to the rules that you specify. For example, you can change an object name to lowercase or uppercase, add or remove a prefix or suffix, or rename objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html#cfn-dms-migrationproject-transformationrules
        '''
        result = self._values.get("transformation_rules")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMigrationProjectMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMigrationProjectPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnMigrationProjectPropsMixin",
):
    '''Provides information that defines a migration project.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-migrationproject.html
    :cloudformationResource: AWS::DMS::MigrationProject
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        cfn_migration_project_props_mixin = dms_mixins.CfnMigrationProjectPropsMixin(dms_mixins.CfnMigrationProjectMixinProps(
            description="description",
            instance_profile_arn="instanceProfileArn",
            instance_profile_identifier="instanceProfileIdentifier",
            instance_profile_name="instanceProfileName",
            migration_project_creation_time="migrationProjectCreationTime",
            migration_project_identifier="migrationProjectIdentifier",
            migration_project_name="migrationProjectName",
            schema_conversion_application_attributes=dms_mixins.CfnMigrationProjectPropsMixin.SchemaConversionApplicationAttributesProperty(
                s3_bucket_path="s3BucketPath",
                s3_bucket_role_arn="s3BucketRoleArn"
            ),
            source_data_provider_descriptors=[dms_mixins.CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty(
                data_provider_arn="dataProviderArn",
                data_provider_identifier="dataProviderIdentifier",
                data_provider_name="dataProviderName",
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_data_provider_descriptors=[dms_mixins.CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty(
                data_provider_arn="dataProviderArn",
                data_provider_identifier="dataProviderIdentifier",
                data_provider_name="dataProviderName",
                secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                secrets_manager_secret_id="secretsManagerSecretId"
            )],
            transformation_rules="transformationRules"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMigrationProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DMS::MigrationProject``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8934ec44c8ff24c57609ea12ca75e4eef87828d4239f134d7a0c7175e6d89b89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad76f390f976ead30afbfb362c54b9f07300328ccff295c917564a42b7c5aa35)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3048d29f27869462b1b0ddda911a766d6cb10b085a2f70790b3e6a010e26ad78)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMigrationProjectMixinProps:
        return typing.cast(CfnMigrationProjectMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_provider_arn": "dataProviderArn",
            "data_provider_identifier": "dataProviderIdentifier",
            "data_provider_name": "dataProviderName",
            "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
            "secrets_manager_secret_id": "secretsManagerSecretId",
        },
    )
    class DataProviderDescriptorProperty:
        def __init__(
            self,
            *,
            data_provider_arn: typing.Optional[builtins.str] = None,
            data_provider_identifier: typing.Optional[builtins.str] = None,
            data_provider_name: typing.Optional[builtins.str] = None,
            secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
            secrets_manager_secret_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a data provider.

            :param data_provider_arn: The Amazon Resource Name (ARN) of the data provider.
            :param data_provider_identifier: 
            :param data_provider_name: The user-friendly name of the data provider.
            :param secrets_manager_access_role_arn: The ARN of the role used to access AWS Secrets Manager.
            :param secrets_manager_secret_id: The identifier of the AWS Secrets Manager Secret used to store access credentials for the data provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-migrationproject-dataproviderdescriptor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                data_provider_descriptor_property = dms_mixins.CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty(
                    data_provider_arn="dataProviderArn",
                    data_provider_identifier="dataProviderIdentifier",
                    data_provider_name="dataProviderName",
                    secrets_manager_access_role_arn="secretsManagerAccessRoleArn",
                    secrets_manager_secret_id="secretsManagerSecretId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__acde54536e87acdd3e7c114fb4b0c0504525cd8b12cff978dbc8befd54e73f50)
                check_type(argname="argument data_provider_arn", value=data_provider_arn, expected_type=type_hints["data_provider_arn"])
                check_type(argname="argument data_provider_identifier", value=data_provider_identifier, expected_type=type_hints["data_provider_identifier"])
                check_type(argname="argument data_provider_name", value=data_provider_name, expected_type=type_hints["data_provider_name"])
                check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
                check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_provider_arn is not None:
                self._values["data_provider_arn"] = data_provider_arn
            if data_provider_identifier is not None:
                self._values["data_provider_identifier"] = data_provider_identifier
            if data_provider_name is not None:
                self._values["data_provider_name"] = data_provider_name
            if secrets_manager_access_role_arn is not None:
                self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
            if secrets_manager_secret_id is not None:
                self._values["secrets_manager_secret_id"] = secrets_manager_secret_id

        @builtins.property
        def data_provider_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the data provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-migrationproject-dataproviderdescriptor.html#cfn-dms-migrationproject-dataproviderdescriptor-dataproviderarn
            '''
            result = self._values.get("data_provider_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_provider_identifier(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-migrationproject-dataproviderdescriptor.html#cfn-dms-migrationproject-dataproviderdescriptor-dataprovideridentifier
            '''
            result = self._values.get("data_provider_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_provider_name(self) -> typing.Optional[builtins.str]:
            '''The user-friendly name of the data provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-migrationproject-dataproviderdescriptor.html#cfn-dms-migrationproject-dataproviderdescriptor-dataprovidername
            '''
            result = self._values.get("data_provider_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role used to access AWS Secrets Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-migrationproject-dataproviderdescriptor.html#cfn-dms-migrationproject-dataproviderdescriptor-secretsmanageraccessrolearn
            '''
            result = self._values.get("secrets_manager_access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_secret_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the AWS Secrets Manager Secret used to store access credentials for the data provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-migrationproject-dataproviderdescriptor.html#cfn-dms-migrationproject-dataproviderdescriptor-secretsmanagersecretid
            '''
            result = self._values.get("secrets_manager_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataProviderDescriptorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnMigrationProjectPropsMixin.SchemaConversionApplicationAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket_path": "s3BucketPath",
            "s3_bucket_role_arn": "s3BucketRoleArn",
        },
    )
    class SchemaConversionApplicationAttributesProperty:
        def __init__(
            self,
            *,
            s3_bucket_path: typing.Optional[builtins.str] = None,
            s3_bucket_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The property describes schema conversion application attributes for the migration project.

            :param s3_bucket_path: 
            :param s3_bucket_role_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-migrationproject-schemaconversionapplicationattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                schema_conversion_application_attributes_property = dms_mixins.CfnMigrationProjectPropsMixin.SchemaConversionApplicationAttributesProperty(
                    s3_bucket_path="s3BucketPath",
                    s3_bucket_role_arn="s3BucketRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a2476c05a0807867cb60ff12a6a6a549a2813919d95c7192d6d958f79c6112a)
                check_type(argname="argument s3_bucket_path", value=s3_bucket_path, expected_type=type_hints["s3_bucket_path"])
                check_type(argname="argument s3_bucket_role_arn", value=s3_bucket_role_arn, expected_type=type_hints["s3_bucket_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket_path is not None:
                self._values["s3_bucket_path"] = s3_bucket_path
            if s3_bucket_role_arn is not None:
                self._values["s3_bucket_role_arn"] = s3_bucket_role_arn

        @builtins.property
        def s3_bucket_path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-migrationproject-schemaconversionapplicationattributes.html#cfn-dms-migrationproject-schemaconversionapplicationattributes-s3bucketpath
            '''
            result = self._values.get("s3_bucket_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_role_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-migrationproject-schemaconversionapplicationattributes.html#cfn-dms-migrationproject-schemaconversionapplicationattributes-s3bucketrolearn
            '''
            result = self._values.get("s3_bucket_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaConversionApplicationAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnReplicationConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_config": "computeConfig",
        "replication_config_identifier": "replicationConfigIdentifier",
        "replication_settings": "replicationSettings",
        "replication_type": "replicationType",
        "resource_identifier": "resourceIdentifier",
        "source_endpoint_arn": "sourceEndpointArn",
        "supplemental_settings": "supplementalSettings",
        "table_mappings": "tableMappings",
        "tags": "tags",
        "target_endpoint_arn": "targetEndpointArn",
    },
)
class CfnReplicationConfigMixinProps:
    def __init__(
        self,
        *,
        compute_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationConfigPropsMixin.ComputeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        replication_config_identifier: typing.Optional[builtins.str] = None,
        replication_settings: typing.Any = None,
        replication_type: typing.Optional[builtins.str] = None,
        resource_identifier: typing.Optional[builtins.str] = None,
        source_endpoint_arn: typing.Optional[builtins.str] = None,
        supplemental_settings: typing.Any = None,
        table_mappings: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_endpoint_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnReplicationConfigPropsMixin.

        :param compute_config: Configuration parameters for provisioning an AWS DMS Serverless replication.
        :param replication_config_identifier: A unique identifier that you want to use to create a ``ReplicationConfigArn`` that is returned as part of the output from this action. You can then pass this output ``ReplicationConfigArn`` as the value of the ``ReplicationConfigArn`` option for other actions to identify both AWS DMS Serverless replications and replication configurations that you want those actions to operate on. For some actions, you can also use either this unique identifier or a corresponding ARN in action filters to identify the specific replication and replication configuration to operate on.
        :param replication_settings: Optional JSON settings for AWS DMS Serverless replications that are provisioned using this replication configuration. For example, see `Change processing tuning settings <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.ChangeProcessingTuning.html>`_ .
        :param replication_type: The type of AWS DMS Serverless replication to provision using this replication configuration. Possible values: - ``"full-load"`` - ``"cdc"`` - ``"full-load-and-cdc"``
        :param resource_identifier: Optional unique value or name that you set for a given resource that can be used to construct an Amazon Resource Name (ARN) for that resource. For more information, see `Fine-grained access control using resource names and tags <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#CHAP_Security.FineGrainedAccess>`_ .
        :param source_endpoint_arn: The Amazon Resource Name (ARN) of the source endpoint for this AWS DMS Serverless replication configuration.
        :param supplemental_settings: Optional JSON settings for specifying supplemental data. For more information, see `Specifying supplemental data for task settings <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.TaskData.html>`_ .
        :param table_mappings: JSON table mappings for AWS DMS Serverless replications that are provisioned using this replication configuration. For more information, see `Specifying table selection and transformations rules using JSON <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TableMapping.SelectionTransformation.html>`_ .
        :param tags: One or more optional tags associated with resources used by the AWS DMS Serverless replication. For more information, see `Tagging resources in AWS Database Migration Service <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tagging.html>`_ .
        :param target_endpoint_arn: The Amazon Resource Name (ARN) of the target endpoint for this AWS DMS serverless replication configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            # replication_settings: Any
            # supplemental_settings: Any
            # table_mappings: Any
            
            cfn_replication_config_mixin_props = dms_mixins.CfnReplicationConfigMixinProps(
                compute_config=dms_mixins.CfnReplicationConfigPropsMixin.ComputeConfigProperty(
                    availability_zone="availabilityZone",
                    dns_name_servers="dnsNameServers",
                    kms_key_id="kmsKeyId",
                    max_capacity_units=123,
                    min_capacity_units=123,
                    multi_az=False,
                    preferred_maintenance_window="preferredMaintenanceWindow",
                    replication_subnet_group_id="replicationSubnetGroupId",
                    vpc_security_group_ids=["vpcSecurityGroupIds"]
                ),
                replication_config_identifier="replicationConfigIdentifier",
                replication_settings=replication_settings,
                replication_type="replicationType",
                resource_identifier="resourceIdentifier",
                source_endpoint_arn="sourceEndpointArn",
                supplemental_settings=supplemental_settings,
                table_mappings=table_mappings,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_endpoint_arn="targetEndpointArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84aee5810690dc43468cacc39b7b24845337c37258b5fa8c25e7bf8d717e059)
            check_type(argname="argument compute_config", value=compute_config, expected_type=type_hints["compute_config"])
            check_type(argname="argument replication_config_identifier", value=replication_config_identifier, expected_type=type_hints["replication_config_identifier"])
            check_type(argname="argument replication_settings", value=replication_settings, expected_type=type_hints["replication_settings"])
            check_type(argname="argument replication_type", value=replication_type, expected_type=type_hints["replication_type"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            check_type(argname="argument source_endpoint_arn", value=source_endpoint_arn, expected_type=type_hints["source_endpoint_arn"])
            check_type(argname="argument supplemental_settings", value=supplemental_settings, expected_type=type_hints["supplemental_settings"])
            check_type(argname="argument table_mappings", value=table_mappings, expected_type=type_hints["table_mappings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_endpoint_arn", value=target_endpoint_arn, expected_type=type_hints["target_endpoint_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_config is not None:
            self._values["compute_config"] = compute_config
        if replication_config_identifier is not None:
            self._values["replication_config_identifier"] = replication_config_identifier
        if replication_settings is not None:
            self._values["replication_settings"] = replication_settings
        if replication_type is not None:
            self._values["replication_type"] = replication_type
        if resource_identifier is not None:
            self._values["resource_identifier"] = resource_identifier
        if source_endpoint_arn is not None:
            self._values["source_endpoint_arn"] = source_endpoint_arn
        if supplemental_settings is not None:
            self._values["supplemental_settings"] = supplemental_settings
        if table_mappings is not None:
            self._values["table_mappings"] = table_mappings
        if tags is not None:
            self._values["tags"] = tags
        if target_endpoint_arn is not None:
            self._values["target_endpoint_arn"] = target_endpoint_arn

    @builtins.property
    def compute_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationConfigPropsMixin.ComputeConfigProperty"]]:
        '''Configuration parameters for provisioning an AWS DMS Serverless replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html#cfn-dms-replicationconfig-computeconfig
        '''
        result = self._values.get("compute_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationConfigPropsMixin.ComputeConfigProperty"]], result)

    @builtins.property
    def replication_config_identifier(self) -> typing.Optional[builtins.str]:
        '''A unique identifier that you want to use to create a ``ReplicationConfigArn`` that is returned as part of the output from this action.

        You can then pass this output ``ReplicationConfigArn`` as the value of the ``ReplicationConfigArn`` option for other actions to identify both AWS DMS Serverless replications and replication configurations that you want those actions to operate on. For some actions, you can also use either this unique identifier or a corresponding ARN in action filters to identify the specific replication and replication configuration to operate on.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html#cfn-dms-replicationconfig-replicationconfigidentifier
        '''
        result = self._values.get("replication_config_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_settings(self) -> typing.Any:
        '''Optional JSON settings for AWS DMS Serverless replications that are provisioned using this replication configuration.

        For example, see `Change processing tuning settings <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.ChangeProcessingTuning.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html#cfn-dms-replicationconfig-replicationsettings
        '''
        result = self._values.get("replication_settings")
        return typing.cast(typing.Any, result)

    @builtins.property
    def replication_type(self) -> typing.Optional[builtins.str]:
        '''The type of AWS DMS Serverless replication to provision using this replication configuration.

        Possible values:

        - ``"full-load"``
        - ``"cdc"``
        - ``"full-load-and-cdc"``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html#cfn-dms-replicationconfig-replicationtype
        '''
        result = self._values.get("replication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''Optional unique value or name that you set for a given resource that can be used to construct an Amazon Resource Name (ARN) for that resource.

        For more information, see `Fine-grained access control using resource names and tags <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html#CHAP_Security.FineGrainedAccess>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html#cfn-dms-replicationconfig-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_endpoint_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the source endpoint for this AWS DMS Serverless replication configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html#cfn-dms-replicationconfig-sourceendpointarn
        '''
        result = self._values.get("source_endpoint_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def supplemental_settings(self) -> typing.Any:
        '''Optional JSON settings for specifying supplemental data.

        For more information, see `Specifying supplemental data for task settings <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.TaskData.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html#cfn-dms-replicationconfig-supplementalsettings
        '''
        result = self._values.get("supplemental_settings")
        return typing.cast(typing.Any, result)

    @builtins.property
    def table_mappings(self) -> typing.Any:
        '''JSON table mappings for AWS DMS Serverless replications that are provisioned using this replication configuration.

        For more information, see `Specifying table selection and transformations rules using JSON <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TableMapping.SelectionTransformation.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html#cfn-dms-replicationconfig-tablemappings
        '''
        result = self._values.get("table_mappings")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more optional tags associated with resources used by the AWS DMS Serverless replication.

        For more information, see `Tagging resources in AWS Database Migration Service <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html#cfn-dms-replicationconfig-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_endpoint_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the target endpoint for this AWS DMS serverless replication configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html#cfn-dms-replicationconfig-targetendpointarn
        '''
        result = self._values.get("target_endpoint_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReplicationConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnReplicationConfigPropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationconfig.html
    :cloudformationResource: AWS::DMS::ReplicationConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        # replication_settings: Any
        # supplemental_settings: Any
        # table_mappings: Any
        
        cfn_replication_config_props_mixin = dms_mixins.CfnReplicationConfigPropsMixin(dms_mixins.CfnReplicationConfigMixinProps(
            compute_config=dms_mixins.CfnReplicationConfigPropsMixin.ComputeConfigProperty(
                availability_zone="availabilityZone",
                dns_name_servers="dnsNameServers",
                kms_key_id="kmsKeyId",
                max_capacity_units=123,
                min_capacity_units=123,
                multi_az=False,
                preferred_maintenance_window="preferredMaintenanceWindow",
                replication_subnet_group_id="replicationSubnetGroupId",
                vpc_security_group_ids=["vpcSecurityGroupIds"]
            ),
            replication_config_identifier="replicationConfigIdentifier",
            replication_settings=replication_settings,
            replication_type="replicationType",
            resource_identifier="resourceIdentifier",
            source_endpoint_arn="sourceEndpointArn",
            supplemental_settings=supplemental_settings,
            table_mappings=table_mappings,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_endpoint_arn="targetEndpointArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReplicationConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DMS::ReplicationConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb432619c78e8ee3c8204cd14c714c30b3c4b5304d42fc8990721c28553ff40b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__469dfaf49e432657eb2c8b61e97032f2eb368796f63326307b4a3febdf1219cc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba96e8fb8aa4946159809c94ad5c71b5ab9cbe036eba1337ef47c34fc57841b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReplicationConfigMixinProps:
        return typing.cast(CfnReplicationConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnReplicationConfigPropsMixin.ComputeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "dns_name_servers": "dnsNameServers",
            "kms_key_id": "kmsKeyId",
            "max_capacity_units": "maxCapacityUnits",
            "min_capacity_units": "minCapacityUnits",
            "multi_az": "multiAz",
            "preferred_maintenance_window": "preferredMaintenanceWindow",
            "replication_subnet_group_id": "replicationSubnetGroupId",
            "vpc_security_group_ids": "vpcSecurityGroupIds",
        },
    )
    class ComputeConfigProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            dns_name_servers: typing.Optional[builtins.str] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
            max_capacity_units: typing.Optional[jsii.Number] = None,
            min_capacity_units: typing.Optional[jsii.Number] = None,
            multi_az: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            preferred_maintenance_window: typing.Optional[builtins.str] = None,
            replication_subnet_group_id: typing.Optional[builtins.str] = None,
            vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration parameters for provisioning an AWS DMS Serverless replication.

            :param availability_zone: The Availability Zone where the AWS DMS Serverless replication using this configuration will run. The default value is a random, system-chosen Availability Zone in the configuration's AWS Region , for example, ``"us-west-2"`` . You can't set this parameter if the ``MultiAZ`` parameter is set to ``true`` .
            :param dns_name_servers: A list of custom DNS name servers supported for the AWS DMS Serverless replication to access your source or target database. This list overrides the default name servers supported by the AWS DMS Serverless replication. You can specify a comma-separated list of internet addresses for up to four DNS name servers. For example: ``"1.1.1.1,2.2.2.2,3.3.3.3,4.4.4.4"``
            :param kms_key_id: An AWS Key Management Service ( AWS ) key Amazon Resource Name (ARN) that is used to encrypt the data during AWS DMS Serverless replication. If you don't specify a value for the ``KmsKeyId`` parameter, AWS DMS uses your default encryption key. AWS creates the default encryption key for your Amazon Web Services account. Your AWS account has a different default encryption key for each AWS Region .
            :param max_capacity_units: Specifies the maximum value of the AWS DMS capacity units (DCUs) for which a given AWS DMS Serverless replication can be provisioned. A single DCU is 2GB of RAM, with 1 DCU as the minimum value allowed. The list of valid DCU values includes 1, 2, 4, 8, 16, 32, 64, 128, 192, 256, and 384. So, the maximum value that you can specify for AWS DMS Serverless is 384. The ``MaxCapacityUnits`` parameter is the only DCU parameter you are required to specify.
            :param min_capacity_units: Specifies the minimum value of the AWS DMS capacity units (DCUs) for which a given AWS DMS Serverless replication can be provisioned. A single DCU is 2GB of RAM, with 1 DCU as the minimum value allowed. The list of valid DCU values includes 1, 2, 4, 8, 16, 32, 64, 128, 192, 256, and 384. So, the minimum DCU value that you can specify for AWS DMS Serverless is 1. If you don't set this value, AWS DMS sets this parameter to the minimum DCU value allowed, 1. If there is no current source activity, AWS DMS scales down your replication until it reaches the value specified in ``MinCapacityUnits`` .
            :param multi_az: Specifies whether the AWS DMS Serverless replication is a Multi-AZ deployment. You can't set the ``AvailabilityZone`` parameter if the ``MultiAZ`` parameter is set to ``true`` .
            :param preferred_maintenance_window: The weekly time range during which system maintenance can occur for the AWS DMS Serverless replication, in Universal Coordinated Time (UTC). The format is ``ddd:hh24:mi-ddd:hh24:mi`` . The default is a 30-minute window selected at random from an 8-hour block of time per AWS Region . This maintenance occurs on a random day of the week. Valid values for days of the week include ``Mon`` , ``Tue`` , ``Wed`` , ``Thu`` , ``Fri`` , ``Sat`` , and ``Sun`` . Constraints include a minimum 30-minute window.
            :param replication_subnet_group_id: Specifies a subnet group identifier to associate with the AWS DMS Serverless replication.
            :param vpc_security_group_ids: Specifies the virtual private cloud (VPC) security group to use with the AWS DMS Serverless replication. The VPC security group must work with the VPC containing the replication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-replicationconfig-computeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
                
                compute_config_property = dms_mixins.CfnReplicationConfigPropsMixin.ComputeConfigProperty(
                    availability_zone="availabilityZone",
                    dns_name_servers="dnsNameServers",
                    kms_key_id="kmsKeyId",
                    max_capacity_units=123,
                    min_capacity_units=123,
                    multi_az=False,
                    preferred_maintenance_window="preferredMaintenanceWindow",
                    replication_subnet_group_id="replicationSubnetGroupId",
                    vpc_security_group_ids=["vpcSecurityGroupIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90d6d556c880cc6f04e65b6a7eb34dc64783ff6d162ed267bea47aa952183521)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument dns_name_servers", value=dns_name_servers, expected_type=type_hints["dns_name_servers"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument max_capacity_units", value=max_capacity_units, expected_type=type_hints["max_capacity_units"])
                check_type(argname="argument min_capacity_units", value=min_capacity_units, expected_type=type_hints["min_capacity_units"])
                check_type(argname="argument multi_az", value=multi_az, expected_type=type_hints["multi_az"])
                check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
                check_type(argname="argument replication_subnet_group_id", value=replication_subnet_group_id, expected_type=type_hints["replication_subnet_group_id"])
                check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if dns_name_servers is not None:
                self._values["dns_name_servers"] = dns_name_servers
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if max_capacity_units is not None:
                self._values["max_capacity_units"] = max_capacity_units
            if min_capacity_units is not None:
                self._values["min_capacity_units"] = min_capacity_units
            if multi_az is not None:
                self._values["multi_az"] = multi_az
            if preferred_maintenance_window is not None:
                self._values["preferred_maintenance_window"] = preferred_maintenance_window
            if replication_subnet_group_id is not None:
                self._values["replication_subnet_group_id"] = replication_subnet_group_id
            if vpc_security_group_ids is not None:
                self._values["vpc_security_group_ids"] = vpc_security_group_ids

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Availability Zone where the AWS DMS Serverless replication using this configuration will run.

            The default value is a random, system-chosen Availability Zone in the configuration's AWS Region , for example, ``"us-west-2"`` . You can't set this parameter if the ``MultiAZ`` parameter is set to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-replicationconfig-computeconfig.html#cfn-dms-replicationconfig-computeconfig-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dns_name_servers(self) -> typing.Optional[builtins.str]:
            '''A list of custom DNS name servers supported for the AWS DMS Serverless replication to access your source or target database.

            This list overrides the default name servers supported by the AWS DMS Serverless replication. You can specify a comma-separated list of internet addresses for up to four DNS name servers. For example: ``"1.1.1.1,2.2.2.2,3.3.3.3,4.4.4.4"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-replicationconfig-computeconfig.html#cfn-dms-replicationconfig-computeconfig-dnsnameservers
            '''
            result = self._values.get("dns_name_servers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''An AWS Key Management Service ( AWS  ) key Amazon Resource Name (ARN) that is used to encrypt the data during AWS DMS Serverless replication.

            If you don't specify a value for the ``KmsKeyId`` parameter, AWS DMS uses your default encryption key.

            AWS  creates the default encryption key for your Amazon Web Services account. Your AWS account has a different default encryption key for each AWS Region .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-replicationconfig-computeconfig.html#cfn-dms-replicationconfig-computeconfig-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum value of the AWS DMS capacity units (DCUs) for which a given AWS DMS Serverless replication can be provisioned.

            A single DCU is 2GB of RAM, with 1 DCU as the minimum value allowed. The list of valid DCU values includes 1, 2, 4, 8, 16, 32, 64, 128, 192, 256, and 384. So, the maximum value that you can specify for AWS DMS Serverless is 384. The ``MaxCapacityUnits`` parameter is the only DCU parameter you are required to specify.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-replicationconfig-computeconfig.html#cfn-dms-replicationconfig-computeconfig-maxcapacityunits
            '''
            result = self._values.get("max_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''Specifies the minimum value of the AWS DMS capacity units (DCUs) for which a given AWS DMS Serverless replication can be provisioned.

            A single DCU is 2GB of RAM, with 1 DCU as the minimum value allowed. The list of valid DCU values includes 1, 2, 4, 8, 16, 32, 64, 128, 192, 256, and 384. So, the minimum DCU value that you can specify for AWS DMS Serverless is 1. If you don't set this value, AWS DMS sets this parameter to the minimum DCU value allowed, 1. If there is no current source activity, AWS DMS scales down your replication until it reaches the value specified in ``MinCapacityUnits`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-replicationconfig-computeconfig.html#cfn-dms-replicationconfig-computeconfig-mincapacityunits
            '''
            result = self._values.get("min_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def multi_az(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the AWS DMS Serverless replication is a Multi-AZ deployment.

            You can't set the ``AvailabilityZone`` parameter if the ``MultiAZ`` parameter is set to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-replicationconfig-computeconfig.html#cfn-dms-replicationconfig-computeconfig-multiaz
            '''
            result = self._values.get("multi_az")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
            '''The weekly time range during which system maintenance can occur for the AWS DMS Serverless replication, in Universal Coordinated Time (UTC).

            The format is ``ddd:hh24:mi-ddd:hh24:mi`` .

            The default is a 30-minute window selected at random from an 8-hour block of time per AWS Region . This maintenance occurs on a random day of the week. Valid values for days of the week include ``Mon`` , ``Tue`` , ``Wed`` , ``Thu`` , ``Fri`` , ``Sat`` , and ``Sun`` .

            Constraints include a minimum 30-minute window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-replicationconfig-computeconfig.html#cfn-dms-replicationconfig-computeconfig-preferredmaintenancewindow
            '''
            result = self._values.get("preferred_maintenance_window")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replication_subnet_group_id(self) -> typing.Optional[builtins.str]:
            '''Specifies a subnet group identifier to associate with the AWS DMS Serverless replication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-replicationconfig-computeconfig.html#cfn-dms-replicationconfig-computeconfig-replicationsubnetgroupid
            '''
            result = self._values.get("replication_subnet_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the virtual private cloud (VPC) security group to use with the AWS DMS Serverless replication.

            The VPC security group must work with the VPC containing the replication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-replicationconfig-computeconfig.html#cfn-dms-replicationconfig-computeconfig-vpcsecuritygroupids
            '''
            result = self._values.get("vpc_security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnReplicationInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_storage": "allocatedStorage",
        "allow_major_version_upgrade": "allowMajorVersionUpgrade",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "dns_name_servers": "dnsNameServers",
        "engine_version": "engineVersion",
        "kms_key_id": "kmsKeyId",
        "multi_az": "multiAz",
        "network_type": "networkType",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "publicly_accessible": "publiclyAccessible",
        "replication_instance_class": "replicationInstanceClass",
        "replication_instance_identifier": "replicationInstanceIdentifier",
        "replication_subnet_group_identifier": "replicationSubnetGroupIdentifier",
        "resource_identifier": "resourceIdentifier",
        "tags": "tags",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnReplicationInstanceMixinProps:
    def __init__(
        self,
        *,
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        dns_name_servers: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        multi_az: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        network_type: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        replication_instance_class: typing.Optional[builtins.str] = None,
        replication_instance_identifier: typing.Optional[builtins.str] = None,
        replication_subnet_group_identifier: typing.Optional[builtins.str] = None,
        resource_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnReplicationInstancePropsMixin.

        :param allocated_storage: The amount of storage (in gigabytes) to be initially allocated for the replication instance.
        :param allow_major_version_upgrade: Indicates that major version upgrades are allowed. Changing this parameter does not result in an outage, and the change is asynchronously applied as soon as possible. This parameter must be set to ``true`` when specifying a value for the ``EngineVersion`` parameter that is a different major version than the replication instance's current version.
        :param auto_minor_version_upgrade: A value that indicates whether minor engine upgrades are applied automatically to the replication instance during the maintenance window. This parameter defaults to ``true`` . Default: ``true``
        :param availability_zone: The Availability Zone that the replication instance will be created in. The default value is a random, system-chosen Availability Zone in the endpoint's AWS Region , for example ``us-east-1d`` .
        :param dns_name_servers: A list of custom DNS name servers supported for the replication instance to access your on-premise source or target database. This list overrides the default name servers supported by the replication instance. You can specify a comma-separated list of internet addresses for up to four on-premise DNS name servers. For example: ``"1.1.1.1,2.2.2.2,3.3.3.3,4.4.4.4"``
        :param engine_version: The engine version number of the replication instance. If an engine version number is not specified when a replication instance is created, the default is the latest engine version available.
        :param kms_key_id: An AWS key identifier that is used to encrypt the data on the replication instance. If you don't specify a value for the ``KmsKeyId`` parameter, AWS DMS uses your default encryption key. AWS creates the default encryption key for your AWS account . Your AWS account has a different default encryption key for each AWS Region .
        :param multi_az: Specifies whether the replication instance is a Multi-AZ deployment. You can't set the ``AvailabilityZone`` parameter if the Multi-AZ parameter is set to ``true`` .
        :param network_type: The type of IP address protocol used by a replication instance, such as IPv4 only or Dual-stack that supports both IPv4 and IPv6 addressing. IPv6 only is not yet supported.
        :param preferred_maintenance_window: The weekly time range during which system maintenance can occur, in UTC. *Format* : ``ddd:hh24:mi-ddd:hh24:mi`` *Default* : A 30-minute window selected at random from an 8-hour block of time per AWS Region , occurring on a random day of the week. *Valid days* ( ``ddd`` ): ``Mon`` | ``Tue`` | ``Wed`` | ``Thu`` | ``Fri`` | ``Sat`` | ``Sun`` *Constraints* : Minimum 30-minute window.
        :param publicly_accessible: Specifies the accessibility options for the replication instance. A value of ``true`` represents an instance with a public IP address. A value of ``false`` represents an instance with a private IP address. The default value is ``true`` .
        :param replication_instance_class: The compute and memory capacity of the replication instance as defined for the specified replication instance class. For example, to specify the instance class dms.c4.large, set this parameter to ``"dms.c4.large"`` . For more information on the settings and capacities for the available replication instance classes, see `Selecting the right AWS DMS replication instance for your migration <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_ReplicationInstance.html#CHAP_ReplicationInstance.InDepth>`_ in the *AWS Database Migration Service User Guide* .
        :param replication_instance_identifier: The replication instance identifier. This parameter is stored as a lowercase string. Constraints: - Must contain 1-63 alphanumeric characters or hyphens. - First character must be a letter. - Can't end with a hyphen or contain two consecutive hyphens. Example: ``myrepinstance``
        :param replication_subnet_group_identifier: A subnet group to associate with the replication instance.
        :param resource_identifier: A display name for the resource identifier at the end of the ``EndpointArn`` response parameter that is returned in the created ``Endpoint`` object. The value for this parameter can have up to 31 characters. It can contain only ASCII letters, digits, and hyphen ('-'). Also, it can't end with a hyphen or contain two consecutive hyphens, and can only begin with a letter, such as ``Example-App-ARN1`` . For example, this value might result in the ``EndpointArn`` value ``arn:aws:dms:eu-west-1:012345678901:rep:Example-App-ARN1`` . If you don't specify a ``ResourceIdentifier`` value, AWS DMS generates a default identifier value for the end of ``EndpointArn`` .
        :param tags: One or more tags to be assigned to the replication instance.
        :param vpc_security_group_ids: Specifies the virtual private cloud (VPC) security group to be used with the replication instance. The VPC security group must work with the VPC containing the replication instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            cfn_replication_instance_mixin_props = dms_mixins.CfnReplicationInstanceMixinProps(
                allocated_storage=123,
                allow_major_version_upgrade=False,
                auto_minor_version_upgrade=False,
                availability_zone="availabilityZone",
                dns_name_servers="dnsNameServers",
                engine_version="engineVersion",
                kms_key_id="kmsKeyId",
                multi_az=False,
                network_type="networkType",
                preferred_maintenance_window="preferredMaintenanceWindow",
                publicly_accessible=False,
                replication_instance_class="replicationInstanceClass",
                replication_instance_identifier="replicationInstanceIdentifier",
                replication_subnet_group_identifier="replicationSubnetGroupIdentifier",
                resource_identifier="resourceIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_security_group_ids=["vpcSecurityGroupIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ebaa16805e9cdcab8fac4057a1720d597407c62be325ac765d925bcf2d14e6c)
            check_type(argname="argument allocated_storage", value=allocated_storage, expected_type=type_hints["allocated_storage"])
            check_type(argname="argument allow_major_version_upgrade", value=allow_major_version_upgrade, expected_type=type_hints["allow_major_version_upgrade"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument dns_name_servers", value=dns_name_servers, expected_type=type_hints["dns_name_servers"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument multi_az", value=multi_az, expected_type=type_hints["multi_az"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument replication_instance_class", value=replication_instance_class, expected_type=type_hints["replication_instance_class"])
            check_type(argname="argument replication_instance_identifier", value=replication_instance_identifier, expected_type=type_hints["replication_instance_identifier"])
            check_type(argname="argument replication_subnet_group_identifier", value=replication_subnet_group_identifier, expected_type=type_hints["replication_subnet_group_identifier"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if allow_major_version_upgrade is not None:
            self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if dns_name_servers is not None:
            self._values["dns_name_servers"] = dns_name_servers
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if network_type is not None:
            self._values["network_type"] = network_type
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if replication_instance_class is not None:
            self._values["replication_instance_class"] = replication_instance_class
        if replication_instance_identifier is not None:
            self._values["replication_instance_identifier"] = replication_instance_identifier
        if replication_subnet_group_identifier is not None:
            self._values["replication_subnet_group_identifier"] = replication_subnet_group_identifier
        if resource_identifier is not None:
            self._values["resource_identifier"] = resource_identifier
        if tags is not None:
            self._values["tags"] = tags
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        '''The amount of storage (in gigabytes) to be initially allocated for the replication instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-allocatedstorage
        '''
        result = self._values.get("allocated_storage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def allow_major_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates that major version upgrades are allowed.

        Changing this parameter does not result in an outage, and the change is asynchronously applied as soon as possible.

        This parameter must be set to ``true`` when specifying a value for the ``EngineVersion`` parameter that is a different major version than the replication instance's current version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-allowmajorversionupgrade
        '''
        result = self._values.get("allow_major_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether minor engine upgrades are applied automatically to the replication instance during the maintenance window.

        This parameter defaults to ``true`` .

        Default: ``true``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone that the replication instance will be created in.

        The default value is a random, system-chosen Availability Zone in the endpoint's AWS Region , for example ``us-east-1d`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_name_servers(self) -> typing.Optional[builtins.str]:
        '''A list of custom DNS name servers supported for the replication instance to access your on-premise source or target database.

        This list overrides the default name servers supported by the replication instance. You can specify a comma-separated list of internet addresses for up to four on-premise DNS name servers. For example: ``"1.1.1.1,2.2.2.2,3.3.3.3,4.4.4.4"``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-dnsnameservers
        '''
        result = self._values.get("dns_name_servers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The engine version number of the replication instance.

        If an engine version number is not specified when a replication instance is created, the default is the latest engine version available.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''An AWS  key identifier that is used to encrypt the data on the replication instance.

        If you don't specify a value for the ``KmsKeyId`` parameter, AWS DMS uses your default encryption key.

        AWS  creates the default encryption key for your AWS account . Your AWS account has a different default encryption key for each AWS Region .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_az(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the replication instance is a Multi-AZ deployment.

        You can't set the ``AvailabilityZone`` parameter if the Multi-AZ parameter is set to ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-multiaz
        '''
        result = self._values.get("multi_az")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''The type of IP address protocol used by a replication instance, such as IPv4 only or Dual-stack that supports both IPv4 and IPv6 addressing.

        IPv6 only is not yet supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range during which system maintenance can occur, in UTC.

        *Format* : ``ddd:hh24:mi-ddd:hh24:mi``

        *Default* : A 30-minute window selected at random from an 8-hour block of time per AWS Region , occurring on a random day of the week.

        *Valid days* ( ``ddd`` ): ``Mon`` | ``Tue`` | ``Wed`` | ``Thu`` | ``Fri`` | ``Sat`` | ``Sun``

        *Constraints* : Minimum 30-minute window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies the accessibility options for the replication instance.

        A value of ``true`` represents an instance with a public IP address. A value of ``false`` represents an instance with a private IP address. The default value is ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def replication_instance_class(self) -> typing.Optional[builtins.str]:
        '''The compute and memory capacity of the replication instance as defined for the specified replication instance class.

        For example, to specify the instance class dms.c4.large, set this parameter to ``"dms.c4.large"`` . For more information on the settings and capacities for the available replication instance classes, see `Selecting the right AWS DMS replication instance for your migration <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_ReplicationInstance.html#CHAP_ReplicationInstance.InDepth>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-replicationinstanceclass
        '''
        result = self._values.get("replication_instance_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_instance_identifier(self) -> typing.Optional[builtins.str]:
        '''The replication instance identifier. This parameter is stored as a lowercase string.

        Constraints:

        - Must contain 1-63 alphanumeric characters or hyphens.
        - First character must be a letter.
        - Can't end with a hyphen or contain two consecutive hyphens.

        Example: ``myrepinstance``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-replicationinstanceidentifier
        '''
        result = self._values.get("replication_instance_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_subnet_group_identifier(self) -> typing.Optional[builtins.str]:
        '''A subnet group to associate with the replication instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-replicationsubnetgroupidentifier
        '''
        result = self._values.get("replication_subnet_group_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''A display name for the resource identifier at the end of the ``EndpointArn`` response parameter that is returned in the created ``Endpoint`` object.

        The value for this parameter can have up to 31 characters. It can contain only ASCII letters, digits, and hyphen ('-'). Also, it can't end with a hyphen or contain two consecutive hyphens, and can only begin with a letter, such as ``Example-App-ARN1`` . For example, this value might result in the ``EndpointArn`` value ``arn:aws:dms:eu-west-1:012345678901:rep:Example-App-ARN1`` . If you don't specify a ``ResourceIdentifier`` value, AWS DMS generates a default identifier value for the end of ``EndpointArn`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more tags to be assigned to the replication instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the virtual private cloud (VPC) security group to be used with the replication instance.

        The VPC security group must work with the VPC containing the replication instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReplicationInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnReplicationInstancePropsMixin",
):
    '''The ``AWS::DMS::ReplicationInstance`` resource creates an AWS DMS replication instance.

    To create a ReplicationInstance, you need permissions to create instances. You'll need similar permissions to terminate instances when you delete stacks with instances.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html
    :cloudformationResource: AWS::DMS::ReplicationInstance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        cfn_replication_instance_props_mixin = dms_mixins.CfnReplicationInstancePropsMixin(dms_mixins.CfnReplicationInstanceMixinProps(
            allocated_storage=123,
            allow_major_version_upgrade=False,
            auto_minor_version_upgrade=False,
            availability_zone="availabilityZone",
            dns_name_servers="dnsNameServers",
            engine_version="engineVersion",
            kms_key_id="kmsKeyId",
            multi_az=False,
            network_type="networkType",
            preferred_maintenance_window="preferredMaintenanceWindow",
            publicly_accessible=False,
            replication_instance_class="replicationInstanceClass",
            replication_instance_identifier="replicationInstanceIdentifier",
            replication_subnet_group_identifier="replicationSubnetGroupIdentifier",
            resource_identifier="resourceIdentifier",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_security_group_ids=["vpcSecurityGroupIds"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReplicationInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DMS::ReplicationInstance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb44d8fe9c688960382dd94cbd90ce05df149e600bbcb1483acaaff1fab1f5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__537dcc1c3964cfe5121e575dd3da9ffa94cbce543133f00f103747ddf4ba90b8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e433d47bf66c5d4670a7ac715b5cc22baac2740bd76c8e26b51bbde262312d06)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReplicationInstanceMixinProps:
        return typing.cast(CfnReplicationInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnReplicationSubnetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "replication_subnet_group_description": "replicationSubnetGroupDescription",
        "replication_subnet_group_identifier": "replicationSubnetGroupIdentifier",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnReplicationSubnetGroupMixinProps:
    def __init__(
        self,
        *,
        replication_subnet_group_description: typing.Optional[builtins.str] = None,
        replication_subnet_group_identifier: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnReplicationSubnetGroupPropsMixin.

        :param replication_subnet_group_description: The description for the subnet group.
        :param replication_subnet_group_identifier: The identifier for the replication subnet group. If you don't specify a name, CloudFormation generates a unique ID and uses that ID for the identifier.
        :param subnet_ids: One or more subnet IDs to be assigned to the subnet group.
        :param tags: One or more tags to be assigned to the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            cfn_replication_subnet_group_mixin_props = dms_mixins.CfnReplicationSubnetGroupMixinProps(
                replication_subnet_group_description="replicationSubnetGroupDescription",
                replication_subnet_group_identifier="replicationSubnetGroupIdentifier",
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63ce34a98449a9e64fdf78c2e5c159ff0b4c4f00c7fe5a1b65838b421476d7e)
            check_type(argname="argument replication_subnet_group_description", value=replication_subnet_group_description, expected_type=type_hints["replication_subnet_group_description"])
            check_type(argname="argument replication_subnet_group_identifier", value=replication_subnet_group_identifier, expected_type=type_hints["replication_subnet_group_identifier"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if replication_subnet_group_description is not None:
            self._values["replication_subnet_group_description"] = replication_subnet_group_description
        if replication_subnet_group_identifier is not None:
            self._values["replication_subnet_group_identifier"] = replication_subnet_group_identifier
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def replication_subnet_group_description(self) -> typing.Optional[builtins.str]:
        '''The description for the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-replicationsubnetgroupdescription
        '''
        result = self._values.get("replication_subnet_group_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_subnet_group_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier for the replication subnet group.

        If you don't specify a name, CloudFormation generates a unique ID and uses that ID for the identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-replicationsubnetgroupidentifier
        '''
        result = self._values.get("replication_subnet_group_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more subnet IDs to be assigned to the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more tags to be assigned to the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationSubnetGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReplicationSubnetGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnReplicationSubnetGroupPropsMixin",
):
    '''The ``AWS::DMS::ReplicationSubnetGroup`` resource creates an AWS DMS replication subnet group.

    Subnet groups must contain at least two subnets in two different Availability Zones in the same AWS Region .
    .. epigraph::

       Resource creation fails if the ``dms-vpc-role`` AWS Identity and Access Management ( IAM ) role doesn't already exist. For more information, see `Creating the IAM Roles to Use With the AWS CLI and AWS DMS API <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.APIRole.html>`_ in the *AWS Database Migration Service User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html
    :cloudformationResource: AWS::DMS::ReplicationSubnetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        cfn_replication_subnet_group_props_mixin = dms_mixins.CfnReplicationSubnetGroupPropsMixin(dms_mixins.CfnReplicationSubnetGroupMixinProps(
            replication_subnet_group_description="replicationSubnetGroupDescription",
            replication_subnet_group_identifier="replicationSubnetGroupIdentifier",
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
        props: typing.Union[CfnReplicationSubnetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DMS::ReplicationSubnetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9101ba56a590aa025d7a09a35454895b199fb70607413bcaa3e3bb0f3de5e75c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__feb6f0074c9438576013414a5e7e9fc0960941bde4c7e0fb0592c228f935621c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf905495a08d179c62181ff0a8d542dd3efb81fa4dddd6a133a8de1121fbafde)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReplicationSubnetGroupMixinProps:
        return typing.cast(CfnReplicationSubnetGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnReplicationTaskMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cdc_start_position": "cdcStartPosition",
        "cdc_start_time": "cdcStartTime",
        "cdc_stop_position": "cdcStopPosition",
        "migration_type": "migrationType",
        "replication_instance_arn": "replicationInstanceArn",
        "replication_task_identifier": "replicationTaskIdentifier",
        "replication_task_settings": "replicationTaskSettings",
        "resource_identifier": "resourceIdentifier",
        "source_endpoint_arn": "sourceEndpointArn",
        "table_mappings": "tableMappings",
        "tags": "tags",
        "target_endpoint_arn": "targetEndpointArn",
        "task_data": "taskData",
    },
)
class CfnReplicationTaskMixinProps:
    def __init__(
        self,
        *,
        cdc_start_position: typing.Optional[builtins.str] = None,
        cdc_start_time: typing.Optional[jsii.Number] = None,
        cdc_stop_position: typing.Optional[builtins.str] = None,
        migration_type: typing.Optional[builtins.str] = None,
        replication_instance_arn: typing.Optional[builtins.str] = None,
        replication_task_identifier: typing.Optional[builtins.str] = None,
        replication_task_settings: typing.Optional[builtins.str] = None,
        resource_identifier: typing.Optional[builtins.str] = None,
        source_endpoint_arn: typing.Optional[builtins.str] = None,
        table_mappings: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_endpoint_arn: typing.Optional[builtins.str] = None,
        task_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnReplicationTaskPropsMixin.

        :param cdc_start_position: Indicates when you want a change data capture (CDC) operation to start. Use either ``CdcStartPosition`` or ``CdcStartTime`` to specify when you want a CDC operation to start. Specifying both values results in an error. The value can be in date, checkpoint, log sequence number (LSN), or system change number (SCN) format. Here is a date example: ``--cdc-start-position "2018-03-08T12:12:12"`` Here is a checkpoint example: ``--cdc-start-position "checkpoint:V1#27#mysql-bin-changelog.157832:1975:-1:2002:677883278264080:mysql-bin-changelog.157832:1876#0#0#*#0#93"`` Here is an LSN example: ``--cdc-start-position “mysql-bin-changelog.000024:373”`` .. epigraph:: When you use this task setting with a source PostgreSQL database, a logical replication slot should already be created and associated with the source endpoint. You can verify this by setting the ``slotName`` extra connection attribute to the name of this logical replication slot. For more information, see `Extra Connection Attributes When Using PostgreSQL as a Source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.PostgreSQL.html#CHAP_Source.PostgreSQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .
        :param cdc_start_time: Indicates the start time for a change data capture (CDC) operation.
        :param cdc_stop_position: Indicates when you want a change data capture (CDC) operation to stop. The value can be either server time or commit time. Here is a server time example: ``--cdc-stop-position "server_time:2018-02-09T12:12:12"`` Here is a commit time example: ``--cdc-stop-position "commit_time: 2018-02-09T12:12:12"``
        :param migration_type: The migration type. Valid values: ``full-load`` | ``cdc`` | ``full-load-and-cdc``
        :param replication_instance_arn: The Amazon Resource Name (ARN) of a replication instance.
        :param replication_task_identifier: An identifier for the replication task. Constraints: - Must contain 1-255 alphanumeric characters or hyphens. - First character must be a letter. - Cannot end with a hyphen or contain two consecutive hyphens.
        :param replication_task_settings: Overall settings for the task, in JSON format. For more information, see `Specifying Task Settings for AWS Database Migration Service Tasks <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.html>`_ in the *AWS Database Migration Service User Guide* .
        :param resource_identifier: A display name for the resource identifier at the end of the ``EndpointArn`` response parameter that is returned in the created ``Endpoint`` object. The value for this parameter can have up to 31 characters. It can contain only ASCII letters, digits, and hyphen ('-'). Also, it can't end with a hyphen or contain two consecutive hyphens, and can only begin with a letter, such as ``Example-App-ARN1`` . For example, this value might result in the ``EndpointArn`` value ``arn:aws:dms:eu-west-1:012345678901:rep:Example-App-ARN1`` . If you don't specify a ``ResourceIdentifier`` value, AWS DMS generates a default identifier value for the end of ``EndpointArn`` .
        :param source_endpoint_arn: An Amazon Resource Name (ARN) that uniquely identifies the source endpoint.
        :param table_mappings: The table mappings for the task, in JSON format. For more information, see `Using Table Mapping to Specify Task Settings <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TableMapping.html>`_ in the *AWS Database Migration Service User Guide* .
        :param tags: One or more tags to be assigned to the replication task.
        :param target_endpoint_arn: An Amazon Resource Name (ARN) that uniquely identifies the target endpoint.
        :param task_data: Supplemental information that the task requires to migrate the data for certain source and target endpoints. For more information, see `Specifying Supplemental Data for Task Settings <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.TaskData.html>`_ in the *AWS Database Migration Service User Guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
            
            cfn_replication_task_mixin_props = dms_mixins.CfnReplicationTaskMixinProps(
                cdc_start_position="cdcStartPosition",
                cdc_start_time=123,
                cdc_stop_position="cdcStopPosition",
                migration_type="migrationType",
                replication_instance_arn="replicationInstanceArn",
                replication_task_identifier="replicationTaskIdentifier",
                replication_task_settings="replicationTaskSettings",
                resource_identifier="resourceIdentifier",
                source_endpoint_arn="sourceEndpointArn",
                table_mappings="tableMappings",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_endpoint_arn="targetEndpointArn",
                task_data="taskData"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477ced8acd9881a3ac17d27cfb65e246432478e379680052f47536adb2f5d480)
            check_type(argname="argument cdc_start_position", value=cdc_start_position, expected_type=type_hints["cdc_start_position"])
            check_type(argname="argument cdc_start_time", value=cdc_start_time, expected_type=type_hints["cdc_start_time"])
            check_type(argname="argument cdc_stop_position", value=cdc_stop_position, expected_type=type_hints["cdc_stop_position"])
            check_type(argname="argument migration_type", value=migration_type, expected_type=type_hints["migration_type"])
            check_type(argname="argument replication_instance_arn", value=replication_instance_arn, expected_type=type_hints["replication_instance_arn"])
            check_type(argname="argument replication_task_identifier", value=replication_task_identifier, expected_type=type_hints["replication_task_identifier"])
            check_type(argname="argument replication_task_settings", value=replication_task_settings, expected_type=type_hints["replication_task_settings"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            check_type(argname="argument source_endpoint_arn", value=source_endpoint_arn, expected_type=type_hints["source_endpoint_arn"])
            check_type(argname="argument table_mappings", value=table_mappings, expected_type=type_hints["table_mappings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_endpoint_arn", value=target_endpoint_arn, expected_type=type_hints["target_endpoint_arn"])
            check_type(argname="argument task_data", value=task_data, expected_type=type_hints["task_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cdc_start_position is not None:
            self._values["cdc_start_position"] = cdc_start_position
        if cdc_start_time is not None:
            self._values["cdc_start_time"] = cdc_start_time
        if cdc_stop_position is not None:
            self._values["cdc_stop_position"] = cdc_stop_position
        if migration_type is not None:
            self._values["migration_type"] = migration_type
        if replication_instance_arn is not None:
            self._values["replication_instance_arn"] = replication_instance_arn
        if replication_task_identifier is not None:
            self._values["replication_task_identifier"] = replication_task_identifier
        if replication_task_settings is not None:
            self._values["replication_task_settings"] = replication_task_settings
        if resource_identifier is not None:
            self._values["resource_identifier"] = resource_identifier
        if source_endpoint_arn is not None:
            self._values["source_endpoint_arn"] = source_endpoint_arn
        if table_mappings is not None:
            self._values["table_mappings"] = table_mappings
        if tags is not None:
            self._values["tags"] = tags
        if target_endpoint_arn is not None:
            self._values["target_endpoint_arn"] = target_endpoint_arn
        if task_data is not None:
            self._values["task_data"] = task_data

    @builtins.property
    def cdc_start_position(self) -> typing.Optional[builtins.str]:
        '''Indicates when you want a change data capture (CDC) operation to start.

        Use either ``CdcStartPosition`` or ``CdcStartTime`` to specify when you want a CDC operation to start. Specifying both values results in an error.

        The value can be in date, checkpoint, log sequence number (LSN), or system change number (SCN) format.

        Here is a date example: ``--cdc-start-position "2018-03-08T12:12:12"``

        Here is a checkpoint example: ``--cdc-start-position "checkpoint:V1#27#mysql-bin-changelog.157832:1975:-1:2002:677883278264080:mysql-bin-changelog.157832:1876#0#0#*#0#93"``

        Here is an LSN example: ``--cdc-start-position “mysql-bin-changelog.000024:373”``
        .. epigraph::

           When you use this task setting with a source PostgreSQL database, a logical replication slot should already be created and associated with the source endpoint. You can verify this by setting the ``slotName`` extra connection attribute to the name of this logical replication slot. For more information, see `Extra Connection Attributes When Using PostgreSQL as a Source for AWS DMS <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.PostgreSQL.html#CHAP_Source.PostgreSQL.ConnectionAttrib>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-cdcstartposition
        '''
        result = self._values.get("cdc_start_position")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdc_start_time(self) -> typing.Optional[jsii.Number]:
        '''Indicates the start time for a change data capture (CDC) operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-cdcstarttime
        '''
        result = self._values.get("cdc_start_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cdc_stop_position(self) -> typing.Optional[builtins.str]:
        '''Indicates when you want a change data capture (CDC) operation to stop.

        The value can be either server time or commit time.

        Here is a server time example: ``--cdc-stop-position "server_time:2018-02-09T12:12:12"``

        Here is a commit time example: ``--cdc-stop-position "commit_time: 2018-02-09T12:12:12"``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-cdcstopposition
        '''
        result = self._values.get("cdc_stop_position")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def migration_type(self) -> typing.Optional[builtins.str]:
        '''The migration type.

        Valid values: ``full-load`` | ``cdc`` | ``full-load-and-cdc``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-migrationtype
        '''
        result = self._values.get("migration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a replication instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-replicationinstancearn
        '''
        result = self._values.get("replication_instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_task_identifier(self) -> typing.Optional[builtins.str]:
        '''An identifier for the replication task.

        Constraints:

        - Must contain 1-255 alphanumeric characters or hyphens.
        - First character must be a letter.
        - Cannot end with a hyphen or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-replicationtaskidentifier
        '''
        result = self._values.get("replication_task_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_task_settings(self) -> typing.Optional[builtins.str]:
        '''Overall settings for the task, in JSON format.

        For more information, see `Specifying Task Settings for AWS Database Migration Service Tasks <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.html>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-replicationtasksettings
        '''
        result = self._values.get("replication_task_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''A display name for the resource identifier at the end of the ``EndpointArn`` response parameter that is returned in the created ``Endpoint`` object.

        The value for this parameter can have up to 31 characters. It can contain only ASCII letters, digits, and hyphen ('-'). Also, it can't end with a hyphen or contain two consecutive hyphens, and can only begin with a letter, such as ``Example-App-ARN1`` .

        For example, this value might result in the ``EndpointArn`` value ``arn:aws:dms:eu-west-1:012345678901:rep:Example-App-ARN1`` . If you don't specify a ``ResourceIdentifier`` value, AWS DMS generates a default identifier value for the end of ``EndpointArn`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_endpoint_arn(self) -> typing.Optional[builtins.str]:
        '''An Amazon Resource Name (ARN) that uniquely identifies the source endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-sourceendpointarn
        '''
        result = self._values.get("source_endpoint_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_mappings(self) -> typing.Optional[builtins.str]:
        '''The table mappings for the task, in JSON format.

        For more information, see `Using Table Mapping to Specify Task Settings <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TableMapping.html>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-tablemappings
        '''
        result = self._values.get("table_mappings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more tags to be assigned to the replication task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_endpoint_arn(self) -> typing.Optional[builtins.str]:
        '''An Amazon Resource Name (ARN) that uniquely identifies the target endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-targetendpointarn
        '''
        result = self._values.get("target_endpoint_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_data(self) -> typing.Optional[builtins.str]:
        '''Supplemental information that the task requires to migrate the data for certain source and target endpoints.

        For more information, see `Specifying Supplemental Data for Task Settings <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.TaskData.html>`_ in the *AWS Database Migration Service User Guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-taskdata
        '''
        result = self._values.get("task_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationTaskMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReplicationTaskPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dms.mixins.CfnReplicationTaskPropsMixin",
):
    '''The ``AWS::DMS::ReplicationTask`` resource creates an AWS DMS replication task.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html
    :cloudformationResource: AWS::DMS::ReplicationTask
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dms import mixins as dms_mixins
        
        cfn_replication_task_props_mixin = dms_mixins.CfnReplicationTaskPropsMixin(dms_mixins.CfnReplicationTaskMixinProps(
            cdc_start_position="cdcStartPosition",
            cdc_start_time=123,
            cdc_stop_position="cdcStopPosition",
            migration_type="migrationType",
            replication_instance_arn="replicationInstanceArn",
            replication_task_identifier="replicationTaskIdentifier",
            replication_task_settings="replicationTaskSettings",
            resource_identifier="resourceIdentifier",
            source_endpoint_arn="sourceEndpointArn",
            table_mappings="tableMappings",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_endpoint_arn="targetEndpointArn",
            task_data="taskData"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReplicationTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DMS::ReplicationTask``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e65e183a0175193df2e7c3e2117ebffd445611c7bca8c208b119ccbd71e49d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d24434e9505d4f6bafa856403bb588cd5ccb29058de9eda7256942553ebe1916)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857ed7cc150346694776d4d77176e76f38dd45441e03ffd5febb8a7d30430fed)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReplicationTaskMixinProps:
        return typing.cast(CfnReplicationTaskMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnCertificateMixinProps",
    "CfnCertificatePropsMixin",
    "CfnDataMigrationMixinProps",
    "CfnDataMigrationPropsMixin",
    "CfnDataProviderMixinProps",
    "CfnDataProviderPropsMixin",
    "CfnEndpointMixinProps",
    "CfnEndpointPropsMixin",
    "CfnEventSubscriptionMixinProps",
    "CfnEventSubscriptionPropsMixin",
    "CfnInstanceProfileMixinProps",
    "CfnInstanceProfilePropsMixin",
    "CfnMigrationProjectMixinProps",
    "CfnMigrationProjectPropsMixin",
    "CfnReplicationConfigMixinProps",
    "CfnReplicationConfigPropsMixin",
    "CfnReplicationInstanceMixinProps",
    "CfnReplicationInstancePropsMixin",
    "CfnReplicationSubnetGroupMixinProps",
    "CfnReplicationSubnetGroupPropsMixin",
    "CfnReplicationTaskMixinProps",
    "CfnReplicationTaskPropsMixin",
]

publication.publish()

def _typecheckingstub__c70a6c0f54de3d4c48820cbd980d20a53cad4178170227a894a9b4fd08c99a1f(
    *,
    certificate_identifier: typing.Optional[builtins.str] = None,
    certificate_pem: typing.Optional[builtins.str] = None,
    certificate_wallet: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7234037361d91287084bf54e83c54395892261316d0e6364a0a3030e7a8617(
    props: typing.Union[CfnCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee082a82efe34d44c3ecb9110a6bc379b7622b2ac0300abcfa8f59439c12b2c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d30bd0c6b668b86d7da50ebdd19c3cf59e1e3579c0bd1c4c698a78ef1f0dfc3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90dbc13e13a47cb11be71c7aa9312933ec33169a36fb281927aa87cc8ee36bf9(
    *,
    data_migration_identifier: typing.Optional[builtins.str] = None,
    data_migration_name: typing.Optional[builtins.str] = None,
    data_migration_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataMigrationPropsMixin.DataMigrationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_migration_type: typing.Optional[builtins.str] = None,
    migration_project_identifier: typing.Optional[builtins.str] = None,
    service_access_role_arn: typing.Optional[builtins.str] = None,
    source_data_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataMigrationPropsMixin.SourceDataSettingsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ad56f45c9791531457418b84e1fc66b862e627878a26c524896a179f28778d(
    props: typing.Union[CfnDataMigrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__932ba2abd6cfdd4a3c6fb01f7f486b6f4d684bf1fd9b7d1c77a0ff6e5e5ad6e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e47108af63e3a3196fa86c9628fafb0a2dc0c64749e6841826cd2ffb988af9d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b074a29c4603c3766a09f83c0bb600c7e7fb34a4061744b090a5b8e1f1e1802(
    *,
    cloudwatch_logs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    number_of_jobs: typing.Optional[jsii.Number] = None,
    selection_rules: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febf5ad16f4d461915c788bf018174e0184025fdd4dd8990859552e3a67b5765(
    *,
    cdc_start_position: typing.Optional[builtins.str] = None,
    cdc_start_time: typing.Optional[builtins.str] = None,
    cdc_stop_time: typing.Optional[builtins.str] = None,
    slot_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d4927345d0666d9a9001178c1330a615d5ce98258a5e1f39321ec0aea15380(
    *,
    data_provider_identifier: typing.Optional[builtins.str] = None,
    data_provider_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    exact_settings: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.SettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047b83c76ce3b76269f0f183b99fde0cef0ecc938f18a86ee9d7902a465bf9d8(
    props: typing.Union[CfnDataProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da92fc69cc8009cd6305c62d73c6690e0070a1994f9e478d46c4786306331d4d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f965c2bef3550e030b2ab082e4680594767f1bb89f2ab0cb3a57c5c28b828815(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7b63b32f64134a49cab5cc53172f2d392a191f418ccb5a2e0374675b026e7d(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8aae24464632da8194c4c0edff59fea61c395c83ae1e11721de742929d33537(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8391960543eeecd5e6487fbc965cbbb5300ac881b612c520fd962d994b990045(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae35873fd5ba7f5015eb9392070fe20b3ce0bb42120d9ce43173bbcddd93899(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0d9578d1246fe7d44409d8b7340727750f5da95d920958cb5a7f891f1c0603(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dafb406842c97c219ec3faa01b1f05c37df1713fadf16e04589be98d87cb9e3(
    *,
    auth_mechanism: typing.Optional[builtins.str] = None,
    auth_source: typing.Optional[builtins.str] = None,
    auth_type: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c3869ac264ec65ed20d092b3d84b8e2087218efad19450b8b12d301951b857(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31292ce834981b09d01ff3ec1420b2d85c6c6590e771777fda90f28c6885cd40(
    *,
    asm_server: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    secrets_manager_oracle_asm_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_oracle_asm_secret_id: typing.Optional[builtins.str] = None,
    secrets_manager_security_db_encryption_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_security_db_encryption_secret_id: typing.Optional[builtins.str] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629201e112f0fc80806495c56e327fe4ef59d962a6b3906d65fb3708e4b58907(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388bbdca2c2dad947685fce9cb7bb6a11bc24d43bdc597823bb2246c68715199(
    *,
    database_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    server_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72b6f2dc1862be6d2d8a14bf262d927d9bb9b11e954f246093e50e8fadcd4c7(
    *,
    doc_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.DocDbSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ibm_db2_luw_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.IbmDb2LuwSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ibm_db2_z_os_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.IbmDb2zOsSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maria_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.MariaDbSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    microsoft_sql_server_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.MicrosoftSqlServerSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mongo_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.MongoDbSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    my_sql_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.MySqlSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    oracle_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.OracleSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    postgre_sql_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.PostgreSqlSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProviderPropsMixin.RedshiftSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2684e4a60971e37b026b9a8ed0390af9df88907d73b8be26de417479dbcea603(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    doc_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.DocDbSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.DynamoDbSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    elasticsearch_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.ElasticsearchSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_identifier: typing.Optional[builtins.str] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    engine_name: typing.Optional[builtins.str] = None,
    extra_connection_attributes: typing.Optional[builtins.str] = None,
    gcp_my_sql_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.GcpMySQLSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ibm_db2_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.IbmDb2SettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kafka_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.KafkaSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.KinesisSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    microsoft_sql_server_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.MicrosoftSqlServerSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mongo_db_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.MongoDbSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    my_sql_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.MySqlSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    neptune_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.NeptuneSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    oracle_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.OracleSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    postgre_sql_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.PostgreSqlSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redis_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.RedisSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.RedshiftSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_identifier: typing.Optional[builtins.str] = None,
    s3_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.S3SettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
    sybase_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointPropsMixin.SybaseSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1455e7231f232d36be063d1bf3d562140a77f7291aa34b4a7763c7bbab0c9de(
    props: typing.Union[CfnEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50dd22fc91a7546d628d3b5fdef50a18ed4396fa38cabf613f101bdd7d139d4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f14cdb3afc1bb521ca37a1d2fdd76cf4d8c78c17d453421cd07c6cbee4e3e6ed(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef9213ce344055e1ac9a7c373ce9013bc07647250bfbdc93eec4382d646da33(
    *,
    docs_to_investigate: typing.Optional[jsii.Number] = None,
    extract_doc_id: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    nesting_level: typing.Optional[builtins.str] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9578a84443d8d08353ae2a5c12fe559666b72cfb92d8b91595bf9d2913af50c(
    *,
    service_access_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc14f1ae62f889f201dee6d174bf78afc5acce1e8454670ded2598abd736361(
    *,
    endpoint_uri: typing.Optional[builtins.str] = None,
    error_retry_duration: typing.Optional[jsii.Number] = None,
    full_load_error_percentage: typing.Optional[jsii.Number] = None,
    service_access_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aee00af5d13ce1e056e7fd111978f44e543ce60de717f370b7ac376dad83a1d(
    *,
    after_connect_script: typing.Optional[builtins.str] = None,
    clean_source_metadata_on_mismatch: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    database_name: typing.Optional[builtins.str] = None,
    events_poll_interval: typing.Optional[jsii.Number] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    parallel_load_threads: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
    server_name: typing.Optional[builtins.str] = None,
    server_timezone: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe3d1b2d109630d26637e093f5a7e1f3365c0fb37bfe415428427d9542e323c(
    *,
    current_lsn: typing.Optional[builtins.str] = None,
    keep_csv_files: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    load_timeout: typing.Optional[jsii.Number] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    max_k_bytes_per_read: typing.Optional[jsii.Number] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
    set_data_capture_changes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    write_buffer_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb2225cd664740e3203879c5c84201ba5dc2243ac35aa43b37657b1674a705a(
    *,
    broker: typing.Optional[builtins.str] = None,
    include_control_details: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_null_and_empty: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_partition_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_table_alter_operations: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_transaction_details: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    message_format: typing.Optional[builtins.str] = None,
    message_max_bytes: typing.Optional[jsii.Number] = None,
    no_hex_prefix: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    partition_include_schema_table: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    sasl_password: typing.Optional[builtins.str] = None,
    sasl_user_name: typing.Optional[builtins.str] = None,
    security_protocol: typing.Optional[builtins.str] = None,
    ssl_ca_certificate_arn: typing.Optional[builtins.str] = None,
    ssl_client_certificate_arn: typing.Optional[builtins.str] = None,
    ssl_client_key_arn: typing.Optional[builtins.str] = None,
    ssl_client_key_password: typing.Optional[builtins.str] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed12e1830ccb059c4627e6b3c51b4b3c2d26f32b5dabf6ba7ee3e9270cb018a0(
    *,
    include_control_details: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_null_and_empty: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_partition_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_table_alter_operations: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_transaction_details: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    message_format: typing.Optional[builtins.str] = None,
    no_hex_prefix: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    partition_include_schema_table: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    service_access_role_arn: typing.Optional[builtins.str] = None,
    stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c51f445e82a3d0b49f8b49b958649e47308bebb43eb574e5213fe8a2331b5c(
    *,
    bcp_packet_size: typing.Optional[jsii.Number] = None,
    control_tables_file_group: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    force_lob_lookup: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    query_single_always_on_node: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    read_backup_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    safeguard_policy: typing.Optional[builtins.str] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
    server_name: typing.Optional[builtins.str] = None,
    tlog_access_mode: typing.Optional[builtins.str] = None,
    trim_space_in_char: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_bcp_full_load: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    username: typing.Optional[builtins.str] = None,
    use_third_party_backup_device: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68bffcca7c8aefbf679c9b7df010ec968c5c47bc2ea3b44d6ea6c12cb3d3224(
    *,
    auth_mechanism: typing.Optional[builtins.str] = None,
    auth_source: typing.Optional[builtins.str] = None,
    auth_type: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    docs_to_investigate: typing.Optional[builtins.str] = None,
    extract_doc_id: typing.Optional[builtins.str] = None,
    nesting_level: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
    server_name: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae6efca6204480a1c37476798996ae31016343a2af917e34b2b9e1d677af2b2(
    *,
    after_connect_script: typing.Optional[builtins.str] = None,
    clean_source_metadata_on_mismatch: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    events_poll_interval: typing.Optional[jsii.Number] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    parallel_load_threads: typing.Optional[jsii.Number] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
    server_timezone: typing.Optional[builtins.str] = None,
    target_db_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c0754c1d032f6e7f9a6fc7f4a62b88fd0cd938aaadd2ca1ff0f413af1c644e(
    *,
    error_retry_duration: typing.Optional[jsii.Number] = None,
    iam_auth_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    max_retry_count: typing.Optional[jsii.Number] = None,
    s3_bucket_folder: typing.Optional[builtins.str] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    service_access_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ee298982a0f55d01a527bed6c28274b895389a6215139ead3e02c07cc98c18(
    *,
    access_alternate_directly: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    additional_archived_log_dest_id: typing.Optional[jsii.Number] = None,
    add_supplemental_logging: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    allow_select_nested_tables: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    archived_log_dest_id: typing.Optional[jsii.Number] = None,
    archived_logs_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    asm_password: typing.Optional[builtins.str] = None,
    asm_server: typing.Optional[builtins.str] = None,
    asm_user: typing.Optional[builtins.str] = None,
    char_length_semantics: typing.Optional[builtins.str] = None,
    direct_path_no_log: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    direct_path_parallel_load: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_homogenous_tablespace: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    extra_archived_log_dest_ids: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    fail_tasks_on_lob_truncation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    number_datatype_scale: typing.Optional[jsii.Number] = None,
    oracle_path_prefix: typing.Optional[builtins.str] = None,
    parallel_asm_read_threads: typing.Optional[jsii.Number] = None,
    read_ahead_blocks: typing.Optional[jsii.Number] = None,
    read_table_space_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    replace_path_prefix: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    retry_interval: typing.Optional[jsii.Number] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_oracle_asm_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_oracle_asm_secret_id: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
    security_db_encryption: typing.Optional[builtins.str] = None,
    security_db_encryption_name: typing.Optional[builtins.str] = None,
    spatial_data_option_to_geo_json_function_name: typing.Optional[builtins.str] = None,
    standby_delay_time: typing.Optional[jsii.Number] = None,
    use_alternate_folder_for_online: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_b_file: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_direct_path_full_load: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_logminer_reader: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_path_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0af8162afce6a0df408d4194bc26145faa2ea14b9a2339c425b1e2ddd859bc(
    *,
    after_connect_script: typing.Optional[builtins.str] = None,
    babelfish_database_name: typing.Optional[builtins.str] = None,
    capture_ddls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    database_mode: typing.Optional[builtins.str] = None,
    ddl_artifacts_schema: typing.Optional[builtins.str] = None,
    execute_timeout: typing.Optional[jsii.Number] = None,
    fail_tasks_on_lob_truncation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    heartbeat_enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    heartbeat_frequency: typing.Optional[jsii.Number] = None,
    heartbeat_schema: typing.Optional[builtins.str] = None,
    map_boolean_as_boolean: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
    slot_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a38b261c2578534b7a4157f2c20ddccdc463b805e639406be3961938c38d28d4(
    *,
    auth_password: typing.Optional[builtins.str] = None,
    auth_type: typing.Optional[builtins.str] = None,
    auth_user_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    server_name: typing.Optional[builtins.str] = None,
    ssl_ca_certificate_arn: typing.Optional[builtins.str] = None,
    ssl_security_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a5501c1d4f0cafb2dc67530f742b208a8a0822803d82053627c7384e7b75a3(
    *,
    accept_any_date: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    after_connect_script: typing.Optional[builtins.str] = None,
    bucket_folder: typing.Optional[builtins.str] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    case_sensitive_names: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    comp_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    connection_timeout: typing.Optional[jsii.Number] = None,
    date_format: typing.Optional[builtins.str] = None,
    empty_as_null: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encryption_mode: typing.Optional[builtins.str] = None,
    explicit_ids: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    file_transfer_upload_streams: typing.Optional[jsii.Number] = None,
    load_timeout: typing.Optional[jsii.Number] = None,
    map_boolean_as_boolean: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    remove_quotes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    replace_chars: typing.Optional[builtins.str] = None,
    replace_invalid_chars: typing.Optional[builtins.str] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
    server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    service_access_role_arn: typing.Optional[builtins.str] = None,
    time_format: typing.Optional[builtins.str] = None,
    trim_blanks: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    truncate_columns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    write_buffer_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41721b1b55355680c2cb8be27878390b4b6b069f0060d78a3637586ece2c3ff1(
    *,
    add_column_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    add_trailing_padding_character: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    bucket_folder: typing.Optional[builtins.str] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    canned_acl_for_objects: typing.Optional[builtins.str] = None,
    cdc_inserts_and_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cdc_inserts_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cdc_max_batch_interval: typing.Optional[jsii.Number] = None,
    cdc_min_file_size: typing.Optional[jsii.Number] = None,
    cdc_path: typing.Optional[builtins.str] = None,
    compression_type: typing.Optional[builtins.str] = None,
    csv_delimiter: typing.Optional[builtins.str] = None,
    csv_no_sup_value: typing.Optional[builtins.str] = None,
    csv_null_value: typing.Optional[builtins.str] = None,
    csv_row_delimiter: typing.Optional[builtins.str] = None,
    data_format: typing.Optional[builtins.str] = None,
    data_page_size: typing.Optional[jsii.Number] = None,
    date_partition_delimiter: typing.Optional[builtins.str] = None,
    date_partition_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    date_partition_sequence: typing.Optional[builtins.str] = None,
    date_partition_timezone: typing.Optional[builtins.str] = None,
    dict_page_size_limit: typing.Optional[jsii.Number] = None,
    enable_statistics: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encoding_type: typing.Optional[builtins.str] = None,
    encryption_mode: typing.Optional[builtins.str] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    external_table_definition: typing.Optional[builtins.str] = None,
    glue_catalog_generation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ignore_header_rows: typing.Optional[jsii.Number] = None,
    include_op_for_full_load: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    parquet_timestamp_in_millisecond: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    parquet_version: typing.Optional[builtins.str] = None,
    preserve_transactions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    rfc4180: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    row_group_length: typing.Optional[jsii.Number] = None,
    server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    service_access_role_arn: typing.Optional[builtins.str] = None,
    timestamp_column_name: typing.Optional[builtins.str] = None,
    use_csv_no_sup_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_task_start_time_for_full_load_timestamp: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c24e5b733f7f0d1e946e1431ee5c7492eafa9ab9dcaf7be77890862ce56029(
    *,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac00da3548a0afa219f29ba69252956da60483eb5cda8543b983a29e2b637329(
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

def _typecheckingstub__a013588cfd17d4e203568f869048f3975534ed0d277dd3f16872c4b60b05784a(
    props: typing.Union[CfnEventSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0647b49d8cc5318e90498c0d1c3e4182c78a4ecb975ae0d3425d3c771c1918de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a231fc1a057af8e51d08e588cb945e8c0d63d5128f2260a859ab34f9663fbf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3ef36481270e451e68307a84256acf375ed5e99c929040304cbe5f3def2d73(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    instance_profile_identifier: typing.Optional[builtins.str] = None,
    instance_profile_name: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    subnet_group_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c22fd11d61f0b6c03bafe36f7fd87b98fbe6551f9b88c369de096f7585f9cd4(
    props: typing.Union[CfnInstanceProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def172694a05f4fbe454d4ba91fd398339500e03310cb259f4152950eb87f7e8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87de77a2832e8bafcc05a3611c6f254e5c71a451d98e4b8295e76904ba5e04c3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf8990bdecb2213bb0145bd4157e6eaa6f46612b78973639baa937d8d007071(
    *,
    description: typing.Optional[builtins.str] = None,
    instance_profile_arn: typing.Optional[builtins.str] = None,
    instance_profile_identifier: typing.Optional[builtins.str] = None,
    instance_profile_name: typing.Optional[builtins.str] = None,
    migration_project_creation_time: typing.Optional[builtins.str] = None,
    migration_project_identifier: typing.Optional[builtins.str] = None,
    migration_project_name: typing.Optional[builtins.str] = None,
    schema_conversion_application_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMigrationProjectPropsMixin.SchemaConversionApplicationAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_data_provider_descriptors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_data_provider_descriptors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMigrationProjectPropsMixin.DataProviderDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    transformation_rules: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8934ec44c8ff24c57609ea12ca75e4eef87828d4239f134d7a0c7175e6d89b89(
    props: typing.Union[CfnMigrationProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad76f390f976ead30afbfb362c54b9f07300328ccff295c917564a42b7c5aa35(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3048d29f27869462b1b0ddda911a766d6cb10b085a2f70790b3e6a010e26ad78(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acde54536e87acdd3e7c114fb4b0c0504525cd8b12cff978dbc8befd54e73f50(
    *,
    data_provider_arn: typing.Optional[builtins.str] = None,
    data_provider_identifier: typing.Optional[builtins.str] = None,
    data_provider_name: typing.Optional[builtins.str] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2476c05a0807867cb60ff12a6a6a549a2813919d95c7192d6d958f79c6112a(
    *,
    s3_bucket_path: typing.Optional[builtins.str] = None,
    s3_bucket_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84aee5810690dc43468cacc39b7b24845337c37258b5fa8c25e7bf8d717e059(
    *,
    compute_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationConfigPropsMixin.ComputeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    replication_config_identifier: typing.Optional[builtins.str] = None,
    replication_settings: typing.Any = None,
    replication_type: typing.Optional[builtins.str] = None,
    resource_identifier: typing.Optional[builtins.str] = None,
    source_endpoint_arn: typing.Optional[builtins.str] = None,
    supplemental_settings: typing.Any = None,
    table_mappings: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_endpoint_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb432619c78e8ee3c8204cd14c714c30b3c4b5304d42fc8990721c28553ff40b(
    props: typing.Union[CfnReplicationConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469dfaf49e432657eb2c8b61e97032f2eb368796f63326307b4a3febdf1219cc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba96e8fb8aa4946159809c94ad5c71b5ab9cbe036eba1337ef47c34fc57841b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d6d556c880cc6f04e65b6a7eb34dc64783ff6d162ed267bea47aa952183521(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    dns_name_servers: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    max_capacity_units: typing.Optional[jsii.Number] = None,
    min_capacity_units: typing.Optional[jsii.Number] = None,
    multi_az: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    replication_subnet_group_id: typing.Optional[builtins.str] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebaa16805e9cdcab8fac4057a1720d597407c62be325ac765d925bcf2d14e6c(
    *,
    allocated_storage: typing.Optional[jsii.Number] = None,
    allow_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    dns_name_servers: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    multi_az: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    network_type: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    replication_instance_class: typing.Optional[builtins.str] = None,
    replication_instance_identifier: typing.Optional[builtins.str] = None,
    replication_subnet_group_identifier: typing.Optional[builtins.str] = None,
    resource_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb44d8fe9c688960382dd94cbd90ce05df149e600bbcb1483acaaff1fab1f5b(
    props: typing.Union[CfnReplicationInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537dcc1c3964cfe5121e575dd3da9ffa94cbce543133f00f103747ddf4ba90b8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e433d47bf66c5d4670a7ac715b5cc22baac2740bd76c8e26b51bbde262312d06(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63ce34a98449a9e64fdf78c2e5c159ff0b4c4f00c7fe5a1b65838b421476d7e(
    *,
    replication_subnet_group_description: typing.Optional[builtins.str] = None,
    replication_subnet_group_identifier: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9101ba56a590aa025d7a09a35454895b199fb70607413bcaa3e3bb0f3de5e75c(
    props: typing.Union[CfnReplicationSubnetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb6f0074c9438576013414a5e7e9fc0960941bde4c7e0fb0592c228f935621c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf905495a08d179c62181ff0a8d542dd3efb81fa4dddd6a133a8de1121fbafde(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477ced8acd9881a3ac17d27cfb65e246432478e379680052f47536adb2f5d480(
    *,
    cdc_start_position: typing.Optional[builtins.str] = None,
    cdc_start_time: typing.Optional[jsii.Number] = None,
    cdc_stop_position: typing.Optional[builtins.str] = None,
    migration_type: typing.Optional[builtins.str] = None,
    replication_instance_arn: typing.Optional[builtins.str] = None,
    replication_task_identifier: typing.Optional[builtins.str] = None,
    replication_task_settings: typing.Optional[builtins.str] = None,
    resource_identifier: typing.Optional[builtins.str] = None,
    source_endpoint_arn: typing.Optional[builtins.str] = None,
    table_mappings: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_endpoint_arn: typing.Optional[builtins.str] = None,
    task_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e65e183a0175193df2e7c3e2117ebffd445611c7bca8c208b119ccbd71e49d(
    props: typing.Union[CfnReplicationTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24434e9505d4f6bafa856403bb588cd5ccb29058de9eda7256942553ebe1916(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857ed7cc150346694776d4d77176e76f38dd45441e03ffd5febb8a7d30430fed(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
