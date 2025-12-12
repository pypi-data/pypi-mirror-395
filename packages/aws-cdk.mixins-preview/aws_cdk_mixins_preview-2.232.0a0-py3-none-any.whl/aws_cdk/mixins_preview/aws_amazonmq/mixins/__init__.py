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
    jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnBrokerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_strategy": "authenticationStrategy",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "broker_name": "brokerName",
        "configuration": "configuration",
        "data_replication_mode": "dataReplicationMode",
        "data_replication_primary_broker_arn": "dataReplicationPrimaryBrokerArn",
        "deployment_mode": "deploymentMode",
        "encryption_options": "encryptionOptions",
        "engine_type": "engineType",
        "engine_version": "engineVersion",
        "host_instance_type": "hostInstanceType",
        "ldap_server_metadata": "ldapServerMetadata",
        "logs": "logs",
        "maintenance_window_start_time": "maintenanceWindowStartTime",
        "publicly_accessible": "publiclyAccessible",
        "security_groups": "securityGroups",
        "storage_type": "storageType",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "users": "users",
    },
)
class CfnBrokerMixinProps:
    def __init__(
        self,
        *,
        authentication_strategy: typing.Optional[builtins.str] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        broker_name: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrokerPropsMixin.ConfigurationIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_replication_mode: typing.Optional[builtins.str] = None,
        data_replication_primary_broker_arn: typing.Optional[builtins.str] = None,
        deployment_mode: typing.Optional[builtins.str] = None,
        encryption_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrokerPropsMixin.EncryptionOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        engine_type: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        host_instance_type: typing.Optional[builtins.str] = None,
        ldap_server_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrokerPropsMixin.LdapServerMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrokerPropsMixin.LogListProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        maintenance_window_start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrokerPropsMixin.MaintenanceWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnBrokerPropsMixin.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        users: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrokerPropsMixin.UserProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnBrokerPropsMixin.

        :param authentication_strategy: Optional. The authentication strategy used to secure the broker. The default is ``SIMPLE`` .
        :param auto_minor_version_upgrade: Enables automatic upgrades to new patch versions for brokers as new versions are released and supported by Amazon MQ. Automatic upgrades occur during the scheduled maintenance window or after a manual broker reboot. Set to ``true`` by default, if no value is specified. .. epigraph:: Must be set to ``true`` for ActiveMQ brokers version 5.18 and above and for RabbitMQ brokers version 3.13 and above.
        :param broker_name: Required. The broker's name. This value must be unique in your AWS account , 1-50 characters long, must contain only letters, numbers, dashes, and underscores, and must not contain white spaces, brackets, wildcard characters, or special characters. .. epigraph:: Do not add personally identifiable information (PII) or other confidential or sensitive information in broker names. Broker names are accessible to other AWS services, including CloudWatch Logs . Broker names are not intended to be used for private or sensitive data.
        :param configuration: A list of information about the configuration.
        :param data_replication_mode: Defines whether this broker is a part of a data replication pair.
        :param data_replication_primary_broker_arn: The Amazon Resource Name (ARN) of the primary broker that is used to replicate data from in a data replication pair, and is applied to the replica broker. Must be set when dataReplicationMode is set to CRDR.
        :param deployment_mode: Required. The broker's deployment mode.
        :param encryption_options: Encryption options for the broker.
        :param engine_type: Required. The type of broker engine. Currently, Amazon MQ supports ``ACTIVEMQ`` and ``RABBITMQ`` .
        :param engine_version: The broker engine version. Defaults to the latest available version for the specified broker engine type. For more information, see the `ActiveMQ version management <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/activemq-version-management.html>`_ and the `RabbitMQ version management <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/rabbitmq-version-management.html>`_ sections in the Amazon MQ Developer Guide.
        :param host_instance_type: Required. The broker's instance type.
        :param ldap_server_metadata: Optional. The metadata of the LDAP server used to authenticate and authorize connections to the broker. Does not apply to RabbitMQ brokers.
        :param logs: Enables Amazon CloudWatch logging for brokers.
        :param maintenance_window_start_time: The parameters that determine the WeeklyStartTime.
        :param publicly_accessible: Enables connections from applications outside of the VPC that hosts the broker's subnets. Set to ``false`` by default, if no value is provided.
        :param security_groups: The list of rules (1 minimum, 125 maximum) that authorize connections to brokers.
        :param storage_type: The broker's storage type.
        :param subnet_ids: The list of groups that define which subnets and IP ranges the broker can use from different Availability Zones. If you specify more than one subnet, the subnets must be in different Availability Zones. Amazon MQ will not be able to create VPC endpoints for your broker with multiple subnets in the same Availability Zone. A SINGLE_INSTANCE deployment requires one subnet (for example, the default subnet). An ACTIVE_STANDBY_MULTI_AZ Amazon MQ for ActiveMQ deployment requires two subnets. A CLUSTER_MULTI_AZ Amazon MQ for RabbitMQ deployment has no subnet requirements when deployed with public accessibility. Deployment without public accessibility requires at least one subnet. .. epigraph:: If you specify subnets in a `shared VPC <https://docs.aws.amazon.com/vpc/latest/userguide/vpc-sharing.html>`_ for a RabbitMQ broker, the associated VPC to which the specified subnets belong must be owned by your AWS account . Amazon MQ will not be able to create VPC endpoints in VPCs that are not owned by your AWS account .
        :param tags: Create tags when creating the broker.
        :param users: The list of broker users (persons or applications) who can access queues and topics. For Amazon MQ for RabbitMQ brokers, one and only one administrative user is accepted and created when a broker is first provisioned. All subsequent broker users are created by making RabbitMQ API calls directly to brokers or via the RabbitMQ web console. When OAuth 2.0 is enabled, the broker accepts one or no users.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
            
            cfn_broker_mixin_props = amazonmq_mixins.CfnBrokerMixinProps(
                authentication_strategy="authenticationStrategy",
                auto_minor_version_upgrade=False,
                broker_name="brokerName",
                configuration=amazonmq_mixins.CfnBrokerPropsMixin.ConfigurationIdProperty(
                    id="id",
                    revision=123
                ),
                data_replication_mode="dataReplicationMode",
                data_replication_primary_broker_arn="dataReplicationPrimaryBrokerArn",
                deployment_mode="deploymentMode",
                encryption_options=amazonmq_mixins.CfnBrokerPropsMixin.EncryptionOptionsProperty(
                    kms_key_id="kmsKeyId",
                    use_aws_owned_key=False
                ),
                engine_type="engineType",
                engine_version="engineVersion",
                host_instance_type="hostInstanceType",
                ldap_server_metadata=amazonmq_mixins.CfnBrokerPropsMixin.LdapServerMetadataProperty(
                    hosts=["hosts"],
                    role_base="roleBase",
                    role_name="roleName",
                    role_search_matching="roleSearchMatching",
                    role_search_subtree=False,
                    service_account_password="serviceAccountPassword",
                    service_account_username="serviceAccountUsername",
                    user_base="userBase",
                    user_role_name="userRoleName",
                    user_search_matching="userSearchMatching",
                    user_search_subtree=False
                ),
                logs=amazonmq_mixins.CfnBrokerPropsMixin.LogListProperty(
                    audit=False,
                    general=False
                ),
                maintenance_window_start_time=amazonmq_mixins.CfnBrokerPropsMixin.MaintenanceWindowProperty(
                    day_of_week="dayOfWeek",
                    time_of_day="timeOfDay",
                    time_zone="timeZone"
                ),
                publicly_accessible=False,
                security_groups=["securityGroups"],
                storage_type="storageType",
                subnet_ids=["subnetIds"],
                tags=[amazonmq_mixins.CfnBrokerPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )],
                users=[amazonmq_mixins.CfnBrokerPropsMixin.UserProperty(
                    console_access=False,
                    groups=["groups"],
                    password="password",
                    replication_user=False,
                    username="username"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3744e9b9b05cbbb4dbd88f7656df5524968ed9f1609bbff41dc95a4c28326977)
            check_type(argname="argument authentication_strategy", value=authentication_strategy, expected_type=type_hints["authentication_strategy"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument broker_name", value=broker_name, expected_type=type_hints["broker_name"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument data_replication_mode", value=data_replication_mode, expected_type=type_hints["data_replication_mode"])
            check_type(argname="argument data_replication_primary_broker_arn", value=data_replication_primary_broker_arn, expected_type=type_hints["data_replication_primary_broker_arn"])
            check_type(argname="argument deployment_mode", value=deployment_mode, expected_type=type_hints["deployment_mode"])
            check_type(argname="argument encryption_options", value=encryption_options, expected_type=type_hints["encryption_options"])
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument host_instance_type", value=host_instance_type, expected_type=type_hints["host_instance_type"])
            check_type(argname="argument ldap_server_metadata", value=ldap_server_metadata, expected_type=type_hints["ldap_server_metadata"])
            check_type(argname="argument logs", value=logs, expected_type=type_hints["logs"])
            check_type(argname="argument maintenance_window_start_time", value=maintenance_window_start_time, expected_type=type_hints["maintenance_window_start_time"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_strategy is not None:
            self._values["authentication_strategy"] = authentication_strategy
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if broker_name is not None:
            self._values["broker_name"] = broker_name
        if configuration is not None:
            self._values["configuration"] = configuration
        if data_replication_mode is not None:
            self._values["data_replication_mode"] = data_replication_mode
        if data_replication_primary_broker_arn is not None:
            self._values["data_replication_primary_broker_arn"] = data_replication_primary_broker_arn
        if deployment_mode is not None:
            self._values["deployment_mode"] = deployment_mode
        if encryption_options is not None:
            self._values["encryption_options"] = encryption_options
        if engine_type is not None:
            self._values["engine_type"] = engine_type
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if host_instance_type is not None:
            self._values["host_instance_type"] = host_instance_type
        if ldap_server_metadata is not None:
            self._values["ldap_server_metadata"] = ldap_server_metadata
        if logs is not None:
            self._values["logs"] = logs
        if maintenance_window_start_time is not None:
            self._values["maintenance_window_start_time"] = maintenance_window_start_time
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def authentication_strategy(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The authentication strategy used to secure the broker. The default is ``SIMPLE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-authenticationstrategy
        '''
        result = self._values.get("authentication_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables automatic upgrades to new patch versions for brokers as new versions are released and supported by Amazon MQ.

        Automatic upgrades occur during the scheduled maintenance window or after a manual broker reboot. Set to ``true`` by default, if no value is specified.
        .. epigraph::

           Must be set to ``true`` for ActiveMQ brokers version 5.18 and above and for RabbitMQ brokers version 3.13 and above.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def broker_name(self) -> typing.Optional[builtins.str]:
        '''Required.

        The broker's name. This value must be unique in your AWS account , 1-50 characters long, must contain only letters, numbers, dashes, and underscores, and must not contain white spaces, brackets, wildcard characters, or special characters.
        .. epigraph::

           Do not add personally identifiable information (PII) or other confidential or sensitive information in broker names. Broker names are accessible to other AWS services, including CloudWatch Logs . Broker names are not intended to be used for private or sensitive data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-brokername
        '''
        result = self._values.get("broker_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.ConfigurationIdProperty"]]:
        '''A list of information about the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.ConfigurationIdProperty"]], result)

    @builtins.property
    def data_replication_mode(self) -> typing.Optional[builtins.str]:
        '''Defines whether this broker is a part of a data replication pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-datareplicationmode
        '''
        result = self._values.get("data_replication_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_replication_primary_broker_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the primary broker that is used to replicate data from in a data replication pair, and is applied to the replica broker.

        Must be set when dataReplicationMode is set to CRDR.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-datareplicationprimarybrokerarn
        '''
        result = self._values.get("data_replication_primary_broker_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_mode(self) -> typing.Optional[builtins.str]:
        '''Required.

        The broker's deployment mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-deploymentmode
        '''
        result = self._values.get("deployment_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.EncryptionOptionsProperty"]]:
        '''Encryption options for the broker.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-encryptionoptions
        '''
        result = self._values.get("encryption_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.EncryptionOptionsProperty"]], result)

    @builtins.property
    def engine_type(self) -> typing.Optional[builtins.str]:
        '''Required.

        The type of broker engine. Currently, Amazon MQ supports ``ACTIVEMQ`` and ``RABBITMQ`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-enginetype
        '''
        result = self._values.get("engine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The broker engine version.

        Defaults to the latest available version for the specified broker engine type. For more information, see the `ActiveMQ version management <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/activemq-version-management.html>`_ and the `RabbitMQ version management <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/rabbitmq-version-management.html>`_ sections in the Amazon MQ Developer Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_instance_type(self) -> typing.Optional[builtins.str]:
        '''Required.

        The broker's instance type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-hostinstancetype
        '''
        result = self._values.get("host_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ldap_server_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.LdapServerMetadataProperty"]]:
        '''Optional.

        The metadata of the LDAP server used to authenticate and authorize connections to the broker. Does not apply to RabbitMQ brokers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-ldapservermetadata
        '''
        result = self._values.get("ldap_server_metadata")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.LdapServerMetadataProperty"]], result)

    @builtins.property
    def logs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.LogListProperty"]]:
        '''Enables Amazon CloudWatch logging for brokers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-logs
        '''
        result = self._values.get("logs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.LogListProperty"]], result)

    @builtins.property
    def maintenance_window_start_time(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.MaintenanceWindowProperty"]]:
        '''The parameters that determine the WeeklyStartTime.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-maintenancewindowstarttime
        '''
        result = self._values.get("maintenance_window_start_time")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.MaintenanceWindowProperty"]], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables connections from applications outside of the VPC that hosts the broker's subnets.

        Set to ``false`` by default, if no value is provided.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of rules (1 minimum, 125 maximum) that authorize connections to brokers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-securitygroups
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''The broker's storage type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-storagetype
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of groups that define which subnets and IP ranges the broker can use from different Availability Zones.

        If you specify more than one subnet, the subnets must be in different Availability Zones. Amazon MQ will not be able to create VPC endpoints for your broker with multiple subnets in the same Availability Zone. A SINGLE_INSTANCE deployment requires one subnet (for example, the default subnet). An ACTIVE_STANDBY_MULTI_AZ Amazon MQ for ActiveMQ deployment requires two subnets. A CLUSTER_MULTI_AZ Amazon MQ for RabbitMQ deployment has no subnet requirements when deployed with public accessibility. Deployment without public accessibility requires at least one subnet.
        .. epigraph::

           If you specify subnets in a `shared VPC <https://docs.aws.amazon.com/vpc/latest/userguide/vpc-sharing.html>`_ for a RabbitMQ broker, the associated VPC to which the specified subnets belong must be owned by your AWS account . Amazon MQ will not be able to create VPC endpoints in VPCs that are not owned by your AWS account .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnBrokerPropsMixin.TagsEntryProperty"]]:
        '''Create tags when creating the broker.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnBrokerPropsMixin.TagsEntryProperty"]], result)

    @builtins.property
    def users(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.UserProperty"]]]]:
        '''The list of broker users (persons or applications) who can access queues and topics.

        For Amazon MQ for RabbitMQ brokers, one and only one administrative user is accepted and created when a broker is first provisioned. All subsequent broker users are created by making RabbitMQ API calls directly to brokers or via the RabbitMQ web console.

        When OAuth 2.0 is enabled, the broker accepts one or no users.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-users
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrokerPropsMixin.UserProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBrokerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBrokerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnBrokerPropsMixin",
):
    '''Creates a broker. Note: This API is asynchronous.

    To create a broker, you must either use the ``AmazonMQFullAccess`` IAM policy or include the following EC2 permissions in your IAM policy.

    - ``ec2:CreateNetworkInterface``

    This permission is required to allow Amazon MQ to create an elastic network interface (ENI) on behalf of your account.

    - ``ec2:CreateNetworkInterfacePermission``

    This permission is required to attach the ENI to the broker instance.

    - ``ec2:DeleteNetworkInterface``
    - ``ec2:DeleteNetworkInterfacePermission``
    - ``ec2:DetachNetworkInterface``
    - ``ec2:DescribeInternetGateways``
    - ``ec2:DescribeNetworkInterfaces``
    - ``ec2:DescribeNetworkInterfacePermissions``
    - ``ec2:DescribeRouteTables``
    - ``ec2:DescribeSecurityGroups``
    - ``ec2:DescribeSubnets``
    - ``ec2:DescribeVpcs``

    For more information, see `Create an IAM User and Get Your AWS Credentials <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/amazon-mq-setting-up.html#create-iam-user>`_ and `Never Modify or Delete the Amazon MQ Elastic Network Interface <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/connecting-to-amazon-mq.html#never-modify-delete-elastic-network-interface>`_ in the *Amazon MQ Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html
    :cloudformationResource: AWS::AmazonMQ::Broker
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
        
        cfn_broker_props_mixin = amazonmq_mixins.CfnBrokerPropsMixin(amazonmq_mixins.CfnBrokerMixinProps(
            authentication_strategy="authenticationStrategy",
            auto_minor_version_upgrade=False,
            broker_name="brokerName",
            configuration=amazonmq_mixins.CfnBrokerPropsMixin.ConfigurationIdProperty(
                id="id",
                revision=123
            ),
            data_replication_mode="dataReplicationMode",
            data_replication_primary_broker_arn="dataReplicationPrimaryBrokerArn",
            deployment_mode="deploymentMode",
            encryption_options=amazonmq_mixins.CfnBrokerPropsMixin.EncryptionOptionsProperty(
                kms_key_id="kmsKeyId",
                use_aws_owned_key=False
            ),
            engine_type="engineType",
            engine_version="engineVersion",
            host_instance_type="hostInstanceType",
            ldap_server_metadata=amazonmq_mixins.CfnBrokerPropsMixin.LdapServerMetadataProperty(
                hosts=["hosts"],
                role_base="roleBase",
                role_name="roleName",
                role_search_matching="roleSearchMatching",
                role_search_subtree=False,
                service_account_password="serviceAccountPassword",
                service_account_username="serviceAccountUsername",
                user_base="userBase",
                user_role_name="userRoleName",
                user_search_matching="userSearchMatching",
                user_search_subtree=False
            ),
            logs=amazonmq_mixins.CfnBrokerPropsMixin.LogListProperty(
                audit=False,
                general=False
            ),
            maintenance_window_start_time=amazonmq_mixins.CfnBrokerPropsMixin.MaintenanceWindowProperty(
                day_of_week="dayOfWeek",
                time_of_day="timeOfDay",
                time_zone="timeZone"
            ),
            publicly_accessible=False,
            security_groups=["securityGroups"],
            storage_type="storageType",
            subnet_ids=["subnetIds"],
            tags=[amazonmq_mixins.CfnBrokerPropsMixin.TagsEntryProperty(
                key="key",
                value="value"
            )],
            users=[amazonmq_mixins.CfnBrokerPropsMixin.UserProperty(
                console_access=False,
                groups=["groups"],
                password="password",
                replication_user=False,
                username="username"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBrokerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AmazonMQ::Broker``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca4e4c5e9083c08ab055248254f4e1b6f44726adcc55756469cc83562847ab6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2376e80cc326b0bbf9aafd4825e6066fbed9b3806f67ef6ac5e635bbf92f053)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5435dc3f401ca81545b57afb6b8b372b13f4c15ab06d109feaad6f32e4ed7c56)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBrokerMixinProps:
        return typing.cast(CfnBrokerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnBrokerPropsMixin.ConfigurationIdProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "revision": "revision"},
    )
    class ConfigurationIdProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            revision: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A list of information about the configuration.

            :param id: Required. The unique ID that Amazon MQ generates for the configuration.
            :param revision: The revision number of the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
                
                configuration_id_property = amazonmq_mixins.CfnBrokerPropsMixin.ConfigurationIdProperty(
                    id="id",
                    revision=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e41d29191b8d9ec03c7fdb8b23faee624f01a848e6005d91de046037864ad192)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if revision is not None:
                self._values["revision"] = revision

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''Required.

            The unique ID that Amazon MQ generates for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html#cfn-amazonmq-broker-configurationid-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def revision(self) -> typing.Optional[jsii.Number]:
            '''The revision number of the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html#cfn-amazonmq-broker-configurationid-revision
            '''
            result = self._values.get("revision")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnBrokerPropsMixin.EncryptionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId", "use_aws_owned_key": "useAwsOwnedKey"},
    )
    class EncryptionOptionsProperty:
        def __init__(
            self,
            *,
            kms_key_id: typing.Optional[builtins.str] = None,
            use_aws_owned_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Encryption options for the broker.

            :param kms_key_id: The customer master key (CMK) to use for the A AWS (KMS). This key is used to encrypt your data at rest. If not provided, Amazon MQ will use a default CMK to encrypt your data.
            :param use_aws_owned_key: Enables the use of an AWS owned CMK using AWS (KMS). Set to ``true`` by default, if no value is provided, for example, for RabbitMQ brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-encryptionoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
                
                encryption_options_property = amazonmq_mixins.CfnBrokerPropsMixin.EncryptionOptionsProperty(
                    kms_key_id="kmsKeyId",
                    use_aws_owned_key=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8378fa45c38d2cb872348dd5b12964b5c9c97af36ba172e8e7350ce1f5fa8656)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument use_aws_owned_key", value=use_aws_owned_key, expected_type=type_hints["use_aws_owned_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if use_aws_owned_key is not None:
                self._values["use_aws_owned_key"] = use_aws_owned_key

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The customer master key (CMK) to use for the A AWS  (KMS).

            This key is used to encrypt your data at rest. If not provided, Amazon MQ will use a default CMK to encrypt your data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-encryptionoptions.html#cfn-amazonmq-broker-encryptionoptions-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_aws_owned_key(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables the use of an AWS owned CMK using AWS  (KMS).

            Set to ``true`` by default, if no value is provided, for example, for RabbitMQ brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-encryptionoptions.html#cfn-amazonmq-broker-encryptionoptions-useawsownedkey
            '''
            result = self._values.get("use_aws_owned_key")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnBrokerPropsMixin.LdapServerMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hosts": "hosts",
            "role_base": "roleBase",
            "role_name": "roleName",
            "role_search_matching": "roleSearchMatching",
            "role_search_subtree": "roleSearchSubtree",
            "service_account_password": "serviceAccountPassword",
            "service_account_username": "serviceAccountUsername",
            "user_base": "userBase",
            "user_role_name": "userRoleName",
            "user_search_matching": "userSearchMatching",
            "user_search_subtree": "userSearchSubtree",
        },
    )
    class LdapServerMetadataProperty:
        def __init__(
            self,
            *,
            hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
            role_base: typing.Optional[builtins.str] = None,
            role_name: typing.Optional[builtins.str] = None,
            role_search_matching: typing.Optional[builtins.str] = None,
            role_search_subtree: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            service_account_password: typing.Optional[builtins.str] = None,
            service_account_username: typing.Optional[builtins.str] = None,
            user_base: typing.Optional[builtins.str] = None,
            user_role_name: typing.Optional[builtins.str] = None,
            user_search_matching: typing.Optional[builtins.str] = None,
            user_search_subtree: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Optional.

            The metadata of the LDAP server used to authenticate and authorize connections to the broker. Does not apply to RabbitMQ brokers.

            :param hosts: 
            :param role_base: 
            :param role_name: 
            :param role_search_matching: 
            :param role_search_subtree: 
            :param service_account_password: 
            :param service_account_username: 
            :param user_base: 
            :param user_role_name: 
            :param user_search_matching: 
            :param user_search_subtree: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
                
                ldap_server_metadata_property = amazonmq_mixins.CfnBrokerPropsMixin.LdapServerMetadataProperty(
                    hosts=["hosts"],
                    role_base="roleBase",
                    role_name="roleName",
                    role_search_matching="roleSearchMatching",
                    role_search_subtree=False,
                    service_account_password="serviceAccountPassword",
                    service_account_username="serviceAccountUsername",
                    user_base="userBase",
                    user_role_name="userRoleName",
                    user_search_matching="userSearchMatching",
                    user_search_subtree=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5feb908abe3e71a4efe29b6c62a30c6d7694cc2acc7c54196d233942927deab6)
                check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
                check_type(argname="argument role_base", value=role_base, expected_type=type_hints["role_base"])
                check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
                check_type(argname="argument role_search_matching", value=role_search_matching, expected_type=type_hints["role_search_matching"])
                check_type(argname="argument role_search_subtree", value=role_search_subtree, expected_type=type_hints["role_search_subtree"])
                check_type(argname="argument service_account_password", value=service_account_password, expected_type=type_hints["service_account_password"])
                check_type(argname="argument service_account_username", value=service_account_username, expected_type=type_hints["service_account_username"])
                check_type(argname="argument user_base", value=user_base, expected_type=type_hints["user_base"])
                check_type(argname="argument user_role_name", value=user_role_name, expected_type=type_hints["user_role_name"])
                check_type(argname="argument user_search_matching", value=user_search_matching, expected_type=type_hints["user_search_matching"])
                check_type(argname="argument user_search_subtree", value=user_search_subtree, expected_type=type_hints["user_search_subtree"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hosts is not None:
                self._values["hosts"] = hosts
            if role_base is not None:
                self._values["role_base"] = role_base
            if role_name is not None:
                self._values["role_name"] = role_name
            if role_search_matching is not None:
                self._values["role_search_matching"] = role_search_matching
            if role_search_subtree is not None:
                self._values["role_search_subtree"] = role_search_subtree
            if service_account_password is not None:
                self._values["service_account_password"] = service_account_password
            if service_account_username is not None:
                self._values["service_account_username"] = service_account_username
            if user_base is not None:
                self._values["user_base"] = user_base
            if user_role_name is not None:
                self._values["user_role_name"] = user_role_name
            if user_search_matching is not None:
                self._values["user_search_matching"] = user_search_matching
            if user_search_subtree is not None:
                self._values["user_search_subtree"] = user_search_subtree

        @builtins.property
        def hosts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-hosts
            '''
            result = self._values.get("hosts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def role_base(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolebase
            '''
            result = self._values.get("role_base")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolename
            '''
            result = self._values.get("role_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_search_matching(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolesearchmatching
            '''
            result = self._values.get("role_search_matching")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_search_subtree(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolesearchsubtree
            '''
            result = self._values.get("role_search_subtree")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def service_account_password(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-serviceaccountpassword
            '''
            result = self._values.get("service_account_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_account_username(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-serviceaccountusername
            '''
            result = self._values.get("service_account_username")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_base(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-userbase
            '''
            result = self._values.get("user_base")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_role_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-userrolename
            '''
            result = self._values.get("user_role_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_search_matching(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-usersearchmatching
            '''
            result = self._values.get("user_search_matching")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_search_subtree(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-usersearchsubtree
            '''
            result = self._values.get("user_search_subtree")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LdapServerMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnBrokerPropsMixin.LogListProperty",
        jsii_struct_bases=[],
        name_mapping={"audit": "audit", "general": "general"},
    )
    class LogListProperty:
        def __init__(
            self,
            *,
            audit: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            general: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The list of information about logs to be enabled for the specified broker.

            :param audit: Enables audit logging. Every user management action made using JMX or the ActiveMQ Web Console is logged. Does not apply to RabbitMQ brokers.
            :param general: Enables general logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
                
                log_list_property = amazonmq_mixins.CfnBrokerPropsMixin.LogListProperty(
                    audit=False,
                    general=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__62cf7c1c5bd3ca0aced5933962000a0a620c8885895ded4eebb3d8d608b04205)
                check_type(argname="argument audit", value=audit, expected_type=type_hints["audit"])
                check_type(argname="argument general", value=general, expected_type=type_hints["general"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audit is not None:
                self._values["audit"] = audit
            if general is not None:
                self._values["general"] = general

        @builtins.property
        def audit(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables audit logging.

            Every user management action made using JMX or the ActiveMQ Web Console is logged. Does not apply to RabbitMQ brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html#cfn-amazonmq-broker-loglist-audit
            '''
            result = self._values.get("audit")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def general(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables general logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html#cfn-amazonmq-broker-loglist-general
            '''
            result = self._values.get("general")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnBrokerPropsMixin.MaintenanceWindowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "day_of_week": "dayOfWeek",
            "time_of_day": "timeOfDay",
            "time_zone": "timeZone",
        },
    )
    class MaintenanceWindowProperty:
        def __init__(
            self,
            *,
            day_of_week: typing.Optional[builtins.str] = None,
            time_of_day: typing.Optional[builtins.str] = None,
            time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters that determine the WeeklyStartTime.

            :param day_of_week: Required. The day of the week.
            :param time_of_day: Required. The time, in 24-hour format.
            :param time_zone: The time zone, UTC by default, in either the Country/City format, or the UTC offset format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
                
                maintenance_window_property = amazonmq_mixins.CfnBrokerPropsMixin.MaintenanceWindowProperty(
                    day_of_week="dayOfWeek",
                    time_of_day="timeOfDay",
                    time_zone="timeZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78612699d0ec14d9b324663b5000d336c3a2e98c337949114a61f5408a0d98a1)
                check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
                check_type(argname="argument time_of_day", value=time_of_day, expected_type=type_hints["time_of_day"])
                check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if day_of_week is not None:
                self._values["day_of_week"] = day_of_week
            if time_of_day is not None:
                self._values["time_of_day"] = time_of_day
            if time_zone is not None:
                self._values["time_zone"] = time_zone

        @builtins.property
        def day_of_week(self) -> typing.Optional[builtins.str]:
            '''Required.

            The day of the week.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-dayofweek
            '''
            result = self._values.get("day_of_week")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_of_day(self) -> typing.Optional[builtins.str]:
            '''Required.

            The time, in 24-hour format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-timeofday
            '''
            result = self._values.get("time_of_day")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_zone(self) -> typing.Optional[builtins.str]:
            '''The time zone, UTC by default, in either the Country/City format, or the UTC offset format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-timezone
            '''
            result = self._values.get("time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnBrokerPropsMixin.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Create tags when creating the broker.

            :param key: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
                
                tags_entry_property = amazonmq_mixins.CfnBrokerPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fefaa53fb097a786b45ceaa314acedc095a8bff622e006004f506fad4843711f)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html#cfn-amazonmq-broker-tagsentry-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html#cfn-amazonmq-broker-tagsentry-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnBrokerPropsMixin.UserProperty",
        jsii_struct_bases=[],
        name_mapping={
            "console_access": "consoleAccess",
            "groups": "groups",
            "password": "password",
            "replication_user": "replicationUser",
            "username": "username",
        },
    )
    class UserProperty:
        def __init__(
            self,
            *,
            console_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            password: typing.Optional[builtins.str] = None,
            replication_user: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The list of broker users (persons or applications) who can access queues and topics.

            For Amazon MQ for RabbitMQ brokers, one and only one administrative user is accepted and created when a broker is first provisioned. All subsequent broker users are created by making RabbitMQ API calls directly to brokers or via the RabbitMQ web console.

            When OAuth 2.0 is enabled, the broker accepts one or no users.

            :param console_access: Enables access to the ActiveMQ Web Console for the ActiveMQ user. Does not apply to RabbitMQ brokers.
            :param groups: The list of groups (20 maximum) to which the ActiveMQ user belongs. This value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 2-100 characters long. Does not apply to RabbitMQ brokers.
            :param password: Required. The password of the user. This value must be at least 12 characters long, must contain at least 4 unique characters, and must not contain commas, colons, or equal signs (,:=).
            :param replication_user: Defines if this user is intended for CRDR replication purposes.
            :param username: The username of the broker user. The following restrictions apply to broker usernames:. - For Amazon MQ for ActiveMQ brokers, this value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 2-100 characters long. - For Amazon MQ for RabbitMQ brokers, this value can contain only alphanumeric characters, dashes, periods, underscores (- . _). This value must not contain a tilde (~) character. Amazon MQ prohibts using ``guest`` as a valid usename. This value must be 2-100 characters long. .. epigraph:: Do not add personally identifiable information (PII) or other confidential or sensitive information in broker usernames. Broker usernames are accessible to other AWS services, including CloudWatch Logs . Broker usernames are not intended to be used for private or sensitive data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
                
                user_property = amazonmq_mixins.CfnBrokerPropsMixin.UserProperty(
                    console_access=False,
                    groups=["groups"],
                    password="password",
                    replication_user=False,
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5181251bfc9fefd8e8cf2d778bd5422663788f1260b4bf0b4a1ec71b0a1d3281)
                check_type(argname="argument console_access", value=console_access, expected_type=type_hints["console_access"])
                check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument replication_user", value=replication_user, expected_type=type_hints["replication_user"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if console_access is not None:
                self._values["console_access"] = console_access
            if groups is not None:
                self._values["groups"] = groups
            if password is not None:
                self._values["password"] = password
            if replication_user is not None:
                self._values["replication_user"] = replication_user
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def console_access(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables access to the ActiveMQ Web Console for the ActiveMQ user.

            Does not apply to RabbitMQ brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-consoleaccess
            '''
            result = self._values.get("console_access")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of groups (20 maximum) to which the ActiveMQ user belongs.

            This value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 2-100 characters long. Does not apply to RabbitMQ brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-groups
            '''
            result = self._values.get("groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''Required.

            The password of the user. This value must be at least 12 characters long, must contain at least 4 unique characters, and must not contain commas, colons, or equal signs (,:=).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replication_user(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Defines if this user is intended for CRDR replication purposes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-replicationuser
            '''
            result = self._values.get("replication_user")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The username of the broker user. The following restrictions apply to broker usernames:.

            - For Amazon MQ for ActiveMQ brokers, this value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 2-100 characters long.
            - For Amazon MQ for RabbitMQ brokers, this value can contain only alphanumeric characters, dashes, periods, underscores (- . _). This value must not contain a tilde (~) character. Amazon MQ prohibts using ``guest`` as a valid usename. This value must be 2-100 characters long.

            .. epigraph::

               Do not add personally identifiable information (PII) or other confidential or sensitive information in broker usernames. Broker usernames are accessible to other AWS services, including CloudWatch Logs . Broker usernames are not intended to be used for private or sensitive data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnConfigurationAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"broker": "broker", "configuration": "configuration"},
)
class CfnConfigurationAssociationMixinProps:
    def __init__(
        self,
        *,
        broker: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationAssociationPropsMixin.ConfigurationIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfigurationAssociationPropsMixin.

        :param broker: ID of the Broker that the configuration should be applied to.
        :param configuration: Returns information about all configurations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
            
            cfn_configuration_association_mixin_props = amazonmq_mixins.CfnConfigurationAssociationMixinProps(
                broker="broker",
                configuration=amazonmq_mixins.CfnConfigurationAssociationPropsMixin.ConfigurationIdProperty(
                    id="id",
                    revision=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39238448003be3ed9ed669957a72003028c4aeb9e2300069c54b22ef79b71e83)
            check_type(argname="argument broker", value=broker, expected_type=type_hints["broker"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if broker is not None:
            self._values["broker"] = broker
        if configuration is not None:
            self._values["configuration"] = configuration

    @builtins.property
    def broker(self) -> typing.Optional[builtins.str]:
        '''ID of the Broker that the configuration should be applied to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-broker
        '''
        result = self._values.get("broker")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationAssociationPropsMixin.ConfigurationIdProperty"]]:
        '''Returns information about all configurations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationAssociationPropsMixin.ConfigurationIdProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigurationAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnConfigurationAssociationPropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html
    :cloudformationResource: AWS::AmazonMQ::ConfigurationAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
        
        cfn_configuration_association_props_mixin = amazonmq_mixins.CfnConfigurationAssociationPropsMixin(amazonmq_mixins.CfnConfigurationAssociationMixinProps(
            broker="broker",
            configuration=amazonmq_mixins.CfnConfigurationAssociationPropsMixin.ConfigurationIdProperty(
                id="id",
                revision=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConfigurationAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AmazonMQ::ConfigurationAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aed119a9ab1832ac5c98cc0edb85999dd9b7e45461eb1ceff662095b96bf371)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e287b6ad923f39df9f2bd3846c11ebe1c7885f916b06ceefa361f75b5e6f949e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c187c7fbdbc1041a9fdb90c08ecad266cbf360281e3069ec8f62c608f8b27f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigurationAssociationMixinProps:
        return typing.cast(CfnConfigurationAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnConfigurationAssociationPropsMixin.ConfigurationIdProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "revision": "revision"},
    )
    class ConfigurationIdProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            revision: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A list of information about the configuration.

            :param id: Required. The unique ID that Amazon MQ generates for the configuration.
            :param revision: The revision number of the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
                
                configuration_id_property = amazonmq_mixins.CfnConfigurationAssociationPropsMixin.ConfigurationIdProperty(
                    id="id",
                    revision=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__923433cae0f448ba3d80ebb4be37a0b6102f72f2288f073aeaf4f50bc9b9e26f)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if revision is not None:
                self._values["revision"] = revision

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''Required.

            The unique ID that Amazon MQ generates for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html#cfn-amazonmq-configurationassociation-configurationid-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def revision(self) -> typing.Optional[jsii.Number]:
            '''The revision number of the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html#cfn-amazonmq-configurationassociation-configurationid-revision
            '''
            result = self._values.get("revision")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_strategy": "authenticationStrategy",
        "data": "data",
        "description": "description",
        "engine_type": "engineType",
        "engine_version": "engineVersion",
        "name": "name",
        "tags": "tags",
    },
)
class CfnConfigurationMixinProps:
    def __init__(
        self,
        *,
        authentication_strategy: typing.Optional[builtins.str] = None,
        data: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine_type: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnConfigurationPropsMixin.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfigurationPropsMixin.

        :param authentication_strategy: Optional. The authentication strategy associated with the configuration. The default is ``SIMPLE`` .
        :param data: Amazon MQ for Active MQ: The base64-encoded XML configuration. Amazon MQ for RabbitMQ: the base64-encoded Cuttlefish configuration.
        :param description: The description of the configuration.
        :param engine_type: Required. The type of broker engine. Currently, Amazon MQ supports ``ACTIVEMQ`` and ``RABBITMQ`` .
        :param engine_version: The broker engine version. Defaults to the latest available version for the specified broker engine type. For more information, see the `ActiveMQ version management <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/activemq-version-management.html>`_ and the `RabbitMQ version management <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/rabbitmq-version-management.html>`_ sections in the Amazon MQ Developer Guide.
        :param name: Required. The name of the configuration. This value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 1-150 characters long.
        :param tags: Create tags when creating the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
            
            cfn_configuration_mixin_props = amazonmq_mixins.CfnConfigurationMixinProps(
                authentication_strategy="authenticationStrategy",
                data="data",
                description="description",
                engine_type="engineType",
                engine_version="engineVersion",
                name="name",
                tags=[amazonmq_mixins.CfnConfigurationPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ced570116f98bc86c7bf6e21b68cc36d4d7b4dfdb48715e23c36ee0c489679)
            check_type(argname="argument authentication_strategy", value=authentication_strategy, expected_type=type_hints["authentication_strategy"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_strategy is not None:
            self._values["authentication_strategy"] = authentication_strategy
        if data is not None:
            self._values["data"] = data
        if description is not None:
            self._values["description"] = description
        if engine_type is not None:
            self._values["engine_type"] = engine_type
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def authentication_strategy(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The authentication strategy associated with the configuration. The default is ``SIMPLE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-authenticationstrategy
        '''
        result = self._values.get("authentication_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''Amazon MQ for Active MQ: The base64-encoded XML configuration.

        Amazon MQ for RabbitMQ: the base64-encoded Cuttlefish configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_type(self) -> typing.Optional[builtins.str]:
        '''Required.

        The type of broker engine. Currently, Amazon MQ supports ``ACTIVEMQ`` and ``RABBITMQ`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-enginetype
        '''
        result = self._values.get("engine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The broker engine version.

        Defaults to the latest available version for the specified broker engine type. For more information, see the `ActiveMQ version management <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/activemq-version-management.html>`_ and the `RabbitMQ version management <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/rabbitmq-version-management.html>`_ sections in the Amazon MQ Developer Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Required.

        The name of the configuration. This value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 1-150 characters long.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnConfigurationPropsMixin.TagsEntryProperty"]]:
        '''Create tags when creating the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnConfigurationPropsMixin.TagsEntryProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnConfigurationPropsMixin",
):
    '''Creates a new configuration for the specified configuration name.

    Amazon MQ uses the default configuration (the engine type and version).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html
    :cloudformationResource: AWS::AmazonMQ::Configuration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
        
        cfn_configuration_props_mixin = amazonmq_mixins.CfnConfigurationPropsMixin(amazonmq_mixins.CfnConfigurationMixinProps(
            authentication_strategy="authenticationStrategy",
            data="data",
            description="description",
            engine_type="engineType",
            engine_version="engineVersion",
            name="name",
            tags=[amazonmq_mixins.CfnConfigurationPropsMixin.TagsEntryProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AmazonMQ::Configuration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284716c64e176e9ec57b7a1001d5e87730e28c5214a951850315c4500d74305e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83e136ac7efc32f8af47f6046c931ccda8c7778132ab31a3628783fb2bf3ba2c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170041027856513bd14e7e257244a6fd85cc47febd79b5e38ba4c84204a15f8a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigurationMixinProps:
        return typing.cast(CfnConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amazonmq.mixins.CfnConfigurationPropsMixin.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The list of all tags associated with this configuration.

            :param key: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amazonmq import mixins as amazonmq_mixins
                
                tags_entry_property = amazonmq_mixins.CfnConfigurationPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1ee99904a09900ec49607fdce189b4c0429230fe9301cd22030aa31408e5d27)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html#cfn-amazonmq-configuration-tagsentry-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html#cfn-amazonmq-configuration-tagsentry-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnBrokerMixinProps",
    "CfnBrokerPropsMixin",
    "CfnConfigurationAssociationMixinProps",
    "CfnConfigurationAssociationPropsMixin",
    "CfnConfigurationMixinProps",
    "CfnConfigurationPropsMixin",
]

publication.publish()

def _typecheckingstub__3744e9b9b05cbbb4dbd88f7656df5524968ed9f1609bbff41dc95a4c28326977(
    *,
    authentication_strategy: typing.Optional[builtins.str] = None,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    broker_name: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrokerPropsMixin.ConfigurationIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_replication_mode: typing.Optional[builtins.str] = None,
    data_replication_primary_broker_arn: typing.Optional[builtins.str] = None,
    deployment_mode: typing.Optional[builtins.str] = None,
    encryption_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrokerPropsMixin.EncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    engine_type: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    host_instance_type: typing.Optional[builtins.str] = None,
    ldap_server_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrokerPropsMixin.LdapServerMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrokerPropsMixin.LogListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maintenance_window_start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrokerPropsMixin.MaintenanceWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_type: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnBrokerPropsMixin.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    users: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrokerPropsMixin.UserProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca4e4c5e9083c08ab055248254f4e1b6f44726adcc55756469cc83562847ab6(
    props: typing.Union[CfnBrokerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2376e80cc326b0bbf9aafd4825e6066fbed9b3806f67ef6ac5e635bbf92f053(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5435dc3f401ca81545b57afb6b8b372b13f4c15ab06d109feaad6f32e4ed7c56(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41d29191b8d9ec03c7fdb8b23faee624f01a848e6005d91de046037864ad192(
    *,
    id: typing.Optional[builtins.str] = None,
    revision: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8378fa45c38d2cb872348dd5b12964b5c9c97af36ba172e8e7350ce1f5fa8656(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
    use_aws_owned_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5feb908abe3e71a4efe29b6c62a30c6d7694cc2acc7c54196d233942927deab6(
    *,
    hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_base: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
    role_search_matching: typing.Optional[builtins.str] = None,
    role_search_subtree: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    service_account_password: typing.Optional[builtins.str] = None,
    service_account_username: typing.Optional[builtins.str] = None,
    user_base: typing.Optional[builtins.str] = None,
    user_role_name: typing.Optional[builtins.str] = None,
    user_search_matching: typing.Optional[builtins.str] = None,
    user_search_subtree: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cf7c1c5bd3ca0aced5933962000a0a620c8885895ded4eebb3d8d608b04205(
    *,
    audit: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    general: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78612699d0ec14d9b324663b5000d336c3a2e98c337949114a61f5408a0d98a1(
    *,
    day_of_week: typing.Optional[builtins.str] = None,
    time_of_day: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefaa53fb097a786b45ceaa314acedc095a8bff622e006004f506fad4843711f(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5181251bfc9fefd8e8cf2d778bd5422663788f1260b4bf0b4a1ec71b0a1d3281(
    *,
    console_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    password: typing.Optional[builtins.str] = None,
    replication_user: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39238448003be3ed9ed669957a72003028c4aeb9e2300069c54b22ef79b71e83(
    *,
    broker: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationAssociationPropsMixin.ConfigurationIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aed119a9ab1832ac5c98cc0edb85999dd9b7e45461eb1ceff662095b96bf371(
    props: typing.Union[CfnConfigurationAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e287b6ad923f39df9f2bd3846c11ebe1c7885f916b06ceefa361f75b5e6f949e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c187c7fbdbc1041a9fdb90c08ecad266cbf360281e3069ec8f62c608f8b27f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923433cae0f448ba3d80ebb4be37a0b6102f72f2288f073aeaf4f50bc9b9e26f(
    *,
    id: typing.Optional[builtins.str] = None,
    revision: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ced570116f98bc86c7bf6e21b68cc36d4d7b4dfdb48715e23c36ee0c489679(
    *,
    authentication_strategy: typing.Optional[builtins.str] = None,
    data: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine_type: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnConfigurationPropsMixin.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284716c64e176e9ec57b7a1001d5e87730e28c5214a951850315c4500d74305e(
    props: typing.Union[CfnConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e136ac7efc32f8af47f6046c931ccda8c7778132ab31a3628783fb2bf3ba2c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170041027856513bd14e7e257244a6fd85cc47febd79b5e38ba4c84204a15f8a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ee99904a09900ec49607fdce189b4c0429230fe9301cd22030aa31408e5d27(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
