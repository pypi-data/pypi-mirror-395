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
    jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnKeyspaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_side_timestamps_enabled": "clientSideTimestampsEnabled",
        "keyspace_name": "keyspaceName",
        "replication_specification": "replicationSpecification",
        "tags": "tags",
    },
)
class CfnKeyspaceMixinProps:
    def __init__(
        self,
        *,
        client_side_timestamps_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        keyspace_name: typing.Optional[builtins.str] = None,
        replication_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKeyspacePropsMixin.ReplicationSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnKeyspacePropsMixin.

        :param client_side_timestamps_enabled: Indicates whether client-side timestamps are enabled (true) or disabled (false) for all tables in the keyspace. To add a Region to a single-Region keyspace with at least one table, the value must be set to true. After you've enabled client-side timestamps for a table, you can’t disable it again.
        :param keyspace_name: The name of the keyspace to be created. The keyspace name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the keyspace name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . *Length constraints:* Minimum length of 1. Maximum length of 48.
        :param replication_specification: Specifies the ``ReplicationStrategy`` of a keyspace. The options are:. - ``SINGLE_REGION`` for a single Region keyspace (optional) or - ``MULTI_REGION`` for a multi-Region keyspace If no ``ReplicationStrategy`` is provided, the default is ``SINGLE_REGION`` . If you choose ``MULTI_REGION`` , you must also provide a ``RegionList`` with the AWS Regions that the keyspace is replicated in.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
            
            cfn_keyspace_mixin_props = cassandra_mixins.CfnKeyspaceMixinProps(
                client_side_timestamps_enabled=False,
                keyspace_name="keyspaceName",
                replication_specification=cassandra_mixins.CfnKeyspacePropsMixin.ReplicationSpecificationProperty(
                    region_list=["regionList"],
                    replication_strategy="replicationStrategy"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec109fb71330fc944d650ac725ffabb5499f94b6f55089ab9df1635479a4da3b)
            check_type(argname="argument client_side_timestamps_enabled", value=client_side_timestamps_enabled, expected_type=type_hints["client_side_timestamps_enabled"])
            check_type(argname="argument keyspace_name", value=keyspace_name, expected_type=type_hints["keyspace_name"])
            check_type(argname="argument replication_specification", value=replication_specification, expected_type=type_hints["replication_specification"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_side_timestamps_enabled is not None:
            self._values["client_side_timestamps_enabled"] = client_side_timestamps_enabled
        if keyspace_name is not None:
            self._values["keyspace_name"] = keyspace_name
        if replication_specification is not None:
            self._values["replication_specification"] = replication_specification
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def client_side_timestamps_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether client-side timestamps are enabled (true) or disabled (false) for all tables in the keyspace.

        To add a Region to a single-Region keyspace with at least one table, the value must be set to true. After you've enabled client-side timestamps for a table, you can’t disable it again.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html#cfn-cassandra-keyspace-clientsidetimestampsenabled
        '''
        result = self._values.get("client_side_timestamps_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def keyspace_name(self) -> typing.Optional[builtins.str]:
        '''The name of the keyspace to be created.

        The keyspace name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the keyspace name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        *Length constraints:* Minimum length of 1. Maximum length of 48.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html#cfn-cassandra-keyspace-keyspacename
        '''
        result = self._values.get("keyspace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKeyspacePropsMixin.ReplicationSpecificationProperty"]]:
        '''Specifies the ``ReplicationStrategy`` of a keyspace. The options are:.

        - ``SINGLE_REGION`` for a single Region keyspace (optional) or
        - ``MULTI_REGION`` for a multi-Region keyspace

        If no ``ReplicationStrategy`` is provided, the default is ``SINGLE_REGION`` . If you choose ``MULTI_REGION`` , you must also provide a ``RegionList`` with the AWS Regions that the keyspace is replicated in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html#cfn-cassandra-keyspace-replicationspecification
        '''
        result = self._values.get("replication_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKeyspacePropsMixin.ReplicationSpecificationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html#cfn-cassandra-keyspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnKeyspaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnKeyspacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnKeyspacePropsMixin",
):
    '''You can use the ``AWS::Cassandra::Keyspace`` resource to create a new keyspace in Amazon Keyspaces (for Apache Cassandra).

    For more information, see `Create a keyspace <https://docs.aws.amazon.com/keyspaces/latest/devguide/getting-started.keyspaces.html>`_ in the *Amazon Keyspaces Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html
    :cloudformationResource: AWS::Cassandra::Keyspace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
        
        cfn_keyspace_props_mixin = cassandra_mixins.CfnKeyspacePropsMixin(cassandra_mixins.CfnKeyspaceMixinProps(
            client_side_timestamps_enabled=False,
            keyspace_name="keyspaceName",
            replication_specification=cassandra_mixins.CfnKeyspacePropsMixin.ReplicationSpecificationProperty(
                region_list=["regionList"],
                replication_strategy="replicationStrategy"
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
        props: typing.Union[CfnKeyspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cassandra::Keyspace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f22242a23f803a0b495e4ba2e0b3b374d60e659b1a145678a60f282b25379720)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc8c39b893c0d347cd709ebee5c006a1b0b347661fe1d273d024e19ca9b0147f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c45081e7dff15382495c97f9abd9b5e2c62095edff0e8e8e917e71f0effc455)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnKeyspaceMixinProps:
        return typing.cast(CfnKeyspaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnKeyspacePropsMixin.ReplicationSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "region_list": "regionList",
            "replication_strategy": "replicationStrategy",
        },
    )
    class ReplicationSpecificationProperty:
        def __init__(
            self,
            *,
            region_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            replication_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''You can use ``ReplicationSpecification`` to configure the ``ReplicationStrategy`` of a keyspace in Amazon Keyspaces .

            The ``ReplicationSpecification`` property applies automatically to all tables in the keyspace.

            To review the permissions that are required to add a new Region to a single-Region keyspace, see `Configure the IAM permissions required to add an AWS Region to a keyspace <https://docs.aws.amazon.com/keyspaces/latest/devguide/howitworks_replication_permissions_addReplica.html>`_ in the *Amazon Keyspaces Developer Guide* .

            For more information about multi-Region replication, see `Multi-Region replication <https://docs.aws.amazon.com/keyspaces/latest/devguide/multiRegion-replication.html>`_ in the *Amazon Keyspaces Developer Guide* .

            :param region_list: Specifies the AWS Regions that the keyspace is replicated in. You must specify at least two Regions, including the Region that the keyspace is being created in. To specify a Region `that's disabled by default <https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-regions.html#rande-manage-enable>`_ , you must first enable the Region. For more information, see `Multi-Region replication in AWS Regions disabled by default <https://docs.aws.amazon.com/keyspaces/latest/devguide/multiRegion-replication_how-it-works.html#howitworks_mrr_opt_in>`_ in the *Amazon Keyspaces Developer Guide* .
            :param replication_strategy: The options are:. - ``SINGLE_REGION`` (optional) - ``MULTI_REGION`` If no value is specified, the default is ``SINGLE_REGION`` . If ``MULTI_REGION`` is specified, ``RegionList`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-keyspace-replicationspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                replication_specification_property = cassandra_mixins.CfnKeyspacePropsMixin.ReplicationSpecificationProperty(
                    region_list=["regionList"],
                    replication_strategy="replicationStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a41520c21d5ee728afb617db1fcc8e1630b668ed448d90d8c71d4d004dc530f4)
                check_type(argname="argument region_list", value=region_list, expected_type=type_hints["region_list"])
                check_type(argname="argument replication_strategy", value=replication_strategy, expected_type=type_hints["replication_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if region_list is not None:
                self._values["region_list"] = region_list
            if replication_strategy is not None:
                self._values["replication_strategy"] = replication_strategy

        @builtins.property
        def region_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the AWS Regions that the keyspace is replicated in.

            You must specify at least two Regions, including the Region that the keyspace is being created in.

            To specify a Region `that's disabled by default <https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-regions.html#rande-manage-enable>`_ , you must first enable the Region. For more information, see `Multi-Region replication in AWS Regions disabled by default <https://docs.aws.amazon.com/keyspaces/latest/devguide/multiRegion-replication_how-it-works.html#howitworks_mrr_opt_in>`_ in the *Amazon Keyspaces Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-keyspace-replicationspecification.html#cfn-cassandra-keyspace-replicationspecification-regionlist
            '''
            result = self._values.get("region_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def replication_strategy(self) -> typing.Optional[builtins.str]:
            '''The options are:.

            - ``SINGLE_REGION`` (optional)
            - ``MULTI_REGION``

            If no value is specified, the default is ``SINGLE_REGION`` . If ``MULTI_REGION`` is specified, ``RegionList`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-keyspace-replicationspecification.html#cfn-cassandra-keyspace-replicationspecification-replicationstrategy
            '''
            result = self._values.get("replication_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_specifications": "autoScalingSpecifications",
        "billing_mode": "billingMode",
        "cdc_specification": "cdcSpecification",
        "client_side_timestamps_enabled": "clientSideTimestampsEnabled",
        "clustering_key_columns": "clusteringKeyColumns",
        "default_time_to_live": "defaultTimeToLive",
        "encryption_specification": "encryptionSpecification",
        "keyspace_name": "keyspaceName",
        "partition_key_columns": "partitionKeyColumns",
        "point_in_time_recovery_enabled": "pointInTimeRecoveryEnabled",
        "regular_columns": "regularColumns",
        "replica_specifications": "replicaSpecifications",
        "table_name": "tableName",
        "tags": "tags",
        "warm_throughput": "warmThroughput",
    },
)
class CfnTableMixinProps:
    def __init__(
        self,
        *,
        auto_scaling_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.AutoScalingSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        billing_mode: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.BillingModeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cdc_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.CdcSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        client_side_timestamps_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        clustering_key_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ClusteringKeyColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        default_time_to_live: typing.Optional[jsii.Number] = None,
        encryption_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.EncryptionSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        keyspace_name: typing.Optional[builtins.str] = None,
        partition_key_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        regular_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        replica_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ReplicaSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        warm_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.WarmThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTablePropsMixin.

        :param auto_scaling_specifications: The optional auto scaling capacity settings for a table in provisioned capacity mode.
        :param billing_mode: The billing mode for the table, which determines how you'll be charged for reads and writes:. - *On-demand mode* (default) - You pay based on the actual reads and writes your application performs. - *Provisioned mode* - Lets you specify the number of reads and writes per second that you need for your application. If you don't specify a value for this property, then the table will use on-demand mode.
        :param cdc_specification: The settings for the CDC stream of a table. For more information about CDC streams, see `Working with change data capture (CDC) streams in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/cdc.html>`_ in the *Amazon Keyspaces Developer Guide* .
        :param client_side_timestamps_enabled: Enables client-side timestamps for the table. By default, the setting is disabled. You can enable client-side timestamps with the following option: - ``status: "enabled"`` After client-side timestamps are enabled for a table, you can't disable this setting.
        :param clustering_key_columns: One or more columns that determine how the table data is sorted.
        :param default_time_to_live: The default Time To Live (TTL) value for all rows in a table in seconds. The maximum configurable value is 630,720,000 seconds, which is the equivalent of 20 years. By default, the TTL value for a table is 0, which means data does not expire. For more information, see `Setting the default TTL value for a table <https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl>`_ in the *Amazon Keyspaces Developer Guide* .
        :param encryption_specification: The encryption at rest options for the table. - *AWS owned key* (default) - The key is owned by Amazon Keyspaces . - *Customer managed key* - The key is stored in your account and is created, owned, and managed by you. .. epigraph:: If you choose encryption with a customer managed key, you must specify a valid customer managed KMS key with permissions granted to Amazon Keyspaces. For more information, see `Encryption at rest in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html>`_ in the *Amazon Keyspaces Developer Guide* .
        :param keyspace_name: The name of the keyspace to create the table in. The keyspace must already exist.
        :param partition_key_columns: One or more columns that uniquely identify every row in the table. Every table must have a partition key.
        :param point_in_time_recovery_enabled: Specifies if point-in-time recovery is enabled or disabled for the table. The options are ``PointInTimeRecoveryEnabled=true`` and ``PointInTimeRecoveryEnabled=false`` . If not specified, the default is ``PointInTimeRecoveryEnabled=false`` .
        :param regular_columns: One or more columns that are not part of the primary key - that is, columns that are *not* defined as partition key columns or clustering key columns. You can add regular columns to existing tables by adding them to the template.
        :param replica_specifications: The AWS Region specific settings of a multi-Region table. For a multi-Region table, you can configure the table's read capacity differently per AWS Region. You can do this by configuring the following parameters. - ``region`` : The Region where these settings are applied. (Required) - ``readCapacityUnits`` : The provisioned read capacity units. (Optional) - ``readCapacityAutoScaling`` : The read capacity auto scaling settings for the table. (Optional)
        :param table_name: The name of the table to be created. The table name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you can't perform updates that require replacing this resource. You can perform updates that require no interruption or some interruption. If you must replace the resource, specify a new name. *Length constraints:* Minimum length of 3. Maximum length of 255. *Pattern:* ``^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$``
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param warm_throughput: Warm throughput configuration for the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
            
            cfn_table_mixin_props = cassandra_mixins.CfnTableMixinProps(
                auto_scaling_specifications=cassandra_mixins.CfnTablePropsMixin.AutoScalingSpecificationProperty(
                    read_capacity_auto_scaling=cassandra_mixins.CfnTablePropsMixin.AutoScalingSettingProperty(
                        auto_scaling_disabled=False,
                        maximum_units=123,
                        minimum_units=123,
                        scaling_policy=cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                            target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        )
                    ),
                    write_capacity_auto_scaling=cassandra_mixins.CfnTablePropsMixin.AutoScalingSettingProperty(
                        auto_scaling_disabled=False,
                        maximum_units=123,
                        minimum_units=123,
                        scaling_policy=cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                            target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        )
                    )
                ),
                billing_mode=cassandra_mixins.CfnTablePropsMixin.BillingModeProperty(
                    mode="mode",
                    provisioned_throughput=cassandra_mixins.CfnTablePropsMixin.ProvisionedThroughputProperty(
                        read_capacity_units=123,
                        write_capacity_units=123
                    )
                ),
                cdc_specification=cassandra_mixins.CfnTablePropsMixin.CdcSpecificationProperty(
                    status="status",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    view_type="viewType"
                ),
                client_side_timestamps_enabled=False,
                clustering_key_columns=[cassandra_mixins.CfnTablePropsMixin.ClusteringKeyColumnProperty(
                    column=cassandra_mixins.CfnTablePropsMixin.ColumnProperty(
                        column_name="columnName",
                        column_type="columnType"
                    ),
                    order_by="orderBy"
                )],
                default_time_to_live=123,
                encryption_specification=cassandra_mixins.CfnTablePropsMixin.EncryptionSpecificationProperty(
                    encryption_type="encryptionType",
                    kms_key_identifier="kmsKeyIdentifier"
                ),
                keyspace_name="keyspaceName",
                partition_key_columns=[cassandra_mixins.CfnTablePropsMixin.ColumnProperty(
                    column_name="columnName",
                    column_type="columnType"
                )],
                point_in_time_recovery_enabled=False,
                regular_columns=[cassandra_mixins.CfnTablePropsMixin.ColumnProperty(
                    column_name="columnName",
                    column_type="columnType"
                )],
                replica_specifications=[cassandra_mixins.CfnTablePropsMixin.ReplicaSpecificationProperty(
                    read_capacity_auto_scaling=cassandra_mixins.CfnTablePropsMixin.AutoScalingSettingProperty(
                        auto_scaling_disabled=False,
                        maximum_units=123,
                        minimum_units=123,
                        scaling_policy=cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                            target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        )
                    ),
                    read_capacity_units=123,
                    region="region"
                )],
                table_name="tableName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                warm_throughput=cassandra_mixins.CfnTablePropsMixin.WarmThroughputProperty(
                    read_units_per_second=123,
                    write_units_per_second=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be147112a4b0711b10c7857d2399a8dae2b1f21bb41a3d3f6e812c863bcab6f)
            check_type(argname="argument auto_scaling_specifications", value=auto_scaling_specifications, expected_type=type_hints["auto_scaling_specifications"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument cdc_specification", value=cdc_specification, expected_type=type_hints["cdc_specification"])
            check_type(argname="argument client_side_timestamps_enabled", value=client_side_timestamps_enabled, expected_type=type_hints["client_side_timestamps_enabled"])
            check_type(argname="argument clustering_key_columns", value=clustering_key_columns, expected_type=type_hints["clustering_key_columns"])
            check_type(argname="argument default_time_to_live", value=default_time_to_live, expected_type=type_hints["default_time_to_live"])
            check_type(argname="argument encryption_specification", value=encryption_specification, expected_type=type_hints["encryption_specification"])
            check_type(argname="argument keyspace_name", value=keyspace_name, expected_type=type_hints["keyspace_name"])
            check_type(argname="argument partition_key_columns", value=partition_key_columns, expected_type=type_hints["partition_key_columns"])
            check_type(argname="argument point_in_time_recovery_enabled", value=point_in_time_recovery_enabled, expected_type=type_hints["point_in_time_recovery_enabled"])
            check_type(argname="argument regular_columns", value=regular_columns, expected_type=type_hints["regular_columns"])
            check_type(argname="argument replica_specifications", value=replica_specifications, expected_type=type_hints["replica_specifications"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument warm_throughput", value=warm_throughput, expected_type=type_hints["warm_throughput"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_specifications is not None:
            self._values["auto_scaling_specifications"] = auto_scaling_specifications
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if cdc_specification is not None:
            self._values["cdc_specification"] = cdc_specification
        if client_side_timestamps_enabled is not None:
            self._values["client_side_timestamps_enabled"] = client_side_timestamps_enabled
        if clustering_key_columns is not None:
            self._values["clustering_key_columns"] = clustering_key_columns
        if default_time_to_live is not None:
            self._values["default_time_to_live"] = default_time_to_live
        if encryption_specification is not None:
            self._values["encryption_specification"] = encryption_specification
        if keyspace_name is not None:
            self._values["keyspace_name"] = keyspace_name
        if partition_key_columns is not None:
            self._values["partition_key_columns"] = partition_key_columns
        if point_in_time_recovery_enabled is not None:
            self._values["point_in_time_recovery_enabled"] = point_in_time_recovery_enabled
        if regular_columns is not None:
            self._values["regular_columns"] = regular_columns
        if replica_specifications is not None:
            self._values["replica_specifications"] = replica_specifications
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags
        if warm_throughput is not None:
            self._values["warm_throughput"] = warm_throughput

    @builtins.property
    def auto_scaling_specifications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.AutoScalingSpecificationProperty"]]:
        '''The optional auto scaling capacity settings for a table in provisioned capacity mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-autoscalingspecifications
        '''
        result = self._values.get("auto_scaling_specifications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.AutoScalingSpecificationProperty"]], result)

    @builtins.property
    def billing_mode(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.BillingModeProperty"]]:
        '''The billing mode for the table, which determines how you'll be charged for reads and writes:.

        - *On-demand mode* (default) - You pay based on the actual reads and writes your application performs.
        - *Provisioned mode* - Lets you specify the number of reads and writes per second that you need for your application.

        If you don't specify a value for this property, then the table will use on-demand mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-billingmode
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.BillingModeProperty"]], result)

    @builtins.property
    def cdc_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.CdcSpecificationProperty"]]:
        '''The settings for the CDC stream of a table.

        For more information about CDC streams, see `Working with change data capture (CDC) streams in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/cdc.html>`_ in the *Amazon Keyspaces Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-cdcspecification
        '''
        result = self._values.get("cdc_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.CdcSpecificationProperty"]], result)

    @builtins.property
    def client_side_timestamps_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables client-side timestamps for the table.

        By default, the setting is disabled. You can enable client-side timestamps with the following option:

        - ``status: "enabled"``

        After client-side timestamps are enabled for a table, you can't disable this setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-clientsidetimestampsenabled
        '''
        result = self._values.get("client_side_timestamps_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def clustering_key_columns(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ClusteringKeyColumnProperty"]]]]:
        '''One or more columns that determine how the table data is sorted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-clusteringkeycolumns
        '''
        result = self._values.get("clustering_key_columns")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ClusteringKeyColumnProperty"]]]], result)

    @builtins.property
    def default_time_to_live(self) -> typing.Optional[jsii.Number]:
        '''The default Time To Live (TTL) value for all rows in a table in seconds.

        The maximum configurable value is 630,720,000 seconds, which is the equivalent of 20 years. By default, the TTL value for a table is 0, which means data does not expire.

        For more information, see `Setting the default TTL value for a table <https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl>`_ in the *Amazon Keyspaces Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-defaulttimetolive
        '''
        result = self._values.get("default_time_to_live")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def encryption_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.EncryptionSpecificationProperty"]]:
        '''The encryption at rest options for the table.

        - *AWS owned key* (default) - The key is owned by Amazon Keyspaces .
        - *Customer managed key* - The key is stored in your account and is created, owned, and managed by you.

        .. epigraph::

           If you choose encryption with a customer managed key, you must specify a valid customer managed KMS key with permissions granted to Amazon Keyspaces.

        For more information, see `Encryption at rest in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html>`_ in the *Amazon Keyspaces Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-encryptionspecification
        '''
        result = self._values.get("encryption_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.EncryptionSpecificationProperty"]], result)

    @builtins.property
    def keyspace_name(self) -> typing.Optional[builtins.str]:
        '''The name of the keyspace to create the table in.

        The keyspace must already exist.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-keyspacename
        '''
        result = self._values.get("keyspace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_key_columns(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ColumnProperty"]]]]:
        '''One or more columns that uniquely identify every row in the table.

        Every table must have a partition key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-partitionkeycolumns
        '''
        result = self._values.get("partition_key_columns")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ColumnProperty"]]]], result)

    @builtins.property
    def point_in_time_recovery_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies if point-in-time recovery is enabled or disabled for the table.

        The options are ``PointInTimeRecoveryEnabled=true`` and ``PointInTimeRecoveryEnabled=false`` . If not specified, the default is ``PointInTimeRecoveryEnabled=false`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-pointintimerecoveryenabled
        '''
        result = self._values.get("point_in_time_recovery_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def regular_columns(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ColumnProperty"]]]]:
        '''One or more columns that are not part of the primary key - that is, columns that are *not* defined as partition key columns or clustering key columns.

        You can add regular columns to existing tables by adding them to the template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-regularcolumns
        '''
        result = self._values.get("regular_columns")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ColumnProperty"]]]], result)

    @builtins.property
    def replica_specifications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ReplicaSpecificationProperty"]]]]:
        '''The AWS Region specific settings of a multi-Region table.

        For a multi-Region table, you can configure the table's read capacity differently per AWS Region. You can do this by configuring the following parameters.

        - ``region`` : The Region where these settings are applied. (Required)
        - ``readCapacityUnits`` : The provisioned read capacity units. (Optional)
        - ``readCapacityAutoScaling`` : The read capacity auto scaling settings for the table. (Optional)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-replicaspecifications
        '''
        result = self._values.get("replica_specifications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ReplicaSpecificationProperty"]]]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''The name of the table to be created.

        The table name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacing this resource. You can perform updates that require no interruption or some interruption. If you must replace the resource, specify a new name.

        *Length constraints:* Minimum length of 3. Maximum length of 255.

        *Pattern:* ``^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def warm_throughput(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.WarmThroughputProperty"]]:
        '''Warm throughput configuration for the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-warmthroughput
        '''
        result = self._values.get("warm_throughput")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.WarmThroughputProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTablePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin",
):
    '''You can use the ``AWS::Cassandra::Table`` resource to create a new table in Amazon Keyspaces (for Apache Cassandra).

    For more information, see `Create a table <https://docs.aws.amazon.com/keyspaces/latest/devguide/getting-started.tables.html>`_ in the *Amazon Keyspaces Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html
    :cloudformationResource: AWS::Cassandra::Table
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
        
        cfn_table_props_mixin = cassandra_mixins.CfnTablePropsMixin(cassandra_mixins.CfnTableMixinProps(
            auto_scaling_specifications=cassandra_mixins.CfnTablePropsMixin.AutoScalingSpecificationProperty(
                read_capacity_auto_scaling=cassandra_mixins.CfnTablePropsMixin.AutoScalingSettingProperty(
                    auto_scaling_disabled=False,
                    maximum_units=123,
                    minimum_units=123,
                    scaling_policy=cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                        target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123,
                            target_value=123
                        )
                    )
                ),
                write_capacity_auto_scaling=cassandra_mixins.CfnTablePropsMixin.AutoScalingSettingProperty(
                    auto_scaling_disabled=False,
                    maximum_units=123,
                    minimum_units=123,
                    scaling_policy=cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                        target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123,
                            target_value=123
                        )
                    )
                )
            ),
            billing_mode=cassandra_mixins.CfnTablePropsMixin.BillingModeProperty(
                mode="mode",
                provisioned_throughput=cassandra_mixins.CfnTablePropsMixin.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                )
            ),
            cdc_specification=cassandra_mixins.CfnTablePropsMixin.CdcSpecificationProperty(
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                view_type="viewType"
            ),
            client_side_timestamps_enabled=False,
            clustering_key_columns=[cassandra_mixins.CfnTablePropsMixin.ClusteringKeyColumnProperty(
                column=cassandra_mixins.CfnTablePropsMixin.ColumnProperty(
                    column_name="columnName",
                    column_type="columnType"
                ),
                order_by="orderBy"
            )],
            default_time_to_live=123,
            encryption_specification=cassandra_mixins.CfnTablePropsMixin.EncryptionSpecificationProperty(
                encryption_type="encryptionType",
                kms_key_identifier="kmsKeyIdentifier"
            ),
            keyspace_name="keyspaceName",
            partition_key_columns=[cassandra_mixins.CfnTablePropsMixin.ColumnProperty(
                column_name="columnName",
                column_type="columnType"
            )],
            point_in_time_recovery_enabled=False,
            regular_columns=[cassandra_mixins.CfnTablePropsMixin.ColumnProperty(
                column_name="columnName",
                column_type="columnType"
            )],
            replica_specifications=[cassandra_mixins.CfnTablePropsMixin.ReplicaSpecificationProperty(
                read_capacity_auto_scaling=cassandra_mixins.CfnTablePropsMixin.AutoScalingSettingProperty(
                    auto_scaling_disabled=False,
                    maximum_units=123,
                    minimum_units=123,
                    scaling_policy=cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                        target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123,
                            target_value=123
                        )
                    )
                ),
                read_capacity_units=123,
                region="region"
            )],
            table_name="tableName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            warm_throughput=cassandra_mixins.CfnTablePropsMixin.WarmThroughputProperty(
                read_units_per_second=123,
                write_units_per_second=123
            )
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
        '''Create a mixin to apply properties to ``AWS::Cassandra::Table``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494fa64445f1d3521f9c663e9115f20fd5643d6636b4131477c7004156bbeacd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f61941ca12919a70111d679b87aaaf62270df5d6606837ac38de506270e07f7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0635a37d22038b0371127d02c0e91308edcdc3a7a572360cf0614c3b03fbd67b)
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
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.AutoScalingSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_scaling_disabled": "autoScalingDisabled",
            "maximum_units": "maximumUnits",
            "minimum_units": "minimumUnits",
            "scaling_policy": "scalingPolicy",
        },
    )
    class AutoScalingSettingProperty:
        def __init__(
            self,
            *,
            auto_scaling_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            maximum_units: typing.Optional[jsii.Number] = None,
            minimum_units: typing.Optional[jsii.Number] = None,
            scaling_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ScalingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The optional auto scaling settings for a table with provisioned throughput capacity.

            To turn on auto scaling for a table in ``throughputMode:PROVISIONED`` , you must specify the following parameters.

            Configure the minimum and maximum capacity units. The auto scaling policy ensures that capacity never goes below the minimum or above the maximum range.

            - ``minimumUnits`` : The minimum level of throughput the table should always be ready to support. The value must be between 1 and the max throughput per second quota for your account (40,000 by default).
            - ``maximumUnits`` : The maximum level of throughput the table should always be ready to support. The value must be between 1 and the max throughput per second quota for your account (40,000 by default).
            - ``scalingPolicy`` : Amazon Keyspaces supports the ``target tracking`` scaling policy. The auto scaling target is a percentage of the provisioned capacity of the table.

            For more information, see `Managing throughput capacity automatically with Amazon Keyspaces auto scaling <https://docs.aws.amazon.com/keyspaces/latest/devguide/autoscaling.html>`_ in the *Amazon Keyspaces Developer Guide* .

            :param auto_scaling_disabled: This optional parameter enables auto scaling for the table if set to ``false`` . Default: - false
            :param maximum_units: Manage costs by specifying the maximum amount of throughput to provision. The value must be between 1 and the max throughput per second quota for your account (40,000 by default).
            :param minimum_units: The minimum level of throughput the table should always be ready to support. The value must be between 1 and the max throughput per second quota for your account (40,000 by default).
            :param scaling_policy: Amazon Keyspaces supports the ``target tracking`` auto scaling policy. With this policy, Amazon Keyspaces auto scaling ensures that the table's ratio of consumed to provisioned capacity stays at or near the target value that you specify. You define the target value as a percentage between 20 and 90.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-autoscalingsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                auto_scaling_setting_property = cassandra_mixins.CfnTablePropsMixin.AutoScalingSettingProperty(
                    auto_scaling_disabled=False,
                    maximum_units=123,
                    minimum_units=123,
                    scaling_policy=cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                        target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123,
                            target_value=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9597a892072f4e6a4e2ebd8c077a92049b2599bc409114f32e6ffcf629617022)
                check_type(argname="argument auto_scaling_disabled", value=auto_scaling_disabled, expected_type=type_hints["auto_scaling_disabled"])
                check_type(argname="argument maximum_units", value=maximum_units, expected_type=type_hints["maximum_units"])
                check_type(argname="argument minimum_units", value=minimum_units, expected_type=type_hints["minimum_units"])
                check_type(argname="argument scaling_policy", value=scaling_policy, expected_type=type_hints["scaling_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_scaling_disabled is not None:
                self._values["auto_scaling_disabled"] = auto_scaling_disabled
            if maximum_units is not None:
                self._values["maximum_units"] = maximum_units
            if minimum_units is not None:
                self._values["minimum_units"] = minimum_units
            if scaling_policy is not None:
                self._values["scaling_policy"] = scaling_policy

        @builtins.property
        def auto_scaling_disabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This optional parameter enables auto scaling for the table if set to ``false`` .

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-autoscalingsetting.html#cfn-cassandra-table-autoscalingsetting-autoscalingdisabled
            '''
            result = self._values.get("auto_scaling_disabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def maximum_units(self) -> typing.Optional[jsii.Number]:
            '''Manage costs by specifying the maximum amount of throughput to provision.

            The value must be between 1 and the max throughput per second quota for your account (40,000 by default).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-autoscalingsetting.html#cfn-cassandra-table-autoscalingsetting-maximumunits
            '''
            result = self._values.get("maximum_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum_units(self) -> typing.Optional[jsii.Number]:
            '''The minimum level of throughput the table should always be ready to support.

            The value must be between 1 and the max throughput per second quota for your account (40,000 by default).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-autoscalingsetting.html#cfn-cassandra-table-autoscalingsetting-minimumunits
            '''
            result = self._values.get("minimum_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scaling_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ScalingPolicyProperty"]]:
            '''Amazon Keyspaces supports the ``target tracking`` auto scaling policy.

            With this policy, Amazon Keyspaces auto scaling ensures that the table's ratio of consumed to provisioned capacity stays at or near the target value that you specify. You define the target value as a percentage between 20 and 90.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-autoscalingsetting.html#cfn-cassandra-table-autoscalingsetting-scalingpolicy
            '''
            result = self._values.get("scaling_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ScalingPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.AutoScalingSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "read_capacity_auto_scaling": "readCapacityAutoScaling",
            "write_capacity_auto_scaling": "writeCapacityAutoScaling",
        },
    )
    class AutoScalingSpecificationProperty:
        def __init__(
            self,
            *,
            read_capacity_auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.AutoScalingSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            write_capacity_auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.AutoScalingSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The optional auto scaling capacity settings for a table in provisioned capacity mode.

            :param read_capacity_auto_scaling: The auto scaling settings for the table's read capacity.
            :param write_capacity_auto_scaling: The auto scaling settings for the table's write capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-autoscalingspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                auto_scaling_specification_property = cassandra_mixins.CfnTablePropsMixin.AutoScalingSpecificationProperty(
                    read_capacity_auto_scaling=cassandra_mixins.CfnTablePropsMixin.AutoScalingSettingProperty(
                        auto_scaling_disabled=False,
                        maximum_units=123,
                        minimum_units=123,
                        scaling_policy=cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                            target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        )
                    ),
                    write_capacity_auto_scaling=cassandra_mixins.CfnTablePropsMixin.AutoScalingSettingProperty(
                        auto_scaling_disabled=False,
                        maximum_units=123,
                        minimum_units=123,
                        scaling_policy=cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                            target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b3c1ff5ad399d59340b8c65fee52dab7e330bb96b2a13300d1ea8033a383f02)
                check_type(argname="argument read_capacity_auto_scaling", value=read_capacity_auto_scaling, expected_type=type_hints["read_capacity_auto_scaling"])
                check_type(argname="argument write_capacity_auto_scaling", value=write_capacity_auto_scaling, expected_type=type_hints["write_capacity_auto_scaling"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if read_capacity_auto_scaling is not None:
                self._values["read_capacity_auto_scaling"] = read_capacity_auto_scaling
            if write_capacity_auto_scaling is not None:
                self._values["write_capacity_auto_scaling"] = write_capacity_auto_scaling

        @builtins.property
        def read_capacity_auto_scaling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.AutoScalingSettingProperty"]]:
            '''The auto scaling settings for the table's read capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-autoscalingspecification.html#cfn-cassandra-table-autoscalingspecification-readcapacityautoscaling
            '''
            result = self._values.get("read_capacity_auto_scaling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.AutoScalingSettingProperty"]], result)

        @builtins.property
        def write_capacity_auto_scaling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.AutoScalingSettingProperty"]]:
            '''The auto scaling settings for the table's write capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-autoscalingspecification.html#cfn-cassandra-table-autoscalingspecification-writecapacityautoscaling
            '''
            result = self._values.get("write_capacity_auto_scaling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.AutoScalingSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.BillingModeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mode": "mode",
            "provisioned_throughput": "provisionedThroughput",
        },
    )
    class BillingModeProperty:
        def __init__(
            self,
            *,
            mode: typing.Optional[builtins.str] = None,
            provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ProvisionedThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Determines the billing mode for the table - on-demand or provisioned.

            :param mode: The billing mode for the table:. - On-demand mode - ``ON_DEMAND`` - Provisioned mode - ``PROVISIONED`` .. epigraph:: If you choose ``PROVISIONED`` mode, then you also need to specify provisioned throughput (read and write capacity) for the table. Valid values: ``ON_DEMAND`` | ``PROVISIONED`` Default: - "ON_DEMAND"
            :param provisioned_throughput: The provisioned read capacity and write capacity for the table. For more information, see `Provisioned throughput capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html#ReadWriteCapacityMode.Provisioned>`_ in the *Amazon Keyspaces Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-billingmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                billing_mode_property = cassandra_mixins.CfnTablePropsMixin.BillingModeProperty(
                    mode="mode",
                    provisioned_throughput=cassandra_mixins.CfnTablePropsMixin.ProvisionedThroughputProperty(
                        read_capacity_units=123,
                        write_capacity_units=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba504e3d4001995c98f08f6116fe87339e79cf19c11361da376dd71d162d1f28)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode
            if provisioned_throughput is not None:
                self._values["provisioned_throughput"] = provisioned_throughput

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The billing mode for the table:.

            - On-demand mode - ``ON_DEMAND``
            - Provisioned mode - ``PROVISIONED``

            .. epigraph::

               If you choose ``PROVISIONED`` mode, then you also need to specify provisioned throughput (read and write capacity) for the table.

            Valid values: ``ON_DEMAND`` | ``PROVISIONED``

            :default: - "ON_DEMAND"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-billingmode.html#cfn-cassandra-table-billingmode-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def provisioned_throughput(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ProvisionedThroughputProperty"]]:
            '''The provisioned read capacity and write capacity for the table.

            For more information, see `Provisioned throughput capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html#ReadWriteCapacityMode.Provisioned>`_ in the *Amazon Keyspaces Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-billingmode.html#cfn-cassandra-table-billingmode-provisionedthroughput
            '''
            result = self._values.get("provisioned_throughput")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ProvisionedThroughputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BillingModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.CdcSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status", "tags": "tags", "view_type": "viewType"},
    )
    class CdcSpecificationProperty:
        def __init__(
            self,
            *,
            status: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
            view_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for the CDC stream of a table.

            For more information about CDC streams, see `Working with change data capture (CDC) streams in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/cdc.html>`_ in the *Amazon Keyspaces Developer Guide* .

            :param status: The status of the CDC stream. You can enable or disable a stream for a table.
            :param tags: The tags (key-value pairs) that you want to apply to the stream.
            :param view_type: The view type specifies the changes Amazon Keyspaces records for each changed row in the stream. After you create the stream, you can't make changes to this selection. The options are: - ``NEW_AND_OLD_IMAGES`` - both versions of the row, before and after the change. This is the default. - ``NEW_IMAGE`` - the version of the row after the change. - ``OLD_IMAGE`` - the version of the row before the change. - ``KEYS_ONLY`` - the partition and clustering keys of the row that was changed. Default: - "NEW_AND_OLD_IMAGES"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-cdcspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                cdc_specification_property = cassandra_mixins.CfnTablePropsMixin.CdcSpecificationProperty(
                    status="status",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    view_type="viewType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7cdd26b678ab8cc3385ae9a3eca71f461e37c443acc651f482bf784b606ef768)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument view_type", value=view_type, expected_type=type_hints["view_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status
            if tags is not None:
                self._values["tags"] = tags
            if view_type is not None:
                self._values["view_type"] = view_type

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the CDC stream.

            You can enable or disable a stream for a table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-cdcspecification.html#cfn-cassandra-table-cdcspecification-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The tags (key-value pairs) that you want to apply to the stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-cdcspecification.html#cfn-cassandra-table-cdcspecification-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        @builtins.property
        def view_type(self) -> typing.Optional[builtins.str]:
            '''The view type specifies the changes Amazon Keyspaces records for each changed row in the stream.

            After you create the stream, you can't make changes to this selection.

            The options are:

            - ``NEW_AND_OLD_IMAGES`` - both versions of the row, before and after the change. This is the default.
            - ``NEW_IMAGE`` - the version of the row after the change.
            - ``OLD_IMAGE`` - the version of the row before the change.
            - ``KEYS_ONLY`` - the partition and clustering keys of the row that was changed.

            :default: - "NEW_AND_OLD_IMAGES"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-cdcspecification.html#cfn-cassandra-table-cdcspecification-viewtype
            '''
            result = self._values.get("view_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CdcSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.ClusteringKeyColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"column": "column", "order_by": "orderBy"},
    )
    class ClusteringKeyColumnProperty:
        def __init__(
            self,
            *,
            column: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ColumnProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            order_by: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an individual column within the clustering key.

            :param column: The name and data type of this clustering key column.
            :param order_by: The order in which this column's data is stored:. - ``ASC`` (default) - The column's data is stored in ascending order. - ``DESC`` - The column's data is stored in descending order. Default: - "ASC"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-clusteringkeycolumn.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                clustering_key_column_property = cassandra_mixins.CfnTablePropsMixin.ClusteringKeyColumnProperty(
                    column=cassandra_mixins.CfnTablePropsMixin.ColumnProperty(
                        column_name="columnName",
                        column_type="columnType"
                    ),
                    order_by="orderBy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6f8ec6265fefe8cb447901c8317abf928852b7465cf6ade386d059a34032502)
                check_type(argname="argument column", value=column, expected_type=type_hints["column"])
                check_type(argname="argument order_by", value=order_by, expected_type=type_hints["order_by"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if column is not None:
                self._values["column"] = column
            if order_by is not None:
                self._values["order_by"] = order_by

        @builtins.property
        def column(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ColumnProperty"]]:
            '''The name and data type of this clustering key column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-clusteringkeycolumn.html#cfn-cassandra-table-clusteringkeycolumn-column
            '''
            result = self._values.get("column")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ColumnProperty"]], result)

        @builtins.property
        def order_by(self) -> typing.Optional[builtins.str]:
            '''The order in which this column's data is stored:.

            - ``ASC`` (default) - The column's data is stored in ascending order.
            - ``DESC`` - The column's data is stored in descending order.

            :default: - "ASC"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-clusteringkeycolumn.html#cfn-cassandra-table-clusteringkeycolumn-orderby
            '''
            result = self._values.get("order_by")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClusteringKeyColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.ColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"column_name": "columnName", "column_type": "columnType"},
    )
    class ColumnProperty:
        def __init__(
            self,
            *,
            column_name: typing.Optional[builtins.str] = None,
            column_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name and data type of an individual column in a table.

            In addition to the data type, you can also use the following two keywords:

            - ``STATIC`` if the table has a clustering column. Static columns store values that are shared by all rows in the same partition.
            - ``FROZEN`` for collection data types. In frozen collections the values of the collection are serialized into a single immutable value, and Amazon Keyspaces treats them like a ``BLOB`` .

            :param column_name: The name of the column. For more information, see `Identifiers <https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.elements.identifier>`_ in the *Amazon Keyspaces Developer Guide* .
            :param column_type: The data type of the column. For more information, see `Data types <https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.data-types>`_ in the *Amazon Keyspaces Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-column.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                column_property = cassandra_mixins.CfnTablePropsMixin.ColumnProperty(
                    column_name="columnName",
                    column_type="columnType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ab99ec8c1315593a714a4c933f1d9ec93659c90cad8c5ea7bb60e08055d1ccb)
                check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
                check_type(argname="argument column_type", value=column_type, expected_type=type_hints["column_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if column_name is not None:
                self._values["column_name"] = column_name
            if column_type is not None:
                self._values["column_type"] = column_type

        @builtins.property
        def column_name(self) -> typing.Optional[builtins.str]:
            '''The name of the column.

            For more information, see `Identifiers <https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.elements.identifier>`_ in the *Amazon Keyspaces Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-column.html#cfn-cassandra-table-column-columnname
            '''
            result = self._values.get("column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def column_type(self) -> typing.Optional[builtins.str]:
            '''The data type of the column.

            For more information, see `Data types <https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.data-types>`_ in the *Amazon Keyspaces Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-column.html#cfn-cassandra-table-column-columntype
            '''
            result = self._values.get("column_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.EncryptionSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_type": "encryptionType",
            "kms_key_identifier": "kmsKeyIdentifier",
        },
    )
    class EncryptionSpecificationProperty:
        def __init__(
            self,
            *,
            encryption_type: typing.Optional[builtins.str] = None,
            kms_key_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the encryption at rest option selected for the table.

            :param encryption_type: The encryption at rest options for the table. - *AWS owned key* (default) - ``AWS_OWNED_KMS_KEY`` - *Customer managed key* - ``CUSTOMER_MANAGED_KMS_KEY`` .. epigraph:: If you choose ``CUSTOMER_MANAGED_KMS_KEY`` , a ``kms_key_identifier`` in the format of a key ARN is required. Valid values: ``CUSTOMER_MANAGED_KMS_KEY`` | ``AWS_OWNED_KMS_KEY`` . Default: - "AWS_OWNED_KMS_KEY"
            :param kms_key_identifier: Requires a ``kms_key_identifier`` in the format of a key ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-encryptionspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                encryption_specification_property = cassandra_mixins.CfnTablePropsMixin.EncryptionSpecificationProperty(
                    encryption_type="encryptionType",
                    kms_key_identifier="kmsKeyIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e07bc27246ae7acaea664d848e7cfa7024bd1e20689841b9531b6d03f7c3884)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                check_type(argname="argument kms_key_identifier", value=kms_key_identifier, expected_type=type_hints["kms_key_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_type is not None:
                self._values["encryption_type"] = encryption_type
            if kms_key_identifier is not None:
                self._values["kms_key_identifier"] = kms_key_identifier

        @builtins.property
        def encryption_type(self) -> typing.Optional[builtins.str]:
            '''The encryption at rest options for the table.

            - *AWS owned key* (default) - ``AWS_OWNED_KMS_KEY``
            - *Customer managed key* - ``CUSTOMER_MANAGED_KMS_KEY``

            .. epigraph::

               If you choose ``CUSTOMER_MANAGED_KMS_KEY`` , a ``kms_key_identifier`` in the format of a key ARN is required.

            Valid values: ``CUSTOMER_MANAGED_KMS_KEY`` | ``AWS_OWNED_KMS_KEY`` .

            :default: - "AWS_OWNED_KMS_KEY"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-encryptionspecification.html#cfn-cassandra-table-encryptionspecification-encryptiontype
            '''
            result = self._values.get("encryption_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_identifier(self) -> typing.Optional[builtins.str]:
            '''Requires a ``kms_key_identifier`` in the format of a key ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-encryptionspecification.html#cfn-cassandra-table-encryptionspecification-kmskeyidentifier
            '''
            result = self._values.get("kms_key_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.ProvisionedThroughputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "read_capacity_units": "readCapacityUnits",
            "write_capacity_units": "writeCapacityUnits",
        },
    )
    class ProvisionedThroughputProperty:
        def __init__(
            self,
            *,
            read_capacity_units: typing.Optional[jsii.Number] = None,
            write_capacity_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The provisioned throughput for the table, which consists of ``ReadCapacityUnits`` and ``WriteCapacityUnits`` .

            :param read_capacity_units: The amount of read capacity that's provisioned for the table. For more information, see `Read/write capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html>`_ in the *Amazon Keyspaces Developer Guide* .
            :param write_capacity_units: The amount of write capacity that's provisioned for the table. For more information, see `Read/write capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html>`_ in the *Amazon Keyspaces Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-provisionedthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                provisioned_throughput_property = cassandra_mixins.CfnTablePropsMixin.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72024675d0d3fca8a426c5a4e4abd8c092ac5bfd0f1da37f731b6ede3eb1135b)
                check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
                check_type(argname="argument write_capacity_units", value=write_capacity_units, expected_type=type_hints["write_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if read_capacity_units is not None:
                self._values["read_capacity_units"] = read_capacity_units
            if write_capacity_units is not None:
                self._values["write_capacity_units"] = write_capacity_units

        @builtins.property
        def read_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The amount of read capacity that's provisioned for the table.

            For more information, see `Read/write capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html>`_ in the *Amazon Keyspaces Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-provisionedthroughput.html#cfn-cassandra-table-provisionedthroughput-readcapacityunits
            '''
            result = self._values.get("read_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def write_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The amount of write capacity that's provisioned for the table.

            For more information, see `Read/write capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html>`_ in the *Amazon Keyspaces Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-provisionedthroughput.html#cfn-cassandra-table-provisionedthroughput-writecapacityunits
            '''
            result = self._values.get("write_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedThroughputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.ReplicaSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "read_capacity_auto_scaling": "readCapacityAutoScaling",
            "read_capacity_units": "readCapacityUnits",
            "region": "region",
        },
    )
    class ReplicaSpecificationProperty:
        def __init__(
            self,
            *,
            read_capacity_auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.AutoScalingSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            read_capacity_units: typing.Optional[jsii.Number] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS Region specific settings of a multi-Region table.

            For a multi-Region table, you can configure the table's read capacity differently per AWS Region. You can do this by configuring the following parameters.

            - ``region`` : The Region where these settings are applied. (Required)
            - ``readCapacityUnits`` : The provisioned read capacity units. (Optional)
            - ``readCapacityAutoScaling`` : The read capacity auto scaling settings for the table. (Optional)

            :param read_capacity_auto_scaling: The read capacity auto scaling settings for the multi-Region table in the specified AWS Region.
            :param read_capacity_units: The provisioned read capacity units for the multi-Region table in the specified AWS Region.
            :param region: The AWS Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-replicaspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                replica_specification_property = cassandra_mixins.CfnTablePropsMixin.ReplicaSpecificationProperty(
                    read_capacity_auto_scaling=cassandra_mixins.CfnTablePropsMixin.AutoScalingSettingProperty(
                        auto_scaling_disabled=False,
                        maximum_units=123,
                        minimum_units=123,
                        scaling_policy=cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                            target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        )
                    ),
                    read_capacity_units=123,
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a34615fc032b5a73ab65641451cbc8d02d1ff105be1ae35dc37843ad190b65f6)
                check_type(argname="argument read_capacity_auto_scaling", value=read_capacity_auto_scaling, expected_type=type_hints["read_capacity_auto_scaling"])
                check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if read_capacity_auto_scaling is not None:
                self._values["read_capacity_auto_scaling"] = read_capacity_auto_scaling
            if read_capacity_units is not None:
                self._values["read_capacity_units"] = read_capacity_units
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def read_capacity_auto_scaling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.AutoScalingSettingProperty"]]:
            '''The read capacity auto scaling settings for the multi-Region table in the specified AWS Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-replicaspecification.html#cfn-cassandra-table-replicaspecification-readcapacityautoscaling
            '''
            result = self._values.get("read_capacity_auto_scaling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.AutoScalingSettingProperty"]], result)

        @builtins.property
        def read_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The provisioned read capacity units for the multi-Region table in the specified AWS Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-replicaspecification.html#cfn-cassandra-table-replicaspecification-readcapacityunits
            '''
            result = self._values.get("read_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-replicaspecification.html#cfn-cassandra-table-replicaspecification-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.ScalingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_tracking_scaling_policy_configuration": "targetTrackingScalingPolicyConfiguration",
        },
    )
    class ScalingPolicyProperty:
        def __init__(
            self,
            *,
            target_tracking_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Amazon Keyspaces supports the ``target tracking`` auto scaling policy.

            With this policy, Amazon Keyspaces auto scaling ensures that the table's ratio of consumed to provisioned capacity stays at or near the target value that you specify. You define the target value as a percentage between 20 and 90.

            :param target_tracking_scaling_policy_configuration: The auto scaling policy that scales a table based on the ratio of consumed to provisioned capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-scalingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                scaling_policy_property = cassandra_mixins.CfnTablePropsMixin.ScalingPolicyProperty(
                    target_tracking_scaling_policy_configuration=cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                        disable_scale_in=False,
                        scale_in_cooldown=123,
                        scale_out_cooldown=123,
                        target_value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a414de0fe93167f406254b8a176c48c92004308ccdc1fdfb798f4f03a3d87be)
                check_type(argname="argument target_tracking_scaling_policy_configuration", value=target_tracking_scaling_policy_configuration, expected_type=type_hints["target_tracking_scaling_policy_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_tracking_scaling_policy_configuration is not None:
                self._values["target_tracking_scaling_policy_configuration"] = target_tracking_scaling_policy_configuration

        @builtins.property
        def target_tracking_scaling_policy_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty"]]:
            '''The auto scaling policy that scales a table based on the ratio of consumed to provisioned capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-scalingpolicy.html#cfn-cassandra-table-scalingpolicy-targettrackingscalingpolicyconfiguration
            '''
            result = self._values.get("target_tracking_scaling_policy_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "disable_scale_in": "disableScaleIn",
            "scale_in_cooldown": "scaleInCooldown",
            "scale_out_cooldown": "scaleOutCooldown",
            "target_value": "targetValue",
        },
    )
    class TargetTrackingScalingPolicyConfigurationProperty:
        def __init__(
            self,
            *,
            disable_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            scale_in_cooldown: typing.Optional[jsii.Number] = None,
            scale_out_cooldown: typing.Optional[jsii.Number] = None,
            target_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Amazon Keyspaces supports the ``target tracking`` auto scaling policy for a provisioned table.

            This policy scales a table based on the ratio of consumed to provisioned capacity. The auto scaling target is a percentage of the provisioned capacity of the table.

            - ``targetTrackingScalingPolicyConfiguration`` : To define the target tracking policy, you must define the target value.
            - ``targetValue`` : The target utilization rate of the table. Amazon Keyspaces auto scaling ensures that the ratio of consumed capacity to provisioned capacity stays at or near this value. You define ``targetValue`` as a percentage. A ``double`` between 20 and 90. (Required)
            - ``disableScaleIn`` : A ``boolean`` that specifies if ``scale-in`` is disabled or enabled for the table. This parameter is disabled by default. To turn on ``scale-in`` , set the ``boolean`` value to ``FALSE`` . This means that capacity for a table can be automatically scaled down on your behalf. (Optional)
            - ``scaleInCooldown`` : A cooldown period in seconds between scaling activities that lets the table stabilize before another scale in activity starts. If no value is provided, the default is 0. (Optional)
            - ``scaleOutCooldown`` : A cooldown period in seconds between scaling activities that lets the table stabilize before another scale out activity starts. If no value is provided, the default is 0. (Optional)

            :param disable_scale_in: Specifies if ``scale-in`` is enabled. When auto scaling automatically decreases capacity for a table, the table *scales in* . When scaling policies are set, they can't scale in the table lower than its minimum capacity.
            :param scale_in_cooldown: Specifies a ``scale-in`` cool down period. A cooldown period in seconds between scaling activities that lets the table stabilize before another scaling activity starts. Default: - 0
            :param scale_out_cooldown: Specifies a scale out cool down period. A cooldown period in seconds between scaling activities that lets the table stabilize before another scaling activity starts. Default: - 0
            :param target_value: Specifies the target value for the target tracking auto scaling policy. Amazon Keyspaces auto scaling scales up capacity automatically when traffic exceeds this target utilization rate, and then back down when it falls below the target. This ensures that the ratio of consumed capacity to provisioned capacity stays at or near this value. You define ``targetValue`` as a percentage. An ``integer`` between 20 and 90.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-targettrackingscalingpolicyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                target_tracking_scaling_policy_configuration_property = cassandra_mixins.CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                    disable_scale_in=False,
                    scale_in_cooldown=123,
                    scale_out_cooldown=123,
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aadb89f4279fe95f874982fd1c79af2ff369f48232e774b9fba34a7ed4df4f32)
                check_type(argname="argument disable_scale_in", value=disable_scale_in, expected_type=type_hints["disable_scale_in"])
                check_type(argname="argument scale_in_cooldown", value=scale_in_cooldown, expected_type=type_hints["scale_in_cooldown"])
                check_type(argname="argument scale_out_cooldown", value=scale_out_cooldown, expected_type=type_hints["scale_out_cooldown"])
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if disable_scale_in is not None:
                self._values["disable_scale_in"] = disable_scale_in
            if scale_in_cooldown is not None:
                self._values["scale_in_cooldown"] = scale_in_cooldown
            if scale_out_cooldown is not None:
                self._values["scale_out_cooldown"] = scale_out_cooldown
            if target_value is not None:
                self._values["target_value"] = target_value

        @builtins.property
        def disable_scale_in(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies if ``scale-in`` is enabled.

            When auto scaling automatically decreases capacity for a table, the table *scales in* . When scaling policies are set, they can't scale in the table lower than its minimum capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-targettrackingscalingpolicyconfiguration.html#cfn-cassandra-table-targettrackingscalingpolicyconfiguration-disablescalein
            '''
            result = self._values.get("disable_scale_in")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def scale_in_cooldown(self) -> typing.Optional[jsii.Number]:
            '''Specifies a ``scale-in`` cool down period.

            A cooldown period in seconds between scaling activities that lets the table stabilize before another scaling activity starts.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-targettrackingscalingpolicyconfiguration.html#cfn-cassandra-table-targettrackingscalingpolicyconfiguration-scaleincooldown
            '''
            result = self._values.get("scale_in_cooldown")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scale_out_cooldown(self) -> typing.Optional[jsii.Number]:
            '''Specifies a scale out cool down period.

            A cooldown period in seconds between scaling activities that lets the table stabilize before another scaling activity starts.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-targettrackingscalingpolicyconfiguration.html#cfn-cassandra-table-targettrackingscalingpolicyconfiguration-scaleoutcooldown
            '''
            result = self._values.get("scale_out_cooldown")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''Specifies the target value for the target tracking auto scaling policy.

            Amazon Keyspaces auto scaling scales up capacity automatically when traffic exceeds this target utilization rate, and then back down when it falls below the target. This ensures that the ratio of consumed capacity to provisioned capacity stays at or near this value. You define ``targetValue`` as a percentage. An ``integer`` between 20 and 90.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-targettrackingscalingpolicyconfiguration.html#cfn-cassandra-table-targettrackingscalingpolicyconfiguration-targetvalue
            '''
            result = self._values.get("target_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingScalingPolicyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTablePropsMixin.WarmThroughputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "read_units_per_second": "readUnitsPerSecond",
            "write_units_per_second": "writeUnitsPerSecond",
        },
    )
    class WarmThroughputProperty:
        def __init__(
            self,
            *,
            read_units_per_second: typing.Optional[jsii.Number] = None,
            write_units_per_second: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Warm throughput configuration for the table.

            :param read_units_per_second: 
            :param write_units_per_second: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-warmthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                warm_throughput_property = cassandra_mixins.CfnTablePropsMixin.WarmThroughputProperty(
                    read_units_per_second=123,
                    write_units_per_second=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d44d95084edd1b63b29f19bb7375b827ff5c9426d8b374ae92105b15766094c3)
                check_type(argname="argument read_units_per_second", value=read_units_per_second, expected_type=type_hints["read_units_per_second"])
                check_type(argname="argument write_units_per_second", value=write_units_per_second, expected_type=type_hints["write_units_per_second"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if read_units_per_second is not None:
                self._values["read_units_per_second"] = read_units_per_second
            if write_units_per_second is not None:
                self._values["write_units_per_second"] = write_units_per_second

        @builtins.property
        def read_units_per_second(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-warmthroughput.html#cfn-cassandra-table-warmthroughput-readunitspersecond
            '''
            result = self._values.get("read_units_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def write_units_per_second(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-warmthroughput.html#cfn-cassandra-table-warmthroughput-writeunitspersecond
            '''
            result = self._values.get("write_units_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WarmThroughputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTypeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "fields": "fields",
        "keyspace_name": "keyspaceName",
        "type_name": "typeName",
    },
)
class CfnTypeMixinProps:
    def __init__(
        self,
        *,
        fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTypePropsMixin.FieldProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        keyspace_name: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTypePropsMixin.

        :param fields: A list of fields that define this type.
        :param keyspace_name: The name of the keyspace to create the type in. The keyspace must already exist.
        :param type_name: The name of the user-defined type. UDT names must contain 48 characters or less, must begin with an alphabetic character, and can only contain alpha-numeric characters and underscores. Amazon Keyspaces converts upper case characters automatically into lower case characters. For more information, see `Create a user-defined type (UDT) in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/keyspaces-create-udt.html>`_ in the *Amazon Keyspaces Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-type.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
            
            cfn_type_mixin_props = cassandra_mixins.CfnTypeMixinProps(
                fields=[cassandra_mixins.CfnTypePropsMixin.FieldProperty(
                    field_name="fieldName",
                    field_type="fieldType"
                )],
                keyspace_name="keyspaceName",
                type_name="typeName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1c7cf942933345f3b9ff7058e102e997eb03e1306f26c193060c7194d539ae)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument keyspace_name", value=keyspace_name, expected_type=type_hints["keyspace_name"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fields is not None:
            self._values["fields"] = fields
        if keyspace_name is not None:
            self._values["keyspace_name"] = keyspace_name
        if type_name is not None:
            self._values["type_name"] = type_name

    @builtins.property
    def fields(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTypePropsMixin.FieldProperty"]]]]:
        '''A list of fields that define this type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-type.html#cfn-cassandra-type-fields
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTypePropsMixin.FieldProperty"]]]], result)

    @builtins.property
    def keyspace_name(self) -> typing.Optional[builtins.str]:
        '''The name of the keyspace to create the type in.

        The keyspace must already exist.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-type.html#cfn-cassandra-type-keyspacename
        '''
        result = self._values.get("keyspace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the user-defined type.

        UDT names must contain 48 characters or less, must begin with an alphabetic character, and can only contain alpha-numeric characters and underscores. Amazon Keyspaces converts upper case characters automatically into lower case characters. For more information, see `Create a user-defined type (UDT) in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/keyspaces-create-udt.html>`_ in the *Amazon Keyspaces Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-type.html#cfn-cassandra-type-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTypeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTypePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTypePropsMixin",
):
    '''The ``CreateType`` operation creates a new user-defined type in the specified keyspace.

    To configure the required permissions, see `Permissions to create a UDT <https://docs.aws.amazon.com/keyspaces/latest/devguide/configure-udt-permissions.html#udt-permissions-create>`_ in the *Amazon Keyspaces Developer Guide* .

    For more information, see `User-defined types (UDTs) <https://docs.aws.amazon.com/keyspaces/latest/devguide/udts.html>`_ in the *Amazon Keyspaces Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-type.html
    :cloudformationResource: AWS::Cassandra::Type
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
        
        cfn_type_props_mixin = cassandra_mixins.CfnTypePropsMixin(cassandra_mixins.CfnTypeMixinProps(
            fields=[cassandra_mixins.CfnTypePropsMixin.FieldProperty(
                field_name="fieldName",
                field_type="fieldType"
            )],
            keyspace_name="keyspaceName",
            type_name="typeName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Cassandra::Type``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09f06ea55b09d84741473867cafc19db3b494a2a2b0abcda8f9062f4c751aa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9854a6be8ecbfbfb850c3fc93c60d6c4870d5d5ea51d1445bf0613e748a11b6e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4113ea30950879723bd358b49f663c6bc546efdc69783df7d0574dbaa2504a5b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTypeMixinProps:
        return typing.cast(CfnTypeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cassandra.mixins.CfnTypePropsMixin.FieldProperty",
        jsii_struct_bases=[],
        name_mapping={"field_name": "fieldName", "field_type": "fieldType"},
    )
    class FieldProperty:
        def __init__(
            self,
            *,
            field_name: typing.Optional[builtins.str] = None,
            field_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name and data type of an individual field in a user-defined type (UDT).

            In addition to a Cassandra data type, you can also use another UDT. When you nest another UDT or collection data type, you have to declare them with the ``FROZEN`` keyword.

            :param field_name: The name of the field.
            :param field_type: The data type of the field. This can be any Cassandra data type or another user-defined type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-type-field.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cassandra import mixins as cassandra_mixins
                
                field_property = cassandra_mixins.CfnTypePropsMixin.FieldProperty(
                    field_name="fieldName",
                    field_type="fieldType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49bbcc48eca44671230b41cd5707255577f284c24224c16d932457a94ed4352a)
                check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
                check_type(argname="argument field_type", value=field_type, expected_type=type_hints["field_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_name is not None:
                self._values["field_name"] = field_name
            if field_type is not None:
                self._values["field_type"] = field_type

        @builtins.property
        def field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-type-field.html#cfn-cassandra-type-field-fieldname
            '''
            result = self._values.get("field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_type(self) -> typing.Optional[builtins.str]:
            '''The data type of the field.

            This can be any Cassandra data type or another user-defined type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-type-field.html#cfn-cassandra-type-field-fieldtype
            '''
            result = self._values.get("field_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnKeyspaceMixinProps",
    "CfnKeyspacePropsMixin",
    "CfnTableMixinProps",
    "CfnTablePropsMixin",
    "CfnTypeMixinProps",
    "CfnTypePropsMixin",
]

publication.publish()

def _typecheckingstub__ec109fb71330fc944d650ac725ffabb5499f94b6f55089ab9df1635479a4da3b(
    *,
    client_side_timestamps_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    keyspace_name: typing.Optional[builtins.str] = None,
    replication_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKeyspacePropsMixin.ReplicationSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22242a23f803a0b495e4ba2e0b3b374d60e659b1a145678a60f282b25379720(
    props: typing.Union[CfnKeyspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8c39b893c0d347cd709ebee5c006a1b0b347661fe1d273d024e19ca9b0147f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c45081e7dff15382495c97f9abd9b5e2c62095edff0e8e8e917e71f0effc455(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41520c21d5ee728afb617db1fcc8e1630b668ed448d90d8c71d4d004dc530f4(
    *,
    region_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be147112a4b0711b10c7857d2399a8dae2b1f21bb41a3d3f6e812c863bcab6f(
    *,
    auto_scaling_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.AutoScalingSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    billing_mode: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.BillingModeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cdc_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.CdcSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    client_side_timestamps_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    clustering_key_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ClusteringKeyColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    default_time_to_live: typing.Optional[jsii.Number] = None,
    encryption_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.EncryptionSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    keyspace_name: typing.Optional[builtins.str] = None,
    partition_key_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    regular_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    replica_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ReplicaSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    warm_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.WarmThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494fa64445f1d3521f9c663e9115f20fd5643d6636b4131477c7004156bbeacd(
    props: typing.Union[CfnTableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f61941ca12919a70111d679b87aaaf62270df5d6606837ac38de506270e07f7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0635a37d22038b0371127d02c0e91308edcdc3a7a572360cf0614c3b03fbd67b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9597a892072f4e6a4e2ebd8c077a92049b2599bc409114f32e6ffcf629617022(
    *,
    auto_scaling_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    maximum_units: typing.Optional[jsii.Number] = None,
    minimum_units: typing.Optional[jsii.Number] = None,
    scaling_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ScalingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3c1ff5ad399d59340b8c65fee52dab7e330bb96b2a13300d1ea8033a383f02(
    *,
    read_capacity_auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.AutoScalingSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    write_capacity_auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.AutoScalingSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba504e3d4001995c98f08f6116fe87339e79cf19c11361da376dd71d162d1f28(
    *,
    mode: typing.Optional[builtins.str] = None,
    provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdd26b678ab8cc3385ae9a3eca71f461e37c443acc651f482bf784b606ef768(
    *,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    view_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f8ec6265fefe8cb447901c8317abf928852b7465cf6ade386d059a34032502(
    *,
    column: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ColumnProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    order_by: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab99ec8c1315593a714a4c933f1d9ec93659c90cad8c5ea7bb60e08055d1ccb(
    *,
    column_name: typing.Optional[builtins.str] = None,
    column_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e07bc27246ae7acaea664d848e7cfa7024bd1e20689841b9531b6d03f7c3884(
    *,
    encryption_type: typing.Optional[builtins.str] = None,
    kms_key_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72024675d0d3fca8a426c5a4e4abd8c092ac5bfd0f1da37f731b6ede3eb1135b(
    *,
    read_capacity_units: typing.Optional[jsii.Number] = None,
    write_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34615fc032b5a73ab65641451cbc8d02d1ff105be1ae35dc37843ad190b65f6(
    *,
    read_capacity_auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.AutoScalingSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    read_capacity_units: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a414de0fe93167f406254b8a176c48c92004308ccdc1fdfb798f4f03a3d87be(
    *,
    target_tracking_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aadb89f4279fe95f874982fd1c79af2ff369f48232e774b9fba34a7ed4df4f32(
    *,
    disable_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    scale_in_cooldown: typing.Optional[jsii.Number] = None,
    scale_out_cooldown: typing.Optional[jsii.Number] = None,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44d95084edd1b63b29f19bb7375b827ff5c9426d8b374ae92105b15766094c3(
    *,
    read_units_per_second: typing.Optional[jsii.Number] = None,
    write_units_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1c7cf942933345f3b9ff7058e102e997eb03e1306f26c193060c7194d539ae(
    *,
    fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTypePropsMixin.FieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    keyspace_name: typing.Optional[builtins.str] = None,
    type_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09f06ea55b09d84741473867cafc19db3b494a2a2b0abcda8f9062f4c751aa2(
    props: typing.Union[CfnTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9854a6be8ecbfbfb850c3fc93c60d6c4870d5d5ea51d1445bf0613e748a11b6e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4113ea30950879723bd358b49f663c6bc546efdc69783df7d0574dbaa2504a5b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49bbcc48eca44671230b41cd5707255577f284c24224c16d932457a94ed4352a(
    *,
    field_name: typing.Optional[builtins.str] = None,
    field_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
