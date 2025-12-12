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
    jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnAwsLogSourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accounts": "accounts",
        "data_lake_arn": "dataLakeArn",
        "source_name": "sourceName",
        "source_version": "sourceVersion",
    },
)
class CfnAwsLogSourceMixinProps:
    def __init__(
        self,
        *,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_lake_arn: typing.Optional[builtins.str] = None,
        source_name: typing.Optional[builtins.str] = None,
        source_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAwsLogSourcePropsMixin.

        :param accounts: Specify the AWS account information where you want to enable Security Lake.
        :param data_lake_arn: The Amazon Resource Name (ARN) used to create the data lake.
        :param source_name: The name for a AWS source. This must be a Regionally unique value. For the list of sources supported by Amazon Security Lake see `Collecting data from AWS services <https://docs.aws.amazon.com//security-lake/latest/userguide/internal-sources.html>`_ in the Amazon Security Lake User Guide.
        :param source_version: The version for a AWS source. For more details about source versions supported by Amazon Security Lake see `OCSF source identification <https://docs.aws.amazon.com//security-lake/latest/userguide/open-cybersecurity-schema-framework.html#ocsf-source-identification>`_ in the Amazon Security Lake User Guide. This must be a Regionally unique value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-awslogsource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
            
            cfn_aws_log_source_mixin_props = securitylake_mixins.CfnAwsLogSourceMixinProps(
                accounts=["accounts"],
                data_lake_arn="dataLakeArn",
                source_name="sourceName",
                source_version="sourceVersion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f24bf3bfafa048d904c5c1bb01daa333ea1804134b0736521fe79171f6dbdf)
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument data_lake_arn", value=data_lake_arn, expected_type=type_hints["data_lake_arn"])
            check_type(argname="argument source_name", value=source_name, expected_type=type_hints["source_name"])
            check_type(argname="argument source_version", value=source_version, expected_type=type_hints["source_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accounts is not None:
            self._values["accounts"] = accounts
        if data_lake_arn is not None:
            self._values["data_lake_arn"] = data_lake_arn
        if source_name is not None:
            self._values["source_name"] = source_name
        if source_version is not None:
            self._values["source_version"] = source_version

    @builtins.property
    def accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify the AWS account information where you want to enable Security Lake.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-awslogsource.html#cfn-securitylake-awslogsource-accounts
        '''
        result = self._values.get("accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def data_lake_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) used to create the data lake.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-awslogsource.html#cfn-securitylake-awslogsource-datalakearn
        '''
        result = self._values.get("data_lake_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_name(self) -> typing.Optional[builtins.str]:
        '''The name for a AWS source.

        This must be a Regionally unique value. For the list of sources supported by Amazon Security Lake see `Collecting data from AWS services <https://docs.aws.amazon.com//security-lake/latest/userguide/internal-sources.html>`_ in the Amazon Security Lake User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-awslogsource.html#cfn-securitylake-awslogsource-sourcename
        '''
        result = self._values.get("source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_version(self) -> typing.Optional[builtins.str]:
        '''The version for a AWS source.

        For more details about source versions supported by Amazon Security Lake see `OCSF source identification <https://docs.aws.amazon.com//security-lake/latest/userguide/open-cybersecurity-schema-framework.html#ocsf-source-identification>`_ in the Amazon Security Lake User Guide. This must be a Regionally unique value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-awslogsource.html#cfn-securitylake-awslogsource-sourceversion
        '''
        result = self._values.get("source_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAwsLogSourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAwsLogSourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnAwsLogSourcePropsMixin",
):
    '''Adds a natively supported AWS service as an AWS source.

    Enables source types for member accounts in required AWS Regions, based on the parameters you specify. You can choose any source type in any Region for either accounts that are part of a trusted organization or standalone accounts. Once you add an AWS service as a source, Security Lake starts collecting logs and events from it.
    .. epigraph::

       If you want to create multiple sources using ``AWS::SecurityLake::AwsLogSource`` , you must use the ``DependsOn`` attribute to create the sources sequentially. With the ``DependsOn`` attribute you can specify that the creation of a specific ``AWSLogSource`` follows another. When you add a ``DependsOn`` attribute to a resource, that resource is created only after the creation of the resource specified in the ``DependsOn`` attribute. For an example, see `Add AWS log sources <https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-awslogsource.html#aws-resource-securitylake-awslogsource--examples>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-awslogsource.html
    :cloudformationResource: AWS::SecurityLake::AwsLogSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
        
        cfn_aws_log_source_props_mixin = securitylake_mixins.CfnAwsLogSourcePropsMixin(securitylake_mixins.CfnAwsLogSourceMixinProps(
            accounts=["accounts"],
            data_lake_arn="dataLakeArn",
            source_name="sourceName",
            source_version="sourceVersion"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAwsLogSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityLake::AwsLogSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4ebf8c35f921877764f0472f5d2b174c71b4e9e5d53ccf8770b09e02ce53a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbbc739640d512d4046c6a70a2590df4e88cb9cec0a5ae54df0791f69afa52a7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e53ed1b50c7a198e3496bbdb1028e0a1adf0408ff84cb16325a3b215a6845dc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAwsLogSourceMixinProps:
        return typing.cast(CfnAwsLogSourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnDataLakeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_configuration": "encryptionConfiguration",
        "lifecycle_configuration": "lifecycleConfiguration",
        "meta_store_manager_role_arn": "metaStoreManagerRoleArn",
        "replication_configuration": "replicationConfiguration",
        "tags": "tags",
    },
)
class CfnDataLakeMixinProps:
    def __init__(
        self,
        *,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataLakePropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataLakePropsMixin.LifecycleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        meta_store_manager_role_arn: typing.Optional[builtins.str] = None,
        replication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataLakePropsMixin.ReplicationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataLakePropsMixin.

        :param encryption_configuration: Provides encryption details of the Amazon Security Lake object.
        :param lifecycle_configuration: You can customize Security Lake to store data in your preferred AWS Regions for your preferred amount of time. Lifecycle management can help you comply with different compliance requirements. For more details, see `Lifecycle management <https://docs.aws.amazon.com//security-lake/latest/userguide/lifecycle-management.html>`_ in the Amazon Security Lake User Guide.
        :param meta_store_manager_role_arn: The Amazon Resource Name (ARN) used to create and update the AWS Glue table. This table contains partitions generated by the ingestion and normalization of AWS log sources and custom sources.
        :param replication_configuration: Provides replication details of Amazon Security Lake object.
        :param tags: An array of objects, one for each tag to associate with the data lake configuration. For each tag, you must specify both a tag key and a tag value. A tag value cannot be null, but it can be an empty string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-datalake.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
            
            cfn_data_lake_mixin_props = securitylake_mixins.CfnDataLakeMixinProps(
                encryption_configuration=securitylake_mixins.CfnDataLakePropsMixin.EncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                ),
                lifecycle_configuration=securitylake_mixins.CfnDataLakePropsMixin.LifecycleConfigurationProperty(
                    expiration=securitylake_mixins.CfnDataLakePropsMixin.ExpirationProperty(
                        days=123
                    ),
                    transitions=[securitylake_mixins.CfnDataLakePropsMixin.TransitionsProperty(
                        days=123,
                        storage_class="storageClass"
                    )]
                ),
                meta_store_manager_role_arn="metaStoreManagerRoleArn",
                replication_configuration=securitylake_mixins.CfnDataLakePropsMixin.ReplicationConfigurationProperty(
                    regions=["regions"],
                    role_arn="roleArn"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a09317cb1bbdaa1c57b0b56a3269cae1e6c67e147b6ac42e5b741df7404070)
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument lifecycle_configuration", value=lifecycle_configuration, expected_type=type_hints["lifecycle_configuration"])
            check_type(argname="argument meta_store_manager_role_arn", value=meta_store_manager_role_arn, expected_type=type_hints["meta_store_manager_role_arn"])
            check_type(argname="argument replication_configuration", value=replication_configuration, expected_type=type_hints["replication_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if lifecycle_configuration is not None:
            self._values["lifecycle_configuration"] = lifecycle_configuration
        if meta_store_manager_role_arn is not None:
            self._values["meta_store_manager_role_arn"] = meta_store_manager_role_arn
        if replication_configuration is not None:
            self._values["replication_configuration"] = replication_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakePropsMixin.EncryptionConfigurationProperty"]]:
        '''Provides encryption details of the Amazon Security Lake object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-datalake.html#cfn-securitylake-datalake-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakePropsMixin.EncryptionConfigurationProperty"]], result)

    @builtins.property
    def lifecycle_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakePropsMixin.LifecycleConfigurationProperty"]]:
        '''You can customize Security Lake to store data in your preferred AWS Regions for your preferred amount of time.

        Lifecycle management can help you comply with different compliance requirements. For more details, see `Lifecycle management <https://docs.aws.amazon.com//security-lake/latest/userguide/lifecycle-management.html>`_ in the Amazon Security Lake User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-datalake.html#cfn-securitylake-datalake-lifecycleconfiguration
        '''
        result = self._values.get("lifecycle_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakePropsMixin.LifecycleConfigurationProperty"]], result)

    @builtins.property
    def meta_store_manager_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) used to create and update the AWS Glue table.

        This table contains partitions generated by the ingestion and normalization of AWS log sources and custom sources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-datalake.html#cfn-securitylake-datalake-metastoremanagerrolearn
        '''
        result = self._values.get("meta_store_manager_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakePropsMixin.ReplicationConfigurationProperty"]]:
        '''Provides replication details of Amazon Security Lake object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-datalake.html#cfn-securitylake-datalake-replicationconfiguration
        '''
        result = self._values.get("replication_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakePropsMixin.ReplicationConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of objects, one for each tag to associate with the data lake configuration.

        For each tag, you must specify both a tag key and a tag value. A tag value cannot be null, but it can be an empty string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-datalake.html#cfn-securitylake-datalake-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataLakeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataLakePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnDataLakePropsMixin",
):
    '''Initializes an Amazon Security Lake instance with the provided (or default) configuration.

    You can enable Security Lake in AWS Regions with customized settings before enabling log collection in Regions. To specify particular Regions, configure these Regions using the ``configurations`` parameter. If you have already enabled Security Lake in a Region when you call this command, the command will update the Region if you provide new configuration parameters. If you have not already enabled Security Lake in the Region when you call this API, it will set up the data lake in the Region with the specified configurations.

    When you enable Security Lake , it starts ingesting security data after the ``CreateAwsLogSource`` call. This includes ingesting security data from sources, storing data, and making data accessible to subscribers. Security Lake also enables all the existing settings and resources that it stores or maintains for your AWS account in the current Region, including security log and event data. For more information, see the `Amazon Security Lake User Guide <https://docs.aws.amazon.com//security-lake/latest/userguide/what-is-security-lake.html>`_ .
    .. epigraph::

       If you use this template to create multiple data lakes in different AWS Regions , and more than one of your data lakes include an `AWS::SecurityLake::AwsLogSource <https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-awslogsource.html>`_ resource, then you must deploy these data lakes sequentially. This is required because data lakes operate globally, and ``AwsLogSource`` resources must be deployed one at a time.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-datalake.html
    :cloudformationResource: AWS::SecurityLake::DataLake
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
        
        cfn_data_lake_props_mixin = securitylake_mixins.CfnDataLakePropsMixin(securitylake_mixins.CfnDataLakeMixinProps(
            encryption_configuration=securitylake_mixins.CfnDataLakePropsMixin.EncryptionConfigurationProperty(
                kms_key_id="kmsKeyId"
            ),
            lifecycle_configuration=securitylake_mixins.CfnDataLakePropsMixin.LifecycleConfigurationProperty(
                expiration=securitylake_mixins.CfnDataLakePropsMixin.ExpirationProperty(
                    days=123
                ),
                transitions=[securitylake_mixins.CfnDataLakePropsMixin.TransitionsProperty(
                    days=123,
                    storage_class="storageClass"
                )]
            ),
            meta_store_manager_role_arn="metaStoreManagerRoleArn",
            replication_configuration=securitylake_mixins.CfnDataLakePropsMixin.ReplicationConfigurationProperty(
                regions=["regions"],
                role_arn="roleArn"
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
        props: typing.Union[CfnDataLakeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityLake::DataLake``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350bac982d1d09da737943c705ad120726fe598fedeae3443f559e66c42af98f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2c41e0a6719f85b9cef144a0bbce8e4bdc2cd3ad99723ee75b2cce903bafb7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf2a87219115ff0831d518217a17b120dd22ae72b55a458918b807833b28beb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataLakeMixinProps:
        return typing.cast(CfnDataLakeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnDataLakePropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class EncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
            '''Provides encryption details of the Amazon Security Lake object.

            The AWS shared responsibility model applies to data protection in Amazon Security Lake . As described in this model, AWS is responsible for protecting the global infrastructure that runs all of the AWS Cloud. You are responsible for maintaining control over your content that is hosted on this infrastructure. For more details, see `Data protection <https://docs.aws.amazon.com//security-lake/latest/userguide/data-protection.html>`_ in the Amazon Security Lake User Guide.

            :param kms_key_id: The ID of KMS encryption key used by Amazon Security Lake to encrypt the Security Lake object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                encryption_configuration_property = securitylake_mixins.CfnDataLakePropsMixin.EncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c857060d0034698133e49fca7d58958af177d1813fa5399241a55610631ccdb)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ID of KMS encryption key used by Amazon Security Lake to encrypt the Security Lake object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-encryptionconfiguration.html#cfn-securitylake-datalake-encryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
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
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnDataLakePropsMixin.ExpirationProperty",
        jsii_struct_bases=[],
        name_mapping={"days": "days"},
    )
    class ExpirationProperty:
        def __init__(self, *, days: typing.Optional[jsii.Number] = None) -> None:
            '''Provides data expiration details of the Amazon Security Lake object.

            You can specify your preferred Amazon S3 storage class and the time period for S3 objects to stay in that storage class before they expire. For more information about Amazon S3 Lifecycle configurations, see `Managing your storage lifecycle <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :param days: The number of days before data expires in the Amazon Security Lake object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-expiration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                expiration_property = securitylake_mixins.CfnDataLakePropsMixin.ExpirationProperty(
                    days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5786e59b6f18a90971c7a28d79eed1b9858e41830b6968c6c8962e7bb4d21646)
                check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days is not None:
                self._values["days"] = days

        @builtins.property
        def days(self) -> typing.Optional[jsii.Number]:
            '''The number of days before data expires in the Amazon Security Lake object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-expiration.html#cfn-securitylake-datalake-expiration-days
            '''
            result = self._values.get("days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExpirationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnDataLakePropsMixin.LifecycleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"expiration": "expiration", "transitions": "transitions"},
    )
    class LifecycleConfigurationProperty:
        def __init__(
            self,
            *,
            expiration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataLakePropsMixin.ExpirationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            transitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataLakePropsMixin.TransitionsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides lifecycle details of Amazon Security Lake object.

            To manage your data so that it is stored cost effectively, you can configure retention settings for the data. You can specify your preferred Amazon S3 storage class and the time period for Amazon S3 objects to stay in that storage class before they transition to a different storage class or expire. For more information about Amazon S3 Lifecycle configurations, see `Managing your storage lifecycle <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>`_ in the *Amazon Simple Storage Service User Guide* .

            In Security Lake , you specify retention settings at the Region level. For example, you might choose to transition all S3 objects in a specific AWS Region to the ``S3 Standard-IA`` storage class 30 days after they're written to the data lake. The default Amazon S3 storage class is S3 Standard.
            .. epigraph::

               Security Lake doesn't support Amazon S3 Object Lock. When the data lake buckets are created, S3 Object Lock is disabled by default. Enabling S3 Object Lock with default retention mode interrupts the delivery of normalized log data to the data lake.

            :param expiration: Provides data expiration details of the Amazon Security Lake object.
            :param transitions: Provides data storage transition details of Amazon Security Lake object. By configuring these settings, you can specify your preferred Amazon S3 storage class and the time period for S3 objects to stay in that storage class before they transition to a different storage class.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-lifecycleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                lifecycle_configuration_property = securitylake_mixins.CfnDataLakePropsMixin.LifecycleConfigurationProperty(
                    expiration=securitylake_mixins.CfnDataLakePropsMixin.ExpirationProperty(
                        days=123
                    ),
                    transitions=[securitylake_mixins.CfnDataLakePropsMixin.TransitionsProperty(
                        days=123,
                        storage_class="storageClass"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58a39b924cd34ddc03a801a1311947197a5d966e3c46903c429589dc883a0811)
                check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
                check_type(argname="argument transitions", value=transitions, expected_type=type_hints["transitions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expiration is not None:
                self._values["expiration"] = expiration
            if transitions is not None:
                self._values["transitions"] = transitions

        @builtins.property
        def expiration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakePropsMixin.ExpirationProperty"]]:
            '''Provides data expiration details of the Amazon Security Lake object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-lifecycleconfiguration.html#cfn-securitylake-datalake-lifecycleconfiguration-expiration
            '''
            result = self._values.get("expiration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakePropsMixin.ExpirationProperty"]], result)

        @builtins.property
        def transitions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakePropsMixin.TransitionsProperty"]]]]:
            '''Provides data storage transition details of Amazon Security Lake object.

            By configuring these settings, you can specify your preferred Amazon S3 storage class and the time period for S3 objects to stay in that storage class before they transition to a different storage class.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-lifecycleconfiguration.html#cfn-securitylake-datalake-lifecycleconfiguration-transitions
            '''
            result = self._values.get("transitions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakePropsMixin.TransitionsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnDataLakePropsMixin.ReplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"regions": "regions", "role_arn": "roleArn"},
    )
    class ReplicationConfigurationProperty:
        def __init__(
            self,
            *,
            regions: typing.Optional[typing.Sequence[builtins.str]] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides replication configuration details for objects stored in the Amazon Security Lake data lake.

            :param regions: Specifies one or more centralized rollup Regions. The AWS Region specified in the region parameter of the ``CreateDataLake`` or ``UpdateDataLake`` operations contributes data to the rollup Region or Regions specified in this parameter. Replication enables automatic, asynchronous copying of objects across Amazon S3 buckets. S3 buckets that are configured for object replication can be owned by the same AWS account or by different accounts. You can replicate objects to a single destination bucket or to multiple destination buckets. The destination buckets can be in different Regions or within the same Region as the source bucket.
            :param role_arn: Replication settings for the Amazon S3 buckets. This parameter uses the AWS Identity and Access Management (IAM) role you created that is managed by Security Lake , to ensure the replication setting is correct.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-replicationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                replication_configuration_property = securitylake_mixins.CfnDataLakePropsMixin.ReplicationConfigurationProperty(
                    regions=["regions"],
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e01f1d92de1efb9177fc0e3004eadcdacf54a0a4058c4009e1eff57a9543bcc)
                check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if regions is not None:
                self._values["regions"] = regions
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies one or more centralized rollup Regions.

            The AWS Region specified in the region parameter of the ``CreateDataLake`` or ``UpdateDataLake`` operations contributes data to the rollup Region or Regions specified in this parameter.

            Replication enables automatic, asynchronous copying of objects across Amazon S3 buckets. S3 buckets that are configured for object replication can be owned by the same AWS account or by different accounts. You can replicate objects to a single destination bucket or to multiple destination buckets. The destination buckets can be in different Regions or within the same Region as the source bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-replicationconfiguration.html#cfn-securitylake-datalake-replicationconfiguration-regions
            '''
            result = self._values.get("regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''Replication settings for the Amazon S3 buckets.

            This parameter uses the AWS Identity and Access Management (IAM) role you created that is managed by Security Lake , to ensure the replication setting is correct.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-replicationconfiguration.html#cfn-securitylake-datalake-replicationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnDataLakePropsMixin.TransitionsProperty",
        jsii_struct_bases=[],
        name_mapping={"days": "days", "storage_class": "storageClass"},
    )
    class TransitionsProperty:
        def __init__(
            self,
            *,
            days: typing.Optional[jsii.Number] = None,
            storage_class: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides transition lifecycle details of the Amazon Security Lake object.

            For more information about Amazon S3 Lifecycle configurations, see `Managing your storage lifecycle <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :param days: The number of days before data transitions to a different S3 Storage Class in the Amazon Security Lake object.
            :param storage_class: The list of storage classes that you can choose from based on the data access, resiliency, and cost requirements of your workloads. The default storage class is *S3 Standard* . For information about other storage classes, see `Setting the storage class of an object <https://docs.aws.amazon.com/AmazonS3/latest/userguide/sc-howtoset.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-transitions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                transitions_property = securitylake_mixins.CfnDataLakePropsMixin.TransitionsProperty(
                    days=123,
                    storage_class="storageClass"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5cd8dba762f9a465575ad1df9b553cde8928b7c130117a0380a6be3934db2cf)
                check_type(argname="argument days", value=days, expected_type=type_hints["days"])
                check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days is not None:
                self._values["days"] = days
            if storage_class is not None:
                self._values["storage_class"] = storage_class

        @builtins.property
        def days(self) -> typing.Optional[jsii.Number]:
            '''The number of days before data transitions to a different S3 Storage Class in the Amazon Security Lake object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-transitions.html#cfn-securitylake-datalake-transitions-days
            '''
            result = self._values.get("days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def storage_class(self) -> typing.Optional[builtins.str]:
            '''The list of storage classes that you can choose from based on the data access, resiliency, and cost requirements of your workloads.

            The default storage class is *S3 Standard* . For information about other storage classes, see `Setting the storage class of an object <https://docs.aws.amazon.com/AmazonS3/latest/userguide/sc-howtoset.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-datalake-transitions.html#cfn-securitylake-datalake-transitions-storageclass
            '''
            result = self._values.get("storage_class")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransitionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnSubscriberMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_types": "accessTypes",
        "data_lake_arn": "dataLakeArn",
        "sources": "sources",
        "subscriber_description": "subscriberDescription",
        "subscriber_identity": "subscriberIdentity",
        "subscriber_name": "subscriberName",
        "tags": "tags",
    },
)
class CfnSubscriberMixinProps:
    def __init__(
        self,
        *,
        access_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_lake_arn: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSubscriberPropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subscriber_description: typing.Optional[builtins.str] = None,
        subscriber_identity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSubscriberPropsMixin.SubscriberIdentityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subscriber_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSubscriberPropsMixin.

        :param access_types: You can choose to notify subscribers of new objects with an Amazon Simple Queue Service (Amazon SQS) queue or through messaging to an HTTPS endpoint provided by the subscriber. Subscribers can consume data by directly querying AWS Lake Formation tables in your Amazon S3 bucket through services like Amazon Athena. This subscription type is defined as ``LAKEFORMATION`` .
        :param data_lake_arn: The Amazon Resource Name (ARN) used to create the data lake.
        :param sources: Amazon Security Lake supports log and event collection for natively supported AWS services . For more information, see the `Amazon Security Lake User Guide <https://docs.aws.amazon.com//security-lake/latest/userguide/source-management.html>`_ .
        :param subscriber_description: The subscriber descriptions for a subscriber account. The description for a subscriber includes ``subscriberName`` , ``accountID`` , ``externalID`` , and ``subscriberId`` .
        :param subscriber_identity: The AWS identity used to access your data.
        :param subscriber_name: The name of your Amazon Security Lake subscriber account.
        :param tags: An array of objects, one for each tag to associate with the subscriber. For each tag, you must specify both a tag key and a tag value. A tag value cannot be null, but it can be an empty string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscriber.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
            
            cfn_subscriber_mixin_props = securitylake_mixins.CfnSubscriberMixinProps(
                access_types=["accessTypes"],
                data_lake_arn="dataLakeArn",
                sources=[securitylake_mixins.CfnSubscriberPropsMixin.SourceProperty(
                    aws_log_source=securitylake_mixins.CfnSubscriberPropsMixin.AwsLogSourceProperty(
                        source_name="sourceName",
                        source_version="sourceVersion"
                    ),
                    custom_log_source=securitylake_mixins.CfnSubscriberPropsMixin.CustomLogSourceProperty(
                        source_name="sourceName",
                        source_version="sourceVersion"
                    )
                )],
                subscriber_description="subscriberDescription",
                subscriber_identity=securitylake_mixins.CfnSubscriberPropsMixin.SubscriberIdentityProperty(
                    external_id="externalId",
                    principal="principal"
                ),
                subscriber_name="subscriberName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3546819b9ab16b1a8aa6b4ef8a0d6cd25af66e284cfbce5dd06f7f68e4d5a2a)
            check_type(argname="argument access_types", value=access_types, expected_type=type_hints["access_types"])
            check_type(argname="argument data_lake_arn", value=data_lake_arn, expected_type=type_hints["data_lake_arn"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument subscriber_description", value=subscriber_description, expected_type=type_hints["subscriber_description"])
            check_type(argname="argument subscriber_identity", value=subscriber_identity, expected_type=type_hints["subscriber_identity"])
            check_type(argname="argument subscriber_name", value=subscriber_name, expected_type=type_hints["subscriber_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_types is not None:
            self._values["access_types"] = access_types
        if data_lake_arn is not None:
            self._values["data_lake_arn"] = data_lake_arn
        if sources is not None:
            self._values["sources"] = sources
        if subscriber_description is not None:
            self._values["subscriber_description"] = subscriber_description
        if subscriber_identity is not None:
            self._values["subscriber_identity"] = subscriber_identity
        if subscriber_name is not None:
            self._values["subscriber_name"] = subscriber_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''You can choose to notify subscribers of new objects with an Amazon Simple Queue Service (Amazon SQS) queue or through messaging to an HTTPS endpoint provided by the subscriber.

        Subscribers can consume data by directly querying AWS Lake Formation tables in your Amazon S3 bucket through services like Amazon Athena. This subscription type is defined as ``LAKEFORMATION`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscriber.html#cfn-securitylake-subscriber-accesstypes
        '''
        result = self._values.get("access_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def data_lake_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) used to create the data lake.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscriber.html#cfn-securitylake-subscriber-datalakearn
        '''
        result = self._values.get("data_lake_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberPropsMixin.SourceProperty"]]]]:
        '''Amazon Security Lake supports log and event collection for natively supported AWS services .

        For more information, see the `Amazon Security Lake User Guide <https://docs.aws.amazon.com//security-lake/latest/userguide/source-management.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscriber.html#cfn-securitylake-subscriber-sources
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberPropsMixin.SourceProperty"]]]], result)

    @builtins.property
    def subscriber_description(self) -> typing.Optional[builtins.str]:
        '''The subscriber descriptions for a subscriber account.

        The description for a subscriber includes ``subscriberName`` , ``accountID`` , ``externalID`` , and ``subscriberId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscriber.html#cfn-securitylake-subscriber-subscriberdescription
        '''
        result = self._values.get("subscriber_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscriber_identity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberPropsMixin.SubscriberIdentityProperty"]]:
        '''The AWS identity used to access your data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscriber.html#cfn-securitylake-subscriber-subscriberidentity
        '''
        result = self._values.get("subscriber_identity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberPropsMixin.SubscriberIdentityProperty"]], result)

    @builtins.property
    def subscriber_name(self) -> typing.Optional[builtins.str]:
        '''The name of your Amazon Security Lake subscriber account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscriber.html#cfn-securitylake-subscriber-subscribername
        '''
        result = self._values.get("subscriber_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of objects, one for each tag to associate with the subscriber.

        For each tag, you must specify both a tag key and a tag value. A tag value cannot be null, but it can be an empty string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscriber.html#cfn-securitylake-subscriber-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriberMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnSubscriberNotificationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "notification_configuration": "notificationConfiguration",
        "subscriber_arn": "subscriberArn",
    },
)
class CfnSubscriberNotificationMixinProps:
    def __init__(
        self,
        *,
        notification_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSubscriberNotificationPropsMixin.NotificationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subscriber_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSubscriberNotificationPropsMixin.

        :param notification_configuration: Specify the configurations you want to use for subscriber notification. The subscriber is notified when new data is written to the data lake for sources that the subscriber consumes in Security Lake .
        :param subscriber_arn: The Amazon Resource Name (ARN) of the Security Lake subscriber.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscribernotification.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
            
            # sqs_notification_configuration: Any
            
            cfn_subscriber_notification_mixin_props = securitylake_mixins.CfnSubscriberNotificationMixinProps(
                notification_configuration=securitylake_mixins.CfnSubscriberNotificationPropsMixin.NotificationConfigurationProperty(
                    https_notification_configuration=securitylake_mixins.CfnSubscriberNotificationPropsMixin.HttpsNotificationConfigurationProperty(
                        authorization_api_key_name="authorizationApiKeyName",
                        authorization_api_key_value="authorizationApiKeyValue",
                        endpoint="endpoint",
                        http_method="httpMethod",
                        target_role_arn="targetRoleArn"
                    ),
                    sqs_notification_configuration=sqs_notification_configuration
                ),
                subscriber_arn="subscriberArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de404ba8f121013453ed61450eb8a36a2a1310dd505a93cadfacc4e640f5f45)
            check_type(argname="argument notification_configuration", value=notification_configuration, expected_type=type_hints["notification_configuration"])
            check_type(argname="argument subscriber_arn", value=subscriber_arn, expected_type=type_hints["subscriber_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if notification_configuration is not None:
            self._values["notification_configuration"] = notification_configuration
        if subscriber_arn is not None:
            self._values["subscriber_arn"] = subscriber_arn

    @builtins.property
    def notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberNotificationPropsMixin.NotificationConfigurationProperty"]]:
        '''Specify the configurations you want to use for subscriber notification.

        The subscriber is notified when new data is written to the data lake for sources that the subscriber consumes in Security Lake .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscribernotification.html#cfn-securitylake-subscribernotification-notificationconfiguration
        '''
        result = self._values.get("notification_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberNotificationPropsMixin.NotificationConfigurationProperty"]], result)

    @builtins.property
    def subscriber_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Security Lake subscriber.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscribernotification.html#cfn-securitylake-subscribernotification-subscriberarn
        '''
        result = self._values.get("subscriber_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriberNotificationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSubscriberNotificationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnSubscriberNotificationPropsMixin",
):
    '''Notifies the subscriber when new data is written to the data lake for the sources that the subscriber consumes in Security Lake.

    You can create only one subscriber notification per subscriber.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscribernotification.html
    :cloudformationResource: AWS::SecurityLake::SubscriberNotification
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
        
        # sqs_notification_configuration: Any
        
        cfn_subscriber_notification_props_mixin = securitylake_mixins.CfnSubscriberNotificationPropsMixin(securitylake_mixins.CfnSubscriberNotificationMixinProps(
            notification_configuration=securitylake_mixins.CfnSubscriberNotificationPropsMixin.NotificationConfigurationProperty(
                https_notification_configuration=securitylake_mixins.CfnSubscriberNotificationPropsMixin.HttpsNotificationConfigurationProperty(
                    authorization_api_key_name="authorizationApiKeyName",
                    authorization_api_key_value="authorizationApiKeyValue",
                    endpoint="endpoint",
                    http_method="httpMethod",
                    target_role_arn="targetRoleArn"
                ),
                sqs_notification_configuration=sqs_notification_configuration
            ),
            subscriber_arn="subscriberArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSubscriberNotificationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityLake::SubscriberNotification``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f8907ed0c44ce3bd88d39a0c8be5ecd43fcb476272d9f3724aa2ba2490af7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b098c28e1c97a262b567de8ef66458d50e9734cddc4e6d51a1f686bcbc75b20)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2e10f97292e015df81281e6c1265dae9454842ff3f86b3bea668ab652e139a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSubscriberNotificationMixinProps:
        return typing.cast(CfnSubscriberNotificationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnSubscriberNotificationPropsMixin.HttpsNotificationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_api_key_name": "authorizationApiKeyName",
            "authorization_api_key_value": "authorizationApiKeyValue",
            "endpoint": "endpoint",
            "http_method": "httpMethod",
            "target_role_arn": "targetRoleArn",
        },
    )
    class HttpsNotificationConfigurationProperty:
        def __init__(
            self,
            *,
            authorization_api_key_name: typing.Optional[builtins.str] = None,
            authorization_api_key_value: typing.Optional[builtins.str] = None,
            endpoint: typing.Optional[builtins.str] = None,
            http_method: typing.Optional[builtins.str] = None,
            target_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specify the configurations you want to use for HTTPS subscriber notification.

            :param authorization_api_key_name: The key name for the notification subscription.
            :param authorization_api_key_value: The key value for the notification subscription.
            :param endpoint: The subscription endpoint in Security Lake . If you prefer notification with an HTTPS endpoint, populate this field.
            :param http_method: The HTTPS method used for the notification subscription.
            :param target_role_arn: The Amazon Resource Name (ARN) of the EventBridge API destinations IAM role that you created. For more information about ARNs and how to use them in policies, see `Managing data access <https://docs.aws.amazon.com///security-lake/latest/userguide/subscriber-data-access.html>`_ and `AWS Managed Policies <https://docs.aws.amazon.com//security-lake/latest/userguide/security-iam-awsmanpol.html>`_ in the *Amazon Security Lake User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscribernotification-httpsnotificationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                https_notification_configuration_property = securitylake_mixins.CfnSubscriberNotificationPropsMixin.HttpsNotificationConfigurationProperty(
                    authorization_api_key_name="authorizationApiKeyName",
                    authorization_api_key_value="authorizationApiKeyValue",
                    endpoint="endpoint",
                    http_method="httpMethod",
                    target_role_arn="targetRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e237e5b7435059295a30f50f005faaa76d770603926bcf0664a3cddf6482ccd6)
                check_type(argname="argument authorization_api_key_name", value=authorization_api_key_name, expected_type=type_hints["authorization_api_key_name"])
                check_type(argname="argument authorization_api_key_value", value=authorization_api_key_value, expected_type=type_hints["authorization_api_key_value"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
                check_type(argname="argument target_role_arn", value=target_role_arn, expected_type=type_hints["target_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_api_key_name is not None:
                self._values["authorization_api_key_name"] = authorization_api_key_name
            if authorization_api_key_value is not None:
                self._values["authorization_api_key_value"] = authorization_api_key_value
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if http_method is not None:
                self._values["http_method"] = http_method
            if target_role_arn is not None:
                self._values["target_role_arn"] = target_role_arn

        @builtins.property
        def authorization_api_key_name(self) -> typing.Optional[builtins.str]:
            '''The key name for the notification subscription.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscribernotification-httpsnotificationconfiguration.html#cfn-securitylake-subscribernotification-httpsnotificationconfiguration-authorizationapikeyname
            '''
            result = self._values.get("authorization_api_key_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def authorization_api_key_value(self) -> typing.Optional[builtins.str]:
            '''The key value for the notification subscription.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscribernotification-httpsnotificationconfiguration.html#cfn-securitylake-subscribernotification-httpsnotificationconfiguration-authorizationapikeyvalue
            '''
            result = self._values.get("authorization_api_key_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''The subscription endpoint in Security Lake .

            If you prefer notification with an HTTPS endpoint, populate this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscribernotification-httpsnotificationconfiguration.html#cfn-securitylake-subscribernotification-httpsnotificationconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_method(self) -> typing.Optional[builtins.str]:
            '''The HTTPS method used for the notification subscription.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscribernotification-httpsnotificationconfiguration.html#cfn-securitylake-subscribernotification-httpsnotificationconfiguration-httpmethod
            '''
            result = self._values.get("http_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the EventBridge API destinations IAM role that you created.

            For more information about ARNs and how to use them in policies, see `Managing data access <https://docs.aws.amazon.com///security-lake/latest/userguide/subscriber-data-access.html>`_ and `AWS Managed Policies <https://docs.aws.amazon.com//security-lake/latest/userguide/security-iam-awsmanpol.html>`_ in the *Amazon Security Lake User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscribernotification-httpsnotificationconfiguration.html#cfn-securitylake-subscribernotification-httpsnotificationconfiguration-targetrolearn
            '''
            result = self._values.get("target_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpsNotificationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnSubscriberNotificationPropsMixin.NotificationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "https_notification_configuration": "httpsNotificationConfiguration",
            "sqs_notification_configuration": "sqsNotificationConfiguration",
        },
    )
    class NotificationConfigurationProperty:
        def __init__(
            self,
            *,
            https_notification_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSubscriberNotificationPropsMixin.HttpsNotificationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs_notification_configuration: typing.Any = None,
        ) -> None:
            '''Specify the configurations you want to use for subscriber notification.

            The subscriber is notified when new data is written to the data lake for sources that the subscriber consumes in Security Lake .

            :param https_notification_configuration: The configurations used for HTTPS subscriber notification.
            :param sqs_notification_configuration: The configurations for SQS subscriber notification. The members of this structure are context-dependent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscribernotification-notificationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                # sqs_notification_configuration: Any
                
                notification_configuration_property = securitylake_mixins.CfnSubscriberNotificationPropsMixin.NotificationConfigurationProperty(
                    https_notification_configuration=securitylake_mixins.CfnSubscriberNotificationPropsMixin.HttpsNotificationConfigurationProperty(
                        authorization_api_key_name="authorizationApiKeyName",
                        authorization_api_key_value="authorizationApiKeyValue",
                        endpoint="endpoint",
                        http_method="httpMethod",
                        target_role_arn="targetRoleArn"
                    ),
                    sqs_notification_configuration=sqs_notification_configuration
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95eec818a57b833cd3d411dc1d717adf16157e6a2a8a6dd0dfe666175d5056cc)
                check_type(argname="argument https_notification_configuration", value=https_notification_configuration, expected_type=type_hints["https_notification_configuration"])
                check_type(argname="argument sqs_notification_configuration", value=sqs_notification_configuration, expected_type=type_hints["sqs_notification_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if https_notification_configuration is not None:
                self._values["https_notification_configuration"] = https_notification_configuration
            if sqs_notification_configuration is not None:
                self._values["sqs_notification_configuration"] = sqs_notification_configuration

        @builtins.property
        def https_notification_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberNotificationPropsMixin.HttpsNotificationConfigurationProperty"]]:
            '''The configurations used for HTTPS subscriber notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscribernotification-notificationconfiguration.html#cfn-securitylake-subscribernotification-notificationconfiguration-httpsnotificationconfiguration
            '''
            result = self._values.get("https_notification_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberNotificationPropsMixin.HttpsNotificationConfigurationProperty"]], result)

        @builtins.property
        def sqs_notification_configuration(self) -> typing.Any:
            '''The configurations for SQS subscriber notification.

            The members of this structure are context-dependent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscribernotification-notificationconfiguration.html#cfn-securitylake-subscribernotification-notificationconfiguration-sqsnotificationconfiguration
            '''
            result = self._values.get("sqs_notification_configuration")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnSubscriberPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnSubscriberPropsMixin",
):
    '''Creates a subscriber for accounts that are already enabled in Amazon Security Lake.

    You can create a subscriber with access to data in the current AWS Region.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securitylake-subscriber.html
    :cloudformationResource: AWS::SecurityLake::Subscriber
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
        
        cfn_subscriber_props_mixin = securitylake_mixins.CfnSubscriberPropsMixin(securitylake_mixins.CfnSubscriberMixinProps(
            access_types=["accessTypes"],
            data_lake_arn="dataLakeArn",
            sources=[securitylake_mixins.CfnSubscriberPropsMixin.SourceProperty(
                aws_log_source=securitylake_mixins.CfnSubscriberPropsMixin.AwsLogSourceProperty(
                    source_name="sourceName",
                    source_version="sourceVersion"
                ),
                custom_log_source=securitylake_mixins.CfnSubscriberPropsMixin.CustomLogSourceProperty(
                    source_name="sourceName",
                    source_version="sourceVersion"
                )
            )],
            subscriber_description="subscriberDescription",
            subscriber_identity=securitylake_mixins.CfnSubscriberPropsMixin.SubscriberIdentityProperty(
                external_id="externalId",
                principal="principal"
            ),
            subscriber_name="subscriberName",
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
        props: typing.Union[CfnSubscriberMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityLake::Subscriber``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f301538c20e2658b736083d326951e326108f61fc48efefcc72aa8583213fb59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3b5dd4294659b37f669061dc5ad1b412a6d4e6c6c339d43a6733268ab892d55)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c27c1fca0cbbab3149c34cd6c4692bd092c7fb109515ad05cc7c4edbbe837b4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSubscriberMixinProps:
        return typing.cast(CfnSubscriberMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnSubscriberPropsMixin.AwsLogSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"source_name": "sourceName", "source_version": "sourceVersion"},
    )
    class AwsLogSourceProperty:
        def __init__(
            self,
            *,
            source_name: typing.Optional[builtins.str] = None,
            source_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Adds a natively supported AWS service as an Amazon Security Lake source.

            Enables source types for member accounts in required AWS Regions, based on the parameters you specify. You can choose any source type in any Region for either accounts that are part of a trusted organization or standalone accounts. Once you add an AWS service as a source, Security Lake starts collecting logs and events from it.

            :param source_name: Source name of the natively supported AWS service that is supported as an Amazon Security Lake source. For the list of sources supported by Amazon Security Lake see `Collecting data from AWS services <https://docs.aws.amazon.com//security-lake/latest/userguide/internal-sources.html>`_ in the Amazon Security Lake User Guide.
            :param source_version: Source version of the natively supported AWS service that is supported as an Amazon Security Lake source. For more details about source versions supported by Amazon Security Lake see `OCSF source identification <https://docs.aws.amazon.com//security-lake/latest/userguide/open-cybersecurity-schema-framework.html#ocsf-source-identification>`_ in the Amazon Security Lake User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-awslogsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                aws_log_source_property = securitylake_mixins.CfnSubscriberPropsMixin.AwsLogSourceProperty(
                    source_name="sourceName",
                    source_version="sourceVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f668608e012ea144e2b798b87771563d17a8d3251a3f7953f6872822e935d68b)
                check_type(argname="argument source_name", value=source_name, expected_type=type_hints["source_name"])
                check_type(argname="argument source_version", value=source_version, expected_type=type_hints["source_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_name is not None:
                self._values["source_name"] = source_name
            if source_version is not None:
                self._values["source_version"] = source_version

        @builtins.property
        def source_name(self) -> typing.Optional[builtins.str]:
            '''Source name of the natively supported AWS service that is supported as an Amazon Security Lake source.

            For the list of sources supported by Amazon Security Lake see `Collecting data from AWS services <https://docs.aws.amazon.com//security-lake/latest/userguide/internal-sources.html>`_ in the Amazon Security Lake User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-awslogsource.html#cfn-securitylake-subscriber-awslogsource-sourcename
            '''
            result = self._values.get("source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_version(self) -> typing.Optional[builtins.str]:
            '''Source version of the natively supported AWS service that is supported as an Amazon Security Lake source.

            For more details about source versions supported by Amazon Security Lake see `OCSF source identification <https://docs.aws.amazon.com//security-lake/latest/userguide/open-cybersecurity-schema-framework.html#ocsf-source-identification>`_ in the Amazon Security Lake User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-awslogsource.html#cfn-securitylake-subscriber-awslogsource-sourceversion
            '''
            result = self._values.get("source_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsLogSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnSubscriberPropsMixin.CustomLogSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"source_name": "sourceName", "source_version": "sourceVersion"},
    )
    class CustomLogSourceProperty:
        def __init__(
            self,
            *,
            source_name: typing.Optional[builtins.str] = None,
            source_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Third-party custom log source that meets the requirements to be added to Amazon Security Lake .

            For more details, see `Custom log source <https://docs.aws.amazon.com//security-lake/latest/userguide/custom-sources.html#iam-roles-custom-sources>`_ in the *Amazon Security Lake User Guide* .

            :param source_name: The name of the custom log source.
            :param source_version: The source version of the custom log source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-customlogsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                custom_log_source_property = securitylake_mixins.CfnSubscriberPropsMixin.CustomLogSourceProperty(
                    source_name="sourceName",
                    source_version="sourceVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea525071295a2bf6258e9f5f2b69ba7a2c2aa0e719427f662f69ab5ced380545)
                check_type(argname="argument source_name", value=source_name, expected_type=type_hints["source_name"])
                check_type(argname="argument source_version", value=source_version, expected_type=type_hints["source_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_name is not None:
                self._values["source_name"] = source_name
            if source_version is not None:
                self._values["source_version"] = source_version

        @builtins.property
        def source_name(self) -> typing.Optional[builtins.str]:
            '''The name of the custom log source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-customlogsource.html#cfn-securitylake-subscriber-customlogsource-sourcename
            '''
            result = self._values.get("source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_version(self) -> typing.Optional[builtins.str]:
            '''The source version of the custom log source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-customlogsource.html#cfn-securitylake-subscriber-customlogsource-sourceversion
            '''
            result = self._values.get("source_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomLogSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnSubscriberPropsMixin.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_log_source": "awsLogSource",
            "custom_log_source": "customLogSource",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            aws_log_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSubscriberPropsMixin.AwsLogSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_log_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSubscriberPropsMixin.CustomLogSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Sources are logs and events generated from a single system that match a specific event class in the Open Cybersecurity Schema Framework (OCSF) schema.

            Amazon Security Lake can collect logs and events from a variety of sources, including natively supported AWS services and third-party custom sources.

            :param aws_log_source: The natively supported AWS service which is used a Amazon Security Lake source to collect logs and events from.
            :param custom_log_source: The custom log source AWS which is used a Amazon Security Lake source to collect logs and events from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                source_property = securitylake_mixins.CfnSubscriberPropsMixin.SourceProperty(
                    aws_log_source=securitylake_mixins.CfnSubscriberPropsMixin.AwsLogSourceProperty(
                        source_name="sourceName",
                        source_version="sourceVersion"
                    ),
                    custom_log_source=securitylake_mixins.CfnSubscriberPropsMixin.CustomLogSourceProperty(
                        source_name="sourceName",
                        source_version="sourceVersion"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b2d5ca1399793aa5069b68c08ba87123fefdc230d69d86b93fac65d5474ba0d)
                check_type(argname="argument aws_log_source", value=aws_log_source, expected_type=type_hints["aws_log_source"])
                check_type(argname="argument custom_log_source", value=custom_log_source, expected_type=type_hints["custom_log_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_log_source is not None:
                self._values["aws_log_source"] = aws_log_source
            if custom_log_source is not None:
                self._values["custom_log_source"] = custom_log_source

        @builtins.property
        def aws_log_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberPropsMixin.AwsLogSourceProperty"]]:
            '''The natively supported AWS service which is used a Amazon Security Lake source to collect logs and events from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-source.html#cfn-securitylake-subscriber-source-awslogsource
            '''
            result = self._values.get("aws_log_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberPropsMixin.AwsLogSourceProperty"]], result)

        @builtins.property
        def custom_log_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberPropsMixin.CustomLogSourceProperty"]]:
            '''The custom log source AWS which is used a Amazon Security Lake source to collect logs and events from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-source.html#cfn-securitylake-subscriber-source-customlogsource
            '''
            result = self._values.get("custom_log_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSubscriberPropsMixin.CustomLogSourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securitylake.mixins.CfnSubscriberPropsMixin.SubscriberIdentityProperty",
        jsii_struct_bases=[],
        name_mapping={"external_id": "externalId", "principal": "principal"},
    )
    class SubscriberIdentityProperty:
        def __init__(
            self,
            *,
            external_id: typing.Optional[builtins.str] = None,
            principal: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specify the AWS account ID and external ID that the subscriber will use to access source data.

            :param external_id: The external ID is a unique identifier that the subscriber provides to you.
            :param principal: Principals can include accounts, users, roles, federated users, or AWS services.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-subscriberidentity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securitylake import mixins as securitylake_mixins
                
                subscriber_identity_property = securitylake_mixins.CfnSubscriberPropsMixin.SubscriberIdentityProperty(
                    external_id="externalId",
                    principal="principal"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87547a6dbaa7224cd892d820cc854a11a0b83a1be01b6afc2f2d64500eb6955f)
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if external_id is not None:
                self._values["external_id"] = external_id
            if principal is not None:
                self._values["principal"] = principal

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID is a unique identifier that the subscriber provides to you.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-subscriberidentity.html#cfn-securitylake-subscriber-subscriberidentity-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def principal(self) -> typing.Optional[builtins.str]:
            '''Principals can include accounts, users, roles, federated users, or AWS services.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securitylake-subscriber-subscriberidentity.html#cfn-securitylake-subscriber-subscriberidentity-principal
            '''
            result = self._values.get("principal")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriberIdentityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAwsLogSourceMixinProps",
    "CfnAwsLogSourcePropsMixin",
    "CfnDataLakeMixinProps",
    "CfnDataLakePropsMixin",
    "CfnSubscriberMixinProps",
    "CfnSubscriberNotificationMixinProps",
    "CfnSubscriberNotificationPropsMixin",
    "CfnSubscriberPropsMixin",
]

publication.publish()

def _typecheckingstub__67f24bf3bfafa048d904c5c1bb01daa333ea1804134b0736521fe79171f6dbdf(
    *,
    accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_lake_arn: typing.Optional[builtins.str] = None,
    source_name: typing.Optional[builtins.str] = None,
    source_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4ebf8c35f921877764f0472f5d2b174c71b4e9e5d53ccf8770b09e02ce53a4(
    props: typing.Union[CfnAwsLogSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbc739640d512d4046c6a70a2590df4e88cb9cec0a5ae54df0791f69afa52a7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e53ed1b50c7a198e3496bbdb1028e0a1adf0408ff84cb16325a3b215a6845dc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a09317cb1bbdaa1c57b0b56a3269cae1e6c67e147b6ac42e5b741df7404070(
    *,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataLakePropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataLakePropsMixin.LifecycleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    meta_store_manager_role_arn: typing.Optional[builtins.str] = None,
    replication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataLakePropsMixin.ReplicationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350bac982d1d09da737943c705ad120726fe598fedeae3443f559e66c42af98f(
    props: typing.Union[CfnDataLakeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c41e0a6719f85b9cef144a0bbce8e4bdc2cd3ad99723ee75b2cce903bafb7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf2a87219115ff0831d518217a17b120dd22ae72b55a458918b807833b28beb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c857060d0034698133e49fca7d58958af177d1813fa5399241a55610631ccdb(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5786e59b6f18a90971c7a28d79eed1b9858e41830b6968c6c8962e7bb4d21646(
    *,
    days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a39b924cd34ddc03a801a1311947197a5d966e3c46903c429589dc883a0811(
    *,
    expiration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataLakePropsMixin.ExpirationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    transitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataLakePropsMixin.TransitionsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e01f1d92de1efb9177fc0e3004eadcdacf54a0a4058c4009e1eff57a9543bcc(
    *,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cd8dba762f9a465575ad1df9b553cde8928b7c130117a0380a6be3934db2cf(
    *,
    days: typing.Optional[jsii.Number] = None,
    storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3546819b9ab16b1a8aa6b4ef8a0d6cd25af66e284cfbce5dd06f7f68e4d5a2a(
    *,
    access_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_lake_arn: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSubscriberPropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subscriber_description: typing.Optional[builtins.str] = None,
    subscriber_identity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSubscriberPropsMixin.SubscriberIdentityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subscriber_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de404ba8f121013453ed61450eb8a36a2a1310dd505a93cadfacc4e640f5f45(
    *,
    notification_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSubscriberNotificationPropsMixin.NotificationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subscriber_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f8907ed0c44ce3bd88d39a0c8be5ecd43fcb476272d9f3724aa2ba2490af7e(
    props: typing.Union[CfnSubscriberNotificationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b098c28e1c97a262b567de8ef66458d50e9734cddc4e6d51a1f686bcbc75b20(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2e10f97292e015df81281e6c1265dae9454842ff3f86b3bea668ab652e139a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e237e5b7435059295a30f50f005faaa76d770603926bcf0664a3cddf6482ccd6(
    *,
    authorization_api_key_name: typing.Optional[builtins.str] = None,
    authorization_api_key_value: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
    http_method: typing.Optional[builtins.str] = None,
    target_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95eec818a57b833cd3d411dc1d717adf16157e6a2a8a6dd0dfe666175d5056cc(
    *,
    https_notification_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSubscriberNotificationPropsMixin.HttpsNotificationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs_notification_configuration: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f301538c20e2658b736083d326951e326108f61fc48efefcc72aa8583213fb59(
    props: typing.Union[CfnSubscriberMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b5dd4294659b37f669061dc5ad1b412a6d4e6c6c339d43a6733268ab892d55(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c27c1fca0cbbab3149c34cd6c4692bd092c7fb109515ad05cc7c4edbbe837b4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f668608e012ea144e2b798b87771563d17a8d3251a3f7953f6872822e935d68b(
    *,
    source_name: typing.Optional[builtins.str] = None,
    source_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea525071295a2bf6258e9f5f2b69ba7a2c2aa0e719427f662f69ab5ced380545(
    *,
    source_name: typing.Optional[builtins.str] = None,
    source_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2d5ca1399793aa5069b68c08ba87123fefdc230d69d86b93fac65d5474ba0d(
    *,
    aws_log_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSubscriberPropsMixin.AwsLogSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_log_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSubscriberPropsMixin.CustomLogSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87547a6dbaa7224cd892d820cc854a11a0b83a1be01b6afc2f2d64500eb6955f(
    *,
    external_id: typing.Optional[builtins.str] = None,
    principal: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
