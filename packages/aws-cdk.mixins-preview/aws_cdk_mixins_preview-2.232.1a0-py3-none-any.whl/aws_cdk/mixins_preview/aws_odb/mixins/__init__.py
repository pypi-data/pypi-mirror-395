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
    jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudAutonomousVmClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "autonomous_data_storage_size_in_t_bs": "autonomousDataStorageSizeInTBs",
        "cloud_exadata_infrastructure_id": "cloudExadataInfrastructureId",
        "cpu_core_count_per_node": "cpuCoreCountPerNode",
        "db_servers": "dbServers",
        "description": "description",
        "display_name": "displayName",
        "is_mtls_enabled_vm_cluster": "isMtlsEnabledVmCluster",
        "license_model": "licenseModel",
        "maintenance_window": "maintenanceWindow",
        "memory_per_oracle_compute_unit_in_g_bs": "memoryPerOracleComputeUnitInGBs",
        "odb_network_id": "odbNetworkId",
        "scan_listener_port_non_tls": "scanListenerPortNonTls",
        "scan_listener_port_tls": "scanListenerPortTls",
        "tags": "tags",
        "time_zone": "timeZone",
        "total_container_databases": "totalContainerDatabases",
    },
)
class CfnCloudAutonomousVmClusterMixinProps:
    def __init__(
        self,
        *,
        autonomous_data_storage_size_in_t_bs: typing.Optional[jsii.Number] = None,
        cloud_exadata_infrastructure_id: typing.Optional[builtins.str] = None,
        cpu_core_count_per_node: typing.Optional[jsii.Number] = None,
        db_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        is_mtls_enabled_vm_cluster: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        license_model: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudAutonomousVmClusterPropsMixin.MaintenanceWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        memory_per_oracle_compute_unit_in_g_bs: typing.Optional[jsii.Number] = None,
        odb_network_id: typing.Optional[builtins.str] = None,
        scan_listener_port_non_tls: typing.Optional[jsii.Number] = None,
        scan_listener_port_tls: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        total_container_databases: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnCloudAutonomousVmClusterPropsMixin.

        :param autonomous_data_storage_size_in_t_bs: The data storage size allocated for Autonomous Databases in the Autonomous VM cluster, in TB. Required when creating an Autonomous VM cluster.
        :param cloud_exadata_infrastructure_id: The unique identifier of the Cloud Exadata Infrastructure containing this Autonomous VM cluster. Required when creating an Autonomous VM cluster.
        :param cpu_core_count_per_node: The number of CPU cores enabled per node in the Autonomous VM cluster. Required when creating an Autonomous VM cluster.
        :param db_servers: The list of database servers associated with the Autonomous VM cluster.
        :param description: The user-provided description of the Autonomous VM cluster.
        :param display_name: The display name of the Autonomous VM cluster. Required when creating an Autonomous VM cluster.
        :param is_mtls_enabled_vm_cluster: Specifies whether mutual TLS (mTLS) authentication is enabled for the Autonomous VM cluster.
        :param license_model: The Oracle license model that applies to the Autonomous VM cluster. Valid values are ``LICENSE_INCLUDED`` or ``BRING_YOUR_OWN_LICENSE`` .
        :param maintenance_window: The scheduling details for the maintenance window. Patching and system updates take place during the maintenance window.
        :param memory_per_oracle_compute_unit_in_g_bs: The amount of memory allocated per Oracle Compute Unit, in GB. Required when creating an Autonomous VM cluster.
        :param odb_network_id: The unique identifier of the ODB network associated with this Autonomous VM cluster. Required when creating an Autonomous VM cluster.
        :param scan_listener_port_non_tls: The SCAN listener port for non-TLS (TCP) protocol. The default is 1521.
        :param scan_listener_port_tls: The SCAN listener port for TLS (TCP) protocol. The default is 2484.
        :param tags: Tags to assign to the Autonomous Vm Cluster.
        :param time_zone: The time zone of the Autonomous VM cluster.
        :param total_container_databases: The total number of Autonomous Container Databases that can be created with the allocated local storage. Required when creating an Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
            
            cfn_cloud_autonomous_vm_cluster_mixin_props = odb_mixins.CfnCloudAutonomousVmClusterMixinProps(
                autonomous_data_storage_size_in_tBs=123,
                cloud_exadata_infrastructure_id="cloudExadataInfrastructureId",
                cpu_core_count_per_node=123,
                db_servers=["dbServers"],
                description="description",
                display_name="displayName",
                is_mtls_enabled_vm_cluster=False,
                license_model="licenseModel",
                maintenance_window=odb_mixins.CfnCloudAutonomousVmClusterPropsMixin.MaintenanceWindowProperty(
                    days_of_week=["daysOfWeek"],
                    hours_of_day=[123],
                    lead_time_in_weeks=123,
                    months=["months"],
                    preference="preference",
                    weeks_of_month=[123]
                ),
                memory_per_oracle_compute_unit_in_gBs=123,
                odb_network_id="odbNetworkId",
                scan_listener_port_non_tls=123,
                scan_listener_port_tls=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                time_zone="timeZone",
                total_container_databases=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7df233982f64b70b9f8338aab569ddf81f47e5b7ee40f0871324c76d6a4dbb6)
            check_type(argname="argument autonomous_data_storage_size_in_t_bs", value=autonomous_data_storage_size_in_t_bs, expected_type=type_hints["autonomous_data_storage_size_in_t_bs"])
            check_type(argname="argument cloud_exadata_infrastructure_id", value=cloud_exadata_infrastructure_id, expected_type=type_hints["cloud_exadata_infrastructure_id"])
            check_type(argname="argument cpu_core_count_per_node", value=cpu_core_count_per_node, expected_type=type_hints["cpu_core_count_per_node"])
            check_type(argname="argument db_servers", value=db_servers, expected_type=type_hints["db_servers"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument is_mtls_enabled_vm_cluster", value=is_mtls_enabled_vm_cluster, expected_type=type_hints["is_mtls_enabled_vm_cluster"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument memory_per_oracle_compute_unit_in_g_bs", value=memory_per_oracle_compute_unit_in_g_bs, expected_type=type_hints["memory_per_oracle_compute_unit_in_g_bs"])
            check_type(argname="argument odb_network_id", value=odb_network_id, expected_type=type_hints["odb_network_id"])
            check_type(argname="argument scan_listener_port_non_tls", value=scan_listener_port_non_tls, expected_type=type_hints["scan_listener_port_non_tls"])
            check_type(argname="argument scan_listener_port_tls", value=scan_listener_port_tls, expected_type=type_hints["scan_listener_port_tls"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument total_container_databases", value=total_container_databases, expected_type=type_hints["total_container_databases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autonomous_data_storage_size_in_t_bs is not None:
            self._values["autonomous_data_storage_size_in_t_bs"] = autonomous_data_storage_size_in_t_bs
        if cloud_exadata_infrastructure_id is not None:
            self._values["cloud_exadata_infrastructure_id"] = cloud_exadata_infrastructure_id
        if cpu_core_count_per_node is not None:
            self._values["cpu_core_count_per_node"] = cpu_core_count_per_node
        if db_servers is not None:
            self._values["db_servers"] = db_servers
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if is_mtls_enabled_vm_cluster is not None:
            self._values["is_mtls_enabled_vm_cluster"] = is_mtls_enabled_vm_cluster
        if license_model is not None:
            self._values["license_model"] = license_model
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if memory_per_oracle_compute_unit_in_g_bs is not None:
            self._values["memory_per_oracle_compute_unit_in_g_bs"] = memory_per_oracle_compute_unit_in_g_bs
        if odb_network_id is not None:
            self._values["odb_network_id"] = odb_network_id
        if scan_listener_port_non_tls is not None:
            self._values["scan_listener_port_non_tls"] = scan_listener_port_non_tls
        if scan_listener_port_tls is not None:
            self._values["scan_listener_port_tls"] = scan_listener_port_tls
        if tags is not None:
            self._values["tags"] = tags
        if time_zone is not None:
            self._values["time_zone"] = time_zone
        if total_container_databases is not None:
            self._values["total_container_databases"] = total_container_databases

    @builtins.property
    def autonomous_data_storage_size_in_t_bs(self) -> typing.Optional[jsii.Number]:
        '''The data storage size allocated for Autonomous Databases in the Autonomous VM cluster, in TB.

        Required when creating an Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-autonomousdatastoragesizeintbs
        '''
        result = self._values.get("autonomous_data_storage_size_in_t_bs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cloud_exadata_infrastructure_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the Cloud Exadata Infrastructure containing this Autonomous VM cluster.

        Required when creating an Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-cloudexadatainfrastructureid
        '''
        result = self._values.get("cloud_exadata_infrastructure_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_core_count_per_node(self) -> typing.Optional[jsii.Number]:
        '''The number of CPU cores enabled per node in the Autonomous VM cluster.

        Required when creating an Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-cpucorecountpernode
        '''
        result = self._values.get("cpu_core_count_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of database servers associated with the Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-dbservers
        '''
        result = self._values.get("db_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The user-provided description of the Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the Autonomous VM cluster.

        Required when creating an Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_mtls_enabled_vm_cluster(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether mutual TLS (mTLS) authentication is enabled for the Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-ismtlsenabledvmcluster
        '''
        result = self._values.get("is_mtls_enabled_vm_cluster")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def license_model(self) -> typing.Optional[builtins.str]:
        '''The Oracle license model that applies to the Autonomous VM cluster.

        Valid values are ``LICENSE_INCLUDED`` or ``BRING_YOUR_OWN_LICENSE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-licensemodel
        '''
        result = self._values.get("license_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudAutonomousVmClusterPropsMixin.MaintenanceWindowProperty"]]:
        '''The scheduling details for the maintenance window.

        Patching and system updates take place during the maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-maintenancewindow
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudAutonomousVmClusterPropsMixin.MaintenanceWindowProperty"]], result)

    @builtins.property
    def memory_per_oracle_compute_unit_in_g_bs(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory allocated per Oracle Compute Unit, in GB.

        Required when creating an Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-memoryperoraclecomputeunitingbs
        '''
        result = self._values.get("memory_per_oracle_compute_unit_in_g_bs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def odb_network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the ODB network associated with this Autonomous VM cluster.

        Required when creating an Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-odbnetworkid
        '''
        result = self._values.get("odb_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scan_listener_port_non_tls(self) -> typing.Optional[jsii.Number]:
        '''The SCAN listener port for non-TLS (TCP) protocol.

        The default is 1521.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-scanlistenerportnontls
        '''
        result = self._values.get("scan_listener_port_non_tls")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scan_listener_port_tls(self) -> typing.Optional[jsii.Number]:
        '''The SCAN listener port for TLS (TCP) protocol.

        The default is 2484.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-scanlistenerporttls
        '''
        result = self._values.get("scan_listener_port_tls")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the Autonomous Vm Cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone of the Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-timezone
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def total_container_databases(self) -> typing.Optional[jsii.Number]:
        '''The total number of Autonomous Container Databases that can be created with the allocated local storage.

        Required when creating an Autonomous VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html#cfn-odb-cloudautonomousvmcluster-totalcontainerdatabases
        '''
        result = self._values.get("total_container_databases")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCloudAutonomousVmClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCloudAutonomousVmClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudAutonomousVmClusterPropsMixin",
):
    '''The ``AWS::ODB::CloudAutonomousVmCluster`` resource creates an Autonomous VM cluster.

    An Autonomous VM cluster provides the infrastructure for running Autonomous Databases.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudautonomousvmcluster.html
    :cloudformationResource: AWS::ODB::CloudAutonomousVmCluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
        
        cfn_cloud_autonomous_vm_cluster_props_mixin = odb_mixins.CfnCloudAutonomousVmClusterPropsMixin(odb_mixins.CfnCloudAutonomousVmClusterMixinProps(
            autonomous_data_storage_size_in_tBs=123,
            cloud_exadata_infrastructure_id="cloudExadataInfrastructureId",
            cpu_core_count_per_node=123,
            db_servers=["dbServers"],
            description="description",
            display_name="displayName",
            is_mtls_enabled_vm_cluster=False,
            license_model="licenseModel",
            maintenance_window=odb_mixins.CfnCloudAutonomousVmClusterPropsMixin.MaintenanceWindowProperty(
                days_of_week=["daysOfWeek"],
                hours_of_day=[123],
                lead_time_in_weeks=123,
                months=["months"],
                preference="preference",
                weeks_of_month=[123]
            ),
            memory_per_oracle_compute_unit_in_gBs=123,
            odb_network_id="odbNetworkId",
            scan_listener_port_non_tls=123,
            scan_listener_port_tls=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            time_zone="timeZone",
            total_container_databases=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCloudAutonomousVmClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ODB::CloudAutonomousVmCluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0f170196c751776269e4e1ee5b606b98d13fffdf7271bbf9502c9b5208f97d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14b1ab0ed8203088dc382c9d797ea54610ea2ea04c40f781b8c151f10b6fd35e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb28d3d8ab1837a8c01d9465697ace00505320c4ca38851733938c9ca80746d0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCloudAutonomousVmClusterMixinProps:
        return typing.cast(CfnCloudAutonomousVmClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudAutonomousVmClusterPropsMixin.MaintenanceWindowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "days_of_week": "daysOfWeek",
            "hours_of_day": "hoursOfDay",
            "lead_time_in_weeks": "leadTimeInWeeks",
            "months": "months",
            "preference": "preference",
            "weeks_of_month": "weeksOfMonth",
        },
    )
    class MaintenanceWindowProperty:
        def __init__(
            self,
            *,
            days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
            hours_of_day: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            lead_time_in_weeks: typing.Optional[jsii.Number] = None,
            months: typing.Optional[typing.Sequence[builtins.str]] = None,
            preference: typing.Optional[builtins.str] = None,
            weeks_of_month: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The scheduling details for the maintenance window.

            Patching and system updates take place during the maintenance window.

            :param days_of_week: The days of the week when maintenance can be performed.
            :param hours_of_day: The hours of the day when maintenance can be performed.
            :param lead_time_in_weeks: The lead time in weeks before the maintenance window.
            :param months: The months when maintenance can be performed.
            :param preference: The preference for the maintenance window scheduling.
            :param weeks_of_month: The weeks of the month when maintenance can be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudautonomousvmcluster-maintenancewindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
                
                maintenance_window_property = odb_mixins.CfnCloudAutonomousVmClusterPropsMixin.MaintenanceWindowProperty(
                    days_of_week=["daysOfWeek"],
                    hours_of_day=[123],
                    lead_time_in_weeks=123,
                    months=["months"],
                    preference="preference",
                    weeks_of_month=[123]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c3cd66a28683c7169ee1c07653d553826d44206e12d498956432bcf8c01e245)
                check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
                check_type(argname="argument hours_of_day", value=hours_of_day, expected_type=type_hints["hours_of_day"])
                check_type(argname="argument lead_time_in_weeks", value=lead_time_in_weeks, expected_type=type_hints["lead_time_in_weeks"])
                check_type(argname="argument months", value=months, expected_type=type_hints["months"])
                check_type(argname="argument preference", value=preference, expected_type=type_hints["preference"])
                check_type(argname="argument weeks_of_month", value=weeks_of_month, expected_type=type_hints["weeks_of_month"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days_of_week is not None:
                self._values["days_of_week"] = days_of_week
            if hours_of_day is not None:
                self._values["hours_of_day"] = hours_of_day
            if lead_time_in_weeks is not None:
                self._values["lead_time_in_weeks"] = lead_time_in_weeks
            if months is not None:
                self._values["months"] = months
            if preference is not None:
                self._values["preference"] = preference
            if weeks_of_month is not None:
                self._values["weeks_of_month"] = weeks_of_month

        @builtins.property
        def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The days of the week when maintenance can be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudautonomousvmcluster-maintenancewindow.html#cfn-odb-cloudautonomousvmcluster-maintenancewindow-daysofweek
            '''
            result = self._values.get("days_of_week")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def hours_of_day(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''The hours of the day when maintenance can be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudautonomousvmcluster-maintenancewindow.html#cfn-odb-cloudautonomousvmcluster-maintenancewindow-hoursofday
            '''
            result = self._values.get("hours_of_day")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def lead_time_in_weeks(self) -> typing.Optional[jsii.Number]:
            '''The lead time in weeks before the maintenance window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudautonomousvmcluster-maintenancewindow.html#cfn-odb-cloudautonomousvmcluster-maintenancewindow-leadtimeinweeks
            '''
            result = self._values.get("lead_time_in_weeks")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def months(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The months when maintenance can be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudautonomousvmcluster-maintenancewindow.html#cfn-odb-cloudautonomousvmcluster-maintenancewindow-months
            '''
            result = self._values.get("months")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def preference(self) -> typing.Optional[builtins.str]:
            '''The preference for the maintenance window scheduling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudautonomousvmcluster-maintenancewindow.html#cfn-odb-cloudautonomousvmcluster-maintenancewindow-preference
            '''
            result = self._values.get("preference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weeks_of_month(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''The weeks of the month when maintenance can be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudautonomousvmcluster-maintenancewindow.html#cfn-odb-cloudautonomousvmcluster-maintenancewindow-weeksofmonth
            '''
            result = self._values.get("weeks_of_month")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudExadataInfrastructureMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "availability_zone_id": "availabilityZoneId",
        "compute_count": "computeCount",
        "customer_contacts_to_send_to_oci": "customerContactsToSendToOci",
        "database_server_type": "databaseServerType",
        "display_name": "displayName",
        "maintenance_window": "maintenanceWindow",
        "shape": "shape",
        "storage_count": "storageCount",
        "storage_server_type": "storageServerType",
        "tags": "tags",
    },
)
class CfnCloudExadataInfrastructureMixinProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        availability_zone_id: typing.Optional[builtins.str] = None,
        compute_count: typing.Optional[jsii.Number] = None,
        customer_contacts_to_send_to_oci: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudExadataInfrastructurePropsMixin.CustomerContactProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        database_server_type: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudExadataInfrastructurePropsMixin.MaintenanceWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        shape: typing.Optional[builtins.str] = None,
        storage_count: typing.Optional[jsii.Number] = None,
        storage_server_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCloudExadataInfrastructurePropsMixin.

        :param availability_zone: The name of the Availability Zone (AZ) where the Exadata infrastructure is located. Required when creating an Exadata infrastructure. Specify either AvailabilityZone or AvailabilityZoneId to define the location of the infrastructure.
        :param availability_zone_id: The AZ ID of the AZ where the Exadata infrastructure is located. Required when creating an Exadata infrastructure. Specify either AvailabilityZone or AvailabilityZoneId to define the location of the infrastructure.
        :param compute_count: The number of database servers for the Exadata infrastructure. Required when creating an Exadata infrastructure.
        :param customer_contacts_to_send_to_oci: The email addresses of contacts to receive notification from Oracle about maintenance updates for the Exadata infrastructure.
        :param database_server_type: The database server model type of the Exadata infrastructure. For the list of valid model names, use the ``ListDbSystemShapes`` operation.
        :param display_name: The user-friendly name for the Exadata infrastructure. Required when creating an Exadata infrastructure.
        :param maintenance_window: The scheduling details for the maintenance window. Patching and system updates take place during the maintenance window.
        :param shape: The model name of the Exadata infrastructure. Required when creating an Exadata infrastructure.
        :param storage_count: The number of storage servers that are activated for the Exadata infrastructure. Required when creating an Exadata infrastructure.
        :param storage_server_type: The storage server model type of the Exadata infrastructure. For the list of valid model names, use the ``ListDbSystemShapes`` operation.
        :param tags: Tags to assign to the Exadata Infrastructure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
            
            cfn_cloud_exadata_infrastructure_mixin_props = odb_mixins.CfnCloudExadataInfrastructureMixinProps(
                availability_zone="availabilityZone",
                availability_zone_id="availabilityZoneId",
                compute_count=123,
                customer_contacts_to_send_to_oci=[odb_mixins.CfnCloudExadataInfrastructurePropsMixin.CustomerContactProperty(
                    email="email"
                )],
                database_server_type="databaseServerType",
                display_name="displayName",
                maintenance_window=odb_mixins.CfnCloudExadataInfrastructurePropsMixin.MaintenanceWindowProperty(
                    custom_action_timeout_in_mins=123,
                    days_of_week=["daysOfWeek"],
                    hours_of_day=[123],
                    is_custom_action_timeout_enabled=False,
                    lead_time_in_weeks=123,
                    months=["months"],
                    patching_mode="patchingMode",
                    preference="preference",
                    weeks_of_month=[123]
                ),
                shape="shape",
                storage_count=123,
                storage_server_type="storageServerType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3d757ac8ffaba8f68dd30b8b38a0a9ccdbe364dfe55e0d55c016ccd2f1265a)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument availability_zone_id", value=availability_zone_id, expected_type=type_hints["availability_zone_id"])
            check_type(argname="argument compute_count", value=compute_count, expected_type=type_hints["compute_count"])
            check_type(argname="argument customer_contacts_to_send_to_oci", value=customer_contacts_to_send_to_oci, expected_type=type_hints["customer_contacts_to_send_to_oci"])
            check_type(argname="argument database_server_type", value=database_server_type, expected_type=type_hints["database_server_type"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument shape", value=shape, expected_type=type_hints["shape"])
            check_type(argname="argument storage_count", value=storage_count, expected_type=type_hints["storage_count"])
            check_type(argname="argument storage_server_type", value=storage_server_type, expected_type=type_hints["storage_server_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if availability_zone_id is not None:
            self._values["availability_zone_id"] = availability_zone_id
        if compute_count is not None:
            self._values["compute_count"] = compute_count
        if customer_contacts_to_send_to_oci is not None:
            self._values["customer_contacts_to_send_to_oci"] = customer_contacts_to_send_to_oci
        if database_server_type is not None:
            self._values["database_server_type"] = database_server_type
        if display_name is not None:
            self._values["display_name"] = display_name
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if shape is not None:
            self._values["shape"] = shape
        if storage_count is not None:
            self._values["storage_count"] = storage_count
        if storage_server_type is not None:
            self._values["storage_server_type"] = storage_server_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The name of the Availability Zone (AZ) where the Exadata infrastructure is located.

        Required when creating an Exadata infrastructure. Specify either AvailabilityZone or AvailabilityZoneId to define the location of the infrastructure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def availability_zone_id(self) -> typing.Optional[builtins.str]:
        '''The AZ ID of the AZ where the Exadata infrastructure is located.

        Required when creating an Exadata infrastructure. Specify either AvailabilityZone or AvailabilityZoneId to define the location of the infrastructure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-availabilityzoneid
        '''
        result = self._values.get("availability_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_count(self) -> typing.Optional[jsii.Number]:
        '''The number of database servers for the Exadata infrastructure.

        Required when creating an Exadata infrastructure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-computecount
        '''
        result = self._values.get("compute_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def customer_contacts_to_send_to_oci(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudExadataInfrastructurePropsMixin.CustomerContactProperty"]]]]:
        '''The email addresses of contacts to receive notification from Oracle about maintenance updates for the Exadata infrastructure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-customercontactstosendtooci
        '''
        result = self._values.get("customer_contacts_to_send_to_oci")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudExadataInfrastructurePropsMixin.CustomerContactProperty"]]]], result)

    @builtins.property
    def database_server_type(self) -> typing.Optional[builtins.str]:
        '''The database server model type of the Exadata infrastructure.

        For the list of valid model names, use the ``ListDbSystemShapes`` operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-databaseservertype
        '''
        result = self._values.get("database_server_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name for the Exadata infrastructure.

        Required when creating an Exadata infrastructure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudExadataInfrastructurePropsMixin.MaintenanceWindowProperty"]]:
        '''The scheduling details for the maintenance window.

        Patching and system updates take place during the maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-maintenancewindow
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudExadataInfrastructurePropsMixin.MaintenanceWindowProperty"]], result)

    @builtins.property
    def shape(self) -> typing.Optional[builtins.str]:
        '''The model name of the Exadata infrastructure.

        Required when creating an Exadata infrastructure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-shape
        '''
        result = self._values.get("shape")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_count(self) -> typing.Optional[jsii.Number]:
        '''The number of storage servers that are activated for the Exadata infrastructure.

        Required when creating an Exadata infrastructure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-storagecount
        '''
        result = self._values.get("storage_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_server_type(self) -> typing.Optional[builtins.str]:
        '''The storage server model type of the Exadata infrastructure.

        For the list of valid model names, use the ``ListDbSystemShapes`` operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-storageservertype
        '''
        result = self._values.get("storage_server_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the Exadata Infrastructure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html#cfn-odb-cloudexadatainfrastructure-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCloudExadataInfrastructureMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCloudExadataInfrastructurePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudExadataInfrastructurePropsMixin",
):
    '''The ``AWS::ODB::CloudExadataInfrastructure`` resource creates an Exadata infrastructure.

    An Exadata infrastructure provides the underlying compute and storage resources for Oracle Database workloads.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudexadatainfrastructure.html
    :cloudformationResource: AWS::ODB::CloudExadataInfrastructure
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
        
        cfn_cloud_exadata_infrastructure_props_mixin = odb_mixins.CfnCloudExadataInfrastructurePropsMixin(odb_mixins.CfnCloudExadataInfrastructureMixinProps(
            availability_zone="availabilityZone",
            availability_zone_id="availabilityZoneId",
            compute_count=123,
            customer_contacts_to_send_to_oci=[odb_mixins.CfnCloudExadataInfrastructurePropsMixin.CustomerContactProperty(
                email="email"
            )],
            database_server_type="databaseServerType",
            display_name="displayName",
            maintenance_window=odb_mixins.CfnCloudExadataInfrastructurePropsMixin.MaintenanceWindowProperty(
                custom_action_timeout_in_mins=123,
                days_of_week=["daysOfWeek"],
                hours_of_day=[123],
                is_custom_action_timeout_enabled=False,
                lead_time_in_weeks=123,
                months=["months"],
                patching_mode="patchingMode",
                preference="preference",
                weeks_of_month=[123]
            ),
            shape="shape",
            storage_count=123,
            storage_server_type="storageServerType",
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
        props: typing.Union[CfnCloudExadataInfrastructureMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ODB::CloudExadataInfrastructure``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d70ccb9d2215718bb919112bbe211426a6ba35462044150257dea6bfb5f98d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dba9692774d15deaedd36c1e67357bfd66efe7c98b2ed248a05b96025d55096d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48785dc20737288f4a9eece5c7307881f6c7fff010ead367cc23810389a7599a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCloudExadataInfrastructureMixinProps:
        return typing.cast(CfnCloudExadataInfrastructureMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudExadataInfrastructurePropsMixin.CustomerContactProperty",
        jsii_struct_bases=[],
        name_mapping={"email": "email"},
    )
    class CustomerContactProperty:
        def __init__(self, *, email: typing.Optional[builtins.str] = None) -> None:
            '''A contact to receive notification from Oracle about maintenance updates for a specific Exadata infrastructure.

            :param email: The email address of the contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-customercontact.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
                
                customer_contact_property = odb_mixins.CfnCloudExadataInfrastructurePropsMixin.CustomerContactProperty(
                    email="email"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec039dbd487c8faf6e9427b0433afae7faa63e45a3791ae165aeb6691a427fcb)
                check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email is not None:
                self._values["email"] = email

        @builtins.property
        def email(self) -> typing.Optional[builtins.str]:
            '''The email address of the contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-customercontact.html#cfn-odb-cloudexadatainfrastructure-customercontact-email
            '''
            result = self._values.get("email")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerContactProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudExadataInfrastructurePropsMixin.MaintenanceWindowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_action_timeout_in_mins": "customActionTimeoutInMins",
            "days_of_week": "daysOfWeek",
            "hours_of_day": "hoursOfDay",
            "is_custom_action_timeout_enabled": "isCustomActionTimeoutEnabled",
            "lead_time_in_weeks": "leadTimeInWeeks",
            "months": "months",
            "patching_mode": "patchingMode",
            "preference": "preference",
            "weeks_of_month": "weeksOfMonth",
        },
    )
    class MaintenanceWindowProperty:
        def __init__(
            self,
            *,
            custom_action_timeout_in_mins: typing.Optional[jsii.Number] = None,
            days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
            hours_of_day: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            is_custom_action_timeout_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            lead_time_in_weeks: typing.Optional[jsii.Number] = None,
            months: typing.Optional[typing.Sequence[builtins.str]] = None,
            patching_mode: typing.Optional[builtins.str] = None,
            preference: typing.Optional[builtins.str] = None,
            weeks_of_month: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The scheduling details for the maintenance window.

            Patching and system updates take place during the maintenance window.

            :param custom_action_timeout_in_mins: The custom action timeout in minutes for the maintenance window.
            :param days_of_week: The days of the week when maintenance can be performed.
            :param hours_of_day: The hours of the day when maintenance can be performed.
            :param is_custom_action_timeout_enabled: Indicates whether custom action timeout is enabled for the maintenance window.
            :param lead_time_in_weeks: The lead time in weeks before the maintenance window.
            :param months: The months when maintenance can be performed.
            :param patching_mode: The patching mode for the maintenance window.
            :param preference: The preference for the maintenance window scheduling.
            :param weeks_of_month: The weeks of the month when maintenance can be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-maintenancewindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
                
                maintenance_window_property = odb_mixins.CfnCloudExadataInfrastructurePropsMixin.MaintenanceWindowProperty(
                    custom_action_timeout_in_mins=123,
                    days_of_week=["daysOfWeek"],
                    hours_of_day=[123],
                    is_custom_action_timeout_enabled=False,
                    lead_time_in_weeks=123,
                    months=["months"],
                    patching_mode="patchingMode",
                    preference="preference",
                    weeks_of_month=[123]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__789fb64928707181b1ddba7a990079d77561f32cf5eb4b227dc5c99d73a5d75b)
                check_type(argname="argument custom_action_timeout_in_mins", value=custom_action_timeout_in_mins, expected_type=type_hints["custom_action_timeout_in_mins"])
                check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
                check_type(argname="argument hours_of_day", value=hours_of_day, expected_type=type_hints["hours_of_day"])
                check_type(argname="argument is_custom_action_timeout_enabled", value=is_custom_action_timeout_enabled, expected_type=type_hints["is_custom_action_timeout_enabled"])
                check_type(argname="argument lead_time_in_weeks", value=lead_time_in_weeks, expected_type=type_hints["lead_time_in_weeks"])
                check_type(argname="argument months", value=months, expected_type=type_hints["months"])
                check_type(argname="argument patching_mode", value=patching_mode, expected_type=type_hints["patching_mode"])
                check_type(argname="argument preference", value=preference, expected_type=type_hints["preference"])
                check_type(argname="argument weeks_of_month", value=weeks_of_month, expected_type=type_hints["weeks_of_month"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_action_timeout_in_mins is not None:
                self._values["custom_action_timeout_in_mins"] = custom_action_timeout_in_mins
            if days_of_week is not None:
                self._values["days_of_week"] = days_of_week
            if hours_of_day is not None:
                self._values["hours_of_day"] = hours_of_day
            if is_custom_action_timeout_enabled is not None:
                self._values["is_custom_action_timeout_enabled"] = is_custom_action_timeout_enabled
            if lead_time_in_weeks is not None:
                self._values["lead_time_in_weeks"] = lead_time_in_weeks
            if months is not None:
                self._values["months"] = months
            if patching_mode is not None:
                self._values["patching_mode"] = patching_mode
            if preference is not None:
                self._values["preference"] = preference
            if weeks_of_month is not None:
                self._values["weeks_of_month"] = weeks_of_month

        @builtins.property
        def custom_action_timeout_in_mins(self) -> typing.Optional[jsii.Number]:
            '''The custom action timeout in minutes for the maintenance window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-maintenancewindow.html#cfn-odb-cloudexadatainfrastructure-maintenancewindow-customactiontimeoutinmins
            '''
            result = self._values.get("custom_action_timeout_in_mins")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The days of the week when maintenance can be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-maintenancewindow.html#cfn-odb-cloudexadatainfrastructure-maintenancewindow-daysofweek
            '''
            result = self._values.get("days_of_week")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def hours_of_day(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''The hours of the day when maintenance can be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-maintenancewindow.html#cfn-odb-cloudexadatainfrastructure-maintenancewindow-hoursofday
            '''
            result = self._values.get("hours_of_day")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def is_custom_action_timeout_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether custom action timeout is enabled for the maintenance window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-maintenancewindow.html#cfn-odb-cloudexadatainfrastructure-maintenancewindow-iscustomactiontimeoutenabled
            '''
            result = self._values.get("is_custom_action_timeout_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def lead_time_in_weeks(self) -> typing.Optional[jsii.Number]:
            '''The lead time in weeks before the maintenance window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-maintenancewindow.html#cfn-odb-cloudexadatainfrastructure-maintenancewindow-leadtimeinweeks
            '''
            result = self._values.get("lead_time_in_weeks")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def months(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The months when maintenance can be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-maintenancewindow.html#cfn-odb-cloudexadatainfrastructure-maintenancewindow-months
            '''
            result = self._values.get("months")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def patching_mode(self) -> typing.Optional[builtins.str]:
            '''The patching mode for the maintenance window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-maintenancewindow.html#cfn-odb-cloudexadatainfrastructure-maintenancewindow-patchingmode
            '''
            result = self._values.get("patching_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preference(self) -> typing.Optional[builtins.str]:
            '''The preference for the maintenance window scheduling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-maintenancewindow.html#cfn-odb-cloudexadatainfrastructure-maintenancewindow-preference
            '''
            result = self._values.get("preference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weeks_of_month(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''The weeks of the month when maintenance can be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudexadatainfrastructure-maintenancewindow.html#cfn-odb-cloudexadatainfrastructure-maintenancewindow-weeksofmonth
            '''
            result = self._values.get("weeks_of_month")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudVmClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_exadata_infrastructure_id": "cloudExadataInfrastructureId",
        "cluster_name": "clusterName",
        "cpu_core_count": "cpuCoreCount",
        "data_collection_options": "dataCollectionOptions",
        "data_storage_size_in_t_bs": "dataStorageSizeInTBs",
        "db_nodes": "dbNodes",
        "db_node_storage_size_in_g_bs": "dbNodeStorageSizeInGBs",
        "db_servers": "dbServers",
        "display_name": "displayName",
        "gi_version": "giVersion",
        "hostname": "hostname",
        "is_local_backup_enabled": "isLocalBackupEnabled",
        "is_sparse_diskgroup_enabled": "isSparseDiskgroupEnabled",
        "license_model": "licenseModel",
        "memory_size_in_g_bs": "memorySizeInGBs",
        "odb_network_id": "odbNetworkId",
        "scan_listener_port_tcp": "scanListenerPortTcp",
        "ssh_public_keys": "sshPublicKeys",
        "system_version": "systemVersion",
        "tags": "tags",
        "time_zone": "timeZone",
    },
)
class CfnCloudVmClusterMixinProps:
    def __init__(
        self,
        *,
        cloud_exadata_infrastructure_id: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        cpu_core_count: typing.Optional[jsii.Number] = None,
        data_collection_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudVmClusterPropsMixin.DataCollectionOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_storage_size_in_t_bs: typing.Optional[jsii.Number] = None,
        db_nodes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudVmClusterPropsMixin.DbNodeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        db_node_storage_size_in_g_bs: typing.Optional[jsii.Number] = None,
        db_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gi_version: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
        is_local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        is_sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        license_model: typing.Optional[builtins.str] = None,
        memory_size_in_g_bs: typing.Optional[jsii.Number] = None,
        odb_network_id: typing.Optional[builtins.str] = None,
        scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        system_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCloudVmClusterPropsMixin.

        :param cloud_exadata_infrastructure_id: The unique identifier of the Exadata infrastructure that this VM cluster belongs to. Required when creating a VM cluster.
        :param cluster_name: The name of the Grid Infrastructure (GI) cluster.
        :param cpu_core_count: The number of CPU cores enabled on the VM cluster. Required when creating a VM cluster.
        :param data_collection_options: The set of diagnostic collection options enabled for the VM cluster.
        :param data_storage_size_in_t_bs: The size of the data disk group, in terabytes (TB), that's allocated for the VM cluster.
        :param db_nodes: The DB nodes that are implicitly created and managed as part of this VM Cluster.
        :param db_node_storage_size_in_g_bs: The amount of local node storage, in gigabytes (GB), that's allocated for the VM cluster.
        :param db_servers: The list of database servers for the VM cluster.
        :param display_name: The user-friendly name for the VM cluster. Required when creating a VM cluster.
        :param gi_version: The software version of the Oracle Grid Infrastructure (GI) for the VM cluster. Required when creating a VM cluster.
        :param hostname: The host name for the VM cluster. Required when creating a VM cluster.
        :param is_local_backup_enabled: Specifies whether database backups to local Exadata storage are enabled for the VM cluster.
        :param is_sparse_diskgroup_enabled: Specifies whether the VM cluster is configured with a sparse disk group.
        :param license_model: The Oracle license model applied to the VM cluster.
        :param memory_size_in_g_bs: The amount of memory, in gigabytes (GB), that's allocated for the VM cluster.
        :param odb_network_id: The unique identifier of the ODB network for the VM cluster. Required when creating a VM cluster.
        :param scan_listener_port_tcp: The port number for TCP connections to the single client access name (SCAN) listener. Valid values: ``1024–8999`` with the following exceptions: ``2484`` , ``6100`` , ``6200`` , ``7060`` , ``7070`` , ``7085`` , and ``7879`` Default: ``1521``
        :param ssh_public_keys: The public key portion of one or more key pairs used for SSH access to the VM cluster. Required when creating a VM cluster.
        :param system_version: The operating system version of the image chosen for the VM cluster.
        :param tags: Tags to assign to the Vm Cluster.
        :param time_zone: The time zone of the VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
            
            cfn_cloud_vm_cluster_mixin_props = odb_mixins.CfnCloudVmClusterMixinProps(
                cloud_exadata_infrastructure_id="cloudExadataInfrastructureId",
                cluster_name="clusterName",
                cpu_core_count=123,
                data_collection_options=odb_mixins.CfnCloudVmClusterPropsMixin.DataCollectionOptionsProperty(
                    is_diagnostics_events_enabled=False,
                    is_health_monitoring_enabled=False,
                    is_incident_logs_enabled=False
                ),
                data_storage_size_in_tBs=123,
                db_nodes=[odb_mixins.CfnCloudVmClusterPropsMixin.DbNodeProperty(
                    backup_ip_id="backupIpId",
                    backup_vnic2_id="backupVnic2Id",
                    cpu_core_count=123,
                    db_node_arn="dbNodeArn",
                    db_node_id="dbNodeId",
                    db_node_storage_size_in_gBs=123,
                    db_server_id="dbServerId",
                    db_system_id="dbSystemId",
                    host_ip_id="hostIpId",
                    hostname="hostname",
                    memory_size_in_gBs=123,
                    ocid="ocid",
                    status="status",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    vnic2_id="vnic2Id",
                    vnic_id="vnicId"
                )],
                db_node_storage_size_in_gBs=123,
                db_servers=["dbServers"],
                display_name="displayName",
                gi_version="giVersion",
                hostname="hostname",
                is_local_backup_enabled=False,
                is_sparse_diskgroup_enabled=False,
                license_model="licenseModel",
                memory_size_in_gBs=123,
                odb_network_id="odbNetworkId",
                scan_listener_port_tcp=123,
                ssh_public_keys=["sshPublicKeys"],
                system_version="systemVersion",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                time_zone="timeZone"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681939acaf5e4dacc4294795188b30becf4322b40ab04003972dd74e2dcb0735)
            check_type(argname="argument cloud_exadata_infrastructure_id", value=cloud_exadata_infrastructure_id, expected_type=type_hints["cloud_exadata_infrastructure_id"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument cpu_core_count", value=cpu_core_count, expected_type=type_hints["cpu_core_count"])
            check_type(argname="argument data_collection_options", value=data_collection_options, expected_type=type_hints["data_collection_options"])
            check_type(argname="argument data_storage_size_in_t_bs", value=data_storage_size_in_t_bs, expected_type=type_hints["data_storage_size_in_t_bs"])
            check_type(argname="argument db_nodes", value=db_nodes, expected_type=type_hints["db_nodes"])
            check_type(argname="argument db_node_storage_size_in_g_bs", value=db_node_storage_size_in_g_bs, expected_type=type_hints["db_node_storage_size_in_g_bs"])
            check_type(argname="argument db_servers", value=db_servers, expected_type=type_hints["db_servers"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gi_version", value=gi_version, expected_type=type_hints["gi_version"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument is_local_backup_enabled", value=is_local_backup_enabled, expected_type=type_hints["is_local_backup_enabled"])
            check_type(argname="argument is_sparse_diskgroup_enabled", value=is_sparse_diskgroup_enabled, expected_type=type_hints["is_sparse_diskgroup_enabled"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument memory_size_in_g_bs", value=memory_size_in_g_bs, expected_type=type_hints["memory_size_in_g_bs"])
            check_type(argname="argument odb_network_id", value=odb_network_id, expected_type=type_hints["odb_network_id"])
            check_type(argname="argument scan_listener_port_tcp", value=scan_listener_port_tcp, expected_type=type_hints["scan_listener_port_tcp"])
            check_type(argname="argument ssh_public_keys", value=ssh_public_keys, expected_type=type_hints["ssh_public_keys"])
            check_type(argname="argument system_version", value=system_version, expected_type=type_hints["system_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_exadata_infrastructure_id is not None:
            self._values["cloud_exadata_infrastructure_id"] = cloud_exadata_infrastructure_id
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if cpu_core_count is not None:
            self._values["cpu_core_count"] = cpu_core_count
        if data_collection_options is not None:
            self._values["data_collection_options"] = data_collection_options
        if data_storage_size_in_t_bs is not None:
            self._values["data_storage_size_in_t_bs"] = data_storage_size_in_t_bs
        if db_nodes is not None:
            self._values["db_nodes"] = db_nodes
        if db_node_storage_size_in_g_bs is not None:
            self._values["db_node_storage_size_in_g_bs"] = db_node_storage_size_in_g_bs
        if db_servers is not None:
            self._values["db_servers"] = db_servers
        if display_name is not None:
            self._values["display_name"] = display_name
        if gi_version is not None:
            self._values["gi_version"] = gi_version
        if hostname is not None:
            self._values["hostname"] = hostname
        if is_local_backup_enabled is not None:
            self._values["is_local_backup_enabled"] = is_local_backup_enabled
        if is_sparse_diskgroup_enabled is not None:
            self._values["is_sparse_diskgroup_enabled"] = is_sparse_diskgroup_enabled
        if license_model is not None:
            self._values["license_model"] = license_model
        if memory_size_in_g_bs is not None:
            self._values["memory_size_in_g_bs"] = memory_size_in_g_bs
        if odb_network_id is not None:
            self._values["odb_network_id"] = odb_network_id
        if scan_listener_port_tcp is not None:
            self._values["scan_listener_port_tcp"] = scan_listener_port_tcp
        if ssh_public_keys is not None:
            self._values["ssh_public_keys"] = ssh_public_keys
        if system_version is not None:
            self._values["system_version"] = system_version
        if tags is not None:
            self._values["tags"] = tags
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def cloud_exadata_infrastructure_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the Exadata infrastructure that this VM cluster belongs to.

        Required when creating a VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-cloudexadatainfrastructureid
        '''
        result = self._values.get("cloud_exadata_infrastructure_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Grid Infrastructure (GI) cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_core_count(self) -> typing.Optional[jsii.Number]:
        '''The number of CPU cores enabled on the VM cluster.

        Required when creating a VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-cpucorecount
        '''
        result = self._values.get("cpu_core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_collection_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudVmClusterPropsMixin.DataCollectionOptionsProperty"]]:
        '''The set of diagnostic collection options enabled for the VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-datacollectionoptions
        '''
        result = self._values.get("data_collection_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudVmClusterPropsMixin.DataCollectionOptionsProperty"]], result)

    @builtins.property
    def data_storage_size_in_t_bs(self) -> typing.Optional[jsii.Number]:
        '''The size of the data disk group, in terabytes (TB), that's allocated for the VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-datastoragesizeintbs
        '''
        result = self._values.get("data_storage_size_in_t_bs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_nodes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudVmClusterPropsMixin.DbNodeProperty"]]]]:
        '''The DB nodes that are implicitly created and managed as part of this VM Cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-dbnodes
        '''
        result = self._values.get("db_nodes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudVmClusterPropsMixin.DbNodeProperty"]]]], result)

    @builtins.property
    def db_node_storage_size_in_g_bs(self) -> typing.Optional[jsii.Number]:
        '''The amount of local node storage, in gigabytes (GB), that's allocated for the VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-dbnodestoragesizeingbs
        '''
        result = self._values.get("db_node_storage_size_in_g_bs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of database servers for the VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-dbservers
        '''
        result = self._values.get("db_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name for the VM cluster.

        Required when creating a VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gi_version(self) -> typing.Optional[builtins.str]:
        '''The software version of the Oracle Grid Infrastructure (GI) for the VM cluster.

        Required when creating a VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-giversion
        '''
        result = self._values.get("gi_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''The host name for the VM cluster.

        Required when creating a VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-hostname
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_local_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether database backups to local Exadata storage are enabled for the VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-islocalbackupenabled
        '''
        result = self._values.get("is_local_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def is_sparse_diskgroup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the VM cluster is configured with a sparse disk group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-issparsediskgroupenabled
        '''
        result = self._values.get("is_sparse_diskgroup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def license_model(self) -> typing.Optional[builtins.str]:
        '''The Oracle license model applied to the VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-licensemodel
        '''
        result = self._values.get("license_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_size_in_g_bs(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory, in gigabytes (GB), that's allocated for the VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-memorysizeingbs
        '''
        result = self._values.get("memory_size_in_g_bs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def odb_network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the ODB network for the VM cluster.

        Required when creating a VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-odbnetworkid
        '''
        result = self._values.get("odb_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scan_listener_port_tcp(self) -> typing.Optional[jsii.Number]:
        '''The port number for TCP connections to the single client access name (SCAN) listener.

        Valid values: ``1024–8999`` with the following exceptions: ``2484`` , ``6100`` , ``6200`` , ``7060`` , ``7070`` , ``7085`` , and ``7879``

        Default: ``1521``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-scanlistenerporttcp
        '''
        result = self._values.get("scan_listener_port_tcp")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssh_public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The public key portion of one or more key pairs used for SSH access to the VM cluster.

        Required when creating a VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-sshpublickeys
        '''
        result = self._values.get("ssh_public_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def system_version(self) -> typing.Optional[builtins.str]:
        '''The operating system version of the image chosen for the VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-systemversion
        '''
        result = self._values.get("system_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the Vm Cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone of the VM cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html#cfn-odb-cloudvmcluster-timezone
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCloudVmClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCloudVmClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudVmClusterPropsMixin",
):
    '''The ``AWS::ODB::CloudVmCluster`` resource creates a VM cluster on the specified Exadata infrastructure in the Oracle Database.

    A VM cluster provides the compute resources for Oracle Database workloads.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-cloudvmcluster.html
    :cloudformationResource: AWS::ODB::CloudVmCluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
        
        cfn_cloud_vm_cluster_props_mixin = odb_mixins.CfnCloudVmClusterPropsMixin(odb_mixins.CfnCloudVmClusterMixinProps(
            cloud_exadata_infrastructure_id="cloudExadataInfrastructureId",
            cluster_name="clusterName",
            cpu_core_count=123,
            data_collection_options=odb_mixins.CfnCloudVmClusterPropsMixin.DataCollectionOptionsProperty(
                is_diagnostics_events_enabled=False,
                is_health_monitoring_enabled=False,
                is_incident_logs_enabled=False
            ),
            data_storage_size_in_tBs=123,
            db_nodes=[odb_mixins.CfnCloudVmClusterPropsMixin.DbNodeProperty(
                backup_ip_id="backupIpId",
                backup_vnic2_id="backupVnic2Id",
                cpu_core_count=123,
                db_node_arn="dbNodeArn",
                db_node_id="dbNodeId",
                db_node_storage_size_in_gBs=123,
                db_server_id="dbServerId",
                db_system_id="dbSystemId",
                host_ip_id="hostIpId",
                hostname="hostname",
                memory_size_in_gBs=123,
                ocid="ocid",
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vnic2_id="vnic2Id",
                vnic_id="vnicId"
            )],
            db_node_storage_size_in_gBs=123,
            db_servers=["dbServers"],
            display_name="displayName",
            gi_version="giVersion",
            hostname="hostname",
            is_local_backup_enabled=False,
            is_sparse_diskgroup_enabled=False,
            license_model="licenseModel",
            memory_size_in_gBs=123,
            odb_network_id="odbNetworkId",
            scan_listener_port_tcp=123,
            ssh_public_keys=["sshPublicKeys"],
            system_version="systemVersion",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            time_zone="timeZone"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCloudVmClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ODB::CloudVmCluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e646df938caff63d6b665c723dd5c7af729c5ca63650df7377d428e2e472b3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9755257abf867fcec554a07bd8d0afa366ff0c7e934f2a8a1cbf0d899eee0d96)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50bd27574a00c4b78537d39020c0b6d6058893ff7c52d1ddc08810d33584249)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCloudVmClusterMixinProps:
        return typing.cast(CfnCloudVmClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudVmClusterPropsMixin.DataCollectionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "is_diagnostics_events_enabled": "isDiagnosticsEventsEnabled",
            "is_health_monitoring_enabled": "isHealthMonitoringEnabled",
            "is_incident_logs_enabled": "isIncidentLogsEnabled",
        },
    )
    class DataCollectionOptionsProperty:
        def __init__(
            self,
            *,
            is_diagnostics_events_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            is_health_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            is_incident_logs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Information about the data collection options enabled for a VM cluster.

            :param is_diagnostics_events_enabled: Specifies whether diagnostic collection is enabled for the VM cluster.
            :param is_health_monitoring_enabled: Specifies whether health monitoring is enabled for the VM cluster.
            :param is_incident_logs_enabled: Specifies whether incident logs are enabled for the VM cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-datacollectionoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
                
                data_collection_options_property = odb_mixins.CfnCloudVmClusterPropsMixin.DataCollectionOptionsProperty(
                    is_diagnostics_events_enabled=False,
                    is_health_monitoring_enabled=False,
                    is_incident_logs_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afeb7b82410bf8822e7970875f78d75f44169c65c9fa8b2b59baf7e5f2c337e0)
                check_type(argname="argument is_diagnostics_events_enabled", value=is_diagnostics_events_enabled, expected_type=type_hints["is_diagnostics_events_enabled"])
                check_type(argname="argument is_health_monitoring_enabled", value=is_health_monitoring_enabled, expected_type=type_hints["is_health_monitoring_enabled"])
                check_type(argname="argument is_incident_logs_enabled", value=is_incident_logs_enabled, expected_type=type_hints["is_incident_logs_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_diagnostics_events_enabled is not None:
                self._values["is_diagnostics_events_enabled"] = is_diagnostics_events_enabled
            if is_health_monitoring_enabled is not None:
                self._values["is_health_monitoring_enabled"] = is_health_monitoring_enabled
            if is_incident_logs_enabled is not None:
                self._values["is_incident_logs_enabled"] = is_incident_logs_enabled

        @builtins.property
        def is_diagnostics_events_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether diagnostic collection is enabled for the VM cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-datacollectionoptions.html#cfn-odb-cloudvmcluster-datacollectionoptions-isdiagnosticseventsenabled
            '''
            result = self._values.get("is_diagnostics_events_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def is_health_monitoring_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether health monitoring is enabled for the VM cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-datacollectionoptions.html#cfn-odb-cloudvmcluster-datacollectionoptions-ishealthmonitoringenabled
            '''
            result = self._values.get("is_health_monitoring_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def is_incident_logs_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether incident logs are enabled for the VM cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-datacollectionoptions.html#cfn-odb-cloudvmcluster-datacollectionoptions-isincidentlogsenabled
            '''
            result = self._values.get("is_incident_logs_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataCollectionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnCloudVmClusterPropsMixin.DbNodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backup_ip_id": "backupIpId",
            "backup_vnic2_id": "backupVnic2Id",
            "cpu_core_count": "cpuCoreCount",
            "db_node_arn": "dbNodeArn",
            "db_node_id": "dbNodeId",
            "db_node_storage_size_in_g_bs": "dbNodeStorageSizeInGBs",
            "db_server_id": "dbServerId",
            "db_system_id": "dbSystemId",
            "host_ip_id": "hostIpId",
            "hostname": "hostname",
            "memory_size_in_g_bs": "memorySizeInGBs",
            "ocid": "ocid",
            "status": "status",
            "tags": "tags",
            "vnic2_id": "vnic2Id",
            "vnic_id": "vnicId",
        },
    )
    class DbNodeProperty:
        def __init__(
            self,
            *,
            backup_ip_id: typing.Optional[builtins.str] = None,
            backup_vnic2_id: typing.Optional[builtins.str] = None,
            cpu_core_count: typing.Optional[jsii.Number] = None,
            db_node_arn: typing.Optional[builtins.str] = None,
            db_node_id: typing.Optional[builtins.str] = None,
            db_node_storage_size_in_g_bs: typing.Optional[jsii.Number] = None,
            db_server_id: typing.Optional[builtins.str] = None,
            db_system_id: typing.Optional[builtins.str] = None,
            host_ip_id: typing.Optional[builtins.str] = None,
            hostname: typing.Optional[builtins.str] = None,
            memory_size_in_g_bs: typing.Optional[jsii.Number] = None,
            ocid: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
            vnic2_id: typing.Optional[builtins.str] = None,
            vnic_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a DB node.

            :param backup_ip_id: The Oracle Cloud ID (OCID) of the backup IP address that's associated with the DB node.
            :param backup_vnic2_id: The OCID of the second backup VNIC.
            :param cpu_core_count: Number of CPU cores enabled on the DB node.
            :param db_node_arn: The Amazon Resource Name (ARN) of the DB node.
            :param db_node_id: The unique identifier of the DB node.
            :param db_node_storage_size_in_g_bs: The amount of local node storage, in gigabytes (GBs), that's allocated on the DB node.
            :param db_server_id: The unique identifier of the Db server that is associated with the DB node.
            :param db_system_id: The OCID of the DB system.
            :param host_ip_id: The OCID of the host IP address that's associated with the DB node.
            :param hostname: The host name for the DB node.
            :param memory_size_in_g_bs: The allocated memory in GBs on the DB node.
            :param ocid: The OCID of the DB node.
            :param status: The current status of the DB node.
            :param tags: 
            :param vnic2_id: The OCID of the second VNIC.
            :param vnic_id: The OCID of the VNIC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
                
                db_node_property = odb_mixins.CfnCloudVmClusterPropsMixin.DbNodeProperty(
                    backup_ip_id="backupIpId",
                    backup_vnic2_id="backupVnic2Id",
                    cpu_core_count=123,
                    db_node_arn="dbNodeArn",
                    db_node_id="dbNodeId",
                    db_node_storage_size_in_gBs=123,
                    db_server_id="dbServerId",
                    db_system_id="dbSystemId",
                    host_ip_id="hostIpId",
                    hostname="hostname",
                    memory_size_in_gBs=123,
                    ocid="ocid",
                    status="status",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    vnic2_id="vnic2Id",
                    vnic_id="vnicId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03a1101f812cb89e2a5aaf711d47fc2262567a9c907316e9920008119eb86ef3)
                check_type(argname="argument backup_ip_id", value=backup_ip_id, expected_type=type_hints["backup_ip_id"])
                check_type(argname="argument backup_vnic2_id", value=backup_vnic2_id, expected_type=type_hints["backup_vnic2_id"])
                check_type(argname="argument cpu_core_count", value=cpu_core_count, expected_type=type_hints["cpu_core_count"])
                check_type(argname="argument db_node_arn", value=db_node_arn, expected_type=type_hints["db_node_arn"])
                check_type(argname="argument db_node_id", value=db_node_id, expected_type=type_hints["db_node_id"])
                check_type(argname="argument db_node_storage_size_in_g_bs", value=db_node_storage_size_in_g_bs, expected_type=type_hints["db_node_storage_size_in_g_bs"])
                check_type(argname="argument db_server_id", value=db_server_id, expected_type=type_hints["db_server_id"])
                check_type(argname="argument db_system_id", value=db_system_id, expected_type=type_hints["db_system_id"])
                check_type(argname="argument host_ip_id", value=host_ip_id, expected_type=type_hints["host_ip_id"])
                check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
                check_type(argname="argument memory_size_in_g_bs", value=memory_size_in_g_bs, expected_type=type_hints["memory_size_in_g_bs"])
                check_type(argname="argument ocid", value=ocid, expected_type=type_hints["ocid"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument vnic2_id", value=vnic2_id, expected_type=type_hints["vnic2_id"])
                check_type(argname="argument vnic_id", value=vnic_id, expected_type=type_hints["vnic_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if backup_ip_id is not None:
                self._values["backup_ip_id"] = backup_ip_id
            if backup_vnic2_id is not None:
                self._values["backup_vnic2_id"] = backup_vnic2_id
            if cpu_core_count is not None:
                self._values["cpu_core_count"] = cpu_core_count
            if db_node_arn is not None:
                self._values["db_node_arn"] = db_node_arn
            if db_node_id is not None:
                self._values["db_node_id"] = db_node_id
            if db_node_storage_size_in_g_bs is not None:
                self._values["db_node_storage_size_in_g_bs"] = db_node_storage_size_in_g_bs
            if db_server_id is not None:
                self._values["db_server_id"] = db_server_id
            if db_system_id is not None:
                self._values["db_system_id"] = db_system_id
            if host_ip_id is not None:
                self._values["host_ip_id"] = host_ip_id
            if hostname is not None:
                self._values["hostname"] = hostname
            if memory_size_in_g_bs is not None:
                self._values["memory_size_in_g_bs"] = memory_size_in_g_bs
            if ocid is not None:
                self._values["ocid"] = ocid
            if status is not None:
                self._values["status"] = status
            if tags is not None:
                self._values["tags"] = tags
            if vnic2_id is not None:
                self._values["vnic2_id"] = vnic2_id
            if vnic_id is not None:
                self._values["vnic_id"] = vnic_id

        @builtins.property
        def backup_ip_id(self) -> typing.Optional[builtins.str]:
            '''The Oracle Cloud ID (OCID) of the backup IP address that's associated with the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-backupipid
            '''
            result = self._values.get("backup_ip_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def backup_vnic2_id(self) -> typing.Optional[builtins.str]:
            '''The OCID of the second backup VNIC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-backupvnic2id
            '''
            result = self._values.get("backup_vnic2_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cpu_core_count(self) -> typing.Optional[jsii.Number]:
            '''Number of CPU cores enabled on the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-cpucorecount
            '''
            result = self._values.get("cpu_core_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def db_node_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-dbnodearn
            '''
            result = self._values.get("db_node_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def db_node_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-dbnodeid
            '''
            result = self._values.get("db_node_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def db_node_storage_size_in_g_bs(self) -> typing.Optional[jsii.Number]:
            '''The amount of local node storage, in gigabytes (GBs), that's allocated on the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-dbnodestoragesizeingbs
            '''
            result = self._values.get("db_node_storage_size_in_g_bs")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def db_server_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the Db server that is associated with the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-dbserverid
            '''
            result = self._values.get("db_server_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def db_system_id(self) -> typing.Optional[builtins.str]:
            '''The OCID of the DB system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-dbsystemid
            '''
            result = self._values.get("db_system_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_ip_id(self) -> typing.Optional[builtins.str]:
            '''The OCID of the host IP address that's associated with the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-hostipid
            '''
            result = self._values.get("host_ip_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hostname(self) -> typing.Optional[builtins.str]:
            '''The host name for the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-hostname
            '''
            result = self._values.get("hostname")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory_size_in_g_bs(self) -> typing.Optional[jsii.Number]:
            '''The allocated memory in GBs on the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-memorysizeingbs
            '''
            result = self._values.get("memory_size_in_g_bs")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ocid(self) -> typing.Optional[builtins.str]:
            '''The OCID of the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-ocid
            '''
            result = self._values.get("ocid")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The current status of the DB node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        @builtins.property
        def vnic2_id(self) -> typing.Optional[builtins.str]:
            '''The OCID of the second VNIC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-vnic2id
            '''
            result = self._values.get("vnic2_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vnic_id(self) -> typing.Optional[builtins.str]:
            '''The OCID of the VNIC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-cloudvmcluster-dbnode.html#cfn-odb-cloudvmcluster-dbnode-vnicid
            '''
            result = self._values.get("vnic_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DbNodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnOdbNetworkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "availability_zone_id": "availabilityZoneId",
        "backup_subnet_cidr": "backupSubnetCidr",
        "client_subnet_cidr": "clientSubnetCidr",
        "custom_domain_name": "customDomainName",
        "default_dns_prefix": "defaultDnsPrefix",
        "delete_associated_resources": "deleteAssociatedResources",
        "display_name": "displayName",
        "s3_access": "s3Access",
        "s3_policy_document": "s3PolicyDocument",
        "tags": "tags",
        "zero_etl_access": "zeroEtlAccess",
    },
)
class CfnOdbNetworkMixinProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        availability_zone_id: typing.Optional[builtins.str] = None,
        backup_subnet_cidr: typing.Optional[builtins.str] = None,
        client_subnet_cidr: typing.Optional[builtins.str] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        default_dns_prefix: typing.Optional[builtins.str] = None,
        delete_associated_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        s3_access: typing.Optional[builtins.str] = None,
        s3_policy_document: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        zero_etl_access: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnOdbNetworkPropsMixin.

        :param availability_zone: The Availability Zone (AZ) where the ODB network is located. Required when creating an ODB network. Specify either AvailabilityZone or AvailabilityZoneId to define the location of the network.
        :param availability_zone_id: The AZ ID of the AZ where the ODB network is located. Required when creating an ODB network. Specify either AvailabilityZone or AvailabilityZoneId to define the location of the network.
        :param backup_subnet_cidr: The CIDR range of the backup subnet in the ODB network.
        :param client_subnet_cidr: The CIDR range of the client subnet in the ODB network. Required when creating an ODB network.
        :param custom_domain_name: The domain name for the resources in the ODB network.
        :param default_dns_prefix: The DNS prefix to the default DNS domain name. The default DNS domain name is oraclevcn.com.
        :param delete_associated_resources: Specifies whether to delete associated OCI networking resources along with the ODB network. Required when creating an ODB network.
        :param display_name: The user-friendly name of the ODB network. Required when creating an ODB network.
        :param s3_access: The configuration for Amazon S3 access from the ODB network.
        :param s3_policy_document: Specifies the endpoint policy for Amazon S3 access from the ODB network.
        :param tags: Tags to assign to the Odb Network.
        :param zero_etl_access: The configuration for Zero-ETL access from the ODB network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
            
            cfn_odb_network_mixin_props = odb_mixins.CfnOdbNetworkMixinProps(
                availability_zone="availabilityZone",
                availability_zone_id="availabilityZoneId",
                backup_subnet_cidr="backupSubnetCidr",
                client_subnet_cidr="clientSubnetCidr",
                custom_domain_name="customDomainName",
                default_dns_prefix="defaultDnsPrefix",
                delete_associated_resources=False,
                display_name="displayName",
                s3_access="s3Access",
                s3_policy_document="s3PolicyDocument",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                zero_etl_access="zeroEtlAccess"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4ee3b6291623a81990313a7525b2473ef87cb422b45c69815cfc6133e4fa4d)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument availability_zone_id", value=availability_zone_id, expected_type=type_hints["availability_zone_id"])
            check_type(argname="argument backup_subnet_cidr", value=backup_subnet_cidr, expected_type=type_hints["backup_subnet_cidr"])
            check_type(argname="argument client_subnet_cidr", value=client_subnet_cidr, expected_type=type_hints["client_subnet_cidr"])
            check_type(argname="argument custom_domain_name", value=custom_domain_name, expected_type=type_hints["custom_domain_name"])
            check_type(argname="argument default_dns_prefix", value=default_dns_prefix, expected_type=type_hints["default_dns_prefix"])
            check_type(argname="argument delete_associated_resources", value=delete_associated_resources, expected_type=type_hints["delete_associated_resources"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument s3_access", value=s3_access, expected_type=type_hints["s3_access"])
            check_type(argname="argument s3_policy_document", value=s3_policy_document, expected_type=type_hints["s3_policy_document"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zero_etl_access", value=zero_etl_access, expected_type=type_hints["zero_etl_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if availability_zone_id is not None:
            self._values["availability_zone_id"] = availability_zone_id
        if backup_subnet_cidr is not None:
            self._values["backup_subnet_cidr"] = backup_subnet_cidr
        if client_subnet_cidr is not None:
            self._values["client_subnet_cidr"] = client_subnet_cidr
        if custom_domain_name is not None:
            self._values["custom_domain_name"] = custom_domain_name
        if default_dns_prefix is not None:
            self._values["default_dns_prefix"] = default_dns_prefix
        if delete_associated_resources is not None:
            self._values["delete_associated_resources"] = delete_associated_resources
        if display_name is not None:
            self._values["display_name"] = display_name
        if s3_access is not None:
            self._values["s3_access"] = s3_access
        if s3_policy_document is not None:
            self._values["s3_policy_document"] = s3_policy_document
        if tags is not None:
            self._values["tags"] = tags
        if zero_etl_access is not None:
            self._values["zero_etl_access"] = zero_etl_access

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone (AZ) where the ODB network is located.

        Required when creating an ODB network. Specify either AvailabilityZone or AvailabilityZoneId to define the location of the network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def availability_zone_id(self) -> typing.Optional[builtins.str]:
        '''The AZ ID of the AZ where the ODB network is located.

        Required when creating an ODB network. Specify either AvailabilityZone or AvailabilityZoneId to define the location of the network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-availabilityzoneid
        '''
        result = self._values.get("availability_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_subnet_cidr(self) -> typing.Optional[builtins.str]:
        '''The CIDR range of the backup subnet in the ODB network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-backupsubnetcidr
        '''
        result = self._values.get("backup_subnet_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_subnet_cidr(self) -> typing.Optional[builtins.str]:
        '''The CIDR range of the client subnet in the ODB network.

        Required when creating an ODB network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-clientsubnetcidr
        '''
        result = self._values.get("client_subnet_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the resources in the ODB network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-customdomainname
        '''
        result = self._values.get("custom_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_dns_prefix(self) -> typing.Optional[builtins.str]:
        '''The DNS prefix to the default DNS domain name.

        The default DNS domain name is oraclevcn.com.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-defaultdnsprefix
        '''
        result = self._values.get("default_dns_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_associated_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to delete associated OCI networking resources along with the ODB network.

        Required when creating an ODB network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-deleteassociatedresources
        '''
        result = self._values.get("delete_associated_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name of the ODB network.

        Required when creating an ODB network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_access(self) -> typing.Optional[builtins.str]:
        '''The configuration for Amazon S3 access from the ODB network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-s3access
        '''
        result = self._values.get("s3_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_policy_document(self) -> typing.Optional[builtins.str]:
        '''Specifies the endpoint policy for Amazon S3 access from the ODB network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-s3policydocument
        '''
        result = self._values.get("s3_policy_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the Odb Network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def zero_etl_access(self) -> typing.Optional[builtins.str]:
        '''The configuration for Zero-ETL access from the ODB network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html#cfn-odb-odbnetwork-zeroetlaccess
        '''
        result = self._values.get("zero_etl_access")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOdbNetworkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOdbNetworkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnOdbNetworkPropsMixin",
):
    '''The ``AWS::ODB::OdbNetwork`` resource creates an ODB network.

    An ODB network provides the networking foundation for Oracle Database resources.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbnetwork.html
    :cloudformationResource: AWS::ODB::OdbNetwork
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
        
        cfn_odb_network_props_mixin = odb_mixins.CfnOdbNetworkPropsMixin(odb_mixins.CfnOdbNetworkMixinProps(
            availability_zone="availabilityZone",
            availability_zone_id="availabilityZoneId",
            backup_subnet_cidr="backupSubnetCidr",
            client_subnet_cidr="clientSubnetCidr",
            custom_domain_name="customDomainName",
            default_dns_prefix="defaultDnsPrefix",
            delete_associated_resources=False,
            display_name="displayName",
            s3_access="s3Access",
            s3_policy_document="s3PolicyDocument",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            zero_etl_access="zeroEtlAccess"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOdbNetworkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ODB::OdbNetwork``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd786f79a91b56f2f7ce0801c7a75e4436a851fa6e4751ddff02cbb4378c9f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92055987bbe30d602d9b57265b84321ddf2b6f5addaee5551a4bc8a8dc490f9a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a43428c745e47910197602e3f102ba1a8684f973618e27481e103d06cfd32b8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOdbNetworkMixinProps:
        return typing.cast(CfnOdbNetworkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnOdbNetworkPropsMixin.ManagedS3BackupAccessProperty",
        jsii_struct_bases=[],
        name_mapping={"ipv4_addresses": "ipv4Addresses", "status": "status"},
    )
    class ManagedS3BackupAccessProperty:
        def __init__(
            self,
            *,
            ipv4_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for managed Amazon S3 backup access from the ODB network.

            :param ipv4_addresses: The IPv4 addresses for the managed Amazon S3 backup access.
            :param status: The status of the managed Amazon S3 backup access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-manageds3backupaccess.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
                
                managed_s3_backup_access_property = odb_mixins.CfnOdbNetworkPropsMixin.ManagedS3BackupAccessProperty(
                    ipv4_addresses=["ipv4Addresses"],
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b7418b9aa72684f3c6e7f9f50358b87cf46ed52e41414900904c17786889912)
                check_type(argname="argument ipv4_addresses", value=ipv4_addresses, expected_type=type_hints["ipv4_addresses"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ipv4_addresses is not None:
                self._values["ipv4_addresses"] = ipv4_addresses
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def ipv4_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IPv4 addresses for the managed Amazon S3 backup access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-manageds3backupaccess.html#cfn-odb-odbnetwork-manageds3backupaccess-ipv4addresses
            '''
            result = self._values.get("ipv4_addresses")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the managed Amazon S3 backup access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-manageds3backupaccess.html#cfn-odb-odbnetwork-manageds3backupaccess-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedS3BackupAccessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnOdbNetworkPropsMixin.ManagedServicesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "managed_s3_backup_access": "managedS3BackupAccess",
            "managed_services_ipv4_cidrs": "managedServicesIpv4Cidrs",
            "resource_gateway_arn": "resourceGatewayArn",
            "s3_access": "s3Access",
            "service_network_arn": "serviceNetworkArn",
            "service_network_endpoint": "serviceNetworkEndpoint",
            "zero_etl_access": "zeroEtlAccess",
        },
    )
    class ManagedServicesProperty:
        def __init__(
            self,
            *,
            managed_s3_backup_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOdbNetworkPropsMixin.ManagedS3BackupAccessProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            managed_services_ipv4_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_gateway_arn: typing.Optional[builtins.str] = None,
            s3_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOdbNetworkPropsMixin.S3AccessProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_network_arn: typing.Optional[builtins.str] = None,
            service_network_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOdbNetworkPropsMixin.ServiceNetworkEndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            zero_etl_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOdbNetworkPropsMixin.ZeroEtlAccessProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The managed services configuration for the ODB network.

            :param managed_s3_backup_access: The managed Amazon S3 backup access configuration.
            :param managed_services_ipv4_cidrs: The IPv4 CIDR blocks for the managed services.
            :param resource_gateway_arn: The Amazon Resource Name (ARN) of the resource gateway.
            :param s3_access: The Amazon S3 access configuration.
            :param service_network_arn: The Amazon Resource Name (ARN) of the service network.
            :param service_network_endpoint: The service network endpoint configuration.
            :param zero_etl_access: The Zero-ETL access configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-managedservices.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
                
                managed_services_property = odb_mixins.CfnOdbNetworkPropsMixin.ManagedServicesProperty(
                    managed_s3_backup_access=odb_mixins.CfnOdbNetworkPropsMixin.ManagedS3BackupAccessProperty(
                        ipv4_addresses=["ipv4Addresses"],
                        status="status"
                    ),
                    managed_services_ipv4_cidrs=["managedServicesIpv4Cidrs"],
                    resource_gateway_arn="resourceGatewayArn",
                    s3_access=odb_mixins.CfnOdbNetworkPropsMixin.S3AccessProperty(
                        domain_name="domainName",
                        ipv4_addresses=["ipv4Addresses"],
                        s3_policy_document="s3PolicyDocument",
                        status="status"
                    ),
                    service_network_arn="serviceNetworkArn",
                    service_network_endpoint=odb_mixins.CfnOdbNetworkPropsMixin.ServiceNetworkEndpointProperty(
                        vpc_endpoint_id="vpcEndpointId",
                        vpc_endpoint_type="vpcEndpointType"
                    ),
                    zero_etl_access=odb_mixins.CfnOdbNetworkPropsMixin.ZeroEtlAccessProperty(
                        cidr="cidr",
                        status="status"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2147cacc5d75fd648850ab585f968edb34ff9fd15d4a0c2f711986664f0e438)
                check_type(argname="argument managed_s3_backup_access", value=managed_s3_backup_access, expected_type=type_hints["managed_s3_backup_access"])
                check_type(argname="argument managed_services_ipv4_cidrs", value=managed_services_ipv4_cidrs, expected_type=type_hints["managed_services_ipv4_cidrs"])
                check_type(argname="argument resource_gateway_arn", value=resource_gateway_arn, expected_type=type_hints["resource_gateway_arn"])
                check_type(argname="argument s3_access", value=s3_access, expected_type=type_hints["s3_access"])
                check_type(argname="argument service_network_arn", value=service_network_arn, expected_type=type_hints["service_network_arn"])
                check_type(argname="argument service_network_endpoint", value=service_network_endpoint, expected_type=type_hints["service_network_endpoint"])
                check_type(argname="argument zero_etl_access", value=zero_etl_access, expected_type=type_hints["zero_etl_access"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if managed_s3_backup_access is not None:
                self._values["managed_s3_backup_access"] = managed_s3_backup_access
            if managed_services_ipv4_cidrs is not None:
                self._values["managed_services_ipv4_cidrs"] = managed_services_ipv4_cidrs
            if resource_gateway_arn is not None:
                self._values["resource_gateway_arn"] = resource_gateway_arn
            if s3_access is not None:
                self._values["s3_access"] = s3_access
            if service_network_arn is not None:
                self._values["service_network_arn"] = service_network_arn
            if service_network_endpoint is not None:
                self._values["service_network_endpoint"] = service_network_endpoint
            if zero_etl_access is not None:
                self._values["zero_etl_access"] = zero_etl_access

        @builtins.property
        def managed_s3_backup_access(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOdbNetworkPropsMixin.ManagedS3BackupAccessProperty"]]:
            '''The managed Amazon S3 backup access configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-managedservices.html#cfn-odb-odbnetwork-managedservices-manageds3backupaccess
            '''
            result = self._values.get("managed_s3_backup_access")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOdbNetworkPropsMixin.ManagedS3BackupAccessProperty"]], result)

        @builtins.property
        def managed_services_ipv4_cidrs(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The IPv4 CIDR blocks for the managed services.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-managedservices.html#cfn-odb-odbnetwork-managedservices-managedservicesipv4cidrs
            '''
            result = self._values.get("managed_services_ipv4_cidrs")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_gateway_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the resource gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-managedservices.html#cfn-odb-odbnetwork-managedservices-resourcegatewayarn
            '''
            result = self._values.get("resource_gateway_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_access(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOdbNetworkPropsMixin.S3AccessProperty"]]:
            '''The Amazon S3 access configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-managedservices.html#cfn-odb-odbnetwork-managedservices-s3access
            '''
            result = self._values.get("s3_access")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOdbNetworkPropsMixin.S3AccessProperty"]], result)

        @builtins.property
        def service_network_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the service network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-managedservices.html#cfn-odb-odbnetwork-managedservices-servicenetworkarn
            '''
            result = self._values.get("service_network_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_network_endpoint(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOdbNetworkPropsMixin.ServiceNetworkEndpointProperty"]]:
            '''The service network endpoint configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-managedservices.html#cfn-odb-odbnetwork-managedservices-servicenetworkendpoint
            '''
            result = self._values.get("service_network_endpoint")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOdbNetworkPropsMixin.ServiceNetworkEndpointProperty"]], result)

        @builtins.property
        def zero_etl_access(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOdbNetworkPropsMixin.ZeroEtlAccessProperty"]]:
            '''The Zero-ETL access configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-managedservices.html#cfn-odb-odbnetwork-managedservices-zeroetlaccess
            '''
            result = self._values.get("zero_etl_access")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOdbNetworkPropsMixin.ZeroEtlAccessProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedServicesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnOdbNetworkPropsMixin.S3AccessProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_name": "domainName",
            "ipv4_addresses": "ipv4Addresses",
            "s3_policy_document": "s3PolicyDocument",
            "status": "status",
        },
    )
    class S3AccessProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            ipv4_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
            s3_policy_document: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for Amazon S3 access from the ODB network.

            :param domain_name: The domain name for the Amazon S3 access.
            :param ipv4_addresses: The IPv4 addresses for the Amazon S3 access.
            :param s3_policy_document: The endpoint policy for the Amazon S3 access.
            :param status: The status of the Amazon S3 access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-s3access.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
                
                s3_access_property = odb_mixins.CfnOdbNetworkPropsMixin.S3AccessProperty(
                    domain_name="domainName",
                    ipv4_addresses=["ipv4Addresses"],
                    s3_policy_document="s3PolicyDocument",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5dabf95f03cd393382600edefdc8eaca81d6842dd0293a1b4a058b747bd45269)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument ipv4_addresses", value=ipv4_addresses, expected_type=type_hints["ipv4_addresses"])
                check_type(argname="argument s3_policy_document", value=s3_policy_document, expected_type=type_hints["s3_policy_document"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if ipv4_addresses is not None:
                self._values["ipv4_addresses"] = ipv4_addresses
            if s3_policy_document is not None:
                self._values["s3_policy_document"] = s3_policy_document
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The domain name for the Amazon S3 access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-s3access.html#cfn-odb-odbnetwork-s3access-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ipv4_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IPv4 addresses for the Amazon S3 access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-s3access.html#cfn-odb-odbnetwork-s3access-ipv4addresses
            '''
            result = self._values.get("ipv4_addresses")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def s3_policy_document(self) -> typing.Optional[builtins.str]:
            '''The endpoint policy for the Amazon S3 access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-s3access.html#cfn-odb-odbnetwork-s3access-s3policydocument
            '''
            result = self._values.get("s3_policy_document")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the Amazon S3 access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-s3access.html#cfn-odb-odbnetwork-s3access-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3AccessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnOdbNetworkPropsMixin.ServiceNetworkEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "vpc_endpoint_id": "vpcEndpointId",
            "vpc_endpoint_type": "vpcEndpointType",
        },
    )
    class ServiceNetworkEndpointProperty:
        def __init__(
            self,
            *,
            vpc_endpoint_id: typing.Optional[builtins.str] = None,
            vpc_endpoint_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for a service network endpoint.

            :param vpc_endpoint_id: The identifier of the VPC endpoint.
            :param vpc_endpoint_type: The type of the VPC endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-servicenetworkendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
                
                service_network_endpoint_property = odb_mixins.CfnOdbNetworkPropsMixin.ServiceNetworkEndpointProperty(
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_endpoint_type="vpcEndpointType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5a7ebe33fa93aca66d3afa873ad7cbc5d75ed104cf7ef47260fcd4257caa964)
                check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
                check_type(argname="argument vpc_endpoint_type", value=vpc_endpoint_type, expected_type=type_hints["vpc_endpoint_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_endpoint_id is not None:
                self._values["vpc_endpoint_id"] = vpc_endpoint_id
            if vpc_endpoint_type is not None:
                self._values["vpc_endpoint_type"] = vpc_endpoint_type

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the VPC endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-servicenetworkendpoint.html#cfn-odb-odbnetwork-servicenetworkendpoint-vpcendpointid
            '''
            result = self._values.get("vpc_endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_endpoint_type(self) -> typing.Optional[builtins.str]:
            '''The type of the VPC endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-servicenetworkendpoint.html#cfn-odb-odbnetwork-servicenetworkendpoint-vpcendpointtype
            '''
            result = self._values.get("vpc_endpoint_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNetworkEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnOdbNetworkPropsMixin.ZeroEtlAccessProperty",
        jsii_struct_bases=[],
        name_mapping={"cidr": "cidr", "status": "status"},
    )
    class ZeroEtlAccessProperty:
        def __init__(
            self,
            *,
            cidr: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for Zero-ETL access from the ODB network.

            :param cidr: The CIDR block for the Zero-ETL access.
            :param status: The status of the Zero-ETL access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-zeroetlaccess.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
                
                zero_etl_access_property = odb_mixins.CfnOdbNetworkPropsMixin.ZeroEtlAccessProperty(
                    cidr="cidr",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e5c8ce5a0db2ef34966d5dcf5eed7c253763729e4726f4eacb5b4e702a6af48)
                check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidr is not None:
                self._values["cidr"] = cidr
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def cidr(self) -> typing.Optional[builtins.str]:
            '''The CIDR block for the Zero-ETL access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-zeroetlaccess.html#cfn-odb-odbnetwork-zeroetlaccess-cidr
            '''
            result = self._values.get("cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the Zero-ETL access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-odb-odbnetwork-zeroetlaccess.html#cfn-odb-odbnetwork-zeroetlaccess-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZeroEtlAccessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnOdbPeeringConnectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_peer_network_cidrs": "additionalPeerNetworkCidrs",
        "display_name": "displayName",
        "odb_network_id": "odbNetworkId",
        "peer_network_id": "peerNetworkId",
        "tags": "tags",
    },
)
class CfnOdbPeeringConnectionMixinProps:
    def __init__(
        self,
        *,
        additional_peer_network_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        odb_network_id: typing.Optional[builtins.str] = None,
        peer_network_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOdbPeeringConnectionPropsMixin.

        :param additional_peer_network_cidrs: The additional CIDR blocks for the ODB peering connection.
        :param display_name: The display name of the ODB peering connection.
        :param odb_network_id: The unique identifier of the ODB network.
        :param peer_network_id: The unique identifier of the peer network.
        :param tags: Tags to assign to the Odb peering connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbpeeringconnection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
            
            cfn_odb_peering_connection_mixin_props = odb_mixins.CfnOdbPeeringConnectionMixinProps(
                additional_peer_network_cidrs=["additionalPeerNetworkCidrs"],
                display_name="displayName",
                odb_network_id="odbNetworkId",
                peer_network_id="peerNetworkId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60afd3f9314634fbb528a2a4e90f5bf57aa18aaf0ab613911595a5bf303316b2)
            check_type(argname="argument additional_peer_network_cidrs", value=additional_peer_network_cidrs, expected_type=type_hints["additional_peer_network_cidrs"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument odb_network_id", value=odb_network_id, expected_type=type_hints["odb_network_id"])
            check_type(argname="argument peer_network_id", value=peer_network_id, expected_type=type_hints["peer_network_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_peer_network_cidrs is not None:
            self._values["additional_peer_network_cidrs"] = additional_peer_network_cidrs
        if display_name is not None:
            self._values["display_name"] = display_name
        if odb_network_id is not None:
            self._values["odb_network_id"] = odb_network_id
        if peer_network_id is not None:
            self._values["peer_network_id"] = peer_network_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def additional_peer_network_cidrs(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional CIDR blocks for the ODB peering connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbpeeringconnection.html#cfn-odb-odbpeeringconnection-additionalpeernetworkcidrs
        '''
        result = self._values.get("additional_peer_network_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the ODB peering connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbpeeringconnection.html#cfn-odb-odbpeeringconnection-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def odb_network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the ODB network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbpeeringconnection.html#cfn-odb-odbpeeringconnection-odbnetworkid
        '''
        result = self._values.get("odb_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the peer network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbpeeringconnection.html#cfn-odb-odbpeeringconnection-peernetworkid
        '''
        result = self._values.get("peer_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the Odb peering connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbpeeringconnection.html#cfn-odb-odbpeeringconnection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOdbPeeringConnectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOdbPeeringConnectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_odb.mixins.CfnOdbPeeringConnectionPropsMixin",
):
    '''Creates a peering connection between an ODB network and a VPC.

    A peering connection enables private connectivity between the networks for application-tier communication.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-odb-odbpeeringconnection.html
    :cloudformationResource: AWS::ODB::OdbPeeringConnection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_odb import mixins as odb_mixins
        
        cfn_odb_peering_connection_props_mixin = odb_mixins.CfnOdbPeeringConnectionPropsMixin(odb_mixins.CfnOdbPeeringConnectionMixinProps(
            additional_peer_network_cidrs=["additionalPeerNetworkCidrs"],
            display_name="displayName",
            odb_network_id="odbNetworkId",
            peer_network_id="peerNetworkId",
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
        props: typing.Union[CfnOdbPeeringConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ODB::OdbPeeringConnection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15584c72cd700c527ee7e80fad50fca5ca8ef05abadbaf9d9deb9ff36bcde61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9509610756e14f7d55d64180773e19be56856fec749d9fc0d5571b3a84011e18)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a315d47ec2e118c532442c8d25e16966cb97e4758ccd19cb0232e4a926b69a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOdbPeeringConnectionMixinProps:
        return typing.cast(CfnOdbPeeringConnectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnCloudAutonomousVmClusterMixinProps",
    "CfnCloudAutonomousVmClusterPropsMixin",
    "CfnCloudExadataInfrastructureMixinProps",
    "CfnCloudExadataInfrastructurePropsMixin",
    "CfnCloudVmClusterMixinProps",
    "CfnCloudVmClusterPropsMixin",
    "CfnOdbNetworkMixinProps",
    "CfnOdbNetworkPropsMixin",
    "CfnOdbPeeringConnectionMixinProps",
    "CfnOdbPeeringConnectionPropsMixin",
]

publication.publish()

def _typecheckingstub__e7df233982f64b70b9f8338aab569ddf81f47e5b7ee40f0871324c76d6a4dbb6(
    *,
    autonomous_data_storage_size_in_t_bs: typing.Optional[jsii.Number] = None,
    cloud_exadata_infrastructure_id: typing.Optional[builtins.str] = None,
    cpu_core_count_per_node: typing.Optional[jsii.Number] = None,
    db_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    is_mtls_enabled_vm_cluster: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    license_model: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudAutonomousVmClusterPropsMixin.MaintenanceWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    memory_per_oracle_compute_unit_in_g_bs: typing.Optional[jsii.Number] = None,
    odb_network_id: typing.Optional[builtins.str] = None,
    scan_listener_port_non_tls: typing.Optional[jsii.Number] = None,
    scan_listener_port_tls: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    total_container_databases: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0f170196c751776269e4e1ee5b606b98d13fffdf7271bbf9502c9b5208f97d(
    props: typing.Union[CfnCloudAutonomousVmClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b1ab0ed8203088dc382c9d797ea54610ea2ea04c40f781b8c151f10b6fd35e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb28d3d8ab1837a8c01d9465697ace00505320c4ca38851733938c9ca80746d0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3cd66a28683c7169ee1c07653d553826d44206e12d498956432bcf8c01e245(
    *,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    hours_of_day: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    lead_time_in_weeks: typing.Optional[jsii.Number] = None,
    months: typing.Optional[typing.Sequence[builtins.str]] = None,
    preference: typing.Optional[builtins.str] = None,
    weeks_of_month: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3d757ac8ffaba8f68dd30b8b38a0a9ccdbe364dfe55e0d55c016ccd2f1265a(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    availability_zone_id: typing.Optional[builtins.str] = None,
    compute_count: typing.Optional[jsii.Number] = None,
    customer_contacts_to_send_to_oci: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudExadataInfrastructurePropsMixin.CustomerContactProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    database_server_type: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudExadataInfrastructurePropsMixin.MaintenanceWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    shape: typing.Optional[builtins.str] = None,
    storage_count: typing.Optional[jsii.Number] = None,
    storage_server_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d70ccb9d2215718bb919112bbe211426a6ba35462044150257dea6bfb5f98d9(
    props: typing.Union[CfnCloudExadataInfrastructureMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba9692774d15deaedd36c1e67357bfd66efe7c98b2ed248a05b96025d55096d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48785dc20737288f4a9eece5c7307881f6c7fff010ead367cc23810389a7599a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec039dbd487c8faf6e9427b0433afae7faa63e45a3791ae165aeb6691a427fcb(
    *,
    email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789fb64928707181b1ddba7a990079d77561f32cf5eb4b227dc5c99d73a5d75b(
    *,
    custom_action_timeout_in_mins: typing.Optional[jsii.Number] = None,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    hours_of_day: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    is_custom_action_timeout_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    lead_time_in_weeks: typing.Optional[jsii.Number] = None,
    months: typing.Optional[typing.Sequence[builtins.str]] = None,
    patching_mode: typing.Optional[builtins.str] = None,
    preference: typing.Optional[builtins.str] = None,
    weeks_of_month: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681939acaf5e4dacc4294795188b30becf4322b40ab04003972dd74e2dcb0735(
    *,
    cloud_exadata_infrastructure_id: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    cpu_core_count: typing.Optional[jsii.Number] = None,
    data_collection_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudVmClusterPropsMixin.DataCollectionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_storage_size_in_t_bs: typing.Optional[jsii.Number] = None,
    db_nodes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudVmClusterPropsMixin.DbNodeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    db_node_storage_size_in_g_bs: typing.Optional[jsii.Number] = None,
    db_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gi_version: typing.Optional[builtins.str] = None,
    hostname: typing.Optional[builtins.str] = None,
    is_local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    license_model: typing.Optional[builtins.str] = None,
    memory_size_in_g_bs: typing.Optional[jsii.Number] = None,
    odb_network_id: typing.Optional[builtins.str] = None,
    scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
    ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    system_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e646df938caff63d6b665c723dd5c7af729c5ca63650df7377d428e2e472b3d(
    props: typing.Union[CfnCloudVmClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9755257abf867fcec554a07bd8d0afa366ff0c7e934f2a8a1cbf0d899eee0d96(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50bd27574a00c4b78537d39020c0b6d6058893ff7c52d1ddc08810d33584249(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afeb7b82410bf8822e7970875f78d75f44169c65c9fa8b2b59baf7e5f2c337e0(
    *,
    is_diagnostics_events_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_health_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_incident_logs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a1101f812cb89e2a5aaf711d47fc2262567a9c907316e9920008119eb86ef3(
    *,
    backup_ip_id: typing.Optional[builtins.str] = None,
    backup_vnic2_id: typing.Optional[builtins.str] = None,
    cpu_core_count: typing.Optional[jsii.Number] = None,
    db_node_arn: typing.Optional[builtins.str] = None,
    db_node_id: typing.Optional[builtins.str] = None,
    db_node_storage_size_in_g_bs: typing.Optional[jsii.Number] = None,
    db_server_id: typing.Optional[builtins.str] = None,
    db_system_id: typing.Optional[builtins.str] = None,
    host_ip_id: typing.Optional[builtins.str] = None,
    hostname: typing.Optional[builtins.str] = None,
    memory_size_in_g_bs: typing.Optional[jsii.Number] = None,
    ocid: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vnic2_id: typing.Optional[builtins.str] = None,
    vnic_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4ee3b6291623a81990313a7525b2473ef87cb422b45c69815cfc6133e4fa4d(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    availability_zone_id: typing.Optional[builtins.str] = None,
    backup_subnet_cidr: typing.Optional[builtins.str] = None,
    client_subnet_cidr: typing.Optional[builtins.str] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    default_dns_prefix: typing.Optional[builtins.str] = None,
    delete_associated_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    s3_access: typing.Optional[builtins.str] = None,
    s3_policy_document: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    zero_etl_access: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd786f79a91b56f2f7ce0801c7a75e4436a851fa6e4751ddff02cbb4378c9f3(
    props: typing.Union[CfnOdbNetworkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92055987bbe30d602d9b57265b84321ddf2b6f5addaee5551a4bc8a8dc490f9a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a43428c745e47910197602e3f102ba1a8684f973618e27481e103d06cfd32b8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7418b9aa72684f3c6e7f9f50358b87cf46ed52e41414900904c17786889912(
    *,
    ipv4_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2147cacc5d75fd648850ab585f968edb34ff9fd15d4a0c2f711986664f0e438(
    *,
    managed_s3_backup_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOdbNetworkPropsMixin.ManagedS3BackupAccessProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    managed_services_ipv4_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_gateway_arn: typing.Optional[builtins.str] = None,
    s3_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOdbNetworkPropsMixin.S3AccessProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_network_arn: typing.Optional[builtins.str] = None,
    service_network_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOdbNetworkPropsMixin.ServiceNetworkEndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    zero_etl_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOdbNetworkPropsMixin.ZeroEtlAccessProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dabf95f03cd393382600edefdc8eaca81d6842dd0293a1b4a058b747bd45269(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    ipv4_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_policy_document: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a7ebe33fa93aca66d3afa873ad7cbc5d75ed104cf7ef47260fcd4257caa964(
    *,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
    vpc_endpoint_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5c8ce5a0db2ef34966d5dcf5eed7c253763729e4726f4eacb5b4e702a6af48(
    *,
    cidr: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60afd3f9314634fbb528a2a4e90f5bf57aa18aaf0ab613911595a5bf303316b2(
    *,
    additional_peer_network_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    odb_network_id: typing.Optional[builtins.str] = None,
    peer_network_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15584c72cd700c527ee7e80fad50fca5ca8ef05abadbaf9d9deb9ff36bcde61(
    props: typing.Union[CfnOdbPeeringConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9509610756e14f7d55d64180773e19be56856fec749d9fc0d5571b3a84011e18(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a315d47ec2e118c532442c8d25e16966cb97e4758ccd19cb0232e4a926b69a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
