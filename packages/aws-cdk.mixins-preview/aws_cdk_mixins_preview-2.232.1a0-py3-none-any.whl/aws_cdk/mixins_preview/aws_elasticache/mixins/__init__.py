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
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnCacheClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "az_mode": "azMode",
        "cache_node_type": "cacheNodeType",
        "cache_parameter_group_name": "cacheParameterGroupName",
        "cache_security_group_names": "cacheSecurityGroupNames",
        "cache_subnet_group_name": "cacheSubnetGroupName",
        "cluster_name": "clusterName",
        "engine": "engine",
        "engine_version": "engineVersion",
        "ip_discovery": "ipDiscovery",
        "log_delivery_configurations": "logDeliveryConfigurations",
        "network_type": "networkType",
        "notification_topic_arn": "notificationTopicArn",
        "num_cache_nodes": "numCacheNodes",
        "port": "port",
        "preferred_availability_zone": "preferredAvailabilityZone",
        "preferred_availability_zones": "preferredAvailabilityZones",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "snapshot_arns": "snapshotArns",
        "snapshot_name": "snapshotName",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "snapshot_window": "snapshotWindow",
        "tags": "tags",
        "transit_encryption_enabled": "transitEncryptionEnabled",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnCacheClusterMixinProps:
    def __init__(
        self,
        *,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        az_mode: typing.Optional[builtins.str] = None,
        cache_node_type: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        ip_discovery: typing.Optional[builtins.str] = None,
        log_delivery_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCacheClusterPropsMixin.LogDeliveryConfigurationRequestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        network_type: typing.Optional[builtins.str] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        num_cache_nodes: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_availability_zone: typing.Optional[builtins.str] = None,
        preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnCacheClusterPropsMixin.

        :param auto_minor_version_upgrade: If you are running Valkey 7.2 or later, or Redis OSS engine version 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.
        :param az_mode: Specifies whether the nodes in this Memcached cluster are created in a single Availability Zone or created across multiple Availability Zones in the cluster's region. This parameter is only supported for Memcached clusters. If the ``AZMode`` and ``PreferredAvailabilityZones`` are not specified, ElastiCache assumes ``single-az`` mode.
        :param cache_node_type: The compute and memory capacity of the nodes in the node group (shard). The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts. Changing the CacheNodeType of a Memcached instance is currently not supported. If you need to scale using Memcached, we recommend forcing a replacement update by changing the ``LogicalResourceId`` of the resource. - General purpose: - Current generation: *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.8xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.16xlarge`` , ``cache.m6g.24xlarge`` *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge`` *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge`` *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium`` *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium`` *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium`` - Previous generation: (not recommended) *T1 node types:* ``cache.t1.micro`` *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge`` *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge`` - Compute optimized: - Previous generation: (not recommended) *C1 node types:* ``cache.c1.xlarge`` - Memory optimized: - Current generation: *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge`` .. epigraph:: The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` . *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.8xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.16xlarge`` , ``cache.r6g.24xlarge`` *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge`` *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge`` - Previous generation: (not recommended) *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge`` *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge`` For region availability, see `Supported Node Types by Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_ *Additional node type info* - All current generation instance types are created in Amazon VPC by default. - Valkey and Redis OSS append-only files (AOF) are not supported for T1 or T2 instances. - Valkey and Redis OSS Multi-AZ with automatic failover is not supported on T1 instances. - Redis OSS configuration variables ``appendonly`` and ``appendfsync`` are not supported on Redis OSS version 2.8.22 and later.
        :param cache_parameter_group_name: The name of the parameter group to associate with this cluster. If this argument is omitted, the default parameter group for the specified engine is used. You cannot use any parameter group which has ``cluster-enabled='yes'`` when creating a cluster.
        :param cache_security_group_names: A list of security group names to associate with this cluster. Use this parameter only when you are creating a cluster outside of an Amazon Virtual Private Cloud (Amazon VPC).
        :param cache_subnet_group_name: The name of the subnet group to be used for the cluster. Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC). .. epigraph:: If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see ``[AWS::ElastiCache::SubnetGroup](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html) .``
        :param cluster_name: A name for the cache cluster. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the cache cluster. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . The name must contain 1 to 50 alphanumeric characters or hyphens. The name must start with a letter and cannot end with a hyphen or contain two consecutive hyphens.
        :param engine: The name of the cache engine to be used for this cluster. Valid values for this parameter are: ``memcached`` | valkey | ``redis``
        :param engine_version: The version number of the cache engine to be used for this cluster. To view the supported cache engine versions, use the DescribeCacheEngineVersions operation. *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SelectEngine.html#VersionManagement>`_ ), but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.
        :param ip_discovery: The network type you choose when modifying a cluster, either ``ipv4`` | ``ipv6`` . IPv6 is supported for workloads using Valkey 7.2 and above, Redis OSS engine version 6.2 to 7.1 and Memcached engine version 1.6.6 and above on all instances built on the `Nitro system <https://docs.aws.amazon.com/ec2/nitro/>`_ .
        :param log_delivery_configurations: Specifies the destination, format and type of the logs.
        :param network_type: Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` . IPv6 is supported for workloads using Valkey 7.2 and above, Redis OSS engine version 6.2 to 7.1 and Memcached engine version 1.6.6 and above on all instances built on the `Nitro system <https://docs.aws.amazon.com/ec2/nitro/>`_ .
        :param notification_topic_arn: The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent. .. epigraph:: The Amazon SNS topic owner must be the same as the cluster owner.
        :param num_cache_nodes: The number of cache nodes that the cache cluster should have. .. epigraph:: However, if the ``PreferredAvailabilityZone`` and ``PreferredAvailabilityZones`` properties were not previously specified and you don't specify any new values, an update requires `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param port: The port number on which each of the cache nodes accepts connections.
        :param preferred_availability_zone: The EC2 Availability Zone in which the cluster is created. All nodes belonging to this cluster are placed in the preferred Availability Zone. If you want to create your nodes across multiple Availability Zones, use ``PreferredAvailabilityZones`` . Default: System chosen Availability Zone.
        :param preferred_availability_zones: A list of the Availability Zones in which cache nodes are created. The order of the zones in the list is not important. This option is only supported on Memcached. .. epigraph:: If you are creating your cluster in an Amazon VPC (recommended) you can only locate nodes in Availability Zones that are associated with the subnets in the selected subnet group. The number of Availability Zones listed must equal the value of ``NumCacheNodes`` . If you want all the nodes in the same Availability Zone, use ``PreferredAvailabilityZone`` instead, or repeat the Availability Zone multiple times in the list. Default: System chosen Availability Zones.
        :param preferred_maintenance_window: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ``ddd`` are: - ``sun`` - ``mon`` - ``tue`` - ``wed`` - ``thu`` - ``fri`` - ``sat`` Example: ``sun:23:00-mon:01:30``
        :param snapshot_arns: A single-element string list containing an Amazon Resource Name (ARN) that uniquely identifies a Valkey or Redis OSS RDB snapshot file stored in Amazon S3. The snapshot file is used to populate the node group (shard). The Amazon S3 object name in the ARN cannot contain any commas. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` . Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``
        :param snapshot_name: The name of a Valkey or Redis OSS snapshot from which to restore data into the new node group (shard). The snapshot status changes to ``restoring`` while the new node group (shard) is being created. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` .
        :param snapshot_retention_limit: The number of days for which ElastiCache retains automatic snapshots before deleting them. For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot taken today is retained for 5 days before being deleted. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` . Default: 0 (i.e., automatic backups are disabled for this cache cluster).
        :param snapshot_window: The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard). Example: ``05:00-09:00`` If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` .
        :param tags: A list of tags to be added to this resource.
        :param transit_encryption_enabled: A flag that enables in-transit encryption when set to true.
        :param vpc_security_group_ids: One or more VPC security groups associated with the cluster. Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
            
            cfn_cache_cluster_mixin_props = elasticache_mixins.CfnCacheClusterMixinProps(
                auto_minor_version_upgrade=False,
                az_mode="azMode",
                cache_node_type="cacheNodeType",
                cache_parameter_group_name="cacheParameterGroupName",
                cache_security_group_names=["cacheSecurityGroupNames"],
                cache_subnet_group_name="cacheSubnetGroupName",
                cluster_name="clusterName",
                engine="engine",
                engine_version="engineVersion",
                ip_discovery="ipDiscovery",
                log_delivery_configurations=[elasticache_mixins.CfnCacheClusterPropsMixin.LogDeliveryConfigurationRequestProperty(
                    destination_details=elasticache_mixins.CfnCacheClusterPropsMixin.DestinationDetailsProperty(
                        cloud_watch_logs_details=elasticache_mixins.CfnCacheClusterPropsMixin.CloudWatchLogsDestinationDetailsProperty(
                            log_group="logGroup"
                        ),
                        kinesis_firehose_details=elasticache_mixins.CfnCacheClusterPropsMixin.KinesisFirehoseDestinationDetailsProperty(
                            delivery_stream="deliveryStream"
                        )
                    ),
                    destination_type="destinationType",
                    log_format="logFormat",
                    log_type="logType"
                )],
                network_type="networkType",
                notification_topic_arn="notificationTopicArn",
                num_cache_nodes=123,
                port=123,
                preferred_availability_zone="preferredAvailabilityZone",
                preferred_availability_zones=["preferredAvailabilityZones"],
                preferred_maintenance_window="preferredMaintenanceWindow",
                snapshot_arns=["snapshotArns"],
                snapshot_name="snapshotName",
                snapshot_retention_limit=123,
                snapshot_window="snapshotWindow",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                transit_encryption_enabled=False,
                vpc_security_group_ids=["vpcSecurityGroupIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4cc3afc7f2337ac60e5736c33e906f912bfe9608538a88971aa4c1a3f3ba2e7)
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument az_mode", value=az_mode, expected_type=type_hints["az_mode"])
            check_type(argname="argument cache_node_type", value=cache_node_type, expected_type=type_hints["cache_node_type"])
            check_type(argname="argument cache_parameter_group_name", value=cache_parameter_group_name, expected_type=type_hints["cache_parameter_group_name"])
            check_type(argname="argument cache_security_group_names", value=cache_security_group_names, expected_type=type_hints["cache_security_group_names"])
            check_type(argname="argument cache_subnet_group_name", value=cache_subnet_group_name, expected_type=type_hints["cache_subnet_group_name"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument ip_discovery", value=ip_discovery, expected_type=type_hints["ip_discovery"])
            check_type(argname="argument log_delivery_configurations", value=log_delivery_configurations, expected_type=type_hints["log_delivery_configurations"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument notification_topic_arn", value=notification_topic_arn, expected_type=type_hints["notification_topic_arn"])
            check_type(argname="argument num_cache_nodes", value=num_cache_nodes, expected_type=type_hints["num_cache_nodes"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_availability_zone", value=preferred_availability_zone, expected_type=type_hints["preferred_availability_zone"])
            check_type(argname="argument preferred_availability_zones", value=preferred_availability_zones, expected_type=type_hints["preferred_availability_zones"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument snapshot_arns", value=snapshot_arns, expected_type=type_hints["snapshot_arns"])
            check_type(argname="argument snapshot_name", value=snapshot_name, expected_type=type_hints["snapshot_name"])
            check_type(argname="argument snapshot_retention_limit", value=snapshot_retention_limit, expected_type=type_hints["snapshot_retention_limit"])
            check_type(argname="argument snapshot_window", value=snapshot_window, expected_type=type_hints["snapshot_window"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transit_encryption_enabled", value=transit_encryption_enabled, expected_type=type_hints["transit_encryption_enabled"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if az_mode is not None:
            self._values["az_mode"] = az_mode
        if cache_node_type is not None:
            self._values["cache_node_type"] = cache_node_type
        if cache_parameter_group_name is not None:
            self._values["cache_parameter_group_name"] = cache_parameter_group_name
        if cache_security_group_names is not None:
            self._values["cache_security_group_names"] = cache_security_group_names
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if engine is not None:
            self._values["engine"] = engine
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if ip_discovery is not None:
            self._values["ip_discovery"] = ip_discovery
        if log_delivery_configurations is not None:
            self._values["log_delivery_configurations"] = log_delivery_configurations
        if network_type is not None:
            self._values["network_type"] = network_type
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if num_cache_nodes is not None:
            self._values["num_cache_nodes"] = num_cache_nodes
        if port is not None:
            self._values["port"] = port
        if preferred_availability_zone is not None:
            self._values["preferred_availability_zone"] = preferred_availability_zone
        if preferred_availability_zones is not None:
            self._values["preferred_availability_zones"] = preferred_availability_zones
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if snapshot_arns is not None:
            self._values["snapshot_arns"] = snapshot_arns
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if snapshot_window is not None:
            self._values["snapshot_window"] = snapshot_window
        if tags is not None:
            self._values["tags"] = tags
        if transit_encryption_enabled is not None:
            self._values["transit_encryption_enabled"] = transit_encryption_enabled
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If you are running Valkey 7.2 or later, or Redis OSS engine version 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def az_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the nodes in this Memcached cluster are created in a single Availability Zone or created across multiple Availability Zones in the cluster's region.

        This parameter is only supported for Memcached clusters.

        If the ``AZMode`` and ``PreferredAvailabilityZones`` are not specified, ElastiCache assumes ``single-az`` mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-azmode
        '''
        result = self._values.get("az_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_node_type(self) -> typing.Optional[builtins.str]:
        '''The compute and memory capacity of the nodes in the node group (shard).

        The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts. Changing the CacheNodeType of a Memcached instance is currently not supported. If you need to scale using Memcached, we recommend forcing a replacement update by changing the ``LogicalResourceId`` of the resource.

        - General purpose:
        - Current generation:

        *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.8xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.16xlarge`` , ``cache.m6g.24xlarge``

        *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge``

        *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge``

        *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium``

        *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium``

        *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium``

        - Previous generation: (not recommended)

        *T1 node types:* ``cache.t1.micro``

        *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge``

        *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge``

        - Compute optimized:
        - Previous generation: (not recommended)

        *C1 node types:* ``cache.c1.xlarge``

        - Memory optimized:
        - Current generation:

        *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge``
        .. epigraph::

           The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` .

        *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.8xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.16xlarge`` , ``cache.r6g.24xlarge``

        *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge``

        *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge``

        - Previous generation: (not recommended)

        *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge``

        *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge``

        For region availability, see `Supported Node Types by Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_

        *Additional node type info*

        - All current generation instance types are created in Amazon VPC by default.
        - Valkey and Redis OSS append-only files (AOF) are not supported for T1 or T2 instances.
        - Valkey and Redis OSS Multi-AZ with automatic failover is not supported on T1 instances.
        - Redis OSS configuration variables ``appendonly`` and ``appendfsync`` are not supported on Redis OSS version 2.8.22 and later.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-cachenodetype
        '''
        result = self._values.get("cache_node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group to associate with this cluster.

        If this argument is omitted, the default parameter group for the specified engine is used. You cannot use any parameter group which has ``cluster-enabled='yes'`` when creating a cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-cacheparametergroupname
        '''
        result = self._values.get("cache_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_security_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group names to associate with this cluster.

        Use this parameter only when you are creating a cluster outside of an Amazon Virtual Private Cloud (Amazon VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-cachesecuritygroupnames
        '''
        result = self._values.get("cache_security_group_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group to be used for the cluster.

        Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC).
        .. epigraph::

           If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see ``[AWS::ElastiCache::SubnetGroup](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html) .``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-cachesubnetgroupname
        '''
        result = self._values.get("cache_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''A name for the cache cluster.

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the cache cluster. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        The name must contain 1 to 50 alphanumeric characters or hyphens. The name must start with a letter and cannot end with a hyphen or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The name of the cache engine to be used for this cluster.

        Valid values for this parameter are: ``memcached`` | valkey | ``redis``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the cache engine to be used for this cluster.

        To view the supported cache engine versions, use the DescribeCacheEngineVersions operation.

        *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SelectEngine.html#VersionManagement>`_ ), but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_discovery(self) -> typing.Optional[builtins.str]:
        '''The network type you choose when modifying a cluster, either ``ipv4`` | ``ipv6`` .

        IPv6 is supported for workloads using Valkey 7.2 and above, Redis OSS engine version 6.2 to 7.1 and Memcached engine version 1.6.6 and above on all instances built on the `Nitro system <https://docs.aws.amazon.com/ec2/nitro/>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-ipdiscovery
        '''
        result = self._values.get("ip_discovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCacheClusterPropsMixin.LogDeliveryConfigurationRequestProperty"]]]]:
        '''Specifies the destination, format and type of the logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-logdeliveryconfigurations
        '''
        result = self._values.get("log_delivery_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCacheClusterPropsMixin.LogDeliveryConfigurationRequestProperty"]]]], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` .

        IPv6 is supported for workloads using Valkey 7.2 and above, Redis OSS engine version 6.2 to 7.1 and Memcached engine version 1.6.6 and above on all instances built on the `Nitro system <https://docs.aws.amazon.com/ec2/nitro/>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent.

        .. epigraph::

           The Amazon SNS topic owner must be the same as the cluster owner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-notificationtopicarn
        '''
        result = self._values.get("notification_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_cache_nodes(self) -> typing.Optional[jsii.Number]:
        '''The number of cache nodes that the cache cluster should have.

        .. epigraph::

           However, if the ``PreferredAvailabilityZone`` and ``PreferredAvailabilityZones`` properties were not previously specified and you don't specify any new values, an update requires `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-numcachenodes
        '''
        result = self._values.get("num_cache_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number on which each of the cache nodes accepts connections.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_availability_zone(self) -> typing.Optional[builtins.str]:
        '''The EC2 Availability Zone in which the cluster is created.

        All nodes belonging to this cluster are placed in the preferred Availability Zone. If you want to create your nodes across multiple Availability Zones, use ``PreferredAvailabilityZones`` .

        Default: System chosen Availability Zone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-preferredavailabilityzone
        '''
        result = self._values.get("preferred_availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_availability_zones(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the Availability Zones in which cache nodes are created.

        The order of the zones in the list is not important.

        This option is only supported on Memcached.
        .. epigraph::

           If you are creating your cluster in an Amazon VPC (recommended) you can only locate nodes in Availability Zones that are associated with the subnets in the selected subnet group.

           The number of Availability Zones listed must equal the value of ``NumCacheNodes`` .

        If you want all the nodes in the same Availability Zone, use ``PreferredAvailabilityZone`` instead, or repeat the Availability Zone multiple times in the list.

        Default: System chosen Availability Zones.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-preferredavailabilityzones
        '''
        result = self._values.get("preferred_availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Specifies the weekly time range during which maintenance on the cluster is performed.

        It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period.

        Valid values for ``ddd`` are:

        - ``sun``
        - ``mon``
        - ``tue``
        - ``wed``
        - ``thu``
        - ``fri``
        - ``sat``

        Example: ``sun:23:00-mon:01:30``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A single-element string list containing an Amazon Resource Name (ARN) that uniquely identifies a Valkey or Redis OSS RDB snapshot file stored in Amazon S3.

        The snapshot file is used to populate the node group (shard). The Amazon S3 object name in the ARN cannot contain any commas.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-snapshotarns
        '''
        result = self._values.get("snapshot_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of a Valkey or Redis OSS snapshot from which to restore data into the new node group (shard).

        The snapshot status changes to ``restoring`` while the new node group (shard) is being created.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-snapshotname
        '''
        result = self._values.get("snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which ElastiCache retains automatic snapshots before deleting them.

        For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot taken today is retained for 5 days before being deleted.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        Default: 0 (i.e., automatic backups are disabled for this cache cluster).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-snapshotretentionlimit
        '''
        result = self._values.get("snapshot_retention_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard).

        Example: ``05:00-09:00``

        If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-snapshotwindow
        '''
        result = self._values.get("snapshot_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to be added to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A flag that enables in-transit encryption when set to true.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-transitencryptionenabled
        '''
        result = self._values.get("transit_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more VPC security groups associated with the cluster.

        Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html#cfn-elasticache-cachecluster-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCacheClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCacheClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnCacheClusterPropsMixin",
):
    '''The ``AWS::ElastiCache::CacheCluster`` type creates an Amazon ElastiCache cache cluster.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-cachecluster.html
    :cloudformationResource: AWS::ElastiCache::CacheCluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
        
        cfn_cache_cluster_props_mixin = elasticache_mixins.CfnCacheClusterPropsMixin(elasticache_mixins.CfnCacheClusterMixinProps(
            auto_minor_version_upgrade=False,
            az_mode="azMode",
            cache_node_type="cacheNodeType",
            cache_parameter_group_name="cacheParameterGroupName",
            cache_security_group_names=["cacheSecurityGroupNames"],
            cache_subnet_group_name="cacheSubnetGroupName",
            cluster_name="clusterName",
            engine="engine",
            engine_version="engineVersion",
            ip_discovery="ipDiscovery",
            log_delivery_configurations=[elasticache_mixins.CfnCacheClusterPropsMixin.LogDeliveryConfigurationRequestProperty(
                destination_details=elasticache_mixins.CfnCacheClusterPropsMixin.DestinationDetailsProperty(
                    cloud_watch_logs_details=elasticache_mixins.CfnCacheClusterPropsMixin.CloudWatchLogsDestinationDetailsProperty(
                        log_group="logGroup"
                    ),
                    kinesis_firehose_details=elasticache_mixins.CfnCacheClusterPropsMixin.KinesisFirehoseDestinationDetailsProperty(
                        delivery_stream="deliveryStream"
                    )
                ),
                destination_type="destinationType",
                log_format="logFormat",
                log_type="logType"
            )],
            network_type="networkType",
            notification_topic_arn="notificationTopicArn",
            num_cache_nodes=123,
            port=123,
            preferred_availability_zone="preferredAvailabilityZone",
            preferred_availability_zones=["preferredAvailabilityZones"],
            preferred_maintenance_window="preferredMaintenanceWindow",
            snapshot_arns=["snapshotArns"],
            snapshot_name="snapshotName",
            snapshot_retention_limit=123,
            snapshot_window="snapshotWindow",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            transit_encryption_enabled=False,
            vpc_security_group_ids=["vpcSecurityGroupIds"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCacheClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElastiCache::CacheCluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db5e4e2268cdb54c9b99d49086cf181011d65a3d79e2bdc9cd28fe18ba17f59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c21d5d5b43ea28194baf332adf00c324e923f03332c4e276c7b62ce05075486e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c7675179697ab3fb7ae886e4a6564da24f20edd33553a3d23b2720c86348d9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCacheClusterMixinProps:
        return typing.cast(CfnCacheClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnCacheClusterPropsMixin.CloudWatchLogsDestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group": "logGroup"},
    )
    class CloudWatchLogsDestinationDetailsProperty:
        def __init__(self, *, log_group: typing.Optional[builtins.str] = None) -> None:
            '''Configuration details of a CloudWatch Logs destination.

            Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.

            :param log_group: The name of the CloudWatch Logs log group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-cloudwatchlogsdestinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                cloud_watch_logs_destination_details_property = elasticache_mixins.CfnCacheClusterPropsMixin.CloudWatchLogsDestinationDetailsProperty(
                    log_group="logGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5c8c39ecfbea9e5b37a3c2248a2651d755278945b0417073667bb48d53f900ca)
                check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group is not None:
                self._values["log_group"] = log_group

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch Logs log group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-cloudwatchlogsdestinationdetails.html#cfn-elasticache-cachecluster-cloudwatchlogsdestinationdetails-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsDestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnCacheClusterPropsMixin.DestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_details": "cloudWatchLogsDetails",
            "kinesis_firehose_details": "kinesisFirehoseDetails",
        },
    )
    class DestinationDetailsProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCacheClusterPropsMixin.CloudWatchLogsDestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_firehose_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCacheClusterPropsMixin.KinesisFirehoseDestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.

            :param cloud_watch_logs_details: The configuration details of the CloudWatch Logs destination. Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.
            :param kinesis_firehose_details: The configuration details of the Kinesis Data Firehose destination. Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-destinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                destination_details_property = elasticache_mixins.CfnCacheClusterPropsMixin.DestinationDetailsProperty(
                    cloud_watch_logs_details=elasticache_mixins.CfnCacheClusterPropsMixin.CloudWatchLogsDestinationDetailsProperty(
                        log_group="logGroup"
                    ),
                    kinesis_firehose_details=elasticache_mixins.CfnCacheClusterPropsMixin.KinesisFirehoseDestinationDetailsProperty(
                        delivery_stream="deliveryStream"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__909a85364b79692107ddfdfdd9900d608710ea30c8edeb18babfce613ae4271e)
                check_type(argname="argument cloud_watch_logs_details", value=cloud_watch_logs_details, expected_type=type_hints["cloud_watch_logs_details"])
                check_type(argname="argument kinesis_firehose_details", value=kinesis_firehose_details, expected_type=type_hints["kinesis_firehose_details"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_details is not None:
                self._values["cloud_watch_logs_details"] = cloud_watch_logs_details
            if kinesis_firehose_details is not None:
                self._values["kinesis_firehose_details"] = kinesis_firehose_details

        @builtins.property
        def cloud_watch_logs_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCacheClusterPropsMixin.CloudWatchLogsDestinationDetailsProperty"]]:
            '''The configuration details of the CloudWatch Logs destination.

            Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-destinationdetails.html#cfn-elasticache-cachecluster-destinationdetails-cloudwatchlogsdetails
            '''
            result = self._values.get("cloud_watch_logs_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCacheClusterPropsMixin.CloudWatchLogsDestinationDetailsProperty"]], result)

        @builtins.property
        def kinesis_firehose_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCacheClusterPropsMixin.KinesisFirehoseDestinationDetailsProperty"]]:
            '''The configuration details of the Kinesis Data Firehose destination.

            Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-destinationdetails.html#cfn-elasticache-cachecluster-destinationdetails-kinesisfirehosedetails
            '''
            result = self._values.get("kinesis_firehose_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCacheClusterPropsMixin.KinesisFirehoseDestinationDetailsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnCacheClusterPropsMixin.KinesisFirehoseDestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_stream": "deliveryStream"},
    )
    class KinesisFirehoseDestinationDetailsProperty:
        def __init__(
            self,
            *,
            delivery_stream: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration details of the Kinesis Data Firehose destination.

            Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :param delivery_stream: The name of the Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-kinesisfirehosedestinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                kinesis_firehose_destination_details_property = elasticache_mixins.CfnCacheClusterPropsMixin.KinesisFirehoseDestinationDetailsProperty(
                    delivery_stream="deliveryStream"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14032e8607ac22281c1b8f1843321d07e5342050225aed189920471fa2c6577b)
                check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_stream is not None:
                self._values["delivery_stream"] = delivery_stream

        @builtins.property
        def delivery_stream(self) -> typing.Optional[builtins.str]:
            '''The name of the Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-kinesisfirehosedestinationdetails.html#cfn-elasticache-cachecluster-kinesisfirehosedestinationdetails-deliverystream
            '''
            result = self._values.get("delivery_stream")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseDestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnCacheClusterPropsMixin.LogDeliveryConfigurationRequestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_details": "destinationDetails",
            "destination_type": "destinationType",
            "log_format": "logFormat",
            "log_type": "logType",
        },
    )
    class LogDeliveryConfigurationRequestProperty:
        def __init__(
            self,
            *,
            destination_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCacheClusterPropsMixin.DestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            destination_type: typing.Optional[builtins.str] = None,
            log_format: typing.Optional[builtins.str] = None,
            log_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the destination, format and type of the logs.

            :param destination_details: Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.
            :param destination_type: Specify either CloudWatch Logs or Kinesis Data Firehose as the destination type. Valid values are either ``cloudwatch-logs`` or ``kinesis-firehose`` .
            :param log_format: Valid values are either ``json`` or ``text`` .
            :param log_type: Valid value is either ``slow-log`` , which refers to `slow-log <https://docs.aws.amazon.com/https://redis.io/commands/slowlog>`_ or ``engine-log`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-logdeliveryconfigurationrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                log_delivery_configuration_request_property = elasticache_mixins.CfnCacheClusterPropsMixin.LogDeliveryConfigurationRequestProperty(
                    destination_details=elasticache_mixins.CfnCacheClusterPropsMixin.DestinationDetailsProperty(
                        cloud_watch_logs_details=elasticache_mixins.CfnCacheClusterPropsMixin.CloudWatchLogsDestinationDetailsProperty(
                            log_group="logGroup"
                        ),
                        kinesis_firehose_details=elasticache_mixins.CfnCacheClusterPropsMixin.KinesisFirehoseDestinationDetailsProperty(
                            delivery_stream="deliveryStream"
                        )
                    ),
                    destination_type="destinationType",
                    log_format="logFormat",
                    log_type="logType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6dc3f2f42abefca95555a5e08511b1ffb48793074f0735b972cd01884c6a73ec)
                check_type(argname="argument destination_details", value=destination_details, expected_type=type_hints["destination_details"])
                check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
                check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
                check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_details is not None:
                self._values["destination_details"] = destination_details
            if destination_type is not None:
                self._values["destination_type"] = destination_type
            if log_format is not None:
                self._values["log_format"] = log_format
            if log_type is not None:
                self._values["log_type"] = log_type

        @builtins.property
        def destination_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCacheClusterPropsMixin.DestinationDetailsProperty"]]:
            '''Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-logdeliveryconfigurationrequest.html#cfn-elasticache-cachecluster-logdeliveryconfigurationrequest-destinationdetails
            '''
            result = self._values.get("destination_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCacheClusterPropsMixin.DestinationDetailsProperty"]], result)

        @builtins.property
        def destination_type(self) -> typing.Optional[builtins.str]:
            '''Specify either CloudWatch Logs or Kinesis Data Firehose as the destination type.

            Valid values are either ``cloudwatch-logs`` or ``kinesis-firehose`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-logdeliveryconfigurationrequest.html#cfn-elasticache-cachecluster-logdeliveryconfigurationrequest-destinationtype
            '''
            result = self._values.get("destination_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_format(self) -> typing.Optional[builtins.str]:
            '''Valid values are either ``json`` or ``text`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-logdeliveryconfigurationrequest.html#cfn-elasticache-cachecluster-logdeliveryconfigurationrequest-logformat
            '''
            result = self._values.get("log_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_type(self) -> typing.Optional[builtins.str]:
            '''Valid value is either ``slow-log`` , which refers to `slow-log <https://docs.aws.amazon.com/https://redis.io/commands/slowlog>`_ or ``engine-log`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-logdeliveryconfigurationrequest.html#cfn-elasticache-cachecluster-logdeliveryconfigurationrequest-logtype
            '''
            result = self._values.get("log_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDeliveryConfigurationRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnGlobalReplicationGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "automatic_failover_enabled": "automaticFailoverEnabled",
        "cache_node_type": "cacheNodeType",
        "cache_parameter_group_name": "cacheParameterGroupName",
        "engine": "engine",
        "engine_version": "engineVersion",
        "global_node_group_count": "globalNodeGroupCount",
        "global_replication_group_description": "globalReplicationGroupDescription",
        "global_replication_group_id_suffix": "globalReplicationGroupIdSuffix",
        "members": "members",
        "regional_configurations": "regionalConfigurations",
    },
)
class CfnGlobalReplicationGroupMixinProps:
    def __init__(
        self,
        *,
        automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        cache_node_type: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        global_node_group_count: typing.Optional[jsii.Number] = None,
        global_replication_group_description: typing.Optional[builtins.str] = None,
        global_replication_group_id_suffix: typing.Optional[builtins.str] = None,
        members: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalReplicationGroupPropsMixin.GlobalReplicationGroupMemberProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        regional_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalReplicationGroupPropsMixin.RegionalConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnGlobalReplicationGroupPropsMixin.

        :param automatic_failover_enabled: Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails. ``AutomaticFailoverEnabled`` must be enabled for Valkey or Redis OSS (cluster mode enabled) replication groups.
        :param cache_node_type: The cache node type of the Global datastore.
        :param cache_parameter_group_name: The name of the cache parameter group to use with the Global datastore. It must be compatible with the major engine version used by the Global datastore.
        :param engine: The ElastiCache engine. For Valkey or Redis OSS only.
        :param engine_version: The Elasticache Valkey or Redis OSS engine version.
        :param global_node_group_count: The number of node groups that comprise the Global Datastore.
        :param global_replication_group_description: The optional description of the Global datastore.
        :param global_replication_group_id_suffix: The suffix name of a Global Datastore. The suffix guarantees uniqueness of the Global Datastore name across multiple regions.
        :param members: The replication groups that comprise the Global datastore.
        :param regional_configurations: The Regions that comprise the Global Datastore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
            
            cfn_global_replication_group_mixin_props = elasticache_mixins.CfnGlobalReplicationGroupMixinProps(
                automatic_failover_enabled=False,
                cache_node_type="cacheNodeType",
                cache_parameter_group_name="cacheParameterGroupName",
                engine="engine",
                engine_version="engineVersion",
                global_node_group_count=123,
                global_replication_group_description="globalReplicationGroupDescription",
                global_replication_group_id_suffix="globalReplicationGroupIdSuffix",
                members=[elasticache_mixins.CfnGlobalReplicationGroupPropsMixin.GlobalReplicationGroupMemberProperty(
                    replication_group_id="replicationGroupId",
                    replication_group_region="replicationGroupRegion",
                    role="role"
                )],
                regional_configurations=[elasticache_mixins.CfnGlobalReplicationGroupPropsMixin.RegionalConfigurationProperty(
                    replication_group_id="replicationGroupId",
                    replication_group_region="replicationGroupRegion",
                    resharding_configurations=[elasticache_mixins.CfnGlobalReplicationGroupPropsMixin.ReshardingConfigurationProperty(
                        node_group_id="nodeGroupId",
                        preferred_availability_zones=["preferredAvailabilityZones"]
                    )]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913b9c8c0e05e2cdf129e0cce2fe08c73815b553b31cf24b1bf70aa023bf8841)
            check_type(argname="argument automatic_failover_enabled", value=automatic_failover_enabled, expected_type=type_hints["automatic_failover_enabled"])
            check_type(argname="argument cache_node_type", value=cache_node_type, expected_type=type_hints["cache_node_type"])
            check_type(argname="argument cache_parameter_group_name", value=cache_parameter_group_name, expected_type=type_hints["cache_parameter_group_name"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument global_node_group_count", value=global_node_group_count, expected_type=type_hints["global_node_group_count"])
            check_type(argname="argument global_replication_group_description", value=global_replication_group_description, expected_type=type_hints["global_replication_group_description"])
            check_type(argname="argument global_replication_group_id_suffix", value=global_replication_group_id_suffix, expected_type=type_hints["global_replication_group_id_suffix"])
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
            check_type(argname="argument regional_configurations", value=regional_configurations, expected_type=type_hints["regional_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatic_failover_enabled is not None:
            self._values["automatic_failover_enabled"] = automatic_failover_enabled
        if cache_node_type is not None:
            self._values["cache_node_type"] = cache_node_type
        if cache_parameter_group_name is not None:
            self._values["cache_parameter_group_name"] = cache_parameter_group_name
        if engine is not None:
            self._values["engine"] = engine
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if global_node_group_count is not None:
            self._values["global_node_group_count"] = global_node_group_count
        if global_replication_group_description is not None:
            self._values["global_replication_group_description"] = global_replication_group_description
        if global_replication_group_id_suffix is not None:
            self._values["global_replication_group_id_suffix"] = global_replication_group_id_suffix
        if members is not None:
            self._values["members"] = members
        if regional_configurations is not None:
            self._values["regional_configurations"] = regional_configurations

    @builtins.property
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails.

        ``AutomaticFailoverEnabled`` must be enabled for Valkey or Redis OSS (cluster mode enabled) replication groups.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-automaticfailoverenabled
        '''
        result = self._values.get("automatic_failover_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cache_node_type(self) -> typing.Optional[builtins.str]:
        '''The cache node type of the Global datastore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-cachenodetype
        '''
        result = self._values.get("cache_node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cache parameter group to use with the Global datastore.

        It must be compatible with the major engine version used by the Global datastore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-cacheparametergroupname
        '''
        result = self._values.get("cache_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The ElastiCache engine.

        For Valkey or Redis OSS only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The Elasticache Valkey or Redis OSS engine version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_node_group_count(self) -> typing.Optional[jsii.Number]:
        '''The number of node groups that comprise the Global Datastore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-globalnodegroupcount
        '''
        result = self._values.get("global_node_group_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def global_replication_group_description(self) -> typing.Optional[builtins.str]:
        '''The optional description of the Global datastore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupdescription
        '''
        result = self._values.get("global_replication_group_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_replication_group_id_suffix(self) -> typing.Optional[builtins.str]:
        '''The suffix name of a Global Datastore.

        The suffix guarantees uniqueness of the Global Datastore name across multiple regions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupidsuffix
        '''
        result = self._values.get("global_replication_group_id_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def members(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalReplicationGroupPropsMixin.GlobalReplicationGroupMemberProperty"]]]]:
        '''The replication groups that comprise the Global datastore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-members
        '''
        result = self._values.get("members")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalReplicationGroupPropsMixin.GlobalReplicationGroupMemberProperty"]]]], result)

    @builtins.property
    def regional_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalReplicationGroupPropsMixin.RegionalConfigurationProperty"]]]]:
        '''The Regions that comprise the Global Datastore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-regionalconfigurations
        '''
        result = self._values.get("regional_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalReplicationGroupPropsMixin.RegionalConfigurationProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGlobalReplicationGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGlobalReplicationGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnGlobalReplicationGroupPropsMixin",
):
    '''Consists of a primary cluster that accepts writes and an associated secondary cluster that resides in a different Amazon region.

    The secondary cluster accepts only reads. The primary cluster automatically replicates updates to the secondary cluster.

    - The *GlobalReplicationGroupIdSuffix* represents the name of the Global datastore, which is what you use to associate a secondary cluster.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html
    :cloudformationResource: AWS::ElastiCache::GlobalReplicationGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
        
        cfn_global_replication_group_props_mixin = elasticache_mixins.CfnGlobalReplicationGroupPropsMixin(elasticache_mixins.CfnGlobalReplicationGroupMixinProps(
            automatic_failover_enabled=False,
            cache_node_type="cacheNodeType",
            cache_parameter_group_name="cacheParameterGroupName",
            engine="engine",
            engine_version="engineVersion",
            global_node_group_count=123,
            global_replication_group_description="globalReplicationGroupDescription",
            global_replication_group_id_suffix="globalReplicationGroupIdSuffix",
            members=[elasticache_mixins.CfnGlobalReplicationGroupPropsMixin.GlobalReplicationGroupMemberProperty(
                replication_group_id="replicationGroupId",
                replication_group_region="replicationGroupRegion",
                role="role"
            )],
            regional_configurations=[elasticache_mixins.CfnGlobalReplicationGroupPropsMixin.RegionalConfigurationProperty(
                replication_group_id="replicationGroupId",
                replication_group_region="replicationGroupRegion",
                resharding_configurations=[elasticache_mixins.CfnGlobalReplicationGroupPropsMixin.ReshardingConfigurationProperty(
                    node_group_id="nodeGroupId",
                    preferred_availability_zones=["preferredAvailabilityZones"]
                )]
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGlobalReplicationGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElastiCache::GlobalReplicationGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0127367a1a081054e093790f995646ca6f9c8a3fc94688fd2032f7920d29dfa0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5f3877606335a33c1c57f85202d3ccc715bcff8eea61a94b90ffdf2899e4998)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f04e80a6c7b2afa29e24529af77e8db5e7953c1cd0540c409c7dbfd104c3707)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGlobalReplicationGroupMixinProps:
        return typing.cast(CfnGlobalReplicationGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnGlobalReplicationGroupPropsMixin.GlobalReplicationGroupMemberProperty",
        jsii_struct_bases=[],
        name_mapping={
            "replication_group_id": "replicationGroupId",
            "replication_group_region": "replicationGroupRegion",
            "role": "role",
        },
    )
    class GlobalReplicationGroupMemberProperty:
        def __init__(
            self,
            *,
            replication_group_id: typing.Optional[builtins.str] = None,
            replication_group_region: typing.Optional[builtins.str] = None,
            role: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A member of a Global datastore.

            It contains the Replication Group Id, the Amazon region and the role of the replication group.

            :param replication_group_id: The replication group id of the Global datastore member.
            :param replication_group_region: The Amazon region of the Global datastore member.
            :param role: Indicates the role of the replication group, ``PRIMARY`` or ``SECONDARY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-globalreplicationgroupmember.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                global_replication_group_member_property = elasticache_mixins.CfnGlobalReplicationGroupPropsMixin.GlobalReplicationGroupMemberProperty(
                    replication_group_id="replicationGroupId",
                    replication_group_region="replicationGroupRegion",
                    role="role"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c6f08296bed475d4dcc499bc927d8f711379b7ebb269ed9aefe501afe34f0b9)
                check_type(argname="argument replication_group_id", value=replication_group_id, expected_type=type_hints["replication_group_id"])
                check_type(argname="argument replication_group_region", value=replication_group_region, expected_type=type_hints["replication_group_region"])
                check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if replication_group_id is not None:
                self._values["replication_group_id"] = replication_group_id
            if replication_group_region is not None:
                self._values["replication_group_region"] = replication_group_region
            if role is not None:
                self._values["role"] = role

        @builtins.property
        def replication_group_id(self) -> typing.Optional[builtins.str]:
            '''The replication group id of the Global datastore member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-globalreplicationgroupmember.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupmember-replicationgroupid
            '''
            result = self._values.get("replication_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replication_group_region(self) -> typing.Optional[builtins.str]:
            '''The Amazon region of the Global datastore member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-globalreplicationgroupmember.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupmember-replicationgroupregion
            '''
            result = self._values.get("replication_group_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role(self) -> typing.Optional[builtins.str]:
            '''Indicates the role of the replication group, ``PRIMARY`` or ``SECONDARY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-globalreplicationgroupmember.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupmember-role
            '''
            result = self._values.get("role")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalReplicationGroupMemberProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnGlobalReplicationGroupPropsMixin.RegionalConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "replication_group_id": "replicationGroupId",
            "replication_group_region": "replicationGroupRegion",
            "resharding_configurations": "reshardingConfigurations",
        },
    )
    class RegionalConfigurationProperty:
        def __init__(
            self,
            *,
            replication_group_id: typing.Optional[builtins.str] = None,
            replication_group_region: typing.Optional[builtins.str] = None,
            resharding_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGlobalReplicationGroupPropsMixin.ReshardingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A list of the replication groups.

            :param replication_group_id: The name of the secondary cluster.
            :param replication_group_region: The Amazon region where the cluster is stored.
            :param resharding_configurations: A list of PreferredAvailabilityZones objects that specifies the configuration of a node group in the resharded cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-regionalconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                regional_configuration_property = elasticache_mixins.CfnGlobalReplicationGroupPropsMixin.RegionalConfigurationProperty(
                    replication_group_id="replicationGroupId",
                    replication_group_region="replicationGroupRegion",
                    resharding_configurations=[elasticache_mixins.CfnGlobalReplicationGroupPropsMixin.ReshardingConfigurationProperty(
                        node_group_id="nodeGroupId",
                        preferred_availability_zones=["preferredAvailabilityZones"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59da2eab26f3d12bdd3c54ffc40e22ffd3c4adb00a19f88725f60f46d154f205)
                check_type(argname="argument replication_group_id", value=replication_group_id, expected_type=type_hints["replication_group_id"])
                check_type(argname="argument replication_group_region", value=replication_group_region, expected_type=type_hints["replication_group_region"])
                check_type(argname="argument resharding_configurations", value=resharding_configurations, expected_type=type_hints["resharding_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if replication_group_id is not None:
                self._values["replication_group_id"] = replication_group_id
            if replication_group_region is not None:
                self._values["replication_group_region"] = replication_group_region
            if resharding_configurations is not None:
                self._values["resharding_configurations"] = resharding_configurations

        @builtins.property
        def replication_group_id(self) -> typing.Optional[builtins.str]:
            '''The name of the secondary cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-regionalconfiguration.html#cfn-elasticache-globalreplicationgroup-regionalconfiguration-replicationgroupid
            '''
            result = self._values.get("replication_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replication_group_region(self) -> typing.Optional[builtins.str]:
            '''The Amazon region where the cluster is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-regionalconfiguration.html#cfn-elasticache-globalreplicationgroup-regionalconfiguration-replicationgroupregion
            '''
            result = self._values.get("replication_group_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resharding_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalReplicationGroupPropsMixin.ReshardingConfigurationProperty"]]]]:
            '''A list of PreferredAvailabilityZones objects that specifies the configuration of a node group in the resharded cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-regionalconfiguration.html#cfn-elasticache-globalreplicationgroup-regionalconfiguration-reshardingconfigurations
            '''
            result = self._values.get("resharding_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGlobalReplicationGroupPropsMixin.ReshardingConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegionalConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnGlobalReplicationGroupPropsMixin.ReshardingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "node_group_id": "nodeGroupId",
            "preferred_availability_zones": "preferredAvailabilityZones",
        },
    )
    class ReshardingConfigurationProperty:
        def __init__(
            self,
            *,
            node_group_id: typing.Optional[builtins.str] = None,
            preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A list of ``PreferredAvailabilityZones`` objects that specifies the configuration of a node group in the resharded cluster.

            :param node_group_id: Either the ElastiCache supplied 4-digit id or a user supplied id for the node group these configuration values apply to.
            :param preferred_availability_zones: A list of preferred availability zones for the nodes in this cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-reshardingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                resharding_configuration_property = elasticache_mixins.CfnGlobalReplicationGroupPropsMixin.ReshardingConfigurationProperty(
                    node_group_id="nodeGroupId",
                    preferred_availability_zones=["preferredAvailabilityZones"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a1d771a202a7d2d1d22d344bc42d1ba3cc0e99853b85cf27012964f9171c9d43)
                check_type(argname="argument node_group_id", value=node_group_id, expected_type=type_hints["node_group_id"])
                check_type(argname="argument preferred_availability_zones", value=preferred_availability_zones, expected_type=type_hints["preferred_availability_zones"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if node_group_id is not None:
                self._values["node_group_id"] = node_group_id
            if preferred_availability_zones is not None:
                self._values["preferred_availability_zones"] = preferred_availability_zones

        @builtins.property
        def node_group_id(self) -> typing.Optional[builtins.str]:
            '''Either the ElastiCache supplied 4-digit id or a user supplied id for the node group these configuration values apply to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-reshardingconfiguration.html#cfn-elasticache-globalreplicationgroup-reshardingconfiguration-nodegroupid
            '''
            result = self._values.get("node_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preferred_availability_zones(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of preferred availability zones for the nodes in this cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-reshardingconfiguration.html#cfn-elasticache-globalreplicationgroup-reshardingconfiguration-preferredavailabilityzones
            '''
            result = self._values.get("preferred_availability_zones")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReshardingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnParameterGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_parameter_group_family": "cacheParameterGroupFamily",
        "description": "description",
        "properties": "properties",
        "tags": "tags",
    },
)
class CfnParameterGroupMixinProps:
    def __init__(
        self,
        *,
        cache_parameter_group_family: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnParameterGroupPropsMixin.

        :param cache_parameter_group_family: The name of the cache parameter group family that this cache parameter group is compatible with. Valid values are: ``valkey8`` | ``valkey7`` | ``memcached1.4`` | ``memcached1.5`` | ``memcached1.6`` | ``redis2.6`` | ``redis2.8`` | ``redis3.2`` | ``redis4.0`` | ``redis5.0`` | ``redis6.x`` | ``redis7``
        :param description: The description for this cache parameter group.
        :param properties: A comma-delimited list of parameter name/value pairs. For example:: "Properties" : { "cas_disabled" : "1", "chunk_size_growth_factor" : "1.02" }
        :param tags: A tag that can be added to an ElastiCache parameter group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your parameter groups. A tag with a null Value is permitted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-parametergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
            
            cfn_parameter_group_mixin_props = elasticache_mixins.CfnParameterGroupMixinProps(
                cache_parameter_group_family="cacheParameterGroupFamily",
                description="description",
                properties={
                    "properties_key": "properties"
                },
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81a1c75c18104579aeefeec3b403c4015dc700e3317500a2893473a043a765b)
            check_type(argname="argument cache_parameter_group_family", value=cache_parameter_group_family, expected_type=type_hints["cache_parameter_group_family"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_parameter_group_family is not None:
            self._values["cache_parameter_group_family"] = cache_parameter_group_family
        if description is not None:
            self._values["description"] = description
        if properties is not None:
            self._values["properties"] = properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cache_parameter_group_family(self) -> typing.Optional[builtins.str]:
        '''The name of the cache parameter group family that this cache parameter group is compatible with.

        Valid values are: ``valkey8`` | ``valkey7`` | ``memcached1.4`` | ``memcached1.5`` | ``memcached1.6`` | ``redis2.6`` | ``redis2.8`` | ``redis3.2`` | ``redis4.0`` | ``redis5.0`` | ``redis6.x`` | ``redis7``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-parametergroup.html#cfn-elasticache-parametergroup-cacheparametergroupfamily
        '''
        result = self._values.get("cache_parameter_group_family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for this cache parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-parametergroup.html#cfn-elasticache-parametergroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''A comma-delimited list of parameter name/value pairs.

        For example::

           "Properties" : { "cas_disabled" : "1", "chunk_size_growth_factor" : "1.02"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-parametergroup.html#cfn-elasticache-parametergroup-properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A tag that can be added to an ElastiCache parameter group.

        Tags are composed of a Key/Value pair. You can use tags to categorize and track all your parameter groups. A tag with a null Value is permitted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-parametergroup.html#cfn-elasticache-parametergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnParameterGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnParameterGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnParameterGroupPropsMixin",
):
    '''The ``AWS::ElastiCache::ParameterGroup`` type creates a new cache parameter group.

    Cache parameter groups control the parameters for a cache cluster.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-parametergroup.html
    :cloudformationResource: AWS::ElastiCache::ParameterGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
        
        cfn_parameter_group_props_mixin = elasticache_mixins.CfnParameterGroupPropsMixin(elasticache_mixins.CfnParameterGroupMixinProps(
            cache_parameter_group_family="cacheParameterGroupFamily",
            description="description",
            properties={
                "properties_key": "properties"
            },
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
        props: typing.Union[CfnParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElastiCache::ParameterGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01805cb0339b231a71ed5e39f4d89b5a9547fe2c42e86a90fc9a5eb01f871314)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fd616234e5aa551d6eec806f67b7d4b8feec75cae4829bce0c87ac5509f4569)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1509da515b4dffb5d7b7d8f026f713b90fd49dd8ddda6e2d1f9db7819a8f123c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnParameterGroupMixinProps:
        return typing.cast(CfnParameterGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnReplicationGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "at_rest_encryption_enabled": "atRestEncryptionEnabled",
        "auth_token": "authToken",
        "automatic_failover_enabled": "automaticFailoverEnabled",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "cache_node_type": "cacheNodeType",
        "cache_parameter_group_name": "cacheParameterGroupName",
        "cache_security_group_names": "cacheSecurityGroupNames",
        "cache_subnet_group_name": "cacheSubnetGroupName",
        "cluster_mode": "clusterMode",
        "data_tiering_enabled": "dataTieringEnabled",
        "engine": "engine",
        "engine_version": "engineVersion",
        "global_replication_group_id": "globalReplicationGroupId",
        "ip_discovery": "ipDiscovery",
        "kms_key_id": "kmsKeyId",
        "log_delivery_configurations": "logDeliveryConfigurations",
        "multi_az_enabled": "multiAzEnabled",
        "network_type": "networkType",
        "node_group_configuration": "nodeGroupConfiguration",
        "notification_topic_arn": "notificationTopicArn",
        "num_cache_clusters": "numCacheClusters",
        "num_node_groups": "numNodeGroups",
        "port": "port",
        "preferred_cache_cluster_a_zs": "preferredCacheClusterAZs",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "primary_cluster_id": "primaryClusterId",
        "replicas_per_node_group": "replicasPerNodeGroup",
        "replication_group_description": "replicationGroupDescription",
        "replication_group_id": "replicationGroupId",
        "security_group_ids": "securityGroupIds",
        "snapshot_arns": "snapshotArns",
        "snapshot_name": "snapshotName",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "snapshotting_cluster_id": "snapshottingClusterId",
        "snapshot_window": "snapshotWindow",
        "tags": "tags",
        "transit_encryption_enabled": "transitEncryptionEnabled",
        "transit_encryption_mode": "transitEncryptionMode",
        "user_group_ids": "userGroupIds",
    },
)
class CfnReplicationGroupMixinProps:
    def __init__(
        self,
        *,
        at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        auth_token: typing.Optional[builtins.str] = None,
        automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        cache_node_type: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        cluster_mode: typing.Optional[builtins.str] = None,
        data_tiering_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        global_replication_group_id: typing.Optional[builtins.str] = None,
        ip_discovery: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_delivery_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationGroupPropsMixin.LogDeliveryConfigurationRequestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        multi_az_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        network_type: typing.Optional[builtins.str] = None,
        node_group_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationGroupPropsMixin.NodeGroupConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        num_cache_clusters: typing.Optional[jsii.Number] = None,
        num_node_groups: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_cache_cluster_a_zs: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        primary_cluster_id: typing.Optional[builtins.str] = None,
        replicas_per_node_group: typing.Optional[jsii.Number] = None,
        replication_group_description: typing.Optional[builtins.str] = None,
        replication_group_id: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshotting_cluster_id: typing.Optional[builtins.str] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        user_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnReplicationGroupPropsMixin.

        :param at_rest_encryption_enabled: A flag that enables encryption at rest when set to ``true`` . *Required:* Only available when creating a replication group in an Amazon VPC using Redis OSS version ``3.2.6`` or ``4.x`` onward. Default: ``false``
        :param auth_token: *Reserved parameter.* The password used to access a password protected server. ``AuthToken`` can be specified only on replication groups where ``TransitEncryptionEnabled`` is ``true`` . For more information, see `Authenticating Valkey or Redis OSS users with the AUTH Command <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/auth.html>`_ . .. epigraph:: For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` . Password constraints: - Must be only printable ASCII characters. - Must be at least 16 characters and no more than 128 characters in length. - Nonalphanumeric characters are restricted to (!, &, #, $, ^, <, >, -, ). For more information, see `AUTH password <https://docs.aws.amazon.com/http://redis.io/commands/AUTH>`_ at http://redis.io/commands/AUTH. .. epigraph:: If ADDING the AuthToken, update requires `Replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param automatic_failover_enabled: Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails. ``AutomaticFailoverEnabled`` must be enabled for Valkey or Redis OSS (cluster mode enabled) replication groups. Default: false
        :param auto_minor_version_upgrade: If you are running Valkey 7.2 or later, or Redis OSS 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.
        :param cache_node_type: The compute and memory capacity of the nodes in the node group (shard). The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts. - General purpose: - Current generation: *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.24xlarge`` *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge`` *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge`` *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium`` *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium`` *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium`` - Previous generation: (not recommended) *T1 node types:* ``cache.t1.micro`` *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge`` *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge`` - Compute optimized: - Previous generation: (not recommended) *C1 node types:* ``cache.c1.xlarge`` - Memory optimized: - Current generation: *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge`` .. epigraph:: The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` . *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.24xlarge`` *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge`` *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge`` - Previous generation: (not recommended) *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge`` *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge`` For region availability, see `Supported Node Types by Amazon Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_
        :param cache_parameter_group_name: The name of the parameter group to associate with this replication group. If this argument is omitted, the default cache parameter group for the specified engine is used. If you are running Valkey or Redis OSS version 3.2.4 or later, only one node group (shard), and want to use a default parameter group, we recommend that you specify the parameter group by name. - To create a Valkey or Redis OSS (cluster mode disabled) replication group, use ``CacheParameterGroupName=default.redis3.2`` . - To create a Valkey or Redis OSS (cluster mode enabled) replication group, use ``CacheParameterGroupName=default.redis3.2.cluster.on`` .
        :param cache_security_group_names: A list of cache security group names to associate with this replication group.
        :param cache_subnet_group_name: The name of the cache subnet group to be used for the replication group. .. epigraph:: If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see `AWS::ElastiCache::SubnetGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html>`_ .
        :param cluster_mode: The mode can be enabled or disabled. To change the cluster mode from disabled to enabled, you must first set the cluster mode to compatible. The compatible mode allows your Valkey or Redis OSS clients to connect using both cluster mode enabled and cluster mode disabled. After you migrate all Valkey or Redis OSS clients to use cluster mode enabled, you can then complete cluster mode configuration and set the cluster mode to enabled. For more information, see `Modify cluster mode <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/modify-cluster-mode.html>`_ .
        :param data_tiering_enabled: Enables data tiering. Data tiering is only supported for replication groups using the r6gd node type. This parameter must be set to true when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/data-tiering.html>`_ .
        :param engine: The name of the cache engine to be used for the clusters in this replication group. The value must be set to ``valkey`` or ``redis`` . .. epigraph:: Upgrading an existing engine from redis to valkey is done through in-place migration, and requires a parameter group.
        :param engine_version: The version number of the cache engine to be used for the clusters in this replication group. To view the supported cache engine versions, use the ``DescribeCacheEngineVersions`` operation. *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SelectEngine.html#VersionManagement>`_ ) in the *ElastiCache User Guide* , but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.
        :param global_replication_group_id: The name of the Global datastore.
        :param ip_discovery: The network type you choose when creating a replication group, either ``ipv4`` | ``ipv6`` . IPv6 is supported for workloads using Valkey 7.2 and above, Redis OSS engine version 6.2 to 7.1 or Memcached engine version 1.6.6 and above on all instances built on the `Nitro system <https://docs.aws.amazon.com/ec2/nitro/>`_ .
        :param kms_key_id: The ID of the KMS key used to encrypt the disk on the cluster.
        :param log_delivery_configurations: Specifies the destination, format and type of the logs.
        :param multi_az_enabled: A flag indicating if you have Multi-AZ enabled to enhance fault tolerance. For more information, see `Minimizing Downtime: Multi-AZ <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/AutoFailover.html>`_ .
        :param network_type: Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` . IPv6 is supported for workloads using Valkey 7.2 and above, Redis OSS engine version 6.2 to 7.1 and Memcached engine version 1.6.6 and above on all instances built on the `Nitro system <https://docs.aws.amazon.com/ec2/nitro/>`_ .
        :param node_group_configuration: ``NodeGroupConfiguration`` is a property of the ``AWS::ElastiCache::ReplicationGroup`` resource that configures an Amazon ElastiCache (ElastiCache) Valkey or Redis OSS cluster node group. If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NodeGroupConfiguration`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NodeGroupConfiguration`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param notification_topic_arn: The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent. .. epigraph:: The Amazon SNS topic owner must be the same as the cluster owner.
        :param num_cache_clusters: The number of clusters this replication group initially has. This parameter is not used if there is more than one node group (shard). You should use ``ReplicasPerNodeGroup`` instead. If ``AutomaticFailoverEnabled`` is ``true`` , the value of this parameter must be at least 2. If ``AutomaticFailoverEnabled`` is ``false`` you can omit this parameter (it will default to 1), or you can explicitly set it to a value between 2 and 6. The maximum permitted value for ``NumCacheClusters`` is 6 (1 primary plus 5 replicas).
        :param num_node_groups: An optional parameter that specifies the number of node groups (shards) for this Valkey or Redis OSS (cluster mode enabled) replication group. For Valkey or Redis OSS (cluster mode disabled) either omit this parameter or set it to 1. If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NumNodeGroups`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NumNodeGroups`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ . Default: 1
        :param port: The port number on which each member of the replication group accepts connections.
        :param preferred_cache_cluster_a_zs: A list of EC2 Availability Zones in which the replication group's clusters are created. The order of the Availability Zones in the list is the order in which clusters are allocated. The primary cluster is created in the first AZ in the list. This parameter is not used if there is more than one node group (shard). You should use ``NodeGroupConfiguration`` instead. .. epigraph:: If you are creating your replication group in an Amazon VPC (recommended), you can only locate clusters in Availability Zones associated with the subnets in the selected subnet group. The number of Availability Zones listed must equal the value of ``NumCacheClusters`` . Default: system chosen Availability Zones.
        :param preferred_maintenance_window: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ``ddd`` are: - ``sun`` - ``mon`` - ``tue`` - ``wed`` - ``thu`` - ``fri`` - ``sat`` Example: ``sun:23:00-mon:01:30``
        :param primary_cluster_id: The identifier of the cluster that serves as the primary for this replication group. This cluster must already exist and have a status of ``available`` . This parameter is not required if ``NumCacheClusters`` , ``NumNodeGroups`` , or ``ReplicasPerNodeGroup`` is specified.
        :param replicas_per_node_group: An optional parameter that specifies the number of replica nodes in each node group (shard). Valid values are 0 to 5.
        :param replication_group_description: A user-created description for the replication group.
        :param replication_group_id: The replication group identifier. This parameter is stored as a lowercase string. Constraints: - A name must contain from 1 to 40 alphanumeric characters or hyphens. - The first character must be a letter. - A name cannot end with a hyphen or contain two consecutive hyphens.
        :param security_group_ids: One or more Amazon VPC security groups associated with this replication group. Use this parameter only when you are creating a replication group in an Amazon Virtual Private Cloud (Amazon VPC).
        :param snapshot_arns: A list of Amazon Resource Names (ARN) that uniquely identify the Valkey or Redis OSS RDB snapshot files stored in Amazon S3. The snapshot files are used to populate the new replication group. The Amazon S3 object name in the ARN cannot contain any commas. The new replication group will have the number of node groups (console: shards) specified by the parameter *NumNodeGroups* or the number of node groups configured by *NodeGroupConfiguration* regardless of the number of ARNs specified here. Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``
        :param snapshot_name: The name of a snapshot from which to restore data into the new replication group. The snapshot status changes to ``restoring`` while the new replication group is being created.
        :param snapshot_retention_limit: The number of days for which ElastiCache retains automatic snapshots before deleting them. For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot that was taken today is retained for 5 days before being deleted. Default: 0 (i.e., automatic backups are disabled for this cluster).
        :param snapshotting_cluster_id: The cluster ID that is used as the daily snapshot source for the replication group. This parameter cannot be set for Valkey or Redis OSS (cluster mode enabled) replication groups.
        :param snapshot_window: The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard). Example: ``05:00-09:00`` If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range.
        :param tags: A list of tags to be added to this resource. Tags are comma-separated key,value pairs (e.g. Key= ``myKey`` , Value= ``myKeyValue`` . You can include multiple tags as shown following: Key= ``myKey`` , Value= ``myKeyValue`` Key= ``mySecondKey`` , Value= ``mySecondKeyValue`` . Tags on replication groups will be replicated to all nodes.
        :param transit_encryption_enabled: A flag that enables in-transit encryption when set to ``true`` . This parameter is only available when creating a replication group in an Amazon VPC using Valkey version ``7.2`` and above, Redis OSS version ``3.2.6`` , or Redis OSS version ``4.x`` and above, and the cluster is being created in an Amazon VPC. If you enable in-transit encryption, you must also specify a value for ``CacheSubnetGroup`` . .. epigraph:: TransitEncryptionEnabled is required when creating a new valkey replication group. Default: ``false`` .. epigraph:: For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` .
        :param transit_encryption_mode: A setting that allows you to migrate your clients to use in-transit encryption, with no downtime. When setting ``TransitEncryptionEnabled`` to ``true`` , you can set your ``TransitEncryptionMode`` to ``preferred`` in the same request, to allow both encrypted and unencrypted connections at the same time. Once you migrate all your Valkey or Redis OSS clients to use encrypted connections you can modify the value to ``required`` to allow encrypted connections only. Setting ``TransitEncryptionMode`` to ``required`` is a two-step process that requires you to first set the ``TransitEncryptionMode`` to ``preferred`` , after that you can set ``TransitEncryptionMode`` to ``required`` . This process will not trigger the replacement of the replication group.
        :param user_group_ids: The ID of user group to associate with the replication group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
            
            cfn_replication_group_mixin_props = elasticache_mixins.CfnReplicationGroupMixinProps(
                at_rest_encryption_enabled=False,
                auth_token="authToken",
                automatic_failover_enabled=False,
                auto_minor_version_upgrade=False,
                cache_node_type="cacheNodeType",
                cache_parameter_group_name="cacheParameterGroupName",
                cache_security_group_names=["cacheSecurityGroupNames"],
                cache_subnet_group_name="cacheSubnetGroupName",
                cluster_mode="clusterMode",
                data_tiering_enabled=False,
                engine="engine",
                engine_version="engineVersion",
                global_replication_group_id="globalReplicationGroupId",
                ip_discovery="ipDiscovery",
                kms_key_id="kmsKeyId",
                log_delivery_configurations=[elasticache_mixins.CfnReplicationGroupPropsMixin.LogDeliveryConfigurationRequestProperty(
                    destination_details=elasticache_mixins.CfnReplicationGroupPropsMixin.DestinationDetailsProperty(
                        cloud_watch_logs_details=elasticache_mixins.CfnReplicationGroupPropsMixin.CloudWatchLogsDestinationDetailsProperty(
                            log_group="logGroup"
                        ),
                        kinesis_firehose_details=elasticache_mixins.CfnReplicationGroupPropsMixin.KinesisFirehoseDestinationDetailsProperty(
                            delivery_stream="deliveryStream"
                        )
                    ),
                    destination_type="destinationType",
                    log_format="logFormat",
                    log_type="logType"
                )],
                multi_az_enabled=False,
                network_type="networkType",
                node_group_configuration=[elasticache_mixins.CfnReplicationGroupPropsMixin.NodeGroupConfigurationProperty(
                    node_group_id="nodeGroupId",
                    primary_availability_zone="primaryAvailabilityZone",
                    replica_availability_zones=["replicaAvailabilityZones"],
                    replica_count=123,
                    slots="slots"
                )],
                notification_topic_arn="notificationTopicArn",
                num_cache_clusters=123,
                num_node_groups=123,
                port=123,
                preferred_cache_cluster_aZs=["preferredCacheClusterAZs"],
                preferred_maintenance_window="preferredMaintenanceWindow",
                primary_cluster_id="primaryClusterId",
                replicas_per_node_group=123,
                replication_group_description="replicationGroupDescription",
                replication_group_id="replicationGroupId",
                security_group_ids=["securityGroupIds"],
                snapshot_arns=["snapshotArns"],
                snapshot_name="snapshotName",
                snapshot_retention_limit=123,
                snapshotting_cluster_id="snapshottingClusterId",
                snapshot_window="snapshotWindow",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                transit_encryption_enabled=False,
                transit_encryption_mode="transitEncryptionMode",
                user_group_ids=["userGroupIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc505e761c91eb763676cd4a8b05f508401e1a9e43340573618327bce15eed0c)
            check_type(argname="argument at_rest_encryption_enabled", value=at_rest_encryption_enabled, expected_type=type_hints["at_rest_encryption_enabled"])
            check_type(argname="argument auth_token", value=auth_token, expected_type=type_hints["auth_token"])
            check_type(argname="argument automatic_failover_enabled", value=automatic_failover_enabled, expected_type=type_hints["automatic_failover_enabled"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument cache_node_type", value=cache_node_type, expected_type=type_hints["cache_node_type"])
            check_type(argname="argument cache_parameter_group_name", value=cache_parameter_group_name, expected_type=type_hints["cache_parameter_group_name"])
            check_type(argname="argument cache_security_group_names", value=cache_security_group_names, expected_type=type_hints["cache_security_group_names"])
            check_type(argname="argument cache_subnet_group_name", value=cache_subnet_group_name, expected_type=type_hints["cache_subnet_group_name"])
            check_type(argname="argument cluster_mode", value=cluster_mode, expected_type=type_hints["cluster_mode"])
            check_type(argname="argument data_tiering_enabled", value=data_tiering_enabled, expected_type=type_hints["data_tiering_enabled"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument global_replication_group_id", value=global_replication_group_id, expected_type=type_hints["global_replication_group_id"])
            check_type(argname="argument ip_discovery", value=ip_discovery, expected_type=type_hints["ip_discovery"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument log_delivery_configurations", value=log_delivery_configurations, expected_type=type_hints["log_delivery_configurations"])
            check_type(argname="argument multi_az_enabled", value=multi_az_enabled, expected_type=type_hints["multi_az_enabled"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument node_group_configuration", value=node_group_configuration, expected_type=type_hints["node_group_configuration"])
            check_type(argname="argument notification_topic_arn", value=notification_topic_arn, expected_type=type_hints["notification_topic_arn"])
            check_type(argname="argument num_cache_clusters", value=num_cache_clusters, expected_type=type_hints["num_cache_clusters"])
            check_type(argname="argument num_node_groups", value=num_node_groups, expected_type=type_hints["num_node_groups"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_cache_cluster_a_zs", value=preferred_cache_cluster_a_zs, expected_type=type_hints["preferred_cache_cluster_a_zs"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument primary_cluster_id", value=primary_cluster_id, expected_type=type_hints["primary_cluster_id"])
            check_type(argname="argument replicas_per_node_group", value=replicas_per_node_group, expected_type=type_hints["replicas_per_node_group"])
            check_type(argname="argument replication_group_description", value=replication_group_description, expected_type=type_hints["replication_group_description"])
            check_type(argname="argument replication_group_id", value=replication_group_id, expected_type=type_hints["replication_group_id"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument snapshot_arns", value=snapshot_arns, expected_type=type_hints["snapshot_arns"])
            check_type(argname="argument snapshot_name", value=snapshot_name, expected_type=type_hints["snapshot_name"])
            check_type(argname="argument snapshot_retention_limit", value=snapshot_retention_limit, expected_type=type_hints["snapshot_retention_limit"])
            check_type(argname="argument snapshotting_cluster_id", value=snapshotting_cluster_id, expected_type=type_hints["snapshotting_cluster_id"])
            check_type(argname="argument snapshot_window", value=snapshot_window, expected_type=type_hints["snapshot_window"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transit_encryption_enabled", value=transit_encryption_enabled, expected_type=type_hints["transit_encryption_enabled"])
            check_type(argname="argument transit_encryption_mode", value=transit_encryption_mode, expected_type=type_hints["transit_encryption_mode"])
            check_type(argname="argument user_group_ids", value=user_group_ids, expected_type=type_hints["user_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if at_rest_encryption_enabled is not None:
            self._values["at_rest_encryption_enabled"] = at_rest_encryption_enabled
        if auth_token is not None:
            self._values["auth_token"] = auth_token
        if automatic_failover_enabled is not None:
            self._values["automatic_failover_enabled"] = automatic_failover_enabled
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if cache_node_type is not None:
            self._values["cache_node_type"] = cache_node_type
        if cache_parameter_group_name is not None:
            self._values["cache_parameter_group_name"] = cache_parameter_group_name
        if cache_security_group_names is not None:
            self._values["cache_security_group_names"] = cache_security_group_names
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name
        if cluster_mode is not None:
            self._values["cluster_mode"] = cluster_mode
        if data_tiering_enabled is not None:
            self._values["data_tiering_enabled"] = data_tiering_enabled
        if engine is not None:
            self._values["engine"] = engine
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if global_replication_group_id is not None:
            self._values["global_replication_group_id"] = global_replication_group_id
        if ip_discovery is not None:
            self._values["ip_discovery"] = ip_discovery
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if log_delivery_configurations is not None:
            self._values["log_delivery_configurations"] = log_delivery_configurations
        if multi_az_enabled is not None:
            self._values["multi_az_enabled"] = multi_az_enabled
        if network_type is not None:
            self._values["network_type"] = network_type
        if node_group_configuration is not None:
            self._values["node_group_configuration"] = node_group_configuration
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if num_cache_clusters is not None:
            self._values["num_cache_clusters"] = num_cache_clusters
        if num_node_groups is not None:
            self._values["num_node_groups"] = num_node_groups
        if port is not None:
            self._values["port"] = port
        if preferred_cache_cluster_a_zs is not None:
            self._values["preferred_cache_cluster_a_zs"] = preferred_cache_cluster_a_zs
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if primary_cluster_id is not None:
            self._values["primary_cluster_id"] = primary_cluster_id
        if replicas_per_node_group is not None:
            self._values["replicas_per_node_group"] = replicas_per_node_group
        if replication_group_description is not None:
            self._values["replication_group_description"] = replication_group_description
        if replication_group_id is not None:
            self._values["replication_group_id"] = replication_group_id
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if snapshot_arns is not None:
            self._values["snapshot_arns"] = snapshot_arns
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if snapshotting_cluster_id is not None:
            self._values["snapshotting_cluster_id"] = snapshotting_cluster_id
        if snapshot_window is not None:
            self._values["snapshot_window"] = snapshot_window
        if tags is not None:
            self._values["tags"] = tags
        if transit_encryption_enabled is not None:
            self._values["transit_encryption_enabled"] = transit_encryption_enabled
        if transit_encryption_mode is not None:
            self._values["transit_encryption_mode"] = transit_encryption_mode
        if user_group_ids is not None:
            self._values["user_group_ids"] = user_group_ids

    @builtins.property
    def at_rest_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A flag that enables encryption at rest when set to ``true`` .

        *Required:* Only available when creating a replication group in an Amazon VPC using Redis OSS version ``3.2.6`` or ``4.x`` onward.

        Default: ``false``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-atrestencryptionenabled
        '''
        result = self._values.get("at_rest_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def auth_token(self) -> typing.Optional[builtins.str]:
        '''*Reserved parameter.* The password used to access a password protected server.

        ``AuthToken`` can be specified only on replication groups where ``TransitEncryptionEnabled`` is ``true`` . For more information, see `Authenticating Valkey or Redis OSS users with the AUTH Command <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/auth.html>`_ .
        .. epigraph::

           For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` .

        Password constraints:

        - Must be only printable ASCII characters.
        - Must be at least 16 characters and no more than 128 characters in length.
        - Nonalphanumeric characters are restricted to (!, &, #, $, ^, <, >, -, ).

        For more information, see `AUTH password <https://docs.aws.amazon.com/http://redis.io/commands/AUTH>`_ at http://redis.io/commands/AUTH.
        .. epigraph::

           If ADDING the AuthToken, update requires `Replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-authtoken
        '''
        result = self._values.get("auth_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails.

        ``AutomaticFailoverEnabled`` must be enabled for Valkey or Redis OSS (cluster mode enabled) replication groups.

        Default: false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-automaticfailoverenabled
        '''
        result = self._values.get("automatic_failover_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If you are running Valkey 7.2 or later, or Redis OSS 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cache_node_type(self) -> typing.Optional[builtins.str]:
        '''The compute and memory capacity of the nodes in the node group (shard).

        The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts.

        - General purpose:
        - Current generation:

        *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.24xlarge``

        *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge``

        *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge``

        *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium``

        *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium``

        *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium``

        - Previous generation: (not recommended)

        *T1 node types:* ``cache.t1.micro``

        *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge``

        *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge``

        - Compute optimized:
        - Previous generation: (not recommended)

        *C1 node types:* ``cache.c1.xlarge``

        - Memory optimized:
        - Current generation:

        *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge``
        .. epigraph::

           The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` .

        *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.24xlarge``

        *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge``

        *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge``

        - Previous generation: (not recommended)

        *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge``

        *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge``

        For region availability, see `Supported Node Types by Amazon Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachenodetype
        '''
        result = self._values.get("cache_node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group to associate with this replication group.

        If this argument is omitted, the default cache parameter group for the specified engine is used.

        If you are running Valkey or Redis OSS version 3.2.4 or later, only one node group (shard), and want to use a default parameter group, we recommend that you specify the parameter group by name.

        - To create a Valkey or Redis OSS (cluster mode disabled) replication group, use ``CacheParameterGroupName=default.redis3.2`` .
        - To create a Valkey or Redis OSS (cluster mode enabled) replication group, use ``CacheParameterGroupName=default.redis3.2.cluster.on`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cacheparametergroupname
        '''
        result = self._values.get("cache_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_security_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of cache security group names to associate with this replication group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesecuritygroupnames
        '''
        result = self._values.get("cache_security_group_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cache subnet group to be used for the replication group.

        .. epigraph::

           If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see `AWS::ElastiCache::SubnetGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesubnetgroupname
        '''
        result = self._values.get("cache_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_mode(self) -> typing.Optional[builtins.str]:
        '''The mode can be enabled or disabled.

        To change the cluster mode from disabled to enabled, you must first set the cluster mode to compatible. The compatible mode allows your Valkey or Redis OSS clients to connect using both cluster mode enabled and cluster mode disabled. After you migrate all Valkey or Redis OSS clients to use cluster mode enabled, you can then complete cluster mode configuration and set the cluster mode to enabled. For more information, see `Modify cluster mode <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/modify-cluster-mode.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-clustermode
        '''
        result = self._values.get("cluster_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_tiering_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables data tiering.

        Data tiering is only supported for replication groups using the r6gd node type. This parameter must be set to true when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/data-tiering.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-datatieringenabled
        '''
        result = self._values.get("data_tiering_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The name of the cache engine to be used for the clusters in this replication group.

        The value must be set to ``valkey`` or ``redis`` .
        .. epigraph::

           Upgrading an existing engine from redis to valkey is done through in-place migration, and requires a parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the cache engine to be used for the clusters in this replication group.

        To view the supported cache engine versions, use the ``DescribeCacheEngineVersions`` operation.

        *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SelectEngine.html#VersionManagement>`_ ) in the *ElastiCache User Guide* , but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_replication_group_id(self) -> typing.Optional[builtins.str]:
        '''The name of the Global datastore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-globalreplicationgroupid
        '''
        result = self._values.get("global_replication_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_discovery(self) -> typing.Optional[builtins.str]:
        '''The network type you choose when creating a replication group, either ``ipv4`` | ``ipv6`` .

        IPv6 is supported for workloads using Valkey 7.2 and above, Redis OSS engine version 6.2 to 7.1 or Memcached engine version 1.6.6 and above on all instances built on the `Nitro system <https://docs.aws.amazon.com/ec2/nitro/>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-ipdiscovery
        '''
        result = self._values.get("ip_discovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the KMS key used to encrypt the disk on the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationGroupPropsMixin.LogDeliveryConfigurationRequestProperty"]]]]:
        '''Specifies the destination, format and type of the logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-logdeliveryconfigurations
        '''
        result = self._values.get("log_delivery_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationGroupPropsMixin.LogDeliveryConfigurationRequestProperty"]]]], result)

    @builtins.property
    def multi_az_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A flag indicating if you have Multi-AZ enabled to enhance fault tolerance.

        For more information, see `Minimizing Downtime: Multi-AZ <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/AutoFailover.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-multiazenabled
        '''
        result = self._values.get("multi_az_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` .

        IPv6 is supported for workloads using Valkey 7.2 and above, Redis OSS engine version 6.2 to 7.1 and Memcached engine version 1.6.6 and above on all instances built on the `Nitro system <https://docs.aws.amazon.com/ec2/nitro/>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationGroupPropsMixin.NodeGroupConfigurationProperty"]]]]:
        '''``NodeGroupConfiguration`` is a property of the ``AWS::ElastiCache::ReplicationGroup`` resource that configures an Amazon ElastiCache (ElastiCache) Valkey or Redis OSS cluster node group.

        If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NodeGroupConfiguration`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NodeGroupConfiguration`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-nodegroupconfiguration
        '''
        result = self._values.get("node_group_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationGroupPropsMixin.NodeGroupConfigurationProperty"]]]], result)

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent.

        .. epigraph::

           The Amazon SNS topic owner must be the same as the cluster owner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-notificationtopicarn
        '''
        result = self._values.get("notification_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_cache_clusters(self) -> typing.Optional[jsii.Number]:
        '''The number of clusters this replication group initially has.

        This parameter is not used if there is more than one node group (shard). You should use ``ReplicasPerNodeGroup`` instead.

        If ``AutomaticFailoverEnabled`` is ``true`` , the value of this parameter must be at least 2. If ``AutomaticFailoverEnabled`` is ``false`` you can omit this parameter (it will default to 1), or you can explicitly set it to a value between 2 and 6.

        The maximum permitted value for ``NumCacheClusters`` is 6 (1 primary plus 5 replicas).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numcacheclusters
        '''
        result = self._values.get("num_cache_clusters")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def num_node_groups(self) -> typing.Optional[jsii.Number]:
        '''An optional parameter that specifies the number of node groups (shards) for this Valkey or Redis OSS (cluster mode enabled) replication group.

        For Valkey or Redis OSS (cluster mode disabled) either omit this parameter or set it to 1.

        If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NumNodeGroups`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NumNodeGroups`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        Default: 1

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numnodegroups
        '''
        result = self._values.get("num_node_groups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number on which each member of the replication group accepts connections.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_cache_cluster_a_zs(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of EC2 Availability Zones in which the replication group's clusters are created.

        The order of the Availability Zones in the list is the order in which clusters are allocated. The primary cluster is created in the first AZ in the list.

        This parameter is not used if there is more than one node group (shard). You should use ``NodeGroupConfiguration`` instead.
        .. epigraph::

           If you are creating your replication group in an Amazon VPC (recommended), you can only locate clusters in Availability Zones associated with the subnets in the selected subnet group.

           The number of Availability Zones listed must equal the value of ``NumCacheClusters`` .

        Default: system chosen Availability Zones.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredcacheclusterazs
        '''
        result = self._values.get("preferred_cache_cluster_a_zs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Specifies the weekly time range during which maintenance on the cluster is performed.

        It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period.

        Valid values for ``ddd`` are:

        - ``sun``
        - ``mon``
        - ``tue``
        - ``wed``
        - ``thu``
        - ``fri``
        - ``sat``

        Example: ``sun:23:00-mon:01:30``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_cluster_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the cluster that serves as the primary for this replication group.

        This cluster must already exist and have a status of ``available`` .

        This parameter is not required if ``NumCacheClusters`` , ``NumNodeGroups`` , or ``ReplicasPerNodeGroup`` is specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-primaryclusterid
        '''
        result = self._values.get("primary_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replicas_per_node_group(self) -> typing.Optional[jsii.Number]:
        '''An optional parameter that specifies the number of replica nodes in each node group (shard).

        Valid values are 0 to 5.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicaspernodegroup
        '''
        result = self._values.get("replicas_per_node_group")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replication_group_description(self) -> typing.Optional[builtins.str]:
        '''A user-created description for the replication group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupdescription
        '''
        result = self._values.get("replication_group_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_group_id(self) -> typing.Optional[builtins.str]:
        '''The replication group identifier. This parameter is stored as a lowercase string.

        Constraints:

        - A name must contain from 1 to 40 alphanumeric characters or hyphens.
        - The first character must be a letter.
        - A name cannot end with a hyphen or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupid
        '''
        result = self._values.get("replication_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more Amazon VPC security groups associated with this replication group.

        Use this parameter only when you are creating a replication group in an Amazon Virtual Private Cloud (Amazon VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARN) that uniquely identify the Valkey or Redis OSS RDB snapshot files stored in Amazon S3.

        The snapshot files are used to populate the new replication group. The Amazon S3 object name in the ARN cannot contain any commas. The new replication group will have the number of node groups (console: shards) specified by the parameter *NumNodeGroups* or the number of node groups configured by *NodeGroupConfiguration* regardless of the number of ARNs specified here.

        Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotarns
        '''
        result = self._values.get("snapshot_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of a snapshot from which to restore data into the new replication group.

        The snapshot status changes to ``restoring`` while the new replication group is being created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotname
        '''
        result = self._values.get("snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which ElastiCache retains automatic snapshots before deleting them.

        For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot that was taken today is retained for 5 days before being deleted.

        Default: 0 (i.e., automatic backups are disabled for this cluster).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotretentionlimit
        '''
        result = self._values.get("snapshot_retention_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshotting_cluster_id(self) -> typing.Optional[builtins.str]:
        '''The cluster ID that is used as the daily snapshot source for the replication group.

        This parameter cannot be set for Valkey or Redis OSS (cluster mode enabled) replication groups.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshottingclusterid
        '''
        result = self._values.get("snapshotting_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard).

        Example: ``05:00-09:00``

        If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotwindow
        '''
        result = self._values.get("snapshot_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to be added to this resource.

        Tags are comma-separated key,value pairs (e.g. Key= ``myKey`` , Value= ``myKeyValue`` . You can include multiple tags as shown following: Key= ``myKey`` , Value= ``myKeyValue`` Key= ``mySecondKey`` , Value= ``mySecondKeyValue`` . Tags on replication groups will be replicated to all nodes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A flag that enables in-transit encryption when set to ``true`` .

        This parameter is only available when creating a replication group in an Amazon VPC using Valkey version ``7.2`` and above, Redis OSS version ``3.2.6`` , or Redis OSS version ``4.x`` and above, and the cluster is being created in an Amazon VPC.

        If you enable in-transit encryption, you must also specify a value for ``CacheSubnetGroup`` .
        .. epigraph::

           TransitEncryptionEnabled is required when creating a new valkey replication group.

        Default: ``false``
        .. epigraph::

           For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-transitencryptionenabled
        '''
        result = self._values.get("transit_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def transit_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''A setting that allows you to migrate your clients to use in-transit encryption, with no downtime.

        When setting ``TransitEncryptionEnabled`` to ``true`` , you can set your ``TransitEncryptionMode`` to ``preferred`` in the same request, to allow both encrypted and unencrypted connections at the same time. Once you migrate all your Valkey or Redis OSS clients to use encrypted connections you can modify the value to ``required`` to allow encrypted connections only.

        Setting ``TransitEncryptionMode`` to ``required`` is a two-step process that requires you to first set the ``TransitEncryptionMode`` to ``preferred`` , after that you can set ``TransitEncryptionMode`` to ``required`` .

        This process will not trigger the replacement of the replication group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-transitencryptionmode
        '''
        result = self._values.get("transit_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ID of user group to associate with the replication group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-usergroupids
        '''
        result = self._values.get("user_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReplicationGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnReplicationGroupPropsMixin",
):
    '''The ``AWS::ElastiCache::ReplicationGroup`` resource creates an Amazon ElastiCache (Valkey or Redis OSS) replication group.

    A Valkey or Redis OSS (cluster mode disabled) replication group is a collection of cache clusters, where one of the clusters is a primary read-write cluster and the others are read-only replicas.

    A Valkey or Redis OSS (cluster mode enabled) cluster is comprised of from 1 to 90 shards (API/CLI: node groups). Each shard has a primary node and up to 5 read-only replica nodes. The configuration can range from 90 shards and 0 replicas to 15 shards and 5 replicas, which is the maximum number or replicas allowed.

    The node or shard limit can be increased to a maximum of 500 per cluster if the engine version is Valkey 7.2 or higher, or Redis OSS 5.0.6 or higher. For example, you can choose to configure a 500 node cluster that ranges between 83 shards (one primary and 5 replicas per shard) and 500 shards (single primary and no replicas). Make sure there are enough available IP addresses to accommodate the increase. Common pitfalls include the subnets in the subnet group have too small a CIDR range or the subnets are shared and heavily used by other clusters. For more information, see `Creating a Subnet Group <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SubnetGroups.Creating.html>`_ . For versions below 5.0.6, the limit is 250 per cluster.

    To request a limit increase, see `Amazon Service Limits <https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html>`_ and choose the limit type *Nodes per cluster per instance type* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html
    :cloudformationResource: AWS::ElastiCache::ReplicationGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
        
        cfn_replication_group_props_mixin = elasticache_mixins.CfnReplicationGroupPropsMixin(elasticache_mixins.CfnReplicationGroupMixinProps(
            at_rest_encryption_enabled=False,
            auth_token="authToken",
            automatic_failover_enabled=False,
            auto_minor_version_upgrade=False,
            cache_node_type="cacheNodeType",
            cache_parameter_group_name="cacheParameterGroupName",
            cache_security_group_names=["cacheSecurityGroupNames"],
            cache_subnet_group_name="cacheSubnetGroupName",
            cluster_mode="clusterMode",
            data_tiering_enabled=False,
            engine="engine",
            engine_version="engineVersion",
            global_replication_group_id="globalReplicationGroupId",
            ip_discovery="ipDiscovery",
            kms_key_id="kmsKeyId",
            log_delivery_configurations=[elasticache_mixins.CfnReplicationGroupPropsMixin.LogDeliveryConfigurationRequestProperty(
                destination_details=elasticache_mixins.CfnReplicationGroupPropsMixin.DestinationDetailsProperty(
                    cloud_watch_logs_details=elasticache_mixins.CfnReplicationGroupPropsMixin.CloudWatchLogsDestinationDetailsProperty(
                        log_group="logGroup"
                    ),
                    kinesis_firehose_details=elasticache_mixins.CfnReplicationGroupPropsMixin.KinesisFirehoseDestinationDetailsProperty(
                        delivery_stream="deliveryStream"
                    )
                ),
                destination_type="destinationType",
                log_format="logFormat",
                log_type="logType"
            )],
            multi_az_enabled=False,
            network_type="networkType",
            node_group_configuration=[elasticache_mixins.CfnReplicationGroupPropsMixin.NodeGroupConfigurationProperty(
                node_group_id="nodeGroupId",
                primary_availability_zone="primaryAvailabilityZone",
                replica_availability_zones=["replicaAvailabilityZones"],
                replica_count=123,
                slots="slots"
            )],
            notification_topic_arn="notificationTopicArn",
            num_cache_clusters=123,
            num_node_groups=123,
            port=123,
            preferred_cache_cluster_aZs=["preferredCacheClusterAZs"],
            preferred_maintenance_window="preferredMaintenanceWindow",
            primary_cluster_id="primaryClusterId",
            replicas_per_node_group=123,
            replication_group_description="replicationGroupDescription",
            replication_group_id="replicationGroupId",
            security_group_ids=["securityGroupIds"],
            snapshot_arns=["snapshotArns"],
            snapshot_name="snapshotName",
            snapshot_retention_limit=123,
            snapshotting_cluster_id="snapshottingClusterId",
            snapshot_window="snapshotWindow",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            transit_encryption_enabled=False,
            transit_encryption_mode="transitEncryptionMode",
            user_group_ids=["userGroupIds"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReplicationGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElastiCache::ReplicationGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af8925354708f65fad81dd8f98f1f8fe5de8e4be58e9de69f5da13e4b63159c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b4fb2d1498800422aa582c3e01fd5b979e61d0448ebefcf5f963c38467df228)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db23d6536b3dadcdb41bcfd73d6396f28cb58b14e18cb224b39c14d1673e670)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReplicationGroupMixinProps:
        return typing.cast(CfnReplicationGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnReplicationGroupPropsMixin.CloudWatchLogsDestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group": "logGroup"},
    )
    class CloudWatchLogsDestinationDetailsProperty:
        def __init__(self, *, log_group: typing.Optional[builtins.str] = None) -> None:
            '''The configuration details of the CloudWatch Logs destination.

            Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.

            :param log_group: The name of the CloudWatch Logs log group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-cloudwatchlogsdestinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                cloud_watch_logs_destination_details_property = elasticache_mixins.CfnReplicationGroupPropsMixin.CloudWatchLogsDestinationDetailsProperty(
                    log_group="logGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc5a56d14566838ed79e52b96da38c27a65d1f7cb06473170f9d9365c956834d)
                check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group is not None:
                self._values["log_group"] = log_group

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch Logs log group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-cloudwatchlogsdestinationdetails.html#cfn-elasticache-replicationgroup-cloudwatchlogsdestinationdetails-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsDestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnReplicationGroupPropsMixin.DestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_details": "cloudWatchLogsDetails",
            "kinesis_firehose_details": "kinesisFirehoseDetails",
        },
    )
    class DestinationDetailsProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationGroupPropsMixin.CloudWatchLogsDestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_firehose_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationGroupPropsMixin.KinesisFirehoseDestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.

            :param cloud_watch_logs_details: The configuration details of the CloudWatch Logs destination. Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.
            :param kinesis_firehose_details: The configuration details of the Kinesis Data Firehose destination. Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-destinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                destination_details_property = elasticache_mixins.CfnReplicationGroupPropsMixin.DestinationDetailsProperty(
                    cloud_watch_logs_details=elasticache_mixins.CfnReplicationGroupPropsMixin.CloudWatchLogsDestinationDetailsProperty(
                        log_group="logGroup"
                    ),
                    kinesis_firehose_details=elasticache_mixins.CfnReplicationGroupPropsMixin.KinesisFirehoseDestinationDetailsProperty(
                        delivery_stream="deliveryStream"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__023e911c2616a60223bdd5249ba9753fd689ad9338fb3c4f537baac96f66ee54)
                check_type(argname="argument cloud_watch_logs_details", value=cloud_watch_logs_details, expected_type=type_hints["cloud_watch_logs_details"])
                check_type(argname="argument kinesis_firehose_details", value=kinesis_firehose_details, expected_type=type_hints["kinesis_firehose_details"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_details is not None:
                self._values["cloud_watch_logs_details"] = cloud_watch_logs_details
            if kinesis_firehose_details is not None:
                self._values["kinesis_firehose_details"] = kinesis_firehose_details

        @builtins.property
        def cloud_watch_logs_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationGroupPropsMixin.CloudWatchLogsDestinationDetailsProperty"]]:
            '''The configuration details of the CloudWatch Logs destination.

            Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-destinationdetails.html#cfn-elasticache-replicationgroup-destinationdetails-cloudwatchlogsdetails
            '''
            result = self._values.get("cloud_watch_logs_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationGroupPropsMixin.CloudWatchLogsDestinationDetailsProperty"]], result)

        @builtins.property
        def kinesis_firehose_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationGroupPropsMixin.KinesisFirehoseDestinationDetailsProperty"]]:
            '''The configuration details of the Kinesis Data Firehose destination.

            Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-destinationdetails.html#cfn-elasticache-replicationgroup-destinationdetails-kinesisfirehosedetails
            '''
            result = self._values.get("kinesis_firehose_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationGroupPropsMixin.KinesisFirehoseDestinationDetailsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnReplicationGroupPropsMixin.KinesisFirehoseDestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_stream": "deliveryStream"},
    )
    class KinesisFirehoseDestinationDetailsProperty:
        def __init__(
            self,
            *,
            delivery_stream: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration details of the Kinesis Data Firehose destination.

            Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :param delivery_stream: The name of the Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-kinesisfirehosedestinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                kinesis_firehose_destination_details_property = elasticache_mixins.CfnReplicationGroupPropsMixin.KinesisFirehoseDestinationDetailsProperty(
                    delivery_stream="deliveryStream"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1361be1cfdfdb6c414283324cbb736cf784c2ebcf06c9c5c2723e1829cb5424)
                check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_stream is not None:
                self._values["delivery_stream"] = delivery_stream

        @builtins.property
        def delivery_stream(self) -> typing.Optional[builtins.str]:
            '''The name of the Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-kinesisfirehosedestinationdetails.html#cfn-elasticache-replicationgroup-kinesisfirehosedestinationdetails-deliverystream
            '''
            result = self._values.get("delivery_stream")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseDestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnReplicationGroupPropsMixin.LogDeliveryConfigurationRequestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_details": "destinationDetails",
            "destination_type": "destinationType",
            "log_format": "logFormat",
            "log_type": "logType",
        },
    )
    class LogDeliveryConfigurationRequestProperty:
        def __init__(
            self,
            *,
            destination_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicationGroupPropsMixin.DestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            destination_type: typing.Optional[builtins.str] = None,
            log_format: typing.Optional[builtins.str] = None,
            log_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the destination, format and type of the logs.

            :param destination_details: Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.
            :param destination_type: Specify either CloudWatch Logs or Kinesis Data Firehose as the destination type. Valid values are either ``cloudwatch-logs`` or ``kinesis-firehose`` .
            :param log_format: Valid values are either ``json`` or ``text`` .
            :param log_type: Valid value is either ``slow-log`` , which refers to `slow-log <https://docs.aws.amazon.com/https://redis.io/commands/slowlog>`_ or ``engine-log`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-logdeliveryconfigurationrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                log_delivery_configuration_request_property = elasticache_mixins.CfnReplicationGroupPropsMixin.LogDeliveryConfigurationRequestProperty(
                    destination_details=elasticache_mixins.CfnReplicationGroupPropsMixin.DestinationDetailsProperty(
                        cloud_watch_logs_details=elasticache_mixins.CfnReplicationGroupPropsMixin.CloudWatchLogsDestinationDetailsProperty(
                            log_group="logGroup"
                        ),
                        kinesis_firehose_details=elasticache_mixins.CfnReplicationGroupPropsMixin.KinesisFirehoseDestinationDetailsProperty(
                            delivery_stream="deliveryStream"
                        )
                    ),
                    destination_type="destinationType",
                    log_format="logFormat",
                    log_type="logType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f74b929b2af970a859e818c4d31a4962cc0f598bdc54da736a946edf6a0302a)
                check_type(argname="argument destination_details", value=destination_details, expected_type=type_hints["destination_details"])
                check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
                check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
                check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_details is not None:
                self._values["destination_details"] = destination_details
            if destination_type is not None:
                self._values["destination_type"] = destination_type
            if log_format is not None:
                self._values["log_format"] = log_format
            if log_type is not None:
                self._values["log_type"] = log_type

        @builtins.property
        def destination_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationGroupPropsMixin.DestinationDetailsProperty"]]:
            '''Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-logdeliveryconfigurationrequest.html#cfn-elasticache-replicationgroup-logdeliveryconfigurationrequest-destinationdetails
            '''
            result = self._values.get("destination_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicationGroupPropsMixin.DestinationDetailsProperty"]], result)

        @builtins.property
        def destination_type(self) -> typing.Optional[builtins.str]:
            '''Specify either CloudWatch Logs or Kinesis Data Firehose as the destination type.

            Valid values are either ``cloudwatch-logs`` or ``kinesis-firehose`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-logdeliveryconfigurationrequest.html#cfn-elasticache-replicationgroup-logdeliveryconfigurationrequest-destinationtype
            '''
            result = self._values.get("destination_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_format(self) -> typing.Optional[builtins.str]:
            '''Valid values are either ``json`` or ``text`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-logdeliveryconfigurationrequest.html#cfn-elasticache-replicationgroup-logdeliveryconfigurationrequest-logformat
            '''
            result = self._values.get("log_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_type(self) -> typing.Optional[builtins.str]:
            '''Valid value is either ``slow-log`` , which refers to `slow-log <https://docs.aws.amazon.com/https://redis.io/commands/slowlog>`_ or ``engine-log`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-logdeliveryconfigurationrequest.html#cfn-elasticache-replicationgroup-logdeliveryconfigurationrequest-logtype
            '''
            result = self._values.get("log_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDeliveryConfigurationRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnReplicationGroupPropsMixin.NodeGroupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "node_group_id": "nodeGroupId",
            "primary_availability_zone": "primaryAvailabilityZone",
            "replica_availability_zones": "replicaAvailabilityZones",
            "replica_count": "replicaCount",
            "slots": "slots",
        },
    )
    class NodeGroupConfigurationProperty:
        def __init__(
            self,
            *,
            node_group_id: typing.Optional[builtins.str] = None,
            primary_availability_zone: typing.Optional[builtins.str] = None,
            replica_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
            replica_count: typing.Optional[jsii.Number] = None,
            slots: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``NodeGroupConfiguration`` is a property of the ``AWS::ElastiCache::ReplicationGroup`` resource that configures an Amazon ElastiCache (ElastiCache) Valkey or Redis OSS cluster node group.

            :param node_group_id: Either the ElastiCache supplied 4-digit id or a user supplied id for the node group these configuration values apply to.
            :param primary_availability_zone: The Availability Zone where the primary node of this node group (shard) is launched.
            :param replica_availability_zones: A list of Availability Zones to be used for the read replicas. The number of Availability Zones in this list must match the value of ``ReplicaCount`` or ``ReplicasPerNodeGroup`` if not specified.
            :param replica_count: The number of read replica nodes in this node group (shard).
            :param slots: A string of comma-separated values where the first set of values are the slot numbers (zero based), and the second set of values are the keyspaces for each slot. The following example specifies three slots (numbered 0, 1, and 2): ``0,1,2,0-4999,5000-9999,10000-16,383`` . If you don't specify a value, ElastiCache allocates keys equally among each slot. When you use an ``UseOnlineResharding`` update policy to update the number of node groups without interruption, ElastiCache evenly distributes the keyspaces between the specified number of slots. This cannot be updated later. Therefore, after updating the number of node groups in this way, you should remove the value specified for the ``Slots`` property of each ``NodeGroupConfiguration`` from the stack template, as it no longer reflects the actual values in each node group. For more information, see `UseOnlineResharding Policy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                node_group_configuration_property = elasticache_mixins.CfnReplicationGroupPropsMixin.NodeGroupConfigurationProperty(
                    node_group_id="nodeGroupId",
                    primary_availability_zone="primaryAvailabilityZone",
                    replica_availability_zones=["replicaAvailabilityZones"],
                    replica_count=123,
                    slots="slots"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa92db00fb47b88462770097f2d6d6b4f456bf0d7362dd13d37856dd2a3e31c0)
                check_type(argname="argument node_group_id", value=node_group_id, expected_type=type_hints["node_group_id"])
                check_type(argname="argument primary_availability_zone", value=primary_availability_zone, expected_type=type_hints["primary_availability_zone"])
                check_type(argname="argument replica_availability_zones", value=replica_availability_zones, expected_type=type_hints["replica_availability_zones"])
                check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
                check_type(argname="argument slots", value=slots, expected_type=type_hints["slots"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if node_group_id is not None:
                self._values["node_group_id"] = node_group_id
            if primary_availability_zone is not None:
                self._values["primary_availability_zone"] = primary_availability_zone
            if replica_availability_zones is not None:
                self._values["replica_availability_zones"] = replica_availability_zones
            if replica_count is not None:
                self._values["replica_count"] = replica_count
            if slots is not None:
                self._values["slots"] = slots

        @builtins.property
        def node_group_id(self) -> typing.Optional[builtins.str]:
            '''Either the ElastiCache supplied 4-digit id or a user supplied id for the node group these configuration values apply to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-nodegroupid
            '''
            result = self._values.get("node_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Availability Zone where the primary node of this node group (shard) is launched.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-primaryavailabilityzone
            '''
            result = self._values.get("primary_availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replica_availability_zones(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of Availability Zones to be used for the read replicas.

            The number of Availability Zones in this list must match the value of ``ReplicaCount`` or ``ReplicasPerNodeGroup`` if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-replicaavailabilityzones
            '''
            result = self._values.get("replica_availability_zones")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def replica_count(self) -> typing.Optional[jsii.Number]:
            '''The number of read replica nodes in this node group (shard).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-replicacount
            '''
            result = self._values.get("replica_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def slots(self) -> typing.Optional[builtins.str]:
            '''A string of comma-separated values where the first set of values are the slot numbers (zero based), and the second set of values are the keyspaces for each slot.

            The following example specifies three slots (numbered 0, 1, and 2): ``0,1,2,0-4999,5000-9999,10000-16,383`` .

            If you don't specify a value, ElastiCache allocates keys equally among each slot.

            When you use an ``UseOnlineResharding`` update policy to update the number of node groups without interruption, ElastiCache evenly distributes the keyspaces between the specified number of slots. This cannot be updated later. Therefore, after updating the number of node groups in this way, you should remove the value specified for the ``Slots`` property of each ``NodeGroupConfiguration`` from the stack template, as it no longer reflects the actual values in each node group. For more information, see `UseOnlineResharding Policy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-slots
            '''
            result = self._values.get("slots")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeGroupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnSecurityGroupIngressMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_security_group_name": "cacheSecurityGroupName",
        "ec2_security_group_name": "ec2SecurityGroupName",
        "ec2_security_group_owner_id": "ec2SecurityGroupOwnerId",
    },
)
class CfnSecurityGroupIngressMixinProps:
    def __init__(
        self,
        *,
        cache_security_group_name: typing.Optional[builtins.str] = None,
        ec2_security_group_name: typing.Optional[builtins.str] = None,
        ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSecurityGroupIngressPropsMixin.

        :param cache_security_group_name: The name of the Cache Security Group to authorize.
        :param ec2_security_group_name: Name of the EC2 Security Group to include in the authorization.
        :param ec2_security_group_owner_id: Specifies the Amazon Account ID of the owner of the EC2 security group specified in the EC2SecurityGroupName property. The Amazon access key ID is not an acceptable value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-securitygroupingress.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
            
            cfn_security_group_ingress_mixin_props = elasticache_mixins.CfnSecurityGroupIngressMixinProps(
                cache_security_group_name="cacheSecurityGroupName",
                ec2_security_group_name="ec2SecurityGroupName",
                ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e376ba9828359ad495944814184c872720c409839a23f1989ff2ffa18f926c86)
            check_type(argname="argument cache_security_group_name", value=cache_security_group_name, expected_type=type_hints["cache_security_group_name"])
            check_type(argname="argument ec2_security_group_name", value=ec2_security_group_name, expected_type=type_hints["ec2_security_group_name"])
            check_type(argname="argument ec2_security_group_owner_id", value=ec2_security_group_owner_id, expected_type=type_hints["ec2_security_group_owner_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_security_group_name is not None:
            self._values["cache_security_group_name"] = cache_security_group_name
        if ec2_security_group_name is not None:
            self._values["ec2_security_group_name"] = ec2_security_group_name
        if ec2_security_group_owner_id is not None:
            self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

    @builtins.property
    def cache_security_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Cache Security Group to authorize.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-securitygroupingress.html#cfn-elasticache-securitygroupingress-cachesecuritygroupname
        '''
        result = self._values.get("cache_security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_security_group_name(self) -> typing.Optional[builtins.str]:
        '''Name of the EC2 Security Group to include in the authorization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-securitygroupingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupname
        '''
        result = self._values.get("ec2_security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_security_group_owner_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Account ID of the owner of the EC2 security group specified in the EC2SecurityGroupName property.

        The Amazon access key ID is not an acceptable value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-securitygroupingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupownerid
        '''
        result = self._values.get("ec2_security_group_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityGroupIngressMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecurityGroupIngressPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnSecurityGroupIngressPropsMixin",
):
    '''The AWS::ElastiCache::SecurityGroupIngress type authorizes ingress to a cache security group from hosts in specified Amazon EC2 security groups.

    For more information about ElastiCache security group ingress, go to `AuthorizeCacheSecurityGroupIngress <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_AuthorizeCacheSecurityGroupIngress.html>`_ in the *Amazon ElastiCache API Reference Guide* .
    .. epigraph::

       Updates are not supported.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-securitygroupingress.html
    :cloudformationResource: AWS::ElastiCache::SecurityGroupIngress
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
        
        cfn_security_group_ingress_props_mixin = elasticache_mixins.CfnSecurityGroupIngressPropsMixin(elasticache_mixins.CfnSecurityGroupIngressMixinProps(
            cache_security_group_name="cacheSecurityGroupName",
            ec2_security_group_name="ec2SecurityGroupName",
            ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSecurityGroupIngressMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElastiCache::SecurityGroupIngress``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9470574937c92bbba0ea6bcb9917391d13b262adcc49b33f86acaf013f0beb2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e940a2c7204f8a1590768a774539d34be5077771f6538185519d09c4e3c9f90)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8089e0a8dbfe09c1497cee85f87e6c2310b79a3b9ced6deb08aa05e34aba61)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecurityGroupIngressMixinProps:
        return typing.cast(CfnSecurityGroupIngressMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnSecurityGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "tags": "tags"},
)
class CfnSecurityGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSecurityGroupPropsMixin.

        :param description: A description for the cache security group.
        :param tags: A tag that can be added to an ElastiCache security group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your security groups. A tag with a null Value is permitted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-securitygroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
            
            cfn_security_group_mixin_props = elasticache_mixins.CfnSecurityGroupMixinProps(
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba8bf5088b54e514aa0aaf5b0852f8ab3fd671f8c4cd87d12ad6e74ef7f085c)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the cache security group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-securitygroup.html#cfn-elasticache-securitygroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A tag that can be added to an ElastiCache security group.

        Tags are composed of a Key/Value pair. You can use tags to categorize and track all your security groups. A tag with a null Value is permitted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-securitygroup.html#cfn-elasticache-securitygroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecurityGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnSecurityGroupPropsMixin",
):
    '''The ``AWS::ElastiCache::SecurityGroup`` resource creates a cache security group.

    For more information about cache security groups, go to `CacheSecurityGroups <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/VPCs.html>`_ in the *Amazon ElastiCache User Guide* or go to `CreateCacheSecurityGroup <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_CreateCacheSecurityGroup.html>`_ in the *Amazon ElastiCache API Reference Guide* .

    For more information, see `CreateCacheSubnetGroup <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_CreateCacheSubnetGroup.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-securitygroup.html
    :cloudformationResource: AWS::ElastiCache::SecurityGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
        
        cfn_security_group_props_mixin = elasticache_mixins.CfnSecurityGroupPropsMixin(elasticache_mixins.CfnSecurityGroupMixinProps(
            description="description",
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
        props: typing.Union[CfnSecurityGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElastiCache::SecurityGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ec36a3f4ea82d1aa6b725dd520bcd6abbfc1bba644ff02d0adf635dfe1109f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96b72b8cb63e4cb2f6bb1b985344754e2fb51c9be5dc35b95c4010a98ca6e092)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817b51786357574f5fa0c920d585cf69616083f878fbaf9bf307ac5bd92c7693)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecurityGroupMixinProps:
        return typing.cast(CfnSecurityGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnServerlessCacheMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_usage_limits": "cacheUsageLimits",
        "daily_snapshot_time": "dailySnapshotTime",
        "description": "description",
        "endpoint": "endpoint",
        "engine": "engine",
        "final_snapshot_name": "finalSnapshotName",
        "kms_key_id": "kmsKeyId",
        "major_engine_version": "majorEngineVersion",
        "reader_endpoint": "readerEndpoint",
        "security_group_ids": "securityGroupIds",
        "serverless_cache_name": "serverlessCacheName",
        "snapshot_arns_to_restore": "snapshotArnsToRestore",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "user_group_id": "userGroupId",
    },
)
class CfnServerlessCacheMixinProps:
    def __init__(
        self,
        *,
        cache_usage_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerlessCachePropsMixin.CacheUsageLimitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        daily_snapshot_time: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerlessCachePropsMixin.EndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        engine: typing.Optional[builtins.str] = None,
        final_snapshot_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        major_engine_version: typing.Optional[builtins.str] = None,
        reader_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerlessCachePropsMixin.EndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        serverless_cache_name: typing.Optional[builtins.str] = None,
        snapshot_arns_to_restore: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnServerlessCachePropsMixin.

        :param cache_usage_limits: The cache usage limit for the serverless cache.
        :param daily_snapshot_time: The daily time that a cache snapshot will be created. Default is NULL, i.e. snapshots will not be created at a specific time on a daily basis. Available for Valkey, Redis OSS and Serverless Memcached only.
        :param description: A description of the serverless cache.
        :param endpoint: Represents the information required for client programs to connect to a cache node. This value is read-only.
        :param engine: The engine the serverless cache is compatible with.
        :param final_snapshot_name: The name of the final snapshot taken of a cache before the cache is deleted.
        :param kms_key_id: The ID of the AWS Key Management Service (KMS) key that is used to encrypt data at rest in the serverless cache.
        :param major_engine_version: The version number of the engine the serverless cache is compatible with.
        :param reader_endpoint: Represents the information required for client programs to connect to a cache node. This value is read-only.
        :param security_group_ids: The IDs of the EC2 security groups associated with the serverless cache.
        :param serverless_cache_name: The unique identifier of the serverless cache.
        :param snapshot_arns_to_restore: The ARN of the snapshot from which to restore data into the new cache.
        :param snapshot_retention_limit: The current setting for the number of serverless cache snapshots the system will retain. Available for Valkey, Redis OSS and Serverless Memcached only.
        :param subnet_ids: If no subnet IDs are given and your VPC is in us-west-1, then ElastiCache will select 2 default subnets across AZs in your VPC. For all other Regions, if no subnet IDs are given then ElastiCache will select 3 default subnets across AZs in your default VPC.
        :param tags: A list of tags to be added to this resource.
        :param user_group_id: The identifier of the user group associated with the serverless cache. Available for Valkey and Redis OSS only. Default is NULL.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
            
            cfn_serverless_cache_mixin_props = elasticache_mixins.CfnServerlessCacheMixinProps(
                cache_usage_limits=elasticache_mixins.CfnServerlessCachePropsMixin.CacheUsageLimitsProperty(
                    data_storage=elasticache_mixins.CfnServerlessCachePropsMixin.DataStorageProperty(
                        maximum=123,
                        minimum=123,
                        unit="unit"
                    ),
                    ecpu_per_second=elasticache_mixins.CfnServerlessCachePropsMixin.ECPUPerSecondProperty(
                        maximum=123,
                        minimum=123
                    )
                ),
                daily_snapshot_time="dailySnapshotTime",
                description="description",
                endpoint=elasticache_mixins.CfnServerlessCachePropsMixin.EndpointProperty(
                    address="address",
                    port="port"
                ),
                engine="engine",
                final_snapshot_name="finalSnapshotName",
                kms_key_id="kmsKeyId",
                major_engine_version="majorEngineVersion",
                reader_endpoint=elasticache_mixins.CfnServerlessCachePropsMixin.EndpointProperty(
                    address="address",
                    port="port"
                ),
                security_group_ids=["securityGroupIds"],
                serverless_cache_name="serverlessCacheName",
                snapshot_arns_to_restore=["snapshotArnsToRestore"],
                snapshot_retention_limit=123,
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_group_id="userGroupId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6514a6b557cce0884fdb538f2299d977083fd2eef44ff225ead9c8d1c827011f)
            check_type(argname="argument cache_usage_limits", value=cache_usage_limits, expected_type=type_hints["cache_usage_limits"])
            check_type(argname="argument daily_snapshot_time", value=daily_snapshot_time, expected_type=type_hints["daily_snapshot_time"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument final_snapshot_name", value=final_snapshot_name, expected_type=type_hints["final_snapshot_name"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument major_engine_version", value=major_engine_version, expected_type=type_hints["major_engine_version"])
            check_type(argname="argument reader_endpoint", value=reader_endpoint, expected_type=type_hints["reader_endpoint"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument serverless_cache_name", value=serverless_cache_name, expected_type=type_hints["serverless_cache_name"])
            check_type(argname="argument snapshot_arns_to_restore", value=snapshot_arns_to_restore, expected_type=type_hints["snapshot_arns_to_restore"])
            check_type(argname="argument snapshot_retention_limit", value=snapshot_retention_limit, expected_type=type_hints["snapshot_retention_limit"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_group_id", value=user_group_id, expected_type=type_hints["user_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_usage_limits is not None:
            self._values["cache_usage_limits"] = cache_usage_limits
        if daily_snapshot_time is not None:
            self._values["daily_snapshot_time"] = daily_snapshot_time
        if description is not None:
            self._values["description"] = description
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if engine is not None:
            self._values["engine"] = engine
        if final_snapshot_name is not None:
            self._values["final_snapshot_name"] = final_snapshot_name
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if major_engine_version is not None:
            self._values["major_engine_version"] = major_engine_version
        if reader_endpoint is not None:
            self._values["reader_endpoint"] = reader_endpoint
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if serverless_cache_name is not None:
            self._values["serverless_cache_name"] = serverless_cache_name
        if snapshot_arns_to_restore is not None:
            self._values["snapshot_arns_to_restore"] = snapshot_arns_to_restore
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if user_group_id is not None:
            self._values["user_group_id"] = user_group_id

    @builtins.property
    def cache_usage_limits(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessCachePropsMixin.CacheUsageLimitsProperty"]]:
        '''The cache usage limit for the serverless cache.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-cacheusagelimits
        '''
        result = self._values.get("cache_usage_limits")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessCachePropsMixin.CacheUsageLimitsProperty"]], result)

    @builtins.property
    def daily_snapshot_time(self) -> typing.Optional[builtins.str]:
        '''The daily time that a cache snapshot will be created.

        Default is NULL, i.e. snapshots will not be created at a specific time on a daily basis. Available for Valkey, Redis OSS and Serverless Memcached only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-dailysnapshottime
        '''
        result = self._values.get("daily_snapshot_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the serverless cache.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessCachePropsMixin.EndpointProperty"]]:
        '''Represents the information required for client programs to connect to a cache node.

        This value is read-only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-endpoint
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessCachePropsMixin.EndpointProperty"]], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The engine the serverless cache is compatible with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def final_snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of the final snapshot taken of a cache before the cache is deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-finalsnapshotname
        '''
        result = self._values.get("final_snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS Key Management Service (KMS) key that is used to encrypt data at rest in the serverless cache.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def major_engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the engine the serverless cache is compatible with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-majorengineversion
        '''
        result = self._values.get("major_engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reader_endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessCachePropsMixin.EndpointProperty"]]:
        '''Represents the information required for client programs to connect to a cache node.

        This value is read-only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-readerendpoint
        '''
        result = self._values.get("reader_endpoint")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessCachePropsMixin.EndpointProperty"]], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the EC2 security groups associated with the serverless cache.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def serverless_cache_name(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the serverless cache.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-serverlesscachename
        '''
        result = self._values.get("serverless_cache_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_arns_to_restore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARN of the snapshot from which to restore data into the new cache.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-snapshotarnstorestore
        '''
        result = self._values.get("snapshot_arns_to_restore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        '''The current setting for the number of serverless cache snapshots the system will retain.

        Available for Valkey, Redis OSS and Serverless Memcached only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-snapshotretentionlimit
        '''
        result = self._values.get("snapshot_retention_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If no subnet IDs are given and your VPC is in us-west-1, then ElastiCache will select 2 default subnets across AZs in your VPC.

        For all other Regions, if no subnet IDs are given then ElastiCache will select 3 default subnets across AZs in your default VPC.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to be added to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_group_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the user group associated with the serverless cache.

        Available for Valkey and Redis OSS only. Default is NULL.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html#cfn-elasticache-serverlesscache-usergroupid
        '''
        result = self._values.get("user_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServerlessCacheMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServerlessCachePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnServerlessCachePropsMixin",
):
    '''The resource representing a serverless cache.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-serverlesscache.html
    :cloudformationResource: AWS::ElastiCache::ServerlessCache
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
        
        cfn_serverless_cache_props_mixin = elasticache_mixins.CfnServerlessCachePropsMixin(elasticache_mixins.CfnServerlessCacheMixinProps(
            cache_usage_limits=elasticache_mixins.CfnServerlessCachePropsMixin.CacheUsageLimitsProperty(
                data_storage=elasticache_mixins.CfnServerlessCachePropsMixin.DataStorageProperty(
                    maximum=123,
                    minimum=123,
                    unit="unit"
                ),
                ecpu_per_second=elasticache_mixins.CfnServerlessCachePropsMixin.ECPUPerSecondProperty(
                    maximum=123,
                    minimum=123
                )
            ),
            daily_snapshot_time="dailySnapshotTime",
            description="description",
            endpoint=elasticache_mixins.CfnServerlessCachePropsMixin.EndpointProperty(
                address="address",
                port="port"
            ),
            engine="engine",
            final_snapshot_name="finalSnapshotName",
            kms_key_id="kmsKeyId",
            major_engine_version="majorEngineVersion",
            reader_endpoint=elasticache_mixins.CfnServerlessCachePropsMixin.EndpointProperty(
                address="address",
                port="port"
            ),
            security_group_ids=["securityGroupIds"],
            serverless_cache_name="serverlessCacheName",
            snapshot_arns_to_restore=["snapshotArnsToRestore"],
            snapshot_retention_limit=123,
            subnet_ids=["subnetIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_group_id="userGroupId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnServerlessCacheMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElastiCache::ServerlessCache``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc3554efabb192042ae81dfaec2a169edae956988392b9c0fd08e295040327b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b5910910c4f422a036c512e7292f46e74a8729a7a0babc61faa41a99fdcb462)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf4a170d41ab75d015c2cc566a3dfcc31bad2caddd9a89482257974b928ea2d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServerlessCacheMixinProps:
        return typing.cast(CfnServerlessCacheMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnServerlessCachePropsMixin.CacheUsageLimitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_storage": "dataStorage",
            "ecpu_per_second": "ecpuPerSecond",
        },
    )
    class CacheUsageLimitsProperty:
        def __init__(
            self,
            *,
            data_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerlessCachePropsMixin.DataStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ecpu_per_second: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerlessCachePropsMixin.ECPUPerSecondProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The usage limits for storage and ElastiCache Processing Units for the cache.

            :param data_storage: The maximum data storage limit in the cache, expressed in Gigabytes.
            :param ecpu_per_second: The number of ElastiCache Processing Units (ECPU) the cache can consume per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-cacheusagelimits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                cache_usage_limits_property = elasticache_mixins.CfnServerlessCachePropsMixin.CacheUsageLimitsProperty(
                    data_storage=elasticache_mixins.CfnServerlessCachePropsMixin.DataStorageProperty(
                        maximum=123,
                        minimum=123,
                        unit="unit"
                    ),
                    ecpu_per_second=elasticache_mixins.CfnServerlessCachePropsMixin.ECPUPerSecondProperty(
                        maximum=123,
                        minimum=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9279e9a7b635997390c39f79b10329ce743a93f3f6252fc5b173204e62bf5bf2)
                check_type(argname="argument data_storage", value=data_storage, expected_type=type_hints["data_storage"])
                check_type(argname="argument ecpu_per_second", value=ecpu_per_second, expected_type=type_hints["ecpu_per_second"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_storage is not None:
                self._values["data_storage"] = data_storage
            if ecpu_per_second is not None:
                self._values["ecpu_per_second"] = ecpu_per_second

        @builtins.property
        def data_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessCachePropsMixin.DataStorageProperty"]]:
            '''The maximum data storage limit in the cache, expressed in Gigabytes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-cacheusagelimits.html#cfn-elasticache-serverlesscache-cacheusagelimits-datastorage
            '''
            result = self._values.get("data_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessCachePropsMixin.DataStorageProperty"]], result)

        @builtins.property
        def ecpu_per_second(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessCachePropsMixin.ECPUPerSecondProperty"]]:
            '''The number of ElastiCache Processing Units (ECPU) the cache can consume per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-cacheusagelimits.html#cfn-elasticache-serverlesscache-cacheusagelimits-ecpupersecond
            '''
            result = self._values.get("ecpu_per_second")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessCachePropsMixin.ECPUPerSecondProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CacheUsageLimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnServerlessCachePropsMixin.DataStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"maximum": "maximum", "minimum": "minimum", "unit": "unit"},
    )
    class DataStorageProperty:
        def __init__(
            self,
            *,
            maximum: typing.Optional[jsii.Number] = None,
            minimum: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The data storage limit.

            :param maximum: The upper limit for data storage the cache is set to use.
            :param minimum: The lower limit for data storage the cache is set to use.
            :param unit: The unit that the storage is measured in, in GB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-datastorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                data_storage_property = elasticache_mixins.CfnServerlessCachePropsMixin.DataStorageProperty(
                    maximum=123,
                    minimum=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c5d238a22f2ce4e011739440e20dedecc05f340fa4f378624119fe47d30639a)
                check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
                check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum is not None:
                self._values["maximum"] = maximum
            if minimum is not None:
                self._values["minimum"] = minimum
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def maximum(self) -> typing.Optional[jsii.Number]:
            '''The upper limit for data storage the cache is set to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-datastorage.html#cfn-elasticache-serverlesscache-datastorage-maximum
            '''
            result = self._values.get("maximum")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum(self) -> typing.Optional[jsii.Number]:
            '''The lower limit for data storage the cache is set to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-datastorage.html#cfn-elasticache-serverlesscache-datastorage-minimum
            '''
            result = self._values.get("minimum")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit that the storage is measured in, in GB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-datastorage.html#cfn-elasticache-serverlesscache-datastorage-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnServerlessCachePropsMixin.ECPUPerSecondProperty",
        jsii_struct_bases=[],
        name_mapping={"maximum": "maximum", "minimum": "minimum"},
    )
    class ECPUPerSecondProperty:
        def __init__(
            self,
            *,
            maximum: typing.Optional[jsii.Number] = None,
            minimum: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration for the number of ElastiCache Processing Units (ECPU) the cache can consume per second.

            :param maximum: The configuration for the maximum number of ECPUs the cache can consume per second.
            :param minimum: The configuration for the minimum number of ECPUs the cache should be able consume per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-ecpupersecond.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                e_cPUPer_second_property = elasticache_mixins.CfnServerlessCachePropsMixin.ECPUPerSecondProperty(
                    maximum=123,
                    minimum=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aee134ae62784c6eada26ade01556ad85deaa4e5c9469fcfb3965c51861fbda5)
                check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
                check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum is not None:
                self._values["maximum"] = maximum
            if minimum is not None:
                self._values["minimum"] = minimum

        @builtins.property
        def maximum(self) -> typing.Optional[jsii.Number]:
            '''The configuration for the maximum number of ECPUs the cache can consume per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-ecpupersecond.html#cfn-elasticache-serverlesscache-ecpupersecond-maximum
            '''
            result = self._values.get("maximum")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum(self) -> typing.Optional[jsii.Number]:
            '''The configuration for the minimum number of ECPUs the cache should be able consume per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-ecpupersecond.html#cfn-elasticache-serverlesscache-ecpupersecond-minimum
            '''
            result = self._values.get("minimum")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ECPUPerSecondProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnServerlessCachePropsMixin.EndpointProperty",
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
            '''Represents the information required for client programs to connect to a cache node.

            This value is read-only.

            :param address: The DNS hostname of the cache node.
            :param port: The port number that the cache engine is listening on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-endpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                endpoint_property = elasticache_mixins.CfnServerlessCachePropsMixin.EndpointProperty(
                    address="address",
                    port="port"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b472df9b9546d301345854c492675c5549fc5dbbd4d737c0a8c2040823f5d4b7)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The DNS hostname of the cache node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-endpoint.html#cfn-elasticache-serverlesscache-endpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The port number that the cache engine is listening on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-serverlesscache-endpoint.html#cfn-elasticache-serverlesscache-endpoint-port
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
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnSubnetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_subnet_group_name": "cacheSubnetGroupName",
        "description": "description",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnSubnetGroupMixinProps:
    def __init__(
        self,
        *,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSubnetGroupPropsMixin.

        :param cache_subnet_group_name: The name for the cache subnet group. This value is stored as a lowercase string. Constraints: Must contain no more than 255 alphanumeric characters or hyphens. Example: ``mysubnetgroup``
        :param description: The description for the cache subnet group.
        :param subnet_ids: The EC2 subnet IDs for the cache subnet group.
        :param tags: A tag that can be added to an ElastiCache subnet group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your subnet groups. A tag with a null Value is permitted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
            
            cfn_subnet_group_mixin_props = elasticache_mixins.CfnSubnetGroupMixinProps(
                cache_subnet_group_name="cacheSubnetGroupName",
                description="description",
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620affba5eadf5ce705d29724fbede5727e6c77b324007eeb01419845eb7ef79)
            check_type(argname="argument cache_subnet_group_name", value=cache_subnet_group_name, expected_type=type_hints["cache_subnet_group_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name
        if description is not None:
            self._values["description"] = description
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name for the cache subnet group. This value is stored as a lowercase string.

        Constraints: Must contain no more than 255 alphanumeric characters or hyphens.

        Example: ``mysubnetgroup``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-cachesubnetgroupname
        '''
        result = self._values.get("cache_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the cache subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The EC2 subnet IDs for the cache subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A tag that can be added to an ElastiCache subnet group.

        Tags are composed of a Key/Value pair. You can use tags to categorize and track all your subnet groups. A tag with a null Value is permitted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubnetGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSubnetGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnSubnetGroupPropsMixin",
):
    '''Creates a cache subnet group.

    For more information about cache subnet groups, go to Cache Subnet Groups in the *Amazon ElastiCache User Guide* or go to `CreateCacheSubnetGroup <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_CreateCacheSubnetGroup.html>`_ in the *Amazon ElastiCache API Reference Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html
    :cloudformationResource: AWS::ElastiCache::SubnetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
        
        cfn_subnet_group_props_mixin = elasticache_mixins.CfnSubnetGroupPropsMixin(elasticache_mixins.CfnSubnetGroupMixinProps(
            cache_subnet_group_name="cacheSubnetGroupName",
            description="description",
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
        props: typing.Union[CfnSubnetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElastiCache::SubnetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fc2ab977a5cfa976b69e648788dc5ae437a04c207e9c175bee3601396d9cb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__620b0dbcd21aa175b7655600fc9c814de843931b9019dc52ec898fd86e754d47)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85eb409b92a3277e7620ec09de38f162e85c5114a15cd8fb9cb6c17721168e64)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSubnetGroupMixinProps:
        return typing.cast(CfnSubnetGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnUserGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "engine": "engine",
        "tags": "tags",
        "user_group_id": "userGroupId",
        "user_ids": "userIds",
    },
)
class CfnUserGroupMixinProps:
    def __init__(
        self,
        *,
        engine: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_group_id: typing.Optional[builtins.str] = None,
        user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnUserGroupPropsMixin.

        :param engine: The current supported values are valkey and redis.
        :param tags: The list of tags.
        :param user_group_id: The ID of the user group.
        :param user_ids: The list of user IDs that belong to the user group. A user named ``default`` must be included.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
            
            cfn_user_group_mixin_props = elasticache_mixins.CfnUserGroupMixinProps(
                engine="engine",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_group_id="userGroupId",
                user_ids=["userIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b7199bfb8a6152e133dde020ea9a4a3bb370c3077e7e83c106ac22607e7919)
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_group_id", value=user_group_id, expected_type=type_hints["user_group_id"])
            check_type(argname="argument user_ids", value=user_ids, expected_type=type_hints["user_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if engine is not None:
            self._values["engine"] = engine
        if tags is not None:
            self._values["tags"] = tags
        if user_group_id is not None:
            self._values["user_group_id"] = user_group_id
        if user_ids is not None:
            self._values["user_ids"] = user_ids

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The current supported values are valkey and redis.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html#cfn-elasticache-usergroup-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html#cfn-elasticache-usergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_group_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html#cfn-elasticache-usergroup-usergroupid
        '''
        result = self._values.get("user_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of user IDs that belong to the user group.

        A user named ``default`` must be included.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html#cfn-elasticache-usergroup-userids
        '''
        result = self._values.get("user_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnUserGroupPropsMixin",
):
    '''For Valkey 7.2 and onwards, or Redis OSS 6.0 and onwards: Creates a user group. For more information, see `Using Role Based Access Control (RBAC) <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Clusters.RBAC.html>`_.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html
    :cloudformationResource: AWS::ElastiCache::UserGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
        
        cfn_user_group_props_mixin = elasticache_mixins.CfnUserGroupPropsMixin(elasticache_mixins.CfnUserGroupMixinProps(
            engine="engine",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_group_id="userGroupId",
            user_ids=["userIds"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElastiCache::UserGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126d8314620159e6c3800d80993d6119a5cefc7f6d3b8944a1960d7654786e37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4134dea3ad0afba5211075ec196d4e9744296d83b87e3c640e846f9011e4b577)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f069c250d4b0cd956ab90217c20f1470de4ad074327598d46d3f612b833c56)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserGroupMixinProps:
        return typing.cast(CfnUserGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnUserMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_string": "accessString",
        "authentication_mode": "authenticationMode",
        "engine": "engine",
        "no_password_required": "noPasswordRequired",
        "passwords": "passwords",
        "tags": "tags",
        "user_id": "userId",
        "user_name": "userName",
    },
)
class CfnUserMixinProps:
    def __init__(
        self,
        *,
        access_string: typing.Optional[builtins.str] = None,
        authentication_mode: typing.Any = None,
        engine: typing.Optional[builtins.str] = None,
        no_password_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPropsMixin.

        :param access_string: Access permissions string used for this user.
        :param authentication_mode: Specifies the authentication mode to use. Below is an example of the possible JSON values:. Example:: { Passwords: ["*****", "******"] // If Type is password. }
        :param engine: The current supported values are valkey and redis.
        :param no_password_required: Indicates a password is not required for this user.
        :param passwords: Passwords used for this user. You can create up to two passwords for each user.
        :param tags: The list of tags.
        :param user_id: The ID of the user.
        :param user_name: The username of the user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
            
            # authentication_mode: Any
            
            cfn_user_mixin_props = elasticache_mixins.CfnUserMixinProps(
                access_string="accessString",
                authentication_mode=authentication_mode,
                engine="engine",
                no_password_required=False,
                passwords=["passwords"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_id="userId",
                user_name="userName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a29e289f6aa6e06243c448a10abb5de5f011ab111da82df888cc80be1c8552)
            check_type(argname="argument access_string", value=access_string, expected_type=type_hints["access_string"])
            check_type(argname="argument authentication_mode", value=authentication_mode, expected_type=type_hints["authentication_mode"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument no_password_required", value=no_password_required, expected_type=type_hints["no_password_required"])
            check_type(argname="argument passwords", value=passwords, expected_type=type_hints["passwords"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_string is not None:
            self._values["access_string"] = access_string
        if authentication_mode is not None:
            self._values["authentication_mode"] = authentication_mode
        if engine is not None:
            self._values["engine"] = engine
        if no_password_required is not None:
            self._values["no_password_required"] = no_password_required
        if passwords is not None:
            self._values["passwords"] = passwords
        if tags is not None:
            self._values["tags"] = tags
        if user_id is not None:
            self._values["user_id"] = user_id
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def access_string(self) -> typing.Optional[builtins.str]:
        '''Access permissions string used for this user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-accessstring
        '''
        result = self._values.get("access_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_mode(self) -> typing.Any:
        '''Specifies the authentication mode to use. Below is an example of the possible JSON values:.

        Example::

           { Passwords: ["*****", "******"] // If Type is password.
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-authenticationmode
        '''
        result = self._values.get("authentication_mode")
        return typing.cast(typing.Any, result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The current supported values are valkey and redis.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_password_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates a password is not required for this user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-nopasswordrequired
        '''
        result = self._values.get("no_password_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def passwords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Passwords used for this user.

        You can create up to two passwords for each user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-passwords
        '''
        result = self._values.get("passwords")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-userid
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The username of the user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-username
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnUserPropsMixin",
):
    '''For Valkey 7.2 and onwards, or Redis OSS engine version 6.0 and onwards: Creates user. For more information, see `Using Role Based Access Control (RBAC) <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Clusters.RBAC.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html
    :cloudformationResource: AWS::ElastiCache::User
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
        
        # authentication_mode: Any
        
        cfn_user_props_mixin = elasticache_mixins.CfnUserPropsMixin(elasticache_mixins.CfnUserMixinProps(
            access_string="accessString",
            authentication_mode=authentication_mode,
            engine="engine",
            no_password_required=False,
            passwords=["passwords"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_id="userId",
            user_name="userName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElastiCache::User``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c46dcaa7a8bafbf6f32abeda8e103edacff46c94cae972237ce0fe904fe655)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5d86f2b745a994b6859d9cc230a3ffa5f841f260514478dfab840252a1c1fa5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65b046805b1f46ec5546e036d0701de8a3dc81e2dc7fbce6c9b65e7f9d73411)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserMixinProps:
        return typing.cast(CfnUserMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticache.mixins.CfnUserPropsMixin.AuthenticationModeProperty",
        jsii_struct_bases=[],
        name_mapping={"passwords": "passwords", "type": "type"},
    )
    class AuthenticationModeProperty:
        def __init__(
            self,
            *,
            passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the authentication mode to use.

            :param passwords: Specifies the passwords to use for authentication if ``Type`` is set to ``password`` .
            :param type: Specifies the authentication type. Possible options are IAM authentication, password and no password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-user-authenticationmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticache import mixins as elasticache_mixins
                
                authentication_mode_property = elasticache_mixins.CfnUserPropsMixin.AuthenticationModeProperty(
                    passwords=["passwords"],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44cf585b74b86fe17855f4db8ad6e30e5b645efa885ba3c891b99c9537796b13)
                check_type(argname="argument passwords", value=passwords, expected_type=type_hints["passwords"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if passwords is not None:
                self._values["passwords"] = passwords
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def passwords(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the passwords to use for authentication if ``Type`` is set to ``password`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-user-authenticationmode.html#cfn-elasticache-user-authenticationmode-passwords
            '''
            result = self._values.get("passwords")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the authentication type.

            Possible options are IAM authentication, password and no password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-user-authenticationmode.html#cfn-elasticache-user-authenticationmode-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticationModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCacheClusterMixinProps",
    "CfnCacheClusterPropsMixin",
    "CfnGlobalReplicationGroupMixinProps",
    "CfnGlobalReplicationGroupPropsMixin",
    "CfnParameterGroupMixinProps",
    "CfnParameterGroupPropsMixin",
    "CfnReplicationGroupMixinProps",
    "CfnReplicationGroupPropsMixin",
    "CfnSecurityGroupIngressMixinProps",
    "CfnSecurityGroupIngressPropsMixin",
    "CfnSecurityGroupMixinProps",
    "CfnSecurityGroupPropsMixin",
    "CfnServerlessCacheMixinProps",
    "CfnServerlessCachePropsMixin",
    "CfnSubnetGroupMixinProps",
    "CfnSubnetGroupPropsMixin",
    "CfnUserGroupMixinProps",
    "CfnUserGroupPropsMixin",
    "CfnUserMixinProps",
    "CfnUserPropsMixin",
]

publication.publish()

def _typecheckingstub__f4cc3afc7f2337ac60e5736c33e906f912bfe9608538a88971aa4c1a3f3ba2e7(
    *,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    az_mode: typing.Optional[builtins.str] = None,
    cache_node_type: typing.Optional[builtins.str] = None,
    cache_parameter_group_name: typing.Optional[builtins.str] = None,
    cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_subnet_group_name: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    ip_discovery: typing.Optional[builtins.str] = None,
    log_delivery_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCacheClusterPropsMixin.LogDeliveryConfigurationRequestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_type: typing.Optional[builtins.str] = None,
    notification_topic_arn: typing.Optional[builtins.str] = None,
    num_cache_nodes: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_availability_zone: typing.Optional[builtins.str] = None,
    preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    snapshot_retention_limit: typing.Optional[jsii.Number] = None,
    snapshot_window: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db5e4e2268cdb54c9b99d49086cf181011d65a3d79e2bdc9cd28fe18ba17f59(
    props: typing.Union[CfnCacheClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21d5d5b43ea28194baf332adf00c324e923f03332c4e276c7b62ce05075486e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c7675179697ab3fb7ae886e4a6564da24f20edd33553a3d23b2720c86348d9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8c39ecfbea9e5b37a3c2248a2651d755278945b0417073667bb48d53f900ca(
    *,
    log_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909a85364b79692107ddfdfdd9900d608710ea30c8edeb18babfce613ae4271e(
    *,
    cloud_watch_logs_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCacheClusterPropsMixin.CloudWatchLogsDestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_firehose_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCacheClusterPropsMixin.KinesisFirehoseDestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14032e8607ac22281c1b8f1843321d07e5342050225aed189920471fa2c6577b(
    *,
    delivery_stream: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc3f2f42abefca95555a5e08511b1ffb48793074f0735b972cd01884c6a73ec(
    *,
    destination_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCacheClusterPropsMixin.DestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    destination_type: typing.Optional[builtins.str] = None,
    log_format: typing.Optional[builtins.str] = None,
    log_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913b9c8c0e05e2cdf129e0cce2fe08c73815b553b31cf24b1bf70aa023bf8841(
    *,
    automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cache_node_type: typing.Optional[builtins.str] = None,
    cache_parameter_group_name: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    global_node_group_count: typing.Optional[jsii.Number] = None,
    global_replication_group_description: typing.Optional[builtins.str] = None,
    global_replication_group_id_suffix: typing.Optional[builtins.str] = None,
    members: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalReplicationGroupPropsMixin.GlobalReplicationGroupMemberProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    regional_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalReplicationGroupPropsMixin.RegionalConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0127367a1a081054e093790f995646ca6f9c8a3fc94688fd2032f7920d29dfa0(
    props: typing.Union[CfnGlobalReplicationGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f3877606335a33c1c57f85202d3ccc715bcff8eea61a94b90ffdf2899e4998(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f04e80a6c7b2afa29e24529af77e8db5e7953c1cd0540c409c7dbfd104c3707(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6f08296bed475d4dcc499bc927d8f711379b7ebb269ed9aefe501afe34f0b9(
    *,
    replication_group_id: typing.Optional[builtins.str] = None,
    replication_group_region: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59da2eab26f3d12bdd3c54ffc40e22ffd3c4adb00a19f88725f60f46d154f205(
    *,
    replication_group_id: typing.Optional[builtins.str] = None,
    replication_group_region: typing.Optional[builtins.str] = None,
    resharding_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGlobalReplicationGroupPropsMixin.ReshardingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d771a202a7d2d1d22d344bc42d1ba3cc0e99853b85cf27012964f9171c9d43(
    *,
    node_group_id: typing.Optional[builtins.str] = None,
    preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81a1c75c18104579aeefeec3b403c4015dc700e3317500a2893473a043a765b(
    *,
    cache_parameter_group_family: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01805cb0339b231a71ed5e39f4d89b5a9547fe2c42e86a90fc9a5eb01f871314(
    props: typing.Union[CfnParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd616234e5aa551d6eec806f67b7d4b8feec75cae4829bce0c87ac5509f4569(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1509da515b4dffb5d7b7d8f026f713b90fd49dd8ddda6e2d1f9db7819a8f123c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc505e761c91eb763676cd4a8b05f508401e1a9e43340573618327bce15eed0c(
    *,
    at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    auth_token: typing.Optional[builtins.str] = None,
    automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cache_node_type: typing.Optional[builtins.str] = None,
    cache_parameter_group_name: typing.Optional[builtins.str] = None,
    cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_subnet_group_name: typing.Optional[builtins.str] = None,
    cluster_mode: typing.Optional[builtins.str] = None,
    data_tiering_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    global_replication_group_id: typing.Optional[builtins.str] = None,
    ip_discovery: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_delivery_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationGroupPropsMixin.LogDeliveryConfigurationRequestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    multi_az_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    network_type: typing.Optional[builtins.str] = None,
    node_group_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationGroupPropsMixin.NodeGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    notification_topic_arn: typing.Optional[builtins.str] = None,
    num_cache_clusters: typing.Optional[jsii.Number] = None,
    num_node_groups: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_cache_cluster_a_zs: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    primary_cluster_id: typing.Optional[builtins.str] = None,
    replicas_per_node_group: typing.Optional[jsii.Number] = None,
    replication_group_description: typing.Optional[builtins.str] = None,
    replication_group_id: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    snapshot_retention_limit: typing.Optional[jsii.Number] = None,
    snapshotting_cluster_id: typing.Optional[builtins.str] = None,
    snapshot_window: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    user_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8925354708f65fad81dd8f98f1f8fe5de8e4be58e9de69f5da13e4b63159c9(
    props: typing.Union[CfnReplicationGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4fb2d1498800422aa582c3e01fd5b979e61d0448ebefcf5f963c38467df228(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db23d6536b3dadcdb41bcfd73d6396f28cb58b14e18cb224b39c14d1673e670(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5a56d14566838ed79e52b96da38c27a65d1f7cb06473170f9d9365c956834d(
    *,
    log_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023e911c2616a60223bdd5249ba9753fd689ad9338fb3c4f537baac96f66ee54(
    *,
    cloud_watch_logs_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationGroupPropsMixin.CloudWatchLogsDestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_firehose_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationGroupPropsMixin.KinesisFirehoseDestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1361be1cfdfdb6c414283324cbb736cf784c2ebcf06c9c5c2723e1829cb5424(
    *,
    delivery_stream: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f74b929b2af970a859e818c4d31a4962cc0f598bdc54da736a946edf6a0302a(
    *,
    destination_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicationGroupPropsMixin.DestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    destination_type: typing.Optional[builtins.str] = None,
    log_format: typing.Optional[builtins.str] = None,
    log_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa92db00fb47b88462770097f2d6d6b4f456bf0d7362dd13d37856dd2a3e31c0(
    *,
    node_group_id: typing.Optional[builtins.str] = None,
    primary_availability_zone: typing.Optional[builtins.str] = None,
    replica_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    slots: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e376ba9828359ad495944814184c872720c409839a23f1989ff2ffa18f926c86(
    *,
    cache_security_group_name: typing.Optional[builtins.str] = None,
    ec2_security_group_name: typing.Optional[builtins.str] = None,
    ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9470574937c92bbba0ea6bcb9917391d13b262adcc49b33f86acaf013f0beb2d(
    props: typing.Union[CfnSecurityGroupIngressMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e940a2c7204f8a1590768a774539d34be5077771f6538185519d09c4e3c9f90(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8089e0a8dbfe09c1497cee85f87e6c2310b79a3b9ced6deb08aa05e34aba61(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba8bf5088b54e514aa0aaf5b0852f8ab3fd671f8c4cd87d12ad6e74ef7f085c(
    *,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ec36a3f4ea82d1aa6b725dd520bcd6abbfc1bba644ff02d0adf635dfe1109f(
    props: typing.Union[CfnSecurityGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b72b8cb63e4cb2f6bb1b985344754e2fb51c9be5dc35b95c4010a98ca6e092(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817b51786357574f5fa0c920d585cf69616083f878fbaf9bf307ac5bd92c7693(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6514a6b557cce0884fdb538f2299d977083fd2eef44ff225ead9c8d1c827011f(
    *,
    cache_usage_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerlessCachePropsMixin.CacheUsageLimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    daily_snapshot_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerlessCachePropsMixin.EndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    engine: typing.Optional[builtins.str] = None,
    final_snapshot_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    major_engine_version: typing.Optional[builtins.str] = None,
    reader_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerlessCachePropsMixin.EndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    serverless_cache_name: typing.Optional[builtins.str] = None,
    snapshot_arns_to_restore: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_retention_limit: typing.Optional[jsii.Number] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc3554efabb192042ae81dfaec2a169edae956988392b9c0fd08e295040327b(
    props: typing.Union[CfnServerlessCacheMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5910910c4f422a036c512e7292f46e74a8729a7a0babc61faa41a99fdcb462(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf4a170d41ab75d015c2cc566a3dfcc31bad2caddd9a89482257974b928ea2d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9279e9a7b635997390c39f79b10329ce743a93f3f6252fc5b173204e62bf5bf2(
    *,
    data_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerlessCachePropsMixin.DataStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ecpu_per_second: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerlessCachePropsMixin.ECPUPerSecondProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5d238a22f2ce4e011739440e20dedecc05f340fa4f378624119fe47d30639a(
    *,
    maximum: typing.Optional[jsii.Number] = None,
    minimum: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee134ae62784c6eada26ade01556ad85deaa4e5c9469fcfb3965c51861fbda5(
    *,
    maximum: typing.Optional[jsii.Number] = None,
    minimum: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b472df9b9546d301345854c492675c5549fc5dbbd4d737c0a8c2040823f5d4b7(
    *,
    address: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620affba5eadf5ce705d29724fbede5727e6c77b324007eeb01419845eb7ef79(
    *,
    cache_subnet_group_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fc2ab977a5cfa976b69e648788dc5ae437a04c207e9c175bee3601396d9cb6(
    props: typing.Union[CfnSubnetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620b0dbcd21aa175b7655600fc9c814de843931b9019dc52ec898fd86e754d47(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85eb409b92a3277e7620ec09de38f162e85c5114a15cd8fb9cb6c17721168e64(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b7199bfb8a6152e133dde020ea9a4a3bb370c3077e7e83c106ac22607e7919(
    *,
    engine: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_group_id: typing.Optional[builtins.str] = None,
    user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126d8314620159e6c3800d80993d6119a5cefc7f6d3b8944a1960d7654786e37(
    props: typing.Union[CfnUserGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4134dea3ad0afba5211075ec196d4e9744296d83b87e3c640e846f9011e4b577(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f069c250d4b0cd956ab90217c20f1470de4ad074327598d46d3f612b833c56(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a29e289f6aa6e06243c448a10abb5de5f011ab111da82df888cc80be1c8552(
    *,
    access_string: typing.Optional[builtins.str] = None,
    authentication_mode: typing.Any = None,
    engine: typing.Optional[builtins.str] = None,
    no_password_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_id: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c46dcaa7a8bafbf6f32abeda8e103edacff46c94cae972237ce0fe904fe655(
    props: typing.Union[CfnUserMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d86f2b745a994b6859d9cc230a3ffa5f841f260514478dfab840252a1c1fa5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65b046805b1f46ec5546e036d0701de8a3dc81e2dc7fbce6c9b65e7f9d73411(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cf585b74b86fe17855f4db8ad6e30e5b645efa885ba3c891b99c9537796b13(
    *,
    passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
