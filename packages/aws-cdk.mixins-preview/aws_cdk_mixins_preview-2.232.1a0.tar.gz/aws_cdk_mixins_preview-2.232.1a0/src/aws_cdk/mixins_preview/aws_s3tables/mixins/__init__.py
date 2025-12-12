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
    jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnNamespaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace", "table_bucket_arn": "tableBucketArn"},
)
class CfnNamespaceMixinProps:
    def __init__(
        self,
        *,
        namespace: typing.Optional[builtins.str] = None,
        table_bucket_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnNamespacePropsMixin.

        :param namespace: The name of the namespace.
        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket to create the namespace in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-namespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
            
            cfn_namespace_mixin_props = s3tables_mixins.CfnNamespaceMixinProps(
                namespace="namespace",
                table_bucket_arn="tableBucketArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec8efc52b9d4aa55901cab63814f92948f7dd96cab0f92523786f757714c9d2)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument table_bucket_arn", value=table_bucket_arn, expected_type=type_hints["table_bucket_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if namespace is not None:
            self._values["namespace"] = namespace
        if table_bucket_arn is not None:
            self._values["table_bucket_arn"] = table_bucket_arn

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The name of the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-namespace.html#cfn-s3tables-namespace-namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_bucket_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the table bucket to create the namespace in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-namespace.html#cfn-s3tables-namespace-tablebucketarn
        '''
        result = self._values.get("table_bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnNamespacePropsMixin",
):
    '''Creates a namespace.

    A namespace is a logical grouping of tables within your table bucket, which you can use to organize tables. For more information, see `Create a namespace <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-namespace-create.html>`_ in the *Amazon Simple Storage Service User Guide* .

    - **Permissions** - You must have the ``s3tables:CreateNamespace`` permission to use this operation.
    - **Cloud Development Kit** - To use S3 Tables AWS CDK constructs, add the ``@aws-cdk/aws-s3tables-alpha`` dependency with one of the following options:
    - NPM: `npm i

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-namespace.html
    :aws-cdk:

    /aws-s3tables-alpha`

    - Yarn: ``yarn add @aws-cdk/aws-s3tables-alpha``
    :cloudformationResource: AWS::S3Tables::Namespace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
        
        cfn_namespace_props_mixin = s3tables_mixins.CfnNamespacePropsMixin(s3tables_mixins.CfnNamespaceMixinProps(
            namespace="namespace",
            table_bucket_arn="tableBucketArn"
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
        '''Create a mixin to apply properties to ``AWS::S3Tables::Namespace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4fb962db5cb7287f82a44a3562af66d98b52729067c52c86eb1a99a2d79191)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee320925454c58c3f6c527130569445057a5979bdda6ce3ad719dab52d5d1961)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce891791c6a34ad82104637e1e00283e92834f25ebdebcde3fa81c87f1616130)
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
    jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTableBucketMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_configuration": "encryptionConfiguration",
        "metrics_configuration": "metricsConfiguration",
        "storage_class_configuration": "storageClassConfiguration",
        "table_bucket_name": "tableBucketName",
        "tags": "tags",
        "unreferenced_file_removal": "unreferencedFileRemoval",
    },
)
class CfnTableBucketMixinProps:
    def __init__(
        self,
        *,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTableBucketPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTableBucketPropsMixin.MetricsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_class_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTableBucketPropsMixin.StorageClassConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_bucket_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        unreferenced_file_removal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTableBucketPropsMixin.UnreferencedFileRemovalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTableBucketPropsMixin.

        :param encryption_configuration: Configuration specifying how data should be encrypted. This structure defines the encryption algorithm and optional KMS key to be used for server-side encryption.
        :param metrics_configuration: Settings governing the Metric configuration for the table bucket.
        :param storage_class_configuration: Specifies storage class settings for the table bucket.
        :param table_bucket_name: The name for the table bucket.
        :param tags: User tags (key-value pairs) to associate with the table bucket.
        :param unreferenced_file_removal: The unreferenced file removal settings for your table bucket. Unreferenced file removal identifies and deletes all objects that are not referenced by any table snapshots. For more information, see the `*Amazon S3 User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-table-buckets-maintenance.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucket.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
            
            cfn_table_bucket_mixin_props = s3tables_mixins.CfnTableBucketMixinProps(
                encryption_configuration=s3tables_mixins.CfnTableBucketPropsMixin.EncryptionConfigurationProperty(
                    kms_key_arn="kmsKeyArn",
                    sse_algorithm="sseAlgorithm"
                ),
                metrics_configuration=s3tables_mixins.CfnTableBucketPropsMixin.MetricsConfigurationProperty(
                    status="status"
                ),
                storage_class_configuration=s3tables_mixins.CfnTableBucketPropsMixin.StorageClassConfigurationProperty(
                    storage_class="storageClass"
                ),
                table_bucket_name="tableBucketName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                unreferenced_file_removal=s3tables_mixins.CfnTableBucketPropsMixin.UnreferencedFileRemovalProperty(
                    noncurrent_days=123,
                    status="status",
                    unreferenced_days=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e49a7ac032f051309883379d0263dc0f3ca574a28226fbc08083a8c7b449f4)
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument metrics_configuration", value=metrics_configuration, expected_type=type_hints["metrics_configuration"])
            check_type(argname="argument storage_class_configuration", value=storage_class_configuration, expected_type=type_hints["storage_class_configuration"])
            check_type(argname="argument table_bucket_name", value=table_bucket_name, expected_type=type_hints["table_bucket_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument unreferenced_file_removal", value=unreferenced_file_removal, expected_type=type_hints["unreferenced_file_removal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if metrics_configuration is not None:
            self._values["metrics_configuration"] = metrics_configuration
        if storage_class_configuration is not None:
            self._values["storage_class_configuration"] = storage_class_configuration
        if table_bucket_name is not None:
            self._values["table_bucket_name"] = table_bucket_name
        if tags is not None:
            self._values["tags"] = tags
        if unreferenced_file_removal is not None:
            self._values["unreferenced_file_removal"] = unreferenced_file_removal

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableBucketPropsMixin.EncryptionConfigurationProperty"]]:
        '''Configuration specifying how data should be encrypted.

        This structure defines the encryption algorithm and optional KMS key to be used for server-side encryption.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucket.html#cfn-s3tables-tablebucket-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableBucketPropsMixin.EncryptionConfigurationProperty"]], result)

    @builtins.property
    def metrics_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableBucketPropsMixin.MetricsConfigurationProperty"]]:
        '''Settings governing the Metric configuration for the table bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucket.html#cfn-s3tables-tablebucket-metricsconfiguration
        '''
        result = self._values.get("metrics_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableBucketPropsMixin.MetricsConfigurationProperty"]], result)

    @builtins.property
    def storage_class_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableBucketPropsMixin.StorageClassConfigurationProperty"]]:
        '''Specifies storage class settings for the table bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucket.html#cfn-s3tables-tablebucket-storageclassconfiguration
        '''
        result = self._values.get("storage_class_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableBucketPropsMixin.StorageClassConfigurationProperty"]], result)

    @builtins.property
    def table_bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name for the table bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucket.html#cfn-s3tables-tablebucket-tablebucketname
        '''
        result = self._values.get("table_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''User tags (key-value pairs) to associate with the table bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucket.html#cfn-s3tables-tablebucket-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def unreferenced_file_removal(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableBucketPropsMixin.UnreferencedFileRemovalProperty"]]:
        '''The unreferenced file removal settings for your table bucket.

        Unreferenced file removal identifies and deletes all objects that are not referenced by any table snapshots. For more information, see the `*Amazon S3 User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-table-buckets-maintenance.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucket.html#cfn-s3tables-tablebucket-unreferencedfileremoval
        '''
        result = self._values.get("unreferenced_file_removal")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableBucketPropsMixin.UnreferencedFileRemovalProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableBucketMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTableBucketPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "resource_policy": "resourcePolicy",
        "table_bucket_arn": "tableBucketArn",
    },
)
class CfnTableBucketPolicyMixinProps:
    def __init__(
        self,
        *,
        resource_policy: typing.Any = None,
        table_bucket_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTableBucketPolicyPropsMixin.

        :param resource_policy: The bucket policy JSON for the table bucket.
        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucketpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
            
            # resource_policy: Any
            
            cfn_table_bucket_policy_mixin_props = s3tables_mixins.CfnTableBucketPolicyMixinProps(
                resource_policy=resource_policy,
                table_bucket_arn="tableBucketArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eea06f2805e3276e5df1737b0736254357d60dd5b81eff2eec2d2bc76b46655)
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            check_type(argname="argument table_bucket_arn", value=table_bucket_arn, expected_type=type_hints["table_bucket_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_policy is not None:
            self._values["resource_policy"] = resource_policy
        if table_bucket_arn is not None:
            self._values["table_bucket_arn"] = table_bucket_arn

    @builtins.property
    def resource_policy(self) -> typing.Any:
        '''The bucket policy JSON for the table bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucketpolicy.html#cfn-s3tables-tablebucketpolicy-resourcepolicy
        '''
        result = self._values.get("resource_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def table_bucket_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the table bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucketpolicy.html#cfn-s3tables-tablebucketpolicy-tablebucketarn
        '''
        result = self._values.get("table_bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableBucketPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTableBucketPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTableBucketPolicyPropsMixin",
):
    '''Creates a new maintenance configuration or replaces an existing table bucket policy for a table bucket.

    For more information, see `Adding a table bucket policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-bucket-policy.html#table-bucket-policy-add>`_ in the *Amazon Simple Storage Service User Guide* .

    - **Permissions** - You must have the ``s3tables:PutTableBucketPolicy`` permission to use this operation.
    - **Cloud Development Kit** - To use S3 Tables AWS CDK constructs, add the ``@aws-cdk/aws-s3tables-alpha`` dependency with one of the following options:
    - NPM: `npm i

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucketpolicy.html
    :aws-cdk:

    /aws-s3tables-alpha`

    - Yarn: ``yarn add @aws-cdk/aws-s3tables-alpha``
    :cloudformationResource: AWS::S3Tables::TableBucketPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
        
        # resource_policy: Any
        
        cfn_table_bucket_policy_props_mixin = s3tables_mixins.CfnTableBucketPolicyPropsMixin(s3tables_mixins.CfnTableBucketPolicyMixinProps(
            resource_policy=resource_policy,
            table_bucket_arn="tableBucketArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTableBucketPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Tables::TableBucketPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06b2919b20d081856f3f6d43480ca5c38a782d45066e4e684f0d74457b24e58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70a54c99ba4646cbb40a5593db0932d2343c14f24fb08f291f54bedce082bcc9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85940d4b0b7272fc30b9df24c27913820ebf843c40d893d484809a67d9acebb8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTableBucketPolicyMixinProps:
        return typing.cast(CfnTableBucketPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnTableBucketPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTableBucketPropsMixin",
):
    '''Creates a table bucket.

    For more information, see `Creating a table bucket <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-buckets-create.html>`_ in the *Amazon Simple Storage Service User Guide* .

    - **Permissions** - - You must have the ``s3tables:CreateTableBucket`` permission to use this operation.
    - If you use this operation with the optional ``encryptionConfiguration`` parameter you must have the ``s3tables:PutTableBucketEncryption`` permission.
    - **Cloud Development Kit** - To use S3 Tables AWS CDK constructs, add the ``@aws-cdk/aws-s3tables-alpha`` dependency with one of the following options:
    - NPM: `npm i

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablebucket.html
    :aws-cdk:

    /aws-s3tables-alpha`

    - Yarn: ``yarn add @aws-cdk/aws-s3tables-alpha``
    :cloudformationResource: AWS::S3Tables::TableBucket
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
        
        cfn_table_bucket_props_mixin = s3tables_mixins.CfnTableBucketPropsMixin(s3tables_mixins.CfnTableBucketMixinProps(
            encryption_configuration=s3tables_mixins.CfnTableBucketPropsMixin.EncryptionConfigurationProperty(
                kms_key_arn="kmsKeyArn",
                sse_algorithm="sseAlgorithm"
            ),
            metrics_configuration=s3tables_mixins.CfnTableBucketPropsMixin.MetricsConfigurationProperty(
                status="status"
            ),
            storage_class_configuration=s3tables_mixins.CfnTableBucketPropsMixin.StorageClassConfigurationProperty(
                storage_class="storageClass"
            ),
            table_bucket_name="tableBucketName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            unreferenced_file_removal=s3tables_mixins.CfnTableBucketPropsMixin.UnreferencedFileRemovalProperty(
                noncurrent_days=123,
                status="status",
                unreferenced_days=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTableBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Tables::TableBucket``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe148dab0c375c474516537a6fa1706a649e9590cdac3fd56b1fbb7739be006)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c70b2339940531411472c57a34a20af288aaa8ec236c9a62f511aad75422e68)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8ce44c555bb7f8c15da085dd684c2f938cbf3eb9a2d5995afa8334389a9f936)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTableBucketMixinProps:
        return typing.cast(CfnTableBucketMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTableBucketPropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn", "sse_algorithm": "sseAlgorithm"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            sse_algorithm: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration specifying how data should be encrypted.

            This structure defines the encryption algorithm and optional KMS key to be used for server-side encryption.

            :param kms_key_arn: The Amazon Resource Name (ARN) of the KMS key to use for encryption. This field is required only when ``sseAlgorithm`` is set to ``aws:kms`` .
            :param sse_algorithm: The server-side encryption algorithm to use. Valid values are ``AES256`` for S3-managed encryption keys, or ``aws:kms`` for AWS KMS-managed encryption keys. If you choose SSE-KMS encryption you must grant the S3 Tables maintenance principal access to your KMS key. For more information, see `Permissions requirements for S3 Tables SSE-KMS encryption <https://docs.aws.amazon.com//AmazonS3/latest/userguide/s3-tables-kms-permissions.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
                
                encryption_configuration_property = s3tables_mixins.CfnTableBucketPropsMixin.EncryptionConfigurationProperty(
                    kms_key_arn="kmsKeyArn",
                    sse_algorithm="sseAlgorithm"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78adc082218c7312551a05f667de1b7f4b45fdda9d0e5f0bfb38e3a702e3f359)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument sse_algorithm", value=sse_algorithm, expected_type=type_hints["sse_algorithm"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if sse_algorithm is not None:
                self._values["sse_algorithm"] = sse_algorithm

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the KMS key to use for encryption.

            This field is required only when ``sseAlgorithm`` is set to ``aws:kms`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-encryptionconfiguration.html#cfn-s3tables-tablebucket-encryptionconfiguration-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sse_algorithm(self) -> typing.Optional[builtins.str]:
            '''The server-side encryption algorithm to use.

            Valid values are ``AES256`` for S3-managed encryption keys, or ``aws:kms`` for AWS KMS-managed encryption keys. If you choose SSE-KMS encryption you must grant the S3 Tables maintenance principal access to your KMS key. For more information, see `Permissions requirements for S3 Tables SSE-KMS encryption <https://docs.aws.amazon.com//AmazonS3/latest/userguide/s3-tables-kms-permissions.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-encryptionconfiguration.html#cfn-s3tables-tablebucket-encryptionconfiguration-ssealgorithm
            '''
            result = self._values.get("sse_algorithm")
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
        jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTableBucketPropsMixin.MetricsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class MetricsConfigurationProperty:
        def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
            '''Settings governing the Metric configuration for the table bucket.

            :param status: Indicates whether Metrics are enabled. Default: - "Disabled"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-metricsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
                
                metrics_configuration_property = s3tables_mixins.CfnTableBucketPropsMixin.MetricsConfigurationProperty(
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f82171fcf81a632054165d04e069363860d5d9f1782b2b237564f64b4be190db)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Indicates whether Metrics are enabled.

            :default: - "Disabled"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-metricsconfiguration.html#cfn-s3tables-tablebucket-metricsconfiguration-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTableBucketPropsMixin.StorageClassConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"storage_class": "storageClass"},
    )
    class StorageClassConfigurationProperty:
        def __init__(
            self,
            *,
            storage_class: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies storage class settings for the table bucket.

            :param storage_class: The storage class for the table bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-storageclassconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
                
                storage_class_configuration_property = s3tables_mixins.CfnTableBucketPropsMixin.StorageClassConfigurationProperty(
                    storage_class="storageClass"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7ef74d9bac670a778393eff87e783a092524eb49b6f269f6a6dc383dfd3cc2e7)
                check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if storage_class is not None:
                self._values["storage_class"] = storage_class

        @builtins.property
        def storage_class(self) -> typing.Optional[builtins.str]:
            '''The storage class for the table bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-storageclassconfiguration.html#cfn-s3tables-tablebucket-storageclassconfiguration-storageclass
            '''
            result = self._values.get("storage_class")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageClassConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTableBucketPropsMixin.UnreferencedFileRemovalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "noncurrent_days": "noncurrentDays",
            "status": "status",
            "unreferenced_days": "unreferencedDays",
        },
    )
    class UnreferencedFileRemovalProperty:
        def __init__(
            self,
            *,
            noncurrent_days: typing.Optional[jsii.Number] = None,
            status: typing.Optional[builtins.str] = None,
            unreferenced_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The unreferenced file removal settings for your table bucket.

            Unreferenced file removal identifies and deletes all objects that are not referenced by any table snapshots. For more information, see the `*Amazon S3 User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-table-buckets-maintenance.html>`_ .

            :param noncurrent_days: The number of days an object can be noncurrent before Amazon S3 deletes it.
            :param status: The status of the unreferenced file removal configuration for your table bucket.
            :param unreferenced_days: The number of days an object must be unreferenced by your table before Amazon S3 marks the object as noncurrent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-unreferencedfileremoval.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
                
                unreferenced_file_removal_property = s3tables_mixins.CfnTableBucketPropsMixin.UnreferencedFileRemovalProperty(
                    noncurrent_days=123,
                    status="status",
                    unreferenced_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8631f11de540150b714cf52a30126aa231e71a335df37ebc338f9f3cdbcfc24)
                check_type(argname="argument noncurrent_days", value=noncurrent_days, expected_type=type_hints["noncurrent_days"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument unreferenced_days", value=unreferenced_days, expected_type=type_hints["unreferenced_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if noncurrent_days is not None:
                self._values["noncurrent_days"] = noncurrent_days
            if status is not None:
                self._values["status"] = status
            if unreferenced_days is not None:
                self._values["unreferenced_days"] = unreferenced_days

        @builtins.property
        def noncurrent_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days an object can be noncurrent before Amazon S3 deletes it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-unreferencedfileremoval.html#cfn-s3tables-tablebucket-unreferencedfileremoval-noncurrentdays
            '''
            result = self._values.get("noncurrent_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the unreferenced file removal configuration for your table bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-unreferencedfileremoval.html#cfn-s3tables-tablebucket-unreferencedfileremoval-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unreferenced_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days an object must be unreferenced by your table before Amazon S3 marks the object as noncurrent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-unreferencedfileremoval.html#cfn-s3tables-tablebucket-unreferencedfileremoval-unreferenceddays
            '''
            result = self._values.get("unreferenced_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UnreferencedFileRemovalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "compaction": "compaction",
        "iceberg_metadata": "icebergMetadata",
        "namespace": "namespace",
        "open_table_format": "openTableFormat",
        "snapshot_management": "snapshotManagement",
        "storage_class_configuration": "storageClassConfiguration",
        "table_bucket_arn": "tableBucketArn",
        "table_name": "tableName",
        "tags": "tags",
        "without_metadata": "withoutMetadata",
    },
)
class CfnTableMixinProps:
    def __init__(
        self,
        *,
        compaction: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.CompactionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        iceberg_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.IcebergMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        namespace: typing.Optional[builtins.str] = None,
        open_table_format: typing.Optional[builtins.str] = None,
        snapshot_management: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.SnapshotManagementProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_class_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.StorageClassConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_bucket_arn: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        without_metadata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTablePropsMixin.

        :param compaction: Contains details about the compaction settings for an Iceberg table.
        :param iceberg_metadata: Contains details about the metadata for an Iceberg table.
        :param namespace: The name of the namespace.
        :param open_table_format: The format of the table.
        :param snapshot_management: Contains details about the Iceberg snapshot management settings for the table.
        :param storage_class_configuration: Specifies storage class settings for the table.
        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket to create the table in.
        :param table_name: The name for the table.
        :param tags: User tags (key-value pairs) to associate with the table.
        :param without_metadata: Indicates that you don't want to specify a schema for the table. This property is mutually exclusive to ``IcebergMetadata`` , and its only possible value is ``Yes`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
            
            cfn_table_mixin_props = s3tables_mixins.CfnTableMixinProps(
                compaction=s3tables_mixins.CfnTablePropsMixin.CompactionProperty(
                    status="status",
                    target_file_size_mb=123
                ),
                iceberg_metadata=s3tables_mixins.CfnTablePropsMixin.IcebergMetadataProperty(
                    iceberg_schema=s3tables_mixins.CfnTablePropsMixin.IcebergSchemaProperty(
                        schema_field_list=[s3tables_mixins.CfnTablePropsMixin.SchemaFieldProperty(
                            name="name",
                            required=False,
                            type="type"
                        )]
                    )
                ),
                namespace="namespace",
                open_table_format="openTableFormat",
                snapshot_management=s3tables_mixins.CfnTablePropsMixin.SnapshotManagementProperty(
                    max_snapshot_age_hours=123,
                    min_snapshots_to_keep=123,
                    status="status"
                ),
                storage_class_configuration=s3tables_mixins.CfnTablePropsMixin.StorageClassConfigurationProperty(
                    storage_class="storageClass"
                ),
                table_bucket_arn="tableBucketArn",
                table_name="tableName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                without_metadata="withoutMetadata"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b6bcb174c4161953fd79c0047ec40ea37e3e613c9f7fdbbcf8cd46a1b569697)
            check_type(argname="argument compaction", value=compaction, expected_type=type_hints["compaction"])
            check_type(argname="argument iceberg_metadata", value=iceberg_metadata, expected_type=type_hints["iceberg_metadata"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument open_table_format", value=open_table_format, expected_type=type_hints["open_table_format"])
            check_type(argname="argument snapshot_management", value=snapshot_management, expected_type=type_hints["snapshot_management"])
            check_type(argname="argument storage_class_configuration", value=storage_class_configuration, expected_type=type_hints["storage_class_configuration"])
            check_type(argname="argument table_bucket_arn", value=table_bucket_arn, expected_type=type_hints["table_bucket_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument without_metadata", value=without_metadata, expected_type=type_hints["without_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compaction is not None:
            self._values["compaction"] = compaction
        if iceberg_metadata is not None:
            self._values["iceberg_metadata"] = iceberg_metadata
        if namespace is not None:
            self._values["namespace"] = namespace
        if open_table_format is not None:
            self._values["open_table_format"] = open_table_format
        if snapshot_management is not None:
            self._values["snapshot_management"] = snapshot_management
        if storage_class_configuration is not None:
            self._values["storage_class_configuration"] = storage_class_configuration
        if table_bucket_arn is not None:
            self._values["table_bucket_arn"] = table_bucket_arn
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags
        if without_metadata is not None:
            self._values["without_metadata"] = without_metadata

    @builtins.property
    def compaction(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.CompactionProperty"]]:
        '''Contains details about the compaction settings for an Iceberg table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html#cfn-s3tables-table-compaction
        '''
        result = self._values.get("compaction")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.CompactionProperty"]], result)

    @builtins.property
    def iceberg_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.IcebergMetadataProperty"]]:
        '''Contains details about the metadata for an Iceberg table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html#cfn-s3tables-table-icebergmetadata
        '''
        result = self._values.get("iceberg_metadata")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.IcebergMetadataProperty"]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The name of the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html#cfn-s3tables-table-namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_table_format(self) -> typing.Optional[builtins.str]:
        '''The format of the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html#cfn-s3tables-table-opentableformat
        '''
        result = self._values.get("open_table_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_management(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SnapshotManagementProperty"]]:
        '''Contains details about the Iceberg snapshot management settings for the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html#cfn-s3tables-table-snapshotmanagement
        '''
        result = self._values.get("snapshot_management")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SnapshotManagementProperty"]], result)

    @builtins.property
    def storage_class_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.StorageClassConfigurationProperty"]]:
        '''Specifies storage class settings for the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html#cfn-s3tables-table-storageclassconfiguration
        '''
        result = self._values.get("storage_class_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.StorageClassConfigurationProperty"]], result)

    @builtins.property
    def table_bucket_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the table bucket to create the table in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html#cfn-s3tables-table-tablebucketarn
        '''
        result = self._values.get("table_bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''The name for the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html#cfn-s3tables-table-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''User tags (key-value pairs) to associate with the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html#cfn-s3tables-table-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def without_metadata(self) -> typing.Optional[builtins.str]:
        '''Indicates that you don't want to specify a schema for the table.

        This property is mutually exclusive to ``IcebergMetadata`` , and its only possible value is ``Yes`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html#cfn-s3tables-table-withoutmetadata
        '''
        result = self._values.get("without_metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTablePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"resource_policy": "resourcePolicy", "table_arn": "tableArn"},
)
class CfnTablePolicyMixinProps:
    def __init__(
        self,
        *,
        resource_policy: typing.Any = None,
        table_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTablePolicyPropsMixin.

        :param resource_policy: The ``JSON`` that defines the policy.
        :param table_arn: The Amazon Resource Name (ARN) of the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
            
            # resource_policy: Any
            
            cfn_table_policy_mixin_props = s3tables_mixins.CfnTablePolicyMixinProps(
                resource_policy=resource_policy,
                table_arn="tableArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efd3c64448ec5b368919c07f978ae3376042eed3ce73f9895158be204e87cbe)
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            check_type(argname="argument table_arn", value=table_arn, expected_type=type_hints["table_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_policy is not None:
            self._values["resource_policy"] = resource_policy
        if table_arn is not None:
            self._values["table_arn"] = table_arn

    @builtins.property
    def resource_policy(self) -> typing.Any:
        '''The ``JSON`` that defines the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablepolicy.html#cfn-s3tables-tablepolicy-resourcepolicy
        '''
        result = self._values.get("resource_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def table_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablepolicy.html#cfn-s3tables-tablepolicy-tablearn
        '''
        result = self._values.get("table_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTablePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTablePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTablePolicyPropsMixin",
):
    '''Creates a new maintenance configuration or replaces an existing table policy for a table.

    For more information, see `Adding a table policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-table-policy.html#table-policy-add>`_ in the *Amazon Simple Storage Service User Guide* .

    - **Permissions** - You must have the ``s3tables:PutTablePolicy`` permission to use this operation.
    - **Cloud Development Kit** - To use S3 Tables AWS CDK constructs, add the ``@aws-cdk/aws-s3tables-alpha`` dependency with one of the following options:
    - NPM: `npm i

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-tablepolicy.html
    :aws-cdk:

    /aws-s3tables-alpha`

    - Yarn: ``yarn add @aws-cdk/aws-s3tables-alpha``
    :cloudformationResource: AWS::S3Tables::TablePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
        
        # resource_policy: Any
        
        cfn_table_policy_props_mixin = s3tables_mixins.CfnTablePolicyPropsMixin(s3tables_mixins.CfnTablePolicyMixinProps(
            resource_policy=resource_policy,
            table_arn="tableArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTablePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Tables::TablePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd563df5ce2b18608fbbe17d8bd5594bfc0800edbf4aa6fd8a403751fe61c62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__308ffc317a0e4c9a7715f31ab0dbb713785e2371b5c12d7e62eb7e0b7735ee44)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9f760a02a789e0f51f82609cb3011666dbc905429d247570ae70678815d26b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTablePolicyMixinProps:
        return typing.cast(CfnTablePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnTablePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTablePropsMixin",
):
    '''Creates a new table associated with the given namespace in a table bucket.

    For more information, see `Creating an Amazon S3 table <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-create.html>`_ in the *Amazon Simple Storage Service User Guide* .

    - **Permissions** - - You must have the ``s3tables:CreateTable`` permission to use this operation.
    - If you use this operation with the optional ``metadata`` request parameter you must have the ``s3tables:PutTableData`` permission.
    - If you use this operation with the optional ``encryptionConfiguration`` request parameter you must have the ``s3tables:PutTableEncryption`` permission.

    .. epigraph::

       Additionally, If you choose SSE-KMS encryption you must grant the S3 Tables maintenance principal access to your KMS key. For more information, see `Permissions requirements for S3 Tables SSE-KMS encryption <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-kms-permissions.html>`_ .

    - **Cloud Development Kit** - To use S3 Tables AWS CDK constructs, add the ``@aws-cdk/aws-s3tables-alpha`` dependency with one of the following options:
    - NPM: `npm i

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3tables-table.html
    :aws-cdk:

    /aws-s3tables-alpha`

    - Yarn: ``yarn add @aws-cdk/aws-s3tables-alpha``
    :cloudformationResource: AWS::S3Tables::Table
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
        
        cfn_table_props_mixin = s3tables_mixins.CfnTablePropsMixin(s3tables_mixins.CfnTableMixinProps(
            compaction=s3tables_mixins.CfnTablePropsMixin.CompactionProperty(
                status="status",
                target_file_size_mb=123
            ),
            iceberg_metadata=s3tables_mixins.CfnTablePropsMixin.IcebergMetadataProperty(
                iceberg_schema=s3tables_mixins.CfnTablePropsMixin.IcebergSchemaProperty(
                    schema_field_list=[s3tables_mixins.CfnTablePropsMixin.SchemaFieldProperty(
                        name="name",
                        required=False,
                        type="type"
                    )]
                )
            ),
            namespace="namespace",
            open_table_format="openTableFormat",
            snapshot_management=s3tables_mixins.CfnTablePropsMixin.SnapshotManagementProperty(
                max_snapshot_age_hours=123,
                min_snapshots_to_keep=123,
                status="status"
            ),
            storage_class_configuration=s3tables_mixins.CfnTablePropsMixin.StorageClassConfigurationProperty(
                storage_class="storageClass"
            ),
            table_bucket_arn="tableBucketArn",
            table_name="tableName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            without_metadata="withoutMetadata"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTableMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3Tables::Table``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7e9968ae9f3676898e534911090508995ba1cf2896132387d91eed5a776eb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1835c57095d5f0d7268f9b878c46eaf2f754f7e91f560b304ea2af5048541614)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0f22b633ee4435f3fb07a2308d800d5348d7de22c44e17487aff05f3707459)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTableMixinProps:
        return typing.cast(CfnTableMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTablePropsMixin.CompactionProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status", "target_file_size_mb": "targetFileSizeMb"},
    )
    class CompactionProperty:
        def __init__(
            self,
            *,
            status: typing.Optional[builtins.str] = None,
            target_file_size_mb: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains details about the compaction settings for an Iceberg table.

            :param status: The status of the maintenance configuration.
            :param target_file_size_mb: The target file size for the table in MB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-compaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
                
                compaction_property = s3tables_mixins.CfnTablePropsMixin.CompactionProperty(
                    status="status",
                    target_file_size_mb=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d9920b8fca2c0bc27df84d470eabaa504ccaca3b2606462da4f8ea82eb3807c)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument target_file_size_mb", value=target_file_size_mb, expected_type=type_hints["target_file_size_mb"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status
            if target_file_size_mb is not None:
                self._values["target_file_size_mb"] = target_file_size_mb

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the maintenance configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-compaction.html#cfn-s3tables-table-compaction-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_file_size_mb(self) -> typing.Optional[jsii.Number]:
            '''The target file size for the table in MB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-compaction.html#cfn-s3tables-table-compaction-targetfilesizemb
            '''
            result = self._values.get("target_file_size_mb")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CompactionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTablePropsMixin.IcebergMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"iceberg_schema": "icebergSchema"},
    )
    class IcebergMetadataProperty:
        def __init__(
            self,
            *,
            iceberg_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.IcebergSchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains details about the metadata for an Iceberg table.

            :param iceberg_schema: The schema for an Iceberg table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-icebergmetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
                
                iceberg_metadata_property = s3tables_mixins.CfnTablePropsMixin.IcebergMetadataProperty(
                    iceberg_schema=s3tables_mixins.CfnTablePropsMixin.IcebergSchemaProperty(
                        schema_field_list=[s3tables_mixins.CfnTablePropsMixin.SchemaFieldProperty(
                            name="name",
                            required=False,
                            type="type"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__627116fd1e8cd5dcb0a51cb375f5de855deb1e1d9f2876f5f359ac811c237868)
                check_type(argname="argument iceberg_schema", value=iceberg_schema, expected_type=type_hints["iceberg_schema"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iceberg_schema is not None:
                self._values["iceberg_schema"] = iceberg_schema

        @builtins.property
        def iceberg_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.IcebergSchemaProperty"]]:
            '''The schema for an Iceberg table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-icebergmetadata.html#cfn-s3tables-table-icebergmetadata-icebergschema
            '''
            result = self._values.get("iceberg_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.IcebergSchemaProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IcebergMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTablePropsMixin.IcebergSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"schema_field_list": "schemaFieldList"},
    )
    class IcebergSchemaProperty:
        def __init__(
            self,
            *,
            schema_field_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.SchemaFieldProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains details about the schema for an Iceberg table.

            :param schema_field_list: The schema fields for the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-icebergschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
                
                iceberg_schema_property = s3tables_mixins.CfnTablePropsMixin.IcebergSchemaProperty(
                    schema_field_list=[s3tables_mixins.CfnTablePropsMixin.SchemaFieldProperty(
                        name="name",
                        required=False,
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__892fb443e35ad865d63214955414ebd85020f45e21de261e240e32de879eca3f)
                check_type(argname="argument schema_field_list", value=schema_field_list, expected_type=type_hints["schema_field_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schema_field_list is not None:
                self._values["schema_field_list"] = schema_field_list

        @builtins.property
        def schema_field_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SchemaFieldProperty"]]]]:
            '''The schema fields for the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-icebergschema.html#cfn-s3tables-table-icebergschema-schemafieldlist
            '''
            result = self._values.get("schema_field_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SchemaFieldProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IcebergSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTablePropsMixin.SchemaFieldProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "required": "required", "type": "type"},
    )
    class SchemaFieldProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains details about a schema field.

            :param name: The name of the field.
            :param required: A Boolean value that specifies whether values are required for each row in this field. By default, this is ``false`` and null values are allowed in the field. If this is ``true`` the field does not allow null values.
            :param type: The field type. S3 Tables supports all Apache Iceberg primitive types. For more information, see the `Apache Iceberg documentation <https://docs.aws.amazon.com/https://iceberg.apache.org/spec/#primitive-types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-schemafield.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
                
                schema_field_property = s3tables_mixins.CfnTablePropsMixin.SchemaFieldProperty(
                    name="name",
                    required=False,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e64be52a69566dea15b4215d92d944caf119ea0c17a22f234a0d19592fc3c2d)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if required is not None:
                self._values["required"] = required
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-schemafield.html#cfn-s3tables-table-schemafield-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value that specifies whether values are required for each row in this field.

            By default, this is ``false`` and null values are allowed in the field. If this is ``true`` the field does not allow null values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-schemafield.html#cfn-s3tables-table-schemafield-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The field type.

            S3 Tables supports all Apache Iceberg primitive types. For more information, see the `Apache Iceberg documentation <https://docs.aws.amazon.com/https://iceberg.apache.org/spec/#primitive-types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-schemafield.html#cfn-s3tables-table-schemafield-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaFieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTablePropsMixin.SnapshotManagementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_snapshot_age_hours": "maxSnapshotAgeHours",
            "min_snapshots_to_keep": "minSnapshotsToKeep",
            "status": "status",
        },
    )
    class SnapshotManagementProperty:
        def __init__(
            self,
            *,
            max_snapshot_age_hours: typing.Optional[jsii.Number] = None,
            min_snapshots_to_keep: typing.Optional[jsii.Number] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains details about the snapshot management settings for an Iceberg table.

            The oldest snapshot expires when its age exceeds the ``maxSnapshotAgeHours`` and the total number of snapshots exceeds the value for the minimum number of snapshots to keep ``minSnapshotsToKeep`` .

            :param max_snapshot_age_hours: The maximum age of a snapshot before it can be expired.
            :param min_snapshots_to_keep: The minimum number of snapshots to keep.
            :param status: The status of the maintenance configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-snapshotmanagement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
                
                snapshot_management_property = s3tables_mixins.CfnTablePropsMixin.SnapshotManagementProperty(
                    max_snapshot_age_hours=123,
                    min_snapshots_to_keep=123,
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45dc1c2d8009397b5469b81fa196e297c8b8e20138bbb80ccba672aa7bab1225)
                check_type(argname="argument max_snapshot_age_hours", value=max_snapshot_age_hours, expected_type=type_hints["max_snapshot_age_hours"])
                check_type(argname="argument min_snapshots_to_keep", value=min_snapshots_to_keep, expected_type=type_hints["min_snapshots_to_keep"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_snapshot_age_hours is not None:
                self._values["max_snapshot_age_hours"] = max_snapshot_age_hours
            if min_snapshots_to_keep is not None:
                self._values["min_snapshots_to_keep"] = min_snapshots_to_keep
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def max_snapshot_age_hours(self) -> typing.Optional[jsii.Number]:
            '''The maximum age of a snapshot before it can be expired.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-snapshotmanagement.html#cfn-s3tables-table-snapshotmanagement-maxsnapshotagehours
            '''
            result = self._values.get("max_snapshot_age_hours")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_snapshots_to_keep(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of snapshots to keep.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-snapshotmanagement.html#cfn-s3tables-table-snapshotmanagement-minsnapshotstokeep
            '''
            result = self._values.get("min_snapshots_to_keep")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the maintenance configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-snapshotmanagement.html#cfn-s3tables-table-snapshotmanagement-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnapshotManagementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3tables.mixins.CfnTablePropsMixin.StorageClassConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"storage_class": "storageClass"},
    )
    class StorageClassConfigurationProperty:
        def __init__(
            self,
            *,
            storage_class: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies storage class settings for the table.

            :param storage_class: The storage class for the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-storageclassconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3tables import mixins as s3tables_mixins
                
                storage_class_configuration_property = s3tables_mixins.CfnTablePropsMixin.StorageClassConfigurationProperty(
                    storage_class="storageClass"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a84c31324290d4645c51e8f2f02593c7e396f03fa354c6f31928d34a152ef168)
                check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if storage_class is not None:
                self._values["storage_class"] = storage_class

        @builtins.property
        def storage_class(self) -> typing.Optional[builtins.str]:
            '''The storage class for the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-storageclassconfiguration.html#cfn-s3tables-table-storageclassconfiguration-storageclass
            '''
            result = self._values.get("storage_class")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageClassConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnNamespaceMixinProps",
    "CfnNamespacePropsMixin",
    "CfnTableBucketMixinProps",
    "CfnTableBucketPolicyMixinProps",
    "CfnTableBucketPolicyPropsMixin",
    "CfnTableBucketPropsMixin",
    "CfnTableMixinProps",
    "CfnTablePolicyMixinProps",
    "CfnTablePolicyPropsMixin",
    "CfnTablePropsMixin",
]

publication.publish()

def _typecheckingstub__8ec8efc52b9d4aa55901cab63814f92948f7dd96cab0f92523786f757714c9d2(
    *,
    namespace: typing.Optional[builtins.str] = None,
    table_bucket_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4fb962db5cb7287f82a44a3562af66d98b52729067c52c86eb1a99a2d79191(
    props: typing.Union[CfnNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee320925454c58c3f6c527130569445057a5979bdda6ce3ad719dab52d5d1961(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce891791c6a34ad82104637e1e00283e92834f25ebdebcde3fa81c87f1616130(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e49a7ac032f051309883379d0263dc0f3ca574a28226fbc08083a8c7b449f4(
    *,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTableBucketPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTableBucketPropsMixin.MetricsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_class_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTableBucketPropsMixin.StorageClassConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_bucket_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    unreferenced_file_removal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTableBucketPropsMixin.UnreferencedFileRemovalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eea06f2805e3276e5df1737b0736254357d60dd5b81eff2eec2d2bc76b46655(
    *,
    resource_policy: typing.Any = None,
    table_bucket_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06b2919b20d081856f3f6d43480ca5c38a782d45066e4e684f0d74457b24e58(
    props: typing.Union[CfnTableBucketPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a54c99ba4646cbb40a5593db0932d2343c14f24fb08f291f54bedce082bcc9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85940d4b0b7272fc30b9df24c27913820ebf843c40d893d484809a67d9acebb8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe148dab0c375c474516537a6fa1706a649e9590cdac3fd56b1fbb7739be006(
    props: typing.Union[CfnTableBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c70b2339940531411472c57a34a20af288aaa8ec236c9a62f511aad75422e68(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ce44c555bb7f8c15da085dd684c2f938cbf3eb9a2d5995afa8334389a9f936(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78adc082218c7312551a05f667de1b7f4b45fdda9d0e5f0bfb38e3a702e3f359(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    sse_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82171fcf81a632054165d04e069363860d5d9f1782b2b237564f64b4be190db(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef74d9bac670a778393eff87e783a092524eb49b6f269f6a6dc383dfd3cc2e7(
    *,
    storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8631f11de540150b714cf52a30126aa231e71a335df37ebc338f9f3cdbcfc24(
    *,
    noncurrent_days: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    unreferenced_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6bcb174c4161953fd79c0047ec40ea37e3e613c9f7fdbbcf8cd46a1b569697(
    *,
    compaction: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.CompactionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iceberg_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.IcebergMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    namespace: typing.Optional[builtins.str] = None,
    open_table_format: typing.Optional[builtins.str] = None,
    snapshot_management: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.SnapshotManagementProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_class_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.StorageClassConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_bucket_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    without_metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efd3c64448ec5b368919c07f978ae3376042eed3ce73f9895158be204e87cbe(
    *,
    resource_policy: typing.Any = None,
    table_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd563df5ce2b18608fbbe17d8bd5594bfc0800edbf4aa6fd8a403751fe61c62(
    props: typing.Union[CfnTablePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308ffc317a0e4c9a7715f31ab0dbb713785e2371b5c12d7e62eb7e0b7735ee44(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9f760a02a789e0f51f82609cb3011666dbc905429d247570ae70678815d26b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7e9968ae9f3676898e534911090508995ba1cf2896132387d91eed5a776eb6(
    props: typing.Union[CfnTableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1835c57095d5f0d7268f9b878c46eaf2f754f7e91f560b304ea2af5048541614(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0f22b633ee4435f3fb07a2308d800d5348d7de22c44e17487aff05f3707459(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d9920b8fca2c0bc27df84d470eabaa504ccaca3b2606462da4f8ea82eb3807c(
    *,
    status: typing.Optional[builtins.str] = None,
    target_file_size_mb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627116fd1e8cd5dcb0a51cb375f5de855deb1e1d9f2876f5f359ac811c237868(
    *,
    iceberg_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.IcebergSchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892fb443e35ad865d63214955414ebd85020f45e21de261e240e32de879eca3f(
    *,
    schema_field_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.SchemaFieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e64be52a69566dea15b4215d92d944caf119ea0c17a22f234a0d19592fc3c2d(
    *,
    name: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45dc1c2d8009397b5469b81fa196e297c8b8e20138bbb80ccba672aa7bab1225(
    *,
    max_snapshot_age_hours: typing.Optional[jsii.Number] = None,
    min_snapshots_to_keep: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84c31324290d4645c51e8f2f02593c7e396f03fa354c6f31928d34a152ef168(
    *,
    storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
