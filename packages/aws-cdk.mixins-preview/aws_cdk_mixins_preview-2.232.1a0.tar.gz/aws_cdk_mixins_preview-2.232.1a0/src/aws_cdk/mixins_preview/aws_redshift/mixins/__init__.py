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
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_version_upgrade": "allowVersionUpgrade",
        "aqua_configuration_status": "aquaConfigurationStatus",
        "automated_snapshot_retention_period": "automatedSnapshotRetentionPeriod",
        "availability_zone": "availabilityZone",
        "availability_zone_relocation": "availabilityZoneRelocation",
        "availability_zone_relocation_status": "availabilityZoneRelocationStatus",
        "classic": "classic",
        "cluster_identifier": "clusterIdentifier",
        "cluster_parameter_group_name": "clusterParameterGroupName",
        "cluster_security_groups": "clusterSecurityGroups",
        "cluster_subnet_group_name": "clusterSubnetGroupName",
        "cluster_type": "clusterType",
        "cluster_version": "clusterVersion",
        "db_name": "dbName",
        "defer_maintenance": "deferMaintenance",
        "defer_maintenance_duration": "deferMaintenanceDuration",
        "defer_maintenance_end_time": "deferMaintenanceEndTime",
        "defer_maintenance_start_time": "deferMaintenanceStartTime",
        "destination_region": "destinationRegion",
        "elastic_ip": "elasticIp",
        "encrypted": "encrypted",
        "endpoint": "endpoint",
        "enhanced_vpc_routing": "enhancedVpcRouting",
        "hsm_client_certificate_identifier": "hsmClientCertificateIdentifier",
        "hsm_configuration_identifier": "hsmConfigurationIdentifier",
        "iam_roles": "iamRoles",
        "kms_key_id": "kmsKeyId",
        "logging_properties": "loggingProperties",
        "maintenance_track_name": "maintenanceTrackName",
        "manage_master_password": "manageMasterPassword",
        "manual_snapshot_retention_period": "manualSnapshotRetentionPeriod",
        "master_password_secret_kms_key_id": "masterPasswordSecretKmsKeyId",
        "master_username": "masterUsername",
        "master_user_password": "masterUserPassword",
        "multi_az": "multiAz",
        "namespace_resource_policy": "namespaceResourcePolicy",
        "node_type": "nodeType",
        "number_of_nodes": "numberOfNodes",
        "owner_account": "ownerAccount",
        "port": "port",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "publicly_accessible": "publiclyAccessible",
        "resource_action": "resourceAction",
        "revision_target": "revisionTarget",
        "rotate_encryption_key": "rotateEncryptionKey",
        "snapshot_cluster_identifier": "snapshotClusterIdentifier",
        "snapshot_copy_grant_name": "snapshotCopyGrantName",
        "snapshot_copy_manual": "snapshotCopyManual",
        "snapshot_copy_retention_period": "snapshotCopyRetentionPeriod",
        "snapshot_identifier": "snapshotIdentifier",
        "tags": "tags",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnClusterMixinProps:
    def __init__(
        self,
        *,
        allow_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        aqua_configuration_status: typing.Optional[builtins.str] = None,
        automated_snapshot_retention_period: typing.Optional[jsii.Number] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        availability_zone_relocation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        availability_zone_relocation_status: typing.Optional[builtins.str] = None,
        classic: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        cluster_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        cluster_subnet_group_name: typing.Optional[builtins.str] = None,
        cluster_type: typing.Optional[builtins.str] = None,
        cluster_version: typing.Optional[builtins.str] = None,
        db_name: typing.Optional[builtins.str] = None,
        defer_maintenance: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        defer_maintenance_duration: typing.Optional[jsii.Number] = None,
        defer_maintenance_end_time: typing.Optional[builtins.str] = None,
        defer_maintenance_start_time: typing.Optional[builtins.str] = None,
        destination_region: typing.Optional[builtins.str] = None,
        elastic_ip: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.EndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        enhanced_vpc_routing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        hsm_client_certificate_identifier: typing.Optional[builtins.str] = None,
        hsm_configuration_identifier: typing.Optional[builtins.str] = None,
        iam_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        logging_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.LoggingPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        maintenance_track_name: typing.Optional[builtins.str] = None,
        manage_master_password: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        manual_snapshot_retention_period: typing.Optional[jsii.Number] = None,
        master_password_secret_kms_key_id: typing.Optional[builtins.str] = None,
        master_username: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[builtins.str] = None,
        multi_az: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        namespace_resource_policy: typing.Any = None,
        node_type: typing.Optional[builtins.str] = None,
        number_of_nodes: typing.Optional[jsii.Number] = None,
        owner_account: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        resource_action: typing.Optional[builtins.str] = None,
        revision_target: typing.Optional[builtins.str] = None,
        rotate_encryption_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        snapshot_cluster_identifier: typing.Optional[builtins.str] = None,
        snapshot_copy_grant_name: typing.Optional[builtins.str] = None,
        snapshot_copy_manual: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        snapshot_copy_retention_period: typing.Optional[jsii.Number] = None,
        snapshot_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnClusterPropsMixin.

        :param allow_version_upgrade: If ``true`` , major version upgrades can be applied during the maintenance window to the Amazon Redshift engine that is running on the cluster. When a new major version of the Amazon Redshift engine is released, you can request that the service automatically apply upgrades during the maintenance window to the Amazon Redshift engine that is running on your cluster. Default: ``true``
        :param aqua_configuration_status: This parameter is retired. It does not set the AQUA configuration status. Amazon Redshift automatically determines whether to use AQUA (Advanced Query Accelerator).
        :param automated_snapshot_retention_period: The number of days that automated snapshots are retained. If the value is 0, automated snapshots are disabled. Even if automated snapshots are disabled, you can still create manual snapshots when you want with `CreateClusterSnapshot <https://docs.aws.amazon.com/redshift/latest/APIReference/API_CreateClusterSnapshot.html>`_ in the *Amazon Redshift API Reference* . Default: ``1`` Constraints: Must be a value from 0 to 35.
        :param availability_zone: The EC2 Availability Zone (AZ) in which you want Amazon Redshift to provision the cluster. For example, if you have several EC2 instances running in a specific Availability Zone, then you might want the cluster to be provisioned in the same zone in order to decrease network latency. Default: A random, system-chosen Availability Zone in the region that is specified by the endpoint. Example: ``us-east-2d`` Constraint: The specified Availability Zone must be in the same region as the current endpoint.
        :param availability_zone_relocation: The option to enable relocation for an Amazon Redshift cluster between Availability Zones after the cluster is created.
        :param availability_zone_relocation_status: Describes the status of the Availability Zone relocation operation.
        :param classic: A boolean value indicating whether the resize operation is using the classic resize process. If you don't provide this parameter or set the value to ``false`` , the resize type is elastic.
        :param cluster_identifier: A unique identifier for the cluster. You use this identifier to refer to the cluster for any subsequent cluster operations such as deleting or modifying. The identifier also appears in the Amazon Redshift console. Constraints: - Must contain from 1 to 63 alphanumeric characters or hyphens. - Alphabetic characters must be lowercase. - First character must be a letter. - Cannot end with a hyphen or contain two consecutive hyphens. - Must be unique for all clusters within an AWS account . Example: ``myexamplecluster``
        :param cluster_parameter_group_name: The name of the parameter group to be associated with this cluster. Default: The default Amazon Redshift cluster parameter group. For information about the default parameter group, go to `Working with Amazon Redshift Parameter Groups <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html>`_ Constraints: - Must be 1 to 255 alphanumeric characters or hyphens. - First character must be a letter. - Cannot end with a hyphen or contain two consecutive hyphens.
        :param cluster_security_groups: A list of security groups to be associated with this cluster. Default: The default cluster security group for Amazon Redshift.
        :param cluster_subnet_group_name: The name of a cluster subnet group to be associated with this cluster. If this parameter is not provided the resulting cluster will be deployed outside virtual private cloud (VPC).
        :param cluster_type: The type of the cluster. When cluster type is specified as. - ``single-node`` , the *NumberOfNodes* parameter is not required. - ``multi-node`` , the *NumberOfNodes* parameter is required. Valid Values: ``multi-node`` | ``single-node`` Default: ``multi-node``
        :param cluster_version: The version of the Amazon Redshift engine software that you want to deploy on the cluster. The version selected runs on all the nodes in the cluster. Constraints: Only version 1.0 is currently available. Example: ``1.0``
        :param db_name: The name of the first database to be created when the cluster is created. To create additional databases after the cluster is created, connect to the cluster with a SQL client and use SQL commands to create a database. For more information, go to `Create a Database <https://docs.aws.amazon.com/redshift/latest/dg/t_creating_database.html>`_ in the Amazon Redshift Database Developer Guide. Default: ``dev`` Constraints: - Must contain 1 to 64 alphanumeric characters. - Must contain only lowercase letters. - Cannot be a word that is reserved by the service. A list of reserved words can be found in `Reserved Words <https://docs.aws.amazon.com/redshift/latest/dg/r_pg_keywords.html>`_ in the Amazon Redshift Database Developer Guide.
        :param defer_maintenance: A Boolean indicating whether to enable the deferred maintenance window.
        :param defer_maintenance_duration: An integer indicating the duration of the maintenance window in days. If you specify a duration, you can't specify an end time. The duration must be 45 days or less.
        :param defer_maintenance_end_time: A timestamp for the end of the time period when we defer maintenance.
        :param defer_maintenance_start_time: A timestamp indicating the start time for the deferred maintenance window.
        :param destination_region: The destination region that snapshots are automatically copied to when cross-region snapshot copy is enabled.
        :param elastic_ip: The Elastic IP (EIP) address for the cluster. Constraints: The cluster must be provisioned in EC2-VPC and publicly-accessible through an Internet gateway. Don't specify the Elastic IP address for a publicly accessible cluster with availability zone relocation turned on. For more information about provisioning clusters in EC2-VPC, go to `Supported Platforms to Launch Your Cluster <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#cluster-platforms>`_ in the Amazon Redshift Cluster Management Guide.
        :param encrypted: If ``true`` , the data in the cluster is encrypted at rest. If you set the value on this parameter to ``false`` , the request will fail. Default: true
        :param endpoint: The connection endpoint.
        :param enhanced_vpc_routing: An option that specifies whether to create the cluster with enhanced VPC routing enabled. To create a cluster that uses enhanced VPC routing, the cluster must be in a VPC. For more information, see `Enhanced VPC Routing <https://docs.aws.amazon.com/redshift/latest/mgmt/enhanced-vpc-routing.html>`_ in the Amazon Redshift Cluster Management Guide. If this option is ``true`` , enhanced VPC routing is enabled. Default: false
        :param hsm_client_certificate_identifier: Specifies the name of the HSM client certificate the Amazon Redshift cluster uses to retrieve the data encryption keys stored in an HSM.
        :param hsm_configuration_identifier: Specifies the name of the HSM configuration that contains the information the Amazon Redshift cluster can use to retrieve and store keys in an HSM.
        :param iam_roles: A list of AWS Identity and Access Management (IAM) roles that can be used by the cluster to access other AWS services. You must supply the IAM roles in their Amazon Resource Name (ARN) format. The maximum number of IAM roles that you can associate is subject to a quota. For more information, go to `Quotas and limits <https://docs.aws.amazon.com/redshift/latest/mgmt/amazon-redshift-limits.html>`_ in the *Amazon Redshift Cluster Management Guide* .
        :param kms_key_id: The AWS Key Management Service (KMS) key ID of the encryption key that you want to use to encrypt data in the cluster.
        :param logging_properties: Specifies logging information, such as queries and connection attempts, for the specified Amazon Redshift cluster.
        :param maintenance_track_name: An optional parameter for the name of the maintenance track for the cluster. If you don't provide a maintenance track name, the cluster is assigned to the ``current`` track.
        :param manage_master_password: If ``true`` , Amazon Redshift uses AWS Secrets Manager to manage this cluster's admin credentials. You can't use ``MasterUserPassword`` if ``ManageMasterPassword`` is true. If ``ManageMasterPassword`` is false or not set, Amazon Redshift uses ``MasterUserPassword`` for the admin user account's password.
        :param manual_snapshot_retention_period: The default number of days to retain a manual snapshot. If the value is -1, the snapshot is retained indefinitely. This setting doesn't change the retention period of existing snapshots. The value must be either -1 or an integer between 1 and 3,653.
        :param master_password_secret_kms_key_id: The ID of the AWS Key Management Service (KMS) key used to encrypt and store the cluster's admin credentials secret. You can only use this parameter if ``ManageMasterPassword`` is true.
        :param master_username: The user name associated with the admin user account for the cluster that is being created. Constraints: - Must be 1 - 128 alphanumeric characters or hyphens. The user name can't be ``PUBLIC`` . - Must contain only lowercase letters, numbers, underscore, plus sign, period (dot), at symbol (@), or hyphen. - The first character must be a letter. - Must not contain a colon (:) or a slash (/). - Cannot be a reserved word. A list of reserved words can be found in `Reserved Words <https://docs.aws.amazon.com/redshift/latest/dg/r_pg_keywords.html>`_ in the Amazon Redshift Database Developer Guide.
        :param master_user_password: The password associated with the admin user account for the cluster that is being created. You can't use ``MasterUserPassword`` if ``ManageMasterPassword`` is ``true`` . Constraints: - Must be between 8 and 64 characters in length. - Must contain at least one uppercase letter. - Must contain at least one lowercase letter. - Must contain one number. - Can be any printable ASCII character (ASCII code 33-126) except ``'`` (single quote), ``"`` (double quote), ``\\`` , ``/`` , or ``@`` .
        :param multi_az: A boolean indicating whether Amazon Redshift should deploy the cluster in two Availability Zones. The default is false.
        :param namespace_resource_policy: The policy that is attached to a resource.
        :param node_type: The node type to be provisioned for the cluster. For information about node types, go to `Working with Clusters <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#how-many-nodes>`_ in the *Amazon Redshift Cluster Management Guide* . Valid Values: ``dc2.large`` | ``dc2.8xlarge`` | ``ra3.large`` | ``ra3.xlplus`` | ``ra3.4xlarge`` | ``ra3.16xlarge``
        :param number_of_nodes: The number of compute nodes in the cluster. This parameter is required when the *ClusterType* parameter is specified as ``multi-node`` . For information about determining how many nodes you need, go to `Working with Clusters <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#how-many-nodes>`_ in the *Amazon Redshift Cluster Management Guide* . If you don't specify this parameter, you get a single-node cluster. When requesting a multi-node cluster, you must specify the number of nodes that you want in the cluster. Default: ``1`` Constraints: Value must be at least 1 and no more than 100.
        :param owner_account: The AWS account used to create or copy the snapshot. Required if you are restoring a snapshot you do not own, optional if you own the snapshot.
        :param port: The port number on which the cluster accepts incoming connections. The cluster is accessible only via the JDBC and ODBC connection strings. Part of the connection string requires the port on which the cluster will listen for incoming connections. Default: ``5439`` Valid Values: - For clusters with ra3 nodes - Select a port within the ranges ``5431-5455`` or ``8191-8215`` . (If you have an existing cluster with ra3 nodes, it isn't required that you change the port to these ranges.) - For clusters with dc2 nodes - Select a port within the range ``1150-65535`` .
        :param preferred_maintenance_window: The weekly time range (in UTC) during which automated cluster maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Default: A 30-minute window selected at random from an 8-hour block of time per region, occurring on a random day of the week. For more information about the time blocks for each region, see `Maintenance Windows <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#rs-maintenance-windows>`_ in Amazon Redshift Cluster Management Guide. Valid Days: Mon | Tue | Wed | Thu | Fri | Sat | Sun Constraints: Minimum 30-minute window.
        :param publicly_accessible: If ``true`` , the cluster can be accessed from a public network. Default: false
        :param resource_action: The Amazon Redshift operation to be performed. Supported operations are ``pause-cluster`` , ``resume-cluster`` , and ``failover-primary-compute`` .
        :param revision_target: Describes a ``RevisionTarget`` object.
        :param rotate_encryption_key: Rotates the encryption keys for a cluster.
        :param snapshot_cluster_identifier: The name of the cluster the source snapshot was created from. This parameter is required if your user or role has a policy containing a snapshot resource element that specifies anything other than * for the cluster name.
        :param snapshot_copy_grant_name: The name of the snapshot copy grant.
        :param snapshot_copy_manual: Indicates whether to apply the snapshot retention period to newly copied manual snapshots instead of automated snapshots.
        :param snapshot_copy_retention_period: The number of days to retain automated snapshots in the destination AWS Region after they are copied from the source AWS Region . By default, this only changes the retention period of copied automated snapshots. If you decrease the retention period for automated snapshots that are copied to a destination AWS Region , Amazon Redshift deletes any existing automated snapshots that were copied to the destination AWS Region and that fall outside of the new retention period. Constraints: Must be at least 1 and no more than 35 for automated snapshots. If you specify the ``manual`` option, only newly copied manual snapshots will have the new retention period. If you specify the value of -1 newly copied manual snapshots are retained indefinitely. Constraints: The number of days must be either -1 or an integer between 1 and 3,653 for manual snapshots.
        :param snapshot_identifier: The name of the snapshot from which to create the new cluster. This parameter isn't case sensitive. You must specify this parameter or ``snapshotArn`` , but not both. Example: ``my-snapshot-id``
        :param tags: A list of tag instances.
        :param vpc_security_group_ids: A list of Virtual Private Cloud (VPC) security groups to be associated with the cluster. Default: The default VPC security group is associated with the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
            
            # namespace_resource_policy: Any
            
            cfn_cluster_mixin_props = redshift_mixins.CfnClusterMixinProps(
                allow_version_upgrade=False,
                aqua_configuration_status="aquaConfigurationStatus",
                automated_snapshot_retention_period=123,
                availability_zone="availabilityZone",
                availability_zone_relocation=False,
                availability_zone_relocation_status="availabilityZoneRelocationStatus",
                classic=False,
                cluster_identifier="clusterIdentifier",
                cluster_parameter_group_name="clusterParameterGroupName",
                cluster_security_groups=["clusterSecurityGroups"],
                cluster_subnet_group_name="clusterSubnetGroupName",
                cluster_type="clusterType",
                cluster_version="clusterVersion",
                db_name="dbName",
                defer_maintenance=False,
                defer_maintenance_duration=123,
                defer_maintenance_end_time="deferMaintenanceEndTime",
                defer_maintenance_start_time="deferMaintenanceStartTime",
                destination_region="destinationRegion",
                elastic_ip="elasticIp",
                encrypted=False,
                endpoint=redshift_mixins.CfnClusterPropsMixin.EndpointProperty(
                    address="address",
                    port="port"
                ),
                enhanced_vpc_routing=False,
                hsm_client_certificate_identifier="hsmClientCertificateIdentifier",
                hsm_configuration_identifier="hsmConfigurationIdentifier",
                iam_roles=["iamRoles"],
                kms_key_id="kmsKeyId",
                logging_properties=redshift_mixins.CfnClusterPropsMixin.LoggingPropertiesProperty(
                    bucket_name="bucketName",
                    log_destination_type="logDestinationType",
                    log_exports=["logExports"],
                    s3_key_prefix="s3KeyPrefix"
                ),
                maintenance_track_name="maintenanceTrackName",
                manage_master_password=False,
                manual_snapshot_retention_period=123,
                master_password_secret_kms_key_id="masterPasswordSecretKmsKeyId",
                master_username="masterUsername",
                master_user_password="masterUserPassword",
                multi_az=False,
                namespace_resource_policy=namespace_resource_policy,
                node_type="nodeType",
                number_of_nodes=123,
                owner_account="ownerAccount",
                port=123,
                preferred_maintenance_window="preferredMaintenanceWindow",
                publicly_accessible=False,
                resource_action="resourceAction",
                revision_target="revisionTarget",
                rotate_encryption_key=False,
                snapshot_cluster_identifier="snapshotClusterIdentifier",
                snapshot_copy_grant_name="snapshotCopyGrantName",
                snapshot_copy_manual=False,
                snapshot_copy_retention_period=123,
                snapshot_identifier="snapshotIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_security_group_ids=["vpcSecurityGroupIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa8e028d7fa71d8b68bae29f2c14a38830e7eae95dc3fc8e4a099f833447051)
            check_type(argname="argument allow_version_upgrade", value=allow_version_upgrade, expected_type=type_hints["allow_version_upgrade"])
            check_type(argname="argument aqua_configuration_status", value=aqua_configuration_status, expected_type=type_hints["aqua_configuration_status"])
            check_type(argname="argument automated_snapshot_retention_period", value=automated_snapshot_retention_period, expected_type=type_hints["automated_snapshot_retention_period"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument availability_zone_relocation", value=availability_zone_relocation, expected_type=type_hints["availability_zone_relocation"])
            check_type(argname="argument availability_zone_relocation_status", value=availability_zone_relocation_status, expected_type=type_hints["availability_zone_relocation_status"])
            check_type(argname="argument classic", value=classic, expected_type=type_hints["classic"])
            check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
            check_type(argname="argument cluster_parameter_group_name", value=cluster_parameter_group_name, expected_type=type_hints["cluster_parameter_group_name"])
            check_type(argname="argument cluster_security_groups", value=cluster_security_groups, expected_type=type_hints["cluster_security_groups"])
            check_type(argname="argument cluster_subnet_group_name", value=cluster_subnet_group_name, expected_type=type_hints["cluster_subnet_group_name"])
            check_type(argname="argument cluster_type", value=cluster_type, expected_type=type_hints["cluster_type"])
            check_type(argname="argument cluster_version", value=cluster_version, expected_type=type_hints["cluster_version"])
            check_type(argname="argument db_name", value=db_name, expected_type=type_hints["db_name"])
            check_type(argname="argument defer_maintenance", value=defer_maintenance, expected_type=type_hints["defer_maintenance"])
            check_type(argname="argument defer_maintenance_duration", value=defer_maintenance_duration, expected_type=type_hints["defer_maintenance_duration"])
            check_type(argname="argument defer_maintenance_end_time", value=defer_maintenance_end_time, expected_type=type_hints["defer_maintenance_end_time"])
            check_type(argname="argument defer_maintenance_start_time", value=defer_maintenance_start_time, expected_type=type_hints["defer_maintenance_start_time"])
            check_type(argname="argument destination_region", value=destination_region, expected_type=type_hints["destination_region"])
            check_type(argname="argument elastic_ip", value=elastic_ip, expected_type=type_hints["elastic_ip"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument enhanced_vpc_routing", value=enhanced_vpc_routing, expected_type=type_hints["enhanced_vpc_routing"])
            check_type(argname="argument hsm_client_certificate_identifier", value=hsm_client_certificate_identifier, expected_type=type_hints["hsm_client_certificate_identifier"])
            check_type(argname="argument hsm_configuration_identifier", value=hsm_configuration_identifier, expected_type=type_hints["hsm_configuration_identifier"])
            check_type(argname="argument iam_roles", value=iam_roles, expected_type=type_hints["iam_roles"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument logging_properties", value=logging_properties, expected_type=type_hints["logging_properties"])
            check_type(argname="argument maintenance_track_name", value=maintenance_track_name, expected_type=type_hints["maintenance_track_name"])
            check_type(argname="argument manage_master_password", value=manage_master_password, expected_type=type_hints["manage_master_password"])
            check_type(argname="argument manual_snapshot_retention_period", value=manual_snapshot_retention_period, expected_type=type_hints["manual_snapshot_retention_period"])
            check_type(argname="argument master_password_secret_kms_key_id", value=master_password_secret_kms_key_id, expected_type=type_hints["master_password_secret_kms_key_id"])
            check_type(argname="argument master_username", value=master_username, expected_type=type_hints["master_username"])
            check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
            check_type(argname="argument multi_az", value=multi_az, expected_type=type_hints["multi_az"])
            check_type(argname="argument namespace_resource_policy", value=namespace_resource_policy, expected_type=type_hints["namespace_resource_policy"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument number_of_nodes", value=number_of_nodes, expected_type=type_hints["number_of_nodes"])
            check_type(argname="argument owner_account", value=owner_account, expected_type=type_hints["owner_account"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument resource_action", value=resource_action, expected_type=type_hints["resource_action"])
            check_type(argname="argument revision_target", value=revision_target, expected_type=type_hints["revision_target"])
            check_type(argname="argument rotate_encryption_key", value=rotate_encryption_key, expected_type=type_hints["rotate_encryption_key"])
            check_type(argname="argument snapshot_cluster_identifier", value=snapshot_cluster_identifier, expected_type=type_hints["snapshot_cluster_identifier"])
            check_type(argname="argument snapshot_copy_grant_name", value=snapshot_copy_grant_name, expected_type=type_hints["snapshot_copy_grant_name"])
            check_type(argname="argument snapshot_copy_manual", value=snapshot_copy_manual, expected_type=type_hints["snapshot_copy_manual"])
            check_type(argname="argument snapshot_copy_retention_period", value=snapshot_copy_retention_period, expected_type=type_hints["snapshot_copy_retention_period"])
            check_type(argname="argument snapshot_identifier", value=snapshot_identifier, expected_type=type_hints["snapshot_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_version_upgrade is not None:
            self._values["allow_version_upgrade"] = allow_version_upgrade
        if aqua_configuration_status is not None:
            self._values["aqua_configuration_status"] = aqua_configuration_status
        if automated_snapshot_retention_period is not None:
            self._values["automated_snapshot_retention_period"] = automated_snapshot_retention_period
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if availability_zone_relocation is not None:
            self._values["availability_zone_relocation"] = availability_zone_relocation
        if availability_zone_relocation_status is not None:
            self._values["availability_zone_relocation_status"] = availability_zone_relocation_status
        if classic is not None:
            self._values["classic"] = classic
        if cluster_identifier is not None:
            self._values["cluster_identifier"] = cluster_identifier
        if cluster_parameter_group_name is not None:
            self._values["cluster_parameter_group_name"] = cluster_parameter_group_name
        if cluster_security_groups is not None:
            self._values["cluster_security_groups"] = cluster_security_groups
        if cluster_subnet_group_name is not None:
            self._values["cluster_subnet_group_name"] = cluster_subnet_group_name
        if cluster_type is not None:
            self._values["cluster_type"] = cluster_type
        if cluster_version is not None:
            self._values["cluster_version"] = cluster_version
        if db_name is not None:
            self._values["db_name"] = db_name
        if defer_maintenance is not None:
            self._values["defer_maintenance"] = defer_maintenance
        if defer_maintenance_duration is not None:
            self._values["defer_maintenance_duration"] = defer_maintenance_duration
        if defer_maintenance_end_time is not None:
            self._values["defer_maintenance_end_time"] = defer_maintenance_end_time
        if defer_maintenance_start_time is not None:
            self._values["defer_maintenance_start_time"] = defer_maintenance_start_time
        if destination_region is not None:
            self._values["destination_region"] = destination_region
        if elastic_ip is not None:
            self._values["elastic_ip"] = elastic_ip
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if enhanced_vpc_routing is not None:
            self._values["enhanced_vpc_routing"] = enhanced_vpc_routing
        if hsm_client_certificate_identifier is not None:
            self._values["hsm_client_certificate_identifier"] = hsm_client_certificate_identifier
        if hsm_configuration_identifier is not None:
            self._values["hsm_configuration_identifier"] = hsm_configuration_identifier
        if iam_roles is not None:
            self._values["iam_roles"] = iam_roles
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if logging_properties is not None:
            self._values["logging_properties"] = logging_properties
        if maintenance_track_name is not None:
            self._values["maintenance_track_name"] = maintenance_track_name
        if manage_master_password is not None:
            self._values["manage_master_password"] = manage_master_password
        if manual_snapshot_retention_period is not None:
            self._values["manual_snapshot_retention_period"] = manual_snapshot_retention_period
        if master_password_secret_kms_key_id is not None:
            self._values["master_password_secret_kms_key_id"] = master_password_secret_kms_key_id
        if master_username is not None:
            self._values["master_username"] = master_username
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if namespace_resource_policy is not None:
            self._values["namespace_resource_policy"] = namespace_resource_policy
        if node_type is not None:
            self._values["node_type"] = node_type
        if number_of_nodes is not None:
            self._values["number_of_nodes"] = number_of_nodes
        if owner_account is not None:
            self._values["owner_account"] = owner_account
        if port is not None:
            self._values["port"] = port
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if resource_action is not None:
            self._values["resource_action"] = resource_action
        if revision_target is not None:
            self._values["revision_target"] = revision_target
        if rotate_encryption_key is not None:
            self._values["rotate_encryption_key"] = rotate_encryption_key
        if snapshot_cluster_identifier is not None:
            self._values["snapshot_cluster_identifier"] = snapshot_cluster_identifier
        if snapshot_copy_grant_name is not None:
            self._values["snapshot_copy_grant_name"] = snapshot_copy_grant_name
        if snapshot_copy_manual is not None:
            self._values["snapshot_copy_manual"] = snapshot_copy_manual
        if snapshot_copy_retention_period is not None:
            self._values["snapshot_copy_retention_period"] = snapshot_copy_retention_period
        if snapshot_identifier is not None:
            self._values["snapshot_identifier"] = snapshot_identifier
        if tags is not None:
            self._values["tags"] = tags
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def allow_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If ``true`` , major version upgrades can be applied during the maintenance window to the Amazon Redshift engine that is running on the cluster.

        When a new major version of the Amazon Redshift engine is released, you can request that the service automatically apply upgrades during the maintenance window to the Amazon Redshift engine that is running on your cluster.

        Default: ``true``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-allowversionupgrade
        '''
        result = self._values.get("allow_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def aqua_configuration_status(self) -> typing.Optional[builtins.str]:
        '''This parameter is retired.

        It does not set the AQUA configuration status. Amazon Redshift automatically determines whether to use AQUA (Advanced Query Accelerator).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-aquaconfigurationstatus
        '''
        result = self._values.get("aqua_configuration_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automated_snapshot_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days that automated snapshots are retained.

        If the value is 0, automated snapshots are disabled. Even if automated snapshots are disabled, you can still create manual snapshots when you want with `CreateClusterSnapshot <https://docs.aws.amazon.com/redshift/latest/APIReference/API_CreateClusterSnapshot.html>`_ in the *Amazon Redshift API Reference* .

        Default: ``1``

        Constraints: Must be a value from 0 to 35.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-automatedsnapshotretentionperiod
        '''
        result = self._values.get("automated_snapshot_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The EC2 Availability Zone (AZ) in which you want Amazon Redshift to provision the cluster.

        For example, if you have several EC2 instances running in a specific Availability Zone, then you might want the cluster to be provisioned in the same zone in order to decrease network latency.

        Default: A random, system-chosen Availability Zone in the region that is specified by the endpoint.

        Example: ``us-east-2d``

        Constraint: The specified Availability Zone must be in the same region as the current endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def availability_zone_relocation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The option to enable relocation for an Amazon Redshift cluster between Availability Zones after the cluster is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-availabilityzonerelocation
        '''
        result = self._values.get("availability_zone_relocation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def availability_zone_relocation_status(self) -> typing.Optional[builtins.str]:
        '''Describes the status of the Availability Zone relocation operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-availabilityzonerelocationstatus
        '''
        result = self._values.get("availability_zone_relocation_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def classic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A boolean value indicating whether the resize operation is using the classic resize process.

        If you don't provide this parameter or set the value to ``false`` , the resize type is elastic.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-classic
        '''
        result = self._values.get("classic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the cluster.

        You use this identifier to refer to the cluster for any subsequent cluster operations such as deleting or modifying. The identifier also appears in the Amazon Redshift console.

        Constraints:

        - Must contain from 1 to 63 alphanumeric characters or hyphens.
        - Alphabetic characters must be lowercase.
        - First character must be a letter.
        - Cannot end with a hyphen or contain two consecutive hyphens.
        - Must be unique for all clusters within an AWS account .

        Example: ``myexamplecluster``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusteridentifier
        '''
        result = self._values.get("cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group to be associated with this cluster.

        Default: The default Amazon Redshift cluster parameter group. For information about the default parameter group, go to `Working with Amazon Redshift Parameter Groups <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html>`_

        Constraints:

        - Must be 1 to 255 alphanumeric characters or hyphens.
        - First character must be a letter.
        - Cannot end with a hyphen or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusterparametergroupname
        '''
        result = self._values.get("cluster_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security groups to be associated with this cluster.

        Default: The default cluster security group for Amazon Redshift.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustersecuritygroups
        '''
        result = self._values.get("cluster_security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cluster_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of a cluster subnet group to be associated with this cluster.

        If this parameter is not provided the resulting cluster will be deployed outside virtual private cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustersubnetgroupname
        '''
        result = self._values.get("cluster_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_type(self) -> typing.Optional[builtins.str]:
        '''The type of the cluster. When cluster type is specified as.

        - ``single-node`` , the *NumberOfNodes* parameter is not required.
        - ``multi-node`` , the *NumberOfNodes* parameter is required.

        Valid Values: ``multi-node`` | ``single-node``

        Default: ``multi-node``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustertype
        '''
        result = self._values.get("cluster_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_version(self) -> typing.Optional[builtins.str]:
        '''The version of the Amazon Redshift engine software that you want to deploy on the cluster.

        The version selected runs on all the nodes in the cluster.

        Constraints: Only version 1.0 is currently available.

        Example: ``1.0``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusterversion
        '''
        result = self._values.get("cluster_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_name(self) -> typing.Optional[builtins.str]:
        '''The name of the first database to be created when the cluster is created.

        To create additional databases after the cluster is created, connect to the cluster with a SQL client and use SQL commands to create a database. For more information, go to `Create a Database <https://docs.aws.amazon.com/redshift/latest/dg/t_creating_database.html>`_ in the Amazon Redshift Database Developer Guide.

        Default: ``dev``

        Constraints:

        - Must contain 1 to 64 alphanumeric characters.
        - Must contain only lowercase letters.
        - Cannot be a word that is reserved by the service. A list of reserved words can be found in `Reserved Words <https://docs.aws.amazon.com/redshift/latest/dg/r_pg_keywords.html>`_ in the Amazon Redshift Database Developer Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-dbname
        '''
        result = self._values.get("db_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def defer_maintenance(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean indicating whether to enable the deferred maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-defermaintenance
        '''
        result = self._values.get("defer_maintenance")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def defer_maintenance_duration(self) -> typing.Optional[jsii.Number]:
        '''An integer indicating the duration of the maintenance window in days.

        If you specify a duration, you can't specify an end time. The duration must be 45 days or less.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-defermaintenanceduration
        '''
        result = self._values.get("defer_maintenance_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def defer_maintenance_end_time(self) -> typing.Optional[builtins.str]:
        '''A timestamp for the end of the time period when we defer maintenance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-defermaintenanceendtime
        '''
        result = self._values.get("defer_maintenance_end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def defer_maintenance_start_time(self) -> typing.Optional[builtins.str]:
        '''A timestamp indicating the start time for the deferred maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-defermaintenancestarttime
        '''
        result = self._values.get("defer_maintenance_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_region(self) -> typing.Optional[builtins.str]:
        '''The destination region that snapshots are automatically copied to when cross-region snapshot copy is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-destinationregion
        '''
        result = self._values.get("destination_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elastic_ip(self) -> typing.Optional[builtins.str]:
        '''The Elastic IP (EIP) address for the cluster.

        Constraints: The cluster must be provisioned in EC2-VPC and publicly-accessible through an Internet gateway. Don't specify the Elastic IP address for a publicly accessible cluster with availability zone relocation turned on. For more information about provisioning clusters in EC2-VPC, go to `Supported Platforms to Launch Your Cluster <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#cluster-platforms>`_ in the Amazon Redshift Cluster Management Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-elasticip
        '''
        result = self._values.get("elastic_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If ``true`` , the data in the cluster is encrypted at rest.

        If you set the value on this parameter to ``false`` , the request will fail.

        Default: true

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-encrypted
        '''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EndpointProperty"]]:
        '''The connection endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-endpoint
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EndpointProperty"]], result)

    @builtins.property
    def enhanced_vpc_routing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''An option that specifies whether to create the cluster with enhanced VPC routing enabled.

        To create a cluster that uses enhanced VPC routing, the cluster must be in a VPC. For more information, see `Enhanced VPC Routing <https://docs.aws.amazon.com/redshift/latest/mgmt/enhanced-vpc-routing.html>`_ in the Amazon Redshift Cluster Management Guide.

        If this option is ``true`` , enhanced VPC routing is enabled.

        Default: false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-enhancedvpcrouting
        '''
        result = self._values.get("enhanced_vpc_routing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def hsm_client_certificate_identifier(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the HSM client certificate the Amazon Redshift cluster uses to retrieve the data encryption keys stored in an HSM.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-hsmclientcertificateidentifier
        '''
        result = self._values.get("hsm_client_certificate_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hsm_configuration_identifier(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the HSM configuration that contains the information the Amazon Redshift cluster can use to retrieve and store keys in an HSM.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-hsmconfigurationidentifier
        '''
        result = self._values.get("hsm_configuration_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of AWS Identity and Access Management (IAM) roles that can be used by the cluster to access other AWS services.

        You must supply the IAM roles in their Amazon Resource Name (ARN) format.

        The maximum number of IAM roles that you can associate is subject to a quota. For more information, go to `Quotas and limits <https://docs.aws.amazon.com/redshift/latest/mgmt/amazon-redshift-limits.html>`_ in the *Amazon Redshift Cluster Management Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-iamroles
        '''
        result = self._values.get("iam_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS Key Management Service (KMS) key ID of the encryption key that you want to use to encrypt data in the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.LoggingPropertiesProperty"]]:
        '''Specifies logging information, such as queries and connection attempts, for the specified Amazon Redshift cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-loggingproperties
        '''
        result = self._values.get("logging_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.LoggingPropertiesProperty"]], result)

    @builtins.property
    def maintenance_track_name(self) -> typing.Optional[builtins.str]:
        '''An optional parameter for the name of the maintenance track for the cluster.

        If you don't provide a maintenance track name, the cluster is assigned to the ``current`` track.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-maintenancetrackname
        '''
        result = self._values.get("maintenance_track_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manage_master_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If ``true`` , Amazon Redshift uses AWS Secrets Manager to manage this cluster's admin credentials.

        You can't use ``MasterUserPassword`` if ``ManageMasterPassword`` is true. If ``ManageMasterPassword`` is false or not set, Amazon Redshift uses ``MasterUserPassword`` for the admin user account's password.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-managemasterpassword
        '''
        result = self._values.get("manage_master_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def manual_snapshot_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The default number of days to retain a manual snapshot.

        If the value is -1, the snapshot is retained indefinitely. This setting doesn't change the retention period of existing snapshots.

        The value must be either -1 or an integer between 1 and 3,653.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-manualsnapshotretentionperiod
        '''
        result = self._values.get("manual_snapshot_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def master_password_secret_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS Key Management Service (KMS) key used to encrypt and store the cluster's admin credentials secret.

        You can only use this parameter if ``ManageMasterPassword`` is true.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masterpasswordsecretkmskeyid
        '''
        result = self._values.get("master_password_secret_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_username(self) -> typing.Optional[builtins.str]:
        '''The user name associated with the admin user account for the cluster that is being created.

        Constraints:

        - Must be 1 - 128 alphanumeric characters or hyphens. The user name can't be ``PUBLIC`` .
        - Must contain only lowercase letters, numbers, underscore, plus sign, period (dot), at symbol (@), or hyphen.
        - The first character must be a letter.
        - Must not contain a colon (:) or a slash (/).
        - Cannot be a reserved word. A list of reserved words can be found in `Reserved Words <https://docs.aws.amazon.com/redshift/latest/dg/r_pg_keywords.html>`_ in the Amazon Redshift Database Developer Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masterusername
        '''
        result = self._values.get("master_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_password(self) -> typing.Optional[builtins.str]:
        '''The password associated with the admin user account for the cluster that is being created.

        You can't use ``MasterUserPassword`` if ``ManageMasterPassword`` is ``true`` .

        Constraints:

        - Must be between 8 and 64 characters in length.
        - Must contain at least one uppercase letter.
        - Must contain at least one lowercase letter.
        - Must contain one number.
        - Can be any printable ASCII character (ASCII code 33-126) except ``'`` (single quote), ``"`` (double quote), ``\\`` , ``/`` , or ``@`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masteruserpassword
        '''
        result = self._values.get("master_user_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_az(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A boolean indicating whether Amazon Redshift should deploy the cluster in two Availability Zones.

        The default is false.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-multiaz
        '''
        result = self._values.get("multi_az")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def namespace_resource_policy(self) -> typing.Any:
        '''The policy that is attached to a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-namespaceresourcepolicy
        '''
        result = self._values.get("namespace_resource_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''The node type to be provisioned for the cluster.

        For information about node types, go to `Working with Clusters <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#how-many-nodes>`_ in the *Amazon Redshift Cluster Management Guide* .

        Valid Values: ``dc2.large`` | ``dc2.8xlarge`` | ``ra3.large`` | ``ra3.xlplus`` | ``ra3.4xlarge`` | ``ra3.16xlarge``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-nodetype
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        '''The number of compute nodes in the cluster.

        This parameter is required when the *ClusterType* parameter is specified as ``multi-node`` .

        For information about determining how many nodes you need, go to `Working with Clusters <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#how-many-nodes>`_ in the *Amazon Redshift Cluster Management Guide* .

        If you don't specify this parameter, you get a single-node cluster. When requesting a multi-node cluster, you must specify the number of nodes that you want in the cluster.

        Default: ``1``

        Constraints: Value must be at least 1 and no more than 100.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-numberofnodes
        '''
        result = self._values.get("number_of_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def owner_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account used to create or copy the snapshot.

        Required if you are restoring a snapshot you do not own, optional if you own the snapshot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-owneraccount
        '''
        result = self._values.get("owner_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number on which the cluster accepts incoming connections.

        The cluster is accessible only via the JDBC and ODBC connection strings. Part of the connection string requires the port on which the cluster will listen for incoming connections.

        Default: ``5439``

        Valid Values:

        - For clusters with ra3 nodes - Select a port within the ranges ``5431-5455`` or ``8191-8215`` . (If you have an existing cluster with ra3 nodes, it isn't required that you change the port to these ranges.)
        - For clusters with dc2 nodes - Select a port within the range ``1150-65535`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range (in UTC) during which automated cluster maintenance can occur.

        Format: ``ddd:hh24:mi-ddd:hh24:mi``

        Default: A 30-minute window selected at random from an 8-hour block of time per region, occurring on a random day of the week. For more information about the time blocks for each region, see `Maintenance Windows <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#rs-maintenance-windows>`_ in Amazon Redshift Cluster Management Guide.

        Valid Days: Mon | Tue | Wed | Thu | Fri | Sat | Sun

        Constraints: Minimum 30-minute window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If ``true`` , the cluster can be accessed from a public network.

        Default: false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def resource_action(self) -> typing.Optional[builtins.str]:
        '''The Amazon Redshift operation to be performed.

        Supported operations are ``pause-cluster`` , ``resume-cluster`` , and ``failover-primary-compute`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-resourceaction
        '''
        result = self._values.get("resource_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def revision_target(self) -> typing.Optional[builtins.str]:
        '''Describes a ``RevisionTarget`` object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-revisiontarget
        '''
        result = self._values.get("revision_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotate_encryption_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Rotates the encryption keys for a cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-rotateencryptionkey
        '''
        result = self._values.get("rotate_encryption_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def snapshot_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster the source snapshot was created from.

        This parameter is required if your user or role has a policy containing a snapshot resource element that specifies anything other than * for the cluster name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotclusteridentifier
        '''
        result = self._values.get("snapshot_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_copy_grant_name(self) -> typing.Optional[builtins.str]:
        '''The name of the snapshot copy grant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotcopygrantname
        '''
        result = self._values.get("snapshot_copy_grant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_copy_manual(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether to apply the snapshot retention period to newly copied manual snapshots instead of automated snapshots.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotcopymanual
        '''
        result = self._values.get("snapshot_copy_manual")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def snapshot_copy_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain automated snapshots in the destination AWS Region after they are copied from the source AWS Region .

        By default, this only changes the retention period of copied automated snapshots.

        If you decrease the retention period for automated snapshots that are copied to a destination AWS Region , Amazon Redshift deletes any existing automated snapshots that were copied to the destination AWS Region and that fall outside of the new retention period.

        Constraints: Must be at least 1 and no more than 35 for automated snapshots.

        If you specify the ``manual`` option, only newly copied manual snapshots will have the new retention period.

        If you specify the value of -1 newly copied manual snapshots are retained indefinitely.

        Constraints: The number of days must be either -1 or an integer between 1 and 3,653 for manual snapshots.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotcopyretentionperiod
        '''
        result = self._values.get("snapshot_copy_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot_identifier(self) -> typing.Optional[builtins.str]:
        '''The name of the snapshot from which to create the new cluster.

        This parameter isn't case sensitive. You must specify this parameter or ``snapshotArn`` , but not both.

        Example: ``my-snapshot-id``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotidentifier
        '''
        result = self._values.get("snapshot_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tag instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Virtual Private Cloud (VPC) security groups to be associated with the cluster.

        Default: The default VPC security group is associated with the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterParameterGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "parameter_group_family": "parameterGroupFamily",
        "parameter_group_name": "parameterGroupName",
        "parameters": "parameters",
        "tags": "tags",
    },
)
class CfnClusterParameterGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        parameter_group_family: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterParameterGroupPropsMixin.ParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnClusterParameterGroupPropsMixin.

        :param description: The description of the parameter group.
        :param parameter_group_family: The name of the cluster parameter group family that this cluster parameter group is compatible with. You can create a custom parameter group and then associate your cluster with it. For more information, see `Amazon Redshift parameter groups <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html>`_ .
        :param parameter_group_name: The name of the cluster parameter group.
        :param parameters: An array of parameters to be modified. A maximum of 20 parameters can be modified in a single request. For each parameter to be modified, you must supply at least the parameter name and parameter value; other name-value pairs of the parameter are optional. For the workload management (WLM) configuration, you must supply all the name-value pairs in the wlm_json_configuration parameter.
        :param tags: The list of tags for the cluster parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
            
            cfn_cluster_parameter_group_mixin_props = redshift_mixins.CfnClusterParameterGroupMixinProps(
                description="description",
                parameter_group_family="parameterGroupFamily",
                parameter_group_name="parameterGroupName",
                parameters=[redshift_mixins.CfnClusterParameterGroupPropsMixin.ParameterProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f13ef7e4d0e278bbb66192a83e1e8f0a5d3024d44c43e1f97eff2ee5747fff)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameter_group_family", value=parameter_group_family, expected_type=type_hints["parameter_group_family"])
            check_type(argname="argument parameter_group_name", value=parameter_group_name, expected_type=type_hints["parameter_group_name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if parameter_group_family is not None:
            self._values["parameter_group_family"] = parameter_group_family
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group_family(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster parameter group family that this cluster parameter group is compatible with.

        You can create a custom parameter group and then associate your cluster with it. For more information, see `Amazon Redshift parameter groups <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parametergroupfamily
        '''
        result = self._values.get("parameter_group_family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterParameterGroupPropsMixin.ParameterProperty"]]]]:
        '''An array of parameters to be modified. A maximum of 20 parameters can be modified in a single request.

        For each parameter to be modified, you must supply at least the parameter name and parameter value; other name-value pairs of the parameter are optional.

        For the workload management (WLM) configuration, you must supply all the name-value pairs in the wlm_json_configuration parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterParameterGroupPropsMixin.ParameterProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of tags for the cluster parameter group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterParameterGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClusterParameterGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterParameterGroupPropsMixin",
):
    '''Describes a parameter group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html
    :cloudformationResource: AWS::Redshift::ClusterParameterGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
        
        cfn_cluster_parameter_group_props_mixin = redshift_mixins.CfnClusterParameterGroupPropsMixin(redshift_mixins.CfnClusterParameterGroupMixinProps(
            description="description",
            parameter_group_family="parameterGroupFamily",
            parameter_group_name="parameterGroupName",
            parameters=[redshift_mixins.CfnClusterParameterGroupPropsMixin.ParameterProperty(
                parameter_name="parameterName",
                parameter_value="parameterValue"
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
        props: typing.Union[CfnClusterParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Redshift::ClusterParameterGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2417dfb72b44e87be5648c0b8cc7d70e94a98127d135fa964536bc44aebea0a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7d830569fff9bf8aed45ea354252ab441fd89124c1632f4e228c8e782ce1c95)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fdec487c1d914bc3db8af8982aa559fb2750c2aaf10c45241f39783eb351320)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClusterParameterGroupMixinProps:
        return typing.cast(CfnClusterParameterGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterParameterGroupPropsMixin.ParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class ParameterProperty:
        def __init__(
            self,
            *,
            parameter_name: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a parameter in a cluster parameter group.

            :param parameter_name: The name of the parameter.
            :param parameter_value: The value of the parameter. If ``ParameterName`` is ``wlm_json_configuration`` , then the maximum size of ``ParameterValue`` is 8000 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-clusterparametergroup-parameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
                
                parameter_property = redshift_mixins.CfnClusterParameterGroupPropsMixin.ParameterProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b8c801500be5524730e9cdd68afeeb3119e87cacf4f8ef8da85aee6a2518d25)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''The name of the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-clusterparametergroup-parameter.html#cfn-redshift-clusterparametergroup-parameter-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''The value of the parameter.

            If ``ParameterName`` is ``wlm_json_configuration`` , then the maximum size of ``ParameterValue`` is 8000 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-clusterparametergroup-parameter.html#cfn-redshift-clusterparametergroup-parameter-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterPropsMixin",
):
    '''Specifies a cluster. A *cluster* is a fully managed data warehouse that consists of a set of compute nodes.

    To create a cluster in Virtual Private Cloud (VPC), you must provide a cluster subnet group name. The cluster subnet group identifies the subnets of your VPC that Amazon Redshift uses when creating the cluster. For more information about managing clusters, go to `Amazon Redshift Clusters <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html>`_ in the *Amazon Redshift Cluster Management Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html
    :cloudformationResource: AWS::Redshift::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
        
        # namespace_resource_policy: Any
        
        cfn_cluster_props_mixin = redshift_mixins.CfnClusterPropsMixin(redshift_mixins.CfnClusterMixinProps(
            allow_version_upgrade=False,
            aqua_configuration_status="aquaConfigurationStatus",
            automated_snapshot_retention_period=123,
            availability_zone="availabilityZone",
            availability_zone_relocation=False,
            availability_zone_relocation_status="availabilityZoneRelocationStatus",
            classic=False,
            cluster_identifier="clusterIdentifier",
            cluster_parameter_group_name="clusterParameterGroupName",
            cluster_security_groups=["clusterSecurityGroups"],
            cluster_subnet_group_name="clusterSubnetGroupName",
            cluster_type="clusterType",
            cluster_version="clusterVersion",
            db_name="dbName",
            defer_maintenance=False,
            defer_maintenance_duration=123,
            defer_maintenance_end_time="deferMaintenanceEndTime",
            defer_maintenance_start_time="deferMaintenanceStartTime",
            destination_region="destinationRegion",
            elastic_ip="elasticIp",
            encrypted=False,
            endpoint=redshift_mixins.CfnClusterPropsMixin.EndpointProperty(
                address="address",
                port="port"
            ),
            enhanced_vpc_routing=False,
            hsm_client_certificate_identifier="hsmClientCertificateIdentifier",
            hsm_configuration_identifier="hsmConfigurationIdentifier",
            iam_roles=["iamRoles"],
            kms_key_id="kmsKeyId",
            logging_properties=redshift_mixins.CfnClusterPropsMixin.LoggingPropertiesProperty(
                bucket_name="bucketName",
                log_destination_type="logDestinationType",
                log_exports=["logExports"],
                s3_key_prefix="s3KeyPrefix"
            ),
            maintenance_track_name="maintenanceTrackName",
            manage_master_password=False,
            manual_snapshot_retention_period=123,
            master_password_secret_kms_key_id="masterPasswordSecretKmsKeyId",
            master_username="masterUsername",
            master_user_password="masterUserPassword",
            multi_az=False,
            namespace_resource_policy=namespace_resource_policy,
            node_type="nodeType",
            number_of_nodes=123,
            owner_account="ownerAccount",
            port=123,
            preferred_maintenance_window="preferredMaintenanceWindow",
            publicly_accessible=False,
            resource_action="resourceAction",
            revision_target="revisionTarget",
            rotate_encryption_key=False,
            snapshot_cluster_identifier="snapshotClusterIdentifier",
            snapshot_copy_grant_name="snapshotCopyGrantName",
            snapshot_copy_manual=False,
            snapshot_copy_retention_period=123,
            snapshot_identifier="snapshotIdentifier",
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
        props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Redshift::Cluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c07df62de57fb6b54d2279775a164d33d89dc3302fb7f7f29e4c7d564bc7a69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d2ae00ae92a0f5817366f5b6a75b0704ecd417bac2910a2ed7db91e9de01f47)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e71cc02c785a4824f1684ec62150c26996594c30838428ffb3fde87675e157)
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
        jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterPropsMixin.EndpointProperty",
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
            '''Describes a connection endpoint.

            :param address: The DNS address of the cluster. This property is read only.
            :param port: The port that the database engine is listening on. This property is read only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-endpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
                
                endpoint_property = redshift_mixins.CfnClusterPropsMixin.EndpointProperty(
                    address="address",
                    port="port"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee91498db9a9e31dd3ba5dc79cf29b8a62b8eeb5639d4c5780d3f6731e4d567e)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The DNS address of the cluster.

            This property is read only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-endpoint.html#cfn-redshift-cluster-endpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The port that the database engine is listening on.

            This property is read only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-endpoint.html#cfn-redshift-cluster-endpoint-port
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
        jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterPropsMixin.LoggingPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "log_destination_type": "logDestinationType",
            "log_exports": "logExports",
            "s3_key_prefix": "s3KeyPrefix",
        },
    )
    class LoggingPropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            log_destination_type: typing.Optional[builtins.str] = None,
            log_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
            s3_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies logging information, such as queries and connection attempts, for the specified Amazon Redshift cluster.

            :param bucket_name: The name of an existing S3 bucket where the log files are to be stored. Constraints: - Must be in the same region as the cluster - The cluster must have read bucket and put object permissions
            :param log_destination_type: The log destination type. An enum with possible values of ``s3`` and ``cloudwatch`` .
            :param log_exports: The collection of exported log types. Possible values are ``connectionlog`` , ``useractivitylog`` , and ``userlog`` .
            :param s3_key_prefix: The prefix applied to the log file names. Valid characters are any letter from any language, any whitespace character, any numeric character, and the following characters: underscore ( ``_`` ), period ( ``.`` ), colon ( ``:`` ), slash ( ``/`` ), equal ( ``=`` ), plus ( ``+`` ), backslash ( ``\\`` ), hyphen ( ``-`` ), at symbol ( ``@`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
                
                logging_properties_property = redshift_mixins.CfnClusterPropsMixin.LoggingPropertiesProperty(
                    bucket_name="bucketName",
                    log_destination_type="logDestinationType",
                    log_exports=["logExports"],
                    s3_key_prefix="s3KeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3120b1dadd07379aa00e87c13d3ba2c2d5334bcb036dc458bef0d7685a2abc5)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument log_destination_type", value=log_destination_type, expected_type=type_hints["log_destination_type"])
                check_type(argname="argument log_exports", value=log_exports, expected_type=type_hints["log_exports"])
                check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if log_destination_type is not None:
                self._values["log_destination_type"] = log_destination_type
            if log_exports is not None:
                self._values["log_exports"] = log_exports
            if s3_key_prefix is not None:
                self._values["s3_key_prefix"] = s3_key_prefix

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of an existing S3 bucket where the log files are to be stored.

            Constraints:

            - Must be in the same region as the cluster
            - The cluster must have read bucket and put object permissions

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html#cfn-redshift-cluster-loggingproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_destination_type(self) -> typing.Optional[builtins.str]:
            '''The log destination type.

            An enum with possible values of ``s3`` and ``cloudwatch`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html#cfn-redshift-cluster-loggingproperties-logdestinationtype
            '''
            result = self._values.get("log_destination_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_exports(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The collection of exported log types.

            Possible values are ``connectionlog`` , ``useractivitylog`` , and ``userlog`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html#cfn-redshift-cluster-loggingproperties-logexports
            '''
            result = self._values.get("log_exports")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def s3_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix applied to the log file names.

            Valid characters are any letter from any language, any whitespace character, any numeric character, and the following characters: underscore ( ``_`` ), period ( ``.`` ), colon ( ``:`` ), slash ( ``/`` ), equal ( ``=`` ), plus ( ``+`` ), backslash ( ``\\`` ), hyphen ( ``-`` ), at symbol ( ``@`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html#cfn-redshift-cluster-loggingproperties-s3keyprefix
            '''
            result = self._values.get("s3_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterSecurityGroupIngressMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidrip": "cidrip",
        "cluster_security_group_name": "clusterSecurityGroupName",
        "ec2_security_group_name": "ec2SecurityGroupName",
        "ec2_security_group_owner_id": "ec2SecurityGroupOwnerId",
    },
)
class CfnClusterSecurityGroupIngressMixinProps:
    def __init__(
        self,
        *,
        cidrip: typing.Optional[builtins.str] = None,
        cluster_security_group_name: typing.Optional[builtins.str] = None,
        ec2_security_group_name: typing.Optional[builtins.str] = None,
        ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnClusterSecurityGroupIngressPropsMixin.

        :param cidrip: The IP range to be added the Amazon Redshift security group.
        :param cluster_security_group_name: The name of the security group to which the ingress rule is added.
        :param ec2_security_group_name: The EC2 security group to be added the Amazon Redshift security group.
        :param ec2_security_group_owner_id: The AWS account number of the owner of the security group specified by the *EC2SecurityGroupName* parameter. The AWS Access Key ID is not an acceptable value. Example: ``111122223333`` Conditional. If you specify the ``EC2SecurityGroupName`` property, you must specify this property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
            
            cfn_cluster_security_group_ingress_mixin_props = redshift_mixins.CfnClusterSecurityGroupIngressMixinProps(
                cidrip="cidrip",
                cluster_security_group_name="clusterSecurityGroupName",
                ec2_security_group_name="ec2SecurityGroupName",
                ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6d64f218de6e4f9ce4021cfff967f2db3845c97587b99c18d5ca529a6babb2)
            check_type(argname="argument cidrip", value=cidrip, expected_type=type_hints["cidrip"])
            check_type(argname="argument cluster_security_group_name", value=cluster_security_group_name, expected_type=type_hints["cluster_security_group_name"])
            check_type(argname="argument ec2_security_group_name", value=ec2_security_group_name, expected_type=type_hints["ec2_security_group_name"])
            check_type(argname="argument ec2_security_group_owner_id", value=ec2_security_group_owner_id, expected_type=type_hints["ec2_security_group_owner_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidrip is not None:
            self._values["cidrip"] = cidrip
        if cluster_security_group_name is not None:
            self._values["cluster_security_group_name"] = cluster_security_group_name
        if ec2_security_group_name is not None:
            self._values["ec2_security_group_name"] = ec2_security_group_name
        if ec2_security_group_owner_id is not None:
            self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

    @builtins.property
    def cidrip(self) -> typing.Optional[builtins.str]:
        '''The IP range to be added the Amazon Redshift security group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-cidrip
        '''
        result = self._values.get("cidrip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_security_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the security group to which the ingress rule is added.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-clustersecuritygroupname
        '''
        result = self._values.get("cluster_security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_security_group_name(self) -> typing.Optional[builtins.str]:
        '''The EC2 security group to be added the Amazon Redshift security group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-ec2securitygroupname
        '''
        result = self._values.get("ec2_security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_security_group_owner_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account number of the owner of the security group specified by the *EC2SecurityGroupName* parameter.

        The AWS Access Key ID is not an acceptable value.

        Example: ``111122223333``

        Conditional. If you specify the ``EC2SecurityGroupName`` property, you must specify this property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-ec2securitygroupownerid
        '''
        result = self._values.get("ec2_security_group_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterSecurityGroupIngressMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClusterSecurityGroupIngressPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterSecurityGroupIngressPropsMixin",
):
    '''Adds an inbound (ingress) rule to an Amazon Redshift security group.

    Depending on whether the application accessing your cluster is running on the Internet or an Amazon EC2 instance, you can authorize inbound access to either a Classless Interdomain Routing (CIDR)/Internet Protocol (IP) range or to an Amazon EC2 security group. You can add as many as 20 ingress rules to an Amazon Redshift security group.

    If you authorize access to an Amazon EC2 security group, specify *EC2SecurityGroupName* and *EC2SecurityGroupOwnerId* . The Amazon EC2 security group and Amazon Redshift cluster must be in the same AWS Region .

    If you authorize access to a CIDR/IP address range, specify *CIDRIP* . For an overview of CIDR blocks, see the Wikipedia article on `Classless Inter-Domain Routing <https://docs.aws.amazon.com/http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

    You must also associate the security group with a cluster so that clients running on these IP addresses or the EC2 instance are authorized to connect to the cluster. For information about managing security groups, go to `Working with Security Groups <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-security-groups.html>`_ in the *Amazon Redshift Cluster Management Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html
    :cloudformationResource: AWS::Redshift::ClusterSecurityGroupIngress
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
        
        cfn_cluster_security_group_ingress_props_mixin = redshift_mixins.CfnClusterSecurityGroupIngressPropsMixin(redshift_mixins.CfnClusterSecurityGroupIngressMixinProps(
            cidrip="cidrip",
            cluster_security_group_name="clusterSecurityGroupName",
            ec2_security_group_name="ec2SecurityGroupName",
            ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnClusterSecurityGroupIngressMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Redshift::ClusterSecurityGroupIngress``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dbc47cd9dd6b2c6a73fcaaa303654eada7093997216e3ecd9f53f7e4a78fc32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28f7c8ea00176ccd59c16ed63ea90e116b7956badb64c981adb4ef90b658a41a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b33fc169dc39499d51a02342b800bef25759767f66abfd41494da88cb0db547)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClusterSecurityGroupIngressMixinProps:
        return typing.cast(CfnClusterSecurityGroupIngressMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterSecurityGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "tags": "tags"},
)
class CfnClusterSecurityGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnClusterSecurityGroupPropsMixin.

        :param description: A description for the security group.
        :param tags: Specifies an arbitrary set of tags (key–value pairs) to associate with this security group. Use tags to manage your resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
            
            cfn_cluster_security_group_mixin_props = redshift_mixins.CfnClusterSecurityGroupMixinProps(
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9b2fef75b50ded26675e22991107ed4ba5e815bdb3f5d8ae7e19a2fe550f7b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the security group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html#cfn-redshift-clustersecuritygroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies an arbitrary set of tags (key–value pairs) to associate with this security group.

        Use tags to manage your resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html#cfn-redshift-clustersecuritygroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterSecurityGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClusterSecurityGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterSecurityGroupPropsMixin",
):
    '''Specifies a new Amazon Redshift security group. You use security groups to control access to non-VPC clusters.

    For information about managing security groups, go to `Amazon Redshift Cluster Security Groups <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-security-groups.html>`_ in the *Amazon Redshift Cluster Management Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html
    :cloudformationResource: AWS::Redshift::ClusterSecurityGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
        
        cfn_cluster_security_group_props_mixin = redshift_mixins.CfnClusterSecurityGroupPropsMixin(redshift_mixins.CfnClusterSecurityGroupMixinProps(
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
        props: typing.Union[CfnClusterSecurityGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Redshift::ClusterSecurityGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1e63c6fd9e6ebab90975718db01e978c87ce0254768bb52fe3113065a9dc61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60b91505218980e1ed4504ead8804d405265154af47e09cc76b95c2da1f292ae)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af6fd5f8c43bf48adefafa8f00cfbdb88a504a68d666a9220c3eaeb58b0368d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClusterSecurityGroupMixinProps:
        return typing.cast(CfnClusterSecurityGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterSubnetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnClusterSubnetGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnClusterSubnetGroupPropsMixin.

        :param description: A description for the subnet group.
        :param subnet_ids: An array of VPC subnet IDs. A maximum of 20 subnets can be modified in a single request.
        :param tags: Specifies an arbitrary set of tags (key–value pairs) to associate with this subnet group. Use tags to manage your resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
            
            cfn_cluster_subnet_group_mixin_props = redshift_mixins.CfnClusterSubnetGroupMixinProps(
                description="description",
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58576fcfc42d27c1e89545f3cccd02c8736732ab9b0f182b82b9c8130be5e090)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the subnet group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of VPC subnet IDs.

        A maximum of 20 subnets can be modified in a single request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies an arbitrary set of tags (key–value pairs) to associate with this subnet group.

        Use tags to manage your resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterSubnetGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClusterSubnetGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnClusterSubnetGroupPropsMixin",
):
    '''Specifies an Amazon Redshift subnet group.

    You must provide a list of one or more subnets in your existing Amazon Virtual Private Cloud ( Amazon VPC ) when creating Amazon Redshift subnet group.

    For information about subnet groups, go to `Amazon Redshift Cluster Subnet Groups <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-cluster-subnet-groups.html>`_ in the *Amazon Redshift Cluster Management Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html
    :cloudformationResource: AWS::Redshift::ClusterSubnetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
        
        cfn_cluster_subnet_group_props_mixin = redshift_mixins.CfnClusterSubnetGroupPropsMixin(redshift_mixins.CfnClusterSubnetGroupMixinProps(
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
        props: typing.Union[CfnClusterSubnetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Redshift::ClusterSubnetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc759bdd8df0bd9323cee5f2a72bd4a1105ce32b4f6a2f6f254a50d3ed71601d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2c28d5736d7ceae92ff3e036ab14ccd607ad6e3249599ee3efa08bb293565d3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efeb564689e69e290d2e63b55209e2bf46d48ea28d26f6e1ff1077bb7a435096)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClusterSubnetGroupMixinProps:
        return typing.cast(CfnClusterSubnetGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnEndpointAccessMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_identifier": "clusterIdentifier",
        "endpoint_name": "endpointName",
        "resource_owner": "resourceOwner",
        "subnet_group_name": "subnetGroupName",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnEndpointAccessMixinProps:
    def __init__(
        self,
        *,
        cluster_identifier: typing.Optional[builtins.str] = None,
        endpoint_name: typing.Optional[builtins.str] = None,
        resource_owner: typing.Optional[builtins.str] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnEndpointAccessPropsMixin.

        :param cluster_identifier: The cluster identifier of the cluster associated with the endpoint.
        :param endpoint_name: The name of the endpoint.
        :param resource_owner: The AWS account ID of the owner of the cluster.
        :param subnet_group_name: The subnet group name where Amazon Redshift chooses to deploy the endpoint.
        :param vpc_security_group_ids: The security group that defines the ports, protocols, and sources for inbound traffic that you are authorizing into your endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointaccess.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
            
            cfn_endpoint_access_mixin_props = redshift_mixins.CfnEndpointAccessMixinProps(
                cluster_identifier="clusterIdentifier",
                endpoint_name="endpointName",
                resource_owner="resourceOwner",
                subnet_group_name="subnetGroupName",
                vpc_security_group_ids=["vpcSecurityGroupIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf67ff620a0e40fedb01d14ea7660fd970e342b73032cec93f0c2ce2604aff29)
            check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
            check_type(argname="argument endpoint_name", value=endpoint_name, expected_type=type_hints["endpoint_name"])
            check_type(argname="argument resource_owner", value=resource_owner, expected_type=type_hints["resource_owner"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_identifier is not None:
            self._values["cluster_identifier"] = cluster_identifier
        if endpoint_name is not None:
            self._values["endpoint_name"] = endpoint_name
        if resource_owner is not None:
            self._values["resource_owner"] = resource_owner
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The cluster identifier of the cluster associated with the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointaccess.html#cfn-redshift-endpointaccess-clusteridentifier
        '''
        result = self._values.get("cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_name(self) -> typing.Optional[builtins.str]:
        '''The name of the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointaccess.html#cfn-redshift-endpointaccess-endpointname
        '''
        result = self._values.get("endpoint_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of the owner of the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointaccess.html#cfn-redshift-endpointaccess-resourceowner
        '''
        result = self._values.get("resource_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The subnet group name where Amazon Redshift chooses to deploy the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointaccess.html#cfn-redshift-endpointaccess-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The security group that defines the ports, protocols, and sources for inbound traffic that you are authorizing into your endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointaccess.html#cfn-redshift-endpointaccess-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEndpointAccessMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEndpointAccessPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnEndpointAccessPropsMixin",
):
    '''Creates a Redshift-managed VPC endpoint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointaccess.html
    :cloudformationResource: AWS::Redshift::EndpointAccess
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
        
        cfn_endpoint_access_props_mixin = redshift_mixins.CfnEndpointAccessPropsMixin(redshift_mixins.CfnEndpointAccessMixinProps(
            cluster_identifier="clusterIdentifier",
            endpoint_name="endpointName",
            resource_owner="resourceOwner",
            subnet_group_name="subnetGroupName",
            vpc_security_group_ids=["vpcSecurityGroupIds"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEndpointAccessMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Redshift::EndpointAccess``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6118db7bc34363910616e0602f53e3e7859b69fba49626d65d35bd64ef0811e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__287371f128f9b2bae6ead87947bac6f9921252a5cc9bc6816636d26d5822f1bf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42bf8911e26f71c374f40932b7eb7adabe8b338c3a1cc77344691724514bf028)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEndpointAccessMixinProps:
        return typing.cast(CfnEndpointAccessMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnEndpointAccessPropsMixin.NetworkInterfaceProperty",
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
            '''Describes a network interface.

            :param availability_zone: The Availability Zone.
            :param network_interface_id: The network interface identifier.
            :param private_ip_address: The IPv4 address of the network interface within the subnet.
            :param subnet_id: The subnet identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-networkinterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
                
                network_interface_property = redshift_mixins.CfnEndpointAccessPropsMixin.NetworkInterfaceProperty(
                    availability_zone="availabilityZone",
                    network_interface_id="networkInterfaceId",
                    private_ip_address="privateIpAddress",
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99daf49752f0bce1454c26923217847adec52a16fff88a518e5a1e5642a473ba)
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
            '''The Availability Zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-networkinterface.html#cfn-redshift-endpointaccess-networkinterface-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_interface_id(self) -> typing.Optional[builtins.str]:
            '''The network interface identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-networkinterface.html#cfn-redshift-endpointaccess-networkinterface-networkinterfaceid
            '''
            result = self._values.get("network_interface_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_ip_address(self) -> typing.Optional[builtins.str]:
            '''The IPv4 address of the network interface within the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-networkinterface.html#cfn-redshift-endpointaccess-networkinterface-privateipaddress
            '''
            result = self._values.get("private_ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''The subnet identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-networkinterface.html#cfn-redshift-endpointaccess-networkinterface-subnetid
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
        jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnEndpointAccessPropsMixin.VpcEndpointProperty",
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
            network_interfaces: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointAccessPropsMixin.NetworkInterfaceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            vpc_endpoint_id: typing.Optional[builtins.str] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connection endpoint for connecting to an Amazon Redshift cluster through the proxy.

            :param network_interfaces: One or more network interfaces of the endpoint. Also known as an interface endpoint.
            :param vpc_endpoint_id: The connection endpoint ID for connecting an Amazon Redshift cluster through the proxy.
            :param vpc_id: The VPC identifier that the endpoint is associated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-vpcendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
                
                vpc_endpoint_property = redshift_mixins.CfnEndpointAccessPropsMixin.VpcEndpointProperty(
                    network_interfaces=[redshift_mixins.CfnEndpointAccessPropsMixin.NetworkInterfaceProperty(
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
                type_hints = typing.get_type_hints(_typecheckingstub__c6f4ae568ec6d302ed4aab5aa576082815dd29c814356f32cb3c41778422a05e)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointAccessPropsMixin.NetworkInterfaceProperty"]]]]:
            '''One or more network interfaces of the endpoint.

            Also known as an interface endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-vpcendpoint.html#cfn-redshift-endpointaccess-vpcendpoint-networkinterfaces
            '''
            result = self._values.get("network_interfaces")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointAccessPropsMixin.NetworkInterfaceProperty"]]]], result)

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
            '''The connection endpoint ID for connecting an Amazon Redshift cluster through the proxy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-vpcendpoint.html#cfn-redshift-endpointaccess-vpcendpoint-vpcendpointid
            '''
            result = self._values.get("vpc_endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The VPC identifier that the endpoint is associated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-vpcendpoint.html#cfn-redshift-endpointaccess-vpcendpoint-vpcid
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
        jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnEndpointAccessPropsMixin.VpcSecurityGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status": "status",
            "vpc_security_group_id": "vpcSecurityGroupId",
        },
    )
    class VpcSecurityGroupProperty:
        def __init__(
            self,
            *,
            status: typing.Optional[builtins.str] = None,
            vpc_security_group_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The security groups associated with the endpoint.

            :param status: The status of the endpoint.
            :param vpc_security_group_id: The identifier of the VPC security group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-vpcsecuritygroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
                
                vpc_security_group_property = redshift_mixins.CfnEndpointAccessPropsMixin.VpcSecurityGroupProperty(
                    status="status",
                    vpc_security_group_id="vpcSecurityGroupId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d91302409d22d8f0ef13b930ad8376acc8d38eba3410180c1264422580bf9916)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument vpc_security_group_id", value=vpc_security_group_id, expected_type=type_hints["vpc_security_group_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status
            if vpc_security_group_id is not None:
                self._values["vpc_security_group_id"] = vpc_security_group_id

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-vpcsecuritygroup.html#cfn-redshift-endpointaccess-vpcsecuritygroup-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_security_group_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the VPC security group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-endpointaccess-vpcsecuritygroup.html#cfn-redshift-endpointaccess-vpcsecuritygroup-vpcsecuritygroupid
            '''
            result = self._values.get("vpc_security_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcSecurityGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnEndpointAuthorizationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "cluster_identifier": "clusterIdentifier",
        "force": "force",
        "vpc_ids": "vpcIds",
    },
)
class CfnEndpointAuthorizationMixinProps:
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        force: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        vpc_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnEndpointAuthorizationPropsMixin.

        :param account: The AWS account ID of either the cluster owner (grantor) or grantee. If ``Grantee`` parameter is true, then the ``Account`` value is of the grantor.
        :param cluster_identifier: The cluster identifier.
        :param force: Indicates whether to force the revoke action. If true, the Redshift-managed VPC endpoints associated with the endpoint authorization are also deleted.
        :param vpc_ids: The virtual private cloud (VPC) identifiers to grant access to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointauthorization.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
            
            cfn_endpoint_authorization_mixin_props = redshift_mixins.CfnEndpointAuthorizationMixinProps(
                account="account",
                cluster_identifier="clusterIdentifier",
                force=False,
                vpc_ids=["vpcIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a5cc006d8b218fa1c415fda0bfc920a55ccd98142afd7d0240bfbd15496492)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
            check_type(argname="argument vpc_ids", value=vpc_ids, expected_type=type_hints["vpc_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if cluster_identifier is not None:
            self._values["cluster_identifier"] = cluster_identifier
        if force is not None:
            self._values["force"] = force
        if vpc_ids is not None:
            self._values["vpc_ids"] = vpc_ids

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of either the cluster owner (grantor) or grantee.

        If ``Grantee`` parameter is true, then the ``Account`` value is of the grantor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointauthorization.html#cfn-redshift-endpointauthorization-account
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The cluster identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointauthorization.html#cfn-redshift-endpointauthorization-clusteridentifier
        '''
        result = self._values.get("cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether to force the revoke action.

        If true, the Redshift-managed VPC endpoints associated with the endpoint authorization are also deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointauthorization.html#cfn-redshift-endpointauthorization-force
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def vpc_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The virtual private cloud (VPC) identifiers to grant access to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointauthorization.html#cfn-redshift-endpointauthorization-vpcids
        '''
        result = self._values.get("vpc_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEndpointAuthorizationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEndpointAuthorizationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnEndpointAuthorizationPropsMixin",
):
    '''Describes an endpoint authorization for authorizing Redshift-managed VPC endpoint access to a cluster across AWS accounts .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-endpointauthorization.html
    :cloudformationResource: AWS::Redshift::EndpointAuthorization
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
        
        cfn_endpoint_authorization_props_mixin = redshift_mixins.CfnEndpointAuthorizationPropsMixin(redshift_mixins.CfnEndpointAuthorizationMixinProps(
            account="account",
            cluster_identifier="clusterIdentifier",
            force=False,
            vpc_ids=["vpcIds"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEndpointAuthorizationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Redshift::EndpointAuthorization``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4772dcc6b30a7387971b128e1c512c3de33d816da9b667aa90be5d2c7c7d0a73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__279041b15eb63b7def3fc41a8f6f59b0347caeaed44d56eff92aea49682edd68)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dbe95e21ebfb45b12e91f61950196a00165cc4546b76090611988309b4a9aba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEndpointAuthorizationMixinProps:
        return typing.cast(CfnEndpointAuthorizationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnEventSubscriptionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "event_categories": "eventCategories",
        "severity": "severity",
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
        severity: typing.Optional[builtins.str] = None,
        sns_topic_arn: typing.Optional[builtins.str] = None,
        source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_type: typing.Optional[builtins.str] = None,
        subscription_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEventSubscriptionPropsMixin.

        :param enabled: A boolean value; set to ``true`` to activate the subscription, and set to ``false`` to create the subscription but not activate it.
        :param event_categories: Specifies the Amazon Redshift event categories to be published by the event notification subscription. Values: configuration, management, monitoring, security, pending
        :param severity: Specifies the Amazon Redshift event severity to be published by the event notification subscription. Values: ERROR, INFO
        :param sns_topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic used to transmit the event notifications. The ARN is created by Amazon SNS when you create a topic and subscribe to it.
        :param source_ids: A list of one or more identifiers of Amazon Redshift source objects. All of the objects must be of the same type as was specified in the source type parameter. The event subscription will return only events generated by the specified objects. If not specified, then events are returned for all objects within the source type specified. Example: my-cluster-1, my-cluster-2 Example: my-snapshot-20131010
        :param source_type: The type of source that will be generating the events. For example, if you want to be notified of events generated by a cluster, you would set this parameter to cluster. If this value is not specified, events are returned for all Amazon Redshift objects in your AWS account . You must specify a source type in order to specify source IDs. Valid values: cluster, cluster-parameter-group, cluster-security-group, cluster-snapshot, and scheduled-action.
        :param subscription_name: The name of the event subscription to be created. Constraints: - Cannot be null, empty, or blank. - Must contain from 1 to 255 alphanumeric characters or hyphens. - First character must be a letter. - Cannot end with a hyphen or contain two consecutive hyphens.
        :param tags: A list of tag instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
            
            cfn_event_subscription_mixin_props = redshift_mixins.CfnEventSubscriptionMixinProps(
                enabled=False,
                event_categories=["eventCategories"],
                severity="severity",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d35ed0d56c5f0369c1e16d3603870aa94b32c810c80b9fc0bc91a33cba9af4ed)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_categories", value=event_categories, expected_type=type_hints["event_categories"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
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
        if severity is not None:
            self._values["severity"] = severity
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
        '''A boolean value;

        set to ``true`` to activate the subscription, and set to ``false`` to create the subscription but not activate it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html#cfn-redshift-eventsubscription-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def event_categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the Amazon Redshift event categories to be published by the event notification subscription.

        Values: configuration, management, monitoring, security, pending

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html#cfn-redshift-eventsubscription-eventcategories
        '''
        result = self._values.get("event_categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Redshift event severity to be published by the event notification subscription.

        Values: ERROR, INFO

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html#cfn-redshift-eventsubscription-severity
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic used to transmit the event notifications.

        The ARN is created by Amazon SNS when you create a topic and subscribe to it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html#cfn-redshift-eventsubscription-snstopicarn
        '''
        result = self._values.get("sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of one or more identifiers of Amazon Redshift source objects.

        All of the objects must be of the same type as was specified in the source type parameter. The event subscription will return only events generated by the specified objects. If not specified, then events are returned for all objects within the source type specified.

        Example: my-cluster-1, my-cluster-2

        Example: my-snapshot-20131010

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html#cfn-redshift-eventsubscription-sourceids
        '''
        result = self._values.get("source_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_type(self) -> typing.Optional[builtins.str]:
        '''The type of source that will be generating the events.

        For example, if you want to be notified of events generated by a cluster, you would set this parameter to cluster. If this value is not specified, events are returned for all Amazon Redshift objects in your AWS account . You must specify a source type in order to specify source IDs.

        Valid values: cluster, cluster-parameter-group, cluster-security-group, cluster-snapshot, and scheduled-action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html#cfn-redshift-eventsubscription-sourcetype
        '''
        result = self._values.get("source_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_name(self) -> typing.Optional[builtins.str]:
        '''The name of the event subscription to be created.

        Constraints:

        - Cannot be null, empty, or blank.
        - Must contain from 1 to 255 alphanumeric characters or hyphens.
        - First character must be a letter.
        - Cannot end with a hyphen or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html#cfn-redshift-eventsubscription-subscriptionname
        '''
        result = self._values.get("subscription_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tag instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html#cfn-redshift-eventsubscription-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnEventSubscriptionPropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-eventsubscription.html
    :cloudformationResource: AWS::Redshift::EventSubscription
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
        
        cfn_event_subscription_props_mixin = redshift_mixins.CfnEventSubscriptionPropsMixin(redshift_mixins.CfnEventSubscriptionMixinProps(
            enabled=False,
            event_categories=["eventCategories"],
            severity="severity",
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
        '''Create a mixin to apply properties to ``AWS::Redshift::EventSubscription``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2cdb472efdacbd75c73095c502dafc993c10baaf3f9409f114d37d9ba97e409)
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
            type_hints = typing.get_type_hints(_typecheckingstub__638651c3d2354a52c519d64ad0ca020eac51ae9b55d0a4cf50013b9d6faceaa7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68bd190773b1ff52d635e36bf569c1b5185a72b722e7ddbb306a3f965d46a23a)
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
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnIntegrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_encryption_context": "additionalEncryptionContext",
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
        integration_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        source_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIntegrationPropsMixin.

        :param additional_encryption_context: The encryption context for the integration. For more information, see `Encryption context <https://docs.aws.amazon.com/>`_ in the *AWS Key Management Service Developer Guide* .
        :param integration_name: The name of the integration.
        :param kms_key_id: The AWS Key Management Service ( AWS KMS) key identifier for the key used to encrypt the integration.
        :param source_arn: The Amazon Resource Name (ARN) of the database used as the source for replication.
        :param tags: The list of tags associated with the integration.
        :param target_arn: The Amazon Resource Name (ARN) of the Amazon Redshift data warehouse to use as the target for replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-integration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
            
            cfn_integration_mixin_props = redshift_mixins.CfnIntegrationMixinProps(
                additional_encryption_context={
                    "additional_encryption_context_key": "additionalEncryptionContext"
                },
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd9f8451c291a31a1642c9013e689f37a8aa853b90342230e444253382a7a667)
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument integration_name", value=integration_name, expected_type=type_hints["integration_name"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
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
        '''The encryption context for the integration.

        For more information, see `Encryption context <https://docs.aws.amazon.com/>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-integration.html#cfn-redshift-integration-additionalencryptioncontext
        '''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def integration_name(self) -> typing.Optional[builtins.str]:
        '''The name of the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-integration.html#cfn-redshift-integration-integrationname
        '''
        result = self._values.get("integration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS Key Management Service ( AWS KMS) key identifier for the key used to encrypt the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-integration.html#cfn-redshift-integration-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the database used as the source for replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-integration.html#cfn-redshift-integration-sourcearn
        '''
        result = self._values.get("source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of tags associated with the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-integration.html#cfn-redshift-integration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Redshift data warehouse to use as the target for replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-integration.html#cfn-redshift-integration-targetarn
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
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnIntegrationPropsMixin",
):
    '''Describes a zero-ETL or S3 integration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-integration.html
    :cloudformationResource: AWS::Redshift::Integration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
        
        cfn_integration_props_mixin = redshift_mixins.CfnIntegrationPropsMixin(redshift_mixins.CfnIntegrationMixinProps(
            additional_encryption_context={
                "additional_encryption_context_key": "additionalEncryptionContext"
            },
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
        '''Create a mixin to apply properties to ``AWS::Redshift::Integration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca123d81c708fedcb173b670a7b86941fd8d65077178f586ee790c491ae89563)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5365556947047ee14f678b6661c841f74570cfc51ecff00fd3e48fe97e82edc2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4139ebfbb07f903f3691a8adf86461a4d35a66cfa2cabe74e93f2d7b7d4f45fe)
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
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnScheduledActionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "end_time": "endTime",
        "iam_role": "iamRole",
        "schedule": "schedule",
        "scheduled_action_description": "scheduledActionDescription",
        "scheduled_action_name": "scheduledActionName",
        "start_time": "startTime",
        "target_action": "targetAction",
    },
)
class CfnScheduledActionMixinProps:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        end_time: typing.Optional[builtins.str] = None,
        iam_role: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        scheduled_action_description: typing.Optional[builtins.str] = None,
        scheduled_action_name: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        target_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledActionPropsMixin.ScheduledActionTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnScheduledActionPropsMixin.

        :param enable: If true, the schedule is enabled. If false, the scheduled action does not trigger. For more information about ``state`` of the scheduled action, see ``ScheduledAction`` .
        :param end_time: The end time in UTC when the schedule is no longer active. After this time, the scheduled action does not trigger.
        :param iam_role: The IAM role to assume to run the scheduled action. This IAM role must have permission to run the Amazon Redshift API operation in the scheduled action. This IAM role must allow the Amazon Redshift scheduler (Principal scheduler.redshift.amazonaws.com) to assume permissions on your behalf. For more information about the IAM role to use with the Amazon Redshift scheduler, see `Using Identity-Based Policies for Amazon Redshift <https://docs.aws.amazon.com/redshift/latest/mgmt/redshift-iam-access-control-identity-based.html>`_ in the *Amazon Redshift Cluster Management Guide* .
        :param schedule: The schedule for a one-time (at format) or recurring (cron format) scheduled action. Schedule invocations must be separated by at least one hour. Format of at expressions is " ``at(yyyy-mm-ddThh:mm:ss)`` ". For example, " ``at(2016-03-04T17:27:00)`` ". Format of cron expressions is " ``cron(Minutes Hours Day-of-month Month Day-of-week Year)`` ". For example, " ``cron(0 10 ? * MON *)`` ". For more information, see `Cron Expressions <https://docs.aws.amazon.com//AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions>`_ in the *Amazon CloudWatch Events User Guide* .
        :param scheduled_action_description: The description of the scheduled action.
        :param scheduled_action_name: The name of the scheduled action.
        :param start_time: The start time in UTC when the schedule is active. Before this time, the scheduled action does not trigger.
        :param target_action: A JSON format string of the Amazon Redshift API operation with input parameters. " ``{\\"ResizeCluster\\":{\\"NodeType\\":\\"ra3.4xlarge\\",\\"ClusterIdentifier\\":\\"my-test-cluster\\",\\"NumberOfNodes\\":3}}`` ".

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-scheduledaction.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
            
            cfn_scheduled_action_mixin_props = redshift_mixins.CfnScheduledActionMixinProps(
                enable=False,
                end_time="endTime",
                iam_role="iamRole",
                schedule="schedule",
                scheduled_action_description="scheduledActionDescription",
                scheduled_action_name="scheduledActionName",
                start_time="startTime",
                target_action=redshift_mixins.CfnScheduledActionPropsMixin.ScheduledActionTypeProperty(
                    pause_cluster=redshift_mixins.CfnScheduledActionPropsMixin.PauseClusterMessageProperty(
                        cluster_identifier="clusterIdentifier"
                    ),
                    resize_cluster=redshift_mixins.CfnScheduledActionPropsMixin.ResizeClusterMessageProperty(
                        classic=False,
                        cluster_identifier="clusterIdentifier",
                        cluster_type="clusterType",
                        node_type="nodeType",
                        number_of_nodes=123
                    ),
                    resume_cluster=redshift_mixins.CfnScheduledActionPropsMixin.ResumeClusterMessageProperty(
                        cluster_identifier="clusterIdentifier"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27c557924556bbe4e2708176f61298b7251abdbfd4a9420865c0ff00398f6b6)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument iam_role", value=iam_role, expected_type=type_hints["iam_role"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument scheduled_action_description", value=scheduled_action_description, expected_type=type_hints["scheduled_action_description"])
            check_type(argname="argument scheduled_action_name", value=scheduled_action_name, expected_type=type_hints["scheduled_action_name"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument target_action", value=target_action, expected_type=type_hints["target_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable is not None:
            self._values["enable"] = enable
        if end_time is not None:
            self._values["end_time"] = end_time
        if iam_role is not None:
            self._values["iam_role"] = iam_role
        if schedule is not None:
            self._values["schedule"] = schedule
        if scheduled_action_description is not None:
            self._values["scheduled_action_description"] = scheduled_action_description
        if scheduled_action_name is not None:
            self._values["scheduled_action_name"] = scheduled_action_name
        if start_time is not None:
            self._values["start_time"] = start_time
        if target_action is not None:
            self._values["target_action"] = target_action

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If true, the schedule is enabled.

        If false, the scheduled action does not trigger. For more information about ``state`` of the scheduled action, see ``ScheduledAction`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-scheduledaction.html#cfn-redshift-scheduledaction-enable
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''The end time in UTC when the schedule is no longer active.

        After this time, the scheduled action does not trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-scheduledaction.html#cfn-redshift-scheduledaction-endtime
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_role(self) -> typing.Optional[builtins.str]:
        '''The IAM role to assume to run the scheduled action.

        This IAM role must have permission to run the Amazon Redshift API operation in the scheduled action. This IAM role must allow the Amazon Redshift scheduler (Principal scheduler.redshift.amazonaws.com) to assume permissions on your behalf. For more information about the IAM role to use with the Amazon Redshift scheduler, see `Using Identity-Based Policies for Amazon Redshift <https://docs.aws.amazon.com/redshift/latest/mgmt/redshift-iam-access-control-identity-based.html>`_ in the *Amazon Redshift Cluster Management Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-scheduledaction.html#cfn-redshift-scheduledaction-iamrole
        '''
        result = self._values.get("iam_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''The schedule for a one-time (at format) or recurring (cron format) scheduled action.

        Schedule invocations must be separated by at least one hour.

        Format of at expressions is " ``at(yyyy-mm-ddThh:mm:ss)`` ". For example, " ``at(2016-03-04T17:27:00)`` ".

        Format of cron expressions is " ``cron(Minutes Hours Day-of-month Month Day-of-week Year)`` ". For example, " ``cron(0 10 ? * MON *)`` ". For more information, see `Cron Expressions <https://docs.aws.amazon.com//AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions>`_ in the *Amazon CloudWatch Events User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-scheduledaction.html#cfn-redshift-scheduledaction-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_action_description(self) -> typing.Optional[builtins.str]:
        '''The description of the scheduled action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-scheduledaction.html#cfn-redshift-scheduledaction-scheduledactiondescription
        '''
        result = self._values.get("scheduled_action_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_action_name(self) -> typing.Optional[builtins.str]:
        '''The name of the scheduled action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-scheduledaction.html#cfn-redshift-scheduledaction-scheduledactionname
        '''
        result = self._values.get("scheduled_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The start time in UTC when the schedule is active.

        Before this time, the scheduled action does not trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-scheduledaction.html#cfn-redshift-scheduledaction-starttime
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_action(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledActionPropsMixin.ScheduledActionTypeProperty"]]:
        '''A JSON format string of the Amazon Redshift API operation with input parameters.

        " ``{\\"ResizeCluster\\":{\\"NodeType\\":\\"ra3.4xlarge\\",\\"ClusterIdentifier\\":\\"my-test-cluster\\",\\"NumberOfNodes\\":3}}`` ".

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-scheduledaction.html#cfn-redshift-scheduledaction-targetaction
        '''
        result = self._values.get("target_action")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledActionPropsMixin.ScheduledActionTypeProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduledActionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnScheduledActionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnScheduledActionPropsMixin",
):
    '''Creates a scheduled action.

    A scheduled action contains a schedule and an Amazon Redshift API action. For example, you can create a schedule of when to run the ``ResizeCluster`` API operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-scheduledaction.html
    :cloudformationResource: AWS::Redshift::ScheduledAction
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
        
        cfn_scheduled_action_props_mixin = redshift_mixins.CfnScheduledActionPropsMixin(redshift_mixins.CfnScheduledActionMixinProps(
            enable=False,
            end_time="endTime",
            iam_role="iamRole",
            schedule="schedule",
            scheduled_action_description="scheduledActionDescription",
            scheduled_action_name="scheduledActionName",
            start_time="startTime",
            target_action=redshift_mixins.CfnScheduledActionPropsMixin.ScheduledActionTypeProperty(
                pause_cluster=redshift_mixins.CfnScheduledActionPropsMixin.PauseClusterMessageProperty(
                    cluster_identifier="clusterIdentifier"
                ),
                resize_cluster=redshift_mixins.CfnScheduledActionPropsMixin.ResizeClusterMessageProperty(
                    classic=False,
                    cluster_identifier="clusterIdentifier",
                    cluster_type="clusterType",
                    node_type="nodeType",
                    number_of_nodes=123
                ),
                resume_cluster=redshift_mixins.CfnScheduledActionPropsMixin.ResumeClusterMessageProperty(
                    cluster_identifier="clusterIdentifier"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnScheduledActionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Redshift::ScheduledAction``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a1177b87021232d0e0bfb755ecb7d1d6c94db3b420a048beed689ab7d30de8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07ad6833ccdbc1bc661315f167328dfceeedc1735b1371a0dce7fb15c2304b90)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f83735d1a2108dac25c20a67733d714092faf2b182ac113cf077910deadf3fb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScheduledActionMixinProps:
        return typing.cast(CfnScheduledActionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnScheduledActionPropsMixin.PauseClusterMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"cluster_identifier": "clusterIdentifier"},
    )
    class PauseClusterMessageProperty:
        def __init__(
            self,
            *,
            cluster_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a pause cluster operation.

            For example, a scheduled action to run the ``PauseCluster`` API operation.

            :param cluster_identifier: The identifier of the cluster to be paused.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-pauseclustermessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
                
                pause_cluster_message_property = redshift_mixins.CfnScheduledActionPropsMixin.PauseClusterMessageProperty(
                    cluster_identifier="clusterIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9120c43fcbe1ebff94ef6b4474b4d51fe6919697d7820453181fa8c6e933e6e2)
                check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_identifier is not None:
                self._values["cluster_identifier"] = cluster_identifier

        @builtins.property
        def cluster_identifier(self) -> typing.Optional[builtins.str]:
            '''The identifier of the cluster to be paused.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-pauseclustermessage.html#cfn-redshift-scheduledaction-pauseclustermessage-clusteridentifier
            '''
            result = self._values.get("cluster_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PauseClusterMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnScheduledActionPropsMixin.ResizeClusterMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "classic": "classic",
            "cluster_identifier": "clusterIdentifier",
            "cluster_type": "clusterType",
            "node_type": "nodeType",
            "number_of_nodes": "numberOfNodes",
        },
    )
    class ResizeClusterMessageProperty:
        def __init__(
            self,
            *,
            classic: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            cluster_identifier: typing.Optional[builtins.str] = None,
            cluster_type: typing.Optional[builtins.str] = None,
            node_type: typing.Optional[builtins.str] = None,
            number_of_nodes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes a resize cluster operation.

            For example, a scheduled action to run the ``ResizeCluster`` API operation.

            :param classic: A boolean value indicating whether the resize operation is using the classic resize process. If you don't provide this parameter or set the value to ``false`` , the resize type is elastic.
            :param cluster_identifier: The unique identifier for the cluster to resize.
            :param cluster_type: The new cluster type for the specified cluster.
            :param node_type: The new node type for the nodes you are adding. If not specified, the cluster's current node type is used.
            :param number_of_nodes: The new number of nodes for the cluster. If not specified, the cluster's current number of nodes is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-resizeclustermessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
                
                resize_cluster_message_property = redshift_mixins.CfnScheduledActionPropsMixin.ResizeClusterMessageProperty(
                    classic=False,
                    cluster_identifier="clusterIdentifier",
                    cluster_type="clusterType",
                    node_type="nodeType",
                    number_of_nodes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a462666ff3e49119f195dda357389b5a1ee74f521115e02259e166a4ab3b97e)
                check_type(argname="argument classic", value=classic, expected_type=type_hints["classic"])
                check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
                check_type(argname="argument cluster_type", value=cluster_type, expected_type=type_hints["cluster_type"])
                check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
                check_type(argname="argument number_of_nodes", value=number_of_nodes, expected_type=type_hints["number_of_nodes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if classic is not None:
                self._values["classic"] = classic
            if cluster_identifier is not None:
                self._values["cluster_identifier"] = cluster_identifier
            if cluster_type is not None:
                self._values["cluster_type"] = cluster_type
            if node_type is not None:
                self._values["node_type"] = node_type
            if number_of_nodes is not None:
                self._values["number_of_nodes"] = number_of_nodes

        @builtins.property
        def classic(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean value indicating whether the resize operation is using the classic resize process.

            If you don't provide this parameter or set the value to ``false`` , the resize type is elastic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-resizeclustermessage.html#cfn-redshift-scheduledaction-resizeclustermessage-classic
            '''
            result = self._values.get("classic")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def cluster_identifier(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the cluster to resize.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-resizeclustermessage.html#cfn-redshift-scheduledaction-resizeclustermessage-clusteridentifier
            '''
            result = self._values.get("cluster_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cluster_type(self) -> typing.Optional[builtins.str]:
            '''The new cluster type for the specified cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-resizeclustermessage.html#cfn-redshift-scheduledaction-resizeclustermessage-clustertype
            '''
            result = self._values.get("cluster_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def node_type(self) -> typing.Optional[builtins.str]:
            '''The new node type for the nodes you are adding.

            If not specified, the cluster's current node type is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-resizeclustermessage.html#cfn-redshift-scheduledaction-resizeclustermessage-nodetype
            '''
            result = self._values.get("node_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def number_of_nodes(self) -> typing.Optional[jsii.Number]:
            '''The new number of nodes for the cluster.

            If not specified, the cluster's current number of nodes is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-resizeclustermessage.html#cfn-redshift-scheduledaction-resizeclustermessage-numberofnodes
            '''
            result = self._values.get("number_of_nodes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResizeClusterMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnScheduledActionPropsMixin.ResumeClusterMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"cluster_identifier": "clusterIdentifier"},
    )
    class ResumeClusterMessageProperty:
        def __init__(
            self,
            *,
            cluster_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a resume cluster operation.

            For example, a scheduled action to run the ``ResumeCluster`` API operation.

            :param cluster_identifier: The identifier of the cluster to be resumed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-resumeclustermessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
                
                resume_cluster_message_property = redshift_mixins.CfnScheduledActionPropsMixin.ResumeClusterMessageProperty(
                    cluster_identifier="clusterIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f16519d903935befc97b833234394951f438b072f19af65434d6c560e0efcc2)
                check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_identifier is not None:
                self._values["cluster_identifier"] = cluster_identifier

        @builtins.property
        def cluster_identifier(self) -> typing.Optional[builtins.str]:
            '''The identifier of the cluster to be resumed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-resumeclustermessage.html#cfn-redshift-scheduledaction-resumeclustermessage-clusteridentifier
            '''
            result = self._values.get("cluster_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResumeClusterMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_redshift.mixins.CfnScheduledActionPropsMixin.ScheduledActionTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pause_cluster": "pauseCluster",
            "resize_cluster": "resizeCluster",
            "resume_cluster": "resumeCluster",
        },
    )
    class ScheduledActionTypeProperty:
        def __init__(
            self,
            *,
            pause_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledActionPropsMixin.PauseClusterMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resize_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledActionPropsMixin.ResizeClusterMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resume_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScheduledActionPropsMixin.ResumeClusterMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The action type that specifies an Amazon Redshift API operation that is supported by the Amazon Redshift scheduler.

            :param pause_cluster: An action that runs a ``PauseCluster`` API operation.
            :param resize_cluster: An action that runs a ``ResizeCluster`` API operation.
            :param resume_cluster: An action that runs a ``ResumeCluster`` API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-scheduledactiontype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_redshift import mixins as redshift_mixins
                
                scheduled_action_type_property = redshift_mixins.CfnScheduledActionPropsMixin.ScheduledActionTypeProperty(
                    pause_cluster=redshift_mixins.CfnScheduledActionPropsMixin.PauseClusterMessageProperty(
                        cluster_identifier="clusterIdentifier"
                    ),
                    resize_cluster=redshift_mixins.CfnScheduledActionPropsMixin.ResizeClusterMessageProperty(
                        classic=False,
                        cluster_identifier="clusterIdentifier",
                        cluster_type="clusterType",
                        node_type="nodeType",
                        number_of_nodes=123
                    ),
                    resume_cluster=redshift_mixins.CfnScheduledActionPropsMixin.ResumeClusterMessageProperty(
                        cluster_identifier="clusterIdentifier"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3cb6a8d480889d44245762317540eac7dc2dedb76247aea97b6797605493db74)
                check_type(argname="argument pause_cluster", value=pause_cluster, expected_type=type_hints["pause_cluster"])
                check_type(argname="argument resize_cluster", value=resize_cluster, expected_type=type_hints["resize_cluster"])
                check_type(argname="argument resume_cluster", value=resume_cluster, expected_type=type_hints["resume_cluster"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pause_cluster is not None:
                self._values["pause_cluster"] = pause_cluster
            if resize_cluster is not None:
                self._values["resize_cluster"] = resize_cluster
            if resume_cluster is not None:
                self._values["resume_cluster"] = resume_cluster

        @builtins.property
        def pause_cluster(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledActionPropsMixin.PauseClusterMessageProperty"]]:
            '''An action that runs a ``PauseCluster`` API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-scheduledactiontype.html#cfn-redshift-scheduledaction-scheduledactiontype-pausecluster
            '''
            result = self._values.get("pause_cluster")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledActionPropsMixin.PauseClusterMessageProperty"]], result)

        @builtins.property
        def resize_cluster(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledActionPropsMixin.ResizeClusterMessageProperty"]]:
            '''An action that runs a ``ResizeCluster`` API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-scheduledactiontype.html#cfn-redshift-scheduledaction-scheduledactiontype-resizecluster
            '''
            result = self._values.get("resize_cluster")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledActionPropsMixin.ResizeClusterMessageProperty"]], result)

        @builtins.property
        def resume_cluster(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledActionPropsMixin.ResumeClusterMessageProperty"]]:
            '''An action that runs a ``ResumeCluster`` API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-scheduledaction-scheduledactiontype.html#cfn-redshift-scheduledaction-scheduledactiontype-resumecluster
            '''
            result = self._values.get("resume_cluster")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScheduledActionPropsMixin.ResumeClusterMessageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduledActionTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnClusterMixinProps",
    "CfnClusterParameterGroupMixinProps",
    "CfnClusterParameterGroupPropsMixin",
    "CfnClusterPropsMixin",
    "CfnClusterSecurityGroupIngressMixinProps",
    "CfnClusterSecurityGroupIngressPropsMixin",
    "CfnClusterSecurityGroupMixinProps",
    "CfnClusterSecurityGroupPropsMixin",
    "CfnClusterSubnetGroupMixinProps",
    "CfnClusterSubnetGroupPropsMixin",
    "CfnEndpointAccessMixinProps",
    "CfnEndpointAccessPropsMixin",
    "CfnEndpointAuthorizationMixinProps",
    "CfnEndpointAuthorizationPropsMixin",
    "CfnEventSubscriptionMixinProps",
    "CfnEventSubscriptionPropsMixin",
    "CfnIntegrationMixinProps",
    "CfnIntegrationPropsMixin",
    "CfnScheduledActionMixinProps",
    "CfnScheduledActionPropsMixin",
]

publication.publish()

def _typecheckingstub__3fa8e028d7fa71d8b68bae29f2c14a38830e7eae95dc3fc8e4a099f833447051(
    *,
    allow_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    aqua_configuration_status: typing.Optional[builtins.str] = None,
    automated_snapshot_retention_period: typing.Optional[jsii.Number] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    availability_zone_relocation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    availability_zone_relocation_status: typing.Optional[builtins.str] = None,
    classic: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cluster_identifier: typing.Optional[builtins.str] = None,
    cluster_parameter_group_name: typing.Optional[builtins.str] = None,
    cluster_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    cluster_subnet_group_name: typing.Optional[builtins.str] = None,
    cluster_type: typing.Optional[builtins.str] = None,
    cluster_version: typing.Optional[builtins.str] = None,
    db_name: typing.Optional[builtins.str] = None,
    defer_maintenance: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    defer_maintenance_duration: typing.Optional[jsii.Number] = None,
    defer_maintenance_end_time: typing.Optional[builtins.str] = None,
    defer_maintenance_start_time: typing.Optional[builtins.str] = None,
    destination_region: typing.Optional[builtins.str] = None,
    elastic_ip: typing.Optional[builtins.str] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.EndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enhanced_vpc_routing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    hsm_client_certificate_identifier: typing.Optional[builtins.str] = None,
    hsm_configuration_identifier: typing.Optional[builtins.str] = None,
    iam_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    logging_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.LoggingPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maintenance_track_name: typing.Optional[builtins.str] = None,
    manage_master_password: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    manual_snapshot_retention_period: typing.Optional[jsii.Number] = None,
    master_password_secret_kms_key_id: typing.Optional[builtins.str] = None,
    master_username: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[builtins.str] = None,
    multi_az: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    namespace_resource_policy: typing.Any = None,
    node_type: typing.Optional[builtins.str] = None,
    number_of_nodes: typing.Optional[jsii.Number] = None,
    owner_account: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    resource_action: typing.Optional[builtins.str] = None,
    revision_target: typing.Optional[builtins.str] = None,
    rotate_encryption_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    snapshot_cluster_identifier: typing.Optional[builtins.str] = None,
    snapshot_copy_grant_name: typing.Optional[builtins.str] = None,
    snapshot_copy_manual: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    snapshot_copy_retention_period: typing.Optional[jsii.Number] = None,
    snapshot_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f13ef7e4d0e278bbb66192a83e1e8f0a5d3024d44c43e1f97eff2ee5747fff(
    *,
    description: typing.Optional[builtins.str] = None,
    parameter_group_family: typing.Optional[builtins.str] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterParameterGroupPropsMixin.ParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2417dfb72b44e87be5648c0b8cc7d70e94a98127d135fa964536bc44aebea0a7(
    props: typing.Union[CfnClusterParameterGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d830569fff9bf8aed45ea354252ab441fd89124c1632f4e228c8e782ce1c95(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fdec487c1d914bc3db8af8982aa559fb2750c2aaf10c45241f39783eb351320(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8c801500be5524730e9cdd68afeeb3119e87cacf4f8ef8da85aee6a2518d25(
    *,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c07df62de57fb6b54d2279775a164d33d89dc3302fb7f7f29e4c7d564bc7a69(
    props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2ae00ae92a0f5817366f5b6a75b0704ecd417bac2910a2ed7db91e9de01f47(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e71cc02c785a4824f1684ec62150c26996594c30838428ffb3fde87675e157(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee91498db9a9e31dd3ba5dc79cf29b8a62b8eeb5639d4c5780d3f6731e4d567e(
    *,
    address: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3120b1dadd07379aa00e87c13d3ba2c2d5334bcb036dc458bef0d7685a2abc5(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    log_destination_type: typing.Optional[builtins.str] = None,
    log_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6d64f218de6e4f9ce4021cfff967f2db3845c97587b99c18d5ca529a6babb2(
    *,
    cidrip: typing.Optional[builtins.str] = None,
    cluster_security_group_name: typing.Optional[builtins.str] = None,
    ec2_security_group_name: typing.Optional[builtins.str] = None,
    ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbc47cd9dd6b2c6a73fcaaa303654eada7093997216e3ecd9f53f7e4a78fc32(
    props: typing.Union[CfnClusterSecurityGroupIngressMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f7c8ea00176ccd59c16ed63ea90e116b7956badb64c981adb4ef90b658a41a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b33fc169dc39499d51a02342b800bef25759767f66abfd41494da88cb0db547(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9b2fef75b50ded26675e22991107ed4ba5e815bdb3f5d8ae7e19a2fe550f7b(
    *,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1e63c6fd9e6ebab90975718db01e978c87ce0254768bb52fe3113065a9dc61(
    props: typing.Union[CfnClusterSecurityGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b91505218980e1ed4504ead8804d405265154af47e09cc76b95c2da1f292ae(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af6fd5f8c43bf48adefafa8f00cfbdb88a504a68d666a9220c3eaeb58b0368d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58576fcfc42d27c1e89545f3cccd02c8736732ab9b0f182b82b9c8130be5e090(
    *,
    description: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc759bdd8df0bd9323cee5f2a72bd4a1105ce32b4f6a2f6f254a50d3ed71601d(
    props: typing.Union[CfnClusterSubnetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c28d5736d7ceae92ff3e036ab14ccd607ad6e3249599ee3efa08bb293565d3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efeb564689e69e290d2e63b55209e2bf46d48ea28d26f6e1ff1077bb7a435096(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf67ff620a0e40fedb01d14ea7660fd970e342b73032cec93f0c2ce2604aff29(
    *,
    cluster_identifier: typing.Optional[builtins.str] = None,
    endpoint_name: typing.Optional[builtins.str] = None,
    resource_owner: typing.Optional[builtins.str] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6118db7bc34363910616e0602f53e3e7859b69fba49626d65d35bd64ef0811e2(
    props: typing.Union[CfnEndpointAccessMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287371f128f9b2bae6ead87947bac6f9921252a5cc9bc6816636d26d5822f1bf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42bf8911e26f71c374f40932b7eb7adabe8b338c3a1cc77344691724514bf028(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99daf49752f0bce1454c26923217847adec52a16fff88a518e5a1e5642a473ba(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    network_interface_id: typing.Optional[builtins.str] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f4ae568ec6d302ed4aab5aa576082815dd29c814356f32cb3c41778422a05e(
    *,
    network_interfaces: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointAccessPropsMixin.NetworkInterfaceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91302409d22d8f0ef13b930ad8376acc8d38eba3410180c1264422580bf9916(
    *,
    status: typing.Optional[builtins.str] = None,
    vpc_security_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a5cc006d8b218fa1c415fda0bfc920a55ccd98142afd7d0240bfbd15496492(
    *,
    account: typing.Optional[builtins.str] = None,
    cluster_identifier: typing.Optional[builtins.str] = None,
    force: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    vpc_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4772dcc6b30a7387971b128e1c512c3de33d816da9b667aa90be5d2c7c7d0a73(
    props: typing.Union[CfnEndpointAuthorizationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279041b15eb63b7def3fc41a8f6f59b0347caeaed44d56eff92aea49682edd68(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbe95e21ebfb45b12e91f61950196a00165cc4546b76090611988309b4a9aba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35ed0d56c5f0369c1e16d3603870aa94b32c810c80b9fc0bc91a33cba9af4ed(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    event_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    severity: typing.Optional[builtins.str] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
    source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_type: typing.Optional[builtins.str] = None,
    subscription_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2cdb472efdacbd75c73095c502dafc993c10baaf3f9409f114d37d9ba97e409(
    props: typing.Union[CfnEventSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638651c3d2354a52c519d64ad0ca020eac51ae9b55d0a4cf50013b9d6faceaa7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68bd190773b1ff52d635e36bf569c1b5185a72b722e7ddbb306a3f965d46a23a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9f8451c291a31a1642c9013e689f37a8aa853b90342230e444253382a7a667(
    *,
    additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    integration_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca123d81c708fedcb173b670a7b86941fd8d65077178f586ee790c491ae89563(
    props: typing.Union[CfnIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5365556947047ee14f678b6661c841f74570cfc51ecff00fd3e48fe97e82edc2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4139ebfbb07f903f3691a8adf86461a4d35a66cfa2cabe74e93f2d7b7d4f45fe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27c557924556bbe4e2708176f61298b7251abdbfd4a9420865c0ff00398f6b6(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    end_time: typing.Optional[builtins.str] = None,
    iam_role: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    scheduled_action_description: typing.Optional[builtins.str] = None,
    scheduled_action_name: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    target_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledActionPropsMixin.ScheduledActionTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a1177b87021232d0e0bfb755ecb7d1d6c94db3b420a048beed689ab7d30de8(
    props: typing.Union[CfnScheduledActionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ad6833ccdbc1bc661315f167328dfceeedc1735b1371a0dce7fb15c2304b90(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f83735d1a2108dac25c20a67733d714092faf2b182ac113cf077910deadf3fb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9120c43fcbe1ebff94ef6b4474b4d51fe6919697d7820453181fa8c6e933e6e2(
    *,
    cluster_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a462666ff3e49119f195dda357389b5a1ee74f521115e02259e166a4ab3b97e(
    *,
    classic: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cluster_identifier: typing.Optional[builtins.str] = None,
    cluster_type: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    number_of_nodes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f16519d903935befc97b833234394951f438b072f19af65434d6c560e0efcc2(
    *,
    cluster_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb6a8d480889d44245762317540eac7dc2dedb76247aea97b6797605493db74(
    *,
    pause_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledActionPropsMixin.PauseClusterMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resize_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledActionPropsMixin.ResizeClusterMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resume_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScheduledActionPropsMixin.ResumeClusterMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
