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
    jsii_type="@aws-cdk/mixins-preview.aws_dax.mixins.CfnClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "cluster_endpoint_encryption_type": "clusterEndpointEncryptionType",
        "cluster_name": "clusterName",
        "description": "description",
        "iam_role_arn": "iamRoleArn",
        "network_type": "networkType",
        "node_type": "nodeType",
        "notification_topic_arn": "notificationTopicArn",
        "parameter_group_name": "parameterGroupName",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "replication_factor": "replicationFactor",
        "security_group_ids": "securityGroupIds",
        "sse_specification": "sseSpecification",
        "subnet_group_name": "subnetGroupName",
        "tags": "tags",
    },
)
class CfnClusterMixinProps:
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cluster_endpoint_encryption_type: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        replication_factor: typing.Optional[jsii.Number] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        sse_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.SSESpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnClusterPropsMixin.

        :param availability_zones: The Availability Zones (AZs) in which the cluster nodes will reside after the cluster has been created or updated. If provided, the length of this list must equal the ``ReplicationFactor`` parameter. If you omit this parameter, DAX will spread the nodes across Availability Zones for the highest availability.
        :param cluster_endpoint_encryption_type: The encryption type of the cluster's endpoint. Available values are:. - ``NONE`` - The cluster's endpoint will be unencrypted. - ``TLS`` - The cluster's endpoint will be encrypted with Transport Layer Security, and will provide an x509 certificate for authentication. The default value is ``NONE`` .
        :param cluster_name: The name of the DAX cluster.
        :param description: The description of the cluster.
        :param iam_role_arn: A valid Amazon Resource Name (ARN) that identifies an IAM role. At runtime, DAX will assume this role and use the role's permissions to access DynamoDB on your behalf.
        :param network_type: The IP address type of the cluster. Values are:. - ``ipv4`` - IPv4 addresses only - ``ipv6`` - IPv6 addresses only - ``dual_stack`` - Both IPv4 and IPv6 addresses
        :param node_type: The node type for the nodes in the cluster. (All nodes in a DAX cluster are of the same type.)
        :param notification_topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to which notifications will be sent. .. epigraph:: The Amazon SNS topic owner must be same as the DAX cluster owner.
        :param parameter_group_name: The parameter group to be associated with the DAX cluster.
        :param preferred_maintenance_window: A range of time when maintenance of DAX cluster software will be performed. For example: ``sun:01:00-sun:09:00`` . Cluster maintenance normally takes less than 30 minutes, and is performed automatically within the maintenance window.
        :param replication_factor: The number of nodes in the DAX cluster. A replication factor of 1 will create a single-node cluster, without any read replicas. For additional fault tolerance, you can create a multiple node cluster with one or more read replicas. To do this, set ``ReplicationFactor`` to a number between 3 (one primary and two read replicas) and 10 (one primary and nine read replicas). ``If the AvailabilityZones`` parameter is provided, its length must equal the ``ReplicationFactor`` . .. epigraph:: AWS recommends that you have at least two read replicas per cluster.
        :param security_group_ids: A list of security group IDs to be assigned to each node in the DAX cluster. (Each of the security group ID is system-generated.) If this parameter is not specified, DAX assigns the default VPC security group to each node.
        :param sse_specification: Represents the settings used to enable server-side encryption on the cluster.
        :param subnet_group_name: The name of the subnet group to be used for the replication group. .. epigraph:: DAX clusters can only run in an Amazon VPC environment. All of the subnets that you specify in a subnet group must exist in the same VPC.
        :param tags: A set of tags to associate with the DAX cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dax import mixins as dax_mixins
            
            # tags: Any
            
            cfn_cluster_mixin_props = dax_mixins.CfnClusterMixinProps(
                availability_zones=["availabilityZones"],
                cluster_endpoint_encryption_type="clusterEndpointEncryptionType",
                cluster_name="clusterName",
                description="description",
                iam_role_arn="iamRoleArn",
                network_type="networkType",
                node_type="nodeType",
                notification_topic_arn="notificationTopicArn",
                parameter_group_name="parameterGroupName",
                preferred_maintenance_window="preferredMaintenanceWindow",
                replication_factor=123,
                security_group_ids=["securityGroupIds"],
                sse_specification=dax_mixins.CfnClusterPropsMixin.SSESpecificationProperty(
                    sse_enabled=False
                ),
                subnet_group_name="subnetGroupName",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2941e600c669a939f436d5237f8c99e80344aa408c59948c9915d58dd26340c8)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cluster_endpoint_encryption_type", value=cluster_endpoint_encryption_type, expected_type=type_hints["cluster_endpoint_encryption_type"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument notification_topic_arn", value=notification_topic_arn, expected_type=type_hints["notification_topic_arn"])
            check_type(argname="argument parameter_group_name", value=parameter_group_name, expected_type=type_hints["parameter_group_name"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument replication_factor", value=replication_factor, expected_type=type_hints["replication_factor"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cluster_endpoint_encryption_type is not None:
            self._values["cluster_endpoint_encryption_type"] = cluster_endpoint_encryption_type
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if description is not None:
            self._values["description"] = description
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if network_type is not None:
            self._values["network_type"] = network_type
        if node_type is not None:
            self._values["node_type"] = node_type
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if replication_factor is not None:
            self._values["replication_factor"] = replication_factor
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Availability Zones (AZs) in which the cluster nodes will reside after the cluster has been created or updated.

        If provided, the length of this list must equal the ``ReplicationFactor`` parameter. If you omit this parameter, DAX will spread the nodes across Availability Zones for the highest availability.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-availabilityzones
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cluster_endpoint_encryption_type(self) -> typing.Optional[builtins.str]:
        '''The encryption type of the cluster's endpoint. Available values are:.

        - ``NONE`` - The cluster's endpoint will be unencrypted.
        - ``TLS`` - The cluster's endpoint will be encrypted with Transport Layer Security, and will provide an x509 certificate for authentication.

        The default value is ``NONE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clusterendpointencryptiontype
        '''
        result = self._values.get("cluster_endpoint_encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the DAX cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''A valid Amazon Resource Name (ARN) that identifies an IAM role.

        At runtime, DAX will assume this role and use the role's permissions to access DynamoDB on your behalf.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''The IP address type of the cluster. Values are:.

        - ``ipv4`` - IPv4 addresses only
        - ``ipv6`` - IPv6 addresses only
        - ``dual_stack`` - Both IPv4 and IPv6 addresses

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''The node type for the nodes in the cluster.

        (All nodes in a DAX cluster are of the same type.)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-nodetype
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic to which notifications will be sent.

        .. epigraph::

           The Amazon SNS topic owner must be same as the DAX cluster owner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-notificationtopicarn
        '''
        result = self._values.get("notification_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The parameter group to be associated with the DAX cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''A range of time when maintenance of DAX cluster software will be performed.

        For example: ``sun:01:00-sun:09:00`` . Cluster maintenance normally takes less than 30 minutes, and is performed automatically within the maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_factor(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes in the DAX cluster.

        A replication factor of 1 will create a single-node cluster, without any read replicas. For additional fault tolerance, you can create a multiple node cluster with one or more read replicas. To do this, set ``ReplicationFactor`` to a number between 3 (one primary and two read replicas) and 10 (one primary and nine read replicas). ``If the AvailabilityZones`` parameter is provided, its length must equal the ``ReplicationFactor`` .
        .. epigraph::

           AWS recommends that you have at least two read replicas per cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-replicationfactor
        '''
        result = self._values.get("replication_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group IDs to be assigned to each node in the DAX cluster.

        (Each of the security group ID is system-generated.)

        If this parameter is not specified, DAX assigns the default VPC security group to each node.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SSESpecificationProperty"]]:
        '''Represents the settings used to enable server-side encryption on the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-ssespecification
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SSESpecificationProperty"]], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group to be used for the replication group.

        .. epigraph::

           DAX clusters can only run in an Amazon VPC environment. All of the subnets that you specify in a subnet group must exist in the same VPC.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''A set of tags to associate with the DAX cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_dax.mixins.CfnClusterPropsMixin",
):
    '''Creates a DAX cluster.

    All nodes in the cluster run the same DAX caching software.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html
    :cloudformationResource: AWS::DAX::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dax import mixins as dax_mixins
        
        # tags: Any
        
        cfn_cluster_props_mixin = dax_mixins.CfnClusterPropsMixin(dax_mixins.CfnClusterMixinProps(
            availability_zones=["availabilityZones"],
            cluster_endpoint_encryption_type="clusterEndpointEncryptionType",
            cluster_name="clusterName",
            description="description",
            iam_role_arn="iamRoleArn",
            network_type="networkType",
            node_type="nodeType",
            notification_topic_arn="notificationTopicArn",
            parameter_group_name="parameterGroupName",
            preferred_maintenance_window="preferredMaintenanceWindow",
            replication_factor=123,
            security_group_ids=["securityGroupIds"],
            sse_specification=dax_mixins.CfnClusterPropsMixin.SSESpecificationProperty(
                sse_enabled=False
            ),
            subnet_group_name="subnetGroupName",
            tags=tags
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
        '''Create a mixin to apply properties to ``AWS::DAX::Cluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3493e0caabd57163e7a4755a5de37007dcb3bf4323a1b1d52ae5c9c1b7af5ca6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69c9ee1372cbd412c91e94128c91f4de3928217ddfe044dac82840832779a903)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374c40dc3c8204667f33dfd242a5e17d1d6045685c4cf70815f94c9580566ca6)
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
        jsii_type="@aws-cdk/mixins-preview.aws_dax.mixins.CfnClusterPropsMixin.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"sse_enabled": "sseEnabled"},
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Represents the settings used to enable server-side encryption.

            :param sse_enabled: Indicates whether server-side encryption is enabled (true) or disabled (false) on the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dax-cluster-ssespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_dax import mixins as dax_mixins
                
                s_sESpecification_property = dax_mixins.CfnClusterPropsMixin.SSESpecificationProperty(
                    sse_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb30d1f0e211f37f34ab248ed295f0cbe2d66d740d5e5e7167d5b1dbffb15c67)
                check_type(argname="argument sse_enabled", value=sse_enabled, expected_type=type_hints["sse_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sse_enabled is not None:
                self._values["sse_enabled"] = sse_enabled

        @builtins.property
        def sse_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether server-side encryption is enabled (true) or disabled (false) on the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dax-cluster-ssespecification.html#cfn-dax-cluster-ssespecification-sseenabled
            '''
            result = self._values.get("sse_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_dax.mixins.CfnParameterGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "parameter_group_name": "parameterGroupName",
        "parameter_name_values": "parameterNameValues",
    },
)
class CfnParameterGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        parameter_name_values: typing.Any = None,
    ) -> None:
        '''Properties for CfnParameterGroupPropsMixin.

        :param description: A description of the parameter group.
        :param parameter_group_name: The name of the parameter group.
        :param parameter_name_values: An array of name-value pairs for the parameters in the group. Each element in the array represents a single parameter. .. epigraph:: ``record-ttl-millis`` and ``query-ttl-millis`` are the only supported parameter names. For more details, see `Configuring TTL Settings <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.cluster-management.html#DAX.cluster-management.custom-settings.ttl>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dax import mixins as dax_mixins
            
            # parameter_name_values: Any
            
            cfn_parameter_group_mixin_props = dax_mixins.CfnParameterGroupMixinProps(
                description="description",
                parameter_group_name="parameterGroupName",
                parameter_name_values=parameter_name_values
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8671e3673ea87669946cc73dded90bccb1be24bbfc071683a9c4712f4533ee69)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameter_group_name", value=parameter_group_name, expected_type=type_hints["parameter_group_name"])
            check_type(argname="argument parameter_name_values", value=parameter_name_values, expected_type=type_hints["parameter_name_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name
        if parameter_name_values is not None:
            self._values["parameter_name_values"] = parameter_name_values

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_name_values(self) -> typing.Any:
        '''An array of name-value pairs for the parameters in the group.

        Each element in the array represents a single parameter.
        .. epigraph::

           ``record-ttl-millis`` and ``query-ttl-millis`` are the only supported parameter names. For more details, see `Configuring TTL Settings <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.cluster-management.html#DAX.cluster-management.custom-settings.ttl>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parameternamevalues
        '''
        result = self._values.get("parameter_name_values")
        return typing.cast(typing.Any, result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_dax.mixins.CfnParameterGroupPropsMixin",
):
    '''A named set of parameters that are applied to all of the nodes in a DAX cluster.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html
    :cloudformationResource: AWS::DAX::ParameterGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dax import mixins as dax_mixins
        
        # parameter_name_values: Any
        
        cfn_parameter_group_props_mixin = dax_mixins.CfnParameterGroupPropsMixin(dax_mixins.CfnParameterGroupMixinProps(
            description="description",
            parameter_group_name="parameterGroupName",
            parameter_name_values=parameter_name_values
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
        '''Create a mixin to apply properties to ``AWS::DAX::ParameterGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06c6dde6531a7cf615392ae4c747138352b50a2379f7cc7017192a164fcf2a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e520e898e4765a7d1c98486f3d4d617d3a144bf216e50d02f73f2751e5c45a4c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__141e0cb2d9a4788cf31c28abd9f44d95a11d18b5419a7636062de4be60ac0267)
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
    jsii_type="@aws-cdk/mixins-preview.aws_dax.mixins.CfnSubnetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "subnet_group_name": "subnetGroupName",
        "subnet_ids": "subnetIds",
    },
)
class CfnSubnetGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnSubnetGroupPropsMixin.

        :param description: The description of the subnet group.
        :param subnet_group_name: The name of the subnet group.
        :param subnet_ids: A list of VPC subnet IDs for the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_dax import mixins as dax_mixins
            
            cfn_subnet_group_mixin_props = dax_mixins.CfnSubnetGroupMixinProps(
                description="description",
                subnet_group_name="subnetGroupName",
                subnet_ids=["subnetIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6404c9ed70be973d5aa89aabfe99b17eeeb068c22f7ec33ed913e350d2363d28)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of VPC subnet IDs for the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_dax.mixins.CfnSubnetGroupPropsMixin",
):
    '''Creates a new subnet group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html
    :cloudformationResource: AWS::DAX::SubnetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_dax import mixins as dax_mixins
        
        cfn_subnet_group_props_mixin = dax_mixins.CfnSubnetGroupPropsMixin(dax_mixins.CfnSubnetGroupMixinProps(
            description="description",
            subnet_group_name="subnetGroupName",
            subnet_ids=["subnetIds"]
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
        '''Create a mixin to apply properties to ``AWS::DAX::SubnetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7190932c7467f8ff94ea2f75fadf451806dbcbe394483b7c6f3fca90ea3d3a60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b73e02d6ac9b259f4b8e50d3a622d18d77743fb0bf43571734f8a383c12159dd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd9fddbb480a835b1c5536644e614e9e107dcf4d3637038e0a5ee0cedf744fc2)
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


__all__ = [
    "CfnClusterMixinProps",
    "CfnClusterPropsMixin",
    "CfnParameterGroupMixinProps",
    "CfnParameterGroupPropsMixin",
    "CfnSubnetGroupMixinProps",
    "CfnSubnetGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__2941e600c669a939f436d5237f8c99e80344aa408c59948c9915d58dd26340c8(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cluster_endpoint_encryption_type: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    notification_topic_arn: typing.Optional[builtins.str] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    replication_factor: typing.Optional[jsii.Number] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    sse_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3493e0caabd57163e7a4755a5de37007dcb3bf4323a1b1d52ae5c9c1b7af5ca6(
    props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c9ee1372cbd412c91e94128c91f4de3928217ddfe044dac82840832779a903(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374c40dc3c8204667f33dfd242a5e17d1d6045685c4cf70815f94c9580566ca6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb30d1f0e211f37f34ab248ed295f0cbe2d66d740d5e5e7167d5b1dbffb15c67(
    *,
    sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8671e3673ea87669946cc73dded90bccb1be24bbfc071683a9c4712f4533ee69(
    *,
    description: typing.Optional[builtins.str] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    parameter_name_values: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06c6dde6531a7cf615392ae4c747138352b50a2379f7cc7017192a164fcf2a8(
    props: typing.Union[CfnParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e520e898e4765a7d1c98486f3d4d617d3a144bf216e50d02f73f2751e5c45a4c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141e0cb2d9a4788cf31c28abd9f44d95a11d18b5419a7636062de4be60ac0267(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6404c9ed70be973d5aa89aabfe99b17eeeb068c22f7ec33ed913e350d2363d28(
    *,
    description: typing.Optional[builtins.str] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7190932c7467f8ff94ea2f75fadf451806dbcbe394483b7c6f3fca90ea3d3a60(
    props: typing.Union[CfnSubnetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73e02d6ac9b259f4b8e50d3a622d18d77743fb0bf43571734f8a383c12159dd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9fddbb480a835b1c5536644e614e9e107dcf4d3637038e0a5ee0cedf744fc2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
