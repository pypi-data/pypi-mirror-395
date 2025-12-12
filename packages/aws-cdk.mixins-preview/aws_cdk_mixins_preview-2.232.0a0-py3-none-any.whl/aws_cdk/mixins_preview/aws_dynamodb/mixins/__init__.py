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
    jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_definitions": "attributeDefinitions",
        "billing_mode": "billingMode",
        "global_secondary_indexes": "globalSecondaryIndexes",
        "global_table_witnesses": "globalTableWitnesses",
        "key_schema": "keySchema",
        "local_secondary_indexes": "localSecondaryIndexes",
        "multi_region_consistency": "multiRegionConsistency",
        "replicas": "replicas",
        "sse_specification": "sseSpecification",
        "stream_specification": "streamSpecification",
        "table_name": "tableName",
        "time_to_live_specification": "timeToLiveSpecification",
        "warm_throughput": "warmThroughput",
        "write_on_demand_throughput_settings": "writeOnDemandThroughputSettings",
        "write_provisioned_throughput_settings": "writeProvisionedThroughputSettings",
    },
)
class CfnGlobalTableMixinProps:
    def __init__(
        self,
        *,
        attribute_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.AttributeDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        billing_mode: typing.Optional[builtins.str] = None,
        global_secondary_indexes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.GlobalSecondaryIndexProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        global_table_witnesses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.GlobalTableWitnessProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        local_secondary_indexes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.LocalSecondaryIndexProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        multi_region_consistency: typing.Optional[builtins.str] = None,
        replicas: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ReplicaSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        sse_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.SSESpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stream_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.StreamSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_name: typing.Optional[builtins.str] = None,
        time_to_live_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.TimeToLiveSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        warm_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.WarmThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        write_on_demand_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        write_provisioned_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGlobalTablePropsMixin.

        :param attribute_definitions: A list of attributes that describe the key schema for the global table and indexes.
        :param billing_mode: Specifies how you are charged for read and write throughput and how you manage capacity. Valid values are:. - ``PAY_PER_REQUEST`` - ``PROVISIONED`` All replicas in your global table will have the same billing mode. If you use ``PROVISIONED`` billing mode, you must provide an auto scaling configuration via the ``WriteProvisionedThroughputSettings`` property. The default value of this property is ``PROVISIONED`` .
        :param global_secondary_indexes: Global secondary indexes to be created on the global table. You can create up to 20 global secondary indexes. Each replica in your global table will have the same global secondary index settings. You can only create or delete one global secondary index in a single stack operation. Since the backfilling of an index could take a long time, CloudFormation does not wait for the index to become active. If a stack operation rolls back, CloudFormation might not delete an index that has been added. In that case, you will need to delete the index manually.
        :param global_table_witnesses: The list of witnesses of the MRSC global table. Only one witness Region can be configured per MRSC global table.
        :param key_schema: Specifies the attributes that make up the primary key for the table. The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.
        :param local_secondary_indexes: Local secondary indexes to be created on the table. You can create up to five local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes. Each replica in your global table will have the same local secondary index settings.
        :param multi_region_consistency: Specifies the consistency mode for a new global table. You can specify one of the following consistency modes: - ``EVENTUAL`` : Configures a new global table for multi-Region eventual consistency (MREC). - ``STRONG`` : Configures a new global table for multi-Region strong consistency (MRSC). If you don't specify this field, the global table consistency mode defaults to ``EVENTUAL`` . For more information about global tables consistency modes, see `Consistency modes <https://docs.aws.amazon.com/V2globaltables_HowItWorks.html#V2globaltables_HowItWorks.consistency-modes>`_ in DynamoDB developer guide.
        :param replicas: Specifies the list of replicas for your global table. The list must contain at least one element, the region where the stack defining the global table is deployed. For example, if you define your table in a stack deployed to us-east-1, you must have an entry in ``Replicas`` with the region us-east-1. You cannot remove the replica in the stack region. .. epigraph:: Adding a replica might take a few minutes for an empty table, or up to several hours for large tables. If you want to add or remove a replica, we recommend submitting an ``UpdateStack`` operation containing only that change. If you add or delete a replica during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new replica, you might need to manually delete the replica. You can create a new global table with as many replicas as needed. You can add or remove replicas after table creation, but you can only add or remove a single replica in each update. For Multi-Region Strong Consistency (MRSC), you can add or remove up to 3 replicas, or 2 replicas plus a witness Region.
        :param sse_specification: Specifies the settings to enable server-side encryption. These settings will be applied to all replicas. If you plan to use customer-managed KMS keys, you must provide a key for each replica using the ``ReplicaSpecification.ReplicaSSESpecification`` property.
        :param stream_specification: Specifies the streams settings on your global table. You must provide a value for this property if your global table contains more than one replica. You can only change the streams settings if your global table has only one replica. For Multi-Region Strong Consistency (MRSC), you do not need to provide a value for this property and can change the settings at any time.
        :param table_name: A name for the global table. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID as the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param time_to_live_specification: Specifies the time to live (TTL) settings for the table. This setting will be applied to all replicas.
        :param warm_throughput: Provides visibility into the number of read and write operations your table or secondary index can instantaneously support. The settings can be modified using the ``UpdateTable`` operation to meet the throughput requirements of an upcoming peak event.
        :param write_on_demand_throughput_settings: Sets the write request settings for a global table or a global secondary index. You can only specify this setting if your resource uses the ``PAY_PER_REQUEST`` ``BillingMode`` .
        :param write_provisioned_throughput_settings: Specifies an auto scaling policy for write capacity. This policy will be applied to all replicas. This setting must be specified if ``BillingMode`` is set to ``PROVISIONED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
            
            # policy_document: Any
            
            cfn_global_table_mixin_props = dynamodb_mixins.CfnGlobalTableMixinProps(
                attribute_definitions=[dynamodb_mixins.CfnGlobalTablePropsMixin.AttributeDefinitionProperty(
                    attribute_name="attributeName",
                    attribute_type="attributeType"
                )],
                billing_mode="billingMode",
                global_secondary_indexes=[dynamodb_mixins.CfnGlobalTablePropsMixin.GlobalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb_mixins.CfnGlobalTablePropsMixin.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb_mixins.CfnGlobalTablePropsMixin.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    ),
                    warm_throughput=dynamodb_mixins.CfnGlobalTablePropsMixin.WarmThroughputProperty(
                        read_units_per_second=123,
                        write_units_per_second=123
                    ),
                    write_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty(
                        max_write_request_units=123
                    ),
                    write_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty(
                        write_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            seed_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        )
                    )
                )],
                global_table_witnesses=[dynamodb_mixins.CfnGlobalTablePropsMixin.GlobalTableWitnessProperty(
                    region="region"
                )],
                key_schema=[dynamodb_mixins.CfnGlobalTablePropsMixin.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                local_secondary_indexes=[dynamodb_mixins.CfnGlobalTablePropsMixin.LocalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb_mixins.CfnGlobalTablePropsMixin.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb_mixins.CfnGlobalTablePropsMixin.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    )
                )],
                multi_region_consistency="multiRegionConsistency",
                replicas=[dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaSpecificationProperty(
                    contributor_insights_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty(
                        enabled=False,
                        mode="mode"
                    ),
                    deletion_protection_enabled=False,
                    global_secondary_indexes=[dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaGlobalSecondaryIndexSpecificationProperty(
                        contributor_insights_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty(
                            enabled=False,
                            mode="mode"
                        ),
                        index_name="indexName",
                        read_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty(
                            max_read_request_units=123
                        ),
                        read_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty(
                            read_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                                max_capacity=123,
                                min_capacity=123,
                                seed_capacity=123,
                                target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                    disable_scale_in=False,
                                    scale_in_cooldown=123,
                                    scale_out_cooldown=123,
                                    target_value=123
                                )
                            ),
                            read_capacity_units=123
                        )
                    )],
                    kinesis_stream_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.KinesisStreamSpecificationProperty(
                        approximate_creation_date_time_precision="approximateCreationDateTimePrecision",
                        stream_arn="streamArn"
                    ),
                    point_in_time_recovery_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.PointInTimeRecoverySpecificationProperty(
                        point_in_time_recovery_enabled=False,
                        recovery_period_in_days=123
                    ),
                    read_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty(
                        max_read_request_units=123
                    ),
                    read_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty(
                        read_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            seed_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        ),
                        read_capacity_units=123
                    ),
                    region="region",
                    replica_stream_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaStreamSpecificationProperty(
                        resource_policy=dynamodb_mixins.CfnGlobalTablePropsMixin.ResourcePolicyProperty(
                            policy_document=policy_document
                        )
                    ),
                    resource_policy=dynamodb_mixins.CfnGlobalTablePropsMixin.ResourcePolicyProperty(
                        policy_document=policy_document
                    ),
                    sse_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaSSESpecificationProperty(
                        kms_master_key_id="kmsMasterKeyId"
                    ),
                    table_class="tableClass",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                sse_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.SSESpecificationProperty(
                    sse_enabled=False,
                    sse_type="sseType"
                ),
                stream_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.StreamSpecificationProperty(
                    stream_view_type="streamViewType"
                ),
                table_name="tableName",
                time_to_live_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.TimeToLiveSpecificationProperty(
                    attribute_name="attributeName",
                    enabled=False
                ),
                warm_throughput=dynamodb_mixins.CfnGlobalTablePropsMixin.WarmThroughputProperty(
                    read_units_per_second=123,
                    write_units_per_second=123
                ),
                write_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty(
                    max_write_request_units=123
                ),
                write_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty(
                    write_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                        max_capacity=123,
                        min_capacity=123,
                        seed_capacity=123,
                        target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a529924f192b1a70167f8c6f33b8112dc78c264381cbfcae636dc03c938367e)
            check_type(argname="argument attribute_definitions", value=attribute_definitions, expected_type=type_hints["attribute_definitions"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument global_secondary_indexes", value=global_secondary_indexes, expected_type=type_hints["global_secondary_indexes"])
            check_type(argname="argument global_table_witnesses", value=global_table_witnesses, expected_type=type_hints["global_table_witnesses"])
            check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
            check_type(argname="argument local_secondary_indexes", value=local_secondary_indexes, expected_type=type_hints["local_secondary_indexes"])
            check_type(argname="argument multi_region_consistency", value=multi_region_consistency, expected_type=type_hints["multi_region_consistency"])
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
            check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
            check_type(argname="argument stream_specification", value=stream_specification, expected_type=type_hints["stream_specification"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument time_to_live_specification", value=time_to_live_specification, expected_type=type_hints["time_to_live_specification"])
            check_type(argname="argument warm_throughput", value=warm_throughput, expected_type=type_hints["warm_throughput"])
            check_type(argname="argument write_on_demand_throughput_settings", value=write_on_demand_throughput_settings, expected_type=type_hints["write_on_demand_throughput_settings"])
            check_type(argname="argument write_provisioned_throughput_settings", value=write_provisioned_throughput_settings, expected_type=type_hints["write_provisioned_throughput_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_definitions is not None:
            self._values["attribute_definitions"] = attribute_definitions
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if global_secondary_indexes is not None:
            self._values["global_secondary_indexes"] = global_secondary_indexes
        if global_table_witnesses is not None:
            self._values["global_table_witnesses"] = global_table_witnesses
        if key_schema is not None:
            self._values["key_schema"] = key_schema
        if local_secondary_indexes is not None:
            self._values["local_secondary_indexes"] = local_secondary_indexes
        if multi_region_consistency is not None:
            self._values["multi_region_consistency"] = multi_region_consistency
        if replicas is not None:
            self._values["replicas"] = replicas
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if stream_specification is not None:
            self._values["stream_specification"] = stream_specification
        if table_name is not None:
            self._values["table_name"] = table_name
        if time_to_live_specification is not None:
            self._values["time_to_live_specification"] = time_to_live_specification
        if warm_throughput is not None:
            self._values["warm_throughput"] = warm_throughput
        if write_on_demand_throughput_settings is not None:
            self._values["write_on_demand_throughput_settings"] = write_on_demand_throughput_settings
        if write_provisioned_throughput_settings is not None:
            self._values["write_provisioned_throughput_settings"] = write_provisioned_throughput_settings

    @builtins.property
    def attribute_definitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.AttributeDefinitionProperty"]]]]:
        '''A list of attributes that describe the key schema for the global table and indexes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-attributedefinitions
        '''
        result = self._values.get("attribute_definitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.AttributeDefinitionProperty"]]]], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies how you are charged for read and write throughput and how you manage capacity. Valid values are:.

        - ``PAY_PER_REQUEST``
        - ``PROVISIONED``

        All replicas in your global table will have the same billing mode. If you use ``PROVISIONED`` billing mode, you must provide an auto scaling configuration via the ``WriteProvisionedThroughputSettings`` property. The default value of this property is ``PROVISIONED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-billingmode
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.GlobalSecondaryIndexProperty"]]]]:
        '''Global secondary indexes to be created on the global table.

        You can create up to 20 global secondary indexes. Each replica in your global table will have the same global secondary index settings. You can only create or delete one global secondary index in a single stack operation.

        Since the backfilling of an index could take a long time, CloudFormation does not wait for the index to become active. If a stack operation rolls back, CloudFormation might not delete an index that has been added. In that case, you will need to delete the index manually.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-globalsecondaryindexes
        '''
        result = self._values.get("global_secondary_indexes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.GlobalSecondaryIndexProperty"]]]], result)

    @builtins.property
    def global_table_witnesses(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.GlobalTableWitnessProperty"]]]]:
        '''The list of witnesses of the MRSC global table.

        Only one witness Region can be configured per MRSC global table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-globaltablewitnesses
        '''
        result = self._values.get("global_table_witnesses")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.GlobalTableWitnessProperty"]]]], result)

    @builtins.property
    def key_schema(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.KeySchemaProperty"]]]]:
        '''Specifies the attributes that make up the primary key for the table.

        The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-keyschema
        '''
        result = self._values.get("key_schema")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.KeySchemaProperty"]]]], result)

    @builtins.property
    def local_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.LocalSecondaryIndexProperty"]]]]:
        '''Local secondary indexes to be created on the table.

        You can create up to five local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes. Each replica in your global table will have the same local secondary index settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-localsecondaryindexes
        '''
        result = self._values.get("local_secondary_indexes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.LocalSecondaryIndexProperty"]]]], result)

    @builtins.property
    def multi_region_consistency(self) -> typing.Optional[builtins.str]:
        '''Specifies the consistency mode for a new global table.

        You can specify one of the following consistency modes:

        - ``EVENTUAL`` : Configures a new global table for multi-Region eventual consistency (MREC).
        - ``STRONG`` : Configures a new global table for multi-Region strong consistency (MRSC).

        If you don't specify this field, the global table consistency mode defaults to ``EVENTUAL`` . For more information about global tables consistency modes, see `Consistency modes <https://docs.aws.amazon.com/V2globaltables_HowItWorks.html#V2globaltables_HowItWorks.consistency-modes>`_ in DynamoDB developer guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-multiregionconsistency
        '''
        result = self._values.get("multi_region_consistency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replicas(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReplicaSpecificationProperty"]]]]:
        '''Specifies the list of replicas for your global table.

        The list must contain at least one element, the region where the stack defining the global table is deployed. For example, if you define your table in a stack deployed to us-east-1, you must have an entry in ``Replicas`` with the region us-east-1. You cannot remove the replica in the stack region.
        .. epigraph::

           Adding a replica might take a few minutes for an empty table, or up to several hours for large tables. If you want to add or remove a replica, we recommend submitting an ``UpdateStack`` operation containing only that change.

           If you add or delete a replica during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new replica, you might need to manually delete the replica.

        You can create a new global table with as many replicas as needed. You can add or remove replicas after table creation, but you can only add or remove a single replica in each update. For Multi-Region Strong Consistency (MRSC), you can add or remove up to 3 replicas, or 2 replicas plus a witness Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-replicas
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReplicaSpecificationProperty"]]]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.SSESpecificationProperty"]]:
        '''Specifies the settings to enable server-side encryption.

        These settings will be applied to all replicas. If you plan to use customer-managed KMS keys, you must provide a key for each replica using the ``ReplicaSpecification.ReplicaSSESpecification`` property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-ssespecification
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.SSESpecificationProperty"]], result)

    @builtins.property
    def stream_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.StreamSpecificationProperty"]]:
        '''Specifies the streams settings on your global table.

        You must provide a value for this property if your global table contains more than one replica. You can only change the streams settings if your global table has only one replica. For Multi-Region Strong Consistency (MRSC), you do not need to provide a value for this property and can change the settings at any time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-streamspecification
        '''
        result = self._values.get("stream_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.StreamSpecificationProperty"]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''A name for the global table.

        If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID as the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_to_live_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.TimeToLiveSpecificationProperty"]]:
        '''Specifies the time to live (TTL) settings for the table.

        This setting will be applied to all replicas.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-timetolivespecification
        '''
        result = self._values.get("time_to_live_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.TimeToLiveSpecificationProperty"]], result)

    @builtins.property
    def warm_throughput(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WarmThroughputProperty"]]:
        '''Provides visibility into the number of read and write operations your table or secondary index can instantaneously support.

        The settings can be modified using the ``UpdateTable`` operation to meet the throughput requirements of an upcoming peak event.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-warmthroughput
        '''
        result = self._values.get("warm_throughput")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WarmThroughputProperty"]], result)

    @builtins.property
    def write_on_demand_throughput_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty"]]:
        '''Sets the write request settings for a global table or a global secondary index.

        You can only specify this setting if your resource uses the ``PAY_PER_REQUEST`` ``BillingMode`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-writeondemandthroughputsettings
        '''
        result = self._values.get("write_on_demand_throughput_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty"]], result)

    @builtins.property
    def write_provisioned_throughput_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty"]]:
        '''Specifies an auto scaling policy for write capacity.

        This policy will be applied to all replicas. This setting must be specified if ``BillingMode`` is set to ``PROVISIONED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-writeprovisionedthroughputsettings
        '''
        result = self._values.get("write_provisioned_throughput_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGlobalTableMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGlobalTablePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin",
):
    '''The ``AWS::DynamoDB::GlobalTable`` resource enables you to create and manage a Version 2019.11.21 global table. This resource cannot be used to create or manage a Version 2017.11.29 global table. For more information, see `Global tables <https://docs.aws.amazon.com//amazondynamodb/latest/developerguide/GlobalTables.html>`_ .

    .. epigraph::

       You cannot convert a resource of type ``AWS::DynamoDB::Table`` into a resource of type ``AWS::DynamoDB::GlobalTable`` by changing its type in your template. *Doing so might result in the deletion of your DynamoDB table.*

       You can instead use the GlobalTable resource to create a new table in a single Region. This will be billed the same as a single Region table. If you later update the stack to add other Regions then Global Tables pricing will apply.

    You should be aware of the following behaviors when working with DynamoDB global tables.

    - The IAM Principal executing the stack operation must have the permissions listed below in all regions where you plan to have a global table replica. The IAM Principal's permissions should not have restrictions based on IP source address. Some global tables operations (for example, adding a replica) are asynchronous, and require that the IAM Principal is valid until they complete. You should not delete the Principal (user or IAM role) until CloudFormation has finished updating your stack.
    - ``application-autoscaling:DeleteScalingPolicy``
    - ``application-autoscaling:DeleteScheduledAction``
    - ``application-autoscaling:DeregisterScalableTarget``
    - ``application-autoscaling:DescribeScalableTargets``
    - ``application-autoscaling:DescribeScalingPolicies``
    - ``application-autoscaling:PutScalingPolicy``
    - ``application-autoscaling:PutScheduledAction``
    - ``application-autoscaling:RegisterScalableTarget``
    - ``dynamodb:BatchWriteItem``
    - ``dynamodb:CreateGlobalTableWitness``
    - ``dynamodb:CreateTable``
    - ``dynamodb:CreateTableReplica``
    - ``dynamodb:DeleteGlobalTableWitness``
    - ``dynamodb:DeleteItem``
    - ``dynamodb:DeleteTable``
    - ``dynamodb:DeleteTableReplica``
    - ``dynamodb:DescribeContinuousBackups``
    - ``dynamodb:DescribeContributorInsights``
    - ``dynamodb:DescribeTable``
    - ``dynamodb:DescribeTableReplicaAutoScaling``
    - ``dynamodb:DescribeTimeToLive``
    - ``dynamodb:DisableKinesisStreamingDestination``
    - ``dynamodb:EnableKinesisStreamingDestination``
    - ``dynamodb:GetItem``
    - ``dynamodb:ListTables``
    - ``dynamodb:ListTagsOfResource``
    - ``dynamodb:PutItem``
    - ``dynamodb:Query``
    - ``dynamodb:Scan``
    - ``dynamodb:TagResource``
    - ``dynamodb:UntagResource``
    - ``dynamodb:UpdateContinuousBackups``
    - ``dynamodb:UpdateContributorInsights``
    - ``dynamodb:UpdateItem``
    - ``dynamodb:UpdateTable``
    - ``dynamodb:UpdateTableReplicaAutoScaling``
    - ``dynamodb:UpdateTimeToLive``
    - ``iam:CreateServiceLinkedRole``
    - ``kms:CreateGrant``
    - ``kms:DescribeKey``
    - When using provisioned billing mode, CloudFormation will create an auto scaling policy on each of your replicas to control their write capacities. You must configure this policy using the ``WriteProvisionedThroughputSettings`` property. CloudFormation will ensure that all replicas have the same write capacity auto scaling property. You cannot directly specify a value for write capacity for a global table.
    - If your table uses provisioned capacity, you must configure auto scaling directly in the ``AWS::DynamoDB::GlobalTable`` resource. You should not configure additional auto scaling policies on any of the table replicas or global secondary indexes, either via API or via ``AWS::ApplicationAutoScaling::ScalableTarget`` or ``AWS::ApplicationAutoScaling::ScalingPolicy`` . Doing so might result in unexpected behavior and is unsupported.
    - In AWS CloudFormation , each global table is controlled by a single stack, in a single region, regardless of the number of replicas. When you deploy your template, CloudFormation will create/update all replicas as part of a single stack operation. You should not deploy the same ``AWS::DynamoDB::GlobalTable`` resource in multiple regions. Doing so will result in errors, and is unsupported. If you deploy your application template in multiple regions, you can use conditions to only create the resource in a single region. Alternatively, you can choose to define your ``AWS::DynamoDB::GlobalTable`` resources in a stack separate from your application stack, and make sure it is only deployed to a single region.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html
    :cloudformationResource: AWS::DynamoDB::GlobalTable
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
        
        # policy_document: Any
        
        cfn_global_table_props_mixin = dynamodb_mixins.CfnGlobalTablePropsMixin(dynamodb_mixins.CfnGlobalTableMixinProps(
            attribute_definitions=[dynamodb_mixins.CfnGlobalTablePropsMixin.AttributeDefinitionProperty(
                attribute_name="attributeName",
                attribute_type="attributeType"
            )],
            billing_mode="billingMode",
            global_secondary_indexes=[dynamodb_mixins.CfnGlobalTablePropsMixin.GlobalSecondaryIndexProperty(
                index_name="indexName",
                key_schema=[dynamodb_mixins.CfnGlobalTablePropsMixin.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                projection=dynamodb_mixins.CfnGlobalTablePropsMixin.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                ),
                warm_throughput=dynamodb_mixins.CfnGlobalTablePropsMixin.WarmThroughputProperty(
                    read_units_per_second=123,
                    write_units_per_second=123
                ),
                write_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty(
                    max_write_request_units=123
                ),
                write_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty(
                    write_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                        max_capacity=123,
                        min_capacity=123,
                        seed_capacity=123,
                        target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123,
                            target_value=123
                        )
                    )
                )
            )],
            global_table_witnesses=[dynamodb_mixins.CfnGlobalTablePropsMixin.GlobalTableWitnessProperty(
                region="region"
            )],
            key_schema=[dynamodb_mixins.CfnGlobalTablePropsMixin.KeySchemaProperty(
                attribute_name="attributeName",
                key_type="keyType"
            )],
            local_secondary_indexes=[dynamodb_mixins.CfnGlobalTablePropsMixin.LocalSecondaryIndexProperty(
                index_name="indexName",
                key_schema=[dynamodb_mixins.CfnGlobalTablePropsMixin.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                projection=dynamodb_mixins.CfnGlobalTablePropsMixin.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                )
            )],
            multi_region_consistency="multiRegionConsistency",
            replicas=[dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaSpecificationProperty(
                contributor_insights_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty(
                    enabled=False,
                    mode="mode"
                ),
                deletion_protection_enabled=False,
                global_secondary_indexes=[dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaGlobalSecondaryIndexSpecificationProperty(
                    contributor_insights_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty(
                        enabled=False,
                        mode="mode"
                    ),
                    index_name="indexName",
                    read_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty(
                        max_read_request_units=123
                    ),
                    read_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty(
                        read_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            seed_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        ),
                        read_capacity_units=123
                    )
                )],
                kinesis_stream_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.KinesisStreamSpecificationProperty(
                    approximate_creation_date_time_precision="approximateCreationDateTimePrecision",
                    stream_arn="streamArn"
                ),
                point_in_time_recovery_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.PointInTimeRecoverySpecificationProperty(
                    point_in_time_recovery_enabled=False,
                    recovery_period_in_days=123
                ),
                read_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty(
                    max_read_request_units=123
                ),
                read_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty(
                    read_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                        max_capacity=123,
                        min_capacity=123,
                        seed_capacity=123,
                        target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123,
                            target_value=123
                        )
                    ),
                    read_capacity_units=123
                ),
                region="region",
                replica_stream_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaStreamSpecificationProperty(
                    resource_policy=dynamodb_mixins.CfnGlobalTablePropsMixin.ResourcePolicyProperty(
                        policy_document=policy_document
                    )
                ),
                resource_policy=dynamodb_mixins.CfnGlobalTablePropsMixin.ResourcePolicyProperty(
                    policy_document=policy_document
                ),
                sse_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaSSESpecificationProperty(
                    kms_master_key_id="kmsMasterKeyId"
                ),
                table_class="tableClass",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )],
            sse_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.SSESpecificationProperty(
                sse_enabled=False,
                sse_type="sseType"
            ),
            stream_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.StreamSpecificationProperty(
                stream_view_type="streamViewType"
            ),
            table_name="tableName",
            time_to_live_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.TimeToLiveSpecificationProperty(
                attribute_name="attributeName",
                enabled=False
            ),
            warm_throughput=dynamodb_mixins.CfnGlobalTablePropsMixin.WarmThroughputProperty(
                read_units_per_second=123,
                write_units_per_second=123
            ),
            write_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty(
                max_write_request_units=123
            ),
            write_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty(
                write_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                    max_capacity=123,
                    min_capacity=123,
                    seed_capacity=123,
                    target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                        disable_scale_in=False,
                        scale_in_cooldown=123,
                        scale_out_cooldown=123,
                        target_value=123
                    )
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGlobalTableMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DynamoDB::GlobalTable``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab7e8de4fc74a8bcf8770715be06ab6d9f2d070219ee9884bc638cb007f2d1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99b064a7522a47b5097a2d24437aa4b7444f6e04bf550fe286bfb667703347c6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bcaf9113dda045b083eeb0ba8358b36151ccc8d8567f763648e1dfe67b3adcd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGlobalTableMixinProps:
        return typing.cast(CfnGlobalTableMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.AttributeDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "attribute_type": "attributeType",
        },
    )
    class AttributeDefinitionProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            attribute_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents an attribute for describing the schema for the table and indexes.

            :param attribute_name: A name for the attribute.
            :param attribute_type: The data type for the attribute, where:. - ``S`` - the attribute is of type String - ``N`` - the attribute is of type Number - ``B`` - the attribute is of type Binary

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-attributedefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                attribute_definition_property = dynamodb_mixins.CfnGlobalTablePropsMixin.AttributeDefinitionProperty(
                    attribute_name="attributeName",
                    attribute_type="attributeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__204a72cf6e6dbaa744d9d7f0645bfe47e2a19d4ae49f1a2a1b9051275ee0e09a)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument attribute_type", value=attribute_type, expected_type=type_hints["attribute_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if attribute_type is not None:
                self._values["attribute_type"] = attribute_type

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''A name for the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-attributedefinition.html#cfn-dynamodb-globaltable-attributedefinition-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def attribute_type(self) -> typing.Optional[builtins.str]:
            '''The data type for the attribute, where:.

            - ``S`` - the attribute is of type String
            - ``N`` - the attribute is of type Number
            - ``B`` - the attribute is of type Binary

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-attributedefinition.html#cfn-dynamodb-globaltable-attributedefinition-attributetype
            '''
            result = self._values.get("attribute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_capacity": "maxCapacity",
            "min_capacity": "minCapacity",
            "seed_capacity": "seedCapacity",
            "target_tracking_scaling_policy_configuration": "targetTrackingScalingPolicyConfiguration",
        },
    )
    class CapacityAutoScalingSettingsProperty:
        def __init__(
            self,
            *,
            max_capacity: typing.Optional[jsii.Number] = None,
            min_capacity: typing.Optional[jsii.Number] = None,
            seed_capacity: typing.Optional[jsii.Number] = None,
            target_tracking_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configures a scalable target and an autoscaling policy for a table or global secondary index's read or write capacity.

            :param max_capacity: The maximum provisioned capacity units for the global table.
            :param min_capacity: The minimum provisioned capacity units for the global table.
            :param seed_capacity: When switching billing mode from ``PAY_PER_REQUEST`` to ``PROVISIONED`` , DynamoDB requires you to specify read and write capacity unit values for the table and for each global secondary index. These values will be applied to all replicas. The table will use these provisioned values until CloudFormation creates the autoscaling policies you configured in your template. CloudFormation cannot determine what capacity the table and its global secondary indexes will require in this time period, since they are application-dependent. If you want to switch a table's billing mode from ``PAY_PER_REQUEST`` to ``PROVISIONED`` , you must specify a value for this property for each autoscaled resource. If you specify different values for the same resource in different regions, CloudFormation will use the highest value found in either the ``SeedCapacity`` or ``ReadCapacityUnits`` properties. For example, if your global secondary index ``myGSI`` has a ``SeedCapacity`` of 10 in us-east-1 and a fixed ``ReadCapacityUnits`` of 20 in eu-west-1, CloudFormation will initially set the read capacity for ``myGSI`` to 20. Note that if you disable ``ScaleIn`` for ``myGSI`` in us-east-1, its read capacity units might not be set back to 10. You must also specify a value for ``SeedCapacity`` when you plan to switch a table's billing mode from ``PROVISIONED`` to ``PAY_PER_REQUEST`` , because CloudFormation might need to roll back the operation (reverting the billing mode to ``PROVISIONED`` ) and this cannot succeed without specifying a value for ``SeedCapacity`` .
            :param target_tracking_scaling_policy_configuration: Defines a target tracking scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-capacityautoscalingsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                capacity_auto_scaling_settings_property = dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                    max_capacity=123,
                    min_capacity=123,
                    seed_capacity=123,
                    target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                        disable_scale_in=False,
                        scale_in_cooldown=123,
                        scale_out_cooldown=123,
                        target_value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c051f75cad5170a2ba829b2b85a80a32cdfbbee12635853a7c0a88a9a9ee5841)
                check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
                check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
                check_type(argname="argument seed_capacity", value=seed_capacity, expected_type=type_hints["seed_capacity"])
                check_type(argname="argument target_tracking_scaling_policy_configuration", value=target_tracking_scaling_policy_configuration, expected_type=type_hints["target_tracking_scaling_policy_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_capacity is not None:
                self._values["max_capacity"] = max_capacity
            if min_capacity is not None:
                self._values["min_capacity"] = min_capacity
            if seed_capacity is not None:
                self._values["seed_capacity"] = seed_capacity
            if target_tracking_scaling_policy_configuration is not None:
                self._values["target_tracking_scaling_policy_configuration"] = target_tracking_scaling_policy_configuration

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            '''The maximum provisioned capacity units for the global table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-capacityautoscalingsettings.html#cfn-dynamodb-globaltable-capacityautoscalingsettings-maxcapacity
            '''
            result = self._values.get("max_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_capacity(self) -> typing.Optional[jsii.Number]:
            '''The minimum provisioned capacity units for the global table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-capacityautoscalingsettings.html#cfn-dynamodb-globaltable-capacityautoscalingsettings-mincapacity
            '''
            result = self._values.get("min_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def seed_capacity(self) -> typing.Optional[jsii.Number]:
            '''When switching billing mode from ``PAY_PER_REQUEST`` to ``PROVISIONED`` , DynamoDB requires you to specify read and write capacity unit values for the table and for each global secondary index.

            These values will be applied to all replicas. The table will use these provisioned values until CloudFormation creates the autoscaling policies you configured in your template. CloudFormation cannot determine what capacity the table and its global secondary indexes will require in this time period, since they are application-dependent.

            If you want to switch a table's billing mode from ``PAY_PER_REQUEST`` to ``PROVISIONED`` , you must specify a value for this property for each autoscaled resource. If you specify different values for the same resource in different regions, CloudFormation will use the highest value found in either the ``SeedCapacity`` or ``ReadCapacityUnits`` properties. For example, if your global secondary index ``myGSI`` has a ``SeedCapacity`` of 10 in us-east-1 and a fixed ``ReadCapacityUnits`` of 20 in eu-west-1, CloudFormation will initially set the read capacity for ``myGSI`` to 20. Note that if you disable ``ScaleIn`` for ``myGSI`` in us-east-1, its read capacity units might not be set back to 10.

            You must also specify a value for ``SeedCapacity`` when you plan to switch a table's billing mode from ``PROVISIONED`` to ``PAY_PER_REQUEST`` , because CloudFormation might need to roll back the operation (reverting the billing mode to ``PROVISIONED`` ) and this cannot succeed without specifying a value for ``SeedCapacity`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-capacityautoscalingsettings.html#cfn-dynamodb-globaltable-capacityautoscalingsettings-seedcapacity
            '''
            result = self._values.get("seed_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def target_tracking_scaling_policy_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty"]]:
            '''Defines a target tracking scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-capacityautoscalingsettings.html#cfn-dynamodb-globaltable-capacityautoscalingsettings-targettrackingscalingpolicyconfiguration
            '''
            result = self._values.get("target_tracking_scaling_policy_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityAutoScalingSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "mode": "mode"},
    )
    class ContributorInsightsSpecificationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures contributor insights settings for a replica or one of its indexes.

            :param enabled: Indicates whether CloudWatch Contributor Insights are to be enabled (true) or disabled (false).
            :param mode: Specifies the CloudWatch Contributor Insights mode for a global table. Valid values are ``ACCESSED_AND_THROTTLED_KEYS`` (tracks all access and throttled events) or ``THROTTLED_KEYS`` (tracks only throttled events). This setting determines what type of contributor insights data is collected for the global table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-contributorinsightsspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                contributor_insights_specification_property = dynamodb_mixins.CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty(
                    enabled=False,
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c1720689debbdd915fae0ee643675f7868dba2a5e4b01938b225c613df75b0dc)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether CloudWatch Contributor Insights are to be enabled (true) or disabled (false).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-contributorinsightsspecification.html#cfn-dynamodb-globaltable-contributorinsightsspecification-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''Specifies the CloudWatch Contributor Insights mode for a global table.

            Valid values are ``ACCESSED_AND_THROTTLED_KEYS`` (tracks all access and throttled events) or ``THROTTLED_KEYS`` (tracks only throttled events). This setting determines what type of contributor insights data is collected for the global table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-contributorinsightsspecification.html#cfn-dynamodb-globaltable-contributorinsightsspecification-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContributorInsightsSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.GlobalSecondaryIndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "key_schema": "keySchema",
            "projection": "projection",
            "warm_throughput": "warmThroughput",
            "write_on_demand_throughput_settings": "writeOnDemandThroughputSettings",
            "write_provisioned_throughput_settings": "writeProvisionedThroughputSettings",
        },
    )
    class GlobalSecondaryIndexProperty:
        def __init__(
            self,
            *,
            index_name: typing.Optional[builtins.str] = None,
            key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            projection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ProjectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            warm_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.WarmThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            write_on_demand_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            write_provisioned_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Allows you to specify a global secondary index for the global table.

            The index will be defined on all replicas.

            :param index_name: The name of the global secondary index. The name must be unique among all other indexes on this table.
            :param key_schema: The complete key schema for a global secondary index, which consists of one or more pairs of attribute names and key types: - ``HASH`` - partition key - ``RANGE`` - sort key > The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. .. epigraph:: The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.
            :param projection: Represents attributes that are copied (projected) from the table into the global secondary index. These are in addition to the primary key attributes and index key attributes, which are automatically projected.
            :param warm_throughput: Represents the warm throughput value (in read units per second and write units per second) for the specified secondary index. If you use this parameter, you must specify ``ReadUnitsPerSecond`` , ``WriteUnitsPerSecond`` , or both.
            :param write_on_demand_throughput_settings: Sets the write request settings for a global table or a global secondary index. You can only specify this setting if your resource uses the ``PAY_PER_REQUEST`` ``BillingMode`` .
            :param write_provisioned_throughput_settings: Defines write capacity settings for the global secondary index. You must specify a value for this property if the table's ``BillingMode`` is ``PROVISIONED`` . All replicas will have the same write capacity settings for this global secondary index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                global_secondary_index_property = dynamodb_mixins.CfnGlobalTablePropsMixin.GlobalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb_mixins.CfnGlobalTablePropsMixin.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb_mixins.CfnGlobalTablePropsMixin.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    ),
                    warm_throughput=dynamodb_mixins.CfnGlobalTablePropsMixin.WarmThroughputProperty(
                        read_units_per_second=123,
                        write_units_per_second=123
                    ),
                    write_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty(
                        max_write_request_units=123
                    ),
                    write_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty(
                        write_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            seed_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
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
                type_hints = typing.get_type_hints(_typecheckingstub__9f202db1f26da98bd43b7623c9ff69995cfd62a67be10cac01d011b8bb481e46)
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
                check_type(argname="argument projection", value=projection, expected_type=type_hints["projection"])
                check_type(argname="argument warm_throughput", value=warm_throughput, expected_type=type_hints["warm_throughput"])
                check_type(argname="argument write_on_demand_throughput_settings", value=write_on_demand_throughput_settings, expected_type=type_hints["write_on_demand_throughput_settings"])
                check_type(argname="argument write_provisioned_throughput_settings", value=write_provisioned_throughput_settings, expected_type=type_hints["write_provisioned_throughput_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if index_name is not None:
                self._values["index_name"] = index_name
            if key_schema is not None:
                self._values["key_schema"] = key_schema
            if projection is not None:
                self._values["projection"] = projection
            if warm_throughput is not None:
                self._values["warm_throughput"] = warm_throughput
            if write_on_demand_throughput_settings is not None:
                self._values["write_on_demand_throughput_settings"] = write_on_demand_throughput_settings
            if write_provisioned_throughput_settings is not None:
                self._values["write_provisioned_throughput_settings"] = write_provisioned_throughput_settings

        @builtins.property
        def index_name(self) -> typing.Optional[builtins.str]:
            '''The name of the global secondary index.

            The name must be unique among all other indexes on this table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html#cfn-dynamodb-globaltable-globalsecondaryindex-indexname
            '''
            result = self._values.get("index_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.KeySchemaProperty"]]]]:
            '''The complete key schema for a global secondary index, which consists of one or more pairs of attribute names and key types:  - ``HASH`` - partition key - ``RANGE`` - sort key  > The partition key of an item is also known as its *hash attribute* .

            The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.
            .. epigraph::

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html#cfn-dynamodb-globaltable-globalsecondaryindex-keyschema
            '''
            result = self._values.get("key_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.KeySchemaProperty"]]]], result)

        @builtins.property
        def projection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ProjectionProperty"]]:
            '''Represents attributes that are copied (projected) from the table into the global secondary index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html#cfn-dynamodb-globaltable-globalsecondaryindex-projection
            '''
            result = self._values.get("projection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ProjectionProperty"]], result)

        @builtins.property
        def warm_throughput(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WarmThroughputProperty"]]:
            '''Represents the warm throughput value (in read units per second and write units per second) for the specified secondary index.

            If you use this parameter, you must specify ``ReadUnitsPerSecond`` , ``WriteUnitsPerSecond`` , or both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html#cfn-dynamodb-globaltable-globalsecondaryindex-warmthroughput
            '''
            result = self._values.get("warm_throughput")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WarmThroughputProperty"]], result)

        @builtins.property
        def write_on_demand_throughput_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty"]]:
            '''Sets the write request settings for a global table or a global secondary index.

            You can only specify this setting if your resource uses the ``PAY_PER_REQUEST`` ``BillingMode`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html#cfn-dynamodb-globaltable-globalsecondaryindex-writeondemandthroughputsettings
            '''
            result = self._values.get("write_on_demand_throughput_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty"]], result)

        @builtins.property
        def write_provisioned_throughput_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty"]]:
            '''Defines write capacity settings for the global secondary index.

            You must specify a value for this property if the table's ``BillingMode`` is ``PROVISIONED`` . All replicas will have the same write capacity settings for this global secondary index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html#cfn-dynamodb-globaltable-globalsecondaryindex-writeprovisionedthroughputsettings
            '''
            result = self._values.get("write_provisioned_throughput_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalSecondaryIndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.GlobalTableWitnessProperty",
        jsii_struct_bases=[],
        name_mapping={"region": "region"},
    )
    class GlobalTableWitnessProperty:
        def __init__(self, *, region: typing.Optional[builtins.str] = None) -> None:
            '''The witness Region for the MRSC global table.

            A MRSC global table can be configured with either three replicas, or with two replicas and one witness.

            The witness must be in a different Region than the replicas and within the same Region set:

            - US Region set: US East (N. Virginia), US East (Ohio), US West (Oregon)
            - EU Region set: Europe (Ireland), Europe (London), Europe (Paris), Europe (Frankfurt)
            - AP Region set: Asia Pacific (Tokyo), Asia Pacific (Seoul), Asia Pacific (Osaka)

            :param region: The name of the AWS Region that serves as a witness for the MRSC global table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globaltablewitness.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                global_table_witness_property = dynamodb_mixins.CfnGlobalTablePropsMixin.GlobalTableWitnessProperty(
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d1a193e67d234e6d50719f93e5c29e0a34dda41c47dbce1adf2c79205ba493c)
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS Region that serves as a witness for the MRSC global table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globaltablewitness.html#cfn-dynamodb-globaltable-globaltablewitness-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalTableWitnessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.KeySchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_name": "attributeName", "key_type": "keyType"},
    )
    class KeySchemaProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents *a single element* of a key schema.

            A key schema specifies the attributes that make up the primary key of a table, or the key attributes of an index.

            A ``KeySchemaElement`` represents exactly one attribute of the primary key. For example, a simple primary key would be represented by one ``KeySchemaElement`` (for the partition key). A composite primary key would require one ``KeySchemaElement`` for the partition key, and another ``KeySchemaElement`` for the sort key.

            A ``KeySchemaElement`` must be a scalar, top-level attribute (not a nested attribute). The data type must be one of String, Number, or Binary. The attribute cannot be nested within a List or a Map.

            :param attribute_name: The name of a key attribute.
            :param key_type: The role that this key attribute will assume:. - ``HASH`` - partition key - ``RANGE`` - sort key .. epigraph:: The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-keyschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                key_schema_property = dynamodb_mixins.CfnGlobalTablePropsMixin.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b7c09cc1b5de671e78f61174c63947436bfd361024fbe370f598e301a8201b1d)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if key_type is not None:
                self._values["key_type"] = key_type

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''The name of a key attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-keyschema.html#cfn-dynamodb-globaltable-keyschema-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''The role that this key attribute will assume:.

            - ``HASH`` - partition key
            - ``RANGE`` - sort key

            .. epigraph::

               The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-keyschema.html#cfn-dynamodb-globaltable-keyschema-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeySchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.KinesisStreamSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "approximate_creation_date_time_precision": "approximateCreationDateTimePrecision",
            "stream_arn": "streamArn",
        },
    )
    class KinesisStreamSpecificationProperty:
        def __init__(
            self,
            *,
            approximate_creation_date_time_precision: typing.Optional[builtins.str] = None,
            stream_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Kinesis Data Streams configuration for the specified global table replica.

            :param approximate_creation_date_time_precision: The precision for the time and date that the stream was created.
            :param stream_arn: The ARN for a specific Kinesis data stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-kinesisstreamspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                kinesis_stream_specification_property = dynamodb_mixins.CfnGlobalTablePropsMixin.KinesisStreamSpecificationProperty(
                    approximate_creation_date_time_precision="approximateCreationDateTimePrecision",
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42edeadc55621a666495f7d3bd73b8496227b65289bb241815fc3552c98cec81)
                check_type(argname="argument approximate_creation_date_time_precision", value=approximate_creation_date_time_precision, expected_type=type_hints["approximate_creation_date_time_precision"])
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if approximate_creation_date_time_precision is not None:
                self._values["approximate_creation_date_time_precision"] = approximate_creation_date_time_precision
            if stream_arn is not None:
                self._values["stream_arn"] = stream_arn

        @builtins.property
        def approximate_creation_date_time_precision(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The precision for the time and date that the stream was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-kinesisstreamspecification.html#cfn-dynamodb-globaltable-kinesisstreamspecification-approximatecreationdatetimeprecision
            '''
            result = self._values.get("approximate_creation_date_time_precision")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN for a specific Kinesis data stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-kinesisstreamspecification.html#cfn-dynamodb-globaltable-kinesisstreamspecification-streamarn
            '''
            result = self._values.get("stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.LocalSecondaryIndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "key_schema": "keySchema",
            "projection": "projection",
        },
    )
    class LocalSecondaryIndexProperty:
        def __init__(
            self,
            *,
            index_name: typing.Optional[builtins.str] = None,
            key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            projection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ProjectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the properties of a local secondary index.

            A local secondary index can only be created when its parent table is created.

            :param index_name: The name of the local secondary index. The name must be unique among all other indexes on this table.
            :param key_schema: The complete key schema for the local secondary index, consisting of one or more pairs of attribute names and key types: - ``HASH`` - partition key - ``RANGE`` - sort key > The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. .. epigraph:: The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.
            :param projection: Represents attributes that are copied (projected) from the table into the local secondary index. These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-localsecondaryindex.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                local_secondary_index_property = dynamodb_mixins.CfnGlobalTablePropsMixin.LocalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb_mixins.CfnGlobalTablePropsMixin.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb_mixins.CfnGlobalTablePropsMixin.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36983d83385e7964ba443990785b94ba16270dc90874f9f1169a60ec674c9d2a)
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
                check_type(argname="argument projection", value=projection, expected_type=type_hints["projection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if index_name is not None:
                self._values["index_name"] = index_name
            if key_schema is not None:
                self._values["key_schema"] = key_schema
            if projection is not None:
                self._values["projection"] = projection

        @builtins.property
        def index_name(self) -> typing.Optional[builtins.str]:
            '''The name of the local secondary index.

            The name must be unique among all other indexes on this table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-localsecondaryindex.html#cfn-dynamodb-globaltable-localsecondaryindex-indexname
            '''
            result = self._values.get("index_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.KeySchemaProperty"]]]]:
            '''The complete key schema for the local secondary index, consisting of one or more pairs of attribute names and key types:  - ``HASH`` - partition key - ``RANGE`` - sort key  > The partition key of an item is also known as its *hash attribute* .

            The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.
            .. epigraph::

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-localsecondaryindex.html#cfn-dynamodb-globaltable-localsecondaryindex-keyschema
            '''
            result = self._values.get("key_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.KeySchemaProperty"]]]], result)

        @builtins.property
        def projection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ProjectionProperty"]]:
            '''Represents attributes that are copied (projected) from the table into the local secondary index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-localsecondaryindex.html#cfn-dynamodb-globaltable-localsecondaryindex-projection
            '''
            result = self._values.get("projection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ProjectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalSecondaryIndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.PointInTimeRecoverySpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "point_in_time_recovery_enabled": "pointInTimeRecoveryEnabled",
            "recovery_period_in_days": "recoveryPeriodInDays",
        },
    )
    class PointInTimeRecoverySpecificationProperty:
        def __init__(
            self,
            *,
            point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            recovery_period_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Represents the settings used to enable point in time recovery.

            :param point_in_time_recovery_enabled: Indicates whether point in time recovery is enabled (true) or disabled (false) on the table.
            :param recovery_period_in_days: The number of preceding days for which continuous backups are taken and maintained. Your table data is only recoverable to any point-in-time from within the configured recovery period. This parameter is optional. If no value is provided, the value will default to 35.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-pointintimerecoveryspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                point_in_time_recovery_specification_property = dynamodb_mixins.CfnGlobalTablePropsMixin.PointInTimeRecoverySpecificationProperty(
                    point_in_time_recovery_enabled=False,
                    recovery_period_in_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a18e14874b35a241ccfc1307e08ca6c43d4055c4fa97736919a2afd740abb8f4)
                check_type(argname="argument point_in_time_recovery_enabled", value=point_in_time_recovery_enabled, expected_type=type_hints["point_in_time_recovery_enabled"])
                check_type(argname="argument recovery_period_in_days", value=recovery_period_in_days, expected_type=type_hints["recovery_period_in_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if point_in_time_recovery_enabled is not None:
                self._values["point_in_time_recovery_enabled"] = point_in_time_recovery_enabled
            if recovery_period_in_days is not None:
                self._values["recovery_period_in_days"] = recovery_period_in_days

        @builtins.property
        def point_in_time_recovery_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether point in time recovery is enabled (true) or disabled (false) on the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-pointintimerecoveryspecification.html#cfn-dynamodb-globaltable-pointintimerecoveryspecification-pointintimerecoveryenabled
            '''
            result = self._values.get("point_in_time_recovery_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def recovery_period_in_days(self) -> typing.Optional[jsii.Number]:
            '''The number of preceding days for which continuous backups are taken and maintained.

            Your table data is only recoverable to any point-in-time from within the configured recovery period. This parameter is optional. If no value is provided, the value will default to 35.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-pointintimerecoveryspecification.html#cfn-dynamodb-globaltable-pointintimerecoveryspecification-recoveryperiodindays
            '''
            result = self._values.get("recovery_period_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PointInTimeRecoverySpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.ProjectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "non_key_attributes": "nonKeyAttributes",
            "projection_type": "projectionType",
        },
    )
    class ProjectionProperty:
        def __init__(
            self,
            *,
            non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
            projection_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents attributes that are copied (projected) from the table into an index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :param non_key_attributes: Represents the non-key attribute names which will be projected into the index. For global and local secondary indexes, the total count of ``NonKeyAttributes`` summed across all of the secondary indexes, must not exceed 100. If you project the same attribute into two different indexes, this counts as two distinct attributes when determining the total. This limit only applies when you specify the ProjectionType of ``INCLUDE`` . You still can specify the ProjectionType of ``ALL`` to project all attributes from the source table, even if the table has more than 100 attributes.
            :param projection_type: The set of attributes that are projected into the index:. - ``KEYS_ONLY`` - Only the index and primary keys are projected into the index. - ``INCLUDE`` - In addition to the attributes described in ``KEYS_ONLY`` , the secondary index will include other non-key attributes that you specify. - ``ALL`` - All of the table attributes are projected into the index. When using the DynamoDB console, ``ALL`` is selected by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-projection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                projection_property = dynamodb_mixins.CfnGlobalTablePropsMixin.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2566d939cb91c39cdb451bec80c2dc379522559b1bd0b8ed906fb8a7bd089ad7)
                check_type(argname="argument non_key_attributes", value=non_key_attributes, expected_type=type_hints["non_key_attributes"])
                check_type(argname="argument projection_type", value=projection_type, expected_type=type_hints["projection_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if non_key_attributes is not None:
                self._values["non_key_attributes"] = non_key_attributes
            if projection_type is not None:
                self._values["projection_type"] = projection_type

        @builtins.property
        def non_key_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents the non-key attribute names which will be projected into the index.

            For global and local secondary indexes, the total count of ``NonKeyAttributes`` summed across all of the secondary indexes, must not exceed 100. If you project the same attribute into two different indexes, this counts as two distinct attributes when determining the total. This limit only applies when you specify the ProjectionType of ``INCLUDE`` . You still can specify the ProjectionType of ``ALL`` to project all attributes from the source table, even if the table has more than 100 attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-projection.html#cfn-dynamodb-globaltable-projection-nonkeyattributes
            '''
            result = self._values.get("non_key_attributes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def projection_type(self) -> typing.Optional[builtins.str]:
            '''The set of attributes that are projected into the index:.

            - ``KEYS_ONLY`` - Only the index and primary keys are projected into the index.
            - ``INCLUDE`` - In addition to the attributes described in ``KEYS_ONLY`` , the secondary index will include other non-key attributes that you specify.
            - ``ALL`` - All of the table attributes are projected into the index.

            When using the DynamoDB console, ``ALL`` is selected by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-projection.html#cfn-dynamodb-globaltable-projection-projectiontype
            '''
            result = self._values.get("projection_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"max_read_request_units": "maxReadRequestUnits"},
    )
    class ReadOnDemandThroughputSettingsProperty:
        def __init__(
            self,
            *,
            max_read_request_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Sets the read request settings for a replica table or a replica global secondary index.

            You can only specify this setting if your resource uses the ``PAY_PER_REQUEST`` ``BillingMode`` .

            :param max_read_request_units: Maximum number of read request units for the specified replica of a global table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-readondemandthroughputsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                read_on_demand_throughput_settings_property = dynamodb_mixins.CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty(
                    max_read_request_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f200eb9addeed59699ee79e3f5fedb3b577e55d50c8d84b2225d2ba23e3e095)
                check_type(argname="argument max_read_request_units", value=max_read_request_units, expected_type=type_hints["max_read_request_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_read_request_units is not None:
                self._values["max_read_request_units"] = max_read_request_units

        @builtins.property
        def max_read_request_units(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of read request units for the specified replica of a global table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-readondemandthroughputsettings.html#cfn-dynamodb-globaltable-readondemandthroughputsettings-maxreadrequestunits
            '''
            result = self._values.get("max_read_request_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadOnDemandThroughputSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "read_capacity_auto_scaling_settings": "readCapacityAutoScalingSettings",
            "read_capacity_units": "readCapacityUnits",
        },
    )
    class ReadProvisionedThroughputSettingsProperty:
        def __init__(
            self,
            *,
            read_capacity_auto_scaling_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            read_capacity_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Allows you to specify the read capacity settings for a replica table or a replica global secondary index when the ``BillingMode`` is set to ``PROVISIONED`` .

            You must specify a value for either ``ReadCapacityUnits`` or ``ReadCapacityAutoScalingSettings`` , but not both. You can switch between fixed capacity and auto scaling.

            :param read_capacity_auto_scaling_settings: Specifies auto scaling settings for the replica table or global secondary index.
            :param read_capacity_units: Specifies a fixed read capacity for the replica table or global secondary index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-readprovisionedthroughputsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                read_provisioned_throughput_settings_property = dynamodb_mixins.CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty(
                    read_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                        max_capacity=123,
                        min_capacity=123,
                        seed_capacity=123,
                        target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123,
                            target_value=123
                        )
                    ),
                    read_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__998a788ab936b30ac1ab33129312acad18dbda2183d6e078b11649ca909f2d93)
                check_type(argname="argument read_capacity_auto_scaling_settings", value=read_capacity_auto_scaling_settings, expected_type=type_hints["read_capacity_auto_scaling_settings"])
                check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if read_capacity_auto_scaling_settings is not None:
                self._values["read_capacity_auto_scaling_settings"] = read_capacity_auto_scaling_settings
            if read_capacity_units is not None:
                self._values["read_capacity_units"] = read_capacity_units

        @builtins.property
        def read_capacity_auto_scaling_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty"]]:
            '''Specifies auto scaling settings for the replica table or global secondary index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-readprovisionedthroughputsettings.html#cfn-dynamodb-globaltable-readprovisionedthroughputsettings-readcapacityautoscalingsettings
            '''
            result = self._values.get("read_capacity_auto_scaling_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty"]], result)

        @builtins.property
        def read_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''Specifies a fixed read capacity for the replica table or global secondary index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-readprovisionedthroughputsettings.html#cfn-dynamodb-globaltable-readprovisionedthroughputsettings-readcapacityunits
            '''
            result = self._values.get("read_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadProvisionedThroughputSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.ReplicaGlobalSecondaryIndexSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "contributor_insights_specification": "contributorInsightsSpecification",
            "index_name": "indexName",
            "read_on_demand_throughput_settings": "readOnDemandThroughputSettings",
            "read_provisioned_throughput_settings": "readProvisionedThroughputSettings",
        },
    )
    class ReplicaGlobalSecondaryIndexSpecificationProperty:
        def __init__(
            self,
            *,
            contributor_insights_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            index_name: typing.Optional[builtins.str] = None,
            read_on_demand_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            read_provisioned_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the properties of a global secondary index that can be set on a per-replica basis.

            :param contributor_insights_specification: Updates the status for contributor insights for a specific table or index. CloudWatch Contributor Insights for DynamoDB graphs display the partition key and (if applicable) sort key of frequently accessed items and frequently throttled items in plaintext. If you require the use of AWS Key Management Service (KMS) to encrypt this table’s partition key and sort key data with an AWS managed key or customer managed key, you should not enable CloudWatch Contributor Insights for DynamoDB for this table.
            :param index_name: The name of the global secondary index. The name must be unique among all other indexes on this table.
            :param read_on_demand_throughput_settings: Sets the read request settings for a replica global secondary index. You can only specify this setting if your resource uses the ``PAY_PER_REQUEST`` ``BillingMode`` .
            :param read_provisioned_throughput_settings: Allows you to specify the read capacity settings for a replica global secondary index when the ``BillingMode`` is set to ``PROVISIONED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaglobalsecondaryindexspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                replica_global_secondary_index_specification_property = dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaGlobalSecondaryIndexSpecificationProperty(
                    contributor_insights_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty(
                        enabled=False,
                        mode="mode"
                    ),
                    index_name="indexName",
                    read_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty(
                        max_read_request_units=123
                    ),
                    read_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty(
                        read_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            seed_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        ),
                        read_capacity_units=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6dc86236431dfce98217d97f5021ff40f97dadc3e66a4783b4ce3635af9ee4d)
                check_type(argname="argument contributor_insights_specification", value=contributor_insights_specification, expected_type=type_hints["contributor_insights_specification"])
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument read_on_demand_throughput_settings", value=read_on_demand_throughput_settings, expected_type=type_hints["read_on_demand_throughput_settings"])
                check_type(argname="argument read_provisioned_throughput_settings", value=read_provisioned_throughput_settings, expected_type=type_hints["read_provisioned_throughput_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contributor_insights_specification is not None:
                self._values["contributor_insights_specification"] = contributor_insights_specification
            if index_name is not None:
                self._values["index_name"] = index_name
            if read_on_demand_throughput_settings is not None:
                self._values["read_on_demand_throughput_settings"] = read_on_demand_throughput_settings
            if read_provisioned_throughput_settings is not None:
                self._values["read_provisioned_throughput_settings"] = read_provisioned_throughput_settings

        @builtins.property
        def contributor_insights_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty"]]:
            '''Updates the status for contributor insights for a specific table or index.

            CloudWatch Contributor Insights for DynamoDB graphs display the partition key and (if applicable) sort key of frequently accessed items and frequently throttled items in plaintext. If you require the use of AWS Key Management Service (KMS) to encrypt this table’s partition key and sort key data with an AWS managed key or customer managed key, you should not enable CloudWatch Contributor Insights for DynamoDB for this table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaglobalsecondaryindexspecification.html#cfn-dynamodb-globaltable-replicaglobalsecondaryindexspecification-contributorinsightsspecification
            '''
            result = self._values.get("contributor_insights_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty"]], result)

        @builtins.property
        def index_name(self) -> typing.Optional[builtins.str]:
            '''The name of the global secondary index.

            The name must be unique among all other indexes on this table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaglobalsecondaryindexspecification.html#cfn-dynamodb-globaltable-replicaglobalsecondaryindexspecification-indexname
            '''
            result = self._values.get("index_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_on_demand_throughput_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty"]]:
            '''Sets the read request settings for a replica global secondary index.

            You can only specify this setting if your resource uses the ``PAY_PER_REQUEST`` ``BillingMode`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaglobalsecondaryindexspecification.html#cfn-dynamodb-globaltable-replicaglobalsecondaryindexspecification-readondemandthroughputsettings
            '''
            result = self._values.get("read_on_demand_throughput_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty"]], result)

        @builtins.property
        def read_provisioned_throughput_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty"]]:
            '''Allows you to specify the read capacity settings for a replica global secondary index when the ``BillingMode`` is set to ``PROVISIONED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaglobalsecondaryindexspecification.html#cfn-dynamodb-globaltable-replicaglobalsecondaryindexspecification-readprovisionedthroughputsettings
            '''
            result = self._values.get("read_provisioned_throughput_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaGlobalSecondaryIndexSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.ReplicaSSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_master_key_id": "kmsMasterKeyId"},
    )
    class ReplicaSSESpecificationProperty:
        def __init__(
            self,
            *,
            kms_master_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Allows you to specify a KMS key identifier to be used for server-side encryption.

            The key can be specified via ARN, key ID, or alias. The key must be created in the same region as the replica.

            :param kms_master_key_id: The AWS key that should be used for the AWS encryption. To specify a key, use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. Note that you should only provide this parameter if the key is different from the default DynamoDB key ``alias/aws/dynamodb`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicassespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                replica_sSESpecification_property = dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaSSESpecificationProperty(
                    kms_master_key_id="kmsMasterKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22350277eb58d83f4972592a2a3071af1c1e55d64eb0eec247f08c6e9e975cee)
                check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_master_key_id is not None:
                self._values["kms_master_key_id"] = kms_master_key_id

        @builtins.property
        def kms_master_key_id(self) -> typing.Optional[builtins.str]:
            '''The AWS  key that should be used for the AWS  encryption.

            To specify a key, use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. Note that you should only provide this parameter if the key is different from the default DynamoDB key ``alias/aws/dynamodb`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicassespecification.html#cfn-dynamodb-globaltable-replicassespecification-kmsmasterkeyid
            '''
            result = self._values.get("kms_master_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaSSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.ReplicaSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "contributor_insights_specification": "contributorInsightsSpecification",
            "deletion_protection_enabled": "deletionProtectionEnabled",
            "global_secondary_indexes": "globalSecondaryIndexes",
            "kinesis_stream_specification": "kinesisStreamSpecification",
            "point_in_time_recovery_specification": "pointInTimeRecoverySpecification",
            "read_on_demand_throughput_settings": "readOnDemandThroughputSettings",
            "read_provisioned_throughput_settings": "readProvisionedThroughputSettings",
            "region": "region",
            "replica_stream_specification": "replicaStreamSpecification",
            "resource_policy": "resourcePolicy",
            "sse_specification": "sseSpecification",
            "table_class": "tableClass",
            "tags": "tags",
        },
    )
    class ReplicaSpecificationProperty:
        def __init__(
            self,
            *,
            contributor_insights_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            global_secondary_indexes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ReplicaGlobalSecondaryIndexSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            kinesis_stream_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.KinesisStreamSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            point_in_time_recovery_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.PointInTimeRecoverySpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            read_on_demand_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            read_provisioned_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            region: typing.Optional[builtins.str] = None,
            replica_stream_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ReplicaStreamSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ResourcePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sse_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ReplicaSSESpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_class: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines settings specific to a single replica of a global table.

            :param contributor_insights_specification: The settings used to enable or disable CloudWatch Contributor Insights for the specified replica. When not specified, defaults to contributor insights disabled for the replica.
            :param deletion_protection_enabled: Determines if a replica is protected from deletion. When enabled, the table cannot be deleted by any user or process. This setting is disabled by default. For more information, see `Using deletion protection <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.Basics.html#WorkingWithTables.Basics.DeletionProtection>`_ in the *Amazon DynamoDB Developer Guide* .
            :param global_secondary_indexes: Defines additional settings for the global secondary indexes of this replica.
            :param kinesis_stream_specification: Defines the Kinesis Data Streams configuration for the specified replica.
            :param point_in_time_recovery_specification: The settings used to enable point in time recovery. When not specified, defaults to point in time recovery disabled for the replica.
            :param read_on_demand_throughput_settings: Sets read request settings for the replica table.
            :param read_provisioned_throughput_settings: Defines read capacity settings for the replica table.
            :param region: The region in which this replica exists.
            :param replica_stream_specification: Represents the DynamoDB Streams configuration for a global table replica.
            :param resource_policy: A resource-based policy document that contains permissions to add to the specified replica of a DynamoDB global table. Resource-based policies let you define access permissions by specifying who has access to each resource, and the actions they are allowed to perform on each resource. In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .
            :param sse_specification: Allows you to specify a customer-managed key for the replica. When using customer-managed keys for server-side encryption, this property must have a value in all replicas.
            :param table_class: The table class of the specified table. Valid values are ``STANDARD`` and ``STANDARD_INFREQUENT_ACCESS`` .
            :param tags: An array of key-value pairs to apply to this replica. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                # policy_document: Any
                
                replica_specification_property = dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaSpecificationProperty(
                    contributor_insights_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty(
                        enabled=False,
                        mode="mode"
                    ),
                    deletion_protection_enabled=False,
                    global_secondary_indexes=[dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaGlobalSecondaryIndexSpecificationProperty(
                        contributor_insights_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty(
                            enabled=False,
                            mode="mode"
                        ),
                        index_name="indexName",
                        read_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty(
                            max_read_request_units=123
                        ),
                        read_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty(
                            read_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                                max_capacity=123,
                                min_capacity=123,
                                seed_capacity=123,
                                target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                    disable_scale_in=False,
                                    scale_in_cooldown=123,
                                    scale_out_cooldown=123,
                                    target_value=123
                                )
                            ),
                            read_capacity_units=123
                        )
                    )],
                    kinesis_stream_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.KinesisStreamSpecificationProperty(
                        approximate_creation_date_time_precision="approximateCreationDateTimePrecision",
                        stream_arn="streamArn"
                    ),
                    point_in_time_recovery_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.PointInTimeRecoverySpecificationProperty(
                        point_in_time_recovery_enabled=False,
                        recovery_period_in_days=123
                    ),
                    read_on_demand_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty(
                        max_read_request_units=123
                    ),
                    read_provisioned_throughput_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty(
                        read_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            seed_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123,
                                target_value=123
                            )
                        ),
                        read_capacity_units=123
                    ),
                    region="region",
                    replica_stream_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaStreamSpecificationProperty(
                        resource_policy=dynamodb_mixins.CfnGlobalTablePropsMixin.ResourcePolicyProperty(
                            policy_document=policy_document
                        )
                    ),
                    resource_policy=dynamodb_mixins.CfnGlobalTablePropsMixin.ResourcePolicyProperty(
                        policy_document=policy_document
                    ),
                    sse_specification=dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaSSESpecificationProperty(
                        kms_master_key_id="kmsMasterKeyId"
                    ),
                    table_class="tableClass",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8fc43b5fa89b6051cfe199f720ab167b0ee20b95635442f1175146a1a5caa3b)
                check_type(argname="argument contributor_insights_specification", value=contributor_insights_specification, expected_type=type_hints["contributor_insights_specification"])
                check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
                check_type(argname="argument global_secondary_indexes", value=global_secondary_indexes, expected_type=type_hints["global_secondary_indexes"])
                check_type(argname="argument kinesis_stream_specification", value=kinesis_stream_specification, expected_type=type_hints["kinesis_stream_specification"])
                check_type(argname="argument point_in_time_recovery_specification", value=point_in_time_recovery_specification, expected_type=type_hints["point_in_time_recovery_specification"])
                check_type(argname="argument read_on_demand_throughput_settings", value=read_on_demand_throughput_settings, expected_type=type_hints["read_on_demand_throughput_settings"])
                check_type(argname="argument read_provisioned_throughput_settings", value=read_provisioned_throughput_settings, expected_type=type_hints["read_provisioned_throughput_settings"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument replica_stream_specification", value=replica_stream_specification, expected_type=type_hints["replica_stream_specification"])
                check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
                check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
                check_type(argname="argument table_class", value=table_class, expected_type=type_hints["table_class"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contributor_insights_specification is not None:
                self._values["contributor_insights_specification"] = contributor_insights_specification
            if deletion_protection_enabled is not None:
                self._values["deletion_protection_enabled"] = deletion_protection_enabled
            if global_secondary_indexes is not None:
                self._values["global_secondary_indexes"] = global_secondary_indexes
            if kinesis_stream_specification is not None:
                self._values["kinesis_stream_specification"] = kinesis_stream_specification
            if point_in_time_recovery_specification is not None:
                self._values["point_in_time_recovery_specification"] = point_in_time_recovery_specification
            if read_on_demand_throughput_settings is not None:
                self._values["read_on_demand_throughput_settings"] = read_on_demand_throughput_settings
            if read_provisioned_throughput_settings is not None:
                self._values["read_provisioned_throughput_settings"] = read_provisioned_throughput_settings
            if region is not None:
                self._values["region"] = region
            if replica_stream_specification is not None:
                self._values["replica_stream_specification"] = replica_stream_specification
            if resource_policy is not None:
                self._values["resource_policy"] = resource_policy
            if sse_specification is not None:
                self._values["sse_specification"] = sse_specification
            if table_class is not None:
                self._values["table_class"] = table_class
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def contributor_insights_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty"]]:
            '''The settings used to enable or disable CloudWatch Contributor Insights for the specified replica.

            When not specified, defaults to contributor insights disabled for the replica.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-contributorinsightsspecification
            '''
            result = self._values.get("contributor_insights_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty"]], result)

        @builtins.property
        def deletion_protection_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines if a replica is protected from deletion.

            When enabled, the table cannot be deleted by any user or process. This setting is disabled by default. For more information, see `Using deletion protection <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.Basics.html#WorkingWithTables.Basics.DeletionProtection>`_ in the *Amazon DynamoDB Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-deletionprotectionenabled
            '''
            result = self._values.get("deletion_protection_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def global_secondary_indexes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReplicaGlobalSecondaryIndexSpecificationProperty"]]]]:
            '''Defines additional settings for the global secondary indexes of this replica.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-globalsecondaryindexes
            '''
            result = self._values.get("global_secondary_indexes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReplicaGlobalSecondaryIndexSpecificationProperty"]]]], result)

        @builtins.property
        def kinesis_stream_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.KinesisStreamSpecificationProperty"]]:
            '''Defines the Kinesis Data Streams configuration for the specified replica.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-kinesisstreamspecification
            '''
            result = self._values.get("kinesis_stream_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.KinesisStreamSpecificationProperty"]], result)

        @builtins.property
        def point_in_time_recovery_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.PointInTimeRecoverySpecificationProperty"]]:
            '''The settings used to enable point in time recovery.

            When not specified, defaults to point in time recovery disabled for the replica.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-pointintimerecoveryspecification
            '''
            result = self._values.get("point_in_time_recovery_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.PointInTimeRecoverySpecificationProperty"]], result)

        @builtins.property
        def read_on_demand_throughput_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty"]]:
            '''Sets read request settings for the replica table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-readondemandthroughputsettings
            '''
            result = self._values.get("read_on_demand_throughput_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty"]], result)

        @builtins.property
        def read_provisioned_throughput_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty"]]:
            '''Defines read capacity settings for the replica table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-readprovisionedthroughputsettings
            '''
            result = self._values.get("read_provisioned_throughput_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty"]], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The region in which this replica exists.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replica_stream_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReplicaStreamSpecificationProperty"]]:
            '''Represents the DynamoDB Streams configuration for a global table replica.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-replicastreamspecification
            '''
            result = self._values.get("replica_stream_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReplicaStreamSpecificationProperty"]], result)

        @builtins.property
        def resource_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ResourcePolicyProperty"]]:
            '''A resource-based policy document that contains permissions to add to the specified replica of a DynamoDB global table.

            Resource-based policies let you define access permissions by specifying who has access to each resource, and the actions they are allowed to perform on each resource.

            In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-resourcepolicy
            '''
            result = self._values.get("resource_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ResourcePolicyProperty"]], result)

        @builtins.property
        def sse_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReplicaSSESpecificationProperty"]]:
            '''Allows you to specify a customer-managed key for the replica.

            When using customer-managed keys for server-side encryption, this property must have a value in all replicas.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-ssespecification
            '''
            result = self._values.get("sse_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ReplicaSSESpecificationProperty"]], result)

        @builtins.property
        def table_class(self) -> typing.Optional[builtins.str]:
            '''The table class of the specified table.

            Valid values are ``STANDARD`` and ``STANDARD_INFREQUENT_ACCESS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-tableclass
            '''
            result = self._values.get("table_class")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of key-value pairs to apply to this replica.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.ReplicaStreamSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_policy": "resourcePolicy"},
    )
    class ReplicaStreamSpecificationProperty:
        def __init__(
            self,
            *,
            resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.ResourcePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the DynamoDB Streams configuration for a global table replica.

            :param resource_policy: A resource-based policy document that contains the permissions for the specified stream of a DynamoDB global table replica. Resource-based policies let you define access permissions by specifying who has access to each resource, and the actions they are allowed to perform on each resource. In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ . You can update the ``ResourcePolicy`` property if you've specified more than one table using the `AWS ::DynamoDB::GlobalTable <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html>`_ resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicastreamspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                # policy_document: Any
                
                replica_stream_specification_property = dynamodb_mixins.CfnGlobalTablePropsMixin.ReplicaStreamSpecificationProperty(
                    resource_policy=dynamodb_mixins.CfnGlobalTablePropsMixin.ResourcePolicyProperty(
                        policy_document=policy_document
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03ad60331c76a840512b1aeba254cb2be4b7cf989bffd858a780720a774c8cd1)
                check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_policy is not None:
                self._values["resource_policy"] = resource_policy

        @builtins.property
        def resource_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ResourcePolicyProperty"]]:
            '''A resource-based policy document that contains the permissions for the specified stream of a DynamoDB global table replica.

            Resource-based policies let you define access permissions by specifying who has access to each resource, and the actions they are allowed to perform on each resource.

            In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .

            You can update the ``ResourcePolicy`` property if you've specified more than one table using the `AWS ::DynamoDB::GlobalTable <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html>`_ resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicastreamspecification.html#cfn-dynamodb-globaltable-replicastreamspecification-resourcepolicy
            '''
            result = self._values.get("resource_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.ResourcePolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaStreamSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.ResourcePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"policy_document": "policyDocument"},
    )
    class ResourcePolicyProperty:
        def __init__(self, *, policy_document: typing.Any = None) -> None:
            '''Creates or updates a resource-based policy document that contains the permissions for DynamoDB resources, such as a table, its indexes, and stream.

            Resource-based policies let you define access permissions by specifying who has access to each resource, and the actions they are allowed to perform on each resource.

            In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .

            While defining resource-based policies in your CloudFormation templates, the following considerations apply:

            - The maximum size supported for a resource-based policy document in JSON format is 20 KB. DynamoDB counts whitespaces when calculating the size of a policy against this limit.
            - Resource-based policies don't support `drift detection <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html#>`_ . If you update a policy outside of the CloudFormation stack template, you'll need to update the CloudFormation stack with the changes.
            - Resource-based policies don't support out-of-band changes. If you add, update, or delete a policy outside of the CloudFormation template, the change won't be overwritten if there are no changes to the policy within the template.

            For example, say that your template contains a resource-based policy, which you later update outside of the template. If you don't make any changes to the policy in the template, the updated policy in DynamoDB won’t be synced with the policy in the template.

            Conversely, say that your template doesn’t contain a resource-based policy, but you add a policy outside of the template. This policy won’t be removed from DynamoDB as long as you don’t add it to the template. When you add a policy to the template and update the stack, the existing policy in DynamoDB will be updated to match the one defined in the template.

            - Within a resource-based policy, if the action for a DynamoDB service-linked role (SLR) to replicate data for a global table is denied, adding or deleting a replica will fail with an error.
            - The `AWS ::DynamoDB::GlobalTable <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html>`_ resource doesn't support creating a replica in the same stack update in Regions other than the Region where you deploy the stack update.

            For a full list of all considerations, see `Resource-based policy considerations <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-considerations.html>`_ .

            :param policy_document: A resource-based policy document that contains permissions to add to the specified DynamoDB table, its indexes, and stream. In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-resourcepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                # policy_document: Any
                
                resource_policy_property = dynamodb_mixins.CfnGlobalTablePropsMixin.ResourcePolicyProperty(
                    policy_document=policy_document
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34515d1180d2f218918968b2a0fbce07d80728e15e3946a929a7e7c8c1c73d16)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_document is not None:
                self._values["policy_document"] = policy_document

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''A resource-based policy document that contains permissions to add to the specified DynamoDB table, its indexes, and stream.

            In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-resourcepolicy.html#cfn-dynamodb-globaltable-resourcepolicy-policydocument
            '''
            result = self._values.get("policy_document")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourcePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"sse_enabled": "sseEnabled", "sse_type": "sseType"},
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            sse_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the settings used to enable server-side encryption.

            :param sse_enabled: Indicates whether server-side encryption is performed using an AWS managed key or an AWS owned key. If enabled (true), server-side encryption type is set to KMS and an AWS managed key is used ( AWS charges apply). If disabled (false) or not specified,server-side encryption is set to an AWS owned key. If you choose to use KMS encryption, you can also use customer managed KMS keys by specifying them in the ``ReplicaSpecification.SSESpecification`` object. You cannot mix AWS managed and customer managed KMS keys.
            :param sse_type: Server-side encryption type. The only supported value is:. - ``KMS`` - Server-side encryption that uses AWS Key Management Service . The key is stored in your account and is managed by AWS ( AWS charges apply).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-ssespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                s_sESpecification_property = dynamodb_mixins.CfnGlobalTablePropsMixin.SSESpecificationProperty(
                    sse_enabled=False,
                    sse_type="sseType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__23dda535fd15a1f4c35a5c9821633b7cf92e2f3d1c0a5549100ffe31f36b4cf7)
                check_type(argname="argument sse_enabled", value=sse_enabled, expected_type=type_hints["sse_enabled"])
                check_type(argname="argument sse_type", value=sse_type, expected_type=type_hints["sse_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sse_enabled is not None:
                self._values["sse_enabled"] = sse_enabled
            if sse_type is not None:
                self._values["sse_type"] = sse_type

        @builtins.property
        def sse_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether server-side encryption is performed using an AWS managed key or an AWS owned key.

            If enabled (true), server-side encryption type is set to KMS and an AWS managed key is used ( AWS  charges apply). If disabled (false) or not specified,server-side encryption is set to an AWS owned key. If you choose to use KMS encryption, you can also use customer managed KMS keys by specifying them in the ``ReplicaSpecification.SSESpecification`` object. You cannot mix AWS managed and customer managed KMS keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-ssespecification.html#cfn-dynamodb-globaltable-ssespecification-sseenabled
            '''
            result = self._values.get("sse_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def sse_type(self) -> typing.Optional[builtins.str]:
            '''Server-side encryption type. The only supported value is:.

            - ``KMS`` - Server-side encryption that uses AWS Key Management Service . The key is stored in your account and is managed by AWS  ( AWS  charges apply).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-ssespecification.html#cfn-dynamodb-globaltable-ssespecification-ssetype
            '''
            result = self._values.get("sse_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.StreamSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_view_type": "streamViewType"},
    )
    class StreamSpecificationProperty:
        def __init__(
            self,
            *,
            stream_view_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the DynamoDB Streams configuration for a table in DynamoDB .

            You can only modify this value for a ``AWS::DynamoDB::GlobalTable`` resource configured for multi-Region eventual consistency (MREC, the default) if that resource contains only one entry in ``Replicas`` . You must specify a value for this property for a ``AWS::DynamoDB::GlobalTable`` resource configured for MREC with more than one entry in ``Replicas`` . For Multi-Region Strong Consistency (MRSC), Streams are not required and can be changed for existing tables.

            :param stream_view_type: When an item in the table is modified, ``StreamViewType`` determines what information is written to the stream for this table. Valid values for ``StreamViewType`` are: - ``KEYS_ONLY`` - Only the key attributes of the modified item are written to the stream. - ``NEW_IMAGE`` - The entire item, as it appears after it was modified, is written to the stream. - ``OLD_IMAGE`` - The entire item, as it appeared before it was modified, is written to the stream. - ``NEW_AND_OLD_IMAGES`` - Both the new and the old item images of the item are written to the stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-streamspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                stream_specification_property = dynamodb_mixins.CfnGlobalTablePropsMixin.StreamSpecificationProperty(
                    stream_view_type="streamViewType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c27ad7c3145f52d23ed4e3849e6b91a9e114eda88631833f4686f37c1f698b97)
                check_type(argname="argument stream_view_type", value=stream_view_type, expected_type=type_hints["stream_view_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stream_view_type is not None:
                self._values["stream_view_type"] = stream_view_type

        @builtins.property
        def stream_view_type(self) -> typing.Optional[builtins.str]:
            '''When an item in the table is modified, ``StreamViewType`` determines what information is written to the stream for this table.

            Valid values for ``StreamViewType`` are:

            - ``KEYS_ONLY`` - Only the key attributes of the modified item are written to the stream.
            - ``NEW_IMAGE`` - The entire item, as it appears after it was modified, is written to the stream.
            - ``OLD_IMAGE`` - The entire item, as it appeared before it was modified, is written to the stream.
            - ``NEW_AND_OLD_IMAGES`` - Both the new and the old item images of the item are written to the stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-streamspecification.html#cfn-dynamodb-globaltable-streamspecification-streamviewtype
            '''
            result = self._values.get("stream_view_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty",
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
            '''Defines a target tracking scaling policy.

            :param disable_scale_in: Indicates whether scale in by the target tracking scaling policy is disabled. The default value is ``false`` .
            :param scale_in_cooldown: The amount of time, in seconds, after a scale-in activity completes before another scale-in activity can start.
            :param scale_out_cooldown: The amount of time, in seconds, after a scale-out activity completes before another scale-out activity can start.
            :param target_value: Defines a target value for the scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-targettrackingscalingpolicyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                target_tracking_scaling_policy_configuration_property = dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                    disable_scale_in=False,
                    scale_in_cooldown=123,
                    scale_out_cooldown=123,
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1d13e6c1b4568d79d978066c3ad4993e50c25aebc2eb02b2e759e34cff0e132)
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
            '''Indicates whether scale in by the target tracking scaling policy is disabled.

            The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-targettrackingscalingpolicyconfiguration.html#cfn-dynamodb-globaltable-targettrackingscalingpolicyconfiguration-disablescalein
            '''
            result = self._values.get("disable_scale_in")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def scale_in_cooldown(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, after a scale-in activity completes before another scale-in activity can start.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-targettrackingscalingpolicyconfiguration.html#cfn-dynamodb-globaltable-targettrackingscalingpolicyconfiguration-scaleincooldown
            '''
            result = self._values.get("scale_in_cooldown")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scale_out_cooldown(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, after a scale-out activity completes before another scale-out activity can start.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-targettrackingscalingpolicyconfiguration.html#cfn-dynamodb-globaltable-targettrackingscalingpolicyconfiguration-scaleoutcooldown
            '''
            result = self._values.get("scale_out_cooldown")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''Defines a target value for the scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-targettrackingscalingpolicyconfiguration.html#cfn-dynamodb-globaltable-targettrackingscalingpolicyconfiguration-targetvalue
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
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.TimeToLiveSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_name": "attributeName", "enabled": "enabled"},
    )
    class TimeToLiveSpecificationProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Represents the settings used to enable or disable Time to Live (TTL) for the specified table.

            All replicas will have the same time to live configuration.

            :param attribute_name: The name of the attribute used to store the expiration time for items in the table. Currently, you cannot directly change the attribute name used to evaluate time to live. In order to do so, you must first disable time to live, and then re-enable it with the new attribute name. It can take up to one hour for changes to time to live to take effect. If you attempt to modify time to live within that time window, your stack operation might be delayed.
            :param enabled: Indicates whether TTL is to be enabled (true) or disabled (false) on the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-timetolivespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                time_to_live_specification_property = dynamodb_mixins.CfnGlobalTablePropsMixin.TimeToLiveSpecificationProperty(
                    attribute_name="attributeName",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9864f704e8a9699286d902d9da30315911168cece8859e7bb11472851b0609f5)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute used to store the expiration time for items in the table.

            Currently, you cannot directly change the attribute name used to evaluate time to live. In order to do so, you must first disable time to live, and then re-enable it with the new attribute name. It can take up to one hour for changes to time to live to take effect. If you attempt to modify time to live within that time window, your stack operation might be delayed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-timetolivespecification.html#cfn-dynamodb-globaltable-timetolivespecification-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether TTL is to be enabled (true) or disabled (false) on the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-timetolivespecification.html#cfn-dynamodb-globaltable-timetolivespecification-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeToLiveSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.WarmThroughputProperty",
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
            '''Provides visibility into the number of read and write operations your table or secondary index can instantaneously support.

            The settings can be modified using the ``UpdateTable`` operation to meet the throughput requirements of an upcoming peak event.

            :param read_units_per_second: Represents the number of read operations your base table can instantaneously support.
            :param write_units_per_second: Represents the number of write operations your base table can instantaneously support.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-warmthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                warm_throughput_property = dynamodb_mixins.CfnGlobalTablePropsMixin.WarmThroughputProperty(
                    read_units_per_second=123,
                    write_units_per_second=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a590116c1bcca33645e4b3251e0d1223e7a48ee0f7029871ec8eb615f206c432)
                check_type(argname="argument read_units_per_second", value=read_units_per_second, expected_type=type_hints["read_units_per_second"])
                check_type(argname="argument write_units_per_second", value=write_units_per_second, expected_type=type_hints["write_units_per_second"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if read_units_per_second is not None:
                self._values["read_units_per_second"] = read_units_per_second
            if write_units_per_second is not None:
                self._values["write_units_per_second"] = write_units_per_second

        @builtins.property
        def read_units_per_second(self) -> typing.Optional[jsii.Number]:
            '''Represents the number of read operations your base table can instantaneously support.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-warmthroughput.html#cfn-dynamodb-globaltable-warmthroughput-readunitspersecond
            '''
            result = self._values.get("read_units_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def write_units_per_second(self) -> typing.Optional[jsii.Number]:
            '''Represents the number of write operations your base table can instantaneously support.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-warmthroughput.html#cfn-dynamodb-globaltable-warmthroughput-writeunitspersecond
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
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"max_write_request_units": "maxWriteRequestUnits"},
    )
    class WriteOnDemandThroughputSettingsProperty:
        def __init__(
            self,
            *,
            max_write_request_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Sets the write request settings for a global table or a global secondary index.

            You can only specify this setting if your resource uses the ``PAY_PER_REQUEST`` ``BillingMode`` .

            :param max_write_request_units: Maximum number of write request settings for the specified replica of a global table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-writeondemandthroughputsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                write_on_demand_throughput_settings_property = dynamodb_mixins.CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty(
                    max_write_request_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aecd5c92cb7d71a337f68acf140fd13d8f1ea93da940a5eb61cf700a26949d86)
                check_type(argname="argument max_write_request_units", value=max_write_request_units, expected_type=type_hints["max_write_request_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_write_request_units is not None:
                self._values["max_write_request_units"] = max_write_request_units

        @builtins.property
        def max_write_request_units(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of write request settings for the specified replica of a global table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-writeondemandthroughputsettings.html#cfn-dynamodb-globaltable-writeondemandthroughputsettings-maxwriterequestunits
            '''
            result = self._values.get("max_write_request_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WriteOnDemandThroughputSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "write_capacity_auto_scaling_settings": "writeCapacityAutoScalingSettings",
        },
    )
    class WriteProvisionedThroughputSettingsProperty:
        def __init__(
            self,
            *,
            write_capacity_auto_scaling_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies an auto scaling policy for write capacity.

            This policy will be applied to all replicas. This setting must be specified if ``BillingMode`` is set to ``PROVISIONED`` .

            :param write_capacity_auto_scaling_settings: Specifies auto scaling settings for the replica table or global secondary index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-writeprovisionedthroughputsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                write_provisioned_throughput_settings_property = dynamodb_mixins.CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty(
                    write_capacity_auto_scaling_settings=dynamodb_mixins.CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty(
                        max_capacity=123,
                        min_capacity=123,
                        seed_capacity=123,
                        target_tracking_scaling_policy_configuration=dynamodb_mixins.CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123,
                            target_value=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e60889fc0e91a064c72aa49b910b826a3032526642568d580d7a1c30dc715ecc)
                check_type(argname="argument write_capacity_auto_scaling_settings", value=write_capacity_auto_scaling_settings, expected_type=type_hints["write_capacity_auto_scaling_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if write_capacity_auto_scaling_settings is not None:
                self._values["write_capacity_auto_scaling_settings"] = write_capacity_auto_scaling_settings

        @builtins.property
        def write_capacity_auto_scaling_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty"]]:
            '''Specifies auto scaling settings for the replica table or global secondary index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-writeprovisionedthroughputsettings.html#cfn-dynamodb-globaltable-writeprovisionedthroughputsettings-writecapacityautoscalingsettings
            '''
            result = self._values.get("write_capacity_auto_scaling_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WriteProvisionedThroughputSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_definitions": "attributeDefinitions",
        "billing_mode": "billingMode",
        "contributor_insights_specification": "contributorInsightsSpecification",
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "global_secondary_indexes": "globalSecondaryIndexes",
        "import_source_specification": "importSourceSpecification",
        "key_schema": "keySchema",
        "kinesis_stream_specification": "kinesisStreamSpecification",
        "local_secondary_indexes": "localSecondaryIndexes",
        "on_demand_throughput": "onDemandThroughput",
        "point_in_time_recovery_specification": "pointInTimeRecoverySpecification",
        "provisioned_throughput": "provisionedThroughput",
        "resource_policy": "resourcePolicy",
        "sse_specification": "sseSpecification",
        "stream_specification": "streamSpecification",
        "table_class": "tableClass",
        "table_name": "tableName",
        "tags": "tags",
        "time_to_live_specification": "timeToLiveSpecification",
        "warm_throughput": "warmThroughput",
    },
)
class CfnTableMixinProps:
    def __init__(
        self,
        *,
        attribute_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.AttributeDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        billing_mode: typing.Optional[builtins.str] = None,
        contributor_insights_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ContributorInsightsSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        global_secondary_indexes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.GlobalSecondaryIndexProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        import_source_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ImportSourceSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        kinesis_stream_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.KinesisStreamSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        local_secondary_indexes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.LocalSecondaryIndexProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        on_demand_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.OnDemandThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        point_in_time_recovery_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.PointInTimeRecoverySpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ProvisionedThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ResourcePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sse_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.SSESpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stream_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.StreamSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_class: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_to_live_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.TimeToLiveSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        warm_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.WarmThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTablePropsMixin.

        :param attribute_definitions: A list of attributes that describe the key schema for the table and indexes. This property is required to create a DynamoDB table. Update requires: `Some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ . Replacement if you edit an existing AttributeDefinition.
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Valid values include: - ``PAY_PER_REQUEST`` - We recommend using ``PAY_PER_REQUEST`` for most DynamoDB workloads. ``PAY_PER_REQUEST`` sets the billing mode to `On-demand capacity mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode.html>`_ . - ``PROVISIONED`` - We recommend using ``PROVISIONED`` for steady workloads with predictable growth where capacity requirements can be reliably forecasted. ``PROVISIONED`` sets the billing mode to `Provisioned capacity mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/provisioned-capacity-mode.html>`_ . If not specified, the default is ``PROVISIONED`` .
        :param contributor_insights_specification: The settings used to specify whether to enable CloudWatch Contributor Insights for the table and define which events to monitor.
        :param deletion_protection_enabled: Determines if a table is protected from deletion. When enabled, the table cannot be deleted by any user or process. This setting is disabled by default. For more information, see `Using deletion protection <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.Basics.html#WorkingWithTables.Basics.DeletionProtection>`_ in the *Amazon DynamoDB Developer Guide* .
        :param global_secondary_indexes: Global secondary indexes to be created on the table. You can create up to 20 global secondary indexes. .. epigraph:: If you update a table to include a new global secondary index, AWS CloudFormation initiates the index creation and then proceeds with the stack update. AWS CloudFormation doesn't wait for the index to complete creation because the backfilling phase can take a long time, depending on the size of the table. You can't use the index or update the table until the index's status is ``ACTIVE`` . You can track its status by using the DynamoDB `DescribeTable <https://docs.aws.amazon.com/cli/latest/reference/dynamodb/describe-table.html>`_ command. If you add or delete an index during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new index, you must manually delete the index. Updates are not supported. The following are exceptions: - If you update either the contributor insights specification or the provisioned throughput values of global secondary indexes, you can update the table without interruption. - You can delete or add one global secondary index without interruption. If you do both in the same update (for example, by changing the index's logical ID), the update fails.
        :param import_source_specification: Specifies the properties of data being imported from the S3 bucket source to the" table. .. epigraph:: If you specify the ``ImportSourceSpecification`` property, and also specify either the ``StreamSpecification`` , the ``TableClass`` property, the ``DeletionProtectionEnabled`` property, or the ``WarmThroughput`` property, the IAM entity creating/updating stack must have ``UpdateTable`` permission.
        :param key_schema: Specifies the attributes that make up the primary key for the table. The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.
        :param kinesis_stream_specification: The Kinesis Data Streams configuration for the specified table.
        :param local_secondary_indexes: Local secondary indexes to be created on the table. You can create up to 5 local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes.
        :param on_demand_throughput: Sets the maximum number of read and write units for the specified on-demand table. If you use this property, you must specify ``MaxReadRequestUnits`` , ``MaxWriteRequestUnits`` , or both.
        :param point_in_time_recovery_specification: The settings used to enable point in time recovery.
        :param provisioned_throughput: Throughput for the specified table, which consists of values for ``ReadCapacityUnits`` and ``WriteCapacityUnits`` . For more information about the contents of a provisioned throughput structure, see `Amazon DynamoDB Table ProvisionedThroughput <https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ProvisionedThroughput.html>`_ . If you set ``BillingMode`` as ``PROVISIONED`` , you must specify this property. If you set ``BillingMode`` as ``PAY_PER_REQUEST`` , you cannot specify this property.
        :param resource_policy: An AWS resource-based policy document in JSON format that will be attached to the table. When you attach a resource-based policy while creating a table, the policy application is *strongly consistent* . The maximum size supported for a resource-based policy document is 20 KB. DynamoDB counts whitespaces when calculating the size of a policy against this limit. For a full list of all considerations that apply for resource-based policies, see `Resource-based policy considerations <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-considerations.html>`_ . .. epigraph:: You need to specify the ``CreateTable`` and ``PutResourcePolicy`` IAM actions for authorizing a user to create a table with a resource-based policy.
        :param sse_specification: Specifies the settings to enable server-side encryption.
        :param stream_specification: The settings for the DynamoDB table stream, which captures changes to items stored in the table. Including this property in your AWS CloudFormation template automatically enables streaming.
        :param table_class: The table class of the new table. Valid values are ``STANDARD`` and ``STANDARD_INFREQUENT_ACCESS`` .
        :param table_name: A name for the table. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the table name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param time_to_live_specification: Specifies the Time to Live (TTL) settings for the table. .. epigraph:: For detailed information about the limits in DynamoDB, see `Limits in Amazon DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html>`_ in the Amazon DynamoDB Developer Guide.
        :param warm_throughput: Represents the warm throughput (in read units per second and write units per second) for creating a table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
            
            # policy_document: Any
            
            cfn_table_mixin_props = dynamodb_mixins.CfnTableMixinProps(
                attribute_definitions=[dynamodb_mixins.CfnTablePropsMixin.AttributeDefinitionProperty(
                    attribute_name="attributeName",
                    attribute_type="attributeType"
                )],
                billing_mode="billingMode",
                contributor_insights_specification=dynamodb_mixins.CfnTablePropsMixin.ContributorInsightsSpecificationProperty(
                    enabled=False,
                    mode="mode"
                ),
                deletion_protection_enabled=False,
                global_secondary_indexes=[dynamodb_mixins.CfnTablePropsMixin.GlobalSecondaryIndexProperty(
                    contributor_insights_specification=dynamodb_mixins.CfnTablePropsMixin.ContributorInsightsSpecificationProperty(
                        enabled=False,
                        mode="mode"
                    ),
                    index_name="indexName",
                    key_schema=[dynamodb_mixins.CfnTablePropsMixin.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    on_demand_throughput=dynamodb_mixins.CfnTablePropsMixin.OnDemandThroughputProperty(
                        max_read_request_units=123,
                        max_write_request_units=123
                    ),
                    projection=dynamodb_mixins.CfnTablePropsMixin.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    ),
                    provisioned_throughput=dynamodb_mixins.CfnTablePropsMixin.ProvisionedThroughputProperty(
                        read_capacity_units=123,
                        write_capacity_units=123
                    ),
                    warm_throughput=dynamodb_mixins.CfnTablePropsMixin.WarmThroughputProperty(
                        read_units_per_second=123,
                        write_units_per_second=123
                    )
                )],
                import_source_specification=dynamodb_mixins.CfnTablePropsMixin.ImportSourceSpecificationProperty(
                    input_compression_type="inputCompressionType",
                    input_format="inputFormat",
                    input_format_options=dynamodb_mixins.CfnTablePropsMixin.InputFormatOptionsProperty(
                        csv=dynamodb_mixins.CfnTablePropsMixin.CsvProperty(
                            delimiter="delimiter",
                            header_list=["headerList"]
                        )
                    ),
                    s3_bucket_source=dynamodb_mixins.CfnTablePropsMixin.S3BucketSourceProperty(
                        s3_bucket="s3Bucket",
                        s3_bucket_owner="s3BucketOwner",
                        s3_key_prefix="s3KeyPrefix"
                    )
                ),
                key_schema=[dynamodb_mixins.CfnTablePropsMixin.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                kinesis_stream_specification=dynamodb_mixins.CfnTablePropsMixin.KinesisStreamSpecificationProperty(
                    approximate_creation_date_time_precision="approximateCreationDateTimePrecision",
                    stream_arn="streamArn"
                ),
                local_secondary_indexes=[dynamodb_mixins.CfnTablePropsMixin.LocalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb_mixins.CfnTablePropsMixin.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb_mixins.CfnTablePropsMixin.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    )
                )],
                on_demand_throughput=dynamodb_mixins.CfnTablePropsMixin.OnDemandThroughputProperty(
                    max_read_request_units=123,
                    max_write_request_units=123
                ),
                point_in_time_recovery_specification=dynamodb_mixins.CfnTablePropsMixin.PointInTimeRecoverySpecificationProperty(
                    point_in_time_recovery_enabled=False,
                    recovery_period_in_days=123
                ),
                provisioned_throughput=dynamodb_mixins.CfnTablePropsMixin.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                ),
                resource_policy=dynamodb_mixins.CfnTablePropsMixin.ResourcePolicyProperty(
                    policy_document=policy_document
                ),
                sse_specification=dynamodb_mixins.CfnTablePropsMixin.SSESpecificationProperty(
                    kms_master_key_id="kmsMasterKeyId",
                    sse_enabled=False,
                    sse_type="sseType"
                ),
                stream_specification=dynamodb_mixins.CfnTablePropsMixin.StreamSpecificationProperty(
                    resource_policy=dynamodb_mixins.CfnTablePropsMixin.ResourcePolicyProperty(
                        policy_document=policy_document
                    ),
                    stream_view_type="streamViewType"
                ),
                table_class="tableClass",
                table_name="tableName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                time_to_live_specification=dynamodb_mixins.CfnTablePropsMixin.TimeToLiveSpecificationProperty(
                    attribute_name="attributeName",
                    enabled=False
                ),
                warm_throughput=dynamodb_mixins.CfnTablePropsMixin.WarmThroughputProperty(
                    read_units_per_second=123,
                    write_units_per_second=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac30cb9d306ee3dda3bdd5f42feb3cef6dcbefa12df5b3c6a899bcae7da600b)
            check_type(argname="argument attribute_definitions", value=attribute_definitions, expected_type=type_hints["attribute_definitions"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument contributor_insights_specification", value=contributor_insights_specification, expected_type=type_hints["contributor_insights_specification"])
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument global_secondary_indexes", value=global_secondary_indexes, expected_type=type_hints["global_secondary_indexes"])
            check_type(argname="argument import_source_specification", value=import_source_specification, expected_type=type_hints["import_source_specification"])
            check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
            check_type(argname="argument kinesis_stream_specification", value=kinesis_stream_specification, expected_type=type_hints["kinesis_stream_specification"])
            check_type(argname="argument local_secondary_indexes", value=local_secondary_indexes, expected_type=type_hints["local_secondary_indexes"])
            check_type(argname="argument on_demand_throughput", value=on_demand_throughput, expected_type=type_hints["on_demand_throughput"])
            check_type(argname="argument point_in_time_recovery_specification", value=point_in_time_recovery_specification, expected_type=type_hints["point_in_time_recovery_specification"])
            check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
            check_type(argname="argument stream_specification", value=stream_specification, expected_type=type_hints["stream_specification"])
            check_type(argname="argument table_class", value=table_class, expected_type=type_hints["table_class"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument time_to_live_specification", value=time_to_live_specification, expected_type=type_hints["time_to_live_specification"])
            check_type(argname="argument warm_throughput", value=warm_throughput, expected_type=type_hints["warm_throughput"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_definitions is not None:
            self._values["attribute_definitions"] = attribute_definitions
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if contributor_insights_specification is not None:
            self._values["contributor_insights_specification"] = contributor_insights_specification
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if global_secondary_indexes is not None:
            self._values["global_secondary_indexes"] = global_secondary_indexes
        if import_source_specification is not None:
            self._values["import_source_specification"] = import_source_specification
        if key_schema is not None:
            self._values["key_schema"] = key_schema
        if kinesis_stream_specification is not None:
            self._values["kinesis_stream_specification"] = kinesis_stream_specification
        if local_secondary_indexes is not None:
            self._values["local_secondary_indexes"] = local_secondary_indexes
        if on_demand_throughput is not None:
            self._values["on_demand_throughput"] = on_demand_throughput
        if point_in_time_recovery_specification is not None:
            self._values["point_in_time_recovery_specification"] = point_in_time_recovery_specification
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if resource_policy is not None:
            self._values["resource_policy"] = resource_policy
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if stream_specification is not None:
            self._values["stream_specification"] = stream_specification
        if table_class is not None:
            self._values["table_class"] = table_class
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags
        if time_to_live_specification is not None:
            self._values["time_to_live_specification"] = time_to_live_specification
        if warm_throughput is not None:
            self._values["warm_throughput"] = warm_throughput

    @builtins.property
    def attribute_definitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.AttributeDefinitionProperty"]]]]:
        '''A list of attributes that describe the key schema for the table and indexes.

        This property is required to create a DynamoDB table.

        Update requires: `Some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ . Replacement if you edit an existing AttributeDefinition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-attributedefinitions
        '''
        result = self._values.get("attribute_definitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.AttributeDefinitionProperty"]]]], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[builtins.str]:
        '''Specify how you are charged for read and write throughput and how you manage capacity.

        Valid values include:

        - ``PAY_PER_REQUEST`` - We recommend using ``PAY_PER_REQUEST`` for most DynamoDB workloads. ``PAY_PER_REQUEST`` sets the billing mode to `On-demand capacity mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode.html>`_ .
        - ``PROVISIONED`` - We recommend using ``PROVISIONED`` for steady workloads with predictable growth where capacity requirements can be reliably forecasted. ``PROVISIONED`` sets the billing mode to `Provisioned capacity mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/provisioned-capacity-mode.html>`_ .

        If not specified, the default is ``PROVISIONED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-billingmode
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contributor_insights_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ContributorInsightsSpecificationProperty"]]:
        '''The settings used to specify whether to enable CloudWatch Contributor Insights for the table and define which events to monitor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-contributorinsightsspecification
        '''
        result = self._values.get("contributor_insights_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ContributorInsightsSpecificationProperty"]], result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Determines if a table is protected from deletion.

        When enabled, the table cannot be deleted by any user or process. This setting is disabled by default. For more information, see `Using deletion protection <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.Basics.html#WorkingWithTables.Basics.DeletionProtection>`_ in the *Amazon DynamoDB Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-deletionprotectionenabled
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def global_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.GlobalSecondaryIndexProperty"]]]]:
        '''Global secondary indexes to be created on the table. You can create up to 20 global secondary indexes.

        .. epigraph::

           If you update a table to include a new global secondary index, AWS CloudFormation initiates the index creation and then proceeds with the stack update. AWS CloudFormation doesn't wait for the index to complete creation because the backfilling phase can take a long time, depending on the size of the table. You can't use the index or update the table until the index's status is ``ACTIVE`` . You can track its status by using the DynamoDB `DescribeTable <https://docs.aws.amazon.com/cli/latest/reference/dynamodb/describe-table.html>`_ command.

           If you add or delete an index during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new index, you must manually delete the index.

           Updates are not supported. The following are exceptions:

           - If you update either the contributor insights specification or the provisioned throughput values of global secondary indexes, you can update the table without interruption.
           - You can delete or add one global secondary index without interruption. If you do both in the same update (for example, by changing the index's logical ID), the update fails.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-globalsecondaryindexes
        '''
        result = self._values.get("global_secondary_indexes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.GlobalSecondaryIndexProperty"]]]], result)

    @builtins.property
    def import_source_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ImportSourceSpecificationProperty"]]:
        '''Specifies the properties of data being imported from the S3 bucket source to the" table.

        .. epigraph::

           If you specify the ``ImportSourceSpecification`` property, and also specify either the ``StreamSpecification`` , the ``TableClass`` property, the ``DeletionProtectionEnabled`` property, or the ``WarmThroughput`` property, the IAM entity creating/updating stack must have ``UpdateTable`` permission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-importsourcespecification
        '''
        result = self._values.get("import_source_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ImportSourceSpecificationProperty"]], result)

    @builtins.property
    def key_schema(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.KeySchemaProperty"]]]]:
        '''Specifies the attributes that make up the primary key for the table.

        The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-keyschema
        '''
        result = self._values.get("key_schema")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.KeySchemaProperty"]]]], result)

    @builtins.property
    def kinesis_stream_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.KinesisStreamSpecificationProperty"]]:
        '''The Kinesis Data Streams configuration for the specified table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-kinesisstreamspecification
        '''
        result = self._values.get("kinesis_stream_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.KinesisStreamSpecificationProperty"]], result)

    @builtins.property
    def local_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.LocalSecondaryIndexProperty"]]]]:
        '''Local secondary indexes to be created on the table.

        You can create up to 5 local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-localsecondaryindexes
        '''
        result = self._values.get("local_secondary_indexes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.LocalSecondaryIndexProperty"]]]], result)

    @builtins.property
    def on_demand_throughput(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.OnDemandThroughputProperty"]]:
        '''Sets the maximum number of read and write units for the specified on-demand table.

        If you use this property, you must specify ``MaxReadRequestUnits`` , ``MaxWriteRequestUnits`` , or both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-ondemandthroughput
        '''
        result = self._values.get("on_demand_throughput")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.OnDemandThroughputProperty"]], result)

    @builtins.property
    def point_in_time_recovery_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.PointInTimeRecoverySpecificationProperty"]]:
        '''The settings used to enable point in time recovery.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-pointintimerecoveryspecification
        '''
        result = self._values.get("point_in_time_recovery_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.PointInTimeRecoverySpecificationProperty"]], result)

    @builtins.property
    def provisioned_throughput(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ProvisionedThroughputProperty"]]:
        '''Throughput for the specified table, which consists of values for ``ReadCapacityUnits`` and ``WriteCapacityUnits`` .

        For more information about the contents of a provisioned throughput structure, see `Amazon DynamoDB Table ProvisionedThroughput <https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ProvisionedThroughput.html>`_ .

        If you set ``BillingMode`` as ``PROVISIONED`` , you must specify this property. If you set ``BillingMode`` as ``PAY_PER_REQUEST`` , you cannot specify this property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-provisionedthroughput
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ProvisionedThroughputProperty"]], result)

    @builtins.property
    def resource_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ResourcePolicyProperty"]]:
        '''An AWS resource-based policy document in JSON format that will be attached to the table.

        When you attach a resource-based policy while creating a table, the policy application is *strongly consistent* .

        The maximum size supported for a resource-based policy document is 20 KB. DynamoDB counts whitespaces when calculating the size of a policy against this limit. For a full list of all considerations that apply for resource-based policies, see `Resource-based policy considerations <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-considerations.html>`_ .
        .. epigraph::

           You need to specify the ``CreateTable`` and ``PutResourcePolicy`` IAM actions for authorizing a user to create a table with a resource-based policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-resourcepolicy
        '''
        result = self._values.get("resource_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ResourcePolicyProperty"]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SSESpecificationProperty"]]:
        '''Specifies the settings to enable server-side encryption.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-ssespecification
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SSESpecificationProperty"]], result)

    @builtins.property
    def stream_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.StreamSpecificationProperty"]]:
        '''The settings for the DynamoDB table stream, which captures changes to items stored in the table.

        Including this property in your AWS CloudFormation template automatically enables streaming.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-streamspecification
        '''
        result = self._values.get("stream_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.StreamSpecificationProperty"]], result)

    @builtins.property
    def table_class(self) -> typing.Optional[builtins.str]:
        '''The table class of the new table.

        Valid values are ``STANDARD`` and ``STANDARD_INFREQUENT_ACCESS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tableclass
        '''
        result = self._values.get("table_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''A name for the table.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the table name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def time_to_live_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.TimeToLiveSpecificationProperty"]]:
        '''Specifies the Time to Live (TTL) settings for the table.

        .. epigraph::

           For detailed information about the limits in DynamoDB, see `Limits in Amazon DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html>`_ in the Amazon DynamoDB Developer Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-timetolivespecification
        '''
        result = self._values.get("time_to_live_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.TimeToLiveSpecificationProperty"]], result)

    @builtins.property
    def warm_throughput(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.WarmThroughputProperty"]]:
        '''Represents the warm throughput (in read units per second and write units per second) for creating a table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-warmthroughput
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
    jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin",
):
    '''The ``AWS::DynamoDB::Table`` resource creates a DynamoDB table. For more information, see `CreateTable <https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_CreateTable.html>`_ in the *Amazon DynamoDB API Reference* .

    You should be aware of the following behaviors when working with DynamoDB tables:

    - AWS CloudFormation typically creates DynamoDB tables in parallel. However, if your template includes multiple DynamoDB tables with indexes, you must declare dependencies so that the tables are created sequentially. Amazon DynamoDB limits the number of tables with secondary indexes that are in the creating state. If you create multiple tables with indexes at the same time, DynamoDB returns an error and the stack operation fails. For an example, see `DynamoDB Table with a DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#aws-resource-dynamodb-table--examples--DynamoDB_Table_with_a_DependsOn_Attribute>`_ .

    .. epigraph::

       Our guidance is to use the latest schema documented for your AWS CloudFormation templates. This schema supports the provisioning of all table settings below. When using this schema in your AWS CloudFormation templates, please ensure that your Identity and Access Management ( IAM ) policies are updated with appropriate permissions to allow for the authorization of these setting changes.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html
    :cloudformationResource: AWS::DynamoDB::Table
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
        
        # policy_document: Any
        
        cfn_table_props_mixin = dynamodb_mixins.CfnTablePropsMixin(dynamodb_mixins.CfnTableMixinProps(
            attribute_definitions=[dynamodb_mixins.CfnTablePropsMixin.AttributeDefinitionProperty(
                attribute_name="attributeName",
                attribute_type="attributeType"
            )],
            billing_mode="billingMode",
            contributor_insights_specification=dynamodb_mixins.CfnTablePropsMixin.ContributorInsightsSpecificationProperty(
                enabled=False,
                mode="mode"
            ),
            deletion_protection_enabled=False,
            global_secondary_indexes=[dynamodb_mixins.CfnTablePropsMixin.GlobalSecondaryIndexProperty(
                contributor_insights_specification=dynamodb_mixins.CfnTablePropsMixin.ContributorInsightsSpecificationProperty(
                    enabled=False,
                    mode="mode"
                ),
                index_name="indexName",
                key_schema=[dynamodb_mixins.CfnTablePropsMixin.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                on_demand_throughput=dynamodb_mixins.CfnTablePropsMixin.OnDemandThroughputProperty(
                    max_read_request_units=123,
                    max_write_request_units=123
                ),
                projection=dynamodb_mixins.CfnTablePropsMixin.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                ),
                provisioned_throughput=dynamodb_mixins.CfnTablePropsMixin.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                ),
                warm_throughput=dynamodb_mixins.CfnTablePropsMixin.WarmThroughputProperty(
                    read_units_per_second=123,
                    write_units_per_second=123
                )
            )],
            import_source_specification=dynamodb_mixins.CfnTablePropsMixin.ImportSourceSpecificationProperty(
                input_compression_type="inputCompressionType",
                input_format="inputFormat",
                input_format_options=dynamodb_mixins.CfnTablePropsMixin.InputFormatOptionsProperty(
                    csv=dynamodb_mixins.CfnTablePropsMixin.CsvProperty(
                        delimiter="delimiter",
                        header_list=["headerList"]
                    )
                ),
                s3_bucket_source=dynamodb_mixins.CfnTablePropsMixin.S3BucketSourceProperty(
                    s3_bucket="s3Bucket",
                    s3_bucket_owner="s3BucketOwner",
                    s3_key_prefix="s3KeyPrefix"
                )
            ),
            key_schema=[dynamodb_mixins.CfnTablePropsMixin.KeySchemaProperty(
                attribute_name="attributeName",
                key_type="keyType"
            )],
            kinesis_stream_specification=dynamodb_mixins.CfnTablePropsMixin.KinesisStreamSpecificationProperty(
                approximate_creation_date_time_precision="approximateCreationDateTimePrecision",
                stream_arn="streamArn"
            ),
            local_secondary_indexes=[dynamodb_mixins.CfnTablePropsMixin.LocalSecondaryIndexProperty(
                index_name="indexName",
                key_schema=[dynamodb_mixins.CfnTablePropsMixin.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                projection=dynamodb_mixins.CfnTablePropsMixin.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                )
            )],
            on_demand_throughput=dynamodb_mixins.CfnTablePropsMixin.OnDemandThroughputProperty(
                max_read_request_units=123,
                max_write_request_units=123
            ),
            point_in_time_recovery_specification=dynamodb_mixins.CfnTablePropsMixin.PointInTimeRecoverySpecificationProperty(
                point_in_time_recovery_enabled=False,
                recovery_period_in_days=123
            ),
            provisioned_throughput=dynamodb_mixins.CfnTablePropsMixin.ProvisionedThroughputProperty(
                read_capacity_units=123,
                write_capacity_units=123
            ),
            resource_policy=dynamodb_mixins.CfnTablePropsMixin.ResourcePolicyProperty(
                policy_document=policy_document
            ),
            sse_specification=dynamodb_mixins.CfnTablePropsMixin.SSESpecificationProperty(
                kms_master_key_id="kmsMasterKeyId",
                sse_enabled=False,
                sse_type="sseType"
            ),
            stream_specification=dynamodb_mixins.CfnTablePropsMixin.StreamSpecificationProperty(
                resource_policy=dynamodb_mixins.CfnTablePropsMixin.ResourcePolicyProperty(
                    policy_document=policy_document
                ),
                stream_view_type="streamViewType"
            ),
            table_class="tableClass",
            table_name="tableName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            time_to_live_specification=dynamodb_mixins.CfnTablePropsMixin.TimeToLiveSpecificationProperty(
                attribute_name="attributeName",
                enabled=False
            ),
            warm_throughput=dynamodb_mixins.CfnTablePropsMixin.WarmThroughputProperty(
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
        '''Create a mixin to apply properties to ``AWS::DynamoDB::Table``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837e0badabebdaa00ca384834c5798a3c72ad815029e67f6ad792d4df2b497ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca7882aaade2e5e9ebda12a8af0a6d4808c4fecc31e51bae72cfb0746e18dafc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090a756886eae0441e803fb77cab2804b4af1ff9b71c7330f5c41cf51eee7aa7)
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
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.AttributeDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "attribute_type": "attributeType",
        },
    )
    class AttributeDefinitionProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            attribute_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents an attribute for describing the schema for the table and indexes.

            :param attribute_name: A name for the attribute.
            :param attribute_type: The data type for the attribute, where:. - ``S`` - the attribute is of type String - ``N`` - the attribute is of type Number - ``B`` - the attribute is of type Binary

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-attributedefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                attribute_definition_property = dynamodb_mixins.CfnTablePropsMixin.AttributeDefinitionProperty(
                    attribute_name="attributeName",
                    attribute_type="attributeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__339655a0289a45a2fb3e7e036553f520218532895cefcb8cff92802cae1c3f33)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument attribute_type", value=attribute_type, expected_type=type_hints["attribute_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if attribute_type is not None:
                self._values["attribute_type"] = attribute_type

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''A name for the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-attributedefinition.html#cfn-dynamodb-table-attributedefinition-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def attribute_type(self) -> typing.Optional[builtins.str]:
            '''The data type for the attribute, where:.

            - ``S`` - the attribute is of type String
            - ``N`` - the attribute is of type Number
            - ``B`` - the attribute is of type Binary

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-attributedefinition.html#cfn-dynamodb-table-attributedefinition-attributetype
            '''
            result = self._values.get("attribute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.ContributorInsightsSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "mode": "mode"},
    )
    class ContributorInsightsSpecificationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures contributor insights settings for a table or one of its indexes.

            :param enabled: Indicates whether CloudWatch Contributor Insights are to be enabled (true) or disabled (false).
            :param mode: Specifies the CloudWatch Contributor Insights mode for a table. Valid values are ``ACCESSED_AND_THROTTLED_KEYS`` (tracks all access and throttled events) or ``THROTTLED_KEYS`` (tracks only throttled events). This setting determines what type of contributor insights data is collected for the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-contributorinsightsspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                contributor_insights_specification_property = dynamodb_mixins.CfnTablePropsMixin.ContributorInsightsSpecificationProperty(
                    enabled=False,
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b11fc104c94194c2b367ff4941890708932d80c69db86ccbe880c989cb15731)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether CloudWatch Contributor Insights are to be enabled (true) or disabled (false).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-contributorinsightsspecification.html#cfn-dynamodb-table-contributorinsightsspecification-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''Specifies the CloudWatch Contributor Insights mode for a table.

            Valid values are ``ACCESSED_AND_THROTTLED_KEYS`` (tracks all access and throttled events) or ``THROTTLED_KEYS`` (tracks only throttled events). This setting determines what type of contributor insights data is collected for the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-contributorinsightsspecification.html#cfn-dynamodb-table-contributorinsightsspecification-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContributorInsightsSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.CsvProperty",
        jsii_struct_bases=[],
        name_mapping={"delimiter": "delimiter", "header_list": "headerList"},
    )
    class CsvProperty:
        def __init__(
            self,
            *,
            delimiter: typing.Optional[builtins.str] = None,
            header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The options for imported source files in CSV format.

            The values are Delimiter and HeaderList.

            :param delimiter: The delimiter used for separating items in the CSV file being imported.
            :param header_list: List of the headers used to specify a common header for all source CSV files being imported. If this field is specified then the first line of each CSV file is treated as data instead of the header. If this field is not specified the the first line of each CSV file is treated as the header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-csv.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                csv_property = dynamodb_mixins.CfnTablePropsMixin.CsvProperty(
                    delimiter="delimiter",
                    header_list=["headerList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ad9b020ca07e271af3c67f669a9cac15b8990c52e823b9b526f83a4f9cb03e7)
                check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
                check_type(argname="argument header_list", value=header_list, expected_type=type_hints["header_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delimiter is not None:
                self._values["delimiter"] = delimiter
            if header_list is not None:
                self._values["header_list"] = header_list

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            '''The delimiter used for separating items in the CSV file being imported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-csv.html#cfn-dynamodb-table-csv-delimiter
            '''
            result = self._values.get("delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of the headers used to specify a common header for all source CSV files being imported.

            If this field is specified then the first line of each CSV file is treated as data instead of the header. If this field is not specified the the first line of each CSV file is treated as the header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-csv.html#cfn-dynamodb-table-csv-headerlist
            '''
            result = self._values.get("header_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CsvProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.GlobalSecondaryIndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "contributor_insights_specification": "contributorInsightsSpecification",
            "index_name": "indexName",
            "key_schema": "keySchema",
            "on_demand_throughput": "onDemandThroughput",
            "projection": "projection",
            "provisioned_throughput": "provisionedThroughput",
            "warm_throughput": "warmThroughput",
        },
    )
    class GlobalSecondaryIndexProperty:
        def __init__(
            self,
            *,
            contributor_insights_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ContributorInsightsSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            index_name: typing.Optional[builtins.str] = None,
            key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            on_demand_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.OnDemandThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            projection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ProjectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ProvisionedThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            warm_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.WarmThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the properties of a global secondary index.

            :param contributor_insights_specification: The settings used to specify whether to enable CloudWatch Contributor Insights for the global table and define which events to monitor.
            :param index_name: The name of the global secondary index. The name must be unique among all other indexes on this table.
            :param key_schema: The complete key schema for a global secondary index, which consists of one or more pairs of attribute names and key types: - ``HASH`` - partition key - ``RANGE`` - sort key > The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. .. epigraph:: The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.
            :param on_demand_throughput: The maximum number of read and write units for the specified global secondary index. If you use this parameter, you must specify ``MaxReadRequestUnits`` , ``MaxWriteRequestUnits`` , or both. You must use either ``OnDemandThroughput`` or ``ProvisionedThroughput`` based on your table's capacity mode.
            :param projection: Represents attributes that are copied (projected) from the table into the global secondary index. These are in addition to the primary key attributes and index key attributes, which are automatically projected.
            :param provisioned_throughput: Represents the provisioned throughput settings for the specified global secondary index. You must use either ``OnDemandThroughput`` or ``ProvisionedThroughput`` based on your table's capacity mode. For current minimum and maximum provisioned throughput values, see `Service, Account, and Table Quotas <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html>`_ in the *Amazon DynamoDB Developer Guide* .
            :param warm_throughput: Represents the warm throughput value (in read units per second and write units per second) for the specified secondary index. If you use this parameter, you must specify ``ReadUnitsPerSecond`` , ``WriteUnitsPerSecond`` , or both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                global_secondary_index_property = dynamodb_mixins.CfnTablePropsMixin.GlobalSecondaryIndexProperty(
                    contributor_insights_specification=dynamodb_mixins.CfnTablePropsMixin.ContributorInsightsSpecificationProperty(
                        enabled=False,
                        mode="mode"
                    ),
                    index_name="indexName",
                    key_schema=[dynamodb_mixins.CfnTablePropsMixin.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    on_demand_throughput=dynamodb_mixins.CfnTablePropsMixin.OnDemandThroughputProperty(
                        max_read_request_units=123,
                        max_write_request_units=123
                    ),
                    projection=dynamodb_mixins.CfnTablePropsMixin.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    ),
                    provisioned_throughput=dynamodb_mixins.CfnTablePropsMixin.ProvisionedThroughputProperty(
                        read_capacity_units=123,
                        write_capacity_units=123
                    ),
                    warm_throughput=dynamodb_mixins.CfnTablePropsMixin.WarmThroughputProperty(
                        read_units_per_second=123,
                        write_units_per_second=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4b07d14869ed7cdf6145761339637271cda9fcc3d69b0591689d6077482d6a7)
                check_type(argname="argument contributor_insights_specification", value=contributor_insights_specification, expected_type=type_hints["contributor_insights_specification"])
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
                check_type(argname="argument on_demand_throughput", value=on_demand_throughput, expected_type=type_hints["on_demand_throughput"])
                check_type(argname="argument projection", value=projection, expected_type=type_hints["projection"])
                check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
                check_type(argname="argument warm_throughput", value=warm_throughput, expected_type=type_hints["warm_throughput"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contributor_insights_specification is not None:
                self._values["contributor_insights_specification"] = contributor_insights_specification
            if index_name is not None:
                self._values["index_name"] = index_name
            if key_schema is not None:
                self._values["key_schema"] = key_schema
            if on_demand_throughput is not None:
                self._values["on_demand_throughput"] = on_demand_throughput
            if projection is not None:
                self._values["projection"] = projection
            if provisioned_throughput is not None:
                self._values["provisioned_throughput"] = provisioned_throughput
            if warm_throughput is not None:
                self._values["warm_throughput"] = warm_throughput

        @builtins.property
        def contributor_insights_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ContributorInsightsSpecificationProperty"]]:
            '''The settings used to specify whether to enable CloudWatch Contributor Insights for the global table and define which events to monitor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-contributorinsightsspecification
            '''
            result = self._values.get("contributor_insights_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ContributorInsightsSpecificationProperty"]], result)

        @builtins.property
        def index_name(self) -> typing.Optional[builtins.str]:
            '''The name of the global secondary index.

            The name must be unique among all other indexes on this table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-indexname
            '''
            result = self._values.get("index_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.KeySchemaProperty"]]]]:
            '''The complete key schema for a global secondary index, which consists of one or more pairs of attribute names and key types:  - ``HASH`` - partition key - ``RANGE`` - sort key  > The partition key of an item is also known as its *hash attribute* .

            The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.
            .. epigraph::

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-keyschema
            '''
            result = self._values.get("key_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.KeySchemaProperty"]]]], result)

        @builtins.property
        def on_demand_throughput(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.OnDemandThroughputProperty"]]:
            '''The maximum number of read and write units for the specified global secondary index.

            If you use this parameter, you must specify ``MaxReadRequestUnits`` , ``MaxWriteRequestUnits`` , or both. You must use either ``OnDemandThroughput`` or ``ProvisionedThroughput`` based on your table's capacity mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-ondemandthroughput
            '''
            result = self._values.get("on_demand_throughput")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.OnDemandThroughputProperty"]], result)

        @builtins.property
        def projection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ProjectionProperty"]]:
            '''Represents attributes that are copied (projected) from the table into the global secondary index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-projection
            '''
            result = self._values.get("projection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ProjectionProperty"]], result)

        @builtins.property
        def provisioned_throughput(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ProvisionedThroughputProperty"]]:
            '''Represents the provisioned throughput settings for the specified global secondary index.

            You must use either ``OnDemandThroughput`` or ``ProvisionedThroughput`` based on your table's capacity mode.

            For current minimum and maximum provisioned throughput values, see `Service, Account, and Table Quotas <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html>`_ in the *Amazon DynamoDB Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-provisionedthroughput
            '''
            result = self._values.get("provisioned_throughput")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ProvisionedThroughputProperty"]], result)

        @builtins.property
        def warm_throughput(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.WarmThroughputProperty"]]:
            '''Represents the warm throughput value (in read units per second and write units per second) for the specified secondary index.

            If you use this parameter, you must specify ``ReadUnitsPerSecond`` , ``WriteUnitsPerSecond`` , or both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-warmthroughput
            '''
            result = self._values.get("warm_throughput")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.WarmThroughputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalSecondaryIndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.ImportSourceSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_compression_type": "inputCompressionType",
            "input_format": "inputFormat",
            "input_format_options": "inputFormatOptions",
            "s3_bucket_source": "s3BucketSource",
        },
    )
    class ImportSourceSpecificationProperty:
        def __init__(
            self,
            *,
            input_compression_type: typing.Optional[builtins.str] = None,
            input_format: typing.Optional[builtins.str] = None,
            input_format_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.InputFormatOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_bucket_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.S3BucketSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the properties of data being imported from the S3 bucket source to the table.

            :param input_compression_type: Type of compression to be used on the input coming from the imported table.
            :param input_format: The format of the source data. Valid values for ``ImportFormat`` are ``CSV`` , ``DYNAMODB_JSON`` or ``ION`` .
            :param input_format_options: Additional properties that specify how the input is formatted,.
            :param s3_bucket_source: The S3 bucket that provides the source for the import.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-importsourcespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                import_source_specification_property = dynamodb_mixins.CfnTablePropsMixin.ImportSourceSpecificationProperty(
                    input_compression_type="inputCompressionType",
                    input_format="inputFormat",
                    input_format_options=dynamodb_mixins.CfnTablePropsMixin.InputFormatOptionsProperty(
                        csv=dynamodb_mixins.CfnTablePropsMixin.CsvProperty(
                            delimiter="delimiter",
                            header_list=["headerList"]
                        )
                    ),
                    s3_bucket_source=dynamodb_mixins.CfnTablePropsMixin.S3BucketSourceProperty(
                        s3_bucket="s3Bucket",
                        s3_bucket_owner="s3BucketOwner",
                        s3_key_prefix="s3KeyPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44646e9a197de3796da7f5326c71455bc0c344bcbaa33f5b054148f0071576fa)
                check_type(argname="argument input_compression_type", value=input_compression_type, expected_type=type_hints["input_compression_type"])
                check_type(argname="argument input_format", value=input_format, expected_type=type_hints["input_format"])
                check_type(argname="argument input_format_options", value=input_format_options, expected_type=type_hints["input_format_options"])
                check_type(argname="argument s3_bucket_source", value=s3_bucket_source, expected_type=type_hints["s3_bucket_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_compression_type is not None:
                self._values["input_compression_type"] = input_compression_type
            if input_format is not None:
                self._values["input_format"] = input_format
            if input_format_options is not None:
                self._values["input_format_options"] = input_format_options
            if s3_bucket_source is not None:
                self._values["s3_bucket_source"] = s3_bucket_source

        @builtins.property
        def input_compression_type(self) -> typing.Optional[builtins.str]:
            '''Type of compression to be used on the input coming from the imported table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-importsourcespecification.html#cfn-dynamodb-table-importsourcespecification-inputcompressiontype
            '''
            result = self._values.get("input_compression_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_format(self) -> typing.Optional[builtins.str]:
            '''The format of the source data.

            Valid values for ``ImportFormat`` are ``CSV`` , ``DYNAMODB_JSON`` or ``ION`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-importsourcespecification.html#cfn-dynamodb-table-importsourcespecification-inputformat
            '''
            result = self._values.get("input_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_format_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.InputFormatOptionsProperty"]]:
            '''Additional properties that specify how the input is formatted,.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-importsourcespecification.html#cfn-dynamodb-table-importsourcespecification-inputformatoptions
            '''
            result = self._values.get("input_format_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.InputFormatOptionsProperty"]], result)

        @builtins.property
        def s3_bucket_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.S3BucketSourceProperty"]]:
            '''The S3 bucket that provides the source for the import.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-importsourcespecification.html#cfn-dynamodb-table-importsourcespecification-s3bucketsource
            '''
            result = self._values.get("s3_bucket_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.S3BucketSourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImportSourceSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.InputFormatOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"csv": "csv"},
    )
    class InputFormatOptionsProperty:
        def __init__(
            self,
            *,
            csv: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.CsvProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The format options for the data that was imported into the target table.

            There is one value, CsvOption.

            :param csv: The options for imported source files in CSV format. The values are Delimiter and HeaderList.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-inputformatoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                input_format_options_property = dynamodb_mixins.CfnTablePropsMixin.InputFormatOptionsProperty(
                    csv=dynamodb_mixins.CfnTablePropsMixin.CsvProperty(
                        delimiter="delimiter",
                        header_list=["headerList"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4af2acdf9a386cd6eee999b63e2d90f809c74011bf9e4693b4d9a1c96eb1a779)
                check_type(argname="argument csv", value=csv, expected_type=type_hints["csv"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if csv is not None:
                self._values["csv"] = csv

        @builtins.property
        def csv(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.CsvProperty"]]:
            '''The options for imported source files in CSV format.

            The values are Delimiter and HeaderList.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-inputformatoptions.html#cfn-dynamodb-table-inputformatoptions-csv
            '''
            result = self._values.get("csv")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.CsvProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputFormatOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.KeySchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_name": "attributeName", "key_type": "keyType"},
    )
    class KeySchemaProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents *a single element* of a key schema.

            A key schema specifies the attributes that make up the primary key of a table, or the key attributes of an index.

            A ``KeySchemaElement`` represents exactly one attribute of the primary key. For example, a simple primary key would be represented by one ``KeySchemaElement`` (for the partition key). A composite primary key would require one ``KeySchemaElement`` for the partition key, and another ``KeySchemaElement`` for the sort key.

            A ``KeySchemaElement`` must be a scalar, top-level attribute (not a nested attribute). The data type must be one of String, Number, or Binary. The attribute cannot be nested within a List or a Map.

            :param attribute_name: The name of a key attribute.
            :param key_type: The role that this key attribute will assume:. - ``HASH`` - partition key - ``RANGE`` - sort key .. epigraph:: The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-keyschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                key_schema_property = dynamodb_mixins.CfnTablePropsMixin.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d62171286374e13bf43f12c0cfb2babc07a0961df338aff1ff75218d59cefdf)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if key_type is not None:
                self._values["key_type"] = key_type

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''The name of a key attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-keyschema.html#cfn-dynamodb-table-keyschema-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''The role that this key attribute will assume:.

            - ``HASH`` - partition key
            - ``RANGE`` - sort key

            .. epigraph::

               The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-keyschema.html#cfn-dynamodb-table-keyschema-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeySchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.KinesisStreamSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "approximate_creation_date_time_precision": "approximateCreationDateTimePrecision",
            "stream_arn": "streamArn",
        },
    )
    class KinesisStreamSpecificationProperty:
        def __init__(
            self,
            *,
            approximate_creation_date_time_precision: typing.Optional[builtins.str] = None,
            stream_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Kinesis Data Streams configuration for the specified table.

            :param approximate_creation_date_time_precision: The precision for the time and date that the stream was created.
            :param stream_arn: The ARN for a specific Kinesis data stream. Length Constraints: Minimum length of 37. Maximum length of 1024.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-kinesisstreamspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                kinesis_stream_specification_property = dynamodb_mixins.CfnTablePropsMixin.KinesisStreamSpecificationProperty(
                    approximate_creation_date_time_precision="approximateCreationDateTimePrecision",
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88766615196f02b1f95f9a2252a4f633d38a19714522417b74e5fba850eb89c3)
                check_type(argname="argument approximate_creation_date_time_precision", value=approximate_creation_date_time_precision, expected_type=type_hints["approximate_creation_date_time_precision"])
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if approximate_creation_date_time_precision is not None:
                self._values["approximate_creation_date_time_precision"] = approximate_creation_date_time_precision
            if stream_arn is not None:
                self._values["stream_arn"] = stream_arn

        @builtins.property
        def approximate_creation_date_time_precision(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The precision for the time and date that the stream was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-kinesisstreamspecification.html#cfn-dynamodb-table-kinesisstreamspecification-approximatecreationdatetimeprecision
            '''
            result = self._values.get("approximate_creation_date_time_precision")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN for a specific Kinesis data stream.

            Length Constraints: Minimum length of 37. Maximum length of 1024.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-kinesisstreamspecification.html#cfn-dynamodb-table-kinesisstreamspecification-streamarn
            '''
            result = self._values.get("stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.LocalSecondaryIndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "key_schema": "keySchema",
            "projection": "projection",
        },
    )
    class LocalSecondaryIndexProperty:
        def __init__(
            self,
            *,
            index_name: typing.Optional[builtins.str] = None,
            key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            projection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ProjectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the properties of a local secondary index.

            A local secondary index can only be created when its parent table is created.

            :param index_name: The name of the local secondary index. The name must be unique among all other indexes on this table.
            :param key_schema: The complete key schema for the local secondary index, consisting of one or more pairs of attribute names and key types: - ``HASH`` - partition key - ``RANGE`` - sort key > The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. .. epigraph:: The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.
            :param projection: Represents attributes that are copied (projected) from the table into the local secondary index. These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-localsecondaryindex.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                local_secondary_index_property = dynamodb_mixins.CfnTablePropsMixin.LocalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb_mixins.CfnTablePropsMixin.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb_mixins.CfnTablePropsMixin.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abd0f002d5461d6bd7f002dbdc4851c05a7323bf65c667d9072f793c5af4b1bf)
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
                check_type(argname="argument projection", value=projection, expected_type=type_hints["projection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if index_name is not None:
                self._values["index_name"] = index_name
            if key_schema is not None:
                self._values["key_schema"] = key_schema
            if projection is not None:
                self._values["projection"] = projection

        @builtins.property
        def index_name(self) -> typing.Optional[builtins.str]:
            '''The name of the local secondary index.

            The name must be unique among all other indexes on this table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-localsecondaryindex.html#cfn-dynamodb-table-localsecondaryindex-indexname
            '''
            result = self._values.get("index_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.KeySchemaProperty"]]]]:
            '''The complete key schema for the local secondary index, consisting of one or more pairs of attribute names and key types:  - ``HASH`` - partition key - ``RANGE`` - sort key  > The partition key of an item is also known as its *hash attribute* .

            The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.
            .. epigraph::

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-localsecondaryindex.html#cfn-dynamodb-table-localsecondaryindex-keyschema
            '''
            result = self._values.get("key_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.KeySchemaProperty"]]]], result)

        @builtins.property
        def projection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ProjectionProperty"]]:
            '''Represents attributes that are copied (projected) from the table into the local secondary index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-localsecondaryindex.html#cfn-dynamodb-table-localsecondaryindex-projection
            '''
            result = self._values.get("projection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ProjectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalSecondaryIndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.OnDemandThroughputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_read_request_units": "maxReadRequestUnits",
            "max_write_request_units": "maxWriteRequestUnits",
        },
    )
    class OnDemandThroughputProperty:
        def __init__(
            self,
            *,
            max_read_request_units: typing.Optional[jsii.Number] = None,
            max_write_request_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Sets the maximum number of read and write units for the specified on-demand table.

            If you use this property, you must specify ``MaxReadRequestUnits`` , ``MaxWriteRequestUnits`` , or both.

            :param max_read_request_units: Maximum number of read request units for the specified table. To specify a maximum ``OnDemandThroughput`` on your table, set the value of ``MaxReadRequestUnits`` as greater than or equal to 1. To remove the maximum ``OnDemandThroughput`` that is currently set on your table, set the value of ``MaxReadRequestUnits`` to -1.
            :param max_write_request_units: Maximum number of write request units for the specified table. To specify a maximum ``OnDemandThroughput`` on your table, set the value of ``MaxWriteRequestUnits`` as greater than or equal to 1. To remove the maximum ``OnDemandThroughput`` that is currently set on your table, set the value of ``MaxWriteRequestUnits`` to -1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ondemandthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                on_demand_throughput_property = dynamodb_mixins.CfnTablePropsMixin.OnDemandThroughputProperty(
                    max_read_request_units=123,
                    max_write_request_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9657fa047b3ea84481b14837aa2d22f16a95bef921c260bdea6d5ed7a7eeb775)
                check_type(argname="argument max_read_request_units", value=max_read_request_units, expected_type=type_hints["max_read_request_units"])
                check_type(argname="argument max_write_request_units", value=max_write_request_units, expected_type=type_hints["max_write_request_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_read_request_units is not None:
                self._values["max_read_request_units"] = max_read_request_units
            if max_write_request_units is not None:
                self._values["max_write_request_units"] = max_write_request_units

        @builtins.property
        def max_read_request_units(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of read request units for the specified table.

            To specify a maximum ``OnDemandThroughput`` on your table, set the value of ``MaxReadRequestUnits`` as greater than or equal to 1. To remove the maximum ``OnDemandThroughput`` that is currently set on your table, set the value of ``MaxReadRequestUnits`` to -1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ondemandthroughput.html#cfn-dynamodb-table-ondemandthroughput-maxreadrequestunits
            '''
            result = self._values.get("max_read_request_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_write_request_units(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of write request units for the specified table.

            To specify a maximum ``OnDemandThroughput`` on your table, set the value of ``MaxWriteRequestUnits`` as greater than or equal to 1. To remove the maximum ``OnDemandThroughput`` that is currently set on your table, set the value of ``MaxWriteRequestUnits`` to -1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ondemandthroughput.html#cfn-dynamodb-table-ondemandthroughput-maxwriterequestunits
            '''
            result = self._values.get("max_write_request_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnDemandThroughputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.PointInTimeRecoverySpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "point_in_time_recovery_enabled": "pointInTimeRecoveryEnabled",
            "recovery_period_in_days": "recoveryPeriodInDays",
        },
    )
    class PointInTimeRecoverySpecificationProperty:
        def __init__(
            self,
            *,
            point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            recovery_period_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The settings used to enable point in time recovery.

            :param point_in_time_recovery_enabled: Indicates whether point in time recovery is enabled (true) or disabled (false) on the table.
            :param recovery_period_in_days: The number of preceding days for which continuous backups are taken and maintained. Your table data is only recoverable to any point-in-time from within the configured recovery period. This parameter is optional. If no value is provided, the value will default to 35.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-pointintimerecoveryspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                point_in_time_recovery_specification_property = dynamodb_mixins.CfnTablePropsMixin.PointInTimeRecoverySpecificationProperty(
                    point_in_time_recovery_enabled=False,
                    recovery_period_in_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a9ebdaa3445699b295d7877742c6cd9d9b6fffb1b71bbc8f4a5b540f4d0681da)
                check_type(argname="argument point_in_time_recovery_enabled", value=point_in_time_recovery_enabled, expected_type=type_hints["point_in_time_recovery_enabled"])
                check_type(argname="argument recovery_period_in_days", value=recovery_period_in_days, expected_type=type_hints["recovery_period_in_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if point_in_time_recovery_enabled is not None:
                self._values["point_in_time_recovery_enabled"] = point_in_time_recovery_enabled
            if recovery_period_in_days is not None:
                self._values["recovery_period_in_days"] = recovery_period_in_days

        @builtins.property
        def point_in_time_recovery_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether point in time recovery is enabled (true) or disabled (false) on the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-pointintimerecoveryspecification.html#cfn-dynamodb-table-pointintimerecoveryspecification-pointintimerecoveryenabled
            '''
            result = self._values.get("point_in_time_recovery_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def recovery_period_in_days(self) -> typing.Optional[jsii.Number]:
            '''The number of preceding days for which continuous backups are taken and maintained.

            Your table data is only recoverable to any point-in-time from within the configured recovery period. This parameter is optional. If no value is provided, the value will default to 35.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-pointintimerecoveryspecification.html#cfn-dynamodb-table-pointintimerecoveryspecification-recoveryperiodindays
            '''
            result = self._values.get("recovery_period_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PointInTimeRecoverySpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.ProjectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "non_key_attributes": "nonKeyAttributes",
            "projection_type": "projectionType",
        },
    )
    class ProjectionProperty:
        def __init__(
            self,
            *,
            non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
            projection_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents attributes that are copied (projected) from the table into an index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :param non_key_attributes: Represents the non-key attribute names which will be projected into the index. For global and local secondary indexes, the total count of ``NonKeyAttributes`` summed across all of the secondary indexes, must not exceed 100. If you project the same attribute into two different indexes, this counts as two distinct attributes when determining the total. This limit only applies when you specify the ProjectionType of ``INCLUDE`` . You still can specify the ProjectionType of ``ALL`` to project all attributes from the source table, even if the table has more than 100 attributes.
            :param projection_type: The set of attributes that are projected into the index:. - ``KEYS_ONLY`` - Only the index and primary keys are projected into the index. - ``INCLUDE`` - In addition to the attributes described in ``KEYS_ONLY`` , the secondary index will include other non-key attributes that you specify. - ``ALL`` - All of the table attributes are projected into the index. When using the DynamoDB console, ``ALL`` is selected by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-projection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                projection_property = dynamodb_mixins.CfnTablePropsMixin.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f3c34c9815eda98df6abc91190c0815839f78678ef0fcb22088f16df8447596)
                check_type(argname="argument non_key_attributes", value=non_key_attributes, expected_type=type_hints["non_key_attributes"])
                check_type(argname="argument projection_type", value=projection_type, expected_type=type_hints["projection_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if non_key_attributes is not None:
                self._values["non_key_attributes"] = non_key_attributes
            if projection_type is not None:
                self._values["projection_type"] = projection_type

        @builtins.property
        def non_key_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents the non-key attribute names which will be projected into the index.

            For global and local secondary indexes, the total count of ``NonKeyAttributes`` summed across all of the secondary indexes, must not exceed 100. If you project the same attribute into two different indexes, this counts as two distinct attributes when determining the total. This limit only applies when you specify the ProjectionType of ``INCLUDE`` . You still can specify the ProjectionType of ``ALL`` to project all attributes from the source table, even if the table has more than 100 attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-projection.html#cfn-dynamodb-table-projection-nonkeyattributes
            '''
            result = self._values.get("non_key_attributes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def projection_type(self) -> typing.Optional[builtins.str]:
            '''The set of attributes that are projected into the index:.

            - ``KEYS_ONLY`` - Only the index and primary keys are projected into the index.
            - ``INCLUDE`` - In addition to the attributes described in ``KEYS_ONLY`` , the secondary index will include other non-key attributes that you specify.
            - ``ALL`` - All of the table attributes are projected into the index.

            When using the DynamoDB console, ``ALL`` is selected by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-projection.html#cfn-dynamodb-table-projection-projectiontype
            '''
            result = self._values.get("projection_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.ProvisionedThroughputProperty",
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
            '''Throughput for the specified table, which consists of values for ``ReadCapacityUnits`` and ``WriteCapacityUnits`` .

            For more information about the contents of a provisioned throughput structure, see `Amazon DynamoDB Table ProvisionedThroughput <https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ProvisionedThroughput.html>`_ .

            :param read_capacity_units: The maximum number of strongly consistent reads consumed per second before DynamoDB returns a ``ThrottlingException`` . For more information, see `Specifying Read and Write Requirements <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html>`_ in the *Amazon DynamoDB Developer Guide* . If read/write capacity mode is ``PAY_PER_REQUEST`` the value is set to 0.
            :param write_capacity_units: The maximum number of writes consumed per second before DynamoDB returns a ``ThrottlingException`` . For more information, see `Specifying Read and Write Requirements <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html>`_ in the *Amazon DynamoDB Developer Guide* . If read/write capacity mode is ``PAY_PER_REQUEST`` the value is set to 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-provisionedthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                provisioned_throughput_property = dynamodb_mixins.CfnTablePropsMixin.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0226e210f2b013e7882a83790c33ea4ae1f43187d6b855dea9297f3ac8dbb60)
                check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
                check_type(argname="argument write_capacity_units", value=write_capacity_units, expected_type=type_hints["write_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if read_capacity_units is not None:
                self._values["read_capacity_units"] = read_capacity_units
            if write_capacity_units is not None:
                self._values["write_capacity_units"] = write_capacity_units

        @builtins.property
        def read_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of strongly consistent reads consumed per second before DynamoDB returns a ``ThrottlingException`` .

            For more information, see `Specifying Read and Write Requirements <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html>`_ in the *Amazon DynamoDB Developer Guide* .

            If read/write capacity mode is ``PAY_PER_REQUEST`` the value is set to 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-provisionedthroughput.html#cfn-dynamodb-table-provisionedthroughput-readcapacityunits
            '''
            result = self._values.get("read_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def write_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of writes consumed per second before DynamoDB returns a ``ThrottlingException`` .

            For more information, see `Specifying Read and Write Requirements <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html>`_ in the *Amazon DynamoDB Developer Guide* .

            If read/write capacity mode is ``PAY_PER_REQUEST`` the value is set to 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-provisionedthroughput.html#cfn-dynamodb-table-provisionedthroughput-writecapacityunits
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
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.ResourcePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"policy_document": "policyDocument"},
    )
    class ResourcePolicyProperty:
        def __init__(self, *, policy_document: typing.Any = None) -> None:
            '''Creates or updates a resource-based policy document that contains the permissions for DynamoDB resources, such as a table, its indexes, and stream.

            Resource-based policies let you define access permissions by specifying who has access to each resource, and the actions they are allowed to perform on each resource.

            In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .

            While defining resource-based policies in your CloudFormation templates, the following considerations apply:

            - The maximum size supported for a resource-based policy document in JSON format is 20 KB. DynamoDB counts whitespaces when calculating the size of a policy against this limit.
            - Resource-based policies don't support `drift detection <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html#>`_ . If you update a policy outside of the CloudFormation stack template, you'll need to update the CloudFormation stack with the changes.
            - Resource-based policies don't support out-of-band changes. If you add, update, or delete a policy outside of the CloudFormation template, the change won't be overwritten if there are no changes to the policy within the template.

            For example, say that your template contains a resource-based policy, which you later update outside of the template. If you don't make any changes to the policy in the template, the updated policy in DynamoDB won’t be synced with the policy in the template.

            Conversely, say that your template doesn’t contain a resource-based policy, but you add a policy outside of the template. This policy won’t be removed from DynamoDB as long as you don’t add it to the template. When you add a policy to the template and update the stack, the existing policy in DynamoDB will be updated to match the one defined in the template.

            For a full list of all considerations, see `Resource-based policy considerations <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-considerations.html>`_ .

            :param policy_document: A resource-based policy document that contains permissions to add to the specified DynamoDB table, index, or both. In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-resourcepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                # policy_document: Any
                
                resource_policy_property = dynamodb_mixins.CfnTablePropsMixin.ResourcePolicyProperty(
                    policy_document=policy_document
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2398ae9cad7279612b6e1cd482efe224ba8613fb64aa2a647dd2573773ce9e44)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_document is not None:
                self._values["policy_document"] = policy_document

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''A resource-based policy document that contains permissions to add to the specified DynamoDB table, index, or both.

            In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-resourcepolicy.html#cfn-dynamodb-table-resourcepolicy-policydocument
            '''
            result = self._values.get("policy_document")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourcePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.S3BucketSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket": "s3Bucket",
            "s3_bucket_owner": "s3BucketOwner",
            "s3_key_prefix": "s3KeyPrefix",
        },
    )
    class S3BucketSourceProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_bucket_owner: typing.Optional[builtins.str] = None,
            s3_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 bucket that is being imported from.

            :param s3_bucket: The S3 bucket that is being imported from.
            :param s3_bucket_owner: The account number of the S3 bucket that is being imported from. If the bucket is owned by the requester this is optional.
            :param s3_key_prefix: The key prefix shared by all S3 Objects that are being imported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-s3bucketsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                s3_bucket_source_property = dynamodb_mixins.CfnTablePropsMixin.S3BucketSourceProperty(
                    s3_bucket="s3Bucket",
                    s3_bucket_owner="s3BucketOwner",
                    s3_key_prefix="s3KeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6551833d002e3321431507b119120c6e52ef340d123bdbc2441680d80abc6505)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_bucket_owner", value=s3_bucket_owner, expected_type=type_hints["s3_bucket_owner"])
                check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_bucket_owner is not None:
                self._values["s3_bucket_owner"] = s3_bucket_owner
            if s3_key_prefix is not None:
                self._values["s3_key_prefix"] = s3_key_prefix

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket that is being imported from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-s3bucketsource.html#cfn-dynamodb-table-s3bucketsource-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The account number of the S3 bucket that is being imported from.

            If the bucket is owned by the requester this is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-s3bucketsource.html#cfn-dynamodb-table-s3bucketsource-s3bucketowner
            '''
            result = self._values.get("s3_bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The key prefix shared by all S3 Objects that are being imported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-s3bucketsource.html#cfn-dynamodb-table-s3bucketsource-s3keyprefix
            '''
            result = self._values.get("s3_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_master_key_id": "kmsMasterKeyId",
            "sse_enabled": "sseEnabled",
            "sse_type": "sseType",
        },
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            kms_master_key_id: typing.Optional[builtins.str] = None,
            sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            sse_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the settings used to enable server-side encryption.

            :param kms_master_key_id: The AWS key that should be used for the AWS encryption. To specify a key, use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. Note that you should only provide this parameter if the key is different from the default DynamoDB key ``alias/aws/dynamodb`` .
            :param sse_enabled: Indicates whether server-side encryption is done using an AWS managed key or an AWS owned key. If enabled (true), server-side encryption type is set to ``KMS`` and an AWS managed key is used ( AWS charges apply). If disabled (false) or not specified, server-side encryption is set to AWS owned key.
            :param sse_type: Server-side encryption type. The only supported value is:. - ``KMS`` - Server-side encryption that uses AWS Key Management Service . The key is stored in your account and is managed by AWS ( AWS charges apply).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                s_sESpecification_property = dynamodb_mixins.CfnTablePropsMixin.SSESpecificationProperty(
                    kms_master_key_id="kmsMasterKeyId",
                    sse_enabled=False,
                    sse_type="sseType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9696b7b05976aa142ecdff24ea3265e252ea8dfd9c83e59bf2f30cddd63ddd0)
                check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
                check_type(argname="argument sse_enabled", value=sse_enabled, expected_type=type_hints["sse_enabled"])
                check_type(argname="argument sse_type", value=sse_type, expected_type=type_hints["sse_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_master_key_id is not None:
                self._values["kms_master_key_id"] = kms_master_key_id
            if sse_enabled is not None:
                self._values["sse_enabled"] = sse_enabled
            if sse_type is not None:
                self._values["sse_type"] = sse_type

        @builtins.property
        def kms_master_key_id(self) -> typing.Optional[builtins.str]:
            '''The AWS  key that should be used for the AWS  encryption.

            To specify a key, use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. Note that you should only provide this parameter if the key is different from the default DynamoDB key ``alias/aws/dynamodb`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html#cfn-dynamodb-table-ssespecification-kmsmasterkeyid
            '''
            result = self._values.get("kms_master_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sse_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether server-side encryption is done using an AWS managed key or an AWS owned key.

            If enabled (true), server-side encryption type is set to ``KMS`` and an AWS managed key is used ( AWS  charges apply). If disabled (false) or not specified, server-side encryption is set to AWS owned key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html#cfn-dynamodb-table-ssespecification-sseenabled
            '''
            result = self._values.get("sse_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def sse_type(self) -> typing.Optional[builtins.str]:
            '''Server-side encryption type. The only supported value is:.

            - ``KMS`` - Server-side encryption that uses AWS Key Management Service . The key is stored in your account and is managed by AWS  ( AWS  charges apply).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html#cfn-dynamodb-table-ssespecification-ssetype
            '''
            result = self._values.get("sse_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.StreamSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_policy": "resourcePolicy",
            "stream_view_type": "streamViewType",
        },
    )
    class StreamSpecificationProperty:
        def __init__(
            self,
            *,
            resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ResourcePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stream_view_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the DynamoDB Streams configuration for a table in DynamoDB.

            :param resource_policy: Creates or updates a resource-based policy document that contains the permissions for DynamoDB resources, such as a table's streams. Resource-based policies let you define access permissions by specifying who has access to each resource, and the actions they are allowed to perform on each resource. .. epigraph:: When you remove the ``StreamSpecification`` property from the template, DynamoDB disables the stream but retains any attached resource policy until the stream is deleted after 24 hours. When you modify the ``StreamViewType`` property, DynamoDB creates a new stream and retains the old stream's resource policy. The old stream and its resource policy are deleted after the 24-hour retention period. In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .
            :param stream_view_type: When an item in the table is modified, ``StreamViewType`` determines what information is written to the stream for this table. Valid values for ``StreamViewType`` are: - ``KEYS_ONLY`` - Only the key attributes of the modified item are written to the stream. - ``NEW_IMAGE`` - The entire item, as it appears after it was modified, is written to the stream. - ``OLD_IMAGE`` - The entire item, as it appeared before it was modified, is written to the stream. - ``NEW_AND_OLD_IMAGES`` - Both the new and the old item images of the item are written to the stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-streamspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                # policy_document: Any
                
                stream_specification_property = dynamodb_mixins.CfnTablePropsMixin.StreamSpecificationProperty(
                    resource_policy=dynamodb_mixins.CfnTablePropsMixin.ResourcePolicyProperty(
                        policy_document=policy_document
                    ),
                    stream_view_type="streamViewType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f018e3c029fa6bef69320b13657979bd6760d06d83e980c1d5baa3b627a78ba)
                check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
                check_type(argname="argument stream_view_type", value=stream_view_type, expected_type=type_hints["stream_view_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_policy is not None:
                self._values["resource_policy"] = resource_policy
            if stream_view_type is not None:
                self._values["stream_view_type"] = stream_view_type

        @builtins.property
        def resource_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ResourcePolicyProperty"]]:
            '''Creates or updates a resource-based policy document that contains the permissions for DynamoDB resources, such as a table's streams.

            Resource-based policies let you define access permissions by specifying who has access to each resource, and the actions they are allowed to perform on each resource.
            .. epigraph::

               When you remove the ``StreamSpecification`` property from the template, DynamoDB disables the stream but retains any attached resource policy until the stream is deleted after 24 hours. When you modify the ``StreamViewType`` property, DynamoDB creates a new stream and retains the old stream's resource policy. The old stream and its resource policy are deleted after the 24-hour retention period.

            In a CloudFormation template, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to DynamoDB . For more information about resource-based policies, see `Using resource-based policies for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html>`_ and `Resource-based policy examples <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-examples.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-streamspecification.html#cfn-dynamodb-table-streamspecification-resourcepolicy
            '''
            result = self._values.get("resource_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ResourcePolicyProperty"]], result)

        @builtins.property
        def stream_view_type(self) -> typing.Optional[builtins.str]:
            '''When an item in the table is modified, ``StreamViewType`` determines what information is written to the stream for this table.

            Valid values for ``StreamViewType`` are:

            - ``KEYS_ONLY`` - Only the key attributes of the modified item are written to the stream.
            - ``NEW_IMAGE`` - The entire item, as it appears after it was modified, is written to the stream.
            - ``OLD_IMAGE`` - The entire item, as it appeared before it was modified, is written to the stream.
            - ``NEW_AND_OLD_IMAGES`` - Both the new and the old item images of the item are written to the stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-streamspecification.html#cfn-dynamodb-table-streamspecification-streamviewtype
            '''
            result = self._values.get("stream_view_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.TimeToLiveSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_name": "attributeName", "enabled": "enabled"},
    )
    class TimeToLiveSpecificationProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Represents the settings used to enable or disable Time to Live (TTL) for the specified table.

            :param attribute_name: The name of the TTL attribute used to store the expiration time for items in the table. .. epigraph:: - The ``AttributeName`` property is required when enabling the TTL, or when TTL is already enabled. - To update this property, you must first disable TTL and then enable TTL with the new attribute name.
            :param enabled: Indicates whether TTL is to be enabled (true) or disabled (false) on the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-timetolivespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                time_to_live_specification_property = dynamodb_mixins.CfnTablePropsMixin.TimeToLiveSpecificationProperty(
                    attribute_name="attributeName",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__adbdcb49d1622b8066a9b707435bbe954fd9968075b58c4c807a52705e35c943)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''The name of the TTL attribute used to store the expiration time for items in the table.

            .. epigraph::

               - The ``AttributeName`` property is required when enabling the TTL, or when TTL is already enabled.
               - To update this property, you must first disable TTL and then enable TTL with the new attribute name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-timetolivespecification.html#cfn-dynamodb-table-timetolivespecification-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether TTL is to be enabled (true) or disabled (false) on the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-timetolivespecification.html#cfn-dynamodb-table-timetolivespecification-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeToLiveSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_dynamodb.mixins.CfnTablePropsMixin.WarmThroughputProperty",
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
            '''Provides visibility into the number of read and write operations your table or secondary index can instantaneously support.

            The settings can be modified using the ``UpdateTable`` operation to meet the throughput requirements of an upcoming peak event.

            :param read_units_per_second: Represents the number of read operations your base table can instantaneously support.
            :param write_units_per_second: Represents the number of write operations your base table can instantaneously support.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-warmthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dynamodb import mixins as dynamodb_mixins
                
                warm_throughput_property = dynamodb_mixins.CfnTablePropsMixin.WarmThroughputProperty(
                    read_units_per_second=123,
                    write_units_per_second=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1020daa1c0e7245bc963e6a630eda00c8f8c3d418845202c7250942ef4b62f93)
                check_type(argname="argument read_units_per_second", value=read_units_per_second, expected_type=type_hints["read_units_per_second"])
                check_type(argname="argument write_units_per_second", value=write_units_per_second, expected_type=type_hints["write_units_per_second"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if read_units_per_second is not None:
                self._values["read_units_per_second"] = read_units_per_second
            if write_units_per_second is not None:
                self._values["write_units_per_second"] = write_units_per_second

        @builtins.property
        def read_units_per_second(self) -> typing.Optional[jsii.Number]:
            '''Represents the number of read operations your base table can instantaneously support.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-warmthroughput.html#cfn-dynamodb-table-warmthroughput-readunitspersecond
            '''
            result = self._values.get("read_units_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def write_units_per_second(self) -> typing.Optional[jsii.Number]:
            '''Represents the number of write operations your base table can instantaneously support.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-warmthroughput.html#cfn-dynamodb-table-warmthroughput-writeunitspersecond
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


__all__ = [
    "CfnGlobalTableMixinProps",
    "CfnGlobalTablePropsMixin",
    "CfnTableMixinProps",
    "CfnTablePropsMixin",
]

publication.publish()

def _typecheckingstub__3a529924f192b1a70167f8c6f33b8112dc78c264381cbfcae636dc03c938367e(
    *,
    attribute_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.AttributeDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    billing_mode: typing.Optional[builtins.str] = None,
    global_secondary_indexes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.GlobalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    global_table_witnesses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.GlobalTableWitnessProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    local_secondary_indexes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.LocalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    multi_region_consistency: typing.Optional[builtins.str] = None,
    replicas: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ReplicaSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    sse_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stream_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.StreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
    time_to_live_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.TimeToLiveSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    warm_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.WarmThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    write_on_demand_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    write_provisioned_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab7e8de4fc74a8bcf8770715be06ab6d9f2d070219ee9884bc638cb007f2d1a(
    props: typing.Union[CfnGlobalTableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b064a7522a47b5097a2d24437aa4b7444f6e04bf550fe286bfb667703347c6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bcaf9113dda045b083eeb0ba8358b36151ccc8d8567f763648e1dfe67b3adcd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204a72cf6e6dbaa744d9d7f0645bfe47e2a19d4ae49f1a2a1b9051275ee0e09a(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    attribute_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c051f75cad5170a2ba829b2b85a80a32cdfbbee12635853a7c0a88a9a9ee5841(
    *,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    seed_capacity: typing.Optional[jsii.Number] = None,
    target_tracking_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.TargetTrackingScalingPolicyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1720689debbdd915fae0ee643675f7868dba2a5e4b01938b225c613df75b0dc(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f202db1f26da98bd43b7623c9ff69995cfd62a67be10cac01d011b8bb481e46(
    *,
    index_name: typing.Optional[builtins.str] = None,
    key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    projection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ProjectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    warm_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.WarmThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    write_on_demand_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.WriteOnDemandThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    write_provisioned_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.WriteProvisionedThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1a193e67d234e6d50719f93e5c29e0a34dda41c47dbce1adf2c79205ba493c(
    *,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c09cc1b5de671e78f61174c63947436bfd361024fbe370f598e301a8201b1d(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42edeadc55621a666495f7d3bd73b8496227b65289bb241815fc3552c98cec81(
    *,
    approximate_creation_date_time_precision: typing.Optional[builtins.str] = None,
    stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36983d83385e7964ba443990785b94ba16270dc90874f9f1169a60ec674c9d2a(
    *,
    index_name: typing.Optional[builtins.str] = None,
    key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    projection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ProjectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18e14874b35a241ccfc1307e08ca6c43d4055c4fa97736919a2afd740abb8f4(
    *,
    point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    recovery_period_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2566d939cb91c39cdb451bec80c2dc379522559b1bd0b8ed906fb8a7bd089ad7(
    *,
    non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    projection_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f200eb9addeed59699ee79e3f5fedb3b577e55d50c8d84b2225d2ba23e3e095(
    *,
    max_read_request_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998a788ab936b30ac1ab33129312acad18dbda2183d6e078b11649ca909f2d93(
    *,
    read_capacity_auto_scaling_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    read_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6dc86236431dfce98217d97f5021ff40f97dadc3e66a4783b4ce3635af9ee4d(
    *,
    contributor_insights_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    index_name: typing.Optional[builtins.str] = None,
    read_on_demand_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    read_provisioned_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22350277eb58d83f4972592a2a3071af1c1e55d64eb0eec247f08c6e9e975cee(
    *,
    kms_master_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8fc43b5fa89b6051cfe199f720ab167b0ee20b95635442f1175146a1a5caa3b(
    *,
    contributor_insights_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ContributorInsightsSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    global_secondary_indexes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ReplicaGlobalSecondaryIndexSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    kinesis_stream_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.KinesisStreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    point_in_time_recovery_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.PointInTimeRecoverySpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    read_on_demand_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ReadOnDemandThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    read_provisioned_throughput_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ReadProvisionedThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    region: typing.Optional[builtins.str] = None,
    replica_stream_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ReplicaStreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ResourcePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sse_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ReplicaSSESpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_class: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ad60331c76a840512b1aeba254cb2be4b7cf989bffd858a780720a774c8cd1(
    *,
    resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.ResourcePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34515d1180d2f218918968b2a0fbce07d80728e15e3946a929a7e7c8c1c73d16(
    *,
    policy_document: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23dda535fd15a1f4c35a5c9821633b7cf92e2f3d1c0a5549100ffe31f36b4cf7(
    *,
    sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    sse_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27ad7c3145f52d23ed4e3849e6b91a9e114eda88631833f4686f37c1f698b97(
    *,
    stream_view_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d13e6c1b4568d79d978066c3ad4993e50c25aebc2eb02b2e759e34cff0e132(
    *,
    disable_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    scale_in_cooldown: typing.Optional[jsii.Number] = None,
    scale_out_cooldown: typing.Optional[jsii.Number] = None,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9864f704e8a9699286d902d9da30315911168cece8859e7bb11472851b0609f5(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a590116c1bcca33645e4b3251e0d1223e7a48ee0f7029871ec8eb615f206c432(
    *,
    read_units_per_second: typing.Optional[jsii.Number] = None,
    write_units_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecd5c92cb7d71a337f68acf140fd13d8f1ea93da940a5eb61cf700a26949d86(
    *,
    max_write_request_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60889fc0e91a064c72aa49b910b826a3032526642568d580d7a1c30dc715ecc(
    *,
    write_capacity_auto_scaling_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalTablePropsMixin.CapacityAutoScalingSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac30cb9d306ee3dda3bdd5f42feb3cef6dcbefa12df5b3c6a899bcae7da600b(
    *,
    attribute_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.AttributeDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    billing_mode: typing.Optional[builtins.str] = None,
    contributor_insights_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ContributorInsightsSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    global_secondary_indexes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.GlobalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    import_source_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ImportSourceSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    kinesis_stream_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.KinesisStreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    local_secondary_indexes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.LocalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    on_demand_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.OnDemandThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    point_in_time_recovery_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.PointInTimeRecoverySpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ResourcePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sse_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stream_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.StreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_class: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_to_live_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.TimeToLiveSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    warm_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.WarmThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837e0badabebdaa00ca384834c5798a3c72ad815029e67f6ad792d4df2b497ce(
    props: typing.Union[CfnTableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7882aaade2e5e9ebda12a8af0a6d4808c4fecc31e51bae72cfb0746e18dafc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090a756886eae0441e803fb77cab2804b4af1ff9b71c7330f5c41cf51eee7aa7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339655a0289a45a2fb3e7e036553f520218532895cefcb8cff92802cae1c3f33(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    attribute_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b11fc104c94194c2b367ff4941890708932d80c69db86ccbe880c989cb15731(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad9b020ca07e271af3c67f669a9cac15b8990c52e823b9b526f83a4f9cb03e7(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b07d14869ed7cdf6145761339637271cda9fcc3d69b0591689d6077482d6a7(
    *,
    contributor_insights_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ContributorInsightsSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    index_name: typing.Optional[builtins.str] = None,
    key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    on_demand_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.OnDemandThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    projection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ProjectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    warm_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.WarmThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44646e9a197de3796da7f5326c71455bc0c344bcbaa33f5b054148f0071576fa(
    *,
    input_compression_type: typing.Optional[builtins.str] = None,
    input_format: typing.Optional[builtins.str] = None,
    input_format_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.InputFormatOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_bucket_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.S3BucketSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af2acdf9a386cd6eee999b63e2d90f809c74011bf9e4693b4d9a1c96eb1a779(
    *,
    csv: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.CsvProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d62171286374e13bf43f12c0cfb2babc07a0961df338aff1ff75218d59cefdf(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88766615196f02b1f95f9a2252a4f633d38a19714522417b74e5fba850eb89c3(
    *,
    approximate_creation_date_time_precision: typing.Optional[builtins.str] = None,
    stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd0f002d5461d6bd7f002dbdc4851c05a7323bf65c667d9072f793c5af4b1bf(
    *,
    index_name: typing.Optional[builtins.str] = None,
    key_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    projection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ProjectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9657fa047b3ea84481b14837aa2d22f16a95bef921c260bdea6d5ed7a7eeb775(
    *,
    max_read_request_units: typing.Optional[jsii.Number] = None,
    max_write_request_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ebdaa3445699b295d7877742c6cd9d9b6fffb1b71bbc8f4a5b540f4d0681da(
    *,
    point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    recovery_period_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3c34c9815eda98df6abc91190c0815839f78678ef0fcb22088f16df8447596(
    *,
    non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    projection_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0226e210f2b013e7882a83790c33ea4ae1f43187d6b855dea9297f3ac8dbb60(
    *,
    read_capacity_units: typing.Optional[jsii.Number] = None,
    write_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2398ae9cad7279612b6e1cd482efe224ba8613fb64aa2a647dd2573773ce9e44(
    *,
    policy_document: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6551833d002e3321431507b119120c6e52ef340d123bdbc2441680d80abc6505(
    *,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_bucket_owner: typing.Optional[builtins.str] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9696b7b05976aa142ecdff24ea3265e252ea8dfd9c83e59bf2f30cddd63ddd0(
    *,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    sse_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f018e3c029fa6bef69320b13657979bd6760d06d83e980c1d5baa3b627a78ba(
    *,
    resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ResourcePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stream_view_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbdcb49d1622b8066a9b707435bbe954fd9968075b58c4c807a52705e35c943(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1020daa1c0e7245bc963e6a630eda00c8f8c3d418845202c7250942ef4b62f93(
    *,
    read_units_per_second: typing.Optional[jsii.Number] = None,
    write_units_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
