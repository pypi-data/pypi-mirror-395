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
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnACLMixinProps",
    jsii_struct_bases=[],
    name_mapping={"acl_name": "aclName", "tags": "tags", "user_names": "userNames"},
)
class CfnACLMixinProps:
    def __init__(
        self,
        *,
        acl_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnACLPropsMixin.

        :param acl_name: The name of the Access Control List.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param user_names: The list of users that belong to the Access Control List.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
            
            cfn_aCLMixin_props = memorydb_mixins.CfnACLMixinProps(
                acl_name="aclName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_names=["userNames"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901275ce2d2b214070fbfa72a3ccb9fc912046aa1831d865264db4a71dfbb583)
            check_type(argname="argument acl_name", value=acl_name, expected_type=type_hints["acl_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_names", value=user_names, expected_type=type_hints["user_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acl_name is not None:
            self._values["acl_name"] = acl_name
        if tags is not None:
            self._values["tags"] = tags
        if user_names is not None:
            self._values["user_names"] = user_names

    @builtins.property
    def acl_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Access Control List.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html#cfn-memorydb-acl-aclname
        '''
        result = self._values.get("acl_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html#cfn-memorydb-acl-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of users that belong to the Access Control List.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html#cfn-memorydb-acl-usernames
        '''
        result = self._values.get("user_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnACLMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnACLPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnACLPropsMixin",
):
    '''Specifies an Access Control List.

    For more information, see `Authenticating users with Access Contol Lists (ACLs) <https://docs.aws.amazon.com/memorydb/latest/devguide/clusters.acls.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html
    :cloudformationResource: AWS::MemoryDB::ACL
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
        
        cfn_aCLProps_mixin = memorydb_mixins.CfnACLPropsMixin(memorydb_mixins.CfnACLMixinProps(
            acl_name="aclName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_names=["userNames"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnACLMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MemoryDB::ACL``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912ce848d284dcc1e3264347231caa8da702ad43b65c02e7f159cfd598aee791)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bccf47bf452d4ffe82f1d5667761e7cb8d79369a7df5ae90d8667d989dccaf4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4719d5f721345431bda2c7cd4871e5755f3131b22cfa092ff5a56cee976bca)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnACLMixinProps:
        return typing.cast(CfnACLMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "acl_name": "aclName",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "cluster_endpoint": "clusterEndpoint",
        "cluster_name": "clusterName",
        "data_tiering": "dataTiering",
        "description": "description",
        "engine": "engine",
        "engine_version": "engineVersion",
        "final_snapshot_name": "finalSnapshotName",
        "ip_discovery": "ipDiscovery",
        "kms_key_id": "kmsKeyId",
        "maintenance_window": "maintenanceWindow",
        "multi_region_cluster_name": "multiRegionClusterName",
        "network_type": "networkType",
        "node_type": "nodeType",
        "num_replicas_per_shard": "numReplicasPerShard",
        "num_shards": "numShards",
        "parameter_group_name": "parameterGroupName",
        "port": "port",
        "security_group_ids": "securityGroupIds",
        "snapshot_arns": "snapshotArns",
        "snapshot_name": "snapshotName",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "snapshot_window": "snapshotWindow",
        "sns_topic_arn": "snsTopicArn",
        "sns_topic_status": "snsTopicStatus",
        "subnet_group_name": "subnetGroupName",
        "tags": "tags",
        "tls_enabled": "tlsEnabled",
    },
)
class CfnClusterMixinProps:
    def __init__(
        self,
        *,
        acl_name: typing.Optional[builtins.str] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        cluster_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.EndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        data_tiering: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        final_snapshot_name: typing.Optional[builtins.str] = None,
        ip_discovery: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[builtins.str] = None,
        multi_region_cluster_name: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        num_replicas_per_shard: typing.Optional[jsii.Number] = None,
        num_shards: typing.Optional[jsii.Number] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        sns_topic_arn: typing.Optional[builtins.str] = None,
        sns_topic_status: typing.Optional[builtins.str] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tls_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnClusterPropsMixin.

        :param acl_name: The name of the Access Control List to associate with the cluster .
        :param auto_minor_version_upgrade: When set to true, the cluster will automatically receive minor engine version upgrades after launch.
        :param cluster_endpoint: The cluster 's configuration endpoint.
        :param cluster_name: The name of the cluster .
        :param data_tiering: Enables data tiering. Data tiering is only supported for clusters using the r6gd node type. This parameter must be set when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/memorydb/latest/devguide/data-tiering.html>`_ .
        :param description: A description of the cluster .
        :param engine: The name of the engine used by the cluster.
        :param engine_version: The Redis engine version used by the cluster .
        :param final_snapshot_name: The user-supplied name of a final cluster snapshot. This is the unique name that identifies the snapshot. MemoryDB creates the snapshot, and then deletes the cluster immediately afterward.
        :param ip_discovery: The mechanism that the cluster uses to discover IP addresses. Returns 'ipv4' when DNS endpoints resolve to IPv4 addresses, or 'ipv6' when DNS endpoints resolve to IPv6 addresses.
        :param kms_key_id: The ID of the KMS key used to encrypt the cluster .
        :param maintenance_window: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ``ddd:hh24:mi-ddd:hh24:mi`` (24H Clock UTC). The minimum maintenance window is a 60 minute period. *Pattern* : ``ddd:hh24:mi-ddd:hh24:mi``
        :param multi_region_cluster_name: The name of the multi-Region cluster that this cluster belongs to.
        :param network_type: The IP address type for the cluster. Returns 'ipv4' for IPv4 only, 'ipv6' for IPv6 only, or 'dual-stack' if the cluster supports both IPv4 and IPv6 addressing.
        :param node_type: The cluster 's node type.
        :param num_replicas_per_shard: The number of replicas to apply to each shard. *Default value* : ``1`` *Maximum value* : ``5``
        :param num_shards: The number of shards in the cluster .
        :param parameter_group_name: The name of the parameter group used by the cluster .
        :param port: The port used by the cluster .
        :param security_group_ids: A list of security group names to associate with this cluster .
        :param snapshot_arns: A list of Amazon Resource Names (ARN) that uniquely identify the RDB snapshot files stored in Amazon S3. The snapshot files are used to populate the new cluster . The Amazon S3 object name in the ARN cannot contain any commas.
        :param snapshot_name: The name of a snapshot from which to restore data into the new cluster . The snapshot status changes to restoring while the new cluster is being created.
        :param snapshot_retention_limit: The number of days for which MemoryDB retains automatic snapshots before deleting them. For example, if you set SnapshotRetentionLimit to 5, a snapshot that was taken today is retained for 5 days before being deleted.
        :param snapshot_window: The daily time range (in UTC) during which MemoryDB begins taking a daily snapshot of your shard. Example: 05:00-09:00 If you do not specify this parameter, MemoryDB automatically chooses an appropriate time range.
        :param sns_topic_arn: When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the SNS topic, such as ``arn:aws:memorydb:us-east-1:123456789012:mySNSTopic``.
        :param sns_topic_status: The SNS topic must be in Active status to receive notifications.
        :param subnet_group_name: The name of the subnet group used by the cluster .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param tls_enabled: A flag to indicate if In-transit encryption is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
            
            cfn_cluster_mixin_props = memorydb_mixins.CfnClusterMixinProps(
                acl_name="aclName",
                auto_minor_version_upgrade=False,
                cluster_endpoint=memorydb_mixins.CfnClusterPropsMixin.EndpointProperty(
                    address="address",
                    port=123
                ),
                cluster_name="clusterName",
                data_tiering="dataTiering",
                description="description",
                engine="engine",
                engine_version="engineVersion",
                final_snapshot_name="finalSnapshotName",
                ip_discovery="ipDiscovery",
                kms_key_id="kmsKeyId",
                maintenance_window="maintenanceWindow",
                multi_region_cluster_name="multiRegionClusterName",
                network_type="networkType",
                node_type="nodeType",
                num_replicas_per_shard=123,
                num_shards=123,
                parameter_group_name="parameterGroupName",
                port=123,
                security_group_ids=["securityGroupIds"],
                snapshot_arns=["snapshotArns"],
                snapshot_name="snapshotName",
                snapshot_retention_limit=123,
                snapshot_window="snapshotWindow",
                sns_topic_arn="snsTopicArn",
                sns_topic_status="snsTopicStatus",
                subnet_group_name="subnetGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tls_enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8638a8c97ccc52572800f407fef2e3f2f0bc8e78d525bac2e029c9e478cd3676)
            check_type(argname="argument acl_name", value=acl_name, expected_type=type_hints["acl_name"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument cluster_endpoint", value=cluster_endpoint, expected_type=type_hints["cluster_endpoint"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument data_tiering", value=data_tiering, expected_type=type_hints["data_tiering"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument final_snapshot_name", value=final_snapshot_name, expected_type=type_hints["final_snapshot_name"])
            check_type(argname="argument ip_discovery", value=ip_discovery, expected_type=type_hints["ip_discovery"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument multi_region_cluster_name", value=multi_region_cluster_name, expected_type=type_hints["multi_region_cluster_name"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument num_replicas_per_shard", value=num_replicas_per_shard, expected_type=type_hints["num_replicas_per_shard"])
            check_type(argname="argument num_shards", value=num_shards, expected_type=type_hints["num_shards"])
            check_type(argname="argument parameter_group_name", value=parameter_group_name, expected_type=type_hints["parameter_group_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument snapshot_arns", value=snapshot_arns, expected_type=type_hints["snapshot_arns"])
            check_type(argname="argument snapshot_name", value=snapshot_name, expected_type=type_hints["snapshot_name"])
            check_type(argname="argument snapshot_retention_limit", value=snapshot_retention_limit, expected_type=type_hints["snapshot_retention_limit"])
            check_type(argname="argument snapshot_window", value=snapshot_window, expected_type=type_hints["snapshot_window"])
            check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
            check_type(argname="argument sns_topic_status", value=sns_topic_status, expected_type=type_hints["sns_topic_status"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tls_enabled", value=tls_enabled, expected_type=type_hints["tls_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acl_name is not None:
            self._values["acl_name"] = acl_name
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if cluster_endpoint is not None:
            self._values["cluster_endpoint"] = cluster_endpoint
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if data_tiering is not None:
            self._values["data_tiering"] = data_tiering
        if description is not None:
            self._values["description"] = description
        if engine is not None:
            self._values["engine"] = engine
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if final_snapshot_name is not None:
            self._values["final_snapshot_name"] = final_snapshot_name
        if ip_discovery is not None:
            self._values["ip_discovery"] = ip_discovery
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if multi_region_cluster_name is not None:
            self._values["multi_region_cluster_name"] = multi_region_cluster_name
        if network_type is not None:
            self._values["network_type"] = network_type
        if node_type is not None:
            self._values["node_type"] = node_type
        if num_replicas_per_shard is not None:
            self._values["num_replicas_per_shard"] = num_replicas_per_shard
        if num_shards is not None:
            self._values["num_shards"] = num_shards
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name
        if port is not None:
            self._values["port"] = port
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if snapshot_arns is not None:
            self._values["snapshot_arns"] = snapshot_arns
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if snapshot_window is not None:
            self._values["snapshot_window"] = snapshot_window
        if sns_topic_arn is not None:
            self._values["sns_topic_arn"] = sns_topic_arn
        if sns_topic_status is not None:
            self._values["sns_topic_status"] = sns_topic_status
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name
        if tags is not None:
            self._values["tags"] = tags
        if tls_enabled is not None:
            self._values["tls_enabled"] = tls_enabled

    @builtins.property
    def acl_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Access Control List to associate with the cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-aclname
        '''
        result = self._values.get("acl_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When set to true, the cluster will automatically receive minor engine version upgrades after launch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cluster_endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EndpointProperty"]]:
        '''The cluster 's configuration endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-clusterendpoint
        '''
        result = self._values.get("cluster_endpoint")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EndpointProperty"]], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_tiering(self) -> typing.Optional[builtins.str]:
        '''Enables data tiering.

        Data tiering is only supported for clusters using the r6gd node type. This parameter must be set when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/memorydb/latest/devguide/data-tiering.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-datatiering
        '''
        result = self._values.get("data_tiering")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The name of the engine used by the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The Redis engine version used by the cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def final_snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The user-supplied name of a final cluster snapshot.

        This is the unique name that identifies the snapshot. MemoryDB creates the snapshot, and then deletes the cluster immediately afterward.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-finalsnapshotname
        '''
        result = self._values.get("final_snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_discovery(self) -> typing.Optional[builtins.str]:
        '''The mechanism that the cluster uses to discover IP addresses.

        Returns 'ipv4' when DNS endpoints resolve to IPv4 addresses, or 'ipv6' when DNS endpoints resolve to IPv6 addresses.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-ipdiscovery
        '''
        result = self._values.get("ip_discovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the KMS key used to encrypt the cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Specifies the weekly time range during which maintenance on the cluster is performed.

        It is specified as a range in the format ``ddd:hh24:mi-ddd:hh24:mi`` (24H Clock UTC). The minimum maintenance window is a 60 minute period.

        *Pattern* : ``ddd:hh24:mi-ddd:hh24:mi``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-maintenancewindow
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_region_cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the multi-Region cluster that this cluster belongs to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-multiregionclustername
        '''
        result = self._values.get("multi_region_cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''The IP address type for the cluster.

        Returns 'ipv4' for IPv4 only, 'ipv6' for IPv6 only, or 'dual-stack' if the cluster supports both IPv4 and IPv6 addressing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''The cluster 's node type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-nodetype
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_replicas_per_shard(self) -> typing.Optional[jsii.Number]:
        '''The number of replicas to apply to each shard.

        *Default value* : ``1``

        *Maximum value* : ``5``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-numreplicaspershard
        '''
        result = self._values.get("num_replicas_per_shard")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def num_shards(self) -> typing.Optional[jsii.Number]:
        '''The number of shards in the cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-numshards
        '''
        result = self._values.get("num_shards")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group used by the cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port used by the cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group names to associate with this cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARN) that uniquely identify the RDB snapshot files stored in Amazon S3.

        The snapshot files are used to populate the new cluster . The Amazon S3 object name in the ARN cannot contain any commas.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotarns
        '''
        result = self._values.get("snapshot_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of a snapshot from which to restore data into the new cluster .

        The snapshot status changes to restoring while the new cluster is being created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotname
        '''
        result = self._values.get("snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which MemoryDB retains automatic snapshots before deleting them.

        For example, if you set SnapshotRetentionLimit to 5, a snapshot that was taken today is retained for 5 days before being deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotretentionlimit
        '''
        result = self._values.get("snapshot_retention_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range (in UTC) during which MemoryDB begins taking a daily snapshot of your shard.

        Example: 05:00-09:00 If you do not specify this parameter, MemoryDB automatically chooses an appropriate time range.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotwindow
        '''
        result = self._values.get("snapshot_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the SNS topic, such as ``arn:aws:memorydb:us-east-1:123456789012:mySNSTopic``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snstopicarn
        '''
        result = self._values.get("sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_status(self) -> typing.Optional[builtins.str]:
        '''The SNS topic must be in Active status to receive notifications.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snstopicstatus
        '''
        result = self._values.get("sns_topic_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group used by the cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tls_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A flag to indicate if In-transit encryption is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-tlsenabled
        '''
        result = self._values.get("tls_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnClusterPropsMixin",
):
    '''Specifies a cluster .

    All nodes in the cluster run the same protocol-compliant engine software.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html
    :cloudformationResource: AWS::MemoryDB::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
        
        cfn_cluster_props_mixin = memorydb_mixins.CfnClusterPropsMixin(memorydb_mixins.CfnClusterMixinProps(
            acl_name="aclName",
            auto_minor_version_upgrade=False,
            cluster_endpoint=memorydb_mixins.CfnClusterPropsMixin.EndpointProperty(
                address="address",
                port=123
            ),
            cluster_name="clusterName",
            data_tiering="dataTiering",
            description="description",
            engine="engine",
            engine_version="engineVersion",
            final_snapshot_name="finalSnapshotName",
            ip_discovery="ipDiscovery",
            kms_key_id="kmsKeyId",
            maintenance_window="maintenanceWindow",
            multi_region_cluster_name="multiRegionClusterName",
            network_type="networkType",
            node_type="nodeType",
            num_replicas_per_shard=123,
            num_shards=123,
            parameter_group_name="parameterGroupName",
            port=123,
            security_group_ids=["securityGroupIds"],
            snapshot_arns=["snapshotArns"],
            snapshot_name="snapshotName",
            snapshot_retention_limit=123,
            snapshot_window="snapshotWindow",
            sns_topic_arn="snsTopicArn",
            sns_topic_status="snsTopicStatus",
            subnet_group_name="subnetGroupName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tls_enabled=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MemoryDB::Cluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5643987f476ea31ebdcddaa41552f1114a79c192f8a98570233ddae40553125a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__457f31a733a141b485e2fd44ca089c1def431da374ff3088beb95f6ba3e1e0de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c28f9e6d73575cceaf83881c4bbe973a5d7f68e8ae01a750feaf516e623268c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClusterMixinProps:
        return typing.cast(CfnClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnClusterPropsMixin.EndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address", "port": "port"},
    )
    class EndpointProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Represents the information required for client programs to connect to the cluster and its nodes.

            :param address: The DNS hostname of the node.
            :param port: The port number that the engine is listening on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-cluster-endpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
                
                endpoint_property = memorydb_mixins.CfnClusterPropsMixin.EndpointProperty(
                    address="address",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcc470e6b378e39f974ff31d430b9fd188ea5b5945b367d4375bf48756a4206a)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The DNS hostname of the node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-cluster-endpoint.html#cfn-memorydb-cluster-endpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number that the engine is listening on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-cluster-endpoint.html#cfn-memorydb-cluster-endpoint-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnMultiRegionClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "engine": "engine",
        "engine_version": "engineVersion",
        "multi_region_cluster_name_suffix": "multiRegionClusterNameSuffix",
        "multi_region_parameter_group_name": "multiRegionParameterGroupName",
        "node_type": "nodeType",
        "num_shards": "numShards",
        "tags": "tags",
        "tls_enabled": "tlsEnabled",
        "update_strategy": "updateStrategy",
    },
)
class CfnMultiRegionClusterMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        multi_region_cluster_name_suffix: typing.Optional[builtins.str] = None,
        multi_region_parameter_group_name: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        num_shards: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tls_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        update_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMultiRegionClusterPropsMixin.

        :param description: The description of the multi-Region cluster.
        :param engine: The name of the engine used by the multi-Region cluster.
        :param engine_version: The version of the engine used by the multi-Region cluster.
        :param multi_region_cluster_name_suffix: A suffix to be added to the Multi-Region cluster name. Amazon MemoryDB automatically applies a prefix to the Multi-Region cluster Name when it is created. Each Amazon Region has its own prefix. For instance, a Multi-Region cluster Name created in the US-West-1 region will begin with "virxk", along with the suffix name you provide. The suffix guarantees uniqueness of the Multi-Region cluster name across multiple regions.
        :param multi_region_parameter_group_name: The name of the multi-Region parameter group associated with the cluster.
        :param node_type: The node type used by the multi-Region cluster.
        :param num_shards: The number of shards in the multi-Region cluster.
        :param tags: A list of tags to be applied to the multi-Region cluster.
        :param tls_enabled: Indiciates if the multi-Region cluster is TLS enabled.
        :param update_strategy: The strategy to use for the update operation. Supported values are "coordinated" or "uncoordinated".

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
            
            cfn_multi_region_cluster_mixin_props = memorydb_mixins.CfnMultiRegionClusterMixinProps(
                description="description",
                engine="engine",
                engine_version="engineVersion",
                multi_region_cluster_name_suffix="multiRegionClusterNameSuffix",
                multi_region_parameter_group_name="multiRegionParameterGroupName",
                node_type="nodeType",
                num_shards=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tls_enabled=False,
                update_strategy="updateStrategy"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37240c6669502dd1f7c2f9667fce8a80cacd410c8ad1418cf8eb9ada02717450)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument multi_region_cluster_name_suffix", value=multi_region_cluster_name_suffix, expected_type=type_hints["multi_region_cluster_name_suffix"])
            check_type(argname="argument multi_region_parameter_group_name", value=multi_region_parameter_group_name, expected_type=type_hints["multi_region_parameter_group_name"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument num_shards", value=num_shards, expected_type=type_hints["num_shards"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tls_enabled", value=tls_enabled, expected_type=type_hints["tls_enabled"])
            check_type(argname="argument update_strategy", value=update_strategy, expected_type=type_hints["update_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if engine is not None:
            self._values["engine"] = engine
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if multi_region_cluster_name_suffix is not None:
            self._values["multi_region_cluster_name_suffix"] = multi_region_cluster_name_suffix
        if multi_region_parameter_group_name is not None:
            self._values["multi_region_parameter_group_name"] = multi_region_parameter_group_name
        if node_type is not None:
            self._values["node_type"] = node_type
        if num_shards is not None:
            self._values["num_shards"] = num_shards
        if tags is not None:
            self._values["tags"] = tags
        if tls_enabled is not None:
            self._values["tls_enabled"] = tls_enabled
        if update_strategy is not None:
            self._values["update_strategy"] = update_strategy

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the multi-Region cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html#cfn-memorydb-multiregioncluster-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The name of the engine used by the multi-Region cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html#cfn-memorydb-multiregioncluster-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version of the engine used by the multi-Region cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html#cfn-memorydb-multiregioncluster-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_region_cluster_name_suffix(self) -> typing.Optional[builtins.str]:
        '''A suffix to be added to the Multi-Region cluster name.

        Amazon MemoryDB automatically applies a prefix to the Multi-Region cluster Name when it is created. Each Amazon Region has its own prefix. For instance, a Multi-Region cluster Name created in the US-West-1 region will begin with "virxk", along with the suffix name you provide. The suffix guarantees uniqueness of the Multi-Region cluster name across multiple regions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html#cfn-memorydb-multiregioncluster-multiregionclusternamesuffix
        '''
        result = self._values.get("multi_region_cluster_name_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_region_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the multi-Region parameter group associated with the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html#cfn-memorydb-multiregioncluster-multiregionparametergroupname
        '''
        result = self._values.get("multi_region_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''The node type used by the multi-Region cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html#cfn-memorydb-multiregioncluster-nodetype
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_shards(self) -> typing.Optional[jsii.Number]:
        '''The number of shards in the multi-Region cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html#cfn-memorydb-multiregioncluster-numshards
        '''
        result = self._values.get("num_shards")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to be applied to the multi-Region cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html#cfn-memorydb-multiregioncluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tls_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indiciates if the multi-Region cluster is TLS enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html#cfn-memorydb-multiregioncluster-tlsenabled
        '''
        result = self._values.get("tls_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def update_strategy(self) -> typing.Optional[builtins.str]:
        '''The strategy to use for the update operation.

        Supported values are "coordinated" or "uncoordinated".

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html#cfn-memorydb-multiregioncluster-updatestrategy
        '''
        result = self._values.get("update_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMultiRegionClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMultiRegionClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnMultiRegionClusterPropsMixin",
):
    '''Represents a multi-Region cluster.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-multiregioncluster.html
    :cloudformationResource: AWS::MemoryDB::MultiRegionCluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
        
        cfn_multi_region_cluster_props_mixin = memorydb_mixins.CfnMultiRegionClusterPropsMixin(memorydb_mixins.CfnMultiRegionClusterMixinProps(
            description="description",
            engine="engine",
            engine_version="engineVersion",
            multi_region_cluster_name_suffix="multiRegionClusterNameSuffix",
            multi_region_parameter_group_name="multiRegionParameterGroupName",
            node_type="nodeType",
            num_shards=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tls_enabled=False,
            update_strategy="updateStrategy"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMultiRegionClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MemoryDB::MultiRegionCluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0efb540e5107f20937a733308f654d35a4ad69d6168e5896c5351ee358c5f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a07fa34ecb412cadb2c2ef13a06ad02ca512ea9dd602910a076ef25ac11c2db)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6507b041b6f694d1da1b7226cee0ce9cfdb8a07306c3c7ca7f6364d78af0e4da)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMultiRegionClusterMixinProps:
        return typing.cast(CfnMultiRegionClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnParameterGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "family": "family",
        "parameter_group_name": "parameterGroupName",
        "parameters": "parameters",
        "tags": "tags",
    },
)
class CfnParameterGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        family: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnParameterGroupPropsMixin.

        :param description: A description of the parameter group.
        :param family: The name of the parameter group family that this parameter group is compatible with.
        :param parameter_group_name: The name of the parameter group.
        :param parameters: Returns the detailed parameter list for the parameter group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
            
            # parameters: Any
            
            cfn_parameter_group_mixin_props = memorydb_mixins.CfnParameterGroupMixinProps(
                description="description",
                family="family",
                parameter_group_name="parameterGroupName",
                parameters=parameters,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2291da450d3338257960b2ceaf0a44d44c1da216b2063788a6fc645129dc12f6)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument parameter_group_name", value=parameter_group_name, expected_type=type_hints["parameter_group_name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if family is not None:
            self._values["family"] = family
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group family that this parameter group is compatible with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-family
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''Returns the detailed parameter list for the parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnParameterGroupPropsMixin",
):
    '''Specifies a new MemoryDB parameter group.

    A parameter group is a collection of parameters and their values that are applied to all of the nodes in any cluster . For more information, see `Configuring engine parameters using parameter groups <https://docs.aws.amazon.com/memorydb/latest/devguide/parametergroups.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html
    :cloudformationResource: AWS::MemoryDB::ParameterGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
        
        # parameters: Any
        
        cfn_parameter_group_props_mixin = memorydb_mixins.CfnParameterGroupPropsMixin(memorydb_mixins.CfnParameterGroupMixinProps(
            description="description",
            family="family",
            parameter_group_name="parameterGroupName",
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
        props: typing.Union[CfnParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MemoryDB::ParameterGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6ed3309228f50659f9219f166c5dc1b4e228fc64e43d4ad42427e764aa1b87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc131f3d720eb8b4f54f5f4f738ac7f6d277f70281dccb94991749fc79a204d8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d0be81747004f74b1010b5b1e1e1b787daf42542e668a41c66d8366cc3ab45)
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
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnSubnetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "subnet_group_name": "subnetGroupName",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnSubnetGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSubnetGroupPropsMixin.

        :param description: A description of the subnet group.
        :param subnet_group_name: The name of the subnet group to be used for the cluster .
        :param subnet_ids: A list of Amazon VPC subnet IDs for the subnet group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
            
            cfn_subnet_group_mixin_props = memorydb_mixins.CfnSubnetGroupMixinProps(
                description="description",
                subnet_group_name="subnetGroupName",
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c88a335f544a0d1b83ff81fb02752e0c0d047079238c9dc3469e25c8ba2a13)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group to be used for the cluster .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon VPC subnet IDs for the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnSubnetGroupPropsMixin",
):
    '''Specifies a subnet group.

    A subnet group is a collection of subnets (typically private) that you can designate for your cluster s running in an Amazon Virtual Private Cloud (VPC) environment. When you create a cluster in an Amazon VPC , you must specify a subnet group. MemoryDB uses that subnet group to choose a subnet and IP addresses within that subnet to associate with your nodes. For more information, see `Subnets and subnet groups <https://docs.aws.amazon.com/memorydb/latest/devguide/subnetgroups.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html
    :cloudformationResource: AWS::MemoryDB::SubnetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
        
        cfn_subnet_group_props_mixin = memorydb_mixins.CfnSubnetGroupPropsMixin(memorydb_mixins.CfnSubnetGroupMixinProps(
            description="description",
            subnet_group_name="subnetGroupName",
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
        '''Create a mixin to apply properties to ``AWS::MemoryDB::SubnetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dfc3e6f45965e1d48223f97aeea008fa01b80c0e0edbd5dfd47906136709f38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9455b01ac7d059a90659ec6b2fd549973bbd55403eb5f7492586412c831078c9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4551ec24811d5c1801d353648cbbb199ffa8fd2b0698321fd374187075ff796d)
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
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnUserMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_string": "accessString",
        "authentication_mode": "authenticationMode",
        "tags": "tags",
        "user_name": "userName",
    },
)
class CfnUserMixinProps:
    def __init__(
        self,
        *,
        access_string: typing.Optional[builtins.str] = None,
        authentication_mode: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPropsMixin.

        :param access_string: Access permissions string used for this user.
        :param authentication_mode: Denotes whether the user requires a password to authenticate. *Example:* ``mynewdbuser: Type: AWS::MemoryDB::User Properties: AccessString: on ~* &* +@all AuthenticationMode: Passwords: '1234567890123456' Type: password UserName: mynewdbuser AuthenticationMode: { "Passwords": ["1234567890123456"], "Type": "Password" }``
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param user_name: The name of the user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
            
            # authentication_mode: Any
            
            cfn_user_mixin_props = memorydb_mixins.CfnUserMixinProps(
                access_string="accessString",
                authentication_mode=authentication_mode,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_name="userName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc77ac7f7337fb4ee406556bb81e0f39bf8654a58a36275b1b49fb3508fecfb)
            check_type(argname="argument access_string", value=access_string, expected_type=type_hints["access_string"])
            check_type(argname="argument authentication_mode", value=authentication_mode, expected_type=type_hints["authentication_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_string is not None:
            self._values["access_string"] = access_string
        if authentication_mode is not None:
            self._values["authentication_mode"] = authentication_mode
        if tags is not None:
            self._values["tags"] = tags
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def access_string(self) -> typing.Optional[builtins.str]:
        '''Access permissions string used for this user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-accessstring
        '''
        result = self._values.get("access_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_mode(self) -> typing.Any:
        '''Denotes whether the user requires a password to authenticate.

        *Example:*

        ``mynewdbuser: Type: AWS::MemoryDB::User Properties: AccessString: on ~* &* +@all AuthenticationMode: Passwords: '1234567890123456' Type: password UserName: mynewdbuser AuthenticationMode: { "Passwords": ["1234567890123456"], "Type": "Password" }``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-authenticationmode
        '''
        result = self._values.get("authentication_mode")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The name of the user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-username
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
    jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnUserPropsMixin",
):
    '''Specifies a MemoryDB user.

    For more information, see `Authenticating users with Access Contol Lists (ACLs) <https://docs.aws.amazon.com/memorydb/latest/devguide/clusters.acls.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html
    :cloudformationResource: AWS::MemoryDB::User
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
        
        # authentication_mode: Any
        
        cfn_user_props_mixin = memorydb_mixins.CfnUserPropsMixin(memorydb_mixins.CfnUserMixinProps(
            access_string="accessString",
            authentication_mode=authentication_mode,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
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
        '''Create a mixin to apply properties to ``AWS::MemoryDB::User``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c08d756879d9930852f5c45817e2eb8d7bb2deb09efb63c0dcf5b2e7bf3070)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14d78d3f75066d52afcefd6fb989911c2d1e62db63ab2fc071f5263162da77c0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c2ce68d7a2c417f889bda0ad73e614c582f506b90b4deffe39f1c0bcc3511e)
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
        jsii_type="@aws-cdk/mixins-preview.aws_memorydb.mixins.CfnUserPropsMixin.AuthenticationModeProperty",
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
            '''Denotes the user's authentication properties, such as whether it requires a password to authenticate.

            Used in output responses.

            :param passwords: The password(s) used for authentication.
            :param type: Indicates whether the user requires a password to authenticate. All newly-created users require a password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-user-authenticationmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_memorydb import mixins as memorydb_mixins
                
                authentication_mode_property = memorydb_mixins.CfnUserPropsMixin.AuthenticationModeProperty(
                    passwords=["passwords"],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9d4abf0b56c5111a4e744e011f5404fb0d3ed96b3e3df24bcdac0314e63a0af)
                check_type(argname="argument passwords", value=passwords, expected_type=type_hints["passwords"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if passwords is not None:
                self._values["passwords"] = passwords
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def passwords(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The password(s) used for authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-user-authenticationmode.html#cfn-memorydb-user-authenticationmode-passwords
            '''
            result = self._values.get("passwords")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Indicates whether the user requires a password to authenticate.

            All newly-created users require a password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-user-authenticationmode.html#cfn-memorydb-user-authenticationmode-type
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
    "CfnACLMixinProps",
    "CfnACLPropsMixin",
    "CfnClusterMixinProps",
    "CfnClusterPropsMixin",
    "CfnMultiRegionClusterMixinProps",
    "CfnMultiRegionClusterPropsMixin",
    "CfnParameterGroupMixinProps",
    "CfnParameterGroupPropsMixin",
    "CfnSubnetGroupMixinProps",
    "CfnSubnetGroupPropsMixin",
    "CfnUserMixinProps",
    "CfnUserPropsMixin",
]

publication.publish()

def _typecheckingstub__901275ce2d2b214070fbfa72a3ccb9fc912046aa1831d865264db4a71dfbb583(
    *,
    acl_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912ce848d284dcc1e3264347231caa8da702ad43b65c02e7f159cfd598aee791(
    props: typing.Union[CfnACLMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bccf47bf452d4ffe82f1d5667761e7cb8d79369a7df5ae90d8667d989dccaf4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4719d5f721345431bda2c7cd4871e5755f3131b22cfa092ff5a56cee976bca(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8638a8c97ccc52572800f407fef2e3f2f0bc8e78d525bac2e029c9e478cd3676(
    *,
    acl_name: typing.Optional[builtins.str] = None,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cluster_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.EndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    data_tiering: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    final_snapshot_name: typing.Optional[builtins.str] = None,
    ip_discovery: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[builtins.str] = None,
    multi_region_cluster_name: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    num_replicas_per_shard: typing.Optional[jsii.Number] = None,
    num_shards: typing.Optional[jsii.Number] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    snapshot_retention_limit: typing.Optional[jsii.Number] = None,
    snapshot_window: typing.Optional[builtins.str] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
    sns_topic_status: typing.Optional[builtins.str] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5643987f476ea31ebdcddaa41552f1114a79c192f8a98570233ddae40553125a(
    props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457f31a733a141b485e2fd44ca089c1def431da374ff3088beb95f6ba3e1e0de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c28f9e6d73575cceaf83881c4bbe973a5d7f68e8ae01a750feaf516e623268c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc470e6b378e39f974ff31d430b9fd188ea5b5945b367d4375bf48756a4206a(
    *,
    address: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37240c6669502dd1f7c2f9667fce8a80cacd410c8ad1418cf8eb9ada02717450(
    *,
    description: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    multi_region_cluster_name_suffix: typing.Optional[builtins.str] = None,
    multi_region_parameter_group_name: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    num_shards: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    update_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0efb540e5107f20937a733308f654d35a4ad69d6168e5896c5351ee358c5f8(
    props: typing.Union[CfnMultiRegionClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a07fa34ecb412cadb2c2ef13a06ad02ca512ea9dd602910a076ef25ac11c2db(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6507b041b6f694d1da1b7226cee0ce9cfdb8a07306c3c7ca7f6364d78af0e4da(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2291da450d3338257960b2ceaf0a44d44c1da216b2063788a6fc645129dc12f6(
    *,
    description: typing.Optional[builtins.str] = None,
    family: typing.Optional[builtins.str] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6ed3309228f50659f9219f166c5dc1b4e228fc64e43d4ad42427e764aa1b87(
    props: typing.Union[CfnParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc131f3d720eb8b4f54f5f4f738ac7f6d277f70281dccb94991749fc79a204d8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d0be81747004f74b1010b5b1e1e1b787daf42542e668a41c66d8366cc3ab45(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c88a335f544a0d1b83ff81fb02752e0c0d047079238c9dc3469e25c8ba2a13(
    *,
    description: typing.Optional[builtins.str] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dfc3e6f45965e1d48223f97aeea008fa01b80c0e0edbd5dfd47906136709f38(
    props: typing.Union[CfnSubnetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9455b01ac7d059a90659ec6b2fd549973bbd55403eb5f7492586412c831078c9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4551ec24811d5c1801d353648cbbb199ffa8fd2b0698321fd374187075ff796d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc77ac7f7337fb4ee406556bb81e0f39bf8654a58a36275b1b49fb3508fecfb(
    *,
    access_string: typing.Optional[builtins.str] = None,
    authentication_mode: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c08d756879d9930852f5c45817e2eb8d7bb2deb09efb63c0dcf5b2e7bf3070(
    props: typing.Union[CfnUserMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d78d3f75066d52afcefd6fb989911c2d1e62db63ab2fc071f5263162da77c0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c2ce68d7a2c417f889bda0ad73e614c582f506b90b4deffe39f1c0bcc3511e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d4abf0b56c5111a4e744e011f5404fb0d3ed96b3e3df24bcdac0314e63a0af(
    *,
    passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
